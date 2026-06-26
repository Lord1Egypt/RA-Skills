#!/usr/bin/env python3
"""蜀宁 OA 公共工具 — 凭证读取、验证码识别、登录、会话构建、工时提交/查询/详情/修改、节假日检查"""

import base64
import datetime
import io
import os
import re
import subprocess
import sys
import time

import requests

MAX_RETRIES = 3
REQ_TIMEOUT = 10
STATE_MAP = {
    "10": "草稿",
    "20": "审批中",
    "30": "已审批",
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


def decrypt_file(enc_path):
    """用 openssl aes-256-cbc 解密 .enc 文件，返回 bytes"""
    key = os.environ.get("OA_ENC_KEY")
    key_file = os.path.expanduser("~/.openclaw/workspace/.cache/oa_enc_key")
    if not key and os.path.exists(key_file):
        with open(key_file) as f:
            key = f.read().strip()
    if not key:
        raise ValueError(f"找不到解密密钥（环境变量 OA_ENC_KEY 或 {key_file}）")
    result = subprocess.run(
        ["openssl", "aes-256-cbc", "-d", "-a", "-pbkdf2", "-pass", f"pass:{key}", "-in", enc_path],
        capture_output=True,
        timeout=10,
    )
    if result.returncode != 0:
        raise ValueError(f"解密失败: {result.stderr.decode(errors='replace')}")
    return result.stdout


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
        expr = re.sub(r"[^0-9+\-*/]", "", text)
        if not expr:
            return None
        try:
            return str(int(eval(expr)))
        except Exception:
            pass
        expr = expr.rstrip("+-*/")
        try:
            return str(int(eval(expr)))
        except Exception:
            return None

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
    if str(result.get("code")) != "200":
        raise RuntimeError(f"查询工时失败: {result}")
    return result.get("data", []) or [], result


def get_time_entry_details(session, base_url, entry_id):
    """根据工时 ID 获取详情。"""
    r = session.get(f"{base_url}/sn/timeEntry/details/{entry_id}", timeout=REQ_TIMEOUT)
    r.raise_for_status()
    result = r.json()
    if str(result.get("code")) != "200":
        raise RuntimeError(f"获取工时详情失败: {result}")
    return result.get("data", {}) or {}, result


def submit_time_entry(
    session,
    base_url,
    fill_date,
    project_id,
    project_name,
    job_desc,
    man_hour=8,
    save_or_submit=1,
    project_phase="1",
    work_type="5",
    bo_to_pm_status=1,
    fill_type="1",
):
    """提交或保存工时记录。"""
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
    r = session.post(f"{base_url}/sn/timeEntry/saveOrUpdate", json=payload, timeout=REQ_TIMEOUT)
    r.raise_for_status()
    result = r.json()
    if str(result.get("code")) != "200":
        raise RuntimeError(f"提交工时失败: {result}")
    return result


def update_time_entry(session, base_url, entry_id, job_desc=None, is_deleted=None):
    """更新工时记录，支持修改描述或逻辑删除。"""
    payload = {"id": entry_id}
    if job_desc is not None:
        payload["jobDesc"] = job_desc
    if is_deleted is not None:
        payload["isDeleted"] = is_deleted
    r = session.put(f"{base_url}/sn/timeEntry/update", json=payload, timeout=REQ_TIMEOUT)
    r.raise_for_status()
    result = r.json()
    if str(result.get("code")) != "200":
        raise RuntimeError(f"修改工时失败: {result}")
    return result
