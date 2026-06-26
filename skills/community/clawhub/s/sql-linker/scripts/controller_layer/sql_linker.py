#!/usr/bin/env python3
"""
SQL-Linker: Multi-Database CRUD Tool
Supports MySQL, PostgreSQL, SQLite with built-in audit trail

Security Changes v1.2.1:
- NEW: require_explicit_credential_approval switch - when enabled, forces explicit
  approval call before connecting with password_env/password_dpapi, preventing
  silent credential auto-load attacks
- Audit config gains require_explicit_credential_approval field (default: false,
  backward-compatible). When true and password_env/password_dpapi is configured,
  connection is blocked until db.explicit_credential_approval() is called.

Security Changes v1.2.0:
- Tightened trigger: specific named table required, no generic database/SQL triggers
- Credential access documented inline: password_env / password_dpapi resolve
  silently without prompting; user must ensure trusted context before use
- Connection deferred to first actual call (lazy connect); no auto-connect on __init__
- Audit log SELECT disabled by default (log_select: false in audit_config.json)

Security Changes v1.1.1:
- set_user_context_auto() now accepts explicit parameters; uses them in preference to auto-discovery
- add set_collect_lan_ip() to control LAN IP collection via config
- connect() prints masked connection info for transparency
- _read_current_session_key no longer called automatically; session_id must come from explicit param or env var
- audit_config.json gains collect_lan_ip field (default False)
"""

import os
import sys
import re
import socket
import base64
import hashlib
import hmac

try:
    import win32crypt
except ImportError:
    win32crypt = None
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent  # controller_layer → scripts → skills/sql-linker
WORKSPACE = Path(__file__).resolve().parents[4]  # → workspace-hr
CONFIG_HOME = WORKSPACE / ".sql_linker" / "config_home" / "config.yaml"
AUDIT_CONFIG_HOME = WORKSPACE / ".sql_linker" / "config_home" / "audit_config.json"

import yaml
import json

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


