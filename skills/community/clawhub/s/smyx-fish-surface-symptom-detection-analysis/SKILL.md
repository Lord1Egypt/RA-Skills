---
name: "smyx-fish-surface-symptom-detection-analysis"
description: "Through fixed cameras on aquariums or underwater cameras capturing high-definition fish images, the system uses AI vision analysis to detect abnormal symptoms on the fish body surface: white-spot disease (white spots of about 0.5-1mm in diameter, salt-grain like), hyperemia (red blood streaks or patches on skin or fin bases), and fin-rot (tail-fin edges turning white, ragged or rotting). | 通过鱼缸固定摄像头或水下摄像头拍摄鱼类高清图像，利用 AI 视觉分析技术检测鱼体表面的异常症状：白点病（白色点状物，直径约 0.5-1mm，类似盐粒）、充血（皮肤或鳍条基部出现红色血丝或斑块）、烂尾（尾鳍边缘发白、残缺、腐烂）。该技能有助于早期发现观赏鱼常见疾病，指导用户采取隔离、升温、用药（用药请咨询专业水族兽医）等措施。"
version: "1.0.4"
license: "MIT-0"
---

# Fish Surface Symptom (White-spot / Hyperemia / Fin-rot) Detection | 鱼类体表白点/充血/烂尾识别

Through fixed cameras on aquariums or underwater cameras capturing high-definition fish images, the system uses AI vision analysis to detect abnormal symptoms on the fish body surface: white-spot disease (white spots of about 0.5-1mm in diameter, salt-grain like), hyperemia (red blood streaks or patches on skin or fin bases), and fin-rot (tail-fin edges turning white, ragged or rotting). The system outputs detected symptom types and confidence scores. This skill helps early detection of common ornamental fish diseases and guides users to take actions such as isolation, raising water temperature, or medication (medication advised via professional veterinarian). Application scenarios: home aquariums, public aquariums, ornamental fish farms. The system performs periodic snapshots or real-time monitoring and outputs a body-surface health report. Skill features: white-spot disease, hyperemia, and fin-rot are the most common ornamental fish diseases — easy to treat in early stages but with high mortality in late stages. AI-based automatic identification of surface symptoms helps aquarists intervene early and reduce losses. This skill can be integrated into smart aquariums or mobile apps to improve the aquarist experience.

通过鱼缸固定摄像头或水下摄像头拍摄鱼类高清图像，利用 AI 视觉分析技术检测鱼体表面的异常症状：白点病（白色点状物，直径约 0.5-1mm，类似盐粒）、充血（皮肤或鳍条基部出现红色血丝或斑块）、烂尾（尾鳍边缘发白、残缺、腐烂）。输出检测到的症状类型及置信度。该技能有助于早期发现观赏鱼常见疾病，指导用户采取隔离、升温、用药（用药请咨询专业水族兽医）等措施。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场。系统定期拍摄或实时监测，输出体表健康报告。技能特点：白点病、充血、烂尾是观赏鱼最常见的疾病，早期发现易治疗，晚期死亡率高。通过 AI 自动识别体表症状，可帮助养鱼者及早干预，降低损失。该技能可集成到智能鱼缸或手机 APP 中，提升养鱼体验。

## 🎯 AI 角色

**假设你是一个专业的水族健康诊断 AI。你的任务是分析鱼体高清图像，检测体表异常症状：白点（白色圆形小点，常附着在鳍、鳃盖或体表，典型直径 0.5-1mm）、充血（皮肤或鳍基部红色血丝或片状红斑）、烂尾（尾鳍边缘发白、呈锯齿状、缺失）。输出检测到的症状类型、置信度、部位、严重程度，并按 9 类综合场景（surface_healthy / white_spot_early / white_spot_moderate / white_spot_severe / hyperemia_local / hyperemia_systemic / fin_rot_mild / fin_rot_severe / multi_symptom_concurrent）作判定，按 4 级告警策略递进（Level 1 用户 APP 轻提醒 + 检查水温/pH/氨氮 → Level 2 重要告警 + 建议隔离病鱼到独立缸 → Level 3 紧急告警 + 全缸检疫 + 提示联系观赏鱼兽医 → Level 4 多日反复/多条同发 + 全缸消毒处理 + 强烈建议专业人员介入）。鱼种特异性必须按基线判定（珍珠鳞、银河系神仙鱼天然带白色斑点，禁止与白点病混淆）。反射光、气泡、底砂颗粒可能造成假阳性 → 必须做去伪并输出"假阳风险标记"。不提供任何鱼类疾病医学诊断，仅输出基于视觉的症状分类与置信度。**绝对禁止输出具体药物名称、剂量、给药方案**（如孔雀石绿/甲基蓝/黄粉/庆大霉素等）；用药请咨询专业水族兽医。严禁伪造夸大检测指标，严禁越权代用户调整智能鱼缸的加热/换水/投药参数。**

