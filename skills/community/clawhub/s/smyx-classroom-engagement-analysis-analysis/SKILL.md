---
name: "smyx-classroom-engagement-analysis-analysis"
description: "Using a fixed classroom camera, the system analyzes students' facial expressions (focused, confused, happy, frustrated, bored, etc.), computes a class-level overall engagement score (0-100), and can identify low-engagement student positions (no identity stored — for real-time teacher reminders only). Real-time analysis provides engagement heatmaps and abnormal alerts. | 通过教室固定摄像头，分析学生面部表情（专注、困惑、开心、沮丧、无聊等），计算班级整体参与度评分（0-100分），并可识别出参与度较低的学生个体（不存储身份，仅用于实时提醒）。该技能可辅助教师调整教学节奏，关注学习困难学生。"
version: "1.0.2"
license: "MIT-0"
---

# Student Classroom Engagement Analysis | 学生课堂情绪参与度分析

Using a fixed classroom camera, the system analyzes students' facial expressions (focused, confused, happy, frustrated, bored, etc.), computes a class-level overall engagement score (0-100), and can identify low-engagement student positions (no identity stored — for real-time teacher reminders only). The skill helps teachers adjust teaching pace and pay attention to students having learning difficulty. Application scenarios: K-12 classrooms, training courses, online education (students must be on camera). Real-time analysis provides engagement heatmaps and abnormal alerts. Skill features: it is difficult for a teacher to monitor every student's facial state in real time. AI-assisted analysis helps teachers timely detect confusion or boredom, adjust teaching strategy, and improve quality. Can be integrated into smart-classroom systems or lecture-recording devices.

通过教室固定摄像头，分析学生面部表情（专注、困惑、开心、沮丧、无聊等），计算班级整体参与度评分（0-100分），并可识别出参与度较低的学生个体（不存储身份，仅用于实时提醒）。该技能可辅助教师调整教学节奏，关注学习困难学生。应用场景：中小学教室、培训课堂、在线教育（需拍摄学生）。系统实时分析，为教师提供参与度热力图和异常提醒。技能特点：教师难以实时关注每个学生的表情状态。通过AI辅助分析，可帮助教师及时发现学生困惑或无聊，调整教学策略，提高教学质量。该技能可集成到智慧教室系统或录播设备中。

## 🎯 AI 角色

**假设你是一个专业的课堂教学分析 AI。你的任务是分析教室固定摄像头的视频，检测学生的人脸表情，识别专注、困惑、开心、沮丧、无聊等情绪类别，计算班级整体参与度评分。不存储学生身份信息，仅输出群体统计和匿名化的低参与度提示（仅返回座位坐标），作为教师实时教学辅助。**

## 任务目标

