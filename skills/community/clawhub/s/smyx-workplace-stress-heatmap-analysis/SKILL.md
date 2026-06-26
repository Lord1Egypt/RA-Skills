---
name: "smyx-workplace-stress-heatmap-analysis"
description: "Using fixed cameras in enterprise office areas (open-plan workstations), the system anonymously analyzes multiple employees' facial expressions (e.g., frowning, downturned mouth corners) and postures (e.g., rigid sitting, forward leaning, frequent eye rubbing), and applies a group-level stress assessment model to compute a real-time stress index for each workstation zone, generating a stress distribution heatmap of the entire office area (color from green to red — green indicates low stress, red indicates high stress). The skill does NOT identify individuals and only outputs group-level anonymous stress distribution to help managers understand team stress and optimize the work environment. Application scenarios: enterprise open-plan offices, R&D centers, customer-service centers. The system periodically (e.g., hourly) generates stress heatmaps for organizational-health monitoring. Skill features: long-term high-intensity work stress reduces efficiency, increases turnover, and causes burnout. With a group stress heatmap, managers can intuitively see team stress distribution, adjust workload, optimize the office environment, and improve employee well-being and productivity. Can be integrated into enterprise security systems or health-management platforms as an innovative smart-office feature. | 通过企业办公区（开放式工位）的固定摄像头，匿名分析多名员工的面部表情（如皱眉、嘴角下垂）和姿态（如僵坐、前倾、频繁揉眼），使用群体压力评估模型计算每个工位区域的实时压力指数，生成整个办公区的压力分布热力图（颜色从绿到红，绿色代表低压力，红色代表高压力）。该技能不识别个人身份，仅输出群体层面的匿名压力分布，帮助企业管理者了解团队压力状态，优化工作环境。应用场景：企业开放式办公区、研发中心、客服中心。系统定期（如每小时）生成压力热力图，用于组织健康度监测。技能特点：长期高强度工作压力会导致员工效率下降、离职率升高、职业倦怠。通过群体压力热力图，管理者可直观了解团队压力分布，及时调整工作安排、优化办公环境，提升员工福祉和企业生产力。该技能可集成到企业安防系统或健康管理平台中，成为智慧办公的创新功能。"
version: "1.0.0"
---

# Workplace Group Stress Heatmap | 职场员工压力群体热力图

Using fixed cameras in enterprise office areas (open-plan workstations), the system anonymously analyzes multiple employees' facial expressions (e.g., frowning, downturned mouth corners) and postures (e.g., rigid sitting, forward leaning, frequent eye rubbing), and applies a group-level stress assessment model to compute a real-time stress index for each workstation zone, generating a stress distribution heatmap of the entire office area (color from green to red — green indicates low stress, red indicates high stress). The skill does NOT identify individuals and only outputs group-level anonymous stress distribution to help managers understand team stress and optimize the work environment. Application scenarios: enterprise open-plan offices, R&D centers, customer-service centers. The system periodically (e.g., hourly) generates stress heatmaps for organizational-health monitoring. Skill features: long-term high-intensity work stress reduces efficiency, increases turnover, and causes burnout. With a group stress heatmap, managers can intuitively see team stress distribution, adjust workload, optimize the office environment, and improve employee well-being and productivity. Can be integrated into enterprise security systems or health-management platforms as an innovative smart-office feature.

通过企业办公区（开放式工位）的固定摄像头，匿名分析多名员工的面部表情（如皱眉、嘴角下垂）和姿态（如僵坐、前倾、频繁揉眼），使用群体压力评估模型计算每个工位区域的实时压力指数，生成整个办公区的压力分布热力图（颜色从绿到红，绿色代表低压力，红色代表高压力）。该技能不识别个人身份，仅输出群体层面的匿名压力分布，帮助企业管理者了解团队压力状态，优化工作环境。应用场景：企业开放式办公区、研发中心、客服中心。系统定期（如每小时）生成压力热力图，用于组织健康度监测。技能特点：长期高强度工作压力会导致员工效率下降、离职率升高、职业倦怠。通过群体压力热力图，管理者可直观了解团队压力分布，及时调整工作安排、优化办公环境，提升员工福祉和企业生产力。该技能可集成到企业安防系统或健康管理平台中，成为智慧办公的创新功能。

## 🎯 AI 角色

**假设你是一个专业的职场健康分析 AI。你的任务是分析办公区固定摄像头的视频，对画面中的员工进行匿名检测（不识别个人身份），提取面部紧张特征（皱眉、嘴角下垂）和姿态僵硬度（长时间保持同一姿势、肩部耸起），计算每个工位区域的群体压力指数，并生成伪彩色热力图。不要识别或记录个人身份，仅输出区域级别的匿名统计与管理者参考建议。**

## 任务目标

