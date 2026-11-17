#!/usr/bin/env python3
"""蜀宁 OA 公共工具 — 登录认证、工时管理、报销查询与节假日检查"""

import base64
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time

import requests

MAX_RETRIES = 3
REQ_TIMEOUT = 10
STATE_MAP = {
    "-1": "已撤回",
    "10": "草稿",
    "20": "审批中",
    "30": "已审批",
}
FEE_STATE_MAP = {
    "-1": "已撤回",
    "0": "已作废",
    "10": "待提交",
    "20": "审批中",
    "30": "已通过",
    "40": "已驳回",
}
FEE_TYPE_MAP = {
    "1": "报销",
    "2": "备用金",
    "3": "补助",
    "4": "外采",
    "5": "其它",
    "6": "备用金抵扣",
}
REIMBURSE_COMPANY_MAP = {
    "1": "蜀宁",
    "2": "天域智慧",
}


def is_workday(date_str):
    """检查是否为工作日（格式：YYYY-MM-DD）。

    优先使用 chinese_calendar；若当前 Python 环境未安装该依赖，
    则降级为“周一到周五视为工作日、周末视为非工作日”的保守判断，
    避免脚本因环境不一致直接崩溃。
    """
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

    try:
        import chinese_calendar

        return chinese_calendar.is_workday(date_obj)
    except ModuleNotFoundError:
        print(
            "[warn] 当前 Python 环境未安装 chinese_calendar，已降级为周末/工作日基础判断；如需中国法定调休的精确结果，请使用已安装该依赖的虚拟环境。",
            file=sys.stderr,
        )
        return date_obj.weekday() < 5


ENC_KEY_FILE = os.path.expanduser("~/.openclaw/workspace/.cache/oa_enc_key")


def get_enc_key():
    """返回 AES 密钥（环境变量 OA_ENC_KEY 优先，其次密钥文件）；都没有返回 None。"""
    key = os.environ.get("OA_ENC_KEY")
    if not key and os.path.exists(ENC_KEY_FILE):
        with open(ENC_KEY_FILE) as f:
            key = f.read().strip()
    return key or None


def openssl_cipher(mode, data):
    """用 openssl aes-256-cbc 加/解密 bytes；mode 取 "-e" 或 "-d"。"""
    key = get_enc_key()
    if not key:
        raise ValueError(f"找不到密钥（环境变量 OA_ENC_KEY 或 {ENC_KEY_FILE}）")
    if mode not in ('-e', '-d'):
        raise ValueError('无效加解密模式')
    encoded = key.encode('utf-8')
    # Keep below OpenSSL's fd passphrase line-buffer boundary; never truncate.
    if not encoded or len(encoded) > 1022 or any(c in encoded for c in (b'\n', b'\r', b'\x00')):
        raise ValueError('密钥必须为不超过1022 UTF-8字节的单行文字')
    from runtime_bootstrap import runtime_environment
    read_fd, write_fd = os.pipe()
    try:
        os.write(write_fd, encoded + b'\n')
        os.close(write_fd)
        write_fd = None
        result = subprocess.run(
            ["openssl", "aes-256-cbc", mode, "-a", "-pbkdf2", "-pass", f"fd:{read_fd}"],
            input=data, capture_output=True, timeout=10,
            pass_fds=(read_fd,), env=runtime_environment(),
        )
    finally:
        os.close(read_fd)
        if write_fd is not None:
            os.close(write_fd)
    if result.returncode != 0:
        raise ValueError(f"openssl {mode} 失败: {result.stderr.decode(errors='replace')}")
    return result.stdout


def decrypt_file(enc_path):
    """解密 .enc 文件，返回 bytes"""
    with open(enc_path, "rb") as fh:
        return openssl_cipher("-d", fh.read())


