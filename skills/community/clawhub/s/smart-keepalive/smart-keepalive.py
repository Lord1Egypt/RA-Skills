#!/usr/bin/env python3
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
from html import unescape
from datetime import date, datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

# RSSHub 公共实例（按顺序 failover）。可用 KEEPALIVE_RSSHUB_BASES 覆盖（逗号分隔完整 base URL）。
# 主消息首行标题（Markdown 加粗），与 prompts/rewrite-main.md 一致；zh/en 同一行。
# 「保活」双关 keepalive（定时在线）与「让资讯保持鲜活」；简报 = 智能提要；后缀 keepalive 点题。
REPORT_TITLE_MD = "**保活简报 keepalive**"


DEFAULT_RSSHUB_BASES: tuple[str, ...] = (
    "https://rsshub.liumingye.cn",
    "https://rsshub.pseudoyu.com",
)
DEFAULT_NMC_WEATHER_DAILY_URL = "https://www.nmc.cn/publish/forecast/ABJ/beijing.html"

# 简报加权池基准权重 + BRIEF_FALLBACK_WEIGHT 应合计为 1.0（见 `build_keepalive_brief` 内 assert）
BRIEF_FALLBACK_WEIGHT = 0.10

BRIEF_TAG_KEYS: tuple[str, ...] = (
    "bilibili-weekly",
    "zhihu-daily",
    "infzm-recommends",
    "idaily-today",
    "sspai-feed",
    "guokr-scientific",
    "rfi-cn",
    "xinhua-whxw",
    "36kr-feed",
    "nmc-weather-daily",
)


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def normalize_channel_alias(channel: str) -> str:
    if channel == "lark":
        return "feishu"
    return channel


def trim_message(msg: str) -> str:
    s = msg.replace("\r", "")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def has_custom_agent_command(environ: Optional[dict[str, str]] = None) -> bool:
    env = environ if environ is not None else os.environ
    return bool((env.get("KEEPALIVE_AGENT_COMMAND", "") or "").strip())


def has_custom_send_command(environ: Optional[dict[str, str]] = None) -> bool:
    env = environ if environ is not None else os.environ
    return bool((env.get("KEEPALIVE_SEND_COMMAND", "") or "").strip())


def resolve_openclaw_bin(environ: Optional[dict[str, str]] = None) -> Optional[str]:
    """解析 CLI 可执行路径。默认 openclaw，可通过 KEEPALIVE_CLI_BIN 指向 hermes。"""
    env = environ if environ is not None else os.environ
    for key in ("KEEPALIVE_CLI_BIN", "OPENCLAW_BIN", "OPENCLAW"):
        cand = env.get(key)
        if cand and os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    path_var = env.get("PATH") or ""
    for name in ("openclaw", "hermes"):
        in_path = shutil.which(name, path=path_var)
        if in_path:
            return in_path
    home = str(Path.home())
    nvm_dir = env.get("NVM_DIR") or str(Path(home) / ".nvm")
    candidates = [
        str(Path(home) / ".local/bin/openclaw"),
        str(Path(home) / ".local/bin/hermes"),
        str(Path(home) / "bin/openclaw"),
        str(Path(home) / "bin/hermes"),
        "/opt/homebrew/bin/openclaw",
        "/opt/homebrew/bin/hermes",
        "/usr/local/bin/openclaw",
        "/usr/local/bin/hermes",
    ]
    node_ver = ""
    try:
        sub_env = dict(env)
        node_ver = subprocess.run(
            ["node", "-v"],
            capture_output=True,
            text=True,
            timeout=2,
            env=sub_env,
        ).stdout.strip()
    except Exception:
        node_ver = ""
    if node_ver:
        candidates.append(f"{nvm_dir}/versions/node/{node_ver}/bin/openclaw")
    for cand in candidates:
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    return None


def run_shell_command(
    command: str,
    timeout_sec: int,
    cwd: Optional[Path] = None,
    extra_env: Optional[dict[str, str]] = None,
) -> tuple[int, str]:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    return run_cmd(["/bin/sh", "-lc", command], timeout_sec=timeout_sec, cwd=cwd, env=env)


def run_agent_command(
    openclaw_bin: str,
    agent_id: str,
    prompt: str,
    timeout_sec: int,
) -> tuple[int, str]:
    custom = os.getenv("KEEPALIVE_AGENT_COMMAND", "").strip()
    if custom:
        return run_shell_command(
            custom,
            timeout_sec=timeout_sec,
            cwd=None,
            extra_env={
                "KEEPALIVE_PROMPT": prompt,
                "KEEPALIVE_AGENT_ID": agent_id,
                "KEEPALIVE_CLI_BIN": openclaw_bin or "",
            },
        )
    if not openclaw_bin:
        return 127, "openclaw/hermes binary not found"
    return run_cmd(
        [
            openclaw_bin,
            "agent",
            "--agent",
            agent_id,
            "--thinking",
            "minimal",
            "--message",
            prompt,
        ],
        timeout_sec=timeout_sec,
        cwd=None,
        env={k: v for k, v in os.environ.items() if k not in ["SKILL_DIR", "OPENCLAW_HOME", "OPENCLAW_CONFIG"]},
    )


def run_send_command(
    openclaw_bin: str,
    message: str,
    channel: str,
    target: str,
    cwd: Path,
    timeout_sec: int,
) -> tuple[int, str]:
    custom = os.getenv("KEEPALIVE_SEND_COMMAND", "").strip()
    if custom:
        custom_cwd = cwd if cwd.is_dir() else None
        return run_shell_command(
            custom,
            timeout_sec=timeout_sec,
            cwd=custom_cwd,
            extra_env={
                "KEEPALIVE_MESSAGE": message,
                "KEEPALIVE_CHANNEL": channel,
                "KEEPALIVE_TARGET": target,
                "KEEPALIVE_CLI_BIN": openclaw_bin or "",
            },
        )
    if not openclaw_bin:
        return 127, "openclaw/hermes binary not found"
    args = [openclaw_bin, "message", "send", "--message", message]
    if channel:
        args += ["--channel", channel]
    if target:
        args += ["--target", target]
    return run_cmd(args, timeout_sec=timeout_sec, cwd=cwd)


def resolve_openclaw_config() -> Optional[Path]:
    env_cfg = os.getenv("OPENCLAW_CONFIG")
    cands = [
        env_cfg,
        str(Path.cwd() / "openclaw.json"),
        str(Path.cwd() / ".openclaw/openclaw.json"),
        str(Path.home() / ".openclaw/openclaw.json"),
    ]
    for c in cands:
        if c and Path(c).is_file():
            return Path(c)
    return None


def run_cmd(
    args: list[str],
    timeout_sec: int,
    cwd: Optional[Path] = None,
    env: Optional[dict[str, str]] = None,
) -> tuple[int, str]:
    try:
        p = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(cwd) if cwd else None,
            env=env if env is not None else os.environ.copy(),
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired as ex:
        out = (ex.stdout or "") + (ex.stderr or "")
        return 124, out + f"\n[timeout] command exceeded {timeout_sec}s\n"
    except Exception as ex:
        return 125, f"[exec-error] {ex}\n"


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_local_config(skill_dir: Path) -> dict[str, Any]:
    cfg_file = skill_dir / "config.json"
    if not cfg_file.is_file():
        return {}
    return read_json(cfg_file)


def write_local_config(skill_dir: Path, data: dict[str, Any]) -> None:
    cfg_file = skill_dir / "config.json"
    cfg_file.parent.mkdir(parents=True, exist_ok=True)
    cfg_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_weather_city(skill_dir: Path) -> str:
    """解析天气城市：环境变量 > 本地 config.json > 默认北京。"""
    env_city = (os.getenv("KEEPALIVE_WEATHER_CITY", "") or "").strip()
    if env_city:
        return env_city
    local_cfg = read_local_config(skill_dir) if skill_dir.is_dir() else {}
    city = str(local_cfg.get("weatherCity", "")).strip()
    if city:
        return city
    script_dir = Path(__file__).parent.resolve()
    if script_dir != skill_dir:
        local_cfg2 = read_local_config(script_dir)
        city2 = str(local_cfg2.get("weatherCity", "")).strip()
        if city2:
            return city2
    return "北京"


def weather_append_enabled() -> bool:
    v = os.getenv("KEEPALIVE_APPEND_WEATHER", "1").strip().lower()
    return v not in ("0", "off", "false", "no")


def weather_strict_realtime_enabled() -> bool:
    """默认严格模式：温度仅信任 /rest/weather 实时接口。"""
    v = os.getenv("KEEPALIVE_WEATHER_STRICT_REALTIME", "1").strip().lower()
    return v not in ("0", "off", "false", "no")


def normalize_city_name(city: str) -> str:
    s = (city or "").strip()
    if not s:
        return ""
    for suf in ("特别行政区", "自治州", "地区", "盟", "市", "区", "县"):
        if s.endswith(suf) and len(s) > len(suf):
            s = s[: -len(suf)]
            break
    return s


def get_default_channel_target(cfg: dict[str, Any]) -> tuple[str, str]:
    ad = cfg.get("agents", {}).get("defaults", {})
    kp = ad.get("keepalive", {}) if isinstance(ad, dict) else {}
    msg = cfg.get("message", {})
    channel = ""
    target = ""
    for v in (kp.get("channel"), ad.get("channel"), msg.get("defaultChannel")):
        if isinstance(v, str) and v.strip():
            channel = normalize_channel_alias(v.strip())
            break
    for v in (kp.get("target"), ad.get("target"), msg.get("defaultTarget")):
        if isinstance(v, str) and v.strip():
            target = v.strip()
            break
    if not target and channel:
        ch = cfg.get("channels", {}).get(channel, {})
        if isinstance(ch, dict):
            groups = ch.get("groups", {})
            if isinstance(groups, dict):
                for gid in groups.keys():
                    if isinstance(gid, str) and gid.strip() and gid != "*":
                        target = gid.strip()
                        break
    if not channel:
        channels = cfg.get("channels", {})
        if isinstance(channels, dict):
            for name, conf in channels.items():
                if isinstance(name, str) and isinstance(conf, dict) and conf.get("enabled") is True:
                    channel = normalize_channel_alias(name.strip())
                    break
    return channel, target


