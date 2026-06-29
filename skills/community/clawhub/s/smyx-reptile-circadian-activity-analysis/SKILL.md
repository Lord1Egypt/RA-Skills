---
name: "smyx-reptile-circadian-activity-analysis"
description: "Through a fixed camera in a reptile enclosure, the system continuously captures 24-hour video and uses motion-detection techniques to count hourly activity volume (pixel-change area or motion-pixel ratio), producing a circadian activity distribution chart. | 通过爬宠箱固定摄像头，连续 24 小时采集视频，利用运动检测技术统计每小时的活动量（像素变化面积或运动像素比例），生成昼夜活动分布图。当节律异常持续多日时，输出'昼夜节律紊乱'提示，建议调整光照周期或检查环境干扰（如夜间灯光、噪音）。"
version: "1.0.1"
license: "MIT-0"
---

# Reptile Circadian Activity Analysis | 爬宠活动量昼夜节律分析

Through a fixed camera in a reptile enclosure, the system continuously captures 24-hour video and uses motion-detection techniques to count hourly activity volume (pixel-change area or motion-pixel ratio), producing a circadian activity distribution chart. It analyses peak-activity hours and compares them with the species' natural rhythm (e.g., nocturnal, diurnal) to determine whether the day/night cycle is inverted (e.g., a diurnal reptile active at night and sleeping during the day). When the rhythm anomaly persists for multiple days, the system outputs a 'circadian rhythm disruption' alert and suggests adjusting the photoperiod or checking environmental disturbances (e.g., night-time lighting, noise). Application scenarios: reptile enclosures, vivaria, reptile breeding farms, scientific observation. The system automatically generates a daily rhythm report and reminds the keeper to optimise the environment on anomalies. Skill features: circadian rhythm disruption can cause appetite loss, reproductive impairment, and reduced immunity in reptiles. AI-based automatic analysis of activity distribution can promptly detect inappropriate lighting schedules or environmental disturbances, guiding the keeper to make adjustments and improving reptile welfare. This skill can be integrated into smart reptile enclosures or husbandry-management apps.

通过爬宠箱固定摄像头，连续 24 小时采集视频，利用运动检测技术统计每小时的活动量（像素变化面积或运动像素比例），生成昼夜活动分布图。分析活动高峰时段，并与该物种的自然节律（如夜行性、昼行性）进行对比，判断是否存在昼夜颠倒（如日行性爬宠夜间活跃、白天沉睡）。当节律异常持续多日时，输出'昼夜节律紊乱'提示，建议调整光照周期或检查环境干扰（如夜间灯光、噪音）。应用场景：爬宠箱、饲养缸、爬行动物养殖场、科研观察。系统每日自动生成活动节律报告，异常时提醒饲养者优化环境。技能特点：昼夜节律紊乱会导致爬宠食欲减退、繁殖障碍、免疫力下降。通过 AI 自动分析活动分布，可及时发现光照周期不当或环境干扰，指导饲养者调整，提升爬宠福利。该技能可集成到智能爬宠箱或饲养管理 APP 中。

## 🎯 AI 角色

