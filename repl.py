# repl.py

import json
from rdbms import Database

db = Database()

print("RDBMS REPL. Type 'exit' to quit.")
print("commands:")
print("create_table users {\"id\":\"int\", \"name\":\"str\", \"email\":\"str\"}")
print("insert users {\"id\":1,\"name\":\"Jessica\",\"email\":\"jessica@mail.com\"}")
print("select users {\"id\":1}")
print("update users {\"id\":1} {\"name\":\"Jessica Updated\"}")
print("delete users {\"id\":1}")

while True:
    cmd = input(">>> ").strip()
    if cmd.lower() == "exit":
        break

    try:
        # split command into action, table name, and rest
        parts = cmd.split(maxsplit=2)
        action = parts[0].lower()

        if action == "create_table":
            table_name, columns_json = parts[1], parts[2]
            columns = json.loads(columns_json)
            db.create_table(table_name, columns)
            print(f"Table '{table_name}' created.")

        elif action == "insert":
            table_name, row_json = parts[1], parts[2]
            row = json.loads(row_json)
            table = db.get_table(table_name)
            table.insert(row)
            print("Row inserted.")

        elif action == "select":
            table_name = parts[1]
            criteria = json.loads(parts[2]) if len(parts) > 2 else None
            table = db.get_table(table_name)
            results = table.select(criteria)
            print(results)

        elif action == "update":
            table_name, rest = parts[1], parts[2]
            # Split into criteria JSON and updates JSON correctly
            split_index = rest.find("}") + 1  # end of first JSON
            criteria_json = rest[:split_index]
            updates_json = rest[split_index:].strip()
            updates_json = updates_json if updates_json.startswith("{") else updates_json[1:]
            
            criteria = json.loads(criteria_json)
            updates = json.loads(updates_json)
            
            table = db.get_table(table_name)
            count = table.update(criteria, updates)
            print(f"{count} row(s) updated.")

        elif action == "delete":
            table_name, criteria_json = parts[1], parts[2]
            criteria = json.loads(criteria_json)
            table = db.get_table(table_name)
            count = table.delete(criteria)
            print(f"{count} row(s) deleted.")

        else:
            print("Unknown command.")

    except Exception as e:
        print("Error:", e)
