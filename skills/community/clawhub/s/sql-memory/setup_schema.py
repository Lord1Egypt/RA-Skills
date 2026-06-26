"""
setup_schema.py — Create the memory.* schema for clawbot-sql-memory

Run once before first use:
    python3 setup_schema.py              # uses 'local' profile
    python3 setup_schema.py --cloud      # uses 'cloud' profile

Requires .env with SQL credentials. See README.md for format.
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    from sql_connector import get_connector
except ImportError:
    print("ERROR: sql-connector not found. Install it first:")
    print("  clawhub install sql-connector")
    sys.exit(1)

SCHEMA_SQL = [
    ("CREATE SCHEMA memory", "memory schema"),

    ("""
    CREATE TABLE memory.Memories (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        category    NVARCHAR(100)  NOT NULL,
        [key]       NVARCHAR(255)  NOT NULL,
        content     NVARCHAR(MAX)  NOT NULL,
        importance  INT            DEFAULT 3,
        tags        NVARCHAR(500)  DEFAULT '',
        status      NVARCHAR(50)   DEFAULT 'active',
        created_at  DATETIME2      DEFAULT GETUTCDATE(),
        updated_at  DATETIME2      DEFAULT GETUTCDATE()
    )
    """, "memory.Memories"),

    ("""
    CREATE TABLE memory.TaskQueue (
        id           INT IDENTITY(1,1) PRIMARY KEY,
        agent        NVARCHAR(100)  NOT NULL,
        task_type    NVARCHAR(100)  NOT NULL,
        payload      NVARCHAR(MAX)  DEFAULT '',
        priority     INT            DEFAULT 5,
        status       NVARCHAR(50)   DEFAULT 'pending',
        retries      INT            DEFAULT 0,
        model_hint   NVARCHAR(100)  DEFAULT '',
        created_at   DATETIME2      DEFAULT GETUTCDATE(),
        updated_at   DATETIME2      DEFAULT GETUTCDATE(),
        claimed_at   DATETIME2      NULL,
        completed_at DATETIME2      NULL,
        error        NVARCHAR(MAX)  DEFAULT ''
    )
    """, "memory.TaskQueue"),

    ("""
    CREATE TABLE memory.ActivityLog (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        event_type  NVARCHAR(100)  NOT NULL,
        agent       NVARCHAR(100)  DEFAULT '',
        description NVARCHAR(MAX)  DEFAULT '',
        metadata    NVARCHAR(MAX)  DEFAULT '',
        importance  INT            DEFAULT 3,
        created_at  DATETIME2      DEFAULT GETUTCDATE()
    )
    """, "memory.ActivityLog"),

    ("""
    CREATE TABLE memory.Sessions (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        session_key NVARCHAR(255)  NOT NULL,
        agent       NVARCHAR(100)  DEFAULT '',
        status      NVARCHAR(50)   DEFAULT 'active',
        metadata    NVARCHAR(MAX)  DEFAULT '',
        started_at  DATETIME2      DEFAULT GETUTCDATE(),
        ended_at    DATETIME2      NULL
    )
    """, "memory.Sessions"),

    ("""
    CREATE TABLE memory.KnowledgeIndex (
        id         INT IDENTITY(1,1) PRIMARY KEY,
        domain     NVARCHAR(100)  NOT NULL,
        [key]      NVARCHAR(255)  NOT NULL,
        content    NVARCHAR(MAX)  NOT NULL,
        source     NVARCHAR(255)  DEFAULT '',
        tags       NVARCHAR(500)  DEFAULT '',
        created_at DATETIME2      DEFAULT GETUTCDATE()
    )
    """, "memory.KnowledgeIndex"),

    ("""
    CREATE TABLE memory.Todos (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        title       NVARCHAR(500)  NOT NULL,
        description NVARCHAR(MAX)  DEFAULT '',
        priority    INT            DEFAULT 3,
        status      NVARCHAR(50)   DEFAULT 'open',
        tags        NVARCHAR(500)  DEFAULT '',
        created_at  DATETIME2      DEFAULT GETUTCDATE(),
        updated_at  DATETIME2      DEFAULT GETUTCDATE(),
        closed_at   DATETIME2      NULL
    )
    """, "memory.Todos"),
]


def table_exists(db, table_name):
    schema, name = table_name.split('.')
    rows = db.query(
        "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
        (schema, name)
    )
    return len(rows) > 0


def schema_exists(db, schema_name):
    rows = db.query(
        "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
        (schema_name,)
    )
    return len(rows) > 0


def run(profile='local'):
    print(f"\nclawbot-sql-memory schema setup — profile: {profile}\n")
    db = get_connector(profile)

    if not db.ping():
        print("ERROR: Cannot connect to SQL Server. Check your .env credentials.")
        sys.exit(1)

    print("✅ Connected to SQL Server\n")

    for sql, label in SCHEMA_SQL:
        if label == "memory schema":
            if schema_exists(db, 'memory'):
                print(f"  SKIP  {label} (already exists)")
                continue
        else:
            if table_exists(db, label):
                print(f"  SKIP  {label} (already exists)")
                continue

        ok = db.execute(sql.strip())
        if ok:
            print(f"  CREATE {label}")
        else:
            print(f"  ERROR  {label} — check logs")

    print("\nSchema setup complete.\n")
    print("Next step: configure your .env and run:")
    print("  python3 -c \"from sql_memory import get_memory; print(get_memory('local').ping())\"")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create memory.* schema for clawbot-sql-memory')
    parser.add_argument('--cloud', action='store_true', help='Use cloud SQL profile')
    args = parser.parse_args()
    run('cloud' if args.cloud else 'local')
