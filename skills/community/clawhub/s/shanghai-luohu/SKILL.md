---
name: 上海落户公示查询
description: 查询上海落户公示信息，包括人才引进公示和居转户公示。触发词包括"上海落户公示"、"查询落户公示"、"人才引进公示"、"居转户公示"、"上海落户"、"户口公示"、"落户公示"、"商米落户"、"得物落户"。
version: 1.2.0
---

# 上海落户公示查询 Skill

## 描述

查询上海落户公示信息，包括：
- 《上海市引进人才申办本市常住户口》公示名单（人才引进）
- 持有《上海市居住证》人员申办本市常住户口公示名单（居转户）

## 数据来源

- 官方网站：上海国际人才网 (https://www.sh-italent.com/)
- 公示列表页：https://www.sh-italent.com/News/NewsList.aspx?TagID=5696

## 运行时工具

执行此 skill 需要以下工具：
- `execute_command`：执行 Python 脚本
- `web_fetch` 或 `search_content`：可选，用于抓取公示页面内容

运行环境要求：
- Python 3.6+（使用 urllib, webbrowser 等标准库，无需额外安装）
- 支持平台：macOS、Windows、Linux

## 支持平台

| 平台 | 支持状态 |
|------|----------|
| macOS | ✅ 支持 |
| Windows | ✅ 支持 |
| Linux | ✅ 支持 |

## 触发关键词

- "查询上海落户公示"
- "上海人才引进公示"
- "上海居转户公示"
- "最新落户公示名单"
- "上海落户"
- "户口公示"
- "落户公示查询"
- "某某公司的落户名单"（如：商米落户、得物落户）

## 执行指令

当触发此 skill 时，执行 skill 目录下的 `query_luohu.py` 脚本：

```bash
python3 "${SKILL_DIR}/query_luohu.py"
```

**说明**：
- `${SKILL_DIR}` 是 skill 的安装目录，由系统自动解析
- 脚本已内置默认参数，无需额外询问用户配置

### 命令行参数

```bash
# 默认查询
python3 query_luohu.py

# 指定浏览器
python3 query_luohu.py -b Chrome      # 使用 Chrome
python3 query_luohu.py -b Firefox     # 使用 Firefox
python3 query_luohu.py -b Edge        # 使用 Edge
python3 query_luohu.py -b Safari      # 使用 Safari

# 不打开浏览器，仅输出查询结果
python3 query_luohu.py -n
python3 query_luohu.py --no-browser
```

### 支持的浏览器

| 浏览器 | 参数值 | 说明 |
|--------|--------|------|
| Safari | `-b Safari` | macOS 默认浏览器 |
| Chrome | `-b Chrome` | Google Chrome |
| Firefox | `-b Firefox` | Mozilla Firefox |
| Edge | `-b Edge` | Microsoft Edge |
| Brave | `-b Brave` | Brave 浏览器 |
| Opera | `-b Opera` | Opera 浏览器 |

## 查询指定公司/人员

用户可以查询特定公司的落户公示名单：

- "商米的上海落户名单"
- "得物的落户公示"
- "查询吕博的落户公示"
- "朱天成的上海落户公示"

## 输出格式

```
==================================================
    上海落户公示信息查询
==================================================

【一】人才引进公示
  公示标题: 《上海市引进人才申办本市常住户口》公示名单
  公示日期: 2026-03-16
  公示链接: https://www.sh-italent.com/Article/xxx.shtml

【二】居转户公示
  公示标题: 持有《上海市居住证》人员申办本市常住户口公示名单
  公示日期: 2026-03-16
  公示链接: https://www.sh-italent.com/Article/xxx.shtml

==================================================
查询时间: 2026-03-16 11:06:59
运行平台: MACOS
==================================================

正在打开浏览器查看公示页面...
✓ 浏览器已打开

提示：公示期通常为 5 天，每月两次公示（月中和月底）
```

## 技术实现

1. 使用 Python urllib 抓取公示列表页面
2. 正则解析 HTML 获取最新公示链接
3. 抓取具体公示页面内容
4. 提取公示标题、日期等信息
5. 使用 webbrowser 模块打开浏览器（跨平台）

## 注意事项

- 公示期通常为 5 天
- 每月两次公示（月中和月底）
- 数据来源于官方网站，仅供参考
- 支持 macOS、Windows、Linux 全平台
- 默认使用系统默认浏览器

## 更新日志

### v1.2.0
- 添加运行时工具声明
- 优化执行指令说明，明确无需用户确认
- 精简文档结构

### v1.1.0
- 支持全平台（macOS/Windows/Linux）
- 移除硬编码路径
- 使用 Python webbrowser 模块实现跨平台浏览器支持
- 优化代码结构

### v1.0.0
- 初始版本
