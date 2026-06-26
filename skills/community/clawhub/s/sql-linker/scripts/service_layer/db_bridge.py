"""
db_bridge — Business Layer Table Bridge
Four-Layer Access Control + System Table Protection + Auto-Bootstrap
System Table (sql_audit_log): SELECT and INSERT only; UPDATE/DELETE blocked
Audit context passes through to sql-linker (data operation layer)

Security Changes v1.2.2:
- _load_linker: connection deferred to caller-initiated connect() call;
  __init__ no longer triggers any network I/O
- DBBridge gains explicit connect() method; write operations (insert/update/delete)
  and query() each call _ensure_connected() on entry, which checks credential
  approval BEFORE attempting to connect (fail-fast)
- DBBridge gains explicit_credential_approval() as public API, mirroring
  sql_linker.py change
- Removed redundant _CREDENTIAL_APPROVAL module-level dict (unused after
  connect() pre-check refactor)

Security Changes v1.1.1:
- bootstrap() adds dry_run parameter to preview files without writing
- .env placeholder comment clarifies it's a placeholder, not a real credential
- _load_linker prints connection info (host/database, masked) on init
"""

from pathlib import Path
from datetime import datetime
import json, re, yaml, sys, os

SKILL_ROOT = Path(__file__).parent.parent.parent        # service_layer → scripts → skills/sql-linker
WORKSPACE  = Path(__file__).resolve().parents[4]       # → workspace-hr

SQL_LINKER_DIR = WORKSPACE / ".sql_linker"
CONFIG_HOME    = SQL_LINKER_DIR / "config_home"
TABLE_HOME     = SQL_LINKER_DIR / "table_home"

CONFIG_YAML     = CONFIG_HOME / "config.yaml"
AUDIT_CONFIG    = CONFIG_HOME / "audit_config.json"
EXTRA_TABLES    = CONFIG_HOME / "extra_tables.json"
TABLE_DICT      = TABLE_HOME  / "table_dictionary.json"

# ── System Tables ─────────────────────────────────────────────────────────────
SYSTEM_TABLES = frozenset({"sql_audit_log"})
SYSTEM_TABLE_WRITE_OPS = frozenset({"SELECT", "INSERT"})


# ── Bootstrap ─────────────────────────────────────────────────────────────