def resolve_effective_channel_target(
    cfg: dict[str, Any], skill_dir: Path
) -> tuple[str, str]:
    """未设置环境变量时：默认仅使用 skill 本地 config.json，避免误发到固定会话（如 heartbeat）。
    
    特殊规则：如果没有 target，则不设置 channel（让 CLI 自动路由到当前会话）。
    
    注意：skill_dir 可能来自 SKILL_DIR 环境变量（可能是虚拟路径），
    所以我们也检查脚本实际所在目录的 config.json。
    """
    default_channel, default_target = get_default_channel_target(cfg)
    follow_openclaw_defaults = os.getenv("KEEPALIVE_FOLLOW_OPENCLAW_DEFAULTS", "").strip() == "1"
    
    # 尝试从多个位置读取 config.json
    local_channel = ""
    local_target = ""
    
    # 1. SKILL_DIR 指定的目录
    if skill_dir.is_dir():
        local_cfg = read_local_config(skill_dir)
        if local_cfg:
            local_channel = str(local_cfg.get("defaultChannel", "")).strip()
            local_target = str(local_cfg.get("defaultTarget", "")).strip()
    
    # 2. 脚本实际所在目录（__file__）
    if not local_channel or not local_target:
        script_dir = Path(__file__).parent.resolve()
        if script_dir != skill_dir:
            local_cfg2 = read_local_config(script_dir)
            if local_cfg2:
                if not local_channel:
                    local_channel = str(local_cfg2.get("defaultChannel", "")).strip()
                if not local_target:
                    local_target = str(local_cfg2.get("defaultTarget", "")).strip()
    
    ch_env = os.getenv("KEEPALIVE_CHANNEL")
    tg_env = os.getenv("KEEPALIVE_TARGET")
    
    # 优先级：环境变量 > config.json (local) > （可选）openclaw.json (default)
    explicit_channel = False
    if ch_env is not None:
        channel = normalize_channel_alias(ch_env.strip()) if ch_env.strip() else ""
        explicit_channel = bool(channel)
    else:
        base_channel = local_channel or (default_channel if follow_openclaw_defaults else "")
        channel = normalize_channel_alias(base_channel)
        explicit_channel = bool(local_channel)
    
    if tg_env is not None:
        target = tg_env.strip()
    else:
        target = local_target or (default_target if follow_openclaw_defaults else "")
    
    # 没有 target 时：
    # - 显式配置了 channel（env/local）=> 保留 channel，尊重用户配置
    # - 否则清空 channel，让 CLI 自动路由到当前会话
    if not target and not explicit_channel:
        channel = ""
    
    return channel, target


def validate_channel(cfg: dict[str, Any], channel: str) -> tuple[bool, str]:
    if not channel:
        return True, ""
    channels = cfg.get("channels", {})
    if not isinstance(channels, dict) or channel not in channels:
        return False, f"ERROR: channel '{channel}' not found in openclaw.json."
    ch = channels.get(channel, {})
    if isinstance(ch, dict) and ch.get("enabled") is False:
        return (
            False,
            f"ERROR: channel '{channel}' is disabled in openclaw.json (set enabled=true).",
        )
    return True, ""


def load_locale(skill_dir: Path) -> str:
    voice = skill_dir / "voice.json"
    if not voice.is_file():
        return "zh"
    try:
        return str(json.loads(voice.read_text(encoding="utf-8")).get("locale", "zh"))
    except Exception:
        return "zh"


def available_channels(cfg: dict[str, Any]) -> list[str]:
    channels = cfg.get("channels", {})
    if not isinstance(channels, dict):
        return []
    result: list[str] = []
    for name, conf in channels.items():
        if not isinstance(name, str) or not isinstance(conf, dict):
            continue
        if conf.get("enabled") is True:
            result.append(name)
    return result


def interactive_setup(skill_dir: Path, cfg: dict[str, Any]) -> int:
    channels = available_channels(cfg)
    if not channels:
        eprint("未找到可用 channel。请先在 openclaw.json 的 channels 中启用至少一个渠道。")
        return 1
    print("=== Smart Keepalive 配置向导 ===")
    print("提示：target 留空时，将默认发送到当前会话（不固定到 heartbeat 或其他会话）。")
    print("可用渠道：")
    for idx, ch in enumerate(channels, 1):
        print(f"  {idx}. {ch}")
    choice = input(f"请选择渠道 [1-{len(channels)}，回车=自动路由]: ").strip()
    picked = ""
    if choice:
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(channels):
            eprint("输入无效。")
            return 1
        picked = channels[int(choice) - 1]
    local_cfg = read_local_config(skill_dir)
    old_target = str(local_cfg.get("defaultTarget", "")).strip()
    target_prompt = "请输入目标 target（例如 user:ou_xxx 或 group:chat_id；留空=当前会话）"
    if old_target:
        target_prompt += f" [默认 {old_target}]"
    target = input(target_prompt + ": ").strip() or old_target
    old_city = str(local_cfg.get("weatherCity", "")).strip() or "北京"
    city = input(f"请输入天气城市（用于天气提取，如 北京/上海） [默认 {old_city}]: ").strip() or old_city
    if normalize_city_name(city) != "北京":
        print(
            "提示：当前输入不是北京。请先打开 "
            "https://www.nmc.cn/publish/forecast/ABJ/beijing.html 选择你想要的城市，"
            "然后让用户的 LLM 记住该城市名称。"
        )
    merged_cfg = dict(local_cfg)
    merged_cfg.update(
        {
            "defaultChannel": picked,
            "defaultTarget": target,
            "weatherCity": city,
        }
    )
    write_local_config(
        skill_dir,
        merged_cfg,
    )
    print(f"已保存配置：{skill_dir / 'config.json'}")
    return 0


def print_scheduler_prompt(openclaw_home: Path, skill_dir: Path, mode: str) -> int:
    keepalive_sh = skill_dir / "smart-keepalive.sh"
    if not keepalive_sh.is_file():
        eprint(f"未找到脚本：{keepalive_sh}")
        return 2
    log_path = openclaw_home / "logs" / "smart-keepalive.log"
    if mode == "launchd":
        print("=== 请把下面提示词直接发给 OpenClaw（创建 macOS launchd 定时任务）===\n")
        print(
            f"""请帮我创建一个 macOS launchd 定时任务：
- Label: com.openclaw.smart-keepalive
- 执行命令: /bin/bash "{keepalive_sh}"
- 执行频率: 每 4 小时一次（StartInterval=14400）
- RunAtLoad: true
- 日志输出到: "{log_path}"
- 环境变量里请至少包含:
  - OPENCLAW_HOME="{openclaw_home}"
  - PATH 保留当前 shell 可用的 node/openclaw 路径
  - KEEPALIVE_TARGET 设为当前会话 target（不要留空，不要路由到 heartbeat 会话）

创建后请自动 load 并告诉我如何验证任务是否生效。"""
        )
        return 0
    print("=== 请把下面提示词直接发给 OpenClaw（创建 Linux cron 定时任务）===\n")
    print(
        f"""请帮我创建一个 cron 定时任务：
- 执行频率: 每 4 小时一次（0 */4 * * *）
- 执行命令: /bin/bash "{keepalive_sh}"
- 日志追加到: "{log_path}"
- 环境变量:
  - OPENCLAW_HOME="{openclaw_home}"
  - PATH 保留当前 shell 可用的 node/openclaw 路径
  - KEEPALIVE_TARGET 设为当前会话 target（不要留空，不要路由到 heartbeat 会话）

创建后请返回最终 crontab 内容，并告诉我如何验证任务是否生效。"""
    )
    return 0


def fetch_rss_titles(feed_url: str, count: int = 5, max_retries: int = 5, with_links: bool = False) -> str:
    """获取 RSS 标题，支持重试机制和链接。
    
    Args:
        feed_url: RSS 源 URL
        count: 获取标题数量
        max_retries: 最大重试次数（默认 5 次）
        with_links: 是否返回链接（默认 False）
    
    Returns:
        标题列表（换行分隔），失败返回空字符串
        with_links=True 时返回 "标题 [链接]" 格式
    """
    import time
    import urllib.parse
    import urllib.request
    import xml.etree.ElementTree as ET

    url = (feed_url or "").strip()
    if not url:
        return ""
    count = max(1, min(count, 15))
    
    last_error = None
    for attempt in range(max_retries):
        try:
            # Encode non-ASCII URLs safely.
            parts = urllib.parse.urlsplit(url)
            safe_url = urllib.parse.urlunsplit(
                (
                    parts.scheme,
                    parts.netloc.encode("idna").decode("ascii"),
                    urllib.parse.quote(parts.path),
                    parts.query,
                    parts.fragment,
                )
            )
            req = urllib.request.Request(
                safe_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
                    ),
                },
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
            root = ET.fromstring(data)
            
            items = root.findall(".//item")
            if not items:
                return ""
                
            out: list[str] = []
            for i, it in enumerate(items[:count], 1):
                title = (it.findtext("title") or "").strip()
                link = (it.findtext("link") or "").strip()
                if title:
                    if with_links and link:
                        out.append(f"{title} [{link}]")
                    else:
                        out.append(f"{i}. {title}")
            
            if out:
                return "\n".join(out)
            else:
                return ""
                
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                # 指数退避：0.5s, 1s, 2s, 4s
                time.sleep(0.5 * (2 ** attempt))
                continue
    
    # 所有重试都失败
    return ""


def _normalize_rsshub_base(base: str) -> str:
    b = (base or "").strip().rstrip("/")
    if not b:
        return ""
    if not (b.startswith("http://") or b.startswith("https://")):
        b = "https://" + b
    return b


def rsshub_bases() -> list[str]:
    """RSSHub 根地址列表；环境变量优先。"""
    raw = os.getenv("KEEPALIVE_RSSHUB_BASES", "").strip()
    if raw:
        out = [_normalize_rsshub_base(x) for x in raw.split(",")]
        return [x for x in out if x]
    return [_normalize_rsshub_base(x) for x in DEFAULT_RSSHUB_BASES if x]


def fetch_rsshub_route(
    route: str, count: int = 5, with_links: bool = False
) -> str:
    """对多个 RSSHub 实例依次尝试 `base/route`，首个非空结果返回。单实例少次重试以便快速换下一域名。"""
    path = (route or "").strip().strip("/")
    if not path:
        return ""
    for base in rsshub_bases():
        url = f"{base}/{path}"
        got = fetch_rss_titles(url, count, max_retries=2, with_links=with_links)
        if got.strip():
            return got
    return ""


def fetch_bilibili_hot_search(count: int = 5) -> str:
    """获取 B 站热搜（官方 API）。
    
    Args:
        count: 获取数量
    
    Returns:
        标题 + 链接列表（换行分隔）
    """
    import json
    import urllib.request
    
    url = "https://api.bilibili.com/x/web-interface/ranking/v2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        if data.get('code') != 0:
            return ""
        
        items = data.get('data', {}).get('list', [])[:count]
        out = []
        for item in items:
            title = item.get('title', '').strip()
            bvid = item.get('bvid', '')
            if title and bvid:
                link = f"https://www.bilibili.com/video/{bvid}"
                out.append(f"{title} [{link}]")
        
        return "\n".join(out) if out else ""
    except Exception:
        return ""


