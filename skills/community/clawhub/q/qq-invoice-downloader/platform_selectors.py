#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平台选择器数据库 - Phase 2
包含 30+ 平台的下载按钮选择器
"""

from typing import Dict, List

# ============================================================================
# 平台 Selector 数据库
# ============================================================================

PLATFORM_SELECTORS: List[Dict] = [
    # --------------------------------------------------------------------------
    # 税务平台类 (tax_platform)
    # --------------------------------------------------------------------------
    {
        "name": "百旺金穗云",
        "domain": ["baiwang.com", "www.baiwang.com", "fp.baiwang.com"],
        "invoice_type": "tax_platform",
        "strategy": "browser_tax",
        "selectors": [
            'button:has-text("电子发票下载")',
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="download-btn"]',
            '[class*="invoice-download"]',
        ],
        "notes": "百旺金穗云税盘平台，需浏览器点击下载"
    },
    {
        "name": "票易通",
        "domain": ["piaoyitong.com", "www.piaoyitong.com", "inv.piaoyitong.com"],
        "invoice_type": "tax_platform",
        "strategy": "browser_tax",
        "selectors": [
            'a:has-text("下载发票")',
            'button:has-text("下载")',
            '[class*="download-invoice"]',
            'a:has-text("电子发票")',
        ],
        "notes": "票易通发票平台，支持电子发票下载"
    },
    {
        "name": "航天信息",
        "domain": ["aisino.com", "www.aisino.com", "fp.aisino.com"],
        "invoice_type": "hangtian",
        "strategy": "browser_tax",
        "selectors": [
            'button:has-text("下载电子票")',
            'a:has-text("电子发票下载")',
            'button:has-text("下载")',
            '[id*="download"]',
        ],
        "notes": "航天信息服务平台"
    },
    {
        "name": "和运国际",
        "domain": ["dppt.shanghai", "chinatax.gov.cn", "etax.shanghai"],
        "invoice_type": "tax_platform",
        "strategy": "browser_tax",
        "selectors": [
            'button:has-text("PDF下载")',
            'button:has-text("下载")',
            'a:has-text("下载PDF")',
            '[id*="download"]',
            '[class*="download"]',
        ],
        "notes": "上海电子税务局，需浏览器点击"
    },

    # --------------------------------------------------------------------------
    # 快递物流类 (shunfeng / express)
    # --------------------------------------------------------------------------
    {
        "name": "顺丰速运",
        "domain": ["sf-express.com", "www.sf-express.com", "sf.com"],
        "invoice_type": "shunfeng",
        "strategy": "browser_simple",
        "selectors": [
            'button:has-text("下载")',
            'a:has-text("下载电子发票")',
            '[class*="download"]',
            'button:has-text("电子发票")',
        ],
        "notes": "顺丰快递发票，需登录后下载"
    },
    {
        "name": "中国邮政",
        "domain": ["ems.com.cn", "www.ems.com.cn", "chinapost.com.cn"],
        "invoice_type": "express",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("下载电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "中国邮政EMS发票"
    },
    {
        "name": "中通快递",
        "domain": ["zto.com", "www.zto.com"],
        "invoice_type": "express",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票下载")',
            'button:has-text("下载")',
            '[class*="invoice-btn"]',
        ],
        "notes": "中通快递发票"
    },
    {
        "name": "韵达快递",
        "domain": ["yundaex.com", "www.yundaex.com", "yunda.com"],
        "invoice_type": "express",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="download-btn"]',
        ],
        "notes": "韵达快递发票"
    },
    {
        "name": "圆通速递",
        "domain": ["yto.net.cn", "www.yto.net.cn"],
        "invoice_type": "express",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("下载电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "圆通速递发票"
    },
    {
        "name": "申通快递",
        "domain": ["sto.cn", "www.sto.cn", "shentong.com"],
        "invoice_type": "express",
        "strategy": "browser_simple",
        "selectors": [
            'button:has-text("电子发票下载")',
            'a:has-text("下载")',
            '[class*="download-invoice"]',
        ],
        "notes": "申通快递发票"
    },

    # --------------------------------------------------------------------------
    # 电商平台类 (ecommerce)
    # --------------------------------------------------------------------------
    {
        "name": "京东电子发票",
        "domain": ["jd.com", "www.jd.com", "invoice.jd.com"],
        "invoice_type": "ecommerce",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票下载")',
            'button:has-text("下载发票")',
            '[id*="downloadInvoice"]',
            '[class*="invoice-download"]',
        ],
        "notes": "京东平台发票"
    },
    {
        "name": "拼多多商家发票",
        "domain": ["pinduoduo.com", "www.pinduoduo.com", "mms.pinduoduo.com"],
        "invoice_type": "ecommerce",
        "strategy": "browser_multi",
        "selectors": [
            'button:has-text("申请开票")',
            'a:has-text("发票下载")',
            '[class*="invoice-btn"]',
        ],
        "notes": "拼多多商家后台发票管理"
    },
    {
        "name": "美团发票",
        "domain": ["meituan.com", "www.meituan.com", "invoice.meituan.com"],
        "invoice_type": "ecommerce",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "美团平台发票"
    },

    # --------------------------------------------------------------------------
    # 出行平台类 (transport)
    # --------------------------------------------------------------------------
    {
        "name": "滴滴出行",
        "domain": ["didiglobal.com", "www.didiglobal.com", "page.didiglobal.com"],
        "invoice_type": "transport",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载发票")',
            '[class*="invoice-download"]',
            'a:has-text("开具发票")',
        ],
        "notes": "滴滴出行发票，需登录后申请"
    },
    {
        "name": "高德打车",
        "domain": ["amap.com", "www.amap.com", "didu.amap.com"],
        "invoice_type": "transport",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-btn"]',
        ],
        "notes": "高德打车发票"
    },
    {
        "name": "曹操出行",
        "domain": ["caocaokeji.cn", "www.caocaokeji.cn", "i.caocaokeji.cn"],
        "invoice_type": "transport",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "曹操出行发票"
    },

    # --------------------------------------------------------------------------
    # 旅游出行类 (travel)
    # --------------------------------------------------------------------------
    {
        "name": "携程发票",
        "domain": ["ctrip.com", "www.ctrip.com", "invoice.ctrip.com"],
        "invoice_type": "travel",
        "strategy": "browser_multi",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
            '[id*="invoice"]',
        ],
        "notes": "携程旅行发票，需多步操作"
    },
    {
        "name": "同程旅行",
        "domain": ["ly.com", "www.ly.com", "tp.ly.com"],
        "invoice_type": "travel",
        "strategy": "browser_multi",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载发票")',
            '[class*="invoice-btn"]',
        ],
        "notes": "同程旅行发票"
    },
    {
        "name": "飞猪机票",
        "domain": ["fliggy.com", "www.fliggy.com", "trip.alipay.com"],
        "invoice_type": "travel",
        "strategy": "browser_multi",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "飞猪机票发票"
    },
    {
        "name": "酒店预订",
        "domain": ["hotel.com", "www.hotel.com", "agoda.com", "booking.com"],
        "invoice_type": "travel",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("Invoice")',
            'button:has-text("Download")',
            '[class*="invoice-btn"]',
            'a:has-text("电子发票")',
        ],
        "notes": "酒店预订发票"
    },
    {
        "name": "饿了么",
        "domain": ["ele.me", "www.ele.me", "mail.ele.me"],
        "invoice_type": "ecommerce",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "饿了么外卖发票"
    },
    {
        "name": "大众点评",
        "domain": ["dianping.com", "www.dianping.com"],
        "invoice_type": "ecommerce",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-btn"]',
        ],
        "notes": "大众点评发票"
    },

    # --------------------------------------------------------------------------
    # 科技云服务类 (tech)
    # --------------------------------------------------------------------------
    {
        "name": "腾讯电子发票",
        "domain": ["qq.com", "www.qq.com", "cloud.tencent.com"],
        "invoice_type": "tech",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载发票")',
            '[class*="invoice-download"]',
            '[id*="downloadInvoice"]',
        ],
        "notes": "腾讯云/腾讯服务发票"
    },
    {
        "name": "阿里云发票",
        "domain": ["aliyun.com", "www.aliyun.com", "bill.aliyun.com"],
        "invoice_type": "tech",
        "strategy": "browser_multi",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("开具发票")',
            '[class*="invoice-btn"]',
            '[id*="invoice"]',
        ],
        "notes": "阿里云发票，需多步操作"
    },
    {
        "name": "华为云发票",
        "domain": ["huawei.com", "www.huawei.com", "console.huaweicloud.com"],
        "invoice_type": "tech",
        "strategy": "browser_multi",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
            '[id*="invoice"]',
        ],
        "notes": "华为云发票"
    },
    {
        "name": "京东云发票",
        "domain": ["jdcloud.com", "www.jdcloud.com", "invoice.jdcloud.com"],
        "invoice_type": "tech",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "京东云发票"
    },

    # --------------------------------------------------------------------------
    # 运营商类 (operator)
    # --------------------------------------------------------------------------
    {
        "name": "移动电子发票",
        "domain": ["10086.cn", "www.10086.cn", "shop.10086.cn"],
        "invoice_type": "operator",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
            'button:has-text("开具发票")',
        ],
        "notes": "中国移动发票"
    },
    {
        "name": "联通电子发票",
        "domain": ["10010.com", "www.10010.com", "iservice.10010.com"],
        "invoice_type": "operator",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载发票")',
            '[class*="invoice-btn"]',
        ],
        "notes": "中国联通发票"
    },
    {
        "name": "电信电子发票",
        "domain": ["189.cn", "www.189.cn", "ah.189.cn"],
        "invoice_type": "operator",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
        ],
        "notes": "中国电信发票"
    },

    # --------------------------------------------------------------------------
    # 银行类 (bank)
    # --------------------------------------------------------------------------
    {
        "name": "招商银行发票",
        "domain": ["cmbchina.com", "www.cmbchina.com", "i.cmbchina.com"],
        "invoice_type": "bank",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-download"]',
            '[id*="download"]',
        ],
        "notes": "招商银行发票"
    },
    {
        "name": "平安银行发票",
        "domain": ["pingan.com", "www.pingan.com", "bank.pingan.com"],
        "invoice_type": "bank",
        "strategy": "browser_simple",
        "selectors": [
            'a:has-text("电子发票")',
            'button:has-text("下载")',
            '[class*="invoice-btn"]',
        ],
        "notes": "平安银行发票"
    },

    # --------------------------------------------------------------------------
    # 其他平台 (misc)
    # --------------------------------------------------------------------------
    {
        "name": "诺诺发票",
        "domain": ["nnfp.jss.com.cn", "www.nuonuo.com", "fp.nuonuo.com"],
        "invoice_type": "nuonuo",
        "strategy": "browser_tax",
        "selectors": [
            'button:has-text("下载发票")',
            'a:has-text("下载发票")',
            'button:has-text("PDF下载")',
            '[data-action="download"]',
        ],
        "notes": "诺诺网发票平台"
    },
    {
        "name": "中海油",
        "domain": ["cnooc.com.cn", "www.cnooc.com.cn", "zzslg.cnooc.com.cn"],
        "invoice_type": "cnooc",
        "strategy": "browser_multi",
        "selectors": [
            'button:has-text("批量zip下载")',
            'a:has-text("批量zip下载")',
            'button:has-text("批量下载")',
            'a:has-text("电子发票下载")',
        ],
        "notes": "中海油批量发票下载"
    },
]


# ============================================================================
# 辅助函数
# ============================================================================

def get_platform_selector(platform_name: str) -> List[Dict]:
    """根据平台名称查找选择器"""
    name_lower = platform_name.lower()
    for platform in PLATFORM_SELECTORS:
        if name_lower in platform["name"].lower():
            return platform
    return None


def get_all_domains() -> List[str]:
    """获取所有平台域名"""
    domains = []
    for platform in PLATFORM_SELECTORS:
        domains.extend(platform["domain"])
    return list(set(domains))


def get_platforms_by_invoice_type(invoice_type: str) -> List[Dict]:
    """根据发票类型获取平台列表"""
    return [p for p in PLATFORM_SELECTORS if p["invoice_type"] == invoice_type]


if __name__ == "__main__":
    print(f"共收录 {len(PLATFORM_SELECTORS)} 个平台选择器")
    print("\n平台列表:")
    for p in PLATFORM_SELECTORS:
        print(f"  - {p['name']} ({p['invoice_type']})")
