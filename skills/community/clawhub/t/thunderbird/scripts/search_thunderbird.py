#!/usr/bin/env python3
"""Search and extract messages from local Thunderbird profile storage.

Supports common Thunderbird on-disk layouts:
- Mbox folders in Mail/ and ImapMail/ (files with no extension, paired with .msf index files)
- Maildir-style directories containing cur/ and new/

Examples:
  python search_thunderbird.py --list-profiles
  python search_thunderbird.py --profile default-release --list-accounts
  python search_thunderbird.py --profile default-release --account user@example.com --folder inbox --query invoice
  python search_thunderbird.py --profile "C:/.../Profiles/xxxx.default-release" --from alice@example.com --limit 20
  python search_thunderbird.py --profile default-release --query receipt --show-body --json
"""

from __future__ import annotations

import argparse
import email
import json
import mailbox
import os
import re
import sys
from datetime import datetime, timezone
from email import policy
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set, Tuple

APPDATA = Path(os.environ.get("APPDATA", ""))
HOME = Path.home()
DEFAULT_PROFILE_ROOTS = [
    APPDATA / "Thunderbird" / "Profiles",
    HOME / ".thunderbird",
    HOME / ".mozilla" / "thunderbird",
]
SKIP_DIRS = {".mozmsgs", "cur", "new", "tmp"}
BODY_MIME_PREFIXES = ("text/plain", "text/html")
FOLDER_ALIASES = {
    "inbox": {"inbox"},
    "sent": {"sent"},
    "archive": {"archive", "archives"},
    "drafts": {"drafts"},
    "junk": {"junk"},
    "trash": {"trash"},
    "spam": {"spam"},
}


def configure_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def existing_profile_roots() -> List[Path]:
    unique_roots: List[Path] = []
    for root in DEFAULT_PROFILE_ROOTS:
        if not root:
            continue
        expanded = root.expanduser()
        if expanded.exists() and expanded not in unique_roots:
            unique_roots.append(expanded)
    return unique_roots


def list_profiles(profiles_dir: Optional[Path] = None) -> List[Path]:
    roots = [profiles_dir] if profiles_dir else existing_profile_roots()
    profiles: List[Path] = []
    for root in roots:
        if not root or not root.exists():
            continue
        for path in root.iterdir():
            if path.is_dir() and path not in profiles:
                profiles.append(path)
    return sorted(profiles)


def resolve_profile(profile_arg: Optional[str]) -> Path:
    profiles = list_profiles()
    if profile_arg:
        candidate = Path(profile_arg).expanduser()
        if candidate.exists() and candidate.is_dir():
            return candidate
        matches = [p for p in profiles if p.name == profile_arg or profile_arg.lower() in p.name.lower()]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            names = ", ".join(p.name for p in matches)
            raise SystemExit(f"Profile '{profile_arg}' is ambiguous: {names}")
        raise SystemExit(f"Profile not found: {profile_arg}")
    if len(profiles) == 1:
        return profiles[0]
    if not profiles:
        searched = ", ".join(str(root) for root in existing_profile_roots()) or ", ".join(str(root) for root in DEFAULT_PROFILE_ROOTS)
        raise SystemExit(f"No Thunderbird profiles found. Searched: {searched}")
    names = ", ".join(p.name for p in profiles)
    raise SystemExit(f"Multiple profiles found. Pass --profile. Available: {names}")


def load_prefs(profile: Path) -> str:
    prefs = profile / "prefs.js"
    if not prefs.exists():
        return ""
    return prefs.read_text(encoding="utf-8", errors="replace")


