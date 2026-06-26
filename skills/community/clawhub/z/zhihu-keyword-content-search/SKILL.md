---
name: zhihu-crawler
description: 爬取知乎问题和回答。当用户要求爬取知乎、抓取知乎数据、搜索知乎问答，或提到"知乎"+"爬虫/爬取/抓取/搜索"时使用此技能。支持按关键词搜索问题、按回答数排序、抓取全部回答并保存为JSON和纯文本。
---

# 知乎爬虫 Skill

## 环境要求

- Python 3.7+（`python` 或 `python3` 命令）
- 依赖：`pip install requests`

## 工作流程

1. **识别关键词**：从用户请求中提取要搜索的关键词
2. **获取 Cookie**：若用户未提供，告知获取方式（见下方）
3. **执行脚本**：运行 `zhihu_crawl.py`，监控进度
4. **汇报结果**：问题数、回答数、输出目录

## 获取 Cookie

> 浏览器打开 zhihu.com 登录 → F12 → Network → 任意请求 → Request Headers → 复制 `cookie:` 后的完整值

## 执行命令

```bash
python zhihu_crawl.py \
  --cookie "用户的Cookie" \
  --keywords "关键词1" "关键词2" \
  --top 100 \
  --output ./zhihu_output
```

**Windows PowerShell：**
```powershell
python zhihu_crawl.py `
  --cookie "用户的Cookie" `
  --keywords "关键词1" "关键词2" `
  --top 100 `
  --output ./zhihu_output
```

> Windows 上若提示 SSL 错误，在命令前加：
> `$env:PATH = "C:\python\anaconda\Library\bin;" + $env:PATH`

## 参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--cookie` | 是 | — | 知乎登录 Cookie |
| `--keywords` | 否 | MyGO Ave Mujica 丰川祥子 | 搜索词，多个用空格分隔，含空格的词用引号 |
| `--top` | 否 | 100 | 取回答数最多的前 N 个问题 |
| `--output` | 否 | zhihu_output | 输出目录路径 |
| `--search-max` | 否 | 200 | 每个关键词最多搜索多少候选 |

## 输出文件

```
output/
├── question_{id}.json     # 每道题的完整数据（含全部回答）
├── _question_list.json    # 问题列表（按回答数降序）
└── _merged_all.txt        # 所有内容合并纯文本（可直接喂给 AI 分析）
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `SSL module not available` | Anaconda PATH 未配置 | 设置 `$env:PATH = "C:\python\anaconda\Library\bin;" + $env:PATH` |
| `ModuleNotFoundError: requests` | 未安装依赖 | `pip install requests` 或 `pip install --user requests` |
| `HTTP 403` | Cookie 失效 | 重新从浏览器复制 Cookie |
| 找到 0 个问题 | Cookie 失效或关键词无结果 | 检查 Cookie 是否完整有效 |

## 使用示例

**抓取单主题：**
```bash
python zhihu_crawl.py --cookie "abc..." --keywords "高松灯" --top 50 --output ./output_灯
```

**抓取多主题，取 TOP 200：**
```bash
python zhihu_crawl.py --cookie "abc..." --keywords "MyGO" "Ave Mujica" "丰川祥子" --top 200
```
