#!/usr/bin/env python3
"""实战 75 意图→搜索策略 (2026-06-17)
- entity 类型 → 搜索语法 (强制精确匹配 + site: 限制)
- 解决犀牛截图问题: '北京暮辰恒信咨询有限公司' 拆成'查找'问题
- 思路: 识别 entity 是公司/产品/人/学术, 选对应权威源 site:
"""
import re
from typing import Dict, List, Optional, Tuple


# 公司/工商 查询权威源
COMPANY_SITES = [
    'qcc.com',       # 企查查
    'tianyancha.com',  # 天眼查
    'aicqgs.com',    # 爱企查
    'baike.baidu.com',  # 百度百科
    'qixin.com',     # 启信宝
    'aiqicha.com',
]

# 人物/社交查询权威源
PERSON_SITES = [
    'weibo.com',     # 微博
    'linkedin.com',  # LinkedIn
    'zhihu.com',     # 知乎
    'baike.baidu.com',  # 百度百科
    'github.com',    # GitHub
    'twitter.com',
    'xiaohongshu.com',  # 小红书
    'bilibili.com',
]

# 产品/品牌查询权威源
PRODUCT_SITES = [
    'baike.baidu.com',  # 百度百科
    'zhihu.com',     # 知乎评测
    'zol.com.cn',    # 中关村在线
    'smzdm.com',     # 什么值得买
    'gamersky.com',  # 游民星空
    'jd.com',        # 京东
    'tmall.com',     # 天猫
    'taobao.com',
    'amazon.cn',
]

# 学术/技术查询权威源
ACADEMIC_SITES = [
    'arxiv.org',     # arXiv
    'scholar.google.com',  # Google Scholar
    'github.com',    # GitHub
    'csdn.net',      # CSDN
    'cnblogs.com',   # 博客园
    'juejin.cn',     # 掘金
    'zhuanlan.zhihu.com',  # 知乎专栏
    'stackoverflow.com',
    'wikipedia.org',
]

# 新闻/资讯查询权威源
NEWS_SITES = [
    'thepaper.cn',   # 澎湃
    'yicai.com',     # 第一财经
    'caixin.com',    # 财新
    'cls.cn',        # 财联社
    'sina.com.cn',   # 新浪
    '163.com',       # 网易
    'qq.com',        # 腾讯
    'sohu.com',      # 搜狐
    'ifeng.com',     # 凤凰
    'gmw.cn',        # 光明网
    'people.com.cn', # 人民网
    'xinhuanet.com',
]

# 视频/娱乐
VIDEO_SITES = [
    'bilibili.com',
    'douyin.com',
    'youtube.com',
    'youtube.com.cn',
    'iqiyi.com',
    'v.qq.com',
    'youku.com',
]

# 购物/比价
SHOPPING_SITES = [
    'jd.com',
    'tmall.com',
    'taobao.com',
    'pinduoduo.com',
    'amazon.cn',
    'smzdm.com',  # 什么值得买
    'guiderank-app.com',  # 盖得排行
]


