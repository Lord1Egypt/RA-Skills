"""
分析师智能体模块
使用 AgentScope ReActAgent 实现数据采集和分析功能
"""

import asyncio
from typing import Dict
from datetime import datetime

from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg

from ..config import config, LLM_API_KEY
from ..tools.toolkit import (
    create_market_analyst_toolkit,
    create_fundamentals_analyst_toolkit,
    create_news_analyst_toolkit,
)


class MarketAnalystAgent:
    """
    技术面分析师 - 使用 AgentScope ReActAgent 实现
    能够自主调用工具获取行情数据并生成分析报告
    """
    
    def __init__(self):
        self.name = "MarketAnalyst"
        
        self.sys_prompt = """你是一名资深的技术面分析师，擅长从技术指标和价格走势中挖掘投资机会。

你的职责是:
1. 使用工具获取股票的日线行情数据
2. 使用工具获取技术指标（MA、MACD、RSI等）
3. 基于数据撰写专业的技术面分析报告

分析报告必须包含以下部分:
- 价格走势分析（均线系统、金叉死叉信号）
- 技术指标解读（MACD、RSI等）
- 成交量能分析
- 关键价位判断（支撑位、阻力位）
- 技术评分（0-100分）
- 投资建议

要求：分析要专业、深入，评分要客观公正，全文使用中文。请用中文回答。
"""
        
        self.agent = ReActAgent(
            name=self.name,
            sys_prompt=self.sys_prompt,
            model=OpenAIChatModel(
                model_name=config.model_name,
                api_key=LLM_API_KEY.get("bailian"),
                client_args={
                    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
                },
                stream=True,
            ),
            formatter=OpenAIChatFormatter(),
            toolkit=create_market_analyst_toolkit(),
            memory=InMemoryMemory(),
            max_iters=5,
        )
    
    def analyze(self, ts_code: str) -> str:
        """
        执行技术面分析
        
        Args:
            ts_code: 股票代码
            
        Returns:
            Markdown格式的技术分析报告
        """
        prompt = f"""请为股票 **{ts_code}** 进行技术面分析。

步骤:
1. 首先使用 get_stock_basic 工具获取股票基本信息
2. 使用 get_stock_daily 工具获取近60日行情数据
3. 使用 get_technical_indicators 工具获取技术指标
4. 基于获取的数据，撰写完整的技术面分析报告

请按照以下Markdown格式输出:

# 技术面分析报告

## 基本信息
- 股票代码: {ts_code}
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 价格走势分析
[分析内容]

## 技术指标解读
[分析内容]

## 成交量能分析
[分析内容]

## 关键价位判断
[分析内容]

## 技术评分: [评分]/100

## 投资建议
[具体建议]
"""
        
        msg = Msg(name="user", content=prompt, role="user")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.agent(msg))
            return self._extract_content(result.content)
        except Exception as e:
            print(f"[{self.name}] 分析失败: {e}")
            return f"# 技术面分析报告\n\n分析过程中出现错误: {str(e)}"
        finally:
            loop.close()
    
    def _extract_content(self, content) -> str:
        """从 Msg.content 中提取字符串内容，优先提取 Markdown 格式的报告，过滤 thinking 内容"""
        if isinstance(content, str):
            # 过滤 thinking 内容
            if "'type': 'thinking'" in content or '"type": "thinking"' in content:
                import re
                content = re.sub(r"\[\{'type': 'thinking'[^\]]*\]\]", "", content)
                content = re.sub(r'\[\{"type": "thinking"[^\]]*\]\]', "", content)
            return content
        elif isinstance(content, list):
            # 如果是列表，优先查找包含 Markdown 标题的内容，跳过 thinking
            for item in reversed(content):  # 从后往前找，最后一条通常是最终报告
                # 跳过 thinking 类型
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        item_str = item.get('text', '')
                    else:
                        item_str = str(item)
                else:
                    item_str = str(item)
                # 跳过 thinking 字符串
                if "'type': 'thinking'" in item_str or '"type": "thinking"' in item_str:
                    continue
                # 检查是否包含 Markdown 标题（分析报告的特征）
                if item_str.startswith('#') or '\n#' in item_str:
                    return item_str
            # 如果没有找到 Markdown，返回最后一个非空、非 thinking 内容
            for item in reversed(content):
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        item_str = item.get('text', '')
                    else:
                        continue  # 跳过其他字典
                else:
                    item_str = str(item).strip()
                if "'type': 'thinking'" in item_str or '"type": "thinking"' in item_str:
                    continue
                if item_str and not item_str.startswith('{'):
                    return item_str
            # 最后备选：合并所有非 thinking 内容
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return "\n".join(texts) if texts else ""
        else:
            return str(content)