def _get_set_env_ps1() -> str:
    """Returns the content of set_env.ps1 (Windows PowerShell)"""
    return '''[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# set_env.ps1 - Encrypted MySQL password setup (reads dbpw_key from config)
# Run: .\\set_env.ps1

$CONFIG_FILE = "$PSScriptRoot\\config_home\\config.yaml"
$envName = "mysql_pw"

Write-Host ""
Write-Host "=== MySQL Password Setup ===" -ForegroundColor Cyan
Write-Host ""

# Read dbpw_key from config
$dbpwKey = $null
if (Test-Path $CONFIG_FILE) {
    $config = Get-Content $CONFIG_FILE -Raw
    if ($config -match '(?m)^dbpw_key:\\s*(\\S+)') {
        $dbpwKey = $matches[1]
    }
}

if (-not $dbpwKey) {
    Write-Host "Error: dbpw_key not found in config.yaml" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Encryption key: $($dbpwKey.Substring(0,2))****" -ForegroundColor Gray
Write-Host ""

# Step 1: Enter password
while ($true) {
    $Password = Read-Host "Enter MySQL password"
    if ($Password -ne "") { break }
    Write-Host "Password cannot be empty" -ForegroundColor Yellow
}

# Step 2: Confirm password
while ($true) {
    $Confirm = Read-Host "Confirm password"
    if ($Confirm -eq $Password) { break }
    Write-Host "Passwords do not match, please try again" -ForegroundColor Yellow
}

# Pure PowerShell encryption (no Python required)
function ConvertTo-HmacSha256 {
    param([byte[]]$Data, [byte[]]$Key)
    $hmac = New-Object System.Security.Cryptography.HMACSHA256
    $hmac.Key = $Key
    return $hmac.ComputeHash($Data)
}

function New-RandomBytes {
    param([int]$Length)
    $bytes = New-Object byte[] $Length
    (New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes)
    return $bytes
}

$keyBytes = [System.Text.Encoding]::UTF8.GetBytes(($dbpwKey * 4).Substring(0, 24))
$pwBytes = [System.Text.Encoding]::UTF8.GetBytes($Password)

$iv = New-RandomBytes -Length 16

$encrypted = New-Object byte[] $pwBytes.Length
for ($i = 0; $i -lt $pwBytes.Length; $i++) {
    $encrypted[$i] = $pwBytes[$i] -bxor $keyBytes[$i % $keyBytes.Length] -bxor $iv[$i % 16]
}

$hmacInput = New-Object byte[] ($iv.Length + $encrypted.Length)
for ($i = 0; $i -lt $iv.Length; $i++) { $hmacInput[$i] = $iv[$i] }
for ($i = 0; $i -lt $encrypted.Length; $i++) { $hmacInput[$iv.Length + $i] = $encrypted[$i] }

$hmacTag = ConvertTo-HmacSha256 -Data $hmacInput -Key $keyBytes
$tag = New-Object byte[] 16
for ($i = 0; $i -lt 16; $i++) { $tag[$i] = $hmacTag[$i] }

$combined = New-Object byte[] ($iv.Length + $encrypted.Length + 16)
for ($i = 0; $i -lt $iv.Length; $i++) { $combined[$i] = $iv[$i] }
for ($i = 0; $i -lt $encrypted.Length; $i++) { $combined[$iv.Length + $i] = $encrypted[$i] }
for ($i = 0; $i -lt 16; $i++) { $combined[$iv.Length + $encrypted.Length + $i] = $tag[$i] }

$encryptedPw = [Convert]::ToBase64String($combined)

$pwLength = $Password.Length
$pwHead = $Password.Substring(0, [Math]::Min(2,$pwLength))
$pwTail = $Password.Substring([Math]::Max(0,$pwLength-2), [Math]::Min(2,$pwLength))
Write-Host ""
Write-Host "Password length: $pwLength" -ForegroundColor Gray
Write-Host "Preview: $pwHead$("\\"*" * [Math]::Max(0,$pwLength-4))$pwTail" -ForegroundColor Gray

[System.Environment]::SetEnvironmentVariable($envName, $encryptedPw, [System.EnvironmentVariableTarget]::User)
Write-Host ""
Write-Host "Password saved!" -ForegroundColor Green
Write-Host "Encrypted length: $($encryptedPw.Length) chars" -ForegroundColor Gray
Write-Host "Restart terminal to apply" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'''


