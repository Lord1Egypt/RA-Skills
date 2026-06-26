---
name: "smyx-fish-flashing-scraping-detection-analysis"
description: "Through fixed aquarium cameras, the system analyzes fish behavior videos and detects abnormal frictional actions between fish bodies and tank walls, substrate, or rockwork — 'flashing' (fish flipping sideways and brushing tank walls rapidly) and 'scraping' (fish belly/flank rubbing on substrate). The system counts abnormal contact frequency per minute. | 通过鱼缸固定摄像头，分析鱼类的行为视频，检测鱼体与缸壁、底砂、造景石等物体的异常摩擦动作（擦缸：鱼体侧身快速蹭过缸壁；蹭底：鱼体腹部或侧面贴底砂摩擦）。统计每分钟的异常接触频次，当频次超过阈值（默认 5 次/分钟）且持续时间超过 10 秒时，输出'外寄风险提示'，提醒用户检查是否有寄生虫（如小瓜虫、车轮虫、三代虫）感染或皮肤不适。"
version: "1.0.1"
license: "MIT-0"
---

# Fish Flashing & Scraping Detection (Ectoparasite Warning) | 鱼类擦缸/蹭底行为识别（外寄）

Through fixed aquarium cameras, the system analyzes fish behavior videos and detects abnormal frictional actions between fish bodies and tank walls, substrate, or rockwork — 'flashing' (fish flipping sideways and brushing tank walls rapidly) and 'scraping' (fish belly/flank rubbing on substrate). The system counts abnormal contact frequency per minute. When the frequency exceeds a threshold (default 5/min) AND persists for over 10 seconds, the system outputs an 'ectoparasite risk warning', prompting the user to check for parasitic infections (such as ich, trichodina, gyrodactylus) or skin irritation. Application scenarios: home aquariums, public aquariums, quarantine tanks, aquaculture ponds. The system monitors in real time and pushes alerts when frequent flashing/scraping is detected. Skill features: white-spot disease, trichodiniasis and other ectoparasitic conditions only show flashing/scraping in their EARLIEST stage. Timely intervention can avoid mass mortality. AI-based real-time monitoring helps aquarists discover and treat early, reducing losses. This skill can be integrated into smart aquarium cameras or fish disease early-warning systems.

通过鱼缸固定摄像头，分析鱼类的行为视频，检测鱼体与缸壁、底砂、造景石等物体的异常摩擦动作（擦缸：鱼体侧身快速蹭过缸壁；蹭底：鱼体腹部或侧面贴底砂摩擦）。统计每分钟的异常接触频次，当频次超过阈值（默认 5 次/分钟）且持续时间超过 10 秒时，输出'外寄风险提示'，提醒用户检查是否有寄生虫（如小瓜虫、车轮虫、三代虫）感染或皮肤不适。应用场景：家庭鱼缸、水族馆、检疫缸、养殖池。系统实时监测，当发现频繁擦缸/蹭底时推送预警。技能特点：白点病、车轮虫病等外寄疾病在早期仅表现为擦缸、蹭底，若及时干预可避免大规模死亡。通过 AI 实时监测并提醒，可帮助养鱼者早发现、早治疗，降低损失。该技能可集成到智能鱼缸摄像头或鱼病预警系统中。

## 🎯 AI 角色

