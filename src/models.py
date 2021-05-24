import sqlite3
import hashlib


def create_connection():
    connection = sqlite3.connect("resurses/pizza_db.db")

    return connection


def close_connection(connection):
    connection.close()


def select_pizza(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM pizza_table
        """
    )
    results = cursor.fetchall()
    dict_results = {}
    for _id, name, price, description, image in results:
        dict_results[_id]={
            "name": name,
            "price": price,
            "description": description,
            "image": image
        }
    return dict_results


def select_order(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM zakaz_table
        """
    )
    results = cursor.fetchall()
    dict_results = {}
    for _id, name, pizza_description, description, price, status in results:
        dict_results[_id]={
            "name": name,
            "pizza_description": pizza_description,
            "description": description,
            "price": price,
            "status": status
        }
    return dict_results


def select_ingr(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM ingr_table
        """
    )
    results = cursor.fetchall()
    dict_results = {}
    for _id, name, price in results:
        dict_results[_id]={
            "name": name,
            "price": price,
        }
    return dict_results


def select_ingr_change(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM ingr_table
        """
    )
    results = cursor.fetchall()
    return results


def select_pizza_by_id(connection, pizza_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * from pizza_table
        WHERE id=?
        """,
        (pizza_id, )
    )
    resulte = cursor.fetchone()
    _id = resulte[0]
    name = resulte[1]
    price = resulte[2]
    description = resulte[3]
    image = resulte[4]

    return {
        "pizza_id": _id,
        "name": name,
        "price": price,
        "description": description,
        "image": image
    }


def select_order_by_id(connection, order_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * from zakaz_table
        WHERE id=?
        """,
        (order_id, )
    )
    resulte = cursor.fetchone()
    _id = resulte[0]
    name = resulte[1]
    pizza_description = resulte[2]
    description = resulte[3]
    price = resulte[4]
    status = resulte[5]


    return {
        "order_id": _id,
        "name": name,
        "pizza_description": pizza_description,
        "description": description,
        "price": price,
        "status": status
    }


def select_order_by_last_id(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM zakaz_table WHERE id=( SELECT MAX(id) from zakaz_table )
        """,
    )
    resulte = cursor.fetchone()
    _id = resulte[0]
    name = resulte[1]
    pizza_description = resulte[2]
    description = resulte[3]
    price = resulte[4]
    status = resulte[5]

    return {
        "order_id": _id,
        "name": name,
        "pizza_description": pizza_description,
        "description": description,
        "price": price,
        "status": status
    }


def select_pizza_by_id_zakaz(connection, pizza_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT pizza_description FROM pizza_table WHERE id=?
        """,
        (pizza_id, )
    )
    results = cursor.fetchone()
    return results


def insert_new_order(connection, pizza_name_zakaz, pizza_description, ingr_name_zakaz, price_zakaz):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO zakaz_table(pizza_name_zakaz, pizza_description, ingr_name_zakaz, price_zakaz)
        VALUES (?, ?, ?, ?)
        """,
        (pizza_name_zakaz, pizza_description, ingr_name_zakaz, price_zakaz)
    )
    connection.commit()


def insert_pizza(connection, pizza_name, pizza_price, pizza_description, pizza_image):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO pizza_table(pizza_name, pizza_price, pizza_description, pizza_image)
        VALUES (?, ?, ?, ?)
        """,
        (pizza_name, pizza_price, pizza_description, pizza_image)
    )
    connection.commit()


def insert_ingr(connection, ingr_name, ingr_price):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO ingr_table(ingr_name, ingr_price)
        VALUES (?, ?)
        """,
        (ingr_name, ingr_price)
    )
    connection.commit()


def update_pizza(connection, pizza_name, pizza_price, pizza_description, pizza_image, pizza_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE pizza_table SET pizza_name=?, pizza_price=?, pizza_description=?, pizza_image=? WHERE id=?
        """,
        (pizza_name, pizza_price, pizza_description, pizza_image, pizza_id)
    )
    connection.commit()


def update_ingr(connection, ingr_name, ingr_price, ingr_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE ingr_table SET ingr_name=?, ingr_price=? WHERE id=?
        """,
        (ingr_name, ingr_price, ingr_id)
    )
    connection.commit()


def delete_pizza_by_id(connection, pizza_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM pizza_table
        WHERE id=?
        """,
        (pizza_id, )
    )
    connection.commit()


def change_status_by_id(connection, order_id):
    cursor = connection.cursor()
    cursor.execute(
        """    
        UPDATE zakaz_table SET status_zakaz=? WHERE id=?
        """,
        ("COOKED", order_id)

    )
    connection.commit()


def change_status_by_id_return(connection, order_id):
    cursor = connection.cursor()
    cursor.execute(
        """    
        UPDATE zakaz_table SET status_zakaz=? WHERE id=?
        """,
        ("BAKED", order_id)

    )
    connection.commit()


def delete_ingr_by_id(connection, ingr_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM ingr_table WHERE id=?
        """,
        (ingr_id, )
    )
    connection.commit()


def delete_order_by_id(connection, order_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM zakaz_table WHERE id=?
        """,
        (order_id, )
    )
    connection.commit()


def authoriz(connection, name):
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT password FROM users WHERE name=?
        ''',
        (name, )
    )
    results = cursor.fetchall()
    return results


def init_db():
    with sqlite3.connect("resurses/pizza_db.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            )
            '''
        )


        cursor.execute(
            '''
            INSERT INTO users(name, password)
            VALUES(?,?)
            ''',
            ("povar", hashlib.md5(("Qwerty").encode('utf-8')).hexdigest())
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pizza_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pizza_name VARCHAR(100) UNIQUE NOT NULL,
            pizza_price INTEGER NOT NULL,
            pizza_description TEXT NOT NULL,
            pizza_image TEXT NOT NULL
            )
            """
        )


        cursor.executemany(
            """
            INSERT INTO pizza_table(pizza_name, pizza_price, pizza_description, pizza_image)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Fodgy", 62, "dough", "static/fodgy.jpg"),
                ("Neapoletano", 70, "dough", "static/neapolitano.jpg"),
                ("Cheese", 75, "dough", "static/cheese.jpg"),
                ("Salami", 65, "dough", "static/salami.jpg"),
                ("Marinara", 60, "dough", "static/marinara.jpg")
            ]
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ingr_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingr_name VARCHAR(100) UNIQUE NOT NULL,
            ingr_price INTEGER NOT NULL
            )
            """
        )


        cursor.executemany(
            """
            INSERT INTO ingr_table(ingr_name, ingr_price)
            VALUES (?, ?)
            """,
            [
                ("double cheese", 6),
                ("mushrooms", 4),
                ("black olives", 8),
                ("salami", 7),
                ("tomatoes", 4),
                ("raw smoked meat", 9),
                ("bacon", 8),
                ("corn", 3),
                ("bavarian sausages", 8),
                ("pineapple", 5)
            ]

        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS zakaz_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pizza_name_zakaz TEXT NOT NULL,
            pizza_description TEXT NOT NULL,
            ingr_name_zakaz TEXT NOT NULL,
            price_zakaz TEXT NOT NULL,
            status_zakaz TEXT NOT NULL DEFAULT "BAKED"
            )
            """
        )


if __name__ == "__main__":
    init_db()
