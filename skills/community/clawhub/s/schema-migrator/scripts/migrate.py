# -*- coding: utf-8 -*-
import sqlite3
import os
import json
from datetime import datetime

RECOMMENDATION_PATH = "/root/.schema/recommendation.json"
DB_PATH = "/var/db/app.db"
MIGRATIONS_TABLE = "_migrations"


def is_valid_index_name(name):
    if not isinstance(name, str):
        return False
    if not name.startswith("idx_"):
        return False
    return all(c.isalnum() or c == '_' for c in name)


def run(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    executed = []
    errors = []

    if not os.path.exists(RECOMMENDATION_PATH):
        return {
            "execution_timestamp": datetime.utcnow().isoformat(),
            "migrations_executed": executed,
            "errors": errors,
            "status": "completed",
        }

    with open(RECOMMENDATION_PATH) as f:
        try:
            rec = json.load(f)
        except json.JSONDecodeError:
            return {
                "execution_timestamp": datetime.utcnow().isoformat(),
                "migrations_executed": executed,
                "errors": [{"error": "invalid recommendation file"}],
                "status": "completed",
            }

    indexes_to_drop = rec.get("indexes_to_drop", [])
    for idx_name in indexes_to_drop:
        if not is_valid_index_name(idx_name):
            errors.append({"index": idx_name, "error": "invalid index name"})
            continue
        try:
            cur.execute("DROP INDEX IF EXISTS [{}]".format(idx_name))
            conn.commit()
            executed.append(idx_name)
        except Exception as e:
            errors.append({"index": idx_name, "error": str(e)})
            conn.rollback()

    return {
        "execution_timestamp": datetime.utcnow().isoformat(),
        "migrations_executed": executed,
        "errors": errors,
        "status": "completed" if not errors else "completed_with_errors",
    }


if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
    result = run(db_path)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
