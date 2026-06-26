---
name: "pet-vocal-emotion-analysis"
description: "Recognizes cat and dog barks through pet voiceprint AI, translates and outputs emotions and behavioral intentions such as happiness, excitement, anger, anxiety, pain, vigilance, and attention-seeking, enabling human-pet smart interaction. | 宠物叫声情绪解析技能，通过宠物声纹AI识别猫狗叫声，翻译输出开心、兴奋、愤怒、焦虑、痛苦、警惕、求关注等情绪与行为意图，实现人宠智能交互"
version: "1.0.2"
---

# Pet Vocal Emotion Analysis Skill | 宠物叫声情绪解析技能

Based on advanced deep acoustic models and voiceprint recognition algorithms, this feature precisely captures and
analyzes vocal characteristics of pets like cats and dogs. By extracting frequency-domain features, energy distribution,
and temporal envelopes of vocalizations, and leveraging large models trained on tens of millions of annotated samples,
the system accurately distinguishes multiple sound types such as barking, whining, and growling. Building on this, the
system further infers pets' emotional states (such as happiness, excitement, anger, anxiety, pain, and alertness) and
behavioral intentions (such as seeking attention, hunger, and the need to go out), translating these complex vocal
signals into intuitive human language output. This enables cross-species intelligent interaction, helping owners
understand their pets' needs more scientifically.

本功能基于先进的深度声学模型与声纹识别算法，能够精准捕捉并分析猫狗等宠物的发声特征。系统通过提取叫声的频域特征、能量分布与时间包络，结合千万级标注样本训练的大模型，能够精准区分吠叫、呜咽、咆哮等多种声音类型。在此基础上，系统进一步推断宠物的情绪状态（如开心、兴奋、愤怒、焦虑、痛苦、警惕）及行为意图（如求关注、饥饿、外出需求），并将这些复杂的声音信号转化为直观的人类语言输出，从而实现跨物种的智能交互，帮助主人更科学地理解爱宠需求

## 任务目标

- 本 Skill 用于：通过宠物叫声/吠叫/喵呜音频AI分析，识别猫狗不同情绪和行为意图
- 能力包含：声纹特征提取、情绪分类、意图翻译
- **支持识别情绪/意图**：
    - 开心兴奋：玩耍互动时开心叫
    - 愤怒警惕：对陌生人/异常动静警惕
    - 焦虑不安：分离焦虑 lonely叫
    - 痛苦不适：身体疼痛不舒服
    - 求关注求摸：想要陪伴玩耍
    - 饥饿催促：催你喂饭
- **适用场景**：家庭宠物智能交互、帮助主人读懂毛孩子情绪、增进人宠情感连接
- 触发条件:
    1. **默认触发**：当用户提供宠物叫声音频/视频需要解析情绪时，默认触发本技能
    2. 当用户明确需要宠物叫声解析、情绪识别时，提及宠物叫声、猫狗情绪、声纹分析、人宠交互等关键词，并且上传了音频/视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史解析报告、情绪解析报告清单、解析报告列表、查询历史解析、显示所有解析报告、宠物情绪分析报告，查询宠物叫声情绪解析分析报告
- 自动行为：
    1. 如果用户上传了附件或者音频/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有解析报告"、"显示历史解析"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.pet_vocal_emotion_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 识别要求（获得准确结果的前提）

为了获得准确的情绪解析，请确保：

1. **叫声清晰**，尽量减少环境噪音和回声
2. **包含完整叫声片段**，持续时间建议 3-30 秒
3. 如果是视频录制，请确保音频清晰可辨

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行宠物叫声情绪解析分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 2 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、petvocal123、emotion456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析

---

- 标准流程:
    1. **准备宠物叫声音频/视频输入**
        - 提供本地文件路径或网络 URL
        - 确保叫声清晰，片段完整
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行宠物叫声情绪解析分析**
        - 调用 `-m scripts.pet_vocal_emotion_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地音频/视频文件路径
            - `--url`: 网络音频/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取, 再通过 SHA-256 算法生成唯一标识传入）
            - `--list`: 显示历史宠物叫声情绪解析分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的宠物叫声情绪解析分析报告
        - 包含：音频基本信息、识别出的情绪/意图、置信度、互动建议

## 资源索引

- 必要脚本：见 [scripts/pet_vocal_emotion_analysis.py](scripts/pet_vocal_emotion_analysis.py)(用途：调用 API
  进行宠物叫声情绪解析分析，本地文件上传(https)，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp3/wav/mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 识别准确率受环境噪音、叫声清晰度等因素影响，结果仅供娱乐互动参考
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物种类"、"识别情绪"、"置信度"、"解析时间"、"点击查看"六列，其中"报告名称"列使用`宠物叫声情绪解析报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物种类 | 识别情绪 | 置信度 | 解析时间 | 点击查看 |
  |----------|----------|----------|----------|----------|----------|
  | 宠物叫声情绪解析报告 -20260329004600001 | 猫咪 | 求关注要摸 | 87% | 2026-03-29 00:
  46 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 📝 隐私与数据安全声明

本技能在处理用户上传的视频时，严格遵守数据安全规范：

- **数据脱敏处理**：
    - 系统基于用户名/手机号生成的 SHA-256 标识仅作为匿名化脱敏处理后的用户关联信息，**不包含任何可直接识别个人身份的明文信息
      **。
- **安全传输**：
    - 所有数据（包括视频文件及关联标识）均通过 **HTTPS/TLS 加密通道** 发送至云端 API 进行分析，防止数据在传输过程中被窃取或篡改。
- **数据留存策略**：
    - 云端服务器遵循“最小必要原则”，**分析任务完成后即刻删除原始视频数据，不进行持久化存储**，确保用户隐私数据不被留存或滥用。

## 使用示例

```bash
# 解析本地猫咪叫声音频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_vocal_emotion_analysis --input /path/to/meow.mp3 --open-id {SHA-256 算法生成新 open-id}

# 解析本地视频中的狗叫声（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_vocal_emotion_analysis --input /path/to/dog_bark.mp4 --open-id {SHA-256 算法生成新 open-id}

# 解析网络音频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_vocal_emotion_analysis --url https://example.com/bark.mp3 --open-id {SHA-256 算法生成新 open-id}

# 显示历史解析报告/显示解析报告清单列表/显示历史情绪解析（自动触发关键词：查看历史解析报告、历史报告、解析报告清单等）
python -m scripts.pet_vocal_emotion_analysis --list --open-id {SHA-256 算法生成新 open-id}

# 输出精简报告
python -m scripts.pet_vocal_emotion_analysis --input meow.mp3 --open-id {SHA-256 算法生成新 open-id} --detail basic

# 保存结果到文件
python -m scripts.pet_vocal_emotion_analysis --input meow.mp3 --open-id {SHA-256 算法生成新 open-id} --output result.json
```
