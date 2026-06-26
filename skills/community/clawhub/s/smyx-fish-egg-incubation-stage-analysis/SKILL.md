---
name: "smyx-fish-egg-incubation-stage-analysis"
description: "Through breeding-tank fixed cameras (macro lens), the system periodically captures high-definition images of fish eggs and uses AI vision analysis to detect egg color changes (transparent → white / black) and embryonic eye-spots (small black dots), identifying incubation stages (unfertilized / early / mid / late-eyespot / hatching). | 通过繁殖缸固定摄像头（微距镜头），定期拍摄鱼卵的高清图像，利用 AI 视觉分析技术检测鱼卵颜色变化（透明 → 发白/发黑）以及胚胎眼睛点（黑色小点）的出现，识别鱼卵的孵化阶段（未受精/早期/中期/晚期/破壳）。系统定时（如每 6 小时）自动分析，输出孵化阶段及建议（如'已出现眼睛点，预计 24 小时内孵化，准备丰年虾'）。"
version: "1.0.0"
license: "MIT-0"
---

# Fish Egg Incubation Stage Identification | 鱼卵孵化状态识别

Through breeding-tank fixed cameras (macro lens), the system periodically captures high-definition images of fish eggs and uses AI vision analysis to detect egg color changes (transparent → white / black) and embryonic eye-spots (small black dots), identifying incubation stages (unfertilized / early / mid / late-eyespot / hatching). This skill helps ornamental fish breeders track incubation progress and timely separate fry or adjust water quality. Application scenarios: ornamental fish breeding tanks, aquaculture hatcheries, laboratories. The system periodically analyzes (e.g. every 6 hours) and outputs incubation stages plus suggestions (such as 'eye-spots have appeared, hatching expected within 24 hours, prepare brine shrimp'). Skill features: incubation period is a critical stage of ornamental fish breeding — separating fry too early causes death, while separating too late risks the parent fish eating the fry. AI-based automatic recognition of eye-spots and color changes helps novice breeders easily grasp the right timing and reduce failure rate. This skill can be integrated into smart breeding tanks or mobile macro lenses, becoming a breeding assistant for ornamental fish enthusiasts.

通过繁殖缸固定摄像头（微距镜头），定期拍摄鱼卵的高清图像，利用 AI 视觉分析技术检测鱼卵颜色变化（透明 → 发白/发黑）以及胚胎眼睛点（黑色小点）的出现，识别鱼卵的孵化阶段（未受精/早期/中期/晚期/破壳）。该技能有助于观赏鱼繁殖者掌握孵化进度，及时分离鱼苗或调整水质。应用场景：观赏鱼繁殖缸、水产育苗场、实验室。系统定时（如每 6 小时）自动分析，输出孵化阶段及建议（如'已出现眼睛点，预计 24 小时内孵化，准备丰年虾'）。技能特点：鱼卵孵化期是观赏鱼繁殖的关键阶段，过早分离鱼苗会导致死亡，过晚则可能被种鱼吞食。通过 AI 自动识别眼睛点和颜色变化，可帮助新手繁殖者轻松掌握时机，降低失败率。该技能可集成到智能繁殖缸或手机微距镜头中，成为观赏鱼爱好者的繁殖助手。

## 🎯 AI 角色

**假设你是一个专业的水产繁育 AI。你的任务是分析鱼卵的微距图像（≥ 3 倍光学微距，分辨率 ≥ 1080p），检测卵的颜色变化（透明 → 发白/灰白 → 发黑）以及胚胎眼睛点（黑色小点，<0.3 mm）的出现，并结合**鱼种 + 水温 + 距产卵时长**联合判定 8 类孵化阶段（incubation_unfertilized / early / mid / late_eyespot / pre_hatch / hatching / mass_failure / signal_unreliable），按 4 级提醒策略递进（Level 1 进度更新 → Level 2 重要提示 + 准备丰年虾/草履虫/分离亲鱼 → Level 3 紧急提示 + 停止充气避免吸入幼苗 + 隔离 → Level 4 大面积失败 + 清理坏卵防霉 + 检查亲鱼/水温/光照）。鱼种特异性必须按基线判定（斑马鱼 48-72h 透明小卵 vs 神仙鱼 60-72h 黄褐色粘性卵 vs 七彩 60-72h 黄色卵 vs 锦鲤 96-120h@20℃ vs 鼠鱼银白色卵），**严禁通用阈值盲判**。必须做白平衡校正避免"背光偏色让透明卵看起来发白"的误判。焦距未对准 / 卵团遮挡 / 浑浊度过高时必须返回 `incubation_signal_unreliable` 并建议重拍/对焦/补光。不提供任何疾病诊断，仅输出基于视觉的孵化阶段分类；**严禁推荐甲基蓝、二氯异氰尿酸钠等防霉化学药物**，**严禁输出具体药物名称和剂量**；严禁伪造夸大颜色比例 / 眼睛点检出率；严禁越权代用户启停加热棒/增氧/换水/灯光（仅建议）。**

