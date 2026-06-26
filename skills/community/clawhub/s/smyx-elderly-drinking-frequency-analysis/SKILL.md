---
name: "smyx-elderly-drinking-frequency-analysis"
description: "Using a fixed camera in the living room or kitchen, the system analyzes video of the water-cup placement area (e.g., coffee table, dining table), detects hand-to-cup contact actions (pickup, putdown), and counts daily cup-pickup events (an indirect proxy for water intake). | 通过客厅或厨房固定摄像头，分析水杯放置区域（如茶几、餐桌）的视频，检测手部与水杯的接触动作（拿起、放下），统计每日水杯拿起次数（间接反映饮水量）。当每日拿起次数低于预设阈值（如每天少于6次）时，输出'脱水风险'提醒，建议家属或护理人员督促老人增加饮水。"
version: "1.0.2"
license: "MIT-0"
---

# Elderly Drinking-Cup Pickup Frequency (Dehydration Risk) | 老年人饮水杯拿起频率（脱水风险）

Using a fixed camera in the living room or kitchen, the system analyzes video of the water-cup placement area (e.g., coffee table, dining table), detects hand-to-cup contact actions (pickup, putdown), and counts daily cup-pickup events (an indirect proxy for water intake). When the daily pickup count falls below a preset threshold (e.g., fewer than 6 times per day), it outputs a 'dehydration risk' alert and suggests family members or caregivers to encourage the elderly to drink more. The skill helps prevent dehydration, urinary tract infection and cognitive decline caused by insufficient water intake. Application scenarios: homes of elderly people living alone, nursing homes, daycare centers. The system generates a daily drinking report; when the count is insufficient, it pushes a mobile-app reminder. Skill features: elderly people often have a dulled thirst sensation and are prone to chronic dehydration, leading to constipation, urinary tract infection, cognitive issues, etc. AI auto-counting of cup pickups helps family members spot insufficient intake in time and intervene. Can be integrated into home-care cameras or community health-management platforms as a practical feature for elderly health protection.

通过客厅或厨房固定摄像头，分析水杯放置区域（如茶几、餐桌）的视频，检测手部与水杯的接触动作（拿起、放下），统计每日水杯拿起次数（间接反映饮水量）。当每日拿起次数低于预设阈值（如每天少于6次）时，输出'脱水风险'提醒，建议家属或护理人员督促老人增加饮水。该技能有助于预防因饮水不足导致的脱水、泌尿系感染及认知功能下降。应用场景：独居老人家庭、养老院、日间照料中心。系统每日生成饮水统计报告，当次数不足时通过手机APP推送提醒。技能特点：老年人对口渴感知迟钝，易发生慢性脱水，导致便秘、尿路感染、认知障碍等问题。通过AI自动统计饮水杯拿起次数，可帮助家属及时发现饮水不足，采取干预措施。该技能可集成到居家养老摄像头或社区健康管理平台中，成为老年人健康守护的实用功能。

## 🎯 AI 角色

**假设你是一个专业的老年人健康护理 AI。你的任务是分析固定摄像头对准水杯区域的视频，检测手部与水杯的接触动作（拿起和放下），统计每天的水杯拿起次数。当次数低于预设阈值时，输出脱水风险提醒。不要提供医疗诊断，仅输出基于视觉的饮水行为统计与方向性提醒。**

## 任务目标

