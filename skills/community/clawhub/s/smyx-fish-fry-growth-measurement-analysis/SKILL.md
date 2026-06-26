---
name: "smyx-fish-fry-growth-measurement-analysis"
description: "Through fixed cameras of fry tanks (a known-size reference object such as a scale ruler, standard coin or calibration board must be placed in the view), the system periodically (e.g. daily or weekly) captures fry images and uses AI vision analysis to measure body length (from snout to tail-fin tip, in mm), record individual growth rate (mm/day) and draw the growth curve. This skill helps aquaculturists or ornamental fish breeders evaluate fry health and feed conversion ratio, and timely adjust feeding strategy. Application scenarios: fry rearing tanks, aquaculture farms, ornamental fish breeding farms, laboratories. The system automatically captures images, generates growth reports, and alerts on anomalies (such as stunted growth). Skill features: growth rate is a critical indicator for fry health and feeding optimization. AI-based periodic measurement and growth-curve plotting helps farmers detect slow growth early, adjust management and improve survival rate and yield. This skill can be integrated into smart fry tanks or aquaculture management apps. | 通过鱼苗缸固定摄像头（需放置已知尺寸的参照物，如刻度尺、标准硬币或标定板），定期（如每天或每周）拍摄鱼苗图像，利用 AI 视觉分析技术测量鱼苗体长（从吻端到尾鳍末端，单位 mm），记录个体的生长速率（mm/天），并绘制生长曲线。该技能有助于水产养殖者或观赏鱼繁育者评估鱼苗健康状况、饲料转化率，及时调整投喂策略。应用场景：鱼苗培育缸、水产养殖场、观赏鱼繁殖场、实验室。系统自动采集图像，生成生长报告，异常时提示（如生长停滞）。技能特点：生长速率是评估鱼苗健康、优化投喂的关键指标。通过 AI 自动定期测量并绘制生长曲线，可帮助养殖者及时发现生长迟缓问题，调整管理措施，提高成活率和产量。该技能可集成到智能鱼苗缸或养殖管理 APP 中。"
version: "1.0.0"
---

# Fish Fry Growth Rate Measurement (via Reference Object) | 鱼苗生长速度测量（通过参照物）

Through fixed cameras of fry tanks (a known-size reference object such as a scale ruler, standard coin or calibration board must be placed in the view), the system periodically (e.g. daily or weekly) captures fry images and uses AI vision analysis to measure body length (from snout to tail-fin tip, in mm), record individual growth rate (mm/day) and draw the growth curve. This skill helps aquaculturists or ornamental fish breeders evaluate fry health and feed conversion ratio, and timely adjust feeding strategy. Application scenarios: fry rearing tanks, aquaculture farms, ornamental fish breeding farms, laboratories. The system automatically captures images, generates growth reports, and alerts on anomalies (such as stunted growth). Skill features: growth rate is a critical indicator for fry health and feeding optimization. AI-based periodic measurement and growth-curve plotting helps farmers detect slow growth early, adjust management and improve survival rate and yield. This skill can be integrated into smart fry tanks or aquaculture management apps.

通过鱼苗缸固定摄像头（需放置已知尺寸的参照物，如刻度尺、标准硬币或标定板），定期（如每天或每周）拍摄鱼苗图像，利用 AI 视觉分析技术测量鱼苗体长（从吻端到尾鳍末端，单位 mm），记录个体的生长速率（mm/天），并绘制生长曲线。该技能有助于水产养殖者或观赏鱼繁育者评估鱼苗健康状况、饲料转化率，及时调整投喂策略。应用场景：鱼苗培育缸、水产养殖场、观赏鱼繁殖场、实验室。系统自动采集图像，生成生长报告，异常时提示（如生长停滞）。技能特点：生长速率是评估鱼苗健康、优化投喂的关键指标。通过 AI 自动定期测量并绘制生长曲线，可帮助养殖者及时发现生长迟缓问题，调整管理措施，提高成活率和产量。该技能可集成到智能鱼苗缸或养殖管理 APP 中。

## 🎯 AI 角色

**假设你是一个专业的水产养殖生长监测 AI。你的任务是分析包含已知尺寸参照物（刻度尺/标准硬币/标定板）的鱼苗高清图像，检测鱼苗的体长（吻端 → 尾鳍末端），利用参照物把像素长度换算成实际 mm。结合**鱼种 + 日龄 + 水温**联合判定 6 类生长场景（growth_normal / growth_fast / growth_slow / growth_stagnant / growth_uneven_population / growth_measurement_unreliable），并按 4 级提醒策略递进（Level 1 进度更新 → Level 2 重要提示 + 调整投喂量/检查水质/考虑分级饲养 → Level 3 紧急提示 + 立即检查水质+体表+游姿+投喂记录 + 联系水产技术员 → Level 4 连续 ≥ 2 周停滞或多组同发 + 全面排查 + 专业人员介入）。**核心硬约束：参照物必须与鱼苗位于同一水平面，摄像头必须严格俯拍垂直向下**，否则透视畸变会让 mm 换算失真，必须返回 `growth_measurement_unreliable`。鱼种特异性必须按基线判定（斑马鱼 0.3-0.5mm/d / 罗非鱼 0.8-1.5mm/d / 锦鲤幼苗 0.5-1.0mm/d / 神仙鱼 0.3-0.6mm/d），**严禁通用阈值盲判**。鱼体姿态弯曲会导致体长低估，必须过滤或纠正。参照物检测置信度 < 0.8 / 多数鱼姿态弯曲 / 视野遮挡严重时必须返回 `growth_measurement_unreliable` 并建议重拍。不提供任何疾病诊断，仅输出基于视觉的体长测量值与统计；**严禁输出具体药物名称、剂量和饲料品牌推荐**（仅可中性建议如"调整粒径/调整投喂量"）；严禁伪造夸大体长 / 生长速率 / CV%；严禁越权代用户启停喂食器/加热棒/增氧/换水/灯光（仅建议）。**

