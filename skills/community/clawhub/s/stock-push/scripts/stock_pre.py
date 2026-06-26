#!/usr/bin/env python3
"""盘前推荐 - 东方财富API + openclaw 发送"""
import subprocess, json, urllib.request, sys
from datetime import datetime

# TODO: 替换为你的微信用户 ID（格式：xxxxxxxxxx@im.wechat）
USER_ID = "o9cq807VF8Kc62teNYUbuEkvEPGk@im.wechat"
EM_HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://quote.eastmoney.com/"}
LOG_FILE = "/tmp/stock_pre.log"

WATCH_LIST = [
    ("1.600490", "600490", "鹏欣资源"),
    ("0.300269", "300269", "联建光电"),
    ("0.002138", "002138", "顺络电子"),
    ("0.300444", "300444", "双杰电气"),
]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def send_via_openclaw(text, retries=3):
    """发送消息，带重试机制"""
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
                    log(f"✅ 发送成功（第{attempt}次尝试）")
                return True
            else:
                log(f"⚠️ 发送失败（第{attempt}次）: {result.stderr[:100]}")
        except Exception as e:
            log(f"⚠️ 发送异常（第{attempt}次）: {e}")
        if attempt < retries:
            import time; time.sleep(3)
    return False

def fetch_indices():
    """
    获取大盘指数（异常隔离 + 数据有效性校验）
    """
    indices = [
        ("1.000001", "上证指数"),
        ("0.399001", "深证成指"),
        ("0.399006", "创业板指"),
        ("1.000688", "科创50"),
    ]
    result = {}
    for secid, name in indices:
        try:
            url = (f"https://push2.eastmoney.com/api/qt/stock/get"
                   f"?secid={secid}&fields=f43,f44,f57,f58,f60"
                   f"&ut=bd1d9ddb04089700cf9c27f4f4961f5b&fltt=2&invt=2")
            req = urllib.request.Request(url, headers=EM_HEADERS)
            with urllib.request.urlopen(req, timeout=10) as r:
                d = json.loads(r.read()).get("data", {})
            yclose_raw = d.get("f44")
            if yclose_raw == "-" or yclose_raw is None:
                # 竞价阶段 f44 返回 '-'，改用 f60（昨收）
                yclose = float(d.get("f60", 0))
            else:
                yclose = float(yclose_raw)
            price  = float(d.get("f43", 0))
            # price=0 表示非交易时段或API异常
            if price <= 0 or yclose <= 0:
                log(f"  {name}: 数据无效 price={price} yclose={yclose}")
                result[name] = {"level": 0, "pct": 0, "valid": False}
                continue
            pct = (price - yclose) / yclose * 100
            result[name] = {"level": price, "pct": pct, "valid": True}
        except Exception as e:
            log(f"  {name} fetch error: {e}")
            result[name] = {"level": 0, "pct": 0, "valid": False}
    return result

def fetch_watch():
    """
    获取自选股行情（异常隔离 + 数据有效性校验）
    """
    result = []
    for secid, code, name in WATCH_LIST:
        try:
            url = (f"https://push2.eastmoney.com/api/qt/stock/get"
                   f"?secid={secid}&fields=f43,f44,f47,f57,f58,f60"
                   f"&ut=bd1d9ddb04089700cf9c27f4f4961f5b&fltt=2&invt=2")
            req = urllib.request.Request(url, headers=EM_HEADERS)
            with urllib.request.urlopen(req, timeout=10) as r:
                d = json.loads(r.read()).get("data", {})
            price  = float(d.get("f43", 0))
            yclose_raw = d.get("f44")
            if yclose_raw == "-" or yclose_raw is None:
                yclose = float(d.get("f60", 0))
            else:
                yclose = float(yclose_raw)
            vol_raw = d.get("f47")
            vol = int(vol_raw) if vol_raw and vol_raw != "-" else 0
            if price <= 0 or yclose <= 0:
                log(f"  {name}: 数据无效 price={price} yclose={yclose}")
                result.append({"code": code, "name": name,
                               "price": 0, "yclose": 0, "vol": 0, "pct": 0,
                               "valid": False})
                continue
            pct = (price - yclose) / yclose * 100
            result.append({
                "code": code,
                "name": d.get("f58", name),
                "price": price,
                "yclose": yclose,
                "vol": vol,
                "pct": pct,
                "valid": True,
            })
        except Exception as e:
            log(f"  {name} fetch error: {e}")
            result.append({"code": code, "name": name,
                           "price": 0, "yclose": 0, "vol": 0, "pct": 0,
                           "valid": False})
    return result

# ── 主程序 ──────────────────────────────────────────────
now = datetime.now()
log(f"=== 盘前推荐启动 ({now}) ===")

if now.weekday() >= 5:
    log("非交易日，跳过")
    sys.exit(0)

indices = fetch_indices()
watch   = fetch_watch()

valid_indices = [k for k, v in indices.items() if v.get("valid")]
valid_watch   = [s for s in watch if s.get("valid")]

log(f"指数有效: {len(valid_indices)}/4  自选有效: {len(valid_watch)}/{len(WATCH_LIST)}")

# 无有效数据 → 不发送（避免误报）
if not valid_indices and not valid_watch:
    log("⚠️ 无有效数据，跳过发送")
    sys.exit(1)

lines = [f"📈 盘前推荐 · {now.strftime('%Y-%m-%d %H:%M')}", ""]

# 大盘指数
lines.append("【大盘情况】")
for name, d in indices.items():
    if not d.get("valid"):
        lines.append(f"⚪ {name}：数据获取异常")
        continue
    pct = d["pct"]
    sign = "+" if pct >= 0 else ""
    emoji = "🔴" if pct > 0 else ("🟢" if pct < 0 else "⚪")
    lines.append(f"{emoji} {name}：{d['level']:.2f}  {sign}{pct:.2f}%")

# 自选股
lines.append("")
lines.append("【自选股】")
if not valid_watch:
    lines.append("⚠️ 数据获取失败，请检查网络")
else:
    for s in watch:
        if not s.get("valid"):
            lines.append(f"⚠️ {s['name']}（{s['code']}）数据获取异常")
            continue
        pct = s["pct"]
        sign = "+" if pct >= 0 else ""
        emoji = "🔴" if pct > 0 else ("🟢" if pct < 0 else "⚪")
        chg = s["price"] - s["yclose"]
        chg_sign = "+" if chg >= 0 else ""
        lines.append(
            f"{emoji} {s['name']}（{s['code']}）"
            f"现价:{s['price']:.2f} 涨跌:{sign}{pct:.2f}%"
            f"({chg_sign}{chg:.2f}) 成交:{s['vol']//100}手"
        )

lines.extend(["", "_9:20 自动推送_"])
text = "\n".join(lines)
ok = send_via_openclaw(text)
log(f"{'✅' if ok else '⚠️'} 盘前推荐推送 {'成功' if ok else '失败'}")
sys.exit(0 if ok else 1)