def read_credentials_raw(path):
    """读取凭证文件（自动处理 .enc 加密文件）"""
    path = os.path.expanduser(path)
    if path.endswith(".enc"):
        return decrypt_file(path).decode("utf-8")
    enc_path = path + ".enc"
    if not os.path.exists(path) and os.path.exists(enc_path):
        return decrypt_file(enc_path).decode("utf-8")
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_credentials(path, require_project=False):
    """解析凭证文件，返回 (账号, 密码, base_url[, projectId, projectName])"""
    creds = {}
    content = read_credentials_raw(path)
    for line in content.splitlines():
        line = line.strip()
        m = re.match(r"[-*]?\s*\*+\s*(账号|密码|Base URL|登录地址|默认项目ID|默认项目名称)\s*\*+[::]：?\s*(.+)", line)
        if not m:
            m = re.match(r"[-*]?\s*(账号|密码|Base URL|登录地址|默认项目ID|默认项目名称)\s*[:：]\s*(.+)", line)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            if "账号" in key:
                creds["账号"] = val
            elif "密码" in key:
                creds["密码"] = val
            elif "Base URL" in key or "登录地址" in key:
                creds["base"] = val.rstrip("/login").rstrip("/")
            elif "默认项目ID" in key:
                creds["projectId"] = val
            elif "默认项目名称" in key:
                creds["projectName"] = val
    if not creds.get("账号") or not creds.get("密码"):
        raise ValueError(f"凭据文件缺少账号或密码: {path}")
    if require_project:
        return creds["账号"], creds["密码"], creds.get("base"), creds.get("projectId"), creds.get("projectName")
    return creds["账号"], creds["密码"], creds.get("base")


def resolve_base_url(base_url, override=None):
    """优先使用命令行覆盖，否则使用凭据中的 base_url。"""
    if override:
        return override.rstrip("/")
    if base_url:
        return base_url.rstrip("/")
    raise ValueError("请通过 --base-url 参数或凭据文件指定 OA 系统地址")


def solve_captcha(img_bytes):
    """ddddocr 识别算术验证码（原图 + 放大灰度 + 二值反色 三重策略）"""
    import ddddocr
    from PIL import Image, ImageOps

    ocr = ddddocr.DdddOcr(show_ad=False)

    def _try(src):
        text = ocr.classification(src)
        expr = re.sub(r"[^0-9+\-*/]", "", text).rstrip("+-*/")
        if not expr or len(expr) > 32:
            return None
        if re.fullmatch(r"[0-9]+", expr):
            return str(int(expr))
        match = re.fullmatch(r"([0-9]+)([+\-*/])([0-9]+)", expr)
        if not match:
            return None
        left, symbol, right = int(match[1]), match[2], int(match[3])
        if symbol == "+":
            answer = left + right
        elif symbol == "-":
            answer = left - right
        elif symbol == "*":
            answer = left * right
        elif right:
            answer = left // right
        else:
            return None
        return str(answer)

    candidates = [("原图", img_bytes)]
    try:
        img = Image.open(io.BytesIO(img_bytes))
        up = img.convert("L").resize((img.width * 3, img.height * 3), Image.LANCZOS)
        buf = io.BytesIO()
        up.save(buf, format="PNG")
        candidates.append(("放大灰度", buf.getvalue()))
        bin_img = up.point(lambda x: 255 if x > 128 else 0)
        bin_img = ImageOps.invert(bin_img)
        buf = io.BytesIO()
        bin_img.save(buf, format="PNG")
        candidates.append(("二值反色", buf.getvalue()))
    except Exception:
        pass

    for name, src in candidates:
        result = _try(src)
        if result is not None:
            print(f"  [captcha] {name} → '{ocr.classification(src)}' → {result}", file=__import__("sys").stderr)
            return result
    return None


