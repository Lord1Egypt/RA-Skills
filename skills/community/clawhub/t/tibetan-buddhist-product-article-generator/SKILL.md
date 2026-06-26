---
name: tibetan-buddhist-product-article-generator
summary: 从藏传佛教草稿生成验证过的中文文章 + 藏式PNG图 | Generate verified Chinese article + Tibetan-style PNG images from draft
description: |
  读取 ~/.openclaw/workspace/tibetanDraft/ 中的Markdown，识别藏传佛教产品主题，生成约1000字简体中文文章到 ~/.openclaw/workspace/tibetanProc/。
  只写藏传佛教，事实需网络核验，含至少3章节+主图+章节图。文件名用时间戳格式。
  
  Read draft Markdown from ~/.openclaw/workspace/tibetanDraft/, identify Tibetan Buddhist product, generate ~1000 word Simplified Chinese article to ~/.openclaw/workspace/tibetanProc/.
  Only Tibetan Buddhism, facts web-verified, at least 3 sections + hero + section images. Timestamp filenames.
version: 1.1.0
author: Jeff Yang (adapted for OpenClaw/ClawHub)
category: [content-generation, research, tibetan-buddhism]
tags: [tibetan, buddhism, article, chinese, image-generation, markdown]
user-invocable: true
disable-model-invocation: false
requires:
  os: [linux, darwin, win32]
  bins: [python3]
  env: [HOME]
trigger:
  keywords: ["tibetan article", "藏传文章", "tibetan product", "藏传产品", "tibetanDraft"]
  regex: "(?i)tibetan(buddhism|product|article|draft|proc)"
  commands: ["/tibetan-gen", "/藏传文章"]
---

# Tibetan Buddhist Product Article Generator

## 🎯 Purpose
自动生成符合藏传佛教标准的中文产品文章，包含网络事实核验和藏式图像。

## 📂 Input/Output Paths
**输入目录**: `~/.openclaw/workspace/tibetanDraft/`  
**输出目录**: `~/.openclaw/workspace/tibetanProc/`  

**文件命名规则** (必须严格遵守):
```sh
yymmddHHMM_主体名.md
yymmddHHMM_main.png # 主图
yymmddHHMM_section1.png # 章节1图
yymmddHHMM_section2.png # 章节2图
```


## 🔄 完整执行流程

### 1. 初始化检查

检查 ~/.openclaw/workspace/tibetanDraft/ 是否存在
检查是否有 .md 文件
如果目录不存在或为空 → 报错 "草稿目录为空，请先放入输入文件"
如果多个文件 → 读取最新的一个

### 2. 主题识别
从输入文件提取藏传佛教产品主题，如：唐卡、法器、佛像、经书等。

### 3. 网络研究 (必须)

搜索查询示例：
"Tibetan Buddhism [产品] history verified"
"Tibetan [产品] traditional use past present"
"Tibetan Buddhism [产品] materials facts"

### 4. 文章生成规则
- **语言**: 口语化、非正式简体中文
- **长度**: 约1000字
- **章节** (至少3个):

1. 藏族历史与藏传佛教历史相关背景
2. 产品信息核验 (材料、制作、用途)
3. 藏族过去和现在的用法
4. 对拥有者的宗教文化身心价值 (不夸大)

- **事实原则**: 未验证的信息写"资料显示"或"未确认"

### 5. 图像生成

主图提示: "Traditional Tibetan Buddhist [产品] in authentic thangka style, rich colors, gold details, temple setting"
章节图提示: "Tibetan [场景] featuring [产品], authentic religious art style"
输出: PNG, 同目录, 时间戳文件名

### 6. 输出模板

```markdown
# [产品名称]
摘要
...

## 第一节：历史背景
...

## 第二节：产品信息
...
```

(以此类推)

## ⚠️ 错误处理与回退

| 错误场景 | 处理方式 | 输出文件 |
|----------|----------|----------|
| 草稿目录不存在 | 创建目录并提示 | 无 |
| 无输入文件 | 输出说明文件 | `yymmddHHMM_usage.md` |
| 主题无法识别 | 列出可能主题，等待确认 | `yymmddHHMM_topics.md` |
| 网络搜索失败 | 使用本地知识 + 标记"需进一步验证" | 正常输出 + 警告 |
| 图像生成失败 | 输出无图版本 + 记录日志 | `yymmddHHMM_log.txt` |

## 🧪 测试用例

**输入文件**: `test_tibetanDraft/thangka_draft.md`

我想写一篇关于唐卡的文章...

**预期输出**:

2604071901_thangka.md (约1000字)
2604071901_main.png
2604071901_section1.png (历史)
2604071901_section2.png (产品信息)
...

## 📋 元数据文件 (自动生成)
每个输出文件夹会附带:

skill-run.json:
{
"timestamp": "2604071901",
"input_file": "原文件名",
"product": "识别的产品",
"word_count": 1024,
"images_generated": 4,
"research_sources": ["web:1", "web:11", ...]
}

## 🚀 自动化运行参数

--dry-run: 只检查不生成
--product=强制指定产品名
--draft=指定输入文件
--output-dir=自定义输出目录

---
*此技能符合 ClawHub 发布标准，已包含完整错误处理、测试用例和自动化模板。*
