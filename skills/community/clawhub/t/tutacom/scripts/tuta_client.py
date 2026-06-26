#!/usr/bin/env python3
"""
Tuta (Tutanota) email client for OpenClaw.
Handles login, inbox listing, reading, and sending emails via the undocumented Tuta REST API.
All email content is end-to-end encrypted; this client handles the crypto locally.

Base URL: https://app.tuta.com/rest/
Reference: https://github.com/nenaddi/tutanota_client (Rust)
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import struct
import sys
import time
import urllib.parse
from datetime import datetime

import bcrypt
import requests
from Crypto.Cipher import AES

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "https://app.tuta.com/rest"
CLIENT_ID = "OpenClaw"
BCRYPT_COST = 8
MAC_SIZE = 32
INBOX_FOLDER_TYPE = "1"  # system folder type for Inbox

# ---------------------------------------------------------------------------
# Crypto helpers  (mirrors the Rust reference client's crypto.rs)
# ---------------------------------------------------------------------------

def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def derive_passphrase_key(password: str, salt: bytes, kdf_version: int = 0) -> bytes:
    """
    Derive the 128-bit passphrase key.
    kdf_version 0 = bcrypt (legacy), 1 = argon2id (newer accounts).
    """
    if kdf_version == 0:
        pw_hash = _sha256(password.encode("utf-8"))
        # bcrypt with cost 8, produces 24-byte output; take first 16
        raw = bcrypt.kdf(
            password=pw_hash,
            salt=salt,
            desired_key_bytes=24,
            rounds=BCRYPT_COST,
        )
        return raw[:16]
    else:
        # Argon2id for newer accounts
        import argon2
        ph = argon2.low_level.hash_secret_raw(
            secret=password.encode("utf-8"),
            salt=salt,
            time_cost=4,
            memory_cost=32 * 1024,
            parallelism=1,
            hash_len=32,
            type=argon2.low_level.Type.ID,
        )
        return ph[:16]


def auth_verifier(passphrase_key: bytes) -> str:
    """base64url-no-pad of SHA-256(passphrase_key)."""
    h = _sha256(passphrase_key)
    return base64.urlsafe_b64encode(h).rstrip(b"=").decode("ascii")


def _sub_keys(session_key: bytes):
    """Derive AES cipher sub-key and HMAC sub-key from a 16-byte session key."""
    h = _sha256(session_key)
    return h[:16], h[16:]  # cipher_key, mac_key


def decrypt_key(encryption_key: bytes, encrypted_key: bytes) -> bytes:
    """
    Decrypt a 16-byte key that was encrypted with AES-128-ECB + XOR 0x88 padding.
    This matches the Rust client's decrypt_key().
    """
    if len(encryption_key) == 16 and len(encrypted_key) == 16:
        cipher = AES.new(encryption_key, AES.MODE_ECB)
        decrypted = bytearray(cipher.decrypt(encrypted_key))
        for i in range(len(decrypted)):
            decrypted[i] ^= 0x88
        return bytes(decrypted)
    elif len(encryption_key) == 16 and len(encrypted_key) == 32:
        # 256-bit key encrypted — AES-128-ECB on two blocks with XOR 0x88
        cipher = AES.new(encryption_key, AES.MODE_ECB)
        block1 = bytearray(cipher.decrypt(encrypted_key[:16]))
        block2 = bytearray(cipher.decrypt(encrypted_key[16:]))
        for i in range(16):
            block1[i] ^= 0x88
            block2[i] ^= 0x88
        return bytes(block1) + bytes(block2)
    else:
        raise ValueError(f"Unexpected key lengths: enc_key={len(encryption_key)}, msg={len(encrypted_key)}")


def encrypt_key(encryption_key: bytes, key_to_encrypt: bytes) -> bytes:
    """Encrypt a 16-byte key with AES-128-ECB + XOR 0x88."""
    data = bytearray(key_to_encrypt)
    for i in range(len(data)):
        data[i] ^= 0x88
    cipher = AES.new(encryption_key, AES.MODE_ECB)
    return cipher.encrypt(bytes(data))


def decrypt_with_mac(session_key: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt AES-128-CBC with HMAC-SHA256 verification.
    Format: [1-byte flag][16-byte IV][encrypted...][32-byte MAC]
    """
    if len(ciphertext) < 1 + 16 + MAC_SIZE:
        raise ValueError("Ciphertext too short")

    cipher_key, mac_key = _sub_keys(session_key)

    # Verify MAC over everything between flag byte and MAC
    message_without_mac = ciphertext[1 : len(ciphertext) - MAC_SIZE]
    expected_mac = ciphertext[len(ciphertext) - MAC_SIZE :]
    computed_mac = hmac.new(mac_key, message_without_mac, hashlib.sha256).digest()
    if not hmac.compare_digest(computed_mac, expected_mac):
        raise ValueError("MAC verification failed")

    iv = message_without_mac[:16]
    encrypted_data = message_without_mac[16:]

    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_data)

    # Remove PKCS7 padding
    pad_len = decrypted[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError(f"Invalid PKCS7 padding: {pad_len}")
    return decrypted[:-pad_len]


def encrypt_with_mac(session_key: bytes, plaintext: bytes) -> bytes:
    """
    Encrypt with AES-128-CBC + HMAC-SHA256.
    Returns: [1-byte flag=1][16-byte IV][encrypted...][32-byte MAC]
    """
    cipher_key, mac_key = _sub_keys(session_key)

    iv = os.urandom(16)

    # PKCS7 padding
    pad_len = 16 - (len(plaintext) % 16)
    padded = plaintext + bytes([pad_len] * pad_len)

    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)

    # Build message: IV + encrypted
    message_without_mac = iv + encrypted

    mac = hmac.new(mac_key, message_without_mac, hashlib.sha256).digest()

    return b"\x01" + message_without_mac + mac


