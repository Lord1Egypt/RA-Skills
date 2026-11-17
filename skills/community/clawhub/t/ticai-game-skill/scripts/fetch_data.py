#!/usr/bin/env python3
"""
体彩历史数据拉取 — 自动抓取并保存为 CSV

数据源（按优先级）:
  1. 500.com 公开 API  (ews.500.com)
  2. 500star.com 数据页 (datachart.500star.com)
  3. 本地缓存文件
"""

import csv, json, os, sys, re, argparse
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")

# ── 彩种映射 ──────────────────────────────────────────────

LOTTERY_IDS = {
    "大乐透": {"id500": "dlt", "name500star": "dlt"},
    "排列3":  {"id500": "pl3",  "name500star": "pl3"},
    "排列5":  {"id500": "pl5",  "name500star": "pl5"},
    "七星彩":  {"id500": "qxc",  "name500star": "qxc"},
}

COLUMNS = {
    "大乐透": ["彩种","期号","开奖日期","号码1","号码2","号码3","号码4","号码5","号码6","号码7","奖池(亿)","销量(亿)"],
    "排列3":  ["彩种","期号","开奖日期","号码1","号码2","号码3"],
    "排列5":  ["彩种","期号","开奖日期","号码1","号码2","号码3","号码4","号码5"],
    "七星彩":  ["彩种","期号","开奖日期","号码1","号码2","号码3","号码4","号码5","号码6","号码7"],
}


# ── 公共工具 ──────────────────────────────────────────────

