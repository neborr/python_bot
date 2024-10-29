import sqlite3

def create_table(path, table_name, **fields):
    field_info = ''

    for key in fields:
        field_info += f'{key} {fields[key]}, '

    else:
        array = list(field_info)

        del array[-1]
        del array[-1]

        field_info = ''.join(array)

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}({field_info})""")

    conn.commit()
    conn.close()

def insert_into_table(path, table_name, **fields):
    keys = []
    values = []

    for key in fields:
        keys.append(key)
        values.append(fields[key])

    else:
        keys = tuple(map(str, keys))
        values = tuple(map(str, values))

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO {table_name}{keys} VALUES{values}""")

    conn.commit()
    conn.close()

def update_table(path, table_name, key, value, **where):
    where_key = list(where.keys())[0]
    where_value = list(where.values())[0]

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(f"""UPDATE {table_name} SET {key}='{value}' WHERE {where_key}='{where_value}'""")

    conn.commit()
    conn.close()

def get_from_table(path, table_name, **where):
    where_key = list(where.keys())[0]
    where_value = list(where.values())[0]

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM {table_name} WHERE {where_key}='{where_value}'""")

    data = cur.fetchone()

    conn.commit()
    conn.close()

    return data

def get_all_from_table(path, table_name):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM {table_name}""")

    data = cur.fetchall()

    conn.commit()
    conn.close()

    return data

def delete_from_table(path, table_name, **where):
    where_key = list(where.keys())[0]
    where_value = list(where.values())[0]

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM {table_name} WHERE {where_key}='{where_value}'""")

    conn.commit()
    conn.close()
