# detect_entity_type 规则优先级 (实战 78, 2026-06-17)

> **核心教训**: LLM 推 intent 准 (88%), 推 entity_type 不准 (49%)。必须**LLM 推 intent + 规则强映射 entity_type**。但**规则顺序决定一切**——顺序错了 LLM 推 academic_set 里的 entity (LLM/AI) 会被"X 是什么"模式错判为 company。

`intent_strategy.detect_entity_type(entity, category, intent, query)` 的规则**优先级从上到下, 一旦命中立即 return**。后写的 17 条规则必须按这个顺序, 否则会互相冲突。

## 完整优先级 (从高到低)

```
1. 自述/复合句 (含"我是/我想/请问/推荐/告诉我/给我/搜索/查询/百度一下") → general
   ↑ 必须在所有之前, 不然"给我搜 韭研公社" 会被 info 截胡

2. query 模式硬编码 - "X 是什么/什么是/简介/介绍/是哪个/哪个国家"
   ├─ 学术类优先 (LLM/AI/ML/算法/理论) → academic
   │   ↑ 必须先 KB hint 检查, 不然 LLM 会走 company (因为 LLM 在 BUILTIN_KB_HINT 里)
   ├─ 公司类 (公司/企业/集团/in BUILTIN_KB_HINT) → company
   ├─ 产品类 (产品/app/系统/工具/服务) → product
   └─ 其他 → general

3. intent 优先 (LLM 已推 intent)
   ├─ news → news
   ├─ transaction → shopping
   ├─ navigation → company (len>=3) / product (短)
   ├─ info → [细分, 见下面]
   └─ comparison → [细分, 见下面]

4. 实战 75 原规则 (KB/关键词/characteristics)
   ├─ company: 含"有限公司/集团/股份/科技" 或 category=finance + 中文
   ├─ person: 含"简历/生平/故事/先生/女士/教授" 或 2-4字中文 + "简历"等
   ├─ product: 型号 (字母+数字) 或 Pro/Plus/Max/Ultra
   ├─ academic: 教程/算法/论文/原理 + category=education
   ├─ news: 新闻/资讯/动态
   ├─ video: 电影/综艺/番剧
   ├─ shopping: category=shopping
   └─ general: 流程/师/指数/查询/服务 等
```

## info 模式细分 (第 3 层)

```python
if intent == 'info':
    # 1) 人物识别 (后缀关键词 → person)
    if re.search(r'(简历|生平|简介|采访|故事|背景|家庭|婚姻)', q) or \
       re.search(r'(先生|女士|教授|博士|医生|律师|老师|经理|董事长|总裁|创始人|CEO|CTO)', e):
        return 'person'

    # 2) KB hint (公司/产品/语言) → 对应类 (大小写不敏感)
    e_lower = e.lower()
    hint_lower = {x.lower() for x in BUILTIN_KB_HINT}
    if e_lower in hint_lower:
        card = _ec.get_entity_card(e)
        if card:
            if card.get('type') == 'language': return 'academic'
            if card.get('type') == 'product': return 'product'
            return 'company'

    # 3) 中文 2-8 字 + 不是"怎么/如何" 模式 → product/company
    if 2 <= len(e) <= 8 and re.search(r'[\u4e00-\u9fff]{2,}', e):
        if category in ('tech', 'shopping', 'social'):
            return 'product'
        if category == 'finance':
            return 'company'

    # 4) 极短 query (1-2 字) 且 KB 没命中 → general
    if len(e) <= 2 and not re.search(r'[a-zA-Z]', e):
        return 'general'

    return 'general'
```

## comparison 模式细分 (第 3 层)

