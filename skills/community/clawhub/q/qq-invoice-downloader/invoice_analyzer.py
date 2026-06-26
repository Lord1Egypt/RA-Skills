#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票邮件智能分析器
根据邮件内容自动分析并选择最佳下载策略
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class InvoiceType(Enum):
    """发票类型枚举"""
    DIRECT_ATTACHMENT = "direct_attachment"  # 直接附件
    ZIP_ATTACHMENT = "zip_attachment"        # 压缩包附件
    DIRECT_PDF_LINK = "direct_pdf_link"      # 直接PDF链接
    TAX_PLATFORM = "tax_platform"            # 税务平台(和运国际等)
    NUONUO = "nuonuo"                        # 诺诺发票
    HANGTIAN = "hangtian"                    # 航天信息
    SHUNFENG = "shunfeng"                    # 顺丰
    CNOOC = "cnooc"                         # 中海油
    TRAIN_12306 = "train_12306"             # 12306火车票
    # ---- Phase 2 新增平台 ----
    EXPRESS = "express"                      # 快递物流 (邮政/中通/韵达/圆通/申通)
    ECOMMERCE = "ecommerce"                  # 电商平台 (京东/拼多多/美团/饿了么/大众点评)
    TRANSPORT = "transport"                  # 出行平台 (滴滴/高德/曹操)
    TRAVEL = "travel"                        # 旅游出行 (携程/同程/飞猪/酒店)
    TECH = "tech"                            # 科技云服务 (腾讯/阿里云/华为云/京东云)
    OPERATOR = "operator"                    # 运营商 (移动/联通/电信)
    BANK = "bank"                            # 银行 (招商/平安)
    BAIWANG = "baiwang"                      # 百旺金穗云
    PIAOYITONG = "piaoyitong"                # 票易通
    UNKNOWN = "unknown"                      # 未知类型

class DownloadStrategy(Enum):
    """下载策略枚举"""
    DIRECT_DOWNLOAD = "direct_download"      # 直接下载
    BROWSER_SIMPLE = "browser_simple"        # 简单浏览器点击
    BROWSER_MULTI_STEP = "browser_multi"     # 多步骤浏览器
    BROWSER_TAX_PLATFORM = "browser_tax"     # 税务平台特殊处理
    MANUAL = "manual"                        # 需要手动处理

@dataclass
class InvoiceAnalysis:
    """发票分析结果"""
    invoice_type: InvoiceType
    strategy: DownloadStrategy
    urls: List[str]
    confidence: float  # 置信度 0-1
    notes: str
    selectors: List[str]  # 推荐的选择器

