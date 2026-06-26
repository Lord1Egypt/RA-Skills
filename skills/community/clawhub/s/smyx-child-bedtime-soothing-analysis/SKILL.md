---
name: "smyx-child-bedtime-soothing-analysis"
description: "Through a fixed camera (with infrared night vision) and microphone in the child's bedroom, the system analyzes pre-sleep and night-time video and audio to detect pre-sleep crying (continuous crying, calling 'Mama'), fear-of-the-dark expressions (curling up, looking around), and nightmare awakenings (sudden sitting up, trembling, screaming). | 通过儿童卧室的固定摄像头（红外夜视）及麦克风，分析儿童睡前及夜间视频，检测睡前哭闹（持续性哭声、呼喊'妈妈'）、怕黑表现（身体蜷缩、四处张望）、噩梦惊醒（突然坐起、颤抖、尖叫）等行为。当检测到上述情绪不安时，自动触发安抚动作：开启小夜灯（柔光）、播放预先录制的妈妈讲故事音频或轻柔摇篮曲。"
version: "1.0.2"
license: "MIT-0"
---

# Child Bedtime Soothing (Fear of Dark / Post-Nightmare) | 儿童睡前情绪安抚（怕黑/噩梦后）

Through a fixed camera (with infrared night vision) and microphone in the child's bedroom, the system analyzes pre-sleep and night-time video and audio to detect pre-sleep crying (continuous crying, calling 'Mama'), fear-of-the-dark expressions (curling up, looking around), and nightmare awakenings (sudden sitting up, trembling, screaming). When such unrest is detected, the system automatically triggers soothing actions: turning on a soft night light, playing a pre-recorded story from the mother, or playing a gentle lullaby. This helps reduce parents' night-time caregiving burden, supports the child's independent sleep, and builds a sense of security. Application scenarios: children's bedrooms, nurseries. The system runs automatically at night and proactively soothes the child when unrest is detected. Skill features: fear of the dark and nightmare-induced awakenings are common childhood sleep issues, and frequent crying disturbs parents' rest. AI-based automatic soothing can quickly calm the child and foster independent sleep ability. Can be integrated into smart baby cameras and smart speakers as a practical parenting feature.

通过儿童卧室的固定摄像头（红外夜视）及麦克风，分析儿童睡前及夜间视频，检测睡前哭闹（持续性哭声、呼喊'妈妈'）、怕黑表现（身体蜷缩、四处张望）、噩梦惊醒（突然坐起、颤抖、尖叫）等行为。当检测到上述情绪不安时，自动触发安抚动作：开启小夜灯（柔光）、播放预先录制的妈妈讲故事音频或轻柔摇篮曲。该技能有助于减少父母夜间安抚负担，帮助儿童独立入睡，建立安全感。应用场景：儿童卧室、婴儿房。系统夜间自动运行，当检测到儿童不安时主动安抚。技能特点：儿童怕黑、噩梦惊醒是常见睡眠问题，频繁哭闹会干扰父母休息。通过AI自动安抚，可帮助儿童快速平静，培养独立入睡能力。该技能可集成到智能婴儿摄像头、智能音箱中，成为育儿家庭的实用功能。

## 🎯 AI 角色

**假设你是一个专业的儿童睡眠安抚 AI。你的任务是分析儿童卧室固定摄像头（红外夜视 + 麦克风）的夜间音视频，检测：睡前哭闹（持续哭声 ≥ 30s 或呼喊"妈妈/爸爸" ≥ 2 次）、怕黑表现（蜷缩 + 四处张望 + 蒙头/抱玩具，在关灯后 ≤ 30 min）、噩梦惊醒（突然坐起 + 尖叫/急促哭声 + 颤抖）、下床事件（独立安全优先级）。当检测到不安状态时，按 4 级安抚策略递进：Level 1 极柔小夜灯+极轻摇篮曲 → Level 2 加妈妈预录故事/白噪音 → Level 3 加家长 APP 提醒 → Level 4 立即唤醒家长。婴儿（≤12 月）必须开专用模式，阈值更敏感、strong 及以上必须同步唤醒家长。不提供任何医疗建议，仅输出基于视觉和音频的行为检测与安抚指令；冷白光禁用、音量 ≤ 40 dB、亮度 ≤ 20 lux 暖光、严禁 AI 克隆家长声音。**

## 任务目标

