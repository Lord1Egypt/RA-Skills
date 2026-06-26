#!/usr/bin/env python3
"""自选股半小时跟踪 - 新浪财经API + curl(GBK) + openclaw发送

读取 WATCHLIST.md 获取自选股列表（多用户独立）
"""
import subprocess, json, sys, re, os
from datetime import datetime

USER_ID = "o9cq807VF8Kc62teNYUbuEkvEPGk@im.wechat"
LOG_FILE = "/tmp/stock_push.log"
REPORT_FILE = "/tmp/stock_report_msg.txt"
WATCHLIST_FILE = os.environ.get(
    "STOCK_WATCHLIST",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "WATCHLIST.md")
)
# 常见 workspace 路径备选
WORKSPACE_CANDIDATES = [
    os.path.join(os.path.expanduser("~/.qclaw/workspace-stock"), "WATCHLIST.md"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "WATCHLIST.md"),
]

def resolve_watchlist():
    """解析 WATCHLIST.md 路径"""
    if os.path.exists(WATCHLIST_FILE):
        return WATCHLIST_FILE
    for p in WORKSPACE_CANDIDATES:
        if os.path.exists(p):
            return p
    return WATCHLIST_FILE

INDICES = [
    ("sh", "000001", "上证指数"),
    ("sz", "399001", "深证成指"),
    ("sz", "399006", "创业板指"),
    ("sh", "000688", "科创50"),
]

def load_watchlist():
    """从 WATCHLIST.md 读取自选股列表（跳过注释和示例）"""
    watch_list = []
    wl_path = resolve_watchlist()
    
    if not os.path.exists(wl_path):
        print(f"[ERROR] WATCHLIST.md 不存在: {wl_path}")
        return watch_list
    
    with open(wl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 匹配格式: sh688158 或 sz300131 或 sh 688158 或 sz 300131
    import re
    pattern = r"^(sh|sz)(\d{6})"
    seen = set()
    
    for line in lines:
        line = line.strip()
        # 跳过空行、注释、示例行
        if not line or line.startswith('#') or line.startswith('>') or line.startswith('<!--'):
            continue
        
        match = re.match(pattern, line)
        if match:
            prefix, code = match.groups()
            key = f"{prefix}{code}"
            if key not in seen:
                seen.add(key)
                # 尝试提取股票名称（同一行后面的中文）
                name_pattern = rf"^{prefix}{code}\s+([\u4e00-\u9fa5a-zA-Z0-9·\-]+)"
                name_match = re.match(name_pattern, line)
                name = name_match.group(1) if name_match else code
                watch_list.append((prefix, code, name))
    
    return watch_list

INDICES = [
    ("sh", "000001", "上证指数"),
    ("sz", "399001", "深证成指"),
    ("sz", "399006", "创业板指"),
    ("sh", "000688", "科创50"),
]


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def sina_fetch(codes_list):
    """批量获取新浪行情，bytes模式避免编码问题"""
    symbols = ",".join(codes_list)
    url = f"https://hq.sinajs.cn/list={symbols}"
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "15",
             "-H", "Referer: https://finance.sina.com.cn", url],
            capture_output=True, timeout=20  # bytes模式
        )
        if r.returncode != 0 or not r.stdout:
            log(f"sina_fetch curl failed: rc={r.returncode}")
            return {}
        # GBK→UTF-8
        raw = r.stdout.decode("gbk", errors="replace")
        # 解析
        result = {}
        for line in raw.strip().split("\n"):
            m = re.match(r'var hq_str_(\w+)="(.*)";', line)
            if m:
                code = m.group(1)
                fields = m.group(2).split(",")
                result[code] = fields
        return result
    except Exception as e:
        log(f"sina_fetch error: {e}")
        return {}


def parse_stock(fields):
    """新浪字段: 0=名称,2=昨收,3=当前价,8=成交量(股)"""
    if len(fields) < 9:
        return None
    try:
        name = fields[0]
        yclose = float(fields[2])
        price = float(fields[3])
        vol = int(float(fields[8]))
        if price <= 0 or yclose <= 0:
            return {"name": name, "price": price, "yclose": yclose, "vol": vol, "pct": 0, "valid": False}
        pct = (price - yclose) / yclose * 100
        return {"name": name, "price": price, "yclose": yclose, "vol": vol, "pct": pct, "valid": True}
    except (ValueError, IndexError):
        return None


