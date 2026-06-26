import os, sys, json, io, re, hashlib

# Force UTF-8 for console output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Patterns that indicate a live credential value (20+ char alphanumeric)
CREDENTIAL_FIELDS = re.compile(
    r'(apikey|api_key|bottoken|bot_token|auth\.token|token|secret|password|bearer|credential)',
    re.IGNORECASE
)
CREDENTIAL_VALUE = re.compile(r'[A-Za-z0-9_\-]{20,}')

def scan_for_secrets(obj, path=""):
    """Recursively scan a parsed JSON object for likely plaintext credentials."""
    findings = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            current_path = f"{path}.{k}" if path else k
            if CREDENTIAL_FIELDS.search(k):
                if isinstance(v, str) and CREDENTIAL_VALUE.match(v) and v != "REDACTED":
                    findings.append((current_path, v[:6] + "..." + v[-4:]))
            findings.extend(scan_for_secrets(v, current_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            findings.extend(scan_for_secrets(item, f"{path}[{i}]"))
    return findings

def verify_checksum(config_path):
    """Check openclaw.json SHA-256 against .stiffened lockfile."""
    stiffened_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        ".stiffened"
    )
    if not os.path.exists(stiffened_path):
        print("⚠️  No .stiffened lockfile found — integrity check skipped.")
        return

    with open(config_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest().upper()

    with open(stiffened_path, 'r') as f:
        content = f.read()

    stored = None
    for line in content.splitlines():
        if line.startswith("sha256:"):
            stored = line.split(":", 1)[1].strip().upper()
            break

    if stored is None:
        print("⚠️  No SHA-256 found in .stiffened — run stiffen.py apply to set baseline.")
    elif current_hash == stored:
        print(f"✅ Integrity check PASSED — config matches stored hash.")
    else:
        print(f"🚨 INTEGRITY ALERT: openclaw.json has been modified since last stiffening!")
        print(f"   Stored : {stored}")
        print(f"   Current: {current_hash}")
        print(f"   Action : Review changes or run stiffen.py apply to re-baseline.")

def audit():
    print("🛡️  OniBoniBot Stiff-Sec Audit v2...")
    print()

    config_path = os.path.expanduser("~/.openclaw/openclaw.json")

    # --- Config file check ---
    if not os.path.exists(config_path):
        print(f"❓ openclaw.json not found at {config_path}")
        return

    print(f"✅ Found openclaw.json at {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ ERROR: Could not parse openclaw.json: {e}")
        return

    # --- Secret scan ---
    print()
    print("🔍 Scanning for plaintext credentials...")
    findings = scan_for_secrets(config)
    if findings:
        print(f"⚠️  FOUND {len(findings)} potential plaintext credential(s):")
        for path, preview in findings:
            print(f"   [{path}] → value starts with: {preview}")
        print("   Recommendation: replace with REDACTED or move to .env")
    else:
        print("✅ No plaintext credentials detected.")

    # --- Integrity check ---
    print()
    print("🔒 Checking config integrity against .stiffened lockfile...")
    verify_checksum(config_path)

    # --- Key hardening fields check ---
    print()
    print("🔧 Checking hardening state...")

    checks = [
        ("gateway.trustedProxies", lambda c: c.get("gateway", {}).get("trustedProxies") == ["127.0.0.1"]),
        ("tools.elevated.enabled = false", lambda c: c.get("tools", {}).get("elevated", {}).get("enabled") == False),
        ("tools.exec.ask = on-miss|always", lambda c: c.get("tools", {}).get("exec", {}).get("ask") in ["on-miss", "always"]),
        ("tools.deny includes sessions_spawn", lambda c: "sessions_spawn" in c.get("tools", {}).get("deny", [])),
    ]

    for label, check_fn in checks:
        status = "✅" if check_fn(config) else "⚠️  MISSING"
        print(f"   {status}  {label}")

    print()
    print("🛡️  Audit complete.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "audit":
        audit()
    else:
        print("Usage: python audit.py audit")
