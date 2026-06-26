---
name: wechat-writing-workflow
description: Standardized WeChat official account writing workflow integrating wechat-publisher, wechat-toolkit, wechat-mp-writer-skill and other skills. Provides complete workflow from material search to publishing with 5 stages.
license: MIT License
metadata:
    skill-author: academic-assistant
    version: 1.0.0
    created: 2026-03-14
---

# WeChat Writing Workflow

## Overview

标准化微信公众号写作工作流，整合多个公众号技能，提供从素材搜索到发布推送的完整流程。

## 5 Workflow Stages

### 1. 素材搜索与整理 (15-30 分钟)
- 文章搜索
- 文章下载
- 素材整理

**使用技能**: wechat-article-search, wechat-toolkit

---

### 2. 内容创作与改写 (30-60 分钟)
- 文章写作
- 内容改写/洗稿
- 标题优化

**使用技能**: wechat-mp-writer-skill, wechat-toolkit, academic-writing

---

### 3. 格式优化与排版 (15-30 分钟)
- Markdown 格式化
- 图片处理
- 排版美化

**使用技能**: wechat-publisher, wechat-toolkit

---

### 4. 发布与推送 (5-10 分钟)
- 创建草稿
- 预览检查
- 定时发布/群发

**使用技能**: wechat-publisher, wechat-mp-publish

---

### 5. 数据分析与优化 (10-20 分钟)
- 数据统计
- 用户画像
- 内容优化

**使用技能**: data-analysis, statistical-analysis

---

## Content Types

### 科普文章 (popular_science)

**特点**:
- 字数：1500-3000
- 风格：轻松易懂
- 频率：每日/每周

**适用场景**:
- 心理学科普
- 健康知识普及
- 研究进展介绍

---

### 研究报告 (research_report)

**特点**:
- 字数：3000-5000
- 风格：专业严谨
- 频率：每月

**适用场景**:
- 调研报告
- 研究进展
- 数据分析报告

---

### 每日小贴士 (daily_tips)

**特点**:
- 字数：300-500
- 风格：简短温馨
- 频率：每日

**适用场景**:
- 心理小贴士
- 健康建议
- 早安/晚安语录

---

### 案例分析 (case_study)

**特点**:
- 字数：2000-4000
- 风格：故事性
- 频率：每周

**适用场景**:
- 咨询案例
- 成功案例
- 失败教训

---

## Usage

### 基本使用

```bash
# 完整工作流
python wechat_writing_workflow.py --type popular_science --topic "幸福感提升"

# 仅素材搜索
python wechat_writing_workflow.py --stage 1 --keyword "心理学"

# 仅内容创作
python wechat_writing_workflow.py --stage 2 --type popular_science

# 仅发布
python wechat_writing_workflow.py --stage 4 --file article.md
```

---

### 高级使用

```bash
# 指定输出格式
python wechat_writing_workflow.py --type daily_tips --output article.md --format markdown

# 定时发布
python wechat_writing_workflow.py --stage 4 --file article.md --schedule "08:00"

# 数据分析
python wechat_writing_workflow.py --stage 5 --article-id "文章 ID"
```

---

## Material Search

### 文章搜索

**使用技能**: wechat-article-search

**搜索命令**:
```bash
# 搜索相关主题文章
node search_wechat.js "心理学 幸福感" -n 20 -c

# 指定数量
node search_wechat.js "AI 心理学" -n 30

# 保存到文件
node search_wechat.js "主观幸福感" -n 20 -o search_results.json

# 抓取正文内容
node search_wechat.js "幸福感研究" -n 10 -c
```

**参数说明**:
- `query`: 搜索关键词（必填）
- `-n, --num`: 返回数量（默认 10，最大 50）
- `-o, --output`: 输出 JSON 文件路径
- `-c, --fetch-content`: 抓取文章正文内容

---

### 文章下载

**使用技能**: wechat-toolkit

