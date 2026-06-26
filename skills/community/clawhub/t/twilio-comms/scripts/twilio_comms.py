#!/usr/bin/env python3
"""Twilio Comms CLI — SMS, Voice, WhatsApp, Verify/2FA."""

import os
import sys
import json
import argparse
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://api.twilio.com/2010-04-01"


def get_auth():
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        print(json.dumps({
            "error": "Missing Twilio credentials",
            "setup": "export TWILIO_ACCOUNT_SID=ACxxx TWILIO_AUTH_TOKEN=xxx TWILIO_FROM_NUMBER=+1xxx"
        }))
        sys.exit(1)
    return sid, token, HTTPBasicAuth(sid, token)


def get_from():
    n = os.environ.get("TWILIO_FROM_NUMBER")
    if not n:
        print(json.dumps({"error": "TWILIO_FROM_NUMBER not set"}))
        sys.exit(1)
    return n


def api(method, path, data=None, base_override=None):
    sid, token, auth = get_auth()
    url = (base_override or f"{BASE}/Accounts/{sid}") + path
    r = requests.request(method, url, auth=auth, data=data)
    if r.status_code in (200, 201):
        return r.json()
    print(json.dumps({"error": r.status_code, "detail": r.text}))
    sys.exit(1)


# ── SMS ─────────────────────────────────────────────────

def sms_send(args):
    from_num = args.from_num or get_from()
    r = api("POST", "/Messages.json", data={
        "From": from_num, "To": args.to, "Body": args.body
    })
    print(json.dumps({
        "sid": r["sid"], "status": r["status"],
        "to": r["to"], "from": r["from"],
        "body": r["body"], "date_created": r["date_created"]
    }, indent=2))


def sms_list(args):
    sid, _, _ = get_auth()
    params = f"?PageSize={args.limit}"
    if args.to:
        params += f"&To={args.to}"
    r = api("GET", f"/Messages.json{params}")
    msgs = []
    for m in r.get("messages", []):
        msgs.append({
            "sid": m["sid"], "status": m["status"],
            "from": m["from"], "to": m["to"],
            "body": m["body"][:100], "date_sent": m["date_sent"]
        })
    print(json.dumps(msgs, indent=2))


def sms_status(args):
    r = api("GET", f"/Messages/{args.sid}.json")
    print(json.dumps({
        "sid": r["sid"], "status": r["status"],
        "from": r["from"], "to": r["to"],
        "body": r["body"], "error_code": r.get("error_code"),
        "error_message": r.get("error_message"),
        "date_sent": r["date_sent"]
    }, indent=2))


# ── VOICE ───────────────────────────────────────────────

def call_make(args):
    from_num = args.from_num or get_from()
    data = {"From": from_num, "To": args.to}
    if args.twiml_url:
        data["Url"] = args.twiml_url
    else:
        msg = args.message or "Hello, this is an automated call."
        twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Say>{msg}</Say></Response>'
        data["Twiml"] = twiml
    r = api("POST", "/Calls.json", data=data)
    print(json.dumps({
        "sid": r["sid"], "status": r["status"],
        "to": r["to"], "from": r["from"],
        "date_created": r["date_created"]
    }, indent=2))


def call_list(args):
    params = f"?PageSize={args.limit}"
    if args.status:
        params += f"&Status={args.status}"
    r = api("GET", f"/Calls.json{params}")
    calls = []
    for c in r.get("calls", []):
        calls.append({
            "sid": c["sid"], "status": c["status"],
            "from": c["from"], "to": c["to"],
            "duration": c["duration"], "start_time": c["start_time"]
        })
    print(json.dumps(calls, indent=2))


def call_status(args):
    r = api("GET", f"/Calls/{args.sid}.json")
    print(json.dumps({
        "sid": r["sid"], "status": r["status"],
        "from": r["from"], "to": r["to"],
        "duration": r["duration"], "direction": r["direction"],
        "start_time": r["start_time"], "end_time": r["end_time"]
    }, indent=2))


def call_recordings(args):
    r = api("GET", f"/Calls/{args.call_sid}/Recordings.json")
    recs = []
    for rec in r.get("recordings", []):
        recs.append({
            "sid": rec["sid"],
            "duration": rec["duration"],
            "url": f"https://api.twilio.com{rec['uri'].replace('.json', '.mp3')}",
            "date_created": rec["date_created"]
        })
    print(json.dumps(recs, indent=2))


# ── WHATSAPP ────────────────────────────────────────────

