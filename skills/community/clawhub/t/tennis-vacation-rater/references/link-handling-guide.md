# Link Handling Guide

## Problem

Users often share links (Xiaohongshu, Instagram, etc.) expecting the agent to extract destination information. However:
- Many platforms block automated access
- Links may be private or expired
- Content may require login

**Critical Issue**: When link access fails, the agent might hallucinate (invent) information instead of admitting it cannot access the link.

## Solution: Stop and Ask Protocol

### When User Provides a Link

```
User: "https://www.xiaohongshu.com/... 想去这里打球"
```

### Step 1: Attempt Access (Max 10 seconds)

```python
# Try WebFetch first
try:
    content = WebFetch(url)
    if content:
        extract_info(content)
        proceed_to_step_2()
except:
    pass

# Try browser automation if available
try:
    content = BrowserOpen(url)
    if content:
        extract_info(content)
        proceed_to_step_2()
except:
    pass
```

### Step 2: If Access Fails  STOP and Ask

**Do NOT proceed with guessed information.**

**Response Template**:

```markdown
 **无法访问链接**

我无法打开您提供的链接（可能是以下原因）：
- 平台限制自动访问（如小红书、Instagram）
- 链接需要登录才能查看
- 网络访问超时

**为了给您准确的评测，请直接提供以下信息**：

| 信息 | 必填 | 示例 |
|------|------|------|
| 球场/目的地名称 |  | 三亚海棠湾网球中心 |
| 您的出发城市 |  | 上海 |
| 计划出行时间 |  | 2025年5月 |
| 最看重的因素 |  | 天气、球场质量 |

**或者**：您也可以直接复制粘贴链接中的文字内容给我。
```

### Step 3: Wait for User Response

**CRITICAL**: Do not proceed until user provides:
1. Destination name (confirmed)
2. Departure city (confirmed)

**If user provides text content**:
- Extract information from pasted content
- Proceed with workflow

**If user declines to provide info**:
- Explain that accurate evaluation requires this information
- Offer to help with general questions instead

## Examples

### Example 1: Link Access Fails

```
User: "https://xhs.link/abc123 这个球场怎么样"

Agent:  无法访问链接...
       [Show stop-and-ask template]

User: "球场是三亚海棠湾网球中心，我从上海出发"

Agent: [Proceed with evaluation]
```

### Example 2: User Pastes Content

```
User: "https://xhs.link/abc123 这个球场怎么样"

Agent:  无法访问链接...
       [Show stop-and-ask template]

User: "我把内容贴给你：
       三亚海棠湾网球中心，有4片硬地场
       住喜来登可以免费打，外人200/小时
       我5月想去"

Agent: [Extract info and proceed]
```

### Example 3: User Doesn't Provide Info

```
User: "https://xhs.link/abc123 这个球场怎么样"

Agent:  无法访问链接...
       [Show stop-and-ask template]

User: "算了，不查了"

Agent: 没问题！如果您之后想查询网旅目的地，
       可以直接告诉我球场名称和出发城市，
       我随时为您评测。
```

## Why This Matters

### Hallucination Risk

Without this protocol:
```
User: "https://xhs.link/abc123"
Agent: [Cannot access, but guesses]
       "这是巴厘岛网球俱乐部，评分8.5分，
        场地费150/小时..."
        
[Actually user was asking about Sanya]
```

With this protocol:
```
User: "https://xhs.link/abc123"
Agent:  无法访问链接，请直接告诉我球场名称
User: "三亚海棠湾"
Agent: [Accurate evaluation based on real data]
```

## Hallucination Prevention Checklist

Before generating any report:

- [ ] Destination name confirmed by user (not guessed)
- [ ] If link provided  either accessed successfully OR user provided direct input
- [ ] No prices invented (use "参考价" or "待补充")
- [ ] No ratings invented (use real platform data or "待补充")
- [ ] All data sources labeled in report

## Common Platform Issues

| Platform | Access Issue | Solution |
|----------|--------------|----------|
| 小红书 (Xiaohongshu) | Requires login, anti-scraping | Ask user to paste content |
| Instagram | Rate limiting, requires login | Ask user to paste content |
| 抖音 (TikTok) | Requires app/login | Ask user to paste content |
| 微博 (Weibo) | Some posts private | Ask user to paste content |
| 普通网页 | May work | Try WebFetch first |

## Response Templates

### Template 1: Link Access Failed

```markdown
 **无法访问您提供的链接**

可能是以下原因：
 平台限制自动访问（小红书、Instagram等）
 链接需要登录才能查看
 网络访问问题

**请直接告诉我**：
1. 球场/目的地名称？
2. 您的出发城市？
3. 计划什么时候去？

或者直接把链接里的文字内容粘贴给我也可以。
```

### Template 2: Partial Information Extracted

```markdown
 **部分信息已获取**

从您提供的内容中，我了解到：
 目的地：三亚海棠湾网球中心
 [其他提取的信息]

**还需要确认**：
 您的出发城市是？
 计划出行时间？
```

### Template 3: User Declines to Provide Info

```markdown
没问题！如果您之后想了解这个目的地，
随时可以告诉我：
 球场名称
 出发城市
 出行时间

我会为您生成详细的网旅评测报告。
```
