---
name: "smyx-excitement-calming-guide-analysis"
description: "AI-powered pet over-excitement detection & calming guidance. Real-time camera analysis tracks movement speed, jump height, spin laps, and jumping-on-people actions to score excitement level. When the score exceeds safety thresholds, the system auto-issues calming cues (play owner's voice command like 'sit'/'slow down', soft prompt tone, release calming pheromone, dim lights). Helps prevent injuries from over-excitement and keeps the household safe. Scenarios: lively pet households, pet boarding centers, pet daycare, dog training schools. | 通过宠物活动区的固定摄像头实时分析宠物的运动状态，检测狂跳、高速转圈、反复扑人等极度兴奋行为，评估兴奋等级。当兴奋等级超过安全阈值时，自动输出冷静引导指令，包括播放主人的语音口令（如\"坐下\"、\"慢下来\"）、发出柔和提示音，或联动环境设备（如释放宠物镇静信息素、调暗灯光），预防宠物因过度兴奋而撞伤、摔倒或伤人，维护家庭安全。应用场景：宠物家庭（尤其活泼好动的犬猫）、宠物寄养中心、宠物日托班、宠物训练学校。"
version: "1.0.0"
---

# Pet Excitement Calming Guide | 宠物兴奋过度冷静引导

AI-powered pet over-excitement detection & calming guidance. Real-time camera analysis tracks movement speed, jump height, spin laps, and jumping-on-people actions to score excitement level. When the score exceeds safety thresholds, the system auto-issues calming cues (play owner's voice command like 'sit'/'slow down', soft prompt tone, release calming pheromone, dim lights). Helps prevent injuries from over-excitement and keeps the household safe. Scenarios: lively pet households, pet boarding centers, pet daycare, dog training schools.

通过宠物活动区的固定摄像头实时分析宠物的运动状态，检测狂跳、高速转圈、反复扑人等极度兴奋行为，评估兴奋等级。当兴奋等级超过安全阈值时，自动输出冷静引导指令，包括播放主人的语音口令（如"坐下"、"慢下来"）、发出柔和提示音，或联动环境设备（如释放宠物镇静信息素、调暗灯光），预防宠物因过度兴奋而撞伤、摔倒或伤人，维护家庭安全。应用场景：宠物家庭（尤其活泼好动的犬猫）、宠物寄养中心、宠物日托班、宠物训练学校。

## 🎯 AI 角色

**假设你是一个专业的宠物行为安全AI。你的任务是分析宠物活动区域摄像头的实时视频，检测宠物的运动速度、跳跃高度、旋转圈数、扑人动作等指标，评估兴奋等级。当兴奋等级达到"危险"或"过度"时，输出冷静引导指令（如播放语音口令或释放镇静信息素）。不要提供医疗建议，仅输出基于视觉的行为判定和推荐的干预动作。**

## 任务目标

- 本 Skill 用于：通过实时视频分析宠物的运动状态，量化兴奋等级，自动输出冷静引导指令，预防意外
- 能力包含：运动速度检测、跳跃高度评估、旋转圈数统计、扑人动作识别、兴奋等级综合评分、冷静引导策略推荐（语音/提示音/环境设备）
- 触发条件:
    1. **默认触发**：当用户提供宠物活动视频需要分析时，默认触发本技能进行兴奋过度监测
    2. 当用户明确需要兴奋冷静引导时，提及兴奋过度、狂跳、扑人、转圈、迎客失控、宠物打翻东西等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史兴奋报告、历史冷静引导报告、兴奋监测报告清单、显示所有兴奋报告、查询兴奋行为记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有兴奋报告"、"显示冷静引导报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_excitement_calming_guide_analysis --list --open-id` 参数调用 API
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

**在执行兴奋冷静引导分析前，必须按以下优先级顺序获取 open-id：**

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
        - 提供本地宠物活动区域视频文件路径或网络视频 URL
        - 拍摄建议：固定摄像头拍摄，视角覆盖宠物主要活动区域，光线充足，能清晰捕捉运动姿态
        - 视频时长：建议 ≥ 30 秒，较长视频可覆盖更完整的兴奋周期
        - 支持视频格式：mp4/avi/mov
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行兴奋冷静引导分析**
        - 调用 `-m scripts.smyx_excitement_calming_guide_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地宠物活动区域视频文件路径
            - `--url`: 网络宠物活动区域视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示兴奋冷静引导历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的兴奋冷静引导报告
        - 包含：**兴奋行为检测**（狂跳/转圈/扑人等）、**运动指标**（速度/跳跃高度/旋转圈数）、**兴奋等级评分**（0-100）、**冷静引导建议**（如"检测到高速转圈+连续扑人，兴奋等级 82，建议播放'坐下'口令"）
        - **重要提示**：仅输出基于视觉的行为判定和推荐干预动作，**不提供医疗建议**

## ⚡ 兴奋行为识别指标

| 行为指标 | 具体表现 | 兴奋权重 |
|----------|----------|----------|
| 🦘 狂跳/蹦跳 | 离地跳跃 >30cm，连续跳跃 | 高 |
| 🔄 高速转圈 | 原地快速旋转 ≥3 圈/次 | 高 |
| 🙋 反复扑人 | 双前肢离地扑向人，频率 ≥3 次/分钟 | 高 |
| 🏃 极速奔跑 | 室内高速冲刺，频繁变向 | 中 |
| 🐕 疯狂摇尾+呜咽 | 尾巴高频摇摆伴随短促呜咽声 | 中 |
| 🧸 疯狂叼玩具 | 反复甩头撕咬玩具，无法安静 | 低-中 |
| 😺 猫咪跑酷 | 突然全速跑动+跳上跳下 | 中 |

## 📊 兴奋等级与干预策略

| 等级 | 评分 | 行为表现 | 干预策略 | APP 通知 |
|------|------|----------|----------|----------|
| 🟢 正常活跃 | 0-40 | 正常玩耍、摇尾、适度跑动 | 无需干预，继续观察 | 不推送 |
| 🟡 兴奋偏高 | 41-65 | 加速跑动、跳跃增多、轻微扑人 | ① 播放柔和提示音<br>② 发出"慢下来"语音口令 | "宠物兴奋度偏高，已发出冷静提示" |
| 🟠 过度兴奋 | 66-85 | 连续狂跳、高速转圈、频繁扑人 | ① 播放主人"坐下"口令<br>② 调暗灯光<br>③ 释放镇静信息素 | ⚠️ "宠物过度兴奋，已执行冷静引导" |
| 🔴 危险失控 | 86-100 | 持续狂暴行为、撞墙/撞家具、无法自控 | ① 循环播放冷静口令<br>② 调暗灯光+信息素<br>③ 建议主人介入隔离 | 🚨 "宠物兴奋失控，有受伤风险，请立即介入！" |

## 🔧 智能设备联动参考

| 联动设备 | 冷静作用 | 适用等级 |
|----------|----------|----------|
| 🔊 智能音箱 | 播放主人语音口令（"坐下"/"慢下来"） | 兴奋偏高起 |
| 💡 智能灯光 | 调暗灯光降低刺激 | 过度兴奋起 |
| 🌿 信息素扩散器 | 释放犬/猫镇静信息素（DAP/Feliway） | 过度兴奋起 |
| 🎵 背景音乐 | 播放舒缓音乐/白噪音 | 兴奋偏高起 |
| 🍪 智能零食机 | 投喂零食引导"坐下-等待"训练 | 兴奋偏高起 |
| 🚪 自动门/围栏 | 隔离至冷静区 | 危险失控 |

## 💡 高风险品种与场景

| 类别 | 重点关注原因 |
|------|--------------|
| 边境牧羊犬、哈士奇、比格犬 | 精力旺盛，兴奋阈值低 |
| 幼犬（<1岁） | 自控力差，易过度兴奋 |
| 大型犬（拉布拉多、金毛） | 体型大，扑人力量大，易伤人 |
| 猫咪（室内猫） | 跑酷时易撞倒物品 |
| 迎客场景 | 访客到来时兴奋度骤升 |
| 玩耍过火 | 互动游戏后期无法自控 |

## 资源索引

- 必要脚本：见 [scripts/smyx_excitement_calming_guide_analysis.py](scripts/smyx_excitement_calming_guide_analysis.py)(用途：调用 API 进行兴奋冷静引导分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 30 秒
- 摄像头需固定，视角覆盖宠物主要活动区域；移动/手持拍摄可能影响运动检测精度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **分析结果仅供行为安全参考，不提供医疗建议**；反复无法冷静的宠物建议咨询行为训练师
- 猫咪正常跑酷与过度兴奋需结合频率和持续时间综合判断
- 智能设备联动为推荐策略，实际执行需用户提前配置对应设备
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`兴奋冷静引导报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 兴奋冷静引导报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物活动视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_excitement_calming_guide_analysis --input /path/to/pet_play.mp4 --pet-type dog --open-id your-open-id

# 分析网络宠物活动视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_excitement_calming_guide_analysis --url https://example.com/pet_play.mp4 --pet-type dog --open-id your-open-id

# 显示历史分析报告/显示报告清单列表（自动触发关键词：查看历史兴奋报告、冷静引导报告清单等）
python -m scripts.smyx_excitement_calming_guide_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_excitement_calming_guide_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_excitement_calming_guide_analysis --input video.mp4 --pet-type dog --open-id your-open-id --output result.json
```
