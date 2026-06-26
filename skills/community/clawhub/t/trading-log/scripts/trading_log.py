#!/usr/bin/env python3
"""
交易日志系统 - 龙虾大元帅记录小魔尊的每一笔交易
用法:
  python3 交易日志.py 买入 600519 28.5 1000 看好白酒龙头
  python3 交易日志.py 卖出 600519 30.0 500 止盈
  python3 交易日志.py 持仓    ← 查看当前持仓
  python3 交易日志.py 日志    ← 查看交易记录
  python3 交易日志.py 盈亏    ← 计算当日盈亏
"""
import json
import sys
import os
from datetime import datetime, date

LOG_FILE = "/home/jocob/Desktop/交易日志_持仓记录.json"
PRICE_FILE = "/home/jocob/Desktop/交易日志_最新价.json"

# ========== 持仓记录 ==========
def load_positions():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {
        "positions": {},      # code -> {name, shares, avg_cost, direction, trades:[]}
        "trade_log": [],       # 所有交易记录
        "daily_pnl": {}        # date -> {total_market_value, total_cost, unrealized_pnl}
    }

def save(data):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== 交易记录 ==========
def record_trade(direction, code, price, quantity, reason="", account="", name=""):
    data = load_positions()
    code = code.zfill(6)
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    ts = now.strftime('%Y-%m-%d %H:%M:%S')

    trade = {
        "date": today,
        "time": ts,
        "direction": direction,
        "code": code,
        "name": name,
        "price": float(price),
        "quantity": float(quantity),
        "amount": float(price) * float(quantity),
        "reason": reason,
        "account": account
    }

    # 记录到交易日志
    data["trade_log"].append(trade)

    # 更新持仓
    if code not in data["positions"]:
        data["positions"][code] = {
            "name": name,
            "shares": 0,
            "avg_cost": 0,
            "direction": "none",
            "trades": [],
            "realized_pnl": 0,
            "sell_record": []  # 记录每次卖出用于计算已实现盈亏
        }

    pos = data["positions"][code]
    pos["name"] = name or pos.get("name", code)
    pos["trades"].append(trade)

    if direction == "买入":
        total_cost = pos["shares"] * pos["avg_cost"] + float(price) * float(quantity)
        pos["shares"] += float(quantity)
        pos["avg_cost"] = total_cost / pos["shares"] if pos["shares"] > 0 else 0
        pos["direction"] = "买入"
    elif direction == "卖出":
        # 计算已实现盈亏（用avg_cost）
        pnl = (float(price) - pos["avg_cost"]) * float(quantity)
        pos["realized_pnl"] += pnl
        pos["shares"] -= float(quantity)
        pos["sell_record"].append({"date": today, "price": float(price), "quantity": float(quantity), "pnl": pnl})
        if pos["shares"] <= 0:
            pos["shares"] = 0
            pos["avg_cost"] = 0
            pos["direction"] = "已清仓"
        else:
            pos["direction"] = "买入"

    save(data)
    return trade, data["positions"]

