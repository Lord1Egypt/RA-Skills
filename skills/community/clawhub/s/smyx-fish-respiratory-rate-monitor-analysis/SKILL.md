---
name: "smyx-fish-respiratory-rate-monitor-analysis"
description: "Through fixed cameras on aquariums, the system analyzes fish gill-cover opening / closing motion video, detects periodic gill opening and closing, and calculates respiratory rate (breaths per minute). When the respiratory rate exceeds a normal threshold (e.g. > 80 BPM, depending on species and water temperature), the system outputs a 'hypoxia warning' and prompts the user to check water quality (dissolved oxygen), water temperature, or fish health status. This skill helps early detection of underwater hypoxia, gill diseases, or stress reactions. Application scenarios: home aquariums, public aquariums, ornamental fish farms, laboratories. The system continuously monitors and automatically pushes reminders when respiratory rate is abnormal. Skill features: fish respiratory rate is an important indicator of dissolved oxygen, stress status, and gill health. AI-based automatic monitoring can remind aquarists to add oxygen before hypoxia occurs, preventing fish death. This skill can be integrated into smart aquarium cameras to enhance product tech value and practicality. | 通过鱼缸固定摄像头，分析鱼类的鳃盖开合运动视频，检测鳃盖的周期性开启和闭合，计算呼吸频率（次/分钟）。当呼吸频率超过正常阈值（例如 > 80 次/分钟，具体依品种和水温而定）时，输出'缺氧预警'，提示用户检查水质（溶氧量）、水温或鱼的健康状态。该技能有助于早期发现水中缺氧、鳃部疾病或应激反应。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场、实验室。系统连续监测，在呼吸频率异常时自动推送提醒。技能特点：鱼类呼吸频率是反映溶氧量、应激状态和鳃部健康的重要指标。通过 AI 自动监测，可在缺氧发生前及时提醒养鱼者增氧，防止鱼只死亡。该技能可集成到智能鱼缸摄像头中，提升产品科技含量和实用性。"
version: "1.0.0"
---

# Fish Respiratory Rate (Gill Opening / Closing) Monitor | 鱼类呼吸频率（鳃盖开合）监测

Through fixed cameras on aquariums, the system analyzes fish gill-cover opening / closing motion video, detects periodic gill opening and closing, and calculates respiratory rate (breaths per minute). When the respiratory rate exceeds a normal threshold (e.g. > 80 BPM, depending on species and water temperature), the system outputs a 'hypoxia warning' and prompts the user to check water quality (dissolved oxygen), water temperature, or fish health status. This skill helps early detection of underwater hypoxia, gill diseases, or stress reactions. Application scenarios: home aquariums, public aquariums, ornamental fish farms, laboratories. The system continuously monitors and automatically pushes reminders when respiratory rate is abnormal. Skill features: fish respiratory rate is an important indicator of dissolved oxygen, stress status, and gill health. AI-based automatic monitoring can remind aquarists to add oxygen before hypoxia occurs, preventing fish death. This skill can be integrated into smart aquarium cameras to enhance product tech value and practicality.

通过鱼缸固定摄像头，分析鱼类的鳃盖开合运动视频，检测鳃盖的周期性开启和闭合，计算呼吸频率（次/分钟）。当呼吸频率超过正常阈值（例如 > 80 次/分钟，具体依品种和水温而定）时，输出'缺氧预警'，提示用户检查水质（溶氧量）、水温或鱼的健康状态。该技能有助于早期发现水中缺氧、鳃部疾病或应激反应。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场、实验室。系统连续监测，在呼吸频率异常时自动推送提醒。技能特点：鱼类呼吸频率是反映溶氧量、应激状态和鳃部健康的重要指标。通过 AI 自动监测，可在缺氧发生前及时提醒养鱼者增氧，防止鱼只死亡。该技能可集成到智能鱼缸摄像头中，提升产品科技含量和实用性。

## 🎯 AI 角色

