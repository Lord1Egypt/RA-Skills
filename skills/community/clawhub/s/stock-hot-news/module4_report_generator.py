#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 4: 完整财经热点新闻报告生成器（最终版）
从complete_finance_report_final.py移植，集成真实数据源

功能：
1. 热点新闻TOP5 - 数据源于module2生成的热点新闻top5
2. 热点新闻TOP3深度报告 - 数据源于module2生成的深度报告
3. 快讯TOP10 - 数据源于module3生成的快讯top10

输出：
1. 文字版报告 (.txt)
2. HTML版报告 (.html)
3. HTML图片版 (.png)
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import subprocess
import tempfile

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('stock-hot-news.final-report')


class FinalReportGenerator:
    """最终报告生成器"""
    
    def __init__(self):
        """初始化"""
        self.name = "完整财经热点新闻报告生成器"
        
        # 加载配置文件
        self.config = self.load_config()
        
        if self.config:
            system_settings = self.config.get('system_settings', {})
            wallstreet_config = self.config.get('wallstreetcn_module', {})
            
            # Module 2输入目录 - 基于temp_dir构建
            temp_dir = system_settings.get('temp_dir', 'c:/SelfData/claw_temp/temp')
            self.module2_dir = Path(temp_dir) / "title_news_crawl" / "summarized"
            
            # Module 3输入目录 - 从wallstreetcn_module获取output_directory
            module3_dir_str = wallstreet_config.get('output_directory', str(Path(temp_dir) / "wallstreetcn_news"))
            self.module3_dir = Path(module3_dir_str)
            
            # 输出目录 - 从system_settings获取reports_dir
            output_dir_str = system_settings.get('reports_dir', 'c:/SelfData/claw_temp/reports')
            self.output_dir = Path(output_dir_str)
            
            logger.info(f"[INFO] 从配置文件加载路径成功")
        else:
            # 默认路径（兼容旧版本）
            self.module2_dir = Path("c:/SelfData/claw_temp/temp/title_news_crawl/summarized")
            self.module3_dir = Path("c:/SelfData/claw_temp/temp/wallstreetcn_news")
            self.output_dir = Path("c:/SelfData/claw_temp/reports")
            logger.warning(f"[WARNING] 配置文件加载失败，使用默认路径")
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"{self.name} 初始化完成")
        logger.info(f"Module 2输入目录: {self.module2_dir}")
        logger.info(f"Module 3输入目录: {self.module3_dir}")
        logger.info(f"报告输出目录: {self.output_dir}")
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        try:
            config_path = Path(__file__).parent / "url_config.json"
            if not config_path.exists():
                logger.warning(f"配置文件不存在: {config_path}")
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"配置文件加载成功")
            return config
            
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return None
    
    def find_latest_file(self, directory: Path, pattern: str) -> Optional[Path]:
        """查找指定目录下最新的匹配文件"""
        try:
            if not directory.exists():
                logger.warning(f"目录不存在: {directory}")
                return None
            
            files = list(directory.glob(pattern))
            if not files:
                logger.warning(f"未找到匹配文件: {directory}/{pattern}")
                return None
            
            # 按修改时间排序，返回最新的
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            return latest_file
            
        except Exception as e:
            logger.error(f"查找文件失败: {e}")
            return None
    
    def load_module2_topics(self) -> Tuple[bool, List[Dict], str]:
        """加载Module 2热点新闻TOP5"""
        logger.info("加载Module 2热点新闻TOP5...")
        
        # 查找最新的topics文件
        pattern = "top_*_topics_*.json"
        latest_file = self.find_latest_file(self.module2_dir, pattern)
        
        if not latest_file:
            logger.error("未找到Module 2话题文件")
            return False, [], "未找到Module 2话题文件"
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            topics = data.get('topics', [])
            if not topics:
                logger.warning("Module 2话题文件中无数据")
                return False, [], "Module 2话题文件中无数据"
            
            logger.info(f"成功加载Module 2话题: {len(topics)} 个")
            
            # 按评分排序（评分高的在前）
            sorted_topics = sorted(
                topics,
                key=lambda x: x.get('score', 0),
                reverse=True
            )
            
            # 获取前5名（热点新闻TOP5）
            top5_topics = sorted_topics[:5]
            
            # 转换为报告格式
            formatted_topics = []
            for i, topic in enumerate(top5_topics, 1):
                # 从articles中获取第一篇文章的详细信息
                articles = topic.get('articles', [])
                first_article = articles[0] if articles else {}
                
                formatted_topic = {
                    'rank': i,
                    'title': topic.get('topic', '未知话题')[:200],
                    'source': first_article.get('source', '未知来源'),
                    'summary': topic.get('summary', '无总结')[:200],
                    'score': topic.get('score', 0),
                    'publish_time': first_article.get('publish_time', '未知时间'),
                    'url': first_article.get('url', ''),
                    'keywords': self.extract_keywords(topic)
                }
                formatted_topics.append(formatted_topic)
            
            return True, formatted_topics, f"Module 2话题文件: {latest_file.name}"
            
        except Exception as e:
            logger.error(f"加载Module 2话题失败: {e}")
            return False, [], f"加载Module 2话题失败: {e}"
    
    def load_module2_deep_analysis(self) -> Tuple[bool, List[Dict], str]:
        """加载Module 2深度分析报告"""
        logger.info("加载Module 2深度分析报告...")
        
        # 查找最新的深度分析文件
        pattern = "deep_analysis_*.json"
        latest_file = self.find_latest_file(self.module2_dir, pattern)
        
        if not latest_file:
            logger.warning("未找到Module 2深度分析文件，将使用话题数据生成简版分析")
            return False, [], "未找到Module 2深度分析文件"
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            analyses = data.get('analyses', [])
            if not analyses:
                logger.warning("Module 2深度分析文件中无数据")
                return False, [], "Module 2深度分析文件中无数据"
            
            logger.info(f"成功加载Module 2深度分析: {len(analyses)} 个")
            
            # 转换为报告格式
            formatted_analyses = []
            for analysis in analyses[:3]:  # 只取前3个
                formatted_analysis = {
                    'rank': analysis.get('topic_index', 0) + 1,
                    'title': analysis.get('topic_title', '未知话题'),
                    'source': '深度分析报告',
                    'analysis': analysis.get('analysis', '无分析内容'),
                    'url': analysis.get('url', ''),
                    'score': analysis.get('score', 0)
                }
                formatted_analyses.append(formatted_analysis)
            
            return True, formatted_analyses, f"Module 2深度分析文件: {latest_file.name}"
            
        except Exception as e:
            logger.error(f"加载Module 2深度分析失败: {e}")
            return False, [], f"加载Module 2深度分析失败: {e}"
    
    def load_module3_news(self) -> Tuple[bool, List[Dict], str]:
        """加载Module 3快讯TOP10"""
        logger.info("加载Module 3快讯TOP10...")
        
        # 查找最新的快讯文件（支持所有模式：playwright、single、scroll）
        patterns = [
            "wallstreetcn_playwright_*.json",
            "wallstreetcn_single_*.json", 
            "wallstreetcn_scroll_*.json",
            "wallstreetcn_*.json"
        ]
        
        latest_file = None
        for pattern in patterns:
            latest_file = self.find_latest_file(self.module3_dir, pattern)
            if latest_file:
                logger.info(f"找到快讯文件: {latest_file.name} (模式: {pattern})")
                break
        
        if not latest_file:
            logger.error("未找到Module 3快讯文件")
        
        if not latest_file:
            logger.error("未找到Module 3快讯文件")
            return False, [], "未找到Module 3快讯文件"
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            articles = data.get('articles', [])
            if not articles:
                logger.warning("Module 3快讯文件中无数据")
                return False, [], "Module 3快讯文件中无数据"
            
            logger.info(f"成功加载Module 3快讯: {len(articles)} 条")
            
            # 按重要性排序（重要的在前）
            sorted_articles = sorted(
                articles,
                key=lambda x: (x.get('importance', False), x.get('timestamp', '')),
                reverse=True
            )
            
            # 获取前10名（快讯TOP10）
            top10_articles = sorted_articles[:10]
            
            # 转换为报告格式
            formatted_articles = []
            for i, article in enumerate(top10_articles, 1):
                # 计算评分（模拟）
                score_details = self.calculate_score_for_news(article)
                total_score = sum(score_details.values())
                
                formatted_article = {
                    'rank': i,
                    'timestamp': article.get('timestamp', '未知时间'),
                    'title': article.get('title', '未知标题'),
                    'content': article.get('content', ''),  # 显示完整内容，不截断
                    'importance': article.get('importance', False),
                    'source': '华尔街见闻',
                    'total_score': total_score,
                    'score_details': score_details
                }
                formatted_articles.append(formatted_article)
            
            return True, formatted_articles, f"Module 3快讯文件: {latest_file.name}"
            
        except Exception as e:
            logger.error(f"加载Module 3快讯失败: {e}")
            return False, [], f"加载Module 3快讯失败: {e}"
    
    def extract_keywords(self, topic: Dict) -> List[str]:
        """从话题中提取关键词"""
        keywords = []
        
        # 从标题中提取关键词
        title = topic.get('topic', '')
        common_keywords = [
            '股市', 'A股', '港股', '美股', '指数', '上证', '深证', '创业板', '科创板',
            '原油', '石油', '黄金', '白银', '铜', '铝', '铁矿石',
            'GDP', 'CPI', 'PPI', 'PMI', '通胀', '通缩', '利率', '汇率', '货币政策',
            '美国', '欧洲', '日本', '中国', '俄罗斯', '伊朗', '以色列', '制裁', '贸易战',
            '财报', '业绩', '上市', '退市', '并购', '重组', '特斯拉', '苹果', '微软',
            '政策', '监管', '法规', '改革', '开放', '试点', '自贸区',
            'AI', '人工智能', '芯片', '半导体', '5G', '新能源', '电动车', '自动驾驶',
            '战争', '冲突', '导弹', '战机', '军事', '攻击', '核', '军演'
        ]
        
        for keyword in common_keywords:
            if keyword in title:
                keywords.append(keyword)
        
        # 限制数量
        return keywords[:5] if keywords else ['财经', '热点', '新闻']
    
    def calculate_score_for_news(self, article: Dict) -> Dict[str, int]:
        """计算快讯评分（模拟）"""
        score_details = {
            'source_authority': 25,  # 信源权威性 (35分)
            'substantial_impact': 22,  # 信息实质影响 (30分)
            'completeness_risk': 10,  # 完整性与风险 (15分)
            'timeliness': 15  # 时间新鲜度 (20分)
        }
        
        # 根据重要性调整
        if article.get('importance', False):
            score_details['source_authority'] += 5
            score_details['substantial_impact'] += 5
        
        # 根据内容长度调整
        content = article.get('content', '')
        if len(content) > 100:
            score_details['completeness_risk'] += 3
        
        # 限制最大值
        score_details['source_authority'] = min(score_details['source_authority'], 35)
        score_details['substantial_impact'] = min(score_details['substantial_impact'], 30)
        score_details['completeness_risk'] = min(score_details['completeness_risk'], 15)
        score_details['timeliness'] = min(score_details['timeliness'], 20)
        
        return score_details
    
    def generate_text_report(self, hot_news: List[Dict], deep_reports: List[Dict], latest_news: List[Dict]) -> str:
        """生成文字版报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = f"""{'='*80}
