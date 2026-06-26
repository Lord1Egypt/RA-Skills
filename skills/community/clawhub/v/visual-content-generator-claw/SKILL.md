---
name: visual-content-generator-claw
description: |
  AI驱动的视觉素材快速生成专家。用于生成海报、社交媒体配图、视频封面、数字人背景等视觉内容。
  触发场景：用户说"生成图片"、"做海报"、"配图"、"封面"、"数字人"、"视觉素材"、"设计"、"出图"、"AI绘画"、"背景图"时使用。
  支持自然语言输入（"帮我做一张科技感海报"）和结构化JSON输入。
  核心能力：Prompt工程优化 → AI模型调用 → 后期处理 → 输出到本地/飞书云盘。
---

# 视觉素材美工虾

AI驱动的视觉素材快速生成专家，10分钟内生成海报、配图、数字人画面。

## 工作流程

### 步骤 1：需求解析

从用户输入中提取：
- **用途**：海报 / 配图 / 封面 / 背景
- **尺寸**：参考 `references/platform-size-guide.md` 确定平台规范尺寸
- **风格**：科技感 / 小清新 / 商务 / 国潮 / 极简
- **核心元素**：人物 / 场景 / 物品 / 氛围
- **文字内容**：标题 / 副标题 / 装饰文字

### 步骤 2：Prompt 工程优化

将需求转换为高质量 AI 绘画提示词，参考 `references/prompt-templates.md` 中的模板：
- 主体描述（详细且具体）
- 风格关键词
- 画质增强词：`high quality, detailed, 8K, professional`
- 负面提示词：`blurry, low quality, distorted text, watermark`
- 构图建议

### 步骤 3：AI 模型调用

使用 `scripts/generate-image.py` 生成图片：

```bash
# 单张生成
python3 scripts/generate-image.py --prompt "<优化后的prompt>" --size 1080x1080

# 批量生成（4张备选）
python3 scripts/generate-image.py --prompt "<prompt>" --size 1080x1920 --count 4

# 使用预设模板
python3 scripts/generate-image.py --template poster-tech --title "标题文字"
```

**模型优先级**（按可用性选择）：
1. 本地 Stable Diffusion（隐私优先）
2. DALL-E 3（写实场景）
3. 文心一格（中文内容友好）
4. Midjourney API（高质量商业图）

### 步骤 4：后期处理

脚本自动完成：尺寸裁剪、文字叠加、色彩调整、压缩优化。

### 步骤 5：输出

- 保存到本地工作目录（`~/.openclaw/workspace/`）
- 可选：上传飞书云盘（用 `feishu_drive_file` action=upload）
- 通过 `MEDIA:./文件名.png` 发送给用户

## 参考资料

- **视觉风格规范**：`references/visual-style-guide.md` — 品牌色、字体、风格标签
- **Prompt 模板库**：`references/prompt-templates.md` — 海报/配图/封面/数字人背景模板
- **平台尺寸规范**：`references/platform-size-guide.md` — 各平台图片尺寸要求

## 注意事项

- AI 生成文字容易变形，精确文字排版建议人工辅助
- 商用图片注意版权，优先使用本地模型
- 本地部署需要 GPU（推荐 NVIDIA RTX 3060+）
