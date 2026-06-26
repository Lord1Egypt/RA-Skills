"""
风险管理智能体模块
使用 AgentScope AgentBase 实现
包含：AggressiveRisk（激进型）、NeutralRisk（中性型）、ConservativeRisk（保守型）、RiskFacilitator（协调人）
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


class AggressiveRisk(AgentBase):
    """激进型风险管理者 - 使用 AgentScope AgentBase 实现"""
    
    def __init__(self):
        super().__init__()
        self.name = "AggressiveRisk"
        
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
        
        self.sys_prompt = """你是一名激进型风险管理者，偏好高风险高收益，但仍需基于量化数据进行评估。

你的特点:
1. 积极乐观，善于发现投资机会
2. 风险容忍度较高
3. 建议较高的仓位配置(15-25%)
4. 量化预期收益率

要求：分析要基于数据，不能无中生有。请用中文回答。
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
                if hasattr(chunk, 'content') and chunk.content:
                    thinking, text = self._extract_thinking_and_text(chunk.content)
                    
                    # 显示 thinking 增量（灰色标记）
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
            content = self._extract_content(response.content)  # type: ignore[union-attr]
        
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
        if msg is not None:
            await self.memory.add(msg)
    
    async def handle_interrupt(self) -> Msg:
        return Msg(name=self.name, content="评估被中断。", role="assistant")
    
    def assess(self, trader_report: str) -> Dict:
        """评估交易决策（同步方法）"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._assess_async(trader_report))
        finally:
            loop.close()
    
    async def _assess_async(self, trader_report: str) -> Dict:
        """异步评估交易决策"""
        report_summary = trader_report[:600] if len(trader_report) > 600 else trader_report
        
        prompt = f"""请从激进型角度评估以下交易决策（300字内）：

{report_summary}

评估要求：从激进角度挖掘潜在高收益机会，建议较高仓位(15-25%)

请直接用Markdown格式回复：
### 激进型评估
- 建议仓位: XX%
- 操作建议: 加大仓位/买入/持有
- 预期收益: +XX%
- 机会分析: [具体理由]
"""

        try:
            msg = Msg(name="user", content=prompt, role="user")
            response = await self.reply(msg)
            content = self._extract_content(response.content)
            return {"perspective": "激进型", "content": content, "position": "20%"}
        except Exception as e:
            print(f"[{self.name}] 评估失败: {e}")
        
        return {"perspective": "激进型", "position": "25%", "content": "市场机会难得，建议适当提高仓位"}


class NeutralRisk(AgentBase):
    """中性型风险管理者 - 使用 AgentScope AgentBase 实现"""
    
    def __init__(self):
        super().__init__()
        self.name = "NeutralRisk"
        
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
        
        self.sys_prompt = """你是一名中性型风险管理者，追求风险与收益的平衡，基于量化数据进行评估。

你的特点:
1. 平衡分析，综合评估机会与风险
2. 建议适中的仓位配置(8-15%)
3. 强调风报比要合理（建议1:2以上）

要求：分析要客观全面，引用具体数据。请用中文回答。
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
                if hasattr(chunk, 'content') and chunk.content:
                    thinking, text = self._extract_thinking_and_text(chunk.content)
                    
                    # 显示 thinking 增量（灰色标记）
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
            content = self._extract_content(response.content)  # type: ignore[union-attr]
        
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
        if msg is not None:
            await self.memory.add(msg)
    
    async def handle_interrupt(self) -> Msg:
        return Msg(name=self.name, content="评估被中断。", role="assistant")
    
    def assess(self, trader_report: str) -> Dict:
        """评估交易决策（同步方法）"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._assess_async(trader_report))
        finally:
            loop.close()
    
    async def _assess_async(self, trader_report: str) -> Dict:
        """异步评估交易决策"""
        report_summary = trader_report[:600] if len(trader_report) > 600 else trader_report
        
        prompt = f"""请从中性型角度评估以下交易决策（300字内）：

