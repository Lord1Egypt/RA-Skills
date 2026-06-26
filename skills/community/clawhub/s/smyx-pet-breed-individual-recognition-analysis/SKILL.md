---
name: "pet-breed-individual-recognition-analysis"
description: "Accurately identifies cat and dog breeds and supports distinguishing between different individuals in multi-pet households; an essential assistant for intelligent pet butlers. | 宠物品种个体识别技能，精准识别猫狗宠物品种，支持多宠家庭区分不同独立个体，智能宠物管家好帮手"
version: "1.0.4"
license: "MIT-0"
---

# Pet Breed & Individual Identification Skill | 宠物品种个体识别技能

Equipped with high-precision breed recognition algorithms based on Deep Convolutional Neural Networks (DCNN), this
feature delivers millisecond-level accurate identification of breed characteristics for common pets like cats and dogs.
The system not only encompasses a database of hundreds of mainstream and rare breeds globally but is also deeply
optimized for multi-pet household scenarios. It supports simultaneous recognition and differentiation of distinct pet
individuals within the same frame. By establishing independent pet identity profiles, the system accurately records the
activity trajectories and behavioral habits of each pet, effectively resolving identity confusion in multi-pet
environments. It provides personalized intelligent management services for pet owners, serving as an indispensable
smart管家 assistant for modern multi-pet families.

本功能搭载了基于深度卷积神经网络的高精度品种识别算法，能够对猫、狗等常见宠物的品种特征进行毫秒级精准判定。系统不仅涵盖了全球数百种主流及稀有品种的数据库，更针对多宠家庭场景进行了深度优化，支持在同一画面中同时识别并区分不同的宠物个体。通过建立独立的宠物身份档案，系统能够准确记录每只宠物的活动轨迹与行为习惯，有效解决多宠环境下的身份混淆问题，为宠物主人提供个性化的智能管理服务，是现代化多宠家庭不可或缺的智能管家助手

## 任务目标

- 本 Skill 用于：识别图片/视频中的宠物，准确判断猫狗品种，支持多宠家庭区分不同独立个体
- 能力包含：宠物检测、品种分类、个体识别、多目标区分
- 支持场景：
    - **品种识别**：精准识别上百种猫狗品种
    - **个体区分**：多宠家庭能分辨出"这只是谁""那只是谁"
    - **智能管家**：配合家庭监控自动记录宠物活动
- 触发条件:
    1. **默认触发**：当用户提供宠物图片/视频需要识别品种/个体时，默认触发本技能
    2. 当用户明确需要宠物识别、品种鉴定时，提及宠物品种识别、猫咪品种、狗狗品种、区分宠物、个体识别等关键词，并且上传了图片/视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史识别报告、宠物识别报告清单、识别报告列表、查询历史识别报告、显示所有识别报告、宠物品种分析报告，查询宠物品种个体识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者图片/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有识别报告"、"显示所有宠物识别"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.pet_breed_individual_recognition_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 识别要求（获得准确结果的前提）

为了获得准确的品种/个体识别，请确保：

1. **宠物完整出镜**，避免过度遮挡
2. **光线充足清晰**，避免过度模糊和暗角
3. 多宠同框时尽量保持宠物间距适中，便于分别识别个体

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行宠物品种个体识别分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 2 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、petbreed123、petid456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析

---

- 标准流程:
    1. **准备宠物图片/视频输入**
        - 提供本地图片/视频文件路径或网络 URL
        - 确保宠物完整出镜，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行宠物品种个体识别分析**
        - 调用 `-m scripts.pet_breed_individual_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图片/视频文件路径
            - `--url`: 网络图片/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史宠物品种个体识别分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的宠物品种个体识别分析报告
        - 包含：输入基本信息、检测到的宠物数量、每个宠物的品种判定、个体区分结果、置信度、趣味备注

## 资源索引

-

必要脚本：见 [scripts/pet_breed_individual_recognition_analysis.py](scripts/pet_breed_individual_recognition_analysis.py)(
用途：调用 API 进行宠物品种个体识别分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供宠物爱好参考，纯种鉴定请以专业机构结果为准
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物数量"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物品种个体识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物数量 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物品种个体识别报告 -20260328221000001 | 2只 | 2026-03-28 22:10:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 📝 隐私与数据安全声明

本技能在处理用户上传的视频时，严格遵守数据安全规范：

- **数据保密处理**：
    - 系统基于 用户名/手机号 生成的标识仅作为用户关联信息，**不保存任何可直接识别个人身份的明文信息**。
- **安全传输**：
    - 所有数据（包括视频文件及关联标识）均通过 **HTTPS/TLS 加密通道** 发送至云端 API 进行分析，防止数据在传输过程中被窃取或篡改。
- **数据留存策略**：
    - 云端服务器遵循“最小必要原则”，**分析任务完成后即刻删除原始视频数据，不进行持久化存储**，确保用户隐私数据不被留存或滥用。

## 使用示例

```bash
# 识别本地图片中的宠物（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_breed_individual_recognition_analysis --input /path/to/pets.jpg --open-id your-open-id

# 识别网络图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_breed_individual_recognition_analysis --url https://example.com/dogs.jpg --open-id your-open-id

# 显示历史识别报告/显示识别报告清单列表/显示历史宠物识别（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.pet_breed_individual_recognition_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.pet_breed_individual_recognition_analysis --input pets.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.pet_breed_individual_recognition_analysis --input pets.jpg --open-id your-open-id --output result.json
```