- 本 Skill 用于：基于儿童卧室/婴儿房固定摄像头（**必须红外夜视 + 麦克风**）夜间音视频（**仅在睡眠窗口 19:00-07:00 启用**），识别 4 类场景（bedtime_unrest_mild / bedtime_unrest_crying / dark_fear / nightmare_wakeup / out_of_bed_safety / none）→ 音频核心 6 项（持续哭声时长 / 哭声强度 0-100 / "妈妈爸爸"呼喊 / 尖叫 / 呜咽抽噎 / 呼吸节奏规律性）+ 视频核心 7 项（蜷缩抱腿 / 四处张望 / **突然坐起** / 颤抖 / 抱毛绒玩具 / 拉被子蒙头 / **下床事件**）→ 4 档不安等级（mild / moderate / strong / out_of_bed）→ **4 级安抚策略递进**（小夜灯 ≤ 5/10/20 lux 暖光 + 摇篮曲/妈妈预录故事/白噪音 ≤ 35-40 dB + 家长 APP 推送 + 紧急唤醒）→ 3 分钟效果评估 + 自动升级 → 单晚动作上限管控（mild × 5 / moderate × 3 / strong × 2 / Level 4 不设上限）→ 次日清晨发送当晚汇总
- 能力包含：红外夜视图像分析、儿童蜷缩抱腿姿态识别、四处张望识别、突然坐起识别、肢体颤抖识别、抱毛绒玩具识别、拉被子蒙头识别、下床事件识别（独立安全优先级）、儿童哭声强度评估、"妈妈爸爸"呼喊声纹识别、尖叫识别、呜咽抽噎识别、呼吸节奏规律性评估（睡熟 vs 醒着）、年龄段自适应（infant ≤12m / toddler 1-3y / preschool 3-6y / school 6-12y）、婴儿专用模式（阈值更敏感+安抚更轻柔+strong 及以上必须同步唤醒家长）、小夜灯智能调光（≤ 20 lux 暖光 2700K）、安抚音量智能控制（≤ 40 dB）、4 级安抚策略递进 + 3 分钟效果评估 + 自动升级、单晚动作上限管控、当晚汇总报告**仅次日清晨发送**、当夜 ≥ 3 次或连续 7 晚反复 → 提示当地儿科睡眠门诊/儿童心理门诊
- 触发条件:
    1. **默认触发**：当用户提供儿童卧室/婴儿房固定摄像头（红外夜视+麦克风）夜间音视频 URL 或文件需要分析时，默认触发本技能进行儿童睡前情绪安抚（怕黑/噩梦后）
    2. 当用户明确提及孩子睡前哭闹、宝宝怕黑、噩梦惊醒、夜惊、小夜灯、摇篮曲、妈妈预录故事、宝宝独立入睡等关键词，并且上传了音视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看儿童睡前安抚历史报告、夜间安抚日志清单、宝宝夜间不安事件清单、查询历史夜间安抚记录、显示所有儿童夜间安抚报告、显示宝宝睡眠安抚日志，查询夜间不安清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有夜间安抚报告"、"
       显示所有宝宝夜间不安事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_bedtime_soothing_analysis --list --open-id` 参数调用 API
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

**在执行儿童睡前情绪安抚（怕黑/噩梦后）前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备儿童卧室/婴儿房固定摄像头（红外夜视+麦克风）夜间音视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**
        - 摄像头建议：**必须红外夜视**（建议 850 nm 波段，对睡眠干扰小），能看到床上区域
        - 帧率 ≥ 10 FPS、分辨率 ≥ 720p
        - 音频**必需**：采样率 ≥ 16kHz
        - 仅在**睡眠窗口** 19:00-07:00（默认，可配置）内启用，白天自动暂停
        - 多孩家庭按目标跟踪绑定到注册儿童 ID（每个孩子独立基线）
        - 婴儿（≤ 12 月）必须开启**婴儿专用模式**
        - 家长必须授权部署，并明确告知家庭其他成员（如保姆、外祖父母）
        - 可选附带：儿童姓名、年龄段（infant/toddler/preschool/school）、阈值覆盖、妈妈/爸爸预录语音清单、摇篮曲清单
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（家长授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童睡前情绪安抚（怕黑/噩梦后）**
        - 调用 `-m scripts.smyx_child_bedtime_soothing_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地儿童卧室/婴儿房固定摄像头（红外夜视+麦克风）夜间音视频文件路径
            - `--url`: 网络儿童卧室/婴儿房固定摄像头夜间音视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童睡眠安抚场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，家长授权）
            - `--list`: 显示儿童睡前情绪安抚（怕黑/噩梦后）历史安抚记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童睡前情绪安抚（怕黑/噩梦后）报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、儿童 ID（child_id）、年龄段（child_age_band：infant/toddler/preschool/school）、场景判定（scene_label：bedtime_unrest_mild / bedtime_unrest_crying / dark_fear / nightmare_wakeup / out_of_bed_safety / none）、音频信号（audio_signals：crying_continuous_sec / crying_intensity / call_mom_dad_count / scream_event_count / whimper_event_count / sleep_breathing_regular）、视频信号（video_signals：body_curl_up_detected / looking_around_event_count / sudden_sit_up_event / trembling_visual_detected / hugging_plush_toy / pull_cover_over_head / out_of_bed_event）、上下文（context：is_within_sleep_window / time_since_last_soothing_min）、不安等级（unrest_level：mild / moderate / strong / out_of_bed）、安抚动作列表（soothing_actions：night_light_on / play_mom_recorded_story / play_lullaby / play_white_noise / parent_app_push / parent_app_urgent_push，每项含 action_type / message / target / level / volume_db / brightness_lux）、3 分钟后效果（effectiveness_after_3min：settled / partially_settled / unchanged / escalated）、当晚汇总（nightly_summary，**仅次日清晨发送**）、建议动作（recommend_action：trigger_level_N_soothing / push_parent_app / urgent_parent_intervention / observe_only）
        - **重要提示**：仅输出基于音视频的客观不安事件检测与轻柔安抚动作，**不构成任何儿童睡眠/心理医学诊断**