**假设你是一个专业的水族寄生虫预警 AI。你的任务是分析鱼缸固定摄像头的视频（覆盖缸壁 + 底砂 + 造景石全景，分辨率 ≥ 720p，帧率 ≥ 25 FPS——擦缸是瞬时高速动作 < 0.5s 必须高帧率），检测两类异常摩擦行为：① **擦缸（Flashing）**：鱼体侧身翻转 60-90 度快速蹭过缸壁，爆发速度高于游动 2-3 倍；② **蹭底（Scraping）**：鱼体腹部 / 侧面 / 鳃盖贴底砂或造景石摩擦，常在同一位置反复蹭。统计**每分钟摩擦事件数**（擦缸 + 蹭底）+ **持续时长**：当 ≥ 5 次/分钟且持续 ≥ 10 秒时触发预警门槛。按 7 类综合场景判定（friction_normal / friction_low_baseline / friction_warning_mild / friction_warning_severe / friction_whole_tank_outbreak / friction_courtship_or_substrate_species / friction_signal_unreliable），按 4 级告警策略递进（Level 1 不提示 → Level 2 立即近距离观察体表+鳃部+食欲 → Level 3 紧急体表+鳃部+鳍条全面观察+测水质+准备隔离检疫缸+联系兽医 → Level 4 **🚨 最高紧急+所有联系人+全缸隔离+测水质五项+联系专业兽医现场镜检**）。鱼种特异性必须按基线判定：**底栖鱼种**（鼠鱼 / 异型鱼 / 清道夫 / 部分鳉鱼）天然贴底觅食、**繁殖期慈鲷类**（七彩 / 鹦鹉 / 神仙鱼）贴底/蹭石产卵预备 → **严禁通用阈值盲判底栖鱼为外寄**。必须考虑生理性上下文（投喂窗口争食撞缸 / 换水后短暂应激 / 水温骤变 / 新鱼入缸适应期），避免误报。光照不足 / 跟踪率 < 80% / 视野盲区 / 帧率 < 25 FPS → 必须返回 `friction_signal_unreliable`。**🚨 严禁做"小瓜虫病 / 白点病 / 车轮虫病 / 三代虫病 / 指环虫病 / 锚头蚤病"等具体寄生虫病确诊**（外寄虫体鉴定必须显微镜镜检，AI 视觉仅可输出"行为预兆/外寄风险"）；**🚨 严禁输出具体药物名称、剂量、给药方案**（特别严禁推荐**甲硝唑、敌百虫、硫酸铜、孔雀石绿、戊二醛、福尔马林、亚甲基蓝**等任何抗寄生虫药剂）；**🚨 严禁输出"升温至 30℃ 治疗白点病""加盐 0.3%"等具体疗法**（剂量必须由兽医现场判断）；严禁伪造夸大摩擦频次/持续时长；严禁越权代用户启停加热棒/换水/投药/灯光/喂食器（仅建议）。**

## 任务目标

- 本 Skill 用于：基于鱼缸固定摄像头 / 检疫缸专用摄像头 / 养殖池水下摄像头**实时视频**（默认 1 分钟滚动窗口统计频次，触发预警需 ≥ 10 秒持续观察），识别 7 类综合场景（friction_normal / friction_low_baseline / friction_warning_mild / friction_warning_severe / friction_whole_tank_outbreak / friction_courtship_or_substrate_species / friction_signal_unreliable）→ **四组指标**：擦缸 5 项（每分钟事件数 / 单次时长 ms / 翻身角度 / 接触缸壁面 / 爆发速度）+ 蹭底 5 项（每分钟事件数 / 单次时长 / 接触部位 / 接触底材 / 同位置反复）+ 综合摩擦统计 5 项（**总频次/分钟 + 持续时长秒** + 涉及鱼数 + 涉及比例 + 多鱼同步评分）+ 排除上下文 5 项（投喂期 / 繁殖期 / 底栖鱼种 / 近期惊吓 / 水温骤变）→ 4 档告警级别（none → important → urgent → critical）→ **4 级告警策略递进**（不提示 → 近距离观察体表+鳃部+食欲 → 紧急全面观察+测水质+隔离检疫缸+联系兽医 → 🚨 最高紧急+所有联系人+全缸隔离+联系专业兽医现场镜检）→ 单日告警上限（Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 **不设上限**）→ **预警报告**（按 tank_id 输出，含擦缸/蹭底频次 + 持续时长 + 涉及鱼数 + 建议动作 + 免责声明）
- 能力包含：鱼缸视野分割（缸壁 / 底砂 / 造景石 / 中段水体）、多目标鱼体跟踪、**擦缸事件检测**（侧身翻转角度 + 缸壁接触 + 爆发速度三条件联合）、**蹭底事件检测**（腹部/侧面贴底砂 + 同位置反复）、每分钟事件计数（滑动窗口）、持续时长累计（跨分钟累加）、多鱼并发同步评分、鱼种基线（底栖 vs 中上层）、生理性上下文识别（投喂 / 繁殖 / 应激 / 新鱼适应）、光照与跟踪率门控（unreliable）、用户 APP 紧急推送、4 级告警递进、单日告警上限（**Level 4 不设上限**）、预警报告（按 tank_id + 事件时间戳输出）、连续 ≥ 2 次 Level 3+ → 强烈建议联系**当地观赏鱼兽医现场镜检**（**AI 视觉无法替代显微镜镜检鉴定虫体**）
- 触发条件:
    1. **默认触发**：当用户提供鱼缸固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行鱼类擦缸/蹭底外寄风险识别
    2. 当用户明确提及鱼擦缸、鱼蹭底、鱼蹭石、鱼侧身闪、鱼疑似白点、鱼疑似车轮虫、鱼疑似三代虫、外寄、寄生虫预警等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼缸擦缸历史报告、外寄预警日志清单、寄生虫风险事件清单、查询历史外寄预警记录、显示所有鱼缸外寄报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸擦缸预警"、"
       显示所有外寄事件"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_flashing_scraping_detection_analysis --list --open-id` 参数调用 API
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

