"""_config.py — campus/learn 配置桥接层

将 learn 业务脚本（learn_api/ops/todos）需要的配置映射到 campus 底座：
- session 文件 → base-cas 的 session.load_session('learn')
- 下载/上传目录 → campus runtime 目录
- 学期 → config 或自动检测
- 学号/姓名 → creds 统一凭据（cas_username / student_id）

保持原有函数签名（get_*），learn_api/ops/todos 几乎零改动。
"""
import sys
import os
import json

# learn/scripts → campus 底座: shared/base-cas/creds 在 ../../ 下
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "creds", "scripts"))
import common
import session
import vault


def _campus_root():
    return common.skill_root()


def get_state_file():
    """返回 learn session 文件路径（与 base-cas session.py 一致）。"""
    return os.path.join(str(common.session_dir()), "learn.json")


def get_semester():
    """从 config 读学期（可手动覆盖），空则自动检测。"""
    cfg = _load_config()
    return cfg.get("semester", "")


def auto_mark_read():
    """是否自动标已读（runtime/config.json 的 auto_mark_read，默认 False）。"""
    return _load_config().get("auto_mark_read", False)


def _load_config():
    p = os.path.join(str(common.runtime_dir()), "config.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_download_dir_abs():
    d = common.runtime_dir("downloads")
    os.makedirs(d, exist_ok=True)
    return d


def get_upload_dir():
    d = common.runtime_dir("uploads")
    os.makedirs(d, exist_ok=True)
    return d


def get_submissions_log():
    d = common.runtime_dir("submissions")
    os.makedirs(d, exist_ok=True)
    return os.path.join(str(d), "submissions_log.json")


def get_student_id():
    """学号：优先专用凭据，否则退回 cas_username。"""
    v = _get_cred("student_id")
    if v:
        return v
    return _get_cred("cas_username")


def get_student_name():
    return _get_cred("student_name")


def get_username():
    return _get_cred("cas_username")


def _get_cred(key):
    """从凭据保险箱取明文（统一走 vault.vault_get）。"""
    return vault.vault_get(key)