def login(username, password, base_url):
    """自动登录 OA 系统，返回 token"""
    import sys

    session = requests.Session()
    session.headers.update({"Accept-Language": "zh-CN,zh;q=0.9", "User-Agent": "SnOAClient/1.0"})

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = session.get(f"{base_url}/sn/captchaImage", timeout=REQ_TIMEOUT)
            r.raise_for_status()
            data = r.json()["data"]
            uuid = data["uuid"]
            img_b64 = data["img"].split(",", 1)[1] if "," in data["img"] else data["img"]
            img_bytes = base64.b64decode(img_b64)

            answer = solve_captcha(img_bytes)
            if not answer:
                print(f"  [attempt {attempt}] ddddocr 识别失败，重试", file=sys.stderr)
                time.sleep(0.5)
                continue

            r = session.get(f"{base_url}/sn/passWord/encryption", params={"passWord": password}, timeout=REQ_TIMEOUT)
            r.raise_for_status()
            encrypted = r.json()["msg"]

            r = session.post(
                f"{base_url}/sn/login",
                json={"username": username, "password": encrypted, "code": answer, "uuid": uuid},
                timeout=REQ_TIMEOUT,
            )
            r.raise_for_status()
            result = r.json()
            if str(result.get("code")) != "200":
                print(f"  [attempt {attempt}] 登录失败({result.get('code')}): {result.get('msg', '')}", file=sys.stderr)
                time.sleep(0.5)
                continue

            token = result.get("data", {}).get("token")
            if not token:
                print(f"  [attempt {attempt}] token 为空", file=sys.stderr)
                time.sleep(0.5)
                continue

            return token

        except requests.exceptions.Timeout:
            print(f"  [attempt {attempt}] 网络超时", file=sys.stderr)
        except requests.exceptions.ConnectionError as e:
            print(f"  [attempt {attempt}] 连接失败: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  [attempt {attempt}] 异常 {type(e).__name__}: {e}", file=sys.stderr)

        if attempt < MAX_RETRIES:
            time.sleep(0.5)

    raise RuntimeError("登录失败（已达最大重试次数）")


def build_session(token):
    """构造带完整认证头的 OA 会话。"""
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Admin-OA-Token": token,
            "Content-Type": "application/json",
        }
    )
    return session


class CaptchaRejectedError(RuntimeError):
    """服务端判定验证码错误。"""


def _new_session():
    session = requests.Session()
    session.headers.update({"Accept-Language": "zh-CN,zh;q=0.9", "User-Agent": "SnOAClient/1.0"})
    return session


def fetch_captcha(base_url):
    """获取验证码，返回 (uuid, 图片字节, data_url)。

    服务端返回的 img 本身已是 data URL（前缀标 image/png，实际字节为 JPEG）。
    无需共享 HTTP 会话——验证码按 uuid 校验，跨进程提交可行（已实测）。
    """
    session = _new_session()
    r = session.get(f"{base_url}/sn/captchaImage", timeout=REQ_TIMEOUT)
    r.raise_for_status()
    data = r.json()["data"]
    img = data["img"]
    raw = base64.b64decode(img.split(",", 1)[1] if "," in img else img)
    return data["uuid"], raw, img


def submit_login(username, password, base_url, code, uuid):
    """用外部提供的验证码提交登录，返回 token。

    验证码被服务端拒绝时抛 CaptchaRejectedError，其他失败抛 RuntimeError。
    """
    session = _new_session()
    r = session.get(
        f"{base_url}/sn/passWord/encryption", params={"passWord": password}, timeout=REQ_TIMEOUT
    )
    r.raise_for_status()
    encrypted = r.json()["msg"]

    r = session.post(
        f"{base_url}/sn/login",
        json={"username": username, "password": encrypted, "code": str(code), "uuid": uuid},
        timeout=REQ_TIMEOUT,
    )
    r.raise_for_status()
    result = r.json()
    if str(result.get("code")) != "200":
        message = str(result.get("msg", ""))
        if "验证码" in message:
            raise CaptchaRejectedError(message or "验证码不正确")
        raise RuntimeError(f"登录失败({result.get('code')}): {message}")

    token = (result.get("data") or {}).get("token")
    if not token:
        raise RuntimeError("登录失败：token 为空")
    return token


