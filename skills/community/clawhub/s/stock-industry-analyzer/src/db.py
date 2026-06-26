# -*- coding: utf-8 -*-
"""
数据库模块 - 股票行业分析 Skill
负责数据存储和查询
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

NEWS_DB = DATA_DIR / 'news.db'


class NewsDB:
    """新闻数据库操作类"""
    
    def __init__(self):
        self.conn = sqlite3.connect(str(NEWS_DB))
        self.create_tables()
    
    def create_tables(self):
        """创建数据表"""
        cursor = self.conn.cursor()
        
        # 新闻表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                source TEXT,
                url TEXT UNIQUE,
                pub_time DATETIME,
                country TEXT,
                industry TEXT,
                sentiment TEXT,
                sentiment_score REAL,
                companies TEXT,
                keywords TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 行业趋势表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS industry_trend (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                industry TEXT NOT NULL,
                news_count INTEGER DEFAULT 0,
                positive_count INTEGER DEFAULT 0,
                negative_count INTEGER DEFAULT 0,
                neutral_count INTEGER DEFAULT 0,
                sentiment_score REAL DEFAULT 0,
                hot_rank INTEGER,
                record_date DATE,
                record_hour INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(industry, record_date, record_hour)
            )
        ''')
        
        # 股票缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT,
                industry TEXT,
                price REAL,
                change_pct REAL,
                volume REAL,
                ma5 REAL,
                ma10 REAL,
                ma20 REAL,
                rsi REAL,
                macd_signal TEXT,
                trend TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 公司行业映射表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_industry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT,
                industry TEXT,
                sub_industry TEXT,
                concepts TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 分析报告表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT,
                title TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 运行日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT,
                status TEXT,
                message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("数据库表创建完成")
    
    def insert_news(self, news_item):
        """插入新闻"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO news 
                (title, content, source, url, pub_time, country, industry, 
                 sentiment, sentiment_score, companies, keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                news_item.get('title', ''),
                news_item.get('content', ''),
                news_item.get('source', ''),
                news_item.get('url', ''),
                news_item.get('pub_time', ''),
                news_item.get('country', '国内'),
                news_item.get('industry', ''),
                news_item.get('sentiment', '中性'),
                news_item.get('sentiment_score', 0),
                json.dumps(news_item.get('companies', []), ensure_ascii=False),
                json.dumps(news_item.get('keywords', []), ensure_ascii=False)
            ))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"插入新闻失败: {e}")
            return None
    
    def insert_news_batch(self, news_list):
        """批量插入新闻"""
        count = 0
        for news in news_list:
            if self.insert_news(news):
                count += 1
        return count
    
    def get_news_by_industry(self, industry, hours=24):
        """获取某行业的新闻"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM news 
            WHERE industry = ? 
            AND created_at > datetime('now', '-{} hours')
            ORDER BY created_at DESC
        '''.format(hours), (industry,))
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_industry_trend(self, hours=24):
        """获取行业热度趋势"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT industry, 
                   COUNT(*) as news_count,
                   SUM(CASE WHEN sentiment = '利好' THEN 1 ELSE 0 END) as positive,
                   SUM(CASE WHEN sentiment = '利空' THEN 1 ELSE 0 END) as negative,
                   AVG(sentiment_score) as sentiment
            FROM news 
            WHERE created_at > datetime('now', '-{} hours')
            GROUP BY industry
            ORDER BY news_count DESC
        '''.format(hours))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_recent_news(self, limit=50):
        """获取最近新闻"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM news 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def save_stock_cache(self, stock_data):
        """保存股票缓存"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO stock_cache 
            (code, name, industry, price, change_pct, volume, 
             ma5, ma10, ma20, rsi, macd_signal, trend, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            stock_data.get('code'),
            stock_data.get('name'),
            stock_data.get('industry'),
            stock_data.get('price'),
            stock_data.get('change_pct'),
            stock_data.get('volume'),
            stock_data.get('ma5'),
            stock_data.get('ma10'),
            stock_data.get('ma20'),
            stock_data.get('rsi'),
            stock_data.get('macd_signal'),
            stock_data.get('trend'),
            datetime.now()
        ))
        self.conn.commit()
    
    def get_stock_cache(self, code):
        """获取股票缓存"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM stock_cache WHERE code = ?', (code,))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else None
    
    def save_report(self, report_type, title, content):
        """保存报告"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reports (report_type, title, content, created_at)
            VALUES (?, ?, ?, ?)
        ''', (report_type, title, json.dumps(content, ensure_ascii=False), datetime.now()))
        self.conn.commit()
        return cursor.lastrowid
    
    def log(self, task_type, status, message):
        """记录日志"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO logs (task_type, status, message, created_at)
            VALUES (?, ?, ?, ?)
        ''', (task_type, status, message, datetime.now()))
        self.conn.commit()
    
    def close(self):
        """关闭连接"""
        self.conn.close()


def init_db():
    """初始化数据库"""
    return NewsDB()


if __name__ == '__main__':
    db = init_db()
    print(f"数据库初始化完成: {NEWS_DB}")
    db.close()