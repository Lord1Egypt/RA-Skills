---
name: vocational-ed-policy
displayName: 职业教育政策抓取
display_name: 职业教育政策抓取
title: 职业教育政策抓取
description: 自动抓取教育部、人社部及各省教育厅官网的职业教育政策文件和课题申报信息。支持按关键词筛选和定期汇总。
category: research
version: 2.0.0
author: erich1566
tags: [vocational-education, policy-scraper, government-documents, research, chinese]
languages: [zh, en]
---

# 职业教育政策信息抓取工具 | Vocational Education Policy Scraper

## 概述 | Overview

自动抓取教育部、人社部及各省教育厅官网的职业教育政策文件、课题申报信息，支持按关键词筛选和定期汇总。

Automatically scrapes vocational education policy documents and project announcements from Ministry of Education, Ministry of Human Resources, and provincial education departments. Supports keyword filtering and periodic summaries.

## 核心功能 | Core Features

### 1. 多源数据抓取 | Multi-Source Data Scraping

**支持的数据源 | Supported Sources:**
- **教育部** (Ministry of Education): https://www.moe.gov.cn
- **人社部** (Ministry of Human Resources): http://www.mohrss.gov.cn
- **各省教育厅** (Provincial Education Departments): 31个省市自治区教育部门官网

**抓取内容 | Content Types:**
- 政策文件 (Policy Documents)
- 课题申报信息 (Project Applications)
- 教学成果奖申报 (Teaching Achievement Awards)
- 产教融合文件 (Industry-Education Integration)
- 1+X证书政策 (1+X Certificate Policies)
- 双高计划通知 (Double High Plan Notifications)

### 2. 智能分类筛选 | Intelligent Classification and Filtering

**分类体系 | Classification System:**
- `policy`: 政策文件 (Policy Documents)
- `project`: 课题申报 (Project Applications)
- `achievement`: 教学成果奖 (Teaching Achievement Awards)
- `integration`: 产教融合 (Industry-Education Integration)
- `certificate`: 1+X证书 (1+X Certificates)
- `double_high`: 双高计划 (Double High Plan)

**筛选功能 | Filtering Capabilities:**
- 关键词筛选 (Keyword Filtering)
- 时间范围筛选 (Date Range Filtering)
- 类别筛选 (Category Filtering)
- 来源筛选 (Source Filtering)

### 3. 定期汇总 | Periodic Summaries

**汇总功能 | Summary Features:**
- 按时间周期汇总 (Daily/Weekly/Monthly summaries)
- 按主题分类汇总 (Themed summaries)
- 按地区分类汇总 (Regional summaries)
- 自动生成报告 (Automatic report generation)

## 快速开始 | Quick Start

### 基本用法 | Basic Usage

**中文示例 | Chinese Examples:**
```bash
# 抓取最近30天的所有政策文件
python scripts/scrape_voc_ed_policy.py --days 30

# 按关键词筛选（双高计划、产教融合）
python scripts/scrape_voc_ed_policy.py --keywords "双高计划" "产教融合" --days 30

# 按类别筛选（仅政策文件）
python scripts/scrape_voc_ed_policy.py --category policy --days 7

# 综合筛选（多个关键词 + 类别 + 时间）
python scripts/scrape_voc_ed_policy.py --keywords "1+X证书" --category certificate --days 14

# 保存到指定文件
python scripts/scrape_voc_ed_policy.py --keywords "教学成果奖" --output results.json
```

**English Examples:**
```bash
# Scrape all policy documents from the last 30 days
python scripts/scrape_voc_ed_policy.py --days 30 --lang en

# Filter by keywords
python scripts/scrape_voc_ed_policy.py --keywords "双高计划" "产教融合" --days 30 --lang en

# Filter by category
python scripts/scrape_voc_ed_policy.py --category policy --days 7 --lang en

# Comprehensive filtering
python scripts/scrape_voc_ed_policy.py --keywords "1+X证书" --category certificate --days 14 --lang en

# Save to specified file
python scripts/scrape_voc_ed_policy.py --keywords "教学成果奖" --output results.json --lang en
```

