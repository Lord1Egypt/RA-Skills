---
name: "smyx-separation-anxiety-relief-analysis"
description: "AI-powered pet separation anxiety detection & relief when the owner leaves home. Real-time monitoring via smart camera detects typical anxiety signs—continuous vocalization, pacing, scratching doors/windows, destructive chewing. When anxiety reaches preset thresholds, the system auto-triggers comfort actions (play owner's pre-recorded voice, dispense treats via smart feeder, activate interactive toys) to reduce anxiety and destructive behavior, improving pet welfare. Scenarios: pet households (especially office workers / frequent travelers), pet boarding centers. | 通过智能家居摄像头（宠物摄像头）实时监测主人离家后宠物的行为，检测持续性发声（哀嚎、嚎叫）、来回踱步、抓挠门窗或破坏家具等分离焦虑典型表现。当焦虑行为达到预设阈值时，自动触发安抚动作，包括播放主人预录的安抚语音、联动智能零食机投掷零食、或启动互动玩具（如自动逗猫棒），减轻宠物独处时的焦虑，减少破坏行为，提升宠物福利。应用场景：宠物家庭（尤其上班族、经常出差的主人）、宠物寄养中心。"
version: "1.0.0"
---

# Pet Separation Anxiety Relief (Owner Away) | 宠物分离焦虑舒缓（主人离家时）

