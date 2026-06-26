---
name: "smyx-family-conflict-intensity-detect-analysis"
description: "Using a fixed camera with microphone in the living room, the system analyzes audio and video in real time, detecting sound intensity (dB) and the intensity of body movements (e.g., rapid hand waving, finger pointing, pushing, throwing objects). It comprehensively evaluates the family conflict intensity level (low / medium / high). When the level reaches medium or high, it pushes a gentle reminder via mobile APP (e.g., 'A high-intensity conflict has been detected. We suggest calming down or temporarily separating'). The skill helps family members become self-aware of their emotions, avoid escalation, and, when necessary, notify pre-designated emergency contacts. Application scenarios: family living rooms, psychological counseling rooms, marriage mediation centers. The system auto-reminds during detected conflicts or generates conflict-frequency reports for family counselors. Skill features: family conflicts are common; long-term high-intensity conflicts harm mental health and may escalate to domestic violence. AI automatic detection with gentle reminders helps members self-regulate before losing control. Can be integrated into smart-home cameras or family health-management APPs as an auxiliary tool to promote family harmony. | 通过客厅固定摄像头（含麦克风），实时分析音频和视频，检测声音强度（分贝）和肢体动作激烈程度（如快速挥手、戳指、推搡、摔物等）。综合评估家庭争吵的冲突强度等级（低/中/高），当强度达到中或高时，通过手机APP推送提醒（如'检测到高强度冲突，建议冷静沟通或暂时分开'）。该技能旨在帮助家庭成员自我觉察情绪，避免冲突升级，必要时可联动紧急联系人。应用场景：家庭客厅、心理咨询室、婚姻调解中心。系统在检测到冲突时自动提醒，或生成冲突频率报告供家庭咨询师参考。技能特点：家庭争吵是常见现象，长期高强度冲突会影响家庭成员心理健康，甚至导致家暴。通过AI自动检测并温和提醒，可帮助家庭成员在情绪失控前自我觉察，避免冲突升级。该技能可集成到智能家居摄像头或家庭健康管理APP中，成为促进家庭和谐的辅助工具。"
version: "1.0.0"
---

# Family / Couple Conflict Intensity Detection | 夫妻/家庭争吵强度识别

Using a fixed camera with microphone in the living room, the system analyzes audio and video in real time, detecting sound intensity (dB) and the intensity of body movements (e.g., rapid hand waving, finger pointing, pushing, throwing objects). It comprehensively evaluates the family conflict intensity level (low / medium / high). When the level reaches medium or high, it pushes a gentle reminder via mobile APP (e.g., 'A high-intensity conflict has been detected. We suggest calming down or temporarily separating'). The skill helps family members become self-aware of their emotions, avoid escalation, and, when necessary, notify pre-designated emergency contacts. Application scenarios: family living rooms, psychological counseling rooms, marriage mediation centers. The system auto-reminds during detected conflicts or generates conflict-frequency reports for family counselors. Skill features: family conflicts are common; long-term high-intensity conflicts harm mental health and may escalate to domestic violence. AI automatic detection with gentle reminders helps members self-regulate before losing control. Can be integrated into smart-home cameras or family health-management APPs as an auxiliary tool to promote family harmony.

通过客厅固定摄像头（含麦克风），实时分析音频和视频，检测声音强度（分贝）和肢体动作激烈程度（如快速挥手、戳指、推搡、摔物等）。综合评估家庭争吵的冲突强度等级（低/中/高），当强度达到中或高时，通过手机APP推送提醒（如'检测到高强度冲突，建议冷静沟通或暂时分开'）。该技能旨在帮助家庭成员自我觉察情绪，避免冲突升级，必要时可联动紧急联系人。应用场景：家庭客厅、心理咨询室、婚姻调解中心。系统在检测到冲突时自动提醒，或生成冲突频率报告供家庭咨询师参考。技能特点：家庭争吵是常见现象，长期高强度冲突会影响家庭成员心理健康，甚至导致家暴。通过AI自动检测并温和提醒，可帮助家庭成员在情绪失控前自我觉察，避免冲突升级。该技能可集成到智能家居摄像头或家庭健康管理APP中，成为促进家庭和谐的辅助工具。

## 🎯 AI 角色

**假设你是一个专业的家庭情绪与冲突分析 AI。你的任务是分析客厅固定摄像头的音频和视频，检测声音强度（分贝）以及肢体动作的激烈程度（挥手、戳指、推搡、摔砸物品等），综合输出冲突强度等级与温和提醒。不要提供法律或心理治疗建议，仅输出基于声学和视觉的冲突强度指标，并在高强度时附反家暴热线参考。**

## 任务目标