**下载命令**:
```bash
# 使用默认路径
node download.js "文章 URL"

# 指定下载路径
node download.js "文章 URL" --output ~/Downloads/wechat-articles

# 跳过图片/视频
node download.js "文章 URL" --no-image
node download.js "文章 URL" --no-video
```

**输出结构**:
```
<下载目录>/<文章标题>/
├── content/article.html      # 完整 HTML
├── metadata.json              # 标题、作者、时间等
├── images/                    # 所有配图
└── videos/                    # 所有视频/音频
```

---

## Content Creation

### 文章写作

**使用技能**: wechat-mp-writer-skill

**写作流程**:
1. 确定文章主题
2. 列提纲（3-5 个要点）
3. 收集素材支撑
4. 原创写作
5. 添加个人观点

**输出**:
- 文章初稿（Markdown 格式）
- 标题建议（3-5 个）
- 摘要（100-200 字）

---

### 内容改写/洗稿

**使用技能**: wechat-toolkit

**改写流程**:
1. 获取原文
2. AI 去痕迹
3. 原创改写
4. 降重处理
5. 质量检查

**改写技巧**:
- 改变文章结构
- 替换同义词
- 调整句式
- 添加个人观点
- 改变叙述角度

---

### 标题优化

**标题类型**:
- **数字型**: "5 个方法提升幸福感"
- **疑问型**: "为什么你总是不快乐？"
- **对比型**: "月薪 3 千和 3 万的区别"
- **悬念型**: "她这样做，彻底改变了人生"
- **权威型**: "清华教授：幸福感的秘密"

**标题检查清单**:
- [ ] 包含关键词
- [ ] 引发好奇心
- [ ] 提供价值承诺
- [ ] 长度适中（20-30 字）
- [ ] 避免标题党

---

## Formatting & Publishing

### Markdown 格式化

**Frontmatter 元数据** (必需):
```markdown
---
title: 文章标题
cover: 封面图片路径
author: 作者名
date: 2026-03-14
tags: [心理学，幸福感]
---
```

**正文格式**:
```markdown
# 一级标题（文章标题）

## 二级标题（章节标题）

### 三级标题（小节标题）

正文内容...

**加粗重点**

> 引用内容

- 列表项 1
- 列表项 2

![图片描述](图片路径)
```

---

### 发布流程

**使用技能**: wechat-publisher

**发布命令**:
```bash
# 发布文章
node publish.js article.md

# 使用 wechat-mp-publish
python wechat_publisher.py --action create_draft --title "标题" --content "内容"
```

**发布检查清单**:
- [ ] 标题正确
- [ ] 封面图正确
- [ ] 摘要完整
- [ ] 正文格式正确
- [ ] 图片显示正常
- [ ] 链接可点击

---

### 定时发布

**最佳发布时间**:
- 工作日：早 8-9 点、午 12-13 点、晚 20-22 点
- 周末：早 9-10 点、晚 20-22 点

**定时发布命令**:
```bash
# 定时发布
python wechat_publisher.py --action schedule --time "2026-03-15 08:00" --draft-id "草稿 ID"

# 立即群发
python wechat_publisher.py --action publish --draft-id "草稿 ID"
```

---

## Data Analysis

### 数据统计

**使用技能**: data-analysis

**统计指标**:
- **阅读量**: 文章被阅读的次数
- **分享率**: 分享次数/阅读量
- **收藏率**: 收藏次数/阅读量
- **完成率**: 读完人数/阅读人数
- **点赞率**: 点赞次数/阅读量

---

### 用户画像

**分析内容**:
- 年龄分布
- 性别比例
- 地域分布
- 阅读时间
- 设备类型

---

### 内容优化

**优化方向**:
- **标题优化**: A/B 测试不同标题
- **内容优化**: 根据完成率调整内容长度
- **发布时间优化**: 根据阅读时间调整发布时间
- **话题优化**: 根据阅读量调整选题方向

---

## Quality Checks

### 内容质量

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| **原创度** | >90% | 70-90% | <70% |
| **价值性** | 高价值 | 中等价值 | 低价值 |
| **可读性** | 流畅易懂 | 基本可读 | 晦涩难懂 |
| **准确性** | 完全准确 | 基本准确 | 有错误 |

