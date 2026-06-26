# -*- coding: utf-8 -*-
import sys
import io

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.db import init_db
from src.fetcher import fetch_news
from src.analyzer import analyze_industry, analyze_stock
from src.reporter import generate_report, generate_stock_report
from datetime import datetime


class StockAnalyst:
    """股票分析器主类"""
    
    def __init__(self):
        self.db = init_db()
        self.log("INFO", "股票分析器初始化完成")
    
    def log(self, status: str, message: str):
        """记录日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status}: {message}")
        self.db.log("stock_analyst", status, message)
    
    def run(self):
        """执行分析流程"""
        self.log("INFO", "开始执行分析任务")
        
        try:
            # 1. 获取新闻
            self.log("INFO", "步骤1: 获取财经新闻")
            news_list = fetch_news()
            self.log("INFO", f"获取到 {len(news_list)} 条新闻")
            
            # 2. 存储新闻到数据库
            self.log("INFO", "步骤2: 存储新闻数据")
            count = self.db.insert_news_batch(news_list)
            self.log("INFO", f"新插入 {count} 条新闻")
            
            # 3. 分析行业趋势
            self.log("INFO", "步骤3: 分析行业趋势")
            trends = analyze_industry(news_list)
            self.log("INFO", f"分析 {len(trends)} 个行业")
            
            # 4. 获取热点股票
            self.log("INFO", "步骤4: 分析热点股票")
            stocks = []
            for trend in trends[:3]:
                companies = trend.get("companies", [])[:2]
                for c in companies:
                    stock = analyze_stock(c.get("code", ""), news_list)
                    if stock not in stocks:
                        stocks.append(stock)
            
            # 5. 生成报告
            self.log("INFO", "步骤5: 生成分析报告")
            report = generate_report(news_list, trends, stocks)
            print("\n" + report)
            
            # 6. 保存所有数据到数据库（长期存储）
            self.log("INFO", "步骤6: 保存数据到数据库")
            
            # 保存行业趋势历史
            self.db.save_industry_trend(trends)
            
            # 保存股票历史行情
            self.db.save_stock_history(stocks)
            
            # 保存股票评分历史
            self.db.save_stock_score(stocks)
            
            # 保存报告
            self.db.save_report("daily", f"日报-{datetime.now().strftime('%Y-%m-%d')}", 
                               report, len(news_list), len(trends), len(stocks))
            
            # 输出统计信息
            stats = self.db.get_statistics()
            self.log("INFO", f"数据统计: 新闻{stats.get('total_news',0)}条, 股票{stats.get('total_stock_records',0)}条, 报告{stats.get('total_reports',0)}份")
            
            self.log("SUCCESS", "分析任务完成")
            
        except Exception as e:
            self.log("ERROR", f"分析任务失败: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.db.close()
    
    def run_once(self):
        """仅运行一次（不存储）"""
        print("=" * 60)
        print("Stock Industry Analysis - Run Once")
        print("=" * 60)
        
        # 获取新闻
        print("\n[Step 1] Fetch Financial News")
        news_list = fetch_news()
        print(f"   Got {len(news_list)} news items")
        
        # 分析行业
        print("\n[Step 2] Analyze Industry Trends")
        trends = analyze_industry(news_list)
        print(f"   Analyzed {len(trends)} industries")
        
        # 分析股票
        print("\n[Step 3] Analyze Hot Stocks")
        stocks = []
        for trend in trends[:3]:
            companies = trend.get("companies", [])[:2]
            for c in companies:
                stock = analyze_stock(c.get("code", ""), news_list)
                if stock not in stocks:
                    stocks.append(stock)
        
        # 生成报告
        print("\n[Step 4] Generate Report")
        report = generate_report(news_list, trends, stocks)
        
        print("\n" + "=" * 60)
        print(report)
        
        return report


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Stock Industry Analysis Tool')
    parser.add_argument('--once', action='store_true', help='Run only once')
    args = parser.parse_args()
    
    analyst = StockAnalyst()
    
    if args.once:
        analyst.run_once()
    else:
        analyst.run()


if __name__ == '__main__':
    main()