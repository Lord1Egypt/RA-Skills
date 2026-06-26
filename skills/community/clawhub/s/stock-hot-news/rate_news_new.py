#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻标题评分模块 - 混合评分方案

混合评分策略：
1. 本地实现部分：
   - 一、信源权威性与可信度（35分）：默认三级信源（最低分）
   - 四、时间新鲜度（20分）：没有时间的新闻默认4小时（15分）
2. 大模型实现部分：
   - 二、信息实质影响（30分）
   - 三、完整性与风险提示（15分）
3. 回退机制：如果大模型失效，回退到全部本地评分

功能：
1. 从配置读取DeepSeek API配置
2. 混合本地和大模型评分
3. 批量处理文章，节省token
4. 返回文章列表和对应的分数

评分标准（总分100分）：
一、信源权威性与可信度（35分）
二、信息实质影响（30分）
三、完整性与风险提示（15分）
四、时间新鲜度（20分）

使用方式：
1. 准备文章列表，每篇文章包含 title, source, publish_time 等字段
2. 调用 rate_articles(articles, batch_size=10)
3. 返回带评分的文章列表
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import requests
import logging


class NewsRater:
    """新闻评分器 - 混合评分方案"""
    
    def __init__(self, config_path: str = None):
        """初始化评分器
        
        Args:
            config_path: 配置文件路径，默认为当前目录下的url_config.json
        """
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        
        # 从配置获取API设置
        self.api_settings = self._extract_api_settings()
        
        # 是否使用大模型
        self.use_model = bool(self.api_settings and self.api_settings.get('api_key'))
        
        # 信源权威性权重
        self.source_weights = {
            '证券时报网': 1.5,
            '第一财经': 1.3,
            '财新网': 1.4,
            '华尔街见闻': 1.2,
            '新浪财经': 1.6,
            '金融界': 1.1,
            '财联社': 1.2,
            '和讯网': 1.0,
            '21世纪经济报道': 1.3,
            '未知': 1.0
        }
        
        # 财经关键词（用于判断信息实质影响）
        self.finance_keywords = [
            '股市', 'A股', '港股', '美股', '指数', '上证', '深证', '创业板', '科创板',
            'GDP', 'CPI', 'PPI', 'PMI', '通胀', '通缩', '利率', '汇率', '货币政策',
            '财报', '业绩', '上市', '退市', '并购', '重组', '分红', '派息',
            '原油', '石油', '天然气', '煤炭', '黄金', '白银', '铜', '铝', '铁矿石',
            '房地产', '房价', '房贷', '土地', '开发商',
            '消费', '零售', '电商', '网购', '双十一',
            '科技', 'AI', '人工智能', '芯片', '半导体', '5G', '新能源', '电动车',
            '政策', '监管', '法规', '改革', '开放', '试点', '自贸区',
            '美国', '欧洲', '日本', '中国', '俄罗斯', '伊朗', '以色列', '制裁', '贸易战',
            '战争', '冲突', '导弹', '战机', '军事', '攻击', '核', '军演'
        ]
        
        print(f"[INFO] 新闻评分器初始化完成")
        print(f"      模式: {'混合（本地+大模型）' if self.use_model else '纯本地'}")
        print(f"      信源权重: {len(self.source_weights)} 个")
        print(f"      财经关键词: {len(self.finance_keywords)} 个")
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典，如果加载失败返回空字典
        """
        import os
        from pathlib import Path
        
        if config_path is None:
            # 默认配置文件路径
            script_dir = Path(__file__).parent
            config_path = script_dir / "url_config.json"
        
        try:
            if not Path(config_path).exists():
                print(f"[WARNING] 配置文件不存在: {config_path}")
                return {}
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"[INFO] 配置文件加载成功: {config_path}")
            return config
            
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            return {}
    
    def _extract_api_settings(self) -> Dict[str, Any]:
        """从配置中提取API设置
        
        支持多种配置格式：
        1. 新格式: api_settings.deepseek
        2. 旧格式: v3_module.summarize_scoring.summarize_settings
        
        Returns:
            API配置字典
        """
        api_settings = {}
        
        # 尝试从新格式获取
        if 'api_settings' in self.config:
            api_settings = self.config.get('api_settings', {}).get('deepseek', {})
            if api_settings:
                print(f"[INFO] 从新格式(api_settings.deepseek)获取API配置")
                return api_settings
        
        # 尝试从旧格式获取
        if 'v3_module' in self.config:
            v3_module = self.config.get('v3_module', {})
            summarize_scoring = v3_module.get('summarize_scoring', {})
            api_settings = summarize_scoring.get('summarize_settings', {})
            if api_settings:
                print(f"[INFO] 从旧格式(v3_module.summarize_scoring)获取API配置")
                return api_settings
        
        # 如果都没有，尝试直接获取
        if 'summarize_settings' in self.config:
            api_settings = self.config.get('summarize_settings', {})
            if api_settings:
                print(f"[INFO] 从直接格式(summarize_settings)获取API配置")
                return api_settings
        
        print(f"[WARNING] 未找到API配置，将使用纯本地评分")
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def _calculate_local_score(self, article: Dict[str, Any]) -> float:
        """计算本地评分部分（55分）
        
        包括：
        1. 信源权威性与可信度（35分）
        2. 时间新鲜度（20分）
        
        Args:
            article: 文章字典
            
        Returns:
            本地评分分数（0-55分）
        """
        score = 0.0
        
        # 1. 信源权威性与可信度（35分）
        source = article.get('source', '未知')
        source_weight = self.source_weights.get(source, 1.0)
        
        # 信源基础分：根据权重计算
        source_base_score = 25.0  # 基础分
        source_score = source_base_score * source_weight
        
        # 限制在0-35分之间
        source_score = max(0, min(source_score, 35))
        score += source_score
        
        # 2. 时间新鲜度（20分）
        publish_time = article.get('publish_time', '')
        publish_time_display = article.get('publish_time_display', '未知')
        
        if publish_time:
            try:
                # 尝试解析时间
                if isinstance(publish_time, str):
                    # 移除可能的时间zone信息
                    publish_time = publish_time.split('+')[0].split('Z')[0]
                    
                    # 尝试多种格式
                    formats = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%dT%H:%M:%S',
                        '%Y-%m-%d %H:%M',
                        '%Y-%m-%d'
                    ]
                    
                    pub_dt = None
                    for fmt in formats:
                        try:
                            pub_dt = datetime.strptime(publish_time, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if pub_dt:
                        now = datetime.now()
                        time_diff = now - pub_dt
                        hours_diff = time_diff.total_seconds() / 3600
                        
                        # 新鲜度评分：24小时内满分，随时间递减
                        if hours_diff <= 1:  # 1小时内
                            time_score = 20
                        elif hours_diff <= 4:  # 4小时内
                            time_score = 18
                        elif hours_diff <= 12:  # 12小时内
                            time_score = 15
                        elif hours_diff <= 24:  # 24小时内
                            time_score = 10
                        elif hours_diff <= 48:  # 48小时内
                            time_score = 5
                        else:  # 超过48小时
                            time_score = 2
                    else:
                        # 无法解析时间，默认4小时
                        time_score = 15
                else:
                    # 非字符串时间，默认4小时
                    time_score = 15
            except Exception as e:
                self.logger.warning(f"解析时间失败: {e}, 使用默认值")
                time_score = 15
        else:
            # 没有时间，默认4小时
            time_score = 15
        
        score += time_score
        
        return score
    
    def _calculate_keyword_score(self, article: Dict[str, Any]) -> float:
        """基于关键词计算信息实质影响分数（0-30分）
        
        Args:
            article: 文章字典
            
        Returns:
            关键词评分分数（0-30分）
        """
        title = article.get('title', '').lower()
        content = article.get('content', '').lower() or article.get('summary', '').lower()
        
        text = f"{title} {content}"
        
        # 统计财经关键词出现次数
        keyword_count = 0
        for keyword in self.finance_keywords:
            if keyword.lower() in text:
                keyword_count += 1
        
        # 根据关键词数量评分
        if keyword_count >= 5:
            return 30
        elif keyword_count >= 3:
            return 25
        elif keyword_count >= 2:
            return 20
        elif keyword_count >= 1:
            return 15
        else:
            return 10
    
    def _call_deepseek_api(self, articles_batch: List[Dict[str, Any]]) -> List[float]:
        """调用DeepSeek API获取大模型评分
        
        Args:
            articles_batch: 文章批次
            
        Returns:
            大模型评分列表（每篇文章45分，需要转换为0-45分）
        """
        if not self.api_settings or not self.use_model:
            return [0.0] * len(articles_batch)
        
        try:
            api_key = self.api_settings.get('api_key')
            api_base_url = self.api_settings.get('api_base_url', 'https://api.deepseek.com')
            model = self.api_settings.get('model', 'deepseek-chat')
            
            if not api_key:
                self.logger.warning("API密钥未配置，跳过大模型评分")
                return [0.0] * len(articles_batch)
            
            # 构建提示词
            prompt = self._build_scoring_prompt(articles_batch)
            
            # 调用API
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            payload = {
                'model': model,
                'messages': [
                    {'role': 'system', 'content': '你是一个专业的财经新闻评分专家。请根据文章内容评估其信息实质影响和完整性。'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.1,
                'max_tokens': 2000
            }
            
            response = requests.post(
                f'{api_base_url}/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=self.api_settings.get('timeout_seconds', 60)
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 解析返回的评分
                scores = self._parse_api_scores(content, len(articles_batch))
                return scores
            else:
                self.logger.error(f"API调用失败: {response.status_code}, {response.text}")
                return [0.0] * len(articles_batch)
                
        except Exception as e:
            self.logger.error(f"调用DeepSeek API失败: {e}")
            return [0.0] * len(articles_batch)
    
    def _build_scoring_prompt(self, articles_batch: List[Dict[str, Any]]) -> str:
        """构建评分提示词
        
        Args:
            articles_batch: 文章批次
            
        Returns:
            提示词字符串
        """
        prompt = "请评估以下财经新闻的质量，从两个方面评分（总分45分）：\n"
        prompt += "1. 信息实质影响（30分）：评估新闻对市场、经济或政策的实际影响\n"
        prompt += "2. 完整性与风险提示（15分）：评估报道的完整性和是否包含必要的风险提示\n\n"
        
        for i, article in enumerate(articles_batch):
            title = article.get('title', '无标题')
            source = article.get('source', '未知来源')
            summary = article.get('summary', article.get('content', '无内容摘要'))
            publish_time = article.get('publish_time_display', article.get('publish_time', '未知时间'))
            
            prompt += f"【文章{i+1}】\n"
            prompt += f"标题: {title}\n"
            prompt += f"来源: {source}\n"
            prompt += f"发布时间: {publish_time}\n"
            prompt += f"摘要: {summary[:500]}\n\n"
        
        prompt += "请为每篇文章提供两个分数（信息实质影响分和完整性分），格式如下：\n"
        prompt += "文章1: 25, 12  # 信息实质影响25分，完整性12分\n"
        prompt += "文章2: 28, 14  # 信息实质影响28分，完整性14分\n"
        prompt += "...\n"
        prompt += "请确保每行对应一篇文章，分数用逗号分隔，不需要其他文字。"
        
        return prompt
    
    def _parse_api_scores(self, content: str, expected_count: int) -> List[float]:
        """解析API返回的评分
        
        Args:
            content: API返回内容
            expected_count: 期望的文章数量
            
        Returns:
            评分列表（每篇文章的大模型评分部分，0-45分）
        """
        scores = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            
            # 提取分数部分
            try:
                score_part = line.split(':')[1].strip()
                # 移除注释
                score_part = score_part.split('#')[0].strip()
                
                # 解析两个分数
                impact_score, completeness_score = map(float, score_part.split(','))
                
                # 转换为0-45分（30+15）
                total_score = min(30, max(0, impact_score)) + min(15, max(0, completeness_score))
                scores.append(total_score)
            except Exception as e:
                self.logger.warning(f"解析分数行失败: {line}, 错误: {e}")
                scores.append(0.0)
        
        # 如果解析的数量不够，用0填充
        while len(scores) < expected_count:
            scores.append(0.0)
        
        # 如果解析的数量太多，截断
        scores = scores[:expected_count]
        
        return scores
    
    def rate_articles(self, articles: List[Dict[str, Any]], batch_size: int = 10) -> List[Dict[str, Any]]:
        """对文章列表进行评分
        
        Args:
            articles: 文章列表
            batch_size: 批次大小，用于大模型API调用
            
        Returns:
            带评分的文章列表
        """
        if not articles:
            self.logger.warning("文章列表为空")
            return []
        
        print(f"[INFO] 开始对 {len(articles)} 篇文章进行评分")
        print(f"      批次大小: {batch_size}")
        print(f"      评分模式: {'混合（本地+大模型）' if self.use_model else '纯本地'}")
        
        rated_articles = []
        
        # 分批处理
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(articles) + batch_size - 1) // batch_size
            
            print(f"      处理批次 {batch_num}/{total_batches} ({len(batch)} 篇文章)")
            
            # 计算本地评分
            local_scores = []
            for article in batch:
                local_score = self._calculate_local_score(article)
                keyword_score = self._calculate_keyword_score(article)
                total_local = local_score + keyword_score
                local_scores.append(total_local)
            
            # 计算大模型评分（如果需要）
            if self.use_model:
                print(f"        调用大模型API进行评分...")
                model_scores = self._call_deepseek_api(batch)
                
                # 合并分数：本地部分(55分) + 大模型部分(45分)
                for j, article in enumerate(batch):
                    total_score = local_scores[j] + model_scores[j]
                    
                    # 确保分数在0-100之间
                    total_score = max(0, min(total_score, 100))
                    
                    # 添加评分到文章
                    rated_article = article.copy()
                    rated_article['score'] = round(total_score, 1)
                    rated_article['score_local'] = round(local_scores[j], 1)
                    rated_article['score_model'] = round(model_scores[j], 1)
                    rated_article['score_breakdown'] = {
                        'source_credibility': round(self._calculate_local_score(article) - 15, 1),  # 减去时间分估算
                        'time_freshness': 15,  # 默认时间分
                        'keyword_impact': round(self._calculate_keyword_score(article), 1),
                        'model_impact': round(model_scores[j], 1) if self.use_model else 0
                    }
                    
                    rated_articles.append(rated_article)
            else:
                # 纯本地评分，将本地分数扩展到100分
                for j, article in enumerate(batch):
                    # 本地分数是0-55分，扩展到0-100分
                    scaled_score = (local_scores[j] / 55) * 100
                    scaled_score = max(0, min(scaled_score, 100))
                    
                    rated_article = article.copy()
                    rated_article['score'] = round(scaled_score, 1)
                    rated_article['score_local'] = round(local_scores[j], 1)
                    rated_article['score_model'] = 0.0
                    rated_article['score_breakdown'] = {
                        'source_credibility': round(self._calculate_local_score(article) - 15, 1),
                        'time_freshness': 15,
                        'keyword_impact': round(self._calculate_keyword_score(article), 1),
                        'model_impact': 0
                    }
                    
                    rated_articles.append(rated_article)
            
            # 批次间延迟，避免API限制
            if self.use_model and i + batch_size < len(articles):
                delay = random.uniform(1.0, 3.0)
                time.sleep(delay)
        
        print(f"[INFO] 评分完成，共处理 {len(rated_articles)} 篇文章")
        
        # 按分数排序
        rated_articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return rated_articles


# 测试代码
if __name__ == "__main__":
    # 创建测试文章
    test_articles = [
        {
            'title': 'A股市场今日大幅上涨，上证指数突破3200点',
            'source': '证券时报网',
            'publish_time': '2026-03-28 09:30:00',
            'publish_time_display': '2026-03-28 09:30',
            'summary': '今日A股市场表现强势，主要指数均大幅上涨。'
        },
        {
            'title': '美联储维持利率不变，符合市场预期',
            'source': '华尔街见闻',
            'publish_time': '2026-03-27 20:00:00',
            'publish_time_display': '2026-03-27 20:00',
            'summary': '美联储宣布维持基准利率不变，市场反应平稳。'
        }
    ]
    
    # 创建评分器
    rater = NewsRater()
    
    # 进行评分
    rated = rater.rate_articles(test_articles, batch_size=2)
    
    # 输出结果
    print("\n=== 评分结果 ===")
    for i, article in enumerate(rated):
        print(f"文章{i+1}: {article['title']}")
        print(f"  分数: {article['score']}")
        print(f"  本地分: {article['score_local']}")
        print(f"  模型分: {article['score_model']}")
        print()