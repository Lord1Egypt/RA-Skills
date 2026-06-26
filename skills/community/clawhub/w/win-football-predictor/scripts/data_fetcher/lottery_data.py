"""
中国体育彩票传统足彩数据采集器
数据源: 500.com 彩票数据 (500.com/tczq/)
历史期号: 2022-2026年
"""
import json
import re
import math
from datetime import datetime, timedelta

# 模拟历史期号数据（实际生产环境需对接真实API）
# 格式: {期号: {home_team, away_team, league, match_time, odds, result}}

# 胜负彩期号前缀
PERIOD_PREFIXES = {
    2022: '220',
    2023: '230',
    2024: '240',
    2025: '250',
    2026: '260',
}


def generate_lottery_periods(year: int) -> list:
    """生成某年的所有期号"""
    prefix = PERIOD_PREFIXS.get(year, f'{year % 100:02d}0')
    periods = []
    if year == 2022:
        # 22001 - 22180 约180期
        for i in range(1, 181):
            periods.append(f'22{i:03d}')
    elif year == 2023:
        for i in range(1, 181):
            periods.append(f'23{i:03d}')
    elif year == 2024:
        for i in range(1, 181):
            periods.append(f'24{i:03d}')
    elif year == 2025:
        for i in range(1, 181):
            periods.append(f'25{i:03d}')
    elif year == 2026:
        for i in range(1, 61):
            periods.append(f'26{i:03d}')
    return periods


def get_league_by_period(period: str, match_index: int) -> str:
    """
    根据期号和比赛索引判断联赛
    传统足彩14场通常混合五大联赛+杯赛
    """
    league_rotation = [
        '英超', '西甲', '意甲', '德甲', '法甲',
        '英超', '西甲', '意甲', '德甲', '法甲',
        '英超', '欧冠', '欧联', '荷甲',
    ]
    return league_rotation[match_index % len(league_rotation)]


def get_match_teams(period: str, match_index: int, league: str) -> tuple:
    """根据期号和比赛索引生成主客队（用于演示）"""
    teams_db = {
        '英超': [('曼城', '阿森纳'), ('利物浦', '曼联'), ('切尔西', '热刺'), ('阿斯顿维拉', '纽卡斯尔'),
                ('布莱顿', '水晶宫'), ('富勒姆', '狼队'), ('西汉姆', '埃弗顿')],
        '西甲': [('皇马', '巴萨'), ('马竞', '塞维利亚'), ('皇家社会', '比利亚雷亚尔'), ('毕尔巴鄂', '巴伦西亚'),
                ('贝蒂斯', '赫罗纳'), ('奥萨苏纳', '阿拉维斯')],
        '意甲': [('国米', '尤文'), ('AC米兰', '那不勒斯'), ('罗马', '拉齐奥'), ('亚特兰大', '佛罗伦萨'),
                ('都灵', '博洛尼亚'), ('乌迪内斯', '萨索洛')],
        '德甲': [('拜仁', '多特'), ('莱比锡', '勒沃库森'), ('法兰克福', '门兴'), ('霍芬海姆', '柏林联合'),
                ('沃尔夫斯堡', '弗赖堡'), ('美因茨', '科隆')],
        '法甲': [('巴黎', '马赛'), ('摩纳哥', '里昂'), ('里尔', '尼斯'), ('雷恩', '兰斯'),
                ('南特', '波尔多'), ('斯特拉斯堡', '蒙彼利埃')],
        '欧冠': [('曼城', '皇马'), ('拜仁', '巴萨'), ('国米', '利物浦'), ('巴黎', '多特'),
                 ('阿森纳', '拜仁'), ('皇马', '曼城'), ('巴萨', '巴黎'), ('尤文', '切尔西')],
        '欧联': [('罗马', '勒沃库森'), ('曼联', ('塞维利亚')), ('尤文', '勒沃库森'), ('国米', ('法兰克福'))],
        '荷甲': [('阿贾克斯', '埃因霍温'), ('费耶诺德', '阿尔克马尔'), ('PSV', 'AZ')],
    }

    teams_list = teams_db.get(league, teams_db['英超'])
    idx = (int(period[-3:]) + match_index) % len(teams_list)
    return teams_list[idx]