class FundamentalsAnalystAgent:
    """
    基本面分析师 - 使用 AgentScope ReActAgent 实现
    能够自主调用工具获取财务数据并生成分析报告
    """
    
    def __init__(self):
        self.name = "FundamentalsAnalyst"
        
        self.sys_prompt = """你是一名资深的基本面分析师，擅长从财务数据和估值指标中评估公司的内在价值。

你的职责是:
1. 使用工具获取股票的基本信息
2. 使用工具获取估值数据（PE、PB、PS等）
3. 使用工具获取财务指标（ROE、毛利率等）
4. 基于数据撰写专业的基本面分析报告

分析报告必须包含以下部分:
- 估值分析（与行业对比）
- 盈利能力分析
- 成长性分析
- 财务健康分析
- 基本面评分（0-100分）
- 投资建议

要求：分析要专业、深入，评分要客观公正，全文使用中文。请用中文回答。
"""
        
        self.agent = ReActAgent(
            name=self.name,
            sys_prompt=self.sys_prompt,
            model=OpenAIChatModel(
                model_name=config.model_name,
                api_key=LLM_API_KEY.get("bailian"),
                client_args={
                    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
                },
                stream=True,
            ),
            formatter=OpenAIChatFormatter(),
            toolkit=create_fundamentals_analyst_toolkit(),
            memory=InMemoryMemory(),
            max_iters=5,
        )
    
    def analyze(self, ts_code: str) -> str:
        """执行基本面分析"""
        prompt = f"""请为股票 **{ts_code}** 进行基本面分析。

步骤:
1. 使用 get_stock_basic 工具获取股票基本信息
2. 使用 get_valuation 工具获取估值数据
3. 使用 get_financial_indicator 工具获取财务指标
4. 基于获取的数据，撰写完整的基本面分析报告

请按照以下Markdown格式输出:

# 基本面分析报告

## 基本信息
- 股票代码: {ts_code}
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 估值分析
[分析内容]

## 盈利能力分析
[分析内容]

## 成长性分析
[分析内容]

## 财务健康分析
[分析内容]

## 基本面评分: [评分]/100

## 投资建议
[具体建议]
"""
        
        msg = Msg(name="user", content=prompt, role="user")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.agent(msg))
            return self._extract_content(result.content)
        except Exception as e:
            print(f"[{self.name}] 分析失败: {e}")
            return f"# 基本面分析报告\n\n分析过程中出现错误: {str(e)}"
        finally:
            loop.close()
    
    def _extract_content(self, content) -> str:
        """从 Msg.content 中提取字符串内容，优先提取 Markdown 格式的报告，过滤 thinking 内容"""
        if isinstance(content, str):
            # 过滤 thinking 内容
            if "'type': 'thinking'" in content or '"type": "thinking"' in content:
                import re
                content = re.sub(r"\[\{'type': 'thinking'[^\]]*\]\]", "", content)
                content = re.sub(r'\[\{"type": "thinking"[^\]]*\]\]', "", content)
            return content
        elif isinstance(content, list):
            # 如果是列表，优先查找包含 Markdown 标题的内容，跳过 thinking
            for item in reversed(content):  # 从后往前找，最后一条通常是最终报告
                # 跳过 thinking 类型
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        item_str = item.get('text', '')
                    else:
                        item_str = str(item)
                else:
                    item_str = str(item)
                # 跳过 thinking 字符串
                if "'type': 'thinking'" in item_str or '"type": "thinking"' in item_str:
                    continue
                # 检查是否包含 Markdown 标题（分析报告的特征）
                if item_str.startswith('#') or '\n#' in item_str:
                    return item_str
            # 如果没有找到 Markdown，返回最后一个非空、非 thinking 内容
            for item in reversed(content):
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        item_str = item.get('text', '')
                    else:
                        continue  # 跳过其他字典
                else:
                    item_str = str(item).strip()
                if "'type': 'thinking'" in item_str or '"type": "thinking"' in item_str:
                    continue
                if item_str and not item_str.startswith('{'):
                    return item_str
            # 最后备选：合并所有非 thinking 内容
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return "\n".join(texts) if texts else ""
        else:
            return str(content)