# ========== 持仓视图 ==========
def get_live_prices(codes):
    """用腾讯快接口获取最新价"""
    try:
        import urllib.request, time
        ts_map = {}
        for c in codes:
            c_stripped = c.lstrip('0')
            # 判断是否是港股
            # 规律：
            # - A股6位代码去掉前导0后长度>=6，或以特定前缀开头(002/000/300/601/603/688等)
            # - 港股4-5位代码去掉前导0后，以9开头(9xxx=9xxxx)或明确已知列表
            known_hk = {'2669', '3320', '9896', '9988'}  # 中海物业,华润医药,名创优品,阿里巴巴
            is_hk = False
            if c_stripped in known_hk:
                is_hk = True
            elif len(c_stripped) <= 5 and len(c_stripped) >= 4:
                # 4-5位代码，去掉前导0后，首位是9的为港股；首位是2/3的为深市A股(002xxx/003xxx)
                # 首位是0→可能是00开头→深市A股; 首位是5/1/6→已有明确前缀分支处理
                if c_stripped.startswith('9') and not c_stripped.startswith('59'):
                    is_hk = True
                # 其余4位数字（2xxx, 3xxx, 4xxx等）均为深市A股
                # 已在下面的sz分支处理

            if is_hk:
                # 港股：腾讯代码去掉前导0，如002669→hk02669
                ts_map[f'hk{c_stripped.zfill(5)}'] = c
            elif c.startswith('688'):
                ts_map[f'sh{c}'] = c
            elif c.startswith('6') or c.startswith('5'):
                # 6=沪A, 5=上海ETF
                ts_map[f'sh{c}'] = c
            elif c.startswith('0') or c.startswith('3') or c.startswith('1') or c.startswith('2'):
                # 0/2/3=深A, 1=深圳ETF(159xxx)
                ts_map[f'sz{c}'] = c
            elif c.startswith('8') or c.startswith('4'):
                ts_map[f'bj{c}'] = c
            else:
                ts_map[f'sz{c}'] = c

        result = {}
        keys = list(ts_map.keys())
        for i in range(0, len(keys), 50):
            batch = keys[i:i+50]
            url = f"https://qt.gtimg.cn/q={','.join(batch)}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    content = resp.read().decode('gbk', errors='replace')
                for line in content.strip().split('\n'):
                    if not line.strip(): continue
                    parts = line.split('~')
                    if len(parts) < 4: continue
                    code_raw = parts[0].replace('v_', '')
                    price_str = parts[3]
                    try: price = float(price_str) if price_str not in ['','-','0.00'] else 0
                    except: price = 0
                    # 处理腾讯接口代码格式：sh600096="1 → 提取sh600096
                    if '=' in code_raw:
                        code_part = code_raw.split('=')[0]
                    else:
                        code_part = code_raw
                    if code_part.startswith('sh') or code_part.startswith('sz') or code_part.startswith('bj') or code_part.startswith('hk'):
                        pure = code_part[2:]  # 去掉sh/sz/bj/hk前缀
                        # 精确匹配
                        if pure in set(ts_map.values()):
                            result[pure] = price
                        else:
                            # 去掉前导0后匹配（腾讯可能把009988返回为09988）
                            pure_stripped = pure.lstrip('0')
                            matched = False
                            for orig in set(ts_map.values()):
                                orig_s = orig.lstrip('0')
                                if pure_stripped == orig_s or pure == orig_s or pure_stripped == orig:
                                    result[orig] = price
                                    matched = True
                                    break
                            if not matched:
                                # 用原始6位格式存储
                                result[pure.zfill(6)] = price
                    else:
                        pure = code_part.zfill(6)
                        if pure in set(ts_map.values()):
                            result[pure] = price
            except: pass
            time.sleep(0.05)
        return result
    except:
        return {}

def show_positions(price_map=None, show_pnl=False):
    """price_map: {code: latest_price}，可选
       show_pnl: 是否显示盈亏（需要价格）"""
    data = load_positions()
    active = {k:v for k,v in data["positions"].items() if v["shares"] > 0}
    if not active:
        print("   暂无持仓记录")
        return

    if show_pnl and not price_map:
        codes = list(active.keys())
        print(f"📡 正在获取 {len(codes)} 只股票最新价...")
        price_map = get_live_prices(codes)
        print(f"   已获取 {len(price_map)} 只价格")

    print(f"\n🦞 {'='*70}")
    print(f"   小魔尊持仓记录  ({datetime.now().strftime('%Y-%m-%d %H:%M')}) {'📈' if (sum((price_map.get(c,0)-v['avg_cost'])*v['shares'] for c,v in active.items()) if price_map else 0) >= 0 else '📉'}")
    print(f"{'='*70}")

    print(f"  {'代码':<8} {'名称':<10} {'持仓':>6} {'均价':>8} {'现价':>8} {'市值':>10} {'浮动':>10} {'已实现':>10}")
    print(f"  {'-'*75}")

    total_market = 0; total_cost = 0; total_unrealized = 0; total_realized = 0

    for code, pos in sorted(active.items(), key=lambda x: x[1]["shares"]*x[1]["avg_cost"], reverse=True):
        price = price_map.get(code, pos["avg_cost"]) if price_map else pos["avg_cost"]
        market = pos["shares"] * price
        unrealized = (price - pos["avg_cost"]) * pos["shares"]
        total_market += market
        total_cost += pos["shares"] * pos["avg_cost"]
        total_unrealized += unrealized
        total_realized += pos["realized_pnl"]
        pct = unrealized/pos["shares"]/pos["avg_cost"]*100 if pos["avg_cost"] > 0 else 0
        print(f"  {code:<8} {pos['name']:<10} {pos['shares']:>6.0f} {pos['avg_cost']:>8.3f} {price:>8.3f} {market:>10,.2f} {unrealized:>+9,.0f}({pct:+.1f}%) {pos['realized_pnl']:>+10,.2f}")

    print(f"  {'-'*75}")
    total_pnl = total_unrealized + total_realized
    print(f"  {'合计':<18} {'':<6} {'':<8} {'':<8} {total_market:>10,.2f} {total_unrealized:>+10,.2f} {total_realized:>+10,.2f}  {total_pnl:>+10,.2f}")
    print(f"  💰 总市值: {total_market:,.2f} | 浮动: {total_unrealized:+,.2f} | 已实现: {total_realized:+,.2f} | 合计: {total_pnl:+,.2f}")
    return active

