"""
基金经理智能体模块
使用 AgentScope AgentBase 实现
负责综合风险评估，做出最终决策
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


class Manager(AgentBase):
    """
    基金经理智能体 - 使用 AgentScope AgentBase 实现
    综合风险评估，做出最终决策
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Manager"
        
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
        
        self.sys_prompt = """你是一名资深的基金经理，负责基于全面量化数据做出最终投资决策。

你的职责:
1. 综合评估所有分析报告和风险建议
2. 权衡交易员的机会观点和风险管理的谨慎观点
3. 给出最终的投资决策（UP或NONE）
4. 制定具体的执行计划和风控措施

决策原则:
- UP: 建议买入/加仓，适用于综合评分较高且风险可控的情况
- NONE: 观望/不操作，适用于综合评分偏低或风险较大的情况

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
        
        # 处理流式响应 - 显示 thinking 思考过程，但报告只保留 text
        if hasattr(response, '__aiter__'):
            last_thinking = ""
            last_text = ""
            final_text = ""
            print(f"\n[{self.name}] ", flush=True)
            async for chunk in response:  # pyright: ignore[reportGeneralTypeIssues]
                # 安全地获取 content 属性
                chunk_content = getattr(chunk, 'content', None)
                if chunk_content:
                    thinking, text = self._extract_thinking_and_text(chunk_content)
                    
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
                        final_text = text
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
        """从响应中提取字符串内容，过滤 thinking"""
        if isinstance(content, str):
            if "'type': 'thinking'" in content or '"type": "thinking"' in content:
                import re
                content = re.sub(r"\[\{'type': 'thinking'[^\]]*\]\]", "", content)
                content = re.sub(r'\[\{"type": "thinking"[^\]]*\]\]', "", content)
            return content
        elif isinstance(content, list):
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
        return Msg(name=self.name, content="决策被中断。", role="assistant")
    
    def make_final_decision(self, ts_code: str, stock_name: str,
                           analyst_reports: Dict[str, str],
                           research_debate: str,
                           trader_report: str,
                           risk_discussion: str) -> str:
        """做出最终决策（同步方法，供外部调用）"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self._make_final_decision_async(
                    ts_code, stock_name, analyst_reports, 
                    research_debate, trader_report, risk_discussion
                )
            )
        finally:
            loop.close()
    
    async def _make_final_decision_async(self, ts_code: str, stock_name: str,
                                         analyst_reports: Dict[str, str],
                                         research_debate: str,
                                         trader_report: str,
                                         risk_discussion: str) -> str:
        """异步做出最终决策"""
        scores = self._extract_all_scores(analyst_reports, research_debate)
        # 直接返回 Markdown 报告
        return await self._generate_decision_async(
            ts_code, stock_name, scores, trader_report, risk_discussion
        )
    
    def _extract_all_scores(self, analyst_reports: Dict[str, str], 
                           research_debate: str) -> Dict:
        """提取所有维度的评分"""
        scores = {"tech_score": 50, "fund_score": 50, "news_score": 50, "research_score": 50}
        
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
        
        if "看涨" in research_debate and "胜出" in research_debate:
            scores["research_score"] = 70
        elif "看跌" in research_debate and "胜出" in research_debate:
            scores["research_score"] = 30
        
        scores["total_score"] = int(
            scores["tech_score"] * config.tech_weight +
            scores["fund_score"] * config.fund_weight +
            scores["news_score"] * config.news_weight +
            scores["research_score"] * config.research_weight
        )
        
        return scores
    
    async def _generate_decision_async(self, ts_code: str, stock_name: str, scores: Dict,
                                       trader_report: str, risk_discussion: str) -> str:
        """异步生成最终决策，直接返回Markdown报告"""
        # 截取报告内容避免请求过大
        trader_summary = trader_report[:600] if len(trader_report) > 600 else trader_report
        risk_summary = risk_discussion[:600] if len(risk_discussion) > 600 else risk_discussion
        
        prompt = f"""作为基金经理，请根据以下信息做出最终投资决策（500字内）：

## 股票信息
- 股票代码: {ts_code}
- 股票名称: {stock_name}

## 综合评分
- 技术面: {scores.get('tech_score', 50)}/100 (权重{int(config.tech_weight*100)}%)
- 基本面: {scores.get('fund_score', 50)}/100 (权重{int(config.fund_weight*100)}%)
- 舆情面: {scores.get('news_score', 50)}/100 (权重{int(config.news_weight*100)}%)
- **综合总分: {scores.get('total_score', 50)}/100**

## 交易员决策摘要
{trader_summary}

## 风险管理建议摘要
{risk_summary}

请直接用Markdown格式输出最终决策报告：

# 最终诊股决策报告

## 股票信息
- 代码: {ts_code}
- 名称: {stock_name}
- 诊断时间: [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]

## 最终决策
- 操作建议: **UP/NONE**
- 置信度: XX/100
- 建议仓位: XX%
- 目标价: XXX
- 止损价: XXX

## 综合评分
| 维度 | 评分 | 权重 |
|------|------|------|
| 技术面 | XX/100 | XX% |
| 基本面 | XX/100 | XX% |
| 舆情面 | XX/100 | XX% |
| **综合评分** | **XX/100** | - |

## 决策理由
[具体理由，权衡交易员和风险管理观点]

## 风险提示
[风险提示内容]

---
*本报告由AgentScope股票诊断智能体系统自动生成*

决策逻辑参考：
- 综合评分75+：UP，仓位15-20%
- 综合评分60-75：UP，仓位10-15%
- 综合评分45-60：谨慎UP或NONE，仓位5-10%
- 综合评分<45：NONE，仓位0%
"""

        try:
            msg = Msg(name="user", content=prompt, role="user")
            response = await self.reply(msg)
            report = self._extract_content(response.content)
            return report
        except Exception as e:
            print(f"[{self.name}] 决策生成失败: {e}")
        
        return self._generate_fallback_report(ts_code, stock_name, scores)
    
    def _generate_fallback_report(self, ts_code: str, stock_name: str, scores: Dict) -> str:
        """生成备用报告"""
        total_score = scores.get("total_score", 50)
        
        if total_score >= 70:
            action, position = "UP", "15%"
        elif total_score >= 55:
            action, position = "UP", "10%"
        else:
            action, position = "NONE", "0%"
        
        return f"""# 最终诊股决策报告

## 股票信息
- 代码: {ts_code}
- 名称: {stock_name}
- 诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 最终决策
- 操作建议: **{action}**
- 置信度: {total_score}/100
- 建议仓位: {position}
- 目标价: 根据技术分析确定
- 止损价: 建议设置8%止损

## 综合评分
| 维度 | 评分 | 权重 |
|------|------|------|
| 技术面 | {scores.get('tech_score', 50)}/100 | {int(config.tech_weight * 100)}% |
| 基本面 | {scores.get('fund_score', 50)}/100 | {int(config.fund_weight * 100)}% |
| 舆情面 | {scores.get('news_score', 50)}/100 | {int(config.news_weight * 100)}% |
| **综合评分** | **{total_score}/100** | - |

## 风险提示
投资有风险，入市需谨慎。本建议仅供参考，不构成投资建议。

---
*本报告由AgentScope股票诊断智能体系统自动生成*
"""

    def _rule_based_decision(self, scores: Dict) -> Dict:
        """基于规则的决策（备用）"""
        total_score = scores.get("total_score", 50)
        
        if total_score >= 70:
            action, confidence, position = "UP", min(90, total_score), "15%"
            reasoning = f"综合评分{total_score}分，较高，具备投资价值"
        elif total_score >= 55:
            action, confidence, position = "UP", total_score, "10%"
            reasoning = f"综合评分{total_score}分，中等偏上，建议适度仓位"
        elif total_score >= 40:
            action, confidence, position = "NONE", 60, "0%"
            reasoning = f"综合评分{total_score}分，一般，存在不确定性，建议观望"
        else:
            action, confidence, position = "NONE", min(90, 100 - total_score), "0%"
            reasoning = f"综合评分{total_score}分，较低，风险较大，不建议买入"
        
        return {
            "action": action, 
            "confidence": confidence, 
            "position": position,
            "target_price": "根据技术分析确定", 
            "stop_loss": "建议设置8%止损",
            "reasoning": reasoning,
            "risk_warning": "投资有风险，入市需谨慎。本建议仅供参考，不构成投资建议。"
        }
    
    def _generate_final_report(self, ts_code: str, stock_name: str,
                               scores: Dict, decision: Dict) -> str:
        return f"""# 最终诊股决策报告

## 股票信息
- 代码: {ts_code}
- 名称: {stock_name}
- 诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 综合评分
| 维度 | 评分 | 权重 |
|------|------|------|
| 技术面 | {scores.get('tech_score', 50)}/100 | {int(config.tech_weight * 100)}% |
| 基本面 | {scores.get('fund_score', 50)}/100 | {int(config.fund_weight * 100)}% |
| 舆情面 | {scores.get('news_score', 50)}/100 | {int(config.news_weight * 100)}% |
| 研究员共识 | {scores.get('research_score', 50)}/100 | {int(config.research_weight * 100)}% |
| **综合评分** | **{scores.get('total_score', 50)}/100** | - |

## 最终决策
| 字段 | 值 |
|------|----||
| 操作建议 | **{decision.get('action', '观望')}** |
| 置信度 | {decision.get('confidence', 50)}/100 |
| 建议仓位 | {decision.get('position', '0%')} |
| 目标价 | {decision.get('target_price', 'N/A')} |
| 止损价 | {decision.get('stop_loss', 'N/A')} |

## 决策理由
{decision.get('reasoning', '综合分析后做出的决策')}

## 风险提示
{decision.get('risk_warning', '投资有风险，入市需谨慎。')}

---
*本报告由AgentScope股票诊断智能体系统自动生成*
"""