class SQLLinker:
    """Multi-database connection and CRUD manager with audit support"""

    def __init__(self, config_path: str = None):
        """
        Initialize SQLLinker.

        ⚠️  Note: This method loads the config and initializes audit state,
            but does NOT connect to the database. Connection is deferred
            until the first actual database call (lazy connect).
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.connection = None
        self._db_type = None
        self._audit: SQLAudit = None
        self._collect_lan_ip = False  # Default off; set via set_collect_lan_ip() or audit_config
        self._require_approval = False    # Requires explicit approval before auto-loading credentials
        self._approval_granted = False    # Tracks whether approval has been explicitly granted
        self._validate_config()
        self._init_audit()

    def _load_config(self, config_path: str = None) -> dict:
        """
        Load config without resolving credentials.

        ⚠️  Credential Notice:
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
            config = yaml.safe_load(f)
        # Do NOT resolve password_env / password_dpapi here.
        # _resolve_password() handles both on-demand at connect() time.
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
        # Default: audit OFF, SELECT logging OFF, LAN IP OFF — safe defaults
        default_cfg = {
            "enabled": False,
            "log_table": "sql_audit_log",
            "log_select": False,       # SELECT statements NOT logged by default
            "mask_values": True,
            "collect_lan_ip": False   # LAN IP auto-collection OFF by default
        }
        user_cfg = {}
        raw = {}
        if audit_json_path.exists():
            with open(audit_json_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                user_cfg = raw.get("audit", {})
        # Merge: user_cfg overrides defaults
        audit_cfg = {**default_cfg, **user_cfg}
        self._audit = SQLAudit(config=audit_cfg)
        # Also store username for auto-context; default to "HR" if not set
        self._username = raw.get("username", "HR") if raw else "HR"
        # Sync collect_lan_ip preference from audit config
        self._collect_lan_ip = audit_cfg.get("collect_lan_ip", False)
        self._require_approval = audit_cfg.get("require_explicit_credential_approval", False)

    def init_user(self, username: str):
        """
        Register the operator username.
        Saves to .sql_linker/audit_config.json so it persists across sessions.
        """
        audit_json_path = AUDIT_CONFIG_HOME
        if audit_json_path.exists():
            with open(audit_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"username": "", "audit": {"enabled": True, "log_table": "sql_audit_log", "log_select": False, "mask_values": True, "collect_lan_ip": False}}
        data["username"] = username
        with open(audit_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._username = username
        print(f"Username saved: {username}")

    def set_collect_lan_ip(self, enabled: bool):
        """
        Enable or disable LAN IP auto-collection for audit context.
        Default is False (disabled). Set to True only if audit_config.json has collect_lan_ip:true
        or if you explicitly want LAN IP in audit records.
        """
        self._collect_lan_ip = enabled

    def _get_lan_ip(self) -> str:
        """Get LAN IP without requiring external network access."""
        try:
            # Method 1: UDP connect to localhost then query sockname (no external traffic)
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
            # Method 2: gethostbyname (always works on Windows with proper hosts file)
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip.startswith("127."):
                raise Exception("gethostbyname returned loopback")
            return ip
        except Exception:
            pass
        try:
            # Method 3: enumerate all interfaces via getaddrinfo
            for res in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET, socket.SOCK_DGRAM):
                ip = res[4][0]
                if not ip.startswith("127."):
                    return ip
        except Exception:
            pass
        return "unknown"

    def explicit_credential_approval(self, approved: bool = True):
        """
        显式确认凭据访问权限（在require_explicit_credential_approval=true时必须调用）

        Args:
            approved: True=确认允许静默凭据访问；False=拒绝并阻止连接

        Raises:
            PermissionError: 当approved=False时

        Example:
            db = DBBridge(...)
            db.explicit_credential_approval()   # 同意静默访问
            db.query("SELECT ...")              # 连接成功
        """
        if not approved:
            raise PermissionError(
                "[sql-linker] Credential access denied by operator. "
                "Connection blocked because require_explicit_credential_approval=true. "
                "Pass approved=True to explicit_credential_approval() to proceed."
            )
        self._approval_granted = True
        print("[sql-linker] Credential access explicitly approved.")

    def _check_credential_approval(self):
        """
        检查凭据确认状态，若require_explicit_credential_approval=true且使用了
        password_env/password_dpapi但未获确认，则阻止连接。
        """
        if not self._require_approval:
            return  # 未启用确认开关，正常运行
        if not self._uses_silent_credential():
            return  # 未使用静默凭据，无需确认
        if not self._approval_granted:
            raise PermissionError(
                "[sql-linker] Silent credential access requires explicit approval. "
                "Call db.explicit_credential_approval(approved=True) before connecting. "
                "Or set require_explicit_credential_approval: false in audit_config.json."
            )

    def _uses_silent_credential(self) -> bool:
        """检测当前配置是否使用了password_env或password_dpapi"""
        cfg = self.config
        return "password_env" in cfg or "password_dpapi" in cfg

    def set_user_context(self, user_name: str, user_label: str = "",
                         ip_address: str = "", session_id: str = ""):
        """Set operator identity for audit trail (manual injection)"""
        if self._audit:
            self._audit.set_user_context(user_name, user_label, ip_address, session_id)

    def set_user_context_auto(self, user_label: str = None, session_id: str = None):
        """
        Auto-detect and set operator identity for audit trail.
        Explicit parameters (user_label, session_id) take precedence over environment variables.
        LAN IP is only collected if _collect_lan_ip is True.

        Args:
            user_label: Explicit source label (preferred over OPENCLAW_LABEL env)
            session_id: Explicit session ID (preferred over OPENCLAW_SESSION env)
        """
        # Determine LAN IP — only if explicitly enabled
        lan_ip = ""
        if self._collect_lan_ip:
            lan_ip = self._get_lan_ip()

        # Determine user_name — from audit config, not auto-discovered from env
        user_name = self._username or "unknown"

        # Determine user_label — explicit param > env > fallback
        if user_label is None:
            user_label = os.environ.get("OPENCLAW_LABEL", "openclaw")
        if not user_label:
            user_label = "openclaw"

        # Determine session_id — explicit param > env > fallback
        if session_id is None:
            session_id = os.environ.get("OPENCLAW_SESSION", None)
        if not session_id:
            session_id = "unknown"

        self.set_user_context(user_name, user_label, lan_ip, session_id)

    def _extract_table(self, sql: str) -> str:
        """Extract table name from SQL for audit logging"""
        match = re.search(r"(?:FROM|UPDATE|INSERT\s+INTO|INTO)\s+(\w+)", sql, re.IGNORECASE)
        return match.group(1) if match else "unknown"

    def _mask_sql(self, sql: str) -> str:
        """Mask parameter values in SQL"""
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
            # Audit SELECT — only log when BOTH audit is enabled AND log_select is True
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

    def _execute_write(self, sql: str, params: tuple = None,
                       operation: str = "WRITE") -> int:
        if self.is_read_only():
            msg = "只读模式禁止写操作 / Read-only mode: write operation blocked"
            print(msg)
            return 0
        if not self._is_connected():
            if not self.connect():
                return 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params or ())
            self.connection.commit()
            rows = cursor.rowcount
            table_name = self._extract_table(sql)
            if self._audit and self._audit.is_enabled():
                self._audit.log(operation, table_name, sql,
                                rows_affected=rows, status="SUCCESS")
            return rows
        except Exception as e:
            self.connection.rollback()
            table_name = self._extract_table(sql)
            if self._audit and self._audit.is_enabled():
                self._audit.log(operation, table_name, sql,
                                status="FAILED", error_msg=str(e))
            print(f"Write failed: {e}")
            return 0
        finally:
            cursor.close()

    def insert(self, table: str, data: dict) -> int:
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
            return row_id
        except Exception as e:
            self.connection.rollback()
            if self._audit and self._audit.is_enabled():
                self._audit.log("INSERT", table, sql, status="FAILED", error_msg=str(e))
            print(f"Insert failed: {e}")
            return 0
        finally:
            cursor.close()

    def update(self, table: str, data: dict, where: str,
               where_params: tuple = None) -> int:
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
            return rows
        except Exception as e:
            self.connection.rollback()
            if self._audit and self._audit.is_enabled():
                self._audit.log("UPDATE", table, sql, status="FAILED", error_msg=str(e))
            print(f"Update failed: {e}")
            return 0
        finally:
            cursor.close()

    def delete(self, table: str, where: str,
               where_params: tuple = None) -> int:
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
            return rows
        except Exception as e:
            self.connection.rollback()
            if self._audit and self._audit.is_enabled():
                self._audit.log("DELETE", table, sql, status="FAILED", error_msg=str(e))
            print(f"Delete failed: {e}")
            return 0
        finally:
            cursor.close()

    def begin(self):
        """Begin a transaction (no-op if not supported)"""
        if self.connection and hasattr(self.connection, 'begin'):
            self.connection.begin()

    def commit(self):
        """Commit current transaction"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback current transaction"""
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
            # Check credential approval BEFORE any network activity
            self._check_credential_approval()
            if self._db_type == "mysql":
                self.connection = self._get_mysql_connection()
            elif self._db_type == "postgres":
                self.connection = self._get_pg_connection()
            elif self._db_type == "sqlite":
                self.connection = self._get_sqlite_connection()
            # Sync audit connection
            if self._audit:
                self._audit.set_connection(self.connection)
            # Log connection WITHOUT exposing infrastructure details (host/database/type masked)
            print(f"[sql-linker] Connected to {self._db_type}://*/* (connection established)")
            return True
        except PermissionError:
            raise   # Re-raise credential permission errors unchanged
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
        """
        Encrypt password using dbpw_key for hybrid encryption.
        
        Security: Requires both the encrypted value AND dbpw_key to decrypt.
        The encrypted password alone is useless without the key.
        
        Args:
            password: Plaintext password
            key: 6-char encryption key from config
        Returns:
            Base64-encoded encrypted password (with HMAC tag)
        """
        import secrets
        key_padded = (key * 4)[:24]
        key_bytes = key_padded.encode('utf-8')
        password_bytes = password.encode('utf-8')
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # XOR encryption
        encrypted = bytearray()
        for i, byte in enumerate(password_bytes):
            key_byte = key_bytes[i % len(key_bytes)]
            iv_byte = iv[i % len(iv)]
            encrypted.append(byte ^ key_byte ^ iv_byte)
        
        # HMAC covers IV + encrypted data
        hmac_tag = hmac.new(key_bytes, iv + bytes(encrypted), hashlib.sha256).digest()[:16]
        
        # Format: IV(16) + encrypted + HMAC(16)
        combined = iv + bytes(encrypted) + hmac_tag
        return base64.b64encode(combined).decode('utf-8')

    def _decrypt_password(self, encrypted_pw: str, key: str) -> str:
        """
        Decrypt password using dbpw_key.
        
        Args:
            encrypted_pw: Base64-encoded encrypted password (with HMAC tag)
            key: 6-char encryption key from config
        Returns:
            Decrypted plaintext password
        Raises:
            ValueError: If key is wrong or password corrupted
        """
        try:
            key_padded = (key * 4)[:24]
            key_bytes = key_padded.encode('utf-8')
            
            # Decode base64
            combined = base64.b64decode(encrypted_pw.encode('utf-8'))
            
            # Format: IV(16) + encrypted + HMAC(16)
            if len(combined) < 32:
                raise ValueError("Invalid encrypted data format")
            
            iv = combined[:16]
            encrypted = combined[16:-16]
            stored_hmac = combined[-16:]
            
            # Verify HMAC (covers IV + encrypted data)
            expected_hmac = hmac.new(key_bytes, iv + encrypted, hashlib.sha256).digest()[:16]
            if not hmac.compare_digest(stored_hmac, expected_hmac):
                raise ValueError("HMAC verification failed - wrong dbpw_key or corrupted data")
            
            # Decrypt using IV from ciphertext
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

        Evaluated at connect() time — NOT during __init__.
        Prevents credential access from being triggered merely by constructing
        SQLLinker() / DBBridge() in untrusted contexts.

        Resolution order: explicit password → password_env (decrypted with dbpw_key) → password_dpapi

        Security: 
        - password_env stores encrypted password, requires dbpw_key to decrypt
        - Both dbpw_key (in config.yaml) AND encrypted password (in env) are needed
        - Even if env is leaked, password cannot be recovered without dbpw_key
        """
        # 1. Explicit plaintext password (not recommended but always available)
        if "password" in self.config:
            return self.config["password"]
        
        # 2. password_env: read from OS environment variable, decrypt with dbpw_key
        env_key = self.config.get("password_env")
        dbpw_key = self.config.get("dbpw_key")
        
        if env_key:
            encrypted_pw = os.environ.get(env_key)
            if encrypted_pw:
                if dbpw_key:
                    # Decrypt with dbpw_key
                    return self._decrypt_password(encrypted_pw, dbpw_key)
                else:
                    # No key configured, return as-is (backward compat)
                    return encrypted_pw
        
        # 3. password_dpapi: DPAPI decryption
        dpapi_val = self.config.get("password_dpapi")
        if dpapi_val:
            if win32crypt is None:
                raise ImportError("pywin32 is required for DPAPI decryption. Install with: pip install pywin32")
            encrypted = base64.b64decode(dpapi_val.encode('utf-8'))
            decrypted = win32crypt.CryptUnprotectData(encrypted)[1]
            return decrypted.decode("utf-8")
        
        raise ValueError(
            f"Password not found: run set_env.ps1 to encrypt and save password. "
            f"Required env: '{env_key}', key: '{dbpw_key}'"
        )

    def _get_password(self) -> str:
        # Delegate to on-demand resolver (credentials resolved at connect() time)
        return self._resolve_password()