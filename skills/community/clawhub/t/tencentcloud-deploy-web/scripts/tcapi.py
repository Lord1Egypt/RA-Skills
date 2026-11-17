#!/usr/bin/env python3
"""直接调用腾讯云 API（TC3-HMAC-SHA256 签名）。纯标准库，Python 3.8+，Windows/macOS/Linux 通用。
不依赖 tccli，也就绕开了 tccli 的 crcmod 依赖、shell 分词、参数语法等一类问题。

命令行：
    python tcapi.py <service> <Action> [Key=字符串 ...] [Key:=JSON ...] [--region R] [--profile P]
例：
    python tcapi.py sts GetCallerIdentity
    python tcapi.py dnspod DescribeRecordList Domain=example.com Subdomain=www
    python tcapi.py dnspod CreateRecord Domain=example.com SubDomain=www RecordType=A RecordLine=默认 Value=1.2.3.4 TTL:=600
    python tcapi.py lighthouse DescribeInstances --region ap-hongkong
    python tcapi.py lighthouse StopInstances InstanceIds:='["lhins-xxx"]' --region ap-hongkong
    python tcapi.py teo ModifyZoneSetting ZoneId=zone-x ForceRedirect:='{"Switch":"on","RedirectStatusCode":301}'
  Key=value  → 一律按字符串传
  Key:=json  → 按 JSON 解析（数字、布尔、数组、对象）
  --json '{...}' → 直接传整个请求体

成功：stdout 输出响应 JSON（已去掉外层 Response），退出码 0
失败：stdout 输出 {"error": {...code/message...}, "kind", "action"}（action 由 tc_error 生成），退出码 1

凭证查找顺序（不打印、不回显）：
    1. 环境变量 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY
    2. ~/.tccli/<profile>.credential（与 tccli 通用，由 setup.py 写入）
profile 默认 agent-ops，也可用环境变量 TC_PROFILE 指定。
"""
import hashlib
import hmac
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VERSIONS = {
    "sts": "2018-08-13", "dnspod": "2021-03-23", "teo": "2022-09-01", "lighthouse": "2020-03-24",
    "ssl": "2019-12-05", "tat": "2020-10-28", "domain": "2018-08-08", "billing": "2018-07-09",
    "cvm": "2017-03-12", "cam": "2019-01-16", "cdn": "2018-06-06",
}
# 只有这些服务需要 region（缺省时用 profile 里配的，或 ap-hongkong）
REGIONAL = {"lighthouse", "tat", "cvm", "sts"}
DEFAULT_PROFILE = os.environ.get("TC_PROFILE", "agent-ops")


PROFILE_RE = re.compile(r"^[A-Za-z0-9_-]{1,40}$")   # profile 名只能是简单名字，防路径穿越
SERVICE_RE = re.compile(r"^[a-z][a-z0-9]{1,30}$")      # 服务名只能是腾讯云的产品缩写


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """签名头里有凭证信息：任何重定向一律拒绝，绝不把请求带到别的地址。"""
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _check_profile(profile: str) -> str:
    if not PROFILE_RE.match(profile or ""):
        raise ValueError(f"profile 名不合法：{profile!r}（只能用字母、数字、- 和 _）")
    return profile


def cred_path(profile: str) -> Path:
    _check_profile(profile)
    return Path.home() / ".tccli" / f"{profile}.credential"


def conf_path(profile: str) -> Path:
    return Path.home() / ".tccli" / f"{profile}.configure"


def load_credential(profile: str = DEFAULT_PROFILE):
    sid, skey = os.environ.get("TENCENTCLOUD_SECRET_ID"), os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if sid and skey:
        return sid, skey, os.environ.get("TENCENTCLOUD_SESSION_TOKEN")
    p = cred_path(profile)
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("secretId") and d.get("secretKey"):
            return d["secretId"], d["secretKey"], d.get("token")
    return None


def save_credential(profile: str, secret_id: str, secret_key: str, region: str = "ap-hongkong") -> Path:
    """写成 tccli 兼容格式。
    - 文件从创建那一刻起就是 600（POSIX），没有"先写入再收权限"的窗口
    - 先写临时文件再原子替换，写到一半失败不会留下残缺的凭证
    - 目标位置是符号链接时拒绝写入
    Windows 上文件位于用户目录下，继承用户目录的默认 ACL。"""
    d = Path.home() / ".tccli"
    d.mkdir(parents=True, exist_ok=True)
    if os.name == "posix":
        os.chmod(d, 0o700)
    p = cred_path(profile)
    if p.is_symlink():
        raise OSError(f"{p} 是符号链接，拒绝写入")
    tmp = d / f".{profile}.credential.{os.getpid()}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"secretId": secret_id.strip(), "secretKey": secret_key.strip()}, f)
        os.replace(tmp, p)
    finally:
        if tmp.exists():
            tmp.unlink()
    c = conf_path(profile)
    if not c.exists():
        c.write_text(json.dumps({"_sys_param": {"region": region, "output": "json"}}), encoding="utf-8")
    return p


