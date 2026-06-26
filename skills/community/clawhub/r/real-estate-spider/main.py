#!/usr/bin/env python3
"""
房产中介网站爬虫主程序
"""

import os
import sys
import json
import argparse
from scripts.real_estate_crawler import RealEstateSpider
from config.real_estate_config import CONFIG, USER_AGENTS, DELAY_CONFIG

def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(description='房产中介网站爬虫主程序')
    parser.add_argument('-w', '--website', choices=['anjuke', 'ke', 'lianjia', 'soufun'], default='anjuke', help='目标网站')
    parser.add_argument('-c', '--city', default='北京', help='城市')
    parser.add_argument('-d', '--district', help='区域')
    parser.add_argument('-p', '--pages', type=int, default=1, help='爬取页数')
    parser.add_argument('-o', '--output', default='output/properties.json', help='输出文件')
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'excel'], default='json', help='输出格式')
    parser.add_argument('-m', '--mode', choices=['python', 'agent-browser'], default='python', help='爬取模式')
    parser.add_argument('--proxy', help='使用代理')
    parser.add_argument('--delay', type=float, help='自定义延迟秒数')
    
    args = parser.parse_args()
    
    print(f"=== 房产中介网站爬虫 ===")
    print(f"网站: {args.website} ({CONFIG[args.website]['name']})")
    print(f"城市: {args.city}")
    print(f"区域: {args.district if args.district else '全部'}")
    print(f"页数: {args.pages}")
    print(f"模式: {args.mode}")
    print(f"反爬虫等级: {CONFIG[args.website]['anti_crawler_level']}")
    print(f"提示: {CONFIG[args.website]['anti_crawler_tips']}")
    
    if args.mode == 'python':
        # Python爬虫模式
        print("\n=== Python爬虫模式 ===")
        spider = RealEstateSpider(args.website)
        
        all_properties = []
        all_stats = []
        
        for page in range(1, args.pages + 1):
            print(f"\n正在爬取第 {page} 页...")
            
            result = spider.crawl(args.city, args.district, page)
            
            if result['data']:
                all_properties.extend(result['data'])
                all_stats.append(result['stats'])
                
                print(f"第 {page} 页爬取完成，找到 {len(result['data'])} 个房产")
                print(f"平均总价: {result['stats']['avg_price_total']} 万元")
                print(f"平均单价: {result['stats']['avg_price_per_m2']} 元/㎡")
                print(f"平均面积: {result['stats']['avg_area']} ㎡")
                
                # 保存当前页的数据
                spider.save_json(result, f"output/page_{page}_properties.json")
                
            else:
                print(f"第 {page} 页没有找到数据")
                break
        
        if all_properties:
            # 保存总数据
            spider.save_json({'data': all_properties}, args.output)
            
            # 计算总体统计
            total_stats = spider.calculate_stats(all_properties)
            
            print(f"\n=== 总体统计 ===")
            print(f"总共爬取: {len(all_properties)} 个房产")
            print(f"平均总价: {total_stats['avg_price_total']} 万元")
            print(f"平均单价: {total_stats['avg_price_per_m2']} 元/㎡")
            print(f"平均面积: {total_stats['avg_area']} ㎡")
            
            # 打印前10个房产信息
            print(f"\n=== 前10个房产信息 ===")
            for i, prop in enumerate(all_properties[:10]):
                print(f"{i+1}. {prop.title}")
                print(f"   总价: {prop.price}万元 | 均价: {prop.avg_price}元/㎡")
                print(f"   面积: {prop.area}㎡ | 年代: {prop.age}")
                print(f"   朝向: {prop.orientation} | 装修: {prop.decoration}")
            
        else:
            print("\n=== 没有找到房产信息 ===")
            
    elif args.mode == 'agent-browser':
        # agent-browser模式
        print("\n=== agent-browser模式 ===")
        print("执行Shell脚本进行浏览器自动化爬取")
        
        script_path = os.path.join(os.path.dirname(__file__), "scripts/bypass_real_estate.sh")
        
        # 构建命令
        command = f"bash {script_path}"
        
        print(f"执行命令: {command}")
        
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("agent-browser脚本执行成功")
            print(f"输出: {result.stdout}")
        else:
            print("agent-browser脚本执行失败")
            print(f"错误: {result.stderr}")
            
    print("\n=== 爬虫完成 ===")
    print(f"数据保存在: {args.output}")
    print(f"后续可以使用数据分析脚本处理数据")

if __name__ == "__main__":
    main()