---
name: trending-news-aggregator
description: |
  智能热点新闻聚合器 - 自动抓取多平台热点新闻，
  AI分析趋势，支持定时推送和热度评分。
  
  核心功能：
  - 每天自动聚合多平台热点（微博、知乎、百度等）
  - 智能分类（科技、财经、社会、国际等）
  - 热度评分算法
  - 增量检测（标记新增热点）
  - AI趋势分析
metadata:
  version: "1.0.0"
  author: "OpenClaw Community"
  category: "productivity"
  tags: ["news", "aggregator", "monitoring", "trending", "automation"]
  minOpenClawVersion: "2026.3.22"
---

# Trending News Aggregator

智能热点新闻聚合器，自动抓取多平台热点，AI分析趋势。

## 核心功能

### 综合热点聚合 (Trending News)
- **频率**: 可配置，建议每天9:00
- **内容**: 多平台热点聚合 + 智能分类 + AI趋势分析
- **输出**: 分类热点 + 热度评分 + 增量标记 + 趋势总结

### 智能分类系统
- **科技**: AI、芯片、华为、字节、腾讯等
- **财经**: 股市、经济、金融、投资等
- **社会**: 民生、教育、医疗、就业等
- **国际**: 美国、中国、欧洲、印度等
- **娱乐**: 电影、明星、综艺、音乐等

### 热度评分算法
基于以下维度加权计算：
- 平台排名权重
- 多平台出现频次
- 新闻时效性
- 用户互动数据

## 使用方法

### 手动触发

**获取今日热点**:
```
获取今日热点新闻
```

或详细指令：
```
【综合热点聚合】执行以下步骤：
1) 使用web_search搜索各平台热点新闻
2) 关键词智能分类：科技/财经/社会/国际/娱乐
3) 热度计算：按排名+频次+时效加权
4) 增量检测：标记新增热点
5) AI趋势分析：一句话总结今日热点趋势
6) 输出格式：总新闻：X条 | 新增：X条 | 时间：XX:XX
   🔥高热度分类：[1/X]分类名（X条）[热度分]
   每条新闻格式：1.[平台] 标题 [排名][🔥热度][🆕新增] 链接：https://具体新闻页面链接
```

### 定时任务配置

**方式1：使用OpenClaw Cron**
```yaml
# 每天9:00执行
schedule: "0 9 * * *"
```

**方式2：系统定时任务**
```bash
# Linux/Mac crontab
0 9 * * * openclaw run-task trending-news

# Windows Task Scheduler
# 每天 9:00 执行
```

### 推送渠道配置

支持多种推送渠道（需单独配置）：
- **微信** (weixin): 个人号/群聊推送
- **钉钉** (dingtalk): 群机器人推送
- **Slack**: 频道消息
- **Telegram**: 频道/群组
- **邮件**: SMTP发送

配置示例：
```yaml
push:
  enabled: true
  channels:
    - weixin
    # - dingtalk
    # - slack
```

## 输出格式示例

```
===今日热点=== 2026-03-25 09:00
总新闻：32条 | 新增：8条

🔥高热度分类：
[1/5] 科技（12条）[热度分：95]
  1.[微博] 华为发布新一代AI芯片 [🔥98][🆕新增]
    链接：https://weibo.com/xxx
  2.[知乎] GPT-5技术细节曝光 [🔥92]
    链接：https://zhihu.com/xxx
  3.[百度] 国产量子计算机突破 [🔥88][🆕新增]
    链接：https://baidu.com/xxx

[2/5] 财经（8条）[热度分：88]
  1.[新浪财经] A股大涨 [🔥85]
    链接：https://sina.com.cn/xxx
  ...

[3/5] 国际（6条）[热度分：76]
  ...

📈 AI趋势分析：
今日科技板块热度最高，AI和芯片成为焦点，
反映市场对技术创新的高度关注。
```

## 配置说明

### config.yaml

