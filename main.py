import psycopg2


class Mybd:
    def __init__(self):
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
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
                    phone VARCHAR(20) NOT NULL UNIQUE
                    );
                    ''')
            conn.commit()

    def add_client(self):
        c_name = input('Введите имя:')
        c_lastname = input('Введите фамилию:')
        c_email = input('Введите e-mail:')
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO clients(c_name, c_lastname, c_email)
                    VALUES(%s, %s, %s);
                    ''', (c_name, c_lastname, c_email))
            conn.commit()

    def add_client_phone(self):
        c_name = input('Введите имя клиента:')
        c_lastname = input('Введите фамилию:')
        c_phone = input('Введите номер телефона:')
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO c_phones(client_id, phone) 
                    VALUES((SELECT client_id FROM clients WHERE c_name = %s AND c_lastname = %s), %s);
                    ''', (c_name, c_lastname, c_phone))
            conn.commit()

    def modify_client(self):
        c_name = input('Введите имя клиента:')
        c_lastname = input('Введите фамилию клиента:')
        c_email = input('Введите e-mail:')
        new_c_name = input('Введите новое имя клиента:')
        new_c_lastname = input('Введите новую фамилию:')
        new_c_email = input('Введите новый e-mail:')
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                           UPDATE clients
                           SET c_name = %s, c_lastname = %s, c_email = %s
                           WHERE c_name = %s AND c_lastname = %s AND c_email = %s;
                           ''', (new_c_name, new_c_lastname, new_c_email, c_name, c_lastname, c_email))
            conn.commit()

    def del_c_phone(self):
        c_name = input('Введите имя клиента:')
        c_lastname = input('Введите фамилию:')
        c_phone = int(input('Введите номер телефона:'))
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    DELETE FROM c_phones 
                    WHERE client_id = (SELECT client_id FROM clients
                        WHERE c_name = %s AND c_lastname = %s) AND c_phone = %s;
                    ''', (c_name, c_lastname, c_phone))
            conn.commit()

    def del_client(self):
        c_name = input('Введите имя клиента:')
        c_lastname = input('Введите фамилию:')
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    DELETE FROM c_phones 
                    WHERE client_id = (SELECT client_id FROM clients
                        WHERE c_name = %s AND c_lastname = %s);
                    ''' % (c_name, c_lastname))
                cur.execute('''
                    DELETE FROM clients
                    WHERE c_name = %s AND c_lastname = %s;
                    ''' % (c_name, c_lastname))
            conn.commit()

    def find_client(self):
        text = input('Введите имя, фамилию, e-mail или номер телефона')
        text = '%' + text + '%'
        with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT c_name, c_lastname, c_email FROM clients cl
                    LEFT JOIN c_phones cp ON cl.client_id = cp.client_id 
                    WHERE c_name LIKE %s
                    OR c_lastname LIKE %s
                    OR c_email LIKE %s
                    OR phone LIKE %s;
                    ''', (text, text, text, text))
                print(cur.fetchall())


if __name__ == '__main__':
    cl_bd = Mybd()
    while True:
        command = input('''Введите команду:
        ac - добавить клиента;
        acp - добавить номер телефона клиенту;
        mc - изменить запись о клиенте;
        dcp - удалить запись телефона клиента;
        dc - удалить запись о клиенте;
        fc - найти клиента.
        ''')
        if command == 'ac':
            cl_bd.add_client()
        elif command == 'acp':
            cl_bd.add_client_phone()
        elif command == 'mc':
            cl_bd.modify_client()
        elif command == 'dcp':
            cl_bd.del_c_phone()
        elif command == 'dc':
            cl_bd.del_client()
        elif command == 'fc':
            cl_bd.find_client()
        else:
            print('Неправильная команда')
