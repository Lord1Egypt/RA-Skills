#!/usr/bin/env python3
# 消费记录添加工具

import json
import sys
import os
import re
import datetime
import fcntl

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(_SCRIPT_DIR, 'expense_records.json'))
LOCK_FILE = os.environ.get('EXPENSE_LOCK_FILE', DATA_FILE + '.lock')

# 地点关键词模式
LOCATION_PATTERNS = [
    # 带关键词：XX商场、XX店、XX路、XX大厦、XX园、XX城、XX广场、XX中心、XX park/COCOPARK 等
    r'([\u4e00-\u9fa5]{2,10}(?:商场|店|路|大厦|园|城|广场|中心|park|COCO[Pp]?[Aa]?[Rr]?[Kk]?|Cocopark))',
    # 深圳知名地标/商圈（不带后缀也能识别）
    r'(华强北|东门|蛇口|大梅沙|小梅沙|世界之窗|欢乐港湾|海上世界|深圳湾|人才公园)',
    # XX+行政区：福田、南山、宝安、龙华、罗湖、龙岗、光明、坪山、大鹏、盐田
    r'((?:福田|南山|宝安|龙华|罗湖|龙岗|光明|坪山|大鹏|盐田|香港|广州|北京|上海|成都|杭州|武汉|长沙|南京|重庆)[\u4e00-\u9fa5a-zA-Z0-9]{0,8})',
    # 通用：两个以上中文 + (大厦|路|街|村|区|街口)
    r'([\u4e00-\u9fa5]{2,8}(?:大厦|路|街|村|区|街口|湾|角|台))',
    # COCO 相关
    r'(COCO[Pp]?[Aa]?[Rr]?[Kk]?(?:广场)?)',
]


def extract_location(note):
    """从备注中自动提取地点信息"""
    if not note:
        return None

    # 第一步：优先从括号内容中找
    # 支持全角和半角括号
    bracket_contents = re.findall(r'[（(【\[]([^）)】\]]+)[）)】\]]', note)

    for content in bracket_contents:
        loc = _match_location(content)
        if loc:
            return loc

    # 第二步：在整个 note 中找
    return _match_location(note)


def _match_location(text):
    """尝试匹配文本中的地点"""
    for pattern in LOCATION_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            loc = m.group(1).strip()
            # 清理无意义前缀
            loc = re.sub(r'^(美团|饿了么|京东|淘宝|拼多多|抖音|大众点评)[，,]?\s*', '', loc)
            # 去掉尾部单字 "店"（如 "宝安大仟里店" → "宝安大仟里"）
            if loc.endswith('店') and len(loc) > 3:
                loc = loc[:-1]
            if loc and len(loc) >= 2:
                return loc
    return None


def add_expense(category, amount, note="", location=None):
    """添加消费记录"""
    try:
        # === 文件锁临界区开始 ===
        with open(LOCK_FILE, 'a') as lock_f:
            fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
            try:
                # 加载现有数据
                try:
                    with open(DATA_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except FileNotFoundError:
                    data = {
                        "records": [],
                        "categories": ["交通", "餐饮", "购物", "娱乐", "医疗", "教育", "其他"],
                        "settings": {},
                        "metadata": {}
                    }

                # 验证分类
                if category not in data['categories']:
                    print(f"❌ 无效分类: {category}")
                    print(f"有效分类: {', '.join(data['categories'])}")
                    sys.exit(1)

                # 验证金额
                try:
                    amount_float = float(amount)
                    if amount_float == 0:
                        print("❌ 金额不能为0")
                        sys.exit(1)
                except ValueError:
                    print("❌ 金额必须是数字")
                    sys.exit(1)

                # 获取当前日期
                today = datetime.datetime.now().strftime('%Y-%m-%d')

                # 查找今天的记录
                today_record = None
                for record in data['records']:
                    if record['date'] == today:
                        today_record = record
                        break

                # 如果今天没有记录，创建新记录
                if today_record is None:
                    today_record = {
                        "date": today,
                        "items": [],
                        "total": 0
                    }
                    data['records'].append(today_record)

                # 地点处理：手动 --location 优先，否则尝试从 note 自动提取
                auto_loc = None
                if not location:
                    auto_loc = extract_location(note)

                # 添加新项目
                now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                new_item = {
                    "datetime": now_str,
                    "category": category,
                    "amount": amount_float,
                    "note": note
                }
                if location:
                    new_item["location"] = location
                elif auto_loc:
                    new_item["location"] = auto_loc

                today_record['items'].append(new_item)

                # 更新总额（正数退款减少总额，负数消费增加总额）
                today_record['total'] = sum(-item['amount'] for item in today_record['items'])

                # 更新元数据
                data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
                data['metadata']['total_days'] = len(data['records'])
                data['metadata']['total_amount'] = sum(record['total'] for record in data['records'])

                # 保存文件
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            finally:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
            # === 文件锁临界区结束 ===

        # 输出
        print(f"✅ 记录添加成功:")
        print(f"   日期: {today}")
        print(f"   分类: {category}")
        if amount_float > 0:
            print(f"   ✅ 退款 +¥{round(amount_float, 2)}")
        else:
            print(f"   💸 消费 ¥{round(abs(amount_float), 2)}")
        if note:
            print(f"   备注: {note}")
        final_loc = location or auto_loc
        if final_loc:
            print(f"   地点: {final_loc}")
        else:
            print(f"   📍 未识别到地点，下次可加 --location 手动标注，方便后续统计")
        print(f"   今日总计: ¥{round(abs(today_record['total']), 2)}")

        return True
        
    except Exception as e:
        print(f"❌ 添加记录失败: {e}")
        return False

def show_help():
    """显示帮助"""
    print("📝 消费记录添加工具")
    print("用法: python3 add_expense.py <分类> <金额> [备注] [--location <地点>]")
    print()
    print("示例:")
    print("  python3 add_expense.py 交通 4 地铁")
    print("  python3 add_expense.py 餐饮 15 午餐 --location 福田cocopark")
    print("  python3 add_expense.py 餐饮 28 午餐 -l 南山海岸城")
    print()
    print("可用分类: 交通, 餐饮, 购物, 娱乐, 医疗, 教育, 其他")

def main():
    # 支持旧格式: add_expense.py <cat> <amt> [note]
    # 支持新格式: add_expense.py <cat> <amt> [note] --location <loc> 或 -l <loc>
    if len(sys.argv) < 3:
        show_help()
        return
    
    # 手动解析以兼容旧调用方式
    category = sys.argv[1]
    amount = sys.argv[2]
    
    # 查找 --location 或 -l
    location = None
    note_parts = []
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] in ('--location', '-l') and i + 1 < len(sys.argv):
            location = sys.argv[i + 1]
            i += 2
        else:
            note_parts.append(sys.argv[i])
            i += 1
    
    note = " ".join(note_parts)
    
    add_expense(category, amount, note, location)

if __name__ == "__main__":
    main()