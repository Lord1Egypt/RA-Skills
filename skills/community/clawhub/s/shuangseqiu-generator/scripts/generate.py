#!/usr/bin/env python3
"""
双色球玄学生成器 - 中式玄学完整版
基于生日、姓名、生肖、星座生成个性化幸运号码
"""

import random
import argparse
import hashlib
from datetime import datetime, date
import sys

# ============ 中式玄学数据 ============

# 生肖对应数字（鼠=1, 牛=2, ... 猪=12）
ZODIAC_MAP = {
    '鼠': 1, '牛': 2, '虎': 3, '兔': 4, 
    '龙': 5, '蛇': 6, '马': 7, '羊': 8, 
    '猴': 9, '鸡': 10, '狗': 11, '猪': 12,
    'rat': 1, 'ox': 2, 'tiger': 3, 'rabbit': 4,
    'dragon': 5, 'snake': 6, 'horse': 7, 'goat': 8,
    'monkey': 9, 'rooster': 10, 'dog': 11, 'pig': 12
}

# 星座日期范围和幸运数
CONSTELLATION_DATA = {
    '白羊座': (3, 21, 4, 19, [1, 9, 18, 24, 32]),
    '金牛座': (4, 20, 5, 20, [2, 6, 15, 24, 30]),
    '双子座': (5, 21, 6, 21, [3, 12, 21, 27, 33]),
    '巨蟹座': (6, 22, 7, 22, [2, 8, 15, 23, 30]),
    '狮子座': (7, 23, 8, 22, [1, 10, 19, 28, 32]),
    '处女座': (8, 23, 9, 22, [5, 14, 23, 28, 31]),
    '天秤座': (9, 23, 10, 23, [3, 11, 20, 27, 33]),
    '天蝎座': (10, 24, 11, 22, [2, 9, 18, 26, 30]),
    '射手座': (11, 23, 12, 21, [1, 12, 21, 27, 32]),
    '摩羯座': (12, 22, 1, 19, [3, 10, 19, 25, 31]),
    '水瓶座': (1, 20, 2, 18, [4, 13, 22, 28, 33]),
    '双鱼座': (2, 19, 3, 20, [2, 11, 20, 26, 30])
}

# 五行对应数字
WU_XING_NUMBERS = {
    '金': [4, 9, 14, 19, 24, 29],
    '木': [1, 8, 13, 18, 23, 28],
    '水': [6, 11, 16, 21, 26, 31],
    '火': [2, 7, 12, 17, 22, 27, 32],
    '土': [5, 10, 15, 20, 25, 30]
}

# 生肖幸运数
ZODIAC_LUCKY_NUMBERS = {
    1: [2, 3, 7, 11, 12],   # 鼠
    2: [1, 9, 10, 19, 29],   # 牛
    3: [1, 3, 4, 13, 24],    # 虎
    4: [2, 3, 9, 14, 25],    # 兔
    5: [1, 6, 7, 15, 28],    # 龙
    6: [2, 3, 9, 18, 27],    # 蛇
    7: [2, 5, 6, 14, 26],    # 马
    8: [2, 4, 6, 13, 25],    # 羊
    9: [1, 7, 10, 19, 28],   # 猴
    10: [2, 5, 9, 12, 24],   # 鸡
    11: [3, 4, 9, 11, 23],   # 狗
    12: [2, 4, 8, 15, 26]    # 猪
}

# 方位对应数字
DIRECTION_NUMBERS = {
    '东': [1, 3, 5, 7, 9],
    '南': [2, 4, 6, 8, 10],
    '西': [11, 13, 15, 17, 19],
    '北': [12, 14, 16, 18, 20],
    '东南': [1, 3, 5, 7, 9],
    '东北': [3, 5, 7, 9, 11],
    '西南': [2, 4, 6, 8, 10],
    '西北': [11, 13, 15, 17, 19]
}

# 幸运颜色
LUCKY_COLORS = ['红色', '蓝色', '绿色', '金色', '紫色', '粉色']


def parse_birthday(birthday_str):
    """解析生日字符串（支持多种格式）"""
    formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%d-%m-%Y', '%d/%m/%Y']
    for fmt in formats:
        try:
            return datetime.strptime(birthday_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"无法解析生日: {birthday_str}")


def get_zodiac_year(birthday):
    """获取生肖"""
    zodiac_animals = ['猴', '鸡', '狗', '猪', '鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊']
    year = birthday.year
    start_year = 2008  # 鼠年
    offset = (year - start_year) % 12
    return zodiac_animals[offset]


def get_constellation(birthday):
    """获取星座"""
    month = birthday.month
    day = birthday.day
    for name, (start_m, start_d, end_m, end_d, lucky) in CONSTELLATION_DATA.items():
        if month == start_m and day >= start_d or month == end_m and day <= end_d:
            return name, lucky
        if month == 12 and day >= 22:
            return '摩羯座', CONSTELLATION_DATA['摩羯座'][4]
        if month == 1 and day <= 19:
            return '摩羯座', CONSTELLATION_DATA['摩羯座'][4]
    return '射手座', CONSTELLATION_DATA['射手座'][4]


