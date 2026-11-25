"""Generate a mock auditee-local database to walk through the audit loop.

In a real engagement this file is not part of the delivery package — the
auditee's database lives on the auditee's machine and the audit script reads
it locally.

Usage:
    python prepare_sample_db.py [output_path]
"""

import sqlite3
import sys
from pathlib import Path


ROWS = [
    ("2026-01-05", "1001", 128000.00, "Hangzhou Yunshan Tech", "INV-2026-0011"),
    ("2026-01-09", "1001", 96000.00, "Suzhou Mingyuan Trading", "INV-2026-0012"),
    ("2026-01-15", "2001", -3200.00, "refund reversal", "INV-2026-0013"),
    ("2026-01-18", "2001", 45000.00, "Ningbo Hengxin Logistics", "INV-2026-0013"),
    ("2026-02-02", "1001", 210000.00, "Hangzhou Yunshan Tech", ""),
    ("2026-02-11", "3001", 78000.00, "Shanghai Lingang Supply Chain", "INV-2026-0021"),
    ("2026-02-20", "3001", 156000.00, "Shanghai Lingang Supply Chain", "INV-2026-0022"),
    ("2026-03-03", "1001", 64000.00, "Suzhou Mingyuan Trading", ""),
]


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "sample_ledger.db")
    out.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(out)
    con.executescript(
        """
        DROP TABLE IF EXISTS ledger;
        CREATE TABLE ledger (
            id           INTEGER PRIMARY KEY,
            entry_date   TEXT    NOT NULL,
            account      TEXT    NOT NULL,
            amount       REAL    NOT NULL,
            counterparty TEXT,
            invoice_no   TEXT
        );
        """
    )
    con.executemany(
        "INSERT INTO ledger (entry_date, account, amount, counterparty, invoice_no)"
        " VALUES (?, ?, ?, ?, ?)",
        ROWS,
    )
    con.commit()
    con.close()
    print(f"sample db written: {out.resolve()} ({len(ROWS)} rows)")


if __name__ == "__main__":
    main()
