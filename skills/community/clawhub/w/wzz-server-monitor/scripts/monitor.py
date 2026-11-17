#!/usr/bin/env python3
"""wzz-server-monitor — 服务器资源监控通知

监控 CPU/内存/磁盘使用率，超过配置阈值时通过 SMTP 发送邮件告警。

支持：
  - 可配置阈值（CPU / 内存 / 多路径磁盘）
  - 通知频率控制：状态变化去重 + cooldown 节流 + 单日上限
  - 可配置发送时间窗口（窗口外静默，但状态照常记录，开窗后补发）
  - 可配置邮件文案模板（jinja2，缺失时回退 string.Template）

用法：
  monitor.py setup            首次初始化（检查依赖、生成目录、复制配置模板）
  monitor.py check            单次检查（cron 入口）
  monitor.py check --now      跳过时间窗口判断（测试用）
  monitor.py check --dry-run  只打印决策，不发信、不写状态
  monitor.py status           打印当前指标快照与状态
  monitor.py send-test        发送一封测试邮件（绕开阈值/窗口/节流）
  monitor.py validate-config  校验配置；--smtp-connect 额外做 SMTP 连接握手
  monitor.py reset-state      清空运行状态

配置文件默认位置（可用 --config 覆盖）：
  ~/.config/resource-monitor/config.yaml
状态文件默认位置（可用 --state 覆盖）：
  ~/.local/state/resource-monitor/state.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as html_mod
import json
import os
import re
import shutil
import socket
import string
import sys
import time
import traceback

# 标准库路径定位（skill 目录 = scripts/ 的上级）
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TPL_DIR = os.path.join(SKILL_DIR, "assets", "templates")

CONFIG_DIR = os.path.expanduser("~/.config/resource-monitor")
STATE_DIR = os.path.expanduser("~/.local/state/resource-monitor")
DEFAULT_CONFIG = os.path.join(CONFIG_DIR, "config.yaml")
DEFAULT_STATE = os.path.join(STATE_DIR, "state.json")
DEFAULT_SECRET = os.path.join(CONFIG_DIR, ".smtp_secret")

# 空配置模板 = 从 assets/config.example.yaml 复制
EXAMPLE_CONFIG = os.path.join(SKILL_DIR, "assets", "config.example.yaml")

COOLDOWN_DEFAULT_MINUTES = 60
DAILY_CAP_DEFAULT = 20

# 发送决策
SEND_ALARM = "SEND_ALARM"
SEND_RECOVERY = "SEND_RECOVERY"
SUPPRESS_COOLDOWN = "SUPPRESS_COOLDOWN"
SUPPRESS_WINDOW = "SUPPRESS_WINDOW"
SUPPRESS_DAILY_CAP = "SUPPRESS_DAILY_CAP"
NONE = "NONE"

REQUIRED_DEPS = ["psutil", "yaml", "jinja2"]


# ---------------------------------------------------------------- 依赖检查
def check_deps() -> list[str]:
    import importlib

    missing = []
    for mod in REQUIRED_DEPS:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(mod)
    return missing


# ---------------------------------------------------------------- 配置加载
def _deep_merge(base: dict, override: dict) -> dict:
    """递归合并，override 优先。"""
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _norm(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def load_config(path: str) -> dict:
    import yaml

    if not os.path.exists(path):
        raise FileNotFoundError(f"配置文件不存在: {path}\n请先运行: python3 scripts/monitor.py setup")
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if not isinstance(raw, dict):
        raise ValueError("配置文件顶层必须是 YAML 映射")

    base = {
        "hostname_label": "",
        "metrics": {
            "cpu": {"enabled": True, "threshold": 80, "cpu_interval": 0.5},
            "memory": {"enabled": True, "threshold": 85},
            "disk": {"enabled": True, "paths": [{"path": "/", "threshold": 85}]},
        },
        "smtp": {
            "host": "",
            "port": 465,
            "security": "ssl",
            "username": "",
            "from": "",
            "to": [],
            "password": "",
            "password_file": "",
            "timeout": 30,
        },
        "cooldown_minutes": COOLDOWN_DEFAULT_MINUTES,
        "recovery": True,
        "daily_cap": DAILY_CAP_DEFAULT,
        "window": {"enabled": True, "rules": [{"start": "09:00", "end": "22:00"}]},
        "templates": {
            "dir": DEFAULT_TPL_DIR,
            "alarm": {
                "subject": "[{{ hostname }}] 资源告警 ({{ alarm_count }}项)",
                "body": "alarm.html",
            },
            "recovery": {
                "subject": "[{{ hostname }}] 资源已恢复",
                "body": "recovery.html",
            },
        },
    }
    cfg = _deep_merge(base, raw)
    cfg["templates"]["dir"] = _norm(cfg["templates"].get("dir") or DEFAULT_TPL_DIR)
    smtp = cfg["smtp"]
    if smtp.get("password_file"):
        smtp["password_file"] = _norm(smtp["password_file"])
    if not smtp.get("password") and not smtp.get("password_file"):
        # 用户两个都没填时，给出默认路径提示，不强制检查文件存在
        smtp["password_file"] = DEFAULT_SECRET
    return cfg


def validate_config(cfg: dict) -> list[str]:
    """返回错误信息列表；空列表 = 通过。"""
    errors = []
    smtp = cfg["smtp"]
    if not smtp.get("host"):
        errors.append("smtp.host 必填（如 smtp.qq.com）")
    if not isinstance(smtp.get("port"), int) or not (1 <= smtp["port"] <= 65535):
        errors.append("smtp.port 必须是 1-65535 的整数")
    if smtp.get("security") not in ("ssl", "tls", "none"):
        errors.append("smtp.security 必须是 ssl / tls / none")
    if not smtp.get("username"):
        errors.append("smtp.username 必填")
    if not smtp.get("to"):
        errors.append("smtp.to 至少需要一个收件人")
    if not smtp.get("password") and not smtp.get("password_file"):
        errors.append("smtp.password 或 smtp.password_file 至少填一个")
    if smtp.get("password_file") and not os.path.exists(smtp["password_file"]):
        errors.append(f"smtp.password_file 文件不存在: {smtp['password_file']}")

    for name, spec in cfg["metrics"].items():
        if isinstance(spec, dict) and spec.get("enabled", True):
            if name == "disk":
                paths = spec.get("paths") or []
                if not paths:
                    errors.append("metrics.disk.paths 至少需要一个挂载路径")
                for p in paths:
                    t = p.get("threshold", 100)
                    if not (0 < t <= 100):
                        errors.append(f"磁盘阈值必须 0-100: {p.get('path')}")
            else:
                t = spec.get("threshold", 100)
                if not (0 < t <= 100):
                    errors.append(f"metrics.{name}.threshold 必须 0-100")

    cooldown = cfg.get("cooldown_minutes", 0)
    if cooldown < 0:
        errors.append("cooldown_minutes 不能为负")

    if cfg.get("window", {}).get("enabled", True):
        for rule in cfg["window"].get("rules", []):
            s, e = rule.get("start"), rule.get("end")
            if not _valid_hhmm(s) or not _valid_hhmm(e):
                errors.append(f"窗口时间必须是 HH:MM 格式: {rule}")
            elif s == e:
                errors.append(f"窗口 start 不能等于 end: {rule}")
    return errors


def _valid_hhmm(s: str) -> bool:
    return isinstance(s, str) and bool(re.fullmatch(r"\d{2}:\d{2}", s)) and 0 <= int(s[:2]) <= 23 and 0 <= int(s[3:]) <= 59


# ---------------------------------------------------------------- 指标采集
def _load_psutil():
    import psutil  # noqa: F401

    return psutil


def collect_metrics(cfg: dict) -> dict:
    """返回 {key: {'metric':..., 'percent':float, 'threshold':int, 'path'?:str}}"""
    psutil = _load_psutil()
    snapshot: dict = {}

    cpu = cfg["metrics"].get("cpu", {})
    if cpu.get("enabled", True):
        # cron 每轮是全新进程，cpu_percent 首次调用必须带 interval，否则恒为 0.0
        interval = float(cpu.get("cpu_interval", 0.5))
        snapshot["cpu"] = {
            "metric": "CPU",
            "percent": round(psutil.cpu_percent(interval=interval), 1),
            "threshold": cpu.get("threshold", 100),
        }

    mem = cfg["metrics"].get("memory", {})
    if mem.get("enabled", True):
        snapshot["memory"] = {
            "metric": "内存",
            "percent": round(psutil.virtual_memory().percent, 1),
            "threshold": mem.get("threshold", 100),
        }

    disk = cfg["metrics"].get("disk", {})
    if disk.get("enabled", True):
        for p in disk.get("paths", []):
            path = p.get("path", "/")
            key = f"disk:{path}"
            try:
                percent = round(psutil.disk_usage(path).percent, 1)
            except (OSError, PermissionError) as e:
                print(f"警告: 无法读取磁盘 {path}: {e}", file=sys.stderr)
                continue
            snapshot[key] = {
                "metric": "磁盘",
                "percent": percent,
                "threshold": p.get("threshold", 100),
                "path": path,
            }
    return snapshot


def evaluate(snapshot: dict) -> dict:
    exceeded = [k for k, v in snapshot.items() if v["percent"] >= v["threshold"]]
    return {"is_alarm": bool(exceeded), "exceeded": exceeded, "all": snapshot}


# ---------------------------------------------------------------- 时间窗口
def _to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def window_open(cfg: dict, now: dt.datetime) -> bool:
    w = cfg.get("window", {})
    if not w.get("enabled", True):
        return True
    rules = w.get("rules", [])
    if not rules:
        return True  # 空列表 = 全天
    cur = now.hour * 60 + now.minute
    for rule in rules:
        s = _to_minutes(rule["start"])
        e = _to_minutes(rule["end"])
        if s <= e:
            if s <= cur <= e:
                return True
        else:  # 跨午夜窗口，如 22:00 - 06:00
            if cur >= s or cur <= e:
                return True
    return False


# ---------------------------------------------------------------- 状态持久化
def load_state(path: str) -> dict:
    default = {
        "level": "normal",
        "alarming": [],
        "since": None,
        "last_sent": None,
        "sent_today": 0,
        "day": "",
    }
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in default:
            data.setdefault(k, default[k])
        return data
    except (json.JSONDecodeError, OSError):
        return default


def save_state(path: str, state: dict) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)  # 原子替换，任何时刻读到完整 JSON


def acquire_lock(state_path: str) -> int | None:
    """非阻塞 flock；返回锁 fd，拿不到锁（上一轮仍在跑）返回 None。"""
    import fcntl

    lock_path = state_path + ".lock"
    os.makedirs(os.path.dirname(lock_path) or ".", exist_ok=True)
    try:
        fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    except OSError:
        return None
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(fd)
        return None
    return fd


def release_lock(fd: int | None) -> None:
    import fcntl

    if fd is None:
        return
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass
    finally:
        os.close(fd)


# ---------------------------------------------------------------- 决策
def decide(state: dict, result: dict, now: dt.datetime, cfg: dict, force_window: bool = False) -> tuple[str, dict]:
    """返回 (decision, new_state)。调用方在获得 SEND_* 后才真正发信并持久化。"""
    new_state = dict(state)
    in_window = force_window or window_open(cfg, now)
    cooldown_secs = int(cfg.get("cooldown_minutes", COOLDOWN_DEFAULT_MINUTES)) * 60
    daily_cap = int(cfg.get("daily_cap", 0))

    day = now.strftime("%Y-%m-%d")
    if new_state.get("day") != day:
        new_state["day"] = day
        new_state["sent_today"] = 0

    def _cap_ok() -> bool:
        return daily_cap == 0 or new_state["sent_today"] < daily_cap

    now_ts = now.timestamp()

    if result["is_alarm"]:
        if new_state["level"] == "normal":
            new_state["level"] = "alarm"
            new_state["since"] = now_ts
            new_state["alarming"] = result["exceeded"]
        else:
            new_state["alarming"] = result["exceeded"]

        last = new_state.get("last_sent")
        if last is not None and (now_ts - last) < cooldown_secs:
            return SUPPRESS_COOLDOWN, new_state
        if not _cap_ok():
            return SUPPRESS_DAILY_CAP, new_state
        if not in_window:
            # 窗口外：静默且不推进 last_sent → 窗口一开首轮补发
            return SUPPRESS_WINDOW, new_state
        new_state["last_sent"] = now_ts
        new_state["sent_today"] += 1
        return SEND_ALARM, new_state

    # 未超限
    if new_state["level"] == "alarm":
        new_state["level"] = "normal"
        new_state["since"] = None
        new_state["alarming"] = []
        if cfg.get("recovery", True):
            last = new_state.get("last_sent")
            if last is None or (now_ts - last) >= cooldown_secs:
                if _cap_ok() and in_window:
                    new_state["last_sent"] = now_ts
                    new_state["sent_today"] += 1
                    return SEND_RECOVERY, new_state
        # 不发恢复邮件也要重置计时：下次告警重新计算
        new_state["last_sent"] = None
        return NONE, new_state

    return NONE, new_state


# ---------------------------------------------------------------- 渲染
def _strip_html(html_text: str) -> str:
    text = re.sub(r"<style.*?</style>", "", html_text, flags=re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = html_mod.unescape(text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def build_data(cfg: dict, result: dict, status: str, now: dt.datetime) -> dict:
    psutil = _load_psutil()
    hostname = (cfg.get("hostname_label") or socket.gethostname()).strip() or "unknown"
    alarms = []
    for key in result["exceeded"]:
        v = result["all"][key]
        alarms.append(
            {
                "metric": v["metric"],
                "current": v["percent"],
                "threshold": v["threshold"],
                "path": v.get("path"),
            }
        )
    metrics = {}
    for key, v in result["all"].items():
        metrics[key] = {
            "percent": v["percent"],
            "threshold": v["threshold"],
            "path": v.get("path"),
        }

    uptime = None
    try:
        boot = dt.datetime.fromtimestamp(psutil.boot_time())
        uptime = now - boot
    except Exception:
        uptime = None

    return {
        "hostname": hostname,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "alarm_count": len(alarms),
        "alarms": alarms,
        "metrics": metrics,
        "uptime": uptime,
        "load_avg": list(psutil.getloadavg()),
    }


def _flatten_data(data: dict) -> dict:
    """string.Template 回退模式：注入标量 + 预拼超限列表文本。"""
    flat = {k: v for k, v in data.items() if not isinstance(v, (list, dict))}
    if data.get("uptime") is not None:
        flat["uptime"] = str(data["uptime"]).split(".")[0]
    flat["load_avg"] = ", ".join(f"{x:.2f}" for x in data.get("load_avg", []))
    lines = [
        f"- {a['metric']}({a['path'] or '系统'}): {a['current']}% (阈值 {a['threshold']}%)"
        for a in data.get("alarms", [])
    ]
    flat["alarms_text"] = "\n".join(lines) or "无"
    return flat


def render(cfg: dict, tpl_cfg: dict, data: dict) -> tuple[str, str]:
    """返回 (subject, html_body)。优先 jinja2，缺失回退 string.Template。"""
    subject_tpl = tpl_cfg.get("subject", "")
    body_file = tpl_cfg.get("body", "alarm.html")
    tpl_dir = cfg["templates"]["dir"]
    body_path = os.path.join(tpl_dir, body_file)

    try:
        import jinja2

        html_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(tpl_dir), autoescape=True, trim_blocks=True, lstrip_blocks=True
        )
        plain_env = jinja2.Environment(autoescape=False)
        subject = plain_env.from_string(subject_tpl).render(**data)
        if not os.path.exists(body_path):
            raise FileNotFoundError(f"模板文件不存在: {body_path}")
        body = html_env.get_template(body_file).render(**data)
    except ImportError:
        flat = _flatten_data(data)
        subject = string.Template(subject_tpl).safe_substitute(**flat)
        if os.path.exists(body_path):
            with open(body_path, "r", encoding="utf-8") as f:
                body_tpl = f.read()
        else:
            body_tpl = "资源告警：\n$alarms_text"
        body = string.Template(body_tpl).safe_substitute(**flat)
    return subject, body


# ---------------------------------------------------------------- SMTP
def _read_password(cfg: dict) -> str:
    smtp = cfg["smtp"]
    if smtp.get("password"):
        return str(smtp["password"])
    pfile = smtp.get("password_file")
    if pfile and os.path.exists(pfile):
        with open(pfile, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def smtp_send(cfg: dict, subject: str, html: str) -> None:
    import smtplib
    from email.message import EmailMessage

    smtp = cfg["smtp"]
    host = smtp["host"]
    port = int(smtp.get("port", 465))
    security = smtp.get("security", "ssl")
    username = smtp.get("username", "")
    password = _read_password(cfg)
    to_list = smtp.get("to", [])
    from_addr = smtp.get("from") or username or f"monitor@{host}"
    timeout = int(smtp.get("timeout", 30))

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg.set_content(_strip_html(html))
    msg.add_alternative(html, subtype="html")

    last_err: Exception | None = None
    for attempt in range(2):
        s = None
        try:
            if security == "ssl":
                s = smtplib.SMTP_SSL(host, port, timeout=timeout)
            elif security == "tls":
                s = smtplib.SMTP(host, port, timeout=timeout)
                s.ehlo()
                s.starttls()
                s.ehlo()
            else:
                s = smtplib.SMTP(host, port, timeout=timeout)
            if username:
                s.login(username, password)
            s.send_message(msg)
            return
        except Exception as e:  # noqa: BLE001 - 上抛给调用方统一处理
            last_err = e
            if s is not None:
                try:
                    s.quit()
                except Exception:
                    pass
            if attempt == 0:
                time.sleep(2)
    raise RuntimeError(f"SMTP 发送失败（已重试一次）: {last_err}")


# ---------------------------------------------------------------- 决策执行
def run_check(cfg: dict, state_path: str, force_window: bool, dry_run: bool) -> int:
    snapshot = collect_metrics(cfg)
    result = evaluate(snapshot)
    now = dt.datetime.now()

    if dry_run:
        state = load_state(state_path)
        decision, new_state = decide(state, result, now, cfg, force_window)
        _print_snapshot(snapshot)
        print(f"决策: {decision}")
        if result["exceeded"]:
            print("超限指标:")
            for k in result["exceeded"]:
                v = result["all"][k]
                print(f"  {k}: {v['percent']}% >= 阈值 {v['threshold']}%")
        print(f"当前状态: level={state.get('level')} last_sent={state.get('last_sent')}")
        print("(dry-run 模式：未发信、未写状态)")
        return 0

    lock_fd = acquire_lock(state_path)
    if lock_fd is None:
        print("上一轮检查仍在运行，本轮跳过。", file=sys.stderr)
        return 0
    try:
        state = load_state(state_path)
        decision, new_state = decide(state, result, now, cfg, force_window)
        _print_snapshot(snapshot)
        print(f"决策: {decision}")

        if decision in (SEND_ALARM, SEND_RECOVERY):
            status = "alarm" if decision == SEND_ALARM else "recovery"
            data = build_data(cfg, result, status, now)
            tpl = cfg["templates"]["alarm"] if decision == SEND_ALARM else cfg["templates"]["recovery"]
            subject, html = render(cfg, tpl, data)
            smtp_send(cfg, subject, html)
            print(f"已发送: {subject} → {', '.join(cfg['smtp']['to'])}")

        save_state(state_path, new_state)
        if decision in (SUPPRESS_WINDOW,):
            print("窗口外，静默（状态已记录，开窗后首轮补发）")
        elif decision == SUPPRESS_COOLDOWN:
            print("冷却期内，跳过（防止告警刷屏）")
        elif decision == SUPPRESS_DAILY_CAP:
            print("已达当日发送上限，跳过")
        return 0
    finally:
        release_lock(lock_fd)


def _print_snapshot(snapshot: dict) -> None:
    print("指标快照:")
    for key, v in snapshot.items():
        flag = " [超限]" if v["percent"] >= v["threshold"] else ""
        label = f"{v['metric']}({v.get('path', '')})" if v.get("path") else v["metric"]
        print(f"  {label:20s} {v['percent']:>6.1f}%  (阈值 {v['threshold']}%){flag}")


# ---------------------------------------------------------------- 子命令
def cmd_setup(args) -> int:
    missing = check_deps()
    if missing:
        print("缺少依赖:", ", ".join(missing))
        print("安装命令（国内镜像）:")
        print("  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil pyyaml jinja2")
        return 1

    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    print(f"配置目录: {CONFIG_DIR}")
    print(f"状态目录: {STATE_DIR}")

    cfg_path = os.path.abspath(os.path.expanduser(args.config))
    if os.path.exists(cfg_path):
        print(f"配置文件已存在: {cfg_path}")
    else:
        if os.path.exists(EXAMPLE_CONFIG):
            os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
            shutil.copy(EXAMPLE_CONFIG, cfg_path)
            print(f"已从模板生成配置: {cfg_path}")
        else:
            print(f"未找到配置模板 {EXAMPLE_CONFIG}，请手动创建 {cfg_path}")
            return 1
    print("\n下一步:")
    print("  1. 编辑配置文件，填入 SMTP 与阈值")
    print("  2. 运行 validate-config 校验")
    print("  3. 运行 send-test 发送测试邮件")
    print("  4. 用 install.sh 或 crontab -e 安装定时任务")
    return 0


def cmd_status(args) -> int:
    cfg = load_config(args.config)
    errors = validate_config(cfg)
    if errors:
        print("配置问题:")
        for e in errors:
            print(f"  ✗ {e}")
    snapshot = collect_metrics(cfg)
    _print_snapshot(snapshot)
    state = load_state(args.state)
    print("\n状态 (state.json):")
    print(json.dumps(state, ensure_ascii=False, indent=2))
    now = dt.datetime.now()
    in_win = window_open(cfg, now)
    print(f"\n当前时间: {now:%Y-%m-%d %H:%M:%S}  时间窗口: {'开' if in_win else '关'}")
    return 0


def cmd_send_test(args) -> int:
    cfg = load_config(args.config)
    errors = validate_config(cfg)
    if errors:
        print("配置有误，无法发送测试邮件:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    now = dt.datetime.now()
    result = {"is_alarm": True, "exceeded": ["cpu", "memory", "disk:/"], "all": {}}
    psutil = _load_psutil()
    result["all"] = {
        "cpu": {"metric": "CPU", "percent": 95.0, "threshold": 80},
        "memory": {"metric": "内存", "percent": 88.0, "threshold": 85},
        "disk:/": {"metric": "磁盘", "percent": 92.0, "threshold": 85, "path": "/"},
    }
    data = build_data(cfg, result, "test", now)
    tpl = cfg["templates"]["alarm"]
    subject, html = render(cfg, tpl, data)
    print(f"发送测试邮件 → {', '.join(cfg['smtp']['to'])}")
    print(f"主题: {subject}")
    smtp_send(cfg, subject, html)
    print("测试邮件已发送 ✓")
    return 0


def cmd_validate(args) -> int:
    try:
        cfg = load_config(args.config)
    except Exception as e:
        print(f"✗ 配置加载失败: {e}")
        return 1
    errors = validate_config(cfg)
    if errors:
        print("配置校验失败:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("✓ 配置校验通过")
    if args.smtp_connect:
        import smtplib

        smtp = cfg["smtp"]
        print(f"SMTP 连接测试 {smtp['host']}:{smtp['port']} ({smtp.get('security')}) ...")
        try:
            if smtp["security"] == "ssl":
                s = smtplib.SMTP_SSL(smtp["host"], int(smtp["port"]), timeout=int(smtp.get("timeout", 30)))
            elif smtp["security"] == "tls":
                s = smtplib.SMTP(smtp["host"], int(smtp["port"]), timeout=int(smtp.get("timeout", 30)))
                s.ehlo()
                s.starttls()
                s.ehlo()
            else:
                s = smtplib.SMTP(smtp["host"], int(smtp["port"]), timeout=int(smtp.get("timeout", 30)))
            try:
                if smtp.get("username"):
                    s.login(smtp["username"], _read_password(cfg))
                print("✓ SMTP 连接与认证成功")
            finally:
                s.quit()
        except Exception as e:
            print(f"✗ SMTP 连接失败: {e}")
            return 1
    return 0


def cmd_reset_state(args) -> int:
    path = os.path.abspath(os.path.expanduser(args.state))
    if os.path.exists(path):
        os.remove(path)
        print(f"已删除状态文件: {path}")
    else:
        print(f"状态文件不存在: {path}")
    return 0


# ---------------------------------------------------------------- 入口
def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=DEFAULT_CONFIG, help="配置文件路径（默认 ~/.config/resource-monitor/config.yaml）")
    common.add_argument("--state", default=DEFAULT_STATE, help="状态文件路径（默认 ~/.local/state/resource-monitor/state.json）")

    p = argparse.ArgumentParser(prog="monitor.py", description="服务器资源监控通知")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("setup", parents=[common], help="首次初始化：检查依赖、生成目录、复制配置模板")

    c = sub.add_parser("check", parents=[common], help="单次检查（cron 入口）")
    c.add_argument("--now", action="store_true", help="跳过时间窗口判断（当作窗口开）")
    c.add_argument("--dry-run", action="store_true", help="只打印决策，不发信、不写状态")

    sub.add_parser("status", parents=[common], help="打印指标快照与状态")

    sub.add_parser("send-test", parents=[common], help="发送测试邮件")

    v = sub.add_parser("validate-config", parents=[common], help="校验配置")
    v.add_argument("--smtp-connect", action="store_true", help="额外执行 SMTP 连接与认证测试")

    sub.add_parser("reset-state", parents=[common], help="清空运行状态")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "setup":
            return cmd_setup(args)
        if args.command == "check":
            cfg = load_config(args.config)
            return run_check(cfg, args.state, args.now, args.dry_run)
        if args.command == "status":
            return cmd_status(args)
        if args.command == "send-test":
            return cmd_send_test(args)
        if args.command == "validate-config":
            return cmd_validate(args)
        if args.command == "reset-state":
            return cmd_reset_state(args)
    except FileNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001 - CLI 顶层兜底
        print(f"✗ 运行出错: {e}", file=sys.stderr)
        if os.environ.get("RESOURCE_MONITOR_DEBUG"):
            traceback.print_exc()
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