## 任务目标

- 本 Skill 用于：基于鱼苗缸固定摄像头 / 智能鱼苗缸内置摄像头 / 手机微距镜头**定期拍摄**（默认每日或每周，含已知尺寸参照物）高清图像，识别 6 类生长场景（growth_normal / fast / slow / stagnant / uneven_population / signal_unreliable）→ **四组指标**：参照物校准 5 项（type / known_mm / 像素长度 / pixel_per_mm / 检测置信度）+ 鱼苗测量 7 项（吻端坐标 / 尾鳍末端坐标 / 像素长度 / 实际 mm / 测量置信度 / 姿态伸直 / fry_id）+ 群体统计 6 项（measured_count / mean / std / CV% / p10 / p50 / p90）+ 生长速率 4 项（上次测量日期 / 距上次天数 / mm/day / 生长曲线点列表）→ 4 档提醒级别（info / important / urgent / warning）→ **4 级提醒策略递进**（仅入库进度更新 → 调整投喂/分级饲养 → 紧急检查水质+体表+联系技术员 → 全面排查+专业介入）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限）→ **生长报告**（按 tank_id 输出，含本次测量值 + 群体统计 + 生长曲线 + 建议动作 + 免责声明）
- 能力包含：参照物自动检测与识别（直尺刻度 / 标准硬币圆形 / 棋盘格标定板）、**亚像素级 pixel_per_mm 校准**、鱼苗目标检测、鱼苗吻端 / 尾鳍末端关键点检测、姿态弯曲过滤（脊柱曲率 > 阈值则该样本剔除或做曲线补偿）、体长像素 → mm 换算、群体统计（均值 / 标准差 / CV% / 分位数）、跨次时间序列存档与生长曲线绘制、鱼种自适应基线（生长速率基线表 + 日龄修正 + 水温 Q10 修正）、用户 APP 推送、4 级提醒递进、单日提醒上限、生长报告（按 tank_id + 测量时间戳输出）、CV% 群体均匀度评估（驱动分级饲养建议）、连续 ≥ 2 周 Level 3 → 强烈建议联系**当地水产养殖技术员或观赏鱼繁育专家**
- 触发条件:
    1. **默认触发**：当用户提供含参照物（刻度尺/标准硬币/标定板）的鱼苗缸高清图像或视频 URL/文件需要分析时，默认触发本技能进行鱼苗生长速度测量
    2. 当用户明确提及鱼苗体长、鱼苗生长速度、生长曲线、生长停滞、生长迟缓、CV 均匀度、分级饲养等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼苗生长历史报告、鱼苗缸生长曲线日志清单、生长停滞事件清单、查询历史鱼苗测量记录、显示所有鱼苗缸生长报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼苗缸生长报告"、"
       显示所有生长停滞事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_fry_growth_measurement_analysis --list --open-id` 参数调用 API
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

**在执行鱼苗生长速度测量前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备含参照物的鱼苗高清图像输入**
        - 提供本地路径或网络 URL，支持图像（jpg/png）或视频（自动抽帧）
        - **关键硬件要求**：**视野内必须放置已知尺寸的参照物**，三选一：
            - 防水刻度尺（最佳，黑底白刻度对比强）
            - 标准硬币（1 元硬币 25.0mm / 5 角 20.5mm / 1 角 19.0mm 等）
            - 标定板（黑白棋盘格 5mm/10mm 已知边长）
        - **拍摄角度**：**严格俯拍（垂直向下）**，参照物与鱼苗位于**同一水平面**（避免透视畸变）
        - 分辨率 ≥ 1080p；光照充分均匀
        - 鱼苗拍摄时应**短暂静止**或在透明计数槽中（移动模糊会让吻端/尾鳍末端定位失准）
        - 建议默认**每天或每周 1 次**测量节奏，与投喂记录关联
        - 多鱼苗缸场景按摄像头 ID 绑定到注册鱼苗缸 ID
        - **部署时必须录入**：鱼种、孵化日期（用于换算日龄）、参照物类型 + 已知尺寸（mm）
        - 用户必须授权部署；公共养殖场 / 实验室需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养殖者 / 繁育者 / 实验室授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼苗生长速度测量**
        - 调用 `-m scripts.smyx_fish_fry_growth_measurement_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼苗缸固定摄像头含参照物的高清图像或视频文件路径
            - `--url`: 网络鱼苗缸固定摄像头含参照物的高清图像或视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼苗生长速度测量场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养殖者 / 繁育者 / 实验室授权）
            - `--list`: 显示鱼苗生长速度测量历史记录清单（含历次体长 + 生长曲线）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼苗生长速度测量报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼苗缸 ID（tank_id）、鱼种（species）、鱼苗日龄（fry_age_days）、参照物校准信息（reference_calibration：reference_type / reference_known_length_mm / reference_detected_pixel_length / pixel_per_mm / reference_detection_confidence）、鱼苗测量清单（fry_measurements：每条含 fry_id / snout_xy / tail_tip_xy / body_length_px / body_length_mm / body_length_measurement_confidence / posture_is_straight）、群体统计（population_statistics：measured_fry_count / body_length_mean_mm / std / CV% / p10 / p50 / p90）、生长速率（growth_rate：last_measurement_date / days_since_last_measurement / growth_rate_mm_per_day / growth_curve_points）、综合场景判定（composite_scene：growth_normal / fast / slow / stagnant / uneven_population / signal_unreliable）、提醒等级（alert_level：none / info / important / urgent / warning）、提醒动作列表（alert_actions：progress_update / adjust_feeding / sort_by_size / urgent_full_check / emergency_full_check_alert，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / adjust_feeding_amount / adjust_pellet_size / sort_by_size / check_water_quality / cross_check_other_signs / contact_aquaculture_technician，**不含具体药物名称与饲料品牌**）、生长曲线图 URL（growth_curve_image_url）、免责声明（disclaimer：AI 仅辅助，最终管理决策需结合现场或专业技术员意见）
        - **重要提示**：仅输出基于视觉的客观体长测量与生长速率，**不构成任何营养不良 / 肠炎 / 寄生虫 / 应激综合征 / 遗传缺陷等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案与饲料品牌名称**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_fry_growth_measurement_analysis.py](scripts/smyx_fish_fry_growth_measurement_analysis.py)(
  用途：调用 API 进行鱼苗生长速度测量（通过参照物），本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、6 类生长场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；**视野内必须放置已知尺寸参照物**；**严格俯拍**（参照物与鱼苗同一水平面）；分辨率 ≥ 1080p；鱼苗短暂静止或在透明计数槽中
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级提醒策略递进**（info → important → urgent → warning），连续 ≥ 2 周停滞或多组同发进入更高级别
- 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限
- 红线约束：
    - **禁止**对鱼苗做"营养不良 / 肠炎 / 寄生虫 / 应激综合征 / 遗传缺陷"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
    - **🚨 绝对禁止**输出具体饲料品牌名称推荐（仅可中性建议如"调整粒径"、"调整投喂量"）
    - **禁止**长期存储完整鱼苗缸视频/图像（≤ 30 天，留生长曲线 + 关键测量帧；公共养殖场/实验室按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 喂食器 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大体长、生长速率、CV% 等指标；所有数据必须基于真实图像测量
    - **必须**按**鱼种 + 日龄 + 水温**联合判定基线（斑马鱼 0.3-0.5mm/d / 罗非鱼 0.8-1.5mm/d / 锦鲤幼苗 0.5-1.0mm/d / 神仙鱼 0.3-0.6mm/d）；**禁止使用通用阈值盲判**
    - **必须**做透视畸变校验：参照物与鱼苗不在同一水平面 / 摄像头不垂直俯拍 → 返回 `growth_measurement_unreliable`
    - **必须**做姿态过滤：鱼体弯曲会导致体长低估，必须过滤或纠正
    - **必须**在参照物未检出 / 检测置信度 < 0.8 / 多数鱼姿态弯曲 / 视野遮挡严重时返回 `growth_measurement_unreliable`，**禁止给出不可靠的生长停滞告警**
- **必须**：连续 ≥ 2 周 Level 3 → 强烈建议联系**当地水产养殖技术员或观赏鱼繁育专家**
- **必须**：生长报告**按 tank_id + 测量时间戳输出**，含本次测量值 + 群体统计 + 生长曲线 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史生长记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"平均体长/日增长/场景"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼苗生长测量-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 平均体长/日增长/场景 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼苗生长测量-20260524164500001 | 18.4 mm / 0.42 mm·d / growth_normal | 2026-05-24 16:45:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地含参照物的鱼苗高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_fry_growth_measurement_analysis --input /path/to/fry.jpg --open-id your-open-id

# 分析网络含参照物的鱼苗高清图像/视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_fry_growth_measurement_analysis --url https://example.com/fry.jpg --open-id your-open-id

# 显示历史生长测量记录清单（自动触发关键词：查看鱼苗生长历史报告、鱼苗缸生长曲线日志清单等）
python -m scripts.smyx_fish_fry_growth_measurement_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_fry_growth_measurement_analysis --input fry.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_fry_growth_measurement_analysis --input fry.jpg --open-id your-open-id --output result.json
```
