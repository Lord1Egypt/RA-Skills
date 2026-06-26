# LLM Prompts

## 1. 机会判定 Prompt（优化版）

```
## 任务
判断以下候选话题是否值得写内参。

## 核心原则
**宁可多写，不可漏写**：即使不确定的话题，也建议写。
领导更关心"为什么写这个"而不是"为什么没写"。

## 候选话题
{topics}

## 判定标准（宽松版）
请从以下维度评估每个话题（1-10分）：

1. **影响力** (1-10分): 是否影响大量用户/开发者？
2. **新颖性** (1-10分): 是否是新发布/新突破？
3. **争议性** (1-10分): 是否有不同观点碰撞？
4. **战略价值** (1-10分): 是否与 AI 竞争格局相关？

## 筛选规则（保持原值）
- **总分 ≥ 25 分** → 值得写
- **或者 任一单项 ≥ 8 分** → 值得写
- **或者 有明确的产品发布/融资/安全事件** → 直接写

## 额外检查
请额外标记以下类型（直接建议写）：
- 🔥 产品发布（GPT、Claude、Sora 等）
- 💰 融资事件（> $100M）
- ⚠️ 安全/伦理事件
- 📜 政策动向（监管、出口管制）
- 🏢 公司重大变化（裁员、高管变动）

## 输出格式
```json
[
  {
    "topic": "话题名",
    "scores": {"影响力": X, "新颖性": X, "争议性": X, "战略价值": X},
    "total": XX,
    "reason": "理由",
    "should_write": true/false,
    "priority": "high/medium/low"
  }
]
```
```

## 2. 内参生成 Prompt

```
## 任务
根据以下素材，生成一份专业内参。

## 话题
{topic}

## 背景信息
{background}

## 相关推文（按热度排序）
{tweets}

## 各方观点
- 支持方: {supporters}
- 质疑方: {critics}
- 中立: {neutrals}

## 内参模板

# AI 内参：{事件标题}

**日期**: {date}
**来源**: Twitter AI 圈动态
**可信度**: ⭐⭐⭐⭐⭐

---

## 核心要点

- 要点1
- 要点2
- 要点3

本报告聚焦{事件}，分析其影响并提出应对建议。

---

## 一、事件背景

### （一）基本信息
- **发布时间**：
- **涉及主体**：
- **触发因素**：

### （二）发展脉络
- 关键时间线

---

## 二、影响分析

### （一）对行业的影响

### （二）对开发者的影响

### （三）对普通用户的影响

---

## 三、各方观点

### 支持方
| 观点 | 来源 |
|------|------|
| ... | [@username](推文链接) |

### 质疑方
| 观点 | 来源 |
|------|------|
| ... | [@username](推文链接) |

**重要：每个观点后面必须包含原始推文链接，格式：[@username](https://x.com/username/status/xxxx)**

---

## 四、趋势展望

- 短期（1-3个月）
- 中期（3-12个月）
- 长期（1年以上）

---

## 五、对策建议

### （一）短期应对（1-3个月）

### （二）中长期布局（3-12个月）

---

## 相关链接

1. [标题](URL)

---

## 🏷️ 标签

#AI #大模型 #具体标签
```

## 3. 关键词过滤配置（优化版）

```python
# AI 相关关键词（扩充）
AI_KEYWORDS = [
    # 模型/产品
    "GPT", "Claude", "Gemini", "Sora", "Codex", "ChatGPT",
    "Llama", "Mistral", "Grok", "Perplexity", "Copilot", "Cursor",
    "Windsurf", "Cline", "Trae", "Devin", "Manus",
    # 技术
    "Agent", "MCP", "Computer Use", "ComputerUse", "RAG", "Fine-tuning",
    "Prompt", "Embedding", "Vector", "LLM", "API",
    "Tool Use", "Function Calling", "Memory", "Context",
    # 模型名
    "o1", "o3", "o4", "GPT-5", "GPT-4", "Claude 4", "Claude 3.5",
    "Gemini 2", "Gemini 1.5", "Llama 4", "DeepSeek",
    # 公司
    "OpenAI", "Anthropic", "Google", "Meta", "xAI", "Mistral", "Cohere",
    "Microsoft", "Amazon", "Apple", "Nvidia", "Tesla",
    # 话题
    "AGI", "ASI", "Safety", "Security", "Alignment", "Regulation",
    "Benchmark", "Training", "Inference", "Model Merge",
    "Reasoning", "Multimodal", "Long Context", "1M Tokens"
]

# 内参话题关键词（扩充，更敏感）
REPORT_TRIGGER_KEYWORDS = [
    # 发布/产品
    "launch", "release", "announce", "debut", "unveil", "ship",
    "new model", "new feature", "beta", "available now",
    # 融资
    "funding", "Series", "round", "acquisition", "acqui",
    "valuation", "invest", "$100M", "$1B",
    # 安全/事件
    "safety", "security", "vulnerability", "breach", "hack",
    "leak", "ban", "block", "restrict",
    # 政策
    "policy", "regulation", "government", "export control",
    "trump", "biden", "congress", "eu ai act",
    # 公司动态
    "layoff", "hire", "resign", "join", "leave",
    "partnership", "collaborate", "deal",
    # 争议
    "controversy", "backlash", "criticize", "debate", "debate"
]

# 热门人物（用于兜底：如果这些 人发帖，即使热度低也要关注）
VIP_USERS = [
    "sama", "elonmusk", "DarioAmodei", "AndrewYNg", "ylecun",
    "JeffDean", "pmarca", "cdixon", "polynoamial"
]
```

## 4. 评分配置（优化）

```python
# 降低热度阈值
MIN_HOTNESS = 300  # 原来 500

# VIP 用户热度加成
VIP_HOTNESS_BONUS = 500

# 报告数量上限
MAX_REPORTS = 5  # 原来 3
```

## 5. 兜底机制

```python
def should_always_include(tweet, vip_users):
    """兜底机制：这些情况必须包含"""
    text = tweet.get("text", "").lower()
    username = tweet.get("username", "").lower()

    # 1. VIP 用户发的
    if username in [u.lower() for u in vip_users]:
        return True

    # 2. 包含明确的发布关键词
    for kw in ["launching", "releasing", "announcing", "new", "breaking"]:
        if kw in text:
            return True

    # 3. 互动量极高（即使不满足关键词）
    if tweet.get("likes", 0) > 5000 or tweet.get("retweets", 0) > 500:
        return True

    return False
```
