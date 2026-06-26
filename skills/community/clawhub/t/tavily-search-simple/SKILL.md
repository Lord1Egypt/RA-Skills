---
name: tavily-search
description: 【极简版省token】使用 Tavily API 执行网络搜索。专为 LLM 与 AI Agent 优化的搜索引擎。
requires:
  env: TAVILY_API_KEY
---

# Tavily Search

使用 Tavily API 在互联网上搜索并总结最新信息。本工具会向 `https://api.tavily.com/search` 发起网络请求。

## 配置环境变量与凭据

此脚本需要 Tavily API 密钥才能运行。请配置 `TAVILY_API_KEY` 环境变量（或将其写入 `~/.openclaw/.env`）：

```bash
export TAVILY_API_KEY="your_api_key_here"
```

## 使用方法

```bash
python3 scripts/tavily_search.py --query "你的搜索词" [--search-depth advanced] [--max-results 5]
```

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--|--|--|--|--|
| `query` | string | **是** | - | 搜索关键词 |
| `search-depth` | string | 否 | `basic` | 搜索深度：`basic` (基础, 1积分), `advanced` (高级, 2积分), `fast` (快速), `ultra-fast` (极速) |
| `topic` | string | 否 | `general` | 主题分类：`general` (通用), `news` (新闻), `finance` (金融) |
| `country` | string | 否 | - | 国家/地区（小写英文全名，如 `china`,`united states`,`singapore`，完整合法取值见 `scripts/tavily_search.py` 中 `TAVILY_COUNTRY_CHOICES`）；**仅 `topic=general` 生效** |
| `time-range` | string | 否 | - | 时间过滤：`day`, `week`, `month`, `year` (或简写 `d`, `w`, `m`, `y`) |
| `start-date` | string | 否 | - | 起始日期，格式如 `YYYY-MM-DD` |
| `end-date` | string | 否 | - | 结束日期，格式如 `YYYY-MM-DD` |
| `max-results` | int | 否 | 5 | 返回结果数量限制（0-20） |
| `include-images` | bool | 否 | `False` | 是否在结果中包含查询相关的图片 |
| `include-domains` | string | 否 | - | 仅搜索指定域名（多个用逗号分隔） |
| `exclude-domains` | string | 否 | - | 排除指定域名（多个用逗号分隔） |
| `chunks-per-source`| int | 否 | 3 | 每个来源提取的文本块数量 (1-3，仅在 depth 为 advanced/fast 时有效) |
| `auto-parameters` | bool | 否 | `False` | 开启后，Tavily 会根据查询意图自动覆盖及配置搜索参数 |
| `format` | string | 否 | `raw` | 输出格式控制：`raw` (原始JSON), `brave` (极简JSON), `md` (人类可读) |

## License

MIT License - Feel free to use and modify.