def detect_entity_type(entity: str, category: str = '', intent: str = '', query: str = '') -> str:
    """实战 75+78: 识别 entity 类型
    返回: 'company' / 'person' / 'product' / 'academic' / 'news' / 'video' / 'shopping' / 'general'

    实战 78 新增:
    - 看 query 不只 entity (模式识别)
    - 看 brain_info.intent (intent 优先)
    - 极长 query → general
    - 自述/复合句 → general
    - 评测/价格 → shopping
    - 泛化词(流程/师/指数) → general
    """
    if not entity:
        return 'general'

    e = entity.strip()
    q = (query or '').strip()
    q_lower = q.lower()

    # 实战 91: 极短 query (1-2 字) - KB hit 走 general (避免 "AI" 推 company)
    # 仅对纯中文生效 (跳过含英文/数字 entity)
    if 1 <= len(e) <= 2 and re.search(r'[\u4e00-\u9fff]', e) and not re.search(r'[a-zA-Z0-9]', e):
        return 'general'

    # 实战 78.6: 自述/复合句 (含"我是/我想/请问/推荐") → general
    if re.search(r'(我是|我想|请问|推荐|告诉我|给我|搜索|查询|百度一下)', q):
        return 'general'

    # 实战 78.2: query 模式硬编码 (高优先级: "X 是什么" 直接判定)
    # "X 是什么" / "什么是 X" / "X 简介" / "X 介绍"
    if re.search(r'(是什么|什么是|简介|介绍|是哪个|哪个国家)', q):
        # 学术类优先 (LLM/AI/ML/算法/理论)
        academic_set = {'llm', 'gpt', 'rag', 'transformer', 'ai', 'ml', 'agi', 'aigc', 'sd', 'cnn', 'rnn', 'lstm', 'diffusion', 'dl',
                        '机器学习', '深度学习', '神经网络', '强化学习', '数据挖掘', '自然语言处理', '图像识别', '计算机视觉'}
        if e.lower() in academic_set or e in academic_set or re.search(r'(模型|算法|框架|理论|概念|原理|技术|架构)', e):
            return 'academic'
        # 实战 88: 中文 entity 4+ 字 + 不在 KB → 学术 (默认)
        if re.search(r'[\u4e00-\u9fff]{4,}', e) and e not in BUILTIN_KB_HINT:
            return 'academic'
        if re.search(r'(公司|企业|集团)', e) or e in BUILTIN_KB_HINT:
            return 'company'
        if re.search(r'(产品|app|系统|工具|服务)', e):
            return 'product'
        return 'general'

    # 实战 86: 学术/教程/方法 类 query → academic
    # 触发条件: 含"教程/怎么/如何/入门/学习/教学/指南/方法/技巧/备考/申请/步骤/流程"
    if re.search(r'(教程|入门|学习|教学|指南|方法|技巧|备考|申请|步骤|复习|练题|做法|做法|怎么用|怎么学|怎么选|怎么治|怎么写|怎么做|怎么配|怎么调|怎么用|如何用|如何学|如何选|如何治|如何写|如何做|如何配|如何调|搜索.*教程)', q):
        return 'academic'

    # 实战 89: 视频/电影/动漫类 query → video
    if re.search(r'(视频|动漫|电视剧|综艺|电影|连续剧|剧集|番剧|动画|连载|追剧|网剧|短剧|解说|影评|影院|首映|上映|票房)', q):
        return 'video'
    if re.search(r'(直播|演唱会|晚会|演出|赛事|比赛|解说回放|录像)', q):
        return 'video'

    # 实战 78.1: intent 优先 (LLM 已推 intent)
    if intent == 'news':
        return 'news'
    if intent == 'transaction':
        return 'shopping'
    if intent == 'navigation':
        # 导航找官网: 4-8 字 entity (公司名) 走 company
        # 否则 (短 entity 2-3 字) 走 product
        if len(e) >= 3 and re.search(r'[\u4e00-\u9fff]{2,}', e):
            return 'company'
        return 'product'
    if intent == 'info':
        # 实战 88: info 模式 - 优先走 KB hint (公司/产品 entity)
        # 先看 entity (剥后缀"公司/集团/股份/有限公司") 在 BUILTIN_KB_HINT
        e_clean = re.sub(r'(公司|集团|股份|有限公司|有限|大学|医院|学校)$', '', e).strip() if e else e
        if e_clean and e_clean in BUILTIN_KB_HINT:
            return 'company'
        # 英文 entity 命中 KB
        if e_clean and e_clean.lower() in {x.lower() for x in BUILTIN_KB_HINT}:
            return 'company'
        # 实战 89: info + 强学术关键词 → academic (放在 KB 之前, 避免 entity 在 KB 被截)
        if re.search(r'(原理|区别|差异|教程|入门|学习|教学|指南|方法|技巧|备考|申请|步骤|流程|算法|模型|架构|框架|协议|标准)', q) and \
           not re.search(r'(公司|集团|创始人|总裁|CEO|股价|商城|多少钱|价格|上市|融资|收购|投资)', q):
            return 'academic'
        # 1) 人物识别 (后缀关键词 → person)
        if re.search(r'(简历|生平|简介|采访|言论|故事|经历|背景|家庭|婚姻)', q) or \
           re.search(r'(先生|女士|教授|博士|医生|律师|老师|经理|董事长|总裁|创始人|CEO|CTO)', e_clean or ''):
            return 'person'
        # 实战 91: entity 在 BUILTIN_KB_EXTRA2 type=person → person
        try:
            import intent_strategy as _is
            for k, v in getattr(_is, 'BUILTIN_KB_EXTRA2', {}).items():
                if k == e or k == e_clean:
                    if v.get('type') == 'person':
                        return 'person'
        except Exception:
            pass
        # 实战 91: "X 在哪 / X 联系方式 / X 创始人" → person
        if e_clean and re.search(r'(在哪|哪里|联系方式|电话|邮箱|地址|创始人|领导|CEO|总裁)', q):
            if 2 <= len(e_clean) <= 5 and re.search(r'[\u4e00-\u9fff]', e_clean):
                return 'person'
        # 2) KB hint (公司/产品/语言) → 对应类 (大小写不敏感)
        e_lower = e.lower()
        hint_lower = {x.lower() for x in BUILTIN_KB_HINT}
        if e_lower in hint_lower:
            import entity_card as _ec
            card = _ec.get_entity_card(e)
            if card:
                if card.get('type') == 'language':
                    return 'academic'
                if card.get('type') == 'product':
                    return 'product'
                return 'company'
        # 3) 中文 2-8 字 + 不是"怎么/如何" 模式 → product/company
        if 2 <= len(e) <= 8 and re.search(r'[\u4e00-\u9fff]{2,}', e):
            if category in ('tech', 'shopping', 'social'):
                return 'product'
            if category == 'finance':
                return 'company'
        # 实战 78.4: 极短 query (1-2 字) 且 KB 没命中 → general
        if len(e) <= 2 and not re.search(r'[a-zA-Z]', e):
            return 'general'
        return 'general'
    if intent == 'comparison':
        # 对比: 第一个 entity 是什么就什么
        # entity 可能是 "X, Y" 格式, 取第一个
        first_e = e.split(',')[0].strip() if ',' in e else e
        if first_e and re.search(r'(有限公司|集团|公司|股份)', first_e):
            return 'company'
        # 实战 89: 第一 entity 在 KB hint → company
        if first_e in BUILTIN_KB_HINT or (first_e and first_e.lower() in {x.lower() for x in BUILTIN_KB_HINT}):
            return 'company'
        # 中文 2-4 字 entity (产品名 / 品牌) → product
        if first_e and re.search(r'[\u4e00-\u9fff]{2,4}', first_e) and not re.search(r'哪个好|哪家|哪家强|哪个强', e):
            return 'product'
        return 'general'  # 默认 general (对比类)
            import entity_card as _ec
            card = _ec.get_entity_card(first_e)
    if intent == 'comparison':
        # 对比: 第一个 entity 是什么就什么
        # entity 可能是 "X, Y" 格式, 取第一个
        first_e = e.split(',')[0].strip() if ',' in e else e
        if first_e and re.search(r'(有限公司|集团|公司|股份)', first_e):
            return 'company'
        # 实战 89: 第一 entity 在 KB hint → company
        if first_e in BUILTIN_KB_HINT or (first_e and first_e.lower() in {x.lower() for x in BUILTIN_KB_HINT}):
            return 'company'
        # 中文 2-4 字 entity (产品名 / 品牌) → product
        if first_e and re.search(r'[\u4e00-\u9fff]{2,4}', first_e) and not re.search(r'哪个好|哪家|哪家强|哪个强', e):
            return 'product'
        return 'general'  # 默认 general (对比类)

    # 实战 78.2: query 模式硬编码
    # "X 官网" / "X 网址" → company/product
    if re.search(r'(官网|网址|官网是什么|官方)', q) and re.search(r'(官网|网址|官方)', e):
        # 去掉 "官网" 看看 entity
        clean_e = re.sub(r'(官网|网址|官方)$', '', e).strip()
        if clean_e:
            return detect_entity_type(clean_e, category, intent, '')
    # "X 是什么" / "什么是 X" / "X 简介" / "X 介绍" → company/product/academic
    if re.search(r'(是什么|什么是|简介|介绍|是哪个|哪个国家)', q):
        if re.search(r'(公司|企业|集团)', e) or e in BUILTIN_KB_HINT:
            return 'company'
        if re.search(r'(模型|算法|框架|理论|概念|原理|技术|架构)', e) or e.lower() in ('llm', 'gpt', 'rag', 'transformer', 'ai', 'ml'):
            return 'academic'
        if re.search(r'(产品|app|系统|工具|服务)', e):
            return 'product'
        # 通用百科 → general
        return 'general'
    # "X vs Y" / "X 和 Y 哪个好" → comparison
    if re.search(r'(vs|VS|对比|区别|哪个好|哪家强|哪个强)', q):
        if re.search(r'(有限公司|集团|公司)', e):
            return 'company'
        return 'product'  # 默认 product
    # "X 进展" / "X 动态" / "X 新闻" → news
    if re.search(r'(进展|动态|新闻|资讯|最新消息)', q):
        return 'news'
    # "X 评测" / "X 体验" / "X 怎么样" → shopping
    if re.search(r'(评测|体验|怎么样|咋样|好吗|好不好)', q):
        if re.search(r'(有限公司|集团|公司)', e) or category == 'tech':
            return 'shopping'  # 评测
        return 'general'
    # "X 怎么 治/做/学" → academic
    if re.search(r'(怎么|如何|教程|学习|入门|教学|指南|怎么用|怎么做)', q):
        return 'academic'
    # "X 多少钱" / "X 价格" → shopping
    if re.search(r'(多少钱|价格|价位|报价|优惠|折扣|购买|下单|比价)', q):
        return 'shopping'

    # === 实战 75 原规则 (按优先级) ===

    # 1) 公司识别
    if re.search(r'(有限公司|有限责任公司|股份有限公司|集团|股份|科技公司|科技集团|贸易|实业|控股|投资|管理|咨询|事务所)', e):
        return 'company'
    if category == 'finance' and not re.search(r'[a-zA-Z]', e):
        return 'company' if len(e) <= 8 else 'general'

    # 2) 人物识别 (实战 78.3 收紧: 2-4 字中文 + 后缀才 person)
    if re.search(r'(简历|生平|简介|采访|言论|故事|经历|背景|感情|婚姻|家庭|孩子|父亲|母亲)', e) or \
       re.search(r'(简历|生平|采访|言论|故事|经历|背景|家庭|婚姻)', q):
        return 'person'
    if re.search(r'(先生|女士|教授|博士|医生|律师|老师|经理|董事长|总裁|创始人|CEO|CTO)', e):
        return 'person'
    # 实战 78.3: 必须含后缀才 person (2-4 字 + 简历/生平/故事 等)
    if category in ('tech', 'social', 'general') and 2 <= len(e) <= 4 and \
       not re.search(r'[a-zA-Z]{2,}|\d', e) and \
       re.search(r'(简历|生平|采访|言论|故事|经历|背景|家庭|婚姻|感情|在哪|哪里)', q):
        return 'person'

    # 3) 产品识别
    if re.search(r'[A-Z][a-z]+\s*\d+|\d+[A-Z][a-z]*', e) and category == 'tech':
        return 'product'
    if re.search(r'\b(Pro|Plus|Max|Ultra|Air|Mini|SE)\b', e, re.IGNORECASE) and category == 'tech':
        return 'product'

    # 4) 学术识别
    if category == 'education':
        return 'academic'
    if re.search(r'(算法|论文|教程|源码|原理|实现|框架|库|API|SDK|架构)', e):
        return 'academic'

    # 5) 新闻/资讯识别
    if intent == 'news' or re.search(r'(新闻|资讯|动态|今日|最新|消息)', e):
        return 'news'

    # 6) 视频/娱乐
    if re.search(r'(剧|电影|综艺|动漫|番剧|视频|短片|解说)', e):
        return 'video'

    # 7) 购物识别
    if category == 'shopping':
        return 'shopping'
    if re.search(r'(价格|多少钱|优惠|折扣|购买|怎么买|哪里买|比价|推荐)', e):
        return 'shopping'

    # 8) 泛化词 → general (实战 78.11)
    if re.search(r'(流程|师|指数|查询|服务|方法|方式|途径|渠道|路径|建议|方案)', e):
        return 'general'
    if re.search(r'(流程|师|指数|查询|服务|方法|方式|途径|渠道|路径|建议|方案)', q):
        return 'general'

    return 'general'


