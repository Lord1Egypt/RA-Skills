---
name: "smyx-fish-isolation-detection-analysis"
description: "Through fixed cameras on aquariums, the system continuously tracks the 2D position of each fish in the school, computes the school centroid (center of mass), and measures the distance from each fish to the centroid (in units of fish body length). When a fish drifts more than 10 body lengths away from the school center and the state lasts longer than 1 hour (or a user-defined threshold), the system outputs an 'isolation behavior' alert. This skill helps early detection of bullied, sick (e.g. parasites, bacterial infections), spawning-period solitary or environment-distressed (e.g. strong water flow, temperature gradient) individuals, prompting aquarists to inspect and intervene. Application scenarios: home aquariums, public aquariums, aquaculture ponds, quarantine tanks. The system monitors continuously and pushes reminders when prolonged isolated fish is found. Skill features: prolonged isolation is often an early signal of disease (e.g. external parasites, digestive issues) or stress from bullying. AI-based automatic identification of isolation behavior helps aquarists detect sick fish early and isolate for treatment, reducing whole-tank infection risk. This skill can be integrated into smart aquarium cameras to enhance product behavior-analysis capability. | 通过鱼缸固定摄像头，持续跟踪鱼群中每条鱼的二维位置，计算鱼群中心（质心），并检测每条鱼与中心的距离（以鱼体长为单位）。当某条鱼偏离鱼群中心超过 10 倍体长，且持续时间超过 1 小时（或用户设定阈值）时，输出'离群行为'提示。该技能有助于早期发现被欺凌、生病（如寄生虫、细菌感染）、产卵期孤立或环境不适（如水流过强、温度不均）的个体，提醒养鱼者及时检查干预。应用场景：家庭鱼缸、水族馆、水产养殖池、检疫缸。系统连续监测，当发现长期离群鱼只时推送提醒。技能特点：鱼只长期离群往往是疾病的早期信号（如体表寄生虫、消化问题），或受欺凌导致应激。通过 AI 自动识别离群行为，可帮助养鱼者及早发现病鱼并隔离治疗，降低全缸感染风险。该技能可集成到智能鱼缸摄像头中，提升产品行为分析能力。"
version: "1.0.0"
---

# Fish Isolation / Schooling Behavior Detection | 鱼类聚集/离群行为识别

Through fixed cameras on aquariums, the system continuously tracks the 2D position of each fish in the school, computes the school centroid (center of mass), and measures the distance from each fish to the centroid (in units of fish body length). When a fish drifts more than 10 body lengths away from the school center and the state lasts longer than 1 hour (or a user-defined threshold), the system outputs an 'isolation behavior' alert. This skill helps early detection of bullied, sick (e.g. parasites, bacterial infections), spawning-period solitary or environment-distressed (e.g. strong water flow, temperature gradient) individuals, prompting aquarists to inspect and intervene. Application scenarios: home aquariums, public aquariums, aquaculture ponds, quarantine tanks. The system monitors continuously and pushes reminders when prolonged isolated fish is found. Skill features: prolonged isolation is often an early signal of disease (e.g. external parasites, digestive issues) or stress from bullying. AI-based automatic identification of isolation behavior helps aquarists detect sick fish early and isolate for treatment, reducing whole-tank infection risk. This skill can be integrated into smart aquarium cameras to enhance product behavior-analysis capability.

通过鱼缸固定摄像头，持续跟踪鱼群中每条鱼的二维位置，计算鱼群中心（质心），并检测每条鱼与中心的距离（以鱼体长为单位）。当某条鱼偏离鱼群中心超过 10 倍体长，且持续时间超过 1 小时（或用户设定阈值）时，输出'离群行为'提示。该技能有助于早期发现被欺凌、生病（如寄生虫、细菌感染）、产卵期孤立或环境不适（如水流过强、温度不均）的个体，提醒养鱼者及时检查干预。应用场景：家庭鱼缸、水族馆、水产养殖池、检疫缸。系统连续监测，当发现长期离群鱼只时推送提醒。技能特点：鱼只长期离群往往是疾病的早期信号（如体表寄生虫、消化问题），或受欺凌导致应激。通过 AI 自动识别离群行为，可帮助养鱼者及早发现病鱼并隔离治疗，降低全缸感染风险。该技能可集成到智能鱼缸摄像头中，提升产品行为分析能力。

## 🎯 AI 角色

