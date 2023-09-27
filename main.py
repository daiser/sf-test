import argparse

from database import Database
from domain_tree import Root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database",
                        type=str, help="Sqlite3 database file")
    parser.add_argument("-k", "--keep-rules",
                        action="store_true")
    args = parser.parse_args()

    with Database(args.database) as db:
        for project_id in db.projects:
            if not args.keep_rules:
                db.clear_rules(project_id)

            project_root = Root()
            for domain in db.domains(project_id):
                project_root.add(domain)

            for domain_group in project_root.compact_tree():
                rule_rx = (r".+\."
                           + domain_group.replace(".",
                                                  r"\."))
                db.add_rule(project_id, rule_rx)

            db.commit()


if __name__ == '__main__':
    main()
