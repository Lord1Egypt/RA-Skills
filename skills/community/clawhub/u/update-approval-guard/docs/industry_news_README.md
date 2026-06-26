# 产业资讯日报自动化系统

## 概述

本系统根据配置的产业名称和关键词，每天自动采集、处理、存储并推送相关资讯日报。

## 目录结构

```
/root/.openclaw/workspace/
├── config/
│   └── industry_news_config.json    # 主配置文件
├── scripts/
│   ├── industry_daily_news.mjs      # 主执行脚本
│   └── industry_daily_news.sh       # Cron 入口脚本
├── logs/
│   └── industry_news/               # 执行日志目录
│       ├── run_YYYY-MM-DD.log       # 详细执行日志
│       └── cron_YYYY-MM-DD.log      # Cron 执行日志
└── docs/
    └── industry_news_README.md      # 本文档
```

## 快速开始

### 1. 配置产业和关键词

编辑 `config/industry_news_config.json`:

```json
{
  "industries": [
    {
      "id": "ocean_economy",
      "name": "海洋经济",
      "enabled": true,
      "keywords": {
        "primary": ["海洋经济", "海上风电"],
        "secondary": ["港口航运", "海洋工程"],
        "international": ["ocean economy", "offshore wind"]
      }
    }
  ]
}
```

### 2. 创建飞书多维表格

系统已自动创建多维表格：
- **App Token**: `JFWebb76KaFd7as501ac3UIDnxb`
- **访问链接**: https://ucn19uuu5wk8.feishu.cn/base/JFWebb76KaFd7as501ac3UIDnxb

**需要手动创建日报汇总表**：
1. 打开上述链接
2. 点击 "+" 创建新数据表
3. 命名为"日报汇总"
4. 添加以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日报日期 | 日期 | |
| 产业名称 | 文本 | |
| 采集时间范围 | 文本 | |
| 原始采集数量 | 数字 | |
| 去重后数量 | 数字 | |
| 入选数量 | 数字 | |
| 完整日报正文 | 文本 | |
| 推送状态 | 单选 | success/failed |
| 推送时间 | 日期 | |
| 异常说明 | 文本 | |

5. 获取新表的 table_id 并更新配置文件中的 `feishu.bitable.tables.dailyReport`

### 3. 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天9:00执行）
0 9 * * * /root/.openclaw/workspace/scripts/industry_daily_news.sh
```

### 4. 手动测试

```bash
# 直接运行主脚本
node /root/.openclaw/workspace/scripts/industry_daily_news.mjs