class InvoiceAnalyzer:
    """发票邮件智能分析器"""
    
    # 平台特征关键词
    PLATFORM_PATTERNS = {
        InvoiceType.TAX_PLATFORM: [
            'chinatax.gov.cn',
            'dppt.shanghai',
            '和运国际',
            '电子税务局',
            '税务'
        ],
        InvoiceType.NUONUO: [
            'nnfp.jss.com.cn',
            '诺诺',
            'nuonuo'
        ],
        InvoiceType.HANGTIAN: [
            'hangtian',
            '航天',
            '航天信息',
            'aisino'
        ],
        InvoiceType.SHUNFENG: [
            'sf-express',
            '顺丰',
            'shunfeng'
        ],
        InvoiceType.CNOOC: [
            'cnooc',
            '中海油',
            '中国海油',
            'zzslg.cnooc',
            '批量zip下载'
        ],
        InvoiceType.TRAIN_12306: [
            '12306',
            '铁路',
            '火车票'
        ],
        # ---- Phase 2 新增平台 ----
        InvoiceType.BAIWANG: [
            'baiwang',
            '百旺金穗云',
            'baiwang.com',
            '百旺'
        ],
        InvoiceType.PIAOYITONG: [
            'piaoyitong',
            '票易通',
            'piaoyitong.com'
        ],
        InvoiceType.EXPRESS: [
            'ems.com.cn',
            '中国邮政',
            'EMS',
            'zto.com',
            '中通快递',
            'yundaex.com',
            '韵达',
            'yto.net.cn',
            '圆通',
            'sto.cn',
            '申通'
        ],
        InvoiceType.ECOMMERCE: [
            'jd.com',
            '京东',
            'pinduoduo.com',
            '拼多多',
            'meituan.com',
            '美团',
            'ele.me',
            '饿了么',
            'dianping.com',
            '大众点评'
        ],
        InvoiceType.TRANSPORT: [
            'didiglobal.com',
            '滴滴',
            'didi',
            'amap.com',
            '高德',
            'caocaokeji.cn',
            '曹操出行'
        ],
        InvoiceType.TRAVEL: [
            'ctrip.com',
            '携程',
            'ly.com',
            '同程',
            'fliggy.com',
            '飞猪',
            'hotel.com',
            'agoda.com',
            'booking.com',
            '酒店预订'
        ],
        InvoiceType.TECH: [
            'cloud.tencent.com',
            '腾讯云',
            'aliyun.com',
            '阿里云',
            'huaweicloud.com',
            '华为云',
            'jdcloud.com',
            '京东云'
        ],
        InvoiceType.OPERATOR: [
            '10086.cn',
            '中国移动',
            '10010.com',
            '中国联通',
            '189.cn',
            '中国电信'
        ],
        InvoiceType.BANK: [
            'cmbchina.com',
            '招商银行',
            'pingan.com',
            '平安银行'
        ]
    }
    
    # 下载按钮选择器模板
    SELECTOR_TEMPLATES = {
        InvoiceType.TAX_PLATFORM: [
            'button:has-text("PDF下载")',
            'button:has-text("下载")',
            'a:has-text("下载PDF")',
            '[id*="download"]',
            '[class*="download"]',
            'button:has-text("电子发票下载")',
        ],
        InvoiceType.NUONUO: [
            'button:has-text("下载发票")',
            'a:has-text("下载发票")',
            'button:has-text("PDF下载")',
            '[data-action="download"]',
        ],
        InvoiceType.HANGTIAN: [
            'button:has-text("下载电子票")',
            'a:has-text("电子发票下载")',
            'button:has-text("下载")',
        ],
        InvoiceType.SHUNFENG: [
            'button:has-text("下载")',
            'a:has-text("下载电子发票")',
        ],
        InvoiceType.CNOOC: [
            'button:has-text("批量zip下载")',
            'a:has-text("批量zip下载")',
            'button:has-text("下载")',
            'a:has-text("电子发票下载")',
            'button:has-text("批量下载")',
            'a:has-text("批量下载")',
        ],
        InvoiceType.TRAIN_12306: [
            'button:has-text("下载")',
            'a:has-text("PDF下载")',
        ],
        # ---- Phase 2 新增选择器模板 ----
        InvoiceType.BAIWANG: [
            'button:has-text("电子发票下载")',
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="download-btn"]',
        ],
        InvoiceType.PIAOYITONG: [
            'a:has-text("下载发票")',
            'button:has-text("下载")',
            '[class*="download-invoice"]',
        ],
        InvoiceType.EXPRESS: [
            'a:has-text("下载电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        InvoiceType.ECOMMERCE: [
            'a:has-text("电子发票下载")',
            'button:has-text("下载发票")',
            '[class*="invoice-download"]',
        ],
        InvoiceType.TRANSPORT: [
            'a:has-text("电子发票")',
            'button:has-text("下载发票")',
            '[class*="invoice-download"]',
        ],
        InvoiceType.TRAVEL: [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        InvoiceType.TECH: [
            'a:has-text("电子发票")',
            'button:has-text("开具发票")',
            '[class*="invoice-btn"]',
        ],
        InvoiceType.OPERATOR: [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        InvoiceType.BANK: [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ]
    }
    
    def analyze(self, subject: str, text: str, html: str, has_attachments: bool) -> InvoiceAnalysis:
        """
        分析邮件内容，返回分析结果
        
        Args:
            subject: 邮件主题
            text: 邮件纯文本内容
            html: 邮件HTML内容
            has_attachments: 是否有附件
            
        Returns:
            InvoiceAnalysis: 分析结果
        """
        full_content = f"{subject} {text} {html}"
        
        # 1. 检查是否有附件
        if has_attachments:
            return self._analyze_attachment(subject, text, html)
        
        # 2. 提取URL
        urls = self._extract_urls(full_content)
        
        # 3. 识别平台类型
        invoice_type = self._identify_platform(full_content, urls)
        
        # 4. 确定下载策略
        strategy = self._determine_strategy(invoice_type, urls)
        
        # 5. 获取推荐选择器
        selectors = self.SELECTOR_TEMPLATES.get(invoice_type, [])
        
        # 6. 计算置信度
        confidence = self._calculate_confidence(invoice_type, urls, has_attachments)
        
        # 7. 生成说明
        notes = self._generate_notes(invoice_type, strategy, urls)
        
        return InvoiceAnalysis(
            invoice_type=invoice_type,
            strategy=strategy,
            urls=urls,
            confidence=confidence,
            notes=notes,
            selectors=selectors
        )
    
    def _analyze_attachment(self, subject: str, text: str, html: str) -> InvoiceAnalysis:
        """分析附件类型邮件"""
        content = f"{subject} {text} {html}"
        
        # 检查是否是压缩包
        if any(ext in content.lower() for ext in ['.zip', '压缩包', 'rar']):
            return InvoiceAnalysis(
                invoice_type=InvoiceType.ZIP_ATTACHMENT,
                strategy=DownloadStrategy.DIRECT_DOWNLOAD,
                urls=[],
                confidence=0.9,
                notes="ZIP压缩包附件，需要解压后提取PDF",
                selectors=[]
            )
        
        return InvoiceAnalysis(
            invoice_type=InvoiceType.DIRECT_ATTACHMENT,
            strategy=DownloadStrategy.DIRECT_DOWNLOAD,
            urls=[],
            confidence=0.95,
            notes="直接附件下载",
            selectors=[]
        )
    
    def _extract_urls(self, content: str) -> List[str]:
        """提取所有URL"""
        urls = []
        
        # 标准URL
        standard = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
        urls.extend(standard)
        
        # 编码URL
        encoded = re.findall(r'https?%3A%2F%2F[^\s<>"{}|\\^`\[\]]+', content)
        from urllib.parse import unquote
        for url in encoded:
            try:
                urls.append(unquote(url))
            except:
                pass
        
        # href中的URL
        hrefs = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        urls.extend(hrefs)
        
        # 去重
        seen = set()
        unique = []
        for url in urls:
            url = url.strip().rstrip('>"\'')
            if url not in seen and len(url) > 20:
                seen.add(url)
                unique.append(url)
        
        return unique
    
    def _identify_platform(self, content: str, urls: List[str]) -> InvoiceType:
        """识别发票平台类型"""
        content_lower = content.lower()
        
        for platform, patterns in self.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    return platform
                for url in urls:
                    if pattern.lower() in url.lower():
                        return platform
        
        # 检查是否是直接PDF链接
        for url in urls:
            if url.lower().endswith('.pdf'):
                return InvoiceType.DIRECT_PDF_LINK
        
        return InvoiceType.UNKNOWN
    
    def _determine_strategy(self, invoice_type: InvoiceType, urls: List[str]) -> DownloadStrategy:
        """确定下载策略"""
        if invoice_type == InvoiceType.DIRECT_ATTACHMENT:
            return DownloadStrategy.DIRECT_DOWNLOAD
        elif invoice_type == InvoiceType.ZIP_ATTACHMENT:
            return DownloadStrategy.DIRECT_DOWNLOAD
        elif invoice_type == InvoiceType.DIRECT_PDF_LINK:
            # v8.0: 如果URL中有.pdf链接，使用DIRECT_DOWNLOAD
            # 否则使用浏览器处理
            pdf_urls = [u for u in urls if '.pdf' in u.lower()]
            if pdf_urls:
                return DownloadStrategy.DIRECT_DOWNLOAD
            else:
                return DownloadStrategy.BROWSER_SIMPLE
        elif invoice_type == InvoiceType.TAX_PLATFORM:
            return DownloadStrategy.BROWSER_TAX_PLATFORM
        elif invoice_type in [InvoiceType.NUONUO, InvoiceType.HANGTIAN]:
            return DownloadStrategy.BROWSER_MULTI_STEP
        elif invoice_type == InvoiceType.UNKNOWN:
            return DownloadStrategy.BROWSER_SIMPLE
        else:
            return DownloadStrategy.BROWSER_SIMPLE
    
    def _calculate_confidence(self, invoice_type: InvoiceType, urls: List[str], has_attachments: bool) -> float:
        """计算分析置信度"""
        confidence = 0.5
        
        # 有附件时置信度高
        if has_attachments:
            confidence += 0.3
        
        # 找到URL增加置信度
        if urls:
            confidence += 0.2
        
        # 已知平台类型增加置信度
        if invoice_type != InvoiceType.UNKNOWN:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _generate_notes(self, invoice_type: InvoiceType, strategy: DownloadStrategy, urls: List[str]) -> str:
        """生成说明文字"""
        notes = f"识别为: {invoice_type.value}, 策略: {strategy.value}"
        if urls:
            notes += f", 找到 {len(urls)} 个URL"
        return notes


# 使用示例
if __name__ == "__main__":
    analyzer = InvoiceAnalyzer()
    
    # 测试案例
    test_cases = [
        {
            "name": "和运国际",
            "subject": "和运国际电子发票通知",
            "text": "请点击链接下载发票 https://dppt.shanghai.chinatax.gov.cn:8443/v/xxx",
            "html": "",
            "has_attachments": False
        },
        {
            "name": "直接PDF",
            "subject": "电子发票",
            "text": "发票下载: https://example.com/invoice.pdf",
            "html": "",
            "has_attachments": False
        },
        {
            "name": "ZIP附件",
            "subject": "发票文件导出成功",
            "text": "",
            "html": "",
            "has_attachments": True
        }
    ]
    
    for case in test_cases:
        result = analyzer.analyze(
            case["subject"],
            case["text"],
            case["html"],
            case["has_attachments"]
        )
        print(f"\n{case['name']}:")
        print(f"  类型: {result.invoice_type.value}")
        print(f"  策略: {result.strategy.value}")
        print(f"  置信度: {result.confidence}")
        print(f"  说明: {result.notes}")
        print(f"  URL数: {len(result.urls)}")