```python
if intent == 'comparison':
    # entity 可能是 "X, Y" 格式, 取第一个
    first_e = e.split(',')[0].strip() if ',' in e else e

    if first_e and re.search(r'(有限公司|集团|公司|股份)', first_e):
        return 'company'

    # KB 里有 → product/company
    first_lower = first_e.lower()
    hint_lower = {x.lower() for x in BUILTIN_KB_HINT}
    if first_lower in hint_lower:
        card = _ec.get_entity_card(first_e)
        if card:
            if card.get('type') == 'language': return 'academic'
            if card.get('type') == 'product': return 'product'
            return 'company'

    # 中文 2-4 字 entity (产品名 / 品牌) → product
    if 2 <= len(first_e) <= 8 and re.search(r'[\u4e00-\u9fff]{2,}', first_e):
        return 'product'

    return 'general'
```

## "X 是什么" 模式 (第 2 层) - 易踩坑

```python
if re.search(r'(是什么|什么是|简介|介绍|是哪个|哪个国家)', q):
    # ⚠️ 学术类优先 (LLM/AI/ML/RAG) → academic
    # 必须在 company 检查之前, 不然 LLM 被 BUILTIN_KB_HINT 命中 → company
    academic_set = {'llm', 'gpt', 'rag', 'transformer', 'ai', 'ml',
                    'agi', 'aigc', 'sd', 'cnn', 'rnn', 'lstm',
                    'diffusion', 'dl'}
    if e.lower() in academic_set or re.search(r'(模型|算法|框架|理论|概念|原理|技术|架构)', e):
        return 'academic'

    # 公司类
    if re.search(r'(公司|企业|集团)', e) or e in BUILTIN_KB_HINT:
        return 'company'

    # 产品类
    if re.search(r'(产品|app|系统|工具|服务)', e):
        return 'product'

    return 'general'
```

## BUILTIN_KB_HINT 60+ 实体 (实战 78 扩展)

```python
BUILTIN_KB_HINT = {
    # 公司
    '苹果', '微软', '谷歌', '亚马逊', 'Meta', '英伟达', '特斯拉', '比亚迪', '华为', '小米',
    'OpenAI', 'openai', 'Anthropic', 'anthropic', 'DeepSeek', 'deepseek', '智谱',
    '百度', '阿里', '腾讯', '字节', '京东', '美团', '拼多多', '宁德时代', '雪球', '同花顺',
    '东方财富', '韭研公社', '小红书', '微博', '知乎', 'B站', '哔哩哔哩', '抖音', '快手',
    'Google', 'Apple', 'Microsoft', 'Tesla', 'Nvidia', 'Meta', 'Amazon', 'AMD', 'Intel',
    '阿里巴巴', '字节跳动', '理想', '蔚来', '小鹏',
    # 产品
    '微信', 'wechat', 'WhatsApp', 'GPT', 'gpt', 'ChatGPT', 'chatgpt', 'Claude', 'claude',
    'Gemini', 'gemini', 'Kimi', 'kimi', '豆包', '文心一言', '通义', 'Cursor', 'cursor',
    'Copilot', 'copilot', 'Midjourney', 'midjourney', 'TikTok', 'tiktok', 'LinkedIn',
    'linkedin', 'YouTube', 'youtube', 'Reddit', 'reddit', 'X', 'twitter', 'Twitter',
    'GitHub', 'github', 'Python', 'python', 'Rust', 'rust', 'VSCode', 'vscode',
    # 概念/技术 (学术) - 大小写
    'LLM', 'llm', 'lmm', 'AI', 'ai', 'AI大模型', 'ML', 'ml', 'RAG', 'rag', 'GPT', 'gpt',
    'Transformer', 'transformer', 'AGI', 'agi', 'AIGC', 'aigc', 'Stable Diffusion', 'sd',
    'CNN', 'RNN', 'LSTM', 'Diffusion', 'diffusion', 'Deep Learning', 'deep learning', 'DL', 'dl',
    '5G', '5g', '4G', '4g', 'WiFi', 'wifi', 'Bluetooth', '蓝牙', 'IoT', 'iot', '区块链', 'bitcoin',
    'Bitcoin', '以太坊', 'Ethereum', 'NFT', 'nft', 'Web3', 'web3', '元宇宙', 'metaverse',
    '量子计算', 'quantum', 'GPU', 'TPU', 'CPU', 'NPU',
}
```

