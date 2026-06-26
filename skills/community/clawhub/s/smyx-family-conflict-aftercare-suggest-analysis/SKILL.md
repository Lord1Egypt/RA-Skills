---
name: "smyx-family-conflict-aftercare-suggest-analysis"
description: "Through fixed cameras (with microphones) in the family living room or kitchen, the system monitors conflict events among family members in real time, identifying high-decibel arguments (sound intensity exceeding a threshold and lasting more than 10 seconds), door slams (object impact sound + door-frame vibration), and aggressive arm-swing actions. After a conflict ends (both audio and video remain calm beyond a preset window, default 10 minutes) and no new conflict occurs, the system automatically outputs an aftercare prompt: playing soft music via a smart speaker or pushing caring messages through a mobile APP (such as 'Need a cup of tea?', 'Take a deep breath, speak slowly'). This skill aims to help family members soothe their emotions after intense arguments and restore communication. Application scenarios: family living rooms, kitchens, dining rooms and other conflict-prone areas. The system provides non-intrusive emotional comfort after conflicts. Skill features: family emotions easily continue to deteriorate after a conflict; appropriate external cues (music, caring words) can break the negative loop and encourage calm communication. AI-based automatic conflict detection with timely soothing helps maintain family harmony, especially for families with teenagers or members prone to emotional escalation. Can be integrated into smart speakers or home-security systems as a distinctive family-care feature. | 通过家庭客厅或厨房的固定摄像头（含麦克风），实时监测家庭成员间的冲突事件，识别高分贝争吵（声音强度超过阈值且持续时间>10秒）、摔门（物体撞击声+门框振动）、甩手等激烈肢体动作。当冲突事件结束后（音频和视频均平静超过预设时间，默认10分钟）且无新冲突，系统自动输出缓和提示：通过智能音箱播放轻柔音乐，或通过手机APP推送关怀语（如'需要一杯茶吗？'、'深呼吸，慢慢说'）。该技能旨在帮助家庭成员在激烈争执后平复情绪，促进沟通恢复。应用场景：家庭客厅、厨房、餐厅等易发生冲突的区域。系统在冲突后提供非介入式情绪安抚。技能特点：家庭冲突后情绪易持续恶化，适当的外界提示（如音乐、关怀语）可打断负面情绪循环，促进冷静沟通。通过AI自动识别冲突并适时提供安抚，有助于维护家庭和谐，尤其适合有青少年或情绪易失控成员的家庭。该技能可集成到智能音箱或家庭安防系统中，成为家庭关怀的特色功能。"
version: "1.0.0"
---

# Family Conflict Aftercare Suggestion | 夫妻/家人冲突后情绪缓和提示

Through fixed cameras (with microphones) in the family living room or kitchen, the system monitors conflict events among family members in real time, identifying high-decibel arguments (sound intensity exceeding a threshold and lasting more than 10 seconds), door slams (object impact sound + door-frame vibration), and aggressive arm-swing actions. After a conflict ends (both audio and video remain calm beyond a preset window, default 10 minutes) and no new conflict occurs, the system automatically outputs an aftercare prompt: playing soft music via a smart speaker or pushing caring messages through a mobile APP (such as 'Need a cup of tea?', 'Take a deep breath, speak slowly'). This skill aims to help family members soothe their emotions after intense arguments and restore communication. Application scenarios: family living rooms, kitchens, dining rooms and other conflict-prone areas. The system provides non-intrusive emotional comfort after conflicts. Skill features: family emotions easily continue to deteriorate after a conflict; appropriate external cues (music, caring words) can break the negative loop and encourage calm communication. AI-based automatic conflict detection with timely soothing helps maintain family harmony, especially for families with teenagers or members prone to emotional escalation. Can be integrated into smart speakers or home-security systems as a distinctive family-care feature.

通过家庭客厅或厨房的固定摄像头（含麦克风），实时监测家庭成员间的冲突事件，识别高分贝争吵（声音强度超过阈值且持续时间>10秒）、摔门（物体撞击声+门框振动）、甩手等激烈肢体动作。当冲突事件结束后（音频和视频均平静超过预设时间，默认10分钟）且无新冲突，系统自动输出缓和提示：通过智能音箱播放轻柔音乐，或通过手机APP推送关怀语（如'需要一杯茶吗？'、'深呼吸，慢慢说'）。该技能旨在帮助家庭成员在激烈争执后平复情绪，促进沟通恢复。应用场景：家庭客厅、厨房、餐厅等易发生冲突的区域。系统在冲突后提供非介入式情绪安抚。技能特点：家庭冲突后情绪易持续恶化，适当的外界提示（如音乐、关怀语）可打断负面情绪循环，促进冷静沟通。通过AI自动识别冲突并适时提供安抚，有助于维护家庭和谐，尤其适合有青少年或情绪易失控成员的家庭。该技能可集成到智能音箱或家庭安防系统中，成为家庭关怀的特色功能。

