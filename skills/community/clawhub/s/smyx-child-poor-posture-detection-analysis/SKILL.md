---
name: "smyx-child-poor-posture-detection-analysis"
description: "Using the camera built into a smart desk lamp or mounted above the desk, the system analyzes the child's sitting-posture video in real time, detecting spinal curvature angle (estimated Cobb angle) and head tilt angle. | 通过智能台灯内置摄像头或书桌上方摄像头，实时分析儿童学习时的坐姿视频，检测脊柱弯曲角度（Cobb角估算）以及头部倾斜度（侧倾角）。当驼背（Cobb角>10°）或歪头（头部侧倾角>15°）持续时间超过预设阈值（如5秒）时，触发语音提醒（如'请坐直'、'头抬正'），帮助儿童养成良好坐姿习惯，预防近视和脊柱侧弯。"
version: "1.0.1"
license: "MIT-0"
---

# Child Poor Posture (Hunchback / Head Tilt) Real-Time Reminder | 儿童坐姿不良（驼背/歪头）实时提醒

Using the camera built into a smart desk lamp or mounted above the desk, the system analyzes the child's sitting-posture video in real time, detecting spinal curvature angle (estimated Cobb angle) and head tilt angle. When hunchback (Cobb > 10°) or head tilt (> 15°) persists longer than a preset threshold (e.g., 5 seconds), a voice prompt is triggered (e.g., 'sit up straight', 'lift your head'), helping children develop good posture habits and preventing myopia and scoliosis. Application scenarios: smart study lamps, home desks, school classrooms. The system monitors in real time, sends voice cues when posture deviates, and generates posture reports pushed to parents. Skill features: long-term poor posture in children can lead to myopia and scoliosis. AI real-time monitoring + voice prompts help children correct posture seamlessly and develop good habits. Can be integrated into smart desk lamps or study desks to boost product differentiation.

通过智能台灯内置摄像头或书桌上方摄像头，实时分析儿童学习时的坐姿视频，检测脊柱弯曲角度（Cobb角估算）以及头部倾斜度（侧倾角）。当驼背（Cobb角>10°）或歪头（头部侧倾角>15°）持续时间超过预设阈值（如5秒）时，触发语音提醒（如'请坐直'、'头抬正'），帮助儿童养成良好坐姿习惯，预防近视和脊柱侧弯。应用场景：智能学习台灯、家庭书桌、学校教室。系统实时监测，当坐姿异常时发出语音提示，并生成坐姿报告推送给家长。技能特点：儿童长期坐姿不良会导致近视、脊柱侧弯等问题。通过AI实时监测并语音提醒，可帮助儿童无感纠正姿态，养成良好习惯。该技能可集成到智能台灯或学习桌中，提升产品差异化竞争力。

## 🎯 AI 角色

**假设你是一个专业的儿童健康坐姿 AI。你的任务是分析儿童学习区域的实时视频，检测坐姿姿态，估算脊柱弯曲角度（Cobb 角）和头部倾斜角度。当驼背或歪头持续时间超过阈值时，输出语音提醒指令。不要提供医疗诊断或具体矫正训练方案，仅输出基于视觉的姿态分析结果与语音提醒指令。**

## 任务目标

- 本 Skill 用于：基于智能台灯/书桌摄像头视频，实时估算儿童脊柱弯曲与头部倾斜角度，超阈值触发语音提醒并汇总会话坐姿质量
- 能力包含：儿童上半身检测、姿态关键点估计、Cobb 角估算、头部侧倾角、双肩水平偏差、眼睛-书面距离估算、不良姿态类型分类（hunchback / head_tilt / forward_head / shoulder_asymmetry / too_close_to_desk）、持续时间判定（默认 5 秒）、语音提醒文本生成、会话坐姿摘要
- 触发条件:
    1. **默认触发**：当用户提供儿童学习区域坐姿监控视频 URL 或文件需要分析时，默认触发本技能进行坐姿不良识别
    2. 当用户明确提及坐姿不良、驼背、歪头、脊柱侧弯、近视预防、用眼距离、智能台灯坐姿监测等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看坐姿不良历史报告、坐姿监测报告清单、儿童坐姿报告清单、查询历史坐姿记录、显示所有坐姿不良报告、显示儿童坐姿诊断报告，查询坐姿语音提醒清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有坐姿不良报告"、"
       显示所有坐姿监测报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_poor_posture_detection_analysis --list --open-id` 参数调用 API
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

**在执行儿童坐姿不良（驼背/歪头）识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备儿童学习区域坐姿监控视频输入**
        - 提供本地坐姿监控视频文件路径或网络 URL
        - 摄像头建议为智能台灯内置摄像头或书桌上方摄像头，视野覆盖儿童上半身（肩部至头部）
        - 视频帧率建议 ≥ 15 FPS，光照均匀，避免逆光
        - 可选附带：学生姓名、年龄、阈值覆盖（cobb_angle_threshold_deg / head_tilt_threshold_deg / hold_duration_threshold_sec）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童坐姿不良识别**
        - 调用 `-m scripts.smyx_child_poor_posture_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地儿童学习区域坐姿监控视频文件路径
            - `--url`: 网络儿童学习区域坐姿监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童健康坐姿场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童坐姿不良历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的坐姿不良识别报告
        - 包含：是否检测到儿童（child_detected）、姿态参数（posture_metrics：cobb_angle_deg / head_tilt_deg / shoulder_horizontal_offset_deg / eye_to_desk_distance_cm）、当前不良姿态类型（poor_posture_type：hunchback / head_tilt / forward_head / shoulder_asymmetry / too_close_to_desk）、持续秒数（hold_duration_sec）、语音提醒指令（voice_prompt：如"请坐直"、"头抬正"、"眼睛离书本远一点"）、事件时间戳（event_time）、现场快照 URL（snapshot_url）、当次会话坐姿摘要（summary）
        - **重要提示**：仅输出基于视觉的姿态分析结果与语音提醒指令，不提供医疗诊断或具体矫正训练方案

## 资源索引

- 必要脚本：见 [scripts/smyx_child_poor_posture_detection_analysis.py](scripts/smyx_child_poor_posture_detection_analysis.py)(
  用途：调用 API 进行儿童坐姿不良（驼背/歪头）实时提醒分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、姿态指标定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议正对面部+上半身、≥ 15 FPS
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- Cobb 角为视觉估算，与影像学测量存在偏差，仅供习惯纠正参考，不能替代脊柱侧弯医学评估
- 隐私合规：儿童学习场景视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"不良姿态"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童坐姿不良识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 不良姿态 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童坐姿不良识别报告-20260312172200001 | 驼背（Cobb 14°）+ 头部前伸 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地儿童坐姿视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_poor_posture_detection_analysis --input /path/to/posture.mp4 --open-id your-open-id

# 分析网络儿童坐姿视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_poor_posture_detection_analysis --url https://example.com/posture.mp4 --open-id your-open-id

# 显示历史坐姿不良识别报告（自动触发关键词：查看坐姿不良历史报告、坐姿监测报告清单等）
python -m scripts.smyx_child_poor_posture_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_poor_posture_detection_analysis --input posture.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_poor_posture_detection_analysis --input posture.mp4 --open-id your-open-id --output result.json
```
