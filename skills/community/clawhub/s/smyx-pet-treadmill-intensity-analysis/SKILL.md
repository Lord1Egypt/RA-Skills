---
name: "smyx-pet-treadmill-intensity-analysis"
description: "AI-powered pet treadmill exercise intensity analysis combined with optional heart-rate band data. Detects stride frequency, limb extension, and respiratory rate from treadmill video to assess current exercise load (Low/Medium/High) and provide real-time pacing suggestions. Scenarios: smart pet treadmills (dog/cat), pet weight-loss training centers, pet rehabilitation. | 通过宠物跑步机内置或外置摄像头实时分析宠物跑步视频，检测步频、四肢伸展幅度、呼吸频率等运动姿态指标，并结合可选的心率带数据（蓝牙心率监测），综合评估当前运动强度等级（低/中/高），辅助宠物主人科学控制运动量，防止过度疲劳或运动损伤。应用场景：宠物跑步机（犬用/猫用）、宠物减肥训练中心、宠物康复理疗。"
version: "1.0.0"
---

# Pet Treadmill Intensity & Heart Rate Analysis | 宠物跑步机运动强度与心率关联

AI-powered pet treadmill exercise intensity analysis combined with optional heart-rate band data. Detects stride frequency, limb extension, and respiratory rate from treadmill video to assess current exercise load (Low/Medium/High) and provide real-time pacing suggestions. Scenarios: smart pet treadmills (dog/cat), pet weight-loss training centers, pet rehabilitation.

通过宠物跑步机内置或外置摄像头实时分析宠物跑步视频，检测步频、四肢伸展幅度、呼吸频率等运动姿态指标，并结合可选的心率带数据（蓝牙心率监测），综合评估当前运动强度等级（低/中/高），辅助宠物主人科学控制运动量，防止过度疲劳或运动损伤。应用场景：宠物跑步机（犬用/猫用）、宠物减肥训练中心、宠物康复理疗。

## 🎯 AI 角色

**假设你是一个专业的宠物运动生理AI。你的任务是分析宠物跑步机上的跑步视频（俯视或侧视最佳），检测宠物的步频、四肢伸展幅度、呼吸特征，并可选择融合心率带数据（若提供），综合评估当前运动负荷强度。不要提供医疗建议，仅输出基于视觉和心率数据的运动强度等级。**

## 任务目标

- 本 Skill 用于：通过宠物跑步机视频（可选叠加心率带数据）进行运动强度综合评估，实时输出强度等级与运动建议
- 能力包含：跑步姿态分析、步频检测、四肢伸展幅度评估、呼吸频率识别、心率数据融合、运动强度综合分级、运动建议生成
- 触发条件:
    1. **默认触发**：当用户提供宠物跑步机运动视频需要分析时，默认触发本技能进行运动强度评估
    2. 当用户明确需要运动强度评估时，提及跑步机、步频、呼吸频率、运动强度、心率监测、宠物运动量等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史运动报告、历史跑步机报告、运动强度报告清单、显示所有跑步报告、查询运动训练记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有跑步机报告"、"显示运动强度报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_treadmill_intensity_analysis --list --open-id` 参数调用 API
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

**在执行运动强度评估前，必须按以下优先级顺序获取 open-id：**

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
        - 提供本地跑步机视频文件路径或网络视频 URL
        - 视频拍摄建议：俯视或侧视最佳，能清晰展示宠物四肢运动姿态，背景稳定，光线充足
        - 支持视频格式（mp4/avi/mov）
        - 可选：通过 API 上下文同时传入蓝牙心率带采集的心率数据（bpm 序列）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行运动强度评估**
        - 调用 `-m scripts.smyx_pet_treadmill_intensity_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地跑步机视频文件路径
            - `--url`: 网络跑步机视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示跑步机运动强度分析历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看评估结果**
        - 接收结构化的运动强度评估报告
        - 包含：**步频（步/分钟）**、**四肢伸展幅度**（小/中/大）、**呼吸频率**（次/分钟）、**心率数据**（若接入，bpm/最大心率百分比）、**运动强度综合等级**（低/中/高）、**运动建议**（如"强度适中，可维持"、"强度偏高，建议降速 20%"、"心率超出最大心率 85%，建议立即降速或休息"）
        - **重要提示**：仅基于视觉和心率数据输出运动强度等级，不提供医疗诊断或治疗建议

## 📊 运动强度等级判定标准

| 强度等级 | 心率范围（最大心率%） | 步频范围 | 呼吸特征 | 运动建议 |
|----------|----------------------|----------|----------|----------|
| 🟢 低强度 | 50%-65% | 慢走/小跑 | 平稳，无明显喘气 | 适合热身、康复训练，可适度提速 |
| 🟡 中强度 | 65%-80% | 稳定中速跑 | 加快但规律 | ✅ 减脂黄金区间，建议维持 |
| 🔴 高强度 | 80%-90% | 快速冲刺 | 明显急促，舌头外吐 | ⚠️ 建议降速或缩短时长 |
| 🚨 危险区 | >90% | 极限冲刺 | 剧烈喘气，跟不上节奏 | ❌ 立即停止，散热休息 |

> **最大心率参考公式**（仅供算法估算）：犬类 ≈ 220 - 年龄（岁）× 2.5；猫类 ≈ 220 - 年龄（岁）× 3。具体以兽医建议为准。

## 💡 应用场景说明

| 场景 | 建议训练时长 | 推荐强度 | 说明 |
|------|--------------|----------|------|
| 减脂训练 | 20-30 分钟 | 中强度 | 持续中强度燃烧脂肪效率最高 |
| 体能提升 | 15-20 分钟 | 中-高强度交替 | 间歇训练增强心肺功能 |
| 康复理疗 | 5-15 分钟 | 低强度 | 关节恢复期，禁止高强度 |
| 日常活动量补充 | 10-15 分钟 | 低-中强度 | 长期久卧宠物补足运动量 |

## 资源索引

- 必要脚本：见 [scripts/smyx_pet_treadmill_intensity_analysis.py](scripts/smyx_pet_treadmill_intensity_analysis.py)(用途：调用 API 进行跑步机运动强度评估分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 30 秒以上以保证步频和呼吸频率统计稳定
- 心率带数据为可选项，未提供时仅基于视觉特征评估运动强度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 评估结果仅供运动训练参考，不提供医疗诊断或治疗建议
- 短鼻品种（如英斗、波斯猫）耐热性较差，请结合环境温度谨慎使用
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史评估报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`跑步机运动强度分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 跑步机运动强度分析报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地跑步机视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_treadmill_intensity_analysis --input /path/to/treadmill_run.mp4 --pet-type dog --open-id your-open-id

# 分析网络跑步机视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_treadmill_intensity_analysis --url https://example.com/treadmill_run.mp4 --pet-type dog --open-id your-open-id

# 显示历史评估报告/显示报告清单列表（自动触发关键词：查看历史运动报告、跑步机报告清单等）
python -m scripts.smyx_pet_treadmill_intensity_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_treadmill_intensity_analysis --input treadmill.mp4 --pet-type dog --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_treadmill_intensity_analysis --input treadmill.mp4 --pet-type dog --open-id your-open-id --output result.json
```
