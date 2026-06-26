"""
交易员智能体模块
使用 AgentScope AgentBase 实现
负责综合分析师报告和研究员结论，提出交易建议
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List

from agentscope.agent import AgentBase
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg

from ..config import config, LLM_API_KEY


class Trader(AgentBase):
    """
    交易员智能体 - 使用 AgentScope AgentBase 实现
    综合研究报告，提出交易建议
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Trader"
        
        self.model = OpenAIChatModel(
            model_name=config.model_name,
            api_key=LLM_API_KEY.get("bailian"),
            client_args={
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            },
            stream=True,
            
        )
        self.formatter = OpenAIChatFormatter()
        self.memory = InMemoryMemory()
        
        self.sys_prompt = """你是一名专业的交易员，负责基于多维度量化数据做出交易决策。

你的职责:
1. 综合评估技术面、基本面、舆情面的分析报告
2. 结合研究员辩论结论调整判断
3. 给出明确的交易建议（买入/卖出/持有/观望）
4. 提供量化的仓位建议、目标价和止损价

要求：决策要基于数据，理由要具体明确，全文使用中文。请用中文回答。
"""
    
    async def reply(self, msg: Msg | List[Msg] | None) -> Msg:
        """处理消息并回复，支持流式输出（显示 thinking 过程）"""
        if msg is not None:
            await self.memory.add(msg)
        
        memory_content = await self.memory.get_memory()
        prompt = await self.formatter.format([
            Msg("system", self.sys_prompt, "system"),
            *memory_content,
        ])
                
        response = await self.model(prompt)
                
        # 处理流式响应 - 显示 thinking 思考过程,但报告只保留 text
        if hasattr(response, '__aiter__'):
            last_thinking = ""
            last_text = ""
            final_text = ""
            print(f"\n[{self.name}] ", flush=True)
            async for chunk in response:  # pyright: ignore[reportGeneralTypeIssues]
                if hasattr(chunk, 'content') and chunk.content:
                    # 分别提取 thinking 和 text
                    thinking, text = self._extract_thinking_and_text(chunk.content)
                    
                    # 显示 thinking 增量
                    if thinking and len(thinking) > len(last_thinking):
                        delta = thinking[len(last_thinking):]
                        print(delta, end='', flush=True)
                        last_thinking = thinking
                    
                    # 显示 text 增量
                    if text and len(text) > len(last_text):
                        delta = text[len(last_text):]
                        print(delta, end='', flush=True)
                        last_text = text
                        final_text = text  # 保留最后的完整 text 内容
            print()  # 换行
            content = final_text
        else:
            # 安全地获取 content 属性
            response_content = getattr(response, 'content', '')
            content = self._extract_content(response_content)
        
        reply_msg = Msg(name=self.name, content=content, role="assistant")
        await self.memory.add(reply_msg)
        return reply_msg
    
    def _extract_thinking_and_text(self, chunk_content) -> tuple:
        """从流式响应块中分别提取 thinking 和 text 内容"""
        thinking = ""
        text = ""
        
        if isinstance(chunk_content, str):
            # 字符串格式，无法区分，都当作 text
            if "'type': 'thinking'" not in chunk_content and '"type": "thinking"' not in chunk_content:
                text = chunk_content
        elif isinstance(chunk_content, dict):
            if chunk_content.get('type') == 'thinking':
                thinking = chunk_content.get('thinking', '')
            elif chunk_content.get('type') == 'text':
                text = chunk_content.get('text', '')
            else:
                text = chunk_content.get('text', '')
        elif isinstance(chunk_content, list):
            for item in chunk_content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        thinking += item.get('thinking', '')
                    elif item.get('type') == 'text':
                        text += item.get('text', '')
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        text += item
        
        return thinking, text
    
    def _extract_content(self, content) -> str:
        """从响应中提取字符串内容，过滤 thinking 内容"""
        if isinstance(content, str):
            # 检查是否包含 thinking 格式的字符串
            if "'type': 'thinking'" in content or '"type": "thinking"' in content:
                # 尝试提取实际文本内容
                import re
                # 移除所有 thinking 块
                content = re.sub(r"\[\{'type': 'thinking'[^\]]*\]\]", "", content)
                content = re.sub(r'\[\{"type": "thinking"[^\]]*\]\]', "", content)
            return content
        elif isinstance(content, list):
            # 过滤 thinking 内容
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                    else:
                        texts.append(str(item))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return "\n".join(texts) if texts else ""
        else:
            return str(content)
    
    async def observe(self, msg: Msg | List[Msg] | None) -> None:
        """观察消息但不回复"""
        if msg is not None:
            await self.memory.add(msg)
    
    async def handle_interrupt(self) -> Msg:
        """处理中断"""
        return Msg(name=self.name, content="交易决策被中断。", role="assistant")
    
    def make_decision(self, analyst_reports: Dict[str, str], 
                      research_debate: str) -> str:
        """做出交易决策（同步方法，供外部调用）"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self._make_decision_async(analyst_reports, research_debate)
            )
            return result
        finally:
            loop.close()
    
    async def _make_decision_async(self, analyst_reports: Dict[str, str], 
                                   research_debate: str) -> str:
        """异步做出交易决策"""
        scores = self._extract_scores(analyst_reports)
        
        # 截取报告内容，避免请求过大
        combined_reports = "\n\n".join([
            f"### {name}\n{report[:600]}..." if len(report) > 600 else f"### {name}\n{report}"
            for name, report in analyst_reports.items()
        ])
        research_summary = research_debate[:800] if len(research_debate) > 800 else research_debate
        
        prompt = f"""请根据以下分析报告做出交易决策：