def http_get(url, headers=None):
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    if headers:
        h.update(headers)
    req = Request(url, headers=h)
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def save_csv(lottery, rows):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{lottery}.csv")
    exists = os.path.exists(path)
    existing_set = set()

    if exists:
        with open(path, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                existing_set.add(r.get("期号", ""))

    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(COLUMNS[lottery])
        for row in rows:
            if str(row[1]) not in existing_set:
                w.writerow(row)
                existing_set.add(str(row[1]))

    return path


def confirm_rows(lottery, rows):
    """去重后按期号排序"""
    seen = set()
    uniq = []
    for r in rows:
        qh = str(r[1])
        if qh not in seen:
            seen.add(qh)
            uniq.append(r)
    uniq.sort(key=lambda x: str(x[1]), reverse=True)
    return uniq


# ── 数据源1: 500star.com 表格抓取 ────────────────────────

BASE_500STAR = "https://datachart.500star.com"

URLS_500STAR = {
    "dlt": f"{BASE_500STAR}/dlt/history/newinc/history.php?start=1&end=100",
    "pl3": f"{BASE_500STAR}/pl3/history/newinc/history.php?start=1&end=100",
    "pl5": f"{BASE_500STAR}/pl5/history/newinc/history.php?start=1&end=100",
    "qxc": f"{BASE_500STAR}/qxc/history/newinc/history.php?start=1&end=100",
}


def parse_500star_table(html, lottery):
    """从 500star HTML 表格解析开奖数据"""
    rows = []

    if lottery == "大乐透":
        # 匹配: <tr class="t_tr1"> <td>期号</td> <td>号码1</td>...<td>后区1</td><td>后区2</td>
        pattern = re.compile(
            r'<tr[^>]*>.*?<td[^>]*>(\d+)</td>'  # 期号
            r'(?:.*?<td[^>]*>(\d+)</td>.*?){5}'  # 前区5个
            r'.*?<td[^>]*>(\d+)</td>'             # 后区1
            r'.*?<td[^>]*>(\d+)</td>'             # 后区2
            r'.*?<td[^>]*>([\d,]+)</td>'          # 奖池
            r'.*?<td[^>]*>([\d,]+)</td>',         # 销量
            re.DOTALL
        )
        for m in pattern.finditer(html):
            qihao = m.group(1)
            front = [m.group(i) for i in range(2, 7)]
            back = [m.group(7), m.group(8)]
            pool = m.group(9).replace(",", "")
            sales = m.group(10).replace(",", "")
            rows.append([lottery, qihao, ""] + front + back + [pool, sales])
    else:
        n = 3 if lottery == "排列3" else 5 if lottery == "排列5" else 7
        # 数字彩: 期号 + N个号码
        pattern = re.compile(
            r'<tr[^>]*>.*?<td[^>]*>(\d+)</td>' +
            r'(?:.*?<td[^>]*>(\d+)</td>.*?){{{}}}'.format(n),
            re.DOTALL
        )
        for m in pattern.finditer(html):
            qihao = m.group(1)
            nums = [m.group(i) for i in range(2, 2 + n)]
            rows.append([lottery, qihao, ""] + nums)

    return rows


# ── 数据源2: 500.com 公开 JSON API ───────────────────────

def fetch_500api(lottery, count=50):
    """通过 500.com API 获取历史数据"""
    lid = LOTTERY_IDS[lottery]["id500"]
    url = f"https://ews.500.com/xcxkj/kaijiang/history?lotid={lid}&num={count}"
    try:
        text = http_get(url)
        data = json.loads(text)
    except Exception:
        return []

    rows = []
    items = data.get("data", {}).get("list", data.get("list", []))
    for item in items:
        qihao = str(item.get("issue", item.get("期号", "")))
        result = item.get("result", item.get("开奖号码", ""))
        date = item.get("opendate", item.get("开奖日期", ""))
        nums = re.findall(r"\d+", result)

        if lottery == "大乐透" and len(nums) >= 7:
            pool = item.get("pool", item.get("奖池", "0")).replace(",", "")
            sale = item.get("sale", item.get("销量", "0")).replace(",", "")
            rows.append([lottery, qihao, date] + nums[:7] + [pool, sale])
        elif lottery in ("排列3", "排列5", "七星彩") and len(nums) >= (3 if lottery == "排列3" else 5 if lottery == "排列5" else 7):
            rows.append([lottery, qihao, date] + nums[: (3 if lottery == "排列3" else 5 if lottery == "排列5" else 7)])

    return rows


# ── 本地生成（离线降级） ──────────────────────────────────

def generate_local(lottery, count=50):
    """离线时用本地生成器制造示例数据"""
    try:
        from generate_data import generate
        rows, _ = generate(lottery, count)
        print(f"[本地生成] 生成 {len(rows)} 条示例数据")
        return confirm_rows(lottery, rows)
    except Exception:
        # 兜底: 硬编码几期
        print("[本地生成] 不可用")
        return []


# ── 组合取数 ──────────────────────────────────────────────

def fetch(lottery, count=50):
    """主入口: 依次尝试各数据源（自动降级）"""
    rows = fetch_500api(lottery, count)
    if rows:
        print(f"[500API] 获取 {len(rows)} 条")
        return confirm_rows(lottery, rows)

    print("[500API] 失败 → 尝试 500star 页面抓取...")
    try:
        lid = LOTTERY_IDS[lottery]["name500star"]
        url = URLS_500STAR[lid]
        html = http_get(url)
        rows = parse_500star_table(html, lottery)
        if rows:
            print(f"[500star] 获取 {len(rows)} 条")
            return confirm_rows(lottery, rows)
    except Exception as e:
        print(f"[500star] 抓取失败: {e}")

    print("⚠️  在线数据源均失败 → 降级为本地生成示例数据")
    return generate_local(lottery, count)


# ── 主 CLI ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="体彩历史数据拉取")
    parser.add_argument("--lottery", "-l", default="大乐透",
                        choices=list(LOTTERY_IDS.keys()), help="彩种")
    parser.add_argument("--count", "-n", type=int, default=50, help="拉取期数(最多100)")
    parser.add_argument("--output", "-o", help="输出路径（默认 cache/目录）")
    parser.add_argument("--no-cache", action="store_true", help="不写入缓存")
    args = parser.parse_args()

    rows = fetch(args.lottery, args.count)
    if not rows:
        sys.exit(1)

    # 生成数据
    if args.output:
        path = args.output
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(COLUMNS[args.lottery])
            w.writerows(rows)
        print(f"✅ 已保存 {len(rows)} 条 → {path}")
    elif not args.no_cache:
        path = save_csv(args.lottery, rows)
        print(f"✅ 已保存 {len(rows)} 条 → {path}")
    else:
        w = csv.writer(sys.stdout)
        w.writerow(COLUMNS[args.lottery])
        w.writerows(rows)

    # 显示最近5期预览
    print(f"\n📋 最近5期预览:")
    for r in rows[:5]:
        if args.lottery == "大乐透":
            nums = " ".join(f"{int(r[i]):02d}" for i in range(3, 8))
            backs = " ".join(f"{int(r[i]):02d}" for i in range(8, 10))
            print(f"  {r[1]}: {nums} + {backs}")
        else:
            print(f"  {r[1]}: {' '.join(str(r[i]) for i in range(3, len(r)))}")


if __name__ == "__main__":
    main()