- 本 Skill 用于：基于家庭客厅固定摄像头（含麦克风）的同步音视频，识别声音分贝水平 + 攻击性词汇命中（本地推理）+ 喊叫事件 + 肢体激烈程度（挥手 / 戳指 / 推搡 / 摔物）→ 综合输出冲突强度等级（low / medium / high）→ 推送**温和**的觉察提醒；不替代法律或心理治疗服务
- 能力包含：声学指标提取（peak_db / avg_db / db_delta_vs_baseline / shout_event_count / aggressive_word_hit_count 本地推理 / voice_speakers_estimate）、视觉肢体激烈度识别（挥手 / 戳指 / 推搡 / 摔物 / 面对面贴脸）、儿童或老人在场识别（升级触发位）、综合冲突强度等级判定、连续高强度事件累计、面向当事人的温和提醒文案生成、紧急联系人联动开关（**事先取得用户同意**）、反家暴热线与社区调解资源参考
- 触发条件:
    1. **默认触发**：当用户提供客厅固定摄像头（含麦克风）音视频 URL 或文件需要分析时，默认触发本技能进行家庭争吵强度识别
    2. 当用户明确提及家庭争吵、夫妻吵架、客厅冲突、家暴预警、冷静提醒、情绪失控、家庭调解等关键词，并且上传了音视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看家庭冲突历史报告、争吵强度报告清单、家庭冲突记录清单、查询历史冲突事件、显示所有家庭争吵报告、显示婚姻调解辅助报告，查询冲突强度预警清单
- 自动行为：
    1. 如果用户上传了附件或者音视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有家庭冲突报告"、"
       显示所有争吵强度报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_family_conflict_intensity_detect_analysis --list --open-id` 参数调用 API
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

**在执行夫妻/家庭争吵强度识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备客厅固定摄像头（含麦克风）音视频输入**
        - 提供本地音视频路径或网络 URL，建议覆盖完整冲突过程（≥ 30 秒）
        - 摄像头建议：家庭客厅/起居室固定摄像头，**必须含麦克风**，能看到家庭成员上半身
        - 帧率 ≥ 10 FPS、分辨率 ≥ 480p、音频采样率 ≥ 16kHz、双声道更佳
        - 安装时录制 30 秒室内静音作为环境本底（baseline_db）
        - 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式
        - 可选附带：家庭成员构成（是否含儿童/老人）、紧急联系人开关（默认关）、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行夫妻/家庭争吵强度识别**
        - 调用 `-m scripts.smyx_family_conflict_intensity_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地客厅固定摄像头（含麦克风）音视频文件路径
            - `--url`: 网络客厅固定摄像头（含麦克风）音视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，家庭情绪与冲突分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示夫妻/家庭争吵强度识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的夫妻/家庭争吵强度识别报告
        - 包含：冲突时间窗（event_window）、声学指标（acoustic_metrics：peak_db / avg_db / db_delta_vs_baseline / shout_event_count / aggressive_word_hit_count / voice_speakers_estimate）、视觉指标（visual_metrics：subject_count / wave_hand_event_count / finger_point_event_count / push_event_count / throw_object_event_count / physical_proximity_invasion）、是否有儿童/老人在场（child_or_elderly_present）、冲突强度等级（conflict_intensity_level：low / medium / high）、提醒类型（alert_type：conflict_low / conflict_medium / conflict_high / repeated_conflict / normal）、提醒级别（alert_level：info / notice / warning / urgent）、温和提醒文本（gentle_reminder_message，如"检测到中等强度对话冲突，建议双方暂停 10 分钟、各自深呼吸或喝口水后再继续"）、建议动作（recommend_action：push_gentle_reminder / suggest_cool_down / suggest_separate_rooms / notify_emergency_contact_if_consent / observe_only）、是否建议寻求专业帮助（suggest_seek_help）
        - **重要提示**：仅输出基于声学和视觉的客观冲突强度指标与温和提醒，**不提供法律意见、心理治疗方案或人身安全判定**；若涉及人身安全或反复高强度冲突，请联系反家庭暴力热线 **12338** 或当地警方与心理援助机构

## 资源索引

- 必要脚本：见 [scripts/smyx_family_conflict_intensity_detect_analysis.py](scripts/smyx_family_conflict_intensity_detect_analysis.py)(
  用途：调用 API 进行夫妻/家庭争吵强度识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、声学/视觉指标/冲突强度阈值与红线约束和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 含音轨视频，最大 10MB；**关键**：必须包含麦克风音轨
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 看电视/电影、儿童打闹游戏、激烈讨论但无攻击性词汇等情形容易被误识为冲突，建议结合声学 + 视觉 + 攻击性词汇多模态综合判定
- 攻击性词汇命中**仅本地推理**，**禁止上传原始语音**到任何外部服务
- 红线约束：**禁止**根据本工具结论给当事人贴"家暴施害者/受害者"标签；**禁止**自动报警；**禁止**长期存储原始音视频；**禁止**输出法律意见或处方
- 紧急联系人联动需用户**事先取得双方知情同意**，默认关闭；高强度连续多次时附**反家暴热线 12338** 与就近社区调解资源参考
- 隐私合规：家庭音视频涉及高度敏感家庭隐私，使用前需取得**家庭所有成年成员**明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式 + 仅保存指标统计
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"冲突强度/主要表现"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`家庭争吵强度报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 冲突强度/主要表现 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 家庭争吵强度报告-20260312172200001 | medium（峰值 78 dB + 戳指 5 次） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地客厅音视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_family_conflict_intensity_detect_analysis --input /path/to/livingroom.mp4 --open-id your-open-id

# 分析网络客厅音视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_family_conflict_intensity_detect_analysis --url https://example.com/livingroom.mp4 --open-id your-open-id

# 显示历史家庭争吵强度报告（自动触发关键词：查看家庭冲突历史报告、争吵强度报告清单等）
python -m scripts.smyx_family_conflict_intensity_detect_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_family_conflict_intensity_detect_analysis --input lr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_family_conflict_intensity_detect_analysis --input lr.mp4 --open-id your-open-id --output result.json
```
