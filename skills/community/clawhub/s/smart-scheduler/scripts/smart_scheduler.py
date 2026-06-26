import argparse
import json
import sqlite3
from pathlib import Path


def runtime_dir(base_dir):
    path = Path(base_dir) / ".runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path(base_dir):
    return runtime_dir(base_dir) / "smart-scheduler.db"


def get_connection(base_dir):
    connection = sqlite3.connect(db_path(base_dir))
    connection.row_factory = sqlite3.Row
    ensure_schema(connection)
    return connection


def ensure_schema(connection):
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organizer TEXT NOT NULL,
            timezone TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            location TEXT,
            status TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            channel TEXT NOT NULL,
            contact TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(request_id) REFERENCES requests(id)
        );
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            proposed_start TEXT NOT NULL,
            proposed_end TEXT NOT NULL,
            source TEXT,
            note TEXT,
            status TEXT DEFAULT 'proposed',
            FOREIGN KEY(request_id) REFERENCES requests(id)
        );
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL UNIQUE,
            proposal_id INTEGER NOT NULL,
            chosen_start TEXT NOT NULL,
            chosen_end TEXT NOT NULL,
            confirmed_by TEXT NOT NULL,
            ics_path TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(request_id) REFERENCES requests(id),
            FOREIGN KEY(proposal_id) REFERENCES proposals(id)
        );
        """
    )
    connection.commit()


def now_iso():
    from datetime import datetime

    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def parse_participant(raw_value):
    parts = [part.strip() for part in raw_value.split("|")]
    if len(parts) != 3:
        raise ValueError("participant values must use name|channel|contact")
    return {"name": parts[0], "channel": parts[1], "contact": parts[2]}


def parse_slot(raw_value):
    parts = [part.strip() for part in raw_value.split("|")]
    if len(parts) != 2:
        raise ValueError("slot values must use start|end")
    return {"start": parts[0], "end": parts[1]}


def create_request(args):
    timestamp = now_iso()
    participants = [parse_participant(item) for item in args.participant]
    with get_connection(args.base_dir) as connection:
        cursor = connection.execute(
            """
            INSERT INTO requests
                (title, organizer, timezone, duration_minutes, location, status, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'open', ?, ?, ?)
            """,
            (
                args.title,
                args.organizer,
                args.timezone,
                args.duration_minutes,
                args.location,
                args.notes,
                timestamp,
                timestamp,
            ),
        )
        request_id = cursor.lastrowid
        for participant in participants:
            connection.execute(
                """
                INSERT INTO participants (request_id, name, channel, contact)
                VALUES (?, ?, ?, ?)
                """,
                (request_id, participant["name"], participant["channel"], participant["contact"]),
            )
        connection.commit()
        row = connection.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
        print(json.dumps({"request": row_to_dict(row), "participants": participants}, indent=2))


def propose_slots(args):
    slots = [parse_slot(item) for item in args.slot]
    with get_connection(args.base_dir) as connection:
        for slot in slots:
            connection.execute(
                """
                INSERT INTO proposals (request_id, proposed_start, proposed_end, source, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (args.request_id, slot["start"], slot["end"], args.source, args.note),
            )
        connection.commit()
        rows = connection.execute(
            "SELECT * FROM proposals WHERE request_id = ? ORDER BY id ASC", (args.request_id,)
        ).fetchall()
        print(json.dumps({"proposals": [row_to_dict(row) for row in rows]}, indent=2))


