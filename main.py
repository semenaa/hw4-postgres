import psycopg2


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
                phone VARCHAR(20) NOT NULL UNIQUE
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
            INSERT INTO c_phones(client_id, phone) 
            VALUES(%s, %s);
            ''', (client_id, c_phone))
    conn.commit()


def modify_client(client_id, c_name=None, c_lastname=None, c_email=None):
    with conn.cursor() as cur:
        for field in [c_name, c_lastname, c_email]:
            if field is not None:
                cur.execute('''
                            UPDATE clients
                            SET  = %s
                            WHERE client_id = %s;
                            ''', (field, client_id))
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


def find_client(c_name=None, c_lastname=None, c_email=None, c_phone=None):
    for field in [c_name, c_lastname, c_email, c_phone]:
        if field is None:
            field = '%%'
        else:
            field = '%' + field + '%'
    with conn.cursor() as cur:
        cur.execute('''
            SELECT c_name, c_lastname, c_email FROM clients cl
            LEFT JOIN c_phones cp ON cl.client_id = cp.client_id 
            WHERE c_name LIKE %s
            OR c_lastname LIKE %s
            OR c_email LIKE %s
            OR phone LIKE %s;
            ''', (c_name, c_lastname, c_email, c_phone))
        print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="cl_db", user="postgres", password="123") as conn:
        create_tables()
        add_client('Sergei', 'Smirnov', 'ssmirnov@mail.ru')
        add_client('Andrei', 'Zakharov', 'azakharov@mail.ru')
        add_client_phone(1, '123456789')
        add_client_phone(1, '987654321')
        modify_client(2, )
        del_c_phone(1, '123456789')
        del_client(2)
        find_client(c_lastname='Smirnov')
        find_client(c_phone='987654321')
        