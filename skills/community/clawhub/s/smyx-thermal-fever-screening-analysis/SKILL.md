---
name: "smyx-thermal-fever-screening-analysis"
description: "Using a fixed thermal-imaging camera installed in public areas (e.g., living room, dining room), the system automatically analyzes each person's skin-surface temperature (usually forehead or facial region) when multiple people gather, and computes the difference between an individual's temperature and the average temperature of others in the scene. When someone's temperature is significantly higher than the surrounding group (delta exceeds a preset threshold, e.g., 1.5 °C), it outputs a 'relative temperature anomaly' alert and recommends rechecking with a calibrated forehead thermometer. The skill is suitable for family gatherings, small meetings, etc., and aids early screening of people with fever. Application scenarios: family living rooms, meeting rooms, kindergarten activity rooms, nursing-home activity areas. The system monitors in real time; when someone's temperature is clearly higher than others, it pushes a mobile-app alert to remind attention to health. Skill features: during flu season or epidemics, if a household member has a fever during gatherings, quick screening enables timely precautions. Relative-temperature detection reduces reliance on absolute-temperature calibration, allowing ordinary families to use a thermal-imaging camera for health monitoring. Can be integrated into smart-home security systems to strengthen family health protection. | 通过安装于公共区域（如客厅、餐厅）的固定热成像摄像头，在多人聚集时自动分析每个人的体表温度（通常为额头或面部区域），计算个体温度与场景内其他人平均温度的差值。当某个人温度显著高于周边人群（差值超过预设阈值，如1.5℃）时，输出'体温相对异常'提醒，建议使用额温枪复测。该技能适用于家庭聚会、小型会议等场景，辅助早期筛查发热人员。应用场景：家庭客厅、会议室、幼儿园活动室、养老院活动区。系统实时监测，当检测到某人体温明显高于他人时，通过手机APP推送提醒，提示注意健康状态。技能特点：在流感季节或疫情期间，家庭聚会中若有成员发热，可快速筛查并采取防护措施。通过相对温度检测，可降低对绝对温度校准的要求，使普通家庭也能使用热成像摄像头进行健康监测。该技能可集成到智能家居安防系统中，提升家庭健康防护能力。"
version: "1.0.0"
---

# Thermal Relative Fever Screening (Multi-Person Gathering) | 家庭多人聚集时体温相对异常检测

Using a fixed thermal-imaging camera installed in public areas (e.g., living room, dining room), the system automatically analyzes each person's skin-surface temperature (usually forehead or facial region) when multiple people gather, and computes the difference between an individual's temperature and the average temperature of others in the scene. When someone's temperature is significantly higher than the surrounding group (delta exceeds a preset threshold, e.g., 1.5 °C), it outputs a 'relative temperature anomaly' alert and recommends rechecking with a calibrated forehead thermometer. The skill is suitable for family gatherings, small meetings, etc., and aids early screening of people with fever. Application scenarios: family living rooms, meeting rooms, kindergarten activity rooms, nursing-home activity areas. The system monitors in real time; when someone's temperature is clearly higher than others, it pushes a mobile-app alert to remind attention to health. Skill features: during flu season or epidemics, if a household member has a fever during gatherings, quick screening enables timely precautions. Relative-temperature detection reduces reliance on absolute-temperature calibration, allowing ordinary families to use a thermal-imaging camera for health monitoring. Can be integrated into smart-home security systems to strengthen family health protection.

通过安装于公共区域（如客厅、餐厅）的固定热成像摄像头，在多人聚集时自动分析每个人的体表温度（通常为额头或面部区域），计算个体温度与场景内其他人平均温度的差值。当某个人温度显著高于周边人群（差值超过预设阈值，如1.5℃）时，输出'体温相对异常'提醒，建议使用额温枪复测。该技能适用于家庭聚会、小型会议等场景，辅助早期筛查发热人员。应用场景：家庭客厅、会议室、幼儿园活动室、养老院活动区。系统实时监测，当检测到某人体温明显高于他人时，通过手机APP推送提醒，提示注意健康状态。技能特点：在流感季节或疫情期间，家庭聚会中若有成员发热，可快速筛查并采取防护措施。通过相对温度检测，可降低对绝对温度校准的要求，使普通家庭也能使用热成像摄像头进行健康监测。该技能可集成到智能家居安防系统中，提升家庭健康防护能力。

## 🎯 AI 角色

**假设你是一个专业的群体体温筛查 AI。你的任务是分析固定热成像摄像头拍摄的多人聚集视频，检测每个个体的体表温度（头部区域），计算个体温度与同期场景内所有个体平均温度的差值。当差值超过预设阈值时，输出相对温度异常提醒。不要提供医疗诊断或具体疾病判定，仅输出基于热成像的相对温度差异与方向性提醒。**

## 任务目标

