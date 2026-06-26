#!/usr/bin/env python3
"""
travel-planner/scripts/itinerary_exporter.py
行程导出为 PDF / Excel / 日历格式
"""

import argparse
import json
import os
from datetime import datetime


def export_text(itinerary: dict, output_path: str):
    """Export as plain text"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"旅行行程: {itinerary['destination']}\n")
        f.write(f"天数: {itinerary['days']}\n")
        f.write(f"出发日期: {itinerary.get('start_date', '未指定')}\n")
        f.write(f"预估总费用: {itinerary['total_estimated_cost']} {itinerary.get('currency', '')}\n")
        f.write("=" * 50 + "\n\n")
        
        for day in itinerary.get('itinerary', []):
            f.write(f"第 {day['day']} 天 - {day['date']}\n")
            f.write(f"预估费用: {day['estimated_cost']}\n")
            f.write("-" * 30 + "\n")
            for activity in day['activities']:
                f.write(f"  {activity['time']} | {activity['name']} ({activity['type']})\n")
                if activity.get('cost'):
                    f.write(f"    费用: {activity['cost']}\n")
                if activity.get('rating'):
                    f.write(f"    评分: {activity['rating']}\n")
            f.write("\n")
    print(f"Text itinerary exported: {output_path}")


def export_csv(itinerary: dict, output_path: str):
    """Export as CSV"""
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Day', 'Date', 'Time', 'Activity', 'Type', 'Duration', 'Cost', 'Rating'])
        
        for day in itinerary.get('itinerary', []):
            for activity in day['activities']:
                writer.writerow([
                    day['day'],
                    day['date'],
                    activity['time'],
                    activity['name'],
                    activity['type'],
                    activity.get('duration', ''),
                    activity.get('cost', ''),
                    activity.get('rating', ''),
                ])
    print(f"CSV itinerary exported: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Export itinerary')
    parser.add_argument('input', help='Input JSON itinerary file')
    parser.add_argument('--format', '-f', choices=['text', 'csv'], default='text',
                        help='Output format')
    parser.add_argument('--output', '-o', required=True, help='Output file')
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        itinerary = json.load(f)
    
    if args.format == 'text':
        export_text(itinerary, args.output)
    elif args.format == 'csv':
        export_csv(itinerary, args.output)


if __name__ == '__main__':
    main()