# 或运行 shell 脚本
bash /root/.openclaw/workspace/scripts/industry_daily_news.sh
```

## 配置说明

### 产业配置 (industries)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| name | string | 显示名称 |
| enabled | boolean | 是否启用 |
| keywords.primary | array | 主要关键词（高优先级） |
| keywords.secondary | array | 次要关键词 |
| keywords.international | array | 国际/英文关键词 |
| sources.whitelist | array | 优先来源域名 |
| sources.blacklist | array | 排除来源关键词 |
| categories | array | 主题分类列表 |

### 搜索配置 (search)

| 字段 | 说明 | 默认值 |
|------|------|--------|
| providers.primary | 主搜索引擎 | tavily |
| providers.fallback | 备用搜索引擎 | brave |
| settings.daysRange | 搜索时间范围（天） | 1 |
| settings.maxResultsPerQuery | 每次搜索最大结果数 | 20 |

### 去重配置 (deduplication)

| 字段 | 说明 | 默认值 |
|------|------|--------|
| url.enabled | URL 去重 | true |
| url.normalize | URL 标准化 | true |
| title.enabled | 标题去重 | true |
| title.similarityThreshold | 标题相似度阈值 | 0.85 |
| content.enabled | 正文去重 | true |
| content.similarityThreshold | 正文相似度阈值 | 0.75 |

### 扩展配置 (expansion)

当有效资讯不足时自动扩展：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| enabled | 是否启用 | true |
| minRequiredArticles | 最低要求条数 | 20 |
| maxIterations | 最大迭代次数 | 3 |

## 飞书权限

需要以下飞书应用权限：

```
- bitable:app:read
- bitable:app
- bitable:record:read
- bitable:record
- im:chat
- im:message
```

## 执行日志

每次执行生成两类日志：

1. **run_YYYY-MM-DD.log** - 详细执行日志
   - 每个步骤的详细信息
   - 错误堆栈
   - 性能指标

2. **cron_YYYY-MM-DD.log** - Cron 执行日志
   - 开始/结束时间
   - 退出码

### 日志示例

```
[2026-03-10T01:00:00.000Z] [INFO] === 产业资讯日报启动 ===
[2026-03-10T01:00:01.000Z] [INFO] Processing industry: 海洋经济
[2026-03-10T01:00:05.000Z] [INFO] Search iteration 1, keywords: 13
[2026-03-10T01:00:30.000Z] [INFO] After dedup: 45 articles (removed 15)
[2026-03-10T01:01:00.000Z] [SUCCESS] Pushed card message successfully
[2026-03-10T01:01:01.000Z] [INFO] === 执行报告 ===
```

## 多维表格字段

### 资讯明细表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日报日期 | 日期 | |
| 产业名称 | 文本 | |
| 标题 | 文本 | |
| 原文链接 | 超链接 | |
| 信源站点 | 文本 | |
| 发布时间 | 日期 | |
| 抓取时间 | 日期 | |
| 正文原文 | 文本 | |
| 中文摘要 | 文本 | |
| 标签 | 多选 | |
| 主题分类 | 单选 | |
| 相关性评分 | 数字 | 0-1 |
| 重要性评分 | 数字 | 0-1 |
| 是否入选日报 | 复选框 | |
| 抓取状态 | 单选 | 成功/失败/超时 |
| 失败原因 | 文本 | |

### 日报汇总表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日报日期 | 日期 | |
| 产业名称 | 文本 | |
| 采集时间范围 | 文本 | |
| 原始采集数量 | 数字 | |
| 去重后数量 | 数字 | |
| 入选数量 | 数字 | |
| 完整日报正文 | 文本 | Markdown 格式 |
| 推送状态 | 单选 | success/failed |
| 推送时间 | 日期 | |
| 异常说明 | 文本 | |

## 故障排查

### 常见问题

1. **搜索无结果**
   - 检查 Tavily API Key 是否配置
   - 检查网络连接
   - 尝试简化关键词

2. **飞书写入失败**
   - 检查 app_token 和 table_id 是否正确
   - 检查飞书应用权限
   - 检查字段名称是否匹配

3. **推送失败**
   - 检查 target user ID 是否正确
   - 检查消息卡片格式
   - 系统会自动回退到文本消息

### 查看日志

```bash
# 查看今日执行日志
cat /root/.openclaw/workspace/logs/industry_news/run_$(date +%Y-%m-%d).log

# 实时监控
tail -f /root/.openclaw/workspace/logs/industry_news/run_$(date +%Y-%m-%d).log
```

## 扩展开发

### 添加新产业

在 `config/industry_news_config.json` 的 `industries` 数组中添加：

```json
{
  "id": "ai_tech",
  "name": "人工智能",
  "enabled": true,
  "keywords": {
    "primary": ["人工智能", "AI", "大模型"],
    "secondary": ["机器学习", "深度学习"],
    "international": ["artificial intelligence", "LLM", "GPT"]
  },
  "categories": ["技术突破", "产业应用", "政策法规", "投融资"]
}
```

### 自定义评分规则

修改 `ContentProcessor` 类中的 `calculateRelevance` 和 `calculateImportance` 方法。

### 添加新的搜索引擎

在 `SearchCollector` 类中添加新的搜索方法。

## 维护说明

1. **定期清理日志**
   ```bash
   # 删除30天前的日志
   find /root/.openclaw/workspace/logs/industry_news -name "*.log" -mtime +30 -delete
   ```

2. **监控执行状态**
   ```bash
   # 检查今日是否执行成功
   grep "SUCCESS" /root/.openclaw/workspace/logs/industry_news/cron_$(date +%Y-%m-%d).log
   ```

3. **更新关键词**
   - 根据实际采集效果调整关键词
   - 添加新的优质来源到白名单

---

**创建时间**: 2026-03-10
**版本**: 1.0.0
**作者**: OpenClaw Agent
