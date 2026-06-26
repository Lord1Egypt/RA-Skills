"""
销量推断使用示例

演示如何使用 sales_inference 模块分析市场数据
"""

import sys
import json
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from cars.sales_inference import (
    analyze_market_without_api,
    calculate_market_popularity,
    analyze_price_distribution,
    rank_by_inferred_popularity,
)


def example_1_basic_analysis():
    """示例 1：基础市场分析"""
    print("=" * 60)
    print("示例 1：基础市场分析")
    print("=" * 60)
    
    # 模拟搜索结果
    search_results = {
        "ok": True,
        "total": 45,
        "items": [
            {"price": 9500, "title": "2018 Toyota Yaris", "is_trade": True, "age": "3 days"},
            {"price": 8800, "title": "2017 Toyota Yaris", "is_trade": False, "age": "1 week"},
            {"price": 10200, "title": "2019 Toyota Yaris", "is_trade": True, "age": "5 hours"},
            {"price": 7500, "title": "2016 Toyota Yaris", "is_trade": False, "age": "2 months"},
            {"price": 9200, "title": "2018 Toyota Yaris", "is_trade": True, "age": "10 days"},
        ]
    }
    
    # 分析
    analysis = analyze_market_without_api(
        make="Toyota",
        model="Yaris",
        search_results=search_results,
        budget=10000,
    )
    
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    print()


def example_2_popularity_scoring():
    """示例 2：热度评分"""
    print("=" * 60)
    print("示例 2：市场热度推断")
    print("=" * 60)
    
    # 场景 A：热门车型
    hot_car = calculate_market_popularity(
        make="Honda",
        model="Jazz",
        total_listings=67,
        price_range=(6500, 11000),
        avg_price=8800,
        budget=10000,
    )
    
    print("🔥 热门车型 - Honda Jazz:")
    print(f"  热度评分: {hot_car['popularity_score']}/100")
    print(f"  供应水平: {hot_car['supply_description']} ({hot_car['total_listings']} 辆)")
    print(f"  销售速度: {hot_car['speed_description']}")
    print(f"  预计售出: {hot_car['estimated_days_to_sell']}")
    print("\n  建议:")
    for rec in hot_car['recommendations']:
        print(f"    {rec}")
    print()
    
    # 场景 B：冷门车型
    cold_car = calculate_market_popularity(
        make="Citroen",
        model="C3",
        total_listings=8,
        price_range=(7000, 9500),
        avg_price=8300,
        budget=10000,
    )
    
    print("❄️  冷门车型 - Citroen C3:")
    print(f"  热度评分: {cold_car['popularity_score']}/100")
    print(f"  供应水平: {cold_car['supply_description']} ({cold_car['total_listings']} 辆)")
    print(f"  销售速度: {cold_car['speed_description']}")
    print(f"  预计售出: {cold_car['estimated_days_to_sell']}")
    print("\n  建议:")
    for rec in cold_car['recommendations']:
        print(f"    {rec}")
    print()


def example_3_price_analysis():
    """示例 3：价格分析"""
    print("=" * 60)
    print("示例 3：价格分布分析")
    print("=" * 60)
    
    items = [
        {"price": 7500},
        {"price": 8200},
        {"price": 8500},
        {"price": 8800},
        {"price": 9000},
        {"price": 9200},
        {"price": 9500},
        {"price": 9800},
        {"price": 10200},
        {"price": 11000},
    ]
    
    price_analysis = analyze_price_distribution(items)
    
    print(f"价格范围: £{price_analysis['min_price']:,} - £{price_analysis['max_price']:,}")
    print(f"平均价格: £{price_analysis['avg_price']:,}")
    print(f"中位数价格: £{price_analysis['median_price']:,}")
    print(f"Q1 价格（25%分位）: £{price_analysis['q1_price']:,}")
    print(f"Q3 价格（75%分位）: £{price_analysis['q3_price']:,}")
    print(f"\n好交易数量（低于Q1）: {price_analysis['good_deals_count']} 辆")
    print(f"好交易阈值: £{price_analysis['good_deals_threshold']:,} 以下")
    print()


