---
name: "smyx-pet-toy-interaction-activity-analysis"
description: "Triggers when a user provides a pet toy area video URL or file for analysis; supports local video uploads or network URLs to call server-side APIs for toy interaction behavior recognition, tracking interaction frequency, duration, and toy preference per pet, generating daily activity curves and trend comparisons to detect declining activity that may indicate illness or depression. Application scenarios: smart pet toys, pet wellness monitoring. | 当用户提供玩具区域视频URL或文件时，触发本技能进行互动行为分析；支持通过上传本地视频或网络视频URL，调用服务端API进行玩具互动识别，记录宠物与各类玩具互动频次、时长、偏好，生成活跃度曲线，活跃度下降提示疾病或抑郁风险。应用场景：智能宠物玩具、宠物健康管理。"
version: "1.0.0"
---

# Pet Toy Interaction Activity Analysis | 宠物玩具互动活跃度分析

Triggers when a user provides a pet toy area video URL or file for analysis; supports local video uploads or network
URLs to call server-side APIs for toy interaction behavior recognition, tracking interaction frequency, duration, and
toy preference per pet, generating daily activity curves and trend comparisons to detect declining activity that may
indicate illness or depression. Application scenarios: smart pet toys, pet wellness monitoring.

当用户提供玩具区域视频URL或文件时，触发本技能进行互动行为分析；支持通过上传本地视频或网络视频URL，调用服务端API进行玩具互动识别，记录宠物与各类玩具互动频次、时长、偏好，生成活跃度曲线，活跃度下降提示疾病或抑郁风险。应用场景：智能宠物玩具、宠物健康管理。

## 🎯 AI 角色

假设你是一个专业的宠物行为分析AI。你的任务是基于玩具区域（或多个玩具区域）的连续视频，检测宠物与玩具之间的互动行为，量化互动频次、持续时间和偏好，输出每日活跃度曲线及变化趋势。不要提供疾病诊断或情绪诊断，仅客观描述行为数据。

## 任务目标

- 本 Skill 用于：通过玩具区域视频进行宠物互动活跃度分析，获取标准化的互动统计结果和活跃度趋势
- 能力包含：视频分析、互动行为检测、互动频次统计、互动时长测量、玩具偏好排序、每日活跃度曲线、历史趋势对比、活跃度骤降预警
- 触发条件:
    1. **默认触发**：当用户提供宠物玩具区域视频 URL 或文件需要分析时，默认触发本技能进行互动活跃度分析
    2. 当用户明确需要进行互动活跃度监测时，提及宠物玩具、互动频次、玩耍时长、玩具偏好、活跃度下降、宠物抑郁、不爱玩了、互动减少等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史互动报告、历史玩具互动报告、活跃度分析报告清单、互动报告清单、查询历史活跃度报告、显示所有互动报告、显示活跃度监测报告，查询健康风险提示报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有互动报告"、"
       显示所有活跃度报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_toy_interaction_activity_analysis --list --open-id` 参数调用 API
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

**在执行互动活跃度分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示玩具区域及宠物互动行为，光线充足，无遮挡
        - 建议视频覆盖较长时段（如2-4小时），以获取完整的互动行为样本
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行互动活跃度分析**
        - 调用 `-m scripts.smyx_pet_toy_interaction_activity_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/bird/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示玩具互动历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的互动活跃度观察报告
        -
       包含：互动频次统计（各类型玩具的互动次数）、互动时长分布（单次时长均值、最长/最短互动）、玩具偏好排序（按互动总时长或次数排名）、每日活跃度曲线（按时段统计的互动密度）、历史趋势对比（与近7天/30天基线对比）、活跃度异常预警（互动骤降提示可能不适或抑郁倾向）
        - **重要提示**：仅客观描述观察到的行为数据变化，不提供疾病诊断或情绪诊断

## 📊 分析指标说明

| 指标     | 说明                  | 预警参考                                       |
|--------|---------------------|--------------------------------------------|
| 互动频次   | 宠物当日与各类玩具互动的总次数     | 猫：正常6-15次/天；狗：正常8-20次/天                    |
| 互动时长   | 每次互动的持续秒数及当日总互动时长   | 猫：单次5-120秒，日总15-60分钟；狗：单次10-300秒，日总30-90分钟 |
| 玩具偏好   | 按互动总时长/次数对各玩具排序     | 偏好突然改变可能值得关注                               |
| 活跃度曲线  | 按时段（每2小时）统计互动密度的日曲线 | 正常猫：晨昏双峰；正常狗：白天分散                          |
| 历史基线对比 | 与近7天/30天的日均值对比      | 骤降>40%触发预警                                 |
| 活跃度骤降  | 日互动总时长/频次明显低于历史基线   | 可能提示身体不适、疼痛或情绪低落                           |

## 🧸 互动行为定义

| 行为类型 | 识别标准                            |
|------|---------------------------------|
| 主动追逐 | 宠物主动跑向/追击移动玩具                   |
| 扑咬抓挠 | 用嘴咬、用爪抓挠玩具                      |
| 拨弄推滚 | 用爪拨弄、推动球类/滚筒玩具                  |
| 抱持蹭磨 | 抱住玩具蹭头、身体摩擦                     |
| 叼取放置 | 叼起玩具并移动到其他位置                    |
| 观察注视 | 对玩具保持关注但未接触（不单独计入互动频次，但影响活跃度评分） |

## 资源索引

-

必要脚本：见 [scripts/smyx_pet_toy_interaction_activity_analysis.py](scripts/smyx_pet_toy_interaction_activity_analysis.py)(
用途：调用 API 进行互动活跃度分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供行为参考，不提供疾病诊断或情绪诊断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 活跃度评估基于视频可观察到的互动行为，无法识别静卧、睡眠等非互动状态
- 多宠家庭需确保视频能区分不同个体的互动行为，建议配合宠物个体识别技能使用
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`玩具互动活跃度分析报告-{记录id}`
  形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 玩具互动活跃度分析报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地玩具区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_toy_interaction_activity_analysis --input /path/to/toy_area_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络玩具区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_toy_interaction_activity_analysis --url https://example.com/toy_area_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史互动报告（自动触发关键词：查看历史互动报告、历史报告、互动报告清单等）
python -m scripts.smyx_pet_toy_interaction_activity_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_toy_interaction_activity_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_toy_interaction_activity_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
