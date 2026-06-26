#!/usr/bin/env python3
"""
travel-planner/scripts/plan_trip.py
完整行程规划生成器
"""

import argparse
import json
import os
import random
from datetime import datetime, timedelta


def load_attractions(city: str):
    """Load attractions for a city from the knowledge base"""
    attractions_db = {
        '东京': [
            {'name': '浅草寺', 'type': '历史', 'duration': 2, 'cost': 0, 'rating': 4.5},
            {'name': '东京塔', 'type': '地标', 'duration': 2, 'cost': 2800, 'rating': 4.3},
            {'name': '涩谷十字路口', 'type': '地标', 'duration': 1, 'cost': 0, 'rating': 4.2},
            {'name': '明治神宫', 'type': '自然/历史', 'duration': 2, 'cost': 0, 'rating': 4.6},
            {'name': '秋叶原', 'type': '购物', 'duration': 3, 'cost': 0, 'rating': 4.4},
            {'name': '银座', 'type': '购物/美食', 'duration': 3, 'cost': 0, 'rating': 4.3},
            {'name': '筑地市场', 'type': '美食', 'duration': 2, 'cost': 3000, 'rating': 4.5},
            {'name': '上野公园', 'type': '自然', 'duration': 3, 'cost': 0, 'rating': 4.4},
            {'name': '东京国立博物馆', 'type': '历史', 'duration': 3, 'cost': 1000, 'rating': 4.5},
            {'name': '新宿御苑', 'type': '自然', 'duration': 2, 'cost': 500, 'rating': 4.4},
        ],
        '京都': [
            {'name': '金阁寺', 'type': '寺庙', 'duration': 2, 'cost': 400, 'rating': 4.5},
            {'name': '清水寺', 'type': '寺庙', 'duration': 2, 'cost': 400, 'rating': 4.6},
            {'name': '伏见稻荷大社', 'type': '寺庙', 'duration': 3, 'cost': 0, 'rating': 4.7},
            {'name': '岚山竹林', 'type': '自然', 'duration': 3, 'cost': 0, 'rating': 4.5},
            {'name': '二条城', 'type': '历史', 'duration': 2, 'cost': 600, 'rating': 4.4},
            {'name': '锦市场', 'type': '美食', 'duration': 2, 'cost': 2000, 'rating': 4.3},
            {'name': '祇园', 'type': '历史/文化', 'duration': 2, 'cost': 0, 'rating': 4.4},
        ],
        '巴黎': [
            {'name': '埃菲尔铁塔', 'type': '地标', 'duration': 3, 'cost': 25, 'rating': 4.5},
            {'name': '卢浮宫', 'type': '历史/艺术', 'duration': 4, 'cost': 17, 'rating': 4.7},
            {'name': '圣母院', 'type': '历史', 'duration': 1.5, 'cost': 0, 'rating': 4.4},
            {'name': '蒙马特高地', 'type': '地标/文化', 'duration': 3, 'cost': 0, 'rating': 4.3},
            {'name': '塞纳河游船', 'type': '体验', 'duration': 1.5, 'cost': 15, 'rating': 4.2},
            {'name': '香榭丽舍大街', 'type': '购物', 'duration': 2, 'cost': 0, 'rating': 4.1},
            {'name': '凡尔赛宫', 'type': '历史', 'duration': 4, 'cost': 20, 'rating': 4.6},
        ],
        '冰岛': [
            {'name': '蓝湖温泉', 'type': '自然/体验', 'duration': 3, 'cost': 70, 'rating': 4.4},
            {'name': '黄金圈', 'type': '自然', 'duration': 6, 'cost': 0, 'rating': 4.6},
            {'name': '黑沙滩', 'type': '自然', 'duration': 2, 'cost': 0, 'rating': 4.5},
            {'name': '冰川徒步', 'type': '冒险', 'duration': 4, 'cost': 120, 'rating': 4.7},
            {'name': '极光狩猎', 'type': '自然', 'duration': 4, 'cost': 100, 'rating': 4.8},
            {'name': '观鲸', 'type': '自然', 'duration': 3, 'cost': 85, 'rating': 4.3},
        ],
    }
    return attractions_db.get(city, [])