def _extract_nmc_daily_weather_points(text: str, count: int) -> list[str]:
    """从中央气象台「每日天气提示」页面提炼关键句。"""
    if not text:
        return []
    cleaned = unescape(text)
    cleaned = re.sub(r"<script[\s\S]*?</script>", " ", cleaned, flags=re.I)
    cleaned = re.sub(r"<style[\s\S]*?</style>", " ", cleaned, flags=re.I)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    fragments = re.split(r"[。！？]", cleaned)
    keywords = (
        "大风",
        "沙尘",
        "降温",
        "大雾",
        "降雨",
        "暴雨",
        "强对流",
        "雨雪",
        "预警",
        "气温",
    )
    reject_keywords = (
        "热门城市",
        "天气实况",
        "天气预报",
        "台风海洋",
        "全球预报",
        "环境气象",
        "农业气象",
        "数值预报",
        "当前位置",
        "字号",
        "打印",
        "首页",
    )
    out: list[str] = []
    for frag in fragments:
        s = (frag or "").strip(" ：:，,；;。")
        if len(s) < 12:
            continue
        if any(k in s for k in reject_keywords):
            continue
        if not any(k in s for k in keywords):
            continue
        if len(s) > 110:
            s = s[:110].rstrip("，,；; ") + "…"
        if s in out:
            continue
        out.append(s)
        if len(out) >= count:
            break
    return out


def _extract_nmc_city_snapshot(text: str, city: str) -> str:
    """在页面文本中提取指定城市实况片段，如：北京 18.3℃ 西南风 微风。"""
    if not text or not city:
        return ""
    cleaned = unescape(text)
    cleaned = re.sub(r"<script[\s\S]*?</script>", " ", cleaned, flags=re.I)
    cleaned = re.sub(r"<style[\s\S]*?</style>", " ", cleaned, flags=re.I)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    pattern = re.compile(
        rf"({re.escape(city)}\s+-?\d+(?:\.\d+)?℃\s+[^\s]{{1,10}}\s+[^\s]{{1,10}})",
        re.I,
    )
    m = pattern.search(cleaned)
    return (m.group(1) if m else "").strip()


def _extract_nmc_publish_time(text: str) -> str:
    """提取页面中的天气提示发布时间，如 2026-04-20 08时。"""
    if not text:
        return ""
    m = re.search(
        r"\*\*(\d{4})\*\*\s*年\s*\*\*(\d{2})\*\*\s*月\s*\*\*(\d{2})\*\*\s*日\s*\*\*(\d{2})\*\*\s*时",
        text,
    )
    if not m:
        m = re.search(r"(\d{4})\s*年\s*(\d{2})\s*月\s*(\d{2})\s*日\s*(\d{2})\s*时", text)
    if not m:
        return ""
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4)}时"


def _fetch_json_url(url: str, timeout: int = 12) -> Any:
    import urllib.request

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
            ),
            "Accept": "application/json",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


@lru_cache(maxsize=256)
def _resolve_nmc_station_code(city: str, base: str) -> str:
    """通过 NMC 省市接口解析城市对应站点 code。"""
    city_name = normalize_city_name(city)
    if not city_name:
        return ""
    try:
        all_provinces = _fetch_json_url(f"{base}/rest/province/all")
    except Exception:
        return ""
    if not isinstance(all_provinces, list):
        return ""
    for p in all_provinces:
        pcode = str((p or {}).get("code") or "").strip()
        if not pcode:
            continue
        try:
            cities = _fetch_json_url(f"{base}/rest/province/{pcode}")
        except Exception:
            continue
        if not isinstance(cities, list):
            continue
        for c in cities:
            cname = str((c or {}).get("city") or "").strip()
            if cname == city_name or normalize_city_name(cname) == city_name:
                return str((c or {}).get("code") or "").strip()
    return ""


def _nmc_base_url() -> str:
    """从天气 URL 推导 API 基础域名，保证数据源一致。"""
    import urllib.parse

    raw = os.getenv("KEEPALIVE_NMC_WEATHER_URL", "").strip() or DEFAULT_NMC_WEATHER_DAILY_URL
    try:
        u = urllib.parse.urlsplit(raw)
        if u.scheme and u.netloc:
            return f"{u.scheme}://{u.netloc}"
    except Exception:
        pass
    return "https://www.nmc.cn"


def _fetch_nmc_realtime_city_weather(city: str) -> tuple[str, str]:
    """读取 NMC 实时接口，返回 (天气行主体, 发布时间)。"""
    city_name = normalize_city_name(city)
    if not city_name:
        return "", ""
    base = _nmc_base_url()
    code = _resolve_nmc_station_code(city_name, base)
    if not code:
        return "", ""
    ts = int(datetime.now().timestamp())
    try:
        payload = _fetch_json_url(f"{base}/rest/weather?stationid={code}&_ts={ts}")
    except Exception:
        return "", ""
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        return "", ""
    real = data.get("real")
    if not isinstance(real, dict):
        return "", ""
    station = real.get("station") if isinstance(real.get("station"), dict) else {}
    weather = real.get("weather") if isinstance(real.get("weather"), dict) else {}
    wind = real.get("wind") if isinstance(real.get("wind"), dict) else {}
    c = str(station.get("city") or city_name).strip() or city_name
    temp = weather.get("temperature")
    temp_s = "-" if temp in (None, "9999", 9999) else f"{temp}℃"
    wd = str(wind.get("direct") or "-").strip()
    ws = str(wind.get("power") or "-").strip()
    line = f"天气：{c} {temp_s} {wd} {ws}"
    publish_time = str(real.get("publish_time") or "").strip()
    return line, publish_time


def fetch_nmc_weather_daily(city: str, count: int = 1, with_links: bool = False) -> str:
    """抓取中央气象台每日天气提示并按城市提取单行天气信息。"""
    import urllib.request

    url = os.getenv("KEEPALIVE_NMC_WEATHER_URL", "").strip() or DEFAULT_NMC_WEATHER_DAILY_URL
    ts = int(datetime.now().timestamp())
    fetch_url = f"{url}{'&' if '?' in url else '?'}_ts={ts}"
    try:
        req = urllib.request.Request(
            fetch_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
                ),
                "Cache-Control": "no-cache, no-store, max-age=0",
                "Pragma": "no-cache",
            },
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            html_text = resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""

    city_name = normalize_city_name(city) or "北京"
    realtime_line, realtime_publish = _fetch_nmc_realtime_city_weather(city_name)
    if weather_strict_realtime_enabled() and not realtime_line:
        return ""
    publish_time = _extract_nmc_publish_time(html_text)
    city_snapshot = _extract_nmc_city_snapshot(html_text, city_name)
    points = _extract_nmc_daily_weather_points(html_text, max(1, min(count, 5)))
    if not realtime_line and not points and not city_snapshot:
        return ""
    out: list[str] = []
    if realtime_line:
        out.append(realtime_line)
    elif city_snapshot:
        out.append(f"天气：{city_snapshot}")
    else:
        out.append(f"天气：{city_name}（页面未命中该城市实况，以下为全国天气提示）")
    if points:
        # 让同一天不同时段可读到不同提醒，避免“永远同一句”的观感。
        pick_idx = (datetime.now().day + datetime.now().hour) % len(points)
        picked = points[pick_idx].strip()
        if len(picked) > 48:
            picked = picked[:48].rstrip("，,；; ") + "…"
        out[0] = f"{out[0]}｜提示：{picked}"
    if realtime_publish:
        out[0] = f"{out[0]}｜发布时间：{realtime_publish}"
    elif publish_time:
        out[0] = f"{out[0]}｜发布时间：{publish_time}"
    first_line = out[0]
    if with_links:
        return f"{first_line} [{url}]"
    return first_line


def pick_rotating_theme() -> int:
    """按 4 小时窗口轮转 4 个主题（1->2->3->4）。"""
    slot = int(datetime.now().timestamp()) // (4 * 3600)
    return (slot % 4) + 1


def _brief_state_path() -> Path:
    raw = os.getenv("KEEPALIVE_BRIEF_STATE_FILE", "").strip()
    if raw:
        return Path(os.path.expanduser(raw))
    return Path.home() / ".smart-keepalive" / "brief-sources.json"


def _brief_audit_log_path() -> Path:
    """与状态文件同目录、同名加 `-audit.log`，避免同目录多份状态时审计串线。"""
    sp = _brief_state_path()
    return sp.parent / f"{sp.stem}-audit.log"


def _resolve_keepalive_log_path() -> Path:
    """与主流程 `LOG_FILE` / `OPENCLAW_HOME` 一致，便于排查。"""
    lf = os.getenv("LOG_FILE", "").strip()
    if lf:
        return Path(os.path.expanduser(lf))
    oh = os.getenv("OPENCLAW_HOME", "").strip()
    if oh:
        return Path(oh) / "logs" / "smart-keepalive.log"
    return Path.home() / ".openclaw" / "logs" / "smart-keepalive.log"


def _brief_audit_enabled() -> bool:
    return os.getenv("KEEPALIVE_BRIEF_AUDIT_LOG", "1").strip().lower() not in (
        "0",
        "off",
        "false",
        "no",
    )


def _brief_log_to_main_enabled() -> bool:
    return os.getenv("KEEPALIVE_BRIEF_LOG_TO_MAIN", "1").strip().lower() not in (
        "0",
        "off",
        "false",
        "no",
    )


def _brief_append_audit_line(
    date: str, added_tag: str, used: set[str], state_path: str
) -> None:
    if not _brief_audit_enabled():
        return
    p = _brief_audit_log_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        keys = ",".join(sorted(used))
        line = f"{ts}\t{date}\t{added_tag}\tcount={len(used)}\t{keys}\tstate={state_path}\n"
        with p.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def _brief_append_main_log_line(date: str, added_tag: str, used_count: int) -> None:
    if not _brief_log_to_main_enabled():
        return
    lp = _resolve_keepalive_log_path()
    try:
        lp.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = (
            f"{ts} [brief-sources] date={date} recorded={added_tag} "
            f"used_total={used_count} file={_brief_state_path()}\n"
        )
        with lp.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def _load_brief_state() -> tuple[str, set[str], dict[str, Any]]:
    """返回 (today, used_today, tag_meta)。tag_meta[tag] = {last, prior} 用于跨日新鲜度衰减。"""
    today = datetime.now().strftime("%Y-%m-%d")
    p = _brief_state_path()
    if not p.is_file():
        return today, set(), {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return today, set(), {}
        d = str(data.get("date") or "").strip()
        raw_meta = data.get("tag_meta")
        tag_meta: dict[str, Any] = raw_meta if isinstance(raw_meta, dict) else {}
        if d != today:
            return today, set(), tag_meta
        used = data.get("used")
        if isinstance(used, list):
            return today, {str(x) for x in used if x}, tag_meta
        return today, set(), tag_meta
    except Exception:
        return today, set(), {}


def _save_brief_state(
    date: str, used: set[str], tag_meta: dict[str, Any], added_tag: str = ""
) -> None:
    """原子写入 JSON；可选记录本次新增的源标签到审计日志与主日志。"""
    p = _brief_state_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            {"date": date, "used": sorted(used), "tag_meta": tag_meta},
            ensure_ascii=False,
            indent=0,
        )
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_text(payload, encoding="utf-8")
        tmp.replace(p)
        if added_tag:
            _brief_append_audit_line(date, added_tag, used, str(p))
            _brief_append_main_log_line(date, added_tag, len(used))
    except Exception:
        pass


