#!/usr/bin/env python3
"""
Ecovacs Robot Control - Core client script
Usage:
  python3 ecovacs.py login <phone> <password>
  python3 ecovacs.py devices
  python3 ecovacs.py cmd <did> <cmdName> [json_body]
  python3 ecovacs.py clean <did> [start|pause|resume|stop]
  python3 ecovacs.py charge <did>
  python3 ecovacs.py battery <did>
  python3 ecovacs.py status <did>

Session stored in ~/.ecovacs_session.json
"""
import sys, json, hashlib, uuid, time, os
from urllib import request as urlreq

SESSION_FILE = os.path.expanduser("~/.ecovacs_session.json")
BASE_URL = "https://api-app.dc-cn.cn.ecouser.net"

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def gen_resource(seed=None):
    """Generate resource. Use a fixed seed for stable resource across logins."""
    r = md5(seed or str(uuid.uuid4()))[:7]
    ck = md5(r[-3:])[-1]
    return f"ANDROID{r}E{ck}"

def post(url, data):
    req = urlreq.Request(url, json.dumps(data).encode(),
                         headers={"Content-Type": "application/json"})
    return json.loads(urlreq.urlopen(req, timeout=15).read())

def load_session(phone=None, password=None):
    """Load session, auto-refresh token if expired."""
    session = {}
    if os.path.exists(SESSION_FILE):
        session = json.load(open(SESSION_FILE))
    token = session.get("token", "")
    if token:
        try:
            import base64
            parts = token.split(".")
            pad = parts[1] + "=" * (4 - len(parts[1]) % 4)
            payload = json.loads(base64.urlsafe_b64decode(pad))
            if time.time() < payload.get("exp", 0) - 300:
                return session
        except Exception:
            pass
    stored_phone = session.get("phone") or phone
    stored_pass = session.get("password") or password
    if stored_phone and stored_pass:
        print("⚠️  Token expired, re-logging in...")
        return login(stored_phone, stored_pass)
    if not token:
        raise Exception("No session. Run: python3 ecovacs.py login <phone> <password>")
    return session

def save_session(s):
    json.dump(s, open(SESSION_FILE, "w"), indent=2)

def login(phone, password):
    """Login with phone and plaintext or md5 password."""
    # Reuse existing resource if session already has one (avoids server throttle on new resources)
    existing = {}
    if os.path.exists(SESSION_FILE):
        existing = json.load(open(SESSION_FILE))
    resource = existing.get("resource") or gen_resource(phone)  # stable resource per phone
    pwd_md5 = password if len(password) == 32 and all(c in '0123456789abcdef' for c in password) else md5(password)
    resp = post(f"{BASE_URL}/api/users/user.do", {
        "todo": "ITLogin", "me": phone,
        "password": pwd_md5,
        "resource": resource, "last": "",
        "country": "CN", "org": "ECOCN", "edition": "ECOGLOBLE"
    })
    if resp.get("result") != "ok":
        raise Exception(f"Login failed: {resp}")
    session = {"token": resp["token"], "userid": resp["userId"], "resource": resource,
               "phone": phone, "password": pwd_md5}
    save_session(session)
    print(f"✅ Login ok | userid={session['userid']} | resource={resource}")
    return session

def get_devices(session):
    auth = {"token": session["token"], "resource": session["resource"],
            "userid": session["userid"], "with": "users", "realm": "ecouser.net"}
    resp = post(f"{BASE_URL}/api/appsvr/app.do", {
        "userid": session["userid"], "todo": "GetGlobalDeviceList",
        "defaultLang": "zh", "lang": "en", "appVer": "1.5.0",
        "platform": "Android", "channel": "c_test", "vendor": "",
        "auth": auth, "aliliving": True, "app_robotconfig": False
    })
    return resp.get("devices", [])

def send_cmd(session, device, cmd_name, body_data=None):
    mqs = device.get("service", {}).get("mqs", "api-ngiot.dc-cn.cn.ecouser.net")
    auth = {"token": session["token"], "resource": session["resource"],
            "userid": session["userid"], "with": "users", "realm": "ecouser.net"}
    payload = {
        "header": {"pri": 1, "ts": str(int(time.time() * 1000)), "tzm": 480, "ver": "0.0.1"},
        "body": {"data": body_data or {}}
    }
    resp = post(f"https://{mqs}/api/iot/devmanager.do", {
        "rn": cmd_name, "payloadType": "j", "payload": payload,
        "auth": auth,
        "toType": device["class"],
        "toRes": device["resource"],
        "toId": device["did"],
        "td": "q", "cmdName": cmd_name
    })
    return resp

def find_device(devices, did):
    for d in devices:
        if d["did"] == did or d.get("nick") == did or d.get("name") == did:
            return d
    raise Exception(f"Device not found: {did}")

def print_devices(devices):
    print(f"{'#':<3} {'Status':<8} {'Name':<30} {'Nick':<20} {'did'}")
    print("-" * 100)
    for i, d in enumerate(devices):
        status = "🟢 online" if d.get("status") == 1 else "⭕ offline"
        print(f"{i:<3} {status:<8} {d.get('deviceName',''):<30} {str(d.get('nick','')):<20} {d['did']}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "login":
        login(args[1], args[2])

    elif cmd == "devices":
        session = load_session()
        devices = get_devices(session)
        print_devices(devices)

    elif cmd == "cmd":
        session = load_session()
        devices = get_devices(session)
        device = find_device(devices, args[1])
        body = json.loads(args[3]) if len(args) > 3 else {}
        result = send_cmd(session, device, args[2], body)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "battery":
        session = load_session()
        devices = get_devices(session)
        device = find_device(devices, args[1])
        result = send_cmd(session, device, "getBattery")
        data = result.get("resp", {}).get("body", {}).get("data", {})
        print(f"🔋 Battery: {data.get('value')}% {'(low)' if data.get('isLow') else ''}")

    elif cmd == "status":
        session = load_session()
        devices = get_devices(session)
        device = find_device(devices, args[1])
        result = send_cmd(session, device, "getCleanInfo_V2")
        data = result.get("resp", {}).get("body", {}).get("data", {})
        print(f"📊 State: {data.get('state')} | trigger: {data.get('trigger')}")
        cs = data.get("cleanState")
        if cs:
            print(f"   type: {cs.get('content',{}).get('type')} | motion: {cs.get('motionState')}")

    elif cmd == "clean":
        session = load_session()
        devices = get_devices(session)
        device = find_device(devices, args[1])
        act = args[2] if len(args) > 2 else "start"
        body = {"act": act}
        if act == "start":
            body["content"] = {"type": "auto", "count": 1}
        result = send_cmd(session, device, "clean_V2", body)
        code = result.get("resp", {}).get("body", {}).get("code")
        print(f"{'✅' if code == 0 else '❌'} clean_V2 act={act} | code={code}")

    elif cmd == "charge":
        session = load_session()
        devices = get_devices(session)
        device = find_device(devices, args[1])
        result = send_cmd(session, device, "charge", {"act": "go"})
        code = result.get("resp", {}).get("body", {}).get("code")
        print(f"{'✅' if code == 0 else '❌'} charge go | code={code}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