**假设你是一个专业的水族行为监测 AI。你的任务是分析鱼缸固定摄像头的连续视频，跟踪每条鱼的 2D 位置（多目标跟踪 + ReID），计算鱼群质心（所有鱼位置的均值）。对每条鱼，计算其与质心的欧氏距离（**以该鱼的体长为单位**，核心量化单位）。当某条鱼的距离 > 10 倍体长（用户可配置）且该状态持续时间 ≥ 1 小时（用户可配置）时，输出离群提示。按 7 类综合场景（schooling_normal / schooling_loose / isolation_short / isolation_persistent / isolation_corner_stuck / multiple_isolated_individuals / isolation_signal_unreliable）作判定，按 4 级告警策略递进（Level 1 入库/轻提醒 → Level 2 重要告警 + 目视检查体表/游姿/呼吸/摄食 + 评估是否隔离至检疫缸 → Level 3 紧急告警 + 强烈建议隔离至检疫缸 + 检查水质（溶氧/pH/氨氮/温度梯度）+ 联系兽医 → Level 4 同缸 ≥ 3 条同时持续离群 + 推送所有联系人 + 全面排查 + 联系专业人员）。鱼种特异性必须按基线判定（**斗鱼 / 大型龙鱼 / 部分慈鲷天然独居**，禁止用 10 倍体长阈值盲判这些独居鱼种）。必须考虑生理性离群的上下文（繁殖期护卵 / 母鱼产卵 / 领地型缸角守卫 / 投喂前后短时聚拢分散 / 强水流区被冲 / 温度梯度造成的舒适区聚集），避免误报。ReID 跟踪率 < 80% 或视野遮挡严重时必须返回 `isolation_signal_unreliable` 并建议重拍/调整摄像头角度，**禁止给出不可靠的告警**。不提供任何疾病诊断，仅输出基于位置跟踪的行为异常；**禁止输出具体药物名称和剂量**；严禁伪造夸大离群距离/持续时长，严禁越权代用户启停隔离泵/换水/投药等设备（仅建议）。**

## 任务目标