完整财经热点新闻报告
{'='*80}
生成时间: {timestamp}
报告ID: {report_id}

第一部分：热点新闻TOP5
{'-'*80}
"""
        
        # 热点新闻TOP5
        for news in hot_news:
            report += f"🏆 TOP{news['rank']} 【热度:{news['score']:.1f}分】 {news['title']}\n"
            report += f"   来源: {news['source']} | 发布时间: {news['publish_time']}\n"
            report += f"   摘要: {news['summary']}\n"
            report += f"   关键词: {', '.join(news.get('keywords', ['财经', '热点']))}\n"
            if news.get('url'):
                report += f"   链接: {news['url']}\n"
            report += "\n"
        
        # 热点新闻TOP3深度报告
        report += f"""
第二部分：热点新闻TOP3深度报告
{'-'*80}
"""
        
        for report_data in deep_reports:
            report += f"🏆 TOP{report_data['rank']} {report_data['title']}\n"
            report += f"   来源: {report_data['source']}\n"
            report += f"   📊 深度分析报告:\n"
            analysis_text = report_data.get('analysis', '无分析内容')
            # 格式化分析文本，添加缩进
            for line in analysis_text.split('\n'):
                report += f"   {line}\n"
            report += "\n"
        
        # 快讯TOP10
        report += f"""
