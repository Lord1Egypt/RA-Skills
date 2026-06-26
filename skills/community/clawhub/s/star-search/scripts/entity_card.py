#!/usr/bin/env python3
"""实战 66 实体知识卡片 (2026-06-16)
- 实体知识库 (字典: entity -> {name, type, description, official_url, pinyin, ...})
- search 后: brain.entity 命中知识库 → 自动返 entity_card
- 类型: company/product/website/person/finance/tech/general
- AI 增强: super_brain 已知信息补全 (LLM 一次性生成)

设计:
- ENTITY_KB = {entity_key: {...}}
- get_entity_card(entity) -> {name, type, description, official_url, logo, ...} | None
- search 端点返: results + entity_card (如果有)
"""
import os
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlparse

LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.token-star.cn/v1')
LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
LLM_MODEL = os.environ.get('LLM_MODEL', 'DeepSeek-V4-Flash')
LLM_TIMEOUT = int(os.environ.get('LLM_TIMEOUT', '10'))

_env_path = Path('/home/ubuntu/star-search/.env')
if _env_path.exists():
    try:
        with open(_env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, _, v = line.partition('=')
                    k, v = k.strip(), v.strip()
                    if k == 'LLM_BASE_URL' and v:
                        LLM_BASE_URL = v
                    elif k == 'LLM_API_KEY' and v:
                        LLM_API_KEY = v
                    elif k == 'LLM_MODEL' and v:
                        LLM_MODEL = v
                    elif k == 'LLM_TIMEOUT' and v:
                        try:
                            LLM_TIMEOUT = int(v)
                        except: pass
    except Exception:
        pass

CACHE_FILE = Path('/home/ubuntu/star-search/entity_kb.json')
KB_LLM_CACHE = Path('/home/ubuntu/star-search/entity_kb_llm.json')


# ============ 内置知识库 (实战 66 起步) ============
BUILTIN_KB = {
    # ========== 金融/投资 (实战 76 扩展) ==========
    '韭研公社': {
        'name': '韭研公社',
        'type': 'community',
        'category': 'finance',
        'description': '新生代股票研究平台 (原韭菜公社), 实战研究赋能, 投资者交流社区',
        'official_url': 'https://www.jiuyangongshe.com/',
        'alt_urls': ['https://pc2.jiucaigongshe.com/', 'https://t.10jqka.com.cn/601319077/'],
        'founded': '2020',
        'tags': ['投资', '股票', '研究', '社区', 'AI 量化'],
        'logo': '🌱',
    },
    '雪球': {
        'name': '雪球',
        'type': 'community',
        'category': 'finance',
        'description': '中国领先的投资者交流与交易平台, 提供股票/基金讨论与实盘交易',
        'official_url': 'https://xueqiu.com/',
        'founded': '2010',
        'tags': ['股票', '基金', '投资', '社区'],
        'logo': '❄️',
    },
    '东方财富': {
        'name': '东方财富',
        'type': 'company',
        'category': 'finance',
        'description': '中国领先的网络财经信息平台, 提供股票/基金/财经资讯',
        'official_url': 'https://www.eastmoney.com/',
        'stock_code': '300059',
        'tags': ['财经', '股票', '资讯', '券商'],
        'logo': '💰',
    },
    '同花顺': {
        'name': '同花顺',
        'type': 'company',
        'category': 'finance',
        'description': '中国主流金融信息服务商, 提供股票行情/交易/资讯',
        'official_url': 'https://www.10jqka.com.cn/',
        'stock_code': '300033',
        'tags': ['股票', '行情', '交易', '金融'],
        'logo': '📊',
    },
    # 实战 76 新增 20+ 公司
    '阿里巴巴': {
        'name': '阿里巴巴',
        'type': 'company',
        'category': 'tech',
        'description': '中国最大电商/云计算公司, 旗下淘宝/天猫/支付宝/钉钉/阿里云',
        'official_url': 'https://www.alibabagroup.com/',
        'alt_urls': ['https://www.1688.com/'],
        'stock_code': 'BABA',
        'founded': '1999',
        'tags': ['电商', '云', '支付', '金融'],
        'logo': '🛒',
    },
    '腾讯': {
        'name': '腾讯',
        'type': 'company',
        'category': 'tech',
        'description': '中国最大互联网公司, 旗下微信/QQ/王者荣耀/腾讯视频',
        'official_url': 'https://www.tencent.com/',
        'alt_urls': ['https://www.qq.com/'],
        'stock_code': '00700.HK',
        'founded': '1998',
        'tags': ['社交', '游戏', '支付', '云'],
        'logo': '🐧',
    },
    '字节跳动': {
        'name': '字节跳动 (ByteDance)',
        'type': 'company',
        'category': 'tech',
        'description': '中国最大短视频/AI 公司, 旗下抖音/TikTok/今日头条/豆包',
        'official_url': 'https://www.bytedance.com/',
        'tags': ['短视频', 'AI', '抖音', '国际化'],
        'logo': '⚡',
    },
    '百度': {
        'name': '百度',
        'type': 'company',
        'category': 'tech',
        'description': '中国最大搜索引擎, 旗下百度文心一言/Apollo/百度地图',
        'official_url': 'https://www.baidu.com/',
        'stock_code': 'BIDU',
        'founded': '2000',
        'tags': ['搜索', 'AI', '地图', '文心'],
        'logo': '🔍',
    },
    '京东': {
        'name': '京东',
        'type': 'company',
        'category': 'shopping',
        'description': '中国最大自营电商, 旗下京东商城/京东物流/京东金融',
        'official_url': 'https://www.jd.com/',
        'stock_code': 'JD',
        'founded': '1998',
        'tags': ['电商', '物流', '金融'],
        'logo': '🛍️',
    },
    '美团': {
        'name': '美团',
        'type': 'company',
        'category': 'shopping',
        'description': '中国最大本地生活服务平台, 涵盖外卖/酒店/出行/电影',
        'official_url': 'https://www.meituan.com/',
        'stock_code': '03690.HK',
        'founded': '2010',
        'tags': ['外卖', '酒店', '出行', '本地生活'],
        'logo': '🍱',
    },
    '拼多多': {
        'name': '拼多多',
        'type': 'company',
        'category': 'shopping',
        'description': '中国社交电商龙头, 主打低价+拼团模式',
        'official_url': 'https://www.pinduoduo.com/',
        'stock_code': 'PDD',
        'founded': '2015',
        'tags': ['电商', '社交', '下沉市场'],
        'logo': '🧧',
    },
    '宁德时代': {
        'name': '宁德时代 (CATL)',
        'type': 'company',
        'category': 'finance',
        'description': '全球最大动力电池制造商, 特斯拉/宝马/蔚来等供应商',
        'official_url': 'https://www.catl.com/',
        'stock_code': '300750',
        'founded': '2011',
        'tags': ['电池', '新能源', '锂电'],
        'logo': '🔋',
    },
    '小米': {
        'name': '小米',
        'type': 'company',
        'category': 'tech',
        'description': '中国领先手机/IoT 公司, 旗下小米/红米/米家/澎湃 OS',
        'official_url': 'https://www.mi.com/',
        'stock_code': '01810.HK',
        'founded': '2010',
        'tags': ['手机', 'IoT', '汽车', '澎湃'],
        'logo': '🌾',
    },
    '蔚来': {
        'name': '蔚来 (NIO)',
        'type': 'company',
        'category': 'tech',
        'description': '中国高端电动车品牌, 换电模式',
        'official_url': 'https://www.nio.com/',
        'stock_code': 'NIO',
        'founded': '2014',
        'tags': ['新能源', '汽车', '换电'],
        'logo': '🚙',
    },
    '小鹏': {
        'name': '小鹏汽车 (XPeng)',
        'type': 'company',
        'category': 'tech',
        'description': '中国智能电动车品牌, 智驾系统领先',
        'official_url': 'https://www.xiaopeng.com/',
        'stock_code': 'XPEV',
        'founded': '2014',
        'tags': ['新能源', '汽车', '智驾'],
        'logo': '🚗',
    },
    '理想': {
        'name': '理想汽车 (Li Auto)',
        'type': 'company',
        'category': 'tech',
        'description': '中国增程式电动车龙头, 家用 SUV 领先',
        'official_url': 'https://www.lixiang.com/',
        'stock_code': 'LI',
        'founded': '2015',
        'tags': ['新能源', '汽车', '增程', 'SUV'],
        'logo': '🚙',
    },
    '特斯拉': {
        'name': '特斯拉 (Tesla)',
        'type': 'company',
        'category': 'tech',
        'description': '美国电动车龙头, Model S/3/X/Y + Cybertruck + FSD',
        'official_url': 'https://www.tesla.com/',
        'stock_code': 'TSLA',
        'founded': '2003',
        'tags': ['新能源', '汽车', 'FSD', '全球'],
        'logo': '⚡',
    },
    '英伟达': {
        'name': '英伟达 (NVIDIA)',
        'type': 'company',
        'category': 'tech',
        'description': '全球最大 GPU/AI 芯片公司, 旗下 GeForce/CUDA/Tesla',
        'official_url': 'https://www.nvidia.com/',
        'stock_code': 'NVDA',
        'tags': ['GPU', 'AI', 'CUDA', '数据中心'],
        'logo': '🟢',
    },
    'amd': {
        'name': 'AMD',
        'type': 'company',
        'category': 'tech',
        'description': '美国半导体公司, CPU/GPU/Ryzen/EPYC/Radeon',
        'official_url': 'https://www.amd.com/',
        'stock_code': 'AMD',
        'tags': ['CPU', 'GPU', '服务器', 'AI'],
        'logo': '🔴',
    },
    'intel': {
        'name': 'Intel',
        'type': 'company',
        'category': 'tech',
        'description': '美国最大 CPU 制造商, Core/Xeon',
        'official_url': 'https://www.intel.com/',
        'stock_code': 'INTC',
        'tags': ['CPU', '服务器', '制造'],
        'logo': '🔵',
    },
    'github copilot': {
        'name': 'GitHub Copilot',
        'type': 'product',
        'category': 'tech',
        'description': 'GitHub 推出的 AI 编程助手, 基于 OpenAI Codex',
        'official_url': 'https://github.com/features/copilot',
        'tags': ['AI', '编程', 'Copilot', 'OpenAI'],
        'logo': '🤖',
    },
    'cursor': {
        'name': 'Cursor',
        'type': 'product',
        'category': 'tech',
        'description': 'AI 优先的代码编辑器, 基于 VSCode + GPT-4',
        'official_url': 'https://cursor.com/',
        'tags': ['AI', '编辑器', 'VSCode', 'GPT-4'],
        'logo': '⌨️',
    },
    'midjourney': {
        'name': 'Midjourney',
        'type': 'product',
        'category': 'tech',
        'description': '最强 AI 绘画工具, Discord 平台',
        'official_url': 'https://www.midjourney.com/',
        'tags': ['AI', '绘画', 'AIGC', 'Discord'],
        'logo': '🎨',
    },
    'stable diffusion': {
        'name': 'Stable Diffusion',
        'type': 'product',
        'category': 'tech',
        'description': '开源 AI 绘画模型, 创始公司 Stability AI',
        'official_url': 'https://stability.ai/',
        'tags': ['AI', '绘画', '开源', 'SD'],
        'logo': '🖼️',
    },
    'hugging face': {
        'name': 'Hugging Face',
        'type': 'product',
        'category': 'tech',
        'description': '全球最大 AI 模型社区, 1M+ 模型',
        'official_url': 'https://huggingface.co/',
        'tags': ['AI', '模型', '社区', '开源'],
        'logo': '🤗',
    },
    'meta': {
        'name': 'Meta (Facebook)',
        'type': 'company',
        'category': 'tech',
        'description': '美国社交巨头, 旗下 Facebook/Instagram/WhatsApp + 开源 LLaMA',
        'official_url': 'https://www.meta.com/',
        'stock_code': 'META',
        'tags': ['社交', 'AI', 'LLaMA', 'VR'],
        'logo': '♾️',
    },
    'tiktok': {
        'name': 'TikTok',
        'type': 'product',
        'category': 'social',
        'description': '字节跳动旗下国际短视频应用, 全球 15 亿月活',
        'official_url': 'https://www.tiktok.com/',
        'tags': ['短视频', '海外', '字节'],
        'logo': '🎵',
    },
    'x': {
        'name': 'X (Twitter)',
        'type': 'product',
        'category': 'social',
        'description': '马斯克旗下社交平台, 改名 X 强调万能应用',
        'official_url': 'https://x.com/',
        'tags': ['社交', '马斯克', '全球'],
        'logo': '𝕏',
    },
    'reddit': {
        'name': 'Reddit',
        'type': 'product',
        'category': 'social',
        'description': '美国最大社区论坛, "互联网首页"',
        'official_url': 'https://www.reddit.com/',
        'tags': ['社区', '论坛', '海外'],
        'logo': '🤖',
    },
    'youtube': {
        'name': 'YouTube',
        'type': 'product',
        'category': 'social',
        'description': '全球最大视频平台, Google 旗下',
        'official_url': 'https://www.youtube.com/',
        'tags': ['视频', 'Google', '全球'],
        'logo': '📺',
    },
    'linkedin': {
        'name': 'LinkedIn',
        'type': 'product',
        'category': 'social',
        'description': '全球最大职业社交平台, 微软旗下',
        'official_url': 'https://www.linkedin.com/',
        'tags': ['职业', '社交', '招聘', '微软'],
        'logo': '💼',
    },
    'deepseek': {
        'name': 'DeepSeek',
        'type': 'company',
        'category': 'tech',
        'description': '中国 AI 大模型公司, DeepSeek-V3/R1 震惊全球',
        'official_url': 'https://www.deepseek.com/',
        'tags': ['AI', 'LLM', '开源', '中国'],
        'logo': '🐋',
    },
    '智谱': {
        'name': '智谱 AI (Zhipu)',
        'type': 'company',
        'category': 'tech',
        'description': '中国领先 AI 公司, 清华系, GLM 系列大模型',
        'official_url': 'https://www.zhipuai.cn/',
        'tags': ['AI', 'GLM', '清华', '中国'],
        'logo': '🧠',
    },
    'kimi': {
        'name': 'Kimi',
        'type': 'product',
        'category': 'tech',
        'description': '月之暗面 AI 助手, 长上下文能力强 (200K tokens)',
        'official_url': 'https://kimi.moonshot.cn/',
        'tags': ['AI', '长上下文', '月之暗面'],
        'logo': '🌙',
    },
    '豆包': {
        'name': '豆包 (Doubao)',
        'type': 'product',
        'category': 'tech',
        'description': '字节跳动旗下 AI 助手, 抖音内置',
        'official_url': 'https://www.doubao.com/',
        'tags': ['AI', '字节', '抖音'],
        'logo': '🥟',
    },
    '文心一言': {
        'name': '文心一言 (ERNIE Bot)',
        'type': 'product',
        'category': 'tech',
        'description': '百度推出的大语言模型, 4.0/3.5 多版本',
        'official_url': 'https://yiyan.baidu.com/',
        'tags': ['AI', '百度', 'LLM'],
        'logo': '🪶',
    },

    # ========== 科技/产品 (原 19 个) ==========
    '华为': {
        'name': '华为',
        'type': 'company',
        'category': 'tech',
        'description': '全球领先的信息与通信技术 (ICT) 解决方案供应商',
        'official_url': 'https://www.huawei.com/',
        'alt_urls': ['https://consumer.huawei.com/cn/'],
        'founded': '1987',
        'tags': ['5G', '手机', '通信', '芯片', '鸿蒙'],
        'logo': '📱',
    },
    '比亚迪': {
        'name': '比亚迪',
        'type': 'company',
        'category': 'tech',
        'description': '中国新能源汽车与电池龙头, 业务涵盖汽车/电池/电子',
        'official_url': 'https://www.bydglobal.com/',
        'alt_urls': ['https://www.byd.com/'],
        'stock_code': '002594',
        'founded': '1995',
        'tags': ['汽车', '新能源', '电池', '电动'],
        'logo': '🚗',
    },
    '苹果': {
        'name': '苹果',
        'type': 'company',
        'category': 'tech',
        'description': '美国科技公司, iPhone/Mac/iPad 制造商',
        'official_url': 'https://www.apple.com/',
        'stock_code': 'AAPL',
        'tags': ['手机', '电脑', 'iOS', 'macOS'],
        'logo': '🍎',
    },
    '微软': {
        'name': '微软',
        'type': 'company',
        'category': 'tech',
        'description': '美国跨国科技公司, Windows/Office/Azure 制造商',
        'official_url': 'https://www.microsoft.com/',
        'stock_code': 'MSFT',
        'tags': ['Windows', 'Office', '云', 'AI'],
        'logo': '🪟',
    },
    '谷歌': {
        'name': '谷歌',
        'type': 'company',
        'category': 'tech',
        'description': '美国跨国科技公司, 全球最大搜索引擎',
        'official_url': 'https://www.google.com/',
        'stock_code': 'GOOGL',
        'tags': ['搜索', '广告', 'AI', '云'],
        'logo': '🔍',
    },
    'openai': {
        'name': 'OpenAI',
        'type': 'company',
        'category': 'tech',
        'description': '美国 AI 研究公司, ChatGPT/GPT-4 制造商',
        'official_url': 'https://openai.com/',
        'tags': ['AI', 'LLM', 'GPT', 'ChatGPT'],
        'logo': '🤖',
    },
    'claude': {
        'name': 'Claude (Anthropic)',
        'type': 'product',
        'category': 'tech',
        'description': 'Anthropic 公司的 AI 助手, 安全/可解释/有用',
        'official_url': 'https://www.anthropic.com/',
        'tags': ['AI', 'LLM', 'Claude'],
        'logo': '🧠',
    },
    '微信': {
        'name': '微信',
        'type': 'product',
        'category': 'social',
        'description': '腾讯旗下社交应用, 月活 13 亿, 中国主流通讯工具',
        'official_url': 'https://weixin.qq.com/',
        'tags': ['社交', '通讯', '支付'],
        'logo': '💬',
    },
    '微博': {
        'name': '微博',
        'type': 'product',
        'category': 'social',
        'description': '新浪旗下社交媒体平台, 中国版 Twitter',
        'official_url': 'https://weibo.com/',
        'tags': ['社交', '媒体', '娱乐'],
        'logo': '📢',
    },
    '知乎': {
        'name': '知乎',
        'type': 'community',
        'category': 'social',
        'description': '中国主流问答社区, 专业/认真的讨论',
        'official_url': 'https://www.zhihu.com/',
        'tags': ['问答', '知识', '社区'],
        'logo': '❓',
    },
    'b站': {
        'name': 'B站 (哔哩哔哩)',
        'type': 'product',
        'category': 'social',
        'description': '中国年轻人视频社区, 弹幕 + 二次元 + 学习',
        'official_url': 'https://www.bilibili.com/',
        'stock_code': '9626.HK',
        'tags': ['视频', '弹幕', '二次元', '学习'],
        'logo': '📺',
    },
    '抖音': {
        'name': '抖音',
        'type': 'product',
        'category': 'social',
        'description': '字节跳动旗下短视频平台, 日活 7 亿+',
        'official_url': 'https://www.douyin.com/',
        'tags': ['短视频', '直播', '电商'],
        'logo': '🎬',
    },
    'python': {
        'name': 'Python',
        'type': 'language',
        'category': 'tech',
        'description': '高级通用编程语言, AI/数据科学/网站首选',
        'official_url': 'https://www.python.org/',
        'tags': ['编程', 'AI', '数据', '科学计算'],
        'logo': '🐍',
    },
    'rust': {
        'name': 'Rust',
        'type': 'language',
        'category': 'tech',
        'description': 'Mozilla 推出的系统级编程语言, 安全/并发/零成本抽象',
        'official_url': 'https://www.rust-lang.org/',
        'tags': ['编程', '系统', '安全', 'WebAssembly'],
        'logo': '🦀',
    },
    'github': {
        'name': 'GitHub',
        'type': 'product',
        'category': 'tech',
        'description': '全球最大代码托管平台, 微软旗下',
        'official_url': 'https://github.com/',
        'tags': ['代码', '开源', '协作'],
        'logo': '🐙',
    },
}


def _normalize_entity(entity: str) -> str:
    """实战 66: 实体归一化"""
    if not entity:
        return ''
    e = entity.strip().lower()
    # 去常见后缀
    for suffix in [' 是什么', ' 怎么样', ' 网址', ' 官网']:
        if e.endswith(suffix):
            e = e[:-len(suffix)].strip()
    return e


def get_entity_card(entity: str) -> Optional[Dict]:
# 实战 66: 查实体卡片
    1) 查内置 KB
    2) 查 LLM 缓存
    3) 没找到返 None

    实战 76: 模糊匹配 (entity="腾讯 微信" → 找 "微信" / "腾讯" 都行)
    实战 79: 优先查 intent_strategy.BUILTIN_KB_EXTRA (8 个新概念/人)
    """
    if not entity:
        return None
    e_norm = _normalize_entity(entity)

    # 实战 79: 优先查 intent_strategy.BUILTIN_KB_EXTRA (8 概念)
    # 实战 85: 优先查 BUILTIN_KB_EXTRA2 (90+ 公司/产品/概念/食物/地点)
    try:
        import intent_strategy as _is
        for _kb_name in ('BUILTIN_KB_EXTRA2', 'BUILTIN_KB_EXTRA'):
            _kb = getattr(_is, _kb_name, {})
            for key, info in _kb.items():
                if key.lower() == e_norm or e_norm == key.lower():
                    return dict(info)
            for word in e_norm.split():
                if not word or len(word) < 2:
                    continue
                for key, info in _kb.items():
                    if key.lower() == word or word == key.lower():
                        return dict(info)
    except Exception:
        pass

    # 1) 内置 KB (精确匹配 + 大小写不敏感)
    for key, info in BUILTIN_KB.items():
        if key.lower() == e_norm or e_norm == key.lower():
            return dict(info)  # copy

    # 实战 76: 模糊匹配 - 拆 entity 为词, 每个词试一次
    for word in e_norm.split():
        if not word or len(word) < 2:
            continue
        for key, info in BUILTIN_KB.items():
            if key.lower() == word or word == key.lower():
                return dict(info)

    # 2) LLM 缓存
    if KB_LLM_CACHE.exists():
        try:
            with open(KB_LLM_CACHE) as f:
                llm_cache = json.load(f)
            if e_norm in llm_cache:
                return llm_cache[e_norm]
        except Exception:
            pass

    # 3) LLM 实时生成 (async 调用, 这里简化)
    # 实际由 get_or_create_entity_card 异步调用
    return None


def _call_llm(prompt: str, max_tokens: int = 400) -> Optional[str]:
    if not LLM_API_KEY:
        return None
    body = json.dumps({
        'model': LLM_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.3,
    }).encode()
    req = urllib.request.Request(
        f'{LLM_BASE_URL}/chat/completions',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LLM_API_KEY}',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
            data = json.loads(resp.read())
            return data['choices'][0]['message']['content']
    except Exception:
        return None


def create_entity_card_via_llm(entity: str) -> Optional[Dict]:
    """实战 66: 用 LLM 生成实体卡片 (异步调用)"""
    e_norm = _normalize_entity(entity)
    if not e_norm:
        return None

    # 避免 LLM 调太频繁
    cache = {}
    if KB_LLM_CACHE.exists():
        try:
            with open(KB_LLM_CACHE) as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    if e_norm in cache:
        return cache[e_norm]

    prompt = f"""你是一个实体知识库助手。用户查询实体: {entity}