# 实战 85: 同步 BUILTIN_KB_HINT (加 EXTRA2 90 个公司/产品/概念)
# 动态合并 EXTRA + EXTRA2
def _build_kb_hint():
    base = {
        # 公司
        '苹果', '微软', '谷歌', '亚马逊', 'Meta', '英伟达', '特斯拉', '比亚迪', '华为', '小米',
        'OpenAI', 'openai', 'Anthropic', 'anthropic', 'DeepSeek', 'deepseek', '智谱',
        '百度', '阿里', '腾讯', '字节', '京东', '美团', '拼多多', '宁德时代', '雪球', '同花顺',
        '东方财富', '韭研公社', '小红书', '微博', '知乎', 'B站', '哔哩哔哩', '抖音', '快手',
        'Google', 'Apple', 'Microsoft', 'Tesla', 'Nvidia', 'Meta', 'Amazon', 'AMD', 'Intel',
        '阿里巴巴', '字节跳动', '理想', '蔚来', '小鹏', '联想', '中兴', '大疆', '滴滴',
        'Spotify', 'Netflix', 'Uber', 'Airbnb', 'Salesforce', 'Oracle', 'SAP', 'Cisco', 'IBM',
        'VMware', '完美世界', '米哈游', 'Anthropic', 'Mistral',
        '保时捷', '宝马', '奔驰', '奥迪', '茅台', '五粮液', '星巴克', '可口可乐', '百事可乐', '迪士尼',
        # 产品
        '微信', 'wechat', 'WhatsApp', 'GPT', 'gpt', 'ChatGPT', 'chatgpt', 'Claude', 'claude',
        'Gemini', 'gemini', 'Kimi', 'kimi', '豆包', '文心一言', '通义', 'Cursor', 'cursor',
        'Copilot', 'copilot', 'Midjourney', 'midjourney', 'TikTok', 'tiktok', 'LinkedIn',
        'linkedin', 'YouTube', 'youtube', 'Reddit', 'reddit', 'X', 'twitter', 'Twitter',
        'GitHub', 'github', 'Python', 'python', 'Rust', 'rust', 'VSCode', 'vscode',
        'Sora', 'Llama', 'Perplexity', 'Notion', 'Figma', 'Slack', '钉钉', '飞书', 'Zoom',
        '黑神话悟空', '原神', '王者荣耀', 'LOL', '英雄联盟', '我的世界', 'Minecraft',
        '宝可梦', '塞尔达传说', '漫威', 'DC', '哈利波特', '三体', '喜茶', '蜜雪冰城',
        # 概念/技术
        'LLM', 'llm', 'lmm', 'AI', 'ai', 'AI大模型', 'ML', 'ml', 'RAG', 'rag', 'GPT', 'gpt',
        'Transformer', 'transformer', 'AGI', 'agi', 'AIGC', 'aigc', 'Stable Diffusion', 'sd',
        'CNN', 'RNN', 'LSTM', 'Diffusion', 'diffusion', 'Deep Learning', 'deep learning', 'DL', 'dl',
        '5G', '5g', '4G', '4g', 'WiFi', 'wifi', 'Bluetooth', '蓝牙', 'IoT', 'iot', '区块链', 'bitcoin',
        'Bitcoin', '以太坊', 'Ethereum', 'NFT', 'nft', 'Web3', 'web3', '元宇宙', 'metaverse',
        '量子计算', 'quantum', 'GPU', 'TPU', 'CPU', 'NPU', '云计算', '大数据', '深度学习', '物联网',
        '咖啡', '茶', '苹果', '香蕉', '故宫', '长城', '上海迪士尼', '环球影城',
    }
    # 实战 85: 动态加 EXTRA2 的人/品牌
    try:
        import intent_strategy as _is
        for key in getattr(_is, 'BUILTIN_KB_EXTRA2', {}).keys():
            base.add(key)
        for key in getattr(_is, 'BUILTIN_KB_EXTRA', {}).keys():
            base.add(key)
    except Exception:
        pass
    return base


BUILTIN_KB_HINT = _build_kb_hint()


