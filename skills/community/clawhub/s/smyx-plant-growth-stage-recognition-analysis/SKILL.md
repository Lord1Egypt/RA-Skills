---
name: "plant-growth-stage-recognition-analysis"
description: "Accurately identifies key growth stages of plants from germination to fruiting based on computer vision and deep learning, provides structured data for precision agriculture decision support. | 植物生长阶段识别技能，基于计算机视觉与深度学习算法，精准识别植物从发芽到结果的全生命周期关键生长阶段，为精准农业提供科学决策支持"
version: "1.0.2"
---

# Plant Growth Stage Recognition Skill | 植物生长阶段识别技能

Equipped with advanced computer vision and deep learning algorithms trained on large-scale plant growth datasets, this
skill accurately identifies key growth stages throughout the entire plant life cycle, including germination, seedling,
vegetative growth, flowering, and fruiting. By analyzing morphological characteristics of the plant, leaf area index,
and reproductive organ development status, the system automatically determines the current growth stage and outputs
structured analysis results. It provides scientific basis and decision support for water and fertilizer management, pest
and disease control, and yield prediction in precision agriculture, helping agricultural producers achieve scientific
management and improve crop yield and quality.

本技能搭载了基于大规模植物生长数据集训练的先进计算机视觉与深度学习算法，能够精准识别植物从发芽、幼苗、营养生长、开花到结果全生命周期中的各个关键生长阶段。系统通过分析植株形态特征、叶面积指数以及生殖器官发育状况，自动判断当前生长状态并输出结构化分析数据，为精准农业中的水肥管理、病虫害防治及产量预估提供科学依据与决策支持，帮助农业生产者实现科学管理，提升作物产量与品质。

## 演示案例

- [🔗 通过网路视频进行识别分析](https://www.coze.cn/s/EGesE1qiHM8/)
- [🔗 通过上传视频进行识别分析](https://www.coze.cn/s/CiyhsWLkihc/)
- [🔗 显示历史分析报告](https://www.coze.cn/s/MJ-xy1q_M7w/)

## 任务目标

- 本 Skill 用于：识别视频/图片中的植物，准确判断其所处的生长阶段，输出结构化生长状态分析数据
- 能力包含：植株检测、生长阶段分类、关键发育特征分析、结构化数据输出
- 支持场景：
    - **精准农业**：大田作物生长监测，指导适时水肥管理
    - **设施园艺**：温室大棚作物生长状态智能判断
    - **农业科研**：作物育种试验生长数据自动化采集
    - **智慧种植**：无人农场生长阶段自动识别与决策
- 触发条件:
    1. **默认触发**：当用户提供植物植株视频/图片需要识别生长阶段时，默认触发本技能
    2. 当用户明确需要植物生长阶段识别、生育期判断时，提及生长阶段识别、生育期识别、发芽阶段、开花结果、生长状态识别等关键词，并且上传了视频/图片，自动触发本技能
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史识别报告、生长阶段识别报告清单、识别报告列表、查询历史识别报告、显示所有识别报告、植物生长阶段分析报告，查询植物生长阶段识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有识别报告"、"
       显示所有植物生长阶段识别"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.plant_growth_stage_recognition_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 识别要求（获得准确结果的前提）

为了获得准确的生长阶段识别，请确保：

1. **植株主体完整**，整株或主要生长部位完整出镜，避免过度遮挡
2. **光线充足清晰**，避免过度模糊、过暗过曝和严重色差
3. 对于田间群体拍摄，尽量聚焦单株主要特征便于分析

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行植物生长阶段识别分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 2 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、plant123、id456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析

---

- 标准流程:
    1. **准备植物视频/图片输入**
        - 提供本地视频/图片文件路径或网络 URL
        - 确保植株主体完整，特征清晰，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行植物生长阶段识别分析**
        - 调用 `-m scripts.plant_growth_stage_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取, 再通过 SHA-256 算法生成唯一标识传入）
            - `--list`: 显示历史植物生长阶段识别分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的植物生长阶段识别分析报告
        - 包含：输入基本信息、检测到的植株数量、判定生长阶段、关键发育特征、置信度、农事管理建议

## 资源索引

- 必要脚本：见 [scripts/plant_growth_stage_recognition_analysis.py](scripts/plant_growth_stage_recognition_analysis.py)
  (用途：调用 API 进行植物生长阶段识别分析，本地文件上传(https)，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png，最大 20MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供农业生产参考，具体农事决策请结合实际经验和专业指导
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"植株数量"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`植物生长阶段识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 植株数量 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 植物生长阶段识别报告-20260414232000001 | 1株 | 2026-04-14 23:20:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

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
# 识别本地视频/图片中植物的生长阶段（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.plant_growth_stage_recognition_analysis --input /path/to/plant.mp4 --open-id {SHA-256 算法生成新 open-id}

# 识别网络视频/图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.plant_growth_stage_recognition_analysis --url https://example.com/crop.mp4 --open-id {SHA-256 算法生成新 open-id}

# 显示历史识别报告/显示识别报告清单列表/显示历史植物生长阶段识别（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.plant_growth_stage_recognition_analysis --list --open-id {SHA-256 算法生成新 open-id}

# 输出精简报告
python -m scripts.plant_growth_stage_recognition_analysis --input crop.jpg --open-id {SHA-256 算法生成新 open-id} --detail basic

# 保存结果到文件
python -m scripts.plant_growth_stage_recognition_analysis --input crop.jpg --open-id {SHA-256 算法生成新 open-id} --output result.json
```