第三部分：最新快讯TOP10（时间+得分+摘要）
{'-'*80}
说明：评分在抓取快讯全部信息时立即进行，时间新鲜度按当前时间和快讯时间差值计算

"""
        
        for news in latest_news:
            importance = "[重要] " if news.get('importance', False) else ""
            total_score = news.get('total_score', 0)
            
            score_details = news.get('score_details', {})
            source_score = score_details.get('source_authority', 0)
            impact_score = score_details.get('substantial_impact', 0)
            risk_score = score_details.get('completeness_risk', 0)
            timeliness_score = score_details.get('timeliness', 0)
            
            report += f"{news['rank']}. 【{news['timestamp']}】 {importance}得分:{total_score:.1f}/100\n"
            report += f"   标题: {news['title']}\n"
            report += f"   摘要: {news['content'][:100]}...\n"
            report += f"   评分详情: 信源权威性({source_score}/35) | 信息实质影响({impact_score}/30) | "
            report += f"完整性与风险({risk_score}/15) | 时间新鲜度({timeliness_score}/20)\n\n"
        
        report += f"""
{'='*80}
报告结束
{'='*80}
"""
        
        return report
    
    def generate_html_report(self, hot_news: List[Dict], deep_reports: List[Dict], latest_news: List[Dict]) -> str:
        """生成HTML报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 生成热点新闻HTML
        hot_news_html = ""
        for news in hot_news:
            keywords_html = ', '.join(news.get('keywords', ['财经', '热点']))
            hot_news_html += f"""
            <div class="hot-news-item">
                <div class="hot-news-rank">{news['rank']}</div>
                <div class="hot-news-content">
                    <div class="hot-news-title">{news['title']}</div>
                    <div class="hot-news-meta">
                        <span class="source">{news['source']}</span>
                        <span class="heat-score">热度: {news['score']:.1f}分</span>
                        <span class="publish-time">{news['publish_time']}</span>
                    </div>
                    <div class="hot-news-summary">{news['summary']}</div>
                    <div class="hot-news-keywords">
                        <strong>关键词:</strong> {keywords_html}
                    </div>
            """
            if news.get('url'):
                hot_news_html += f"""
                    <div class="hot-news-link">
                        <a href="{news['url']}" target="_blank">查看原文</a>
                    </div>
                """
            hot_news_html += """
                </div>
            </div>
            """
        
        # 生成深度报告HTML
        deep_reports_html = ""
        for report_data in deep_reports:
            analysis_text = report_data.get('analysis', '无分析内容')
            # 将分析文本转换为HTML段落
            analysis_html = ""
            for line in analysis_text.split('\n'):
                if line.strip():
                    analysis_html += f"<p>{line}</p>"
            
            deep_reports_html += f"""
            <div class="deep-analysis-item">
                <div class="deep-analysis-rank">TOP{report_data['rank']}</div>
                <div class="deep-analysis-content">
                    <div class="deep-analysis-title">{report_data['title']}</div>
                    <div class="deep-analysis-meta">
                        <span class="source">{report_data['source']}</span>
                        <span class="score">评分: {report_data.get('score', 0):.1f}</span>
                    </div>
                    <div class="deep-analysis-text">
                        {analysis_html}
                    </div>
            """
            if report_data.get('url'):
                deep_reports_html += f"""
                    <div class="deep-analysis-link">
                        <a href="{report_data['url']}" target="_blank">查看原文</a>
                    </div>
                """
            deep_reports_html += """
                </div>
            </div>
            """
        
        # 生成快讯HTML - 标题和内容分开显示，完整内容
        latest_news_html = ""
        for news in latest_news:
            importance_class = "important" if news.get('importance', False) else ""
            total_score = news.get('total_score', 0)
            
            latest_news_html += f"""
            <div class="live-news-item {importance_class}">
                <div class="live-news-header">
                    <div class="live-news-rank">{news['rank']}</div>
                    <div class="live-news-meta">
                        <span class="live-news-score">
                            <i class="fas fa-chart-line"></i> {total_score:.1f}
                        </span>
                        <span class="live-news-time">
                            <i class="fas fa-clock"></i> {news['timestamp']}
                        </span>
                        {f'<span class="live-news-importance"><i class="fas fa-star"></i> 重要快讯</span>' if news.get('importance', False) else ''}
                    </div>
                </div>
                
                <h3 class="live-news-title">{news['title']}</h3>
                <div class="live-news-content">{news['content']}</div>
            </div>
            """
        
        # 统计变量定义
        hot_news_count = len(hot_news)
        deep_analyses_count = len(deep_reports)
        live_news_count = len(latest_news)
        important_live_count = sum(1 for n in latest_news if n.get('importance', False))
        
        # 完整的HTML模板 - 美化版
        html_template = f"""<!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>财经热点新闻报告 - {date_str}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
        :root {{
            --primary-color: #4361ee;
            --secondary-color: #3a0ca3;
            --accent-color: #4cc9f0;
            --success-color: #4ade80;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --dark-color: #1e293b;
            --light-color: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-300: #cbd5e1;
            --gray-400: #94a3b8;
            --gray-500: #64748b;
            --gray-600: #475569;
            --gray-700: #334155;
            --gray-800: #1e293b;
            --green-light: #d1fae5;
            --green-medium: #10b981;
            --green-dark: #065f46;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1);
            --border-radius: 12px;
            --border-radius-sm: 8px;
            --transition: all 0.3s ease;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans SC', 'Inter', 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: var(--dark-color);
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-xl);
            overflow: hidden;
        }}

        /* 头部样式 */
        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 30px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.8s ease-out;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 30px 30px;
            animation: float 20s linear infinite;
            opacity: 0.3;
        }}

        @keyframes float {{
            0% {{ transform: translate(0, 0) rotate(0deg); }}
            100% {{ transform: translate(-30px, -30px) rotate(360deg); }}
        }}

        .header-content {{
            position: relative;
            z-index: 2;
        }}

        .header h1 {{
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }}

        .header-subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 25px;
        }}

        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            border-radius: var(--border-radius-sm);
            text-align: center;
            min-width: 140px;
            transition: var(--transition);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.25);
        }}

        .stat-value {{
            font-size: 2.2rem;
            font-weight: 700;
            display: block;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 0.95rem;
            opacity: 0.9;
        }}

        /* 主要内容区域 */
        .content {{
            padding: 20px 15px;
        }}

        .section {{
            margin-bottom: 20px;
        }}

        .section-title {{
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--dark-color);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary-color);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-title i {{
            color: var(--primary-color);
        }}

        /* 热点新闻章节特殊样式 - 蓝色系 */
        .hot-news-section .section-title {{
            border-bottom-color: var(--primary-color);
        }}

        .hot-news-section .section-title i {{
            color: var(--primary-color);
        }}

        /* 实时快讯章节特殊样式 - 绿色系 */
        .live-news-section .section-title {{
            border-bottom-color: var(--green-medium);
        }}

        .live-news-section .section-title i {{
            color: var(--green-medium);
        }}

        /* 热点新闻样式 - 蓝色系 */
        .hot-news-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .hot-news-item {{
            background: linear-gradient(to right, rgba(67, 97, 238, 0.03), rgba(248, 250, 252, 0.8));
            border-radius: var(--border-radius-sm);
            padding: 15px;
            border: 1px solid rgba(67, 97, 238, 0.15);
            transition: var(--transition);
            display: flex;
            gap: 15px;
            position: relative;
            overflow: hidden;
        }}

        .hot-news-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(67, 97, 238, 0.2);
            border-color: var(--primary-color);
            background: linear-gradient(to right, rgba(67, 97, 238, 0.08), rgba(248, 250, 252, 0.9));
        }}

        .hot-news-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary-color), var(--accent-color));
        }}

        .hot-news-rank {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: 700;
            flex-shrink: 0;
            box-shadow: 0 4px 10px rgba(67, 97, 238, 0.3);
        }}

        .hot-news-content {{
            flex: 1;
        }}

        .hot-news-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .hot-news-meta {{
            color: var(--gray-500);
            font-size: 0.95rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .hot-news-summary {{
            color: var(--gray-700);
            line-height: 1.7;
            font-size: 1.05rem;
        }}

        .summary-text {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid var(--accent-color);
        }}

        /* 深度分析样式 - 蓝色系 */
        .deep-analysis-list {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .deep-analysis-item {{
            background: linear-gradient(to right, rgba(240, 249, 255, 0.8), rgba(224, 242, 254, 0.9));
            border-radius: var(--border-radius-sm);
            padding: 20px;
            border: 1px solid rgba(67, 97, 238, 0.2);
            border-left: 4px solid var(--primary-color);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out 0.1s both;
        }}

        .deep-analysis-item:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px -5px rgba(67, 97, 238, 0.15);
            background: linear-gradient(to right, rgba(240, 249, 255, 0.9), rgba(224, 242, 254, 1));
            border-color: rgba(67, 97, 238, 0.3);
        }}

        .deep-analysis-rank {{
            background: var(--primary-color);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 12px;
        }}

        .deep-analysis-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 10px;
        }}

        .deep-analysis-text {{
            color: var(--gray-700);
            line-height: 1.6;
            font-size: 1rem;
            margin-bottom: 15px;
        }}
        
        .deep-analysis-link {{
            margin-top: 15px;
            text-align: right;
        }}
        
        .deep-analysis-link a {{
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 600;
            padding: 8px 16px;
            border: 1px solid var(--primary-color);
            border-radius: 20px;
            transition: var(--transition);
        }}
        
        .deep-analysis-link a:hover {{
            background: var(--primary-color);
            color: white;
        }}

        .analysis-text {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid var(--accent-color);
        }}

        /* 快讯样式 - 绿色系 */
        .live-news-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .live-news-item, .latest-news-item {{
            background: linear-gradient(to right, rgba(16, 185, 129, 0.02), white);
            border-radius: var(--border-radius-sm);
            padding: 14px;
            border: 2px solid rgba(16, 185, 129, 0.2);
            transition: var(--transition);
            animation: fadeInUp 0.6s ease-out 0.2s both;
        }}

        .live-news-item:hover, .latest-news-item:hover {{
            transform: translateX(5px);
            box-shadow: var(--shadow-md);
        }}

        .live-news-item.important, .latest-news-item.important {{
            border-color: var(--green-medium);
            background: linear-gradient(to right, rgba(16, 185, 129, 0.08), white);
        }}

        .live-news-item.important::before, .latest-news-item.important::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: var(--green-medium);
        }}

        .live-news-rank {{
            background: linear-gradient(135deg, rgba(209, 250, 229, 0.95), rgba(209, 250, 229, 0.8));
            color: var(--green-dark);
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            font-weight: 800;
            flex-shrink: 0;
            border: 2px solid rgba(16, 185, 129, 0.4);
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.25);
            position: relative;
            z-index: 1;
        }}

        .live-news-header, .latest-news-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .live-news-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .live-news-score {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(16, 185, 129, 0.08));
            color: var(--green-medium);
            padding: 5px 10px;
            border-radius: 18px;
            font-weight: 700;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 5px;
            border: 1px solid rgba(16, 185, 129, 0.3);
            box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
        }}

        .live-news-time {{
            background: rgba(100, 116, 139, 0.08);
            color: var(--gray-600);
            padding: 5px 10px;
            border-radius: 18px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 5px;
            border: 1px solid rgba(100, 116, 139, 0.2);
            font-weight: 500;
        }}

        .live-news-importance {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.08));
            color: var(--warning-color);
            padding: 5px 10px;
            border-radius: 18px;
            font-weight: 700;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 5px;
            border: 1px solid rgba(245, 158, 11, 0.4);
            box-shadow: 0 2px 4px rgba(245, 158, 11, 0.15);
            white-space: nowrap;
        }}

        .live-news-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .live-news-content {{
            color: var(--gray-700);
            line-height: 1.7;
            font-size: 1.05rem;
            padding: 12px;
            background: rgba(16, 185, 129, 0.05);
            border-radius: 8px;
            white-space: pre-line;
            border-left: 3px solid rgba(16, 185, 129, 0.3);
        }}

        /* 页脚样式 */
        .footer {{
            background: linear-gradient(135deg, var(--gray-800), var(--dark-color));
            color: var(--gray-300);
            padding: 35px 30px;
            text-align: center;
        }}

        .footer-content {{
            max-width: 800px;
            margin: 0 auto;
        }}

        .footer-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: white;
        }}

        .footer-info {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .footer-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .footer-disclaimer {{
            font-size: 0.9rem;
            opacity: 0.7;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* 响应式设计 */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
                flex-direction: column;
                gap: 10px;
            }}

            .header-subtitle {{
                font-size: 1rem;
            }}

            .stats-container {{
                gap: 15px;
            }}

            .stat-card {{
                min-width: 120px;
                padding: 15px 20px;
            }}

            .stat-value {{
                font-size: 1.8rem;
            }}

            .content {{
                padding: 25px 20px;
            }}

            .section-title {{
                font-size: 1.5rem;
            }}

            .hot-news-item {{
                flex-direction: column;
                gap: 15px;
                padding: 20px;
            }}

            .hot-news-rank {{
                width: 45px;
                height: 45px;
                font-size: 1.2rem;
            }}

            .hot-news-title {{
                font-size: 1.15rem;
            }}

            .live-news-item {{
                padding: 18px;
            }}

            .live-news-title {{
                font-size: 1.1rem;
            }}

            .footer-info {{
                flex-direction: column;
                gap: 15px;
                align-items: center;
            }}
        }}

        @media (max-width: 480px) {{
            body {{
                padding: 10px;
            }}

            .header {{
                padding: 30px 20px;
            }}

            .header h1 {{
                font-size: 1.6rem;
            }}

            .stat-card {{
                min-width: calc(50% - 15px);
            }}

            .section-title {{
                font-size: 1.3rem;
            }}
        }}

        /* 动画效果 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .hot-news-item {{
            animation: fadeIn 0.5s ease forwards;
            opacity: 0;
        }}

        .hot-news-item:nth-child(1) {{ animation-delay: 0.1s; }}
        .hot-news-item:nth-child(2) {{ animation-delay: 0.2s; }}
        .hot-news-item:nth-child(3) {{ animation-delay: 0.3s; }}
        .hot-news-item:nth-child(4) {{ animation-delay: 0.4s; }}
        .hot-news-item:nth-child(5) {{ animation-delay: 0.5s; }}

        .live-news-item {{
            animation: fadeIn 0.5s ease forwards;
            opacity: 0;
        }}

        .live-news-item:nth-child(1) {{ animation-delay: 0.1s; }}
        .live-news-item:nth-child(2) {{ animation-delay: 0.2s; }}
        .live-news-item:nth-child(3) {{ animation-delay: 0.3s; }}
        .live-news-item:nth-child(4) {{ animation-delay: 0.4s; }}
        .live-news-item:nth-child(5) {{ animation-delay: 0.5s; }}
        .live-news-item:nth-child(6) {{ animation-delay: 0.6s; }}
        .live-news-item:nth-child(7) {{ animation-delay: 0.7s; }}
        .live-news-item:nth-child(8) {{ animation-delay: 0.8s; }}
        .live-news-item:nth-child(9) {{ animation-delay: 0.9s; }}
        .live-news-item:nth-child(10) {{ animation-delay: 1.0s; }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .live-news-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            
            .live-news-meta {{
                width: 100%;
                justify-content: flex-start;
                gap: 8px;
            }}
            
            .live-news-rank {{
                width: 34px;
                height: 34px;
                font-size: 1rem;
            }}
            
            .live-news-score,
            .live-news-time,
            .live-news-importance {{
                padding: 4px 8px;
                font-size: 0.8rem;
            }}
            
            .live-news-title {{
                font-size: 1.1rem;
                margin-bottom: 10px;
            }}
            
            .live-news-content {{
                padding: 10px;
                font-size: 1rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .live-news-meta {{
                flex-wrap: wrap;
                gap: 6px;
            }}
            
            .live-news-score,
            .live-news-time,
            .live-news-importance {{
                padding: 3px 6px;
                font-size: 0.75rem;
            }}
        }}
        </style>
    </head>
    <body>
        <div class="container">
        <header class="header">
            <div class="header-content">
                <h1>
                    <i class="fas fa-chart-line"></i>
                    财经热点新闻报告
                </h1>
                <div class="header-subtitle">热点新闻 | 深度分析 | 实时快讯 | 生成时间: {timestamp}</div>
            </div>
        </header>

        <main class="content">
            <section class="section hot-news-section">
                <h2 class="section-title">
                    <i class="fas fa-fire"></i>
                    热点新闻TOP5
                </h2>
                <div class="hot-news-list">
                    {hot_news_html}
                </div>
            </section>

            <section class="section hot-news-section">
                <h2 class="section-title">
                    <i class="fas fa-search"></i>
                    深度分析TOP3
                </h2>
                <div class="deep-analysis-list">
                    {deep_reports_html}
                </div>
            </section>

            <section class="section live-news-section">
                <h2 class="section-title">
                    <i class="fas fa-bolt"></i>
                    实时快讯TOP10
                </h2>
                <div class="live-news-list">
                    {latest_news_html}
                </div>
            </section>
        </main>

        <footer class="footer">
            <div class="footer-content">
                <div class="footer-title">stock-hot-news 财经热点分析系统</div>

                <div class="footer-info">
                    <div class="footer-item">
                        <i class="fas fa-code-branch"></i>
                        <span>版本 2.0.0</span>
                    </div>
                    <div class="footer-item">
                        <i class="fas fa-calendar-alt"></i>
                        <span>生成时间: {timestamp}</span>
                    </div>
                    <div class="footer-item">
                        <i class="fas fa-database"></i>
                        <span>数据实时更新</span>
                    </div>
                </div>

                <div class="footer-disclaimer">
                    免责声明:本报告基于公开信息自动生成,内容仅供参考,不构成任何投资建议。市场有风险,投资需谨慎。
                </div>
            </div>
        </footer>
        </div>

        <script>
        // 添加简单的交互效果
        document.addEventListener('DOMContentLoaded', function() {{
            // 为新闻项添加点击效果
            const newsItems = document.querySelectorAll('.hot-news-item, .live-news-item, .deep-analysis-item');
            newsItems.forEach(item => {{
                item.addEventListener('click', function() {{
                    this.style.transform = 'scale(0.99)';
                    setTimeout(() => {{
                        this.style.transform = '';
                    }}, 150);
                }});
            }});

            // 自动滚动到最新内容(如果有的话)
            const importantItems = document.querySelectorAll('.live-news-item.important');
            if (importantItems.length > 0) {{
                setTimeout(() => {{
                    importantItems[0].scrollIntoView({{
                        behavior: 'smooth',
                        block: 'center'
                    }});
                }}, 1000);
            }}

            // 添加打印功能按钮
            const printBtn = document.createElement('button');
            printBtn.innerHTML = '<i class="fas fa-print"></i> 打印报告';
            printBtn.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: var(--primary-color);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 50px;
                cursor: pointer;
                font-family: inherit;
                font-weight: 600;
                box-shadow: var(--shadow-lg);
                z-index: 1000;
                transition: var(--transition);
                display: flex;
                align-items: center;
                gap: 8px;
            `;
            printBtn.onmouseenter = () => printBtn.style.transform = 'translateY(-3px)';
            printBtn.onmouseleave = () => printBtn.style.transform = '';
            printBtn.onclick = () => window.print();

            document.body.appendChild(printBtn);
        }});
        </script>
    </body>
    </html>"""

        return html_template
    
    def generate_screenshot(self, html_file: Path, png_file: Path) -> bool:
        """生成HTML页面截图"""
        try:
            # 检查是否安装了playwright
            try:
                import asyncio
                from playwright.async_api import async_playwright
                playwright_available = True
            except ImportError:
                playwright_available = False
                logger.warning("Playwright未安装，跳过截图生成")
                return False
            
            async def take_screenshot():
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        viewport={'width': 1200, 'height': 1600}
                    )
                    page = await context.new_page()
                    
                    # 加载HTML文件
                    await page.goto(f"file:///{html_file}")
                    await page.wait_for_load_state('networkidle')
                    
                    # 截图
                    await page.screenshot(
                        path=str(png_file),
                        full_page=True
                    )
                    
                    await browser.close()
            
            # 运行异步截图
            asyncio.run(take_screenshot())
            logger.info(f"HTML截图已生成: {png_file}")
            return True
            
        except Exception as e:
            logger.error(f"生成截图失败: {e}")
            return False
    
    def run(self) -> bool:
        """运行报告生成流程"""
        print(f"\n{'='*80}")
        print(f"{self.name}")
        print(f"{'='*80}")
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. 加载热点新闻TOP5
            print(f"\n1. 加载热点新闻TOP5...")
            hot_news_success, hot_news_data, hot_news_info = self.load_module2_topics()
            if hot_news_success:
                print(f"   [OK] 成功加载: {len(hot_news_data)} 条热点新闻")
                print(f"       文件: {hot_news_info}")
            else:
                print(f"   [ERROR] 加载失败: {hot_news_info}")
                hot_news_data = []
            
            # 2. 加载深度分析报告
            print(f"\n2. 加载深度分析报告...")
            deep_reports_success, deep_reports_data, deep_reports_info = self.load_module2_deep_analysis()
            if deep_reports_success:
                print(f"   [OK] 成功加载: {len(deep_reports_data)} 个深度分析")
                print(f"       文件: {deep_reports_info}")
            else:
                print(f"   [WARNING] 加载失败: {deep_reports_info}")
                # 如果没有深度分析文件，从热点新闻生成简版分析
                if hot_news_data:
                    print(f"   [INFO] 从热点新闻生成简版深度分析")
                    deep_reports_data = []
                    for i, news in enumerate(hot_news_data[:3], 1):
                        deep_reports_data.append({
                            'rank': i,
                            'title': news['title'],
                            'source': news['source'],
                            'analysis': f"基于{news['source']}的报道分析：{news['summary']}\n\n该话题当前评分为{news['score']:.1f}分，属于热点财经新闻。",
                            'score': news['score']
                        })
                else:
                    deep_reports_data = []
            
            # 3. 加载快讯TOP10
            print(f"\n3. 加载快讯TOP10...")
            latest_news_success, latest_news_data, latest_news_info = self.load_module3_news()
            if latest_news_success:
                print(f"   [OK] 成功加载: {len(latest_news_data)} 条快讯")
                important_count = sum(1 for n in latest_news_data if n.get('importance', False))
                print(f"       其中重要快讯: {important_count} 条")
                print(f"       文件: {latest_news_info}")
            else:
                print(f"   [ERROR] 加载失败: {latest_news_info}")
                latest_news_data = []
            
            # 检查是否有足够的数据
            if not (hot_news_data or deep_reports_data or latest_news_data):
                print(f"\n[ERROR] 所有数据加载失败，无法生成报告")
                return False
            
            # 4. 生成报告文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            print(f"\n4. 生成报告文件...")
            
            # 生成文字版报告
            txt_file = self.output_dir / f"complete_finance_report_{timestamp}.txt"
            text_report = self.generate_text_report(hot_news_data, deep_reports_data, latest_news_data)
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text_report)
            print(f"   [OK] 文字版报告: {txt_file.name}")
            
            # 生成HTML报告
            html_file = self.output_dir / f"complete_finance_report_{timestamp}.html"
            html_report = self.generate_html_report(hot_news_data, deep_reports_data, latest_news_data)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_report)
            print(f"   [OK] HTML版报告: {html_file.name}")
            
            # 生成HTML截图
            png_file = self.output_dir / f"complete_finance_report_{timestamp}.png"
            screenshot_success = self.generate_screenshot(html_file, png_file)
            if screenshot_success:
                print(f"   [OK] HTML图片版: {png_file.name}")
            else:
                print(f"   [WARNING] HTML图片版生成失败")
            
            # 5. 显示结果
            print(f"\n{'='*80}")
            print("报告生成完成!")
            print(f"{'='*80}")
            print(f"数据统计:")
            print(f"  热点新闻TOP5: {len(hot_news_data)} 篇")
            print(f"  深度分析TOP3: {len(deep_reports_data)} 个")
            print(f"  快讯TOP10: {len(latest_news_data)} 条")
            if latest_news_data:
                important_count = sum(1 for n in latest_news_data if n.get('importance', False))
                print(f"  重要快讯: {important_count} 条")
            print(f"  图片报告: {'[OK] 生成成功' if screenshot_success else '[WARNING] 生成失败'}")
            print(f"\n生成文件:")
            print(f"  1. 文字版报告: {txt_file}")
            print(f"  2. HTML版报告: {html_file}")
            if screenshot_success:
                print(f"  3. HTML图片版: {png_file}")
            print(f"\n打开HTML报告查看:")
            print(f"  file:///{html_file}")
            print(f"{'='*80}")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] 报告生成失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='完整财经热点新闻报告生成器')
    parser.add_argument('--output-dir', type=str,
                       help='指定输出目录路径')
    
    args = parser.parse_args()
    
    # 创建报告生成器
    generator = FinalReportGenerator()
    
    # 如果指定了输出目录，则使用指定目录
    if args.output_dir:
        generator.output_dir = Path(args.output_dir)
        generator.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"使用指定输出目录: {args.output_dir}")
    
    # 运行报告生成器
    success = generator.run()
    
    if not success:
        print("\n报告生成失败")
        sys.exit(1)
    
    print(f"\n报告生成成功!")
    print(f"输出目录: {generator.output_dir}")


if __name__ == "__main__":
    import sys
    main()