def confirm_slot(args):
    with get_connection(args.base_dir) as connection:
        proposal = connection.execute(
            "SELECT * FROM proposals WHERE id = ? AND request_id = ?",
            (args.slot_id, args.request_id),
        ).fetchone()
        if proposal is None:
            raise SystemExit("Requested slot does not exist for that request.")
        connection.execute(
            "UPDATE proposals SET status = 'accepted' WHERE id = ?",
            (args.slot_id,),
        )
        connection.execute(
            "UPDATE requests SET status = 'confirmed', updated_at = ? WHERE id = ?",
            (now_iso(), args.request_id),
        )
        connection.execute(
            """
            INSERT INTO bookings (request_id, proposal_id, chosen_start, chosen_end, confirmed_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(request_id) DO UPDATE SET
                proposal_id = excluded.proposal_id,
                chosen_start = excluded.chosen_start,
                chosen_end = excluded.chosen_end,
                confirmed_by = excluded.confirmed_by
            """,
            (
                args.request_id,
                args.slot_id,
                proposal["proposed_start"],
                proposal["proposed_end"],
                args.confirmed_by,
                now_iso(),
            ),
        )
        connection.commit()
        booking = connection.execute("SELECT * FROM bookings WHERE request_id = ?", (args.request_id,)).fetchone()
        print(json.dumps({"booking": row_to_dict(booking)}, indent=2))


def export_ics(args):
    with get_connection(args.base_dir) as connection:
        booking = connection.execute(
            """
            SELECT bookings.*, requests.title, requests.organizer, requests.timezone, requests.location
            FROM bookings
            JOIN requests ON requests.id = bookings.request_id
            WHERE bookings.request_id = ?
            """,
            (args.request_id,),
        ).fetchone()
        if booking is None:
            raise SystemExit("No confirmed booking exists for this request.")

        output = Path(args.output) if args.output else runtime_dir(args.base_dir) / f"request-{args.request_id}.ics"
        output.parent.mkdir(parents=True, exist_ok=True)
        contents = "\n".join(
            [
                "BEGIN:VCALENDAR",
                "VERSION:2.0",
                "PRODID:-//OpenClaw Skill Suite//Smart Scheduler//EN",
                "BEGIN:VEVENT",
                f"UID:request-{args.request_id}@openclaw-skill-suite",
                f"SUMMARY:{booking['title']}",
                f"DTSTART;TZID={booking['timezone']}:{booking['chosen_start'].replace('-', '').replace(':', '')}",
                f"DTEND;TZID={booking['timezone']}:{booking['chosen_end'].replace('-', '').replace(':', '')}",
                f"DESCRIPTION:Organized by {booking['organizer']}; confirmed by {booking['confirmed_by']}",
                f"LOCATION:{booking['location'] or ''}",
                "END:VEVENT",
                "END:VCALENDAR",
                "",
            ]
        )
        output.write_text(contents, encoding="utf-8")
        connection.execute("UPDATE bookings SET ics_path = ? WHERE request_id = ?", (str(output), args.request_id))
        connection.commit()
        print(json.dumps({"output": str(output)}, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="Track scheduling requests and exports.")
    parser.add_argument("--base-dir", default=Path(__file__).resolve().parents[1], help="Skill directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create-request")
    create_parser.add_argument("--title", required=True)
    create_parser.add_argument("--organizer", required=True)
    create_parser.add_argument("--timezone", required=True)
    create_parser.add_argument("--duration-minutes", required=True, type=int)
    create_parser.add_argument("--participant", action="append", default=[])
    create_parser.add_argument("--location")
    create_parser.add_argument("--notes")
    create_parser.set_defaults(handler=create_request)

    propose_parser = subparsers.add_parser("propose-slots")
    propose_parser.add_argument("--request-id", required=True, type=int)
    propose_parser.add_argument("--slot", action="append", default=[])
    propose_parser.add_argument("--source", default="manual")
    propose_parser.add_argument("--note")
    propose_parser.set_defaults(handler=propose_slots)

    confirm_parser = subparsers.add_parser("confirm-slot")
    confirm_parser.add_argument("--request-id", required=True, type=int)
    confirm_parser.add_argument("--slot-id", required=True, type=int)
    confirm_parser.add_argument("--confirmed-by", required=True)
    confirm_parser.set_defaults(handler=confirm_slot)

    export_parser = subparsers.add_parser("export-ics")
    export_parser.add_argument("--request-id", required=True, type=int)
    export_parser.add_argument("--output")
    export_parser.set_defaults(handler=export_ics)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