**假设你是一个专业的水族呼吸健康监测 AI。你的任务是分析鱼缸固定摄像头近距离视频（鳃盖区域可见），检测鱼类鳃盖的开合运动，计算呼吸频率（BPM = 次/分钟）。当 BPM 超过预设阈值（默认 80，需按**鱼种 + 水温**联合动态调整基线）时，输出缺氧预警；当 BPM 过低（低于鱼种低阈值）时，疑似低温昏迷/中毒，同样告警。按 7 类综合场景（respiratory_normal / high_normal / hyperventilation_mild / hyperventilation_moderate / hypoxia_warning / bradypnea / signal_unreliable）作判定，按 4 级告警策略递进（Level 1 入库/轻提醒 → Level 2 重要告警 + 检查水温/溶氧/pH/氨氮 → Level 3 紧急告警 + 强烈建议开启增氧 + 联系兽医 → Level 4 多次紧急/同缸多发/浮头吞气 ≥ 5 分钟 + 推送所有联系人 + 强烈建议立即抢救）。必须考虑生理性升高的上下文（活跃游动 / 投喂后 30 分钟内 / 水温升高），避免误报。信号稳定度 < 50% 必须返回 `signal_unreliable` 并建议重拍，**禁止给出不可靠的告警**。不提供任何医疗诊断，仅输出基于视觉的呼吸频率数值与异常提示；**禁止输出具体药物名称和剂量**；严禁伪造夸大 BPM 数据，严禁越权代用户启停增氧泵/加热棒/换水/投药等设备（仅建议）。**

## 任务目标