def _tag_meta_streak_penalty(tag_meta: dict[str, Any], tag: str, today: str) -> float:
    """连续两个日历日都选中同一源时，下一日该源权重 ×0.5。"""
    if not _brief_freshness_enabled():
        return 1.0
    old = tag_meta.get(tag)
    if not isinstance(old, dict):
        return 1.0
    last = old.get("last")
    prior = old.get("prior")
    if not last or prior is None:
        return 1.0
    try:
        d_last = date.fromisoformat(str(last))
        d_prior = date.fromisoformat(str(prior))
        d_today = date.fromisoformat(today)
    except ValueError:
        return 1.0
    if (d_last - d_prior).days == 1 and (d_today - d_last).days == 1:
        return 0.5
    return 1.0


def _tag_meta_record_pick(tag_meta: dict[str, Any], tag: str, today: str) -> None:
    y = (date.fromisoformat(today) - timedelta(days=1)).isoformat()
    old = tag_meta.get(tag)
    last = None
    if isinstance(old, dict):
        last = old.get("last")
    if last == y:
        tag_meta[tag] = {"prior": last, "last": today}
    else:
        tag_meta[tag] = {"prior": None, "last": today}


def _brief_daily_once_enabled() -> bool:
    v = os.getenv("KEEPALIVE_BRIEF_DAILY_ONCE", "1").strip().lower()
    return v not in ("0", "off", "false", "no")


def _brief_freshness_enabled() -> bool:
    return os.getenv("KEEPALIVE_BRIEF_FRESHNESS", "1").strip().lower() not in (
        "0",
        "off",
        "false",
        "no",
    )


def _brief_rotation_enabled() -> bool:
    return os.getenv("KEEPALIVE_BRIEF_ROTATION", "1").strip().lower() not in (
        "0",
        "off",
        "false",
        "no",
    )


def _brief_holiday_boost_enabled() -> bool:
    return os.getenv("KEEPALIVE_BRIEF_HOLIDAY_BOOST", "1").strip().lower() not in (
        "0",
        "off",
        "false",
        "no",
    )


def _brief_chaos_probability() -> float:
    """0~1，0 关闭「盲盒」均匀随机。"""
    raw = os.getenv("KEEPALIVE_BRIEF_CHAOS", "0.1").strip()
    try:
        p = float(raw)
    except ValueError:
        return 0.1
    return max(0.0, min(1.0, p))


def _brief_time_weights_enabled() -> bool:
    return os.getenv("KEEPALIVE_BRIEF_TIME_WEIGHTS", "1").strip().lower() not in (
        "0",
        "off",
        "false",
        "no",
    )


def _brief_time_bucket() -> str:
    """本地时间分段：凌晨国外 / 早新闻 / 日科技·热 / 晚轻松。"""
    h = datetime.now().hour
    if 0 <= h < 6:
        return "night"
    if 6 <= h < 10:
        return "morning"
    if 10 <= h < 17:
        return "day"
    return "evening"


def _brief_time_weight_multipliers(bucket: str) -> dict[str, float]:
    """各时段对加权池内源的相对乘数（与「今日已用」无关，在过滤后再归一化）。"""
    m = {t: 1.0 for t in BRIEF_TAG_KEYS}
    if not _brief_time_weights_enabled():
        return m
    if bucket == "night":
        for t in ("idaily-today", "rfi-cn"):
            m[t] = 2.2
        for t in ("zhihu-daily", "infzm-recommends"):
            m[t] = 1.5
        m["xinhua-whxw"] = 1.1
        m["nmc-weather-daily"] = 1.25
        m["36kr-feed"] = 1.0
        for t in ("bilibili-weekly", "sspai-feed", "guokr-scientific"):
            m[t] = 0.35
    elif bucket == "morning":
        for t in (
            "idaily-today",
            "zhihu-daily",
            "infzm-recommends",
            "xinhua-whxw",
            "rfi-cn",
        ):
            m[t] = 2.0
        m["nmc-weather-daily"] = 2.2
        m["guokr-scientific"] = 1.45
        m["36kr-feed"] = 1.55
        m["bilibili-weekly"] = 0.45
        m["sspai-feed"] = 0.55
    elif bucket == "day":
        for t in (
            "zhihu-daily",
            "bilibili-weekly",
            "sspai-feed",
            "infzm-recommends",
            "guokr-scientific",
            "36kr-feed",
        ):
            m[t] = 2.0
        m["xinhua-whxw"] = 1.55
        m["nmc-weather-daily"] = 1.8
        m["rfi-cn"] = 1.0
        m["idaily-today"] = 0.9
    else:
        m["bilibili-weekly"] = 2.5
        for t in ("zhihu-daily", "infzm-recommends"):
            m[t] = 2.5
        m["sspai-feed"] = 1.0
        m["guokr-scientific"] = 1.45
        m["36kr-feed"] = 1.45
        m["xinhua-whxw"] = 1.1
        m["nmc-weather-daily"] = 1.15
        for t in ("idaily-today", "rfi-cn"):
            m[t] = 0.65
    return m


def _is_holiday_like(d: date) -> bool:
    if d.weekday() >= 5:
        return True
    raw = os.getenv("KEEPALIVE_BRIEF_EXTRA_HOLIDAYS", "").strip()
    if raw:
        for part in raw.split(","):
            p = part.strip()
            if p == d.isoformat():
                return True
    return False


def _brief_holiday_multipliers(d: date) -> dict[str, float]:
    """周末 / 额外节假日略提高知乎（深度阅读）。"""
    m = {t: 1.0 for t in BRIEF_TAG_KEYS}
    if not _brief_holiday_boost_enabled() or not _is_holiday_like(d):
        return m
    for t in ("zhihu-daily", "infzm-recommends", "guokr-scientific"):
        m[t] *= 1.35
    for t in ("sspai-feed", "36kr-feed"):
        m[t] *= 1.12
    m["nmc-weather-daily"] *= 0.95
    return m


def _brief_rotation_multipliers(bucket: str) -> dict[str, float]:
    """与 `pick_rotating_theme` 结合：早/晚强制新闻或热搜；其余时段按 4h 槽轮换。"""
    m = {t: 1.0 for t in BRIEF_TAG_KEYS}
    if not _brief_rotation_enabled():
        return m
    if bucket == "morning":
        for t in (
            "idaily-today",
            "zhihu-daily",
            "infzm-recommends",
            "xinhua-whxw",
            "rfi-cn",
            "36kr-feed",
        ):
            m[t] *= 1.42
        m["bilibili-weekly"] *= 0.58
    elif bucket == "evening":
        for t in (
            "bilibili-weekly",
            "zhihu-daily",
            "sspai-feed",
            "infzm-recommends",
            "guokr-scientific",
            "36kr-feed",
        ):
            m[t] *= 1.42
        for t in ("idaily-today", "rfi-cn"):
            m[t] *= 0.78
    else:
        slot = pick_rotating_theme()
        if slot == 1:
            for t in (
                "idaily-today",
                "zhihu-daily",
                "infzm-recommends",
                "xinhua-whxw",
                "36kr-feed",
                "nmc-weather-daily",
            ):
                m[t] *= 1.38
        elif slot == 2:
            for t in ("idaily-today", "rfi-cn"):
                m[t] *= 1.32
            m["nmc-weather-daily"] *= 1.18
        elif slot == 3:
            for t in ("sspai-feed", "zhihu-daily", "infzm-recommends", "guokr-scientific", "36kr-feed"):
                m[t] *= 1.38
            m["nmc-weather-daily"] *= 0.92
        else:
            for t in ("bilibili-weekly", "idaily-today", "36kr-feed"):
                m[t] *= 1.38
            m["nmc-weather-daily"] *= 1.12
    return m


def _brief_merge_mult(*parts: dict[str, float]) -> dict[str, float]:
    out = {t: 1.0 for t in BRIEF_TAG_KEYS}
    for p in parts:
        for t in BRIEF_TAG_KEYS:
            out[t] *= p.get(t, 1.0)
    return out


def _hot_fallback_step_order(
    steps: list[tuple[str, str, Callable[[], str]]],
    time_bucket: str,
    rng: Any,
) -> list[tuple[str, str, Callable[[], str]]]:
    """兜底链路与 `_brief_time_bucket` 对齐：晚间偏 B 站/虎嗅，凌晨/早晨偏国际视野/虎嗅等。"""
    prefer: tuple[str, ...]
    if time_bucket == "evening":
        prefer = (
            "bilibili-weekly",
            "infzm-recommends",
            "guokr-scientific",
            "36kr-feed",
            "huxiu-rss",
        )
    elif time_bucket == "night":
        prefer = ("idaily-today", "rfi-cn", "huxiu-rss")
    elif time_bucket == "morning":
        prefer = (
            "xinhua-whxw",
            "infzm-recommends",
            "rfi-cn",
            "36kr-feed",
            "huxiu-rss",
        )
    elif time_bucket == "day":
        prefer = (
            "bilibili-weekly",
            "zhihu-daily",
            "xinhua-whxw",
            "infzm-recommends",
            "36kr-feed",
            "huxiu-rss",
        )
    else:
        order = list(steps)
        rng.shuffle(order)
        return order
    pref = [s for s in steps if s[0] in prefer]
    rest = [s for s in steps if s[0] not in prefer]
    rng.shuffle(pref)
    rng.shuffle(rest)
    return pref + rest


def _hot_fallback_max_rounds() -> int:
    raw = (os.getenv("KEEPALIVE_BRIEF_HOT_FALLBACK_ROUNDS") or "4").strip()
    try:
        n = int(raw)
    except ValueError:
        n = 4
    return max(1, min(32, n))


def run_theme_hot_fallback(
    with_links: bool,
    used: set[str],
    rng: Any,
    time_bucket: str = "",
    weather_city: str = "",
) -> tuple[str, str]:
    """热点兜底：多轮随机打乱顺序重试；跳过当日已用过的源；均失败再无视跳过重试。

    若成功返回正文，第二项为用于去重的源标签（如 bilibili-weekly）；失败时第二项为空。"""
    steps: list[tuple[str, str, Callable[[], str]]] = [
        (
            "bilibili-weekly",
            "📺 B站每周必看（RSSHub）\n",
            lambda: fetch_rsshub_route("bilibili/weekly", 8, with_links=with_links),
        ),
        (
            "infzm-recommends",
            "📰 南方周末推荐\n",
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/infzm/recommends", 8, with_links=with_links
            ),
        ),
        (
            "xinhua-whxw",
            "📰 新华社（新华网）\n",
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/newscn/whxw", 8, with_links=with_links
            ),
        ),
        (
            "rfi-cn",
            "📰 法广中文网\n",
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/rfi/cn", 8, with_links=with_links
            ),
        ),
        (
            "guokr-scientific",
            "🧪 果壳科学人\n",
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/guokr/scientific", 8, with_links=with_links
            ),
        ),
        (
            "36kr-feed",
            "📰 36氪\n",
            lambda: fetch_rss_titles("https://36kr.com/feed", 8, with_links=with_links),
        ),
        (
            "huxiu-rss",
            "🔥 24 小时热点\n",
            lambda: fetch_rss_titles("https://rss.huxiu.com/", 8, with_links=with_links),
        ),
    ]
    max_rounds = _hot_fallback_max_rounds()
    for _ in range(max_rounds):
        order = _hot_fallback_step_order(steps, time_bucket, rng)
        for tag, prefix, fn in order:
            if tag in used:
                continue
            body = fn()
            if body and body.strip():
                return prefix + body, tag
        for tag, prefix, fn in order:
            body = fn()
            if body and body.strip():
                return prefix + body, tag
    return "🔥 热搜源抓取不完整，建议手动看榜单。", ""


