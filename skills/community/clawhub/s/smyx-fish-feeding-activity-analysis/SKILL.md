---
name: "smyx-fish-feeding-activity-analysis"
description: "Through built-in cameras of smart feeders or fixed cameras on aquariums, the system captures fish feeding videos after feeding. Using AI object detection and motion analysis, it identifies the number of fish gathering for food, feeding intensity (fish swimming speed, feeding action frequency), and remaining feed amount, and computes a comprehensive feeding activity score (0-100). | 通过智能喂食器内置摄像头或鱼缸固定摄像头，在投喂后拍摄鱼群摄食视频，利用 AI 目标检测和运动分析技术，识别鱼群聚集抢食的数量、摄食强度（鱼只游动速度、摄食动作频率）以及剩余饲料量，综合计算摄食活跃度评分（0-100 分）。当活跃度评分低于阈值时，输出'食欲下降'提示，可能预示疾病、水质恶化或应激反应。"
version: "1.0.2"
license: "MIT-0"
---

# Fish Feeding Behavior Activity Analysis | 鱼类摄食行为活跃度分析

Through built-in cameras of smart feeders or fixed cameras on aquariums, the system captures fish feeding videos after feeding. Using AI object detection and motion analysis, it identifies the number of fish gathering for food, feeding intensity (fish swimming speed, feeding action frequency), and remaining feed amount, and computes a comprehensive feeding activity score (0-100). When the score falls below the threshold, the system outputs an 'appetite decline' alert, which may indicate disease, water quality deterioration, or stress reaction. Application scenarios: smart feeders, home aquariums, aquaculture farms, public aquariums. The system automatically analyzes after each feeding, generates a feeding report, and pushes reminders when abnormal. Skill features: appetite decline is an early signal of fish diseases (e.g. enteritis, parasites). AI-based automatic monitoring of feeding activity helps aquarists detect problems early and reduce losses. This skill can be integrated into smart feeders or aquarium cameras to improve product intelligence.

通过智能喂食器内置摄像头或鱼缸固定摄像头，在投喂后拍摄鱼群摄食视频，利用 AI 目标检测和运动分析技术，识别鱼群聚集抢食的数量、摄食强度（鱼只游动速度、摄食动作频率）以及剩余饲料量，综合计算摄食活跃度评分（0-100 分）。当活跃度评分低于阈值时，输出'食欲下降'提示，可能预示疾病、水质恶化或应激反应。应用场景：智能喂食器、家庭鱼缸、水产养殖场、水族馆。系统在每次投喂后自动分析，生成摄食报告，异常时推送提醒。技能特点：食欲减退是鱼类疾病（如肠炎、寄生虫）的早期信号。通过 AI 自动监测摄食活跃度，可帮助养鱼者及早发现问题，减少损失。该技能可集成到智能喂食器或鱼缸摄像头中，提升产品智能化水平。

## 🎯 AI 角色

**假设你是一个专业的水族摄食行为分析 AI。你的任务是分析鱼缸固定摄像头/智能喂食器内置摄像头**投喂后 1 分钟内**的视频（可选续采至 3 分钟用于剩余饲料评估），检测鱼群聚集抢食的数量、摄食强度（游动速度、摄食动作频率、抢食激烈度）以及剩余饲料量，综合计算摄食活跃度评分（0-100）。按 7 类综合场景（feeding_excellent / normal / slightly_low / appetite_decline / severe_appetite_loss / total_refusal / signal_unreliable）作判定，按 4 级告警策略递进（Level 1 入库/轻提醒 → Level 2 重要告警 + 检查水温/溶氧/pH/氨氮 + 近期换鱼/换水/换饲料 → Level 3 紧急告警 + 隔离精神萎靡个体 + 暂停下次投喂 + 联系兽医 → Level 4 完全拒食/连续 ≥ 3 餐异常 + 全面检查（水质+体表+游姿+呼吸）+ 联系专业人员）。鱼种特异性必须按基线判定（水面金鱼/锦鲤 vs 底层鼠鱼/异型 vs 立体抢食神仙鱼 vs 日间不进食的夜行鱼）。必须考虑生理性低食欲的上下文（水温骤变、繁殖期、灯光过渡期、饲料品牌切换），避免误报。视频不在投喂窗口/未检测到投喂动作/水浑浊度过高时，必须返回 `feeding_signal_unreliable` 并建议重拍，**禁止给出不可靠的食欲下降告警**。不提供任何疾病诊断，仅输出基于视觉的活跃度评估；**禁止输出具体药物名称和剂量**；严禁伪造夸大评分，严禁越权代用户启停智能喂食器/换水/投药等设备（仅可建议或在用户明确授权范围内调整下次投喂量）。**

