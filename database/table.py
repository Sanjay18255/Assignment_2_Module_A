"""
table.py — Table abstraction for CallHub, following instructor's boilerplate.
CS 432 Databases | Module A

Table(name, schema, order=8, search_key=None)
- schema : dict of {column_name: python_type}  e.g. {'member_id': int, 'name': str}
- search_key : which column is the B+ Tree index key

Return convention (matching boilerplate usage in main.ipynb):
  insert  → (True, key)      or  (False, error_msg)
  get     → record_dict      or  None
  update  → (True, msg)      or  (False, msg)
  delete  → (True, msg)      or  (False, msg)
  get_all → [(key, record), ...]
  range_query → [(key, record), ...]
"""

from .bplustree import BPlusTree

TYPE_MAP = {
    'int':   int,
    'str':   str,
    'float': float,
    'bool':  bool,
    int:     int,
    str:     str,
    float:   float,
    bool:    bool,
}


class Table:
    def __init__(self, name, schema, order=8, search_key=None):
        self.name       = name        
        self.schema     = schema      
        self.order      = order      
        self.data       = BPlusTree(order=order)   
        self.search_key = search_key  

        if self.search_key is None and schema:
            self.search_key = next(iter(schema))

    def validate_record(self, record):
        for col, expected_type in self.schema.items():
            if col not in record:
                return False, f"Missing required field: '{col}'"
            val = record[col]
            if val is None:
                continue  
            actual_type = TYPE_MAP.get(expected_type, expected_type)
            if not isinstance(val, actual_type):
                try:
                    actual_type(val)
                except (TypeError, ValueError):
                    return False, (
                        f"Field '{col}' expects {actual_type.__name__}, "
                        f"got {type(val).__name__}"
                    )
        return True, None

    def insert(self, record):
        valid, err = self.validate_record(record)
        if not valid:
            return False, err

        if self.search_key not in record:
            return False, f"Search key '{self.search_key}' not found in record"

        key = record[self.search_key]
        self.data.insert(key, record)
        return True, key

    def get(self, record_id):
        return self.data.search(record_id)

    def get_all(self):
        return self.data.get_all()

    def update(self, record_id, new_record):
        existing = self.data.search(record_id)
        if existing is None:
            return False, f"Record with id '{record_id}' not found"

        updated = dict(existing)
        updated.update(new_record)

        updated[self.search_key] = record_id

        valid, err = self.validate_record(updated)
        if not valid:
            return False, err

        self.data.update(record_id, updated)
        return True, "Record updated successfully"

    def delete(self, record_id):
        result = self.data.delete(record_id)
        if result:
            return True, "Record deleted"
        return False, f"Record with id '{record_id}' not found"

    def range_query(self, start_value, end_value):
        return self.data.range_query(start_value, end_value)

    def search_by_field(self, field, value):
        return [(k, v) for k, v in self.data.get_all() if v.get(field) == value]

    def count(self):
        return self.data.count()

    def tree_height(self):
        return self.data.height()

    def __repr__(self):
        return (f"Table(name='{self.name}', "
                f"search_key='{self.search_key}', "
                f"records={self.count()}, "
                f"order={self.order})")
