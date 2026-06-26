#!/usr/bin/env python3
"""
自然语言记账解析器（CSV 格式版）

将中文自然语言输入解析为 CSV 格式账本条目。
完全原创 CSV 格式。

CSV 格式：日期,类型,金额,分类,描述,账户
- 类型：支出 / 收入
- 无层级账户，无多行条目

用法:
    python parse_entry.py -- "今天吃饭花了50块"
    python parse_entry.py -- "收到工资 15000 元" --json
    python parse_entry.py -- "昨天打车35" --append /path/to/ledger.csv
    echo "午饭35" | python parse_entry.py
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path


# ==================== 分类关键词映射 ====================

CATEGORY_KEYWORDS = {
    "餐饮": [
        "吃饭", "外卖", "午餐", "晚餐", "早餐", "午饭", "晚饭", "早饭",
        "夜宵", "零食", "奶茶", "咖啡", "饮料", "水果", "聚餐",
        "食堂", "快餐", "火锅", "烧烤", "小龙虾", "面", "米饭", "面包",
        "蛋糕", "甜品", "黄焖鸡", "麻辣烫", "冒菜", "米线",
        "肯德基", "KFC", "麦当劳", "星巴克", "瑞幸", "蜜雪冰城",
        "饭", "菜", "肉", "吃喝", "餐",
    ],
    "交通": [
        "打车", "滴滴", "地铁", "公交", "加油", "停车", "过路费", "高速",
        "火车", "高铁", "飞机", "机票", "车票", "共享单车", "骑车",
        "出行", "通勤", "摩的", "出租车",
        "顺风车", "拼车", "船票", "轮渡", "电瓶车", "违章", "充电桩",
    ],
    "购物": [
        "买衣服", "买鞋", "买包", "买手机", "买电脑", "买书", "外套", "衣服",
        "裤子", "裙子", "帽子", "鞋子",
        "淘宝", "京东", "拼多多", "网购", "超市", "便利店", "盒马",
        "日用品", "生活用品", "洗衣液", "纸巾", "牙膏",
        "数码", "家电", "amazon", "得物", "唯品会",
    ],
    "居住": [
        "房租", "水电", "电费", "水费", "燃气", "物业", "网费",
        "宽带", "维修", "家具", "装修", "租房",
        "月供", "房贷", "还款", "押金", "搬家", "家政", "保洁",
        "燃气费", "暖气", "空调费", "垃圾费",
    ],
    "娱乐": [
        "电影", "游戏", "KTV", "唱歌", "酒吧", "旅游", "门票",
        "演出", "音乐会", "展览", "健身房", "运动", "会员",
        "VIP", "视频会员", "音乐会员", "爱奇艺", "优酷", "腾讯视频",
        "netflix", "spotify", "B站大会员",
    ],
    "通讯": [
        "话费", "充值", "流量", "手机套餐", "电话费",
    ],
    "医疗": [
        "看病", "医院", "药", "挂号", "体检", "牙科", "眼科",
        "门诊", "手术", "保险", "医保", "药房", "药店",
        "输液", "疫苗", "验血", "中医", "理疗",
    ],
    "教育": [
        "课程", "培训", "学费", "书", "考试", "报名费",
        "网课", "知识付费", "得到", "知乎", "极客时间",
    ],
    "社交": [
        "红包", "礼物", "请客", "随份子", "份子钱", "生日",
        "结婚", "请吃饭",
    ],
    "其他": [],
}

# 收入关键词
INCOME_KEYWORDS = [
    "工资", "薪资", "薪水", "奖金", "年终", "绩效", "补贴",
    "收到", "报销", "退款", "转账到", "红包收到", "理财收益",
    "利息", "分红", "兼职", "副业", "稿费", "提成",
    "入账", "到账", "进账",
]

# 收入分类映射
INCOME_CATEGORIES = {
    "工资": ["工资", "薪资", "薪水", "底薪"],
    "奖金": ["奖金", "年终", "绩效", "提成"],
    "理财收益": ["理财", "利息", "分红", "基金", "股票"],
    "兼职": ["兼职", "副业", "外快", "稿费"],
    "报销退款": ["报销", "退款"],
}

# 账户关键词映射
ACCOUNT_KEYWORDS = {
    "微信钱包": ["微信", "微信支付", "零钱"],
    "支付宝": ["支付宝", "花呗"],
    "银行卡": ["招行", "招商银行", "银行卡", "工行", "工商银行", "建行", "建设银行", "银行"],
    "现金": ["现金", "钞", "纸币"],
    "信用卡": ["信用卡"],
}


# ==================== 解析函数（原创实现） ====================

def parse_date(text: str, ref_date: datetime = None) -> tuple:
    """从文本中提取日期，返回 (date_str, remaining_text)。"""
    if ref_date is None:
        ref_date = datetime.now()

    # ISO 格式 YYYY-MM-DD
    m = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
    if m:
        date_str = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        remaining = text[:m.start()] + text[m.end():]
        return date_str, remaining.strip()

    # 中文日期：X月X号/日
    m = re.search(r'(\d{1,2})月(\d{1,2})[号日]', text)
    if m:
        month = int(m.group(1))
        day = int(m.group(2))
        year = ref_date.year
        date_str = f"{year}-{month:02d}-{day:02d}"
        remaining = text[:m.start()] + text[m.end():]
        return date_str, remaining.strip()

    # 相对日期
    relative_map = {
        "大前天": 3, "前天": 2, "昨天": 1,
        "今天": 0, "今日": 0,
    }
    for word, days_ago in relative_map.items():
        if word in text:
            d = ref_date - timedelta(days=days_ago)
            date_str = d.strftime("%Y-%m-%d")
            remaining = text.replace(word, "").strip()
            return date_str, remaining

    # 默认今天
    return ref_date.strftime("%Y-%m-%d"), text


def parse_amount(text: str) -> tuple:
    """从文本中提取金额，返回 (amount_float, remaining_text)。"""
    remaining = text

    # ¥ / ￥ 符号
    m = re.search(r'[¥￥]\s*(\d+\.?\d*)', remaining)
    if m:
        amount = float(m.group(1))
        remaining = remaining[:m.start()] + remaining[m.end():]
        return amount, remaining.strip()

    # X万Y千 格式（支持 1万5千 / 1万5 / 1万5000 / 1万5000千 等）
    m = re.search(r'(\d+\.?\d*)\s*万\s*(\d+)(?:千)?', remaining)
    if m:
        base = float(m.group(1)) * 10000
        rest = m.group(2)
        # 判断 rest 的量级：如果 >=4 位则直接加；否则当作千位
        rest_val = float(rest)
        if rest_val >= 1000:
            amount = base + rest_val
        else:
            amount = base + rest_val * 1000
        remaining = remaining[:m.start()] + remaining[m.end():]
        return amount, remaining.strip()

    # X万 格式
    m = re.search(r'(\d+\.?\d*)\s*万', remaining)
    if m:
        amount = float(m.group(1)) * 10000
        remaining = remaining[:m.start()] + remaining[m.end():]
        return amount, remaining.strip()

    # 数字 + 可选单位
    m = re.search(r'(\d+\.?\d*)\s*(?:块钱?|元)?', remaining)
    if m and float(m.group(1)) > 0:
        amount = float(m.group(1))
        remaining = remaining[:m.start()] + remaining[m.end():]
        remaining = re.sub(r'^\s*[块元块钱]+\s*', '', remaining)
        return amount, remaining.strip()

    return None, remaining


def detect_type(text: str) -> str:
    """判断是收入还是支出。返回 '收入' 或 '支出'（CSV 格式用中文）。"""
    for kw in INCOME_KEYWORDS:
        if kw in text:
            return "收入"
    expense_hints = ["花了", "买了", "付了", "消费", "扣了", "付款", "支付", "花费", "开销", "用了"]
    for kw in expense_hints:
        if kw in text:
            return "支出"
    return "支出"


def infer_category(text: str, txn_type: str) -> str:
    """根据文本推断分类。"""
    if txn_type == "收入":
        for cat, keywords in INCOME_CATEGORIES.items():
            for kw in keywords:
                if kw in text:
                    return cat
        return "其他"
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return cat
    return "其他"


def infer_account(text: str) -> str:
    """根据文本推断账户。"""
    for account, keywords in ACCOUNT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return account
    return "微信钱包"  # 默认账户


def extract_note(text: str) -> str:
    """提取备注信息。"""
    note = re.sub(r'(花了|买了|付了|收到|消费|扣了|充值)', '', text)
    note = re.sub(r'[\d\.]+\s*(万|块|元|块钱)?', '', note)
    note = re.sub(r'\s+', ' ', note).strip()
    return note if len(note) >= 2 else ""


# ==================== 核心解析 ====================

def parse_entry(text: str, ref_date: datetime = None, account: str = None) -> dict:
    """解析自然语言为结构化条目（字典格式）。"""
    text = text.strip()
    if not text:
        return None

    raw = text
    txn_type = detect_type(text)
    date_str, text = parse_date(text, ref_date)
    amount, text = parse_amount(text)

    if amount is None:
        return {"error": "无法识别金额", "raw": raw}

    category = infer_category(text, txn_type)
    used_account = account if account else (infer_account(text) or "微信钱包")
    description = text.strip() if text.strip() else category
    note = extract_note(text)

    return {
        "date": date_str,
        "type": txn_type,
        "category": category,
        "amount": round(amount, 2),
        "account": used_account,
        "description": description or category,
        "note": note,
        "raw": raw,
    }


def format_csv_line(entry: dict) -> str:
    """将解析结果格式化为 CSV 行。

    CSV 格式（6列，无表头）：
    日期,类型,金额,分类,描述,账户

    与传统双行记账的本质区别：
    - 无层级账户（不用 Assets:Assets:XXX）
    - 无多行条目（单行记录一笔交易）
    - 无需借贷平衡
    - 无 flag 标记（无 * 或 !）
    """
    if entry.get("error"):
        return None
    # CSV 格式：日期,类型,金额,分类,描述,账户
    # 描述中如果有逗号则加双引号包裹
    desc = entry["description"] or entry["category"]
    if ',' in desc or '"' in desc:
        desc = '"' + desc.replace('"', '""') + '"'
    return f"{entry['date']},{entry['type']},{entry['amount']:.2f},{entry['category']},{desc},{entry['account']}"


def parse_csv_line(line: str) -> dict:
    """解析一行 CSV，恢复为字典。使用 csv 模块正确处理引号包裹的描述字段。"""
    import csv
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    parts = next(csv.reader([line]))
    if len(parts) < 6:
        return None
    try:
        return {
            "date": parts[0],
            "type": parts[1],
            "amount": float(parts[2]),
            "category": parts[3],
            "description": parts[4],
            "account": parts[5],
        }
    except ValueError:
        return None


def _safe_write_path(path: Path) -> bool:
    """安全校验：只允许写入 ~/.openclaw/workspace/ 范围内的路径，返回 True/False"""
    try:
        if str(path.resolve()).startswith(str(Path.home() / ".openclaw" / "workspace")):
            return True
    except Exception:
        pass
    return False


def append_to_ledger(entry: dict, ledger_path: str) -> bool:
    """将条目追加到 CSV 账本文件。自动处理账户定义和初始余额。"""
    line = format_csv_line(entry)
    if not line:
        return False

    path = Path(ledger_path)
    if not _safe_write_path(path):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)

    account = entry["account"]

    with open(path, "a", encoding="utf-8-sig") as f:
        # 确保账户已定义
        _ensure_account_defined(path, account, f)
        # 追加交易行
        f.write(line + "\n")

    return True


def _ensure_account_defined(ledger_path: Path, account: str, file_handle) -> None:
    """检查账户是否已定义，没有则追加账户定义行和初始余额行。

    初始余额统一使用「余额,账户,金额」格式（与 SKILL.md 文档一致），
    默认 0.00，确保 query_ledger --balance 能正确读取。
    """
    content = ""
    if ledger_path.exists():
        content = ledger_path.read_text(encoding="utf-8")

    # 检查是否已有该账户的定义（正则精确匹配 "# 账户 {account}" 行首）
    if not re.search(rf"^# 账户 {re.escape(account)}(?:\s|$)", content, re.MULTILINE):
        file_handle.write(f"# 账户 {account}\n")

    # 检查是否已有该账户的初始余额行，没有则写入默认 0.00
    if not re.search(rf"^余额,{re.escape(account)},", content, re.MULTILINE):
        file_handle.write(f"余额,{account},0.00\n")


def read_all_entries(ledger_path: str) -> list:
    """读取账本所有条目（跳过注释和空行）。自动处理 UTF-8 BOM。"""
    path = Path(ledger_path)
    if not path.exists():
        return []

    entries = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        e = parse_csv_line(line)
        if e:
            entries.append(e)
    return entries


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(
        description="自然语言记账解析器（CSV 格式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python parse_entry.py --json "收到工资 15000 元"
  python parse_entry.py "今天吃饭花了50块"
  python parse_entry.py --append ./my.csv "昨天打车35"
        """,
    )

    parser.add_argument("--append", metavar="FILE", help="直接追加到指定账本文件")
    parser.add_argument("--account", metavar="账户", help="指定账户（覆盖自动推断）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出解析结果")
    parser.add_argument("text", nargs="+", help="自然语言记账文本")

    args = parser.parse_args()
    input_text = " ".join(args.text)

    if not input_text:
        print("❌ 无输入内容")
        sys.exit(1)

    # 解析日期参数（支持 --date YYYY-MM-DD）
    ref_date = None
    # argparse 不支持 --date，故通过检测文本中是否含日期来处理

    entry = parse_entry(input_text, ref_date=ref_date, account=args.account)

    if entry is None:
        print("❌ 无法解析输入")
        sys.exit(1)

    if entry.get("error"):
        print(f"❌ {entry['error']}，原文：{entry['raw']}")
        sys.exit(1)

    if args.json:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    else:
        line = format_csv_line(entry)
        print(line)
        print()

    if args.append:
        if append_to_ledger(entry, args.append):
            print(f"✅ 已追加到 {args.append}")
        else:
            print(f"❌ 追加失败")


if __name__ == "__main__":
    main()