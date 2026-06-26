#!/usr/bin/env python3
"""
travel-planner/scripts/packing_list.py
智能 packing 清单生成器
"""

import argparse
import json
import os


def generate_packing_list(destination: str, days: int, activities: list,
                          climate: str = None, gender: str = 'neutral'):
    """Generate a smart packing list based on destination and activities"""
    
    # Climate detection
    climate_map = {
        '东京': 'temperate', '京都': 'temperate', '大阪': 'temperate',
        '巴黎': 'temperate', '伦敦': 'rainy', '冰岛': 'cold',
        '新加坡': 'tropical', '曼谷': 'tropical', '悉尼': 'warm',
        '迪拜': 'hot', '开罗': 'hot', '莫斯科': 'cold',
        '纽约': 'temperate', '洛杉矶': 'warm', '夏威夷': 'tropical',
    }
    
    detected_climate = climate or climate_map.get(destination, 'temperate')
    
    # Base items everyone needs
    base_items = [
        {'category': '证件', 'items': ['护照/身份证', '签证', '机票/车票', '酒店预订确认', '旅行保险单', '紧急联系卡']},
        {'category': '电子设备', 'items': ['手机', '充电器', '移动电源', '转换插头', '耳机', '相机（可选）']},
        {'category': '药品', 'items': ['常用药（感冒/止泻/止痛）', '创可贴', '防晒霜', '驱蚊液']},
        {'category': '洗漱', 'items': ['牙刷/牙膏', '洗发水/沐浴露（小瓶）', '护肤品', '剃须刀']},
    ]
    
    # Clothing based on climate and days
    clothing_items = []
    if detected_climate == 'cold':
        clothing_items = [
            f'保暖外套 x {max(1, days // 3)}',
            f'毛衣/抓绒衣 x {max(2, days // 2)}',
            f'保暖内衣 x {days}',
            f'厚长裤 x {max(2, days // 2)}',
            '手套', '围巾', '帽子',
            '厚袜子 x {}'.format(days + 2),
            '防水靴/雪地靴',
        ]
    elif detected_climate == 'hot':
        clothing_items = [
            f'T恤/背心 x {days + 1}',
            f'短裤/轻薄长裤 x {max(2, days // 2)}',
            '防晒衣/薄外套',
            '凉鞋/透气鞋',
            '遮阳帽', '太阳镜',
            f'内裤 x {days + 2}',
            f'袜子 x {days + 2}',
        ]
    elif detected_climate == 'tropical':
        clothing_items = [
            f'轻薄T恤 x {days + 1}',
            f'短裤/沙滩裤 x {max(3, days // 2)}',
            '泳衣/泳裤',
            '人字拖',
            '防晒衣',
            '遮阳帽', '太阳镜',
            f'内裤 x {days + 2}',
            '速干毛巾',
        ]
    elif detected_climate == 'rainy':
        clothing_items = [
            f'T恤/衬衫 x {days + 1}',
            f'长裤 x {max(2, days // 2)}',
            '防水外套/雨衣',
            '防水鞋/雨靴',
            '折叠伞',
            f'内裤 x {days + 2}',
            f'袜子 x {days + 2}',
            '薄毛衣',
        ]
    else:  # temperate
        clothing_items = [
            f'T恤/衬衫 x {days + 1}',
            f'长裤/牛仔裤 x {max(2, days // 2)}',
            '薄外套/卫衣',
            '舒适步行鞋',
            f'内裤 x {days + 2}',
            f'袜子 x {days + 2}',
        ]
    
    # Activity-specific gear
    activity_gear = {
        '徒步': ['登山鞋', '登山杖', '背包', '水壶', '头灯', '急救包'],
        '潜水': ['潜水证', '水下相机', '防水袋', '速干衣', '珊瑚友好防晒霜'],
        '滑雪': ['滑雪镜', '滑雪手套', '护脸', '滑雪袜', '保暖中层'],
        '露营': ['帐篷（或确认租赁）', '睡袋', '头灯', '多功能刀', '防虫喷雾'],
        '观鲸': ['望远镜', '晕船药', '防水外套', '相机长焦镜头'],
        '温泉': ['泳衣（部分需要）', '速干毛巾', '拖鞋'],
        '摄影': ['三脚架', '备用电池', '存储卡', '镜头清洁布'],
        '商务': ['正装', '皮鞋', '笔记本电脑', '名片'],
    }
    
    activity_items = []
    for act in activities:
        if act in activity_gear:
            activity_items.extend(activity_gear[act])
    
    packing_list = {
        'destination': destination,
        'days': days,
        'climate': detected_climate,
        'activities': activities,
        'categories': base_items + [
            {'category': '衣物', 'items': clothing_items},
            {'category': '活动装备', 'items': activity_items if activity_items else ['无特殊装备']},
        ],
        'tips': [
            '出发前检查证件有效期',
            '液体物品注意航空限制（100ml）',
            '贵重物品随身携带',
            '留一份证件复印件在云端',
        ],
    }
    
    return packing_list


def main():
    parser = argparse.ArgumentParser(description='Generate packing list')
    parser.add_argument('--destination', '-d', required=True, help='Destination')
    parser.add_argument('--days', '-n', type=int, required=True, help='Number of days')
    parser.add_argument('--activities', '-a', help='Comma-separated activities')
    parser.add_argument('--climate', '-c', choices=['cold', 'hot', 'tropical', 'rainy', 'temperate'],
                        help='Override climate detection')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()
    
    activities = [a.strip() for a in args.activities.split(',')] if args.activities else []
    
    packing = generate_packing_list(args.destination, args.days, activities, args.climate)
    
    print(json.dumps(packing, indent=2, ensure_ascii=False))
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(packing, f, indent=2, ensure_ascii=False)
        print(f"\nPacking list saved: {args.output}")


if __name__ == '__main__':
    main()