## 🎯 AI 角色

**假设你是一个专业的家庭情绪缓和 AI。你的任务是分析家庭公共活动区域（客厅 / 厨房 / 餐厅）固定摄像头的音视频，检测冲突事件：高分贝争吵（≥ 75 dB 且持续 ≥ 10 秒，与正常大笑/儿童欢闹区分）、摔门（撞击声 + 短暂低频共振）、物体砸落、大幅甩手、来回踱步、转身背对。当冲突结束后**连续 10 分钟（默认值，可配置）静默且无新冲突**，触发缓和动作：智能音箱播放轻柔音乐 / 温柔语音提示 / 家庭群 APP 关怀语推送。不提供心理咨询，仅输出基于音视频的事件检测和缓和动作建议；冲突中**不介入**避免激化；遇到疑似肢体暴力、未成年人在场、危险物等红线信号**立即转走"安全风险"路径**，推送 12338 反家暴热线 + 110 报警 + 400-161-9995 全国心理援助。**

## 任务目标

- 本 Skill 用于：基于家庭客厅/厨房/餐厅固定摄像头（**必须含麦克风**）音视频，识别冲突事件（核心音频 7 项：分贝峰值 / 持续 ≥ 75 dB 时长 / 喊叫声纹 / 摔门 / 物体砸落 / 哭泣声 / 静音时长；辅助视频 5 项：大幅甩手 / 来回踱步 / 有人离开画面 / 两人最近距离 / 转身背对时长）→ 5 档冲突等级（none / mild_dispute / conflict / intense_conflict / **critical_redline**）→ **平静窗口判定**（默认 10 min 静默 + 无新冲突 + 物理距离回归 + 至少一人回到画面）→ 触发 3 类缓和动作（智能音箱轻柔音乐 / 温柔语音 / 家庭群 APP 关怀语，**单日上限 2 次**避免过度介入）→ 红线触发立即转**安全资源路径**（12338 / 110 / 400-161-9995 / 妇联权益部 / 当地社工司法所）
- 能力包含：分贝峰值与持续时长检测、喊叫/嘶吼声纹与正常大笑/儿童欢闹声区分、摔门撞击声 + 低频共振识别、物体砸落识别、哭泣声检测、大幅甩手挥手势识别、来回踱步检测、人物离开画面检测、两人最近物理距离测算、转身背对持续时长统计、平静窗口判定（多条件 AND）、**疑似肢体暴力红线识别**（推搡/挥拳/抓握）、**冲突现场未成年人在场识别**、**危险物（刀具/重物）可见识别**、疑似受伤征兆识别（摔倒/抚摸面部/蜷缩）、缓和动作 3 秒前导铃声、缓和文案中立性校验（**不指责任何一方**）、家庭主用户一键关闭今日 / 整日关闭（聚会场景）/ 永久退出
- 触发条件:
    1. **默认触发**：当用户提供家庭客厅/厨房/餐厅固定摄像头音视频 URL 或文件需要分析时，默认触发本技能进行夫妻/家人冲突后情绪缓和提示
    2. 当用户明确提及夫妻吵架、家人冲突、摔门、家里争执后、家庭情绪缓和、智能音箱关怀等关键词，并且上传了音视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看家庭冲突缓和历史报告、家庭情绪事件清单、缓和提示记录、查询历史冲突缓和记录、显示所有家庭冲突缓和报告、显示家庭情绪关怀日志，查询家庭冲突清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有家庭冲突缓和报告"、"
       显示所有家庭情绪事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --list --open-id` 参数调用 API
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

**在执行夫妻/家人冲突后情绪缓和提示前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备家庭客厅/厨房/餐厅固定摄像头（含麦克风）音视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**，离线分析建议 ≥ 30 分钟（覆盖完整冲突 → 平静窗口）
        - 摄像头建议：仅部署在公共活动区域；**严禁卧室/卫生间/儿童独立房间**
        - 帧率 ≥ 5 FPS（推荐 10 FPS）、分辨率 ≥ 480p
        - 音频**必需**：采样率 ≥ 16kHz（用于分贝/声纹/摔门撞击检测）
        - 仅缓存 ≤ 24 小时事件片段，**不**长期保存家庭原始对话
        - 家庭主用户必须授权部署，并提供：一键关闭今日 / 整日关闭（聚会场景）/ 永久退出 入口
        - 可选附带：阈值覆盖（db_threshold / calm_window_sec）、家庭成员清单（识别未成年人在场）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（家庭主用户授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行夫妻/家人冲突后情绪缓和提示**
        - 调用 `-m scripts.smyx_family_conflict_aftercare_suggest_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地家庭客厅/厨房/餐厅固定摄像头（含麦克风）音视频文件路径
            - `--url`: 网络家庭客厅/厨房/餐厅固定摄像头（含麦克风）音视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，家庭情绪缓和场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，家庭主用户授权）
            - `--list`: 显示夫妻/家人冲突后情绪缓和提示历史事件清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的夫妻/家人冲突后情绪缓和提示报告
        - 包含：事件 ID（event_id）、冲突起止时间（conflict_start_time / conflict_end_time / conflict_duration_min）、音频信号（audio_signals：db_level_peak / db_level_sustained_duration_sec / shouting_voice_detected / door_slam_event_count / object_impact_event_count / crying_audio_detected / silence_duration_sec）、视频信号（video_signals：arm_swing_aggressive_count / pacing_back_and_forth / person_walked_out_event / physical_distance_minimum_m / body_facing_away_duration_sec）、冲突等级（conflict_level：none / mild_dispute / conflict / intense_conflict / **critical_redline**）、红线信号清单（redline_flags：physical_violence_suspected / child_present_during_conflict / weapon_or_dangerous_object_visible / injury_visual_signs）、平静窗口状态（calm_window_status：observing / met / reset_by_new_conflict）、平静持续时长（calm_window_duration_sec）、缓和动作列表（aftercare_actions：smart_speaker_soft_music / smart_speaker_gentle_voice / family_app_push，每项含 action_type / message / target）、建议动作（recommend_action：trigger_soft_music / push_gentle_message / observe_only / **escalate_safety_path**）、安全资源（safety_resource：12338 反家暴热线 / 妇联权益部 / 110 / 400-161-9995 / 当地社工司法所）
        - **重要提示**：仅输出基于音视频的**客观冲突事件检测和缓和动作建议**，**不构成婚姻/亲子关系咨询或心理治疗**；任何疑似家庭暴力请立即拨打 **12338 反家暴热线**或 **110**

