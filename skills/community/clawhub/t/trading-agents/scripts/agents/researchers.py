"""
研究员智能体模块
使用 AgentScope AgentBase 实现辩证式研究分析
"""

import asyncio
from typing import Dict, List, Optional

from agentscope.agent import AgentBase
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg

from ..config import config, LLM_API_KEY


class BullishResearcherAgent(AgentBase):
    """
    看多研究员 - 使用 AgentScope AgentBase 实现
    从乐观角度分析股票的投资价值
    """
    
    def __init__(self):
        super().__init__()
        self.name = "BullishResearcher"
        
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
        
        self.sys_prompt = """你是一名看多研究员，擅长发掘股票的投资亮点和上涨潜力。

你的角色特点:
1. 积极乐观，善于发现投资机会
2. 关注成长性、行业前景、竞争优势
3. 对利好消息敏感，合理推断正面影响
4. 在辩论中要有理有据地阐述看多观点

分析风格:
- 重点挖掘被低估的价值
- 强调公司的成长空间
- 分析行业红利和政策支持
- 关注资金流入和市场情绪转暖信号

注意：虽然你是看多派，但分析要基于数据，不能无中生有。请用中文回答。
"""
    
    async def reply(self, msg: Msg | List[Msg] | None) -> Msg:
        """处理消息并回复，支持流式输出"""
        if msg is not None:
            await self.memory.add(msg)
        
        memory_content = await self.memory.get_memory()
        prompt = await self.formatter.format([
            Msg("system", self.sys_prompt, "system"),
            *memory_content,
        ])
        
        response = await self.model(prompt)
        
        # 处理流式响应 - DashScope返回累积内容，需要取增量
        if hasattr(response, '__aiter__'):
            last_content = ""
            final_content = ""
            print(f"\n[{self.name}] ", end='', flush=True)
            async for chunk in response:  # pyright: ignore[reportGeneralTypeIssues]
                if hasattr(chunk, 'content') and chunk.content:
                    current_text = self._extract_text_from_chunk(chunk.content)
                    if current_text:
                        # 计算增量部分用于显示
                        if len(current_text) > len(last_content):
                            delta = current_text[len(last_content):]
                            print(delta, end='', flush=True)
                        last_content = current_text
                        final_content = current_text  # 保留最后的完整内容
            print()  # 换行
            content = final_content
        else:
            # 非流式响应处理
            content = self._extract_content(getattr(response, 'content', str(response)))
        
        reply_msg = Msg(name=self.name, content=content, role="assistant")
        await self.memory.add(reply_msg)
        return reply_msg
    
    def _extract_text_from_chunk(self, chunk_content) -> str:
        """从流式响应块中提取文本，过滤 thinking 内容"""
        if isinstance(chunk_content, str):
            if "'type': 'thinking'" in chunk_content or '"type": "thinking"' in chunk_content:
                return ""
            return chunk_content
        elif isinstance(chunk_content, dict):
            if chunk_content.get('type') == 'thinking':
                return ""
            if chunk_content.get('type') == 'text':
                return chunk_content.get('text', '')
            return chunk_content.get('text', '')
        elif isinstance(chunk_content, list):
            texts = []
            for item in chunk_content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return ''.join(texts)
        return ""
    
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


class BearishResearcherAgent(AgentBase):
    """
    看空研究员 - 使用 AgentScope AgentBase 实现
    从谨慎角度分析股票的风险因素
    """
    
    def __init__(self):
        super().__init__()
        self.name = "BearishResearcher"
        
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
        
        self.sys_prompt = """你是一名看空研究员，擅长发现股票的潜在风险和下跌隐患。

你的角色特点:
1. 谨慎保守，善于发现风险因素
2. 关注估值泡沫、业绩下滑、行业风险
3. 对利空消息敏感，评估负面影响
4. 在辩论中要有理有据地阐述看空观点

分析风格:
- 重点识别被高估的风险
- 强调公司面临的挑战
- 分析行业竞争和政策风险
- 关注资金流出和市场情绪恶化信号

注意：虽然你是看空派，但分析要基于数据，不能危言耸听。请用中文回答。
"""
    
    async def reply(self, msg: Msg | List[Msg] | None) -> Msg:
        """处理消息并回复，支持流式输出"""
        if msg is not None:
            await self.memory.add(msg)
        
        memory_content = await self.memory.get_memory()
        prompt = await self.formatter.format([
            Msg("system", self.sys_prompt, "system"),
            *memory_content,
        ])
        
        response = await self.model(prompt)
        
        # 处理流式响应 - DashScope返回累积内容，需要取增量
        if hasattr(response, '__aiter__'):
            last_content = ""
            final_content = ""
            print(f"\n[{self.name}] ", end='', flush=True)
            async for chunk in response:  # pyright: ignore[reportGeneralTypeIssues]
                if hasattr(chunk, 'content') and chunk.content:
                    current_text = self._extract_text_from_chunk(chunk.content)
                    if current_text:
                        # 计算增量部分用于显示
                        if len(current_text) > len(last_content):
                            delta = current_text[len(last_content):]
                            print(delta, end='', flush=True)
                        last_content = current_text
                        final_content = current_text  # 保留最后的完整内容
            print()  # 换行
            content = final_content
        else:
            # 非流式响应处理
            content = self._extract_content(getattr(response, 'content', str(response)))
        
        reply_msg = Msg(name=self.name, content=content, role="assistant")
        await self.memory.add(reply_msg)
        return reply_msg
    
    def _extract_text_from_chunk(self, chunk_content) -> str:
        """从流式响应块中提取文本，过滤 thinking 内容"""
        if isinstance(chunk_content, str):
            if "'type': 'thinking'" in chunk_content or '"type": "thinking"' in chunk_content:
                return ""
            return chunk_content
        elif isinstance(chunk_content, dict):
            if chunk_content.get('type') == 'thinking':
                return ""
            if chunk_content.get('type') == 'text':
                return chunk_content.get('text', '')
            return chunk_content.get('text', '')
        elif isinstance(chunk_content, list):
            texts = []
            for item in chunk_content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return ''.join(texts)
        return ""
    
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
        return Msg(name=self.name, content="分析被中断。", role="assistant")
    
    def analyze_sync(self, context: str) -> str:
        """同步分析方法"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            msg = Msg(name="user", content=context, role="user")
            result = loop.run_until_complete(self.reply(msg))
            return self._extract_content(result.content)
        finally:
            loop.close()


class ResearchFacilitatorAgent(AgentBase):
    """
    研究主持人 - 使用 AgentScope AgentBase 实现
    负责组织和总结看多看空研究员的辩论
    """
    
    def __init__(self):
        super().__init__()
        self.name = "ResearchFacilitator"
        
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
        
        self.sys_prompt = """你是一名资深的研究主持人，负责组织和总结看多、看空研究员的辩论。

