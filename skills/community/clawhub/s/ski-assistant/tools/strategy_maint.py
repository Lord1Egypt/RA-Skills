#!/usr/bin/env python3
"""
search_strategies.json 维护工具

用法:
  python tools/strategy_maint.py check          # 检查数据健康度
  python tools/strategy_maint.py verify         # 验证官方渠道名称（手动）
  python tools/strategy_maint.py report          # 生成维护报告
  python tools/strategy_maint.py add-channel     # 添加官方渠道
  python tools/strategy_maint.py review          # 季度复核流程

安全说明:
  - 仅读写本地 JSON 文件
  - 不执行任何网络请求
  - 不修改 resorts_db.json
"""

import json
import os
import sys
from datetime import datetime, timedelta
from collections import Counter

STRATEGY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'search_strategies.json')
RESORTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'resorts_db.json')


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def check_health():
    """检查数据健康度"""
    strategies = load_json(STRATEGY_FILE)
    resorts = load_json(RESORTS_FILE)

    print('=== Search Strategies 健康度检查 ===\n')

    # 1. region_strategies 覆盖度
    rs = strategies['region_strategies']
    total_resorts = len([k for k in resorts if not k.startswith('_')])

    # 构建 region -> resort 映射
    resort_regions = Counter()
    for name, info in resorts.items():
        if name.startswith('_'):
            continue
        region = info.get('region', 'Unknown')
        resort_regions[region] += 1

    # 区域映射
    region_mapping = {
        '崇礼': ['河北'],
        '东北': ['吉林', '黑龙江', '辽宁'],
        '新疆': ['新疆'],
        '北京': ['北京'],
        '国内其他': ['山东', '河南', '山西', '湖北', '四川', '江苏', '浙江', '安徽', '湖南', '内蒙古', '陕西', '广东', '云南', '贵州', '福建', '重庆', '天津', '江西', '广西', '海南', '青海', '宁夏', '上海', '甘肃'],
        '日本': ['日本', '长野县', '北海道', '岩手县', '新潟县', '群马县', '长野', '青森县', '山形县', '秋田县'],
        '韩国': ['韩国', '江原道·平昌', '江原道·旌善', '江原道', '全罗北道', '京畿道', '江原道·洪川'],
        '欧洲': ['法国', '瑞士', '奥地利', '意大利', '安道尔', '德国·巴伐利亚', '法国·萨瓦', '法国·上萨瓦', '瑞士·格劳宾登州', '瑞士·瓦莱', '奥地利·蒂罗尔', '意大利·特伦蒂诺', '法国·萨瓦省', '奥地利·蒂罗尔州', '法国·伊泽尔', '法国·上阿尔卑斯省', '法国·上萨瓦省', '奥地利·萨尔茨堡州', '芬兰', '西班牙', '瑞士·格劳宾登', '瑞士·上瓦尔登', '奥地利·萨尔茨堡', '法国·上阿尔卑斯', '瑞士·伯尔尼', '瑞士·乌里', '法国·伊泽尔省', '瑞士·上瓦尔登州', '瑞士·施维克州', '奥地利·施蒂利亚州', '意大利·伦巴第', '斯洛文尼亚·戈伦尼斯卡', '斯洛伐克·日利纳州', '捷克·赫拉德茨克拉洛韦州', '罗马尼亚·布拉索夫县', '西班牙·加泰罗尼亚', '意大利·瓦莱达奥斯塔', '法国·杜省', '瑞士·瓦莱州', '瑞士·伯尔尼州', '瑞士·提契诺州', '奥地利·福拉尔贝格州', '意大利·威尼托', '意大利·皮埃蒙特'],
        '北美': ['美国', '加拿大', '美国·科罗拉多', '科罗拉多州', '加拿大·BC', '美国·加州', '加拿大·阿尔伯塔', '加利福尼亚州', '佛蒙特州', '犹他州', '不列颠哥伦比亚省', '魁北克省', '爱达荷州', '艾伯塔省', '美国·佛蒙特', '加拿大·魁北克', '美国·加州/内华达', '美国·犹他', '美国·怀俄明州', '美国·蒙大拿州', '美国·犹他州'],
        '南半球': ['新西兰', '澳大利亚', '阿根廷', '智利', '新西兰·瓦纳卡', '新西兰·皇后镇', '澳大利亚·新南威尔士', '圣地亚哥大区', '瓦尔帕莱索大区', '内格罗河省', '门多萨省']
    }

    covered = 0
    for strategy_name, mapped_regions in region_mapping.items():
        count = sum(resort_regions.get(r, 0) for r in mapped_regions)
        covered += count
        status = rs.get(strategy_name, {}).get('priority', 'unknown')
        print(f'  {strategy_name}: {count} resorts (priority: {status})')

    print(f'\n  总覆盖: {covered}/{total_resorts} ({covered/total_resorts*100:.1f}%)')
    print(f'  未覆盖: {total_resorts - covered} (由 default 策略兜底)')

    # 2. official_channels 复核状态
    oc = strategies['official_channels']
    meta = {k: v for k, v in oc.items() if k.startswith('_')}
    channels = {k: v for k, v in oc.items() if not k.startswith('_')}

    verification_date = meta.get('_verification_status', 'unknown')
    print(f'\n  官方渠道: {len(channels)} 个')
    print(f'  上次复核: {verification_date}')

    # 计算是否超期
    if 'next_review_' in verification_date:
        next_review = verification_date.split('next_review_')[1]
        try:
            review_date = datetime.strptime(next_review, '%Y-%m-%d')
            days_until = (review_date - datetime.now()).days
            if days_until < 0:
                print(f'  状态: 超期 {-days_until} 天，需要复核')
            elif days_until < 30:
                print(f'  状态: {days_until} 天后到期，建议提前复核')
            else:
                print(f'  状态: 正常 ({days_until} 天后复核)')
        except:
            print(f'  状态: 无法解析复核日期')

    # 3. 必填字段检查
    print(f'\n  必填字段检查:')
    required_fields = ['description', 'flyai_params', 'websearch_keywords', 'priority', 'season']
    issues = []
    for region, strategy in rs.items():
        missing = [f for f in required_fields if f not in strategy]
        if missing:
            issues.append(f'{region}: missing {missing}')

    if issues:
        for issue in issues:
            print(f'    FAIL: {issue}')
    else:
        print(f'    PASS: 所有 region_strategies 包含必填字段')

    # 4. 关键词质量
    print(f'\n  关键词质量:')
    empty_keywords = 0
    placeholder_count = 0
    for region, strategy in rs.items():
        for kw_type in ['websearch_keywords', 'fliggy_keywords']:
            kws = strategy.get(kw_type, [])
            for kw in kws:
                if not kw.strip():
                    empty_keywords += 1
                if '{' in kw:
                    placeholder_count += 1

    if empty_keywords > 0:
        print(f'    WARN: {empty_keywords} 个空关键词')
    else:
        print(f'    PASS: 无空关键词')
    print(f'    NOTE: {placeholder_count} 个占位符关键词（正常）')

    print(f'\n=== 检查完成 ===')