def _get_set_env_sh() -> str:
    """Returns the content of set_env.sh (Linux/macOS Bash)"""
    return '''#!/bin/bash
# set_env.sh - Encrypted MySQL password setup (reads dbpw_key from config)
# Run: ./set_env.sh or bash set_env.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config_home/config.yaml"
ENV_NAME="mysql_pw"

echo ""
echo "=== MySQL Password Setup ==="
echo ""

# Read dbpw_key from config
DBPW_KEY=$(grep '^dbpw_key:' "$CONFIG_FILE" 2>/dev/null | awk '{print $2}')
if [ -z "$DBPW_KEY" ]; then
    echo "Error: dbpw_key not found in config.yaml" >&2
    exit 1
fi

KEY_PREVIEW="${DBPW_KEY:0:2}****"
echo "Encryption key: $KEY_PREVIEW"
echo ""

# Step 1: Enter password
while true; do
    read -sp "Enter MySQL password: " PASSWORD
    echo ""
    if [ -n "$PASSWORD" ]; then
        break
    fi
    echo "Password cannot be empty"
done

# Step 2: Confirm password
while true; do
    read -sp "Confirm password: " CONFIRM
    echo ""
    if [ "$CONFIRM" = "$PASSWORD" ]; then
        break
    fi
    echo "Passwords do not match, please try again"
done

# Pure bash encryption using OpenSSL (no Python required)
key_padded=$(printf "%s%s%s%s" "$DBPW_KEY" "$DBPW_KEY" "$DBPW_KEY" "$DBPW_KEY" | head -c 24)

# Generate random IV
iv=$(openssl rand -hex 16)
iv_bin=$(printf "%b" "$(echo "$iv" | xxd -r -p)")

encrypted=""
for ((i=0; i<${#PASSWORD}; i++)); do
    pw_byte=$(printf "%d" "'${PASSWORD:$i:1}")
    key_byte=$(printf "%d" "'${key_padded:$((i%24)):1}")
    iv_byte=$(printf "%d" "'${iv_bin:$((i%16)):1}")
    xor=$((pw_byte ^ key_byte ^ iv_byte))
    encrypted+=$(printf "\\x%02x" "$xor")
done

# HMAC covers IV + encrypted data
hmac_input=$(printf "%b%s" "$iv_bin" "$(printf "%b" "$encrypted")")
tag=$(printf "%b" "$hmac_input" | openssl dgst -sha256 -hmac "$key_padded" -binary | head -c 16 | xxd -p -c 256)

# Format: IV(16) + encrypted + HMAC(16)
combined=$(printf "%b%s%s" "$iv_bin" "$(printf "%b" "$encrypted")" "$(echo "$tag" | xxd -r -p)")
ENCRYPTED=$(printf "%b" "$combined" | base64)

PW_LEN=${#PASSWORD}
PW_HEAD="${PASSWORD:0:2}"
PW_TAIL="${PASSWORD:$((PW_LEN-2))}"
echo ""
echo "Password length: $PW_LEN"
echo "Preview: ${PW_HEAD}$(printf '*%.0s' $(seq 1 $((PW_LEN>4?PW_LEN-4:0))))${PW_TAIL}"

# Save to shell config
SHELL_RC=""
if [ -f ~/.bashrc ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f ~/.zshrc ]; then
    SHELL_RC="$HOME/.zshrc"
else
    echo "Error: Could not find ~/.bashrc or ~/.zshrc" >&2
    exit 1
fi

# Escape special chars in encrypted password
ESCAPED=$(echo "$ENCRYPTED" | sed 's/["$`\\]/\\&/g')

if grep -q "^export $ENV_NAME=" "$SHELL_RC" 2>/dev/null; then
    sed -i "s|^export $ENV_NAME=.*|export $ENV_NAME=\\"$ESCAPED\\"|" "$SHELL_RC"
else
    echo "export $ENV_NAME=\\"$ESCAPED\\"" >> "$SHELL_RC"
fi

echo ""
echo "Password saved!"
echo "Encrypted length: ${#ENCRYPTED} chars"
echo "Run 'source $SHELL_RC' or restart terminal to apply"
'''


