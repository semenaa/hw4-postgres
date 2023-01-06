import psycopg2
from psycopg2.sql import SQL, Identifier


def create_tables():
    with conn.cursor() as cur:
        cur.execute('''
            DROP TABLE IF EXISTS c_phones;
            DROP TABLE IF EXISTS clients;
            CREATE TABLE clients (
                client_id SERIAL PRIMARY KEY,
                c_name VARCHAR(25),
                c_lastname VARCHAR(30),
                c_email VARCHAR(30)
            );
            CREATE TABLE c_phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(client_id),
                c_phone VARCHAR(20) NOT NULL UNIQUE
            );
            ''')
    conn.commit()


def add_client(c_name, c_lastname, c_email):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO clients(c_name, c_lastname, c_email)
            VALUES(%s, %s, %s);
            ''', (c_name, c_lastname, c_email))
    conn.commit()


def add_client_phone(client_id, c_phone):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO c_phones(client_id, c_phone) 
            VALUES(%s, %s);
            ''', (client_id, c_phone))
    conn.commit()


def modify_client(client_id, c_name=None, c_lastname=None, c_email=None):
    with conn.cursor() as cur:
        for name, field in {'c_name': c_name, 'c_lastname': c_lastname, 'c_email': c_email}.items():
            if field is not None:
                cur.execute(SQL('''
                            UPDATE clients
                            SET {} = %s
                            WHERE client_id = %s;
                            ''').format(Identifier(name)), (field, client_id))
    conn.commit()


def del_c_phone(client_id, c_phone):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM c_phones 
            WHERE client_id = %s AND c_phone = %s;
            ''', (client_id, c_phone))
    conn.commit()


def del_client(client_id):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM c_phones 
            WHERE client_id = %s;
            ''', (client_id,))
        cur.execute('''
            DELETE FROM clients
            WHERE client_id = %s;
            ''', (client_id,))
    conn.commit()


def enrich(stringgg):
    if stringgg is not None:
        stringgg = '%' + stringgg + '%'
    return stringgg


def find_client(c_name=None, c_lastname=None, c_email=None, c_phone=None):
    c_name = enrich(c_name)
    c_lastname = enrich(c_lastname)
    c_email = enrich(c_email)
    c_phone = enrich(c_phone)
    with conn.cursor() as cur:
        cur.execute('''
            SELECT c_name, c_lastname, c_email FROM clients cl
            LEFT JOIN c_phones cp ON cl.client_id = cp.client_id 
            WHERE c_name LIKE %s
            OR c_lastname LIKE %s
            OR c_email LIKE %s
            OR c_phone LIKE %s;
            ''', (c_name, c_lastname, c_email, c_phone))
        result = cur.fetchall()
        if result != []:
            print(result)
        else:
            print('No such row')


if __name__ == '__main__':
    with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
        create_tables()
        add_client('Sergei', 'Smirnov', 'ssmirnov@mail.ru')
        add_client('Andrei', 'Zakharov', 'azakharov@gmail.ru')
        add_client('Tupac', 'Shakur', '2pac@yahoo.com')
        add_client_phone(1, '123456789')
        add_client_phone(1, '987654321')
        modify_client(2, c_name='Ondrei')
        del_c_phone(1, '123456789')
        del_client(2)
        find_client(c_lastname='Smirnov')
        find_client(c_phone='987654321')
        find_client(c_email='2pac')
        find_client(c_name='Ond')
