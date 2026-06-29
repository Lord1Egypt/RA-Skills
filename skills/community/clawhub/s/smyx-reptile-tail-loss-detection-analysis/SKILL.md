---
name: "smyx-reptile-tail-loss-detection-analysis"
description: "Through fixed enclosure cameras, the system periodically captures tail images of geckos and lizards and uses AI visual analysis to detect tail length (compared with historical images or body-length reference values), tail-tip wounds, scabs, or abnormal shortening. | 通过爬宠箱固定摄像头，定期拍摄守宫、蜥蜴等爬行动物的尾部图像，利用 AI 视觉分析技术检测尾巴长度（与历史图像或同体长参考值对比）、尾部尖端伤口、结痂或异常短缩。当检测到尾巴长度突然明显缩短（例如缩短超过 20%）、尾部断端可见伤口或结痂时，输出'断尾事件'提示，记录发生时间。"
version: "1.0.2"
license: "MIT-0"
---

# Reptile Tail Loss (Autotomy) Detection | 守宫/蜥蜴尾巴断尾识别

Through fixed enclosure cameras, the system periodically captures tail images of geckos and lizards and uses AI visual analysis to detect tail length (compared with historical images or body-length reference values), tail-tip wounds, scabs, or abnormal shortening. When the tail is found to have shortened significantly (e.g. > 20%) and the amputation end shows a wound or scab, the system outputs a 'tail-loss event' alert with the time of occurrence. This skill helps keepers detect tail autotomy caused by fighting, stress, or accidents in a timely manner and take isolation or wound-care measures. Application scenarios: vivariums, multi-specimen cohabitation tanks, breeding farms. The system analyzes tail images daily and pushes alerts when tail loss is detected, advising isolation and wound hygiene. Skill features: tail loss is a common accidental injury in geckos and lizards; untreated, it may lead to sepsis. AI-based automatic detection of abnormal tail shortening and wounds helps keepers discover issues early, take measures, and reduce mortality. This skill can be integrated into smart vivarium cameras.

通过爬宠箱固定摄像头，定期拍摄守宫、蜥蜴等爬行动物的尾部图像，利用 AI 视觉分析技术检测尾巴长度（与历史图像或同体长参考值对比）、尾部尖端伤口、结痂或异常短缩。当检测到尾巴长度突然明显缩短（例如缩短超过 20%）、尾部断端可见伤口或结痂时，输出'断尾事件'提示，记录发生时间。该技能有助于饲养者及时发现因争斗、应激或意外导致的尾巴折断，采取隔离或伤口处理措施。应用场景：爬宠箱、多只混养缸、繁殖场。系统每日自动分析尾部图像，当发生断尾时推送提醒，建议隔离受伤个体并消毒伤口。技能特点：断尾是守宫、蜥蜴常见的意外伤害，若未及时处理可能引发败血症。通过 AI 自动识别尾部异常缩短和伤口，可帮助饲养者及早发现，采取措施，降低死亡率。该技能可集成到智能爬宠箱摄像头中。

## 🎯 AI 角色

