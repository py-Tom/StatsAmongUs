import sqlite3

conn = sqlite3.connect("statistics.db")
c = conn.cursor()


def create_db():

    c.execute(
        """CREATE TABLE AmongStats (
                'UserName' text,
                'UploadDate' text,
                'Stats' text
            )"""
    )

    conn.commit()
    conn.close()
    return None


def new_entry(user, date, values):
    with conn:
        c.execute(
            f"INSERT INTO AmongStats VALUES (:UserName, :UploadDate, :Stats)",
            {"UserName": user, "UploadDate": date, "Stats": values},
        )
    return None


def update_entry(user, date, values):
    with conn:
        c.execute(
            f"UPDATE AmongStats SET UploadDate=:UploadDate, Stats=:Stats WHERE UserName=:UserName",
            {"UserName": user, "UploadDate": date, "Stats": values},
        )
    return None


def select_entry(user):
    c.execute(f"SELECT * FROM AmongStats WHERE UserName=:UserName", {"UserName": user})
    return c.fetchone()


def remove_entry(user):
    with conn:
        c.execute(
            f"DELETE from AmongStats WHERE UserName=:UserName", {"UserName": user}
        )
    return None


def select_table():
    c.execute(f"SELECT * FROM AmongStats")
    return c.fetchall()


if __name__ == "__main__":
    create_db()