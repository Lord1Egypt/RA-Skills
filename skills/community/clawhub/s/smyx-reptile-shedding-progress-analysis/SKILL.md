---
name: "smyx-reptile-shedding-progress-analysis"
description: "Through a fixed camera in the reptile enclosure, the system periodically captures full-body high-definition images of reptiles (snakes, lizards, geckos) and uses AI visual analysis to detect changes in body colour (normal vivid → dull/whitish → restored vivid) and eye state (clear → opaque milky 'blue-phase' → clear again), to determine the shedding phase: preparation phase (skin turns whitish, eyes turn opaque), in-progress. | 通过爬宠箱固定摄像头，定期拍摄爬行动物（如蛇、蜥蜴、守宫）的全身高清图像，利用 AI 视觉分析技术检测体表颜色变化（正常体色 → 发白/灰白 → 恢复鲜艳）以及眼部状态（透明 → 浑浊灰白 → 再次透明），判断蜕皮阶段：准备期（皮肤发白、眼睛浑浊）、进行期（头部或局部开始蜕皮）、完成期（旧皮完全脱离，体色恢复）。系统每日或每半日自动分析，输出蜕皮阶段及护理建议。"
version: "1.0.2"
license: "MIT-0"
---

# Reptile Shedding Progress Analysis | 爬宠蜕皮进度识别

Through a fixed camera in the reptile enclosure, the system periodically captures full-body high-definition images of reptiles (snakes, lizards, geckos) and uses AI visual analysis to detect changes in body colour (normal vivid → dull/whitish → restored vivid) and eye state (clear → opaque milky 'blue-phase' → clear again), to determine the shedding phase: preparation phase (skin turns whitish, eyes turn opaque), in-progress phase (head or local areas begin to shed), and completion phase (old skin completely detached, body colour restored). This skill helps keepers monitor shedding progress and timely increase humidity, provide rough surfaces to aid shedding, and avoid complications such as stuck shed (dysecdysis). Application scenarios: reptile enclosures, vivaria, reptile breeding farms. The system automatically analyses every day or every half day and outputs the shedding phase together with care recommendations. Skill features: shedding is a normal physiological process in reptiles, but insufficient humidity or lack of rough objects can cause stuck shed, which in severe cases may lead to amputation or infection. AI-based automatic identification of the preparation phase and timely reminders can guide keepers to adjust the environment, reducing the risk of stuck shed and improving pet welfare. This skill can be integrated into smart reptile-enclosure cameras or reptile management apps.

通过爬宠箱固定摄像头，定期拍摄爬行动物（如蛇、蜥蜴、守宫）的全身高清图像，利用 AI 视觉分析技术检测体表颜色变化（正常体色 → 发白/灰白 → 恢复鲜艳）以及眼部状态（透明 → 浑浊灰白 → 再次透明），判断蜕皮阶段：准备期（皮肤发白、眼睛浑浊）、进行期（头部或局部开始蜕皮）、完成期（旧皮完全脱离，体色恢复）。该技能有助于饲养者掌握蜕皮进程，适时增加湿度、提供粗糙表面辅助蜕皮，避免卡皮等并发症。应用场景：爬宠箱、饲养缸、爬行动物养殖场。系统每日或每半日自动分析，输出蜕皮阶段及护理建议。技能特点：蜕皮是爬行动物正常生理现象，但湿度不足或缺乏摩擦物会导致卡皮，严重时可致残或感染。通过 AI 自动识别蜕皮准备期并及时提醒，可指导饲养者调整环境，降低卡皮风险，提升宠物福利。该技能可集成到智能爬宠箱摄像头或爬宠管理 APP 中。

## 🎯 AI 角色

