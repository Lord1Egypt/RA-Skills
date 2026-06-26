#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 增强型发票邮件分析器 - Phase 1
当硬编码分析器置信度 < 0.7 或平台未知时，调用 LLM 分析

用法：
    set MINIMAX_API_KEY=你的API密钥
    python invoice_downloader_v9.py 260201 260310
"""

import os
import json
import re
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum

# ===== MiniMax LLM 客户端 =====

class MiniMaxLLM:
    """MiniMax API 客户端（OpenAI 兼容格式）"""

    BASE_URL = "https://api.minimaxi.com/v1"

    def __init__(self, api_key: str = None, model: str = "MiniMax-M2.7"):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.model = model
        if not self.api_key:
            raise ValueError("需要设置 MINIMAX_API_KEY 环境变量")

    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.3,
             max_tokens: int = 1024) -> str:
        """
        发送对话请求，返回文本内容
        
        Args:
            messages: [{"role": "user", "content": "..."}]
            temperature: 0.0=确定输出, 0.7=平衡, 1.0=创意
            max_tokens: 最大输出 token 数
        """
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
                # MiniMax 模型：content 可能为空，内容在 reasoning_content
                return msg.get("content") or msg.get("reasoning_content") or ""
        except urllib.error.HTTPError as e:
            body = json.loads(e.read().decode("utf-8"))
            raise RuntimeError(f"LLM API 错误 {e.code}: {body.get('error', body)}")


# ===== 分析结果结构 =====

class InvoiceType(Enum):
    DIRECT_ATTACHMENT = "direct_attachment"
    ZIP_ATTACHMENT = "zip_attachment"
    DIRECT_PDF_LINK = "direct_pdf_link"
    TAX_PLATFORM = "tax_platform"
    NUONUO = "nuonuo"
    HANGTIAN = "hangtian"
    SHUNFENG = "shunfeng"
    CNOOC = "cnooc"
    TRAIN_12306 = "train_12306"
    UNKNOWN = "unknown"

class DownloadStrategy(Enum):
    DIRECT_DOWNLOAD = "direct_download"
    BROWSER_SIMPLE = "browser_simple"
    BROWSER_MULTI_STEP = "browser_multi"
    BROWSER_TAX_PLATFORM = "browser_tax"
    MANUAL = "manual"

@dataclass
class InvoiceAnalysis:
    invoice_type: str
    strategy: str
    urls: List[str]
    confidence: float
    notes: str
    selectors: List[str]
    platform_name: str = ""
    llm_used: bool = False
    reasoning: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ===== LLM Prompt =====

SYSTEM_PROMPT = """你是一个专业的发票下载专家，擅长分析各种发票邮件并确定最佳下载策略。

## 你的任务
分析邮件内容，输出一个 JSON 对象描述下载策略。

