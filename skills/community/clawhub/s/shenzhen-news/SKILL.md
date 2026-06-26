---
name: shenzhen-news

description: A skill for retrieving Shenzhen local news and information, helping users quickly access various news updates from Shenzhen.
---

## Why This Skill Matters

As the core city of the Guangdong-Hong Kong-Macao Greater Bay Area and the first demonstration zone of socialism with Chinese characteristics, Shenzhen has frequent policy updates, vibrant business activity, and active tech innovation. This skill helps:

- **Media professionals** - Quickly get Shenzhen local news leads
- **Business people** - Track Shenzhen business dynamics and opportunities
- **Tech professionals** - Follow Shenzhen tech innovation and industrial policies
- **General citizens** - Learn about Shenzhen local life and practical information

## Features

- Search Shenzhen regional news across various topics
- Get Shenzhen local hot topics
- Track Shenzhen policy developments and planning
- Collect Shenzhen tech/business/finance information
- Follow Shenzhen transportation, real estate, education, and other livelihood information

## Usage

### 1. Basic Search

Use the `web_search` tool to search for Shenzhen-related news:

```
Shenzhen + topic
```

### 2. Category-Specific Search

Shenzhen news covers multiple fields. Here are common search combinations:

**Technology & Innovation**
- `深圳 科技` - Tech industry news
- `深圳 AI` - Artificial intelligence industry
- `深圳 半导体` - Chip industry dynamics
- `深圳 互联网` - Internet company news
- `深圳 创业` - Entrepreneurship & innovation news
- `深圳 高交会` - China Hi-Tech Fair related

**Policy & Planning**
- `深圳 政策` - Government policy updates
- `深圳 规划` - Urban planning and industrial development plans
- `深圳 前海` - Qianhai Shenzhen-Hong Kong Modern Service Industry Cooperation Zone
- `深圳 河套` - Shenzhen-Hong Kong Technology Innovation Cooperation Zone
- `深圳 先行示范区` - Demonstration Zone of Socialism with Chinese Characteristics

**Business & Finance**
- `深圳 商业` - Business & finance news
- `深圳 企业` - Corporate dynamics
- `深圳 上市公司` - Listed company news
- `深圳 金融` - Financial industry dynamics

**Livelihood & Lifestyle**
- `深圳 交通` - Transportation & infrastructure (subway, high-speed rail, roads)
- `深圳 房产` - Real estate market and policies
- `深圳 教育` - Education policies and school news
- `深圳 医疗` - Healthcare news
- `深圳 人才` - Talent recruitment and hukou policies

**Events & Exhibitions**
- `深圳 展会` - Exhibitions and events
- `深圳 论坛` - Industry forums and conferences
- `深圳 活动` - Cultural and art events

### 3. Timeliness Search

Get the latest news:

- `深圳 今日新闻` or `深圳 今天` - Today's news
- `深圳 本周热点` - Weekly highlights
- `深圳 最新政策` - Latest policies
- `深圳 昨日` - Yesterday's news

### 4. In-Depth Search

For deep coverage on specific topics:

- `深圳 新能源汽车` - Shenzhen new energy vehicle industry
- `深圳 低空经济` - Low-altitude economy and eVTOL
- `深圳 跨境电商` - Cross-border trade
- `深圳 专精特新` - "Specialized, Refined, Exclusive, and New" enterprises

## Recommended News Sources

Add these source keywords to your searches for more reliable information:

- `深圳新闻网` - Shenzhen official news website
- `深圳卫视` - Shenzhen Broadcasting & TV Station
- `读特新闻` - Shenzhen news

## Output Format

When returning news summaries, include these fields:

1. **Title** - News headline
2. **Source** - Publishing media (with link)
3. **Time** - Publication date
4. **Summary** - Key content (100-200 words)
5. **Link** - Original article link

**Example:**

> **Qianhai Releases New Batch of Financial Innovation Policies**
> - Source: [Shenzhen Special Zone Daily](https://www.sznews.com/)  
> - Time: January 15, 2024  
> - Summary: The Qianhai Shenzhen-Hong Kong Modern Service Industry Cooperation Zone today released "Several Measures for Promoting High-Quality Financial Development," introducing 20 financial innovation policies...  
> - Link: https://example.com/news

## Practical Tips

### Combined Searches

Combine multiple keywords for more precise results:

```
Shenzhen + [Industry] + [Specific Topic]
```

Example: `深圳 + 半导体 ` (Shenzhen + semiconductor)

### Time Filtering

Use the `freshness` parameter when searching:
- `day` - Within 24 hours
- `week` - This week
- `month` - This month

### Search Strategies

1. **Policy news** - Prioritize official media (Shenzhen Special Zone Daily, Shenzhen Government Online)
2. **Corporate news** - Combine with company names
3. **Livelihood news** - Use local service accounts like "Shenzhen Local Guide"
4. **Tech news** - Follow official channels like "Shenzhen Science & Technology Innovation Commission"

## Scheduled Push Configuration

To schedule regular Shenzhen news updates, configure in HEARTBEAT.md:

```markdown
## Regular Tasks
- Search "深圳 今日新闻" and summarize every day at 9:00
- Search "深圳 本周热点" every Monday
- Follow policy releases: search "深圳 最新政策" weekly
```

## Notes

1. Shenzhen news updates frequently - verify important information from multiple sources
2. For policy-related information, check government official websites for confirmation
3. Some business information may have timeliness issues - verify before taking action