import sys
import mariadb
from dataclasses import dataclass
from typing import List


@dataclass()
class Conf:
    user: str
    password: str
    host: str
    port: int
    database: str

    def __init__(self,
                 user="root",
                 password="example",
                 host="host.docker.internal",
                 port=3306,
                 database="verhalenbank_omeka"):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    @staticmethod
    def get_connection() -> mariadb.connection:
        # Connect to MariaDB
        try:
            conn: mariadb.connection = mariadb.connect(
                user="root",
                password="example",
                host="host.docker.internal",
                port=3306,
                database="verhalenbank_omeka"
            )
            print('db connected. ok!')
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