def filter_by_interests(attractions: list, interests: list):
    """Filter attractions by interests"""
    if not interests:
        return attractions
    
    filtered = []
    for a in attractions:
        a_types = [t.strip().lower() for t in a['type'].split('/')]
        for interest in interests:
            if interest.lower() in a_types or any(interest.lower() in t for t in a_types):
                filtered.append(a)
                break
    
    return filtered if filtered else attractions


def generate_itinerary(city: str, days: int, interests: list, start_date: str = None):
    attractions = load_attractions(city)
    if not attractions:
        return {'error': f'No attractions data for {city}'}
    
    filtered = filter_by_interests(attractions, interests)
    sorted_attractions = sorted(filtered, key=lambda x: x['rating'], reverse=True)
    
    # Generate daily schedule
    itinerary = []
    date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else datetime.now()
    
    for day in range(1, days + 1):
        day_plan = {
            'day': day,
            'date': (date + timedelta(days=day-1)).strftime('%Y-%m-%d'),
            'activities': [],
            'estimated_cost': 0,
            'total_duration': 0,
        }
        
        # Morning activity
        if sorted_attractions:
            morning = sorted_attractions.pop(0)
            day_plan['activities'].append({
                'time': '09:00-12:00',
                'name': morning['name'],
                'type': morning['type'],
                'duration': morning['duration'],
                'cost': morning['cost'],
                'rating': morning['rating'],
            })
            day_plan['estimated_cost'] += morning['cost']
            day_plan['total_duration'] += morning['duration']
        
        # Lunch break
        day_plan['activities'].append({
            'time': '12:00-13:30',
            'name': '午餐',
            'type': '餐饮',
            'duration': 1.5,
            'cost': 30,
            'rating': None,
        })
        day_plan['estimated_cost'] += 30
        
        # Afternoon activity
        if sorted_attractions:
            afternoon = sorted_attractions.pop(0)
            day_plan['activities'].append({
                'time': '14:00-17:00',
                'name': afternoon['name'],
                'type': afternoon['type'],
                'duration': afternoon['duration'],
                'cost': afternoon['cost'],
                'rating': afternoon['rating'],
            })
            day_plan['estimated_cost'] += afternoon['cost']
            day_plan['total_duration'] += afternoon['duration']
        
        # Dinner
        day_plan['activities'].append({
            'time': '18:00-20:00',
            'name': '晚餐',
            'type': '餐饮',
            'duration': 2,
            'cost': 40,
            'rating': None,
        })
        day_plan['estimated_cost'] += 40
        
        itinerary.append(day_plan)
    
    total_cost = sum(d['estimated_cost'] for d in itinerary)
    
    return {
        'destination': city,
        'days': days,
        'interests': interests,
        'start_date': (date).strftime('%Y-%m-%d') if start_date else None,
        'itinerary': itinerary,
        'total_estimated_cost': total_cost,
        'currency': 'USD' if city == '巴黎' else 'JPY' if city in ['东京', '京都'] else 'ISK',
    }


def main():
    parser = argparse.ArgumentParser(description='Generate travel itinerary')
    parser.add_argument('--destination', '-d', required=True, help='Destination city')
    parser.add_argument('--days', '-n', type=int, required=True, help='Number of days')
    parser.add_argument('--interests', '-i', help='Comma-separated interests (e.g. 美食,历史,自然)')
    parser.add_argument('--start-date', '-s', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()
    
    interests = [i.strip() for i in args.interests.split(',')] if args.interests else []
    
    plan = generate_itinerary(args.destination, args.days, interests, args.start_date)
    
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"\nItinerary saved: {args.output}")


if __name__ == '__main__':
    main()
