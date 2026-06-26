# Vision Skill

Vision Skill 是专为 AI Agent（如 Trae, Claude, OpenClaw 等）设计的视觉能力扩展插件。它赋予纯文本模型强大的**视觉理解（Recognition）**和**图像生成（Generation）**能力，通过集成豆包大模型（Doubao Vision & Image Models）和腾讯云 COS，实现高效、异步、高质量的视觉任务处理。

## 🌟 项目亮点

*   **最新模型支持**：深度集成豆包视觉大模型（`doubao-seed-2-0-pro-260215`）和图像生成模型（`doubao-seedream-5-0-260128`），效果拔群。
*   **全能视觉识别**：支持 OCR 文字提取、场景描述、细节问答，准确率极高。
*   **全场景图像生成**：
    *   **文生图（Text-to-Image）**：精准理解 Prompt 生成高质量图像。
    *   **图生图（Image-to-Image）**：基于参考图进行风格迁移或细节修改。
    *   **文生图组（Sequential Generation）**：支持生成连贯的故事插画或分镜。
    *   **图生图组（Image-to-Images）**：基于参考图生成多张变体。
*   **场景化预置 (Presets)**：内置 `ppt`, `business_flat`, `tech_isometric`, `hand_drawn` 等生成风格，以及 `invoice`, `contract`, `form`, `slide`, `whiteboard`, `table`, `json` 等识别输出格式，让 Agent 调用更智能。
*   **批处理与稳定性增强**：支持一次识别多张图片，内置失败重试、可选降级模型，面对网络抖动和接口波动更稳定。
*   **自动化云存储**：内置腾讯云 COS 客户端，自动将本地文件流转为云端 URL，Agent 无需操心文件上传问题。
*   **可观测任务元数据**：任务状态中包含 `started_at / ended_at / duration_ms / api_attempts` 等字段，便于排障和监控。
*   **灵活的任务架构**：既支持**异步轮询**（适合批量大任务），也支持**同步等待**（适合即时反馈），满足不同 Agent 的工作流需求。

## 💡 核心价值

AI Agent 通常受限于纯文本交互或有限的多模态窗口。Vision Skill 解决了以下核心痛点：

1.  **打破模态壁垒**：让 Agent 能“看”懂本地文件，能“画”出创意想法。
2.  **专业能力外挂**：相比通用模型，Skill 封装了特定的 Prompt 优化和参数调优（如连贯性生成配置）。
3.  **流程自动化**：从本地图片 -> 上传云端 -> 识别/生成 -> 结果回传/保存，全流程自动化，Agent 只需调用一条指令。

## 🚀 使用场景

*   **UI/UX 设计辅助**：上传草图，生成高保真渲染图；或者根据现有 UI 生成变体。
*   **文档数字化**：批量识别发票、海报、文档中的文字并结构化输出为 JSON 或 Markdown 表格。
*   **内容创作**：为文章自动配图，或制作连贯的故事绘本（使用 `cartoon` 风格预置）。
*   **数据分析**：识别图表内容，转换为 Excel 或 Markdown 表格数据。
*   **无障碍辅助**：为视障用户生成图片的详细描述。

## 🔄 工作流 (Workflow)

Vision Skill 采用**异步任务**模式，确保 Agent 在处理耗时生成任务时不会超时。

1.  **提交任务 (Submit)**：Agent 调用 CLI（如 `vision_cli.py recognize` 或 `generate`）。
2.  **预处理 (Pre-process)**：
    *   若是本地图片，自动上传至腾讯云 COS 获取 URL。
    *   构建符合豆包 API 规范的请求体。
3.  **异步执行 (Async Execution)**：
    *   Worker 进程后台启动，调用豆包大模型 API。
    *   CLI 立即返回 `task_id` 和 `status: pending`。
4.  **状态轮询 (Polling)**：
    *   Agent 使用 `vision_cli.py status <task_id>` 查询进度。
5.  **结果处理 (Result)**：
    *   任务完成后，返回 JSON 格式的识别文本或生成图片的 URL。

## 🛠️ 安装与使用

### 1. 极速安装