请生成该实体的结构化信息:
1. name: 名称
2. type: 类型 (company 公司 / product 产品 / website 网站 / community 社区 / person 人物 / language 编程语言)
3. category: 类别 (finance/tech/social/general)
4. description: 50-100 字简介
5. official_url: 官方网址
6. founded: 成立年份 (如适用)
7. tags: 5-8 个相关标签
8. logo: 一个合适的 emoji

请严格按以下 JSON 格式返回 (不要其他说明):
{{
  "name": "...",
  "type": "...",
  "category": "...",
  "description": "...",
  "official_url": "...",
  "founded": "...",
  "tags": ["...", "..."],
  "logo": "..."
}}"""

    content = _call_llm(prompt, max_tokens=400)
    if not content:
        return None

    try:
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        card = json.loads(content)

        # 缓存
        cache[e_norm] = card
        # 限 500 条
        if len(cache) > 500:
            cache = dict(list(cache.items())[-500:])
        try:
            with open(KB_LLM_CACHE, 'w') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return card
    except Exception:
        return None


def match_entity_to_card(entity: str, results: list = None) -> Optional[Dict]:
    """实战 66: 智能匹配实体
    1) 内置 KB 查
    2) results 里查官方域名
    3) LLM 生成
    """
    # 1) 内置
    card = get_entity_card(entity)
    if card:
        return card

    # 2) results 里查 official_url
    if results:
        for r in results:
            url = r.get('url', '')
            source = r.get('source', '')
            title = r.get('title', '')
            # 如果 title 含 entity, 且有 url, 拿第一个当候选
            if entity in title and url:
                # 试解析主域名
                try:
                    d = urlparse(url).netloc.lower()
                    if d.startswith('www.'):
                        d = d[4:]
                    return {
                        'name': entity,
                        'type': 'auto',
                        'category': 'general',
                        'description': f'搜索结果: {title}',
                        'official_url': url,
                        'source_domain': d,
                        'logo': '🔎',
                        'tags': [],
                        'auto_matched': True,
                    }
                except Exception:
                    pass

    # 3) LLM 生成 (会比较慢 3-5s, 可选)
    return None