def _bootstrap(dry_run: bool = True, explicit_confirm: bool = False) -> list:
    """
    检查并生成缺失的配置文件（幂等操作，可重复执行）
    生成顺序：目录 → config.yaml → audit_config.json → extra_tables.json → table_dictionary.json → set_env.ps1 → set_env.sh

    Security Notice:
        默认 dry_run=True，不实际写入文件。如需创建，请显式传递 dry_run=False。
        Bootstrap 会无提示地创建配置文件，在共享工作区中请谨慎使用。

        ⚠️  当 dry_run=False 时，必须同时传入 explicit_confirm=True 才能执行实际写入。
        否则写入请求被拒绝并抛出 BootstrapConfirmationRequired，以防止意外持久化。

    Args:
        dry_run: True (默认)=仅返回将创建的文件列表，不实际写入；
                 False=执行实际创建（需 explicit_confirm=True）。
        explicit_confirm: False (默认)=拒绝实际写入，即使 dry_run=False；
                         True=允许实际写入文件（与 dry_run=False 组合使用）。
    Returns:
        被创建（或将创建）的文件路径列表
    Raises:
        BootstrapConfirmationRequired: 当 dry_run=False 且 explicit_confirm=False 时
    """
    created = []


    # Fail-fast: require explicit confirmation before any write
    if not dry_run and not explicit_confirm:
        raise BootstrapConfirmationRequired(
            "[sql-linker] Bootstrap write request blocked: "
            "dry_run=False requires explicit_confirm=True to proceed. "
            "This prevents accidental file creation in shared workspaces. "
            "Call bootstrap(dry_run=False, explicit_confirm=True) to confirm."
        )

    if dry_run:
        print("[sql-linker] Bootstrap dry-run mode: 以下文件将被创建（实际不会写入）")

    # 1. Directory structure
    for d in (CONFIG_HOME, TABLE_HOME):
        if not d.exists():
            if not dry_run:
                d.mkdir(parents=True, exist_ok=True)
            created.append(str(d))

    # 2. config.yaml (default template)
    if not CONFIG_YAML.exists():
        if not dry_run:
            # Generate random 6-char encryption key
            import secrets
            import string
            chars = string.ascii_letters + string.digits
            dbpw_key = ''.join(secrets.choice(chars) for _ in range(6))
            
            CONFIG_YAML.write_text(
                "# Database connection config\n"
                "# type: mysql / postgres / sqlite\n"
                "type: mysql\n"
                "host: 127.0.0.1\n"
                "port: 3306\n"
                "database: db_dev\n"
                "user: admin\n"
                "# password_env: OS env key (stores encrypted password)\n"
                "password_env: mysql_pw\n"
                f"# dbpw_key: 6-char encryption key for password (KEEP SECRET!)\n"
                f"dbpw_key: {dbpw_key}\n"
                "read_only: true\n"
                "max_rows: 1000\n"
                "timeout: 30\n"
                "extra_tables_enabled: false\n",
                encoding="utf-8"
            )
            print(f"[sql-linker] Generated dbpw_key: {dbpw_key[:2]}**** (SAVE THIS KEY!)")
        created.append(str(CONFIG_YAML))

    # 3. audit_config.json
    if not AUDIT_CONFIG.exists():
        if not dry_run:
            with open(AUDIT_CONFIG, "w", encoding="utf-8") as f:
                json.dump({
                    "username": "HR",
                    "audit": {
                        "enabled": True,
                        "log_table": "sql_audit_log",
                        "log_select": False,
                        "mask_values": True,
                        "collect_lan_ip": False   # LAN IP auto-collection OFF by default
                    }
                }, f, indent=2)
        created.append(str(AUDIT_CONFIG))

    # 4. extra_tables.json
    if not EXTRA_TABLES.exists():
        if not dry_run:
            with open(EXTRA_TABLES, "w", encoding="utf-8") as f:
                json.dump({
                    "version": 1,
                    "enabled": False,
                    "max_extra_tables": 10,
                    "tables": []
                }, f, indent=2)
        created.append(str(EXTRA_TABLES))

    # 5. table_dictionary.json (with example table)
    if not TABLE_DICT.exists():
        if not dry_run:
            with open(TABLE_DICT, "w", encoding="utf-8") as f:
                json.dump({
                    "version": 1,
                    "tables": [
                        {
                            "table_name": "example_table",
                            "comment": "Example table (replace with actual business tables)",
                            "fields": [
                                {"name": "id",         "type": "BIGINT",      "pk": True,  "auto": True},
                                {"name": "name",        "type": "VARCHAR(64)", "pk": False, "auto": False},
                                {"name": "status",      "type": "VARCHAR(16)", "pk": False, "auto": False},
                                {"name": "created_at",  "type": "DATETIME",    "pk": False, "auto": False},
                                {"name": "updated_at",  "type": "DATETIME",    "pk": False, "auto": False}
                            ]
                        }
                    ]
                }, f, indent=2)
        created.append(str(TABLE_DICT))

    # 6. set_env.ps1 (Windows)
    SET_ENV_PS1 = SQL_LINKER_DIR / "set_env.ps1"
    if not SET_ENV_PS1.exists():
        if not dry_run:
            SET_ENV_PS1.write_text(_get_set_env_ps1(), encoding="utf-8")
        created.append(str(SET_ENV_PS1))

    # 7. set_env.sh (Linux/macOS)
    SET_ENV_SH = SQL_LINKER_DIR / "set_env.sh"
    if not SET_ENV_SH.exists():
        if not dry_run:
            SET_ENV_SH.write_text(_get_set_env_sh(), encoding="utf-8")
        created.append(str(SET_ENV_SH))

    return created