def wa_send(args):
    from_num = f"whatsapp:{args.from_num or get_from()}"
    to_num = f"whatsapp:{args.to}"
    r = api("POST", "/Messages.json", data={
        "From": from_num, "To": to_num, "Body": args.body
    })
    print(json.dumps({
        "sid": r["sid"], "status": r["status"],
        "to": r["to"], "body": r["body"]
    }, indent=2))


def wa_template(args):
    from_num = f"whatsapp:{args.from_num or get_from()}"
    to_num = f"whatsapp:{args.to}"
    body = args.template
    if args.params:
        for i, param in enumerate(args.params.split(",")):
            body = body.replace(f"{{{{{i+1}}}}}", param.strip())
    r = api("POST", "/Messages.json", data={
        "From": from_num, "To": to_num, "Body": body
    })
    print(json.dumps({
        "sid": r["sid"], "status": r["status"],
        "to": r["to"], "body": r["body"]
    }, indent=2))


# ── VERIFY ──────────────────────────────────────────────

def get_verify_sid():
    vsid = os.environ.get("TWILIO_VERIFY_SERVICE_SID")
    if not vsid:
        print(json.dumps({"error": "TWILIO_VERIFY_SERVICE_SID not set"}))
        sys.exit(1)
    return vsid


def verify_send(args):
    vsid = get_verify_sid()
    sid, token, auth = get_auth()
    r = requests.post(
        f"https://verify.twilio.com/v2/Services/{vsid}/Verifications",
        auth=auth,
        data={"To": args.to, "Channel": args.channel}
    )
    if r.status_code in (200, 201):
        data = r.json()
        print(json.dumps({
            "sid": data["sid"], "to": data["to"],
            "channel": data["channel"], "status": data["status"]
        }, indent=2))
    else:
        print(json.dumps({"error": r.status_code, "detail": r.text}))
        sys.exit(1)


def verify_check(args):
    vsid = get_verify_sid()
    sid, token, auth = get_auth()
    r = requests.post(
        f"https://verify.twilio.com/v2/Services/{vsid}/VerificationCheck",
        auth=auth,
        data={"To": args.to, "Code": args.code}
    )
    if r.status_code in (200, 201):
        data = r.json()
        print(json.dumps({
            "sid": data["sid"], "to": data["to"],
            "status": data["status"], "valid": data["status"] == "approved"
        }, indent=2))
    else:
        print(json.dumps({"error": r.status_code, "detail": r.text}))
        sys.exit(1)


# ── CLI ─────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Twilio Comms CLI")
    sub = p.add_subparsers(dest="cmd")

    # sms-send
    ss = sub.add_parser("sms-send")
    ss.add_argument("--to", required=True)
    ss.add_argument("--body", required=True)
    ss.add_argument("--from", dest="from_num")

    # sms-list
    sl = sub.add_parser("sms-list")
    sl.add_argument("--limit", type=int, default=20)
    sl.add_argument("--to")

    # sms-status
    sst = sub.add_parser("sms-status")
    sst.add_argument("--sid", required=True)

    # call-make
    cm = sub.add_parser("call-make")
    cm.add_argument("--to", required=True)
    cm.add_argument("--message")
    cm.add_argument("--twiml-url", dest="twiml_url")
    cm.add_argument("--from", dest="from_num")

    # call-list
    cll = sub.add_parser("call-list")
    cll.add_argument("--limit", type=int, default=20)
    cll.add_argument("--status")

    # call-status
    cst = sub.add_parser("call-status")
    cst.add_argument("--sid", required=True)

    # call-recordings
    cr = sub.add_parser("call-recordings")
    cr.add_argument("--call-sid", required=True, dest="call_sid")

    # wa-send
    ws = sub.add_parser("wa-send")
    ws.add_argument("--to", required=True)
    ws.add_argument("--body", required=True)
    ws.add_argument("--from", dest="from_num")

    # wa-template
    wt = sub.add_parser("wa-template")
    wt.add_argument("--to", required=True)
    wt.add_argument("--template", required=True)
    wt.add_argument("--params")
    wt.add_argument("--from", dest="from_num")

    # verify-send
    vs = sub.add_parser("verify-send")
    vs.add_argument("--to", required=True)
    vs.add_argument("--channel", default="sms", choices=["sms", "voice", "email"])

    # verify-check
    vc = sub.add_parser("verify-check")
    vc.add_argument("--to", required=True)
    vc.add_argument("--code", required=True)

    args = p.parse_args()
    dispatch = {
        "sms-send": sms_send, "sms-list": sms_list, "sms-status": sms_status,
        "call-make": call_make, "call-list": call_list,
        "call-status": call_status, "call-recordings": call_recordings,
        "wa-send": wa_send, "wa-template": wa_template,
        "verify-send": verify_send, "verify-check": verify_check,
    }
    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