---

### 传播效果

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| **阅读量** | >10000 | 1000-10000 | <1000 |
| **分享率** | >10% | 5-10% | <5% |
| **完成率** | >60% | 40-60% | <40% |
| **互动率** | >5% | 2-5% | <2% |

---

## Best Practices

### 最佳实践

1. **内容为王**
   - 提供真实价值
   - 保持原创性
   - 持续输出优质内容

2. **标题优化**
   - 吸引但不标题党
   - 包含关键词
   - 引发好奇心

3. **视觉呈现**
   - 高质量配图
   - 统一视觉风格
   - 适当留白

4. **数据分析**
   - 定期分析数据
   - 根据数据优化
   - A/B 测试

---

### 避免错误

1. **内容问题**
   - ❌ 抄袭洗稿
   - ✅ 原创 + 合理引用

2. **标题问题**
   - ❌ 过度标题党
   - ✅ 吸引但准确

3. **排版问题**
   - ❌ 花哨混乱
   - ✅ 简洁清晰

4. **发布问题**
   - ❌ 频繁推送
   - ✅ 固定频率（如每日/每周）

---

## Integration

### 与学术写作配合

```
academic-writing: 负责学术内容
wechat-writing-workflow: 负责转化为公众号文章
```

---

### 与数据分析配合

```
data-analysis: 负责阅读数据分析
wechat-writing-workflow: 负责根据数据优化内容
```

---

## Examples

### 示例 1: 心理学科普文章

```bash
# 阶段 1: 素材搜索
node search_wechat.js "心理学 幸福感" -n 20 -c

# 阶段 2: 内容创作
python wechat_writing_workflow.py --stage 2 --type popular_science

# 阶段 3: 格式优化
# 添加 frontmatter，准备图片

# 阶段 4: 发布
node publish.js 心理学科普.md

# 阶段 5: 数据分析
# 微信公众号后台查看数据
```

**输出**: 心理学科普文章

---

### 示例 2: 每日心理小贴士

```bash
# 阶段 1-2: 快速创作
python wechat_writing_workflow.py --type daily_tips --topic "今日心情"

# 阶段 3: 简单排版
# 添加温馨配图

# 阶段 4: 定时发布
python wechat_publisher.py --action schedule --time "08:00" --file 心理小贴士.md
```

**输出**: 每日心理小贴士

---

### 示例 3: 研究进展报告

```bash
# 阶段 1: 整理研究数据
# 使用 data-analysis 分析数据

# 阶段 2: 撰写报告
python wechat_writing_workflow.py --stage 2 --type research_report

# 阶段 3: 添加图表
# 使用 scientific-visualization 生成图表

# 阶段 4: 发布
python wechat_publisher.py --action publish --file 研究进展.md

# 阶段 5: 数据分析
# 查看阅读、分享数据
```

**输出**: 研究进展报告

---

## Configuration

### 环境配置

**微信公众号配置**:
```bash
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
```

**wenyan-cli 安装**:
```bash
npm install -g @wenyan-md/cli
```

**wechat-toolkit 依赖**:
```bash
npm install -g cheerio
```

---

### 配置检查清单

- [ ] 已获取微信公众号 AppID
- [ ] 已启用并保存 AppSecret
- [ ] 已设置 IP 白名单
- [ ] 已安装 wenyan-cli
- [ ] 已配置环境变量
- [ ] 已安装 wechat-toolkit 依赖

---

## References

- 微信公众号开发文档：https://developers.weixin.qq.com/
- wenyan-cli: https://github.com/wenyan-md/cli
- wechat-toolkit: `skills/wechat-toolkit-1.0.1/SKILL.md`

---

**技能版本**: v1.0.1  
**创建时间**: 2026-03-14  
**维护者**: academic-assistant  
**下次更新**: 功能改进时

---

*高效公众号写作，从标准化工作流开始！*📱✍️