def simulate_match_result(home_team: str, away_team: str, league: str,
                          period: str, match_index: int,
                          use_random=True, seed=None) -> dict:
    """
    模拟比赛结果（用于无真实数据时的演示）
    真实场景对接 https://datachain.500.com/sfc/
    """
    import random
    if seed:
        random.seed(seed + int(period) * 100 + match_index)

    # 主场优势系数
    league_home = {'英超': 1.25, '西甲': 1.15, '意甲': 1.20, '德甲': 1.22,
                   '法甲': 1.12, '欧冠': 1.10, '欧联': 1.08, '默认': 1.15}
    home_boost = league_home.get(league, 1.15)

    # 基础胜率（根据主客队实力差）
    base_home_win = 0.35 * home_boost
    base_draw = 0.28
    base_away_win = 1 - base_home_win - base_draw

    # 加入随机性
    if use_random:
        base_home_win += random.uniform(-0.08, 0.12)
        base_draw += random.uniform(-0.05, 0.05)
        base_away_win = max(0.15, 1 - base_home_win - base_draw)

    # 生成进球
    r = random.random()
    if r < base_home_win:
        home_goals = random.choices([1, 2, 3, 4], weights=[0.45, 0.30, 0.18, 0.07])[0]
        away_goals = random.choices([0, 1, 2], weights=[0.55, 0.35, 0.10])[0]
        result = 'win'
    elif r < base_home_win + base_draw:
        home_goals = random.choices([0, 1, 2], weights=[0.50, 0.40, 0.10])[0]
        away_goals = home_goals
        result = 'draw'
    else:
        away_goals = random.choices([1, 2, 3], weights=[0.50, 0.35, 0.15])[0]
        home_goals = random.choices([0, 1, 2], weights=[0.55, 0.35, 0.10])[0]
        result = 'lose'

    # 模拟赔率
    odds = {
        'win': round(1 / base_home_win * 0.92 + random.uniform(-0.05, 0.05), 2),
        'draw': round(1 / base_draw * 0.92 + random.uniform(-0.05, 0.05), 2),
        'lose': round(1 / base_away_win * 0.92 + random.uniform(-0.05, 0.05), 2),
    }

    return {
        'home_team': home_team,
        'away_team': away_team,
        'home_goals': home_goals,
        'away_goals': away_goals,
        'result': result,
        'odds': odds,
        'result_code': {'win': '3', 'draw': '1', 'lose': '0'}[result],
    }


def generate_period_data(period: str, year: int = None) -> dict:
    """生成某一期的完整14场比赛数据"""
    data = {
        'period': period,
        'year': year or 2000 + int(period[:2]),
        'matches': []
    }

    for i in range(14):
        league = get_league_by_period(period, i)
        home, away = get_match_teams(period, i, league)
        match_result = simulate_match_result(home, away, league, period, i)

        # 生成比赛时间（每周六/周日）
        base_date = datetime(2020, 1, 1)
        days_offset = (int(period[-3:]) - 1) * 3 + i * 1
        match_date = base_date + timedelta(days=days_offset)
        match_time = match_date.strftime('%Y-%m-%d 22:00')

        match_data = {
            'match_id': f'{period}-{i+1:02d}',
            'period': period,
            'match_index': i + 1,
            'home_team': match_result['home_team'],
            'away_team': match_result['away_team'],
            'league': league,
            'match_time': match_time,
            'home_goals': match_result['home_goals'],
            'away_goals': match_result['away_goals'],
            'result': match_result['result'],
            'result_code': match_result['result_code'],
            'odds': match_result['odds'],
            # 以下为预测所需特征（模拟）
            'recent_form': {
                'home': [round(random.uniform(0.3, 1.0), 2) for _ in range(5)],
                'away': [round(random.uniform(0.3, 1.0), 2) for _ in range(5)],
            },
            'home_stats': {
                'win_rate': round(random.uniform(0.35, 0.75), 3),
                'goals_avg': round(random.uniform(1.0, 2.5), 2),
                'goals_conceded': round(random.uniform(0.8, 2.0), 2),
            },
            'away_stats': {
                'win_rate': round(random.uniform(0.25, 0.65), 3),
                'goals_avg': round(random.uniform(0.8, 2.2), 2),
                'goals_conceded': round(random.uniform(0.9, 2.2), 2),
            },
            'absentees': {
                'home': random.randint(0, 3),
                'away': random.randint(0, 3),
            },
            'h2h': [
                {'winner': random.choice(['home', 'away', 'draw'])}
                for _ in range(random.randint(3, 8))
            ],
            'schedule': {
                'home_rest_days': random.randint(3, 14),
                'away_rest_days': random.randint(3, 14),
            },
            'weather': {
                'temperature': random.randint(5, 30),
                'home_referee': round(random.uniform(0.3, 0.7), 2),
            },
        }
        data['matches'].append(match_data)

    return data


def fetch_all_history(years: list = None) -> dict:
    """采集所有历史期数据"""
    if years is None:
        years = [2022, 2023, 2024, 2025, 2026]

    all_data = {}
    for year in years:
        print(f'采集 {year} 年数据...')
        periods = generate_lottery_periods(year)
        for p in periods:
            try:
                all_data[p] = generate_period_data(p, year)
            except Exception as e:
                print(f'  期号 {p} 失败: {e}')

    return all_data


def get_lottery_result_file(year: int, period: str) -> str:
    """获取某期开奖结果（格式化字符串）"""
    return f'第{period}期开奖: 胜平负结果'


if __name__ == '__main__':
    # 测试
    data = generate_period_data('26049', 2026)
    print(json.dumps(data['matches'][0], ensure_ascii=False, indent=2))
