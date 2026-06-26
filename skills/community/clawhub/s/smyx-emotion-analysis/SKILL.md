---
name: "emotion-analysis"
description: "Professional discernment of subtle cues! It performs detailed analysis and recognition of facial micro-expressions, outputs precise emotional state reports, and unveils true inner emotional activities. | 微观情绪（微表情）识别分析工具，专业察言观色！针对人物面部微表情进行细致分析识别，输出精准的情绪状态分析报告，揭示真实内心情绪活动"
version: "1.0.1"
---

# Micro-Expression Recognition & Analysis Tool | 微观情绪识别分析工具

This tool is a professional emotion analysis system based on cutting-edge computer vision and psychological
micro-expression theory. It captures facial features with millimeter-level precision and deeply analyzes fleeting,
subtle muscle changes. By accurately identifying basic emotions—such as surprise, fear, anger, and joy—as well as
complex psychological states, the system generates a detailed emotional state analysis report. Designed to penetrate
linguistic and superficial disguises, it objectively reveals an individual's true inner emotional fluctuations,
providing scientific and quantifiable data support for psychological assessment, human-computer interaction, and
behavioral analysis.

本工具是一款基于前沿计算机视觉与心理学微表情理论的专业情绪分析系统，能够对人物面部进行毫米级特征捕捉，深度解析转瞬即逝的细微肌肉变化。通过对惊讶、恐惧、愤怒、愉悦等基础情绪及复杂心理状态的精准识别，系统将生成一份详尽的情绪状态分析报告，旨在穿透语言与表层的伪装，客观揭示个体最真实的内心情感波动，为心理评估、人机交互及行为分析提供科学、量化的数据支撑。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过视频分析对人物面部微表情进行精准识别，获取结构化的真实情绪状态分析报告
- 能力包含：视频分析、基础情绪识别、复合情绪识别、微表情捕捉、真实情绪揭示、情绪波动分析、人际交往情绪建议
- 触发条件:
    1. **默认触发**：当用户提供需要分析的人物面部视频 URL 或文件需要进行微表情情绪分析时，默认触发本技能
    2. 当用户明确需要进行微表情分析、情绪识别、察言观色、真实情绪探测时，提及情绪分析、微表情、表情识别、察言观色、真实情绪等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史情绪报告、微表情分析报告清单、情绪分析列表、显示所有情绪报告，查询微表情情绪分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有情绪报告"、"
       显示所有微表情分析报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.emotion_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 微表情情绪识别分析维度

本技能重点识别分析以下面部微观情绪表现维度：

### 1. **基础情绪识别**

基于面部动作编码系统（FACS）识别七种基础情绪：

- **开心/愉悦**：眼角鱼尾纹、嘴角上扬、面颊抬起
    - 轻微愉悦：礼貌性微笑，肌肉轻微收缩
    - 中度愉悦：自然开心笑，双眼弯起
    - 重度愉悦：开怀大笑，面部肌肉充分舒展

- **悲伤/难过**：嘴角下拉、眉头紧皱、眼睑下垂
    - 轻微悲伤：神情黯淡，嘴角微微下沉
    - 中度悲伤：眼眶湿润，眉头紧锁
    - 重度悲伤：哭泣抽搐，面部肌肉颤抖

- **愤怒/生气**：眉毛下压、眼睛瞪大、嘴唇紧闭
    - 轻微愤怒：不满表情，神情严肃
    - 中度愤怒：怒目相对，鼻翼扩张
    - 重度愤怒：面部紧绷，青筋暴起

- **惊讶/震惊**：眉毛上抬、眼睛睁大、嘴巴张开
    - 轻微惊讶：轻度挑眉，嘴唇微张
    - 中度惊讶：明显吃惊，眼睛圆睁
    - 重度惊讶：极度震惊，嘴巴大张

- **恐惧/害怕**：眉毛上抬并聚拢、眼睛睁大、嘴部拉伸
    - 轻微恐惧：紧张不安，神情警惕
    - 中度恐惧：明显害怕，身体后仰
    - 重度恐惧：极度惊恐，面部僵硬