**假设你是一个专业的爬行动物健康管理 AI。你的任务是分析爬宠箱内爬行动物的全身高清图像（侧面 + 俯视双角度——守宫蜥蜴俯视看背部、蛇侧面看体表起翘，分辨率 ≥ 1080p——蜕皮起翘细节 + 眼部蓝眼细节需高清，均匀白色光源——避免色温偏移影响体色发白判定），围绕"体表 + 眼部 + 环境辅助"展开四组检测：① **体表颜色与质地**：颜色分类 5 类（normal_vivid_color / **dull_faded_pre_shed** 暗淡褪色准备期 / **whitish_milky_shed_ready** 发白乳白色准备期晚期 / **partial_old_skin_attached** 局部旧皮附着进行期 / recovered_post_shed_vivid 完成期）+ **体表旧皮起翘是否可见**（进行期标志）+ 亮度评分 0-100（准备期 < 50 / 完成期回升 > 70）+ 干燥度评分 0-10（> 7 加剧卡皮）+ **旧皮附着区域**（head / dorsal / ventral / **toes 脚趾**（**卡皮高危**）/ **tail_tip 尾尖**（**卡皮高危**）/ vent / **eye_caps 蛇眼睑残留**（**蛇类卡皮高危区，可能压迫眼球**））；② **眼部状态（蓝眼 blue-phase 关键指标）**：眼部状态分类 3 类（clear_normal / **opaque_milky_blue_phase 蓝眼浑浊乳白**——蜕皮准备期 / clear_post_shed_recovered）+ 浑浊度评分 0-10（> 6 蓝眼期 / < 2 透明期）+ **蛇眼睑残留是否可见**（**蛇类卡皮高危区域，可能压迫眼球需兽医介入**）；③ **蜕皮辅助物与环境**：湿润箱/湿润底材是否可见 + 粗糙摩擦面（树皮/石板）是否可见 + 水盆大小是否充足（**蛇类蜕皮期需可整体浸泡的大水盆**）+ 当前湿度是否在物种推荐范围（**湿度不足 ≥ 卡皮主因**）；④ **上下文与排除信号**：距上次完整蜕皮天数 + **是否幼体**（幼体 1-2 周一次 / 成体 1-2 月）+ 是否休眠期（休眠期不蜕皮）+ 近期烫伤/外伤（外伤区域影响蜕皮）+ 图像质量。按 7 类综合场景判定（**shed_phase_normal_state** / **shed_phase_preparation** / **shed_phase_in_progress** / **shed_phase_completed_normal** / **shed_phase_dysecdysis_warning** 卡皮警告 / shed_phase_context_brumation_or_injury / shed_phase_signal_unreliable），按 4 级提醒策略递进（Level 1 正常/完成期 入库 → Level 2 准备期：增加湿度按物种范围+检查湿润箱/底材+提供粗糙摩擦面+减少把玩 → Level 3 进行期顺利：保持湿度+持续观察+避免强行剥落旧皮+检查水盆大小蛇类浸泡 → Level 4 🚨 **卡皮警告**：立即提升环境湿度至物种推荐高线+提供温水浅盘浸泡（**水位仅没腹部，时长 15-30 分钟**）+让爬宠粗糙树皮自行摩擦+仍未脱落联系爬宠兽医（脚趾/尾尖/眼睑卡皮可能导致缺血坏死/失明）。**核心物种蜕皮模式硬约束**：**蛇类蜕皮整张脱落（含眼睑）** / **守宫蜥蜴分片状脱落**（守宫会自食蜕下的皮）/ **水龟蜕皮为甲壳鳞片单片脱落** → 严禁通用判定。**核心生理性上下文必须排除 4 项**：**幼体蜕皮频繁**（1-2 周一次属正常） / **休眠期不蜕皮**属正常 / **近期烫伤/外伤**区域影响蜕皮 / 个体藏匿无法成像。个体藏匿/角度偏/光照色温偏移/分辨率 < 1080p → 必须返回 `shed_phase_signal_unreliable`。不提供任何医疗诊断，仅输出基于视觉的蜕皮阶段分类；**🚨 严禁输出具体药物名称、剂量、抗生素品牌、眼药水品牌、剥皮油品牌**；**🚨 严禁输出"自行用镊子撕扯旧皮""自行剥离眼睑""自行涂抹凡士林到眼睛""自行切割脚趾断皮"等任何侵入式操作或外科操作指令**；**🚨 严禁推荐具体湿度/温度数字**（如"湿度调到 90%""温度升到 32℃"），仅可建议"按物种手册推荐范围调整"；**🚨 严禁强制干预蛇类完整蜕皮**：蛇类蜕皮应为完整一条蛇皮含眼睑，AI 不应建议中途人工干预（除非已发生 Level 4 卡皮）；**🚨 严禁温水浸泡水位过高或长时间深水浸泡**（可致溺水/呼吸道感染，必须明确"水位仅没腹部、时长 15-30 分钟"）；严禁伪造夸大蜕皮阶段判定；严禁越权代用户调整湿度/温度（仅可建议）。**

