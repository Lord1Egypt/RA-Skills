---
name: "pet-body-health-analysis"
description: "Identifies obesity, emaciation, external injuries, skin abnormalities, and abnormal mental states, helping pet owners detect health issues promptly. | 宠物体态健康分析技能，识别肥胖、消瘦、外伤、皮肤异常、精神状态异常，帮助宠物主人及时发现宠物健康问题"
version: "1.0.4"
license: "MIT-0"
---

# Pet Body Condition & Health Analysis Skill | 宠物体态健康分析技能

Based on advanced computer vision and behavior analysis technologies, this feature conducts multi-dimensional
intelligent monitoring of pets' body posture, skin condition, and mental state. The system precisely identifies body
changes such as obesity and emaciation, automatically detects skin abnormalities like trauma, swelling, and hair loss,
and analyzes activity levels and behavioral patterns to determine if the mental state is abnormal. This feature helps
pet owners break through the barriers of professional knowledge, promptly identify potential health risks, and provide
reliable data support for scientific pet ownership and early intervention.

本功能基于先进的计算机视觉与行为分析技术，对宠物的体态特征、皮肤状况及精神面貌进行多维度智能监测。系统能够精准识别肥胖与消瘦等体态变化，自动检测外伤、红肿、脱毛等皮肤异常，并通过对活动量与行为模式的分析判断精神状态是否异常。这一功能帮助宠物主人突破专业知识的壁垒，及时发现潜在的健康风险，为科学养宠与早期干预提供可靠的数据支持

## 任务目标

- 本 Skill 用于：通过视频/图片对宠物进行体态健康分析，识别常见体态异常和健康问题，输出结构化的宠物体态健康分析报告
- 能力包含：
    - 体态识别：肥胖、消瘦
    - 体表识别：外伤、皮肤异常（脱毛、红疹、肿块等）
    - 精神状态：活跃度异常判断
- 触发条件:
    1. **默认触发**：当用户提供宠物视频/图片 URL 或文件需要进行宠物体态健康分析时，默认触发本技能
    2. 当用户明确需要进行宠物体态分析，提及肥胖、消瘦、皮肤异常、外伤检查、体态健康等关键词，并且上传了视频或图片
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史分析报告、宠物体态分析报告清单、分析报告列表、查询历史报告、显示所有体态分析报告、宠物体态健康分析历史记录
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有体态分析报告"、"
       显示所有宠物体态报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.pet_body_health_analysis --list --open-id` 参数调用 API
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

**在执行宠物体态健康分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 2 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、petbody123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析

---

- 标准流程:
    1. **准备媒体输入**
        - 提供宠物全身视频/清晰照片，最好覆盖全身和异常部位
        - 确保光线充足，宠物体态清晰可见
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行宠物体态健康分析**
        - 调用 `-m scripts.pet_body_health_analysis` 处理素材（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--media-type`: 媒体类型，可选值：video/image，默认 video
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示宠物体态健康分析历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的宠物体态健康分析报告
        - 包含：体态评估、皮肤状况、精神状态、异常提示建议

## 资源索引

- 必要脚本：见 [scripts/pet_body_health_analysis.py](scripts/pet_body_health_analysis.py)(用途：调用 API
  进行宠物体态健康分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和媒体格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供健康参考，不能替代专业兽医诊断，发现异常请及时就医
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析时间"、"宠物昵称"、"点击查看"四列，其中"报告名称"列使用`宠物体态健康分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 宠物昵称 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物体态健康分析报告-20260312172200001 | 2026-03-12 17:22:00 |
  咪咪 | [🔗 查看报告](https://example.com/report?id=xxx) |

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
# 分析本地宠物视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_body_health_analysis --input /path/to/pet_video.mp4 --media-type video --open-id your-open-id

# 分析宠物照片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_body_health_analysis --input /path/to/pet.jpg --media-type image --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史宠物体态报告（自动触发关键词：查看历史分析报告、历史报告、分析报告清单等）
python -m scripts.pet_body_health_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.pet_body_health_analysis --input pet_video.mp4 --media-type video --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.pet_body_health_analysis --input pet.jpg --media-type image --open-id your-open-id --output result.json
```
