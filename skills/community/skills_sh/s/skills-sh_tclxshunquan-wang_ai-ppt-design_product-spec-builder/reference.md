# Google AI Studio 能力清单

本文档列出了 Google AI Studio Builder 支持的主要 AI 能力，用于在生成 Product Spec 时匹配合适的能力。

## 图像相关能力

### 图像生成
- **图像生成（Image Generation）**：根据文本描述生成图像
- **图像编辑（Image Editing）**：修改、增强或编辑现有图像
- **图像风格转换（Style Transfer）**：将图像转换为不同艺术风格

### 图像理解
- **图像识别（Image Recognition）**：识别图像中的对象、场景、人物
- **OCR（光学字符识别）**：从图像中提取文字
- **图像标注（Image Captioning）**：为图像生成文字描述
- **图像分类（Image Classification）**：对图像进行分类

## 视频相关能力

### 视频生成
- **视频生成（Video Generation）**：根据文本或图像生成视频
- **视频编辑（Video Editing）**：剪辑、拼接、添加特效

### 视频理解
- **视频分析（Video Analysis）**：分析视频内容、场景、动作
- **视频摘要（Video Summarization）**：生成视频摘要或关键帧提取
- **视频字幕生成（Video Captioning）**：为视频生成字幕

## 语音相关能力

### 语音生成
- **文本转语音（TTS）**：将文本转换为自然语音
- **语音克隆（Voice Cloning）**：复制特定声音特征

### 语音理解
- **语音转文本（STT）**：将语音转换为文字
- **语音识别（Speech Recognition）**：识别说话人、情感、语言
- **语音命令识别（Voice Commands）**：识别和执行语音指令

## 智能增强能力

### 内容生成
- **文本生成（Text Generation）**：生成文章、摘要、翻译等
- **代码生成（Code Generation）**：根据描述生成代码
- **创意写作（Creative Writing）**：生成创意内容、故事、诗歌

### 内容优化
- **文本优化（Text Optimization）**：优化文本的可读性、风格、语气
- **内容改写（Content Rewriting）**：改写文本保持原意
- **语法检查（Grammar Checking）**：检查并修正语法错误

### 智能推荐
- **个性化推荐（Personalized Recommendations）**：基于用户行为推荐内容
- **智能建议（Smart Suggestions）**：提供上下文相关的建议
- **内容推荐（Content Recommendations）**：推荐相关内容或选项

### 数据分析
- **数据提取（Data Extraction）**：从非结构化数据中提取信息
- **数据分析（Data Analysis）**：分析数据并生成洞察
- **数据可视化建议（Visualization Suggestions）**：建议合适的数据可视化方式

## 数据连接能力

### 外部数据源
- **API 集成（API Integration）**：连接外部 API 获取数据
- **数据库连接（Database Connection）**：连接数据库查询数据
- **文件处理（File Processing）**：处理各种格式的文件（PDF、Excel、Word等）

### 实时数据
- **实时数据流（Real-time Data Streams）**：处理实时数据流
- **数据同步（Data Synchronization）**：同步多个数据源

## 使用建议

1. **图像处理需求** → 优先考虑图像相关能力
2. **视频内容需求** → 优先考虑视频相关能力
3. **语音交互需求** → 优先考虑语音相关能力
4. **内容生成/优化需求** → 优先考虑智能增强能力
5. **需要外部数据** → 考虑数据连接能力

## 能力组合

多个能力可以组合使用：
- **图像生成 + 图像编辑**：生成后进一步编辑
- **语音转文本 + 文本生成**：语音输入，生成内容
- **数据提取 + 数据分析**：提取数据后进行分析
- **文本生成 + 文本优化**：生成后优化内容
