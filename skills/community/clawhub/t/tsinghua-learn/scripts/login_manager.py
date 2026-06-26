#!/usr/bin/env python3
"""
login_manager.py — 中央认证网关
所有脚本遇到认证问题时统一调用此模块。

用法（模块导入）：
  from login_manager import ensure_session, init_credentials
  session = ensure_session()

用法（CLI）：
  python login_manager.py                   # 确保 session 有效，输出 JSON
  python login_manager.py --init            # 初始化凭据（缺少字段时交互式补充）
  python login_manager.py --init --username=X --password=Y --student-id=Z --name=W
  python login_manager.py --check           # 仅检查 session 是否有效
"""
import sys, os, json, time, subprocess, requests
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load_credentials, save_credentials, get_state_file, is_initialized

BASE = "https://learn.tsinghua.edu.cn"
STATE_FILE = get_state_file()


def _check_session_valid(state):
    if not state.get("learn_jsession") or not state.get("csrf"):
        return False
    h = {
        "Accept": "application/json, */*",
        "Referer": f"{BASE}/f/wlxt/index/course/student/",
        "X-XSRF-TOKEN": state["csrf"],
        "Cookie": f"JSESSIONID={state['learn_jsession']}; XSRF-TOKEN={state['csrf']}",
    }
    try:
        r = requests.get(
            f"{BASE}/b/wlxt/kczy/zy/student/index/zyListWj?wlkcid=&size=1",
            headers=h, timeout=10
        )
        return not ("location.href" in r.text and r.status_code == 200)
    except:
        return False


def _try_auto_login():
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_auto.py")
    r = subprocess.run([sys.executable, script])
    return r.returncode == 0


def _try_supervised_login():
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_supervised.py")
    print("自动登录失败，需要人工完成二次验证。弹出浏览器...")
    r = subprocess.run([sys.executable, script])
    return r.returncode == 0


def ensure_session():
    """统一 session 保证入口。未初始化时自动提示。"""
    if not is_initialized():
        print("未初始化，请先运行 --init")
        raise SystemExit(3)

    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            state = json.load(f)

    if _check_session_valid(state):
        return {"jsession": state["learn_jsession"], "csrf": state["csrf"], "valid": True}

    print("Session 无效，尝试自动续期...")
    if _try_auto_login():
        with open(STATE_FILE, encoding='utf-8') as f:
            state = json.load(f)
        return {"jsession": state["learn_jsession"], "csrf": state["csrf"], "valid": True}

    print("自动续期失败，尝试人工登录...")
    if _try_supervised_login():
        with open(STATE_FILE, encoding='utf-8') as f:
            state = json.load(f)
        return {"jsession": state["learn_jsession"], "csrf": state["csrf"], "valid": True}

    raise SystemExit(2)


def init_credentials(username=None, password=None, student_id=None, name=None, learn_account=None):
    """初始化凭据。AI 通过命令行参数传入，不阻塞等待输入。缺失字段报错返回。"""
    existing = load_credentials()
    username = username or existing.get("username", "")
    password = password or existing.get("password", "")
    learn_account = learn_account or student_id or existing.get("student_id", "") or username
    name = name or existing.get("name", "")

    missing = []
    if not learn_account: missing.append("learn-account (网络学堂登录账号)")
    if not password: missing.append("password (网络学堂登录密码)")
    if not username: missing.append("username (学号)")
    if not name: missing.append("name (姓名)")

    if missing:
        result = {"status": "error", "message": "缺少必要字段", "missing": missing}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    save_credentials(username, password, learn_account, name)
    result = {
        "status": "ok",
        "message": "凭据已保存（Windows DPAPI 加密）",
        "fields": {
            "learn_account": learn_account,
            "password": "***",
            "username": "***",
            "name": name,
        },
    }
    print(json.dumps(result, ensure_ascii=False))