def default_region(profile: str) -> str:
    try:
        return json.loads(conf_path(profile).read_text(encoding="utf-8"))["_sys_param"]["region"]
    except Exception:
        return "ap-hongkong"


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def build_request(service, action, params, secret_id, secret_key, region=None, token=None,
                  version=None, timestamp=None):
    """返回 (url, headers, body)。拆出来便于离线测试签名。"""
    host = f"{service}.tencentcloudapi.com"
    ts = int(timestamp if timestamp is not None else time.time())
    date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    body = json.dumps(params, ensure_ascii=False, separators=(",", ":"))
    ct = "application/json; charset=utf-8"
    canonical = "\n".join([
        "POST", "/", "",
        f"content-type:{ct}\nhost:{host}\nx-tc-action:{action.lower()}\n",
        "content-type;host;x-tc-action",
        hashlib.sha256(body.encode("utf-8")).hexdigest(),
    ])
    scope = f"{date}/{service}/tc3_request"
    to_sign = "\n".join(["TC3-HMAC-SHA256", str(ts), scope, hashlib.sha256(canonical.encode("utf-8")).hexdigest()])
    k = _sign(_sign(_sign(("TC3" + secret_key).encode("utf-8"), date), service), "tc3_request")
    signature = hmac.new(k, to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    headers = {
        "Authorization": f"TC3-HMAC-SHA256 Credential={secret_id}/{scope}, "
                         f"SignedHeaders=content-type;host;x-tc-action, Signature={signature}",
        "Content-Type": ct, "Host": host, "X-TC-Action": action, "X-TC-Timestamp": str(ts),
        "X-TC-Version": version or VERSIONS.get(service, ""),
    }
    if region:
        headers["X-TC-Region"] = region
    if token:
        headers["X-TC-Token"] = token
    return f"https://{host}/", headers, body.encode("utf-8")


class TcError(Exception):
    def __init__(self, code, message, request_id=""):
        super().__init__(f"{code}: {message}")
        self.code, self.message, self.request_id = code, message, request_id


def call(service, action, params=None, region=None, profile=DEFAULT_PROFILE, version=None, timeout=30):
    """调用一个 API。成功返回 Response 字典（不含 Error），失败抛 TcError。"""
    cred = load_credential(profile)
    if not cred:
        raise TcError("Local.NoCredential", f"没有找到腾讯云凭证（profile={profile}），需要先运行 setup.py")
    if service in REGIONAL and not region:
        region = default_region(profile)
    return call_with(cred, service, action, params, region, version, timeout)


def call_with(cred, service, action, params=None, region=None, version=None, timeout=30):
    """用显式凭证 (secret_id, secret_key[, token]) 调用。setup.py 在保存密钥之前用它验证。"""
    sid, skey = cred[0], cred[1]
    token = cred[2] if len(cred) > 2 else None
    if service in REGIONAL and not region:
        region = "ap-hongkong"
    if not SERVICE_RE.match(service or "") or not re.match(r"^[A-Z][A-Za-z0-9]{1,80}$", action or ""):
        raise TcError("Local.BadArgs", f"服务名或接口名不合法：{service!r} {action!r}")
    url, headers, body = build_request(service, action, params or {}, sid, skey, region, token, version)
    assert url == f"https://{service}.tencentcloudapi.com/"   # 请求只发往腾讯云 API 域名
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            data = json.loads(e.read().decode("utf-8") or "{}")
        except ValueError:
            data = {}
        if "Response" not in data:      # 没有标准响应体的 HTTP 错误（网关/重定向被拒等）绝不能当成功
            raise TcError("Local.HTTPError", f"HTTP {e.code}")
    except urllib.error.URLError as e:
        raise TcError("Local.NetworkError", str(e.reason))
    except ValueError:
        raise TcError("Local.BadResponse", "响应不是合法 JSON")
    if "Response" not in data:
        raise TcError("Local.BadResponse", "响应缺少 Response 字段")
    resp = data["Response"]
    if "Error" in resp:
        raise TcError(resp["Error"].get("Code", ""), resp["Error"].get("Message", ""), resp.get("RequestId", ""))
    return resp


def error_report(e: TcError, action: str = "") -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from tc_error import classify_code
    return {"error": {"code": e.code, "message": e.message, "request_id": e.request_id},
            **classify_code(e.code, e.message, action)}


def _parse_args(argv):
    params, region, profile, version, rest = {}, None, DEFAULT_PROFILE, None, []
    it = iter(argv)
    for a in it:
        if a == "--region":
            region = next(it)
        elif a == "--profile":
            profile = next(it)
        elif a == "--version":
            version = next(it)
        elif a == "--json":
            params.update(json.loads(next(it)))
        elif ":=" in a and not a.startswith("-"):
            k, v = a.split(":=", 1)
            params[k] = json.loads(v)
        elif "=" in a and not a.startswith("-"):
            k, v = a.split("=", 1)
            params[k] = v
        else:
            rest.append(a)
    return rest, params, region, profile, version


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # Windows 控制台默认 GBK，统一输出 UTF-8
    rest, params, region, profile, version = _parse_args(sys.argv[1:] if argv is None else argv)
    if len(rest) != 2:
        print(__doc__)
        return 2
    service, action = rest
    try:
        resp = call(service, action, params, region, profile, version)
        resp.pop("RequestId", None)
        print(json.dumps(resp, ensure_ascii=False, indent=1))
        return 0
    except TcError as e:
        print(json.dumps(error_report(e, action), ensure_ascii=False, indent=1))
        return 1


if __name__ == "__main__":
    sys.exit(main())