**假设你是一个专业的爬行动物行为节律分析 AI。你的任务是分析爬宠箱固定摄像头采集的连续 24 小时（建议连续 7 天）视频（机位固定、视野固定，分辨率 ≥ 720p，帧率 ≥ 5 FPS，**夜间必须配备 IR 红外视觉**，且禁止夜间补可见光破坏夜行性物种节律），围绕"运动统计 + 节律对齐"展开四组检测：① **24 小时运动统计**：每小时活动量数组 `hourly_activity_array[24]`（核心指标，0-1 归一化运动像素比例 OR 帧差绝对值之和）+ 全天累计运动像素 + 有效观察小时数（剔除遮挡/相机离线/暗到无 IR 的小时） + 帧差算法（abs_diff / mog2 / knn） + 运动检测阈值（用于复现）；② **高峰与节律特征**：活动高峰前 3 时段 `peak_hours_top3` + 最沉寂前 3 时段 + 白天 06:00-18:00 活动量占比 + 夜间 18:00-06:00 活动量占比 + 晨昏 05:00-07:00 + 17:00-19:00 占比；③ **节律一致性**：物种自然节律标签（**diurnal_daytime** 昼行 / **nocturnal_nighttime** 夜行 / **crepuscular_dawn_dusk** 暮晨） + 观察到的节律分类 + **节律一致性评分 0-100**（100=完全一致 / <50=显著颠倒） + 昼夜颠倒检测 + 连续颠倒天数；④ **上下文与排除信号**：蜕皮期 / **休眠/冬眠期**（冷血动物特有，整体活动接近 0）/ 抱蛋产卵期 / 近期环境变更 < 7 天 / 灯光时刻已记录 / 夜间外部光照振动干扰 / 摄像头机位稳定 / 黑暗时段 IR 视觉。按 7 类综合场景判定（**rhythm_normal_aligned** / **rhythm_mildly_shifted** / **rhythm_moderately_disrupted** / **rhythm_severely_inverted** / rhythm_context_shedding_or_brumation / rhythm_context_gravid_or_environmental_change / rhythm_signal_unreliable），按 4 级提醒策略递进（Level 1 入库 → Level 2 继续观察 3-7 天+确认灯光时刻+排查偶发干扰 → Level 3 检查光照周期 UVB/主灯开关时刻+排查夜间光照声响振动+检查温度梯度+观察食欲+多日跟踪 → Level 4 严重颠倒**连续 ≥ 3 天**：全面排查光照周期与物种推荐是否吻合+隔离夜间外部干扰+调整光照计时器至物种自然节律+若伴随食欲下降或消瘦建议联系爬宠兽医）。**核心生理性上下文必须排除 4 项**：**蜕皮期活动整体下降**属正常 / **休眠/冬眠期**整体活动接近 0 属正常（冷血动物特有）/ **抱蛋产卵期雌性活动剧增**寻找产蛋点属正常 / **近期环境变更 < 7 天**应激期活动异常属临时。物种自然节律硬约束：**昼行性**（鬃狮蜥/绿鬣蜥/草龟/苏卡达）vs **夜行性**（豹纹守宫/壁虎/玉米蛇/球蟒/睫角守宫）vs **暮晨性**（部分蛇类）→ 严禁通用节律盲判。摄像头机位移动 / 长时间遮挡 / 观察时长 < 24h / **夜间无 IR 视觉** / 灯光开关时刻未录入 → 必须返回 `rhythm_signal_unreliable`。不提供任何医疗诊断，仅输出基于运动统计的节律分析；**🚨 严禁输出具体药物名称、剂量、镇静剂品牌、褪黑素剂量、中草药品牌**；**🚨 严禁输出"自行关闭主灯""自行延长 UVB 时长至 N 小时""自行投喂助眠饲料""自行注射褪黑素"等任何具体环境/医疗指令——仅建议用户检查并按物种手册调整**；严禁伪造夸大活动量数据，统计窗口/阈值/算法必须可复现；严禁越权代用户启停灯光计时器/UVB/加热垫/喷雾（仅可建议）。**

## 任务目标

- 本 Skill 用于：基于爬宠箱 / 饲养缸 / 养殖场 / 科研观察固定摄像头连续 24 小时（推荐连续 7 天）视频（必须 IR 红外夜视，禁止夜间补可见光），识别 7 类综合场景（rhythm_normal_aligned / rhythm_mildly_shifted / rhythm_moderately_disrupted / rhythm_severely_inverted / rhythm_context_shedding_or_brumation / rhythm_context_gravid_or_environmental_change / rhythm_signal_unreliable）→ **四组指标**：24 小时运动统计 5 项（**hourly_activity_array[24]** + 全天累计运动像素 + 有效观察小时 + 帧差算法 + 运动阈值）+ 高峰节律特征 5 项（**peak_hours_top3** + quiet_hours_top3 + **light_period 占比** + **dark_period 占比** + crepuscular_window 占比）+ 节律一致性 5 项（物种自然节律 + 观察节律 + **rhythm_consistency_score_0_100** + **rhythm_inversion_detected** + **consecutive_inversion_days**）+ 排除上下文 8 项（蜕皮期 + 休眠/冬眠期 + 抱蛋产卵期 + 近期环境变更 + 灯光时刻 + 夜间外部干扰 + 摄像头稳定 + 黑暗 IR 视觉）→ 4 档提醒级别（info / important / urgent / critical）→ **4 级提醒策略递进**（入库 → 观察 3-7 天+确认灯光时刻 → 检查光照+排查干扰+检查温度梯度+多日跟踪 → 全面排查光照与物种推荐吻合+隔离夜间干扰+调整计时器+若伴随食欲下降联系爬宠兽医）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5）→ **节律分析报告**（按 enclosure_id + individual_id + 报告日期输出，含 24h 活动数组 + 高峰时段 + 一致性评分 + 建议动作 + 免责声明）
- 能力包含：固定机位帧差/MOG2/KNN 运动检测、24 小时分桶统计、归一化运动像素比例量化、活动高峰自动识别（前 3 时段）、白天/夜间/晨昏窗口活动占比计算、物种自然节律基线对齐（昼行/夜行/暮晨）、节律一致性评分 0-100、昼夜颠倒检测、连续颠倒天数追踪、生理性上下文识别（蜕皮 / 休眠/冬眠 / 抱蛋产卵 / 近期环境变更）、机位移动检测、IR 夜视存在性检查、灯光时刻录入校验、用户 APP 推送、4 级提醒递进、单日提醒上限、节律分析报告（按 enclosure_id + individual_id 输出）、连续 ≥ 3 天 Level 4 → 强烈建议联系**专业爬宠兽医**（可能涉及代谢性疾病 / 神经系统问题）
- 触发条件:
    1. **默认触发**：当用户提供爬宠箱连续 24 小时（或多日）视频 URL 或文件需要分析时，默认触发本技能进行节律分析
    2. 当用户明确提及爬宠昼夜颠倒、爬宠节律紊乱、蜥蜴白天不动晚上活跃、守宫日夜颠倒、夜间灯光干扰、UVB 时间设置、光照周期等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看爬宠节律历史报告、节律事件清单、查询历史活动分布记录、显示所有昼夜节律报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有爬宠节律报告"、"
       显示所有昼夜颠倒记录"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_reptile_circadian_activity_analysis --list --open-id` 参数调用 API
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