## 输出格式（严格 JSON，无其他内容）
{
  "platform_name": "平台名称，如：和运国际、诺诺网、中海油、未知",
  "invoice_type": "direct_attachment | zip_attachment | direct_pdf_link | tax_platform | nuonuo | cnooc | unknown",
  "strategy": "direct_download | browser_simple | browser_multi | browser_tax",
  "confidence": 0.0-1.0,
  "reasoning": "50字以内的分析理由",
  "key_urls": ["关键URL列表，只保留最相关的1-3个"],
  "selectors": ["浏览器选择器，如包含'下载'的按钮CSS选择器，留空[]"],
  "action_steps": ["如需浏览器操作，列出点击步骤"],
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

## 注意事项
- 只输出 JSON，不要有其他文字
- skip_reason 非空表示这不是发票邮件，应跳过
- confidence 低于 0.6 时用 browser_simple 作为默认策略
"""

USER_PROMPT_TEMPLATE = """## 邮件信息
- 主题：{subject}
- 正文：
{text}
- HTML内容：
{html}
- 是否有附件：{has_attachments}

请分析这张发票邮件，输出JSON。"""


# ===== LLM 分析器 =====

class LLMInvoiceAnalyzer:
    """LLM 增强型发票分析器"""

    def __init__(self, api_key: str = None, model: str = "MiniMax-M2.5-Lightning"):
        """
        初始化 LLM 分析器
        
        Args:
            api_key: MiniMax API Key，不传则从 MINIMAX_API_KEY 环境变量读取
            model: 使用的模型，默认 MiniMax-M2.5-Lightning（速度快便宜）
        """
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.model = model
        self._llm: Optional[MiniMaxLLM] = None

    @property
    def llm(self) -> MiniMaxLLM:
        if self._llm is None:
            if not self.api_key:
                raise RuntimeError(
                    "LLM 分析未启用：请设置 MINIMAX_API_KEY 环境变量\n"
                    "  Windows: set MINIMAX_API_KEY=你的密钥\n"
                    "  或运行: python -c \"import os; os.environ['MINIMAX_API_KEY']='你的密钥'\""
                )
            self._llm = MiniMaxLLM(self.api_key, self.model)
        return self._llm

    def analyze(self, subject: str, text: str, html: str, 
                has_attachments: bool) -> InvoiceAnalysis:
        """
        使用 LLM 分析邮件内容
        
        Args:
            subject: 邮件主题
            text: 纯文本内容
            html: HTML 内容
            has_attachments: 是否有附件
            
        Returns:
            InvoiceAnalysis: 包含完整分析结果的 dataclass
        """
        user_prompt = USER_PROMPT_TEMPLATE.format(
            subject=subject,
            text=text or "(无正文)",
            html=html or "(无HTML)",
            has_attachments="是" if has_attachments else "否"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        raw = self.llm.chat(messages, temperature=0.2, max_tokens=1024)

        # 提取 JSON（可能有 markdown 包裹）
        json_str = self._extract_json(raw)
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            # LLM 输出格式错误，降级
            return InvoiceAnalysis(
                invoice_type="unknown",
                strategy="browser_simple",
                urls=[],
                confidence=0.3,
                notes=f"LLM解析失败: {e}，使用默认策略",
                selectors=[],
                llm_used=True,
                reasoning="LLM JSON解析失败，降级为简单浏览器策略"
            )

        # 验证必填字段
        skip_reason = data.get("skip_reason", "")
        if skip_reason:
            return InvoiceAnalysis(
                invoice_type="unknown",
                strategy="manual",
                urls=data.get("key_urls", []),
                confidence=float(data.get("confidence", 0.5)),
                notes=f"跳过：{skip_reason}",
                selectors=data.get("selectors", []),
                llm_used=True,
                reasoning=data.get("reasoning", "非发票邮件")
            )

        return InvoiceAnalysis(
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

    def _extract_json(self, raw: str) -> str:
        """从 LLM 输出中提取 JSON 字符串"""
        raw = raw.strip()
        # 去掉 markdown 代码块包裹
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:] if lines[0].startswith("```") else lines)
            raw = raw.rstrip("```").rstrip()
        # 去掉前后空白
        return raw.strip()


# ===== 使用示例 =====

if __name__ == "__main__":
    import sys

    # 检查 API key
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        print("⚠️  MINIMAX_API_KEY 未设置，LLM 功能不可用")
        print("   设置方式：")
        print("   Windows: set MINIMAX_API_KEY=你的密钥")
        print("   运行以下命令测试硬编码分析器：")
        print()
        # 回退到内置分析器演示
        from invoice_analyzer import InvoiceAnalyzer
        analyzer = InvoiceAnalyzer()
        result = analyzer.analyze(
            "和运国际电子发票通知",
            "请点击链接下载发票 https://dppt.shanghai.chinatax.gov.cn:8443/v/xxx",
            "", False
        )
        print(f"硬编码分析结果：{result.invoice_type.value}, 置信度: {result.confidence}")
        sys.exit(0)

    # LLM 分析演示
    analyzer = LLMInvoiceAnalyzer(api_key)
    
    test_cases = [
        {
            "name": "和运国际税务",
            "subject": "【和运国际】电子发票开具成功",
            "text": "贵公司申请的电子发票已开具完成，请点击下方链接进入电子税务局下载。https://dppt.shanghai.chinatax.gov.cn:8443/web/xw/slist4.do",
            "html": "",
            "has_attachments": False
        },
        {
            "name": "中海油批量",
            "subject": "中国海油电子发票下载通知",
            "text": "您的电子发票已开具，请点击批量zip下载按钮进行下载。",
            "html": "",
            "has_attachments": False
        },
        {
            "name": "诺诺网",
            "subject": "诺诺网发票下载提醒",
            "text": "您的发票已开好，请登录诺诺网下载。https://nnfp.jss.com.cn/",
            "html": "",
            "has_attachments": False
        }
    ]

    for case in test_cases:
        print(f"\n测试: {case['name']}")
        result = analyzer.analyze(
            case["subject"], case["text"], case["html"], case["has_attachments"]
        )
        print(f"  平台: {result.platform_name}")
        print(f"  类型: {result.invoice_type}")
        print(f"  策略: {result.strategy}")
        print(f"  置信度: {result.confidence}")
        print(f"  推理: {result.reasoning}")
        print(f"  URLs: {result.urls}")
        if result.selectors:
            print(f"  选择器: {result.selectors}")