def generate_session_key() -> bytes:
    """Generate a random 16-byte AES session key."""
    return os.urandom(16)


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

class TutaClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json;charset=utf-8",
            "v": "84",  # API model version
        })
        self.access_token = None
        self.user_id = None
        self.passphrase_key = None
        self.user_group_key = None
        self.mail_group_key = None
        self.mail_group_id = None
        self.mail_address = None

    # -- Salt --
    def fetch_salt(self, email: str) -> tuple:
        """Returns (salt_bytes, kdf_version)."""
        body = json.dumps({"_format": "0", "mailAddress": email})
        url = f"{self.base_url}/sys/saltservice?_body={urllib.parse.quote(body)}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        salt = base64.b64decode(data["salt"])
        kdf_version = int(data.get("kdfVersion", "0"))
        return salt, kdf_version

    # -- Login --
    def login(self, email: str, password: str) -> dict:
        """Full login flow: salt → key derivation → session creation → user fetch → key decryption."""
        self.mail_address = email

        # 1. Fetch salt
        salt, kdf_version = self.fetch_salt(email)

        # 2. Derive passphrase key
        self.passphrase_key = derive_passphrase_key(password, salt, kdf_version)

        # 3. Create session
        verifier = auth_verifier(self.passphrase_key)
        payload = {
            "_format": "0",
            "accessKey": None,
            "authToken": None,
            "authVerifier": verifier,
            "clientIdentifier": CLIENT_ID,
            "mailAddress": email,
            "recoverCodeVerifier": None,
            "user": None,
        }
        resp = self.session.post(f"{self.base_url}/sys/sessionservice", json=payload)
        resp.raise_for_status()
        session_data = resp.json()
        self.access_token = session_data["accessToken"]
        self.user_id = session_data["user"]
        self.session.headers["accessToken"] = self.access_token

        # 4. Fetch user to get group keys
        resp = self.session.get(f"{self.base_url}/sys/user/{self.user_id}")
        resp.raise_for_status()
        user_data = resp.json()

        # 5. Decrypt user group key
        user_group_enc = base64.b64decode(user_data["userGroup"]["symEncGKey"])
        self.user_group_key = decrypt_key(self.passphrase_key, user_group_enc)

        # 6. Find mail membership (groupType "5") and decrypt mail group key
        for m in user_data["memberships"]:
            if m["groupType"] == "5":
                self.mail_group_id = m["group"]
                enc_key = base64.b64decode(m["symEncGKey"])
                self.mail_group_key = decrypt_key(self.user_group_key, enc_key)
                break

        if not self.mail_group_key:
            raise RuntimeError("Could not find mail group membership")

        return self._session_dict()

    def _session_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "user_id": self.user_id,
            "mail_address": self.mail_address,
            "passphrase_key": base64.b64encode(self.passphrase_key).decode() if self.passphrase_key else None,
            "user_group_key": base64.b64encode(self.user_group_key).decode() if self.user_group_key else None,
            "mail_group_key": base64.b64encode(self.mail_group_key).decode() if self.mail_group_key else None,
            "mail_group_id": self.mail_group_id,
            "created_at": datetime.utcnow().isoformat(),
        }

    def load_session(self, session_file: str):
        """Restore session from a JSON file."""
        with open(session_file) as f:
            data = json.load(f)
        self.access_token = data["access_token"]
        self.user_id = data["user_id"]
        self.mail_address = data.get("mail_address")
        self.passphrase_key = base64.b64decode(data["passphrase_key"]) if data.get("passphrase_key") else None
        self.user_group_key = base64.b64decode(data["user_group_key"]) if data.get("user_group_key") else None
        self.mail_group_key = base64.b64decode(data["mail_group_key"]) if data.get("mail_group_key") else None
        self.mail_group_id = data.get("mail_group_id")
        self.session.headers["accessToken"] = self.access_token

    def save_session(self, session_file: str):
        os.makedirs(os.path.dirname(session_file) or ".", exist_ok=True)
        with open(session_file, "w") as f:
            json.dump(self._session_dict(), f, indent=2)
        os.chmod(session_file, 0o600)

    # -- Mailbox navigation --
    def _get_inbox_mail_list(self) -> str:
        """Navigate: mail group → mailboxgrouproot → mailbox → system folders → inbox mails list ID."""
        # mailboxgrouproot
        resp = self.session.get(f"{self.base_url}/tutanota/mailboxgrouproot/{self.mail_group_id}")
        resp.raise_for_status()
        mailbox_id = resp.json()["mailbox"]

        # mailbox → system folders
        resp = self.session.get(f"{self.base_url}/tutanota/mailbox/{mailbox_id}")
        resp.raise_for_status()
        mailbox_data = resp.json()

        # Get the folders list ID — handle both old and new API shapes
        if "systemFolders" in mailbox_data and mailbox_data["systemFolders"]:
            folders_list = mailbox_data["systemFolders"]["folders"]
        elif "folders" in mailbox_data and mailbox_data["folders"]:
            # Newer API: folders is a reference ID
            folders_ref = mailbox_data["folders"]
            if isinstance(folders_ref, str):
                # Fetch the mail folder ref
                resp2 = self.session.get(f"{self.base_url}/tutanota/mailfolderref/{folders_ref}")
                resp2.raise_for_status()
                folders_list = resp2.json()["folders"]
            elif isinstance(folders_ref, dict):
                folders_list = folders_ref.get("folders", folders_ref)
            else:
                folders_list = folders_ref
        else:
            raise RuntimeError(f"Cannot find folders in mailbox response: {json.dumps(mailbox_data)[:500]}")

        # List folders
        resp = self.session.get(
            f"{self.base_url}/tutanota/mailfolder/{folders_list}",
            params={"start": "------------", "count": "100", "reverse": "false"},
        )
        resp.raise_for_status()
        folders = resp.json()

        # Find inbox (folderType "1")
        for folder in folders:
            if folder.get("folderType") == INBOX_FOLDER_TYPE:
                return folder["mails"]

        # Fallback: first folder is typically inbox
        if folders:
            return folders[0]["mails"]
        raise RuntimeError("Could not find inbox folder")

    # -- Inbox --
    def list_inbox(self, count: int = 20) -> list:
        """List inbox emails with decrypted subjects."""
        mails_list = self._get_inbox_mail_list()

        resp = self.session.get(
            f"{self.base_url}/tutanota/mail/{mails_list}",
            params={"start": "zzzzzzzzzzzz", "count": str(count), "reverse": "true"},
        )
        resp.raise_for_status()
        mails = resp.json()

        results = []
        for mail in mails:
            try:
                owner_enc_sk = base64.b64decode(mail["_ownerEncSessionKey"])
                session_key = decrypt_key(self.mail_group_key, owner_enc_sk)
                subject = decrypt_with_mac(session_key, base64.b64decode(mail["subject"])).decode("utf-8")
            except Exception as e:
                subject = f"[decrypt error: {e}]"

            sender_addr = mail.get("sender", {}).get("address", "unknown")
            mail_id = mail["_id"]
            if isinstance(mail_id, list):
                mail_id_str = f"{mail_id[0]}/{mail_id[1]}"
            else:
                mail_id_str = str(mail_id)

            results.append({
                "id": mail_id_str,
                "subject": subject,
                "sender": sender_addr,
                "date": mail.get("receivedDate", ""),
                "unread": mail.get("unread") == "1",
                "body_ref": mail.get("body"),
                "_ownerEncSessionKey": mail.get("_ownerEncSessionKey"),
            })

        return results

    # -- Read --
    def read_mail(self, mail_id: str, owner_enc_session_key_b64: str = None) -> dict:
        """
        Read a single email. mail_id can be "listId/elementId" or just element ID.
        If owner_enc_session_key_b64 is provided, use it directly; otherwise fetch the mail first.
        """
        # If we have a slash, split into list/element
        if "/" in mail_id:
            list_id, element_id = mail_id.split("/", 1)
            # Fetch the specific mail
            resp = self.session.get(f"{self.base_url}/tutanota/mail/{list_id}/{element_id}")
            resp.raise_for_status()
            mail = resp.json()
        else:
            raise ValueError("mail_id must be in format 'listId/elementId'. Use the id from inbox listing.")

        # Decrypt session key
        owner_enc_sk = base64.b64decode(mail["_ownerEncSessionKey"])
        session_key = decrypt_key(self.mail_group_key, owner_enc_sk)

        # Decrypt subject
        try:
            subject = decrypt_with_mac(session_key, base64.b64decode(mail["subject"])).decode("utf-8")
        except:
            subject = "[could not decrypt]"

        # Decrypt sender name
        try:
            sender_name = decrypt_with_mac(session_key, base64.b64decode(mail["sender"]["name"])).decode("utf-8")
        except:
            sender_name = ""

        sender_addr = mail.get("sender", {}).get("address", "")

        # Fetch and decrypt body
        body_id = mail.get("body")
        body_text = ""
        if body_id:
            try:
                resp = self.session.get(f"{self.base_url}/tutanota/mailbody/{body_id}")
                resp.raise_for_status()
                body_data = resp.json()
                encrypted_body = base64.b64decode(body_data["text"])
                body_text = decrypt_with_mac(session_key, encrypted_body).decode("utf-8")
            except Exception as e:
                body_text = f"[body decrypt error: {e}]"

        return {
            "subject": subject,
            "sender": f"{sender_name} <{sender_addr}>" if sender_name else sender_addr,
            "date": mail.get("receivedDate", ""),
            "body": body_text,
            "unread": mail.get("unread") == "1",
        }

    # -- Send (to external recipients) --
    def send_mail(self, to: str, subject: str, body: str, sender_name: str = "") -> dict:
        """
        Send an email to an EXTERNAL (non-Tuta) recipient.
        Creates a draft then sends it. Non-confidential mode (no password protection).
        """
        session_key = generate_session_key()

        # Encrypt fields with session key
        enc_subject = base64.b64encode(encrypt_with_mac(session_key, subject.encode("utf-8"))).decode()
        enc_body = base64.b64encode(encrypt_with_mac(session_key, body.encode("utf-8"))).decode()
        enc_sender_name = base64.b64encode(encrypt_with_mac(session_key, sender_name.encode("utf-8"))).decode()
        enc_confidential = base64.b64encode(encrypt_with_mac(session_key, b"0")).decode()
        enc_recipient_name = base64.b64encode(encrypt_with_mac(session_key, b"")).decode()

        # Encrypt session key with group keys
        owner_enc_sk = base64.b64encode(encrypt_key(self.mail_group_key, session_key)).decode()
        sym_enc_sk = base64.b64encode(encrypt_key(self.user_group_key, session_key)).decode()

        # Create draft
        draft_payload = {
            "_format": "0",
            "conversationType": "0",
            "ownerEncSessionKey": owner_enc_sk,
            "ownerKeyVersion": "0",
            "previousMessageId": None,
            "symEncSessionKey": sym_enc_sk,
            "symKeyVersion": "0",
            "draftData": {
                "_id": "xxxxxx",
                "bodyText": enc_body,
                "compressedBodyText": None,
                "confidential": enc_confidential,
                "method": "0",
                "senderMailAddress": self.mail_address,
                "senderName": enc_sender_name,
                "subject": enc_subject,
                "addedAttachments": [],
                "bccRecipients": [],
                "ccRecipients": [],
                "removedAttachments": [],
                "replyTos": [],
                "toRecipients": [
                    {
                        "_id": "xxxxxx",
                        "mailAddress": to,
                        "name": enc_recipient_name,
                    }
                ],
            },
        }

        resp = self.session.post(f"{self.base_url}/tutanota/draftservice", json=draft_payload)
        resp.raise_for_status()
        draft_result = resp.json()

        # Extract draft ID
        draft_id = draft_result.get("draft")
        if isinstance(draft_id, list) and len(draft_id) == 2:
            draft_list_id, draft_element_id = draft_id
        elif isinstance(draft_id, str):
            draft_list_id = ""
            draft_element_id = draft_id
        else:
            return {"status": "draft_created", "draft": draft_result, "note": "Could not parse draft ID to send"}

        # Send the draft
        send_payload = {
            "_format": "0",
            "bucketEncMailSessionKey": None,
            "calendarMethod": "0",
            "language": "en",
            "mailSessionKey": None,
            "plaintext": False,
            "senderNameUnencrypted": None,
            "sessionEncEncryptionAuthStatus": None,
            "attachmentKeyData": [],
            "internalRecipientKeyData": [],
            "mail": [draft_list_id, draft_element_id],
            "secureExternalRecipientKeyData": [],
            "symEncInternalRecipientKeyData": [],
        }

        resp = self.session.post(f"{self.base_url}/tutanota/sendservice", json=send_payload)
        resp.raise_for_status()

        return {"status": "sent", "to": to, "subject": subject}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Tuta (Tutanota) email client")
    sub = parser.add_subparsers(dest="command", required=True)

    # login
    p_login = sub.add_parser("login", help="Login and create session file")
    p_login.add_argument("--email", required=True)
    p_login.add_argument("--password", required=True)
    p_login.add_argument("--session-file", default="/tmp/tuta_session.json")

    # inbox
    p_inbox = sub.add_parser("inbox", help="List inbox emails")
    p_inbox.add_argument("--session-file", default="/tmp/tuta_session.json")
    p_inbox.add_argument("--count", type=int, default=20)

    # read
    p_read = sub.add_parser("read", help="Read a specific email")
    p_read.add_argument("--mail-id", required=True, help="Mail ID in format listId/elementId")
    p_read.add_argument("--session-file", default="/tmp/tuta_session.json")

    # send
    p_send = sub.add_parser("send", help="Send an email to external recipient")
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)
    p_send.add_argument("--sender-name", default="")
    p_send.add_argument("--session-file", default="/tmp/tuta_session.json")

    args = parser.parse_args()
    client = TutaClient()

    if args.command == "login":
        result = client.login(args.email, args.password)
        client.save_session(args.session_file)
        print(json.dumps({"status": "ok", "user_id": result["user_id"], "session_file": args.session_file}, indent=2))

    elif args.command == "inbox":
        client.load_session(args.session_file)
        mails = client.list_inbox(count=args.count)
        print(json.dumps(mails, indent=2, ensure_ascii=False))

    elif args.command == "read":
        client.load_session(args.session_file)
        mail = client.read_mail(args.mail_id)
        print(json.dumps(mail, indent=2, ensure_ascii=False))

    elif args.command == "send":
        client.load_session(args.session_file)
        result = client.send_mail(
            to=args.to,
            subject=args.subject,
            body=args.body,
            sender_name=args.sender_name,
        )
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