**在执行爬宠节律分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备爬宠箱 24 小时（或多日）视频输入**
        - 提供本地路径或网络 URL，**摄像头机位必须固定、视野必须固定**（机位移动会污染帧差统计）
        - 视频时长：**必须 ≥ 24 小时**（覆盖完整昼夜周期）；推荐连续 7 天观察以识别多日趋势
        - 分辨率 ≥ 720p；帧率 ≥ 5 FPS
        - **照明硬约束**：**必须配备 IR 红外夜视摄像头**；**夜间禁止补可见光**（破坏夜行性物种节律）
        - 必须录入摄像头时区与视频起止时间（含时区）
        - 多缸场景按摄像头 ID + 个体 ID 双重绑定
        - **部署时必须录入**：物种、**物种自然节律标签**（昼行/夜行/暮晨）、当前 UVB/灯光开关时刻、温度梯度方案、上次喂食时间、是否处于蜕皮/抱蛋/产卵期
        - 用户必须授权部署；养殖场/科研按管理规定
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（饲养者 / 养殖场 / 科研机构授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行爬宠节律分析**
        - 调用 `-m scripts.smyx_reptile_circadian_activity_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地爬宠箱 24 小时视频文件路径
            - `--url`: 网络爬宠箱 24 小时视频 URL（API 服务自动下载）
            - `--pet-type`: 类别标识，爬宠节律场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填）
            - `--list`: 显示爬宠昼夜节律历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的爬宠节律分析报告
        - 包含：事件 ID（event_id）、报告日期（report_date）、缸 ID（enclosure_id）、个体 ID（individual_id）、物种（species）、物种自然节律标签（species_natural_rhythm：diurnal_daytime / nocturnal_nighttime / crepuscular_dawn_dusk）、24h 运动信号（motion_signals：hourly_activity_array[24] / total_motion_pixels_24h / effective_observation_hours / frame_diff_method / motion_threshold_used）、高峰节律特征（rhythm_features：peak_hours_top3 / quiet_hours_top3 / light_period_activity_ratio / dark_period_activity_ratio / crepuscular_window_activity_ratio）、节律一致性信号（consistency_signals：observed_rhythm_classified / rhythm_consistency_score_0_100 / rhythm_inversion_detected / consecutive_inversion_days）、排除上下文（context_signals：is_during_shedding_period / is_during_brumation_or_hibernation / is_during_gravid_or_egg_laying / recent_environmental_change / light_schedule_recorded / night_disturbance_detected / camera_stable / ir_visible_during_dark / observation_signal_acceptable）、综合场景判定（composite_scene）、提醒等级（alert_level）、提醒动作列表（alert_actions）、建议动作（recommended_actions：检查光照周期 / 排查夜间光照-声响-振动干扰 / 调整光照计时器至物种自然节律 / 检查温度梯度 / 观察食欲精神 / 联系爬宠兽医，**绝不含具体药物、镇静剂、褪黑素剂量、具体灯光时刻数字、具体投喂物**）、免责声明（disclaimer：AI 节律分析仅供参考，**持续异常或伴随明显健康征兆需联系专业爬宠兽医（可能涉及代谢性疾病 / 神经系统问题）**）
        - **重要提示**：仅输出基于运动统计的节律分析，**不构成任何昼夜节律失调综合征 / 代谢性骨病 MBD / 抑郁 / 应激反应 等具体医学诊断**；**绝对不输出具体药物名称、剂量、镇静剂品牌、褪黑素剂量、中草药品牌**；**绝对不输出"自行关闭主灯""自行延长 UVB 时长至 N 小时""自行投喂助眠饲料""自行注射褪黑素"等任何具体环境/医疗指令——仅建议用户检查并按物种手册调整**

## 资源索引

- 必要脚本：见 [scripts/smyx_reptile_circadian_activity_analysis.py](scripts/smyx_reptile_circadian_activity_analysis.py)(
  用途：调用 API 进行爬宠 24h 节律分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、7 类综合场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4，最大 10MB；**摄像头必须固定机位、固定视野**；视频时长 **≥ 24 小时**；分辨率 ≥ 720p；帧率 ≥ 5 FPS；**夜间必须 IR 红外视觉，禁止夜间补可见光**
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心采样**：连续 24 小时（推荐连续 7 天以识别多日趋势）
- **核心评估三要素联合**：24 小时活动数组 + 物种自然节律对齐 + 一致性评分 0-100（< 50 显著颠倒）
- **4 级提醒策略递进**（info → important → urgent → critical），**严重颠倒连续 ≥ 3 天**直接 Level 4
- 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5
- 红线约束：
    - **🚨 禁止**做"昼夜节律失调综合征 / 代谢性骨病 MBD / 抑郁 / 应激反应"等具体医学诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、镇静剂品牌、褪黑素剂量、中草药品牌
    - **🚨 绝对禁止**输出"自行关闭主灯""自行延长 UVB 时长至 N 小时""自行投喂助眠饲料""自行注射褪黑素"等任何具体环境/医疗指令；**仅建议用户检查并按物种手册调整**
    - **🚨 严禁伪造或夸大活动量数据**；所有数据必须基于真实帧差/光流统计；统计窗口、阈值、算法必须可复现
    - **禁止**长期存储完整爬宠箱 24h 视频（≤ 14 天，留每小时活动量数组 + 节律事件关键截图；养殖场/科研按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停灯光计时器 / UVB / 加热垫 / 喷雾；任何环境控制变更必须由用户确认（仅可建议）
    - **必须**按 **species 自然节律基线判定**（昼行/夜行/暮晨），**严禁通用节律盲判**
    - **必须**考虑生理性上下文（**蜕皮期活动整体下降 / 休眠/冬眠期整体接近 0 / 抱蛋产卵期雌性活动剧增 / 近期环境变更 < 7 天**），避免误报
    - **夜间禁止**补可见光评估夜行性物种（必须 IR 红外，否则信号 unreliable）
    - **必须**在摄像头机位移动 / 长时间遮挡 / 观察时长 < 24h / 夜间无 IR 视觉 / 灯光开关时刻未录入时返回 `rhythm_signal_unreliable`
- **必须**：连续 ≥ 3 天 Level 4 → 强烈建议联系**专业爬宠兽医**（可能涉及代谢性疾病 / 神经系统问题）
- **必须**：节律分析报告**按 enclosure_id + individual_id + 报告日期输出**，含 24h 活动数组 + 高峰时段 + 一致性评分 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史节律分析记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"节律评分/高峰/场景"、"分析日期"、"点击查看"四列，其中"报告名称"列使用`爬宠节律分析-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 节律评分/高峰/场景 | 分析日期 | 点击查看 |
  |----------|----------|----------|----------|
  | 爬宠节律分析-20260525124200001 | 32/100 / [02,03,23] / rhythm_severely_inverted | 2026-05-25 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地爬宠箱24小时视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_circadian_activity_analysis --input /path/to/enclosure_24h.mp4 --open-id your-open-id

# 分析网络爬宠箱24小时视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_circadian_activity_analysis --url https://example.com/enclosure_24h.mp4 --open-id your-open-id

# 显示历史爬宠节律记录清单（自动触发关键词：查看爬宠节律历史报告等）
python -m scripts.smyx_reptile_circadian_activity_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_reptile_circadian_activity_analysis --input enclosure_24h.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_reptile_circadian_activity_analysis --input enclosure_24h.mp4 --open-id your-open-id --output result.json
```