# ── Internal Utilities ──────────────────────────────────────────────────────────

def _load_dict() -> (dict, set):
    """Load main dictionary + privileged table set"""
    with open(TABLE_DICT, "r", encoding="utf-8") as f:
        dict_data = json.load(f)
    tables = {t["table_name"]: t for t in dict_data.get("tables", [])}

    extra = set()
    if EXTRA_TABLES.exists():
        with open(EXTRA_TABLES, "r", encoding="utf-8") as f:
            extra_data = json.load(f)
        if extra_data.get("enabled", False):
            extra = {t["table_name"] for t in extra_data.get("tables", [])}
    return tables, extra


def _load_extra_enabled() -> bool:
    """Check extra_tables_enabled switch in config.yaml"""
    if not CONFIG_YAML.exists():
        return False
    with open(CONFIG_YAML, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("extra_tables_enabled", False) is True


def _load_audit_config() -> dict:
    """Load audit config, return dict with collect_lan_ip defaulting to False"""
    if not AUDIT_CONFIG.exists():
        return {"collect_lan_ip": False}
    with open(AUDIT_CONFIG, "r", encoding="utf-8") as f:
        data = json.load(f)
    audit_cfg = data.get("audit", {})
    audit_cfg["collect_lan_ip"] = audit_cfg.get("collect_lan_ip", False)
    return audit_cfg


def _load_linker(user_label: str, session_id: str, collect_lan_ip: bool = False):
    """
    Import and initialize sql-linker in "pre-connect" state.

    Connection is deliberately NOT triggered here — caller must invoke
    linker.connect() AFTER any require_explicit_credential_approval check.

    os.environ writes removed — pass user_label/session_id directly to
    set_user_context_auto() to avoid cross-request contamination via
    process-wide environment variables.
    """
    sys.path.insert(0, str(SKILL_ROOT / "scripts" / "controller_layer"))
    from sql_linker import SQLLinker

    linker = SQLLinker()
    # Do NOT call linker.connect() here — let caller decide when to connect
    # after any explicit_credential_approval() call
    linker.set_collect_lan_ip(collect_lan_ip)
    linker.set_user_context_auto(user_label=user_label, session_id=session_id)
    return linker


# ── Exceptions ──────────────────────────────────────────────────────────────

class TableAccessDenied(Exception):
    """Table not in dictionary and not authorized as privileged table"""
    pass


class SystemTableWriteDenied(Exception):
    """System table prohibits UPDATE/DELETE operations"""
    pass


class BootstrapConfirmationRequired(Exception):
    """
    Raised when bootstrap(dry_run=False) is called without explicit_confirm=True.

    Prevents accidental file creation in shared workspaces. Callers must
    explicitly pass both dry_run=False AND explicit_confirm=True to proceed.
    """
    pass


# ── Main Class ───────────────────────────────────────────────────────────

class DBBridge:
    """
    Four-Layer Access Model:
    ┌──────────┬────────────────────┬──────────────────┬──────────────────┐
    │ SYSTEM   │  NORMAL (dict)     │  PRIVILEGED      │  BLOCKED         │
    ├──────────┼────────────────────┼──────────────────┼──────────────────┤
    │ SELECT   │  ✓                 │  ✓               │                  │
    │ INSERT   │  ✓                 │  ✓               │                  │
    │ UPDATE   │  ✓                 │  ✓               │                  │
    │ DELETE   │  ✓                 │  ✓               │                  │
    ├──────────┼────────────────────┼──────────────────┼──────────────────┤
    │ SELECT   │  ✓                 │  ✓               │                  │
    │ INSERT   │  ✓                 │  ✓               │                  │
    │ UPDATE   │  ✗ SystemTableWriteDenied             │                  │
    │ DELETE   │  ✗ SystemTableWriteDenied             │                  │
    └──────────┴────────────────────┴──────────────────┴──────────────────┘

    Usage:
        from skills.db_bridge.db_bridge import DBBridge
        db = DBBridge(user_label="openclaw-control-ui", session_id="agent:hr:main")
        db.explicit_credential_approval()   # if require_explicit_credential_approval=true
        db.connect()
        db.query("SELECT ...")
    """

    def __init__(self, user_label: str, session_id: str):
        self.user_label = user_label
        self.session_id = session_id

        # Load audit config to get collect_lan_ip preference
        audit_cfg = _load_audit_config()
        collect_lan_ip = audit_cfg.get("collect_lan_ip", False)

        self._linker = _load_linker(user_label, session_id, collect_lan_ip=collect_lan_ip)
        self._tables, self._extra_tables = _load_dict()
        self._extra_enabled = _load_extra_enabled()
        self._now = None
        self._connected = False   # Track connection state; connect() must be called explicitly

    def connect(self) -> bool:
        """
        Establish the database connection.

        Performs the actual network connection to the database.
        Call this after DBBridge() and any explicit_credential_approval().

        Returns:
            True if connection succeeded, False otherwise.
        """
        if self._connected and self._linker._is_connected():
            return True
        # Check credential approval BEFORE any network activity (fail-fast)
        self._linker._check_credential_approval()
        ok = self._linker.connect()
        if ok:
            self._connected = True
        return ok

    def explicit_credential_approval(self, approved: bool = True):
        """
        显式确认凭据访问权限（在 require_explicit_credential_approval=true 时必须调用）

        Args:
            approved: True=确认允许静默凭据访问；False=拒绝并阻止连接

        Raises:
            PermissionError: 当 approved=False 时
        """
        self._linker.explicit_credential_approval(approved=approved)

    # ── Access Level ────────────────────────────────────────────────────────────

    def _access_level(self, table: str) -> str:
        if table in SYSTEM_TABLES:
            return "system"
        if table in self._tables:
            return "normal"
        if self._extra_enabled and table in self._extra_tables:
            return "privileged"
        return "blocked"

    def _check_access(self, table: str):
        level = self._access_level(table)
        if level == "blocked":
            raise TableAccessDenied(
                f"Table '{table}' is not in table_dictionary.json and not in extra_tables.json. "
                f"Access denied. To enable, add it to extra_tables.json and set enabled:true."
            )
        return level

    def _check_write_op(self, table: str, op: str):
        level = self._access_level(table)
        if level == "system" and op not in SYSTEM_TABLE_WRITE_OPS:
            raise SystemTableWriteDenied(
                f"System table '{table}' does not allow {op}. "
                f"Only SELECT and INSERT are permitted on audit log table."
            )

    # ── Timestamp ─────────────────────────────────────────────────────────────

    def _now_str(self) -> str:
        if self._now is None:
            self._now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self._now

    # ── Whitelist ─────────────────────────────────────────────────────────────

    def _whitelist(self, table: str, data: dict) -> dict:
        allowed = {f["name"] for f in self._tables[table]["fields"]}
        return {k: v for k, v in data.items() if k in allowed}

    # ── Connection Guard ────────────────────────────────────────────────────────

    def _ensure_connected(self):
        """
        Ensure database is connected before any operation.

        Calls _check_credential_approval() to enforce fail-fast on
        require_explicit_credential_approval=true BEFORE any network I/O.
        """
        if self._connected and self._linker._is_connected():
            return
        self._linker._check_credential_approval()
        ok = self._linker.connect()
        if ok:
            self._connected = True
        if not ok:
            raise ConnectionError("Failed to connect to database")

    # ── INSERT ──────────────────────────────────────────────────────────────

    def insert(self, table: str, data: dict) -> int:
        self._ensure_connected()
        self._check_write_op(table, "INSERT")
        self._check_access(table)
        if table in SYSTEM_TABLES:
            return self._linker.insert(table, data)
        data = self._whitelist(table, data)
        data["created_at"] = self._now_str()
        data["updated_at"] = data["created_at"]

        # Transaction: main write + audit same transaction, audit failure rolls back business write
        self._linker.begin()
        try:
            row_id = self._linker.insert(table, data)
            self._linker.commit()
            return row_id
        except Exception as e:
            self._linker.rollback()
            raise

    # ── UPDATE ──────────────────────────────────────────────────────────────

    def update(self, table: str, data: dict, where: str,
               where_params: tuple = None) -> int:
        self._ensure_connected()
        self._check_write_op(table, "UPDATE")
        level = self._check_access(table)
        data = self._whitelist(table, data)
        data["updated_at"] = self._now_str()

        # Transaction: main write + audit same transaction, audit failure rolls back business write
        self._linker.begin()
        try:
            rows = self._linker.update(table, data, where, where_params)
            self._linker.commit()
            return rows
        except Exception as e:
            self._linker.rollback()
            raise

    # ── DELETE ──────────────────────────────────────────────────────────────

    def delete(self, table: str, where: str,
               where_params: tuple = None) -> int:
        self._ensure_connected()
        self._check_write_op(table, "DELETE")
        self._check_access(table)

        # Transaction: main write + audit same transaction, audit failure rolls back business write
        self._linker.begin()
        try:
            rows = self._linker.delete(table, where, where_params)
            self._linker.commit()
            return rows
        except Exception as e:
            self._linker.rollback()
            raise

    # ── SELECT ─────────────────────────────────────────────────────────────

    def query(self, sql: str, params: tuple = None):
        self._ensure_connected()
        table = self._extract_table(sql)
        level = self._access_level(table)
        if level == "blocked":
            raise TableAccessDenied(
                f"Table '{table}' is not in table_dictionary.json and not in extra_tables.json. "
                f"Access denied. To enable, add it to extra_tables.json and set enabled:true."
            )
        return self._linker.query(sql, params)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def tables(self) -> list:
        return list(self._tables.keys())

    def extra_tables(self) -> list:
        return sorted(self._extra_tables)

    def system_tables(self) -> list:
        return sorted(SYSTEM_TABLES)

    def bootstrap(self, dry_run: bool = True, explicit_confirm: bool = False) -> list:
        """
        Execute bootstrap, generating missing config files.
        Returns list of created file paths (empty list means all already existed).
        Idempotent; safe to call multiple times.

        Security: dry_run=False REQUIRES explicit_confirm=True to write any files.
        This prevents accidental configuration persistence in shared workspaces.

        Args:
            dry_run: If True (default), only returns file list without writing anything.
                     If False, actually creates missing files (requires explicit_confirm=True).
            explicit_confirm: Must be True alongside dry_run=False to confirm writes.
        Returns:
            list of created file paths
        Raises:
            BootstrapConfirmationRequired: when dry_run=False but explicit_confirm=False
        """
        return _bootstrap(dry_run=dry_run, explicit_confirm=explicit_confirm)

    def fields(self, table: str) -> list:
        if table in self._tables:
            return [f["name"] for f in self._tables[table]["fields"]]
        return []

    def _extract_table(self, sql: str) -> str:
        m = re.search(
            r"(?:FROM|UPDATE|INSERT\s+INTO|INTO|DELETE\s+FROM)\s+(\w+)",
            sql, re.IGNORECASE
        )
        return m.group(1) if m else ""