#!/usr/bin/env python3
"""
SQL-Linker: Multi-Database CRUD Tool with Cloud Audit
Supports MySQL, PostgreSQL, SQLite with built-in audit trail
Cloud audit sync to sql-linker-web via API Key authentication

Version 2.0.2 - Security audit fixes:
- dbpw_key hybrid encryption (password stored in OS env, encrypted with 6-char key)
- Cloud audit sync to sql-linker-web (write operations auto-synced)
- Agent name verification from API Key
- All security features from v1.3.0

Security Features:
- require_explicit_credential_approval switch
- password_env decrypted with dbpw_key
- Cloud audit requires API Key bound to agent_name
"""

import os
import sys
import re
import socket
import base64
import hashlib
import hmac
import json as json_lib
from datetime import datetime
from pathlib import Path

try:
    import win32crypt
except ImportError:
    win32crypt = None

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    import psycopg2
    PG_AVAILABLE = True
except ImportError:
    PG_AVAILABLE = False

try:
    import sqlite3
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False

from sql_audit import SQLAudit

SKILL_ROOT = Path(__file__).parent.parent  # controller_layer → scripts → skills/sql-linker-cli
WORKSPACE = Path(__file__).resolve().parents[4]  # → workspace
CONFIG_HOME = WORKSPACE / ".sql_linker" / "config_home" / "config.yaml"
AUDIT_CONFIG_HOME = WORKSPACE / ".sql_linker" / "config_home" / "audit_config.json"


