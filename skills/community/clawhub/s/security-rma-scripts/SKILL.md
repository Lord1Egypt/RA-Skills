---
name: Investment Advisory Scripts & Talk-Point Assistant
slug: security-advisory-scripts
description: AI-powered investment advisory scripts and talk-point generator for China wealth management — covers stock recommendations, fund allocation, market commentary, client objection handling, and compliance-compliant communication templates. Built for China securities brokers, wealth management advisors, and relationship managers. Keywords: investment advisory scripts, wealth management talk points, client communication, stock recommendations, fund sales scripts, compliance communication, China securities, 投顾话术, 财富管理, 客户沟通, 基金销售, 合规话术, 理财经理, 基金推荐, 资产配置, 客户维护, 异议处理, 营销话术.
version: "3.0.1"
---

# Investment Advisory Scripts & Talk-Point Assistant / 投顾话术智能助手

> **English:** AI-powered investment advisory scripts generator — covers stock/fund recommendation scripts, market commentary templates, client objection handling, and compliance-compliant communication frameworks. Solves pain points: repetitive client calls, pressure to increase AUM, and maintaining compliance in client interactions. Built for securities brokers, wealth advisors, and relationship managers.
>
> **中文:** 投顾话术智能助手——覆盖股票/基金推荐话术、市场点评模板、客户异议处理、合规沟通框架。解决痛点：重复性客户沟通、AUM增长压力、合规要求。适用：券商理财顾问、财富管理师、客户经理。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年Q1：投资者适当性管理要求进一步强化 | 投顾话术模板需更新合规和适当性要求 |
| 证券监管 | 产品分级和风险匹配要求升级，投顾话术需更新 | 投顾话术模板需更新合规和适当性要求 |
| 证券监管 | 证监会加强投资者保护，销售行为合规要求提升 | 投顾话术模板需更新合规和适当性要求 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **话术重复单调** | 客户体验差，转化率低 | AI生成个性化话术，每次沟通不重样 |
| **产品理解不深** | 无法解答客户专业问题 | 产品卖点话术库+常见问题应答 |
| **异议处理不当** | 客户流失率高 | 标准异议处理SOP+话术模板 |
| **合规风险** | 监管处罚风险高 | 合规话术检查+禁说清单 |
| **市场波动应对** | 客户恐慌导致赎回 | 危机沟通话术+心理安抚框架 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** investment advisory scripts, wealth management talk points, client communication, stock recommendations, fund sales scripts, compliance communication, client objection handling, market commentary, China securities, wealth advisor

**中文触发词（优先）：** 投顾话术 / 财富管理 / 客户沟通 / 基金销售 / 股票推荐 / 产品话术 / 异议处理 / 客户拒绝 / 合规话术 / 市场点评 / 客户维护 / 首次开发 / 二次开发 / 盘后沟通 / 追涨话术 / 止损沟通 / 客户安抚 / 产品对比 / 收益解释 / 风险提示 / KYC适配 / 适当性匹配 / 投诉处理 / 回访话术 / 投教沟通

---

## Core Capabilities / 核心能力

### 1. Product Recommendation Scripts / 产品推荐话术

#### 1.1 Stock Recommendation Framework / 股票推荐话术

```markdown
## 股票推荐话术标准框架（合规版）

### 开场白（30秒）
"张总您好，我是XX证券的小李，今天想和您分享一下我们最新研究覆盖的[行业/板块]机会，
主要基于以下几点考虑，供您参考。"

### 核心逻辑（3分钟）
"第一，行业层面：[宏观政策/行业景气度/供需格局]
第二，公司层面：[竞争优势/业绩增速/估值水平]
第三，催化剂：[政策利好/订单落地/业绩超预期可能]
第四，风险提示：[需要说明的风险因素]

综合来看，我们认为[公司]在[时间维度]内具备[预期收益]的空间，
建议关注区间[XX-XX]元。"

### 风险提示（必须）
"当然，市场有风险，投资需谨慎。股票投资受多种因素影响，
过往业绩不代表未来表现。请您根据自身风险承受能力谨慎决策。
我司对[公司]的研究报告可在官网查询。"

### 追加提问
"您对这个板块/公司有什么看法？有什么想进一步了解的？"
```

#### 1.2 Fund Recommendation Scripts / 基金推荐话术