def pick_time_preferred_theme() -> tuple[int, str]:
    """按时段选择更偏好的主题编号（供 `run_theme` 演示链预留）。

    简报主逻辑已用 `_brief_rotation_multipliers` + `pick_rotating_theme()`，勿与本函数混用。"""
    hour = datetime.now().hour
    # 早上 07:00-08:59：更偏国内/国际新闻
    if 7 <= hour <= 8:
        return (1 if datetime.now().minute < 30 else 2), "morning-focus"
    # 晚间 20:00-22:59：更偏热搜热榜
    if 20 <= hour <= 22:
        return 4, "evening-hot"
    # 其余时段：提高热搜/热榜出现频率
    minute = datetime.now().minute
    if minute < 30:
        return 4, "hots-first"
    if minute < 45:
        return 3, "hots-first"
    return pick_rotating_theme(), "rotate"


def run_theme(theme: int, with_links: bool = False) -> str:
    if theme == 1:
        # 综合资讯：知乎 → 新华社 → 南周 → 环球 → 法广 → 果壳 → 少数派 → 36氪 → 虎嗅
        zh = fetch_rss_titles("https://plink.anyfeeder.com/zhihu/daily", 5, with_links=with_links)
        if zh:
            return f"📰 知乎日报\n{zh}"
        xh = fetch_rss_titles("https://plink.anyfeeder.com/newscn/whxw", 5, with_links=with_links)
        if xh:
            return f"📰 新华社（新华网）\n{xh}"
        nf = fetch_rss_titles("https://plink.anyfeeder.com/infzm/recommends", 5, with_links=with_links)
        if nf:
            return f"📰 南方周末推荐\n{nf}"
        idaily = fetch_rss_titles("https://plink.anyfeeder.com/idaily/today", 5, with_links=with_links)
        if idaily:
            return f"📰 每日环球视野\n{idaily}"
        rfi = fetch_rss_titles("https://plink.anyfeeder.com/rfi/cn", 5, with_links=with_links)
        if rfi:
            return f"📰 法广中文网\n{rfi}"
        gk = fetch_rss_titles("https://plink.anyfeeder.com/guokr/scientific", 5, with_links=with_links)
        if gk:
            return f"🧪 果壳科学人\n{gk}"
        s = fetch_rss_titles("https://sspai.com/feed", 5, with_links=with_links)
        if s:
            return f"🛰️ 科技动态（少数派）\n{s}"
        k36 = fetch_rss_titles("https://36kr.com/feed", 5, with_links=with_links)
        if k36:
            return f"📰 36氪\n{k36}"
        h = fetch_rss_titles("https://rss.huxiu.com/", 5, with_links=with_links)
        return f"🔥 24 小时热点（虎嗅）\n{h}" if h else "📰 新闻源暂时抓取较少。"
    if theme == 2:
        idaily = fetch_rss_titles("https://plink.anyfeeder.com/idaily/today", 5, with_links=with_links)
        if idaily:
            return f"📰 每日环球视野\n{idaily}"
        rfi = fetch_rss_titles("https://plink.anyfeeder.com/rfi/cn", 5, with_links=with_links)
        if rfi:
            return f"📰 法广中文网\n{rfi}"
        zh = fetch_rss_titles("https://plink.anyfeeder.com/zhihu/daily", 5, with_links=with_links)
        if zh:
            return f"📰 知乎日报\n{zh}"
        nf = fetch_rss_titles("https://plink.anyfeeder.com/infzm/recommends", 5, with_links=with_links)
        if nf:
            return f"📰 南方周末推荐\n{nf}"
        r = fetch_rsshub_route("bilibili/weekly", 5, with_links=with_links)
        if r:
            return f"📺 B站每周必看\n{r}"
        s = fetch_rss_titles("https://sspai.com/feed", 5, with_links=with_links)
        if s:
            return f"🛰️ 少数派\n{s}"
        xh = fetch_rss_titles("https://plink.anyfeeder.com/newscn/whxw", 5, with_links=with_links)
        if xh:
            return f"📰 新华社（新华网）\n{xh}"
        gk = fetch_rss_titles("https://plink.anyfeeder.com/guokr/scientific", 5, with_links=with_links)
        if gk:
            return f"🧪 果壳科学人\n{gk}"
        k36 = fetch_rss_titles("https://36kr.com/feed", 5, with_links=with_links)
        if k36:
            return f"📰 36氪\n{k36}"
        return "📰 今天新闻源较少，建议看实时资讯客户端。"
    if theme == 3:
        s = fetch_rss_titles("https://sspai.com/feed", 5, with_links=with_links)
        if s:
            return f"🛰️ 科技动态（少数派）\n{s}"
        h = fetch_rss_titles("https://rss.huxiu.com/", 5, with_links=with_links)
        return f"🛰️ 科技动态（虎嗅）\n{h}" if h else "🛰️ 科技动态暂时抓取较少。"
    raw, _ = run_theme_hot_fallback(
        with_links,
        set(),
        __import__("random").Random(),
        time_bucket="",
        weather_city=(os.getenv("KEEPALIVE_WEATHER_CITY", "") or "北京"),
    )
    return raw


def _brief_take_lines(raw: str, max_n: int = 5) -> Optional[list[str]]:
    if not raw or not raw.strip():
        return None
    lines = [re.sub(r"^\d+\.\s*", "", x.strip()) for x in raw.splitlines() if x.strip()]
    selected = lines[: min(max_n, len(lines))]
    return selected if selected else None


def build_keepalive_brief(
    with_links: bool = False,
    skill_dir: Optional[Path] = None,
) -> tuple[str, str]:
    """组装 RSS 原始行；成稿规则见 `prompts/rewrite-main.md`。

    选材、权重、环境变量与状态文件与 **SKILL.md**（「RSS 与 RSSHub」「简报素材随机」）对齐；勿在脚本注释重复维护长说明。
    """
    import random

    rng = random.Random()
    resolved_skill_dir = skill_dir if skill_dir is not None else Path(__file__).parent.resolve()
    weather_city = resolve_weather_city(resolved_skill_dir)
    today = datetime.now().strftime("%Y-%m-%d")
    daily_once = _brief_daily_once_enabled()
    used: set[str] = set()
    tag_meta: dict[str, Any] = {}
    if daily_once:
        d, used, tag_meta = _load_brief_state()
        if d != today:
            used = set()

    bucket = _brief_time_bucket()
    merged = _brief_merge_mult(
        _brief_time_weight_multipliers(bucket),
        _brief_rotation_multipliers(bucket),
        _brief_holiday_multipliers(date.today()),
    )
    fin: dict[str, float] = {}
    for t in BRIEF_TAG_KEYS:
        fin[t] = merged[t] * _tag_meta_streak_penalty(tag_meta, t, today)

    # 基准权重之和 + BRIEF_FALLBACK_WEIGHT == 1.0；再乘 fin 后在 eligible 上归一化
    base_weighted: list[tuple[str, float, Callable[[], str]]] = [
        ("bilibili-weekly", 0.10, lambda: fetch_rsshub_route("bilibili/weekly", 5, with_links=with_links)),
        (
            "zhihu-daily",
            0.10,
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/zhihu/daily", 5, with_links=with_links
            ),
        ),
        (
            "infzm-recommends",
            0.10,
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/infzm/recommends", 5, with_links=with_links
            ),
        ),
        (
            "idaily-today",
            0.10,
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/idaily/today", 5, with_links=with_links
            ),
        ),
        (
            "sspai-feed",
            0.10,
            lambda: fetch_rss_titles("https://sspai.com/feed", 5, with_links=with_links),
        ),
        (
            "guokr-scientific",
            0.10,
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/guokr/scientific", 5, with_links=with_links
            ),
        ),
        (
            "rfi-cn",
            0.10,
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/rfi/cn", 5, with_links=with_links
            ),
        ),
        (
            "xinhua-whxw",
            0.10,
            lambda: fetch_rss_titles(
                "https://plink.anyfeeder.com/newscn/whxw", 5, with_links=with_links
            ),
        ),
        (
            "36kr-feed",
            0.10,
            lambda: fetch_rss_titles("https://36kr.com/feed", 5, with_links=with_links),
        ),
    ]
    assert abs(sum(w for _, w, _ in base_weighted) + BRIEF_FALLBACK_WEIGHT - 1.0) < 1e-9
    fetch_by_tag = {t: f for t, w, f in base_weighted}

    def mark_used(tag: str) -> None:
        if daily_once and tag:
            used.add(tag)
            _tag_meta_record_pick(tag_meta, tag, today)
            _save_brief_state(today, used, tag_meta, added_tag=tag)

    def mark_and_return(text: str, tag: str) -> tuple[str, str]:
        mark_used(tag)
        return text, tag

    chaos_p = _brief_chaos_probability()
    if chaos_p > 0 and rng.random() < chaos_p:
        chaos_eligible = [
            t
            for t in BRIEF_TAG_KEYS
            if t != "nmc-weather-daily" and (not daily_once or t not in used)
        ]
        rng.shuffle(chaos_eligible)
        for tag in chaos_eligible:
            if tag not in fetch_by_tag:
                continue
            raw_try = fetch_by_tag[tag]()
            picked = _brief_take_lines(raw_try)
            if picked:
                mark_used(tag)
                return "\n".join(picked), "brief-chaos"

    weighted: list[tuple[str, float, Callable[[], str]]] = [
        (t, w * fin.get(t, 1.0), f) for t, w, f in base_weighted
    ]

    eligible = [(t, w, f) for t, w, f in weighted if w > 0 and (not daily_once or t not in used)]
    w_sum = sum(w for _, w, _ in eligible)
    if eligible and w_sum > 0:
        total = w_sum + BRIEF_FALLBACK_WEIGHT
        r = rng.random() * total
        if r < w_sum:
            acc = 0.0
            first_tag: Optional[str] = None
            first_fetch: Optional[Callable[[], str]] = None
            for tag, w, fetch in eligible:
                acc += w
                if r < acc:
                    first_tag, first_fetch = tag, fetch
                    break
            if first_fetch is not None and first_tag is not None:
                order_try: list[tuple[str, Callable[[], str]]] = [(first_tag, first_fetch)]
                rest = [(t, f) for t, w, f in eligible if t != first_tag]
                rng.shuffle(rest)
                order_try.extend(rest)
                for tag, fetch in order_try:
                    raw_try = fetch()
                    picked = _brief_take_lines(raw_try)
                    if picked:
                        return mark_and_return("\n".join(picked), tag)

    raw, sub_tag = run_theme_hot_fallback(
        with_links,
        used if daily_once else set(),
        rng,
        time_bucket=bucket,
        weather_city=weather_city,
    )
    lines = [re.sub(r"^\d+\.\s*", "", x.strip()) for x in raw.splitlines() if x.strip()]
    # 丢弃源标题行（如“📺 B站每周必看（RSSHub）”），仅保留真实条目
    lines = [
        x
        for x in lines
        if not re.match(r"^[📰🛰️🔥📺🌤️]\s*\S+", x)
        or re.search(r"\[https?://[^\]]+\]|\(https?://[^)]+\)", x)
    ]
    lines = [x for x in lines if not re.search(r"编排说明|优先级|policy|priority", x, re.I)]

    if not lines:
        return "本轮暂无可用条目。", "hots-default"

    rng.shuffle(lines)
    selected = lines[: min(5, len(lines))]

    if len(selected) >= 2:
        mark_used(sub_tag)
        return "\n".join(selected), "hots-multi"
    if selected:
        mark_used(sub_tag)
        return selected[0], "hots-single"
    return "本轮暂无可用条目。", "hots-default"