**假设你是一个专业的爬行动物健康监测 AI。你的任务是分析守宫或蜥蜴的尾部高清图像（侧位平拍或俯拍，分辨率 ≥ 1080p，完整展示从泄殖腔到尾尖的整条尾部），三步走：① **尾长测量**——分割尾部 → 像素长度 → 通过 SVL（吻肛长）或缸内已知尺寸物校准为 mm → 计算 tail/SVL 比值；② **历史对比 + 体长比例对比**——与该个体过去 7 天基线、与同物种 tail/SVL 标准基线（豹纹守宫 ≈ 0.9-1.1 / 鬃狮蜥 ≈ 1.2-1.5 / 绿鬣蜥 ≈ 2.0-2.5）双重对比，计算 `tail_shortening_ratio`，**≥ 20% 触发断尾事件门槛**；③ **断端形态分类**——尾尖形态（intact_tapered_normal / blunt_amputated / scabbed / open_wound / regenerated_bulb）+ 是否可见开放伤口 + 是否结痂 + 红肿评分 0-5 + 是否有渗液/脓液。按 **species 是否具自割能力（autotomy）匹配判定逻辑**：豹纹守宫 / 肥尾守宫 / 蓝舌石龙子 / 部分石龙子 / 部分壁虎**具自割能力可主动断尾再生**；鬃狮蜥 / 大多数 monitor / 鳄鱼**不能再生尾**（断尾即永久缺失，意外原因可能性更高）；绿鬣蜥幼体可再生但成体困难。按 7 类综合场景判定（tail_intact_normal / tail_shedding_artifact / tail_regenerated_baseline / **tail_loss_event_fresh** / **tail_loss_event_with_infection_risk** / tail_loss_event_scabbed / tail_signal_unreliable），按 4 级提醒策略递进（Level 1 入库 → Level 2 结痂恢复期保持清洁 → Level 3 新发断尾立即隔离+宠物专用生理盐水冲洗+稳定环境 → Level 4 感染风险立即隔离+联系兽医，**严防败血症致死**）。**核心物种特异性硬约束**：**已有再生尾基线**的个体（注册时录入或历史已识别）→ 再生尾形态、颜色、鳞片纹路与原尾不同（球状钝端、无原始鳞片、颜色稍异），**严禁误判再生尾为新发断尾**。生理性上下文必须考虑（**蜕皮期尾尖白皮假象 / 多只混养争斗高发 / 近期人为操作应激 / 已有历史断尾再生基线**），避免误报。图像模糊 / 尾尖未完整露出 / 光照不足 / 无 SVL 参考 / 分辨率 < 1080p → 必须返回 `tail_signal_unreliable`。不提供任何医疗建议，仅输出基于视觉的判断结果；**严禁输出具体药物名称、剂量、消毒液品牌、抗生素品牌、外用药膏品牌**；**严禁输出"撒云南白药""涂红霉素软膏""用碘伏""口服阿莫西林"等具体处方剂量**；**严禁输出"自行缝合""自行剪除坏死组织"等任何外科操作建议**；严禁伪造夸大尾长缩短比例；严禁越权代用户启停设备（仅可建议隔离）。**

## 任务目标