```bash
# 克隆仓库
git clone https://github.com/lgwanai/vision-skill.git
cd vision-skill

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

复制配置文件并填入密钥：

```bash
cp .env.example .env
```

在 `.env` 中填入你的腾讯云和豆包 API 密钥：
```ini
# Tencent Cloud COS
COS_SECRET_ID=your_id
COS_SECRET_KEY=your_key
COS_REGION=ap-beijing
COS_BUCKET_NAME=your_bucket

# Doubao API
DOUBAO_API_KEY=your_key
# 模型名称通常无需修改，除非有新版本
DOUBAO_VISION_MODEL=doubao-seed-2-0-pro-260215
DOUBAO_IMAGE_MODEL=doubao-seedream-5-0-260128
```

### 3. IDE 集成 (Trae / Cursor / Claude)

将 `dist/vision-skill.skill` (或者整个项目目录) 作为 MCP 工具或自定义 Skill 导入到你的 Agent 配置中。
*   **Trae/Claude Desktop**: 在设置中添加本地 Skill 路径。
*   **OpenClaw**: 将 `scripts/vision_cli.py` 注册为 Tool。

### 4. 命令行使用指南

#### 👁️ 视觉识别
```bash
# 基础用法：识别本地图片
python3 scripts/vision_cli.py recognize ./photo.jpg --prompt "提取图中的文字"

# 进阶用法：使用预置格式 (--format)
# 可选格式：invoice, contract, form, slide, whiteboard, table, json, key_value, markdown_note, qa_pairs, code, ocr, analysis
python3 scripts/vision_cli.py recognize ./invoice.jpg --format json

# 批量识别（多图输入）
python3 scripts/vision_cli.py recognize ./a.jpg ./b.jpg ./c.jpg --format table --wait --output ./batch_result.json

# 质量模式与重试
python3 scripts/vision_cli.py recognize ./doc.jpg --format contract --quality high --retry 3 --wait

# 同步等待并保存结果 (--wait --output)
python3 scripts/vision_cli.py recognize ./doc.jpg --format ocr --wait --output ./result.txt
```

#### 🎨 图像生成
```bash
# 基础用法：文生图
python3 scripts/vision_cli.py generate "一只赛博朋克风格的猫"

# 进阶用法：使用预置风格 (--style)
# 可选风格：ppt, business_flat, cartoon, tech_isometric, hand_drawn, icon, photo, anime, sketch
python3 scripts/vision_cli.py generate "团队协作开会" --style ppt

# 图生图 (指定参考图)
python3 scripts/vision_cli.py generate "变成素描风格" --ref ./cat.jpg

# 连续生成 (生成4张连贯图)
python3 scripts/vision_cli.py generate "四季变化的树" --seq 4 --style cartoon

# 同步等待并保存图片
python3 scripts/vision_cli.py generate "相机App图标" --style icon --wait --output ./icon.png

# 质量模式与重试
python3 scripts/vision_cli.py generate "企业级数据平台架构插图" --style tech_isometric --quality high --retry 3 --wait
```

#### 🔍 查询结果
```bash
python3 scripts/vision_cli.py status <task_id>

# 如果任务已完成，直接保存结果
python3 scripts/vision_cli.py status <task_id> --output ./final_result.png
```

## ❓ 常见问题 (FAQ)

**Q: 需要 GPU 吗？**
A: 不需要。所有计算都在豆包云端大模型上完成，本地只需能运行 Python 即可。

**Q: 图片上传到哪里了？安全吗？**
A: 图片上传到你配置的腾讯云 COS 存储桶中。请确保你的 COS Bucket 权限配置正确（建议私有读写或限制来源），Skill 仅生成临时访问链接给大模型。

**Q: 为什么识别结果有延迟？**
A: 视觉大模型处理需要时间，尤其是高清图片分析或批量生成任务。通常识别在 3-5秒，生成在 10-30秒左右。建议使用 `--wait` 参数让脚本自动等待。

**Q: 支持哪些图片格式？**
A: 支持 JPG, PNG, WEBP 等常见格式。文件大小建议不超过 10MB。

**Q: 如何获取豆包 API Key？**
A: 请访问 [火山引擎控制台](https://console.volcengine.com/) 开通豆包大模型服务并创建 API Key。