# 实战 85: 100+ 新 entity 加入 KB (常见公司/产品/技术/人物/电影/游戏/食物/地点/汽车/医药)
BUILTIN_KB_EXTRA2 = {
    # === 人物 (15) ===
    '乔布斯': {
        'name': '史蒂夫·乔布斯 (Steve Jobs)',
        'type': 'person',
        'category': 'tech',
        'description': '苹果公司联合创始人, iPhone/iPad/Mac 缔造者, 1976 创立苹果, 2011 去世',
        'official_url': 'https://www.apple.com/leadership/',
        'tags': ['苹果', '创始人', '科技', '传奇'],
        'logo': '🍎',
    },
    '比尔盖茨': {
        'name': '比尔·盖茨 (Bill Gates)',
        'type': 'person',
        'category': 'tech',
        'description': '微软公司联合创始人, 全球慈善家, 比尔与梅琳达·盖茨基金会',
        'official_url': 'https://www.gatesfoundation.org/',
        'tags': ['微软', '创始人', '慈善'],
        'logo': '💻',
    },
    '雷军': {
        'name': '雷军 (Lei Jun)',
        'type': 'person',
        'category': 'tech',
        'description': '小米科技创始人/CEO/董事长, 金山软件董事长, Are You OK',
        'official_url': 'https://www.mi.com/about',
        'tags': ['小米', '创始人', 'CEO'],
        'logo': '🌾',
    },
    '任正非': {
        'name': '任正非 (Ren Zhengfei)',
        'type': 'person',
        'category': 'tech',
        'description': '华为公司创始人/总裁, 1944 生, 1987 创立华为',
        'official_url': 'https://www.huawei.com/cn/about-huawei/management',
        'tags': ['华为', '创始人'],
        'logo': '📡',
    },
    '马云': {
        'name': '马云 (Jack Ma)',
        'type': 'person',
        'category': 'tech',
        'description': '阿里巴巴集团创始人, 1964 生, 1999 创立阿里, 2019 卸任董事长',
        'official_url': 'https://www.alibabagroup.com/about-alibaba/management',
        'tags': ['阿里', '创始人', '电商'],
        'logo': '🛒',
    },
    '马化腾': {
        'name': '马化腾 (Pony Ma)',
        'type': 'person',
        'category': 'tech',
        'description': '腾讯公司创始人/董事会主席, 1971 生, 1998 创立腾讯',
        'official_url': 'https://www.tencent.com/about',
        'tags': ['腾讯', '创始人'],
        'logo': '🐧',
    },
    '李彦宏': {
        'name': '李彦宏 (Robin Li)',
        'type': 'person',
        'category': 'tech',
        'description': '百度公司创始人/董事长/CEO, 1968 生, 2000 创立百度',
        'official_url': 'https://ir.baidu.com/management',
        'tags': ['百度', '创始人'],
        'logo': '🔍',
    },
    '刘强东': {
        'name': '刘强东 (Richard Liu)',
        'type': 'person',
        'category': 'tech',
        'description': '京东集团创始人/董事局主席/CEO, 1973 生, 1998 创立京东',
        'official_url': 'https://ir.jd.com/management',
        'tags': ['京东', '创始人'],
        'logo': '🛍️',
    },
    '张一鸣': {
        'name': '张一鸣 (Zhang Yiming)',
        'type': 'person',
        'category': 'tech',
        'description': '字节跳动创始人, 1983 生, 2012 创立字节跳动, 2021 卸任 CEO',
        'official_url': 'https://www.bytedance.com/about',
        'tags': ['字节', '创始人', '抖音'],
        'logo': '⚡',
    },
    '黄仁勋': {
        'name': '黄仁勋 (Jensen Huang)',
        'type': 'person',
        'category': 'tech',
        'description': '英伟达 (NVIDIA) 创始人/CEO, 1963 生, 1993 创立 NVIDIA, AI 教父',
        'official_url': 'https://www.nvidia.com/en-us/about-nvidia/leadership/',
        'tags': ['英伟达', 'CEO', 'AI'],
        'logo': '🟢',
    },
    '巴菲特': {
        'name': '沃伦·巴菲特 (Warren Buffett)',
        'type': 'person',
        'category': 'finance',
        'description': '伯克希尔·哈撒韦 CEO, 1930 生, 股神, 全球顶级投资人',
        'official_url': 'https://www.berkshirehathaway.com/',
        'tags': ['投资', '股神', '伯克希尔'],
        'logo': '💰',
    },
    '查理芒格': {
        'name': '查理·芒格 (Charlie Munger)',
        'type': 'person',
        'category': 'finance',
        'description': '伯克希尔·哈撒韦副主席, 巴菲特合伙人, 2023 去世, 99 岁',
        'official_url': 'https://www.berkshirehathaway.com/',
        'tags': ['投资', '巴菲特', '伯克希尔'],
        'logo': '📈',
    },
    '陆奇': {
        'name': '陆奇 (Qi Lu)',
        'type': 'person',
        'category': 'tech',
        'description': '百度前总裁/COO, 微软前执行副总裁, YC 中国前 CEO, 奇绩创坛创始人',
        'official_url': 'https://www.miracleplus.com/',
        'tags': ['百度', '微软', 'YC', '奇绩创坛'],
        'logo': '🎯',
    },
    '李开复': {
        'name': '李开复 (Kai-Fu Lee)',
        'type': 'person',
        'category': 'tech',
        'description': '创新工场创始人/董事长, 谷歌大中华区前总裁, 微软/苹果前高管, AI 专家',
        'official_url': 'https://www.sinovationventures.com/',
        'tags': ['创新工场', '谷歌', 'AI'],
        'logo': '🧠',
    },
    '山姆·奥特曼': {
        'name': '山姆·奥特曼 (Sam Altman)',
        'type': 'person',
        'category': 'tech',
        'description': 'OpenAI CEO, Y Combinator 前总裁, 1985 生',
        'official_url': 'https://openai.com/about',
        'tags': ['OpenAI', 'CEO', 'YC'],
        'logo': '🤖',
    },
    # === 互联网/科技公司 (15) ===
    'Spotify': {
        'name': 'Spotify',
        'type': 'product',
        'category': 'tech',
        'description': '全球最大音乐流媒体平台, 瑞典, 2006 创立, 月活 5 亿+',
        'official_url': 'https://www.spotify.com/',
        'tags': ['音乐', '流媒体', '瑞典'],
        'logo': '🎵',
    },
    'Netflix': {
        'name': 'Netflix',
        'type': 'company',
        'category': 'tech',
        'description': '全球最大流媒体平台, 美国, 1997 创立, 自制剧《纸牌屋》《鱿鱼游戏》',
        'official_url': 'https://www.netflix.com/',
        'stock_code': 'NFLX',
        'tags': ['流媒体', '自制剧', '电影'],
        'logo': '🎬',
    },
    'Uber': {
        'name': 'Uber',
        'type': 'company',
        'category': 'tech',
        'description': '美国网约车公司, 2009 创立, 全球 700+ 城市',
        'official_url': 'https://www.uber.com/',
        'stock_code': 'UBER',
        'tags': ['网约车', '出行', '外卖'],
        'logo': '🚗',
    },
    'Airbnb': {
        'name': 'Airbnb 爱彼迎',
        'type': 'company',
        'category': 'tech',
        'description': '全球民宿短租平台, 2008 创立, 400 万房源',
        'official_url': 'https://www.airbnb.com/',
        'stock_code': 'ABNB',
        'tags': ['民宿', '短租', '旅行'],
        'logo': '🏠',
    },
    'Salesforce': {
        'name': 'Salesforce',
        'type': 'company',
        'category': 'tech',
        'description': '全球最大 CRM 云服务公司, 1999 创立, 创始人 贝尼奥夫',
        'official_url': 'https://www.salesforce.com/',
        'stock_code': 'CRM',
        'tags': ['CRM', '云计算', 'SaaS'],
        'logo': '☁️',
    },
    'Oracle': {
        'name': 'Oracle 甲骨文',
        'type': 'company',
        'category': 'tech',
        'description': '全球最大数据库软件公司, 1977 创立, 创始人 埃里森',
        'official_url': 'https://www.oracle.com/',
        'stock_code': 'ORCL',
        'tags': ['数据库', '企业软件'],
        'logo': '🔶',
    },
    'SAP': {
        'name': 'SAP',
        'type': 'company',
        'category': 'tech',
        'description': '德国最大软件公司, ERP 龙头, 1972 创立',
        'official_url': 'https://www.sap.com/',
        'stock_code': 'SAP',
        'tags': ['ERP', '企业软件', '德国'],
        'logo': '🔷',
    },
    'Cisco': {
        'name': 'Cisco 思科',
        'type': 'company',
        'category': 'tech',
        'description': '全球网络设备龙头, 1984 创立, 路由器/交换机',
        'official_url': 'https://www.cisco.com/',
        'stock_code': 'CSCO',
        'tags': ['网络', '路由', '企业'],
        'logo': '🌐',
    },
    'IBM': {
        'name': 'IBM',
        'type': 'company',
        'category': 'tech',
        'description': '美国百年科技公司, 1911 创立, AI/Watson 大型机',
        'official_url': 'https://www.ibm.com/',
        'stock_code': 'IBM',
        'tags': ['AI', '大型机', '咨询'],
        'logo': '🖥️',
    },
    'VMware': {
        'name': 'VMware',
        'type': 'company',
        'category': 'tech',
        'description': '虚拟化龙头, 1998 创立, 2023 被博通收购',
        'official_url': 'https://www.vmware.com/',
        'tags': ['虚拟化', '云', '企业'],
        'logo': '🖧',
    },
    '联想': {
        'name': '联想集团',
        'type': 'company',
        'category': 'tech',
        'description': '全球最大 PC 厂商, 1984 创立, ThinkPad 品牌',
        'official_url': 'https://www.lenovo.com/',
        'stock_code': '992.HK',
        'tags': ['PC', '笔记本', '服务器'],
        'logo': '💻',
    },
    '中兴': {
        'name': '中兴通讯 (ZTE)',
        'type': 'company',
        'category': 'tech',
        'description': '中国通信设备龙头, 1985 创立, 5G 主力',
        'official_url': 'https://www.zte.com.cn/',
        'stock_code': '000063',
        'tags': ['5G', '通信', '手机'],
        'logo': '📡',
    },
    '大疆': {
        'name': 'DJI 大疆',
        'type': 'company',
        'category': 'tech',
        'description': '全球消费无人机龙头, 2006 创立, 70% 全球份额',
        'official_url': 'https://www.dji.com/',
        'tags': ['无人机', '航拍', '深圳'],
        'logo': '🚁',
    },
    '滴滴': {
        'name': '滴滴出行',
        'type': 'company',
        'category': 'tech',
        'description': '中国最大网约车平台, 2012 创立, 国内日单 3000 万+',
        'official_url': 'https://www.didiglobal.com/',
        'tags': ['网约车', '出行'],
        'logo': '🚖',
    },
    '快手': {
        'name': '快手 (Kuaishou)',
        'type': 'company',
        'category': 'tech',
        'description': '中国短视频平台, 2011 创立, 2021 上市',
        'official_url': 'https://www.kuaishou.com/',
        'stock_code': '1024.HK',
        'tags': ['短视频', '直播', '电商'],
        'logo': '⚡',
    },
    'B站': {
        'name': 'B站 (哔哩哔哩)',
        'type': 'company',
        'category': 'tech',
        'description': '中国年轻人视频社区, 2009 创立, 弹幕文化起源',
        'official_url': 'https://www.bilibili.com/',
        'stock_code': '9626.HK',
        'tags': ['视频', '弹幕', '二次元'],
        'logo': '📺',
    },
    '完美世界': {
        'name': '完美世界',
        'type': 'company',
        'category': 'tech',
        'description': '中国游戏龙头, 2004 创立, 《诛仙》《完美新世界》',
        'official_url': 'https://www.perfectworld.com/',
        'stock_code': '002624',
        'tags': ['游戏', '影视'],
        'logo': '🎮',
    },
    '米哈游': {
        'name': '米哈游 (miHoYo)',
        'type': 'company',
        'category': 'tech',
        'description': '中国游戏公司, 2012 创立, 《原神》《崩坏3》《星穹铁道》',
        'official_url': 'https://www.mihoyo.com/',
        'tags': ['游戏', '原神', '二次元'],
        'logo': '🌟',
    },
    # === AI 产品/技术 (10) ===
    'Sora': {
        'name': 'Sora (OpenAI)',
        'type': 'product',
        'category': 'tech',
        'description': 'OpenAI 视频生成 AI, 2024 发布, 60 秒视频',
        'official_url': 'https://openai.com/sora',
        'tags': ['AI', '视频', 'OpenAI'],
        'logo': '🎥',
    },
    'Gemini': {
        'name': 'Gemini (Google)',
        'type': 'product',
        'category': 'tech',
        'description': 'Google 多模态大模型, 1.0/1.5/2.0/2.5 多版本',
        'official_url': 'https://gemini.google.com/',
        'tags': ['AI', 'Google', '多模态'],
        'logo': '♊',
    },
    'Llama': {
        'name': 'Llama (Meta)',
        'type': 'product',
        'category': 'tech',
        'description': 'Meta 开源大模型系列, Llama 1/2/3/3.1/3.2/3.3',
        'official_url': 'https://llama.meta.com/',
        'tags': ['AI', '开源', 'Meta'],
        'logo': '🦙',
    },
    'Mistral': {
        'name': 'Mistral AI',
        'type': 'company',
        'category': 'tech',
        'description': '法国 AI 公司, 开源大模型 Mixtral/Mistral 7B/8x7B',
        'official_url': 'https://mistral.ai/',
        'tags': ['AI', '开源', '法国'],
        'logo': '🇫🇷',
    },
    'Anthropic': {
        'name': 'Anthropic',
        'type': 'company',
        'category': 'tech',
        'description': '美国 AI 安全公司, Claude 大模型, 2021 创立, 由 OpenAI 前员工成立',
        'official_url': 'https://www.anthropic.com/',
        'tags': ['AI', 'Claude', '安全'],
        'logo': '🛡️',
    },
    'Perplexity': {
        'name': 'Perplexity AI',
        'type': 'product',
        'category': 'tech',
        'description': 'AI 搜索公司, "答案引擎", Pro 模式, 2022 创立',
        'official_url': 'https://www.perplexity.ai/',
        'tags': ['AI', '搜索', '答案引擎'],
        'logo': '🔮',
    },
    'Notion': {
        'name': 'Notion',
        'type': 'product',
        'category': 'tech',
        'description': '全球知名笔记+协作工具, 2016 创立, AI 加持',
        'official_url': 'https://www.notion.so/',
        'tags': ['笔记', '协作', 'AI'],
        'logo': '📝',
    },
    'Figma': {
        'name': 'Figma',
        'type': 'product',
        'category': 'tech',
        'description': '协作设计工具, 2016 创立, Adobe 收购失败',
        'official_url': 'https://www.figma.com/',
        'tags': ['设计', '协作', 'UI'],
        'logo': '🎨',
    },
    'Slack': {
        'name': 'Slack',
        'type': 'product',
        'category': 'tech',
        'description': '企业协作 IM, 2013 创立, 2020 被 Salesforce 收购',
        'official_url': 'https://slack.com/',
        'tags': ['IM', '企业', '协作'],
        'logo': '💬',
    },
    '钉钉': {
        'name': '钉钉 (DingTalk)',
        'type': 'product',
        'category': 'tech',
        'description': '阿里旗下企业协作平台, 2015 推出, 7 亿+ 用户',
        'official_url': 'https://www.dingtalk.com/',
        'tags': ['企业', '协作', '阿里'],
        'logo': '📞',
    },
    '飞书': {
        'name': '飞书 (Lark)',
        'type': 'product',
        'category': 'tech',
        'description': '字节跳动企业协作平台, 2019 推出, 全球化 Lark',
        'official_url': 'https://www.feishu.cn/',
        'tags': ['企业', '协作', '字节'],
        'logo': '🚀',
    },
    'Zoom': {
        'name': 'Zoom',
        'type': 'product',
        'category': 'tech',
        'description': '全球视频会议龙头, 2011 创立, 疫情期间爆发',
        'official_url': 'https://www.zoom.us/',
        'stock_code': 'ZM',
        'tags': ['视频', '会议', '企业'],
        'logo': '📹',
    },
    # === 概念/技术 (10) ===
    '区块链': {
        'name': '区块链 (Blockchain)',
        'type': 'concept',
        'category': 'tech',
        'description': '去中心化分布式账本, 比特币/以太坊底层, 2008 中本聪提出',
        'official_url': 'https://en.wikipedia.org/wiki/Blockchain',
        'tags': ['加密', '去中心化', 'Web3'],
        'logo': '⛓️',
    },
    '比特币': {
        'name': 'Bitcoin 比特币',
        'type': 'concept',
        'category': 'finance',
        'description': '第一个去中心化加密货币, 2009 创世, 中本聪',
        'official_url': 'https://bitcoin.org/',
        'tags': ['加密货币', '数字货币', '稀缺'],
        'logo': '₿',
    },
    '以太坊': {
        'name': 'Ethereum 以太坊',
        'type': 'concept',
        'category': 'finance',
        'description': '第二大加密货币, 智能合约平台, 2015 创立, V 神 (Vitalik)',
        'official_url': 'https://ethereum.org/',
        'tags': ['加密货币', '智能合约', 'Web3'],
        'logo': 'Ξ',
    },
    'NFT': {
        'name': 'NFT (Non-Fungible Token)',
        'type': 'concept',
        'category': 'tech',
        'description': '非同质化代币, 区块链上唯一数字资产凭证, 2021 火爆',
        'official_url': 'https://en.wikipedia.org/wiki/Non-fungible_token',
        'tags': ['加密', '数字资产', '区块链'],
        'logo': '🖼️',
    },
    'Web3': {
        'name': 'Web3',
        'type': 'concept',
        'category': 'tech',
        'description': '去中心化互联网, 区块链+加密, 2021 概念大火',
        'official_url': 'https://en.wikipedia.org/wiki/Web3',
        'tags': ['区块链', '去中心化', '加密'],
        'logo': '🌐',
    },
    '元宇宙': {
        'name': 'Metaverse 元宇宙',
        'type': 'concept',
        'category': 'tech',
        'description': 'Meta/Facebook 提出的 3D 虚拟世界, 2021 改名 Meta',
        'official_url': 'https://en.wikipedia.org/wiki/Metaverse',
        'tags': ['VR', 'AR', '3D'],
        'logo': '🌌',
    },
    '云计算': {
        'name': '云计算 (Cloud Computing)',
        'type': 'concept',
        'category': 'tech',
        'description': '通过网络提供计算/存储/网络服务, AWS/Azure/GCP 三巨头',
        'official_url': 'https://en.wikipedia.org/wiki/Cloud_computing',
        'tags': ['云', 'AWS', 'Azure'],
        'logo': '☁️',
    },
    '大数据': {
        'name': '大数据 (Big Data)',
        'type': 'concept',
        'category': 'tech',
        'description': '海量、高速、多样化的数据集合, 4V 特征',
        'official_url': 'https://en.wikipedia.org/wiki/Big_data',
        'tags': ['数据', 'Hadoop', 'Spark'],
        'logo': '📊',
    },
    '物联网': {
        'name': 'IoT 物联网',
        'type': 'concept',
        'category': 'tech',
        'description': 'Internet of Things, 万物互联, 1999 凯文·阿什顿提出',
        'official_url': 'https://en.wikipedia.org/wiki/Internet_of_things',
        'tags': ['IoT', '传感器', '5G'],
        'logo': '🌐',
    },
    '量子计算': {
        'name': '量子计算',
        'type': 'concept',
        'category': 'tech',
        'description': '利用量子比特叠加+纠缠的计算范式, Google/IBM 量子霸权',
        'official_url': 'https://en.wikipedia.org/wiki/Quantum_computing',
        'tags': ['量子', 'IBM', 'Google'],
        'logo': '⚛️',
    },
    '深度学习': {
        'name': '深度学习 (Deep Learning)',
        'type': 'concept',
        'category': 'tech',
        'description': '基于多层神经网络的机器学习, 2012 ImageNet 突破, Geoffrey Hinton',
        'official_url': 'https://en.wikipedia.org/wiki/Deep_learning',
        'tags': ['AI', '神经网络', 'AI'],
        'logo': '🧠',
    },
    # === 电影/动漫/游戏 (10) ===
    '黑神话悟空': {
        'name': '黑神话: 悟空',
        'type': 'product',
        'category': 'entertainment',
        'description': '中国 3A 游戏, 游戏科学开发, 2024.8.20 上市, Steam 同时在线 235 万',
        'official_url': 'https://www.heishenhua.com/',
        'tags': ['游戏', '3A', '西游'],
        'logo': '🐵',
    },
    '原神': {
        'name': '原神 (Genshin Impact)',
        'type': 'product',
        'category': 'entertainment',
        'description': '米哈游开放世界 RPG, 2020 上市, 全球 5 亿+ 玩家',
        'official_url': 'https://ys.mihoyo.com/',
        'tags': ['游戏', '开放世界', '二次元'],
        'logo': '🌟',
    },
    '王者荣耀': {
        'name': '王者荣耀',
        'type': 'product',
        'category': 'entertainment',
        'description': '腾讯天美 MOBA 手游, 2015 上市, 日活 1 亿+',
        'official_url': 'https://pvp.qq.com/',
        'tags': ['游戏', 'MOBA', '腾讯'],
        'logo': '👑',
    },
    'LOL': {
        'name': '英雄联盟 (League of Legends)',
        'type': 'product',
        'category': 'entertainment',
        'description': 'Riot Games MOBA 游戏, 2009 上市, 全球最火 PC 游戏',
        'official_url': 'https://www.leagueoflegends.com/',
        'tags': ['游戏', 'MOBA', 'Riot'],
        'logo': '⚔️',
    },
    '我的世界': {
        'name': 'Minecraft 我的世界',
        'type': 'product',
        'category': 'entertainment',
        'description': '沙盒游戏, Mojang 2009, Microsoft 2014 收购, 全球销量 3 亿+',
        'official_url': 'https://www.minecraft.net/',
        'tags': ['游戏', '沙盒', '微软'],
        'logo': '⛏️',
    },
    '宝可梦': {
        'name': 'Pokémon 宝可梦',
        'type': 'product',
        'category': 'entertainment',
        'description': '任天堂经典 IP, 1996 推出, 全球收入 1000 亿美元+',
        'official_url': 'https://www.pokemon.com/',
        'tags': ['游戏', '动漫', '任天堂'],
        'logo': '⚡',
    },
    '塞尔达传说': {
        'name': '塞尔达传说 (Zelda)',
        'type': 'product',
        'category': 'entertainment',
        'description': '任天堂经典 ARPG, 1986 推出, 《旷野之息》《王国之泪》神作',
        'official_url': 'https://www.zelda.com/',
        'tags': ['游戏', 'ARPG', '任天堂'],
        'logo': '🗡️',
    },
    '漫威': {
        'name': '漫威 (Marvel)',
        'type': 'product',
        'category': 'entertainment',
        'description': '美国漫画巨头, 钢铁侠/蜘蛛侠/复仇者联盟, 2009 被 Disney 收购',
        'official_url': 'https://www.marvel.com/',
        'tags': ['漫画', '电影', 'IP'],
        'logo': '🦸',
    },
    'DC': {
        'name': 'DC Comics',
        'type': 'product',
        'category': 'entertainment',
        'description': '美国漫画巨头, 蝙蝠侠/超人/神奇女侠, Warner Bros 旗下',
        'official_url': 'https://www.dc.com/',
        'tags': ['漫画', '电影', '华纳'],
        'logo': '🦇',
    },
    '哈利波特': {
        'name': 'Harry Potter 哈利波特',
        'type': 'product',
        'category': 'entertainment',
        'description': 'J.K.罗琳魔法小说, 7 部 + 8 部电影 + 霍格沃茨之遗游戏',
        'official_url': 'https://www.wizardingworld.com/',
        'tags': ['小说', '电影', '魔法'],
        'logo': '⚡',
    },
    '三体': {
        'name': '三体 (The Three-Body Problem)',
        'type': 'product',
        'category': 'entertainment',
        'description': '刘慈欣科幻小说, 雨果奖, 腾讯电视剧, Netflix 剧集',
        'official_url': 'https://3body.fandom.com/',
        'tags': ['科幻', '小说', '电视剧'],
        'logo': '🌌',
    },
    # === 食物/水果/饮料 (10) ===
    '咖啡': {
        'name': '咖啡 (Coffee)',
        'type': 'concept',
        'category': 'general',
        'description': '世界三大饮料之一, 含咖啡因, 起源埃塞俄比亚',
        'official_url': 'https://en.wikipedia.org/wiki/Coffee',
        'tags': ['饮料', '咖啡因', '提神'],
        'logo': '☕',
    },
    '茶': {
        'name': '茶 (Tea)',
        'type': 'concept',
        'category': 'general',
        'description': '世界三大饮料之一, 起源中国, 茶马古道',
        'official_url': 'https://en.wikipedia.org/wiki/Tea',
        'tags': ['饮料', '茶文化', '中国'],
        'logo': '🍵',
    },
    '可口可乐': {
        'name': 'Coca-Cola 可口可乐',
        'type': 'product',
        'category': 'general',
        'description': '全球最大软饮品牌, 1886 美国, 全球日销 19 亿杯',
        'official_url': 'https://www.coca-cola.com/',
        'stock_code': 'KO',
        'tags': ['饮料', '美国', '百年'],
        'logo': '🥤',
    },
    '百事可乐': {
        'name': 'Pepsi 百事可乐',
        'type': 'product',
        'category': 'general',
        'description': '全球第二大软饮, 1893 美国, 与可口可乐百年竞争',
        'official_url': 'https://www.pepsi.com/',
        'stock_code': 'PEP',
        'tags': ['饮料', '美国', '百年'],
        'logo': '🥤',
    },
    '茅台': {
        'name': '贵州茅台',
        'type': 'company',
        'category': 'general',
        'description': '中国高端白酒龙头, 1951 创立, 飞天茅台 1499 元',
        'official_url': 'https://www.moutaichina.com/',
        'stock_code': '600519',
        'tags': ['白酒', '中国', '高端'],
        'logo': '🍶',
    },
    '五粮液': {
        'name': '五粮液',
        'type': 'company',
        'category': 'general',
        'description': '中国白酒龙头, 1959 创立, 四川宜宾',
        'official_url': 'https://www.wuliangye.com/',
        'stock_code': '000858',
        'tags': ['白酒', '中国'],
        'logo': '🍶',
    },
    '苹果': {
        'name': '苹果 (水果)',
        'type': 'concept',
        'category': 'general',
        'description': '常见水果, 蔷薇科, 富含纤维, 一天一苹果医生远离我',
        'official_url': 'https://en.wikipedia.org/wiki/Apple',
        'tags': ['水果', '健康'],
        'logo': '🍎',
    },
    '香蕉': {
        'name': '香蕉',
        'type': 'concept',
        'category': 'general',
        'description': '常见热带水果, 富含钾, 芭蕉科',
        'official_url': 'https://en.wikipedia.org/wiki/Banana',
        'tags': ['水果', '热带'],
        'logo': '🍌',
    },
    '星巴克': {
        'name': 'Starbucks 星巴克',
        'type': 'company',
        'category': 'general',
        'description': '全球最大咖啡连锁, 1971 美国西雅图, 全球 38000+ 店',
        'official_url': 'https://www.starbucks.com/',
        'stock_code': 'SBUX',
        'tags': ['咖啡', '连锁', '美国'],
        'logo': '☕',
    },
    '喜茶': {
        'name': '喜茶 (HEYTEA)',
        'type': 'company',
        'category': 'general',
        'description': '中国新式茶饮品牌, 2012 创立于江门, 芝士茶鼻祖',
        'official_url': 'https://www.heytea.com/',
        'tags': ['茶饮', '新茶饮', '深圳'],
        'logo': '🍵',
    },
    '蜜雪冰城': {
        'name': '蜜雪冰城',
        'type': 'company',
        'category': 'general',
        'description': '中国最大平价茶饮, 1997 创立郑州, 36000+ 店',
        'official_url': 'https://www.mxbc.com/',
        'tags': ['茶饮', '下沉', '平价'],
        'logo': '🍧',
    },
    # === 地点/品牌 (10) ===
    '故宫': {
        'name': '故宫博物院',
        'type': 'concept',
        'category': 'general',
        'description': '明清两代皇宫, 1987 列入世界遗产, 中国最大古建筑群',
        'official_url': 'https://www.dpm.org.cn/',
        'tags': ['北京', '古建筑', '明清'],
        'logo': '🏯',
    },
    '长城': {
        'name': '长城 (Great Wall)',
        'type': 'concept',
        'category': 'general',
        'description': '中国古代军事防御工程, 1987 世界遗产, 总长 21196 km',
        'official_url': 'https://www.greatwall.cn/',
        'tags': ['北京', '古建筑', '世界遗产'],
        'logo': '🧱',
    },
    '迪士尼': {
        'name': 'Disney 迪士尼',
        'type': 'company',
        'category': 'entertainment',
        'description': '全球最大娱乐公司, 1923 创立, 米老鼠/漫威/星战/皮克斯',
        'official_url': 'https://www.disney.com/',
        'stock_code': 'DIS',
        'tags': ['娱乐', '动画', 'IP'],
        'logo': '🏰',
    },
    '上海迪士尼': {
        'name': '上海迪士尼乐园',
        'type': 'concept',
        'category': 'entertainment',
        'description': '中国大陆首座迪士尼乐园, 2016 开园, 上海浦东',
        'official_url': 'https://www.shanghaidisneyresort.com/',
        'tags': ['主题乐园', '上海'],
        'logo': '🏰',
    },
    '环球影城': {
        'name': 'Universal Studios 环球影城',
        'type': 'concept',
        'category': 'entertainment',
        'description': '美国环球影业主题乐园, 哈利波特/变形金刚/小黄人, 北京/大阪/新加坡有',
        'official_url': 'https://www.universalstudios.com/',
        'tags': ['主题乐园', 'IP', '电影'],
        'logo': '🎬',
    },
    '特斯拉': {
        'name': 'Tesla 特斯拉',
        'type': 'company',
        'category': 'tech',
        'description': '美国电动车龙头, Model S/3/X/Y + Cybertruck + FSD',
        'official_url': 'https://www.tesla.com/',
        'stock_code': 'TSLA',
        'tags': ['新能源', '汽车', 'FSD', '全球'],
        'logo': '⚡',
    },
    '保时捷': {
        'name': 'Porsche 保时捷',
        'type': 'company',
        'category': 'tech',
        'description': '德国豪华跑车品牌, 1931 创立, 911/Cayenne/Taycan',
        'official_url': 'https://www.porsche.com/',
        'tags': ['跑车', '德国', '豪华'],
        'logo': '🏎️',
    },
    '宝马': {
        'name': 'BMW 宝马',
        'type': 'company',
        'category': 'tech',
        'description': '德国豪华汽车, 1916 创立, 3/5/7/X 系列 + iX/i7 新能源',
        'official_url': 'https://www.bmw.com/',
        'stock_code': 'BMW.DE',
        'tags': ['汽车', '德国', '豪华'],
        'logo': '🚙',
    },
    '奔驰': {
        'name': 'Mercedes-Benz 奔驰',
        'type': 'company',
        'category': 'tech',
        'description': '德国豪华汽车, 1926 创立, "汽车的发明者"',
        'official_url': 'https://www.mercedes-benz.com/',
        'stock_code': 'MBG.DE',
        'tags': ['汽车', '德国', '豪华'],
        'logo': '⭐',
    },
    '奥迪': {
        'name': 'Audi 奥迪',
        'type': 'company',
        'category': 'tech',
        'description': '德国豪华汽车, 1909 创立, A4/A6/A8/Q5/Q7 + e-tron',
        'official_url': 'https://www.audi.com/',
        'stock_code': 'NSU.DE',
        'tags': ['汽车', '德国', '豪华'],
        'logo': '⭕',
    },
}


