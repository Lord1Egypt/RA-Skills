---
name: "smyx-child-outdoor-activity-monitor-analysis"
description: "Using a fixed camera at the balcony door or home entrance, the system detects how many times the child enters/exits the home or balcony. With person-tracking and region-entry/exit logic, it records the timestamps of each 'leaving indoor (outdoor)' and 'returning indoor' event, and accumulates the daily total outdoor-activity duration. | 通过家庭阳台门或入户门口的固定摄像头，检测儿童进出家门或阳台的次数，利用人体跟踪和区域进出判定技术，记录每次离开室内（外出）和返回室内（归来）的时间点，累计每日户外活动总时长。当当日总时长低于预设推荐值（默认建议学龄儿童每天至少1小时户外活动）时，输出'户外活动不足'提醒，建议家长带孩子增加户外时间。"
version: "1.0.1"
license: "MIT-0"
---

# Child Outdoor Activity Duration Monitoring | 儿童户外活动时长监测

Using a fixed camera at the balcony door or home entrance, the system detects how many times the child enters/exits the home or balcony. With person-tracking and region-entry/exit logic, it records the timestamps of each 'leaving indoor (outdoor)' and 'returning indoor' event, and accumulates the daily total outdoor-activity duration. When the daily total falls below a preset recommendation (default: at least 1 hour of outdoor activity per day for school-age children), it outputs an 'insufficient outdoor activity' alert, suggesting parents take the child out more. Application scenarios: family parenting, child health management, schools / kindergartens. The system automatically generates daily outdoor-activity reports; if multiple consecutive days fall short, it pushes app reminders to parents. Skill features: outdoor activity is crucial for child vision protection (myopia prevention), bone development, and mental health. AI automatic monitoring helps parents objectively understand the child's outdoor situation and adjust parenting strategies. Can be integrated into smart cameras or family education apps as a practical feature for child health management.

通过家庭阳台门或入户门口的固定摄像头，检测儿童进出家门或阳台的次数，利用人体跟踪和区域进出判定技术，记录每次离开室内（外出）和返回室内（归来）的时间点，累计每日户外活动总时长。当当日总时长低于预设推荐值（默认建议学龄儿童每天至少1小时户外活动）时，输出'户外活动不足'提醒，建议家长带孩子增加户外时间。应用场景：家庭育儿、儿童健康管理、学校/幼儿园。系统自动生成每日户外活动报告，若连续多日不足，通过APP推送提醒家长。技能特点：户外活动对儿童视力保护（预防近视）、骨骼发育、心理健康至关重要。通过AI自动监测，可帮助家长客观了解孩子户外活动情况，及时调整育儿方式。该技能可集成到智能摄像头或家庭教育APP中，成为儿童健康管理的实用功能。

## 🎯 AI 角色

**假设你是一个专业的儿童健康成长 AI。你的任务是分析阳台门或入户门口固定摄像头的视频，检测儿童进出区域的行为，记录外出和归来时间，累计每日户外活动总时长。当总时长低于推荐值时输出提醒。不要提供医疗建议或医学诊断，仅输出基于视觉的活动统计与友好提醒。**

## 任务目标

