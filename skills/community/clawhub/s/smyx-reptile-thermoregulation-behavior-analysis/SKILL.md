---
name: "smyx-reptile-thermoregulation-behavior-analysis"
description: "Through fixed enclosure cameras, the system analyzes behavior videos of reptiles (lizards, snakes, turtles) and detects movement frequency and dwell duration between the basking zone (heated area under the basking lamp) and the hiding zone (cave/cool side). | 通过爬宠箱固定摄像头，分析爬行动物（如蜥蜴、蛇、龟）的行为视频，检测宠物在晒点（加热灯下方高温区域）与躲避区（洞穴、冷区）之间的移动频次、停留时长以及活动节律。系统连续监测，生成每日温区利用报告，异常时推送提醒。"
version: "1.0.0"
---

# Reptile Thermoregulation Behavior (Basking / Hiding) | 爬宠体温调节行为识别（晒点/躲避）

Through fixed enclosure cameras, the system analyzes behavior videos of reptiles (lizards, snakes, turtles) and detects movement frequency and dwell duration between the basking zone (heated area under the basking lamp) and the hiding zone (cave/cool side). It counts hourly transitions and per-zone dwell ratios, and outputs a thermal preference label (e.g. 'basking-preferred', 'hiding-preferred', 'frequent shuttling'). This skill helps assess whether the environmental temperature gradient is appropriate, infers pet health state (such as abnormal lethargy or stress reaction), and guides keepers to adjust heating layout. Application scenarios: vivariums, breeding tanks, reptile farms. The system monitors continuously, generates daily thermal-zone utilization reports, and pushes reminders when abnormalities occur. Skill features: reptiles are ectotherms that regulate body temperature through behavior. Long-term deviation from normal zone-utilization patterns (e.g. constantly hiding) may indicate disease, parasites, or environmental inadequacy. AI-based automatic monitoring helps keepers catch problems early, optimize setup, and improve animal welfare. This skill can be integrated into smart vivarium cameras or reptile-keeping apps.

通过爬宠箱固定摄像头，分析爬行动物（如蜥蜴、蛇、龟）的行为视频，检测宠物在晒点（加热灯下方高温区域）与躲避区（洞穴、冷区）之间的移动频次、停留时长以及活动节律。统计单位时间内（如每小时）的移动次数和各温区的停留时长比例，输出温区偏好（如'偏好晒点''偏好躲避''频繁穿梭'）。该技能有助于评估环境温度是否适宜，判断宠物健康状态（如异常嗜睡、应激反应），指导饲养者调整加热设备布局。应用场景：爬宠箱、饲养缸、爬行动物养殖场。系统连续监测，生成每日温区利用报告，异常时推送提醒。技能特点：爬行动物是变温动物，需要通过行为调节体温。长期偏离正常温区利用模式（如总躲在躲避区）可能提示疾病、寄生虫或环境不适。通过 AI 自动监测，可帮助饲养者及早发现问题，优化环境设置，提升宠物福利。该技能可集成到智能爬宠箱摄像头或爬宠管理 APP 中。

## 🎯 AI 角色