- **厌恶/反感**：眉毛下压、上嘴唇抬起、鼻翼皱起
    - 轻微厌恶：不屑表情，轻微撇嘴
    - 中度厌恶：明显排斥，鼻子皱起
    - 重度厌恶：极度反感，扭头回避

- **惊讶/好奇**：眉毛微抬、目光聚焦、神情关注
    - 轻微好奇：轻度关注，眼神好奇
    - 中度好奇：明显感兴趣，身体前倾
    - 重度好奇：极度关注，全神贯注

### 2. **复合情绪与微表情捕捉**

- **真实情绪伪装识别**：识别语言与表情不一致，捕捉一闪而过的真实微表情
- **情绪波动分析**：追踪情绪变化过程，识别情绪起伏波动
- **压抑情绪识别**：识别被刻意压抑的真实情绪，从细微肌肉变化中发现线索
- **矛盾情绪识别**：同时存在多种情绪，分析主次情绪关系

### 3. **面部肌肉细节分析**

- **眼部区域**：瞳孔缩放、眨眼频率、眉毛位置变化、眼睑开合程度
- **嘴部区域**：嘴角微扬/下沉、嘴唇紧绷程度、咬肌紧张度
- **鼻部区域**：鼻翼扩张/收缩、鼻梁皱纹变化
- **面颊区域**：面颊抬起/下垂、肌肉紧张程度

### 4. **情绪可信度评估**

- 表情一致性评估：言语表达 vs 微表情表现一致性打分
- 情绪真实度打分：0-100分，分数越低说明情绪掩饰可能性越高
- 关键微表情线索：列出最能反映真实情绪的微表情关键点

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行微表情情绪分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、emoC113、emo123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询微表情情绪分析报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - **关键要求**：视频必须清晰展示人物面部，光线充足，面部无遮挡（口罩、墨镜、帽子会影响分析精度）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行微表情情绪分析**
        - 调用 `-m scripts.emotion_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--analysis-type`: 分析类型，可选值：comprehensive/basic/micro/trust/other，默认 comprehensive（综合分析）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示微表情情绪分析历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的微表情情绪分析报告
        - 包含：整体情绪状态、基础情绪识别、微表情关键线索、真实情绪揭示、情绪真实度打分、人际交往建议

## 资源索引

- 必要脚本：见 [scripts/emotion_analysis.py](scripts/emotion_analysis.py)(用途：调用 API 进行微表情情绪分析，本地文件上传，网络
  URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- **专业说明**：本分析基于计算机视觉微表情识别技术，仅供参考交流使用。微表情识别不能替代专业心理测谎或心理咨询。
- **精度提示**：分析精度受视频质量、面部遮挡、光线条件等因素影响，结果仅供参考
- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- **面部要求**：建议正面清晰拍摄，面部无遮挡，光线均匀，这样能获得最佳分析效果
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`微表情情绪分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 微表情情绪分析报告-20260312172200001 | 综合分析 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 综合微表情情绪分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.emotion_analysis --input /path/to/face_video.mp4 --analysis-type comprehensive --open-id openclaw-control-ui

# 基础情绪识别专项（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.emotion_analysis --url https://example.com/face_video.mp4 --analysis-type basic --open-id openclaw-control-ui

# 微表情捕捉专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.emotion_analysis --input /path/to/micro_video.mp4 --analysis-type micro --open-id openclaw-control-ui

# 情绪可信度评估（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.emotion_analysis --input /path/to/trust_video.mp4 --analysis-type trust --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史情绪报告（自动触发关键词：查看历史情绪报告、历史报告、情绪报告清单等）
python -m scripts.emotion_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.emotion_analysis --input video.mp4 --analysis-type comprehensive --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.emotion_analysis --input video.mp4 --analysis-type comprehensive --open-id your-open-id --output result.json
```