### 命令行参数 | Command Line Arguments

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keywords` | 关键词列表 | `--keywords "双高计划" "产教融合"` |
| `--days` | 回溯天数（默认30） | `--days 7` |
| `--category` | 筛选类别 | `--category policy` |
| `--output` | 输出文件路径 | `--output results.json` |
| `--lang` | 语言 (zh/en) | `--lang zh` |

## 工作流程 | Workflow

### 步骤 1: 确定抓取需求 | Step 1: Determine Scraping Requirements

**中文:**
明确需要抓取的内容类型、时间范围、关键词和类别。

**English:**
Clarify the content type, time range, keywords, and category needed.

**示例 | Example:**
- 内容：双高计划相关政策 (Double high plan policies)
- 时间：最近30天 (Last 30 days)
- 类别：政策文件 (Policy documents)

### 步骤 2: 运行抓取脚本 | Step 2: Run Scraping Script

**中文:**
根据需求配置参数，运行抓取脚本。

**English:**
Configure parameters based on requirements and run the scraping script.

```bash
python scripts/scrape_voc_ed_policy.py --keywords "双高计划" --category policy --days 30
```

### 步骤 3: 查看结果 | Step 3: Review Results

**中文:**
抓取完成后，查看生成的JSON文件或终端输出摘要。

**English:**
After scraping is complete, review the generated JSON file or terminal summary.

**输出格式 | Output Format:**
```json
{
  "websites_scraped": 3,
  "total_documents": 45,
  "results": [
    {
      "title": "教育部关于公布中国特色高水平高职学校和专业建设计划名单的通知",
      "url": "https://www.moe.gov.cn/...",
      "date": "2024-01-15",
      "source": "教育部",
      "category": "double_high",
      "keywords": ["双高计划", "高职学校"]
    }
  ],
  "errors": [],
  "timestamp": "2024-01-20T10:30:00",
  "filters": {
    "keywords": ["双高计划"],
    "days": 30,
    "category": "policy"
  }
}
```

### 步骤 4: 数据分析和汇总 | Step 4: Data Analysis and Summary

**中文:**
根据抓取结果进行分析，生成汇总报告。

**English:**
Analyze the scraped results and generate summary reports.

## 高级功能 | Advanced Features

### 定期抓取设置 | Scheduled Scraping Setup

**中文:**
使用cronjob设置定期抓取任务。

**English:**
Use cronjob to set up scheduled scraping tasks.

```bash
# 每天早上8点抓取最近30天的政策文件
0 8 * * * python /path/to/scripts/scrape_voc_ed_policy.py --days 30 --output /path/to/results/daily_$(date +\%Y\%m\%d).json

# 每周一抓取最近7天的政策文件
0 8 * * 1 python /path/to/scripts/scrape_voc_ed_policy.py --days 7 --output /path/to/results/weekly_$(date +\%Y\%m\%d).json
```

### 自定义网站配置 | Custom Website Configuration

**中文:**
在脚本中添加新的网站配置。

**English:**
Add new website configurations in the script.

```python
EDU_WEBSITES = {
    "新增网站": {
        "base_url": "https://example.gov.cn",
        "policy_url": "https://example.gov.cn/policy/",
        "selectors": {
            "title": "a[title]",
            "date": ".date",
            "link": "a[href]"
        },
        "keywords": ["职业教育", "政策"]
    }
}
```

### 结果导出和格式化 | Result Export and Formatting

**中文:**
将JSON结果转换为其他格式（CSV、Markdown、HTML）。

**English:**
Convert JSON results to other formats (CSV, Markdown, HTML).

```python
# 导出为CSV
import pandas as pd
df = pd.DataFrame(results['results'])
df.to_csv('results.csv', index=False, encoding='utf-8-sig')

# 导出为Markdown
def to_markdown(results):
    md = "# 职业教育政策抓取结果\n\n"
    for item in results['results']:
        md += f"## {item['title']}\n"
        md += f"- **来源**: {item['source']}\n"
        md += f"- **日期**: {item['date']}\n"
        md += f"- **链接**: {item['url']}\n\n"
    return md
