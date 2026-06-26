#!/usr/bin/env python3
"""
Shared Memory Synchronization for OpenClaw Multi-Agent Deployment

Implements file-based and SQLite shared memory systems for agent coordination.
Use --backend sqlite for production deployments with concurrent agents.

Backends:
  file   — JSON file with file locking (default, zero deps)
  sqlite — SQLite3 with WAL mode, ACID transactions (std lib, no pip)

HTTP REST API (--listen):
  Exposes shared memory over HTTP using only Python stdlib. No pip install needed.
  GET  /health, /keys, /count, /stats, /schemas, /read/<agent>/<key>
  POST /write, /cleanup
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time
import hashlib
import os
from typing import Dict, Any, Optional, List, Union

# HTTP server imports (stdlib only)
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    HAS_HTTP = True
except ImportError:
    HAS_HTTP = False


# ──────────────────────────────────────────────
# FILE-BASED BACKEND (default, backward compatible)
# ──────────────────────────────────────────────

class FileSharedMemory:
    """File-based shared memory system for multi-agent coordination."""

    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path)
        self.data_file = self.memory_path / "shared_data.json"
        self.lock_file = self.memory_path / ".lock"
        self.events_dir = self.memory_path.parent / "events"
        self.logs_dir = self.memory_path.parent / "logs"

        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        if not self.data_file.exists():
            self._write_data({
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "agents": {},
                "shared": {},
                "events": [],
                "metadata": {
                    "last_sync": None,
                    "agent_count": 0,
                    "total_operations": 0
                }
            })

    def _read_data(self) -> Dict[str, Any]:
        max_retries = 5
        retry_delay = 0.1
        for attempt in range(max_retries):
            try:
                if not self.data_file.exists():
                    return {}
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)
        return {}

    def _write_data(self, data: Dict[str, Any]):
        temp_file = self.data_file.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_file.replace(self.data_file)

    def _acquire_lock(self, timeout: float = 5.0) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.lock_file.touch(exist_ok=False)
                return True
            except FileExistsError:
                time.sleep(0.01)
        return False

    def _release_lock(self):
        try:
            self.lock_file.unlink(missing_ok=True)
        except Exception:
            pass

    def agent_write(self, agent_id: str, key: str, value: Any, ttl: Optional[int] = None):
        if not self._acquire_lock():
            raise RuntimeError("Could not acquire lock for writing")
        try:
            data = self._read_data()
            data["metadata"]["last_sync"] = datetime.now().isoformat()
            data["metadata"]["total_operations"] = data["metadata"].get("total_operations", 0) + 1

            if agent_id not in data["agents"]:
                data["agents"][agent_id] = {
                    "first_seen": datetime.now().isoformat(),
                    "last_active": datetime.now().isoformat(),
                    "write_count": 0, "read_count": 0
                }

            data["agents"][agent_id]["last_active"] = datetime.now().isoformat()
            data["agents"][agent_id]["write_count"] = data["agents"][agent_id].get("write_count", 0) + 1

            entry = {
                "value": value,
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat(),
                "ttl": ttl,
                "version": data["agents"][agent_id].get("write_count", 1)
            }

            # Handle multi-key write (dict of keys)
            if isinstance(key, dict):
                for k, v in key.items():
                    entry_k = {**entry, "value": v, "timestamp": datetime.now().isoformat()}
                    data["shared"][k] = dict(entry_k)
            else:
                data["shared"][key] = entry

            event = {
                "type": "write",
                "agent_id": agent_id,
                "key": str(key),
                "timestamp": datetime.now().isoformat(),
                "value_hash": hashlib.sha256(json.dumps(value).encode()).hexdigest()[:16]
            }
            data["events"].append(event)
            if len(data["events"]) > 1000:
                data["events"] = data["events"][-1000:]

            self._write_data(data)
            event_file = self.events_dir / f"{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(event_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event) + '\n')
            return True
        finally:
            self._release_lock()

    def agent_read(self, agent_id: str, key: str) -> Optional[Any]:
        if not self._acquire_lock():
            raise RuntimeError("Could not acquire lock for reading")
        try:
            data = self._read_data()
            data["metadata"]["last_sync"] = datetime.now().isoformat()
            if agent_id not in data["agents"]:
                data["agents"][agent_id] = {
                    "first_seen": datetime.now().isoformat(),
                    "last_active": datetime.now().isoformat(),
                    "write_count": 0, "read_count": 0
                }
            data["agents"][agent_id]["last_active"] = datetime.now().isoformat()
            data["agents"][agent_id]["read_count"] = data["agents"][agent_id].get("read_count", 0) + 1

            if key not in data["shared"]:
                self._write_data(data)
                return None
            entry = data["shared"][key]
            if entry.get("ttl"):
                entry_time = datetime.fromisoformat(entry["timestamp"])
                if datetime.now() - entry_time > timedelta(seconds=entry["ttl"]):
                    del data["shared"][key]
                    self._write_data(data)
                    return None

            self._write_data(data)
            return entry["value"]
        finally:
            self._release_lock()

    def get_agent_stats(self) -> Dict[str, Any]:
        data = self._read_data()
        stats = {
            "backend": "file",
            "total_agents": len(data.get("agents", {})),
            "total_shared_keys": len(data.get("shared", {})),
            "total_events": len(data.get("events", [])),
            "metadata": data.get("metadata", {}),
            "agents": {}
        }
        for agent_id, agent_data in data.get("agents", {}).items():
            stats["agents"][agent_id] = {
                "write_count": agent_data.get("write_count", 0),
                "read_count": agent_data.get("read_count", 0),
                "last_active": agent_data.get("last_active"),
                "first_seen": agent_data.get("first_seen")
            }
        return stats

    def cleanup_expired(self) -> int:
        if not self._acquire_lock():
            return 0
        try:
            data = self._read_data()
            removed = 0
            current_time = datetime.now()
            expired_keys = [key for key, entry in data.get("shared", {}).items()
                            if entry.get("ttl") and
                            current_time - datetime.fromisoformat(entry["timestamp"]) > timedelta(seconds=entry["ttl"])]
            for key in expired_keys:
                del data["shared"][key]
                removed += 1
            if removed > 0:
                self._write_data(data)
            return removed
        finally:
            self._release_lock()

    def get_keys(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List shared memory keys, optionally filtered by agent."""
        data = self._read_data()
        keys = []
        for k, v in data.get("shared", {}).items():
            if agent_id is None or v.get("agent_id") == agent_id:
                keys.append({
                    "key": k,
                    "agent_id": v.get("agent_id"),
                    "timestamp": v.get("timestamp"),
                    "ttl": v.get("ttl"),
                    "value_type": type(v.get("value")).__name__
                })
        return sorted(keys, key=lambda x: x.get("timestamp", ""), reverse=True)

    def count_by_agent(self) -> Dict[str, int]:
        """Count keys per agent."""
        data = self._read_data()
        counts = {}
        for v in data.get("shared", {}).values():
            a = v.get("agent_id", "unknown")
            counts[a] = counts.get(a, 0) + 1
        return counts


