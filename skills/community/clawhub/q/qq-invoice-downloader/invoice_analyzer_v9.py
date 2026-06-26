#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InvoiceAnalyzer LLM 包装器 - Phase 1
保持与原 InvoiceAnalyzer 相同的接口，内部自动做 LLM fallback

触发条件：confidence < 0.7 或 invoice_type == "unknown"
"""

import os
import json
import logging
from typing import Dict, List, Any

# 尝试导入原有分析器
try:
    from invoice_analyzer import InvoiceAnalyzer, InvoiceType
except ImportError:
    InvoiceAnalyzer = None
    InvoiceType = None

logger = logging.getLogger("invoice")

# ===== MiniMax LLM 客户端 =====

class MiniMaxLLM:
    """MiniMax API 客户端（OpenAI 兼容格式）"""

    BASE_URL = "https://api.minimaxi.com/v1"

    def __init__(self, api_key: str = None, model: str = "MiniMax-M2.7"):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.model = model
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY 环境变量未设置")

    def chat(self, messages: List[Dict[str, str]],
             temperature: float = 0.2,
             max_tokens: int = 1024) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/text/chatcompletion_v2",
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                msg = result["choices"][0]["message"]
                return msg.get("content") or msg.get("reasoning_content") or ""
        except urllib.error.HTTPError as e:
            body = json.loads(e.read().decode("utf-8"))
            raise RuntimeError(f"LLM API 错误 {e.code}: {body.get('error', body)}")


SYSTEM_PROMPT = """你是一个专业的发票下载专家，擅长分析各种发票邮件并确定最佳下载策略。

## 输出格式（严格 JSON，无其他内容）
{
  "platform_name": "平台名称，如：和运国际、诺诺网、中海油、未知",
  "invoice_type": "direct_attachment | zip_attachment | direct_pdf_link | tax_platform | nuonuo | cnooc | unknown",
  "strategy": "direct_download | browser_simple | browser_multi | browser_tax",
  "confidence": 0.0-1.0,
  "reasoning": "50字以内的分析理由",
  "key_urls": ["关键URL列表，只保留最相关的1-3个"],
  "selectors": ["浏览器选择器，如包含'下载'的按钮CSS选择器，留空[]"],
  "skip_reason": "如果判断为非发票，填写跳过原因，否则填空字符串"
}

## 平台识别规则
- 和运国际（上海税务）：dppt.shanghai.chinatax.gov.cn，税务平台，需要浏览器
- 诺诺网：nnfp.jss.com.cn，需要浏览器点击"下载发票"
- 百旺金穗云：税务平台，需要浏览器
- 中海油：CNOOC/中国海油，常有"批量zip下载"
- 飒拉商业：ZARA，有PDF链接直接下载
- 中国联通：直接附件
- 12306火车票：直接附件或ZIP
- 通行费电子发票：ZIP

## 策略选择
- 直接附件/ZIP/PDF链接 → direct_download
- 单一下载按钮页面 → browser_simple
- 多步骤（登录→查找→下载）→ browser_multi
- 税务平台（和运国际等）→ browser_tax

## 注意：只输出JSON，不要有其他文字"""


class LLMInvoiceAnalyzer:
    """独立 LLM 分析器（不依赖原有 InvoiceAnalyzer）"""

    def __init__(self, api_key: str = None, model: str = "MiniMax-M2.7"):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.model = model
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = MiniMaxLLM(self.api_key, self.model)
        return self._llm

    def analyze(self, subject: str, text: str, html: str, has_attachments: bool) -> 'LLMAnalysisResult':
        """调用 LLM 分析邮件"""
        user_prompt = f"""## 邮件信息
- 主题：{subject}
- 正文：{text[:2000] if text else '(无正文)'}
- HTML：{html[:2000] if html else '(无HTML)'}
- 附件：{'有' if has_attachments else '无'}

分析这张发票邮件，输出JSON。"""

        try:
            raw = self.llm.chat(
                [{"role": "system", "content": SYSTEM_PROMPT},
                 {"role": "user", "content": user_prompt}],
                temperature=0.2, max_tokens=1024
            )
            data = json.loads(self._extract_json(raw))

            skip_reason = data.get("skip_reason", "")
            if skip_reason:
                return LLMAnalysisResult(
                    invoice_type="unknown",
                    strategy="manual",
                    urls=data.get("key_urls", []),
                    confidence=float(data.get("confidence", 0.5)),
                    notes=f"跳过：{skip_reason}",
                    selectors=data.get("selectors", []),
                    platform_name=data.get("platform_name", "未知"),
                    llm_used=True,
                    reasoning=data.get("reasoning", "")
                )

            return LLMAnalysisResult(
                invoice_type=data.get("invoice_type", "unknown"),
                strategy=data.get("strategy", "browser_simple"),
                urls=data.get("key_urls", []),
                confidence=float(data.get("confidence", 0.5)),
                notes=data.get("reasoning", ""),
                selectors=data.get("selectors", []),
                platform_name=data.get("platform_name", "未知平台"),
                llm_used=True,
                reasoning=data.get("reasoning", "")
            )
        except Exception as e:
            logger.warning(f"LLM 分析失败，降级: {e}")
            return LLMAnalysisResult(
                invoice_type="unknown",
                strategy="browser_simple",
                urls=[],
                confidence=0.3,
                notes=f"LLM错误: {e}，使用默认浏览器策略",
                selectors=[],
                llm_used=True,
                reasoning="LLM调用失败"
            )

    def _extract_json(self, raw: str) -> str:
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:] if lines[0].startswith("```") else lines)
            raw = raw.rstrip("```").rstrip()
        return raw.strip()


