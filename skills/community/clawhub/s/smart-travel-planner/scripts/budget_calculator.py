#!/usr/bin/env python3
"""
travel-planner/scripts/budget_calculator.py
旅行预算计算与管理
"""

import argparse
import json
import os


def calculate_budget(destination: str, days: int, travelers: int = 1,
                     accommodation_level: str = 'mid', food_level: str = 'mid'):
    """Calculate estimated travel budget"""
    
    # Base cost templates per day per person
    templates = {
        '东京': {
            'accommodation': {'budget': 4000, 'mid': 8000, 'luxury': 20000},  # JPY
            'food': {'budget': 3000, 'mid': 6000, 'luxury': 15000},
            'transport': 1000,
            'attractions': 3000,
            'shopping': 5000,
        },
        '京都': {
            'accommodation': {'budget': 3500, 'mid': 7000, 'luxury': 18000},
            'food': {'budget': 2500, 'mid': 5000, 'luxury': 12000},
            'transport': 800,
            'attractions': 2500,
            'shopping': 4000,
        },
        '巴黎': {
            'accommodation': {'budget': 50, 'mid': 120, 'luxury': 400},  # EUR
            'food': {'budget': 30, 'mid': 60, 'luxury': 150},
            'transport': 15,
            'attractions': 30,
            'shopping': 50,
        },
        '冰岛': {
            'accommodation': {'budget': 80, 'mid': 150, 'luxury': 400},  # EUR/USD
            'food': {'budget': 40, 'mid': 80, 'luxury': 200},
            'transport': 50,
            'attractions': 80,
            'shopping': 30,
        },
    }
    
    template = templates.get(destination, templates['东京'])
    
    # Calculate per day per person
    acc_cost = template['accommodation'][accommodation_level]
    food_cost = template['food'][food_level]
    transport = template['transport']
    attractions = template['attractions']
    shopping = template['shopping']
    
    daily_per_person = acc_cost + food_cost + transport + attractions + shopping
    
    # Total for all travelers and days
    total = daily_per_person * days * travelers
    
    # Add international flight estimate (per person)
    flight_estimates = {
        '东京': 5000,  # CNY
        '京都': 4500,
        '巴黎': 6000,
        '冰岛': 8000,
    }
    flight_cost = flight_estimates.get(destination, 5000) * travelers
    
    total_with_flight = total + flight_cost
    
    budget = {
        'destination': destination,
        'days': days,
        'travelers': travelers,
        'accommodation_level': accommodation_level,
        'food_level': food_level,
        'breakdown': {
            'flight': flight_cost,
            'accommodation': acc_cost * days * travelers,
            'food': food_cost * days * travelers,
            'local_transport': transport * days * travelers,
            'attractions': attractions * days * travelers,
            'shopping_misc': shopping * days * travelers,
        },
        'daily_per_person': daily_per_person,
        'total_without_flight': total,
        'total_with_flight': total_with_flight,
        'currency': 'CNY',
    }
    
    return budget


def main():
    parser = argparse.ArgumentParser(description='Calculate travel budget')
    parser.add_argument('--destination', '-d', required=True, help='Destination')
    parser.add_argument('--days', '-n', type=int, required=True, help='Number of days')
    parser.add_argument('--travelers', '-t', type=int, default=1, help='Number of travelers')
    parser.add_argument('--accommodation', '-a', choices=['budget', 'mid', 'luxury'],
                        default='mid', help='Accommodation level')
    parser.add_argument('--food', '-f', choices=['budget', 'mid', 'luxury'],
                        default='mid', help='Food level')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()
    
    budget = calculate_budget(args.destination, args.days, args.travelers,
                             args.accommodation, args.food)
    
    print(json.dumps(budget, indent=2, ensure_ascii=False))
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(budget, f, indent=2, ensure_ascii=False)
        print(f"\nBudget saved: {args.output}")


if __name__ == '__main__':
    main()