# ──────────────────────────────────────────────
# SQLITE BACKEND (production-grade, std lib only)
# ──────────────────────────────────────────────

class SQLiteSharedMemory:
    """SQLite-backed shared memory for concurrent multi-agent deployments.

    Uses WAL mode for concurrent reads + writes without blocking.
    ACID transactions ensure data integrity under load.
    """

    def __init__(self, memory_path: Path):
        import sqlite3
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)

        self.db_path = self.memory_path / "shared_memory.sqlite"
        self.events_dir = self.memory_path.parent / "events"
        self.events_dir.mkdir(exist_ok=True)

        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        self._conn.execute("PRAGMA foreign_keys=ON;")
        self._init_schema()

    def _init_schema(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id     TEXT PRIMARY KEY,
                first_seen   TEXT NOT NULL,
                last_active  TEXT NOT NULL,
                write_count  INTEGER DEFAULT 0,
                read_count   INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS shared_data (
                key         TEXT PRIMARY KEY,
                value       TEXT NOT NULL,
                agent_id    TEXT NOT NULL,
                timestamp   TEXT NOT NULL,
                ttl         INTEGER,
                version     INTEGER DEFAULT 1,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            );

            CREATE TABLE IF NOT EXISTS events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                type        TEXT NOT NULL,
                agent_id    TEXT NOT NULL,
                key         TEXT,
                timestamp   TEXT NOT NULL,
                value_hash  TEXT,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            );

            CREATE INDEX IF NOT EXISTS idx_events_time ON events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_shared_agent ON shared_data(agent_id);
        """)
        self._conn.commit()

    def _ensure_agent(self, agent_id: str, cur):
        cur.execute(
            "INSERT INTO agents (agent_id, first_seen, last_active, write_count, read_count) "
            "VALUES (?, ?, ?, 0, 0) "
            "ON CONFLICT(agent_id) DO UPDATE SET last_active=excluded.last_active",
            (agent_id, datetime.now().isoformat(), datetime.now().isoformat())
        )

    def agent_write(self, agent_id: str, key: str, value: Any, ttl: Optional[int] = None):
        cur = self._conn.cursor()
        try:
            self._ensure_agent(agent_id, cur)
            now = datetime.now().isoformat()
            value_json = json.dumps(value, ensure_ascii=False)
            vhash = hashlib.sha256(value_json.encode()).hexdigest()[:16]

            # Handle multi-key dict
            if isinstance(key, dict):
                for k, v in key.items():
                    vj = json.dumps(v, ensure_ascii=False)
                    cur.execute(
                        "INSERT INTO shared_data (key, value, agent_id, timestamp, ttl, version) "
                        "VALUES (?, ?, ?, ?, ?, COALESCE((SELECT version+1 FROM shared_data WHERE key=?), 1)) "
                        "ON CONFLICT(key) DO UPDATE SET value=excluded.value, agent_id=excluded.agent_id, "
                        "timestamp=excluded.timestamp, ttl=excluded.ttl, version=shared_data.version+1",
                        (k, vj, agent_id, now, ttl, k)
                    )
            else:
                cur.execute(
                    "INSERT INTO shared_data (key, value, agent_id, timestamp, ttl, version) "
                    "VALUES (?, ?, ?, ?, ?, COALESCE((SELECT version+1 FROM shared_data WHERE key=?), 1)) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value, agent_id=excluded.agent_id, "
                    "timestamp=excluded.timestamp, ttl=excluded.ttl, version=shared_data.version+1",
                    (key, value_json, agent_id, now, ttl, key)
                )

            cur.execute(
                "UPDATE agents SET write_count=write_count+1, last_active=? WHERE agent_id=?",
                (now, agent_id)
            )

            # Event journaling to SQLite
            cur.execute(
                "INSERT INTO events (type, agent_id, key, timestamp, value_hash) "
                "VALUES (?, ?, ?, ?, ?)",
                ("write", agent_id, str(key), now, vhash)
            )

            # Also write daily event log file
            event_file = self.events_dir / f"{datetime.now().strftime('%Y%m%d')}.jsonl"
            with open(event_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "type": "write", "agent_id": agent_id,
                    "key": str(key), "timestamp": now,
                    "value_hash": vhash
                }) + '\n')

            self._conn.commit()
            return True
        except Exception:
            self._conn.rollback()
            raise

    def agent_read(self, agent_id: str, key: str) -> Optional[Any]:
        cur = self._conn.cursor()
        try:
            self._ensure_agent(agent_id, cur)
            now = datetime.now().isoformat()

            cur.execute("SELECT value, ttl, timestamp FROM shared_data WHERE key=?", (key,))
            row = cur.fetchone()

            if row is None:
                cur.execute("UPDATE agents SET read_count=read_count+1, last_active=? WHERE agent_id=?",
                            (now, agent_id))
                self._conn.commit()
                return None

            # Check TTL expiry
            if row["ttl"] is not None:
                entry_time = datetime.fromisoformat(row["timestamp"])
                if datetime.now() - entry_time > timedelta(seconds=row["ttl"]):
                    cur.execute("DELETE FROM shared_data WHERE key=?", (key,))
                    cur.execute("UPDATE agents SET read_count=read_count+1, last_active=? WHERE agent_id=?",
                                (now, agent_id))
                    self._conn.commit()
                    return None

            cur.execute(
                "INSERT INTO events (type, agent_id, key, timestamp) VALUES (?, ?, ?, ?)",
                ("read", agent_id, key, now)
            )
            cur.execute("UPDATE agents SET read_count=read_count+1, last_active=? WHERE agent_id=?",
                        (now, agent_id))
            self._conn.commit()

            return json.loads(row["value"])
        except Exception:
            self._conn.rollback()
            raise

    def get_agent_stats(self) -> Dict[str, Any]:
        cur = self._conn.cursor()
        stats = {"backend": "sqlite", "db_path": str(self.db_path)}

        cur.execute("SELECT COUNT(*) as cnt FROM agents")
        stats["total_agents"] = cur.fetchone()["cnt"]

        cur.execute("SELECT COUNT(*) as cnt FROM shared_data")
        stats["total_shared_keys"] = cur.fetchone()["cnt"]

        cur.execute("SELECT COUNT(*) as cnt FROM events")
        stats["total_events"] = cur.fetchone()["cnt"]

        cur.execute("SELECT MAX(timestamp) as last_sync FROM events")
        row = cur.fetchone()
        stats["metadata"] = {"last_sync": row["last_sync"] if row else None}

        stats["agents"] = {}
        cur.execute("SELECT agent_id, write_count, read_count, last_active, first_seen FROM agents")
        for row in cur.fetchall():
            stats["agents"][row["agent_id"]] = {
                "write_count": row["write_count"],
                "read_count": row["read_count"],
                "last_active": row["last_active"],
                "first_seen": row["first_seen"]
            }

        # DB file size
        try:
            stats["db_size_bytes"] = os.path.getsize(self.db_path)
        except OSError:
            stats["db_size_bytes"] = 0

        return stats

    def cleanup_expired(self) -> int:
        cur = self._conn.cursor()
        try:
            now = datetime.now().isoformat()
            cur.execute("""
                DELETE FROM shared_data
                WHERE ttl IS NOT NULL
                AND datetime(timestamp, '+' || ttl || ' seconds') < datetime(?)
            """, (now,))
            removed = cur.rowcount
            self._conn.commit()
            return removed
        except Exception:
            self._conn.rollback()
            return 0

    def get_keys(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        if agent_id:
            cur.execute(
                "SELECT key, agent_id, timestamp, ttl, value FROM shared_data WHERE agent_id=? ORDER BY timestamp DESC",
                (agent_id,)
            )
        else:
            cur.execute("SELECT key, agent_id, timestamp, ttl, value FROM shared_data ORDER BY timestamp DESC")

        keys = []
        for row in cur.fetchall():
            try:
                vt = type(json.loads(row["value"])).__name__
            except (json.JSONDecodeError, TypeError):
                vt = "unknown"
            keys.append({
                "key": row["key"],
                "agent_id": row["agent_id"],
                "timestamp": row["timestamp"],
                "ttl": row["ttl"],
                "value_type": vt
            })
        return keys

    def count_by_agent(self) -> Dict[str, int]:
        cur = self._conn.cursor()
        cur.execute("SELECT agent_id, COUNT(*) as cnt FROM shared_data GROUP BY agent_id")
        return {row["agent_id"]: row["cnt"] for row in cur.fetchall()}

    def close(self):
        self._conn.close()


# ──────────────────────────────────────────────
# HTTP REST API SERVER (stdlib, zero deps)
# ──────────────────────────────────────────────

class SharedMemoryHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler exposing shared memory over REST.

    Uses only Python stdlib (http.server, json, urllib).
    No pip install required.

    Endpoints:
      GET  /health         — Health check
      GET  /keys           — List all keys (?agent=X to filter)
      GET  /count          — Keys per agent
      GET  /stats          — Shared memory statistics
      GET  /schemas        — List typed schemas
      GET  /read/<agent>/<key>  — Read shared memory value
      POST /write          — Write shared memory value
      POST /cleanup        — Cleanup expired entries
    """

    # Shared across instances via class vars
    memory = None
    backend_type = "file"

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        try:
            if path == "/health":
                self._json_response({"status": "ok", "backend": self.backend_type})

            elif path == "/keys":
                agent_q = qs.get("agent", [None])[0]
                keys = self.memory.get_keys(agent_q if agent_q else None)
                self._json_response({"total": len(keys), "keys": keys})

            elif path == "/count":
                counts = self.memory.count_by_agent()
                self._json_response(counts)

            elif path == "/stats":
                stats = self.memory.get_agent_stats()
                self._json_response(stats)

            elif path == "/schemas":
                self._json_response({
                    "schemas": AVAILABLE_SCHEMAS,
                    "count": len(AVAILABLE_SCHEMAS)
                })

            elif path.startswith("/read/"):
                parts = path[len("/read/"):].split("/", 1)
                if len(parts) != 2:
                    self._json_response({"error": "Use /read/<agent_id>/<key>"}, 400)
                    return
                agent_id, key = parts
                value = self.memory.agent_read(agent_id, key)
                if value is not None:
                    self._json_response({"key": key, "agent_id": agent_id, "value": value})
                else:
                    self._json_response({"error": "Key not found or expired"}, 404)

            else:
                self._json_response({"error": f"Not found: {path}"}, 404)

        except Exception as e:
            self._json_response({"error": str(e)}, 500)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._json_response({"error": "Invalid JSON body"}, 400)
            return
        except Exception:
            self._json_response({"error": "Cannot read request body"}, 400)
            return

        try:
            if path == "/write":
                agent_id = data.get("agent_id")
                key = data.get("key")
                value = data.get("value")
                ttl = data.get("ttl")
                schema_type = data.get("schema")

                if not agent_id or not key or value is None:
                    self._json_response({
                        "error": "Missing required fields: agent_id, key, value"
                    }, 400)
                    return

                # Schema validation
                if schema_type:
                    if isinstance(value, dict):
                        inner = value.get("data", value)
                        valid, errors = validate_schema(schema_type, inner)
                        if not valid:
                            self._json_response({
                                "error": "Schema validation failed",
                                "schema": schema_type,
                                "errors": errors
                            }, 422)
                            return

                success = self.memory.agent_write(agent_id, key, value, ttl)
                if success:
                    self._json_response({
                        "status": "written",
                        "key": key,
                        "agent_id": agent_id
                    }, 201)
                else:
                    self._json_response({"error": "Write failed"}, 500)

            elif path == "/cleanup":
                removed = self.memory.cleanup_expired()
                self._json_response({"status": "ok", "removed": removed})

            else:
                self._json_response({"error": f"Not found: {path}"}, 404)

        except Exception as e:
            self._json_response({"error": str(e)}, 500)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path == "/cleanup":
            try:
                removed = self.memory.cleanup_expired()
                self._json_response({"status": "ok", "removed": removed})
            except Exception as e:
                self._json_response({"error": str(e)}, 500)
        else:
            self._json_response({"error": f"Not found: {path}"}, 404)

    def _json_response(self, data, status=200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        sys.stderr.write(f"[{datetime.now().isoformat()}] {args[0]} {args[1]} {args[2]}\n")


def run_http_server(memory, backend_type, host, port):
    """Start the REST API server."""
    SharedMemoryHTTPRequestHandler.memory = memory
    SharedMemoryHTTPRequestHandler.backend_type = backend_type

    server = HTTPServer((host, int(port)), SharedMemoryHTTPRequestHandler)
    print(f"Shared Memory REST API running on http://{host}:{port}")
    print(f"  Backend: {backend_type}")
    print(f"  Endpoints:")
    print(f"    GET  /health          — Health check")
    print(f"    GET  /keys            — List keys (?agent=X filter)")
    print(f"    GET  /count           — Keys per agent")
    print(f"    GET  /stats           — Statistics")
    print(f"    GET  /schemas         — List typed schemas")
    print(f"    GET  /read/<a>/<k>    — Read a value")
    print(f"    POST /write           — Write value (JSON body)")
    print(f"    POST /cleanup         — Cleanup expired entries")
    print(f"  Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()
        print("Server stopped.")


# ──────────────────────────────────────────────
# SCHEMA VALIDATION (shared across backends)
# ──────────────────────────────────────────────

def validate_schema(schema_type: str, data: dict) -> tuple:
    """Validate data dict against a known typed schema.

    Returns (is_valid: bool, errors: list[str]).
    """
    if not isinstance(data, dict):
        return True, []
    if not schema_type:
        return True, []

    errors = []

    schemas = {
        "task_assignment": {
            "required": ["task_id", "assigned_by", "assigned_to", "priority", "title", "description"],
            "enums": {"priority": ["critical", "high", "normal", "low"]},
        },
        "status_update": {
            "required": ["task_id", "agent_id", "status", "progress_pct", "message"],
            "enums": {"status": ["in_progress", "blocked", "completed", "failed"]},
        },
        "coordination_message": {
            "required": ["message_id", "sender", "recipient", "subject", "body"],
            "enums": {"priority": ["normal", "high", "critical"]},
        },
        "research_finding": {
            "required": ["topic", "summary", "confidence", "sources"],
        },
        "builder_output": {
            "required": ["task_id", "language", "files"],
        },
        "audit_report": {
            "required": ["task_id", "reviewed_by", "verdict", "findings", "overall_score"],
            "enums": {"verdict": ["pass", "pass_with_warnings", "fail"]},
        },
    }

    if schema_type not in schemas:
        errors.append(f"Unknown schema type: '{schema_type}'")
        return False, errors

    schema = schemas[schema_type]

    for field in schema.get("required", []):
        if field not in data or data[field] is None:
            errors.append(f"Missing required field '{field}' in {schema_type}")

    for field, valid_values in schema.get("enums", {}).items():
        if field in data and data[field] not in valid_values:
            errors.append(f"Field '{field}' must be one of {valid_values}, got '{data[field]}'")

    return len(errors) == 0, errors


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

AVAILABLE_SCHEMAS = [
    "task_assignment", "status_update", "coordination_message",
    "research_finding", "builder_output", "audit_report"
]


def create_backend(backend: str, path: Path) -> Union[FileSharedMemory, SQLiteSharedMemory]:
    if backend == "sqlite":
        return SQLiteSharedMemory(path)
    return FileSharedMemory(path)


def main():
    parser = argparse.ArgumentParser(description="Shared Memory Synchronization System")
    parser.add_argument("--init", action="store_true", help="Initialize shared memory system")
    parser.add_argument("--path", default="./shared_memory", help="Path to shared memory directory")
    parser.add_argument("--write", help="Write data: --write 'agent_id:key:value'")
    parser.add_argument("--read", help="Read data: --read 'agent_id:key'")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup expired entries")
    parser.add_argument("--schema", help=f"Validate write against a typed schema ({'|'.join(AVAILABLE_SCHEMAS)})")
    parser.add_argument("--list-schemas", action="store_true", help="List available typed schemas")
    parser.add_argument("--backend", choices=["file", "sqlite"], default="file",
                        help="Storage backend (file=JSON+lock, sqlite=WAL+ACID)")
    parser.add_argument("--keys", nargs="?", const=True, metavar="AGENT",
                        help="List shared memory keys (optionally filtered by agent)")
    parser.add_argument("--count-by-agent", action="store_true",
                        help="Show key count per agent")
    parser.add_argument("--compact", action="store_true",
                        help="SQLite: VACUUM to reclaim space")
    parser.add_argument("--migrate-to-sqlite", help="Migrate from file backend to SQLite: --migrate-to-sqlite ./shared_memory")
    parser.add_argument("--listen", nargs="?", const="8080", metavar="PORT",
                        help="Start REST API server (default port 8080, stdlib only, no pip)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Listen address for --listen (default: 127.0.0.1)")

    args = parser.parse_args()

    memory_path = Path(args.path)
    backend_type = args.backend

    # Migration: file → sqlite
    if args.migrate_to_sqlite:
        src_path = Path(args.migrate_to_sqlite)
        if not src_path.exists():
            print(f"Error: Source path not found: {src_path}")
            sys.exit(1)

        file_mem = FileSharedMemory(src_path)
        data = file_mem._read_data()

        dst_path = src_path.parent / "shared_memory_sqlite"
        sqlite_mem = SQLiteSharedMemory(dst_path)

        count = 0
        for key, entry in data.get("shared", {}).items():
            sqlite_mem.agent_write(
                entry.get("agent_id", "migration"),
                key,
                entry.get("value"),
                entry.get("ttl")
            )
            count += 1

        # Copy agent stats
        cur = sqlite_mem._conn.cursor()
        for agent_id, agent_data in data.get("agents", {}).items():
            cur.execute(
                "INSERT OR REPLACE INTO agents (agent_id, first_seen, last_active, write_count, read_count) "
                "VALUES (?, ?, ?, ?, ?)",
                (agent_id,
                 agent_data.get("first_seen", datetime.now().isoformat()),
                 agent_data.get("last_active", datetime.now().isoformat()),
                 agent_data.get("write_count", 0),
                 agent_data.get("read_count", 0))
            )
        sqlite_mem._conn.commit()

        print(f"Migration complete: {count} keys migrated")
        print(f"  Source (file):  {src_path / 'shared_data.json'}")
        print(f"  Destination:     {dst_path / 'shared_memory.sqlite'}")
        print(f"  Use: python memory_sync.py --path {dst_path} --backend sqlite")
        return

    # Init
    if args.init:
        memory = create_backend(backend_type, memory_path)
        print(f"Shared memory initialized ({backend_type} backend): {memory_path.absolute()}")
        if backend_type == "file":
            print(f"  Data file: {memory.data_file.absolute()}")
        else:
            print(f"  Database: {memory.db_path.absolute()}")
            print(f"  Journal mode: WAL")
        print(f"  Events directory: {memory.events_dir.absolute()}")
        return

    memory = create_backend(backend_type, memory_path)

    # HTTP REST API server
    if args.listen is not None:
        if not HAS_HTTP:
            print("Error: HTTP server module not available in this Python environment")
            sys.exit(1)
        run_http_server(memory, backend_type, args.host, args.listen)
        return

    # List schemas
    if args.list_schemas:
        print("Available typed schemas (use with --schema):")
        for s in AVAILABLE_SCHEMAS:
            print(f"  - {s}")
        print()
        print("See references/memory-schemas.md for full field definitions.")
        return

    # Compact (sqlite VACUUM)
    if args.compact:
        if backend_type != "sqlite":
            print("Error: --compact only supports sqlite backend")
            sys.exit(1)
        print("Running VACUUM to reclaim space...")
        memory._conn.execute("VACUUM;")
        print("Compact complete.")
        return

    # Write
    if args.write:
        try:
            agent_id, key, value = args.write.split(':', 2)
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass

            if args.schema:
                if isinstance(value, dict):
                    if "type" not in value:
                        inner_data = value
                    else:
                        inner_data = value.get("data", value)
                    valid, errors = validate_schema(args.schema, inner_data)
                else:
                    print(f"Warning: --schema {args.schema} ignored for non-object value")
                    valid, errors = True, []

                if not valid:
                    print("Schema validation FAILED:")
                    for err in errors:
                        print(f"  - {err}")
                    sys.exit(1)
                print(f"Schema validation PASSED ({args.schema})")

            success = memory.agent_write(agent_id, key, value)
            if success:
                print(f"Write successful [{backend_type}]: {agent_id} -> {key}")
            else:
                print("Write failed")
        except ValueError:
            print("Invalid write format. Use: agent_id:key:value")
            sys.exit(1)

    # Read
    elif args.read:
        try:
            agent_id, key = args.read.split(':', 1)
            value = memory.agent_read(agent_id, key)
            if value is not None:
                print(f"Value for {key}:")
                print(json.dumps(value, indent=2))
            else:
                print(f"No value found for key: {key}")
        except ValueError:
            print("Invalid read format. Use: agent_id:key")
            sys.exit(1)

    # Stats
    elif args.stats:
        stats = memory.get_agent_stats()
        print(f"Shared Memory Statistics ({backend_type} backend):")
        print(json.dumps(stats, indent=2))

    # Keys
    elif args.keys is not None:
        agent_filter = args.keys if isinstance(args.keys, str) and args.keys != "True" else None
        keys = memory.get_keys(agent_filter)
        if not keys:
            print("No keys found in shared memory.")
        else:
            print(f"Shared Memory Keys ({len(keys)} total):")
            for k in keys:
                ttl_str = f", TTL={k['ttl']}s" if k.get('ttl') else ""
                print(f"  {k['key']:<30} agent={k['agent_id']:<15} type={k.get('value_type','?'):<10}{ttl_str}")

    # Count by agent
    elif args.count_by_agent:
        counts = memory.count_by_agent()
        if not counts:
            print("No keys found.")
        else:
            print("Keys per agent:")
            for agent, cnt in sorted(counts.items(), key=lambda x: -x[1]):
                print(f"  {agent:<20} {cnt} keys")

    # Cleanup
    elif args.cleanup:
        removed = memory.cleanup_expired()
        print(f"Removed {removed} expired entries")

    else:
        stats = memory.get_agent_stats()
        print(f"Shared Memory Status ({backend_type} backend):")
        print(f"  Location: {memory_path.absolute()}")
        print(f"  Total agents: {stats['total_agents']}")
        print(f"  Shared keys: {stats['total_shared_keys']}")
        print(f"  Total events: {stats['total_events']}")
        if backend_type == "sqlite":
            print(f"  DB size: {stats.get('db_size_bytes', 0)} bytes")
        print(f"  Last sync: {stats['metadata'].get('last_sync', 'Never')}")
        print()
        print("Usage examples:")
        print(f"  # File backend (default)")
        print("  python memory_sync.py --write 'coordinator:task_status:{\"status\":\"completed\"}'")
        print("  python memory_sync.py --read 'research:search_results'")
        print(f"  # SQLite backend (production)")
        print(f"  python memory_sync.py --backend sqlite --init --path ./shared_memory")
        print("  python memory_sync.py --backend sqlite --write 'coordinator:task:{\"id\":\"t1\"}'")
        print("  python memory_sync.py --keys")
        print("  python memory_sync.py --count-by-agent")
        print("  python memory_sync.py --stats")
        print("  python memory_sync.py --cleanup")
        print("  # HTTP REST API (stdlib, zero deps)")
        print("  python memory_sync.py --listen --backend sqlite --path ./shared_memory")
        print("  curl http://localhost:8080/health")
        print('  curl -X POST http://localhost:8080/write \\')
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"agent_id":"coordinator","key":"task:t001","value":{"status":"active"}}\'')


if __name__ == "__main__":
    main()