## 资源索引

- 必要脚本：见 [scripts/smyx_family_conflict_aftercare_suggest_analysis.py](scripts/smyx_family_conflict_aftercare_suggest_analysis.py)(
  用途：调用 API 进行夫妻/家人冲突后情绪缓和提示，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、音频/视频信号、5 档冲突等级、平静窗口判定、缓和动作和红线约束/安全资源时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；**关键**：必须含麦克风
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **冲突中绝不介入**：`intense_conflict` 期间播放音乐或语音会激化情绪；**必须等待平静窗口**
- 与正常高分贝场景区分：聚会、大笑、儿童欢闹、看球赛——支持家庭主用户**整日关闭**
- 红线约束：
    - **禁止**部署在卧室、卫生间、儿童独立房间
    - **禁止**录制并长期存储家庭对话原始音频（仅保留指标 + ≤ 24h 事件片段）
    - **禁止**做"婚姻/亲子关系评分"或"性格分析"
    - **禁止**对疑似肢体暴力进行"缓和处理"——必须独立走**安全风险**路径
    - **禁止**将冲突事件转发给除家庭主用户外的第三方
- **必须**：缓和动作前 3 秒柔和铃声前导避免突然出声二次惊吓；缓和文案**中立、不指责任何一方**；同一事件单日触发**上限 2 次**
- **必须**在 `critical_redline` 触发时**立即**推送 **12338** 反家暴热线 + **110** 报警提示；有未成年人在场优先级最高
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史事件清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"冲突等级/持续时长/已执行缓和动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`家庭冲突缓和事件-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 冲突等级/持续时长/已执行缓和动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 家庭冲突缓和事件-20260312172200001 | conflict / 8min / 轻音乐+APP 关怀语 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地家庭公共区域音视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --input /path/to/livingroom.mp4 --open-id your-open-id

# 分析网络家庭公共区域音视频/实时流（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --url https://example.com/livingroom.mp4 --open-id your-open-id

# 显示历史家庭冲突缓和事件清单（自动触发关键词：查看家庭冲突缓和历史报告、家庭情绪事件清单等）
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --input lr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --input lr.mp4 --open-id your-open-id --output result.json
```