- 本 Skill 用于：基于企业办公区固定摄像头视频，**匿名**提取面部紧张特征 + 姿态僵硬度 + 揉眼/前倾等疲劳信号 → 按 ROI 区域聚合 → 输出区域级压力指数 + 整个办公区伪彩色热力图
- 能力包含：人体检测（不做人脸比对/身份关联）、面部紧张特征提取（皱眉强度 + 嘴角下垂幅度）、姿态僵硬度（同姿势持续时长 + 肩部耸起角度）、揉眼事件计数、前倾坐姿比例统计、按工位 ROI 聚合 + 最小样本数保护（< 3 人时不输出，避免单人识别）、综合群体压力指数（0-100）、伪彩色映射（green → red）、与上一时段对比的趋势分析、热点区域识别、管理者中性参考建议生成
- 触发条件:
    1. **默认触发**：当用户提供办公区固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行职场员工压力群体热力图分析
    2. 当用户明确提及职场压力、办公区压力、群体压力、压力热力图、组织健康、员工倦怠、智慧办公健康等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看职场压力历史报告、压力热力图报告清单、办公区压力分布清单、查询历史群体压力记录、显示所有职场压力分析报告、显示组织健康度诊断报告，查询压力热力图预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有职场压力热力图报告"、"
       显示所有办公区压力报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_workplace_stress_heatmap_analysis --list --open-id` 参数调用 API
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

**在执行职场员工压力群体热力图分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备办公区固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议时长 ≥ 5 分钟
        - 摄像头建议：企业开放式办公区/研发中心/客服中心固定摄像头，**高位俯视或斜俯视**，画面应覆盖多个工位区域
        - 帧率 ≥ 2 FPS、分辨率 ≥ 720p、光照稳定
        - 初次部署需在画面中**框选多个工位区域 ROI**（zone_id + zone_label，如 zone_A / zone_B / zone_C）
        - **强匿名约束**：禁止启用人脸识别 / 人脸比对 / 身份关联
        - 可选附带：办公区平面图（用于叠加热力图）、采样窗口（如每小时一次）、最小样本数阈值（默认 3）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行职场员工压力群体热力图分析**
        - 调用 `-m scripts.smyx_workplace_stress_heatmap_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地办公区固定摄像头视频文件路径
            - `--url`: 网络办公区固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，职场健康分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示职场员工压力群体热力图历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的职场员工压力群体热力图报告
        - 包含：采样时间窗口（time_window）、各工位区域聚合数据（zones：zone_id / zone_label / person_count_in_zone / facial_tension_score / posture_rigidity_score / eye_rubbing_event_count_hourly / forward_leaning_ratio / stress_index / heatmap_color）、整个办公区综合压力指数（office_overall_stress_index）、压力最高的若干区域（top_pressure_zones）、相比上一时段变化（trend_vs_last_window：delta_pct）、提醒类型（alert_type：zone_high_stress / overall_high_stress / improving / normal）、提醒级别（alert_level：info / notice / warning）、管理者建议（manager_suggestion，如"zone_B 连续 3 个时段高压力，建议关注负责的项目排期、增加短茶歇"）、伪彩色热力图 URL（heatmap_image_url，叠加在办公区平面图上）
        - **重要提示**：仅输出基于视觉的群体行为聚合统计与管理者参考建议，**不提供员工个人心理诊断、绩效评价或个人画像**；任何针对个体的关怀沟通应由 HR / 直属经理依据自愿性问卷和访谈进行

## 资源索引

- 必要脚本：见 [scripts/smyx_workplace_stress_heatmap_analysis.py](scripts/smyx_workplace_stress_heatmap_analysis.py)(
  用途：调用 API 进行职场员工压力群体热力图匿名分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、区域压力指数/伪彩色映射/强匿名约束和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：高位俯视或斜俯视、画面覆盖多个工位区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 单区域人数 < 3 时只输出 `insufficient_sample`，**不输出 stress_index**，避免实际等同于单人识别
- 部分日常动作（讨论、阅读、思考）可能在面部表情上接近"皱眉"特征，建议结合多帧时序均值
- 强匿名约束：本工具**禁止**做人脸识别 / 人脸比对 / 身份绑定；**禁止**输出"某员工压力高"这类个体结论；**禁止**长期存储原始视频或可识别个人特征的数据
- 合规建议：部署前**面向全体员工公示并取得知情同意**，建议由 HR + 工会双方备案；明确告知"采集方式 / 数据保存期限 / 不绑定个人 / 不参与绩效评价"
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"办公区压力/热点区域"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`职场员工压力群体热力图报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 办公区压力/热点区域 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 职场员工压力群体热力图报告-20260312172200001 | 整体 72 / 热点 zone_B (85, red) | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地办公区视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_workplace_stress_heatmap_analysis --input /path/to/office.mp4 --open-id your-open-id

# 分析网络办公区视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_workplace_stress_heatmap_analysis --url https://example.com/office.mp4 --open-id your-open-id

# 显示历史职场员工压力群体热力图报告（自动触发关键词：查看职场压力历史报告、压力热力图报告清单等）
python -m scripts.smyx_workplace_stress_heatmap_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_workplace_stress_heatmap_analysis --input office.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_workplace_stress_heatmap_analysis --input office.mp4 --open-id your-open-id --output result.json
```