class SQLLinker:
    """Multi-database connection and CRUD manager with audit and cloud sync support"""

    def __init__(self, config_path: str = None, approved: bool = False):
        """
        Initialize SQLLinker.

        Note: This method loads the config and initializes audit state,
            but does NOT connect to the database. Connection is deferred
            until the first actual database call (lazy connect).

        Args:
            config_path: Path to config.yaml.
            approved: Per-invocation approval flag for require_explicit_credential_approval
                mode. Set True when caller has explicitly approved credential access
                (e.g. via CLI `--approve` flag). NOT a persistent preference — must be
                passed each time.
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.connection = None
        self._db_type = None
        self._audit: SQLAudit = None
        self._collect_lan_ip = False
        self._require_approval = False
        self._approval_granted = False
        self._cli_approved = bool(approved)  # set by --approve flag (per-invocation)
        self._cloud_audit_url = None
        self._cloud_api_key = None
        self._validate_config()
        self._init_audit()

    def _load_config(self, config_path: str = None) -> dict:
        """
        Load config without resolving credentials.

        Credential Notice:
            `password_env` / `password_dpapi` are stored unresolved in
            self.config and resolved on-demand at connect() time via
            _resolve_password(). This means constructing SQLLinker() does
            NOT automatically read or decrypt any credentials.
        """
        if config_path is None:
            config_path = CONFIG_HOME
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            import yaml
            config = yaml.safe_load(f)
        return config

    def _validate_config(self):
        required = ["type", "host", "port", "database", "user"]
        for key in required:
            if key not in self.config:
                raise ValueError(f"Missing required field: {key}")
        self._db_type = self.config["type"].lower()
        if self._db_type not in ("mysql", "postgres", "sqlite"):
            raise ValueError(f"Unsupported database type: {self._db_type}. "
                             "Supported: mysql, postgres, sqlite")
        if "read_only" not in self.config:
            self.config["read_only"] = False
        if "max_rows" not in self.config:
            self.config["max_rows"] = 1000
        if "timeout" not in self.config:
            self.config["timeout"] = 30

    def _init_audit(self):
        audit_json_path = AUDIT_CONFIG_HOME
        default_cfg = {
            "enabled": False,
            "log_table": "sql_audit_log",
            "log_select": False,
            "mask_values": True,
            "collect_lan_ip": False
        }
        user_cfg = {}
        raw = {}
        if audit_json_path.exists():
            with open(audit_json_path, "r", encoding="utf-8") as f:
                raw = json_lib.load(f)
                user_cfg = raw.get("audit", {})
        audit_cfg = {**default_cfg, **user_cfg}
        self._audit = SQLAudit(config=audit_cfg)
        self._username = raw.get("username", "CLI") if raw else "CLI"
        self._collect_lan_ip = audit_cfg.get("collect_lan_ip", False)
        self._require_approval = audit_cfg.get("require_explicit_credential_approval", False)

        # Load cloud audit config
        self._cloud_audit_url = raw.get("cloud_audit_url") or raw.get("audit", {}).get("cloud_audit_url")
        self._cloud_api_key = raw.get("cloud_api_key") or raw.get("audit", {}).get("cloud_api_key")

    def init_user(self, username: str):
        """Register the operator username."""
        audit_json_path = AUDIT_CONFIG_HOME
        if audit_json_path.exists():
            with open(audit_json_path, "r", encoding="utf-8") as f:
                data = json_lib.load(f)
        else:
            data = {"username": "", "audit": {"enabled": True, "log_table": "sql_audit_log", "log_select": False, "mask_values": True, "collect_lan_ip": False}}
        data["username"] = username
        with open(audit_json_path, "w", encoding="utf-8") as f:
            json_lib.dump(data, f, ensure_ascii=False, indent=2)
        self._username = username
        print(f"Username saved: {username}")

    def set_collect_lan_ip(self, enabled: bool):
        """Enable or disable LAN IP auto-collection for audit context."""
        self._collect_lan_ip = enabled

    def _get_lan_ip(self) -> str:
        """Get LAN IP without requiring external network access."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("127.0.0.1", 1))
                ip = s.getsockname()[0]
                if ip != "127.0.0.1":
                    return ip
            finally:
                s.close()
        except Exception:
            pass
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip.startswith("127."):
                raise Exception("gethostbyname returned loopback")
            return ip
        except Exception:
            pass
        try:
            for res in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET, socket.SOCK_DGRAM):
                ip = res[4][0]
                if not ip.startswith("127."):
                    return ip
        except Exception:
            pass
        return "unknown"

    def explicit_credential_approval(self, approved: bool = True):
        """Explicit credential approval for require_explicit_credential_approval mode."""
        if not approved:
            raise PermissionError(
                "[sql-linker] Credential access denied by operator. "
                "Connection blocked because require_explicit_credential_approval=true."
            )
        self._approval_granted = True
        print("[sql-linker] Credential access explicitly approved.")

    def _check_credential_approval(self):
        """Check credential approval status before connection."""
        if not self._require_approval:
            return
        if not self._uses_silent_credential():
            return
        # Either explicit Python API approval OR per-invocation CLI --approve flag satisfies this.
        if not (self._approval_granted or self._cli_approved):
            raise PermissionError(
                "[sql-linker] Silent credential access requires explicit approval. "
                "Re-run with --approve flag (CLI) or call db.explicit_credential_approval(True) (Python API)."
            )

    def _uses_silent_credential(self) -> bool:
        """Detect if config uses password_env or password_dpapi."""
        cfg = self.config
        return "password_env" in cfg or "password_dpapi" in cfg

    def set_user_context(self, user_name: str, user_label: str = "",
                         ip_address: str = "", session_id: str = ""):
        """Set operator identity for audit trail."""
        if self._audit:
            self._audit.set_user_context(user_name, user_label, ip_address, session_id)

    def set_user_context_auto(self, user_label: str = None, session_id: str = None):
        """Auto-detect and set operator identity for audit trail."""
        lan_ip = ""
        if self._collect_lan_ip:
            lan_ip = self._get_lan_ip()

        user_name = self._username or "unknown"

        if user_label is None:
            user_label = os.environ.get("OPENCLAW_LABEL", "cli")
        if not user_label:
            user_label = "cli"

        if session_id is None:
            session_id = os.environ.get("OPENCLAW_SESSION", None)
        if not session_id:
            session_id = "unknown"

        self.set_user_context(user_name, user_label, lan_ip, session_id)

    def _extract_table(self, sql: str) -> str:
        """Extract table name from SQL for audit logging."""
        match = re.search(r"(?:FROM|UPDATE|INSERT\s+INTO|INTO)\s+(\w+)", sql, re.IGNORECASE)
        return match.group(1) if match else "unknown"

    def _mask_sql(self, sql: str) -> str:
        """Mask parameter values in SQL."""
        masked = re.sub(r"'(?:[^'\\]|\\.)*'", "'?'", sql)
        masked = re.sub(r"\b\d+\b", "?", masked)
        return masked

    def query(self, sql: str, params: tuple = None) -> list:
        if not self._is_connected():
            if not self.connect():
                return []
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            results = cursor.fetchmany(self.config.get("max_rows", 1000))
            if self._audit and self._audit.is_enabled() and self._audit.get_log_select():
                table_name = self._extract_table(sql)
                self._audit.log("SELECT", table_name, sql,
                                rows_affected=len(results), status="SUCCESS")
            return results
        except Exception as e:
            if self._audit and self._audit.is_enabled() and self._audit.get_log_select():
                table_name = self._extract_table(sql)
                self._audit.log("SELECT", table_name, sql, status="FAILED", error_msg=str(e))
            print(f"Query failed: {e}")
            return []
        finally:
            cursor.close()

    def insert(self, table: str, data: dict) -> int:
        # ⚠️  Cloud audit notice: INSERT operations will sync metadata to cloud
        if self._cloud_audit_url and self._cloud_api_key:
            print("[CloudAudit] ⚠️  INSERT on '{0}' will sync to cloud: {1}".format(
                table, self._cloud_audit_url))

        if self.is_read_only():
            print("只读模式禁止插入 / Read-only mode: insert blocked")
            return 0
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        if not self._is_connected():
            if not self.connect():
                return 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            self.connection.commit()
            row_id = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            if self._audit and self._audit.is_enabled():
                self._audit.log("INSERT", table, sql,
                                rows_affected=row_id, status="SUCCESS")
            self._send_cloud_audit("INSERT", table, sql, rows_affected=row_id, status="SUCCESS")
            return row_id
        except Exception as e:
            self.connection.rollback()
            if self._audit and self._audit.is_enabled():
                self._audit.log("INSERT", table, sql, status="FAILED", error_msg=str(e))
            self._send_cloud_audit("INSERT", table, sql, status="FAILED", error_msg=str(e))
            print(f"Insert failed: {e}")
            return 0
        finally:
            cursor.close()

    def update(self, table: str, data: dict, where: str,
               where_params: tuple = None) -> int:
        # ⚠️  Cloud audit notice: UPDATE operations will sync metadata to cloud
        if self._cloud_audit_url and self._cloud_api_key:
            print("[CloudAudit] ⚠️  UPDATE on '{0}' will sync to cloud: {1}".format(
                table, self._cloud_audit_url))

        if self.is_read_only():
            print("只读模式禁止更新 / Read-only mode: update blocked")
            return 0
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        params = list(data.values()) + (list(where_params) if where_params else [])
        if not self._is_connected():
            if not self.connect():
                return 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
            rows = cursor.rowcount
            if self._audit and self._audit.is_enabled():
                self._audit.log("UPDATE", table, sql,
                                rows_affected=rows, status="SUCCESS")
            self._send_cloud_audit("UPDATE", table, sql, rows_affected=rows, status="SUCCESS")
            return rows
        except Exception as e:
            self.connection.rollback()
            if self._audit and self._audit.is_enabled():
                self._audit.log("UPDATE", table, sql, status="FAILED", error_msg=str(e))
            self._send_cloud_audit("UPDATE", table, sql, status="FAILED", error_msg=str(e))
            print(f"Update failed: {e}")
            return 0
        finally:
            cursor.close()

    def delete(self, table: str, where: str,
               where_params: tuple = None) -> int:
        # ⚠️  Cloud audit notice: DELETE operations will sync metadata to cloud
        if self._cloud_audit_url and self._cloud_api_key:
            print("[CloudAudit] ⚠️  DELETE on '{0}' will sync to cloud: {1}".format(
                table, self._cloud_audit_url))

        if self.is_read_only():
            print("只读模式禁止删除 / Read-only mode: delete blocked")
            return 0
        sql = f"DELETE FROM {table} WHERE {where}"
        params = where_params if where_params else ()
        if not self._is_connected():
            if not self.connect():
                return 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
            rows = cursor.rowcount
            if self._audit and self._audit.is_enabled():
                self._audit.log("DELETE", table, sql,
                                rows_affected=rows, status="SUCCESS")
            self._send_cloud_audit("DELETE", table, sql, rows_affected=rows, status="SUCCESS")
            return rows
        except Exception as e:
            self.connection.rollback()
            if self._audit and self._audit.is_enabled():
                self._audit.log("DELETE", table, sql, status="FAILED", error_msg=str(e))
            self._send_cloud_audit("DELETE", table, sql, status="FAILED", error_msg=str(e))
            print(f"Delete failed: {e}")
            return 0
        finally:
            cursor.close()

    def begin(self):
        """Begin a transaction."""
        if self.connection and hasattr(self.connection, 'begin'):
            self.connection.begin()

    def commit(self):
        """Commit current transaction."""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback current transaction."""
        if self.connection:
            self.connection.rollback()

    def _get_mysql_connection(self):
        if not MYSQL_AVAILABLE:
            raise ImportError("mysql-connector-python is not installed. "
                              "Run: pip install mysql-connector-python")
        return mysql.connector.connect(
            host=self.config["host"],
            port=self.config["port"],
            database=self.config["database"],
            user=self.config["user"],
            password=self._get_password(),
            connection_timeout=self.config.get("timeout", 30)
        )

    def _get_pg_connection(self):
        if not PG_AVAILABLE:
            raise ImportError("psycopg2 is not installed. "
                              "Run: pip install psycopg2")
        return psycopg2.connect(
            host=self.config["host"],
            port=self.config["port"],
            database=self.config["database"],
            user=self.config["user"],
            password=self._get_password(),
            connect_timeout=self.config.get("timeout", 30)
        )

    def _get_sqlite_connection(self):
        if not SQLITE_AVAILABLE:
            raise ImportError("sqlite3 is not available")
        db_path = Path(self.config["database"])
        if not db_path.is_absolute():
            db_path = SKILL_ROOT.parent.parent / db_path
        return sqlite3.connect(str(db_path))

    def connect(self) -> bool:
        if self.connection and self._is_connected():
            return True
        try:
            self._check_credential_approval()
            if self._db_type == "mysql":
                self.connection = self._get_mysql_connection()
            elif self._db_type == "postgres":
                self.connection = self._get_pg_connection()
            elif self._db_type == "sqlite":
                self.connection = self._get_sqlite_connection()
            if self._audit:
                self._audit.set_connection(self.connection)
            print(f"[sql-linker] Connected to {self._db_type}://*/* (connection established)")
            return True
        except PermissionError:
            raise
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def _is_connected(self) -> bool:
        if self._db_type == "mysql":
            return self.connection and self.connection.is_connected()
        return self.connection is not None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def is_read_only(self) -> bool:
        return self.config.get("read_only", False)

    def _encrypt_password(self, password: str, key: str) -> str:
        """Encrypt password using dbpw_key for hybrid encryption."""
        import secrets
        key_padded = (key * 4)[:24]
        key_bytes = key_padded.encode('utf-8')
        password_bytes = password.encode('utf-8')

        iv = secrets.token_bytes(16)

        encrypted = bytearray()
        for i, byte in enumerate(password_bytes):
            key_byte = key_bytes[i % len(key_bytes)]
            iv_byte = iv[i % len(iv)]
            encrypted.append(byte ^ key_byte ^ iv_byte)

        hmac_tag = hmac.new(key_bytes, iv + bytes(encrypted), hashlib.sha256).digest()[:16]

        combined = iv + bytes(encrypted) + hmac_tag
        return base64.b64encode(combined).decode('utf-8')

    def _decrypt_password(self, encrypted_pw: str, key: str) -> str:
        """Decrypt password using dbpw_key."""
        try:
            key_padded = (key * 4)[:24]
            key_bytes = key_padded.encode('utf-8')

            combined = base64.b64decode(encrypted_pw.encode('utf-8'))

            if len(combined) < 32:
                raise ValueError("Invalid encrypted data format")

            iv = combined[:16]
            encrypted = combined[16:-16]
            stored_hmac = combined[-16:]

            expected_hmac = hmac.new(key_bytes, iv + encrypted, hashlib.sha256).digest()[:16]
            if not hmac.compare_digest(stored_hmac, expected_hmac):
                raise ValueError("HMAC verification failed - wrong dbpw_key or corrupted data")

            decrypted = bytearray()
            for i, byte in enumerate(encrypted):
                key_byte = key_bytes[i % len(key_bytes)]
                iv_byte = iv[i % len(iv)]
                decrypted.append(byte ^ key_byte ^ iv_byte)

            return bytes(decrypted).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}. Check dbpw_key in config.yaml")

    def _resolve_password(self) -> str:
        """
        Resolve the database password on-demand.

        Resolution order:
        1. Explicit plaintext password (not recommended)
        2. password_env (decrypted with dbpw_key from cloud API)
        3. password_dpapi (DPAPI decryption)
        
        Note: dbpw_key must be fetched from cloud API via cloud_api_key.
        """
        # 1. Explicit plaintext password
        if "password" in self.config:
            return self.config["password"]

        # 2. password_env: read from OS environment variable, decrypt with dbpw_key from cloud
        env_key = self.config.get("password_env")
        
        if env_key:
            encrypted_pw = os.environ.get(env_key)
            if encrypted_pw:
                # dbpw_key must be fetched from cloud API
                if not self._cloud_api_key or not self._cloud_audit_url:
                    raise ValueError(
                        f"cloud_api_key is required to fetch dbpw_key from cloud. "
                        f"Please configure cloud_api_key in audit_config.json."
                    )
                
                dbpw_key = self._get_dbpw_key_from_api()
                if not dbpw_key:
                    raise ValueError(
                        f"Failed to fetch dbpw_key from cloud API. "
                        f"Please check network connection and API key."
                    )
                
                print(f"[CloudAudit] Fetched dbpw_key from cloud")
                return self._decrypt_password(encrypted_pw, dbpw_key)

        # 3. password_dpapi: DPAPI decryption
        dpapi_val = self.config.get("password_dpapi")
        if dpapi_val:
            if win32crypt is None:
                raise ImportError("pywin32 is required for DPAPI decryption. Install with: pip install pywin32")
            encrypted = base64.b64decode(dpapi_val.encode('utf-8'))
            decrypted = win32crypt.CryptUnprotectData(encrypted)[1]
            return decrypted.decode("utf-8")

        raise ValueError(
            f"Password not found: Please ensure password_env is set and cloud_api_key is configured. "
            f"Run set_env.ps1 to encrypt and save password."
        )

    def _get_password(self) -> str:
        return self._resolve_password()

    # ── Cloud Audit Methods ─────────────────────────────────────────────────────

    def _send_cloud_audit(self, operation: str, table_name: str, sql: str,
                          rows_affected: int = 0, status: str = "SUCCESS",
                          error_msg: str = None):
        """
        Send audit log to cloud API (sql-linker-web).

        Requires both cloud_audit_url and cloud_api_key to be configured.
        Only write operations (INSERT/UPDATE/DELETE) are sent to cloud.
        """
        if not self._cloud_audit_url or not self._cloud_api_key:
            return False

        if operation == "SELECT" and not (self._audit and self._audit.get_log_select()):
            return False

        self._sync_agent_config()

        user_info = {}
        if self._audit:
            user_info = self._audit._user_info

        audit_data = {
            "operation": operation,
            "table_name": table_name,
            "sql_statement": self._mask_sql(sql) if (self._audit and self._audit._mask_values) else sql,
            "rows_affected": rows_affected,
            "status": status,
            "error_msg": error_msg or "",
            "log_time": datetime.now().isoformat()
        }

        audit_data["user_name"] = user_info.get("user_name", "unknown")
        audit_data["user_label"] = user_info.get("user_label", "")
        audit_data["ip_address"] = user_info.get("ip_address", "")
        audit_data["session_id"] = user_info.get("session_id", "")
        audit_data["db_type"] = self._db_type

        try:
            import urllib.request
            import urllib.error
            data = json_lib.dumps([audit_data]).encode('utf-8')
            req = urllib.request.Request(
                self._cloud_audit_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'X-API-Key': self._cloud_api_key
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json_lib.loads(response.read().decode('utf-8'))
                if result.get('status') == 'success':
                    print(f"[CloudAudit] Sent: {operation} on {table_name}")
                    return True
                else:
                    print(f"[CloudAudit] Server returned error: {result.get('error')}")
                    return False
        except urllib.error.URLError as e:
            print(f"[CloudAudit] Failed: {e}")
            return False
        except Exception as e:
            print(f"[CloudAudit] Unexpected error: {e}")
            return False

    def _derive_api_base(self) -> str:
        """Derive API base URL from cloud_audit_url.

        Expected cloud_audit_url format: https://host/api/audit/logs
        Returns: https://host

        Using split('/api/', 1) avoids the double-/api problem that occurs with
        rsplit('/', 2) when the URL already contains an /api/ segment.
        """
        if '/api/' in self._cloud_audit_url:
            return self._cloud_audit_url.split('/api/', 1)[0]
        return self._cloud_audit_url.rstrip('/')

    def _get_agent_name_from_api(self) -> str:
        """Get agent name from API key."""
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{self._derive_api_base()}/api/user/api-keys/by-key",
                headers={'X-API-Key': self._cloud_api_key},
                method='GET'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json_lib.loads(response.read().decode('utf-8'))
                if result.get('status') == 'success':
                    key_data = result.get('data', {})
                    return key_data.get('agent_name', '')
        except Exception:
            pass
        return ''

    def _get_dbpw_key_from_api(self) -> str:
        """Get dbpw_key from cloud API."""
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{self._derive_api_base()}/api/user/api-keys/by-key",
                headers={'X-API-Key': self._cloud_api_key},
                method='GET'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json_lib.loads(response.read().decode('utf-8'))
                if result.get('status') == 'success':
                    key_data = result.get('data', {})
                    return key_data.get('dbpw_key', '')
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            try:
                error_data = json_lib.loads(error_body)
                if error_data.get('membership_active') is False or '会员' in error_data.get('error', ''):
                    raise PermissionError(
                        f"Membership expired. Cannot fetch dbpw_key: {error_data.get('error', 'Please renew your membership.')}"
                    )
            except (json_lib.JSONDecodeError, ValueError):
                pass
            raise
        except Exception as e:
            if 'membership' in str(e).lower() or '会员' in str(e):
                raise PermissionError(f"Membership expired: {e}")
            pass
        return ''

    def require_cloud_api_key(self) -> bool:
        """
        Verify and sync cloud API key configuration.
        Must be called before any database operations when cloud_audit is enabled.
        """
        if not self._cloud_api_key:
            raise PermissionError(
                "cloud_api_key is not configured. Please configure cloud_api_key "
                "in your audit_config.json to enable cloud audit logging."
            )

        agent_name = self._get_agent_name_from_api()
        if not agent_name:
            raise PermissionError(
                f"API key '{self._cloud_api_key[-8:]}...' does not have an agent_name bound. "
                "Please set an agent name for this API key in sql-linker-web before proceeding."
            )

        self._update_username_config(agent_name)
        print(f"[CloudAudit] Agent name verified: {agent_name}")
        return True

    def _sync_agent_config(self):
        """Sync agent name from API Key to local config file."""
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{self._derive_api_base()}/api/user/api-keys/by-key",
                headers={'X-API-Key': self._cloud_api_key},
                method='GET'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json_lib.loads(response.read().decode('utf-8'))
                if result.get('status') == 'success':
                    key_data = result.get('data', {})
                    agent_name = key_data.get('agent_name')
                    if agent_name:
                        self._update_username_config(agent_name)
                        print(f"[CloudAudit] Synced agent name: {agent_name}")
        except Exception:
            pass

    def _update_username_config(self, username: str):
        """Update username in audit_config.json (only if username field is empty or matches)."""
        audit_json_path = AUDIT_CONFIG_HOME
        if not audit_json_path.exists():
            return

        with open(audit_json_path, "r", encoding="utf-8") as f:
            data = json_lib.load(f)

        # Only update if username is empty — do NOT blindly overwrite user-set values
        current = data.get("username", "")
        if not current:
            data["username"] = username
            with open(audit_json_path, "w", encoding="utf-8") as f:
                json_lib.dump(data, f, ensure_ascii=False, indent=2)
            self._username = username
            self._reload_audit_config()
        else:
            # Keep existing local username — do not replace with cloud value
            self._username = current

    def _reload_audit_config(self):
        """Reload audit config from file to sync in-memory state."""
        audit_json_path = AUDIT_CONFIG_HOME
        if not audit_json_path.exists():
            return

        with open(audit_json_path, "r", encoding="utf-8") as f:
            raw = json_lib.load(f)

        if self._audit:
            self._audit._user_info["user_name"] = self._username

    def fetch_api_key_info(self) -> dict:
        """
        Fetch current API key metadata from cloud (introspection only — no DB connection).

        Returns ONLY non-sensitive metadata: agent_name, key_name, id, key_masked.
        The full api_key and dbpw_key are NEVER returned to callers.

        Raises:
            PermissionError: if cloud_api_key is not configured.
            ConnectionError: on network / cloud errors.
        """
        import urllib.request
        import urllib.error

        if not self._cloud_api_key:
            raise PermissionError(
                "cloud_api_key is not configured. Set cloud_api_key in audit_config.json."
            )
        if not self._cloud_audit_url:
            raise PermissionError(
                "cloud_audit_url is not configured. Set cloud_audit_url in audit_config.json."
            )

        url = f"{self._derive_api_base()}/api/user/api-keys/by-key"
        try:
            req = urllib.request.Request(
                url,
                headers={'X-API-Key': self._cloud_api_key, 'Accept': 'application/json'},
                method='GET'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json_lib.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else ''
            try:
                err = json_lib.loads(body).get('error', body)
            except Exception:
                err = body or str(e)
            raise ConnectionError(f"Cloud rejected API key (HTTP {e.code}): {err}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Network error reaching cloud API: {e.reason}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error fetching API key info: {e}")

        if result.get('status') != 'success':
            raise ConnectionError(f"Cloud returned error: {result.get('error', 'unknown')}")
        data = result.get('data') or {}
        # Sanity check expected fields.
        for required in ('agent_name', 'api_key', 'dbpw_key', 'id'):
            if required not in data:
                raise ConnectionError(f"Cloud response missing field: {required}")

        # Return ONLY non-sensitive metadata — NEVER expose full api_key or dbpw_key
        key = data.get('api_key', '')
        masked = f"{key[:8]}...{key[-4:]}" if len(key) >= 12 else "(too short)"
        dbpw_len = len(data.get('dbpw_key', ''))
        return {
            "agent_name": data.get('agent_name', ''),
            "key_name": data.get('key_name', ''),
            "id": data.get('id', ''),
            "key_masked": masked,
            "dbpw_key": f"{dbpw_len} chars (value hidden)"
        }