```python
FUND_RECOMMENDATION_TEMPLATES = {
    "股票型基金": {
        "适用场景": "市场趋势向上 + 客户风险偏好较高",
        "话术模板": """
        "根据我们对市场的判断，[宏观因素]对权益资产形成支撑。
        我们建议关注[基金名称]，该基金[基金经理优势/策略特点/历史业绩]。
        
        业绩参考：近一年收益{return_1y}%，同类排名{percentile}，
        最大回撤{max_drawdown}%。
        
        配置建议：建议占您整体股票的{alloc}%，
        一次性买入{amount}元，配合定投{monthly}元/月效果更佳。"
        """,
        "异议处理": {
            "亏损怎么办": "我们建议采用定投方式分散成本，同时...（见异议处理模块）",
            "费率太高": "目前有优惠活动，申购费率打{discount}折...",
            "看不懂策略": "简单来说就是...（用生活化比喻解释）"
        }
    },
    
    "债券型基金": {
        "适用场景": "市场震荡 + 客户风险偏好较低",
        "话术模板": """
        "考虑到当前市场波动加大，我们建议适当增配固定收益资产。
        [基金名称]是专门投资于债券的基金，特点是[稳定性/收益性/流动性]。
        
        业绩参考：近一年收益{return_1y}%，年化波动率{volatility}%，
        适合作为资产组合的'压舱石'。"
        """
    },
    
    "混合型基金": {
        "适用场景": "平衡型客户 + 不确定市场方向",
        "话术模板": """
        "对于追求'进可攻退可守'的客户，我们推荐关注混合型基金。
        [基金名称]股债配比约{stock}%:{bond}%，
        既有股票市场的上涨弹性，又有债券的稳定收益。
        
        历史表现：牛市收益{bull_return}%，熊市回撤{downside}%，
        攻守兼备。"
        """
    }
}
```

### 2. Market Commentary Templates / 市场点评话术

```markdown
## 市场点评话术模板库

### 每日盘后话术（5分钟版）
```
各位投资者朋友，下午好。今日（{date}）市场点评：

【大盘表现】
今日{index_name}收于{close}点，{up/down}{change_pct}%，
{成交量变化}，整体呈现'{市场特征}'。

【板块轮动】
今日表现较强的板块：{strong_sectors}，
主要受益于{催化剂}；
表现较弱的板块：{weak_sectors}，
{原因分析}。

【资金动向】
北向资金今日{净流入/净流出}{amount}亿，
主力资金净流入{板块}居前。

【后市展望】
我们认为{短期判断}，建议关注{投资方向}。
中期来看，{中期逻辑}。

【风险提示】
市场有风险，投资需谨慎。以上仅供参考，
不构成投资建议。"
```

### 3. Client Objection Handling / 客户异议处理SOP

```python
OBJECTION_HANDLING_SOP = {
    # 收益类异议
    "收益率太低": {
        "情绪识别": "客户可能觉得产品收益不达预期",
        "应对策略": "1. 引导客户看风险调整后收益；2. 对比同类产品；3. 说明收益来源",
        "话术示例": """
        "您说得对，从绝对收益看确实不算高。
        不过您可以看一下这个产品的'风险调整后收益'——
        同样的风险投入，这个产品获得收益的效率是比较高的。
        
        而且这个收益来源是[优质资产]，相对稳健。
        比起追求高收益但可能亏损，选择这类'稳稳的幸福'也是明智的。"
        """
    },
    
    # 亏损类异议
    "亏损了怎么办": {
        "情绪识别": "客户恐慌/焦虑，需要安抚",
        "应对策略": "1. 表达理解；2. 分析亏损原因；3. 给出应对方案；4. 引导长期视角",
        "话术示例": """
        "我非常理解您的心情，账户波动确实让人不舒服。
        
        首先请您放心，这次回撤主要是因为{市场因素}，
        不是产品本身出了问题。
        
        目前我们有几种应对方案：
        方案一：保持现状，等待市场回暖（历史数据看，通常{时间}会恢复）
        方案二：定投加仓，降低平均成本
        方案三：调整仓位，配置更稳健的产品
        
        您倾向于哪种方案？我来帮您分析一下。"
        """
    },
    
    # 信任类异议
    "你们公司靠谱吗": {
        "情绪识别": "客户对平台/公司不信任",
        "应对策略": "1. 展示资质；2. 介绍实力；3. 强调合规；4. 提供证据",
        "话术示例": """
        "非常感谢您问这个问题，选对平台确实很重要。
        
        您可以放心：[公司名称]是{资质牌照}持牌机构，
        成立于{年份}年，管理资产规模{规模}亿，
        累计服务客户{数量}万户。
        
        我们受{监管机构}监管，所有产品都经过严格审核。
        您可以在[官方网站/证监会网站]查询我们的资质。
        
        此外，我可以给您介绍一些[客户见证/案例]，帮助您更了解我们。"
        """
    },
    
    # 合规应对
    "保本吗": {
        "情绪识别": "客户风险偏好与产品不匹配",
        "应对策略": "必须合规回答，明确说明产品风险，不能虚假承诺",
        "话术示例": """
        "根据监管要求，我们不能承诺'保本'。
        [产品名称]是[产品类型]，投资有风险，
        可能会发生本金损失。
        
        不过，我们可以通过以下方式控制风险：
        1. [风险控制措施1]
        2. [风险控制措施2]
        3. 分散投资，不把鸡蛋放一个篮子
        
        根据您的风险测评结果，您属于{R风险等级}投资者，
        这个产品是适合您的风险承受范围的。
        """
    }
}
```

### 4. Compliance Communication Check / 合规沟通检查

```markdown
## 合规话术禁说清单