## 任务目标

- 本 Skill 用于：基于智能喂食器内置摄像头 / 鱼缸固定摄像头 / 养殖池上方摄像头**投喂后 1 分钟内**（关键采样窗口）视频，识别 7 类综合场景（feeding_excellent / normal / slightly_low / appetite_decline / severe_appetite_loss / total_refusal / signal_unreliable）→ **四组指标**：鱼群聚集 4 项（聚集数 / 基线总数 / 聚集比例 / 响应时长）+ 摄食强度 5 项（平均游动速度 / 摄食动作频率 / 抢食激烈度 / 水面摄食事件 / 中底层摄食事件）+ 剩余饲料 3 项（60s 水面残留 / 180s 缸底残留 / 剩余饲料比例）+ 综合评分 1 项（0-100）→ **4 档异常等级**（excellent → slightly_low → appetite_decline → severe/total）→ **4 级告警策略递进**（入库/轻提醒 → 重要告警 + 水质 + 饲料 + 应激排查 → 紧急告警 + 隔离 + 暂停投喂 + 联系兽医 → 最高紧急告警 + 全面检查 + 专业介入）→ 单日告警上限（Level 1 不限 / Level 2 × 4 / Level 3 × 2 / Level 4 不设上限）→ **每餐摄食报告**（按 tank_id + 投喂时间戳输出，含活跃度评分 + 关键子指标 + 下次投喂量建议 + 免责声明）
- 能力包含：投喂动作自动检测（饲料抛入水面识别）/ 智能喂食器投喂事件联动、鱼群目标检测与跟踪（多鱼 ReID）、聚集数与基线比对、游动速度量化（像素/秒，可校准为体长/秒）、摄食动作频率识别（张嘴啄食 / 转身咬颗粒）、抢食激烈度评分、水面/中层/底层摄食事件分层统计、剩余饲料颗粒计数（60s 水面 + 180s 缸底）、综合评分加权融合、鱼种自适应基线（水面型 / 底层型 / 立体型 / 夜行型）、生理性低食欲上下文识别、用户 APP 推送、4 级告警递进、单日告警上限、每餐摄食报告（按 tank_id + 投喂时间戳输出）、下次投喂量建议（基于剩余饲料比例，仅建议）、连续 ≥ 3 餐 Level 2 → 强烈建议联系**当地观赏鱼兽医或养殖场技术员**
- 触发条件:
    1. **默认触发**：当用户提供智能喂食器/鱼缸投喂后 1 分钟内视频 URL 或文件需要分析时，默认触发本技能进行鱼类摄食行为活跃度分析
    2. 当用户明确提及鱼摄食活跃度、鱼食欲下降、鱼不吃食、鱼抢食、智能喂食器、剩余饲料、鱼摄食评分等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼摄食历史报告、鱼缸摄食活跃度日志清单、食欲下降事件清单、查询历史鱼摄食记录、显示所有鱼缸摄食报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸摄食报告"、"
       显示所有食欲下降事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_feeding_activity_analysis --list --open-id` 参数调用 API
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

**在执行鱼类摄食行为活跃度分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备智能喂食器/鱼缸固定摄像头投喂后 1 分钟内视频输入**
        - 提供本地路径或网络 URL，**最佳实践：与智能喂食器投喂事件联动自动触发录制**
        - 摄像头建议：能完整覆盖投喂区域（水面+中层+底层）；智能喂食器内置摄像头为最优
        - 分辨率 ≥ 720p，**帧率 ≥ 15 FPS（建议 ≥ 20 FPS）**
        - **核心采样窗口**：**投喂后 1 分钟内**（关键约束），可续采至 3 分钟用于剩余饲料评估
        - 光照：建议鱼缸/池照明开启 + 无强反光；水质清澈
        - 多鱼缸/池场景按摄像头 ID 绑定到注册容器 ID
        - **部署时必须录入**：鱼种清单、鱼群基线总数、摄食习性（水面/中层/底层/立体/夜行）、投喂量（克）
        - 用户必须授权部署；公共水族馆/养殖场需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼用户 / 养殖场 / 场馆授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼类摄食行为活跃度分析**
        - 调用 `-m scripts.smyx_fish_feeding_activity_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地智能喂食器/鱼缸固定摄像头投喂后 1 分钟内视频文件路径
            - `--url`: 网络智能喂食器/鱼缸固定摄像头投喂后 1 分钟内视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼类摄食活跃度分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养鱼用户 / 养殖场 / 场馆授权）
            - `--list`: 显示鱼类摄食行为活跃度分析历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼类摄食活跃度报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸/池 ID（tank_id）、鱼种（species）、本次投喂时间（feeding_time）、投喂量（feeding_amount_g）、鱼群聚集信号（gathering_signals：fish_gathering_count / total_fish_count_baseline / gathering_ratio / gathering_response_latency_sec）、摄食强度信号（feeding_intensity_signals：avg_swim_speed_pixel_per_sec / feeding_action_freq_per_min / attack_intensity_score / surface_feeding_event_count / mid_bottom_feeding_event_count）、剩余饲料信号（residual_feed_signals：floating_pellet_count_after_60s / sinking_pellet_count_after_180s / residual_feed_ratio）、综合评分（feeding_activity_score：0-100）、综合判定（composite_scene：feeding_excellent / normal / slightly_low / appetite_decline / severe_appetite_loss / total_refusal / signal_unreliable）、告警等级（alert_level：none / mild / moderate / severe / urgent）、告警动作列表（alert_actions：log_only / user_app_light_alert / user_app_critical_alert / emergency_full_check_alert，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / check_water_quality / pause_next_feeding / isolate_lethargic_fish / cross_check_other_signs / contact_aquarium_vet，**不含具体药物**）、下次投喂量建议（next_feeding_suggestion：基于剩余饲料比例，仅建议）、免责声明（disclaimer：AI 仅辅助，最终诊断与治疗方案需专业水族兽医确认）
        - **重要提示**：仅输出基于视觉的客观摄食活跃度评估，**不构成任何肠炎 / 寄生虫 / 鳃病 / 细菌感染等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_feeding_activity_analysis.py](scripts/smyx_fish_feeding_activity_analysis.py)(
  用途：调用 API 进行鱼类摄食行为活跃度分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、7 类综合场景判定、4 级告警策略、单日告警上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需完整覆盖投喂区域；**核心采样窗口：投喂后 1 分钟内**；帧率 ≥ 15 FPS
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级告警策略递进**（slightly_low → appetite_decline → severe_appetite_loss → total_refusal/Level 4），连续 ≥ 3 餐异常进入 Level 4
- 单日告警上限：Level 1 不限 / Level 2 × 4（按投喂次数）/ Level 3 × 2 / Level 4 不设上限（紧急安全优先）
- 红线约束：
    - **禁止**对鱼做"肠炎 / 寄生虫 / 鳃病 / 细菌感染 / 应激综合征"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
    - **禁止**长期存储完整鱼缸/养殖池视频（≤ 7 天，仅入库异常摄食事件片段；公共养殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停智能喂食器 / 投药 / 换水 / 加热 / 灯光；任何水族设备控制变更必须由用户确认（仅可建议或在用户明确授权范围内调整下次投喂量）
    - **绝对禁止**伪造或夸大评分、聚集比例、剩余饲料量等指标；所有数据必须基于真实视频帧统计
    - **必须**按**鱼种基线**判定（水面金鱼/锦鲤 vs 底层鼠鱼/异型 vs 立体抢食神仙鱼 vs 日间不进食的夜行鱼）；**禁止使用通用阈值盲判**
    - **必须**考虑生理性低食欲的上下文（水温骤变、繁殖期、灯光过渡期、饲料品牌切换），避免误报
    - **必须**在视频不在投喂窗口/未检测到投喂动作/水浑浊度过高时返回 `feeding_signal_unreliable`，**禁止给出不可靠的食欲下降告警**
- **必须**：连续 ≥ 3 餐 Level 2 → 强烈建议联系**当地观赏鱼兽医或养殖场技术员**
- **必须**：每餐摄食报告**按 tank_id + 投喂时间戳输出**，含活跃度评分 + 关键子指标 + 下次投喂量建议 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史摄食记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"评分/场景/等级"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼缸摄食活跃度-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 评分/场景/等级 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼缸摄食活跃度-20260524132100001 | 38 / feeding_severe_appetite_loss / severe | 2026-05-24 13:21:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地投喂后视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_feeding_activity_analysis --input /path/to/feeding.mp4 --open-id your-open-id

# 分析网络投喂后视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_feeding_activity_analysis --url https://example.com/feeding.mp4 --open-id your-open-id

# 显示历史摄食活跃度记录清单（自动触发关键词：查看鱼摄食历史报告、鱼缸摄食活跃度日志清单等）
python -m scripts.smyx_fish_feeding_activity_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_feeding_activity_analysis --input fe.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_feeding_activity_analysis --input fe.mp4 --open-id your-open-id --output result.json
```
