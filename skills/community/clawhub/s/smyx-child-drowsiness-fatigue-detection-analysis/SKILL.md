---
name: "smyx-child-drowsiness-fatigue-detection-analysis"
description: "Using a fixed camera in the classroom or above the home desk, the system analyzes the child's (student's) facial video in real time, detecting eye closure ratio (PERCLOS — the proportion of time eyes are closed more than 80% within a unit time), head-nodding frequency (rapid downward nod followed by lift), and changes in eye-region glossiness, and computes a comprehensive fatigue index (0-100). The skill helps teachers or parents detect drowsiness in time and adjust learning schedules or remind the child to rest. Application scenarios: classrooms, home desks, online classes. The system monitors in real time and, when the fatigue index exceeds a threshold, pushes reminders or triggers voice prompts (e.g., 'kid, time to take a break'). Skill features: safeguarding sleep health. | 通过教室或家庭书桌的固定摄像头，实时分析儿童（学生）的面部视频，检测眼部闭合比例（PERCLOS，单位时间内眼睛闭合超过80%的时间占比）、点头动作频率（头部快速下点后抬起）以及眼部区域的光泽度变化，综合计算疲劳指数（0-100）。该技能可帮助教师或家长及时发现儿童困倦状态，调整学习安排或提醒休息。应用场景：教室、家庭书桌、在线课堂。系统实时监测，当疲劳指数超过阈值时，推送提醒或触发语音提示（如'小朋友，休息一下吧'）。技能特点：保障睡眠健康。"
version: "1.0.0"
---

# Child Drowsiness / Fatigue Detection | 儿童打瞌睡/疲劳检测

Using a fixed camera in the classroom or above the home desk, the system analyzes the child's (student's) facial video in real time, detecting eye closure ratio (PERCLOS — the proportion of time eyes are closed more than 80% within a unit time), head-nodding frequency (rapid downward nod followed by lift), and changes in eye-region glossiness, and computes a comprehensive fatigue index (0-100). The skill helps teachers or parents detect drowsiness in time and adjust learning schedules or remind the child to rest. Application scenarios: classrooms, home desks, online classes. The system monitors in real time and, when the fatigue index exceeds a threshold, pushes reminders or triggers voice prompts (e.g., 'kid, time to take a break'). Skill features: safeguarding sleep health.

通过教室或家庭书桌的固定摄像头，实时分析儿童（学生）的面部视频，检测眼部闭合比例（PERCLOS，单位时间内眼睛闭合超过80%的时间占比）、点头动作频率（头部快速下点后抬起）以及眼部区域的光泽度变化，综合计算疲劳指数（0-100）。该技能可帮助教师或家长及时发现儿童困倦状态，调整学习安排或提醒休息。应用场景：教室、家庭书桌、在线课堂。系统实时监测，当疲劳指数超过阈值时，推送提醒或触发语音提示（如'小朋友，休息一下吧'）。技能特点：保障睡眠健康。

## 🎯 AI 角色

**假设你是一个专业的儿童学习疲劳监测 AI。你的任务是分析儿童面部视频，检测眼部闭合状态和头部点头动作，计算疲劳指数。不要提供医疗诊断或睡眠障碍诊断，仅输出基于视觉的疲劳评估结果与方向性休息提醒。**

## 任务目标

- 本 Skill 用于：基于教室/家庭书桌摄像头视频，量化儿童眼部闭合（PERCLOS）+ 点头动作 + 眼部光泽度变化，输出 0-100 疲劳指数与等级判定
- 能力包含：儿童面部检测、眼部状态识别（闭合 / 半闭 / 睁开）、PERCLOS 计算、连续闭眼时长、眨眼频次、点头次数与角度、眼部光泽度变化、疲劳综合得分（0-100）、疲劳等级（alert / mild_fatigue / moderate_fatigue / drowsy）、打瞌睡事件列表、语音提醒文本生成
- 触发条件:
    1. **默认触发**：当用户提供儿童面部学习区域视频 URL 或文件需要分析时，默认触发本技能进行打瞌睡/疲劳检测
    2. 当用户明确提及打瞌睡、疲劳、困倦、PERCLOS、点头、眨眼、上课走神、写作业犯困、智能台灯疲劳提醒等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看儿童疲劳历史报告、打瞌睡报告清单、疲劳指数报告清单、查询历史疲劳记录、显示所有儿童疲劳检测报告、显示儿童睡眠健康诊断报告，查询疲劳提醒清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有儿童疲劳报告"、"
       显示所有打瞌睡报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_drowsiness_fatigue_detection_analysis --list --open-id` 参数调用 API
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

**在执行儿童打瞌睡/疲劳检测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备儿童面部学习区域视频输入**
        - 提供本地儿童面部学习区域视频路径或网络 URL
        - 摄像头建议正对儿童面部（教室/书桌正前方或智能台灯内置）
        - 帧率建议 ≥ 15 FPS；光照均匀避免逆光、镜片反光
        - 可选附带：学生姓名、年龄、当次学习场景（课堂 / 写作业 / 在线课）、阈值覆盖（fatigue_score_threshold）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童打瞌睡/疲劳检测**
        - 调用 `-m scripts.smyx_child_drowsiness_fatigue_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地儿童面部学习区域视频文件路径
            - `--url`: 网络儿童面部学习区域视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童学习疲劳监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童打瞌睡/疲劳历史检测报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童打瞌睡/疲劳检测报告
        - 包含：是否检测到儿童（child_detected）、各项疲劳指标数值（fatigue_metrics：perclos / eye_closure_duration_sec / blink_rate_per_min / nod_frequency_per_min / head_drop_angle_deg）、综合疲劳指数（fatigue_score，0-100）、疲劳等级（fatigue_level：alert / mild_fatigue / moderate_fatigue / drowsy）、打瞌睡事件列表（drowsiness_events）、语音提醒文本（voice_prompt：如"小朋友，休息一下吧"）、当次会话疲劳统计摘要（summary）
        - **重要提示**：仅输出基于视觉的疲劳评估结果与方向性休息提醒，不提供医学诊断或睡眠障碍诊断

## 资源索引

- 必要脚本：见 [scripts/smyx_child_drowsiness_fatigue_detection_analysis.py](scripts/smyx_child_drowsiness_fatigue_detection_analysis.py)(
  用途：调用 API 进行儿童打瞌睡/疲劳检测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、疲劳指标定义/分级和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议正对面部、≥ 15 FPS
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 检测结果仅作为学习/课堂辅助参考，本工具不替代家长/教师的实际观察与教育判断，疑似长期严重困倦请就医
- 隐私合规：儿童学习场景视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"疲劳指数"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童疲劳检测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 疲劳指数 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童疲劳检测报告-20260312172200001 | 78 / drowsy | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地儿童学习面部视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_drowsiness_fatigue_detection_analysis --input /path/to/class.mp4 --open-id your-open-id

# 分析网络儿童学习面部视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_drowsiness_fatigue_detection_analysis --url https://example.com/class.mp4 --open-id your-open-id

# 显示历史儿童疲劳检测报告（自动触发关键词：查看儿童疲劳历史报告、打瞌睡报告清单等）
python -m scripts.smyx_child_drowsiness_fatigue_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_drowsiness_fatigue_detection_analysis --input class.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_drowsiness_fatigue_detection_analysis --input class.mp4 --open-id your-open-id --output result.json
```