你的职责:
1. 引导辩论有序进行
2. 确保双方观点充分表达
3. 提炼关键分歧点
4. 综合双方观点形成结论

总结报告要求:
- 公正客观，不偏向任何一方
- 明确列出多空双方的核心论点
- 分析哪些观点更有说服力
- 给出综合研判和投资建议

全文使用中文撰写。请用中文回答。
"""
    
    async def reply(self, msg: Msg | List[Msg] | None) -> Msg:
        """处理消息并回复，支持流式输出"""
        if msg is not None:
            await self.memory.add(msg)
        
        memory_content = await self.memory.get_memory()
        prompt = await self.formatter.format([
            Msg("system", self.sys_prompt, "system"),
            *memory_content,
        ])
        
        response = await self.model(prompt)
        
        # 处理流式响应 - DashScope返回累积内容，需要取增量
        if hasattr(response, '__aiter__'):
            last_content = ""
            final_content = ""
            print(f"\n[{self.name}] ", end='', flush=True)
            async for chunk in response:  # pyright: ignore[reportGeneralTypeIssues]
                if hasattr(chunk, 'content') and chunk.content:
                    current_text = self._extract_text_from_chunk(chunk.content)
                    if current_text:
                        # 计算增量部分用于显示
                        if len(current_text) > len(last_content):
                            delta = current_text[len(last_content):]
                            print(delta, end='', flush=True)
                        last_content = current_text
                        final_content = current_text  # 保留最后的完整内容
            print()  # 换行
            content = final_content
        else:
            # 非流式响应处理
            content = self._extract_content(getattr(response, 'content', str(response)))
        
        reply_msg = Msg(name=self.name, content=content, role="assistant")
        await self.memory.add(reply_msg)
        return reply_msg
    
    def _extract_text_from_chunk(self, chunk_content) -> str:
        """从流式响应块中提取文本，过滤 thinking 内容"""
        if isinstance(chunk_content, str):
            if "'type': 'thinking'" in chunk_content or '"type": "thinking"' in chunk_content:
                return ""
            return chunk_content
        elif isinstance(chunk_content, dict):
            if chunk_content.get('type') == 'thinking':
                return ""
            if chunk_content.get('type') == 'text':
                return chunk_content.get('text', '')
            return chunk_content.get('text', '')
        elif isinstance(chunk_content, list):
            texts = []
            for item in chunk_content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        continue
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    if "'type': 'thinking'" not in item and '"type": "thinking"' not in item:
                        texts.append(item)
            return ''.join(texts)
        return ""
    
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
    
    def facilitate_debate_sync(
        self,
        bullish: BullishResearcherAgent,
        bearish: BearishResearcherAgent,
        analyst_reports: Dict[str, str],
        rounds: int = 2
    ) -> str:
        """
        同步执行辩论流程
        
        Args:
            bullish: 看多研究员
            bearish: 看空研究员
            analyst_reports: 分析师报告
            rounds: 辩论轮数
            
        Returns:
            辩论总结报告
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self._facilitate_debate(bullish, bearish, analyst_reports, rounds)
            )
            return result
        finally:
            loop.close()
    
    async def _facilitate_debate(
        self,
        bullish: BullishResearcherAgent,
        bearish: BearishResearcherAgent,
        analyst_reports: Dict[str, str],
        rounds: int = 2
    ) -> str:
        """
        执行辩论流程
        """
        debate_history = []
        
        # 清空研究员的 memory，避免累积导致请求过大
        bullish.memory = InMemoryMemory()
        bearish.memory = InMemoryMemory()
        self.memory = InMemoryMemory()
        
        # 带重试的安全调用方法
        async def safe_reply(agent, msg, max_retries=3) -> Msg:
            """带重试的安全调用"""
            for attempt in range(max_retries):
                try:
                    # 每次重试前清空 memory
                    agent.memory = InMemoryMemory()
                    return await agent.reply(msg)
                except Exception as e:
                    print(f"\n[{agent.name}] 调用失败 (attempt {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)  # 等待2秒后重试
            # 所有重试失败后返回默认响应
            return Msg(name=agent.name, content=f"[网络超时,未能获取{agent.name}的分析]", role="assistant")
        
        # 准备分析报告摘要，限制每份报告最多800字符
        reports_summary = "\n\n".join([
            f"### {name}\n{report[:800]}..." if len(report) > 800 else f"### {name}\n{report}"
            for name, report in analyst_reports.items()
        ])
        
        # 第一轮：初始观点
        bullish_prompt = f"""基于以下分析师报告，请从看多角度阐述你的投资观点：

{reports_summary}

请简洁分析这只股票的投资亮点和上涨潜力，给出具体论据（500字内）。
"""
        
        bearish_prompt = f"""基于以下分析师报告，请从看空角度阐述你的风险观点：

{reports_summary}

请简洁分析这只股票的风险因素和下跌隐患，给出具体论据（500字内）。
"""
        
        # 看多先发言
        bullish_msg = Msg(name="user", content=bullish_prompt, role="user")
        bullish_response = await safe_reply(bullish, bullish_msg)
        bullish_content = self._extract_content(bullish_response.content)[:1000]
        debate_history.append(f"## 看多研究员（第1轮）\n\n{bullish_content}")
        
        # 看空发言
        bearish_msg = Msg(name="user", content=bearish_prompt, role="user")
        bearish_response = await safe_reply(bearish, bearish_msg)
        bearish_content = self._extract_content(bearish_response.content)[:1000]
        debate_history.append(f"## 看空研究员（第1轮）\n\n{bearish_content}")
        
        # 后续轮次：互相回应（清空 memory 避免累积）
        for round_num in range(2, rounds + 1):
            # 看多回应看空
            bullish_rebuttal = f"""看空研究员的观点是：

{bearish_content[:500]}

请简洁回应这些看空观点，并进一步阐述你的看多理由（500字内）。
"""
            bullish_msg = Msg(name="user", content=bullish_rebuttal, role="user")
            bullish_response = await safe_reply(bullish, bullish_msg)
            bullish_content = self._extract_content(bullish_response.content)[:1000]
            debate_history.append(f"## 看多研究员（第{round_num}轮）\n\n{bullish_content}")
            
            # 看空回应看多
            bearish_rebuttal = f"""看多研究员的观点是：

{bullish_content[:500]}

请简洁回应这些看多观点，并进一步阐述你的看空理由（500字内）。
"""
            bearish_msg = Msg(name="user", content=bearish_rebuttal, role="user")
            bearish_response = await safe_reply(bearish, bearish_msg)
            bearish_content = self._extract_content(bearish_response.content)[:1000]
            debate_history.append(f"## 看空研究员（第{round_num}轮）\n\n{bearish_content}")
        
        # 主持人总结（限制辩论历史长度）
        debate_summary = "\n\n".join(debate_history)[:4000]
        summary_prompt = f"""以下是看多研究员和看空研究员的辩论记录：

{debate_summary}

请作为研究主持人，对这场辩论进行总结（800字内）：

# 研究员辩论总结报告

## 辩论概述
[概述内容]

## 核心分歧点
[分歧点列表]

## 看多观点评价
[评价内容]

## 看空观点评价
[评价内容]

## 综合研判
[研判结论]

## 投资建议
[具体建议]

## 风险提示
[风险点列表]
"""
        
        # 主持人也使用安全调用
        self.memory = InMemoryMemory()
        summary_msg = Msg(name="user", content=summary_prompt, role="user")
        try:
            summary_response = await self.reply(summary_msg)
            summary_content = self._extract_content(summary_response.content)
        except Exception as e:
            print(f"\n[{self.name}] 总结失败: {e}")
            summary_content = "## 辩论总结\n\n由于网络问题，未能生成完整总结。"
        
        # 组合完整报告
        separator = "\n\n---\n\n"
        full_report = f"""# 研究员辩论报告

---

{separator.join(debate_history)}

---

{summary_content}
"""
        
        return full_report


def create_research_team() -> Dict[str, object]:
    """
    创建研究员团队
    
    Returns:
        包含研究员和主持人的字典
    """
    return {
        "BullishResearcher": BullishResearcherAgent(),
        "BearishResearcher": BearishResearcherAgent(),
        "ResearchFacilitator": ResearchFacilitatorAgent(),
    }
