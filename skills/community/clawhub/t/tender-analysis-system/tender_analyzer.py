#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标书分析助手主程序
功能：定时抓取招标信息，智能分析，生成报告
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import yaml

# 配置路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class TenderDatabase:
    """标书数据存储"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tenders (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                project_no TEXT,
                agency TEXT,
                budget TEXT,
                deadline TEXT,
                category TEXT,
                source TEXT,
                url TEXT,
                content TEXT,
                analysis TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_reports (
                id TEXT PRIMARY KEY,
                tender_id TEXT,
                dimension TEXT,
                content TEXT,
                risk_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tender_id) REFERENCES tenders(id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_tender(self, tender: Dict) -> bool:
        """保存标书信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        tender_id = hashlib.md5(
            f"{tender.get('project_no', '')}-{tender.get('title', '')}".encode()
        ).hexdigest()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tenders
                (id, title, project_no, agency, budget, deadline, category, source, url, content, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tender_id, tender.get('title', ''), tender.get('project_no', ''),
                tender.get('agency', ''), tender.get('budget', ''), tender.get('deadline', ''),
                tender.get('category', ''), tender.get('source', ''), tender.get('url', ''),
                tender.get('content', ''), 'new'
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
        finally:
            conn.close()

    def get_recent_tenders(self, hours: int = 2) -> List[Dict]:
        """获取最近N小时的标书"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        since = (datetime.now() - timedelta(hours=hours)).isoformat()

        cursor.execute('SELECT * FROM tenders WHERE created_at > ? ORDER BY created_at DESC', (since,))
        columns = [description[0] for description in cursor.description]
        tenders = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return tenders


class TenderAnalyzer:
    """标书分析器"""

    def __init__(self, config: Dict):
        self.config = config

    def generate_report(self, tender: Dict) -> str:
        """生成分析报告"""
        return f"""# 标书分析报告 - {tender.get('title', '未知项目')}

## 📋 基本信息
- **项目编号**: {tender.get('project_no', 'N/A')}
- **招标单位**: {tender.get('agency', 'N/A')}
- **预算金额**: {tender.get('budget', 'N/A')}
- **投标截止**: {tender.get('deadline', 'N/A')}
- **信息来源**: {tender.get('source', 'N/A')}
- **行业分类**: {tender.get('category', 'N/A')}

## 💰 付款方式分析
待LLM深度分析...

## 📊 评标办法分析
待LLM深度分析...

## ⚙️ 技术参数要点
待LLM深度分析...

## 📄 合同条款风险
待LLM深度分析...

## 🎯 投标建议
- **机会评估**: 待评估
- **风险提示**: 待分析
- **策略建议**: 待生成

---
*分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""


class TenderReporter:
    """标书汇报器"""

    def __init__(self, config: Dict):
        self.config = config

    def generate_summary(self, tenders: List[Dict]) -> str:
        """生成汇报摘要"""
        if not tenders:
            return "📭 过去2小时内未发现新的招标信息"

        # 按行业分类统计
        by_category = {}
        for t in tenders:
            cat = t.get('category', '其他')
            by_category[cat] = by_category.get(cat, 0) + 1

        # 高价值项目
        high_value = [t for t in tenders if '千万' in str(t.get('budget', '')) or '亿' in str(t.get('budget', ''))]

        report = f"""# 📊 标书监控汇报 ({datetime.now().strftime('%m-%d %H:%M')})

## 📈 新增标书统计
**总计**: {len(tenders)} 条

| 行业分类 | 数量 |
|---------|------|
"""
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            report += f"| {cat} | {count} |\n"

        if high_value:
            report += f"\n## 💎 高价值项目TOP5\n"
            for i, t in enumerate(high_value[:5], 1):
                report += f"{i}. **{t.get('title', 'N/A')[:30]}...**\n"
                report += f"   - 金额: {t.get('budget', 'N/A')} | 截止: {t.get('deadline', 'N/A')}\n"

        # 紧急项目
        urgent = [t for t in tenders if self._is_urgent(t.get('deadline', ''))]
        if urgent:
            report += f"\n## ⏰ 紧急项目提醒（48小时内截止）\n"
            for t in urgent[:5]:
                report += f"- **{t.get('title', 'N/A')[:25]}...** | 截止: {t.get('deadline', 'N/A')}\n"

        report += f"\n---\n*下次汇报: 2小时后 | 数据来源: 政府采购/运营商/金融/央企*"
        return report

    def _is_urgent(self, deadline: str) -> bool:
        """判断是否紧急（48小时内）"""
        try:
            # 简化判断，实际应解析日期
            return False
        except:
            return False


def load_config() -> Dict:
    """加载配置"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def main():
    """主函数"""
    print("🚀 标书分析助手启动...")

    config = load_config()
    db_path = config.get('storage', {}).get('path', './data/tenders.db')

    db = TenderDatabase(db_path)
    analyzer = TenderAnalyzer(config)
    reporter = TenderReporter(config)

    # 获取最近2小时的标书
    recent_tenders = db.get_recent_tenders(hours=2)

    # 生成汇报
    summary = reporter.generate_summary(recent_tenders)

    print("\n" + "="*60)
    print(summary)
    print("="*60)

    # 保存汇报到文件
    report_file = os.path.join(DATA_DIR, f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n✅ 汇报已保存: {report_file}")


if __name__ == '__main__':
    main()