def _prompt_search_dirs(skill_dir: Path) -> list[Path]:
    out: list[Path] = []
    if skill_dir.is_dir():
        out.append(skill_dir.resolve())
    script_dir = Path(__file__).resolve().parent
    if script_dir not in out:
        out.append(script_dir)
    return out


def load_prompt_file(skill_dir: Path, name: str) -> str:
    for d in _prompt_search_dirs(skill_dir):
        p = d / "prompts" / name
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def fill_prompt_template(template: str, mapping: dict[str, str]) -> str:
    s = template
    for k, v in mapping.items():
        s = s.replace("{{" + k + "}}", v)
    return s


def strip_code_fence(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        t = "\n".join(lines).strip()
    return t


def theme_section_label(locale: str, theme_tag: str) -> str:
    """与 build_keepalive_brief 的 theme_tag 对应，用于有序列表前的「栏目说明」一行（非新闻标题）。"""
    if locale == "en":
        m = {
            "bilibili-weekly": "Bilibili Weekly Picks",
            "zhihu-daily": "Zhihu Daily",
            "infzm-recommends": "Southern Weekly picks",
            "idaily-today": "iDaily world",
            "sspai-feed": "sspai (tech)",
            "guokr-scientific": "Guokr Science",
            "rfi-cn": "RFI Chinese",
            "xinhua-whxw": "Xinhua (news.cn)",
            "36kr-feed": "36Kr",
            "nmc-weather-daily": "NMC daily weather",
            "brief-chaos": "Surprise picks",
            "hots-multi": "Hot picks",
            "hots-single": "Hot picks",
            "hots-default": "Hot picks",
        }
        return m.get(theme_tag, "Hot picks")
    m = {
        "bilibili-weekly": "B站每周必看",
        "zhihu-daily": "知乎日报",
        "infzm-recommends": "南方周末推荐",
        "idaily-today": "每日环球视野",
        "sspai-feed": "少数派",
        "guokr-scientific": "果壳科学人",
        "rfi-cn": "法广中文网",
        "xinhua-whxw": "新华社新闻",
        "36kr-feed": "36氪",
        "nmc-weather-daily": "天气提示",
        "brief-chaos": "随机盲盒",
        "hots-multi": "热点快览",
        "hots-single": "热点快览",
        "hots-default": "热点快览",
    }
    return m.get(theme_tag, "热点快览")


def greeting_with_topic_line(locale: str, greet: str, label: str) -> str:
    """无作息时第二段：问候与栏目说明同一行（zh：…｜ 以下是…；en：… — Below: …）。"""
    if locale == "en":
        return f"{greet} Below: {label}"
    return greet + " 以下是" + label


def parse_greeting_topic_line(locale: str, line: str) -> Optional[Tuple[str, str]]:
    """从第二段解析问候前缀与栏目名；无法识别时返回 None。"""
    s = (line or "").strip()
    if not s:
        return None
    if locale == "en":
        m = re.match(r"^(.+?—)\s*Below:\s*(.+)$", s)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        return None
    m = re.match(r"^(.+?｜)\s*以下是\s*(.+)$", s)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None


def insert_wellness_after_greeting(message: str, hint: str, locale: str) -> str:
    """作息关怀与问候同一行（紧接在「｜」后）；下一行单独为栏目名 + 列表。须能解析「以下是/ Below:」版式。"""
    if not (hint or "").strip():
        return message
    msg = trim_message(message)
    parts = [p for p in re.split(r"\n\n+", msg) if p.strip()]
    if len(parts) < 2:
        return f"{msg}\n\n{hint.strip()}"
    title = parts[0]
    first = parts[1].strip()
    rest = "\n\n".join(parts[2:]) if len(parts) > 2 else ""
    parsed = parse_greeting_topic_line(locale, first)
    if parsed:
        greet_prefix, label = parsed
        new_second = f"{greet_prefix}{hint.strip()}\n\n{label}"
        if rest:
            return f"{title}\n\n{new_second}\n\n{rest}"
        return f"{title}\n\n{new_second}"
    if rest:
        return f"{title}\n\n{first}\n\n{hint.strip()}\n\n{rest}"
    return f"{title}\n\n{first}\n\n{hint.strip()}"


def time_greeting_line(locale: str, hour: int) -> str:
    """与 prompts/rewrite-main.md 中时段问候一致，仅用于 agent 失败时的极简兜底。"""
    if locale == "en":
        if hour <= 5:
            return "Early hours —"
        if hour <= 11:
            return "Morning —"
        if hour <= 17:
            return "Afternoon —"
        return "Evening —"
    if hour <= 5:
        return "凌晨｜"
    if hour <= 11:
        return "早安｜"
    if hour <= 17:
        return "下午好｜"
    return "晚间｜"


def _clickable_title(line: str) -> str:
    """将 `标题 [URL]` 规范为 Markdown 可点击标题 `[标题](URL)`。"""
    s = (line or "").strip()
    if not s:
        return s
    if re.search(r"\[[^\]]+\]\(https?://[^)]+\)", s):
        return s
    m = re.match(r"^(.*?)\s*\[(https?://[^\]]+)\]\s*$", s)
    if m:
        title = (m.group(1) or "").strip()
        url = (m.group(2) or "").strip()
        if title and url:
            title = title.replace("[", r"\[").replace("]", r"\]")
            url = url.replace(")", r"\)")
            return f"[{title}]({url})"
    return s


def _is_weather_item_line(line: str) -> bool:
    s = (line or "").strip().lower()
    if not s:
        return False
    if "nmc.cn/publish/weatherperday" in s:
        return True
    if s.startswith("天气：") or s.startswith("weather:"):
        return True
    return "每日天气提示" in s or "weather daily" in s


def _weather_last_sort_items(items: list[str]) -> list[str]:
    normal = [x for x in items if not _is_weather_item_line(x)]
    weather = [x for x in items if _is_weather_item_line(x)]
    return normal + weather if weather else items


def normalize_clickable_ordered_items(text: str) -> str:
    """将有序列表中的 `标题 [URL]` 规范化为可点击的 `[标题](URL)`。"""
    lines = (text or "").splitlines()
    out: list[str] = []
    for line in lines:
        m = re.match(r"^(\s*\d+\.\s+)(.+?)\s*\[(https?://[^\]]+)\]\s*$", line.strip())
        if m:
            prefix = m.group(1)
            title = m.group(2).strip().replace("[", r"\[").replace("]", r"\]")
            url = m.group(3).strip().replace(")", r"\)")
            out.append(f"{prefix}[{title}]({url})")
        else:
            out.append(line)
    return "\n".join(out)


def move_weather_ordered_items_to_end(text: str) -> str:
    """将有序列表中的天气条目挪到列表末尾，并重排编号。"""
    lines = (text or "").splitlines()
    indexed: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        m = re.match(r"^\s*\d+\.\s+(.+)$", line.strip())
        if m:
            indexed.append((idx, m.group(1).strip()))
    if len(indexed) <= 1:
        return text
    reordered = _weather_last_sort_items([x[1] for x in indexed])
    for n, (idx, _) in enumerate(indexed, 1):
        lines[idx] = f"{n}. {reordered[n - 1]}"
    return "\n".join(lines)


def format_smart_report_fallback(locale: str, hour: int, brief: str, theme_tag: str) -> str:
    """agent 不可用时的固定版式兜底，逻辑以提示词为准，此处仅保证结构一致。"""
    title = REPORT_TITLE_MD
    greet = time_greeting_line(locale, hour)
    label = theme_section_label(locale, theme_tag)
    b = (brief or "").strip()
    if not b:
        b = "No usable items this round." if locale == "en" else "本轮暂无可用条目。"
    parts = [p.strip() for p in b.splitlines() if p.strip()]
    items = _weather_last_sort_items([_clickable_title(p) for p in parts])
    intro = greeting_with_topic_line(locale, greet, label)
    if len(items) > 1:
        body_main = "\n".join(f"{i + 1}. {p}" for i, p in enumerate(items))
    elif len(items) == 1:
        body_main = items[0]
    else:
        body_main = ""
    body = body_main or b
    return f"{title}\n\n{intro}\n\n{body}"


FALLBACK_REWRITE_PROMPT = """你是定时推送编辑。按「保活简报 keepalive」版式只输出最终正文，不要代码围栏。

版式：第一行「**保活简报 keepalive**」；空一行；第二段**单独一行**：zh 为「时段问候｜ 以下是{{THEME_HINT}}」（「以下是」与栏目名之间无空格，与「{{THEME_HINT}}」示例一致）；en 为「时段问候 — Below: {{THEME_HINT}}」。再空一行接有序列表（`1. [标题](URL)`）；**列表中 [标题] 须与素材原标题逐字一致（各类信息源均不得改写）**。若包含天气条目（如天气提示/天气：/Weather:），必须放到列表最后，且天气行应优先采用初始化城市「{{WEATHER_CITY}}」对应信息。作息关怀由脚本插入，**不要**写在正文里。禁止「听说」「刚看到」等口语起句。locale={{LOCALE}}。

风格：{{STYLE_GUIDE}}

素材：
{{BRIEF}}

时间：{{LOCAL_TIME}}（{{HOUR}}:{{MINUTE}}）
"""


def scene_description(locale: str, scene: str, active_minutes: int) -> str:
    if locale == "en":
        return {
            "breakfast": "Breakfast-time reminder",
            "lunch": "Lunchtime reminder",
            "dinner": "Dinner reminder",
            "late-night": f"Late-night reminder (active within ~{active_minutes}m)",
        }.get(scene, "Wellness reminder")
    return {
        "breakfast": "早餐时段提醒",
        "lunch": "午饭时间提醒",
        "dinner": "晚饭时间提醒",
        "late-night": f"凌晨提醒（最近约{active_minutes}分钟仍在活跃）",
    }.get(scene, "作息提醒")


def latest_non_heartbeat_session_active(
    openclaw_home: Path, agent_id: str, window_minutes: int
) -> bool:
    p = openclaw_home / "agents" / agent_id / "sessions" / "sessions.json"
    if not p.is_file():
        return False
    data = read_json(p)
    if not isinstance(data, dict):
        return False
    best = 0
    for _, v in data.items():
        if not isinstance(v, dict):
            continue
        o = v.get("origin", {})
        prov = str(o.get("provider", "")).lower() if isinstance(o, dict) else ""
        lab = str(o.get("label", "")).lower() if isinstance(o, dict) else ""
        if prov == "heartbeat" or lab == "heartbeat":
            continue
        try:
            u = int(v.get("updatedAt") or 0)
        except Exception:
            u = 0
        if u > best:
            best = u
    if best <= 0:
        return False
    now_ms = int(datetime.now().timestamp() * 1000)
    return (now_ms - best) <= window_minutes * 60 * 1000


def appendix_wellness_scene(
    openclaw_home: Path, agent_id: str, active_minutes: int
) -> str:
    mins = datetime.now().hour * 60 + datetime.now().minute
    # 早餐 07:00–08:00
    if 420 <= mins <= 480:
        return "breakfast"
    # 午餐 11:45–13:00
    if 705 <= mins <= 780:
        return "lunch"
    # 晚餐 17:45–19:00
    if 1065 <= mins <= 1140:
        return "dinner"
    # 凌晨提醒 00:00–05:59
    if 0 <= datetime.now().hour <= 5 and latest_non_heartbeat_session_active(
        openclaw_home, agent_id, active_minutes
    ):
        return "late-night"
    return ""


WELLNESS_FALLBACK = {
    "en": {
        "breakfast": "Good morning. Grab a quick breakfast, then keep going.",
        "lunch": "You've been focused for a while. Take a lunch break and reset.",
        "dinner": "Wrap this stretch with a proper dinner, then continue.",
        "late-night": "It's getting late. A short pause now can keep the pace steady.",
    },
    "zh": {
        "breakfast": "早上好，先吃点早餐垫一下，再继续也不迟",
        "lunch": "忙了一阵了，先去吃个午饭，回来更精彩",
        "dinner": "这段先收一收，吃顿晚饭，一会再继续",
        "late-night": "夜深了，晚安，早点休息。",
    },
}


def generate_wellness_hint(
    openclaw_bin: str,
    locale: str,
    scene: str,
    active_minutes: int,
    skill_dir: Path,
    agent_id: str,
) -> str:
    if not scene:
        return ""
    lk = "en" if locale == "en" else "zh"
    fallback = WELLNESS_FALLBACK[lk].get(
        scene, "Take a short break if needed." if lk == "en" else "先休息一会儿，回来再继续。"
    )
    if scene == "late-night" and lk == "zh":
        fallback = (
            f"夜深了：检测到最近一条非 heartbeat 会话在约 {active_minutes} 分钟内活跃，先停几分钟缓一缓，回来再继续。"
        )
    if scene == "late-night" and lk == "en":
        fallback = (
            f"It's late: a non-heartbeat session was active within ~{active_minutes}m. Pause for a few minutes, then continue."
        )

    tpl = load_prompt_file(skill_dir, "wellness.md")
    if not tpl.strip():
        tpl = (
            "写一句提醒，只输出一句。场景：{{SCENE_DESC}}。风格补充：{{EXTRA_STYLE}}。语言与 {{LOCALE}} 一致。"
        )
    extra = os.getenv("KEEPALIVE_WELLNESS_STYLE_GUIDE", "").strip() or "（无）"
    prompt = fill_prompt_template(
        tpl,
        {
            "LOCALE": locale,
            "SCENE_DESC": scene_description(locale, scene, active_minutes),
            "EXTRA_STYLE": extra,
        },
    )

    code, out = run_agent_command(
        openclaw_bin=openclaw_bin,
        agent_id=agent_id,
        prompt=prompt,
        timeout_sec=20,
    )
    if code == 0:
        line = out.strip().splitlines()[0].strip() if out.strip() else ""
        line = strip_code_fence(line)
        if line and not re.search(r"error|failed|usage:|unknown|timeout", line, re.I):
            return trim_message(line)
    return fallback


def read_identity_name(openclaw_home: Path, agent_id: str) -> str:
    """读取 agents/<id>/IDENTITY.md 中的 NAME；可用 KEEPALIVE_AGENT_NAME 覆盖。"""
    o = os.getenv("KEEPALIVE_AGENT_NAME", "").strip()
    if o:
        return o
    p = openclaw_home / "agents" / agent_id / "IDENTITY.md"
    if not p.is_file():
        return ""
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    for line in text.splitlines():
        m = re.match(r"^NAME:\s*(.+)$", line.strip(), re.I)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    in_name = False
    for line in text.splitlines():
        if re.match(r"^#+\s*NAME\s*$", line.strip(), re.I):
            in_name = True
            continue
        if in_name:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                break
            return s.strip("-* ").strip('"').strip("'")
    return ""


def generate_status_footer_line(
    openclaw_bin: str,
    locale: str,
    skill_dir: Path,
    message: str,
    openclaw_home: Path,
    agent_id: str,
) -> str:
    """文末状态彩蛋：openclaw agent 生成一句；失败用短句兜底。"""
    lk = "en" if locale == "en" else "zh"
    fallback = (
        "当前系统运行良好，随叫随到"
        if lk == "zh"
        else "Keepalive pipeline OK — here when you need."
    )
    tpl = load_prompt_file(skill_dir, "status-footer.md")
    if not tpl.strip():
        tpl = (
            "写一句文末状态彩蛋（keepalive 已跑通），只输出一句；称呼用 IDENTITY.md 的 NAME，"
            "已知称呼：{{AGENT_NAME}}。语言与 {{LOCALE}} 一致。风格：{{EXTRA_STYLE}}。可参考：{{MESSAGE_SNIPPET}}"
        )
    snippet = (message or "")[:800]
    if len(message or "") > 800:
        snippet += "\n…"
    extra = os.getenv("KEEPALIVE_STATUS_STYLE_GUIDE", "").strip() or "（无）"
    agent_name = read_identity_name(openclaw_home, agent_id)
    prompt = fill_prompt_template(
        tpl,
        {
            "LOCALE": locale,
            "EXTRA_STYLE": extra,
            "MESSAGE_SNIPPET": snippet or "（无）",
            "AGENT_NAME": agent_name or "（未注入，请仍用 IDENTITY.md 的 NAME）",
        },
    )
    code, out = run_agent_command(
        openclaw_bin=openclaw_bin,
        agent_id=agent_id,
        prompt=prompt,
        timeout_sec=20,
    )
    if code == 0:
        line = out.strip().splitlines()[0].strip() if out.strip() else ""
        line = strip_code_fence(line)
        if line and not re.search(r"error|failed|usage:|unknown|timeout", line, re.I):
            return trim_message(line)
    return fallback


def resolve_status_footer_line(
    openclaw_bin: str,
    locale: str,
    skill_dir: Path,
    message: str,
    openclaw_home: Path,
    agent_id: str,
) -> str:
    """未设置 KEEPALIVE_STATUS_FOOTER 时用 agent；设为非空字符串则作固定文案；0/off 关闭。"""
    raw = os.getenv("KEEPALIVE_STATUS_FOOTER", "").strip()
    if raw.lower() in ("0", "off", "false", "none", "-"):
        return ""
    if raw:
        return raw
    return generate_status_footer_line(
        openclaw_bin, locale, skill_dir, message, openclaw_home, agent_id
    )


def append_status_footer(
    message: str,
    locale: str,
    openclaw_bin: str,
    skill_dir: Path,
    openclaw_home: Path,
    agent_id: str,
) -> str:
    msg = trim_message(message)
    line = resolve_status_footer_line(
        openclaw_bin, locale, skill_dir, msg, openclaw_home, agent_id
    )
    if not line:
        return msg
    return trim_message(msg + "\n\n" + line)


def appendix_wellness_hint(
    locale: str,
    openclaw_bin: str,
    openclaw_home: Path,
    agent_id: str,
    active_minutes: int,
    skill_dir: Path,
) -> str:
    scene = appendix_wellness_scene(openclaw_home, agent_id, active_minutes)
    if scene:
        return generate_wellness_hint(
            openclaw_bin, locale, scene, active_minutes, skill_dir, agent_id
        )
    return ""


def generate_message(
    openclaw_bin: str, locale: str, skill_dir: Path, agent_id: str
) -> tuple[str, str]:
    brief, theme_tag = build_keepalive_brief(with_links=True, skill_dir=skill_dir)
    weather_city = resolve_weather_city(skill_dir)
    if weather_append_enabled():
        weather_line = fetch_nmc_weather_daily(weather_city, 1, with_links=True)
        if weather_line.strip():
            brief = f"{brief}\n{weather_line}"
    now = datetime.now()
    style = os.getenv("KEEPALIVE_STYLE_GUIDE", "").strip() or "（无）"
    tpl = load_prompt_file(skill_dir, "rewrite-main.md")
    if not tpl.strip():
        tpl = FALLBACK_REWRITE_PROMPT
    prompt = fill_prompt_template(
        tpl,
        {
            "LOCALE": locale,
            "BRIEF": brief,
            "HOUR": str(now.hour),
            "MINUTE": str(now.minute),
            "LOCAL_TIME": now.strftime("%Y-%m-%d %H:%M:%S"),
            "STYLE_GUIDE": style,
            "THEME_HINT": theme_section_label(locale, theme_tag),
            "WEATHER_CITY": weather_city,
        },
    )

    code, out = run_agent_command(
        openclaw_bin=openclaw_bin,
        agent_id=agent_id,
        prompt=prompt,
        timeout_sec=45,
    )
    if code == 0 and (out or "").strip():
        text = strip_code_fence(out.strip())
        if text and not re.search(
            r"^(error|failed|usage:)|^unknown|timeout", text, re.I | re.M
        ):
            return _finalize_report_text(text), theme_tag

    return _finalize_report_text(
        format_smart_report_fallback(locale, now.hour, brief, theme_tag)
    ), theme_tag


def _finalize_report_text(text: str) -> str:
    """规范化链接。问候与栏目行间距由 main 在插入作息附录后统一收紧。"""
    t = normalize_clickable_ordered_items(text)
    t = move_weather_ordered_items_to_end(t)
    return trim_message(t)


def parse_paths() -> Tuple[Optional[Path], Path]:
    cfg_path = resolve_openclaw_config()
    if cfg_path:
        return cfg_path, cfg_path.parent
    home = Path(os.getenv("OPENCLAW_HOME", str(Path.home() / ".openclaw")))
    return None, home


LAUNCHD_PLIST_NAME = "com.openclaw.smart-keepalive.plist"


def merge_plist_env_into_environ(plist_path: Path) -> dict[str, str]:
    """将 launchd plist 中的 EnvironmentVariables 合并进当前环境，用于模拟定时任务环境。"""
    merged: dict[str, str] = dict(os.environ)
    if not plist_path.is_file():
        return merged
    try:
        with plist_path.open("rb") as f:
            pl = plistlib.load(f)
        ev = pl.get("EnvironmentVariables") or {}
        if isinstance(ev, dict):
            for k, v in ev.items():
                if isinstance(k, str) and isinstance(v, str):
                    merged[k] = v
    except Exception:
        pass
    return merged


def run_doctor() -> int:
    cfg_path, openclaw_home = parse_paths()
    skill_dir = Path(os.getenv("SKILL_DIR", str(openclaw_home / "skills" / "smart-keepalive")))
    plist_path = Path.home() / "Library" / "LaunchAgents" / LAUNCHD_PLIST_NAME

    print("=== smart-keepalive --doctor ===\n")
    bad = 0

    if sys.platform == "darwin":
        if plist_path.is_file():
            print(f"✅ launchd 配置存在：{plist_path}")
        else:
            print(
                f"⚠️  未找到 launchd 配置（若使用定时任务可执行 --install-launchd）：\n   {plist_path}"
            )
    else:
        print("ℹ️  非 macOS，跳过 launchd 检查。")

    sim_env = merge_plist_env_into_environ(plist_path) if sys.platform == "darwin" else dict(os.environ)
    plist_pth = ""
    if plist_path.is_file():
        try:
            with plist_path.open("rb") as f:
                pl = plistlib.load(f)
            ev = pl.get("EnvironmentVariables") or {}
            if isinstance(ev, dict):
                plist_pth = str(ev.get("PATH") or "")
        except Exception:
            plist_pth = ""

    if sys.platform == "darwin" and plist_path.is_file():
        if plist_pth:
            print("✅ launchd plist 已设置 PATH")
            low = plist_pth.lower()
            if ".nvm" in plist_pth or "homebrew" in low or ".local" in plist_pth:
                print("✅ PATH 中含 nvm / homebrew / .local 等常见片段")
            elif "/usr/bin" in plist_pth or "/bin:" in plist_pth:
                print("⚠️  PATH 偏短；若定时任务找不到 node，请在已加载 nvm 的终端中重新执行 --install-launchd")
        else:
            print("⚠️  plist 中未设置 PATH；请重新执行 --install-launchd")
            bad += 1
    elif sys.platform != "darwin":
        print("ℹ️  使用当前 shell 环境检查 PATH（cron 请确认 crontab 中的 PATH）。")

    node_line = ""
    try:
        nr = subprocess.run(
            ["node", "-v"],
            capture_output=True,
            text=True,
            timeout=3,
            env=sim_env,
        )
        if nr.returncode == 0:
            node_line = (nr.stdout or "").strip()
    except Exception:
        node_line = ""
    if node_line:
        print(f"✅ node 在模拟环境（launchd PATH）下可用：{node_line}")
    else:
        print("❌ node 在模拟环境下不可用；请设置 PATH 或重新 --install-launchd（在已 nvm use 的终端中）")
        bad += 1

    oc_sim = resolve_openclaw_bin(sim_env)
    if oc_sim:
        print(f"✅ CLI 可执行文件：{oc_sim}")
    else:
        if has_custom_agent_command(sim_env) and has_custom_send_command(sim_env):
            print("ℹ️  未解析到 openclaw/hermes，但已配置 KEEPALIVE_AGENT_COMMAND + KEEPALIVE_SEND_COMMAND")
        else:
            print("❌ 无法在模拟环境下解析 openclaw/hermes；请设置 KEEPALIVE_CLI_BIN 或修正 PATH")
            bad += 1

    if not cfg_path:
        print("\n⚠️  未找到 openclaw.json（设置 OPENCLAW_CONFIG 或 ~/.openclaw/openclaw.json）")
        print("   若使用 Hermes 或自定义发送命令，可忽略此项。")
        cfg = {}
    else:
        cfg = read_json(cfg_path)

    channel, target = resolve_effective_channel_target(cfg, skill_dir)
    print(f"\n📋 渠道（解析结果）：{channel or '(CLI 默认路由)'}")
    print(f"📋 target：{target or '(未设置)'}")
    rb = rsshub_bases()
    print(f"📡 RSSHub base（{len(rb)} 个，KEEPALIVE_RSSHUB_BASES 可覆盖）：")
    for b in rb:
        print(f"   - {b}")

    if cfg_path:
        ok_ch, msg_ch = validate_channel(cfg, channel)
        if ok_ch:
            print("✅ 渠道在 openclaw.json 中存在且已启用")
        else:
            print(f"❌ {msg_ch}")
            bad += 1
    elif channel:
        print("ℹ️  当前 channel 来自环境变量/local config（未校验 openclaw.json）")

    if oc_sim:
        if channel:
            print("✅ 当前配置将使用指定 channel 发送")
        else:
            print("ℹ️  将使用默认路由（无 --channel）")

    if (target or "").strip():
        print("✅ target 已配置（是否送达以渠道与权限为准，建议试发一条验证）")
    else:
        print("ℹ️  未固定 target：将由 CLI 自动路由到当前会话")

    print("")
    if bad == 0:
        print("结论：检查通过。")
        return 0
    print(f"结论：有 {bad} 项需处理（见上文 ❌ / ⚠️）。")
    return 1


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(
            "用法: python3 smart-keepalive.py [--setup] [--install-launchd] [--install-cron] [--doctor]"
        )
        return 0

    cfg_path, openclaw_home = parse_paths()
    skill_dir = Path(os.getenv("SKILL_DIR", str(openclaw_home / "skills" / "smart-keepalive")))

    if "--doctor" in sys.argv:
        return run_doctor()

    if "--setup" in sys.argv:
        if not cfg_path:
            eprint("ERROR: openclaw.json not found，无法读取可用渠道。")
            eprint("请先设置 OPENCLAW_CONFIG 或确保 ~/.openclaw/openclaw.json 存在。")
            return 2
        return interactive_setup(skill_dir, read_json(cfg_path))

    if "--install-launchd" in sys.argv:
        return print_scheduler_prompt(openclaw_home, skill_dir, "launchd")
    if "--install-cron" in sys.argv:
        return print_scheduler_prompt(openclaw_home, skill_dir, "cron")

    os.environ["OPENCLAW_HOME"] = str(openclaw_home)
    if cfg_path:
        os.environ["OPENCLAW_CONFIG"] = str(cfg_path)
    os.environ.setdefault("SKILL_DIR", str(skill_dir))

    log_file = Path(os.getenv("LOG_FILE", str(openclaw_home / "logs" / "smart-keepalive.log")))
    log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(msg: str, err: bool = False) -> None:
        with log_file.open("a", encoding="utf-8") as f:
            f.write(msg + "\n")
        if err:
            eprint(msg)

    openclaw_bin = resolve_openclaw_bin() or ""
    if not openclaw_bin and (not has_custom_agent_command() or not has_custom_send_command()):
        log(
            "ERROR: CLI binary not found. Set KEEPALIVE_CLI_BIN (or OPENCLAW_BIN) "
            "or configure both KEEPALIVE_AGENT_COMMAND and KEEPALIVE_SEND_COMMAND.",
            True,
        )
        return 127

    cfg = read_json(cfg_path) if cfg_path else {}
    channel, target = resolve_effective_channel_target(cfg, skill_dir)

    ok, reason = validate_channel(cfg, channel) if cfg_path else (True, "")
    if not ok and not has_custom_send_command():
        log(f"❌ 发送失败：channel '{channel}' 不可用", True)
        log("可能原因：", True)
        log("1) openclaw.json 中没有该 channel", True)
        log("2) 该 channel 被禁用（enabled: false）", True)
        log("3) CLI 版本较旧，不支持该 channel", True)
        log("修复建议：", True)
        log('1) 检查 ~/.openclaw/openclaw.json 的 "channels" 配置', True)
        log(f'2) 确保 "{channel}" 的 enabled 为 true', True)
        log("3) 或取消 KEEPALIVE_CHANNEL，让 CLI 自动路由", True)
        log(reason, True)
        return 4
    if cfg_path is None:
        log("ℹ️  未找到 openclaw.json：将仅使用环境变量/local config 解析 channel/target")
    if not target:
        log("ℹ️  未指定 target，将发送到当前会话", True)

    locale = load_locale(skill_dir)
    agent_id = os.getenv("KEEPALIVE_AGENT_ID", "main").strip() or "main"
    message, theme_tag = generate_message(openclaw_bin, locale, skill_dir, agent_id)

    rest_enable = os.getenv("KEEPALIVE_REST_REMINDER", "1").strip() != "0"
    try:
        active_minutes = int(os.getenv("KEEPALIVE_SESSION_ACTIVE_MINUTES", "90"))
    except ValueError:
        active_minutes = 90
    if active_minutes <= 0:
        active_minutes = 90

    hint = ""
    if rest_enable:
        hint = appendix_wellness_hint(
            locale, openclaw_bin, openclaw_home, agent_id, active_minutes, skill_dir
        )
    if hint:
        message = insert_wellness_after_greeting(message, hint, locale)
    message = append_status_footer(
        trim_message(message), locale, openclaw_bin, skill_dir, openclaw_home, agent_id
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"=== Keepalive {now} locale={locale} body={theme_tag} ===")
    log(message)
    log("---")

    # 发送消息时临时清除可能影响 openclaw CLI 的环境变量
    saved_env = {}
    for key in ["SKILL_DIR", "OPENCLAW_HOME", "OPENCLAW_CONFIG"]:
        if key in os.environ:
            saved_env[key] = os.environ.pop(key)
    
    code, out = run_send_command(
        openclaw_bin=openclaw_bin,
        message=message,
        channel=channel,
        target=target,
        cwd=openclaw_home,
        timeout_sec=35,
    )
    
    # 恢复环境变量
    for key, value in saved_env.items():
        os.environ[key] = value
    
    if out.strip():
        log(out.rstrip())
    if code == 0:
        log(f"发送成功 channel={channel}")
        return 0

    log(f"发送失败 channel={channel} code={code}", True)
    if "Unknown channel" in out and not has_custom_send_command():
        log(
            "提示：Unknown channel 可能是 CLI 帮助未列出该 channel（但实际支持）。将重试发送。",
            True,
        )
        # 重试时也清除环境变量
        saved_env2 = {}
        for key in ["SKILL_DIR", "OPENCLAW_HOME", "OPENCLAW_CONFIG"]:
            if key in os.environ:
                saved_env2[key] = os.environ.pop(key)
        
        rcode, rout = run_send_command(
            openclaw_bin=openclaw_bin,
            message=message,
            channel=channel,
            target=target,
            cwd=openclaw_home,
            timeout_sec=35,
        )
        
        # 恢复环境变量
        for key, value in saved_env2.items():
            os.environ[key] = value
        
        if rout.strip():
            log(rout.rstrip())
        if rcode == 0:
            log("重试成功")
            return 0
        log(f"重试也失败 code={rcode}", True)
        return rcode
    return code


if __name__ == "__main__":
    sys.exit(main())