```yaml
# 新闻源配置
sources:
  weibo: true      # 微博热搜
  zhihu: true      # 知乎热榜
  baidu: true      # 百度热搜
  douyin: true     # 抖音热点
  toutiao: false   # 今日头条（按需启用）

# 智能分类关键词
categories:
  tech:
    name: "科技"
    keywords: ["AI", "人工智能", "芯片", "量子", "华为", "字节", "腾讯", "阿里", "百度", "小米"]
    
  finance:
    name: "财经"
    keywords: ["股市", "A股", "港股", "美股", "经济", "金融", "银行", "投资", "基金"]
    
  social:
    name: "社会"
    keywords: ["社会", "民生", "教育", "医疗", "就业", "房价", "养老", "环保"]
    
  international:
    name: "国际"
    keywords: ["美国", "中国", "日本", "韩国", "欧洲", "印度", "俄罗斯", "联合国"]
    
  entertainment:
    name: "娱乐"
    keywords: ["电影", "电视剧", "明星", "综艺", "音乐", "演唱会", "票房"]

# 热度评分配置
scoring:
  base_score: 50
  rank_weight: 10
  frequency_weight: 5
  freshness_weight: 15
  max_score: 100

# 推送设置
push:
  enabled: true
  channels:
    - weixin
  schedule: "09:00"

# 输出格式
output:
  show_category_count: true
  show_heat_score: true
  show_new_mark: true
  show_trend_analysis: true
  max_news_per_category: 5
```

## 依赖

**必需**:
- `web_search` tool (Brave Search / Tavily)
- OpenClaw >= 2026.3.22

**可选**:
- 推送渠道配置（微信/钉钉/Slack等）

## 安装

### 通过 ClawHub 安装（推荐）

```bash
clawdhub install trending-news-aggregator
```

### 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/trending-news-aggregator.git

# 2. 复制到OpenClaw skills目录
cp -r trending-news-aggregator ~/.openclaw/skills/

# 3. 重启OpenClaw或刷新skills
```

## 使用示例

### 示例1：手动获取热点

**用户**: 今天有什么热点新闻？

**Agent**: 
```
我来为您获取今日热点新闻...

===今日热点=== 2026-03-25 09:00
总新闻：28条 | 新增：6条

🔥高热度分类：
[1/4] 科技（10条）[热度分：92]
  1.[微博] 华为发布新芯片 [🔥95][🆕新增]
  2.[知乎] AI技术突破 [🔥88]
  ...

📈 趋势分析：科技板块持续火热
```

### 示例2：设置定时推送

**用户**: 每天早上9点给我推送新闻

**Agent**: 
```
已为您设置每日9:00热点推送。

配置详情：
- 任务：综合热点聚合
- 时间：每天 09:00
- 渠道：微信
- 内容：科技/财经/社会/国际热点
```

### 示例3：查看配置

**用户**: 新闻聚合器配置了哪些分类？

**Agent**: 
```
当前配置的分类：

1. 科技 - AI、芯片、华为、字节等
2. 财经 - 股市、经济、金融等
3. 社会 - 民生、教育、医疗等
4. 国际 - 美国、中国、欧洲等
5. 娱乐 - 电影、明星、综艺等

共5个分类，覆盖32个关键词。
```

## 隐私说明

本Skill：
- ✅ 不收集用户个人信息
- ✅ 不存储浏览历史
- ✅ 仅使用公开网络搜索
- ✅ 所有配置存储在用户本地

## 注意事项

1. **API限制**: web_search有调用频率限制，请合理使用
2. **新闻时效**: 新闻链接有效期有限，建议及时查看
3. **分类准确性**: AI分类可能存在偏差，仅供参考
4. **推送测试**: 首次使用建议先手动测试推送渠道

## 故障排除

### 问题1：无法获取新闻
- 检查web_search工具是否启用
- 检查网络连接
- 查看OpenClaw日志

### 问题2：推送失败
- 检查推送渠道配置
- 确认微信/钉钉等已正确配置
- 查看推送渠道日志

### 问题3：分类不准确
- 在config.yaml中调整关键词
- 添加或删除分类
- 反馈给开发者改进算法

## 更新日志

### v1.0.0 (2026-03-25)
- 初始版本发布
- 多平台热点聚合功能
- 智能分类系统
- 热度评分算法
- 增量检测功能
- AI趋势分析
- 定时推送支持

## 贡献

欢迎提交Issue和PR！

GitHub: https://github.com/yourusername/trending-news-aggregator

## License

MIT License

Copyright (c) 2026 OpenClaw Community