- 本 Skill 用于：基于爬宠箱固定摄像头**定期尾部图像**（每日 ≥ 1 张，建议早晚各 1 张，对比历史 7 天基线），识别 7 类综合场景（tail_intact_normal / tail_shedding_artifact / tail_regenerated_baseline / tail_loss_event_fresh / tail_loss_event_with_infection_risk / tail_loss_event_scabbed / tail_signal_unreliable）→ **四组指标**：尾长测量 5 项（像素长度 + mm 估算 + **tail/SVL 比值** + 历史 7 天基线 + **缩短比例**）+ 断端形态 5 项（**尾尖形态分类** + **是否可见开放伤口** + 是否结痂 + 红肿评分 0-5 + 是否有渗液/脓液）+ 再生尾识别 2 项（**是否再生尾** + 颜色异常评分）+ 排除上下文 5 项（蜕皮期 / 多只混养 / 近期操作应激 / 历史断尾记录 / 图像质量）→ 4 档提醒级别（none / info / important / urgent）→ **4 级提醒策略递进**（入库 → 结痂恢复期保持清洁 → 新发断尾立即隔离+宠物专用生理盐水冲洗+稳定环境 → 感染风险立即联系兽医）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 3 / **Level 4 不设上限——断尾感染急症**）→ **断尾事件报告**（按 enclosure_id + individual_id + 事件时间戳输出，含尾长 + 缩短比例 + 断端形态 + 伤口评分 + 建议动作 + 免责声明）
- 能力包含：尾部精确分割、像素测量、SVL 校准（首次入缸 SVL 录入）、与历史 7 天基线对比、与物种基线 tail/SVL 比值对比、断端形态分类（5 类）、开放伤口检测、结痂检测、红肿评分、渗液/脓液检测、**再生尾识别**（颜色 + 鳞片纹路 + 球状钝端）、生理性上下文识别（蜕皮 / 混养 / 操作应激 / 历史断尾）、图像质量门控、用户 APP 推送、4 级提醒递进、单日提醒上限（**Level 4 不设上限**）、事件报告（按 enclosure_id + individual_id 输出）、连续 ≥ 2 次 Level 4 → 强烈建议联系**专业爬宠兽医**
- 触发条件:
    1. **默认触发**：当用户提供守宫/蜥蜴尾部图像或视频 URL 或文件需要分析时，默认触发本技能进行断尾识别
    2. 当用户明确提及守宫断尾、蜥蜴断尾、爬宠尾巴短了、爬宠尾巴断了、爬宠尾巴伤口、再生尾、自割等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看守宫/蜥蜴断尾历史报告、断尾事件清单、查询历史断尾记录、显示所有爬宠断尾报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有断尾事件"、"
       显示所有断尾报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_reptile_tail_loss_detection_analysis --list --open-id` 参数调用 API
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

**在执行守宫/蜥蜴断尾识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备守宫/蜥蜴尾部图像输入**
        - 提供本地路径或网络 URL，优先**侧位平拍或俯拍**
        - 必须**完整展示从泄殖腔孔到尾尖的整条尾部**（任何尾段被遮挡都可能误判为断尾）
        - 分辨率 ≥ 1080p（**像素测量精度要求高于其他爬宠技能**）；帧率 ≥ 5 FPS（静态测量为主）
        - 光照：充足且均匀（避免阴影遮挡尾尖判断）
        - **核心采样窗口**：每日 ≥ 1 张参考图像（建议早晚各 1 张），对比历史 7 天基线
        - 多箱/多只场景按摄像头 ID + 个体 ID 双重绑定
        - **部署时必须录入**：宠物物种、个体 ID（多只混养时唯一标识）、首次入缸基线照片、首次入缸 SVL（吻肛长，单位 mm）、是否已有历史断尾记录（已断尾个体新长尾巴 = 再生尾，形态颜色不同）
        - 用户必须授权部署；繁殖场需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（饲养者 / 繁殖场管理员授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行守宫/蜥蜴断尾识别**
        - 调用 `-m scripts.smyx_reptile_tail_loss_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地守宫/蜥蜴尾部高清图像或视频文件路径
            - `--url`: 网络守宫/蜥蜴尾部图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，爬宠断尾场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，饲养者 / 繁殖场管理员授权）
            - `--list`: 显示守宫/蜥蜴断尾事件历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的守宫/蜥蜴断尾事件报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、爬宠箱 ID（enclosure_id）、个体 ID（individual_id）、宠物物种（species）、尾长测量信号（tail_length_signals：tail_length_pixels / tail_length_mm_estimated / tail_to_svl_ratio / tail_length_history_baseline / tail_shortening_ratio）、断端形态信号（tail_tip_signals：tail_tip_morphology / wound_visible / scab_present / redness_swelling_score_0_5 / discharge_or_pus_detected）、再生尾信号（regenerated_signals：is_regenerated_tail / regenerated_tail_color_anomaly）、排除上下文（context_signals：is_during_shedding_cycle / multi_individual_cohabitation / recent_handling_stress / previous_autotomy_recorded / image_quality_acceptable）、综合场景判定（composite_scene：tail_intact_normal / tail_shedding_artifact / tail_regenerated_baseline / tail_loss_event_fresh / tail_loss_event_with_infection_risk / tail_loss_event_scabbed / tail_signal_unreliable）、提醒等级（alert_level：none / info / important / urgent）、提醒动作列表（alert_actions：log_only / log_scabbed_recovery / important_isolate_clean_stable_env / urgent_isolate_vet_contact，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / isolate_to_separate_enclosure / rinse_wound_with_pet_saline / keep_environment_clean / monitor_appetite_alertness / contact_reptile_vet，**不含具体药物品牌、剂量、消毒液品牌、抗生素品牌、外科操作**）、免责声明（disclaimer：AI 视觉识别仅供参考，伤口处理与感染判断需结合现场观察并由专业爬宠兽医确认）
        - **重要提示**：仅输出基于视觉的客观判断结果，**不构成任何败血症 / 骨髓炎 / 蜂窝织炎 / 坏死性皮炎等具体疾病诊断**；**绝对不输出具体药物名称、剂量、消毒液品牌、抗生素品牌、外用药膏品牌**；**绝对不输出"撒云南白药""涂红霉素软膏""用碘伏""口服阿莫西林""自行缝合""自行剪除坏死组织"等任何处方剂量或外科操作建议**

