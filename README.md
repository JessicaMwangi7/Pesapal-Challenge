# Pesapal Junior Developer Challenge 2026
## Relational Database Management System (RDBMS)

This project is a simplified implementation of a relational database management system (RDBMS) built as part of the **Pesapal Junior Developer Challenge 2026**.

The goal of this challenge is not to build a production-ready database, but to demonstrate clear thinking, understanding of database fundamentals, and the ability to design and implement systems from first principles.

---

## What This Project Does

This project implements:

- A **custom in-memory RDBMS**
- Support for:
  - Table creation with schemas
  - CRUD operations (Create, Read, Update, Delete)
  - Primary key enforcement
  - Basic indexing
- A **SQL-like interactive REPL**
- A **Flask web application** that uses the RDBMS for real-world CRUD operations

No external database (MySQL, PostgreSQL, SQLite) is used.

---

## Project Structure
- `rdbms.py`: Core database engine
- `repl.py`: Interactive SQL-like interface
- `web_app/`: Flask web app using the custom RDBMS

---

## How the RDBMS Works

### Tables
Each table:
- Has a name and schema (column names and data types)
- Stores rows as Python dictionaries
- Supports insert, select, update, and delete operations

### Indexing
- Primary keys are indexed using a dictionary
- This allows faster lookups and uniqueness enforcement

### Data Types
Supported types:
- `int`
- `str`
- `float`

---

## Interactive REPL

The project includes a REPL (Read-Eval-Print Loop) that allows users to interact with the database using simple SQL-like commands.


### Run the REPL
```bash
python repl.py

##How to run
```bash
python app.py