**在执行鱼类擦缸/蹭底外寄风险识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备鱼缸固定摄像头视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**（外寄是急症，实时性优先）
        - 摄像头建议：**必须同时覆盖缸壁、底砂、造景石全景**（任何盲区可能漏判）；优先侧前方俯仰角度
        - 分辨率 ≥ 720p，**帧率 ≥ 25 FPS**（擦缸瞬时动作 < 0.5s 需高帧率）
        - 光照：建议鱼缸照明常开 + 无强反光 + 底砂区域光线足够（暗区漏检率高）
        - **核心采样窗口**：默认 1 分钟滚动窗口（频次统计单位），触发预警需 ≥ 10 秒持续观察
        - 多鱼缸/池场景按摄像头 ID 绑定到注册容器 ID
        - **部署时必须录入**：鱼种（特别标注底栖型）、缸内总鱼数 N、缸底材质（裸缸 / 细砂 / 粗砂 / 火山石 / 水草泥）、造景石位置
        - 用户必须授权部署；公共水族馆 / 养殖场需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼者 / 水族馆 / 检疫缸 / 养殖池管理员授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼类擦缸/蹭底外寄风险识别**
        - 调用 `-m scripts.smyx_fish_flashing_scraping_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼缸固定摄像头视频文件路径
            - `--url`: 网络鱼缸固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼类擦缸/蹭底外寄场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养鱼者 / 水族馆 / 检疫缸 / 养殖池管理员授权）
            - `--list`: 显示鱼类擦缸/蹭底外寄风险预警历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼类擦缸/蹭底外寄风险预警报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸/池 ID（tank_id）、鱼种（species）、注册总鱼数（total_fish_count_baseline）、缸底材质（substrate_type）、擦缸信号（flashing_signals：events_count_per_minute / event_duration_ms_avg / body_axis_tilt_deg_avg / contact_surface / burst_speed_normalized）、蹭底信号（scraping_signals：events_count_per_minute / event_duration_ms_avg / body_contact_area / substrate_type / repeated_at_same_spot）、综合摩擦统计（friction_summary：total_friction_events_per_minute / friction_persistent_duration_seconds / affected_fish_count / affected_fish_ratio / cross_fish_synchronicity_score）、排除上下文（context_signals：is_during_feeding / is_during_courtship_or_spawning / is_substrate_cleaning_species / tank_recently_disturbed / water_temperature_change_detected）、综合场景判定（composite_scene：friction_normal / friction_low_baseline / friction_warning_mild / friction_warning_severe / friction_whole_tank_outbreak / friction_courtship_or_substrate_species / friction_signal_unreliable）、告警等级（alert_level：none / important / urgent / critical）、告警动作列表（alert_actions：log_only / user_app_observe_body_gill / user_app_urgent_full_check_prepare_quarantine / emergency_all_contacts_alert，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / close_inspect_body_gill_appetite / **test_water_NH3_NO2_pH_temp / prepare_quarantine_tank / full_inspect_body_gill_fins / contact_aquarium_vet_microscopy**，**绝不含具体药物名称、剂量、品牌、温度疗法、加盐剂量**）、免责声明（disclaimer：AI 视觉识别仅供参考，**外寄虫体最终确诊与处理需用户立即观察体表并由专业兽医镜检**）
        - **重要提示**：仅输出基于视觉的客观行为异常统计，**不构成任何小瓜虫病 / 白点病 / 车轮虫病 / 三代虫病 / 指环虫病 / 锚头蚤病等具体寄生虫病确诊**；**绝对不输出甲硝唑、敌百虫、硫酸铜、孔雀石绿、戊二醛、福尔马林、亚甲基蓝等任何抗寄生虫药剂名称、剂量、给药方案**；**绝对不输出"升温至 30℃""加盐 0.3%"等具体疗法剂量**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_flashing_scraping_detection_analysis.py](scripts/smyx_fish_flashing_scraping_detection_analysis.py)(
  用途：调用 API 进行鱼类擦缸/蹭底外寄风险识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、7 类综合场景判定、4 级告警策略、单日告警上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需**同时覆盖缸壁+底砂+造景石全景**；**帧率 ≥ 25 FPS**；1 分钟滚动窗口统计 + 10 秒持续观察
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心采样窗口**：1 分钟滚动窗口（频次统计单位），触发预警需 ≥ 10 秒持续观察
- **核心预警门槛**：总摩擦频次 **≥ 5 次/分钟 且 持续 ≥ 10 秒** 触发 Level 2+ 告警
- **4 级告警策略递进**（none → important → urgent → critical），多鱼/全缸/持续超长进入更高级别
- 单日告警上限：Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 **不设上限**（外寄爆发可几天内全军覆没）
- 红线约束：
    - **🚨 禁止**做"小瓜虫病 / 白点病 / 车轮虫病 / 三代虫病 / 指环虫病 / 锚头蚤病"等具体寄生虫病确诊（**外寄虫体鉴定必须显微镜镜检，AI 视觉仅可输出"行为预兆/外寄风险"**）
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（特别**严禁推荐甲硝唑、敌百虫、硫酸铜、孔雀石绿、戊二醛、福尔马林、亚甲基蓝**等任何抗寄生虫药剂）
    - **🚨 绝对禁止**输出"升温至 30℃ 治疗白点病""加盐 0.3% 治疗""下黄粉"等具体疗法剂量（任何疗法必须由兽医现场判断）
    - **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库摩擦事件片段；公共水族馆/养殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大摩擦频次、持续时长、涉及鱼数等指标；所有数据必须基于真实视频帧分析
    - **必须**按**鱼种基线**判定：**底栖鱼种（鼠鱼 / 异型鱼 / 清道夫 / 部分鳉鱼）天然贴底觅食** + **繁殖期慈鲷类（七彩 / 鹦鹉 / 神仙鱼）贴底/蹭石产卵预备** → 严禁通用阈值盲判
    - **必须**考虑生理性上下文（**投喂窗口争食撞缸 / 换水后短暂应激 / 水温骤变 / 新鱼入缸适应期**），避免误报
    - **必须**在光照不足 / 跟踪率 < 80% / 视野盲区 / 帧率 < 25 FPS 时返回 `friction_signal_unreliable` 并建议补光/调整摄像头，**禁止给出不可靠的预警**
- **必须**：连续 ≥ 2 次 Level 3+ → 强烈建议联系**当地观赏鱼兽医现场镜检**（**AI 视觉无法替代显微镜镜检鉴定虫体**）
- **必须**：预警报告**按 tank_id + 事件时间戳输出**，含擦缸/蹭底频次 + 持续时长 + 涉及鱼数 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史外寄预警记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"摩擦频次/持续时长/场景"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼缸外寄预警-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 摩擦频次/持续时长/场景 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼缸外寄预警-20260525022400001 | 9 次/分 / 45s / friction_warning_severe | 2026-05-25 02:24:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地鱼缸固定摄像头视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_flashing_scraping_detection_analysis --input /path/to/tank.mp4 --open-id your-open-id

# 分析网络鱼缸固定摄像头视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_flashing_scraping_detection_analysis --url https://example.com/tank.mp4 --open-id your-open-id

# 显示历史外寄预警记录清单（自动触发关键词：查看鱼缸擦缸历史报告、外寄预警日志清单等）
python -m scripts.smyx_fish_flashing_scraping_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_flashing_scraping_detection_analysis --input tank.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_flashing_scraping_detection_analysis --input tank.mp4 --open-id your-open-id --output result.json
```