def list_accounts(profile: Path) -> List[dict]:
    prefs = load_prefs(profile)
    if not prefs:
        return []

    server_re = re.compile(r'user_pref\("mail\.server\.(server\d+)\.(name|userName|hostname|directory(?:-rel)?)", "([^"]*)"\);')
    identity_re = re.compile(r'user_pref\("mail\.identity\.(id\d+)\.useremail", "([^"]*)"\);')
    account_server_re = re.compile(r'user_pref\("mail\.account\.(account\d+)\.server", "([^"]*)"\);')
    account_identity_re = re.compile(r'user_pref\("mail\.account\.(account\d+)\.identities", "([^"]*)"\);')

    servers: Dict[str, dict] = {}
    for server_id, key, value in server_re.findall(prefs):
        servers.setdefault(server_id, {})[key] = value

    identities = {identity_id: email for identity_id, email in identity_re.findall(prefs)}
    account_servers = {account_id: server_id for account_id, server_id in account_server_re.findall(prefs)}
    account_identities = {account_id: identities_raw.split(",") for account_id, identities_raw in account_identity_re.findall(prefs)}

    results = []
    for account_id, server_id in sorted(account_servers.items()):
        server = servers.get(server_id, {})
        emails = [identities[i] for i in account_identities.get(account_id, []) if i in identities]
        directory = server.get("directory", "")
        if not directory and server.get("directory-rel"):
            rel_value = server.get("directory-rel", "")
            if rel_value.startswith("[ProfD]"):
                directory = str(profile / rel_value[len("[ProfD]"):].lstrip("/\\"))
        results.append({
            "account": account_id,
            "server": server_id,
            "email": emails[0] if emails else server.get("userName") or server.get("name") or "",
            "hostname": server.get("hostname", ""),
            "name": server.get("name", ""),
            "directory": directory,
        })
    return results


def resolve_account(profile: Path, account_arg: Optional[str]) -> Optional[dict]:
    if not account_arg:
        return None
    accounts = list_accounts(profile)
    matches = []
    needle = account_arg.lower()
    for account in accounts:
        haystacks = [account.get("email", ""), account.get("hostname", ""), account.get("name", ""), account.get("directory", "")]
        if any(needle in value.lower() for value in haystacks if value):
            matches.append(account)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        summary = ", ".join(a.get("email") or a.get("name") or a.get("hostname") or a["account"] for a in matches)
        raise SystemExit(f"Account '{account_arg}' is ambiguous: {summary}")
    raise SystemExit(f"Account not found in profile {profile.name}: {account_arg}")


def folder_matches(path: Path, folder_arg: Optional[str]) -> bool:
    if not folder_arg:
        return True
    aliases = FOLDER_ALIASES.get(folder_arg.lower(), {folder_arg.lower()})
    lowered_parts = [part.lower() for part in path.parts]
    lowered_name = path.name.lower()
    return lowered_name in aliases or any(part in aliases for part in lowered_parts)


def iter_storage_roots(profile: Path, account: Optional[dict] = None) -> Iterator[Path]:
    if account and account.get("directory"):
        directory = Path(account["directory"])
        if directory.exists():
            yield directory
            return
    for name in ("Mail", "ImapMail"):
        root = profile / name
        if root.exists():
            yield root


def is_probable_mbox(path: Path) -> bool:
    return path.is_file() and path.suffix == "" and not path.name.startswith(".") and path.stat().st_size > 0


def iter_mbox_files(profile: Path, account: Optional[dict] = None, folder: Optional[str] = None) -> Iterator[Path]:
    for root in iter_storage_roots(profile, account=account):
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for filename in filenames:
                path = Path(dirpath) / filename
                if is_probable_mbox(path) and folder_matches(path, folder):
                    yield path


def iter_maildir_dirs(profile: Path, account: Optional[dict] = None, folder: Optional[str] = None) -> Iterator[Path]:
    for root in iter_storage_roots(profile, account=account):
        for dirpath, dirnames, _ in os.walk(root):
            current = Path(dirpath)
            if (current / "cur").is_dir() and (current / "new").is_dir() and folder_matches(current, folder):
                yield current
                dirnames[:] = []


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', '_', name).strip()
    return cleaned or 'attachment.bin'


def extract_attachments(msg: email.message.Message) -> List[Tuple[str, bytes]]:
    attachments: List[Tuple[str, bytes]] = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        filename = part.get_filename()
        disposition = (part.get_content_disposition() or '').lower()
        if not filename and disposition != 'attachment':
            continue
        payload = part.get_payload(decode=True) or b''
        attachments.append((filename or 'attachment.bin', payload))
    return attachments


def unread_message_keys_from_msf(msf_path: Path) -> Set[int]:
    if not msf_path.exists():
        return set()
    data = msf_path.read_bytes()
    marker = b'(^A2='
    unread: Set[int] = set()
    start = 0
    while True:
        idx = data.find(marker, start)
        if idx == -1:
            break
        number_start = idx + len(marker)
        number_end = number_start
        while number_end < len(data) and 48 <= data[number_end] <= 57:
            number_end += 1
        if number_end > number_start:
            try:
                unread.add(int(data[number_start:number_end].decode('ascii')))
            except ValueError:
                pass
        start = number_end
    return unread


