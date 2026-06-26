---
name: "infant-cry-analysis"
description: "Detects baby cries via audio AI in real-time, analyzes causes, and precisely identifies needs like hunger, tiredness, pain, discomfort, or irritability to assist new parents. | 婴儿哭声智能解析技能，通过音频AI实时检测婴儿哭声，自动解析哭声成因，精准识别饥饿、困倦、疼痛、身体不适、情绪烦躁等不同需求，辅助新手爸妈科学育婴"
version: "1.0.0"
---

# Smart Baby Cry Analysis Skill | 婴儿哭声智能解析技能

Equipped with an advanced audio AI analysis engine, this feature conducts millisecond-level real-time monitoring and
capture of infant crying. Through deep learning algorithms, the system automatically analyzes the acoustic features of
the cry, precisely distinguishing between specific needs such as hunger, tiredness, pain, physical discomfort, and
emotional distress. This intelligent recognition mechanism helps new parents break through communication barriers and
respond quickly to their baby's true demands, achieving an upgrade in parenting methods from "guessing" to "scientific
response."

本功能搭载先进的音频AI分析引擎，能够对婴儿的哭声进行毫秒级实时监测与捕捉。系统通过深度学习算法，自动解析哭声的声纹特征，精准区分饥饿、困倦、疼痛、身体不适及情绪烦躁等多种具体需求。这一智能化识别机制能帮助新手父母突破沟通壁垒，快速响应宝宝的真实诉求，实现从“猜测”到“科学应对”的育婴方式升级

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过婴儿哭声音频AI分析，自动解析不同哭声成因，帮助家长读懂宝宝需求
- 能力包含：哭声检测、成因分类、需求识别
- **支持识别类型**：
    - 饥饿：饥饿哭闹
    - 困倦：困了闹觉
    - 疼痛：肚子痛/胀气/不舒服
    - 身体不适：发烧/过敏/不舒服
    - 情绪烦躁：需要安抚陪伴
    - 尿布湿了：需要更换
- **特点**：低误报、高响应速度，适合家庭日常育婴看护
- **适用场景**：新手爸妈育婴辅助、夜间哭声自动识别、宝宝需求快速响应
- 触发条件:
    1. **默认触发**：当用户提供婴儿哭声音频/视频需要解析成因时，默认触发本技能
    2. 当用户明确需要婴儿哭声解析、需求识别时，提及哭声解析、宝宝哭了、婴儿哭声、读懂哭声等关键词，并且上传了音频/视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史解析报告、哭声解析报告清单、解析报告列表、查询历史解析、显示所有解析报告、哭声分析报告，查询婴儿哭声智能解析分析报告
- 自动行为：
    1. 如果用户上传了附件或者音频/视频文件，则自动保存到技能目录下 attachments
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有解析报告"、"显示历史解析"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.infant_cry_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 检测要求（获得准确结果的前提）

为了获得准确的哭声解析，请确保：

1. **音频清晰**，尽量减少背景噪音干扰
2. **包含完整哭声片段**，持续时间建议 5-30 秒
3. 如果是视频录制，请确保音频清晰可辨

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行婴儿哭声智能解析分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、babycry123、needfeed456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询解析报告记录），并询问是否继续

---

- 标准流程:
    1. **准备哭声音频/视频输入**
        - 提供本地文件路径或网络 URL
        - 确保哭声清晰，片段完整
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行婴儿哭声智能解析分析**
        - 调用 `-m scripts.infant_cry_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地音频/视频文件路径（使用 multipart/form-data 方式上传）
            - `--url`: 网络音频/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史婴儿哭声智能解析分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的婴儿哭声智能解析分析报告
        - 包含：音频基本信息、识别出的哭声成因、置信度、应对建议

## 资源索引

- 必要脚本：见 [scripts/infant_cry_analysis.py](scripts/infant_cry_analysis.py)(用途：调用 API 进行婴儿哭声智能解析分析，本地文件使用
  multipart/form-data 方式上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp3/wav/mp4/avi/mov，最大 100MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **⚠️ 重要提示**：本分析结果仅供育婴参考辅助，宝宝持续哭闹不适请及时就医检查
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"识别结果"、"置信度"、"解析时间"、"点击查看"五列，其中"报告名称"列使用`婴儿哭声解析报告-{记录id}`形式拼接, "
  点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 识别结果 | 置信度 | 解析时间 | 点击查看 |
  |----------|----------|----------|----------|----------|
  | 婴儿哭声解析报告 -20260329004000001 | 饥饿 | 92% | 2026-03-29 00:
  40 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 解析本地哭声音频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_cry_analysis --input /path/to/cry.mp3 --open-id openclaw-control-ui

# 解析本地视频中的哭声（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_cry_analysis --input /path/to/baby.mp4 --open-id openclaw-control-ui

# 解析网络音频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_cry_analysis --url https://example.com/cry.mp3 --open-id openclaw-control-ui

# 显示历史解析报告/显示解析报告清单列表/显示历史哭声解析（自动触发关键词：查看历史解析报告、历史报告、解析报告清单等）
python -m scripts.infant_cry_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.infant_cry_analysis --input cry.mp3 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.infant_cry_analysis --input cry.mp3 --open-id your-open-id --output result.json
```