def login_with_code(username, password, base_url, code, uuid, fallback_ddddocr=True):
    """优先使用外部识别结果登录（如 agent 多模态），失败回退 ddddocr 闭环。

    返回 (token, method)，method 取值 'provided-code' / 'ddddocr'。
    """
    try:
        return submit_login(username, password, base_url, code, uuid), "provided-code"
    except CaptchaRejectedError as exc:
        if not fallback_ddddocr:
            raise
        print(f"  [login] 外部验证码被拒绝（{exc}），回退 ddddocr", file=sys.stderr)
    return login(username, password, base_url), "ddddocr"


def session_from_token_or_login(base_url, username, password, token=None):
    """返回 (session, token)：显式 token > 缓存 token > 重新登录（ddddocr）。"""
    auth = OAAuth(base_url, username, password, token)
    return auth.session, auth.token


TOKEN_CACHE_DIR = os.path.expanduser("~/.cache/sn-oa")
TOKEN_CACHE_ENC = os.path.join(TOKEN_CACHE_DIR, "token.enc")
TOKEN_CACHE_PLAIN = os.path.join(TOKEN_CACHE_DIR, "token.json")
TOKEN_TTL_SECONDS = 20 * 60


class AuthExpiredError(RuntimeError):
    """OA 返回 401，token 已失效。"""


def _ensure_ok(result, action):
    """校验业务码：200 通过，401 抛 AuthExpiredError，其余抛 RuntimeError。"""
    code = str(result.get("code"))
    if code == "200":
        return result
    if code == "401":
        raise AuthExpiredError(f"{action}：认证失败，token 可能已过期")
    raise RuntimeError(f"{action}: {result}")


def _account_fingerprint(username):
    """账号指纹（哈希），用于绑定缓存；不落明文账号。"""
    return hashlib.sha256((username or "").encode("utf-8")).hexdigest()[:16]


def _write_private(path, data):
    """以 0600 直接落盘，不产生宽权限窗口。"""
    os.makedirs(TOKEN_CACHE_DIR, mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)


def _remove_quietly(path):
    try:
        os.remove(path)
    except OSError:
        pass


def _cache_files():
    return (TOKEN_CACHE_ENC, TOKEN_CACHE_PLAIN)


def _cache_present():
    return any(os.path.exists(p) for p in _cache_files())


def _read_cache_bytes():
    """优先读加密缓存；解密失败或无密钥时回退明文缓存。"""
    if os.path.exists(TOKEN_CACHE_ENC):
        try:
            with open(TOKEN_CACHE_ENC, "rb") as fh:
                return openssl_cipher("-d", fh.read())
        except (OSError, ValueError):
            return None
    if os.path.exists(TOKEN_CACHE_PLAIN):
        try:
            with open(TOKEN_CACHE_PLAIN, "rb") as fh:
                return fh.read()
        except OSError:
            return None
    return None


def save_cached_token(token, base_url, account=None):
    """写 token 缓存：有密钥则加密（token.enc），否则明文 0600（token.json）。

    缓存与 base_url + 账号指纹绑定，避免换账号后误用旧会话。失败只告警。
    """
    payload = json.dumps(
        {
            "v": 2,
            "token": token,
            "base_url": base_url,
            "account": _account_fingerprint(account) if account else None,
            "acquired_at": time.time(),
        },
        ensure_ascii=False,
    ).encode("utf-8")
    try:
        if get_enc_key():
            _write_private(TOKEN_CACHE_ENC, openssl_cipher("-e", payload))
            _remove_quietly(TOKEN_CACHE_PLAIN)
        else:
            _write_private(TOKEN_CACHE_PLAIN, payload)
            _remove_quietly(TOKEN_CACHE_ENC)
    except (OSError, ValueError) as exc:
        print(f"  [auth] token 缓存写入失败（忽略）: {exc}", file=sys.stderr)