{report_summary}

评估要求：平衡分析机会与风险，建议适中仓位(8-15%)，强调风报比

请直接用Markdown格式回复：
### 中性型评估
- 建议仓位: XX%
- 操作建议: 维持/调整/平衡
- 预期收益: +XX%
- 风报比: X:X
- 平衡分析: [具体理由]
"""

        try:
            msg = Msg(name="user", content=prompt, role="user")
            response = await self.reply(msg)
            content = self._extract_content(response.content)
            return {"perspective": "中性型", "content": content, "position": "10%"}
        except Exception as e:
            print(f"[{self.name}] 评估失败: {e}")
        
        return {"perspective": "中性型", "position": "10%", "content": "交易员的建议基本合理"}


class ConservativeRisk(AgentBase):
    """保守型风险管理者 - 使用 AgentScope AgentBase 实现"""
    
    def __init__(self):
        super().__init__()
        self.name = "ConservativeRisk"
        
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
        
        self.sys_prompt = """你是一名保守型风险管理者，优先考虑风险控制，基于量化数据进行评估。

你的特点:
1. 谨慎保守，善于发现风险因素
2. 风险容忍度较低
3. 建议较低的仓位配置(3-10%)
4. 量化最大可能损失

要求：分析要基于数据，不能危言耸听。请用中文回答。
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
                if hasattr(chunk, 'content') and chunk.content:
                    thinking, text = self._extract_thinking_and_text(chunk.content)
                    
                    # 显示 thinking 增量（灰色标记）
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
            content = self._extract_content(response.content)  # type: ignore[union-attr]
        
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
        if msg is not None:
            await self.memory.add(msg)
    
    async def handle_interrupt(self) -> Msg:
        return Msg(name=self.name, content="评估被中断。", role="assistant")
    
    def assess(self, trader_report: str) -> Dict:
        """评估交易决策（同步方法）"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._assess_async(trader_report))
        finally:
            loop.close()
    
    async def _assess_async(self, trader_report: str) -> Dict:
        """异步评估交易决策"""
        report_summary = trader_report[:600] if len(trader_report) > 600 else trader_report
        
        prompt = f"""请从保守型角度评估以下交易决策（300字内）：

{report_summary}

评估要求：重点识别潜在风险点，建议较低仓位(3-10%)，量化最大可能损失

请直接用Markdown格式回复：
### 保守型评估
- 建议仓位: XX%
- 操作建议: 降低仓位/谨慎/观望
- 最大损失: -XX%
- 风险警示: [具体风险点]
"""

        try:
            msg = Msg(name="user", content=prompt, role="user")
            response = await self.reply(msg)
            content = self._extract_content(response.content)
            return {"perspective": "保守型", "content": content, "position": "5%"}
        except Exception as e:
            print(f"[{self.name}] 评估失败: {e}")
        
        return {"perspective": "保守型", "position": "5%", "content": "市场存在不确定性，建议降低仓位"}


class RiskFacilitator(AgentBase):
    """风险讨论协调人 - 使用 AgentScope AgentBase 实现"""
    
    def __init__(self):
        super().__init__()
        self.name = "RiskFacilitator"
        
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
        
        self.sys_prompt = """你是一名专业的风险管理协调者，负责基于量化数据协调三种风险偏好。

你的职责:
1. 量化对比三种观点的仓位、风险等级、收益预期
2. 按权重(30%激进 + 40%中性 + 30%保守)计算综合仓位
3. 给出平衡后的风险等级
4. 提供具体的风控措施

