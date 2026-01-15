# rdbms.py

class Table:
    def __init__(self, name, columns, primary_key=None, unique_keys=None):
        """
        name: table name
        columns: dict {column_name: type_name as string} e.g. {"id": "int", "name": "str"}
        primary_key: column name
        unique_keys: list of column names
        """
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique_keys = unique_keys or []

        self.rows = []
        self.index = {}

    def _cast_type(self, value, type_name):
        """Convert string value to the correct type based on type_name"""
        if type_name == "int":
            return int(value)
        elif type_name == "str":
            return str(value)
        elif type_name == "float":
            return float(value)
        else:
            raise ValueError(f"Unsupported type: {type_name}")

    def insert(self, row):
        # Validate columns and types
        for col, type_name in self.columns.items():
            if col not in row:
                raise ValueError(f"Missing column: {col}")
            row[col] = self._cast_type(row[col], type_name)

        # Primary key enforcement
        if self.primary_key:
            pk = row[self.primary_key]
            if pk in self.index:
                raise ValueError("Duplicate primary key")
            self.index[pk] = row

        # Unique key enforcement
        for key in self.unique_keys:
            for existing in self.rows:
                if existing[key] == row[key]:
                    raise ValueError(f"Duplicate value for unique key: {key}")

        self.rows.append(row)

    def select(self, criteria=None):
        if not criteria:
            return self.rows
        return [
            row for row in self.rows
            if all(row.get(k) == self._cast_type(v, self.columns[k]) for k, v in criteria.items())
        ]

    def update(self, criteria, updates):
        count = 0
        for row in self.rows:
            if all(row.get(k) == self._cast_type(v, self.columns[k]) for k, v in criteria.items()):
                for key, value in updates.items():
                    if key in self.columns:
                        row[key] = self._cast_type(value, self.columns[key])
                count += 1
        return count

    def delete(self, criteria):
        original = len(self.rows)
        self.rows = [
            row for row in self.rows
            if not all(row.get(k) == self._cast_type(v, self.columns[k]) for k, v in criteria.items())
        ]
        return original - len(self.rows)


class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns, primary_key=None, unique_keys=None):
        self.tables[name] = Table(name, columns, primary_key, unique_keys)

    def get_table(self, name):
        if name not in self.tables:
            raise KeyError(f"Table '{name}' does not exist")
        return self.tables[name]

    def join(self, table1, table2, key1, key2):
        t1 = self.get_table(table1)
        t2 = self.get_table(table2)
        results = []
        for r1 in t1.rows:
            for r2 in t2.rows:
                if r1[key1] == r2[key2]:
                    results.append({**r1, **r2})
        return results