### 绝对禁止用语
| 禁止表述 | 违规原因 | 替代话术 |
|---------|---------|---------|
| "保本保收益" | 违规承诺 | "历史业绩仅供参考，不保证未来收益" |
| "稳赚不赔" | 违规承诺 | "追求稳健增值" |
| "国家队救市" | 虚假信息 | "政策支持实体经济" |
| "内幕消息" | 违规信息 | "基于公开信息分析" |
| "推荐必涨" | 虚假宣传 | "建议关注，中长期机会" |
| "抄底" | 误导性表述 | "逢低布局" |

### 必须包含的合规表述
- "市场有风险，投资需谨慎"
- "过往业绩不代表未来表现"
- "请根据自身风险承受能力决策"
- "详情请阅产品说明书/招募说明书"
```

### 5. First-Time Client Development / 首次客户开发话术

```python
FIRST_VISIT_SCRIPTS = {
    "自我介绍": """
    "您好，请问是[客户姓名]先生/女士吗？
    我是[证券公司名称]的[理财顾问姓名]，
    今天打电话给您是想分享一下我们的财富管理服务。
    
    您方便聊几分钟吗？"
    """,
    
    "需求挖掘": """
    提问框架（SPIN法则）：
    - S（现状）："您目前投资了哪些产品？"
    - P（问题）："在投资过程中有什么让您困扰的吗？"
    - I（影响）："这给您带来了什么影响？"
    - N（需求）："如果有一个方案能解决您的问题，您有兴趣了解吗？"
    """,
    
    "产品介绍": """
    FAB法则（特征-优势-利益）：
    - F（Feature）："这是一款混合型基金，股票仓位60%，债券40%"
    - A（Advantage）："相比纯债基金，收益弹性更大；相比股票基金，回撤更小"
    - B（Benefit）："对您来说，可以在承担一定波动的情况下，追求更好的收益"
    """,
    
    "促成成交": """
    成交信号识别：
    - 语言信号："这个怎么买？""收益怎么算？"
    - 行为信号：主动询问细节、表示认同
    
    促成话术：
    "根据您的需求，我觉得这款产品很适合您。
    要不要先体验一下小额定投，感受一下？"
    """
}
```

---

## Quick Command Templates / 快速指令模板

**生成产品推荐话术：**
```
生成[基金/股票/理财]推荐话术：
- 产品名称：[名称]
- 目标客户：[客户画像]
- 客户异议：[主要异议]
- 是否需要合规检查：是
```

**生成市场点评：**
```
生成今日（[日期]）[大盘/板块/个股]点评话术：
- 市场特征：[震荡上行/单边下跌/横盘整理]
- 重点关注：[板块/个股]
- 目标受众：[客户类型]
```

**处理客户投诉：**
```
处理客户[姓名]的投诉：
- 投诉原因：[描述]
- 客户情绪：[激动/平和/失望]
- 涉及产品：[产品名称]
```

---

## Disclaimer

This skill provides communication templates and scripts for educational and reference purposes. All client communications must comply with applicable securities regulations and internal compliance policies. Investment recommendations must be based on proper suitability assessment and risk disclosure.
