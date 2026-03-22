"""
bruteforce.py — Linear-scan baseline for performance comparison.
CS 432 Databases | Module A | CallHub
"""


class BruteForceDB:

    def __init__(self):
        self.records = []  

    def insert(self, key, value):
        for i, (k, _) in enumerate(self.records):
            if k == key:
                self.records[i] = (key, value)
                return
        self.records.append((key, value))

    def search(self, key):
        for k, v in self.records:
            if k == key: return v
        return None

    def delete(self, key):
        for i, (k, _) in enumerate(self.records):
            if k == key:
                self.records.pop(i)
                return True
        return False

    def range_query(self, start_key, end_key):
        return [(k, v) for k, v in self.records if start_key <= k <= end_key]

    def get_all(self):
        return sorted(self.records, key=lambda x: x[0])

    def count(self):   return len(self.records)
    def min_key(self): return min((k for k,_ in self.records), default=None)
    def max_key(self): return max((k for k,_ in self.records), default=None)
    def __repr__(self): return f"BruteForceDB({len(self.records)} records)"