def message_to_text(msg: email.message.Message) -> str:
    parts: List[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype.startswith(BODY_MIME_PREFIXES):
                try:
                    parts.append(part.get_content())
                except Exception:
                    payload = part.get_payload(decode=True) or b""
                    parts.append(payload.decode(part.get_content_charset() or "utf-8", errors="replace"))
    else:
        try:
            return str(msg.get_content())
        except Exception:
            payload = msg.get_payload(decode=True) or b""
            return payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
    return "\n".join(parts)


def normalize(text: Optional[str]) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def parse_cli_datetime(value: str, *, end_of_day: bool = False) -> float:
    text = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        dt = datetime.fromisoformat(text).replace(tzinfo=timezone.utc)
        if end_of_day:
            dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        return dt.timestamp()
    normalized = text.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise SystemExit(f"Invalid date/time '{value}'. Use YYYY-MM-DD or ISO-8601, e.g. 2026-03-12 or 2026-03-12T08:00:00+01:00") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def day_range_utc(day_offset: int) -> tuple[float, float]:
    now = datetime.now(timezone.utc)
    target = now.date().toordinal() + day_offset
    start = datetime.fromordinal(target).replace(tzinfo=timezone.utc)
    end = start.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start.timestamp(), end.timestamp()


def date_sort_key(date_header: Optional[str]) -> float:
    if not date_header:
        return 0.0
    try:
        return parsedate_to_datetime(date_header).timestamp()
    except Exception:
        return 0.0


def message_record(
    msg: email.message.Message,
    source: str,
    include_body: bool = False,
    unread: Optional[bool] = None,
    message_key: Optional[int] = None,
    include_attachments: bool = False,
) -> Dict[str, object]:
    body = message_to_text(msg)
    attachment_names: List[str] = []
    if include_attachments:
        attachments = extract_attachments(msg)
        attachment_names = [name for name, _ in attachments]
    date_header = normalize(msg.get("date"))
    record: Dict[str, object] = {
        "source": source,
        "subject": normalize(msg.get("subject")),
        "from": normalize(msg.get("from")),
        "to": normalize(msg.get("to")),
        "date": date_header,
        "date_sort": date_sort_key(date_header),
        "message_id": normalize(msg.get("message-id")),
        "body_preview": normalize(body)[:300],
        "unread": unread,
        "message_key": message_key,
    }
    if include_attachments:
        record["has_attachments"] = bool(attachment_names)
        record["attachment_names"] = attachment_names
    if include_body:
        record["body"] = body
    return record


def matches_filters(record: Dict[str, object], args: argparse.Namespace) -> bool:
    subject_text = str(record.get("subject", ""))
    from_text = str(record.get("from", ""))
    to_text = str(record.get("to", ""))
    date_text = str(record.get("date", ""))
    body_text = str(record.get("body", "") or record.get("body_preview", ""))
    full_haystack = "\n".join([subject_text, from_text, to_text, date_text, body_text]).lower()

    if args.subject_only:
        query_haystack = subject_text.lower()
    elif args.body_only:
        query_haystack = body_text.lower()
    else:
        query_haystack = full_haystack

    if args.unread_only and record.get("unread") is not True:
        return False
    date_value = float(record.get("date_sort", 0) or 0)
    if args.since_ts is not None and date_value < args.since_ts:
        return False
    if args.until_ts is not None and date_value > args.until_ts:
        return False
    if args.query and args.query.lower() not in query_haystack:
        return False
    if args.exclude and args.exclude.lower() in full_haystack:
        return False
    if args.has_attachment and record.get("has_attachments") is not True:
        return False
    if args.attachment_name:
        attachment_names = [str(name).lower() for name in record.get("attachment_names", [])]
        if not any(args.attachment_name.lower() in name for name in attachment_names):
            return False
    if args.sender and args.sender.lower() not in from_text.lower():
        return False
    if args.recipient and args.recipient.lower() not in to_text.lower():
        return False
    if args.subject and args.subject.lower() not in subject_text.lower():
        return False
    return True


def maybe_save_attachments(msg: email.message.Message, record: Dict[str, object], args: argparse.Namespace) -> None:
    if not args.save_attachments:
        return
    output_dir = Path(args.save_attachments)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: List[str] = []
    for filename, payload in extract_attachments(msg):
        if args.attachment_name and args.attachment_name.lower() not in filename.lower():
            continue
        target = output_dir / sanitize_filename(filename)
        base = target.stem
        suffix = target.suffix
        counter = 1
        while target.exists():
            target = output_dir / f"{base}-{counter}{suffix}"
            counter += 1
        target.write_bytes(payload)
        saved_paths.append(str(target))
    if saved_paths:
        record["saved_attachments"] = saved_paths


def search_mbox(path: Path, args: argparse.Namespace) -> Iterator[Dict[str, object]]:
    include_attachments = any([args.has_attachment, args.attachment_name, args.list_attachments, args.save_attachments])
    unread_keys = unread_message_keys_from_msf(path.with_suffix(path.suffix + ".msf"))
    mbox = mailbox.mbox(path, factory=lambda f: email.message_from_binary_file(f, policy=policy.default))
    for key, msg in mbox.iteritems():
        try:
            message_key = int(key)
        except Exception:
            message_key = None
        unread = message_key in unread_keys if message_key is not None else None
        record = message_record(
            msg,
            str(path),
            include_body=args.show_body,
            unread=unread,
            message_key=message_key,
            include_attachments=include_attachments,
        )
        if matches_filters(record, args):
            if args.save_attachments:
                record["_message"] = msg
            yield record


def search_maildir(path: Path, args: argparse.Namespace) -> Iterator[Dict[str, object]]:
    include_attachments = any([args.has_attachment, args.attachment_name, args.list_attachments, args.save_attachments])
    md = mailbox.Maildir(path, factory=lambda f: email.message_from_binary_file(f, policy=policy.default), create=False)
    for key, msg in md.iteritems():
        record = message_record(
            msg,
            str(path),
            include_body=args.show_body,
            unread=None,
            message_key=None,
            include_attachments=include_attachments,
        )
        if matches_filters(record, args):
            if args.save_attachments:
                record["_message"] = msg
            yield record


def sort_value(record: Dict[str, object], sort_by: str) -> object:
    if sort_by == "date":
        return float(record.get("date_sort", 0) or 0)
    if sort_by == "from":
        return str(record.get("from", "")).lower()
    if sort_by == "subject":
        return str(record.get("subject", "")).lower()
    if sort_by == "to":
        return str(record.get("to", "")).lower()
    return float(record.get("date_sort", 0) or 0)


def print_record(record: Dict[str, object], show_body: bool = False, list_attachments: bool = False) -> None:
    print(f"Source:   {record['source']}")
    print(f"Date:     {record['date']}")
    print(f"Unread:   {record.get('unread')}")
    print(f"From:     {record['from']}")
    print(f"To:       {record['to']}")
    print(f"Subject:  {record['subject']}")
    if list_attachments:
        print(f"Attachments: {', '.join(record.get('attachment_names', [])) if record.get('attachment_names') else 'None'}")
    if record.get("saved_attachments"):
        print(f"Saved:    {', '.join(record.get('saved_attachments', []))}")
    if show_body:
        print("Body:")
        print(record.get("body", ""))
    else:
        print(f"Preview:  {record['body_preview']}")
    print("-" * 80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search local Thunderbird message storage")
    parser.add_argument("--profile", help="Profile name fragment or absolute path")
    parser.add_argument("--list-profiles", action="store_true", help="List detected Thunderbird profiles and exit")
    parser.add_argument("--list-accounts", action="store_true", help="List accounts in the selected profile and exit")
    parser.add_argument("--account", help="Account selector, usually an email address like user@example.com")
    parser.add_argument("--folder", choices=sorted(FOLDER_ALIASES.keys()), help="Restrict search to a common folder name")
    parser.add_argument("--query", help="Case-insensitive substring matched across headers and preview/body")
    parser.add_argument("--exclude", help="Exclude results containing this substring anywhere in the message summary/body")
    parser.add_argument("--subject-only", action="store_true", help="Apply --query only to the subject")
    parser.add_argument("--body-only", action="store_true", help="Apply --query only to the body/preview")
    parser.add_argument("--has-attachment", action="store_true", help="Return only messages that contain at least one attachment")
    parser.add_argument("--attachment-name", help="Return only messages with an attachment whose filename contains this substring")
    parser.add_argument("--list-attachments", action="store_true", help="Include attachment names in output")
    parser.add_argument("--save-attachments", help="Directory where matching message attachments should be saved")
    parser.add_argument("--from", dest="sender", help="Filter sender")
    parser.add_argument("--to", dest="recipient", help="Filter recipient")
    parser.add_argument("--subject", help="Filter subject")
    parser.add_argument("--show-body", action="store_true", help="Include full extracted body in results")
    parser.add_argument("--unread-only", action="store_true", help="Return only unread messages when unread state can be determined")
    parser.add_argument("--since", help="Return only messages on/after this UTC date or timestamp (YYYY-MM-DD or ISO-8601)")
    parser.add_argument("--until", help="Return only messages on/before this UTC date or timestamp (YYYY-MM-DD or ISO-8601)")
    parser.add_argument("--today", action="store_true", help="Shortcut for the current UTC day")
    parser.add_argument("--yesterday", action="store_true", help="Shortcut for the previous UTC day")
    parser.add_argument("--sort-by", choices=["date", "from", "subject", "to"], default="date", help="Sort field for returned messages")
    parser.add_argument("--sort-order", choices=["asc", "desc"], default="desc", help="Sort order for returned messages")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--limit", type=int, default=25, help="Maximum results to return")
    args = parser.parse_args()
    if args.subject_only and args.body_only:
        raise SystemExit("Use either --subject-only or --body-only, not both")
    if args.save_attachments and not args.has_attachment and not args.attachment_name:
        args.has_attachment = True
    if args.today and args.yesterday:
        raise SystemExit("Use either --today or --yesterday, not both")
    if (args.today or args.yesterday) and (args.since or args.until):
        raise SystemExit("Do not combine --today/--yesterday with --since or --until")
    if args.today:
        args.since_ts, args.until_ts = day_range_utc(0)
    elif args.yesterday:
        args.since_ts, args.until_ts = day_range_utc(-1)
    else:
        args.since_ts = parse_cli_datetime(args.since) if args.since else None
        args.until_ts = parse_cli_datetime(args.until, end_of_day=True) if args.until else None
    if args.since_ts is not None and args.until_ts is not None and args.since_ts > args.until_ts:
        raise SystemExit("--since must be earlier than or equal to --until")
    return args


def main() -> int:
    configure_stdout()
    args = parse_args()
    if args.list_profiles:
        profiles = list_profiles()
        if args.json:
            print(json.dumps([str(p) for p in profiles], indent=2))
        else:
            for profile in profiles:
                print(profile)
        return 0

    profile = resolve_profile(args.profile)

    if args.list_accounts:
        accounts = list_accounts(profile)
        if args.json:
            print(json.dumps({"profile": str(profile), "accounts": accounts}, indent=2, ensure_ascii=False))
        else:
            print(f"Profile: {profile}")
            print(f"Accounts: {len(accounts)}")
            print("=" * 80)
            for account in accounts:
                print(f"Account:   {account['account']}")
                print(f"Email:     {account['email']}")
                print(f"Hostname:  {account['hostname']}")
                print(f"Name:      {account['name']}")
                print(f"Directory: {account['directory']}")
                print("-" * 80)
        return 0

    account = resolve_account(profile, args.account)
    results: List[Dict[str, object]] = []

    for mbox_path in iter_mbox_files(profile, account=account, folder=args.folder):
        for record in search_mbox(mbox_path, args):
            results.append(record)

    for maildir_path in iter_maildir_dirs(profile, account=account, folder=args.folder):
        for record in search_maildir(maildir_path, args):
            results.append(record)

    results.sort(key=lambda record: sort_value(record, args.sort_by), reverse=(args.sort_order == "desc"))
    results = results[:args.limit]
    if args.save_attachments:
        for record in results:
            raw_message = record.pop("_message", None)
            if isinstance(raw_message, email.message.Message):
                maybe_save_attachments(raw_message, record, args)
    for record in results:
        record.pop("_message", None)
        record.pop("date_sort", None)
        record.pop("message_key", None)
        if not args.list_attachments:
            record.pop("attachment_names", None)

    if args.json:
        print(json.dumps({"profile": str(profile), "account": account, "folder": args.folder, "results": results}, indent=2, ensure_ascii=False))
    else:
        print(f"Profile: {profile}")
        print(f"Results: {len(results)}")
        print("=" * 80)
        for record in results:
            print_record(record, show_body=args.show_body, list_attachments=args.list_attachments)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