def get_wu_xing(birthday):
    """根据生日计算五行"""
    year = birthday.year
    # 天干地支简化计算
    tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    
    # 五行对应
    wu_xing_map = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
        '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
        '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
        '戌': '土', '亥': '水'
    }
    
    gan = tian_gan[gan_idx]
    zhi = di_zhi[zhi_idx]
    wu_xing = wu_xing_map.get(gan, '土')
    
    return wu_xing, gan, zhi


def calculate_name_energy(name):
    """计算姓名能量（基于Unicode编码）"""
    if not name:
        return 0
    energy = sum(ord(c) for c in name)
    return energy % 100


def generate_seed(birthday, name=None, zodiac=None, constellation=None):
    """生成随机种子"""
    base = birthday.year * 10000 + birthday.month * 100 + birthday.day
    
    if name:
        name_energy = calculate_name_energy(name)
        base = base * 100 + (name_energy % 100)
    
    if zodiac and zodiac in ZODIAC_MAP:
        base = base * 10 + ZODIAC_MAP[zodiac]
    
    seed = int(hashlib.md5(str(base).encode()).hexdigest()[:8], 16) % (10**8)
    return seed


def calculate_fortune_level(birthday, name=None):
    """计算当日运势等级"""
    base_score = 60
    day = (birthday.day * birthday.month + birthday.year) % 100
    
    if name:
        name_bonus = calculate_name_energy(name) % 30
        day += name_bonus
    
    weekday = birthday.weekday()
    if weekday in [4, 5]:  # 周末加分
        day += 10
    
    level = min(5, max(1, int(day / 25) + 1))
    return level


def get_direction(birthday, name=None):
    """获取吉利方位"""
    base = (birthday.month + birthday.day) % 8
    directions = ['东', '东南', '南', '西南', '西', '西北', '北', '东北']
    lucky_direction = directions[base % 8]
    
    if name:
        bonus = calculate_name_energy(name) % 8
        lucky_direction = directions[(base + bonus) % 8]
    
    return lucky_direction


def get_lucky_color(birthday, name=None):
    """获取幸运颜色"""
    base = (birthday.month * birthday.day) % len(LUCKY_COLORS)
    color = LUCKY_COLORS[base]
    
    if name:
        bonus = calculate_name_energy(name) % len(LUCKY_COLORS)
        color = LUCKY_COLORS[(base + bonus) % len(LUCKY_COLORS)]
    
    return color


def weighted_random_choice(pool, weights, count, seed_state):
    """加权随机选择"""
    random.seed(seed_state)
    if len(pool) <= count:
        return sorted(pool)
    
    selected = []
    remaining_pool = list(pool)
    remaining_weights = list(weights)
    
    while len(selected) < count and remaining_pool:
        total_weight = sum(remaining_weights)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for i, w in enumerate(remaining_weights):
            cumulative += w
            if r <= cumulative:
                selected.append(remaining_pool[i])
                remaining_pool.pop(i)
                remaining_weights.pop(i)
                break
    
    return sorted(selected)


def generate_xuanxue_shuangseqiu(birthday, name=None, zodiac=None, constellation=None, count=1):
    """玄学生成双色球"""
    
    # 解析输入
    zodiac_num = ZODIAC_MAP.get(zodiac) if zodiac else None
    constellation_name, constellation_lucky = (get_constellation(birthday) if not constellation 
                                                else (constellation, CONSTELLATION_DATA.get(constellation, [0,0,0,0,[1,2,3,4,5]])[4]))
    wu_xing, gan, zhi = get_wu_xing(birthday)
    fortune_level = calculate_fortune_level(birthday, name)
    lucky_direction = get_direction(birthday, name)
    lucky_color = get_lucky_color(birthday, name)
    
    # 生成种子
    seed = generate_seed(birthday, name, zodiac, constellation)
    random.seed(seed)
    
    results = []
    
    for _ in range(count):
        # ====== 生成红球 ======
        all_balls = list(range(1, 34))
        weights = [1] * 33
        
        # 生肖加权
        if zodiac_num and zodiac_num in ZODIAC_LUCKY_NUMBERS:
            for n in ZODIAC_LUCKY_NUMBERS[zodiac_num]:
                if n <= 33:
                    idx = n - 1
                    weights[idx] += 3
        
        # 星座幸运数加权
        for n in constellation_lucky:
            if n <= 33:
                idx = n - 1
                weights[idx] += 2
        
        # 五行幸运数加权
        wu_xing_nums = WU_XING_NUMBERS.get(wu_xing, [])
        for n in wu_xing_nums:
            if n <= 33:
                idx = n - 1
                weights[idx] += 2
        
        # 运势加权（运势高有更多机会选到幸运数）
        fortune_bonus = fortune_level
        for i in range(33):
            if random.random() < fortune_bonus * 0.1:
                weights[i] += 1
        
        # 生成6个红球
        red_balls = weighted_random_choice(all_balls, weights, 6, seed + _)
        
        # ====== 生成蓝球 ======
        blue_pool = list(range(1, 17))
        blue_weights = [1] * 16
        
        # 星座蓝球幸运数
        if constellation_lucky:
            for n in constellation_lucky:
                if n <= 16:
                    blue_weights[n-1] += 3
        
        # 五行蓝球加权
        wu_xing_blue_map = {'金': [4, 9], '木': [3, 8], '水': [6, 11], '火': [2, 7], '土': [5, 10]}
        for n in wu_xing_blue_map.get(wu_xing, []):
            if n <= 16:
                blue_weights[n-1] += 2
        
        blue_ball = weighted_random_choice(blue_pool, blue_weights, 1, seed + 100 + _)[0]
        
        results.append((red_balls, blue_ball))
    
    return {
        'name': name,
        'birthday': birthday,
        'zodiac': zodiac or get_zodiac_year(birthday),
        'constellation': constellation_name,
        'wu_xing': wu_xing,
        'gan': gan,
        'zhi': zhi,
        'fortune_level': fortune_level,
        'lucky_direction': lucky_direction,
        'lucky_color': lucky_color,
        'results': results
    }


