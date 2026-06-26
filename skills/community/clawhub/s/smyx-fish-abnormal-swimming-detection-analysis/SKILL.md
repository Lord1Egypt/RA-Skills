---
name: "smyx-fish-abnormal-swimming-detection-analysis"
description: "Through fixed cameras on aquariums, the system analyzes fish swimming videos and computes the angle between the fish body axis and the horizontal plane (normal fish bodies stay nearly horizontal). When the body tilt exceeds a threshold (default > 30°), the head points downward by > 45° (upside-down), or continuous rotation around the body's longitudinal axis occurs, the swimming posture is flagged as abnormal, and the proportion of abnormal duration over total observation time is recorded. This skill helps early detection of swim bladder disorder, neurological diseases, water poisoning and other health issues, prompting aquarists to intervene promptly. Application scenarios: home aquariums, public aquariums, ornamental fish farms. The system monitors continuously and generates a daily swimming-posture health report. Skill features: abnormal swimming posture is a common symptom of swim bladder disorder, poisoning, and infection. AI-based automatic identification and quantification of abnormal-time ratio helps aquarists detect issues early and take measures such as water change or medication, reducing mortality. This skill can be integrated into smart aquariums or aquarium cameras as a practical tool for aquarists. | 通过鱼缸固定摄像头，分析鱼类的游动视频，检测鱼体轴线与水平面的夹角（正常鱼体基本保持水平），当鱼体倾斜角度超过阈值（默认 > 30°）或出现倒立（头部向下 > 45°）、旋转（绕自身纵轴连续翻转）等异常游姿时，标记为异常，并记录异常时长占观察总时长的比例。该技能有助于早期发现鱼鳔失调、神经系统疾病或水质中毒等健康问题，提醒养鱼爱好者及时干预。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场。系统连续监测，生成每日游姿健康报告。技能特点：鱼类游姿异常是鱼鳔失调、中毒、感染等疾病的常见症状。通过 AI 自动识别并量化异常时间占比，可帮助养鱼者及早发现问题，采取换水、用药等措施，降低死亡率。该技能可集成到智能鱼缸或水族摄像头中，成为养鱼爱好者的实用工具。"
version: "1.0.0"
---

# Fish Abnormal Swimming Posture (Side-swim / Upside-down) Detection | 鱼类游动姿态异常（侧游/倒立）识别

Through fixed cameras on aquariums, the system analyzes fish swimming videos and computes the angle between the fish body axis and the horizontal plane (normal fish bodies stay nearly horizontal). When the body tilt exceeds a threshold (default > 30°), the head points downward by > 45° (upside-down), or continuous rotation around the body's longitudinal axis occurs, the swimming posture is flagged as abnormal, and the proportion of abnormal duration over total observation time is recorded. This skill helps early detection of swim bladder disorder, neurological diseases, water poisoning and other health issues, prompting aquarists to intervene promptly. Application scenarios: home aquariums, public aquariums, ornamental fish farms. The system monitors continuously and generates a daily swimming-posture health report. Skill features: abnormal swimming posture is a common symptom of swim bladder disorder, poisoning, and infection. AI-based automatic identification and quantification of abnormal-time ratio helps aquarists detect issues early and take measures such as water change or medication, reducing mortality. This skill can be integrated into smart aquariums or aquarium cameras as a practical tool for aquarists.

通过鱼缸固定摄像头，分析鱼类的游动视频，检测鱼体轴线与水平面的夹角（正常鱼体基本保持水平），当鱼体倾斜角度超过阈值（默认 > 30°）或出现倒立（头部向下 > 45°）、旋转（绕自身纵轴连续翻转）等异常游姿时，标记为异常，并记录异常时长占观察总时长的比例。该技能有助于早期发现鱼鳔失调、神经系统疾病或水质中毒等健康问题，提醒养鱼爱好者及时干预。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场。系统连续监测，生成每日游姿健康报告。技能特点：鱼类游姿异常是鱼鳔失调、中毒、感染等疾病的常见症状。通过 AI 自动识别并量化异常时间占比，可帮助养鱼者及早发现问题，采取换水、用药等措施，降低死亡率。该技能可集成到智能鱼缸或水族摄像头中，成为养鱼爱好者的实用工具。

## 🎯 AI 角色