## 分析师报告摘要
{combined_reports}

## 研究员辩论结论
{research_summary}

## 决策要求：
1. **综合评分**：汇总技术面、基本面、舆情面的评分
2. **加权计算**：按权重({int(config.tech_weight*100)}%技术 + {int(config.fund_weight*100)}%基本 + {int(config.news_weight*100)}%舆情)计算总分
3. **量化决策**：给出具体的仓位、目标价、止损价

请直接用Markdown格式输出交易决策报告（500字内）：

# 交易决策报告

## 决策信号
- 方向: 买入/卖出/持有/观望
- 置信度: XX/100
- 建议仓位: XX%

## 综合评分
- 技术面: XX/100
- 基本面: XX/100
- 舆情面: XX/100
- 加权总分: XX/100

## 决策依据
[技术面、基本面、舆情面的具体分析理由]

## 目标价位
- 目标价: XXX
- 止损价: XXX
"""

        try:
            msg = Msg(name="user", content=prompt, role="user")
            response = await self.reply(msg)
            report = self._extract_content(response.content)
            return report
        except Exception as e:
            print(f"[{self.name}] 模型调用失败: {e}")
        
        # 备用报告
        return self._generate_fallback_report(scores)
    
    def _extract_scores(self, analyst_reports: Dict[str, str]) -> Dict:
        """从报告中提取评分"""
        scores = {"tech_score": 50, "fund_score": 50, "news_score": 50}
        
        for name, report in analyst_reports.items():
            lines = report.split('\n')
            for line in lines:
                if "技术评分" in line and "/100" in line:
                    try:
                        scores["tech_score"] = int(line.split(':')[1].split('/')[0].strip())
                    except:
                        pass
                elif "基本面评分" in line and "/100" in line:
                    try:
                        scores["fund_score"] = int(line.split(':')[1].split('/')[0].strip())
                    except:
                        pass
                elif "舆情评分" in line and "/100" in line:
                    try:
                        scores["news_score"] = int(line.split(':')[1].split('/')[0].strip())
                    except:
                        pass
        return scores
    
    def _generate_fallback_report(self, scores: Dict) -> str:
        """生成备用报告"""
        total_score = int(
            scores["tech_score"] * config.tech_weight +
            scores["fund_score"] * config.fund_weight +
            scores["news_score"] * config.news_weight
        ) // (config.tech_weight + config.fund_weight + config.news_weight)
        
        if total_score >= 70:
            action, position = "买入", "15%"
        elif total_score >= 55:
            action, position = "持有", "10%"
        elif total_score >= 40:
            action, position = "观望", "5%"
        else:
            action, position = "观望", "0%"
        
        return f"""# 交易决策报告

## 决策时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 决策信号
- 方向: **{action}**
- 置信度: {total_score}/100
- 建议仓位: {position}

## 综合评分
- 技术面: {scores.get('tech_score', 50)}/100
- 基本面: {scores.get('fund_score', 50)}/100
- 舆情面: {scores.get('news_score', 50)}/100
- 加权总分: {total_score}/100

## 目标价位
- 目标价: 根据技术分析确定
- 止损价: 建议设置8%止损
"""

    def _make_rule_based_decision(self, scores: Dict, research_debate: str) -> Dict:
        """基于规则的决策（备用）"""
        total_score = (
            scores["tech_score"] * config.tech_weight +
            scores["fund_score"] * config.fund_weight +
            scores["news_score"] * config.news_weight
        ) / (config.tech_weight + config.fund_weight + config.news_weight)
        
        if "看涨" in research_debate and "胜出" in research_debate:
            total_score += 10
        elif "看跌" in research_debate and "胜出" in research_debate:
            total_score -= 10
        
        if total_score >= 70:
            action, confidence, position = "买入", min(95, int(total_score + 10)), "15%"
        elif total_score >= 55:
            action, confidence, position = "持有", int(total_score), "10%"
        elif total_score >= 40:
            action, confidence, position = "观望", int(total_score), "0%"
        else:
            action, confidence, position = "卖出", min(95, int(100 - total_score)), "0%"
        
        return {
            "action": action, "confidence": confidence, "position": position,
            "target_price": "根据技术分析确定", "stop_loss": "建议设置8%止损",
            "tech_reason": f"技术面评分{scores['tech_score']}分",
            "fund_reason": f"基本面评分{scores['fund_score']}分",
            "news_reason": f"舆情面评分{scores['news_score']}分"
        }
    
    def _generate_report(self, scores: Dict, decision: Dict) -> str:
        """生成交易决策报告"""
        return f"""# 交易决策报告

## 决策时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 决策信号
| 字段 | 值 |
|------|----||
| 方向 | **{decision.get('action', '观望')}** |
| 置信度 | {decision.get('confidence', 50)}/100 |
| 建议仓位 | {decision.get('position', '0%')} |

## 决策依据
### 技术面（权重{int(config.tech_weight * 100)}%）
- 综合评分: {scores.get('tech_score', 50)}/100
- 核心理由: {decision.get('tech_reason', '无')}

### 基本面（权重{int(config.fund_weight * 100)}%）
- 综合评分: {scores.get('fund_score', 50)}/100
- 核心理由: {decision.get('fund_reason', '无')}

### 舆情面（权重{int(config.news_weight * 100)}%）
- 综合评分: {scores.get('news_score', 50)}/100
- 核心理由: {decision.get('news_reason', '无')}

## 目标价位
- 目标价: {decision.get('target_price', 'N/A')}
- 止损价: {decision.get('stop_loss', 'N/A')}
"""
