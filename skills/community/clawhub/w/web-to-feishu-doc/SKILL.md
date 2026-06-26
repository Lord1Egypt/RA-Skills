---
name: web-to-feishu-doc
description: |
  将任意网页链接转为结构化 Markdown 并保存到飞书云文档。
  触发词：转文档、抓网页存飞书、网页转文档、web to feishu、url 转文档、保存网页
---

# 网页转飞书文档

## 功能概述

将任意网页链接一键转为结构化 Markdown，并保存到飞书云文档。

**支持的信源：**
- X/Twitter 推文、长文、Thread 线程
- 微信公众号文章
- 小红书笔记
- 微博
- YouTube 视频
- 任意 HTML 网页
- 本地文件：PDF、Word、PPT、Excel、图片、音频等

**工作流：** 自动识别 URL/文件类型 → 路由到最佳抓取工具 → 结构化 Markdown → 保存到飞书

**触发条件：** 当用户提供任意 URL 或本地文件并要求转存为文档时。

---

## 安全配置

⚠️ **凭证必须通过环境变量配置，禁止硬编码：**

### 飞书配置

```bash
# 设置环境变量
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 知识库目录配置（可选）

```bash
export FEISHU_SPACE_ID="7610267053223644346"  # OpenClaw 知识库
export FEISHU_TARGET_FOLDER="TJ4jwWi6wivQxCkiefKcwJKcnES"  # 使用指南目录
```

---

## 工作流程

### 步骤 1：识别内容类型

自动检测链接类型：

| 类型 | URL 特征 | 处理方式 |
|------|---------|----------|
| X/Twitter | x.com / twitter.com | 提取推文 JSON → 结构化转换 |
| 微信公众号 | mp.weixin.qq.com | 使用 markitdown 抓取 |
| 小红书 | xiaohongshu.com | 使用 markitdown 抓取 |
| 微博 | weibo.com | 使用 markitdown 抓取 |
| YouTube | youtube.com / youtu.be | 提取标题 + 简介 + 时间戳 |
| 普通网页 | 其他 https:// | 使用 web_fetch 抓取 |
| 本地文件 | .pdf/.docx/.pptx 等 | 下载后转换 |

### 步骤 2：获取网页内容

使用 `web_fetch` 获取内容：

```
web_fetch --url <用户提供的链接> --extractMode markdown
```

### 步骤 3：分析内容并分类

LLM 自动分析内容：
- 提取标题、摘要、关键词
- 判断内容类型（教程、文档、新闻、产品等）
- 匹配知识库映射规则
- 如无法自动判断，询问用户

**知识库映射规则：**

| 内容特征 | 目标知识库 | 目标目录 |
|----------|-----------|---------|
| OpenClaw 相关 | OpenClaw 小龙虾 | 二、使用指南 |
| AI Agent 技术 | AI 机器人维修智能体 | - |
| 项目文档 | 垂直大模型项目 | - |
| 参考资料 | 参考资料 | - |
| 提示词 | GPT Prompts 提示词 | - |
| 解决方案 | 解决方案 | - |
| 无法判断 | 参考资料 | 待分类 |

### 步骤 4：确认保存位置（智能确认）

- 如内容特征明确且知识库存在 → 直接创建
- 如无法判断 → 输出建议并等待用户确认

### 步骤 5：创建飞书文档

使用 `feishu_create_doc` 创建文档：

**文档格式：**
```markdown
# 文档标题

> 来源：原始 URL
> 抓取时间：2026-05-14
> 整理：小万同学 AI

---

## 正文内容

（结构化 Markdown 内容）

---

## 元数据

- 原始链接：[URL](原始链接)
- 抓取时间：YYYY-MM-DD HH:MM
- 关键词：tag1, tag2, tag3
```

---

## 使用示例

### 示例 1：保存教程链接

用户发送：`https://www.runoob.com/ai-agent/openclaw-feishu.html`

自动回复：
```
✅ 识别到 OpenClaw 教程链接

分析结果：
- 标题：OpenClaw 接入飞书
- 类型：技术教程
- 建议保存：OpenClaw 知识库 → 二、使用指南

是否立即保存？
```

### 示例 2：保存无法分类的链接

用户发送：`https://example.com/unknown-article`

自动回复：
```
📄 获取到网页内容

分析结果：
- 标题：未知文章
- 类型：待分类

请选择保存位置：
1. 参考资料 → 待分类
2. 其他知识库（请告知）

回复数字或直接指定知识库名称。
```

---

## 故障处理

| 问题 | 解决方案 |
|------|---------|
| 网页无法访问 | 尝试 web_fetch 失败后，告知用户检查链接或手动粘贴内容 |
| 飞书凭证无效 | 检查 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量 |
| 知识库无权限 | 自动切换到「参考资料」知识库或询问用户 |
| 内容过长 | 截断后保存，或分多个文档保存 |
| 重复链接 | 提示用户该链接已保存，询问是否覆盖 |

---

## 依赖与依赖管理

本技能使用 OpenClaw 内置工具，无需额外安装：
- `web_fetch` - 网页内容获取
- `feishu_create_doc` - 飞书文档创建
- `feishu_wiki_space_node` - 知识库目录操作

---

## 环境变量说明

| 变量名 | 说明 | 必填 | 默认值 |
|--------|------|------|--------|
| FEISHU_APP_ID | 飞书应用 App ID | 是 | - |
| FEISHU_APP_SECRET | 飞书应用 App Secret | 是 | - |
| FEISHU_SPACE_ID | 默认知识库 ID | 否 | 7610267053223644346 |
| FEISHU_TARGET_FOLDER | 默认目录 ID | 否 | 动态判断 |

---

## 隐私与安全

- **凭证安全**：所有 API 凭证通过环境变量配置，无硬编码
- **内容处理**：仅处理用户提供的 URL 或文件
- **文件范围**：仅创建用户明确请求的文档
- **权限透明**：所有写入操作均有日志记录

---

## 扩展支持

如需扩展支持更多平台（如 B 站、知乎、Medium），在 SKILL.md 的「支持的信源」表格中添加对应 URL 特征和处理方式。