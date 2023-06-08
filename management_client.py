import psycopg2

# # Вам необходимо разработать структуру БД для хранения информации и несколько функций на Python для управления данными.
# # # Функция, создающая структуру БД (таблицы).
def create_db(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        surname VARCHAR(200) NOT NULL,
        email VARCHAR(200) NOT NULL UNIQUE
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS phone_number(
        number VARCHAR(15) PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES client(id)
    );
    """)
# #
# # # Функция, позволяющая добавить нового клиента.
def add_client(conn, name, surname, email, number=None):
    conn.execute("""
    INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);
    """, (name, surname, email))
# #
# # # Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, number):
    conn.execute("""
    INSERT INTO phone_number(number, client_id) VALUES(%s, %s) RETURNING client_id;
    """, (number, client_id))
# #
# # # Функция, позволяющая изменить данные о клиенте.
def change_client(conn, id, name, surname, email, number=None):
    conn.execute("""
    UPDATE client SET name=%s, surname=%s, email=%s WHERE id=%s;
    """, (name, surname, email, id))
    conn.execute("""
    SELECT * FROM client;
    """)

# # Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id):
    conn.execute("""
    DELETE FROM phone_number WHERE client_id=%s;
    """, (client_id,))
    conn.execute("""
    SELECT * FROM phone_number;
    """)

# # Функция, позволяющая удалить существующего клиента.
def delete_client(conn, id):
    conn.execute("""
    DELETE FROM client WHERE id=%s;
    """, (id,))
    conn.execute("""
    SELECT * FROM client;
    """)
#
# # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, name=None, surname=None, email=None, number=None):
    def find_client_by_name(conn, name=None):
        conn.execute('''
        SELECT name FROM client
        JOIN phone_number ON client.id = phone_number.client_id
        WHERE name=%s;
        ''', (name))

    def find_client_by_surname(conn, surname=None):
        conn.execute('''
        SELECT surname FROM client
        JOIN phone_number ON client.id = phone_number.client_id
        WHERE name=%s;
        ''', (surname))

    def find_client_by_email(conn, email=None):
        conn.execute('''
        SELECT email FROM client
        JOIN phone_number ON client.id = phone_number.client_id
        WHERE email=%s;
        ''', (email))

    def find_client_by_number(conn, number=None):
        conn.execute('''
        SELECT number FROM phone_number
        JOIN client ON phone_number.client_id = client.id
        WHERE number=%s;
        ''', (number))

if __name__ == '__main__':
    with psycopg2.connect(database="client_management", user="postgres", password="...") as conn:
        with conn.cursor() as cur:
            # create_db(cur)
            # add_client(cur,'Имя', 'Фамилия', 'email@email.com', number=None)
            # add_phone(cur, 5, '8 999 999 99 99')
            # add_client(cur,'Имя_1', 'Фамилия_1', 'email_1@email.com', number=None)
            # add_phone(cur, 6, '8 777 777 77 77')
            # add_client(cur,'Имя_2', 'Фамилия_2', 'email_2@email.com', number=None)
            # add_phone(cur, 7, '8 888 888 88 88')
            # change_client(cur, 7, 'Имя_новое', 'Фамилия_новая', 'новый@email', number=None)
            # delete_phone(cur, 1)
            # delete_client(cur, 1)
            find_client(cur, number = '8 777 777 77 77')
conn.close()