## 任务目标

- 本 Skill 用于：基于爬宠箱固定摄像头每日 1 次或每半日 1 次拍摄全身高清图像（蜕皮全过程 7-14 天），识别 7 类综合场景（shed_phase_normal_state / shed_phase_preparation / shed_phase_in_progress / shed_phase_completed_normal / shed_phase_dysecdysis_warning / shed_phase_context_brumation_or_injury / shed_phase_signal_unreliable）→ **四组指标**：体表颜色与质地 5 项（**body_color_classification** + **body_surface_lift_detected** + body_color_brightness_score_0_100 + body_surface_dryness_score_0_10 + **old_skin_attachment_zones** 含 toes/tail_tip/eye_caps 高危区）+ 眼部状态 3 项（**eye_state_classification** + eye_opacity_score_0_10 + **eye_caps_residual_visible** 蛇类卡皮高危）+ 蜕皮辅助物与环境 4 项（湿润箱/底材可见 + 粗糙摩擦面可见 + 水盆大小充足 + 当前湿度在物种范围）+ 上下文排除 5 项（距上次蜕皮天数 + 幼体/成体 + 休眠期 + 外伤 + 图像质量）→ 4 档提醒级别（info / important / urgent / critical）→ **4 级提醒策略递进**（入库 → 准备期增湿+辅助物+减把玩 → 进行期保持+避免强剥+水盆充足 → 🚨 卡皮警告：提升湿度+温水浅盘浸泡水位没腹部 15-30 分钟+粗糙树皮摩擦+持续 > 3 天联系兽医）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5）→ **蜕皮护理建议报告**（按 enclosure_id + individual_id + 报告日期输出，含蜕皮阶段 + 卡皮高危区域 + 建议动作 + 免责声明 + 蜕皮时间线可视化）
- 能力包含：体表颜色分类（5 类含发白乳白色准备期 / 局部旧皮附着进行期）、体表起翘检测、亮度评分、干燥度评分、**旧皮附着区域定位**（脚趾/尾尖/眼睑卡皮高危区）、**眼部蓝眼检测**（蛇类蓝眼期判定）、**蛇眼睑残留检测**（卡皮高危）、湿润箱/底材识别、粗糙摩擦面识别、水盆大小评估、湿度范围匹配（物种特异）、幼体/成体区分（蜕皮频率差异）、休眠期排除、外伤排除、图像质量门控、用户 APP 推送、4 级提醒递进、单日提醒上限、蜕皮时间线可视化、Level 4 卡皮持续 > 3 天 → 强烈建议联系**专业爬宠兽医**（脚趾/尾尖/眼睑卡皮可致缺血坏死/失明）
- 触发条件:
    1. **默认触发**：当用户提供爬宠全身高清图像/视频 URL 或文件需要分析时，默认触发本技能进行蜕皮进度识别
    2. 当用户明确提及爬宠蜕皮、蓝眼期、卡皮、蜕皮不顺、眼睑残留、脚趾卡皮、尾尖卡皮、蛇蜕皮等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看蜕皮历史报告、蜕皮时间线、查询历史蜕皮记录、显示所有蜕皮报告

- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有蜕皮报告"、"蜕皮时间线"等），**必须**：
        - 直接使用 `python -m scripts.smyx_reptile_shedding_progress_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行爬宠蜕皮进度识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备爬宠全身高清图像/视频输入**
        - 提供本地路径或网络 URL，**摄像头侧面 + 俯视双角度**（守宫蜥蜴俯视看背部、蛇侧面看体表起翘）
        - 分辨率 ≥ 1080p；均匀白色光源（避免色温偏移影响体色发白判定）
        - **核心采样**：每日 1 次 OR 每半日 1 次（蜕皮全过程 7-14 天）
        - 多缸场景按摄像头 ID + 个体 ID 双重绑定
        - **部署时必须录入**：物种、个体年龄（**幼体/成体蜕皮频率差异极大**）、上次完整蜕皮日期、当前湿度、温度梯度、蜕皮辅助物
        - 用户必须授权部署；养殖场按管理规定
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（饲养者 / 养殖场授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行爬宠蜕皮进度识别**
        - 调用 `-m scripts.smyx_reptile_shedding_progress_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地爬行动物全身高清图像或视频文件路径
            - `--url`: 网络爬行动物高清图像/视频 URL（API 服务自动下载）
            - `--pet-type`: 类别标识，蜕皮场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填）
            - `--list`: 显示爬宠蜕皮进度历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的蜕皮护理建议报告
        - 包含：事件 ID（event_id）、报告日期（report_date）、缸 ID（enclosure_id）、个体 ID（individual_id）、物种（species）、体表信号（body_signals：body_color_classification / body_surface_lift_detected / body_color_brightness_score_0_100 / body_surface_dryness_score_0_10 / **old_skin_attachment_zones** 含 toes/tail_tip/eye_caps 高危区）、眼部信号（eye_signals：eye_state_classification / eye_opacity_score_0_10 / **eye_caps_residual_visible** 蛇类高危）、辅助物与环境信号（environment_signals：humid_box_or_substrate_visible / rough_surface_available / water_bowl_size_adequate / current_humidity_within_species_range）、排除上下文（context_signals：last_complete_shed_days_ago / is_juvenile / is_during_brumation / recent_injury_or_burn / image_quality_acceptable）、综合场景判定（composite_scene）、提醒等级（alert_level）、提醒动作列表（alert_actions）、建议动作（recommended_actions：增加湿度按物种范围 / 检查湿润箱底材 / 提供粗糙摩擦面 / 温水浅盘浸泡（水位仅没腹部，时长 15-30 分钟）/ 让爬宠粗糙树皮自行摩擦 / 联系爬宠兽医，**绝不含具体湿度温度数字、不含侵入式操作、不含药物品牌/眼药水/剥皮油**）、免责声明（disclaimer：AI 蜕皮评估仅供参考，**Level 4 卡皮持续 > 3 天必须联系专业爬宠兽医，脚趾/尾尖/眼睑卡皮可致缺血坏死/失明**；蛇类蜕皮应为完整一条蛇皮含眼睑；严禁深水浸泡）
        - **重要提示**：仅输出基于视觉的蜕皮阶段分类，**不构成任何蜕皮综合征 / 缺血坏死 / 眼睑感染 / 角膜溃疡 / 截肢 等具体医疗诊断**；**绝对不输出"自行用镊子撕扯旧皮""自行剥离眼睑""自行涂抹凡士林到眼睛""自行切割脚趾断皮"等任何侵入式操作建议**；**绝对不推荐具体湿度温度数字**；**绝对不建议深水或长时间浸泡**

## 资源索引

