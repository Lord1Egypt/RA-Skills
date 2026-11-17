"""Local storage and the fixed TypeSafe transport. Python 3.10+, no dependencies."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3
import time
import urllib.error
import urllib.request
import uuid

VERSION = "0.1.0"
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MAX_BYTES = 2_000_000


class XjevError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def require(ok, message, code="invalid_input"):
    if not ok:
        raise XjevError(code, message)


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, allow_nan=False, sort_keys=True)


def digest(obj):
    return hashlib.sha256(dump(obj).encode()).hexdigest()


def parse(text):
    try:
        return json.loads(text, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, TypeError):
        raise XjevError("invalid_json", "需要有效 JSON；不接受 NaN / Infinity。") from None


def uid(prefix):
    return prefix + "_" + uuid.uuid4().hex[:16]


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def home():
    return Path(os.environ.get("XJEV_HOME", str(Path.home()/".local/share/xjev"))).expanduser()


def private_dir(path):
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.chmod(0o700)


def config():
    path = home()/"config.json"
    if not path.exists():
        return {}
    try:
        data = parse(path.read_text())
        require(isinstance(data, dict), "本机配置格式无效。", "invalid_config")
        return data
    except OSError:
        raise XjevError("invalid_config", "无法读取本机配置。") from None


def key():
    value = os.environ.get("TYPESAFE_API_KEY") or config().get("api_key")
    if not value:
        raise XjevError("setup_required", "请运行 xjev.py setup，在本机页面配置 Jev API key；不要把 key 发进聊天。")
    require(isinstance(value, str) and 1 <= len(value) <= 4096 and not any(c.isspace() for c in value),
            "API key 格式无效，请在本机配置页重新输入。", "invalid_key")
    return value


def save_key(value):
    require(isinstance(value, str) and value and not any(c.isspace() for c in value), "API key 格式无效。")
    private_dir(home())
    data = config()
    data.update(api_key=value, verified_at=now())
    target = home()/"config.json"
    temp = home()/(".config-"+uuid.uuid4().hex)
    fd = os.open(temp, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(dump(data))
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.unlink()


def status():
    c = config()
    env = bool(os.environ.get("TYPESAFE_API_KEY"))
    return {"version": VERSION, "configured": env or bool(c.get("api_key")),
            "key_source": "environment" if env else ("local_config" if c.get("api_key") else None),
            "verified_at": None if env else c.get("verified_at"),
            "state_dir": str(home()), "endpoint": ENDPOINT,
            "setup_command": "python3 <skill>/scripts/xjev.py setup"}


def no_key_in(value):
    """Reject rather than persist accidentally included credentials."""
    secrets = [os.environ.get("TYPESAFE_API_KEY"), config().get("api_key")]
    encoded = dump(value)
    require(all(not secret or secret not in encoded for secret in secrets),
            "输入含当前 API key，已拒绝写入或发送；请移除凭据。", "secret_in_input")


def text_field(value, label):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 40000, label+" 必须是非空文本。")


def finite(value, lo, hi):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and lo <= value <= hi


def validate_questions(questions):
    require(isinstance(questions, dict) and 1 <= len(questions) <= 128, "questions 需要 1–128 个问题。")
    for qid, q in questions.items():
        text_field(qid, "question id")
        require(isinstance(q, dict) and q.get("type") in ("score", "choice", "noul"), "问题类型必须是 score/choice/noul。")
        require(isinstance(q.get("instructions"), (str, dict, list)) and bool(q["instructions"]), "问题必须有 instructions。")
        criteria = q.get("criteria")
        if q["type"] == "score":
            require(isinstance(criteria, list) and 2 <= len(criteria) <= 10, "Score 需要 2–10 个档位。")
            require(all(isinstance(c, (str, dict, list)) and bool(c) for c in criteria), "档位描述不能为空。")
        elif q["type"] == "choice":
            require(isinstance(criteria, dict) and 2 <= len(criteria) <= 255, "Choice 需要 2–255 个选项。")
            require(all(isinstance(k, str) and k for k in criteria), "Choice 选项名称无效。")
            require(all(v is None or isinstance(v, (str, dict, list)) for v in criteria.values()), "Choice 描述类型无效。")
        elif criteria is not None:
            require(isinstance(criteria, dict) and set(criteria) == {"true", "false"}, "Noul criteria 需要 true/false 描述。")


def validate_response(questions, data):
    require(isinstance(data, dict) and isinstance(data.get("model"), str) and data["model"], "响应缺少模型版本。", "invalid_response")
    answers = data.get("answers")
    require(isinstance(answers, dict) and set(answers) == set(questions), "响应问题集合不匹配。", "invalid_response")
    for qid, q in questions.items():
        a = answers[qid]
        require(isinstance(a, dict) and a.get("type") == q["type"], "响应类型不匹配。", "invalid_response")
        if q["type"] == "noul":
            require(finite(a.get("noul"), 0, 1), "Noul 概率无效。", "invalid_response")
            continue
        expected = set(q["criteria"]) if q["type"] == "choice" else {str(i) for i in range(len(q["criteria"]))}
        probs = a.get("probabilities")
        require(isinstance(probs, dict) and set(probs) == expected, "概率项与请求不匹配。", "invalid_response")
        require(all(finite(p, 0, 1) for p in probs.values()) and abs(sum(probs.values())-1) <= 0.001,
                "概率分布无效；不会静默归一化。", "invalid_response")
        require(finite(a.get("confidence"), 0, 1), "缺少有效 confidence。", "invalid_response")
        if q["type"] == "choice":
            chosen = a.get("choice")
            require(chosen in expected and probs[chosen] >= max(probs.values())-0.001, "Choice 与概率不一致。", "invalid_response")
        else:
            mean = sum(int(i)*p for i,p in probs.items())
            require(finite(a.get("score"), 0, len(expected)-1) and abs(a["score"]-mean) <= 0.011,
                    "Score 与档位分布不一致。", "invalid_response")
            require(isinstance(a.get("legend"), dict) and a["legend"] == {str(i):v for i,v in enumerate(q["criteria"])},
                    "Score legend 与请求标准不匹配。", "invalid_response")
    return data


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(state, questions, model="jev-latest", api_key=None):
    require(isinstance(state, (str, dict, list)), "state 必须是文本、对象或数组。")
    validate_questions(questions)
    text_field(model, "model")
    payload = {"model":model, "state":state, "questions":questions}
    secret = api_key or key()
    require(secret not in dump(payload), "请求包含 API key，已拒绝发送。", "secret_in_input")
    body = dump(payload).encode()
    require(len(body) <= MAX_BYTES, "请求过大，请缩小相关上下文。")
    opener = urllib.request.build_opener(NoRedirect())
    for attempt in range(3):
        req = urllib.request.Request(ENDPOINT, data=body, headers={"Authorization":"Bearer "+secret,
                                    "Content-Type":"application/json", "User-Agent":"xjev/"+VERSION})
        try:
            with opener.open(req, timeout=20) as response:
                raw = response.read(MAX_BYTES+1)
            require(len(raw) <= MAX_BYTES, "API 响应过大。", "invalid_response")
            data = parse(raw)
            require(secret not in dump(data), "API 响应包含凭据，已丢弃。", "invalid_response")
            return validate_response(questions, data)
        except urllib.error.HTTPError as e:
            code = e.code
            e.close()  # Never print server bodies: they may echo request data.
            if code in (429, 529) and attempt < 2:
                time.sleep(2**attempt)
                continue
            messages = {401:"Jev API key 无效，请重新配置。", 403:"Jev 访问被拒绝，请检查账户权限。",
                        422:"Jev 拒绝请求格式；请检查问题标准。", 429:"Jev 限流，请稍后再试。", 529:"Jev 暂时过载，请稍后再试。"}
            raise XjevError("http_"+str(code), messages.get(code, "Jev 请求失败（HTTP "+str(code)+"）。")) from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise XjevError("network_error", "无法连接 Jev；未产生有效判断。检查网络后再试。") from None


def probe(api_key=None):
    result = request("The supplied value is exactly 7.", {"check":{"type":"noul", "instructions":"The supplied value is 7."}}, api_key=api_key)
    return {"connected":True, "model":result["model"], "verified_at":now()}


class Store:
    def __init__(self):
        private_dir(home())
        target = home()/"decisions.sqlite3"
        fd = os.open(target, os.O_CREAT|os.O_RDWR, 0o600)
        os.close(fd)
        target.chmod(0o600)
        self.db = sqlite3.connect(target, timeout=10)
        self.db.execute("CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT, scope TEXT, data TEXT)")

    def close(self):
        self.db.close()

    def put(self, kind, data):
        no_key_in(data)
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO records VALUES (?,?,?,?)", (data["id"],kind,data.get("scope", ""),dump(data)))
        return data

    def get(self, id, kind=None):
        row = self.db.execute("SELECT kind,data FROM records WHERE id=?", (id,)).fetchone()
        require(row is not None and (kind is None or row[0] == kind), "记录不存在。", "not_found")
        return parse(row[1])

    def all(self, kind, scope=None):
        if scope is None:
            rows = self.db.execute("SELECT data FROM records WHERE kind=? ORDER BY rowid", (kind,)).fetchall()
        else:
            rows = self.db.execute("SELECT data FROM records WHERE kind=? AND scope=? ORDER BY rowid", (kind,scope)).fetchall()
        return [parse(r[0]) for r in rows]