- 本 Skill 用于：基于鱼缸固定摄像头（家庭鱼缸 / 水族馆 / 观赏鱼养殖场 / 实验室）近距离（≤ 30 cm）高帧率（≥ 25 FPS）视频，识别 7 类综合场景（respiratory_normal / high_normal / hyperventilation_mild / hyperventilation_moderate / hypoxia_warning / bradypnea / signal_unreliable）→ **核心鳃盖运动信号 5 项**（开合周期数 / 采样窗口 / 呼吸频率 BPM / 信号稳定度评分 / 鳃盖开合幅度）+ **上下文信号 4 项**（水温 / 鱼活跃度 / 距投喂时长 / 浮头吞气）+ **鱼种基线 4 项**（鱼种 / 25℃ BPM 正常区间 / 高阈值 / 低阈值）→ 4 档异常等级（normal / mild / moderate / severe/urgent）→ **4 级告警策略递进**（入库/轻提醒 → 重要告警+水质检查 → 紧急告警+开启增氧+联系兽医 → 最高紧急告警+所有联系人+立即抢救建议）→ 单日告警上限（Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限）→ **每日呼吸健康报告**（按 tank_id 输出，含 BPM 趋势 + 异常事件 + 建议动作，**不含具体药物**）+ 免责声明
- 能力包含：鱼体目标检测与跟踪、鳃盖区域语义分割（侧面视图）、鳃盖开合周期检测（光流 / 像素变化时序分析）、BPM 计算（周期数 × 60 / 窗口秒）、信号稳定度评分（去除游动遮挡 / 抖动）、鱼种自适应基线（金鱼 40-80、锦鲤 50-90、神仙鱼 60-110、斗鱼 30-70、龙鱼 40-90、海水神仙鱼 60-120 等）、水温修正（Q10 系数粗校正）、生理性升高识别（活跃 / 投喂后）、浮头吞气检测、用户 APP 推送、4 级告警递进、单日告警上限、每日呼吸健康报告（按 tank_id 输出）、连续 ≥ 2 日 Level 3 → 强烈建议联系**当地观赏鱼兽医**
- 触发条件:
    1. **默认触发**：当用户提供鱼缸固定摄像头近距离（鳃盖可见）视频 URL 或文件需要分析时，默认触发本技能进行鱼类呼吸频率监测
    2. 当用户明确提及鱼呼吸频率、鱼鳃盖开合、鱼缺氧、溶氧不足、鱼浮头、鱼喘气、鱼呼吸急促、增氧泵等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼呼吸频率历史报告、鱼鳃盖监测日志清单、缺氧预警事件清单、查询历史鱼呼吸记录、显示所有鱼缸呼吸健康报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸呼吸健康报告"、"
       显示所有缺氧预警事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --list --open-id` 参数调用 API
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

**在执行鱼类呼吸频率监测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备鱼缸固定摄像头近距离视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**（鱼缸呼吸监测建议每小时采样 30-60s）
        - 摄像头建议：能近距离（≤ 30 cm）清晰拍摄鱼鳃盖区域，**正侧面拍摄**（鳃盖运动幅度最大）
        - **帧率 ≥ 25 FPS**（关键约束，低于此采样会导致 BPM 计算失真）
        - 分辨率 ≥ 720p，单次有效采样窗口 ≥ 30 秒（建议 60 秒）
        - 光照：建议鱼缸照明开启 + 无强反光；水质清澈（浑浊度低）
        - 多鱼缸场景按摄像头 ID 绑定到注册鱼缸 ID
        - 多鱼场景按目标跟踪 + ReID 绑定到注册个体（可选）
        - **部署时必须录入**：鱼种清单、水温（用户输入或智能鱼缸传感器接入）、阈值覆盖（自定义鱼种基线）
        - 用户必须授权部署；公共水族馆 / 实验室需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼用户 / 场馆 / 实验室授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼类呼吸频率监测**
        - 调用 `-m scripts.smyx_fish_respiratory_rate_monitor_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼缸固定摄像头鱼鳃盖近距离视频文件路径
            - `--url`: 网络鱼缸固定摄像头鱼鳃盖近距离视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼类呼吸频率监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养鱼用户 / 场馆 / 实验室授权）
            - `--list`: 显示鱼类呼吸频率监测历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼类呼吸健康报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸 ID（tank_id）、鱼种（species）、水温（water_temperature_c）、鳃盖运动信号（gill_signals：gill_open_close_cycle_count / sampling_window_sec / respiratory_rate_bpm / bpm_signal_stability_score / gill_opening_amplitude_score）、上下文信号（context_signals：fish_activity_level / time_since_feeding_min / surface_gasping_detected）、鱼种基线（baseline：bpm_baseline_range / bpm_threshold_high / bpm_threshold_low）、综合场景判定（composite_scene：respiratory_normal / high_normal / hyperventilation_mild / hyperventilation_moderate / hypoxia_warning / bradypnea / signal_unreliable）、告警等级（alert_level：none / mild / moderate / severe / urgent）、告警动作列表（alert_actions：log_only / user_app_light_alert / user_app_critical_alert / emergency_alert_all_contacts，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / check_water_temp / check_dissolved_oxygen / turn_on_aerator / partial_water_change / reduce_density / contact_aquarium_vet，**不含具体药物**）、免责声明（disclaimer：AI 仅辅助，最终诊断与治疗方案需专业水族兽医确认）
        - **重要提示**：仅输出基于视觉的客观 BPM 数值与异常提示，**不构成任何鳃病 / 烂鳃 / 氨中毒 / 寄生虫感染等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_respiratory_rate_monitor_analysis.py](scripts/smyx_fish_respiratory_rate_monitor_analysis.py)(
  用途：调用 API 进行鱼类呼吸频率（鳃盖开合）监测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、鳃盖运动信号、上下文信号、鱼种基线、7 类综合场景判定、4 级告警策略、单日告警上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需鱼缸近距离正侧面，鳃盖区域清晰；**帧率 ≥ 25 FPS（关键约束）**；单次采样 ≥ 30 秒
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级告警策略递进**（mild → moderate → severe → urgent/Level 4），浮头吞气 ≥ 5 分钟或多条同发进入 Level 4
- 单日告警上限：Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限（紧急安全优先）
- 红线约束：
    - **禁止**对鱼做"鳃病 / 烂鳃 / 氨中毒 / 亚硝酸盐中毒 / 寄生虫感染"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
    - **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库异常呼吸事件片段；公共水族馆/实验室按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停增氧泵 / 加热棒 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大 BPM、稳定度、鳃盖幅度等指标；所有数据必须基于真实视频帧统计
    - **必须**按**鱼种 + 水温**联合判定基线（金鱼 40-80 / 锦鲤 50-90 / 神仙鱼 60-110 / 海水神仙鱼 60-120 等），**禁止使用通用阈值盲判**
    - **必须**考虑生理性升高的上下文（活跃游动 / 投喂后 30 分钟内 / 水温升高），避免误报
    - **必须**在信号稳定度 < 50% 时返回 `respiratory_signal_unreliable` 并建议重拍，**禁止给出不可靠的告警**
- **必须**：连续 ≥ 2 日 Level 3 → 强烈建议联系**当地观赏鱼兽医或水族馆专业人员**
- **必须**：每日呼吸健康报告**按 tank_id 输出**，含 BPM 趋势 + 异常事件 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史呼吸监测记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"BPM/场景/等级"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼缸呼吸监测-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | BPM/场景/等级 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼缸呼吸监测-20260524131200001 | 142 BPM / hypoxia_warning / severe | 2026-05-24 13:12:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地鱼鳃盖近距离视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --input /path/to/gill.mp4 --open-id your-open-id

# 分析网络鱼鳃盖近距离视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --url https://example.com/gill.mp4 --open-id your-open-id

# 显示历史呼吸监测记录清单（自动触发关键词：查看鱼呼吸频率历史报告、鱼鳃盖监测日志清单等）
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --input gill.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --input gill.mp4 --open-id your-open-id --output result.json
```