要求：结论要客观公正，引用具体数据。请用中文回答。
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
                if hasattr(chunk, 'content') and chunk.content:
                    # 分别提取 thinking 和 text
                    thinking, text = self._extract_thinking_and_text(chunk.content)
                    
                    # 显示 thinking 增量（灰色标记）
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
            content = self._extract_content(response.content)  # type: ignore[union-attr]
        
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
        if msg is not None:
            await self.memory.add(msg)
    
    async def handle_interrupt(self) -> Msg:
        return Msg(name=self.name, content="协调被中断。", role="assistant")
    
    def facilitate_discussion(self, aggressive: AggressiveRisk, neutral: NeutralRisk,
                             conservative: ConservativeRisk, trader_report: str,
                             rounds: int = 2) -> str:
        """主持风险讨论（同步方法）"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self._facilitate_discussion_async(aggressive, neutral, conservative, trader_report, rounds)
            )
        finally:
            loop.close()
    
    async def _facilitate_discussion_async(self, aggressive: AggressiveRisk, neutral: NeutralRisk,
                                           conservative: ConservativeRisk, trader_report: str,
                                           rounds: int = 2) -> str:
        """异步主持风险讨论"""
        # 在异步方法中直接调用异步方法，避免嵌套事件循环
        agg_assess = await aggressive._assess_async(trader_report)
        neu_assess = await neutral._assess_async(trader_report)
        cons_assess = await conservative._assess_async(trader_report)
        
        recommendation = await self._make_recommendation_async(agg_assess, neu_assess, cons_assess)
        
        return self._generate_report(agg_assess, neu_assess, cons_assess, recommendation, rounds)
    
    async def _make_recommendation_async(self, agg: Dict, neu: Dict, cons: Dict) -> Dict:
        """异步形成最终风险建议"""
        def parse_position(pos_str):
            try:
                return float(str(pos_str).replace('%', ''))
            except:
                return 10.0
        
        agg_pos = parse_position(agg.get('position', '20%'))
        neu_pos = parse_position(neu.get('position', '10%'))
        cons_pos = parse_position(cons.get('position', '5%'))
        adjusted_position = (agg_pos * 0.3 + neu_pos * 0.4 + cons_pos * 0.3)
        
        prompt = f"""请协调三种风险管理者的评估（300字内）：

【激进型】建议仓位 {agg.get('position', '20%')}
{agg.get('content', '')[:200]}

【中性型】建议仓位 {neu.get('position', '10%')}
{neu.get('content', '')[:200]}

【保守型】建议仓位 {cons.get('position', '5%')}
{cons.get('content', '')[:200]}

协调要求：按权重(30%激进 + 40%中性 + 30%保守)计算综合仓位，提供风控措施

请直接用Markdown格式回复：
### 协调结果
- 综合仓位: XX%
- 风控措施: [具体措施]
- 综合结论: [结论]
"""

        try:
            msg = Msg(name="user", content=prompt, role="user")
            response = await self.reply(msg)
            content = self._extract_content(response.content)
            return {
                "adjusted_position": f"{adjusted_position:.1f}%",
                "content": content,
                "risk_controls": "设置止损线、分批建仓、密切关注市场变化"
            }
        except Exception as e:
            print(f"[{self.name}] 协调失败: {e}")
        
        return {
            "adjusted_position": f"{adjusted_position:.1f}%",
            "content": "综合三方观点，建议采取平衡策略",
            "risk_controls": "设置止损线、分批建仓、密切关注市场变化"
        }
    
    def _generate_report(self, agg: Dict, neu: Dict, cons: Dict, 
                        recommendation: Dict, rounds: int) -> str:
        return f"""# 风险管理讨论报告

## 讨论信息
- 讨论轮次: {rounds}
- 讨论时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 激进派观点
- 建议仓位: {agg.get('position', 'N/A')}
{agg.get('content', '')}

## 中性派观点
- 建议仓位: {neu.get('position', 'N/A')}
{neu.get('content', '')}

## 保守派观点
- 建议仓位: {cons.get('position', 'N/A')}
{cons.get('content', '')}

## 协调结果
- 风险调整后仓位: {recommendation.get('adjusted_position', 'N/A')}
- 风险控制措施: {recommendation.get('risk_controls', 'N/A')}

{recommendation.get('content', '')}
"""
