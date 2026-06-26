---
name: selection-agent
description: "全渠道选品 Agent — 关键词调研、SEO分析、竞品分析、TrendPlus数据。触发词：选品、关键词调研、SEO分析、竞品分析、keyword research、competitor analysis。执行前必须读取 AGENT_CONFIG.md。"
---

# Selection Agent Skill — 全渠道选品 Agent

## 触发条件
当用户提到"选品"、"关键词调研"、"SEO分析"、"竞品分析"、"keyword research"、"competitor analysis"时激活。

## ⚠️ 必读配置
**执行前必须读取**: `/tmp/powerful-trendplus/AGENT_CONFIG.md`
这里面写死了所有 Token、竞品列表、输出结构、环境变量，不要忘记！

## 快速执行
```bash
cd /tmp/powerful-trendplus
source .env.local 2>/dev/null
python3 scripts/run_full_research.py
```

## 环境变量（全部已配置）
| 变量 | 状态 |
|------|------|
| `SEMRUSH_API_KEY` | ✅ 系统环境变量 |
| `FB_ADS_TOKEN` | ✅ `.env.local`（App需 `ads_read` 权限） |
| `NOTION_API_KEY` | ✅ 系统环境变量（DB未授权） |
| `GEMINI_API_KEY` | ✅ `~/.bashrc` |

## 竞品列表（固定）
photoroom.com, remini.ai, fotor.com, picsart.com, faceapp.com, cutout.pro

## 去重数据源
- A. Sitemap: `https://art.myshell.ai/sitemap.xml` → `enpage.xml`
- B. CMS Base44: `https://app.base44.com/api`
- C. Notion Bot DB: `1113f81ff51e802f8056d66c76a9f9e6`（待授权）

## 固定输出结构
```json
{
  "keyword": "...", "func_cn": "...", "kd": 42, "volume": 49500,
  "region": "US", "comp_url": "...", "comp_domain": "...",
  "coverage": "new|exists_sitemap|exists_cms|exists_notion|duplicate",
  "dedup_source": "", "fb_ads_count": 0, "fb_top_advertiser": "",
  "gap_score": 85.2, "priority": "high|medium|low"
}
```

## 项目仓库
https://github.com/Arxchibobo/powerful-trendplus

## 依赖
- Semrush Skill（关键词数据）→ 需要 `SEMRUSH_API_KEY`
- Google Workspace Skill（Sheets 输出）→ 需要 OAuth
- MySQL Skill（内部数据对比）→ 需要数据库凭证

## 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| Semrush API 限额 | 免费版有日请求上限 | 减少关键词批量，分批查询 |
| 关键词为空 | 查询词太窄或拼写错误 | 放宽匹配，尝试同义词 |
| Sheets 写入失败 | OAuth token 过期 | 提示用户重新授权 |
| 超时 | 大量关键词并发查询 | 分批处理，每批 ≤20 个 |