```

## 资源说明 | Resources

### scripts/scrape_voc_ed_policy.py
核心抓取脚本，支持：
- 多网站并行抓取
- 智能关键词匹配
- 自动分类
- 双语输出
- 错误处理
- 真实网页抓取实现（requests + BeautifulSoup4）

**实现详情**: See `references/implementation-notes.md` for complete technical implementation notes, date parsing patterns, filtering logic, and ClawHub publishing workflow.

### references/edu_websites.md
教育部、人社部及各省教育厅官网列表，包含：
- 官网URL
- 职业教育专栏URL
- 常见关键词

### references/implementation-notes.md
网页抓取实现技术笔记，包含：
- 完整实现流程
- 日期解析模式
- 过滤机制详解
- 错误处理策略
- WSL 发布工作流
- ClawHub 特定说明

### i18n_helper.py
国际化辅助模块，支持：
- 自动语言检测
- 双语输出
- 可扩展的语言支持

### i18n.json
翻译文件，包含：
- UI字符串
- 错误消息
- 分类名称
- 帮助文本

## 注意事项 | Important Notes

### ClawHub 显示名称限制 | ClawHub Display Name Limitations

**中文:**
- ⚠️ **重要限制**: ClawHub 的技能显示名称由系统自动生成，无法自定义
- 显示名称基于 slug 自动转换为 Title Case（如 `voc-ed-policy` → "Voc Ed Policy Scraper"）
- **无效字段**: `displayName`、`title`、`display_name` 字段目前不影响实际显示
- **建议**: 接受英文显示名称，但保持 `description` 字段为完整中文描述
- **用户可见内容**: 用户安装时会看到 `slug - 系统生成的英文名称` + 完整的中文 description

**English:**
- ⚠️ **Important Limitation**: ClawHub automatically generates skill display names from slugs; custom display names are not supported
- Display names are auto-converted to Title Case (e.g., `voc-ed-policy` → "Voc Ed Policy Scraper")
- **Ineffective fields**: `displayName`, `title`, and `display_name` fields currently do not affect actual display
- **Recommendation**: Accept English display names but maintain full Chinese `description` field
- **User-visible content**: Users see `slug - system-generated English name` + complete Chinese description when installing

### Slug 格式要求 | Slug Format Requirements

**中文:**
- **格式**: 仅允许小写字母、数字、单个连字符
- **限制**: 不能以连字符开头或结尾，不能有连续连字符
- **示例**: ✅ `voc-ed-policy`、`zhinao-vocational-policy` | ❌ `职业教育政策`、`voc--ed-policy`
- **原因**: ClawHub 系统限制（slug 验证器）

**English:**
- **Format**: Only lowercase letters, digits, single hyphens allowed
- **Restrictions**: Cannot start or end with hyphen, no consecutive hyphens
- **Examples**: ✅ `voc-ed-policy`, `zhinao-vocational-policy` | ❌ `职业教育政策`, `voc--ed-policy`
- **Reason**: ClawHub system limitations (slug validator)

### WSL 环境发布 ClawHub 技能 | Publishing from WSL to ClawHub

**中文:**
**发布流程**:
1. 复制技能到 Windows 桌面: `cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/`
2. 使用 PowerShell 发布: `powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version X.X.X"`
3. 清理桌面: `rm -rf /mnt/c/Users/lenovo/Desktop/your-skill`

**覆盖更新现有技能**:
1. 修改 SKILL.md，提升版本号
2. 复制到桌面并发布（使用相同 slug）
3. 系统会自动覆盖原有版本

**English:**
**Publishing Workflow**:
1. Copy skill to Windows Desktop: `cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/`
2. Publish via PowerShell: `powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version X.X.X"`
3. Clean up desktop: `rm -rf /mnt/c/Users/lenovo/Desktop/your-skill`

**Updating Existing Skills**:
1. Modify SKILL.md, increment version number
2. Copy to desktop and publish (using same slug)
3. System automatically overwrites previous version

### 网站访问限制 | Website Access Restrictions

**中文:**
1. 部分政府网站可能有反爬虫机制，需要设置合理的访问频率
2. 建议每次抓取间隔至少1秒（代码已实现 `time.sleep(1)`）
3. 避免短时间内大量请求
4. 遵守网站的robots.txt规则
5. 使用合理的 User-Agent 头（代码已设置）

**English:**
1. Some government websites may have anti-scraping mechanisms; set reasonable request intervals
2. Recommend at least 1 second interval between requests (implemented in code as `time.sleep(1)`)
3. Avoid massive requests in a short time
4. Follow website robots.txt rules
5. Use reasonable User-Agent headers (already configured in code)

### 数据准确性 | Data Accuracy

**中文:**
1. 官方网站可能随时更新，URL结构可能变化
2. 不同网站的HTML结构差异大，需要针对性解析
3. 日期格式不统一，需要灵活解析
4. 建议定期验证抓取结果的准确性

**English:**
1. Official websites may update at any time, URL structures may change
2. HTML structures vary significantly between websites, requiring targeted parsing
3. Date formats are not uniform, requiring flexible parsing
4. Regularly verify the accuracy of scraped results

### 法律合规 | Legal Compliance

**中文:**
1. 仅用于学习和研究目的
2. 不得用于商业用途
3. 遵守相关法律法规
4. 尊重网站版权和使用条款

**English:**
1. For learning and research purposes only
2. Not for commercial use
3. Comply with relevant laws and regulations
4. Respect website copyright and terms of use

## Pitfalls | 常见问题

### Q1: 抓取时出现 "缺少依赖库" 错误怎么办？| How to fix "missing dependencies" error?

**中文**: 
```bash
pip install requests beautifulsoup4
```

**English**:
```bash
pip install requests beautifulsoup4
```

### Q2: 抓取结果包含很多无关链接怎么办？| Too many irrelevant links?

**中文**: 脚本已添加过滤规则，自动排除：
- javascript: 链接和锚点
- 导航链接（司局、委员会、办公室）
- 备案信息（ICP、网安备）
- 太短的标题（< 5字符）