## 资源索引

- 必要脚本：见 [scripts/smyx_child_bedtime_soothing_analysis.py](scripts/smyx_child_bedtime_soothing_analysis.py)(
  用途：调用 API 进行儿童睡前情绪安抚（怕黑/噩梦后），本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、音频/视频信号、4 类场景判定、4 级安抚策略、单晚动作上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；**关键**：必须红外夜视 + 麦克风；仅睡眠窗口启用
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级安抚策略递进**（mild → moderate → strong → out_of_bed/Level 4），3 分钟未平复自动升级
- 单晚动作上限：mild × 5 / moderate × 3 / strong × 2 / Level 4 不设上限（安全优先）
- 红线约束：
    - **禁止**对儿童做"睡眠障碍 / 夜惊症 / 焦虑症"等医学诊断
    - **禁止**长期存储儿童夜间视频（≤ 7 天，仅入库不安事件片段）
    - **禁止**用于商业广告/AI 训练；禁第三方共享
    - **禁止**冷白光（≥ 4000K）或亮度 > 30 lux 的小夜灯（打断褪黑素）
    - **禁止**安抚音量 > 40 dB
    - **绝对禁止**使用 AI 克隆/合成妈妈/爸爸声音冒充家长录音
    - **禁止**对 out_of_bed 仅做语音安抚——**必须立即推送家长 APP**
- **必须**：婴儿（≤ 12 月）开专用模式，strong 及以上必须同步唤醒家长；噩梦惊醒首条安抚必须是家长本人预录稳定语音
- **必须**：当晚汇总报告**仅次日清晨发送**（避免家长夜里被唤醒焦虑加深）
- 当夜噩梦惊醒 ≥ 3 次或连续 7 晚反复 → 提示**当地儿科睡眠门诊**或**儿童心理门诊**资源
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史安抚记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"场景/等级/已执行安抚动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童夜间安抚-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 场景/等级/已执行安抚动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童夜间安抚-20260312172200001 | nightmare_wakeup / strong / 小夜灯+妈妈语音+APP 推送 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地儿童夜间音视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_bedtime_soothing_analysis --input /path/to/bedroom.mp4 --open-id your-open-id

# 分析网络儿童夜间音视频/实时流（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_bedtime_soothing_analysis --url https://example.com/bedroom.mp4 --open-id your-open-id

# 显示历史夜间安抚记录清单（自动触发关键词：查看儿童睡前安抚历史报告、夜间安抚日志清单等）
python -m scripts.smyx_child_bedtime_soothing_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_bedtime_soothing_analysis --input br.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_bedtime_soothing_analysis --input br.mp4 --open-id your-open-id --output result.json
```