- 本 Skill 用于：基于热成像摄像头多人聚集视频，自动检测每个人额头体表温度 → 计算个体相对群体均值的差值 → 输出相对体温异常提醒并建议额温枪复测
- 能力包含：多人体检测与身份编号、头部/额头 ROI 定位、热成像像素 → 温度（°C）换算、群体均值/标准差统计、个体 - 群体差值计算、相对异常判定（默认 |Δ| > 1.5 °C）、有效样本数校验、持续时间过滤（≥ 3 秒）、APP 推送文本生成
- 触发条件:
    1. **默认触发**：当用户提供热成像摄像头多人聚集视频 URL 或文件需要分析时，默认触发本技能进行体温相对异常筛查
    2. 当用户明确提及发热筛查、体温相对异常、热成像、群体测温、家庭聚会健康、流感季节、疫情防控、幼儿园/养老院测温等关键词，并且上传了热成像视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看体温筛查历史报告、发热相对异常报告清单、群体测温报告清单、查询历史筛查记录、显示所有体温筛查报告、显示家庭聚会健康报告，查询体温异常预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有体温筛查报告"、"
       显示所有发热相对异常报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_thermal_fever_screening_analysis --list --open-id` 参数调用 API
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

**在执行家庭多人聚集体温相对异常检测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备热成像摄像头多人聚集视频输入**
        - 提供本地热成像视频路径或网络 URL
        - 摄像头建议：**必须为热成像（红外测温）摄像头**，普通可见光摄像头无法支持
        - 安装于客厅/餐厅/会议室/活动室等公共区域，可同时覆盖 ≥ 2 人；分辨率 ≥ 256×192（建议 384×288 或更高），帧率 ≥ 5 FPS
        - 测温距离 1-3 m 之间为佳；测温目标头部需充分露出（避免帽子/口罩遮挡额头）
        - 环境温度建议恒定，避免短时空调直吹、紧邻热源（炉灶/取暖器）
        - 可选附带：场景名称、参与人数、阈值覆盖（temperature_delta_threshold_c / min_sample_size）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行多人聚集体温相对异常检测**
        - 调用 `-m scripts.smyx_thermal_fever_screening_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地热成像摄像头多人聚集视频文件路径
            - `--url`: 网络热成像摄像头多人聚集视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，群体体温筛查场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示家庭多人聚集体温相对异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的体温相对异常筛查报告
        - 包含：检测到人数（persons_detected）、有效样本数（face_visible_count / sample_sufficient）、群体统计（group_metrics：group_avg_temperature / group_temperature_std）、每个人结果列表（per_person_results，含 person_id / forehead_temp_c / delta_c / is_relative_anomaly / anomaly_type：relatively_hotter / relatively_colder / insufficient_sample）、异常人数（anomaly_count）、推送文本（如"客厅检测到 4 人，其中 1 人额头体表温度比群体均值高 1.8°C，建议使用额温枪复测体温"）、建议动作（recommend_action：recheck_with_thermometer / push_app_notice / observe_only）
        - **重要提示**：仅输出基于热成像的相对温度差异与方向性提醒，不提供发热/流感/COVID 等具体医学诊断；正式体温判定请使用经过校准的医用红外/水银/电子额温枪/口腔体温计复测，并由专业医生评估

## 资源索引

- 必要脚本：见 [scripts/smyx_thermal_fever_screening_analysis.py](scripts/smyx_thermal_fever_screening_analysis.py)(
  用途：调用 API 进行家庭多人聚集时体温相对异常检测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、相对体温阈值/有效样本/异常类型定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须是热成像（红外测温）摄像头视频，普通可见光视频无法识别温度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **本工具仅基于"群体相对差异"判定，不依赖绝对温度校准**；任何相对异常都建议使用经过校准的医用额温枪/电子体温计复测
- 戴帽子/口罩、刚运动/喝热饮/晒太阳、紧邻空调或取暖器等情况会显著影响额头体表温度，可能造成误报
- 隐私合规：热成像家庭视频涉及个人健康隐私，使用前需取得家庭成员/参与者知情同意，妥善加密保管
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"相对异常人数"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`家庭多人体温相对异常报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 相对异常人数 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 家庭多人体温相对异常报告-20260312172200001 | 1 人（Δ +1.8°C，relatively_hotter） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地热成像多人聚集视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_thermal_fever_screening_analysis --input /path/to/thermal.mp4 --open-id your-open-id

# 分析网络热成像多人聚集视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_thermal_fever_screening_analysis --url https://example.com/thermal.mp4 --open-id your-open-id

# 显示历史体温相对异常报告（自动触发关键词：查看体温筛查历史报告、发热相对异常报告清单等）
python -m scripts.smyx_thermal_fever_screening_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_thermal_fever_screening_analysis --input thermal.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_thermal_fever_screening_analysis --input thermal.mp4 --open-id your-open-id --output result.json
```
