#!/usr/bin/env python3
"""
Theta简化评分系统 - 临时版本
使用可用数据（换手率、成交额、涨幅）进行评分
适用于主力资金和连板数数据缺失的情况
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/data/real_stock_data.db"

class SimplifiedThetaScorer:
    """简化版Theta评分器"""
    
    def __init__(self):
        self.db_path = DB_PATH
        
    def calculate_turnover_score(self, turnover_rate):
        """
        换手率评分 (30分)
        最佳区间: 5-10% → 30分
        可接受: 3-5% 或 10-15% → 20分
        过低或过高 → 0分
        """
        if pd.isna(turnover_rate):
            return 0
        
        if 5 <= turnover_rate <= 10:
            return 30
        elif (3 <= turnover_rate < 5) or (10 < turnover_rate <= 15):
            return 20
        else:
            return 0
    
    def calculate_amount_rank_score(self, amount_rank):
        """
        成交额排名评分 (30分)
        排名越高，资金关注度越高
        """
        if pd.isna(amount_rank):
            return 0
        
        if amount_rank >= 0.9:  # 前10%
            return 30
        elif amount_rank >= 0.7:  # 前30%
            return 25
        elif amount_rank >= 0.5:  # 前50%
            return 20
        elif amount_rank >= 0.3:  # 前70%
            return 15
        else:
            return 10
    
    def calculate_change_rank_score(self, change_rank):
        """
        涨幅排名评分 (20分)
        排名越高，动量越强
        """
        if pd.isna(change_rank):
            return 0
        
        if change_rank >= 0.9:  # 前10%
            return 20
        elif change_rank >= 0.7:  # 前30%
            return 15
        elif change_rank >= 0.5:  # 前50%
            return 10
        else:
            return 5
    
    def calculate_date_score(self, day_of_week):
        """
        日期特征评分 (20分)
        周一: 新一周开始，资金积极 → 20分
        周五: 周末前，资金谨慎 → 10分
        其他: 中性 → 15分
        """
        if day_of_week == 0:  # 周一
            return 20
        elif day_of_week == 4:  # 周五
            return 10
        else:
            return 15
    
    def get_rating(self, total_score):
        """
        获取评级
        95-100: ⭐⭐⭐⭐⭐ 强烈推荐
        80-94: ⭐⭐⭐⭐ 推荐
        70-79: ⭐⭐⭐ 谨慎
        60-69: ⭐⭐ 观望
        <60: ⭐ 不建议
        """
        if total_score >= 95:
            return "⭐⭐⭐⭐⭐", "强烈推荐"
        elif total_score >= 80:
            return "⭐⭐⭐⭐", "推荐"
        elif total_score >= 70:
            return "⭐⭐⭐", "谨慎"
        elif total_score >= 60:
            return "⭐⭐", "观望"
        else:
            return "⭐", "不建议"
    
    def score_stocks(self, date=None, top_n=10):
        """
        评分股票
        """
        conn = sqlite3.connect(self.db_path)
        
        # 获取最新日期（如果未指定）
        if date is None:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(date) FROM limit_up_stocks")
            date = cursor.fetchone()[0]
        
        # 获取当日涨停股
        df = pd.read_sql_query(f"""
            SELECT date, code, name, close, change_pct, turnover_rate, amount
            FROM limit_up_stocks
            WHERE date = '{date}'
            ORDER BY change_pct DESC
        """, conn)
        
        conn.close()
        
        if len(df) == 0:
            return pd.DataFrame()
        
        # 计算排名
        df['amount_rank'] = df['amount'].rank(pct=True)
        df['change_rank'] = df['change_pct'].rank(pct=True)
        
        # 计算日期特征
        df['date_obj'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date_obj'].dt.dayofweek
        
        # 计算各维度得分
        df['turnover_score'] = df['turnover_rate'].apply(self.calculate_turnover_score)
        df['amount_score'] = df['amount_rank'].apply(self.calculate_amount_rank_score)
        df['change_score'] = df['change_rank'].apply(self.calculate_change_rank_score)
        df['date_score'] = df['day_of_week'].apply(self.calculate_date_score)
        
        # 总分
        df['total_score'] = (
            df['turnover_score'] + 
            df['amount_score'] + 
            df['change_score'] + 
            df['date_score']
        )
        
        # 评级
        df[['stars', 'rating']] = df['total_score'].apply(
            lambda x: pd.Series(self.get_rating(x))
        )
        
        # 排序
        df = df.sort_values('total_score', ascending=False)
        
        # 返回前N个
        return df.head(top_n)[[
            'code', 'name', 'close', 'change_pct', 'turnover_rate',
            'turnover_score', 'amount_score', 'change_score', 'date_score',
            'total_score', 'stars', 'rating'
        ]]
    
    def print_recommendations(self, date=None, top_n=10):
        """
        打印推荐结果
        """
        df = self.score_stocks(date=date, top_n=top_n)
        
        if len(df) == 0:
            print("⚠️ 无可用数据")
            return
        
        print("=" * 80)
        print("📊 Theta简化评分系统 - 股票推荐")
        print("=" * 80)
        print(f"📅 日期: {date or '2026-03-21'}")
        print(f"📈 推荐股票数: {len(df)}")
        print("=" * 80)
        
        for idx, row in df.iterrows():
            print(f"\n{row['stars']} {row['code']} {row['name']}")
            print(f"  💰 价格: {row['close']:.2f}元  涨幅: {row['change_pct']:.2f}%")
            print(f"  📊 换手率: {row['turnover_rate']:.2f}%")
            print(f"  🎯 总分: {row['total_score']:.0f}分 ({row['rating']})")
            print(f"  📈 细分: 换手{row['turnover_score']:.0f} + 额度{row['amount_score']:.0f} + 动量{row['change_score']:.0f} + 日期{row['date_score']:.0f}")
        
        print("\n" + "=" * 80)
        print("⚠️ 注意: 这是简化版评分系统，仅供参考")
        print("⚠️ 完整版需要主力资金和连板数数据")
        print("=" * 80)


if __name__ == "__main__":
    scorer = SimplifiedThetaScorer()
    scorer.print_recommendations(top_n=10)