def send_via_openclaw(text, retries=3):
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(
                ["openclaw", "message", "send",
                 "--channel", "openclaw-weixin",
                 "--target", USER_ID,
                 "--message", text],
                capture_output=True, text=True, timeout=25,
            )
            if result.returncode == 0:
                if attempt > 1:
                    log(f"发送成功（第{attempt}次尝试）")
                return True
            else:
                log(f"发送失败（第{attempt}次）: {result.stderr[:100]}")
        except Exception as e:
            log(f"发送异常（第{attempt}次）: {e}")
        if attempt < retries:
            import time; time.sleep(3)
    return False


# ── 主程序 ──────────────────────────────────────────────
now = datetime.now()
log(f"=== 自选股半小时跟踪启动 ({now}) ===")

if now.weekday() >= 5:
    log("非交易日，跳过")
    sys.exit(0)

# 动态加载自选股
WATCH_LIST = load_watchlist()
if not WATCH_LIST:
    log("WATCHLIST.md 无有效股票，请先配置自选股")
    sys.exit(1)

log(f"加载 {len(WATCH_LIST)} 只自选股")

all_codes = [f"{prefix}{code}" for prefix, code, name in INDICES + WATCH_LIST]
log(f"请求{len(all_codes)}只行情...")
raw = sina_fetch(all_codes)
log(f"获取{len(raw)}条数据")

indices = []
for prefix, code, name in INDICES:
    key = f"{prefix}{code}"
    if key in raw:
        d = parse_stock(raw[key])
        if d:
            d["code"] = code
            d["label"] = name
            indices.append(d)
            continue
    indices.append({"label": name, "price": 0, "yclose": 0, "pct": 0, "valid": False})

watch = []
for prefix, code, name in WATCH_LIST:
    key = f"{prefix}{code}"
    if key in raw:
        d = parse_stock(raw[key])
        if d:
            d["code"] = code
            watch.append(d)
            continue
    watch.append({"name": name, "code": code, "price": 0, "yclose": 0, "vol": 0, "pct": 0, "valid": False})

valid_indices = [d for d in indices if d.get("valid")]
valid_watch = [d for d in watch if d.get("valid")]
log(f"指数有效: {len(valid_indices)}/{len(INDICES)}  自选有效: {len(valid_watch)}/{len(WATCH_LIST)}")

if not valid_indices and not valid_watch:
    log("无有效数据，跳过发送")
    sys.exit(1)

valid_sorted = sorted(valid_watch, key=lambda x: x["pct"], reverse=True)

lines = [f"📊 自选股跟踪 · {now.strftime('%H:%M')}", ""]

lines.append("【大盘】")
for d in indices:
    if not d.get("valid"):
        lines.append(f"⚪ {d['label']}：数据异常")
        continue
    pct = d["pct"]
    sign = "+" if pct >= 0 else ""
    emoji = "🔴" if pct > 0 else ("🟢" if pct < 0 else "⚪")
    lines.append(f"{emoji} {d['label']} {d['price']:.2f} {sign}{pct:.2f}%")

lines.append("")
lines.append("【自选股·涨跌排序】")
up = [s for s in valid_sorted if s["pct"] > 0]
dn = [s for s in valid_sorted if s["pct"] < 0]
flat = [s for s in valid_sorted if s["pct"] == 0]

if up:
    lines.append("🟢 涨幅:")
    for s in up:
        chg = s["price"] - s["yclose"]
        chg_sign = "+" if chg >= 0 else ""
        lines.append(f"  🔴 {s['name']} {s['price']:.2f} +{s['pct']:.2f}%({chg_sign}{chg:.2f})")
if dn:
    lines.append("📉 跌幅:")
    for s in dn:
        chg = s["price"] - s["yclose"]
        lines.append(f"  🟢 {s['name']} {s['price']:.2f} {s['pct']:.2f}%({chg:.2f})")
if flat:
    lines.append("⚪ 平盘:")
    for s in flat:
        lines.append(f"  ⚪ {s['name']} {s['price']:.2f}")

invalid = [s for s in watch if not s.get("valid")]
if invalid:
    lines.append("")
    lines.append(f"⚠️ 数据异常({len(invalid)}只): " + ", ".join(s["name"] for s in invalid))

text = "\n".join(lines)

try:
    with open(REPORT_FILE, "w") as f:
        f.write(text)
except Exception:
    pass

ok = send_via_openclaw(text)
log(f"{'✅' if ok else '⚠️'} 推送{'成功' if ok else '失败'}")
sys.exit(0 if ok else 1)
