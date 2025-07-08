import sqlite3


def create_table():
    connection = sqlite3.connect("eurobike.db")
    cursor = connection.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                description TEXT,
                country TEXT,
                website TEXT,
                email TEXT,
                phone TEXT
            )
        """
    )
    connection.commit()
    connection.close()


def insert_participant(participant):
    connection = sqlite3.connect("eurobike.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO participants (company_name, description, country, website, email, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            participant["company_name"],
            participant["description"],
            participant["country"],
            participant["website"],
            participant["email"],
            participant["phone"]
        )
    )
    connection.commit()
    connection.close()