# ========== 交易日志视图 ==========
def show_trade_log(limit=20):
    data = load_positions()
    log = data["trade_log"][-limit:]
    print(f"\n📖 最近{len(log)}条交易记录:")
    print(f"  {'日期':<12} {'时间':<8} {'方向':<4} {'代码':<8} {'名称':<10} {'价格':>8} {'数量':>6} {'金额':>12} 原因")
    print(f"  {'-'*95}")
    for t in log:
        print(f"  {t['date']:<12} {t['time'][11:]:<8} {t['direction']:<4} {t['code']:<8} {t['name']:<10} {t['price']:>8.3f} {t['quantity']:>6.0f} {t['amount']:>12,.2f}  {t.get('reason','')}")

# ========== 更新持仓价格并计算盈亏 ==========
def update_prices_and_calc(price_map):
    """用最新价格更新市值和盈亏"""
    data = load_positions()
    total_market = 0
    total_cost = 0
    total_unrealized = 0
    total_realized = 0

    results = []
    for code, pos in data["positions"].items():
        if pos["shares"] <= 0:
            continue
        price = price_map.get(code, pos["avg_cost"])
        market = pos["shares"] * price
        unrealized = (price - pos["avg_cost"]) * pos["shares"]
        cost = pos["shares"] * pos["avg_cost"]
        total_market += market
        total_cost += cost
        total_unrealized += unrealized
        total_realized += pos["realized_pnl"]
        results.append({
            "code": code, "name": pos["name"], "shares": pos["shares"],
            "avg_cost": pos["avg_cost"], "price": price,
            "market": market, "unrealized": unrealized,
            "realized_pnl": pos["realized_pnl"]
        })

    today = date.today().isoformat()
    data["daily_pnl"][today] = {
        "total_market": round(total_market, 2),
        "total_cost": round(total_cost, 2),
        "unrealized_pnl": round(total_unrealized, 2),
        "realized_pnl": round(total_realized, 2),
        "total_pnl": round(total_unrealized + total_realized, 2)
    }
    save(data)

    return results, total_market, total_unrealized, total_realized

