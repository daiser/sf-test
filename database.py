import sqlite3
import typing


class Database:
    def __init__(self, file: str):
        self.__connection = sqlite3.connect(file)

    def close(self):
        self.__connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def projects(self) -> typing.Generator[str, None, None]:
        cur = self.__connection.cursor()
        cur.execute("select distinct project_id from domains;")
        yield from (row[0] for row in cur)

    def domains(self, project_id: str) -> typing.Generator[str, None, None]:
        cur = self.__connection.cursor()
        cur.execute("select name from domains where project_id = ?",
                    (project_id,))
        yield from (row[0] for row in cur)

    def clear_rules(self, project_id: str):
        cur = self.__connection.cursor()
        cur.execute("delete from rules where project_id = ?",
                    (project_id,))

    def add_rule(self, project_id: str, rx: str):
        cur = self.__connection.cursor()
        cur.execute("insert into rules(project_id, regexp) values(?,?)",
                    (project_id, rx))

    def commit(self):
        self.__connection.commit()