- 本 Skill 用于：基于客厅/厨房固定摄像头视频，检测手-杯接触事件 + 抬手到口部动作 → 统计当日拿起次数与饮水频率 → 对比个人基线 → 输出脱水风险提醒（供家属/护理员主动督促老人饮水）
- 能力包含：人体检测、手部检测、杯子检测、水杯放置 ROI 定义、手-杯接触事件识别（拿起/放下）、伴随饮水手势识别（抬手到口部）、当日拿起次数与时段分布统计、相邻饮水间隔、长时间未饮水检测（默认 > 4 小时）、个人历史基线统计、风险类型分类（low_daily_intake / long_no_drink_interval / below_personal_baseline / normal）、家属/护理员提醒文本生成
- 触发条件:
    1. **默认触发**：当用户提供客厅/厨房水杯区域视频 URL 或文件需要分析时，默认触发本技能进行饮水频率（脱水风险）分析
    2. 当用户明确提及老人饮水、脱水风险、慢性脱水、便秘、尿路感染、认知障碍预警、独居老人健康、督促饮水、养老护理等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看老人饮水历史报告、脱水风险报告清单、饮水频率报告清单、查询历史饮水记录、显示所有老人饮水报告、显示养老护理诊断报告，查询脱水风险预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有老人饮水报告"、"
       显示所有脱水风险报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_drinking_frequency_analysis --list --open-id` 参数调用 API
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

**在执行老年人饮水频率（脱水风险）分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备客厅/厨房水杯区域视频输入**
        - 提供本地视频路径或网络 URL，建议覆盖一整天（08:00-22:00）或多段拼接覆盖白天
        - 摄像头建议：客厅/厨房/卧室固定摄像头，**画面应稳定覆盖老人常放水杯的区域（茶几/餐桌/床头柜）**
        - 帧率 ≥ 5 FPS、分辨率 ≥ 480p、光照稳定；隐私敏感场景可启用人体轮廓模式
        - 初次部署可在画面中**框选水杯放置区域 ROI（cup_region）**，提升识别准确度
        - 可选附带：老人姓名、年龄、近期身体状况、阈值覆盖（daily_pickup_threshold / no_drink_interval_hours）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老年人饮水频率（脱水风险）分析**
        - 调用 `-m scripts.smyx_elderly_drinking_frequency_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地客厅/厨房水杯区域视频文件路径
            - `--url`: 网络客厅/厨房水杯区域视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老年人健康护理场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老年人饮水频率（脱水风险）历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的老年人饮水频率（脱水风险）分析报告
        - 包含：是否检测到老人（subject_detected）、水杯区域/杯子可见性（cup_region_defined / cup_visible）、当日指标（daily_metrics：cup_pickup_count_daily / drink_gesture_count_daily / interval_between_drinks_min / last_pickup_time）、历史基线（baseline_metrics：baseline_daily_pickup_avg / baseline_daily_pickup_std）、风险类型（risk_type：low_daily_intake / long_no_drink_interval / below_personal_baseline / normal）、风险等级（risk_level：safe / notice / warning）、推送文本（如"老人今日只拿了 3 次水杯，已 5 小时未喝水，建议提醒老人增加饮水"）、建议动作（recommended_action：remind_to_drink / family_call_check / observe_only）
        - **重要提示**：仅输出基于视觉的饮水行为统计，**不直接代表实际饮水量**（杯里可能没装水/可能是别人拿杯子），不提供脱水症 / 泌尿系统感染 / 认知障碍等具体医学诊断；连续低饮水或老人有明显不适请及时就医

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_drinking_frequency_analysis.py](scripts/smyx_elderly_drinking_frequency_analysis.py)(
  用途：调用 API 进行老年人饮水杯拿起频率（脱水风险）分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、饮水阈值/基线/风险类型定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：画面必须稳定覆盖水杯放置区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **拿起次数仅作为饮水频率的间接代理**，杯里是否装水、是不是真的喝下去、是不是别人拿的杯子，本工具无法 100% 判定；建议结合饮水手势 + 个人基线 + 家属沟通综合判断
- 多人共用水杯、家中有客人 / 看护人员、老人在他人家或外出，会显著影响计数准确性
- 隐私合规：家庭/养老机构视频涉及个人隐私，使用前需取得老人/监护人明确知情同意，妥善加密保管；建议优先采用人体轮廓+物体框模式
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"饮水次数/风险"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`老年人饮水频率脱水风险报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 饮水次数/风险 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 老年人饮水频率脱水风险报告-20260312172200001 | 3 次 / warning（5h 未饮水，低于基线 7.5） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地客厅/厨房水杯区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_drinking_frequency_analysis --input /path/to/livingroom_day.mp4 --open-id your-open-id

# 分析网络客厅/厨房水杯区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_drinking_frequency_analysis --url https://example.com/livingroom_day.mp4 --open-id your-open-id

# 显示历史老人饮水频率（脱水风险）报告（自动触发关键词：查看老人饮水历史报告、脱水风险报告清单等）
python -m scripts.smyx_elderly_drinking_frequency_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_drinking_frequency_analysis --input day.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_drinking_frequency_analysis --input day.mp4 --open-id your-open-id --output result.json
```
