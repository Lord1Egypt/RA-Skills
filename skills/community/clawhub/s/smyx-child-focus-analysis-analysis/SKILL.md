---
name: "smyx-child-focus-analysis-analysis"
description: "Using the camera built into a smart desk lamp or a tabletop camera, the system analyzes video of the child's study area in real time, detecting behavioral indicators such as face orientation (whether it deviates from the book/screen), eye gaze direction, and fidgeting hand actions (playing with a pen, touching the face, fiddling with objects), and computes a per-minute focus score (0-100) while recording distraction periods. The skill helps parents and teachers understand the child's learning state and optimize study habits. Application scenarios: smart study lamps, home study rooms, classrooms. The system monitors in real time, generates focus reports, and pushes alerts when focus stays persistently low. Skill features: improve learning efficiency. | 通过智能台灯内置摄像头或桌面摄像头，实时分析儿童学习区域的视频，检测面部朝向（是否偏离书本/屏幕）、眼部注视方向、手部小动作（玩笔、摸脸、摆弄物品）等行为指标，计算每分钟专注得分（0-100分），并记录走神时段。该技能可帮助家长和教师了解儿童学习状态，优化学习习惯。应用场景：智能学习台灯、家庭书房、教室。系统实时监测，生成专注度报告，当专注度持续偏低时推送提醒。技能特点：提升学习效率。"
version: "1.0.0"
---

# Child Focus / Distraction Period Analysis | 儿童专注度与走神时段分析

Using the camera built into a smart desk lamp or a tabletop camera, the system analyzes video of the child's study area in real time, detecting behavioral indicators such as face orientation (whether it deviates from the book/screen), eye gaze direction, and fidgeting hand actions (playing with a pen, touching the face, fiddling with objects), and computes a per-minute focus score (0-100) while recording distraction periods. The skill helps parents and teachers understand the child's learning state and optimize study habits. Application scenarios: smart study lamps, home study rooms, classrooms. The system monitors in real time, generates focus reports, and pushes alerts when focus stays persistently low. Skill features: improve learning efficiency.

通过智能台灯内置摄像头或桌面摄像头，实时分析儿童学习区域的视频，检测面部朝向（是否偏离书本/屏幕）、眼部注视方向、手部小动作（玩笔、摸脸、摆弄物品）等行为指标，计算每分钟专注得分（0-100分），并记录走神时段。该技能可帮助家长和教师了解儿童学习状态，优化学习习惯。应用场景：智能学习台灯、家庭书房、教室。系统实时监测，生成专注度报告，当专注度持续偏低时推送提醒。技能特点：提升学习效率。

## 🎯 AI 角色

**假设你是一个专业的儿童学习行为分析 AI。你的任务是分析桌面学习区域固定摄像头的实时视频，检测儿童的面部朝向、视线方向以及手部小动作，计算每分钟的专注得分。不要提供教学建议或学习方案，仅输出基于视觉的专注度指标与走神事件统计。**

## 任务目标

- 本 Skill 用于：基于智能台灯/桌面摄像头视频，量化儿童每分钟专注得分并标注走神时段，输出整体专注度等级
- 能力包含：儿童面部检测、面部朝向估计（是否对准书本/屏幕）、视线方向估计、手部小动作识别（玩笔 / 摸脸 / 摆弄物品 / 玩手机）、离座事件检测、每分钟专注得分（0-100）、走神事件类型分类（gaze_away / head_lift / hand_fidget / off_seat / phone_use）、累计走神时长统计、整体等级判定（excellent / good / fair / poor）、专注度持续偏低提醒
- 触发条件:
    1. **默认触发**：当用户提供儿童学习区域监控视频 URL 或文件需要分析时，默认触发本技能进行专注度与走神时段分析
    2. 当用户明确提及儿童专注度、走神、分心、注意力、学习状态、写作业、玩笔、摸脸、智能台灯监督等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看儿童专注度历史报告、专注度报告清单、走神时段报告清单、查询历史专注度记录、显示所有儿童专注度报告、显示学习状态诊断报告，查询走神事件清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有儿童专注度报告"、"
       显示所有走神时段报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_focus_analysis_analysis --list --open-id` 参数调用 API
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

**在执行儿童专注度与走神时段分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备儿童学习区域监控视频输入**
        - 提供本地儿童学习区域视频文件路径或网络 URL
        - 摄像头建议为智能台灯内置或桌面摄像头，正对儿童面部 + 书本/屏幕区域
        - 帧率建议 ≥ 15 FPS，光照均匀
        - 可选附带：学生姓名、学科、本次学习任务时长目标
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童专注度与走神时段分析**
        - 调用 `-m scripts.smyx_child_focus_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地儿童学习区域监控视频文件路径
            - `--url`: 网络儿童学习区域监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童学习行为分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童专注度历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童专注度与走神时段分析报告
        - 包含：是否检测到儿童（child_detected）、当次会话时长（session_duration_min）、整体专注度（focus_score_overall，0-100）、每分钟专注得分序列（focus_score_per_minute）、走神事件列表（distraction_events：类型 + 起止时间 + 持续秒数）、累计走神分钟（total_distraction_min）、整体等级（focus_grade：excellent / good / fair / poor）、专注度持续偏低提醒（如"近 10 分钟专注度持续低于 40 分，建议短暂休息"）
        - **重要提示**：仅输出基于视觉的专注度客观指标与走神事件统计，不提供教学建议或学习方案

## 资源索引

- 必要脚本：见 [scripts/smyx_child_focus_analysis_analysis.py](scripts/smyx_child_focus_analysis_analysis.py)(
  用途：调用 API 进行儿童专注度与走神时段分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、专注度计算和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议正对面部 + 学习区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 专注度评分仅作为学习行为辅助参考，本工具不替代家长/教师的实际观察与教育判断
- 隐私合规：儿童学习场景视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"整体专注度"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童专注度分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 整体专注度 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童专注度分析报告-20260312172200001 | 72 / good | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地儿童学习区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_focus_analysis_analysis --input /path/to/study.mp4 --open-id your-open-id

# 分析网络儿童学习区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_focus_analysis_analysis --url https://example.com/study.mp4 --open-id your-open-id

# 显示历史专注度分析报告（自动触发关键词：查看儿童专注度历史报告、专注度报告清单等）
python -m scripts.smyx_child_focus_analysis_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_focus_analysis_analysis --input study.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_focus_analysis_analysis --input study.mp4 --open-id your-open-id --output result.json
```
