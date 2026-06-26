---
name: skill-combo-recommender
description: Recommend skill combinations and workflows based on user tasks and goals. Use when: (1) user asks "what skills should I use for X?", (2) user wants to optimize their workflow, (3) user is unsure how to combine skills for a project. Provides intelligent recommendations with usage examples.
---

# Skill Combo Recommender

智能推荐技能组合，帮助用户找到最佳工作流程。

## 核心功能

1. **任务分析**：根据用户描述的任务，分析需要的技能
2. **技能组合推荐**：推荐最佳技能组合和工作流程
3. **使用示例**：提供具体的使用示例和命令
4. **预设工作流**：提供常见场景的预设工作流（小红书运营、内容创作、视频制作等）

## 使用场景

**场景 1：小红书运营**
用户想要运营小红书账号
- 推荐技能：xiaohongshu-content + xiaohongshu-image-gen + xiaohongshu-proxy-manager + social-media-scheduler
- 工作流程：内容创作 → 图片生成 → 发布排期
- 使用示例：
  ```bash
  # 1. 生成爆款内容
  xiaohongshu-content --category 家装 --style 种草
  
  # 2. 生成配图
  xiaohongshu-image-gen --prompt 现代简约风格客厅设计
  
  # 3. 设置排期发布
  social-media-scheduler --platform xiaohongshu --schedule "2026-03-20 10:00"
  ```

**场景 2：内容创作流水线**
用户想要高效创作多平台内容
- 推荐技能：content-researcher + social-publisher + ai-content-tailor + wechat-formatter
- 工作流程：内容调研 → 内容裁剪 → 格式化 → 多平台发布
- 使用示例：
  ```bash
  # 1. 调研热门话题
  content-researcher --topic 人工智能 --days 7
  
  # 2. 裁剪为多平台版本
  ai-content-tailor --input article.md --platforms xiaohongshu,zhihu,wechat
  
  # 3. 发布到多平台
  social-publisher --input xiaohongshu.md --platform xiaohongshu
  ```

**场景 3：视频内容制作**
用户想要制作视频内容
- 推荐技能：video-frames + auto-subtitle + video-generate + text-to-podcast
- 工作流程：视频生成 → 提取帧 → 生成字幕 → 音频配音
- 使用示例：
  ```bash
  # 1. 生成视频
  video-generate --prompt AI助手介绍 --duration 15s
  
  # 2. 生成字幕
  auto-subtitle --input video.mp4 --language zh-CN
  
  # 3. 文本转音频
  text-to-podcast --input script.txt --voice male
  ```

**场景 4：数据分析和可视化**
用户想要分析数据并生成图表
- 推荐技能：stock-analyzer + data-chart-tool + tushare-finance
- 工作流程：数据获取 → 数据分析 → 图表生成
- 使用示例：
  ```bash
  # 1. 获取股票数据
  tushare-finance --code 000001 --period daily
  
  # 2. 分析股票
  stock-analyzer --symbol 000001 --indicators MA,RSI,MACD
  
  # 3. 生成图表
  data-chart-tool --input data.csv --type line --title 股票走势
  ```

## 核心逻辑

### 技能标签系统

每个技能都有标签，用于匹配用户需求：

**内容创作**：xiaohongshu-content, content-researcher, social-publisher, ai-content-tailor, wechat-formatter
**视频制作**：video-generate, video-frames, auto-subtitle, text-to-podcast
**数据分析**：stock-analyzer, data-chart-tool, tushare-finance
**文件管理**：batch-renamer, photo-organizer, download-organizer, video-organizer, music-tagger, file-sorter
**音频处理**：audio-note-taker, auto-subtitle, text-to-podcast
**项目管理**：skill-composer, social-media-scheduler, email-ai-assistant
**AI 工具**：summarize, openai-image-gen, openai-whisper

### 推荐算法

1. **关键词匹配**：根据用户描述的关键词匹配技能标签
2. **权重排序**：根据匹配度排序推荐技能
3. **工作流生成**：将推荐技能组织成工作流程
4. **示例生成**：为每个推荐技能提供使用示例

### 预设工作流

**小红书运营全流程**：
- 技能：xiaohongshu-content + xiaohongshu-image-gen + xiaohongshu-proxy-manager + social-media-scheduler
- 步骤：1. 生成爆款内容 → 2. 生成配图 → 3. 设置代理 → 4. 排期发布

**内容创作流水线**：
- 技能：content-researcher + social-publisher + ai-content-tailor + wechat-formatter
- 步骤：1. 调研热门话题 → 2. 裁剪内容 → 3. 格式化 → 4. 多平台发布

**视频内容制作**：
- 技能：video-generate + video-frames + auto-subtitle + text-to-podcast
- 步骤：1. 生成视频 → 2. 提取帧 → 3. 生成字幕 → 4. 音频配音

**数据分析和可视化**：
- 技能：stock-analyzer + data-chart-tool + tushare-finance
- 步骤：1. 获取数据 → 2. 分析数据 → 3. 生成图表

## CLI 命令

```bash
# 基础用法：根据任务描述推荐技能
skill-combo-recommender --task "我想运营小红书账号"

# 指定平台：推荐特定平台的技能组合
skill-combo-recommender --task "内容创作" --platform xiaohongshu,wechat

# 查看预设工作流：列出所有预设工作流
skill-combo-recommender --list-workflows

# 使用预设工作流：使用特定的工作流
skill-combo-recommender --workflow "小红书运营全流程"

# 查看技能库：列出所有可用技能和标签
skill-combo-recommender --list-skills

# 生成文档：生成推荐的工作流文档
skill-combo-recommender --task "内容创作" --output markdown
```

## 扩展性

### 添加新技能

在 `source/skill_database.py` 中添加新技能：

```python
skills = {
    "skill-name": {
        "name": "技能名称",
        "description": "技能描述",
        "tags": ["标签1", "标签2"],
        "examples": ["示例1", "示例2"]
    },
    # ... 添加更多技能
}
```

### 添加新工作流

在 `source/workflow_database.py` 中添加新工作流：

```python
workflows = {
    "workflow-name": {
        "name": "工作流名称",
        "description": "工作流描述",
        "skills": ["skill1", "skill2", "skill3"],
        "steps": ["步骤1", "步骤2", "步骤3"]
    },
    # ... 添加更多工作流
}
```

## 优化方向

1. **学习用户行为**：记录用户选择的工作流，优化推荐算法
2. **个性化推荐**：根据用户历史使用记录，提供个性化推荐
3. **工作流模板**：提供更多预设工作流模板
4. **集成 skill-composer**：直接生成 skill-composer 配置文件