def generate_report():
    """生成维护报告"""
    strategies = load_json(STRATEGY_FILE)
    resorts = load_json(RESORTS_FILE)

    report = []
    report.append('# Search Strategies 维护报告')
    report.append(f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')

    rs = strategies['region_strategies']
    total_resorts = len([k for k in resorts if not k.startswith('_')])

    report.append('## 1. 区域策略覆盖')
    for region, strategy in sorted(rs.items(), key=lambda x: x[1].get('resort_count', 0), reverse=True):
        count = strategy.get('resort_count', 0)
        priority = strategy.get('priority', 'unknown')
        season = strategy.get('season', 'unknown')
        report.append(f'- **{region}**: {count} resorts, priority={priority}, season={season}')

    oc = {k: v for k, v in strategies['official_channels'].items() if not k.startswith('_')}
    report.append(f'\n## 2. 官方渠道 ({len(oc)} 个)')
    for name, info in sorted(oc.items()):
        verified = '✅' if info.get('verified') else '⏳'
        report.append(f'- {verified} {name}: {info.get("note", "")}')

    report.append(f'\n## 3. 维护建议')
    report.append('- region_strategies: 无需定期更新，事件驱动调整')
    report.append('- official_channels: 季度复核微信公众号名称')
    report.append('- fliggy_platform: 每年雪季前（9月）验证一次')

    report_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'strategies_maintenance_report.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f'报告已生成: {report_path}')


def add_channel():
    """交互式添加官方渠道"""
    print('添加官方渠道（输入空值取消）:')
    name = input('雪场名称: ').strip()
    if not name:
        return

    wechat_name = input('微信公众号名称: ').strip()
    if not wechat_name:
        print('取消：微信公众号名称不能为空')
        return

    note = input('备注（可选）: ').strip()

    strategies = load_json(STRATEGY_FILE)
    strategies['official_channels'][name] = {
        'type': 'wechat',
        'name': name,
        'value': f'{wechat_name} (WeChat MP)',
        'url': '',
        'verified': False,
        'note': note or f'微信搜索公众号：{wechat_name}'
    }

    save_json(STRATEGY_FILE, strategies)
    print(f'已添加: {name} -> {wechat_name}')


def review():
    """季度复核流程"""
    strategies = load_json(STRATEGY_FILE)
    oc = strategies['official_channels']
    channels = {k: v for k, v in oc.items() if not k.startswith('_')}

    print('=== 季度复核官方渠道 ===\n')
    print('请在微信中搜索以下公众号，确认名称是否有效:\n')

    for i, (name, info) in enumerate(channels.items(), 1):
        expected = info.get('note', '')
        print(f'{i:2d}. {name}')
        print(f'    预期: {expected}')
        confirm = input(f'    有效? (y/n/skip): ').strip().lower()

        if confirm == 'n':
            new_name = input(f'    新名称: ').strip()
            if new_name:
                info['value'] = f'{new_name} (WeChat MP)'
                info['note'] = f'微信搜索公众号：{new_name}'
                info['verified'] = True
                info['last_reviewed'] = datetime.now().strftime('%Y-%m-%d')
                print(f'    已更新: {new_name}')
            else:
                print(f'    跳过')
        elif confirm == 'y':
            info['verified'] = True
            info['last_reviewed'] = datetime.now().strftime('%Y-%m-%d')
            print(f'    已标记为已验证')
        else:
            print(f'    跳过')
        print()

    # 更新复核日期
    next_review = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    oc['_verification_status'] = f'reviewed_{datetime.now().strftime("%Y-%m-%d")}_next_review_{next_review}'

    save_json(STRATEGY_FILE, strategies)
    print(f'\n复核完成！下次复核日期: {next_review}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    cmds = {
        'check': check_health,
        'report': generate_report,
        'add-channel': add_channel,
        'review': review,
    }

    if cmd in cmds:
        cmds[cmd]()
    elif cmd == 'verify':
        print('验证需要手动在微信中搜索公众号名称')
        print('请运行: python tools/strategy_maint.py review')
    else:
        print(f'未知命令: {cmd}')
        print(__doc__)
        sys.exit(1)