def load_cached_token(base_url, account=None, ttl_seconds=TOKEN_TTL_SECONDS):
    """读缓存 token；文件缺失/损坏/主机或账号不符/超时都返回 None。"""
    raw = _read_cache_bytes()
    if not raw:
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    if data.get("base_url") != base_url:
        return None
    if data.get("account") != (_account_fingerprint(account) if account else None):
        return None
    try:
        age = time.time() - float(data.get("acquired_at", 0))
    except (TypeError, ValueError):
        return None
    if age > ttl_seconds:
        return None
    return data.get("token") or None


def clear_cached_token():
    """删除 token 缓存（加密与明文两种形态都清）。"""
    for path in _cache_files():
        _remove_quietly(path)


class OAAuth:
    """持有 OA 会话：无 token 时登录（优先复用缓存），401 时清缓存并重新登录刷新会话。"""

    def __init__(self, base_url, username, password, token=None, use_cache=True):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session, self.token = self._acquire(token, use_cache)
        from submission_guard import bind_submission_session
        bind_submission_session(self.session, self.base_url, self.username)

    def _acquire(self, token, use_cache):
        if token:
            return build_session(token), token
        if use_cache:
            cached = load_cached_token(self.base_url, self.username)
            if cached:
                print("  [auth] 复用缓存 token，跳过登录", file=sys.stderr)
                return build_session(cached), cached
            if _cache_present():
                print("  [auth] 缓存 token 不可用（主机/账号不符或已过期），重新登录", file=sys.stderr)
        new_token = login(self.username, self.password, self.base_url)
        save_cached_token(new_token, self.base_url, self.username)
        return build_session(new_token), new_token

    def refresh(self):
        """清缓存并重新登录，刷新 self.session / self.token。"""
        clear_cached_token()
        print("  [auth] token 已失效，重新登录…", file=sys.stderr)
        self.session, self.token = self._acquire(None, use_cache=False)
        from submission_guard import bind_submission_session
        bind_submission_session(self.session, self.base_url, self.username)
        return self.session

    def call(self, operation, allow_relogin=True):
        """执行 operation(session)。

        遇到 401：只读操作默认清缓存、重新登录并重试一次；
        写操作用 allow_relogin=False 关闭自动重试，避免重复提交。
        """
        try:
            return operation(self.session)
        except AuthExpiredError:
            clear_cached_token()
            if not allow_relogin:
                raise RuntimeError("token 已失效，缓存已清除；请重新执行本命令（会重新登录）")
            self.refresh()
            return operation(self.session)


def state_to_text(state):
    """把工时状态码转成人类可读文本。"""
    return STATE_MAP.get(str(state), str(state) if state not in (None, "") else "未知")


def query_time_entries(session, base_url, fill_date):
    """查询某天工时列表，返回 records。"""
    r = session.post(
        f"{base_url}/sn/timeEntry/findEveryDayList",
        json={"fillDate": fill_date},
        timeout=REQ_TIMEOUT,
    )
    r.raise_for_status()
    result = r.json()
    _ensure_ok(result, "查询工时失败")
    return result.get("data", []) or [], result


def fee_state_to_text(state):
    """把报销申请状态码转成人类可读文本。"""
    return FEE_STATE_MAP.get(str(state), str(state) if state not in (None, "") else "未知")


def fee_type_to_text(fee_type):
    """把费用申请类型码转成人类可读文本。"""
    return FEE_TYPE_MAP.get(str(fee_type), str(fee_type) if fee_type not in (None, "") else "未知")


def reimburse_company_to_text(company):
    """把报销公司码转成人类可读文本。"""
    return REIMBURSE_COMPANY_MAP.get(str(company), str(company) if company not in (None, "") else "未知")