def format_output(data, count=1):
    """格式化输出"""
    birthday_str = data['birthday'].strftime('%Y年%m月%d日')
    name_str = f"【{data['name']}】" if data['name'] else ''
    
    # 运势星星
    stars = '⭐' * data['fortune_level']
    
    output = f"""
╔══════════════════════════════════════════════════════════╗
║           🎰 双色球玄学能量号码 🎰                          ║
╠══════════════════════════════════════════════════════════╣
║  {name_str}专属定制                                              ║
╠══════════════════════════════════════════════════════════╣
║  📅 生日: {birthday_str}                                      ║
║  🐾 生肖: {data['zodiac']}  星座: {data['constellation']}                         ║
║  🧭 五行: {data['wu_xing']}（{data['gan']}{data['zhi']}）                              ║
║  ⭐ 运势: {stars} ({data['fortune_level']}星)                                   ║
║  🎨 幸运色: {data['lucky_color']}  方位: {data['lucky_direction']}                        ║
╚══════════════════════════════════════════════════════════╝

"""
    
    for i, (red, blue) in enumerate(data['results'], 1):
        red_str = ' '.join(f'{n:02d}' for n in red)
        if len(data['results']) > 1:
            output += f"🔮 第{i}组:\n"
        output += f"   🔴 红球: {red_str}\n"
        output += f"   🔵 蓝球: {blue:02d}\n\n"
    
    # 玄学解说
    fortune_texts = {
        1: '今日运势平稳，适合守号观望',
        2: '今日小吉，运势上升中',
        3: '今日运势良好，幸运指数攀升',
        4: '今日大吉！能量充沛，中奖概率UP!',
        5: '今日超级旺！宇宙能量汇聚，抓住机会!'
    }
    
    lucky_tips = [
        '记得多晒晒太阳，吸收阳能量',
        '今天适合穿幸运色服装',
        '保持心情愉悦，好运自然来',
        f'往{data["lucky_direction"]}方向走，遇见惊喜',
        '买完彩票别忘了许愿哦'
    ]
    
    output += f"✨ 【玄学指引】\n"
    output += f"   {fortune_texts[data['fortune_level']]}\n"
    output += f"   {random.choice(lucky_tips)}\n"
    output += f"\n🍀 祝您好运常在，心想事成！"
    
    return output


def main():
    parser = argparse.ArgumentParser(description='双色球玄学生成器')
    parser.add_argument('--name', '-n', type=str, help='姓名（选填）')
    parser.add_argument('--birthday', '-b', type=str, required=True, help='出生日期（必填），格式: YYYY-MM-DD')
    parser.add_argument('--zodiac', '-z', type=str, help='生肖（选填），如: 鼠、牛、虎...')
    parser.add_argument('--constellation', '-c', type=str, help='星座（选填），如: 白羊座、金牛座...')
    parser.add_argument('--count', '-k', type=int, default=1, help='生成组数（默认1，最多10）')
    
    args = parser.parse_args()
    
    try:
        birthday = parse_birthday(args.birthday)
    except ValueError as e:
        print(f"❌ 生日格式错误: {e}")
        print("正确格式: YYYY-MM-DD (如: 1990-05-15)")
        sys.exit(1)
    
    if args.count < 1 or args.count > 10:
        print("❌ 组数必须在1-10之间")
        sys.exit(1)
    
    result = generate_xuanxue_shuangseqiu(
        birthday=birthday,
        name=args.name,
        zodiac=args.zodiac,
        constellation=args.constellation,
        count=args.count
    )
    
    print(format_output(result, args.count))


if __name__ == '__main__':
    main()