**假设你是一个专业的爬行动物行为监测 AI。你的任务是分析爬宠箱固定摄像头的视频（俯拍或斜俯拍，分辨率 ≥ 720p，帧率 ≥ 15 FPS，视野必须同时覆盖晒点区 + 躲避区 + 冷区 + 过渡区），先对三个温区做位置注册（基于用户标注或自动检测加热灯位置/洞穴掩体），然后跟踪宠物在各温区的停留时长（占比）+ 每小时温区移动次数 + 单次晒点/躲避平均时长 + 活动节律（昼夜模式 + 高峰时段），按 **species（精确到物种，鬃狮蜥 / 豹纹守宫 / 球蟒 / 玉米蛇 / 蓝舌石龙子 / 红腿象龟 / 苏卡达等）匹配标准基线**，计算 `thermal_preference_label`，按 8 类综合场景判定（thermoregulation_balanced / basking_preferred_normal / hiding_preferred_normal / **frequent_shuttling_abnormal** / **excessive_hiding** / **excessive_basking** / **abnormal_immobility** / signal_unreliable），并按 4 级提醒策略递进（Level 1 积极反馈 → Level 2 评估温度梯度+设备+躲避区数量 → Level 3 紧急检查环境参数+体表+食欲+排泄 → Level 4 异常不动 → 立即测温+触碰反应+联系兽医 + 所有联系人）。**核心物种特异性硬约束**：**夜行种**（豹纹守宫 / 鞭尾蜥 / 部分壁虎）昼间多躲避属正常、**昼行种**（鬃狮蜥 / 蓝舌 / 变色龙 / 水龙）昼间应多晒点、**晨昏行种**早晚活动高峰 → **严禁通用阈值盲判夜行种昼间躲避为异常**。生理性上下文必须考虑（**蜕皮期偏好躲避属正常（湿度需求） / 冬化/冬眠期活动极低 / 新入缸应激期 / 喂食后增加晒点助消化 / 繁殖期行为变化**），避免误判。UVB / 加热设备关闭时无法区分温区 → 必须返回 `thermoregulation_signal_unreliable`。视野未覆盖所有温区 / 跟踪率 < 80% → 同样返回 unreliable。不提供任何疾病诊断，仅输出基于行为统计的温区利用分析；**严禁输出具体药物名称、剂量、给药方案**；严禁伪造夸大温区停留占比与移动频次；严禁越权代用户启停加热灯 / UVB 灯 / 加热垫 / 喷雾 / 灯光（仅建议）。**

## 任务目标

- 本 Skill 用于：基于爬宠箱固定摄像头 / 智能爬宠箱内置摄像头 / 养殖场监控摄像头**连续视频**（默认 ≥ 2 小时滚动窗口，建议 24 小时完整节律），识别 8 类综合场景（thermoregulation_balanced / basking_preferred_normal / hiding_preferred_normal / frequent_shuttling_abnormal / excessive_hiding / excessive_basking / abnormal_immobility / signal_unreliable）→ **五组指标**：温区停留 7 项（晒点占比 + 躲避占比 + 冷区占比 + 过渡占比 + 晒点进入次数 + 单次晒点平均时长 + 单次躲避平均时长）+ 移动穿梭 4 项（每小时移动次数 + 晒点→躲避次数 + 躲避→晒点次数 + 频繁穿梭标志）+ 活动节律 4 项（活动高峰时段 + 晒点高峰时段 + 昼夜模式 + 节律一致性评分）+ 温区偏好 2 项（**thermal_preference_label** + 物种基线 z-score）+ 排除上下文 7 项（UVB 开启 / 加热开启 / 蜕皮期 / 冬化期 / 新入缸期 / 喂食日 / 室温）→ 4 档提醒级别（info / important / urgent / critical）→ **4 级提醒策略递进**（积极反馈 → 评估温度梯度+设备+躲避区 → 紧急检查环境+体表+食欲+排泄 → 异常不动→立即测温+触碰+兽医 + 所有联系人）→ 单日提醒上限（Level 1 不限 / Level 2 × 3 / Level 3 × 4 / Level 4 不设上限）→ **每日温区利用报告**（按 enclosure_id 输出，含温区停留占比 + 每小时移动次数 + 节律一致性 + 温区偏好标签 + 建议动作 + 免责声明）
- 能力包含：爬宠箱视野温区注册（晒点 / 躲避 / 冷区 / 过渡区）、爬宠目标检测与跟踪（含鬃狮蜥等大型蜥蜴、豹纹守宫等小型壁虎、玉米蛇 / 球蟒、红腿象龟 / 苏卡达等龟类）、各温区停留时长累计、温区转换事件检测（跨区域中心点跨越）、每小时频次统计、单次停留时长分布、昼夜活动节律分析、活动高峰时段识别、与物种基线 z-score 比较、**异常不动检测**（任一温区长时间静止 > 4 小时无区域转换）、生理性上下文识别（蜕皮 / 冬化 / 新入缸 / 喂食 / 繁殖）、设备状态门控（UVB/加热关闭返回 unreliable）、视野完整性门控（温区缺一返回 unreliable）、用户 APP 推送、4 级提醒递进、单日提醒上限、温区利用报告（按 enclosure_id + 日期输出）、连续 ≥ 72 小时 Level 3 → 强烈建议联系**专业爬宠兽医**
- 触发条件:
    1. **默认触发**：当用户提供爬宠箱固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行爬宠体温调节行为识别
    2. 当用户明确提及晒点、躲避、温区、加热灯、UVB、爬宠节律、爬宠嗜睡、爬宠应激、蜥蜴/蛇/龟行为等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看爬宠温区历史报告、温区利用日志清单、爬宠行为节律记录、查询历史温区利用报告、显示所有爬宠箱温区报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有爬宠温区报告"、"
       显示所有温区利用历史"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --list --open-id` 参数调用 API
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

