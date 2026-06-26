#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from yuboto_client import YubotoClient, YubotoConfig, YubotoApiError

FINAL_STATUSES = {
    "delivered",
    "failed",
    "expired",
    "rejected",
    "undelivered",
    "invalid",
    "blacklisted",
}

API_MAX_RECIPIENTS_PER_REQUEST = 1000
SAFE_DEFAULT_BATCH_SIZE = 200

# Local state retention (override via env if needed)
MAX_SENT_LOG_LINES = int(os.getenv("YUBOTO_MAX_SENT_LOG_LINES", "5000"))
MAX_STATE_RECORDS = int(os.getenv("YUBOTO_MAX_STATE_RECORDS", "5000"))

# Privacy: do not persist sensitive payload/text by default.
YUBOTO_STORE_FULL_PAYLOAD = os.getenv("YUBOTO_STORE_FULL_PAYLOAD", "false").lower() in {"1", "true", "yes", "on"}


def _default_state_dir() -> Path:
    explicit = os.getenv("YUBOTO_STATE_DIR")
    if explicit:
        return Path(explicit).expanduser()
    xdg_state = os.getenv("XDG_STATE_HOME")
    if xdg_state:
        return Path(xdg_state).expanduser() / "openclaw" / "yuboto-omni-api"
    return Path.home() / ".local" / "state" / "openclaw" / "yuboto-omni-api"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def p(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _safe_read_json(path: Path, default: Any):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _safe_write_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _state_paths(state_dir: Path):
    return {
        "sent": state_dir / "messages_sent.jsonl",
        "state": state_dir / "messages_state.json",
        "pending": state_dir / "pending_ids.json",
    }


def _append_sent(state_dir: Path, row: Dict[str, Any]):
    paths = _state_paths(state_dir)
    paths["sent"].parent.mkdir(parents=True, exist_ok=True)
    with paths["sent"].open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _rotate_sent_log(state_dir: Path, max_lines: int = MAX_SENT_LOG_LINES):
    if max_lines <= 0:
        return
    sent = _state_paths(state_dir)["sent"]
    if not sent.exists():
        return
    try:
        lines = sent.read_text(encoding="utf-8").splitlines()
    except Exception:
        return
    if len(lines) <= max_lines:
        return
    kept = lines[-max_lines:]
    sent.write_text("\n".join(kept) + "\n", encoding="utf-8")


def _prune_state_records(state: Dict[str, Any], pending: List[str], max_records: int = MAX_STATE_RECORDS) -> Dict[str, Any]:
    if max_records <= 0 or len(state) <= max_records:
        return state

    pending_set = set([x for x in pending if x])
    keep: Dict[str, Any] = {}

    # Always keep pending entries.
    for k in pending_set:
        if k in state:
            keep[k] = state[k]

    # Fill remaining slots with most recently updated records.
    remaining = max_records - len(keep)
    if remaining <= 0:
        return keep

    candidates = []
    for k, v in state.items():
        if k in keep:
            continue
        ts = ""
        if isinstance(v, dict):
            ts = str(v.get("lastCheckedAt") or v.get("createdAt") or "")
        candidates.append((ts, k, v))

    candidates.sort(key=lambda x: x[0])
    for _, k, v in candidates[-remaining:]:
        keep[k] = v

    return keep


def _load_state(state_dir: Path):
    paths = _state_paths(state_dir)
    state = _safe_read_json(paths["state"], {})
    pending = _safe_read_json(paths["pending"], [])
    if not isinstance(state, dict):
        state = {}
    if not isinstance(pending, list):
        pending = []
    return state, pending


def _save_state(state_dir: Path, state: Dict[str, Any], pending: List[str]):
    paths = _state_paths(state_dir)
    pending = sorted(set([x for x in pending if x]))
    state = _prune_state_records(state, pending, MAX_STATE_RECORDS)
    _safe_write_json(paths["state"], state)
    _safe_write_json(paths["pending"], pending)


def _extract_message_guid(payload: Any) -> Optional[str]:
    if isinstance(payload, dict):
        for k in ["messageGuid", "MessageGuid", "id", "Id"]:
            v = payload.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    if isinstance(payload, list) and payload:
        return _extract_message_guid(payload[0])
    return None


def _extract_statuses_from_dlr(payload: Any) -> List[str]:
    out: List[str] = []
    if isinstance(payload, dict):
        channels = payload.get("Channels") or payload.get("channels") or []
        if isinstance(channels, list):
            for ch in channels:
                if isinstance(ch, dict):
                    s = ch.get("Status") or ch.get("status")
                    if isinstance(s, str) and s.strip():
                        out.append(s.strip())
    return out


def _is_final_status(statuses: List[str]) -> bool:
    if not statuses:
        return False
    return all((s or "").strip().lower() in FINAL_STATUSES for s in statuses)


def build_client(args):
    api_key = args.api_key or os.getenv("OCTAPUSH_API_KEY")
    if not api_key:
        print("ERROR: missing API key. Use --api-key or OCTAPUSH_API_KEY env var.", file=sys.stderr)
        sys.exit(2)
    cfg = YubotoConfig(api_key=api_key, base_url=args.base_url, timeout=args.timeout)
    return YubotoClient(cfg)


def _track_send(state_dir: Path, payload: Any, *, recipients: List[str], sender: str, text: str, dlr_requested: bool, callback_url: Optional[str], send_type: str = "send_sms"):
    guid = _extract_message_guid(payload)
    send_log = {
        "ts": utc_now(),
        "type": send_type,
        "messageGuid": guid,
        "recipientCount": len(recipients),
        "dlrRequested": dlr_requested,
    }
    if YUBOTO_STORE_FULL_PAYLOAD:
        send_log.update({
            "recipients": recipients,
            "sender": sender,
            "textPreview": text[:140],
            "callbackUrl": callback_url,
            "response": payload,
        })

    _append_sent(state_dir, send_log)
    _rotate_sent_log(state_dir, MAX_SENT_LOG_LINES)

    if guid:
        state, pending = _load_state(state_dir)
        state[guid] = {
            "messageGuid": guid,
            "createdAt": utc_now(),
            "lastCheckedAt": None,
            "lastStatus": "Submitted",
            "final": False,
            "recipientCount": len(recipients),
        }
        if YUBOTO_STORE_FULL_PAYLOAD:
            state[guid].update({
                "sender": sender,
                "recipients": recipients,
                "textPreview": text[:140],
                "lastDlrPayload": None,
            })
        pending.append(guid)
        _save_state(state_dir, state, pending)
    return guid


GSM_7BIT_BASIC = (
    "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ"
    " !\"#¤%&'()*+,-./0123456789:;<=>?¡"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿"
    "abcdefghijklmnopqrstuvwxyzäöñüà"
)
GSM_7BIT_EXT = "^{}\\[~]|€"


def _is_gsm7_text(text: str) -> bool:
    allowed = set(GSM_7BIT_BASIC) | set(GSM_7BIT_EXT)
    return all(ch in allowed for ch in text)


def _sms_type_and_longsms(text: str, mode: str) -> tuple[Optional[str], Optional[bool]]:
    m = (mode or "auto").strip().lower()
    if m == "unicode":
        return "unicode", True
    if m == "gsm":
        return "sms", True
    # auto
    if _is_gsm7_text(text):
        return "sms", True
    return "unicode", True


def _chunked(items: List[str], size: int) -> List[List[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def _effective_batch_size(raw: int) -> int:
    if raw <= 0:
        return SAFE_DEFAULT_BATCH_SIZE
    return min(raw, API_MAX_RECIPIENTS_PER_REQUEST)


def cmd_send_sms(args, client: YubotoClient):
    recipients = args.to or ([os.getenv("TEST_PHONENUMBER")] if os.getenv("TEST_PHONENUMBER") else None)
    if not recipients:
        print("ERROR: provide --to or set TEST_PHONENUMBER env var", file=sys.stderr)
        sys.exit(2)

    recipients = [r.strip() for r in recipients if (r or "").strip()]
    if not recipients:
        print("ERROR: recipient list is empty after normalization", file=sys.stderr)
        sys.exit(2)

    batch_size = _effective_batch_size(args.batch_size)
    batches = _chunked(recipients, batch_size)

    sms_type, sms_longsms = _sms_type_and_longsms(args.text, args.sms_encoding)

    state_dir = Path(args.state_dir)
    out = []
    for idx, batch in enumerate(batches, 1):
        payload = client.send_message(
            contacts=batch,
            sms_text=args.text,
            sms_sender=args.sender,
            sms_type=sms_type,
            sms_longsms=sms_longsms,
            dlr=(not args.no_dlr),
            callback_url=args.callback_url,
        )

        guid = _track_send(
            state_dir,
            payload,
            recipients=batch,
            sender=args.sender,
            text=args.text,
            dlr_requested=(not args.no_dlr),
            callback_url=args.callback_url,
            send_type="send_sms",
        )

        out.append({
            "batch": idx,
            "batchSize": len(batch),
            "messageGuid": guid,
            "response": payload,
        })

        if args.batch_delay_ms > 0 and idx < len(batches):
            time.sleep(args.batch_delay_ms / 1000.0)

    p({
        "totalRecipients": len(recipients),
        "batchSize": batch_size,
        "batchCount": len(batches),
        "smsEncodingRequested": args.sms_encoding,
        "smsTypeUsed": sms_type,
        "results": out,
    })


def cmd_send_csv(args, client: YubotoClient):
    csv_path = Path(args.file)
    if not csv_path.exists():
        print(f"ERROR: file not found: {csv_path}", file=sys.stderr)
        sys.exit(2)

    state_dir = Path(args.state_dir)
    sent = 0
    failed = 0
    results = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=args.delimiter)
        for i, row in enumerate(reader, 1):
            phone = (row.get(args.phone_col) or "").strip()
            text = (row.get(args.text_col) or "").strip()
            sender = (row.get(args.sender_col) or "").strip() if args.sender_col else args.sender
            sender = sender or args.sender

            if not phone or not text:
                failed += 1
                results.append({"row": i, "ok": False, "error": "missing phone/text"})
                continue

            try:
                sms_type, sms_longsms = _sms_type_and_longsms(text, args.sms_encoding)
                payload = client.send_message(
                    contacts=[phone],
                    sms_text=text,
                    sms_sender=sender,
                    sms_type=sms_type,
                    sms_longsms=sms_longsms,
                    dlr=(not args.no_dlr),
                    callback_url=args.callback_url,
                )
                guid = _track_send(
                    state_dir,
                    payload,
                    recipients=[phone],
                    sender=sender,
                    text=text,
                    dlr_requested=(not args.no_dlr),
                    callback_url=args.callback_url,
                    send_type="send_csv",
                )
                sent += 1
                results.append({"row": i, "ok": True, "messageGuid": guid, "to": phone})
            except YubotoApiError as e:
                failed += 1
                results.append({"row": i, "ok": False, "to": phone, "error": str(e), "statusCode": e.status_code})

            if args.delay_ms > 0:
                time.sleep(args.delay_ms / 1000.0)

            if args.max_rows and (i >= args.max_rows):
                break

    p({
        "file": str(csv_path),
        "sent": sent,
        "failed": failed,
        "total_processed": sent + failed,
        "results": results,
    })


def _poll_one(args, client: YubotoClient, guid: str) -> Dict[str, Any]:
    dlr_payload = client.dlr(guid)
    statuses = _extract_statuses_from_dlr(dlr_payload)
    final = _is_final_status(statuses)

    state_dir = Path(args.state_dir)
    state, pending = _load_state(state_dir)
    row = state.get(guid, {"messageGuid": guid, "createdAt": None})
    row["lastCheckedAt"] = utc_now()
    row["lastStatus"] = statuses[0] if statuses else "Unknown"
    row["allStatuses"] = statuses
    row["final"] = final
    if YUBOTO_STORE_FULL_PAYLOAD:
        row["lastDlrPayload"] = dlr_payload
    state[guid] = row

    if final:
        pending = [x for x in pending if x != guid]
    elif guid not in pending:
        pending.append(guid)

    _save_state(state_dir, state, pending)

    return {
        "messageGuid": guid,
        "statuses": statuses,
        "final": final,
        "dlr": dlr_payload,
    }


def cmd_poll_pending(args, client: YubotoClient):
    state_dir = Path(args.state_dir)
    state, pending = _load_state(state_dir)
    if not pending:
        p({"pending": 0, "checked": 0, "results": []})
        return

    results = []
    for guid in list(pending):
        try:
            results.append(_poll_one(args, client, guid))
        except YubotoApiError as e:
            results.append({"messageGuid": guid, "error": str(e), "statusCode": e.status_code})

    state2, pending2 = _load_state(state_dir)
    summary = {
        "checked": len(results),
        "pending_before": len(pending),
        "pending_after": len(pending2),
        "final_count": sum(1 for r in results if r.get("final") is True),
        "error_count": sum(1 for r in results if r.get("error")),
        "results": results,
    }
    p(summary)


def cmd_history(args):
    state_dir = Path(args.state_dir)
    sent = _state_paths(state_dir)["sent"]
    if not sent.exists():
        p([])
        return

    lines = sent.read_text(encoding="utf-8").splitlines()
    rows = []
    for ln in lines:
        try:
            rows.append(json.loads(ln))
        except Exception:
            continue

    out = rows[-args.last:]
    p(out)


def cmd_status(args):
    state_dir = Path(args.state_dir)
    state, pending = _load_state(state_dir)

    if args.id:
        row = state.get(args.id)
        if not row:
            print(f"Not found: {args.id}", file=sys.stderr)
            sys.exit(1)
        p(row)
        return

    counters: Dict[str, int] = {}
    for _, row in state.items():
        st = str(row.get("lastStatus") or "Unknown").strip() or "Unknown"
        key = st.lower()
        counters[key] = counters.get(key, 0) + 1

    p({
        "total_tracked": len(state),
        "pending": len(pending),
        "pending_ids": pending,
        "status_counts": counters,
    })


def main():
    ap = argparse.ArgumentParser(description="Yuboto Omni API CLI (core flows)")
    ap.add_argument("--api-key", help="Yuboto API key (or set OCTAPUSH_API_KEY)")
    ap.add_argument("--base-url", default="https://api.yuboto.com")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--state-dir", default=str(_default_state_dir()), help="Directory for local send/status state (default: outside skill dir)")

    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("balance")

    c = sub.add_parser("cost")
    c.add_argument("--channel", required=True, help="SMS or Viber")
    c.add_argument("--iso2")
    c.add_argument("--phonenumber")

    s = sub.add_parser("send-sms")
    s.add_argument("--to", action="append", help="Recipient contact. Repeat --to for many. Defaults to TEST_PHONENUMBER env var if omitted.")
    s.add_argument("--text", required=True)
    s.add_argument("--sender", default=os.getenv("SMS_SENDER", "Yuboto"), help="SMS sender/originator (must be approved on account)")
    s.add_argument("--batch-size", type=int, default=SAFE_DEFAULT_BATCH_SIZE, help="Recipients per API request (safe default 200, max 1000)")
    s.add_argument("--batch-delay-ms", type=int, default=250, help="Delay between batches in milliseconds")
    s.add_argument("--sms-encoding", choices=["auto", "unicode", "gsm"], default="auto", help="SMS encoding mode (default auto; unicode for Greek/Arabic/Chinese, gsm for GSM-7)")
    s.add_argument("--callback-url")
    s.add_argument("--no-dlr", action="store_true")

    sc = sub.add_parser("send-csv")
    sc.add_argument("--file", required=True, help="CSV file path")
    sc.add_argument("--phone-col", default="phonenumber", help="Column name for recipient number")
    sc.add_argument("--text-col", default="text", help="Column name for message text")
    sc.add_argument("--sender-col", help="Optional column name for sender override")
    sc.add_argument("--sender", default=os.getenv("SMS_SENDER", "Yuboto"), help="Default sender when sender-col not used")
    sc.add_argument("--delimiter", default=",", help="CSV delimiter (default ,)")
    sc.add_argument("--max-rows", type=int, default=0, help="Process only first N rows (0 = all)")
    sc.add_argument("--delay-ms", type=int, default=100, help="Delay between CSV rows in milliseconds")
    sc.add_argument("--sms-encoding", choices=["auto", "unicode", "gsm"], default="auto", help="SMS encoding mode for CSV rows")
    sc.add_argument("--callback-url")
    sc.add_argument("--no-dlr", action="store_true")

    d = sub.add_parser("dlr")
    d.add_argument("--id", required=True, help="message guid")

    x = sub.add_parser("cancel")
    x.add_argument("--id", required=True, help="message guid")

    pol = sub.add_parser("poll")
    pol.add_argument("--id", required=True, help="message guid")

    sub.add_parser("poll-pending")

    h = sub.add_parser("history")
    h.add_argument("--last", type=int, default=20)

    st = sub.add_parser("status")
    st.add_argument("--id", help="message guid")

    args = ap.parse_args()

    # Offline/read-only commands
    if args.cmd in {"history", "status"}:
        if args.cmd == "history":
            cmd_history(args)
        else:
            cmd_status(args)
        return

    client = build_client(args)

    try:
        if args.cmd == "balance":
            p(client.user_balance())
        elif args.cmd == "cost":
            p(client.cost(channel=args.channel, iso2=args.iso2, phonenumber=args.phonenumber))
        elif args.cmd == "send-sms":
            cmd_send_sms(args, client)
        elif args.cmd == "send-csv":
            cmd_send_csv(args, client)
        elif args.cmd == "dlr":
            res = _poll_one(args, client, args.id)
            p(res["dlr"])
        elif args.cmd == "cancel":
            p(client.cancel_message(args.id))
        elif args.cmd == "poll":
            p(_poll_one(args, client, args.id))
        elif args.cmd == "poll-pending":
            cmd_poll_pending(args, client)
        else:
            raise RuntimeError(f"Unknown command {args.cmd}")
    except YubotoApiError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        if e.payload is not None:
            try:
                print(json.dumps(e.payload, ensure_ascii=False, indent=2), file=sys.stderr)
            except Exception:
                print(str(e.payload), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
