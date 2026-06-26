#!/usr/bin/env python3
"""次日关注 - 持仓止损位 + 操作建议"""
import subprocess, json, urllib.request, sys, time
from datetime import datetime

# TODO: 替换为你的微信用户 ID
USER_ID = "o9cq807VF8Kc62teNYUbuEkvEPGk@im.wechat"
EM_HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://quote.eastmoney.com/"}
LOG_FILE = "/tmp/stock_next.log"

HOLDINGS = [
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

def fetch_stocks():
    """
    获取持仓股行情（异常隔离 + 数据有效性校验）
    """
    result = []
    for secid, code, name in HOLDINGS:
        try:
            url = (f"https://push2.eastmoney.com/api/qt/stock/get"
                   f"?secid={secid}&fields=f43,f44,f57,f58,f60"
                   f"&ut=bd1d9ddb04089700cf9c27f4f4961f5b&fltt=2&invt=2")
            req = urllib.request.Request(url, headers=EM_HEADERS)
            with urllib.request.urlopen(req, timeout=10) as r:
                d = json.loads(r.read()).get("data", {})
            yclose_raw = d.get("f44")
            if yclose_raw == "-" or yclose_raw is None:
                yclose = float(d.get("f60", 0))
            else:
                yclose = float(yclose_raw)
            price  = float(d.get("f43", 0))
            if price <= 0 or yclose <= 0:
                log(f"  {name}: 数据无效 price={price} yclose={yclose}")
                result.append({"code": code, "name": name,
                               "price": 0, "yclose": 0, "pct": 0,
                               "valid": False})
                continue
            pct = (price - yclose) / yclose * 100
            result.append({
                "code": code,
                "name": d.get("f58", name),
                "price": price,
                "yclose": yclose,
                "pct": pct,
                "valid": True,
            })
        except Exception as e:
            log(f"  {name} fetch error: {e}")
            result.append({"code": code, "name": name,
                           "price": 0, "yclose": 0, "pct": 0,
                           "valid": False})
    return result

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
            time.sleep(3)
    return False

# ── 主程序 ──────────────────────────────────────────────
now = datetime.now()
log(f"=== 次日关注启动 ({now}) ===")

if now.weekday() >= 5:
    log("非交易日，跳过")
    sys.exit(0)

stocks = fetch_stocks()
valid  = [s for s in stocks if s.get("valid")]

log(f"有效数据: {len(valid)}/{len(HOLDINGS)}")

if not valid:
    log("⚠️ 无有效数据，跳过发送")
    sys.exit(1)

lines = [f"📋 次日关注 · {now.strftime('%Y-%m-%d %H:%M')}", ""]
lines.append("【持仓概况】")

for s in stocks:
    if not s.get("valid"):
        lines.append(f"⚠️ {s['name']}（{s['code']}）数据获取异常")
        continue
    pct = s["pct"]
    sign = "+" if pct >= 0 else ""
    emoji = "🔴" if pct > 0 else ("🟢" if pct < 0 else "⚪")
    lines.append(
        f"{emoji} {s['name']}（{s['code']}）"
        f"收盘:{s['price']:.3f} 今日:{sign}{pct:.2f}%"
    )

lines.extend([
    "",
    "【明日建议】",
    "• 止损纪律：单票亏损超 -7% 无条件止损",
    "• 仓位管理：持仓不超过总仓位 50%",
    "• 明日竞价关注：涨幅 >3% 不追，跌幅 <0 观望",
])

lines.extend(["", "_20:00 自动推送_"])
text = "\n".join(lines)
ok = send_via_openclaw(text)
log(f"{'✅' if ok else '⚠️'} 次日关注推送 {'成功' if ok else '失败'}")
sys.exit(0 if ok else 1)