## 任务目标

- 本 Skill 用于：基于繁殖缸固定摄像头 / 微距镜头（≥ 3× 光学微距）/ 智能繁殖缸内置微距**定时拍摄**（默认每 6 小时 ≥ 1 张），识别 8 类孵化阶段（incubation_unfertilized / early / mid / late_eyespot / pre_hatch / hatching / mass_failure / signal_unreliable）→ **三组指标**：卵颜色 5 项（卵总数 / 透明比例 / 发白比例 / 发黑比例 / 黄色卵黄囊比例）+ 胚胎发育 4 项（眼睛点检出数 / 检出比例 / 胚胎抽动 / 破壳事件）+ 上下文与基线 4 项（鱼种 / 鱼种基线孵化时长 / 当前水温 / 距产卵时长）→ 4 档提醒级别（info / important / urgent / warning）→ **4 级提醒策略递进**（仅入库进度更新 → 准备丰年虾分离亲鱼 → 停止充气+隔离 → 大面积失败建议清理坏卵+检查亲鱼水温光照）→ 单日提醒上限（Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 × 2）→ **每次定时分析的孵化阶段报告**（按 tank_id + spawn_time 输出，含颜色分布 + 眼睛点检出率 + 预计破壳时间窗 + 建议动作 + 免责声明）
- 能力包含：鱼卵小目标检测（直径 0.5-2 mm）、卵分类（透明 / 发白 / 发黑 / 含黄色卵黄囊）、**胚胎眼睛点检测**（黑色亚毫米小点）、胚胎抽动光流检测、破壳事件识别（卵壳破裂 + 鱼苗游出）、鱼种自适应基线（孵化时长 + 卵颜色基线）、**水温修正的孵化龄估算**（Q10 系数粗校正）、白平衡校正（避免背光偏色误判）、用户 APP 推送、4 级提醒递进、单日提醒上限、每次定时分析的孵化阶段报告（按 tank_id + spawn_time 输出）、预计破壳时间窗给出（"24h 内孵化"等开口饵料准备提示）、**侧重育苗助手定位**（非健康告警，更偏积极进度提示）
- 触发条件:
    1. **默认触发**：当用户提供繁殖缸固定摄像头/微距镜头鱼卵高清图像或视频 URL/文件需要分析时，默认触发本技能进行鱼卵孵化状态识别
    2. 当用户明确提及鱼卵孵化、眼睛点、丰年虾准备、未受精卵、坏卵清理、亲鱼分离、破壳等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼卵孵化历史报告、繁殖缸孵化进度日志清单、孵化阶段事件清单、查询历史鱼卵记录、显示所有繁殖缸孵化报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有繁殖缸孵化报告"、"
       显示所有孵化阶段事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_egg_incubation_stage_analysis --list --open-id` 参数调用 API
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

**在执行鱼卵孵化状态识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备繁殖缸固定摄像头/微距镜头鱼卵高清图像输入**
        - 提供本地路径或网络 URL，支持图像（jpg/png）或视频
        - 摄像头建议：**≥ 3 倍光学微距 + 冷白补光 + 透过卵层背光**；分辨率 ≥ 1080p
        - 拍摄角度：俯拍卵团或正侧面贴近卵层，焦距对准卵团中心；建议每 6 小时 ≥ 1 张
        - 光照：避免直射强光；水质清澈无杂质
        - 视频会自动抽帧进行卵层分析
        - 多繁殖缸场景按摄像头 ID 绑定到注册繁殖缸 ID
        - **部署时必须录入**：鱼种（决定孵化总时长基线，如斑马鱼 48-72h / 神仙鱼 60-72h / 七彩 60-72h / 锦鲤 96-120h@20℃）、**产卵时间戳**（用于换算孵化龄）、当前水温
        - 用户必须授权部署；公共育苗场/实验室需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（繁殖者 / 育苗场 / 实验室授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼卵孵化状态识别**
        - 调用 `-m scripts.smyx_fish_egg_incubation_stage_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地繁殖缸固定摄像头/微距镜头鱼卵高清图像或视频文件路径
            - `--url`: 网络繁殖缸固定摄像头/微距镜头鱼卵高清图像或视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼卵孵化状态识别场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，繁殖者 / 育苗场 / 实验室授权）
            - `--list`: 显示鱼卵孵化状态识别历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼卵孵化阶段报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、繁殖缸 ID（tank_id）、鱼种（species）、产卵时间戳（spawn_time）、当前水温（water_temperature_c）、距产卵时长（hours_since_spawn）、卵颜色信号（egg_color_signals：egg_count_total / egg_transparent_ratio / egg_white_opaque_ratio / egg_black_dead_ratio / egg_yellow_yolk_visible_ratio）、胚胎发育信号（embryo_signals：eye_spot_detected_count / eye_spot_detected_ratio / embryo_movement_detected / hatching_event_detected）、综合场景判定（composite_scene：incubation_unfertilized / early / mid / late_eyespot / pre_hatch / hatching / mass_failure / signal_unreliable）、**预计破壳时间窗**（estimated_hatching_window_hours）、提醒等级（alert_level：info / important / urgent / warning）、提醒动作列表（alert_actions：progress_update / prepare_brine_shrimp / stop_aeration_isolate_fry / cleanup_dead_eggs，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / prepare_brine_shrimp / prepare_paramecium / separate_parent_fish / stop_aeration / cleanup_dead_eggs / check_parent_health_water_temp_light，**不含具体化学药物**）、免责声明（disclaimer：AI 仅辅助，最终繁殖决策需用户结合现场或专业繁殖者意见）
        - **重要提示**：仅输出基于视觉的客观孵化阶段分类，**不构成任何水霉感染 / 真菌污染 / 受精率不足等具体疾病或繁殖学诊断**；**绝对不输出甲基蓝、二氯异氰尿酸钠等防霉化学药物名称、剂量、给药方案**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_egg_incubation_stage_analysis.py](scripts/smyx_fish_egg_incubation_stage_analysis.py)(
  用途：调用 API 进行鱼卵孵化状态识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、三组指标、8 类孵化阶段判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；摄像头需 **≥ 3× 光学微距 + 冷白补光 + 透过卵层背光**；分辨率 ≥ 1080p；建议每 6 小时定时 ≥ 1 张
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级提醒策略递进**（info → important → urgent → warning），偏育苗助手定位（非健康告警）
- 单日提醒上限：Level 1 不限 / Level 2 × 4 / Level 3 × 6（破壳事件可能密集）/ Level 4 × 2
- 红线约束：
    - **禁止**做"水霉感染 / 真菌污染 / 受精率不足 / 亲鱼不孕"等具体疾病或繁殖学诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（特别**严禁推荐甲基蓝、二氯异氰尿酸钠等防霉化学剂**）
    - **禁止**长期存储完整鱼缸视频/图像（≤ 14 天，仅入库孵化阶段事件帧；公共育苗场/实验室按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大颜色比例、眼睛点检出比例、孵化进度等指标；所有数据必须基于真实图像识别
    - **必须**按**鱼种 + 水温**联合判定基线（斑马鱼 48-72h 透明小卵 / 神仙鱼 60-72h 黄褐色 / 七彩 60-72h 黄色 / 锦鲤 96-120h@20℃ / 鼠鱼银白色卵）；**禁止使用通用阈值盲判**
    - **必须**做白平衡校正，避免"背光偏色让透明卵看起来发白"导致的未受精误判
    - **必须**在焦距未对准 / 卵团遮挡 / 浑浊度过高时返回 `incubation_signal_unreliable`，**禁止给出不可靠的失败/未受精判定**
- **必须**：每次定时分析的孵化阶段报告**按 tank_id + spawn_time 输出**，含颜色分布 + 眼睛点检出率 + 预计破壳时间窗 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史孵化记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"阶段/眼睛点率/预计破壳"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`繁殖缸孵化-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 阶段/眼睛点率/预计破壳 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 繁殖缸孵化-20260524152000001 | late_eyespot / 68% / 约 18 小时 | 2026-05-24 15:20:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地鱼卵微距图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_egg_incubation_stage_analysis --input /path/to/eggs.jpg --open-id your-open-id

# 分析网络鱼卵微距图像/视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_egg_incubation_stage_analysis --url https://example.com/eggs.jpg --open-id your-open-id

# 显示历史孵化状态记录清单（自动触发关键词：查看鱼卵孵化历史报告、繁殖缸孵化进度日志清单等）
python -m scripts.smyx_fish_egg_incubation_stage_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_egg_incubation_stage_analysis --input eggs.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_egg_incubation_stage_analysis --input eggs.jpg --open-id your-open-id --output result.json
```