class NewsAnalystAgent:
    """
    舆情分析师 - 使用 AgentScope ReActAgent 实现
    能够自主调用工具获取新闻数据并生成舆情分析报告
    """
    
    def __init__(self):
        self.name = "NewsAnalyst"
        
        self.sys_prompt = """你是一名资深的舆情分析师，擅长从新闻和市场情绪中挖掘投资机会和风险。

你的职责是:
1. 使用工具获取股票基本信息
2. 使用工具获取个股相关新闻
3. 使用工具获取市场整体情绪
4. 基于数据撰写专业的舆情分析报告

分析报告必须包含以下部分:
- 舆情概述
- 关键新闻解读
- 市场情绪分析
- 舆情风险警示
- 舆情评分（0-100分）
- 投资建议

要求：分析要专业、敏锐，评分要客观公正，全文使用中文。请用中文回答。
"""
        
        self.agent = ReActAgent(
            name=self.name,
            sys_prompt=self.sys_prompt,
            model=OpenAIChatModel(
                model_name=config.model_name,
                api_key=LLM_API_KEY.get("bailian"),
                client_args={
                    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
                },
                stream=True,
            ),
            formatter=OpenAIChatFormatter(),
            toolkit=create_news_analyst_toolkit(),
            memory=InMemoryMemory(),
            max_iters=5,
        )
    
    def analyze(self, ts_code: str, stock_name: str = "") -> str:
        """执行舆情分析"""
        prompt = f"""请为股票 **{ts_code}** ({stock_name or '未知'}) 进行舆情分析。

步骤:
1. 使用 get_stock_basic 工具获取股票基本信息（如果没有提供股票名称）
2. 使用 get_stock_news 工具获取近7天的相关新闻
3. 使用 get_market_sentiment 工具获取市场整体情绪
4. 基于获取的数据，撰写完整的舆情分析报告

请按照以下Markdown格式输出:

# 新闻舆情分析报告

## 基本信息
- 股票代码: {ts_code}
- 股票名称: {stock_name or '待获取'}
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 新闻周期: 近7天

## 舆情概述
[分析内容]

## 关键新闻解读
[分析内容]

## 市场情绪分析
[分析内容]

## 舆情风险警示
[分析内容]

## 舆情评分: [评分]/100

## 投资建议
[具体建议]
"""
        
        msg = Msg(name="user", content=prompt, role="user")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.agent(msg))
            return self._extract_content(result.content)
        except Exception as e:
            print(f"[{self.name}] 分析失败: {e}")
            return f"# 新闻舆情分析报告\n\n分析过程中出现错误: {str(e)}"
        finally:
            loop.close()
    
    def _extract_content(self, content) -> str:
        """从 Msg.content 中提取字符串内容，优先提取 Markdown 格式的报告，过滤 thinking 内容"""
        if isinstance(content, str):
            # 过滤 thinking 内容
            if "'type': 'thinking'" in content or '"type": "thinking"' in content:
                import re
                content = re.sub(r"\[\{'type': 'thinking'[^\]]*\]\]", "", content)
                content = re.sub(r'\[\{"type": "thinking"[^\]]*\]\]', "", content)
            return content
        elif isinstance(content, list):
            # 如果是列表，优先查找包含 Markdown 标题的内容，跳过 thinking
            for item in reversed(content):  # 从后往前找，最后一条通常是最终报告
                # 跳过 thinking 类型
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        item_str = item.get('text', '')
                    else:
                        item_str = str(item)
                else:
                    item_str = str(item)
                # 跳过 thinking 字符串
                if "'type': 'thinking'" in item_str or '"type": "thinking"' in item_str:
                    continue
                # 检查是否包含 Markdown 标题（分析报告的特征）
                if item_str.startswith('#') or '\n#' in item_str:
                    return item_str
            # 如果没有找到 Markdown，返回最后一个非空、非 thinking 内容
            for item in reversed(content):
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        item_str = item.get('text', '')
                    else:
                        continue  # 跳过其他字典
                else:
                    item_str = str(item).strip()
                if "'type': 'thinking'" in item_str or '"type": "thinking"' in item_str:
                    continue
                if item_str and not item_str.startswith('{'):
                    return item_str
            # 最后备选：合并所有非 thinking 内容
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return "\n".join(texts) if texts else ""
        else:
            return str(content)


def create_analyst_team() -> Dict[str, object]:
    """
    创建分析师团队
    
    Returns:
        包含三个分析师的字典
    """
    return {
        "MarketAnalyst": MarketAnalystAgent(),
        "FundamentalsAnalyst": FundamentalsAnalystAgent(),
        "NewsAnalyst": NewsAnalystAgent(),
    }