# ====== CLI ======
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="网络学堂中央认证网关")
    parser.add_argument("--init", action="store_true", help="初始化凭据")
    parser.add_argument("--cred-stdin", action="store_true", help="从标准输入读取凭据 JSON（避免密码出现在命令行）")
    parser.add_argument("--reset", action="store_true", help="清空所有数据（凭据/session/profile/下载/上传/配置），保留文件结构")
    parser.add_argument("--learn-account", default=None, help="网络学堂登录账号")
    parser.add_argument("--password", default=None, help="网络学堂登录密码")
    parser.add_argument("--username", default=None, help="学号")
    parser.add_argument("--student-id", default=None, help="(已弃用，使用 --learn-account)")
    parser.add_argument("--name", default=None, help="姓名")
    parser.add_argument("--check", action="store_true", help="仅检查 session")
    parser.add_argument("--verify", action="store_true", help="验证环境：检查 Chromium + 尝试登录")
    parser.add_argument("--force-login", action="store_true", help="强制执行完整登录（可能触发浏览器，较慢）")
    args = parser.parse_args()

    if args.reset:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cleared = []
        for d in ["downloads", "uploads"]:
            path = os.path.join(skill_dir, d)
            if os.path.isdir(path):
                for f in os.listdir(path):
                    fp = os.path.join(path, f)
                    if os.path.isfile(fp):
                        os.remove(fp)
                cleared.append(d)
        # 清空 session 文件（保留文件结构）
        session_file = os.path.join(skill_dir, "sessions", "learn_session.json")
        if os.path.exists(session_file):
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            cleared.append("session")
        # 清空 submissions 日志（保留文件结构）
        sub_file = os.path.join(skill_dir, "submissions", "submissions_log.json")
        if os.path.exists(sub_file):
            with open(sub_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            cleared.append("submissions")
        # 清空 profile（保留目录）
        profile_dir = os.path.join(skill_dir, "profiles", "learn_profile")
        if os.path.isdir(profile_dir):
            for name in os.listdir(profile_dir):
                fp = os.path.join(profile_dir, name)
                if os.path.isdir(fp):
                    import shutil
                    shutil.rmtree(fp, ignore_errors=True)
                else:
                    os.remove(fp)
            cleared.append("profile")
        # 清空凭据
        save_credentials("", "", "", "")
        cleared.append("credentials")
        # 重置 config.json
        cfg_path = os.path.join(skill_dir, "config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "auto_mark_read": True,
                    "confirm_before_cleanup": True,
                    "confirm_before_download": True,
                }, f, ensure_ascii=False, indent=2)
            cleared.append("config")
        print(json.dumps({"status": "ok", "cleared": cleared}, ensure_ascii=False))
        sys.exit(0)

    if args.init:
        learn_account = args.learn_account or args.student_id
        if args.cred_stdin:
            try:
                data = json.loads(sys.stdin.read())
                learn_account = data.get("learn_account") or data.get("student_id") or learn_account
                args.username = data.get("username") or args.username
                args.password = data.get("password") or args.password
                args.name = data.get("name") or args.name
            except Exception as e:
                print(json.dumps({"status": "error", "message": f"stdin JSON 解析失败: {e}"}, ensure_ascii=False))
                sys.exit(1)
        init_credentials(args.username, args.password, learn_account=learn_account, name=args.name)
        sys.exit(0)

    if args.verify:
        result = {"python": False, "deps": False, "chromium": False, "login": False, "needs_2fa": False}
        # 检查 Python 版本
        installer = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_deps.py")
        r_py = subprocess.run([sys.executable, installer], capture_output=True, timeout=120)
        py_out = r_py.stdout.decode("utf-8", errors="replace")
        try:
            py_data = json.loads(py_out)
            if py_data.get("status") == "ok":
                result["python"] = True
                result["python_version"] = py_data.get("python", "")
                result["deps"] = True
        except Exception:
            result["python"] = False
        if not result["python"]:
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(0)
        # 检查 Chromium
        try:
            import subprocess as _sp
            _r = _sp.run([sys.executable, "-m", "playwright", "install", "--dry-run", "chromium"],
                         capture_output=True, timeout=30)
            _out = _r.stdout.decode("utf-8", errors="replace")
            if "already" in _out:
                result["chromium"] = True
            else:
                _ri = _sp.run([sys.executable, "-m", "playwright", "install", "chromium"],
                             capture_output=False, timeout=120)
                if _ri.returncode == 0:
                    result["chromium"] = True
                    result["chromium_installed"] = True
        except Exception:
            result["chromium"] = False
        # 尝试登录
        try:
            sess = ensure_session()
            result["login"] = True
        except SystemExit as e:
            if e.code == 2:
                result["needs_2fa"] = True
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    if args.check:
        init_ok = is_initialized()
        state = {}
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, encoding='utf-8') as f:
                state = json.load(f)
        valid = _check_session_valid(state)
        print(json.dumps({
            "initialized": init_ok,
            "valid": valid,
            "age_h": (time.time() - state.get("timestamp", 0)) / 3600 if state else None,
        }))
        sys.exit(0 if valid else 1)

    if args.force_login:
        try:
            sess = ensure_session()
            print(json.dumps({"valid": True, "jsession": sess["jsession"][:10] + "...", "csrf": sess["csrf"][:10] + "..."}))
        except SystemExit as e:
            print(json.dumps({"valid": False, "code": e.code}))
            sys.exit(e.code)
        sys.exit(0)

    # 默认行为：快速检查（<1 秒，纯 API，不启动浏览器）
    init_ok = is_initialized()
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            state = json.load(f)
    valid = _check_session_valid(state)
    print(json.dumps({
        "initialized": init_ok,
        "valid": valid,
        "age_h": (time.time() - state.get("timestamp", 0)) / 3600 if state else None,
    }))
    sys.exit(0 if valid else 1)