- 本 Skill 用于：基于阳台门/入户门口固定摄像头视频，识别儿童跨区域进出事件 → 累计每日户外活动总时长 → 对比推荐值（默认 ≥ 60 min）→ 输出户外活动不足提醒
- 能力包含：人体检测与跟踪、儿童识别（结合身高/外观特征）、室内/户外两个 ROI 划分（indoor_region / outdoor_region）、区域进出事件识别（exit / return）、配对生成每次"外出-归来"会话、累计每日总时长 + 会话次数 + 每次时长、推荐值对比与达成率计算、连续不足天数累计、提醒类型分类（daily_outdoor_insufficient / multi_day_outdoor_insufficient / outdoor_goal_met / normal）、家长友好提醒文本生成
- 触发条件:
    1. **默认触发**：当用户提供阳台门/入户门口固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行儿童户外活动时长监测
    2. 当用户明确提及儿童户外活动、近视预防、户外时间、骨骼发育、阳光时间、宝宝出门、家庭育儿健康等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看儿童户外活动历史报告、户外时长报告清单、儿童出门记录清单、查询历史儿童户外活动记录、显示所有儿童户外活动报告、显示家庭育儿健康诊断报告，查询儿童户外活动不足预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有儿童户外活动报告"、"
       显示所有户外时长报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_outdoor_activity_monitor_analysis --list --open-id` 参数调用 API
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

**在执行儿童户外活动时长监测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备阳台门/入户门口固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议覆盖一整天（白天+傍晚）
        - 摄像头建议：家庭阳台门 / 入户门口 / 楼道门口固定摄像头，对准门口/阳台门通道区域；可同时清晰看到"门内侧"和"门外侧/阳台外侧"两个区域
        - 帧率 ≤ 10 FPS 即可、分辨率 ≥ 480p、光照稳定
        - 初次部署需在画面中**框选两个 ROI**：`indoor_region`（室内区域）+ `outdoor_region`（户外区域）
        - 建议儿童佩戴可识别特征（如颜色/身高），用于在多人场景下区分识别
        - 可选附带：儿童姓名、年龄、推荐户外时长（recommended_outdoor_min）、最小有效会话时长（min_valid_session_min）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童户外活动时长监测**
        - 调用 `-m scripts.smyx_child_outdoor_activity_monitor_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地阳台门/入户门口固定摄像头视频文件路径
            - `--url`: 网络阳台门/入户门口固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童健康成长场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童户外活动时长监测历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童户外活动时长监测报告
        - 包含：儿童是否检测到（child_detected）、两个 ROI 是否已定义（indoor_region_defined / outdoor_region_defined）、当日指标（today_metrics：outdoor_session_count_today / outdoor_session_durations_today / total_outdoor_duration_today_min / last_exit_time / last_return_time）、推荐户外时长（recommended_outdoor_min）、达成率（goal_completion_pct）、连续不足天数（consecutive_insufficient_days）、提醒类型（alert_type：daily_outdoor_insufficient / multi_day_outdoor_insufficient / outdoor_goal_met / normal）、提醒级别（alert_level：info / notice / warning）、推送给家长的文本（如"宝宝今天累计户外活动只有 25 分钟，离推荐 60 分钟还有差距，下午带 TA 去公园玩一会儿吧~"）、建议动作（recommend_action：push_app_notice / suggest_outdoor_plan / observe_only）
        - **重要提示**：仅输出基于视觉的进出门事件统计与友好提醒，**不直接代表真实户外运动量**（短时下楼丢垃圾/收快递可能被排除），不提供视力/骨骼/心理等医学诊断或处方

## 资源索引

- 必要脚本：见 [scripts/smyx_child_outdoor_activity_monitor_analysis.py](scripts/smyx_child_outdoor_activity_monitor_analysis.py)(
  用途：调用 API 进行儿童户外活动时长监测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、户外阈值/有效会话/提醒类型定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：画面必须同时覆盖室内与户外（阳台/楼道）两个区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 户外时长统计仅基于"进出门事件"，**不直接代表真实户外运动量**；孩子从阳台门出去阳台坐着也会被计入"户外"，建议结合家长主观感受参考
- 多孩家庭、儿童外观相近时需注意身份混淆；可结合身高/衣着辅助识别
- 短时间下楼丢垃圾、收快递（< 5 min）默认视为无效会话，可由调用方覆盖阈值
- 隐私合规：家庭门口/阳台视频涉及未成年人隐私，使用前需取得监护人明确知情同意，妥善加密保管；建议优先采用人体轮廓模式
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"户外时长/达成"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童户外活动时长监测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 户外时长/达成 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童户外活动时长监测报告-20260312172200001 | 25 min / 42%（建议增加户外） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地阳台门/入户门口视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --input /path/to/door.mp4 --open-id your-open-id

# 分析网络阳台门/入户门口视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --url https://example.com/door.mp4 --open-id your-open-id

# 显示历史儿童户外活动时长监测报告（自动触发关键词：查看儿童户外活动历史报告、户外时长报告清单等）
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --input door.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --input door.mp4 --open-id your-open-id --output result.json
```