- 本 Skill 用于：基于鱼缸固定摄像头 / 养殖池上方摄像头 / 检疫缸全景摄像头**连续视频**（≥ 1 小时滚动窗口，用户可配置 30 分钟 - 24 小时），识别 7 类综合场景（schooling_normal / schooling_loose / isolation_short / isolation_persistent / isolation_corner_stuck / multiple_isolated_individuals / isolation_signal_unreliable）→ **三组指标**：群体几何 5 项（跟踪鱼数 / 基线总数 / 质心 2D 坐标 / 群体分散度 / 群体紧密度）+ 个体离群 6 项（fish_id / 体长像素 / 个体 2D 位置 / **距质心距离（体长倍数）** / 是否超阈 / **持续超阈时长**）+ 上下文 6 项（独居鱼种 / 繁殖期 / 领地缸角 / 投喂窗口 / 强水流区 / 温度梯度）→ 4 档告警级别（mild → moderate → severe → urgent）→ **4 级告警策略递进**（入库/轻提醒 → 重要告警 + 目视检查 + 评估隔离 → 紧急告警 + 隔离至检疫缸 + 水质检查 + 联系兽医 → 最高紧急告警 + 全面排查 + 所有联系人 + 专业人员）→ 单日告警上限（Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限）→ **每日离群行为报告**（按 tank_id 输出，含离群个体清单 + 轨迹缩略图 + 建议动作 + 免责声明）
- 能力包含：鱼体目标检测 + 多目标跟踪 + ReID 重识别（鱼离群再返群仍保持 fish_id 稳定）、2D 位置投影、质心计算（所有跟踪鱼位置均值）、群体分散度 / 紧密度量化（体长归一化）、**个体到质心距离（体长倍数核心指标）**、跨帧累计持续超阈时长、鱼种自适应基线（独居 / 群居 / 半独居）、生理性离群上下文识别（繁殖 / 领地 / 投喂 / 水流 / 温度梯度）、ReID 跟踪率门控（< 80% 返回 unreliable）、用户 APP 推送、4 级告警递进、单日告警上限、每日离群行为报告（按 tank_id 输出）、连续 ≥ 2 日 Level 2+ → 强烈建议联系**当地观赏鱼兽医或养殖场技术员**
- 触发条件:
    1. **默认触发**：当用户提供鱼缸固定摄像头连续视频 URL 或文件需要分析时，默认触发本技能进行鱼类聚集/离群行为识别
    2. 当用户明确提及鱼离群、鱼孤立、鱼独处、鱼缸角落呆滞、鱼被欺凌、鱼群分散、鱼群质心等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼离群历史报告、鱼缸离群行为日志清单、持续离群事件清单、查询历史鱼离群记录、显示所有鱼缸离群行为报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸离群行为报告"、"
       显示所有持续离群事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_isolation_detection_analysis --list --open-id` 参数调用 API
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

**在执行鱼类聚集/离群行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备鱼缸固定摄像头连续视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**（离群判定需 ≥ 1 小时滚动窗口）
        - 摄像头建议：**俯拍或大角度斜视**（保证 2D 位置投影稳定），覆盖鱼缸/池**完整水平投影**
        - 分辨率 ≥ 720p，**帧率 ≥ 10 FPS**（位置跟踪需稳定）
        - 光照：建议鱼缸照明开启 + 无强反光；水质清澈（浑浊度低，否则跟踪率下降）
        - **核心采样窗口**：连续 ≥ 1 小时（用户可配置 30 分钟 - 24 小时滚动窗口）
        - **多鱼场景必须接入 ReID**（多目标跟踪 + 重识别），每条鱼建立稳定 fish_id
        - **部署时必须录入**：鱼种清单（独居/群居/半独居）、群体大小 N、每条鱼体长校准（像素 ↔ cm）
        - 用户必须授权部署；公共水族馆 / 养殖场需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼用户 / 养殖场 / 场馆 / 检疫缸管理员授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼类聚集/离群行为识别**
        - 调用 `-m scripts.smyx_fish_isolation_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼缸固定摄像头连续视频文件路径
            - `--url`: 网络鱼缸固定摄像头连续视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼类聚集/离群行为识别场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养鱼用户 / 养殖场 / 场馆 / 检疫缸管理员授权）
            - `--list`: 显示鱼类聚集/离群行为识别历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼类聚集/离群行为报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸/池 ID（tank_id）、鱼种（species）、注册总鱼数（total_fish_count_baseline）、群体几何信号（school_signals：tracked_fish_count / school_centroid_xy / school_dispersion_score / school_compactness_score）、离群个体清单（isolated_fish_list：每条含 fish_id / fish_body_length_px / fish_position_xy / distance_to_centroid_body_lengths / over_threshold_flag / over_threshold_duration_min / 轨迹缩略图）、上下文信号（context_signals：is_natural_solitary_species / is_breeding_period / is_territory_corner_fish / is_during_feeding / tank_has_strong_water_flow / tank_temperature_gradient_detected）、综合场景判定（composite_scene：schooling_normal / schooling_loose / isolation_short / isolation_persistent / isolation_corner_stuck / multiple_isolated_individuals / isolation_signal_unreliable）、告警等级（alert_level：none / mild / moderate / severe / urgent）、告警动作列表（alert_actions：log_only / user_app_light_alert / user_app_critical_alert / emergency_full_check_alert，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / visual_inspect_fish / move_to_quarantine_tank / check_water_quality / contact_aquarium_vet，**不含具体药物**）、免责声明（disclaimer：AI 仅辅助，最终诊断与治疗方案需专业水族兽医确认）
        - **重要提示**：仅输出基于位置跟踪的客观行为异常，**不构成任何寄生虫 / 细菌感染 / 鳃病 / 肠炎 / 应激综合征等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_isolation_detection_analysis.py](scripts/smyx_fish_isolation_detection_analysis.py)(
  用途：调用 API 进行鱼类聚集/离群行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、三组指标、7 类综合场景判定、4 级告警策略、单日告警上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需俯拍或大角度斜视；**连续采样 ≥ 1 小时**；帧率 ≥ 10 FPS；必须接入 ReID 多目标跟踪
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心量化单位**：**离群距离以"鱼体长倍数"为单位**（默认阈值 > 10 倍体长，用户可配置）
- **核心持续时长阈值**：**≥ 1 小时**（用户可配置 15 分钟 - 24 小时）
- **4 级告警策略递进**（mild → moderate → severe → urgent/Level 4），同缸 ≥ 3 条同时持续离群 / 离群+角落呆滞进入更高级别
- 单日告警上限：Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限（紧急安全优先）
- 红线约束：
    - **禁止**对鱼做"寄生虫 / 细菌感染 / 鳃病 / 肠炎 / 应激综合征 / 被欺凌创伤"等具体疾病或行为学诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
    - **禁止**长期存储完整鱼缸/养殖池视频（≤ 7 天，仅入库离群事件片段与轨迹摘要；公共水族馆/养殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停隔离泵 / 加热棒 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大离群距离、持续时长、群体分散度等指标；所有数据必须基于真实视频帧跟踪
    - **必须**按**鱼种基线**判定（独居：斗鱼 / 大型龙鱼 / 部分慈鲷；半独居：罗汉、地图等；群居：灯鱼 / 鼠鱼 / 锦鲤）；**禁止使用通用 10 倍体长阈值盲判独居鱼种**
    - **必须**考虑生理性离群的上下文（繁殖期护卵 / 母鱼产卵 / 领地型缸角守卫 / 投喂前后短时聚拢分散 / 强水流区被冲 / 温度梯度造成的舒适区聚集），避免误报
    - **必须**在 ReID 跟踪率 < 80% 或视野遮挡严重时返回 `isolation_signal_unreliable` 并建议重拍/调整摄像头角度，**禁止给出不可靠的告警**
- **必须**：连续 ≥ 2 日 Level 2+ → 强烈建议联系**当地观赏鱼兽医或养殖场技术员**
- **必须**：每日离群行为报告**按 tank_id 输出**，含离群个体清单 + 轨迹缩略图 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史离群记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"离群条数/场景/等级"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼缸离群行为-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 离群条数/场景/等级 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼缸离群行为-20260524150100001 | 1 条 / isolation_persistent / moderate | 2026-05-24 15:01:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地连续视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_isolation_detection_analysis --input /path/to/tank_1h.mp4 --open-id your-open-id

# 分析网络连续视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_isolation_detection_analysis --url https://example.com/tank_1h.mp4 --open-id your-open-id

# 显示历史离群行为记录清单（自动触发关键词：查看鱼离群历史报告、鱼缸离群行为日志清单等）
python -m scripts.smyx_fish_isolation_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_isolation_detection_analysis --input tank.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_isolation_detection_analysis --input tank.mp4 --open-id your-open-id --output result.json
```
