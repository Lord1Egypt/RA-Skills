---
name: "pet-detection-feeder-analysis"
description: "Based on computer vision, automatically detects and recognizes cats and dogs appearing in the target area from the perspective of feeder/IPC cameras, and supports pet identity recognition and database entry, suitable for pet identification management in smart feeding scenarios. | 智能喂食器宠物检测识别技能，基于计算机视觉从喂食器/IPC摄像头视角自动检测识别目标区域出现的猫、狗宠物，并支持宠物身份识别和底库录入，适用于智能喂养场景的宠物识别管理"
version: "1.0.2"
---

# Smart Feeder Pet Detection & Recognition Skill | 智能喂食器宠物检测识别技能

Based on advanced computer vision and deep learning technologies, this feature automatically detects and identifies pets
such as cats and dogs within a target area from the specific perspective of smart feeders or IPC cameras. The system not
only supports high-precision breed determination but also possesses powerful individual identity recognition
capabilities, allowing users to establish a dedicated database of pet facial or body features. In smart feeding
scenarios, this function accurately distinguishes between different individuals in multi-pet households, enabling
personalized "recognition-based feeding" services. This effectively prevents non-target pets from stealing food,
providing reliable technical support for scientific pet ownership and refined health management.

本功能基于先进的计算机视觉与深度学习技术，能够从智能喂食器或IPC摄像头的特定视角出发，自动检测并识别目标区域内出现的猫、狗等宠物。系统不仅支持对宠物品种的高精度判定，更具备强大的个体身份识别能力，支持用户建立专属的宠物面部或体态特征底库。在智能喂养场景中，该功能能够精准区分多宠家庭中的不同个体，实现“认宠下粮”的个性化服务，有效防止非目标宠物抢食，为科学养宠与精细化健康管理提供可靠的技术支撑

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史检测报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过喂食器/IPC摄像头视角的视频/图片进行宠物检测识别，获取结构化的宠物识别分析报告
- 能力包含：宠物检测识别、猫/狗分类、宠物身份识别、宠物底库录入、历史检测记录查询
- 触发条件:
    1. **默认触发**：当用户提供喂食器/IPC摄像头视角的视频/图片 URL 或文件需要进行宠物检测时，默认触发本技能
    2. 当用户明确需要进行宠物检测、宠物身份识别、喂食器宠物识别、IPC摄像头宠物监测、宠物底库录入时，提及宠物检测、喂食器识别、宠物身份、底库录入等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史检测报告、宠物检测报告清单、检测报告列表、查询历史报告、显示所有检测报告、宠物识别历史记录，查询宠物检测分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有检测报告"、"
       显示所有宠物检测报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.pet_detection_feeder_analysis --list --open-id` 参数调用 API
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

**在执行宠物检测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、petFeeder123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询宠物检测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备媒体输入**
        - 提供喂食器视角本地视频/图片文件路径或网络视频/图片 URL
        - 确保画面清晰展示喂食区域，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行宠物检测分析/底库录入**
        - 调用 `-m scripts.pet_detection_feeder_analysis` 处理媒体文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--media-type`: 媒体类型，可选值：video/image，默认 video
            - `--pet-type`: 宠物类型，可选值：cat/dog，默认 cat
            - `--pet-id`: 宠物ID/名称，用于底库录入（必填项，录入时必须提供）
            - `--action`: 操作类型，可选值：detect/enroll，默认 detect（detect=检测识别，enroll=底库录入）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示宠物检测历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 检测识别：接收结构化的宠物识别报告，包含：宠物基本信息、宠物类型、身份识别结果、置信度、出现次数统计
        - 底库录入：接收录入结果反馈，确认宠物信息已存入底库

## 资源索引

- 必要脚本：见 [scripts/pet_detection_feeder_analysis.py](scripts/pet_detection_feeder_analysis.py)(用途：调用 API
  进行宠物检测识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和媒体格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB
- 适用于喂食器、IPC摄像头等固定视角场景，检测准确率更高
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供智能喂养参考，不能替代人工确认
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史检测报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"媒体类型"、"检测时间"、"点击查看"四列，其中"报告名称"列使用`宠物喂食器检测分析报告-{记录id}`形式拼接, "
  点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 媒体类型 | 检测时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物喂食器检测分析报告-20260312172200001 | 视频 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 检测本地视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_detection_feeder_analysis --input /path/to/video.mp4 --media-type video --pet-type cat --open-id openclaw-control-ui

# 检测网络视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_detection_feeder_analysis --url https://example.com/video.mp4 --media-type video --pet-type cat --open-id openclaw-control-ui

# 检测本地图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_detection_feeder_analysis --input /path/to/image.jpg --media-type image --pet-type dog --open-id openclaw-control-ui

# 宠物底库录入（将猫咪橘橘录入到底库，OpenClaw UI 上下文）
python -m scripts.pet_detection_feeder_analysis --input /path/to/juju.jpg --media-type image --pet-type cat --pet-id 橘橘 --action enroll --open-id openclaw-control-ui

# 显示历史检测报告/显示检测报告清单列表/显示历史宠物检测报告（自动触发关键词：查看历史检测报告、历史报告、检测报告清单等）
python -m scripts.pet_detection_feeder_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.pet_detection_feeder_analysis --input video.mp4 --media-type video --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.pet_detection_feeder_analysis --input video.mp4 --media-type video --pet-type cat --open-id your-open-id --output result.json
```
