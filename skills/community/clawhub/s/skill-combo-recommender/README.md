# Skill Combo Recommender 🎯

智能推荐技能组合，帮助你找到最佳工作流程。

## 功能特点

- ✅ **智能推荐**：根据任务描述推荐最适合的技能
- ✅ **工作流生成**：自动生成完整的工作流程
- ✅ **预设工作流**：提供常见场景的预设工作流（小红书运营、内容创作、视频制作等）
- ✅ **使用示例**：为每个推荐技能提供具体的使用示例

## 安装

```bash
# 使用 OpenClaw 安装
clawhub install skill-combo-recommender

# 或手动安装
git clone https://github.com/utopiabenben/ai-skills.git
cd ai-skills/skills/skill-combo-recommender
./install.sh
```

## 使用方法

### 基础用法

根据任务描述推荐技能：

```bash
skill-combo-recommender --task "我想运营小红书账号"
```

输出示例：
```
🎯 任务: 我想运营小红书账号
============================================================

📋 推荐技能:

🎯 xiaohongshu-content (匹配度: 3.0)
   描述: 小红书爆款内容创作
   标签: content-creation, xiaohongshu, social-media
   示例: 生成小红书爆款笔记, 创作种草文案

🎯 xiaohongshu-image-gen (匹配度: 2.0)
   描述: 小红书图片生成技能
   标签: ai, image, xiaohongshu
   示例: 生成小红书配图, 家装图片

...

============================================================

🚀 推荐工作流: 小红书运营全流程
   描述: 完整的小红书账号运营工作流
   涉及技能: xiaohongshu-content, xiaohongshu-image-gen, xiaohongshu-proxy-manager, social-media-scheduler

   步骤:
   1. 使用 xiaohongshu-content 生成爆款内容
   2. 使用 xiaohongshu-image-gen 生成配图
   3. 使用 xiaohongshu-proxy-manager 设置代理IP
   4. 使用 social-media-scheduler 排期发布
```

### 指定平台

推荐特定平台的技能组合：

```bash
skill-combo-recommender --task "内容创作" --platform xiaohongshu,wechat
```

### 查看预设工作流

列出所有预设工作流：

```bash
skill-combo-recommender --list-workflows
```

输出示例：
```
🚀 所有预设工作流：

• 小红书运营全流程: 完整的小红书账号运营工作流
  技能: xiaohongshu-content, xiaohongshu-image-gen, xiaohongshu-proxy-manager, social-media-scheduler

• 内容创作流水线: 高效的多平台内容创作工作流
  技能: content-researcher, ai-content-tailor, social-publisher, wechat-formatter

• 视频内容制作: 完整的视频内容制作工作流
  技能: video-generate, video-frames, auto-subtitle, text-to-podcast
...
```

### 使用预设工作流

使用特定的工作流：

```bash
skill-combo-recommender --workflow "小红书运营全流程"
```

### 查看技能库

列出所有可用技能和标签：

```bash
skill-combo-recommender --list-skills
```

### 输出格式

生成 Markdown 或 JSON 格式的输出：

```bash
# Markdown 格式
skill-combo-recommender --task "数据分析" --output markdown

# JSON 格式
skill-combo-recommender --task "数据分析" --output json
```

## 预设工作流

### 小红书运营全流程
适合：小红书账号运营、MCN 机构
- xiaohongshu-content: 生成爆款内容
- xiaohongshu-image-gen: 生成配图
- xiaohongshu-proxy-manager: 设置代理IP
- social-media-scheduler: 排期发布

### 内容创作流水线
适合：内容创作者、自媒体运营
- content-researcher: 调研热门话题
- ai-content-tailor: 裁剪为多平台版本
- wechat-formatter: 格式化公众号版本
- social-publisher: 发布到各平台

### 视频内容制作
适合：视频创作者、短视频制作
- video-generate: 生成视频
- video-frames: 提取关键帧
- auto-subtitle: 生成字幕
- text-to-podcast: 生成音频配音

### 数据分析和可视化
适合：数据分析师、投资者
- tushare-finance: 获取数据
- stock-analyzer: 分析数据
- data-chart-tool: 生成图表

### 文件整理自动化
适合：文件整理、归档
- download-organizer: 整理下载文件夹
- photo-organizer: 整理照片
- file-sorter: 智能分类其他文件

### 会议记录自动化
适合：会议管理、秘书工作
- openai-whisper: 转写录音
- audio-note-taker: 生成结构化纪要
- ai-content-tailor: 裁剪为不同格式

## 技能标签系统

- **内容创作**: xiaohongshu-content, content-researcher, social-publisher, ai-content-tailor, wechat-formatter
- **视频制作**: video-generate, video-frames, auto-subtitle, text-to-podcast
- **数据分析**: stock-analyzer, data-chart-tool, tushare-finance
- **文件管理**: batch-renamer, photo-organizer, download-organizer, video-organizer, music-tagger, file-sorter
- **音频处理**: audio-note-taker, auto-subtitle, text-to-podcast
- **项目管理**: skill-composer, social-media-scheduler, email-ai-assistant
- **AI 工具**: summarize, openai-image-gen, openai-whisper

## 扩展性

### 添加新技能

在 `source/skill_combo_recommender.py` 中的 `SKILLS` 字典添加新技能：

```python
SKILLS = {
    "your-skill-name": {
        "name": "技能名称",
        "description": "技能描述",
        "tags": ["标签1", "标签2"],
        "examples": ["示例1", "示例2"]
    },
    # ...
}
```

### 添加新工作流

在 `WORKFLOWS` 字典添加新工作流：

```python
WORKFLOWS = {
    "your-workflow-key": {
        "name": "工作流名称",
        "description": "工作流描述",
        "skills": ["skill1", "skill2"],
        "steps": ["步骤1", "步骤2"]
    },
    # ...
}
```

## 常见问题

**Q: 推荐的技能我还没有安装怎么办？**

A: 使用 `clawhub install <skill-name>` 安装技能。

**Q: 如何自定义工作流？**

A: 你可以根据推荐的技能，使用 `skill-composer` 编排自定义工作流。

**Q: 推荐的技能组合不准确怎么办？**

A: 请提供更详细的任务描述，或者直接查看 `--list-skills` 和 `--list-workflows` 手动选择。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

---

**作者**: 小叮当 (智脑)
**版本**: 1.0.0
**主页**: https://clawhub.ai/skills/skill-combo-recommender
