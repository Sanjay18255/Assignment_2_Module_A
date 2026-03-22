"""
db_manager.py — DatabaseManager for CallHub.
CS 432 Databases | Module A

Follows exact boilerplate structure:
  self.databases = {db_name: {table_name: Table}}

Return convention (matches main.ipynb usage):
  create_database → (True, msg)  or  (False, msg)
  delete_database → (True, msg)  or  (False, msg)
  list_databases  → [db_name, ...]
  create_table    → (True, msg)  or  (False, msg)
  delete_table    → (True, msg)  or  (False, msg)
  list_tables     → ([table_names], msg)  or  (None, msg)
  get_table       → (Table, msg)          or  (None, msg)
"""

from .table import Table


class DatabaseManager:
    def __init__(self):
        self.databases = {} 

    def create_database(self, db_name):

        if db_name in self.databases:
            return False, f"Database '{db_name}' already exists"
        self.databases[db_name] = {}
        return True, f"Database '{db_name}' created successfully"

    def delete_database(self, db_name):

        if db_name not in self.databases:
            return False, f"Database '{db_name}' does not exist"
        del self.databases[db_name]
        return True, f"Database '{db_name}' deleted successfully"

    def list_databases(self):
        return list(self.databases.keys())

    def create_table(self, db_name, table_name, schema, order=8, search_key=None):
        if db_name not in self.databases:
            return False, f"Database '{db_name}' does not exist"
        if table_name in self.databases[db_name]:
            return False, f"Table '{table_name}' already exists in database '{db_name}'"

        self.databases[db_name][table_name] = Table(
            name=table_name,
            schema=schema,
            order=order,
            search_key=search_key
        )
        return True, f"Table '{table_name}' created successfully in database '{db_name}'"

    def delete_table(self, db_name, table_name):
        if db_name not in self.databases:
            return False, f"Database '{db_name}' does not exist"
        if table_name not in self.databases[db_name]:
            return False, f"Table '{table_name}' does not exist in database '{db_name}'"
        del self.databases[db_name][table_name]
        return True, f"Table '{table_name}' deleted from database '{db_name}'"

    def list_tables(self, db_name):
        if db_name not in self.databases:
            return None, f"Database '{db_name}' does not exist"
        return list(self.databases[db_name].keys()), "OK"

    def get_table(self, db_name, table_name):
        if db_name not in self.databases:
            return None, f"Database '{db_name}' does not exist"
        if table_name not in self.databases[db_name]:
            return None, f"Table '{table_name}' does not exist in database '{db_name}'"
        return self.databases[db_name][table_name], "OK"