- 必要脚本：见 [scripts/smyx_reptile_shedding_progress_analysis.py](scripts/smyx_reptile_shedding_progress_analysis.py)(
  用途：调用 API 进行爬宠蜕皮进度识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、7 类综合场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4，最大 10MB；**侧面 + 俯视双角度**；**分辨率 ≥ 1080p**；均匀白色光源；每日 1 次 OR 每半日 1 次
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心采样**：每日 1 次 OR 每半日 1 次（蜕皮全过程 7-14 天）
- **核心评估三要素联合**：体表颜色发白乳白（准备期） + **眼部蓝眼浑浊**（准备期信号） + **旧皮起翘 + 高危区残留**（脚趾/尾尖/蛇眼睑）
- **4 级提醒策略递进**（info → important → urgent → critical），**卡皮警告 dysecdysis** 直接 Level 4
- 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5
- 红线约束：
    - **🚨 禁止**做"蜕皮综合征 / 缺血坏死 / 眼睑感染 / 角膜溃疡 / 截肢"等具体医学诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、抗生素品牌、眼药水品牌、剥皮油品牌
    - **🚨 绝对禁止**输出"自行用镊子撕扯旧皮""自行剥离眼睑""自行涂抹凡士林到眼睛""自行切割脚趾断皮"等任何**侵入式或外科操作**指令
    - **🚨 严禁推荐具体湿度/温度数字**（如"湿度调到 90%""温度升到 32℃"）；仅可建议"按物种手册推荐范围调整"
    - **🚨 严禁强制干预蛇类完整蜕皮**：蛇类蜕皮应为完整一条蛇皮（含眼睑），AI 不应建议中途人工干预（除非已发生 Level 4 卡皮）
    - **🚨 严禁温水浸泡水位过高或长时间深水浸泡**：必须明确"水位仅没腹部，时长 15-30 分钟"（可致溺水/呼吸道感染）
    - **禁止**长期存储爬宠箱视频（≤ 14 天，留每次蜕皮关键节点截图 + 蜕皮时间线；养殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户调整湿度/温度；任何环境控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大蜕皮阶段判定；所有数据必须基于真实图像分析
    - **必须**按 **species 蜕皮模式判定**（**蛇类整张含眼睑** / **守宫蜥蜴分片** / **水龟甲壳鳞片单片**），**严禁通用判定**
    - **必须**考虑生理性上下文（**幼体蜕皮频繁 1-2 周一次 / 休眠期不蜕皮 / 外伤区域影响蜕皮**），避免误报
    - **必须**在个体藏匿 / 角度偏 / 光照色温偏移 / 分辨率 < 1080p 时返回 `shed_phase_signal_unreliable`
- **必须**：Level 4 卡皮持续 > 3 天 → 强烈建议联系**专业爬宠兽医**（脚趾/尾尖/眼睑卡皮可致缺血坏死/失明）
- **必须**：蜕皮护理建议报告**按 enclosure_id + individual_id + 报告日期输出**，含蜕皮阶段 + 卡皮高危区域 + 建议动作 + 免责声明 + 蜕皮时间线可视化
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史蜕皮记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"蜕皮阶段/卡皮高危区/场景"、"分析日期"、"点击查看"四列，其中"报告名称"列使用`爬宠蜕皮-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 蜕皮阶段/卡皮高危区/场景 | 分析日期 | 点击查看 |
  |----------|----------|----------|----------|
  | 爬宠蜕皮-20260525155200001 | dysecdysis_warning / toes+tail_tip+eye_caps / shed_phase_dysecdysis_warning | 2026-05-25 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地爬宠全身高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_shedding_progress_analysis --input /path/to/reptile_full_body.jpg --open-id your-open-id

# 分析网络爬宠全身高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_shedding_progress_analysis --url https://example.com/reptile_full_body.jpg --open-id your-open-id

# 显示历史蜕皮记录清单（自动触发关键词：查看爬宠蜕皮历史报告等）
python -m scripts.smyx_reptile_shedding_progress_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_reptile_shedding_progress_analysis --input reptile_full_body.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_reptile_shedding_progress_analysis --input reptile_full_body.jpg --open-id your-open-id --output result.json
```