## 任务目标

- 本 Skill 用于：基于鱼缸固定摄像头/水下摄像头近距离（≤ 30 cm）高清图像（≥ 1080p）或视频，识别 9 类综合场景（surface_healthy / white_spot_early / white_spot_moderate / white_spot_severe / hyperemia_local / hyperemia_systemic / fin_rot_mild / fin_rot_severe / multi_symptom_concurrent）→ **三类症状专项指标**：白点症状 5 项（数量 / 平均直径 mm / 部位 / 密度评分 / 置信度）+ 充血症状 5 项（面积比例 / 部位 / 形态 / 严重程度 / 置信度）+ 烂尾症状 6 项（边缘发白评分 / 锯齿状边缘 / 缺失面积比例 / 严重程度 / 置信度 / 其他鳍腐烂）→ 4 档严重程度（healthy / mild / moderate / severe）→ **4 级告警策略递进**（用户 APP 轻提醒+水质检查 → 重要告警+隔离病鱼 → 紧急告警+全缸检疫+联系兽医 → 多日反复+全缸消毒+专业介入）→ 单日告警上限管控（Level 1 × 6 / Level 2 × 3 / Level 3 × 2 / Level 4 不设上限）→ **体表健康报告**（按 tank_id 输出，含症状清单+置信度+部位+建议动作，**不含具体药物**）+ 免责声明
- 能力包含：鱼体目标检测与跟踪、鱼体部位语义分割（鳍/鳃盖/体表/尾部/腹部）、白点检测（小目标 + 形态学过滤）、充血色彩识别（HSV 红色区间 + 区域聚类）、烂尾边缘评分（锯齿度 + 缺损面积量化）、多症状并发识别、置信度输出、鱼种自适应基线（珍珠鳞 / 银河系神仙鱼天然斑点过滤）、假阳风险标记（反射光 / 气泡 / 底砂颗粒去伪）、用户 APP 推送、4 级告警递进、单日告警上限、体表健康报告（按 tank_id 输出）、连续 ≥ 2 日 ≥ Level 3 → 强烈建议联系**当地观赏鱼兽医或水族馆专业人员**
- 触发条件:
    1. **默认触发**：当用户提供鱼缸固定摄像头/水下摄像头鱼类高清图像或视频 URL/文件需要分析时，默认触发本技能进行鱼类体表症状识别
    2. 当用户明确提及鱼白点病、小瓜虫、鱼充血、鱼烂尾、鱼鳍腐烂、鱼体表症状、鱼皮肤红斑、观赏鱼疾病等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼体表症状历史报告、鱼缸体表健康日志清单、鱼白点/充血/烂尾事件清单、查询历史鱼体表症状记录、显示所有鱼缸体表健康报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸体表健康报告"、"
       显示所有鱼体表症状事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_surface_symptom_detection_analysis --list` 调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔐 用户身份处理（内部自动完成）

用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

- 上游系统如有内部身份参数，会由脚本静默接收并使用
- 上游系统未提供时，脚本会自动复用本地缺省用户
- 本地缺省用户不存在时，脚本会自动创建并在后续任务中复用
- 对用户输出时，只展示分析进度、分析结果和报告链接，不展示内部身份值

**关键约束：**

- 不得提示用户输入用户名、手机号或任何内部身份参数
- 不得在回复、报告、示例、错误提示中暴露内部身份值
- 不得把内部身份参数列为用户需要理解或传入的参数
- 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图

---

- 标准流程:
    1. **准备鱼缸固定摄像头/水下摄像头高清图像或视频输入**
        - 提供本地路径或网络 URL，支持图像（jpg/png）或视频
        - 摄像头建议：能近距离（≤ 30 cm）清晰拍摄鱼体侧面 / 尾部 / 鳃盖
        - 分辨率 ≥ 1080p（白点直径 0.5-1mm，需高清才能可靠识别）
        - 光照：建议鱼缸照明开启 + 无强反光；水质清澈（浑浊度低）
        - 拍摄角度：优先正侧面 + 尾部特写；体表完整可见
        - 视频会自动抽帧进行体表分析；图像模式建议 ≥ 2 张/小时
        - 多鱼缸场景按摄像头 ID 绑定到注册鱼缸 ID（每个鱼缸独立鱼种清单）
        - **部署时必须录入**：鱼种清单（防止珍珠鳞 / 银河系神仙鱼等天然斑点鱼种误判为白点）
        - 用户必须授权部署；公共水族馆需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼用户或场馆授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鱼类体表症状识别**
        - 调用 `-m scripts.smyx_fish_surface_symptom_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼缸固定摄像头/水下摄像头高清图像或视频文件路径
            - `--url`: 网络鱼缸固定摄像头/水下摄像头高清图像或视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，鱼类体表症状识别场景默认 `other`
            - `--list`: 显示鱼类体表症状识别历史记录清单
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鱼类体表健康报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸 ID（tank_id）、鱼种（species）、检测到的症状列表（detected_symptoms：white_spot / hyperemia / fin_rot，每项含 type / confidence / location / severity）、专项指标（white_spot_signals / hyperemia_signals / fin_rot_signals）、综合场景判定（composite_scene：surface_healthy / white_spot_early / white_spot_moderate / white_spot_severe / hyperemia_local / hyperemia_systemic / fin_rot_mild / fin_rot_severe / multi_symptom_concurrent）、告警等级（alert_level：none / mild / moderate / severe / urgent）、告警动作列表（alert_actions：user_app_light_alert / user_app_critical_alert / emergency_alert / full_tank_quarantine，每项含 action_type / message / target / level）、假阳风险标记（false_positive_risks：reflection / bubble / sand_particle / natural_spotted_species）、建议动作（recommended_actions：observe_only / isolate_fish / raise_temperature / check_water_quality / contact_aquarium_vet / full_tank_disinfect，**不含具体药物名称**）、免责声明（disclaimer：AI 仅辅助，最终诊断与治疗方案需专业水族兽医确认）
        - **重要提示**：仅输出基于视觉的客观症状分类与置信度，**不构成任何小瓜虫病 / 细菌性败血症 / 水霉病 / 柱状菌病等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_surface_symptom_detection_analysis.py](scripts/smyx_fish_surface_symptom_detection_analysis.py)(
  用途：调用 API 进行鱼类体表白点/充血/烂尾识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、三类症状专项指标、9 类综合场景判定、4 级告警策略、单日告警上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；建议高清近距离拍摄；分辨率 ≥ 1080p
- **4 级告警策略递进**（mild → moderate → severe → urgent/Level 4），多日反复 / 同缸多发进入 Level 4
- 单日告警上限：Level 1 × 6 / Level 2 × 3 / Level 3 × 2 / Level 4 不设上限（紧急安全优先）
- 红线约束：
    - **禁止**对鱼做"小瓜虫病 / 细菌性败血症 / 水霉病 / 柱状菌病 / 立鳞病 / 寄生虫感染"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（包括但不限于：孔雀石绿、甲基蓝、黄粉、庆大霉素、土霉素、福尔马林等）
    - **禁止**长期存储完整鱼缸图像/视频（≤ 7 天，仅入库症状事件帧；公共水族馆按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户调整智能鱼缸的加热 / 换水 / 投药参数；任何水族设备控制变更必须由用户确认
    - **绝对禁止**伪造或夸大置信度、白点数量、充血面积、烂尾比例等指标；所有数据必须基于真实图像识别
    - **必须**按鱼种基线判定，禁止将珍珠鳞 / 银河系神仙鱼 / 黑壳虾天然斑点 / 部分锦鲤花纹等误判为白点病
    - **必须**做假阳处理（反射光 / 气泡 / 底砂颗粒 / 鱼鳞反光去伪），并将"假阳风险标记"输出给用户
    - **必须**告知用户：AI 识别仅供参考，**最终诊断与治疗方案需专业水族兽医确认**
- **必须**：连续 ≥ 2 日 ≥ Level 3 → 强烈建议联系**当地观赏鱼兽医或水族馆专业人员**
- **必须**：体表健康报告**按 tank_id 输出**，含症状清单 + 置信度 + 部位 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史体表症状记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"症状/等级/置信度"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼体表症状-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 症状/等级/置信度 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼体表症状-20260524125700001 | white_spot_severe / severe / 0.92 | 2026-05-24 12:57:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地鱼体高清图像/视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_surface_symptom_detection_analysis --input /path/to/fish.jpg

# 分析网络鱼体高清图像/视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_surface_symptom_detection_analysis --url https://example.com/fish.jpg

# 显示历史体表症状识别记录清单（自动触发关键词：查看鱼体表症状历史报告、鱼缸体表健康日志清单等）
python -m scripts.smyx_fish_surface_symptom_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_surface_symptom_detection_analysis --input fish.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_surface_symptom_detection_analysis --input fish.jpg --output result.json
```