AI-powered pet separation anxiety detection & relief when the owner leaves home. Real-time monitoring via smart camera detects typical anxiety signs—continuous vocalization, pacing, scratching doors/windows, destructive chewing. When anxiety reaches preset thresholds, the system auto-triggers comfort actions (play owner's pre-recorded voice, dispense treats via smart feeder, activate interactive toys) to reduce anxiety and destructive behavior, improving pet welfare. Scenarios: pet households (especially office workers / frequent travelers), pet boarding centers.

通过智能家居摄像头（宠物摄像头）实时监测主人离家后宠物的行为，检测持续性发声（哀嚎、嚎叫）、来回踱步、抓挠门窗或破坏家具等分离焦虑典型表现。当焦虑行为达到预设阈值时，自动触发安抚动作，包括播放主人预录的安抚语音、联动智能零食机投掷零食、或启动互动玩具（如自动逗猫棒），减轻宠物独处时的焦虑，减少破坏行为，提升宠物福利。应用场景：宠物家庭（尤其上班族、经常出差的主人）、宠物寄养中心。

## 🎯 AI 角色

**假设你是一个专业的宠物行为健康AI。你的任务是分析主人离家后宠物活动区域的视频，检测宠物的分离焦虑相关行为（持续性发声、来回踱步、抓挠门/窗、破坏物品等），并根据焦虑等级触发相应的安抚动作建议。不要提供医疗诊断，仅输出行为识别结果及推荐的干预措施。**

## 任务目标

- 本 Skill 用于：通过独处时段视频分析宠物的分离焦虑行为，识别焦虑等级，输出干预建议（可联动智能设备执行安抚动作）
- 能力包含：分离焦虑行为识别（持续吠叫/嚎叫、来回踱步、抓挠门窗、破坏家具、过度舔毛/自残）、焦虑等级量化（轻度/中度/重度）、行为发生时间与持续时长统计、安抚策略推荐（语音/零食/互动玩具）
- 触发条件:
    1. **默认触发**：当用户提供主人离家后宠物独处状态的视频需要分析时，默认触发本技能进行分离焦虑监测
    2. 当用户明确需要分离焦虑监测时，提及分离焦虑、独处、哀嚎、吠叫、破坏家具、抓门、上班族养宠等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史焦虑报告、历史分离焦虑报告、焦虑监测报告清单、显示所有焦虑报告、查询独处行为记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有焦虑报告"、"显示分离焦虑监测报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_separation_anxiety_relief_analysis --list --open-id` 参数调用 API
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

**在执行分离焦虑监测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备视频输入**
        - 提供本地宠物独处状态视频文件路径或网络视频 URL
        - 拍摄建议：固定宠物摄像头拍摄，视角覆盖宠物主要活动区域（门口、客厅、休息区等），含音频更佳
        - 视频时段：主人离家后的独处时段，建议时长 ≥ 2 分钟以覆盖焦虑行为周期
        - 支持视频格式：mp4/avi/mov
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行分离焦虑监测**
        - 调用 `-m scripts.smyx_separation_anxiety_relief_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地宠物独处状态视频文件路径
            - `--url`: 网络宠物独处状态视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示分离焦虑监测历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看监测结果**
        - 接收结构化的分离焦虑监测报告
        - 包含：**焦虑行为检测**（持续性发声/踱步/抓挠/破坏）、**焦虑等级**（轻度/中度/重度）、**行为时间线**（每种行为的发生时段和持续时长）、**安抚建议**（如"狗狗表现出中度焦虑，已推荐播放主人录音"）、**干预执行记录**（若有联动设备）
        - **重要提示**：仅输出基于视觉和音频的行为识别结果，**不提供医疗诊断**；严重焦虑建议咨询兽医或行为师

## 😰 分离焦虑行为识别指标

| 行为指标 | 具体表现 | 严重程度标记 |
|----------|----------|--------------|
| 🔊 持续性发声 | 哀嚎、嚎叫、连续吠叫（非警示性） | 单次 <2min 轻度；2-10min 中度；>10min 重度 |
| 🚶 来回踱步 | 在门/窗附近反复走动，无法安顿 | 偶尔轻度；持续 >5min 中度；>15min 重度 |
| 🚪 抓挠门窗 | 用爪抓挠门框、窗台，试图突破 | 轻微抓挠轻度；持续抓挠中度；造成损伤重度 |
| 💔 破坏物品 | 咬碎枕头、沙发、鞋子等 | 偶尔轻度；频繁中度；大规模破坏重度 |
| 🐾 过度舔毛/自残 | 反复舔舐同一部位至脱毛/皮肤破损 | 轻度舔舐中度；明显脱毛/伤口重度 |
| 😿 拒食/拒水 | 主人离开后长时间不进食饮水 | — |
| 😰 异常排泄 | 在非指定区域排泄（非行为问题导致） | — |

## 📊 焦虑等级与安抚策略

| 焦虑等级 | 行为表现 | 推荐安抚策略 | APP 通知 |
|----------|----------|--------------|----------|
| 🟢 轻度 | 偶尔吠叫/踱步，能自行安顿 | 无需干预，持续观察 | 不推送，日志记录 |
| 🟡 中度 | 持续吠叫/踱步 2-10 分钟 | ① 播放主人预录安抚语音<br>② 智能零食机投喂零食<br>③ 启动低强度互动玩具 | "狗狗表现出分离焦虑，已播放你的录音" |
| 🔴 重度 | 持续嚎叫 >10 分钟、破坏物品、自残 | ① 播放主人语音（循环）<br>② 零食投喂（转移注意力）<br>③ 启动互动玩具（高强度）<br>④ 建议主人远程通话 | ⚠️ "狗狗严重焦虑，正在执行安抚，建议远程通话或提前回家" |

## 🔧 智能设备联动参考

| 联动设备 | 安抚作用 | 适用等级 |
|----------|----------|----------|
| 🔊 智能音箱 | 播放主人预录语音/轻音乐 | 中度起 |
| 🍪 智能零食机 | 投喂零食转移注意力 | 中度起 |
| 🎮 自动逗猫棒/互动球 | 消耗精力、转移焦点 | 中度起 |
| 📱 远程视频通话 | 主人实时安抚 | 重度 |
| 💡 智能灯光 | 调暗灯光营造安静氛围 | 轻度起 |
| 🌡️ 智能温控 | 调节至舒适温度（焦虑+喘息时降温） | 中度起 |

## 💡 日常预防建议参考

| 策略 | 说明 |
|------|------|
| 🚪 渐进式离家训练 | 从 5 分钟开始逐步延长独处时间 |
| 🎾 离家前充分运动 | 消耗精力减少焦虑 |
| 🍖 离家时留益智玩具 | KONG 填食玩具、嗅闻垫等 |
| 🚫 离家/回家不过度互动 | 避免强化"主人离开=大事"的认知 |
| 🛏️ 设置安全区 | 狗窝/猫窝+主人气味的衣物 |

## 资源索引

- 必要脚本：见 [scripts/smyx_separation_anxiety_relief_analysis.py](scripts/smyx_separation_anxiety_relief_analysis.py)(用途：调用 API 进行分离焦虑监测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 2 分钟
- **含音频的视频可提升检测准确率**（吠叫/嚎叫是核心焦虑指标），建议使用带麦克风的宠物摄像头
- 摄像头需固定，视角覆盖门口、客厅等宠物主要活动区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **监测结果仅供行为观察参考，不提供医疗诊断**；严重焦虑建议咨询兽医或专业行为师
- 部分宠物在门口等待属于正常行为，需与持续性焦虑行为区分（结合时长和频次综合判断）
- 智能设备联动为推荐策略，实际执行需用户提前配置对应设备
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史监测报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`分离焦虑监测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 分离焦虑监测报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物独处状态视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_separation_anxiety_relief_analysis --input /path/to/pet_alone.mp4 --pet-type dog --open-id your-open-id

# 分析网络宠物独处状态视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_separation_anxiety_relief_analysis --url https://example.com/pet_alone.mp4 --pet-type dog --open-id your-open-id

# 显示历史监测报告/显示报告清单列表（自动触发关键词：查看历史焦虑报告、焦虑报告清单等）
python -m scripts.smyx_separation_anxiety_relief_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_separation_anxiety_relief_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_separation_anxiety_relief_analysis --input video.mp4 --pet-type dog --open-id your-open-id --output result.json
```