使用 `--keywords` 参数进一步筛选：
```bash
python scrape_voc_ed_policy.py --keywords "双高计划" "产教融合"
```

**English**: Script includes built-in filters to exclude:
- javascript: links and anchors
- Navigation links (bureaus, committees, offices)
- ICP/license info
- Short titles (< 5 chars)

Use `--keywords` for additional filtering.

### Q3: ClawHub 发布 slug 格式限制 | ClawHub slug format restrictions

**中文**: ClawHub slug 必须符合以下规则：
- 只能包含小写字母、数字和单个连字符
- 必须以字母或数字开头和结尾
- 不能包含中文字符
- 不能包含连续连字符

**示例**：
- ✅ `voc-ed-policy`
- ✅ `zhinao-vocational-policy`
- ❌ `职业教育政策抓取`（包含中文）
- ❌ `voc--ed`（连续连字符）

**English**: ClawHub slug must:
- Contain only lowercase letters, digits, and single hyphens
- Start and end with a letter or digit
- NOT contain Chinese characters
- NOT contain consecutive hyphens

**Examples**:
- ✅ `voc-ed-policy`
- ✅ `zhinao-vocational-policy`
- ❌ `职业教育政策抓取` (contains Chinese)
- ❌ `voc--ed` (consecutive hyphens)

### Q4: ClawHub 显示名称无法自定义？| Can't customize display name?

**中文**: ClawHub 系统会根据 slug 自动生成英文显示名称，`displayName` 字段不会影响显示。

**解决方案**：
- 在 `description` 字段使用中文完整描述
- slug 选择简短易记的英文（如 `voc-ed-policy`）
- 用户在技能列表中会看到中文描述

**English**: ClawHub auto-generates English display names from slug. `displayName` field does not affect display.

**Workaround**:
- Use full Chinese description in `description` field
- Choose short, memorable slug (e.g., `voc-ed-policy`)
- Users will see Chinese description in skill list

### Q5: WSL 环境下如何发布技能到 ClawHub？| How to publish from WSL?

**中文**: WSL 不能直接运行 Windows 命令（如 powershell.exe），需要使用工作流程：

```bash
# 1. 复制技能到 Windows Desktop
cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/

# 2. 使用 PowerShell 发布
powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version 1.0.0"

# 3. 清理临时文件
rm -rf /mnt/c/Users/lenovo/Desktop/your-skill
```

**注意**：如果 slug 冲突，使用 `--slug` 参数指定或使用 `clawhub skill rename`。

**English**: WSL cannot run Windows commands directly. Use this workflow:

```bash
# 1. Copy skill to Windows Desktop
cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/

# 2. Publish using PowerShell
powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version 1.0.0"

# 3. Clean up temp files
rm -rf /mnt/c/Users/lenovo/Desktop/your-skill
```

**Note**: If slug conflict, use `--slug` parameter or `clawhub skill rename`.

### Q6: 如何覆盖已发布的技能而不是创建新的？| How to update existing skill not create new?

**中文**: 使用相同的 slug 发布会提示冲突。正确的工作流程：

```bash
# 方式 1: 直接发布相同 slug（覆盖）
clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version 1.1.0

# 方式 2: 如果需要改名，先 rename 再发布
clawhub skill rename old-slug new-slug --yes
```

**关键点**：更新版本号，不要修改 name 字段的 slug。

**English**: Publishing with same slug triggers conflict. Correct workflow:

```bash
# Option 1: Publish with same slug (overwrite)
clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version 1.1.0

# Option 2: Rename if needed, then publish
clawhub skill rename old-slug new-slug --yes
```

**Key point**: Update version number, do not change slug in name field.

## 扩展建议 | Extension Suggestions

### 未来可能的改进 | Potential Future Improvements

1. **增量抓取**: 只抓取新增和更新的内容
2. **智能推荐**: 基于用户历史行为推荐相关政策
3. **全文搜索**: 支持对抓取内容的全文检索
4. **可视化分析**: 生成图表和可视化报告
5. **邮件通知**: 新政策发布时自动发送通知
6. **多格式输出**: 支持导出为PDF、Word等格式

### 贡献指南 | Contribution Guidelines

**中文:**
欢迎提交问题和改进建议。在提交PR之前，请确保：
1. 代码符合PEP 8规范
2. 添加必要的注释和文档
3. 测试新增功能
4. 更新相关文档

**English:**
Issues and improvement suggestions are welcome. Before submitting a PR, ensure:
1. Code follows PEP 8 standards
2. Add necessary comments and documentation
3. Test new features
4. Update relevant documentation

---

*版本: 1.0.0 | Version: 1.0.0*
*最后更新: 2024年 | Last Updated: 2024*