def show_pnl():
    data = load_positions()
    today = date.today().isoformat()

    print(f"\n💹 持仓盈亏报表  ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"  {'='*60}")

    if today in data["daily_pnl"]:
        d = data["daily_pnl"][today]
        print(f"  📌 今日汇总:")
        print(f"     总市值:   {d['total_market']:>12,.2f}")
        print(f"     总成本:   {d['total_cost']:>12,.2f}")
        print(f"     浮动盈亏: {d['unrealized_pnl']:>+12,.2f} ({d['unrealized_pnl']/d['total_cost']*100:+.2f}%)")
        print(f"     已实现:   {d['realized_pnl']:>+12,.2f}")
        print(f"     合计盈亏: {d['total_pnl']:>+12,.2f}")

    # 历史每日汇总
    print(f"\n  📅 历史每日收盘盈亏:")
    print(f"  {'日期':<12} {'市值':>12} {'成本':>12} {'浮动':>12} {'已实现':>10} {'合计':>12}")
    print(f"  {'-'*72}")
    for d_str in sorted(data["daily_pnl"].keys(), reverse=True)[:10]:
        d = data["daily_pnl"][d_str]
        print(f"  {d_str:<12} {d['total_market']:>12,.2f} {d['total_cost']:>12,.2f} {d['unrealized_pnl']:>+12,.2f} {d['realized_pnl']:>+10,.2f} {d['total_pnl']:>+12,.2f}")

# ========== 命令行解析 ==========
if __name__ == '__main__':
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == '买入':
        # 格式: 买入 代码 价格 数量 [原因] [账户]
        code = args[1].zfill(6) if len(args) > 1 else ''
        price = float(args[2]) if len(args) > 2 else 0
        quantity = float(args[3]) if len(args) > 3 else 0
        reason = args[4] if len(args) > 4 else ''
        account = args[5] if len(args) > 5 else ''
        if not code or not price or not quantity:
            print("❌ 格式: 买入 代码 价格 数量 [原因] [账户]")
            sys.exit(1)
        trade, positions = record_trade("买入", code, price, quantity, reason, account)
        print(f"✅ 买入记录成功!")
        print(f"   {trade['code']} {trade['name']} {trade['price']} × {trade['quantity']} = {trade['amount']:,.2f}")
        print(f"   原因: {reason} | 账户: {account}")
        show_positions()

    elif cmd == '卖出':
        code = args[1].zfill(6) if len(args) > 1 else ''
        price = float(args[2]) if len(args) > 2 else 0
        quantity = float(args[3]) if len(args) > 3 else 0
        reason = args[4] if len(args) > 4 else ''
        account = args[5] if len(args) > 5 else ''
        if not code or not price or not quantity:
            print("❌ 格式: 卖出 代码 价格 数量 [原因] [账户]")
            sys.exit(1)
        trade, positions = record_trade("卖出", code, price, quantity, reason, account)
        print(f"✅ 卖出记录成功!")
        print(f"   {trade['code']} {trade['name']} {trade['price']} × {trade['quantity']} = {trade['amount']:,.2f}")
        print(f"   原因: {reason} | 账户: {account}")
        show_positions()

    elif cmd == '持仓':
        # 持仓 [live] ← 加live参数实时刷价格
        live = 'live' in args or '实时' in args
        show_positions(show_pnl=live)

    elif cmd == '日志':
        limit = int(args[1]) if len(args) > 1 else 20
        show_trade_log(limit)

    elif cmd == '盈亏':
        # 获取实时价格
        data = load_positions()
        codes = [k for k,v in data["positions"].items() if v["shares"] > 0]
        print(f"📡 正在获取 {len(codes)} 只股票最新价...")
        price_map = get_live_prices(codes)
        print(f"   已获取 {len(price_map)} 只价格")

        results, tm, tu, tr = update_prices_and_calc(price_map)

        print(f"\n💹 持仓盈亏明细")
        print(f"  {'代码':<8} {'名称':<10} {'持仓':>6} {'均价':>8} {'现价':>8} {'市值':>10} {'浮动':>10} {'已实现':>10}")
        print(f"  {'-'*75}")
        for r in sorted(results, key=lambda x: x['market'], reverse=True):
            print(f"  {r['code']:<8} {r['name']:<10} {r['shares']:>6.0f} {r['avg_cost']:>8.3f} {r['price']:>8.3f} {r['market']:>10,.2f} {r['unrealized']:>+10,.2f} {r['realized_pnl']:>+10,.2f}")
        print(f"  {'='*75}")
        total_pnl = tu + tr
        print(f"  {'合计':<18} {'':<6} {'':<8} {'':<8} {tm:>10,.2f} {tu:>+10,.2f} {tr:>+10,.2f}  {total_pnl:>+10,.2f}")
        show_pnl()

    elif cmd == '清仓':
        code = args[1].zfill(6) if len(args) > 1 else ''
        reason = args[2] if len(args) > 2 else ''
        data = load_positions()
        if code in data["positions"]:
            pos = data["positions"][code]
            if pos["shares"] > 0:
                trade, _ = record_trade("卖出", code, 0, pos["shares"], f"清仓: {reason}", "清仓")
                print(f"✅ {code} 已清仓，数量: {pos['shares']}")
            else:
                print(f"⚠️ {code} 当前无持仓")
        show_positions()

    elif cmd == '修改名称':
        code = args[1].zfill(6) if len(args) > 1 else ''
        name = args[2] if len(args) > 2 else ''
        data = load_positions()
        if code in data["positions"]:
            data["positions"][code]["name"] = name
            save(data)
            print(f"✅ {code} 名称已修改为: {name}")
        else:
            print(f"⚠️ {code} 不在持仓中")

    else:
        print(f"❌ 未知命令: {cmd}")
        print(__doc__)
