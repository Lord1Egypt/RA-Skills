---
name: "human-emotion-recognition-analysis"
description: "Uses visual AI on frontal faces to recognize multi-dimensional emotions like happiness, sadness, depression, calmness, anger, surprise, and fear in real-time. Supports emotion intensity quantification and abnormal emotion marking, suitable for human-computer interaction and mental health monitoring. | 人体视觉情绪识别技能，基于正面人脸视觉AI实时识别快乐、悲伤、抑郁、平静、愤怒、惊讶、恐惧等多维度情绪状态，支持情绪强度量化与异常情绪标记，适配人机交互、心理健康监测场景"
version: "1.0.4"
license: "MIT-0"
---

# Visual Emotion Recognition Skill | 人体视觉情绪识别技能

Based on frontal face visual AI technology, this capability recognizes multi-dimensional emotional states in real-time,
including happiness, sadness, depression, calmness, anger, surprise, and fear, while supporting emotion intensity
quantification and automatic anomaly marking. By analyzing facial expressions, eye dynamics, and micro-expression
features, the system achieves high-precision affective understanding. It is applicable to scenarios such as emotional
feedback in human-computer interaction and mental health monitoring, assisting in judging changes in user psychological
states and providing data support for intelligent intervention and emotional counseling.

本技能基于正面人脸视觉AI技术，实时识别快乐、悲伤、抑郁、平静、愤怒、惊讶、恐惧等多维度情绪状态，并支持情绪强度量化与异常情绪自动标记。系统通过分析面部表情、眼部动态及微表情特征，实现高精度情感理解。适用于人机交互中的情感反馈、心理健康监测等场景，辅助判断用户心理状态变化，为智能干预与情绪疏导提供数据支撑。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史识别报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过人脸视频/图片进行多维度情绪识别，获取结构化的情绪识别分析报告
- 能力包含：多分类情绪识别、情绪强度量化、异常情绪标记、情绪趋势统计
- 支持识别情绪：快乐、悲伤、抑郁、平静、愤怒、惊讶、恐惧七种基础情绪
- 触发条件:
    1. **默认触发**：当用户提供人脸视频/图片 URL 或文件需要进行情绪识别时，默认触发本技能
    2. 当用户明确需要进行情绪识别、心理健康监测，提及情绪识别、情绪分析、心理健康、压力情绪等关键词，并且上传了视频或图片
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史识别报告、情绪识别报告清单、识别报告列表、查询历史报告、显示所有识别报告、情绪识别历史记录，查询人体情绪识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有识别报告"、"显示所有情绪报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.human_emotion_recognition_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行情绪识别前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、emotion123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询情绪识别报告记录），并询问是否继续

---

- 标准流程:
    1. **准备素材输入**
        - 提供人脸视频文件路径、网络视频 URL 或正面人脸图片
        - 确保人脸清晰完整，正面对准摄像头，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行情绪识别**
        - 调用 `-m scripts.human_emotion_recognition_analysis` 处理素材（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--media-type`: 媒体类型，可选值：video/image，默认 video
            - `--threshold`: 异常情绪强度阈值，高于该分值标记为异常，默认 0.7
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示人体情绪识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的情绪识别报告
        - 包含：基本信息、各情绪概率评分、主导情绪、异常情绪标记、情绪状态提示

## 资源索引

- 必要脚本：见 [scripts/human_emotion_recognition_analysis.py](scripts/human_emotion_recognition_analysis.py)(用途：调用
  API 进行人体情绪识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和媒体格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB
- 本技能仅作情绪状态参考，不能替代专业心理咨询和诊断，发现持续异常情绪请及时寻求专业帮助
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史识别报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"识别时间"、"主导情绪"、"点击查看"四列，其中"报告名称"列使用`人体情绪识别报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 识别时间 | 主导情绪 | 点击查看 |
  |----------|----------|----------|----------|
  | 人体情绪识别报告-20260312172200001 | 2026-03-12 17:22:00 | 平静 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 识别本地人脸视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.human_emotion_recognition_analysis --input /path/to/face_video.mp4 --media-type video --open-id openclaw-control-ui

# 识别本地人脸照片，设置异常阈值（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.human_emotion_recognition_analysis --input /path/to/face.jpg --media-type image --threshold 0.65 --open-id openclaw-control-ui

# 识别网络视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.human_emotion_recognition_analysis --url https://example.com/face_video.mp4 --media-type video --open-id openclaw-control-ui

# 显示历史识别报告/显示识别报告清单列表/显示历史情绪报告（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.human_emotion_recognition_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.human_emotion_recognition_analysis --input video.mp4 --media-type video --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.human_emotion_recognition_analysis --input video.mp4 --media-type video --open-id your-open-id --output result.json
```
