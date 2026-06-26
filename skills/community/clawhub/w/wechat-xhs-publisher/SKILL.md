---
name: wechat-xhs-publisher
version: 1.0.0
description: 微信公众号与小红书一键发布工具。当需要将热点新闻改写成公众号文章并发布到微信公众号和小红书时使用，包括：1)根据热点新闻改写公众号文章 2)使用AI生成文章配图 3)发布前IP检测 4)发布到微信公众号 5)发布到小红书。触发场景：热点新闻发布、公众号文章发布、小红书种草、社交媒体同步发布。
---

# 微信公众号与小红书发布工具

将热点新闻一键改写并发布到微信公众号和小红书。

## 工作流程

```
[热点新闻] → [Step1:公众号文章创作] → [Step2:AI配图生成] → [Step3:IP检测] → [Step4:公众号发布] → [Step5:小红书发布]
```

## Step 1: 公众号文章创作

### 输入
- 热点新闻素材（标题、内容要点）
- 写作风格要求

### 核心命令
根据热点新闻和写作风格，生成一篇新的公众号文章：
1. 分析热点新闻的核心要点
2. 按照指定风格创作文章
3. 生成Markdown格式文章，包含frontmatter元数据

### 写作风格
- 根据用户指定风格执行
- frontmatter中的author使用用户提供的作者名

### 输出
- Markdown格式文章
- 保存在 `post-to-wechat/YYYY-MM-DD/` 目录
- frontmatter包含：title, author, date, source, cover_image

## Step 2: AI配图生成

### 核心命令
根据文章内容，分析需要生成的配图和插图数量，调用图像API生成对应图片：
1. 分析文章结构和内容要点
2. 确定需要几张配图（封面+内文插图）
3. 为每张图片生成合适的prompt
4. 调用图像API生成图片

### 配图规划
根据文章内容确定配图数量和风格

### 工具
使用 baoyu-image-gen 或直接调用图像API

### 保存路径
- 复制到文章目录：`post-to-wechat/YYYY-MM-DD/img/`
- 并保存到工作区：`img/`

## Step 3: IP检测

### 核心命令
在发布公众号文章前，调用 wechat-ip-checker 技能检测公网IP：
1. 获取当前公网IP（通过 ip38.com）
2. 与配置文件中的记录IP比对
3. IP无变化 → 继续执行公众号发布
4. IP有变化 → 中断流程，通知用户确认

### 工具
使用 wechat-ip-checker skill

### 配置文件
- 位置：`{workspace}/wechat_ip_config.md`
- 格式：
```markdown
# 微信公众号发布公网IP记录
公网IP地址: xxx.xxx.xxx.xxx
IP查询来源: https://www.ip38.com/
```

### 判断逻辑
- ✅ IP相同：继续执行 Step 4
- ❌ IP不同：中断流程，提示用户添加新IP到白名单

## Step 4: 公众号发布

### 工具
使用 baoyu-post-to-wechat

### 发布命令
```bash
cd <baoyu-post-to-wechat路径>
npx -y bun scripts/wechat-api.ts <文章md文件> \
  --theme default \
  --cover <封面图绝对路径> \
  --author "<作者名称>"
```

### 关键参数
- `--theme default` 必填
- `--cover` 使用绝对路径
- 配图路径需转换为相对路径（相对于文章md文件）

### 重要
- 发布时勾选原创声明
- 确保图片与文章一起上传

## Step 5: 小红书发布

### 工具
使用 xiaohongshu MCP (mcporter)

### 发布命令
```bash
mcporter call 'xiaohongshu.publish_content(
  title: "标题",
  content: "正文",
  images: ["图片绝对路径1", "图片绝对路径2"],
  tags: ["话题1", "话题2"],
  is_original: true
)'
```

### 关键参数
- `is_original: true` **必须**勾选原创
- 图片使用绝对路径
- 标题≤20字
- 正文不要包含#标签（通过tags传递）

## 常见问题

### Q: 图片路径问题
A: 封面图使用绝对路径；文章内配图使用相对于md文件的相对路径，并将图片复制到md文件同目录下

### Q: 小红书漏掉原创
A: 必须在参数中添加 `is_original: true`

### Q: 公众号图片未上传
A: 确保图片在md文件同目录下，脚本会自动上传

## 输出报告格式

```
## ✅ 发布完成

### 公众号
- 状态：草稿已保存
- media_id：xxx

### 小红书
- 状态：发布完成
- 原创：✅
```
