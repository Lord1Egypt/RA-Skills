---
name: "smyx-vocal-emotion-classification-analysis"
description: "Triggers when a user provides a pet vocalization audio/video URL or file for analysis; extracts acoustic features such as frequency, duration, interval, and harmonic structure via AI audio analysis, and classifies the vocalization into 6+ emotion categories (howling, growling, excitement, loneliness, fear, whining/coaxing) with confidence scores. Helps owners understand pet emotional states, improve human-pet interaction, and detect potential stress or health issues early. Application: daily companionship (smart camera / collar), boarding center mood monitoring, vet clinic calming assessment, behavior training assistance. Does NOT provide medical or behavior-modification advice — only outputs audio-based emotion classification results with confidence. | 当用户提供宠物（犬/猫）叫声音频或视频URL/文件时，触发本技能进行叫声情绪深度分类分析；利用AI音频分析技术提取频率、时长、间隔、谐波结构等声学特征，将叫声分类为哀嚎、低吼、兴奋、孤独、恐惧、撒娇等6种以上情绪类别，并输出置信度；帮助宠物主人理解宠物情绪状态，改善人宠互动，及时发现潜在压力或健康问题。应用场景：宠物家庭日常陪伴（智能摄像头/项圈）、寄养中心情绪监测、宠物医院安抚评估、行为训练辅助。仅输出基于音频的情绪分类结果及置信度，不提供医疗或行为矫正建议。"
version: "1.0.0"
---

# Pet Vocal Emotion Deep Classification | 宠物叫声情绪深度分类

Triggers when a user provides a pet vocalization audio/video URL or file for analysis; extracts acoustic features such as frequency, duration, interval, and harmonic structure via AI audio analysis, and classifies the vocalization into 6+ emotion categories (howling, growling, excitement, loneliness, fear, whining/coaxing) with confidence scores. Helps owners understand pet emotional states, improve human-pet interaction, and detect potential stress or health issues early. Application: daily companionship (smart camera / collar), boarding center mood monitoring, vet clinic calming assessment, behavior training assistance. Does NOT provide medical or behavior-modification advice — only outputs audio-based emotion classification results with confidence.

当用户提供宠物（犬/猫）叫声音频或视频URL/文件时，触发本技能进行叫声情绪深度分类分析；利用AI音频分析技术提取频率、时长、间隔、谐波结构等声学特征，将叫声分类为哀嚎、低吼、兴奋、孤独、恐惧、撒娇等6种以上情绪类别，并输出置信度；帮助宠物主人理解宠物情绪状态，改善人宠互动，及时发现潜在压力或健康问题。应用场景：宠物家庭日常陪伴（智能摄像头/项圈）、寄养中心情绪监测、宠物医院安抚评估、行为训练辅助。仅输出基于音频的情绪分类结果及置信度，不提供医疗或行为矫正建议。


## 🎯 AI 角色

**你是一个专业的宠物行为与情绪分析AI。你的任务是分析宠物（犬或猫）的叫声音频片段，提取声学特征（频率、时长、间隔、谐波结构等），并将其分类为多种预设的情绪类别。不要提供医疗或行为矫正建议，仅输出基于音频的情绪分类结果及置信度。**

## 任务目标

- 本 Skill 用于：通过宠物（犬/猫）叫声音频/视频片段进行情绪深度分类，获取标准化的情绪标签和置信度分布
- 能力包含：音频降噪与切片、声学特征提取（基频/能量/时长/间隔/谐波）、情绪分类（哀嚎、低吼、兴奋、孤独、恐惧、撒娇等≥6类）、置信度计算、长期情绪趋势提示
- 触发条件:
    1. **默认触发**：当用户提供宠物叫声音频或包含叫声的视频 URL/文件需要分析时，默认触发本技能进行情绪分类
    2. 当用户明确需要理解宠物情绪时，提及狗叫、猫叫、宠物叫声、情绪识别、情绪分类、低吼、撒娇、哀嚎、宠物焦虑/兴奋等关键词，并且上传了音频或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史叫声情绪报告、历史情绪分析、叫声分类报告清单、查询情绪历史报告、显示所有情绪分类报告
- 自动行为：
    1. 如果用户上传了附件或者音频/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有情绪报告"、"显示历史叫声分析"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_vocal_emotion_classification_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行叫声情绪分类分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：skills/smyx_common/scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/skills/smyx_common/scripts/config.yaml
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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备音频/视频输入**
        - 提供本地音频/视频文件路径或网络 URL
        - 确保叫声片段清晰可辨，背景噪音较少，时长建议 1～30 秒
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行叫声情绪分类**
        - 调用 `-m scripts.smyx_vocal_emotion_classification_analysis` 处理音频/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地音频/视频文件路径
            - `--url`: 网络音频/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示叫声情绪历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的情绪分类报告
        - 包含：主情绪标签（哀嚎/低吼/兴奋/孤独/恐惧/撒娇等）、置信度（0-1）、Top-3 情绪分布、声学特征摘要（基频Hz、时长ms、能量、谐波丰富度）、片段时间戳、潜在状态提示
        - **重要提示**：仅输出基于音频的情绪分类客观结果，不提供医疗诊断或行为矫正建议

## 资源索引

- 必要脚本：见 [scripts/smyx_vocal_emotion_classification_analysis.py](scripts/smyx_vocal_emotion_classification_analysis.py)（用途：调用 API 进行叫声情绪深度分类，本地文件上传，网络 URL 由 API 服务自动下载）
- 配置文件：见 [scripts/config.py](scripts/config.py)（用途：配置 API 地址、默认参数和媒体格式限制）
- 领域参考：见 [references/api_doc.md](references/api_doc.md)（何时读取：需要了解 API 接口详细规范和错误码时）

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp3/wav/m4a 音频或 mp4/avi/mov 视频格式，最大 10MB
- 推荐音频时长 1～30 秒；过短/过长可能影响分类置信度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅作情绪参考，不提供医疗、训练或行为矫正建议
- 若叫声混杂多种情绪或背景噪声过大，可能返回 "low_confidence"
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物叫声情绪分类报告-{记录id}`形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物叫声情绪分类报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物叫声音频/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_vocal_emotion_classification_analysis --input /path/to/pet_bark.mp3 --pet-type dog --open-id your-open-id

# 分析网络宠物叫声音频/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_vocal_emotion_classification_analysis --url https://example.com/pet_bark.mp4 --pet-type dog --open-id your-open-id

# 显示历史分析报告/情绪分类历史清单（自动触发关键词：查看历史叫声情绪报告等）
python -m scripts.smyx_vocal_emotion_classification_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_vocal_emotion_classification_analysis --input bark.mp3 --pet-type dog --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_vocal_emotion_classification_analysis --input bark.mp3 --pet-type dog --open-id your-open-id --output result.json
```