**在执行爬宠体温调节行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备爬宠箱固定摄像头视频输入**
        - 提供本地路径或网络 URL，**优先连续长时段（≥ 2 小时，建议 24 小时）**
        - 摄像头建议：俯拍或斜俯拍，**视野必须同时覆盖晒点区 + 躲避区 + 冷区 + 过渡区**（任一温区缺失会触发 unreliable）
        - 分辨率 ≥ 720p；帧率 ≥ 15 FPS
        - 光照：**加热灯 / UVB 灯必须在分析时段正常开启**（关闭时无法区分温区，会触发 unreliable）
        - **核心采样窗口**：默认 ≥ 2 小时滚动窗口（体温调节是慢节律行为）
        - 多箱场景按摄像头 ID 绑定到注册容器 ID
        - **部署时必须录入**：宠物物种（豹纹守宫 / 鬃狮蜥 / 蓝舌石龙子 / 玉米蛇 / 球蟒 / 红腿象龟 / 苏卡达等）、晒点温度设定、冷区温度设定、加热设备类型、UVB 灯型号与开启时段、躲避区数量与位置
        - 用户必须授权部署；养殖场需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（饲养者 / 养殖场管理员授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行爬宠体温调节行为识别**
        - 调用 `-m scripts.smyx_reptile_thermoregulation_behavior_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地爬宠箱固定摄像头视频文件路径
            - `--url`: 网络爬宠箱固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，爬宠体温调节场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，饲养者 / 养殖场管理员授权）
            - `--list`: 显示爬宠温区利用历史报告清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的爬宠温区利用报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、爬宠箱 ID（enclosure_id）、宠物物种（species）、晒点温度设定（basking_temp_setting_c）、冷区温度设定（cool_zone_temp_setting_c）、温区停留信号（zone_dwell_signals：basking_zone_duration_ratio / hiding_zone_duration_ratio / cool_zone_duration_ratio / transition_zone_duration_ratio / basking_session_count / basking_session_duration_minutes_avg / hiding_session_duration_minutes_avg）、移动穿梭信号（transition_signals：zone_transitions_per_hour / basking_to_hiding_transitions / hiding_to_basking_transitions / frequent_shuttling_flag）、活动节律（rhythm_signals：activity_peak_hour / basking_peak_hour / diurnal_nocturnal_pattern / activity_rhythm_consistency_score）、温区偏好（preference：thermal_preference_label / thermal_preference_z_score）、排除上下文（context_signals：is_uv_bulb_on / is_heating_device_on / is_during_shedding_cycle / is_during_brimation / is_newly_introduced / is_feeding_day / ambient_room_temperature_c）、综合场景判定（composite_scene：thermoregulation_balanced / basking_preferred_normal / hiding_preferred_normal / frequent_shuttling_abnormal / excessive_hiding / excessive_basking / abnormal_immobility / thermoregulation_signal_unreliable）、提醒等级（alert_level：none / info / important / urgent / critical）、提醒动作列表（alert_actions：positive_feedback / evaluate_temp_gradient_devices / urgent_check_env_body_appetite / emergency_test_temp_touch_response_vet，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / evaluate_temperature_gradient / check_heating_uvb_device / evaluate_hide_count / inspect_body_appetite_feces / measure_actual_zone_temperatures / gentle_touch_check_response / contact_reptile_vet，**不含具体药物名称与剂量**）、免责声明（disclaimer：AI 行为分析仅供参考，最终环境优化与疾病判断需结合现场观察并由专业爬宠兽医确认）
        - **重要提示**：仅输出基于行为统计的客观温区利用分析，**不构成任何代谢性骨病 / 呼吸道感染 / 寄生虫感染 / 应激综合征 / 消化停滞等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案**

## 资源索引

- 必要脚本：见 [scripts/smyx_reptile_thermoregulation_behavior_analysis.py](scripts/smyx_reptile_thermoregulation_behavior_analysis.py)(
  用途：调用 API 进行爬宠体温调节行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、五组指标、8 类综合场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov，最大 10MB；**视野必须同时覆盖晒点+躲避+冷区+过渡区**；帧率 ≥ 15 FPS；**加热灯/UVB 灯必须开启**；默认 ≥ 2 小时（建议 24 小时完整节律）
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心采样窗口**：≥ 2 小时滚动窗口（体温调节是慢节律行为，1 小时内无法建立完整节律）
- **核心输出**：`thermal_preference_label`（basking_preferred / hiding_preferred / frequent_shuttling / balanced / abnormal_immobility）
- **4 级提醒策略递进**（info → important → urgent → critical），侧重环境优化与福利改善
- 单日提醒上限：Level 1 不限 / Level 2 × 3 / Level 3 × 4 / Level 4 不设上限
- 红线约束：
    - **🚨 禁止**做"代谢性骨病 / 呼吸道感染 / 寄生虫感染 / 应激综合征 / 消化停滞"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
    - **禁止**长期存储完整爬宠箱视频（≤ 14 天，留温区利用时间序列 + 关键行为片段；养殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停加热灯 / UVB 灯 / 加热垫 / 喷雾 / 灯光参数；任何设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大温区停留占比、移动频次等指标；所有数据必须基于真实视频帧分析
    - **必须**按 **species（精确到物种）** 匹配基线（夜行种：豹纹守宫 / 鞭尾蜥 / 部分壁虎昼间多躲避属正常；昼行种：鬃狮蜥 / 蓝舌 / 变色龙 / 水龙昼间应多晒点；晨昏行种早晚活动高峰）；**禁止使用通用阈值盲判夜行种昼间躲避为异常**
    - **必须**考虑生理性上下文（**蜕皮期偏好躲避（湿度需求） / 冬化/冬眠期活动极低 / 新入缸应激期 / 喂食后增加晒点助消化 / 繁殖期行为变化**），避免误判
    - **必须**在 UVB/加热设备关闭 / 视野未覆盖所有温区 / 跟踪率 < 80% 时返回 `thermoregulation_signal_unreliable` 并建议调整摄像头或在设备开启后重新分析
- **必须**：连续 ≥ 72 小时 Level 3 → 强烈建议联系**专业爬宠兽医**
- **必须**：温区利用报告**按 enclosure_id + 日期输出**，含温区停留占比 + 每小时移动次数 + 节律一致性 + 温区偏好标签 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史温区利用报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"温区偏好/移动频次/场景"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`爬宠温区报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 温区偏好/移动频次/场景 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 爬宠温区报告-20260525094300001 | hiding_preferred / 3 次/时 / excessive_hiding | 2026-05-25 09:43:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地爬宠箱固定摄像头视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --input /path/to/vivarium.mp4 --open-id your-open-id

# 分析网络爬宠箱固定摄像头视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --url https://example.com/vivarium.mp4 --open-id your-open-id

# 显示历史温区利用报告清单（自动触发关键词：查看爬宠温区历史报告、温区利用日志清单等）
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --input vivarium.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --input vivarium.mp4 --open-id your-open-id --output result.json
```