def query_fee_requests(session, base_url, page=1, size=20, start_time="", end_time=""):
    """分页查询当前用户的费用/报销申请。"""
    payload = {
        "page": page,
        "size": size,
        "total": 0,
        "startTime": start_time or "",
        "endTime": end_time or "",
    }
    r = session.post(f"{base_url}/sn/feeRequest/findPageList", json=payload, timeout=REQ_TIMEOUT)
    r.raise_for_status()
    result = r.json()
    _ensure_ok(result, "查询报销申请失败")
    data = result.get("data", {}) or {}
    return data.get("content", []) or [], data, result


def get_fee_request_details(session, base_url, request_id):
    """根据费用申请 ID 获取报销详情。"""
    r = session.get(f"{base_url}/sn/feeRequest/details/{request_id}", timeout=REQ_TIMEOUT)
    r.raise_for_status()
    result = r.json()
    _ensure_ok(result, "获取报销详情失败")
    return result.get("data", {}) or {}, result


def get_workflow_process_detail(session, base_url, proc_ins_id):
    """查询费用申请的审批流程详情。"""
    r = session.get(
        f"{base_url}/sn/workflow/process/detail",
        params={"procInsId": proc_ins_id},
        timeout=REQ_TIMEOUT,
    )
    r.raise_for_status()
    result = r.json()
    _ensure_ok(result, "获取审批进度失败")
    return result.get("data", {}) or {}, result


def get_time_entry_details(session, base_url, entry_id):
    """根据工时 ID 获取详情。"""
    r = session.get(f"{base_url}/sn/timeEntry/details/{entry_id}", timeout=REQ_TIMEOUT, allow_redirects=False)
    if 300 <= r.status_code < 400:
        raise ValueError('工时详情禁止 HTTP 重定向')
    r.raise_for_status()
    result = r.json()
    _ensure_ok(result, "获取工时详情失败")
    return result.get("data", {}) or {}, result


def submit_time_entry(
    session,
    base_url,
    fill_date,
    project_id,
    project_name,
    job_desc,
    man_hour=None,
    save_or_submit=1,
    project_phase=None,
    work_type=None,
    bo_to_pm_status=None,
    fill_type=None,
):
    """提交或保存工时记录；必填项不得使用隐式业务默认值。"""
    from personal_settings import validate_fields
    validate_fields(dict(project_id=project_id, project_name=project_name,
                         man_hour=man_hour, project_phase=project_phase,
                         work_type=work_type, bo_to_pm_status=bo_to_pm_status,
                         fill_type=fill_type))
    if not fill_date or not isinstance(job_desc, str) or not job_desc.strip():
        raise ValueError("日期和描述必须显式提供")
    payload = {
        "timeEntryList": [
            {
                "fillDate": fill_date,
                "projectName": project_name,
                "projectId": str(project_id),
                "projectPhase": str(project_phase),
                "workType": str(work_type),
                "manHour": man_hour,
                "jobDesc": job_desc,
                "boToPmStatus": bo_to_pm_status,
                "fillType": str(fill_type),
            }
        ],
        "saveOrSubmit": save_or_submit,
    }
    from submission_guard import guarded_submit

    def write():
        r = session.post(f"{base_url}/sn/timeEntry/saveOrUpdate", json=payload, timeout=REQ_TIMEOUT, allow_redirects=False)
        r.raise_for_status()
        result = r.json()
        _ensure_ok(result, "提交工时失败")
        return result

    return guarded_submit(session, base_url, payload, query_time_entries, write)


def update_time_entry(session, base_url, entry_id, job_desc=None, is_deleted=None, *, confirm_entry_id=None):
    """Update description only; production deletion/restoration is disabled."""
    if is_deleted is not None:
        raise ValueError('删除/恢复暂禁：服务端无可靠恢复契约；不得尝试删除或恢复')
    payload = {"id": entry_id}
    if job_desc is not None:
        payload["jobDesc"] = job_desc
    r = session.put(f"{base_url}/sn/timeEntry/update", json=payload, timeout=REQ_TIMEOUT)
    r.raise_for_status()
    result = r.json()
    _ensure_ok(result, "修改工时失败")
    return result