def build_search_query(entity: str, entity_type: str = '', original_query: str = '') -> Tuple[str, List[str]]:
    """实战 75: 根据 entity 类型构建精确搜索 query
    返回: (rewrite_query, sites_used)
    """
    if not entity:
        return original_query, []

    # 强制加引号 (避免被引擎拆词)
    quoted_entity = f'"{entity}"'

    # 选 site
    sites = []
    if entity_type == 'company':
        sites = COMPANY_SITES
    elif entity_type == 'person':
        sites = PERSON_SITES
    elif entity_type == 'product':
        sites = PRODUCT_SITES
    elif entity_type == 'academic':
        sites = ACADEMIC_SITES
    elif entity_type == 'news':
        sites = NEWS_SITES
    elif entity_type == 'video':
        sites = VIDEO_SITES
    elif entity_type == 'shopping':
        sites = SHOPPING_SITES
    else:
        # general - 用广义权威源
        sites = COMPANY_SITES + PERSON_SITES + ACADEMIC_SITES

    # 取前 3 个 site (避免 site: 太多 bing 不接受)
    top_sites = sites[:3]
    site_query = ' OR '.join([f'site:{s}' for s in top_sites])
    new_query = f'{quoted_entity} {site_query}'

    return new_query, top_sites


def strategy_for_query(query: str, brain_info: Dict = None) -> Dict:
    """实战 75+78: 主入口 - 根据 query + brain_info 给搜索策略
    返回: {
        'entity': str,
        'entity_type': 'company' / 'person' / ...,
        'rewrite_query': str (加引号 + site:),
        'sites': list,
        'reason': str (为什么这样改)
    }
    """
    entity = ''
    category = ''
    intent = ''
    if brain_info:
        entity = brain_info.get('entity', '')
        category = brain_info.get('category', '')
        intent = brain_info.get('intent', '')

    if not entity:
        # 降级: 用原 query 第一个词
        parts = query.split()
        entity = parts[0] if parts else query

    entity_type = detect_entity_type(entity, category, intent, query)
    rewrite_query, sites = build_search_query(entity, entity_type, query)

    reason = f'识别为{entity_type}类, 加引号强制精确匹配 + site: {", ".join(sites)}'

    return {
        'entity': entity,
        'entity_type': entity_type,
        'rewrite_query': rewrite_query,
        'sites': sites,
        'reason': reason,
    }


# 实战 78.13-78.17: query 改写 + 错别字纠正
QUERY_REWRITES = {
    # 拼音 → 中文
    'huwei': '华为', 'mate70': 'mate 70', 'jiage': '价格', 'zhendong': '震动',
    'taishou': '台州', 'shoufu': '首付', 'baba': '爸爸', 'mama': '妈妈',
    # 错别字
    '怎嘛样': '怎么样', '恁说': '你说', '咋样': '怎么样', '咋办': '怎么办',
    '晓得': '知道', '晓得 比亚迪 哪儿的 伐': '知道 比亚迪 哪里',
    '马思克': '马斯克', '特里拉': '特斯拉', '拜迪 比亚 蒂': '比亚迪',
    '苹果怎嘛样': '苹果怎么样',
    # 方言
    '啥玩意儿': '什么东西',
    '咋': '怎么', '啥': '什么', '恁': '你', '伐': '吗',
}


def rewrite_query(query: str) -> str:
    """实战 78.13-78.14: 拼音 + 错别字 + 方言纠正
    """
    q = query
    for old, new in QUERY_REWRITES.items():
        q = q.replace(old, new)
    return q.strip()