class LLMAnalysisResult:
    """兼容 v82 InvoiceAnalyzer 返回格式的分析结果"""
    def __init__(self, invoice_type: str, strategy: str, urls: List[str],
                 confidence: float, notes: str, selectors: List[str],
                 platform_name: str = "", llm_used: bool = False, reasoning: str = ""):
        self.invoice_type = InvoiceTypeResult(invoice_type)
        self.strategy = StrategyResult(strategy)
        self.urls = urls
        self.confidence = confidence
        self.notes = notes
        self.selectors = selectors
        self.platform_name = platform_name
        self.llm_used = llm_used
        self.reasoning = reasoning


class InvoiceTypeResult:
    """兼容 InvoiceType enum"""
    def __init__(self, value: str):
        self.value = value


class StrategyResult:
    """兼容 DownloadStrategy enum"""
    def __init__(self, value: str):
        self.value = value


class InvoiceAnalyzerWithLLM:
    """
    Phase 1: LLM 增强版 InvoiceAnalyzer

    策略：
    1. 优先使用原有硬编码分析器（速度快，零成本）
    2. 当 confidence < 0.7 或平台未知时，自动调用 LLM
    3. LLM 未配置时，无条件降级到硬编码（保持 v8.2 行为）
    """

    # LLM 触发阈值
    LLM_CONFIDENCE_THRESHOLD = 0.7

    def __init__(self, api_key: str = None):
        """
        Args:
            api_key: MiniMax API Key，不传则从 MINIMAX_API_KEY 读取
        """
        self.base_analyzer = InvoiceAnalyzer() if InvoiceAnalyzer else None
        self.llm_analyzer = None
        self._api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self._llm_available = bool(self._api_key)

        if self._llm_available:
            try:
                self.llm_analyzer = LLMInvoiceAnalyzer(self._api_key)
                logger.info("✅ LLM 分析器已就绪（Phase 1 启用）")
            except Exception as e:
                logger.warning(f"⚠️ LLM 初始化失败: {e}，仅使用硬编码分析器")
                self._llm_available = False
        else:
            logger.info("ℹ️ MINIMAX_API_KEY 未设置，使用纯硬编码分析器（v8.2模式）")

    def analyze(self, subject: str, text: str, html: str, has_attachments: bool):
        """
        分析邮件，自动选择硬编码或 LLM

        Returns:
            InvoiceAnalysis 结果对象（兼容 v8.2 InvoiceAnalyzer 接口）
        """
        if self.base_analyzer is None:
            # 没有原分析器，必须用 LLM
            if self.llm_analyzer:
                return self.llm_analyzer.analyze(subject, text, html, has_attachments)
            raise RuntimeError("无可用分析器")

        # Step 1: 硬编码分析器优先
        base_result = self.base_analyzer.analyze(subject, text, html, has_attachments)

        # Step 2: 判断是否需要 LLM fallback
        need_llm = (
            base_result.confidence < self.LLM_CONFIDENCE_THRESHOLD or
            base_result.invoice_type.value == "unknown"
        )

        if not need_llm:
            return base_result

        # Step 3: LLM fallback
        if not self._llm_available:
            logger.info(f"   ⚡ 置信度 {base_result.confidence:.2f} < {self.LLM_CONFIDENCE_THRESHOLD}，"
                        f"但 LLM 未配置，使用硬编码结果")
            return base_result

        logger.info(f"   🤖 置信度 {base_result.confidence:.2f} < {self.LLM_CONFIDENCE_THRESHOLD}，"
                    f"触发 LLM 分析...")
        try:
            llm_result = self.llm_analyzer.analyze(subject, text, html, has_attachments)
            if llm_result.confidence > base_result.confidence:
                logger.info(f"   ✅ LLM 胜出：置信度 {llm_result.confidence:.2f} > {base_result.confidence:.2f}，"
                            f"平台={llm_result.platform_name}，策略={llm_result.strategy.value}")
                return llm_result
            else:
                logger.info(f"   ⬇️ LLM 置信度 {llm_result.confidence:.2f} ≤ 硬编码 {base_result.confidence:.2f}，"
                            f"保留硬编码结果")
                return base_result
        except Exception as e:
            logger.warning(f"   ⚠️ LLM 调用失败，退回硬编码: {e}")
            return base_result