## 资源索引

- 必要脚本：见 [scripts/smyx_reptile_tail_loss_detection_analysis.py](scripts/smyx_reptile_tail_loss_detection_analysis.py)(
  用途：调用 API 进行守宫/蜥蜴断尾识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、7 类综合场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4，最大 10MB；摄像头需**完整展示从泄殖腔到尾尖的整条尾部**；**分辨率 ≥ 1080p**（像素测量精度要求高）；每日 ≥ 1 张
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心采样窗口**：每日 ≥ 1 张（建议早晚各 1 张），对比历史 7 天基线
- **核心阈值**：`tail_shortening_ratio` **≥ 20%** + 断端可见伤口或新鲜创面 → 触发断尾事件
- **4 级提醒策略递进**（none → info → important → urgent）
- 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 3 / **Level 4 不设上限（断尾感染急症）**
- 红线约束：
    - **🚨 禁止**做"败血症 / 骨髓炎 / 蜂窝织炎 / 坏死性皮炎"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、消毒液品牌、抗生素品牌、外用药膏品牌（仅可中性表述"宠物专用生理盐水冲洗"）
    - **🚨 绝对禁止**输出"撒云南白药""涂红霉素软膏""用碘伏""口服阿莫西林"等具体处方剂量
    - **🚨 绝对禁止**输出"自行缝合伤口""自行剪除坏死组织"等任何外科操作（必须由兽医现场判断）
    - **禁止**长期存储完整爬宠箱视频/图像（≤ 30 天，留尾长时间序列 + 断尾事件关键图像；繁殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停加热灯 / UVB / 灯光参数；任何设备控制变更必须由用户确认（仅可建议隔离）
    - **绝对禁止**伪造或夸大尾长缩短比例、伤口评分等指标；所有数据必须基于真实图像分析
    - **必须**按 **species 是否具自割能力（autotomy）匹配判定**：豹纹守宫 / 肥尾守宫 / 蓝舌石龙子 / 部分石龙子 / 部分壁虎具自割能力可再生；鬃狮蜥 / 大多数 monitor / 鳄鱼不能再生；绿鬣蜥幼体可再生但成体困难
    - **必须**识别**再生尾基线**：再生尾形态颜色与原尾不同（球状钝端、无原始鳞片、颜色稍异），**严禁误判再生尾为新发断尾**
    - **必须**考虑生理性上下文（**蜕皮期尾尖白皮假象 / 多只混养争斗高发 / 近期人为操作应激 / 已有历史断尾再生基线**），避免误判
    - **必须**在图像模糊 / 尾尖未完整露出 / 光照不足 / 无 SVL 参考 / 分辨率 < 1080p 时返回 `tail_signal_unreliable` 并建议重新拍摄
- **必须**：连续 ≥ 2 次 Level 4 → 强烈建议联系**专业爬宠兽医**（断尾感染可能引发败血症致死）
- **必须**：断尾事件报告**按 enclosure_id + individual_id + 事件时间戳输出**，含尾长 + 缩短比例 + 断端形态 + 伤口评分 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史断尾事件记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"缩短比例/形态/场景"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`爬宠断尾事件-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 缩短比例/形态/场景 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 爬宠断尾事件-20260525102300001 | 35% / open_wound / tail_loss_event_with_infection_risk | 2026-05-25 10:23:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地守宫/蜥蜴尾部高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_tail_loss_detection_analysis --input /path/to/tail.jpg --open-id your-open-id

# 分析网络守宫/蜥蜴尾部图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_reptile_tail_loss_detection_analysis --url https://example.com/tail.jpg --open-id your-open-id

# 显示历史断尾事件记录清单（自动触发关键词：查看守宫/蜥蜴断尾历史报告等）
python -m scripts.smyx_reptile_tail_loss_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_reptile_tail_loss_detection_analysis --input tail.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_reptile_tail_loss_detection_analysis --input tail.jpg --open-id your-open-id --output result.json
```