def example_4_ranking():
    """示例 4：智能排序"""
    print("=" * 60)
    print("示例 4：基于推断热度排序")
    print("=" * 60)
    
    items = [
        {
            "title": "2018 Honda Jazz 1.3 SE",
            "price": 8500,
            "is_trade": True,
            "age": "2 days",
            "image_url": "https://example.com/image.jpg",
        },
        {
            "title": "2017 Honda Jazz 1.3 EX",
            "price": 7800,
            "is_trade": False,
            "age": "3 weeks",
            "image_url": "https://example.com/image2.jpg",
        },
        {
            "title": "2019 Honda Jazz 1.5 Sport",
            "price": 10500,
            "is_trade": True,
            "age": "5 hours",
            "image_url": "https://example.com/image3.jpg",
        },
        {
            "title": "2016 Honda Jazz 1.3 S",
            "price": 6500,
            "is_trade": False,
            "age": "2 months",
            "image_url": None,
        },
    ]
    
    ranked = rank_by_inferred_popularity(items, budget=10000)
    
    print("排序结果（按推断热度）:\n")
    for i, item in enumerate(ranked, 1):
        print(f"{i}. {item['title']}")
        print(f"   💷 价格: £{item['price']:,}")
        print(f"   📊 推断评分: {item['inferred_popularity_score']}/100")
        print(f"   🏪 卖家: {'Trade' if item.get('is_trade') else 'Private'}")
        print(f"   📅 上架: {item.get('age', 'Unknown')}")
        print()


def example_5_compare_models():
    """示例 5：对比多个车型"""
    print("=" * 60)
    print("示例 5：车型对比（基于市场数据）")
    print("=" * 60)
    
    models_data = [
        {"make": "Toyota", "model": "Yaris", "listings": 45, "avg_price": 9200},
        {"make": "Honda", "model": "Jazz", "listings": 34, "avg_price": 8800},
        {"make": "Mazda", "model": "2", "listings": 18, "avg_price": 9500},
        {"make": "Ford", "model": "Fiesta", "listings": 67, "avg_price": 8500},
    ]
    
    budget = 10000
    
    for data in models_data:
        popularity = calculate_market_popularity(
            make=data["make"],
            model=data["model"],
            total_listings=data["listings"],
            price_range=(data["avg_price"] - 1500, data["avg_price"] + 1500),
            avg_price=data["avg_price"],
            budget=budget,
        )
        
        print(f"\n{data['make']} {data['model']}:")
        print(f"  📊 热度评分: {popularity['popularity_score']}/100")
        print(f"  🚗 供应量: {data['listings']} 辆")
        print(f"  💷 平均价格: £{data['avg_price']:,}")
        print(f"  ⚡ 销售速度: {popularity['sales_speed']}")
        print(f"  📅 预计售出: {popularity['estimated_days_to_sell']}")
    
    print("\n" + "=" * 60)
    print("推荐排名（综合评分）:")
    print("=" * 60)
    
    # 排序
    models_sorted = sorted(
        [
            {
                "model": f"{d['make']} {d['model']}",
                "score": calculate_market_popularity(
                    d["make"], d["model"], d["listings"],
                    (d["avg_price"] - 1500, d["avg_price"] + 1500),
                    d["avg_price"], budget
                )["popularity_score"]
            }
            for d in models_data
        ],
        key=lambda x: x["score"],
        reverse=True
    )
    
    for i, model in enumerate(models_sorted, 1):
        print(f"{i}. {model['model']} - 评分: {model['score']}/100")


if __name__ == "__main__":
    print("\n🎯 销量推断模块 - 使用示例\n")
    
    example_1_basic_analysis()
    input("按 Enter 继续...")
    
    example_2_popularity_scoring()
    input("按 Enter 继续...")
    
    example_3_price_analysis()
    input("按 Enter 继续...")
    
    example_4_ranking()
    input("按 Enter 继续...")
    
    example_5_compare_models()
    
    print("\n✅ 所有示例完成！")