**假设你是一个专业的水族健康监测 AI。你的任务是分析鱼缸固定摄像头的视频，检测鱼类的游动姿态，计算鱼体轴线与水平面的夹角。当夹角 > 30°（侧游）或头部向下 > 45°（倒立）或出现连续轴向旋转（≥ 2 圈/秒）时，判定为异常游姿。统计异常游姿时长占总观察时长的比例（异常占比），并按 7 类场景（fish_swimming_normal / side_swim_brief / side_swim_persistent / upside_down / axial_rotation / floating_or_sinking / strong_abnormal）做综合判定，按 4 级告警策略（Level 1 仅入库 → Level 2 用户 APP 轻提醒 → Level 3 用户 APP 重要告警 + 建议立即检查水质 → Level 4 紧急告警 + 建议换水/隔离/咨询观赏鱼兽医）递进。不同鱼种正常游姿差异极大（比目鱼天然侧卧、神仙鱼立泳、海马垂直游动），必须按鱼种基线判定，禁止使用通用阈值对特殊鱼种盲判。不提供任何鱼类疾病医学诊断，仅输出基于视觉的姿态分析结果、异常占比与建议动作；严禁伪造夸大异常数据，严禁越权代用户调整智能鱼缸的加热/换水/投喂/灯光参数。**

## 任务目标

