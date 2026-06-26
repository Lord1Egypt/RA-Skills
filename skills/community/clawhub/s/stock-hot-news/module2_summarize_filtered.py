#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 2: 热点新闻话题归纳模块 - 过滤版
添加过滤器，过滤掉无关内容，结合summarize和关键词过滤
"""

import os
import sys
import json
import re
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter

# 导入新闻评分模块
try:
    from rate_news_new import NewsRater
    RATE_NEWS_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 无法导入rate_news_new: {e}")
    RATE_NEWS_AVAILABLE = False

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TopicSummarizerFiltered:
    """话题归纳器（过滤版）"""
    
    def __init__(self):
        """初始化归纳器"""
        self.name = "话题归纳器（过滤版）"
        
        # 先设置默认路径，加载配置后会更新
        self.temp_dir = Path("c:/SelfData/claw_temp/temp/title_news_crawl/temp")
        self.output_dir = Path("c:/SelfData/claw_temp/temp/title_news_crawl/summarized")
        
        # 财经相关关键词（用于过滤）
        self.finance_keywords = [
            # 股市相关
            'A股', '股市', '股票', '指数', '上证', '深证', '创业板', '科创板', '北交所',
            '涨停', '跌停', '暴涨', '暴跌', '牛市', '熊市', '震荡', '调整',
            
            # 金融相关
            '银行', '保险', '证券', '基金', '信托', '理财', '信贷', '利率', '货币政策',
            '央行', '美联储', '欧央行', '日央行', '加息', '降息', '降准', '存款准备金',
            
            # 经济相关
            'GDP', '经济', '增长', '通胀', '通缩', 'CPI', 'PPI', 'PMI', '消费', '投资',
            '出口', '进口', '贸易', '顺差', '逆差', '外汇', '汇率', '人民币', '美元',
            
            # 科技相关
            'AI', '人工智能', '芯片', '半导体', '5G', '6G', '云计算', '大数据', '区块链',
            '数字经济', '数字化转型', '智能制造', '工业互联网', '物联网',
            
            # 产业相关
            '房地产', '楼市', '房价', '房贷', '汽车', '新能源车', '电动车', '自动驾驶',
            '能源', '石油', '天然气', '煤炭', '电力', '新能源', '太阳能', '风能', '核能',
            '医药', '医疗', '生物医药', '创新药', '医疗器械',
            
            # 政策相关
            '政策', '法规', '监管', '改革', '开放', '试点', '示范区', '自贸区', '自贸港',
            '十四五', '规划', '指导意见', '管理办法', '条例',
            
            # 公司相关
            '财报', '业绩', '上市', '退市', 'IPO', '并购', '重组', '收购', '合作', '签约',
            '利润', '营收', '净利润', '毛利率', '净利率',
            
            # 国际相关
            '美国', '欧洲', '日本', '韩国', '俄罗斯', '印度', '一带一路', '贸易战', '关税',
            '制裁', '地缘政治', '国际关系', '全球化', '产业链', '供应链',
            
            # 投资相关
            '投资', '融资', '估值', '市值', '市盈率', '市净率', 'ROE', 'ROA', '股息率',
            '资产配置', '风险投资', '私募', '公募', '量化', '对冲',
        ]
        
        # 需要过滤的无关内容关键词
        self.filter_keywords = [
            # 非财经内容
            '春季花粉', '过敏', '服务窗', '探访', '聚焦', '年会', '论坛', '会议', '活动',
            '展览', '展会', '比赛', '赛事', '娱乐', '明星', '影视', '音乐', '体育',
            '美食', '旅游', '健康', '养生', '教育', '培训', '学校', '考试',
            
            # 过于宽泛的内容
            '其他', '综合', '杂谈', '随笔', '评论', '观点', '观察', '思考',
            
            # 广告和推广
            '广告', '推广', '营销', '促销', '优惠', '打折', '特价', '团购',
        ]
        
        # 加载配置文件
        self.config = self.load_config()
        if self.config:
            print(f"[INFO] 配置文件加载成功")
            
            # 从配置文件读取路径设置
            system_settings = self.config.get('system_settings', {})
            if system_settings:
                # 获取temp_dir目录
                temp_dir = system_settings.get('temp_dir', 'c:/SelfData/claw_temp/temp')
                if temp_dir:
                    # 在temp_dir下创建title_news_crawl子目录
                    base_dir = Path(temp_dir) / "title_news_crawl"
                    self.temp_dir = base_dir / "temp"
                    self.output_dir = base_dir / "summarized"
                    print(f"[INFO] 从配置文件加载路径:")
                    print(f"  temp_dir: {self.temp_dir}")
                    print(f"  output_dir: {self.output_dir}")
                else:
                    print(f"[WARNING] 配置文件中未找到temp_dir路径，使用默认路径")
            else:
                print(f"[WARNING] 配置文件中未找到system_settings，使用默认路径")
            
            # 创建目录
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 提取summarize配置（支持新旧配置结构）
            # 旧结构: v3_module.summarize_scoring.summarize_settings
            # 新结构: api_settings.deepseek
            old_summarize_config = self.config.get('v3_module', {}).get('summarize_scoring', {})
            old_summarize_settings = old_summarize_config.get('summarize_settings', {})
            
            # 新结构配置
            api_settings = self.config.get('api_settings', {})
            deepseek_config = api_settings.get('deepseek', {})
            
            # 合并配置（新结构优先）
            self.summarize_settings = {}
            if old_summarize_settings:
                self.summarize_settings.update(old_summarize_settings)
                print(f"[INFO] 从旧结构加载summarize配置")
            if deepseek_config:
                self.summarize_settings.update(deepseek_config)
                print(f"[INFO] 从新结构加载deepseek API配置")
            
            print(f"[INFO] summarize配置加载完成")
        else:
            print(f"[WARNING] 配置文件加载失败，使用默认配置")
            self.summarize_settings = {}
            # 使用默认路径并创建目录
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化SummarizeManager
        try:
            from summarize_utils import SummarizeManager
            self.summarize_manager = SummarizeManager(self.summarize_settings)
            print(f"[INFO] SummarizeManager初始化成功")
        except Exception as e:
            print(f"[WARNING] SummarizeManager初始化失败: {e}")
            self.summarize_manager = None
        
        print(f"{self.name} 初始化完成")
        print(f"临时目录: {self.temp_dir}")
        print(f"输出目录: {self.output_dir}")
        print(f"财经关键词数量: {len(self.finance_keywords)} 个")
        print(f"过滤关键词数量: {len(self.filter_keywords)} 个")
        print(f"配置文件状态: {'已加载' if self.config else '未加载'}")
        print(f"SummarizeManager状态: {'可用' if self.summarize_manager else '不可用'}")
        print("-" * 70)
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        try:
            config_path = Path(__file__).parent / "url_config.json"
            if not config_path.exists():
                print(f"[WARNING] 配置文件不存在: {config_path}")
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"[INFO] 配置文件加载成功: {config_path.name}")
            return config
            
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            return None
    
    def find_latest_input_file(self) -> Optional[Path]:
        """查找最新的module1输出文件"""
        pattern = "main_sites_news_*.json"
        files = list(self.temp_dir.glob(pattern))
        
        if not files:
            print(f"[ERROR] 在 {self.temp_dir} 中未找到module1输出文件")
            return None
        
        # 按修改时间排序，获取最新的文件
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        print(f"找到最新输入文件: {latest_file.name}")
        print(f"修改时间: {datetime.fromtimestamp(latest_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        return latest_file
    
    def load_and_filter_articles(self, input_file: Path) -> List[Dict[str, Any]]:
        """加载并过滤文章数据"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            articles = data.get('articles', [])
            metadata = data.get('metadata', {})
            
            print(f"加载原始文章数据:")
            print(f"  来源: {metadata.get('source', '未知')}")
            print(f"  爬取时间: {metadata.get('crawl_time', '未知')}")
            print(f"  网站数量: {metadata.get('site_count', 0)} 个")
            print(f"  原始文章数量: {len(articles)} 篇")
            print(f"  时间过滤: {metadata.get('time_filter', '未知')}")
            
            # 过滤文章
            filtered_articles = []
            removed_count = 0
            
            for article in articles:
                title = article.get('title', '')
                content = article.get('content', '') or article.get('summary', '')
                
                # 检查1: 标题长度是否太短
                if len(title) < 5:
                    removed_count += 1
                    continue
                
                # 检查2: 是否包含过滤关键词
                title_lower = title.lower()
                if any(keyword.lower() in title_lower for keyword in self.filter_keywords):
                    removed_count += 1
                    continue
                
                # 检查3: 是否包含财经关键词
                text = f"{title} {content}"
                text_lower = text.lower()
                
                # 检查是否包含财经关键词
                has_finance_keyword = False
                for keyword in self.finance_keywords:
                    if keyword.lower() in text_lower:
                        has_finance_keyword = True
                        break
                
                if not has_finance_keyword:
                    removed_count += 1
                    continue
                
                # 通过所有检查，添加到过滤后的列表
                filtered_articles.append(article)
            
            print(f"过滤后文章数据:")
            print(f"  保留文章数量: {len(filtered_articles)} 篇")
            print(f"  过滤掉文章数量: {removed_count} 篇")
            print(f"  过滤比例: {removed_count/len(articles)*100:.1f}%")
            
            return filtered_articles
            
        except Exception as e:
            print(f"[ERROR] 加载文件失败: {type(e).__name__}: {e}")
            return []
    
    def group_articles_by_topic(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """根据标题关键词对文章进行初步分组（改进版）"""
        print("开始对文章进行话题分组...")
        
        # 定义更精确的话题关键词
        topic_keywords = {
            '股市动态': ['A股', '股市', '股票', '指数', '上证', '深证', '创业板', '科创板', '北交所', '涨停', '跌停'],
            '金融政策': ['银行', '保险', '证券', '基金', '央行', '货币政策', '利率', '信贷', '监管'],
            '宏观经济': ['GDP', '经济', '增长', '通胀', 'CPI', 'PPI', 'PMI', '消费', '投资', '出口'],
            '科技创新': ['AI', '人工智能', '芯片', '半导体', '5G', '6G', '云计算', '大数据', '区块链', '数字经济'],
            '房地产市场': ['房地产', '楼市', '房价', '房贷', '土地', '开发商', '物业'],
            '汽车产业': ['汽车', '新能源车', '电动车', '自动驾驶', '特斯拉', '比亚迪', '蔚来'],
            '能源市场': ['石油', '天然气', '煤炭', '电力', '新能源', '太阳能', '风能', '核能'],
            '国际贸易': ['美国', '欧洲', '日本', '贸易', '关税', '制裁', '一带一路', '全球化'],
            '公司财报': ['财报', '业绩', '上市', 'IPO', '并购', '重组', '利润', '营收'],
            '投资理财': ['投资', '融资', '估值', '市值', '理财', '资产配置', '风险投资'],
        }
        
        # 初始化话题组
        topic_groups = {topic: [] for topic in topic_keywords.keys()}
        topic_groups['其他财经'] = []  # 其他财经相关但未明确分类的文章
        
        for article in articles:
            title = article.get('title', '').lower()
            matched = False
            
            for topic, keywords in topic_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in title:
                        topic_groups[topic].append(article)
                        matched = True
                        break
                if matched:
                    break
            
            if not matched:
                # 检查是否至少包含一个财经关键词
                text = f"{title} {article.get('content', '')}"
                text_lower = text.lower()
                
                has_finance = False
                for keyword in self.finance_keywords:
                    if keyword.lower() in text_lower:
                        has_finance = True
                        break
                
                if has_finance:
                    topic_groups['其他财经'].append(article)
                # 否则完全过滤掉（不添加到任何组）
        
        # 统计分组结果
        print(f"话题分组完成:")
        total_articles = 0
        for topic, articles_in_topic in topic_groups.items():
            if articles_in_topic:
                print(f"  {topic}: {len(articles_in_topic)} 篇文章")
                total_articles += len(articles_in_topic)
        
        print(f"  总计分组文章: {total_articles} 篇")
        
        # 移除空的话题组
        topic_groups = {k: v for k, v in topic_groups.items() if v}
        
        return topic_groups
    
    def create_topic_summary_prompt(self, topic: str, articles: List[Dict[str, Any]]) -> str:
        """创建话题归纳提示词（改进版）"""
        # 收集文章标题和来源
        article_info = []
        for i, article in enumerate(articles[:8], 1):  # 最多8篇文章
            title = article.get('title', '')
            source = article.get('source', '未知来源')
            publish_time = article.get('publish_time', '')
            article_info.append(f"{i}. [{source}] {title} ({publish_time})")
        
        prompt = f"""请为以下关于"{topic}"的财经新闻进行专业的归纳总结：

相关文章信息:
{chr(10).join(article_info)}

要求:
1. 生成一个专业、准确的财经话题总结（120-180字）
2. 提取3-5个核心关键观点
3. 分析对市场、行业或经济的可能影响
4. 提供专业的未来展望或投资建议
5. 用中文输出，保持专业财经分析的语气

请以JSON格式返回结果，包含以下字段:
- topic: 话题名称
- summary: 专业的话题总结
- key_points: 核心关键观点列表（每个观点20-40字）
- impact: 影响分析（50-100字）
- outlook: 未来展望（50-100字）"""
        
        return prompt
    
    def summarize_with_cli(self, prompt: str) -> Optional[Dict[str, Any]]:
        """使用summarize CLI进行归纳（从配置文件读取API key和URL）"""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(prompt)
                temp_file = f.name
            
            # 获取配置中的API key和URL
            api_key = self.summarize_settings.get('api_key', '')
            api_base_url = self.summarize_settings.get('api_base_url', '')
            
            if not api_key or not api_base_url:
                print(f"  [WARNING] 配置中缺少API key或base URL，使用默认值")
                # 尝试从环境变量获取
                print(f"api_key 和 base URL 缺失!!")
            
            # 设置环境变量
            env = os.environ.copy()
            env['OPENAI_API_KEY'] = api_key
            env['OPENAI_BASE_URL'] = api_base_url
            
            # 确定summarize命令路径
            summarize_cmd = 'summarize'  # 默认命令
            if self.summarize_manager and hasattr(self.summarize_manager, 'summarize_path'):
                if self.summarize_manager.summarize_path:
                    summarize_cmd = self.summarize_manager.summarize_path
                    print(f"  使用summarize路径: {summarize_cmd}")
            
            # 构建命令
            cmd = []
            if summarize_cmd.endswith('.ps1'):
                # PowerShell脚本
                # 根据错误信息，--max-tokens参数不被支持，尝试使用--maxTokens或去掉
                cmd = [
                    'powershell',
                    '-Command',
                    f'& "{summarize_cmd}" --model {self.summarize_settings.get("model", "deepseek-chat")} '
                    f'--format json --maxTokens 600 "{temp_file}"'
                ]
                print(f"  使用PowerShell命令格式 (maxTokens替代max-tokens)")
            else:
                # 普通可执行文件
                cmd = [
                    summarize_cmd,
                    temp_file,
                    '--model', self.summarize_settings.get('model', 'deepseek-chat'),
                    '--format', 'json',
                    '--maxTokens', '600'  # 改为camelCase格式
                ]
            
            # 如果配置中指定了其他参数，可以添加
            if self.summarize_settings.get('length'):
                if summarize_cmd.endswith('.ps1'):
                    # PowerShell命令需要重新构建
                    pass  # 暂时不处理
                else:
                    cmd.extend(['--length', self.summarize_settings.get('length')])
            
            print(f"  执行summarize命令: {' '.join(cmd[:3])}...")
            print(f"  使用API base URL: {api_base_url}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=self.summarize_settings.get('timeout_seconds', 60),
                env=env,
                shell=True
            )
            
            # 清理临时文件
            os.unlink(temp_file)
            
            if result.returncode != 0:
                print(f"  [WARNING] summarize CLI失败，返回码: {result.returncode}")
                if result.stderr:
                    print(f"  错误信息: {result.stderr[:200]}")
                return None
            
            # 解析JSON输出
            try:
                output = result.stdout.strip()
                summary_data = json.loads(output)
                
                # 检查返回的格式
                if 'summary' in summary_data:
                    print(f"  summarize调用成功，总结长度: {len(summary_data.get('summary', ''))} 字")
                    return summary_data
                else:
                    print(f"  [WARNING] summarize输出缺少summary字段")
                    # 可能返回了其他格式，尝试使用整个输出
                    if isinstance(summary_data, dict):
                        return summary_data
                    else:
                        return None
                    
            except json.JSONDecodeError as e:
                print(f"  [WARNING] 解析JSON失败: {e}")
                print(f"  原始输出: {result.stdout[:200]}...")
                return None
                
        except FileNotFoundError:
            print(f"  [ERROR] summarize CLI未找到，请确保已安装summarize工具")
            return None
        except subprocess.TimeoutExpired:
            print(f"  [ERROR] summarize CLI超时")
            return None
        except Exception as e:
            print(f"  [ERROR] summarize CLI异常: {type(e).__name__}: {e}")
            return None
    
    def summarize_with_fallback(self, topic: str, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """备用归纳方法（当summarize不可用时）- 生成80-120字总结"""
        print(f"  使用备用方法归纳话题: {topic}")
        
        # 提取文章中的关键词
        all_text = ' '.join([article.get('title', '') + ' ' + (article.get('content', '') or article.get('summary', '')) 
                           for article in articles[:8]])
        
        # 简单的关键词提取
        words = re.findall(r'[\u4e00-\u9fff]{2,}', all_text)
        word_counts = Counter(words)
        top_keywords = [word for word, count in word_counts.most_common(15) 
                       if len(word) >= 2 and word not in ['相关', '市场', '政策', '公司', '行业', '企业', '投资', '分析', '新闻', '报道']]
        
        # 提取关键信息
        sources = set(article.get('source', '未知') for article in articles[:5])
        article_count = len(articles)
        
        # 生成80-120字的详细总结
        summary_parts = []
        summary_parts.append(f"近期{topic}领域出现重要动态，相关报道共计{article_count}篇。")
        
        if top_keywords:
            summary_parts.append(f"涉及{', '.join(top_keywords[:5])}等方面。")
        
        if sources:
            source_list = list(sources)[:3]
            if len(sources) > 3:
                summary_parts.append(f"信息来源包括{', '.join(source_list)}等{len(sources)}个不同来源。")
            else:
                summary_parts.append(f"信息来源包括{', '.join(source_list)}。")
        
        summary_parts.append("这对相关行业和市场可能产生重要影响，投资者需密切关注后续政策动向和市场反应。")
        summary_parts.append("建议关注相关板块的后续发展，并结合宏观经济环境进行综合判断。")
        
        summary = ' '.join(summary_parts)
        
        # 确保总结长度在80-120字左右
        if len(summary) < 80:
            # 添加一些通用内容
            summary += "当前市场环境复杂，需谨慎评估风险与机遇，保持理性投资态度。"
        elif len(summary) > 120:
            # 截断
            summary = summary[:115] + "..."
        
        # 生成关键观点
        key_points = []
        if article_count >= 3:
            key_points.append(f"{topic}领域近期出现多个重要发展，显示行业动态活跃。")
            key_points.append(f"政策面和市场面的双重影响可能对相关板块产生结构性变化。")
            key_points.append(f"投资者应关注基本面变化，同时注意风险控制和资产配置。")
        
        # 生成影响分析和展望
        impact = f"{topic}相关动态可能对产业链上下游产生影响，涉及多个行业板块。市场情绪可能因此波动，需要关注资金流向和政策信号。"
        outlook = f"未来一段时间，{topic}领域预计将继续受到关注。建议投资者保持关注，结合宏观数据和行业趋势进行判断，把握结构性机会。"
        
        return {
            'topic': topic,
            'summary': summary,
            'key_points': key_points,
            'impact': impact,
            'outlook': outlook
        }
    
    def score_topic(self, topic: str, articles: List[Dict[str, Any]], summary_data: Dict[str, Any]) -> float:
        """计算话题评分（改进版）"""
        score = 0.0
        
        # 1. 文章数量（最高5分）
        article_count = len(articles)
        if article_count >= 10:
            score += 5.0
        elif article_count >= 5:
            score += 3.0
        elif article_count >= 3:
            score += 2.0
        elif article_count >= 1:
            score += 1.0
        
        # 2. 来源多样性（最高3分）
        sources = set(article.get('source', '') for article in articles)
        source_count = len(sources)
        if source_count >= 3:
            score += 3.0
        elif source_count >= 2:
            score += 2.0
        elif source_count >= 1:
            score += 1.0
        
        # 3. 总结质量（最高2分）
        summary = summary_data.get('summary', '')
        if len(summary) > 100:
            score += 2.0
        elif len(summary) > 50:
            score += 1.0
        
        # 4. 关键观点数量（最高2分）
        key_points = summary_data.get('key_points', [])
        if len(key_points) >= 3:
            score += 2.0
        elif len(key_points) >= 1:
            score += 1.0
        
        # 5. 话题重要性（基于关键词匹配，最高3分）
        important_keywords = ['A股', '股市', '央行', '政策', '经济', 'GDP', '通胀', '利率', '贸易', '科技']
        topic_lower = topic.lower()
        text = ' '.join([article.get('title', '') for article in articles[:3]])
        text_lower = text.lower()
        
        for keyword in important_keywords:
            if keyword.lower() in topic_lower or keyword.lower() in text_lower:
                score += 0.5  # 每个重要关键词加0.5分，最多3分
        
        # 限制在0-15分之间
        return min(max(score, 0.0), 15.0)
    
    def summarize_all_topics(self, topic_groups: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """归纳所有话题（改进版）"""
        print(f"\n开始归纳所有话题...")
        
        summarized_topics = []
        
        for topic, articles in topic_groups.items():
            print(f"\n归纳话题: {topic} ({len(articles)} 篇文章)")
            
            # 1. 创建提示词
            prompt = self.create_topic_summary_prompt(topic, articles)
            
            # 2. 使用summarize CLI进行归纳
            summary_data = self.summarize_with_cli(prompt)
            
            # 3. 如果summarize失败，使用备用方法
            if not summary_data:
                print(f"  [WARNING] summarize失败，使用备用方法")
                summary_data = self.summarize_with_fallback(topic, articles)
            
            # 确保summary_data是一个字典
            if not isinstance(summary_data, dict):
                print(f"  [ERROR] summary_data不是字典类型: {type(summary_data)}")
                summary_data = {
                    'summary': f'{topic}相关新闻总结',
                    'key_points': [f'{topic}领域出现重要动态'],
                    'impact': '对市场可能产生影响',
                    'outlook': '建议关注后续发展'
                }
            
            # 4. 计算话题评分
            topic_score = self.score_topic(topic, articles, summary_data)
            
            # 5. 构建完整的话题总结
            topic_summary = {
                'topic': topic,
                'summary': summary_data.get('summary', ''),
                'key_points': summary_data.get('key_points', []),
                'impact': summary_data.get('impact', ''),
                'outlook': summary_data.get('outlook', ''),
                'score': topic_score,
                'article_count': len(articles),
                'sources': list(set(article.get('source', '') for article in articles)),
                'representative_articles': articles[:3]  # 前3篇作为代表性文章
            }
            
            summarized_topics.append(topic_summary)
            
            print(f"  归纳完成! 评分: {topic_score:.2f}")
            summary_text = topic_summary.get('summary', '')
            if len(summary_text) > 80:
                print(f"  总结: {summary_text[:80]}...")
            else:
                print(f"  总结: {summary_text}")
        
        print(f"\n话题归纳完成! 总共归纳了 {len(summarized_topics)} 个话题")
        
        return summarized_topics
    
    def get_top_topics(self, summarized_topics: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """获取评分最高的话题"""
        # 过滤掉无效的话题（缺少必要字段）
        valid_topics = []
        for topic in summarized_topics:
            if not isinstance(topic, dict):
                print(f"  [WARNING] 跳过非字典类型的话题: {type(topic)}")
                continue
            
            # 确保话题包含必需的字段
            if 'topic' not in topic:
                print(f"  [WARNING] 话题缺少'topic'键，添加默认值")
                topic['topic'] = '未知话题'
            
            if 'score' not in topic:
                print(f"  [WARNING] 话题缺少'score'键，设置默认值0")
                topic['score'] = 0.0
            
            valid_topics.append(topic)
        
        if not valid_topics:
            print(f"  [WARNING] 没有有效的话题数据")
            return []
        
        # 按评分降序排序
        sorted_topics = sorted(valid_topics, key=lambda x: x.get('score', 0), reverse=True)
        
        # 获取前N名
        top_topics = sorted_topics[:top_n]
        
        print(f"\n获取前 {top_n} 名热点话题:")
        for i, topic in enumerate(top_topics, 1):
            topic_name = topic.get('topic', '未知话题')
            topic_score = topic.get('score', 0.0)
            print(f"  {i}. {topic_name} - 评分: {topic_score:.2f}")
            
            summary_text = topic.get('summary', '')
            if len(summary_text) > 60:
                print(f"     总结: {summary_text[:60]}...")
            else:
                print(f"     总结: {summary_text}")
            
            article_count = topic.get('article_count', 0)
            sources = topic.get('sources', [])
            if sources:
                print(f"     文章数: {article_count} | 来源: {', '.join(sources)[:50]}")
            else:
                print(f"     文章数: {article_count} | 来源: 未知")
        
        return top_topics
    
    def save_top_topics(self, top_topics: List[Dict[str, Any]], top_n: int = 5):
        """保存前N名话题"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f"top_{top_n}_topics_{timestamp}.json"
        
        output_data = {
            'metadata': {
                'module': '热点新闻话题归纳模块（过滤版）',
                'summarize_time': datetime.now().isoformat(),
                'top_n': top_n,
                'filter_applied': True,
                'finance_keywords_count': len(self.finance_keywords),
                'filter_keywords_count': len(self.filter_keywords)
            },
            'topics': top_topics
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n前{top_n}名热点话题已保存: {output_file}")
        return output_file

    def generate_deep_analysis(self, output_file: Path, max_urls: int = 3):
        """生成深度分析报告（使用summarize技能）
        
        Args:
            output_file: 已保存的话题结果文件路径
            max_urls: 最多分析多少个URL（默认前3个）
        """
        print(f"\n{'='*70}")
        print(f"开始生成深度分析报告")
        print(f"{'='*70}")
        
        if not output_file.exists():
            print(f"[ERROR] 输出文件不存在: {output_file}")
            return None
        
        # 读取openclaw配置中的deepseek API设置
        openclaw_config_path = Path.home() / '.openclaw' / 'openclaw.json'
        deepseek_api_key = None
        deepseek_base_url = None
        
        if openclaw_config_path.exists():
            try:
                with open(openclaw_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 提取deepseek配置
                deepseek_config = config.get('models', {}).get('providers', {}).get('deepseek-com', {})
                deepseek_api_key = deepseek_config.get('apiKey')
                deepseek_base_url = deepseek_config.get('baseUrl')
                
                if deepseek_api_key and deepseek_base_url:
                    print(f"  已加载openclaw deepseek配置:")
                    print(f"    API Key: {deepseek_api_key[:5]}...{deepseek_api_key[-4:]}")
                    print(f"    Base URL: {deepseek_base_url}")
                else:
                    print(f"  [WARNING] openclaw配置中未找到完整的deepseek API配置")
                    print(f"    使用默认环境变量")
            except Exception as e:
                print(f"  [WARNING] 读取openclaw配置失败: {e}")
                print(f"    使用默认环境变量")
        else:
            print(f"  [WARNING] openclaw配置文件不存在: {openclaw_config_path}")
            print(f"    使用默认环境变量")
        
        try:
            # 读取输出文件
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            topics = data.get('topics', [])
            if not topics:
                print("[WARNING] 无话题数据，跳过深度分析")
                return None
            
            # 提取前max_urls个URL
            urls_to_analyze = []
            for i, topic in enumerate(topics[:max_urls]):
                articles = topic.get('articles', [])
                if articles:
                    # 取第一个文章的URL
                    article = articles[0]
                    url = article.get('url')
                    if url:
                        urls_to_analyze.append({
                            'topic_index': i,
                            'topic_title': topic.get('topic', f'话题{i+1}'),
                            'url': url,
                            'score': topic.get('score', 0)
                        })
            
            if not urls_to_analyze:
                print(f"[WARNING] 未找到可分析的URL，跳过深度分析")
                return None
            
            print(f"  找到 {len(urls_to_analyze)} 个URL进行深度分析")
            
            # 分析结果列表
            analysis_results = []
            
            # 检查summarize命令是否可用
            try:
                import subprocess
                result = subprocess.run(['summarize', '--version'], 
                                       capture_output=True, text=True, timeout=5, shell=True)
                summarize_available = result.returncode == 0
            except Exception:
                summarize_available = False
            
            if not summarize_available:
                print(f"[WARNING] summarize CLI不可用，跳过深度分析")
                print(f"  请安装: brew install steipete/tap/summarize 或 pip install summarize-sh")
                return None
            
            # 对每个URL进行分析
            for i, url_info in enumerate(urls_to_analyze):
                url = url_info['url']
                print(f"\n  [{i+1}/{len(urls_to_analyze)}] 分析URL: {url}")
                
                try:
                    # 调用summarize命令，生成80-120字的深度分析
                    # 使用--length medium（大约100-200字）或指定字符数
                    # 使用openclaw配置中的deepseek API
                    cmd = ['summarize', url, '--length', 'medium', '--json', '--model', 'openai/deepseek-chat']
                    
                    print(f"    执行命令: {' '.join(cmd)}")
                    
                    # 准备环境变量
                    env = os.environ.copy()
                    if deepseek_api_key:
                        env['OPENAI_API_KEY'] = deepseek_api_key
                    if deepseek_base_url:
                        env['OPENAI_BASE_URL'] = deepseek_base_url
                    
                    print(f"    环境变量: OPENAI_API_KEY={deepseek_api_key[:10]}...{deepseek_api_key[-4:] if deepseek_api_key else '未设置'}")
                    print(f"               OPENAI_BASE_URL={deepseek_base_url}")
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        timeout=60,  # 60秒超时
                        shell=True,
                        env=env
                    )
                    
                    if result.returncode == 0:
                        # 解析JSON输出
                        try:
                            summary_data = json.loads(result.stdout)
                            analysis_text = summary_data.get('summary', '').strip()
                            
                            # 如果没有summary字段，尝试其他字段
                            if not analysis_text and 'text' in summary_data:
                                analysis_text = summary_data.get('text', '').strip()
                            
                            # 限制长度在80-120字左右
                            words = analysis_text.split()
                            if len(words) > 120:
                                analysis_text = ' '.join(words[:120]) + '...'
                            elif len(words) < 80:
                                # 如果太短，保留原样
                                pass
                            
                            analysis_results.append({
                                'topic_index': url_info['topic_index'],
                                'topic_title': url_info['topic_title'],
                                'url': url,
                                'score': url_info['score'],
                                'analysis': analysis_text,
                                'word_count': len(analysis_text.split()),
                                'timestamp': datetime.now().isoformat(),
                                'status': 'success'
                            })
                            
                            print(f"    分析成功，字数: {len(analysis_text.split())}")
                            
                        except json.JSONDecodeError:
                            # 如果输出不是JSON，使用原始输出
                            analysis_text = result.stdout.strip()
                            if not analysis_text:
                                analysis_text = result.stderr.strip()
                            
                            analysis_results.append({
                                'topic_index': url_info['topic_index'],
                                'topic_title': url_info['topic_title'],
                                'url': url,
                                'score': url_info['score'],
                                'analysis': analysis_text[:500],  # 截断
                                'word_count': len(analysis_text.split()),
                                'timestamp': datetime.now().isoformat(),
                                'status': 'success_non_json'
                            })
                            print(f"    分析成功（非JSON输出），字数: {len(analysis_text.split())}")
                    
                    else:
                        print(f"    [ERROR] summarize命令失败，返回码: {result.returncode}")
                        print(f"    错误输出: {result.stderr[:200]}")
                        analysis_results.append({
                            'topic_index': url_info['topic_index'],
                            'topic_title': url_info['topic_title'],
                            'url': url,
                            'score': url_info['score'],
                            'analysis': f"分析失败: {result.stderr[:200]}",
                            'word_count': 0,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'error'
                        })
                
                except subprocess.TimeoutExpired:
                    print(f"    [ERROR] 分析超时（60秒）")
                    analysis_results.append({
                        'topic_index': url_info['topic_index'],
                        'topic_title': url_info['topic_title'],
                        'url': url,
                        'score': url_info['score'],
                        'analysis': "分析超时（60秒）",
                        'word_count': 0,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'timeout'
                    })
                except Exception as e:
                    print(f"    [ERROR] 分析过程中出错: {e}")
                    analysis_results.append({
                        'topic_index': url_info['topic_index'],
                        'topic_title': url_info['topic_title'],
                        'url': url,
                        'score': url_info['score'],
                        'analysis': f"分析错误: {str(e)[:200]}",
                        'word_count': 0,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'error'
                    })
            
            # 保存分析报告
            if analysis_results:
                analysis_file = output_file.parent / f"deep_analysis_{output_file.stem}.json"
                analysis_data = {
                    'metadata': {
                        'module': '深度分析报告',
                        'generated_time': datetime.now().isoformat(),
                        'source_file': output_file.name,
                        'urls_analyzed': len(analysis_results),
                        'successful_analyses': sum(1 for r in analysis_results if r['status'] == 'success'),
                        'failed_analyses': sum(1 for r in analysis_results if r['status'] in ['error', 'timeout'])
                    },
                    'analyses': analysis_results
                }
                
                with open(analysis_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis_data, f, ensure_ascii=False, indent=2)
                
                print(f"\n{'='*70}")
                print(f"深度分析报告已保存")
                print(f"{'='*70}")
                print(f"报告文件: {analysis_file}")
                print(f"分析URL数量: {len(analysis_results)}")
                print(f"成功分析: {sum(1 for r in analysis_results if r['status'] == 'success')}")
                print(f"失败分析: {sum(1 for r in analysis_results if r['status'] in ['error', 'timeout'])}")
                print(f"{'='*70}")
                
                # 显示分析摘要
                print(f"\n分析摘要:")
                for i, result in enumerate(analysis_results):
                    status_marker = '[OK]' if result['status'] == 'success' else '[ERROR]'
                    print(f"  {i+1}. {status_marker} {result['topic_title'][:50]}...")
                    print(f"     字数: {result['word_count']}, 状态: {result['status']}")
                    if result['status'] == 'success' and result['analysis']:
                        preview = result['analysis'][:100] + ('...' if len(result['analysis']) > 100 else '')
                        print(f"     预览: {preview}")
                
                return analysis_file
            else:
                print(f"\n[WARNING] 未生成任何分析结果")
                return None
                
        except Exception as e:
            print(f"\n[ERROR] 生成深度分析报告失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def run(self, top_n: int = 5):
        """运行话题归纳流程（过滤版）"""
        print(f"\n{'='*70}")
        print(f"运行话题归纳流程（过滤版）")
        print(f"{'='*70}")
        
        start_time = time.time()
        
        try:
            # 1. 查找输入文件
            print("\n1. 查找输入文件...")
            input_file = self.find_latest_input_file()
            if not input_file:
                return None, None
            
            # 2. 加载并过滤文章
            print("\n2. 加载并过滤文章数据...")
            articles = self.load_and_filter_articles(input_file)
            if not articles:
                print("[ERROR] 无文章数据或所有文章都被过滤")
                return None, None
            
            # 3. 对文章质量进行评分
            print("\n3. 对文章质量进行评分...")
            if not RATE_NEWS_AVAILABLE:
                print("[ERROR] rate_news_new模块不可用，无法进行评分")
                return None, None
            
            try:
                # 使用修复配置的评分器
                class FixedNewsRater(NewsRater):
                    def _load_config(self, config_path=None):
                        # 首先尝试从父类加载配置
                        parent_config = super()._load_config(config_path)
                        
                        # 检查是否有API配置
                        if parent_config and self._has_api_config(parent_config):
                            print("[INFO] FixedNewsRater: 使用配置文件中的API设置")
                            return parent_config
                        
                        # 如果没有API配置，使用占位符配置并提示用户
                        print("[WARNING] FixedNewsRater: 未找到有效的API配置，使用占位符配置")
                        print("[INFO] 请在url_config.json中配置您的DeepSeek API密钥")
                        return {
                            "summarize_scoring": {
                                "summarize_settings": {
                                    "api_key": "你的API KEY",
                                    "api_base_url": "https://api.deepseek.com",
                                    "model": "deepseek-chat"
                                }
                            }
                        }
                    
                    def _has_api_config(self, config):
                        """检查配置中是否有有效的API设置"""
                        # 检查新格式: api_settings.deepseek
                        if 'api_settings' in config:
                            deepseek_config = config.get('api_settings', {}).get('deepseek', {})
                            if deepseek_config.get('api_key') and deepseek_config.get('api_key') != '你的API KEY':
                                return True
                        
                        # 检查旧格式: summarize_scoring.summarize_settings
                        if 'summarize_scoring' in config:
                            settings = config.get('summarize_scoring', {}).get('summarize_settings', {})
                            if settings.get('api_key') and settings.get('api_key') != '你的API KEY':
                                return True
                        
                        return False
                
                rater = FixedNewsRater()
                print(f"  评分器初始化成功，模式: {'混合（本地+大模型）' if rater.use_model else '纯本地'}")
                
                # 对文章进行评分
                print(f"  开始对 {len(articles)} 篇文章进行评分...")
                rated_articles = rater.rate_articles(articles, batch_size=5)
                
                if not rated_articles:
                    print("[ERROR] 文章评分失败")
                    return None, None
                
                print(f"  评分完成，共处理 {len(rated_articles)} 篇文章")
                
                # 显示评分统计
                scores = [a.get('score', 0) for a in rated_articles]
                if scores:
                    avg_score = sum(scores) / len(scores)
                    print(f"  评分统计 - 平均分: {avg_score:.1f}, 最高分: {max(scores):.1f}, 最低分: {min(scores):.1f}")
                
            except Exception as e:
                print(f"[ERROR] 文章评分过程中出错: {e}")
                import traceback
                traceback.print_exc()
                return None, None
            
            # 4. 创建话题列表（基于评分）
            print("\n4. 创建话题列表（基于文章评分）...")
            all_topics = []
            
            for article in rated_articles:
                # 将每篇文章转换为话题格式
                topic = {
                    'topic': article.get('title', '未知话题')[:100],
                    'score': article.get('score', 0.0),
                    'summary': article.get('summary', article.get('content', ''))[:200],
                    'article_count': 1,
                    'sources': [article.get('source', '未知来源')],
                    'articles': [article],
                    'rating_details': {
                        'source_credibility': article.get('category_scores', {}).get('source_credibility', 0),
                        'impact': article.get('category_scores', {}).get('impact', 0),
                        'completeness_risk': article.get('category_scores', {}).get('completeness_risk', 0),
                        'time_recency': article.get('category_scores', {}).get('time_recency', 0),
                        'scoring_method': article.get('scoring_method', 'unknown')
                    }
                }
                all_topics.append(topic)
            
            print(f"  创建了 {len(all_topics)} 个话题（每篇文章一个话题）")
            # 5. 获取前N名话题
            print(f"\n5. 获取前{top_n}名热点话题...")
            top_topics = self.get_top_topics(all_topics, top_n)
            if not top_topics:
                print("[ERROR] 无法获取前N名话题")
                return all_topics, None
            
            # 6. 保存结果
            print(f"\n6. 保存结果...")
            output_file = self.save_top_topics(top_topics, top_n)
            
            # 7. 生成深度分析报告
            print(f"\n7. 生成深度分析报告...")
            analysis_file = self.generate_deep_analysis(output_file, max_urls=3)
            if analysis_file:
                print(f"   深度分析报告已保存: {analysis_file}")
            else:
                print(f"   深度分析报告生成失败或跳过")
            
            # 8. 计算执行时间
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"\n{'='*70}")
            print(f"归纳完成!")
            print(f"{'='*70}")
            print(f"统计:")
            print(f"  总话题数: {len(all_topics)}")
            print(f"  前{top_n}名话题: {len(top_topics)}")
            print(f"  耗时: {execution_time:.2f} 秒")
            print(f"  输出文件: {output_file}")
            print(f"{'='*70}")
            
            return all_topics, top_topics
            
        except Exception as e:
            print(f"\n[ERROR] 归纳流程失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None, None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='热点新闻话题归纳模块（过滤版）')
    parser.add_argument('--top-n', type=int, default=5,
                       help='获取前N名热点话题（默认: 5）')
    
    args = parser.parse_args()
    
    # 创建归纳器
    summarizer = TopicSummarizerFiltered()
    
    # 运行归纳流程
    all_topics, top_topics = summarizer.run(top_n=args.top_n)
    
    if not top_topics:
        print("\n归纳失败")
        sys.exit(1)
    
    print(f"\n归纳成功!")
    print(f"输出目录: {summarizer.output_dir}")


if __name__ == "__main__":
    import sys
    main()