- 本 Skill 用于：基于教室固定摄像头视频，识别学生面部 6 类情绪（focused / confused / happy / frustrated / bored / neutral）+ 头部朝向 + 举手互动 → 输出班级群体参与度评分（0-100）→ 输出匿名低参与度座位坐标 + 困惑集中座位 + 教师实时教学建议 + 参与度热力图
- 能力包含：人脸检测（不做身份关联）、6 类情绪分类、头部姿态朝向估计（朝向讲台比例）、举手事件计数、教学环节推测（lecture / interaction / practice）、座位 ROI 网格映射（row × col）、班级整体参与度评分、低参与度座位识别（仅返回坐标）、困惑/沮丧热点识别、与上一时间窗对比的趋势分析、面向教师的中性教学建议生成、参与度伪彩色热力图
- 触发条件:
    1. **默认触发**：当用户提供教室固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行学生课堂情绪参与度分析
    2. 当用户明确提及课堂参与度、学生情绪、教学反馈、智慧教室、课堂困惑、走神、举手互动等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看课堂参与度历史报告、参与度报告清单、教学情绪报告清单、查询历史课堂参与度记录、显示所有课堂情绪分析报告、显示班级参与度诊断报告，查询课堂参与度预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有课堂参与度报告"、"
       显示所有班级情绪报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_classroom_engagement_analysis_analysis --list --open-id` 参数调用 API
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

**在执行学生课堂情绪参与度分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备教室固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议时长 ≥ 5 分钟、覆盖完整教学环节
        - 摄像头建议：中小学教室/培训课堂/在线教育摄像头，**讲台对面或斜侧高位**，画面应覆盖大部分学生脸部
        - 帧率 ≥ 5 FPS（推荐 10-15 FPS）、分辨率 ≥ 720p、光照稳定避免逆光
        - 初次部署需标定座位 ROI 网格（row × col，如 6×8）
        - **匿名约束**：禁止启用人脸识别 / 学生身份绑定；低参与度提醒仅返回座位坐标
        - 可选附带：教学环节标签（lecture/interaction/practice）、班级人数、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行学生课堂情绪参与度分析**
        - 调用 `-m scripts.smyx_classroom_engagement_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地教室固定摄像头视频文件路径
            - `--url`: 网络教室固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，课堂教学分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示学生课堂情绪参与度历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的学生课堂情绪参与度分析报告
        - 包含：采样时间窗口（time_window）、推测教学环节（teaching_phase_hint：lecture / interaction / practice / unknown）、当前学生人数（student_count_detected）、班级情绪分布（emotion_distribution：focused / confused / happy / frustrated / bored / neutral 占比）、专注比例（focus_ratio）、困惑比例（confusion_ratio）、无聊比例（bored_ratio）、头部朝向讲台比例（head_pose_toward_teacher_ratio）、举手次数（hand_raise_event_count）、班级整体参与度评分（engagement_score：0-100）、等级（engagement_level：excellent / good / fair / low）、**匿名**低参与度座位坐标（low_engagement_seats：[{row, col}, ...]，**不含身份**）、困惑集中座位（confusion_hotspot_seats：[{row, col}, ...]）、与上一时间窗变化（trend_vs_last_window：delta_pct）、提醒类型（alert_type：low_engagement / high_confusion / improving / normal）、提醒级别（alert_level：info / notice / warning）、教师建议（teacher_suggestion，如"班级整体参与度 38（low），建议穿插一个 2 分钟小组讨论或提问环节；困惑集中在 row=3 col=2 附近，建议复述刚才的概念"）、参与度热力图 URL（engagement_heatmap_image_url，叠加在教室座位图上）
        - **重要提示**：仅输出基于视觉的群体行为聚合统计与教学辅助提示，**不构成对任何学生的能力评价、心理诊断或个人画像**；任何针对个体的关怀沟通应由教师 / 心理老师依据课堂观察与自愿性谈话进行

## 资源索引

- 必要脚本：见 [scripts/smyx_classroom_engagement_analysis_analysis.py](scripts/smyx_classroom_engagement_analysis_analysis.py)(
  用途：调用 API 进行学生课堂情绪参与度分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、6 类情绪/参与度阈值/座位匿名约束和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：讲台对面/斜侧高位、覆盖大部分学生脸部
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 在线教育场景需确保学生摄像头开启且采集合法合规
- 部分日常表情（思考、记笔记低头）易被误识为"无聊"或"困惑"，建议结合短时序均值
- 教学环节切换（如讲解 → 练习）期间短暂参与度下降视为正常，不应立即触发提醒
- 强匿名约束：本工具**禁止**做人脸识别 / 学生身份绑定；**禁止**用于学生绩效评估、家长沟通或公开排名；**禁止**长期存储原始视频或可识别个人特征的数据
- 合规要点：涉及未成年人，必须取得**学校 + 家长**双重知情同意，并明确告知用途与数据保存期限；建议由教务处统一备案
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"参与度/教学环节/热点"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`课堂情绪参与度报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 参与度/教学环节/热点 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 课堂情绪参与度报告-20260312172200001 | 62 (good) / lecture / 困惑集中 row=3 col=2 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地教室视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_classroom_engagement_analysis_analysis --input /path/to/classroom.mp4 --open-id your-open-id

# 分析网络教室视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_classroom_engagement_analysis_analysis --url https://example.com/classroom.mp4 --open-id your-open-id

# 显示历史学生课堂情绪参与度报告（自动触发关键词：查看课堂参与度历史报告、参与度报告清单等）
python -m scripts.smyx_classroom_engagement_analysis_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_classroom_engagement_analysis_analysis --input classroom.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_classroom_engagement_analysis_analysis --input classroom.mp4 --open-id your-open-id --output result.json
```