- 本 Skill 用于：基于鱼缸固定摄像头（家庭鱼缸 / 水族馆 / 观赏鱼养殖场）视频，识别 7 类场景（fish_swimming_normal / side_swim_brief / side_swim_persistent / upside_down / axial_rotation / floating_or_sinking / strong_abnormal）→ 视频核心 8 项（鱼体轴线夹角 / 头部向下角度 / 轴向旋转事件 / 侧游累计时长 / 倒立累计时长 / 漂浮时长 / 沉底时长 / 游速异常评分）+ 衍生指标 4 项（异常总时长 / 观察总时长 / 异常占比 / 鱼体计数）→ 4 档异常等级（normal / brief / persistent / strong_abnormal）→ **4 级告警策略递进**（仅入库 → 用户 APP 轻提醒 → 用户 APP 重要告警 + 检查水质 → 紧急告警 + 建议换水/隔离/咨询兽医）→ 单日告警上限管控（Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限）→ **每日游姿健康报告**（按 tank_id 生成，含异常占比 + 近 7 日趋势 + Top 3 异常场景 + 建议动作）
- 能力包含：鱼体目标检测与跟踪（多鱼场景 ReID 可选）、鱼体轴线（头-尾向量）几何重建、轴线与水平面夹角逐帧计算、头部朝向识别（区分侧游 vs 倒立）、绕纵轴翻转检测（连续旋转）、异常游姿时长统计、异常占比量化、游速异常识别（过慢 / 抽搐式急加速）、异常漂浮 / 沉底识别、鱼种自适应基线（普通观赏鱼 / 比目鱼 / 神仙鱼 / 海马 / 锦鲤 / 龙鱼等）、夜间灯光关闭时段处理（红外辅助 / 自动暂停）、用户 APP 推送、4 级告警递进、单日告警上限、每日游姿健康报告（按 tank_id 输出）、连续 ≥ 2 日显著异常 → 紧急提醒
- 触发条件:
    1. **默认触发**：当用户提供鱼缸固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行鱼类游动姿态异常识别
    2. 当用户明确提及鱼游姿异常、鱼侧游、鱼倒立、鱼翻肚、鱼鳔失调、鱼缸监测、观赏鱼健康、鱼类异常游动等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼类游姿历史报告、鱼缸游姿监测日志清单、鱼游姿异常事件清单、查询历史鱼游姿记录、显示所有鱼缸游姿报告、显示鱼类游姿健康日志，查询鱼缸异常清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸游姿报告"、"
       显示所有鱼游姿异常事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_abnormal_swimming_detection_analysis --list --open-id` 参数调用 API
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

**在执行鱼类游动姿态异常识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备鱼缸固定摄像头视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**（鱼缸监测建议 24h 连续）
        - 摄像头建议：鱼缸侧面固定摄像头，能完整覆盖主活动区域；正对鱼缸长边方向
        - 帧率 ≥ 15 FPS（高速游动鱼建议 ≥ 25 FPS）、分辨率 ≥ 720p
        - 光照：建议保留鱼缸照明，避免反光过强；水浑浊度低
        - 多鱼缸场景按摄像头 ID 绑定到注册鱼缸 ID（每个鱼缸独立基线 + 鱼种清单）
        - 多鱼场景按目标跟踪 + ReID 绑定到注册个体（可选）
        - **部署时必须录入**：鱼种清单（普通观赏鱼 / 比目鱼 / 神仙鱼 / 海马 / 锦鲤 / 龙鱼等）、阈值覆盖（如比目鱼天然侧卧基线 ≈ 90°）
        - 用户必须授权部署；公共水族馆需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼用户或场馆授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼类游动姿态异常识别**
        - 调用 `-m scripts.smyx_fish_abnormal_swimming_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼缸固定摄像头视频文件路径
            - `--url`: 网络鱼缸固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼类游姿监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养鱼用户或场馆授权）
            - `--list`: 显示鱼类游姿异常监测历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼类游姿监测报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸 ID（tank_id）、鱼种基线（species_baseline）、被跟踪鱼数量（fish_count_detected）、场景判定（scene_label：fish_swimming_normal / side_swim_brief / side_swim_persistent / upside_down / axial_rotation / floating_or_sinking / strong_abnormal）、视频信号（video_signals：body_axis_angle_deg / head_down_angle_deg / axial_rotation_event_count / side_swim_duration_sec / upside_down_duration_sec / floating_duration_sec / sinking_duration_sec / swim_speed_anomaly_score）、衍生指标（derived：abnormal_total_duration_sec / observation_total_duration_sec / abnormal_ratio）、异常等级（abnormal_level：normal / brief / persistent / strong_abnormal）、告警动作列表（alert_actions：log_only / user_app_light_alert / user_app_critical_alert / emergency_alert，每项含 action_type / message / target / level）、每日游姿健康报告（daily_swimming_report：report_date / observation_hours / abnormal_ratio_today / abnormal_ratio_7d_avg / abnormal_ratio_trend / top_abnormal_scenes / recommended_actions）、建议动作（recommend_action：observe_only / check_water_quality / isolate_fish / contact_aquarium_vet / urgent_water_change）
        - **重要提示**：仅输出基于视觉的客观姿态分析结果与异常占比量化，**不构成任何鱼鳔病 / 神经系统疾病 / 水质中毒等医学诊断**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_abnormal_swimming_detection_analysis.py](scripts/smyx_fish_abnormal_swimming_detection_analysis.py)(
  用途：调用 API 进行鱼类游动姿态异常（侧游/倒立）识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、视频信号/衍生指标、7 类场景判定、4 级告警策略、单日告警上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需鱼缸侧面固定，主活动区可见；帧率 ≥ 15 FPS
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级告警策略递进**（normal → brief → persistent → strong_abnormal/Level 4），异常占比 > 20% 或多项叠加进入 Level 4
- 单日告警上限：Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限（紧急安全优先）
- 红线约束：
    - **禁止**对鱼做"鱼鳔病 / 神经系统疾病 / 重金属中毒 / 立鳞病 / 寄生虫感染"等疾病诊断
    - **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库异常事件片段；公共水族馆按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户调整智能鱼缸的加热 / 换水 / 投喂 / 灯光参数；任何水族设备控制变更必须由用户确认
    - **绝对禁止**伪造或夸大异常占比、异常时长等指标；所有数据必须基于真实视频帧统计
    - **禁止**使用通用阈值对特殊鱼种盲判（比目鱼天然侧卧、神仙鱼立泳、海马垂直游动等）；必须按鱼种基线判定
    - **必须**在部署时录入鱼种清单和自定义阈值覆盖
- **必须**：连续 ≥ 2 日显著异常 → 紧急提醒用户尽快联系**当地观赏鱼兽医**或**水族馆专业人员**
- **必须**：每日游姿健康报告**按 tank_id 输出**，含异常占比 + 近 7 日趋势 + Top 3 异常场景 + 建议动作
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史游姿监测记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"场景/等级/异常占比"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼缸游姿监测-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 场景/等级/异常占比 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼缸游姿监测-20260524125000001 | fish_upside_down / strong_abnormal / 异常占比 35% | 2026-05-24 12:50:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地鱼缸视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_abnormal_swimming_detection_analysis --input /path/to/aquarium.mp4 --open-id your-open-id

# 分析网络鱼缸视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_abnormal_swimming_detection_analysis --url https://example.com/aquarium.mp4 --open-id your-open-id

# 显示历史游姿监测记录清单（自动触发关键词：查看鱼类游姿历史报告、鱼缸游姿监测日志清单等）
python -m scripts.smyx_fish_abnormal_swimming_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_abnormal_swimming_detection_analysis --input aq.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_abnormal_swimming_detection_analysis --input aq.mp4 --open-id your-open-id --output result.json
```