**关键**: **大小写不敏感** — 必须用 `e.lower() in {x.lower() for x in BUILTIN_KB_HINT}`。

## 5 大易踩坑 (实战 78 调试踩过)

### 坑 1: 极短 query 1-2 字被截胡
- "微信" 2 字 → 极短规则立刻 return general
- **修**: 极短规则移到 KB hint 检查之后
- **修前**: 微信 → general (错)
- **修后**: 微信 → product (对, KB 命中)

### 坑 2: intent=info 没看 KB hint
- "openai 是什么公司" → info 走 person 检查 → 没命中 → 直接 return general
- **修**: info 模式 1) person → 2) KB hint → 3) 中文 2-8 字 fallback
- **修前**: openai 是什么 → general (错)
- **修后**: openai 是什么 → company (对, KB 命中)

### 坑 3: "X 是什么" academic_set 没优先
- "什么是 LLM" → entity="LLM" → LLM 在 BUILTIN_KB_HINT → 走 company (错)
- **修**: 学术 set 检查必须在 company 检查之前
- **修前**: 什么是 LLM → company (错)
- **修后**: 什么是 LLM → academic (对)

### 坑 4: comparison 没拆 "X, Y"
- "比亚迪 vs 特斯拉" → entity="比亚迪, 特斯拉" (带逗号空格) → detect 失败
- **修**: `first_e = e.split(',')[0].strip() if ',' in e else e`
- **修前**: 比亚迪 vs → general
- **修后**: 比亚迪 vs → company (对, 比亚迪在 KB_HINT)

### 坑 5: navigation 4-8 字全走 product
- "华为官网" → entity="华为官网" → len 4 → navigation 规则 → product
- **修**: navigation 看 `len(e) >= 3 and 2+ 中文` → company
- **修前**: 华为官网 → product (错)
- **修后**: 华为官网 → company (对)

## 测试驱动 (实战 78 关键)

**不要直接发布 detect_entity_type 改动**! 必须先跑测试基准:

```bash
# 1. 写 10 query 关键测试
TESTS = [
    ("韭研公社 网址", "navigation", "company"),
    ("华为官网", "navigation", "company"),
    ("华为 Mate 70 价格", "transaction", "shopping"),
    ("比亚迪 vs 特斯拉", "comparison", "company"),
    ("Kimi 和 豆包 哪个好", "comparison", "product"),
    ("最新 5G 进展", "news", "news"),
    ("openai 是什么公司", "info", "company"),
    ("什么是 LLM", "info", "academic"),
    ("马斯克 简历", "info", "person"),
    ("微信", "info", "product"),
]

# 2. 跑 10 query
ssh root@server "rm -f /home/ubuntu/star-search/brain_cache.json; \
PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages \
python3 /tmp/test_q10.py"

# 3. 必须 10/10 100% 准才发版
# 8/10 → 排查剩余 2 个
# < 8/10 → 改回, 重新分析
```

**实战 78 调试 8 轮才到 10/10** (从 26/40 → 40/40)。

## 复用清单 (下次类似项目)

```python
def detect_entity_type(entity, category, intent, query):
    """检测 entity 类型 - 必须按此顺序"""
    e = entity.strip()
    q = (query or '').strip()

    # 1. 自述/复合句 (最早)
    if re.search(r'(我是|我想|请问|推荐)', q): return 'general'

    # 2. "X 是什么" 模式 (含 academic_set 优先)
    if re.search(r'(是什么|什么是|简介|介绍)', q):
        if e.lower() in ACADEMIC_SET: return 'academic'  # ⚠️ 优先
        if e in KB_HINT: return 'company'
        # ...

    # 3. intent 优先
    if intent == 'news': return 'news'
    if intent == 'transaction': return 'shopping'
    # ... 4 个 intent 细分

    # 4. 实战 75 原规则 (最后 fallback)
    # ... company/person/product/academic/news/video/shopping
```

**复用口诀**: **自述 → 模式 → intent → fallback**, 4 段顺序固定, 段内 academic 优先 company。
