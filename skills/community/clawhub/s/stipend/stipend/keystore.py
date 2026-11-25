"""Non-custodial key management.

The private key is generated locally and stored as a Web3 Secret Storage (V3)
keystore — the same encrypted format geth and MetaMask use. We deliberately do
NOT hand-roll any cryptography: key generation, encryption and signing all come
from `eth-account`, which is audited and widely used.

The passphrase comes from the environment, never from a file. That matters:
an attacker who reads the keystore file still cannot spend, and an agent whose
`read` tool is abused leaks a useless encrypted blob rather than a spendable
key.
"""

import json
import os
import stat

from .config import KEYSTORE_FILE, PASSPHRASE_ENV, ensure_dirs


class KeystoreError(RuntimeError):
    pass


def _account_module():
    try:
        from eth_account import Account
        return Account
    except ImportError as e:
        raise KeystoreError(
            "eth-account is not installed. Run: pip install eth-account"
        ) from e


PASSPHRASE_FILE_NOTE = (
    "Stored locally because no passphrase was supplied. This protects a leaked "
    "BACKUP of the keystore, but not an attacker who can already read this "
    "directory. Your real protection in that case is the spending caps and the "
    "destination allowlist. Keep the balance small."
)


def generate_passphrase():
    """Create a passphrase and store it beside the keystore.

    This exists so an agent can install unattended. Be honest about what it
    costs: a passphrase sitting next to the file it encrypts is not protecting
    you from someone who can read both. It still protects a leaked backup, and
    it keeps the key out of plaintext. Where a human is available, supply
    STIPEND_PASSPHRASE from the environment instead — that is strictly better.
    """
    import secrets
    from .config import CONFIG_DIR, ensure_dirs
    ensure_dirs()
    path = CONFIG_DIR / "passphrase"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    pw = secrets.token_urlsafe(32)
    path.write_text(pw, encoding="utf-8")
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except (OSError, NotImplementedError):
        pass
    return pw


def stored_passphrase():
    from .config import CONFIG_DIR
    path = CONFIG_DIR / "passphrase"
    if path.exists():
        try:
            return path.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return ""


def get_passphrase(allow_missing=False):
    pw = os.environ.get(PASSPHRASE_ENV, "") or stored_passphrase()
    if not pw and not allow_missing:
        raise KeystoreError(
            f"{PASSPHRASE_ENV} is not set.\n"
            "Set it before any wallet operation, e.g.\n"
            f"  export {PASSPHRASE_ENV}='a long random passphrase'\n"
            "Store it in your process environment or a secret manager — never "
            "in the agent's workspace, and never in a file the agent can read."
        )
    if pw and len(pw) < 12:
        raise KeystoreError(
            f"{PASSPHRASE_ENV} is too short (minimum 12 characters). "
            "This passphrase is the only thing standing between a stolen "
            "keystore file and your funds."
        )
    return pw


def exists():
    return KEYSTORE_FILE.exists()


def _write_keystore(payload):
    ensure_dirs()
    KEYSTORE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    try:
        os.chmod(KEYSTORE_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 0600
    except (OSError, NotImplementedError):
        pass  # Windows has no POSIX modes; ACLs govern instead


def create(overwrite=False, auto_passphrase=False):
    """Generate a new wallet. Returns the address. Private key never leaves here.

    `auto_passphrase` lets an agent install with no human present, at the cost
    described in generate_passphrase().
    """
    if exists() and not overwrite:
        raise KeystoreError(
            f"A wallet already exists at {KEYSTORE_FILE}.\n"
            "Refusing to overwrite it — that would permanently destroy access "
            "to any funds it holds. Use --overwrite only if you are certain, "
            "and back up the existing file first."
        )
    Account = _account_module()
    if auto_passphrase and not os.environ.get(PASSPHRASE_ENV):
        generate_passphrase()
    pw = get_passphrase()
    acct = Account.create()
    _write_keystore(Account.encrypt(acct.key, pw))
    return acct.address


def import_key(private_key, overwrite=False):
    """Import an existing private key (hex, with or without 0x)."""
    if exists() and not overwrite:
        raise KeystoreError(
            f"A wallet already exists at {KEYSTORE_FILE}. Use --overwrite to replace it."
        )
    Account = _account_module()
    pw = get_passphrase()
    key = private_key.strip()
    if not key.startswith("0x"):
        key = "0x" + key
    try:
        acct = Account.from_key(key)
    except Exception as e:
        raise KeystoreError(f"Not a valid private key: {e}") from e
    _write_keystore(Account.encrypt(acct.key, pw))
    return acct.address


def address():
    """Public address. Does NOT require the passphrase."""
    if not exists():
        raise KeystoreError("No wallet yet. Run: stipend wallet create")
    try:
        data = json.loads(KEYSTORE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise KeystoreError(f"Keystore is unreadable or corrupt: {e}") from e
    addr = data.get("address", "")
    if not addr:
        raise KeystoreError("Keystore has no address field — file may be corrupt.")
    return addr if addr.startswith("0x") else "0x" + addr


def load_account():
    """Decrypt and return a signing account. Requires the passphrase.

    Callers should hold the result for as short a time as possible and never
    log, print or serialise it.
    """
    if not exists():
        raise KeystoreError("No wallet yet. Run: stipend wallet create")
    Account = _account_module()
    pw = get_passphrase()
    try:
        data = json.loads(KEYSTORE_FILE.read_text(encoding="utf-8"))
        key = Account.decrypt(data, pw)
    except ValueError as e:
        raise KeystoreError(
            "Could not decrypt the keystore — the passphrase is probably wrong. "
            f"({e})"
        ) from e
    except (OSError, json.JSONDecodeError) as e:
        raise KeystoreError(f"Keystore is unreadable or corrupt: {e}") from e
    return Account.from_key(key)


def export_warning():
    return (
        "Exporting a private key removes every protection this kit provides. "
        "Anyone who sees it can drain the wallet instantly and irreversibly. "
        "Never paste it into a chat, a file in the agent workspace, or a log."
    )
