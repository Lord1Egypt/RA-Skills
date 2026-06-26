---
name: "smyx-sneeze-cough-detection-analysis"
description: "AI-powered pet sneeze/cough detection from real-time camera (optional audio fusion). Analyzes head and thoracic-abdominal motion plus sound features to distinguish single occasional events (normal airway clearing) from continuous bursts (e.g. ≥3 sneezes/min, frequent dry/wet coughing) and records event time and frequency. Helps catch respiratory infection, allergy, or foreign-body irritation early. Scenarios: home health monitoring, animal hospital wards, pet boarding centers. | 通过宠物摄像头实时分析宠物头部和胸腹部的动作，结合可选的声音分析，识别宠物是否发生打喷嚏或咳嗽行为。区分单次偶发（可能是正常清理呼吸道）与连续发作（如频繁打喷嚏、干咳、湿咳等异常模式），并记录发生时间及频率。有助于早期发现宠物呼吸道感染、过敏或异物刺激。应用场景：宠物家庭日常健康监测、宠物医院住院观察、宠物寄养中心。"
version: "1.0.1"
license: "MIT-0"
---

# Pet Sneeze / Cough Detection | 宠物打喷嚏/咳嗽检测

AI-powered pet sneeze/cough detection from real-time camera (optional audio fusion). Analyzes head and thoracic-abdominal motion plus sound features to distinguish single occasional events (normal airway clearing) from continuous bursts (e.g. ≥3 sneezes/min, frequent dry/wet coughing) and records event time and frequency. Helps catch respiratory infection, allergy, or foreign-body irritation early. Scenarios: home health monitoring, animal hospital wards, pet boarding centers.

通过宠物摄像头实时分析宠物头部和胸腹部的动作，结合可选的声音分析，识别宠物是否发生打喷嚏或咳嗽行为。区分单次偶发（可能是正常清理呼吸道）与连续发作（如频繁打喷嚏、干咳、湿咳等异常模式），并记录发生时间及频率。有助于早期发现宠物呼吸道感染、过敏或异物刺激。应用场景：宠物家庭日常健康监测、宠物医院住院观察、宠物寄养中心。

## 🎯 AI 角色

**假设你是一个专业的宠物呼吸健康AI。你的任务是分析宠物活动的实时视频（可选配合音频），检测打喷嚏或咳嗽行为。区分单次偶发（可能是正常清理）与连续发作（异常），记录事件时间、频次和类型。不要提供医疗诊断，仅输出基于视觉和音频的客观行为识别结果。**

## 任务目标

- 本 Skill 用于：通过室内摄像头视频（可选叠加音频）进行打喷嚏与咳嗽行为识别，区分偶发与连续发作，记录事件时间、频次和类型
- 能力包含：打喷嚏动作识别（头部抖动+鼻部喷气）、咳嗽动作识别（颈部前伸+腹部收缩）、咳嗽类型区分（干咳/湿咳）、音频特征融合（可选）、连续发作频次统计、单次偶发与异常发作区分
- 触发条件:
    1. **默认触发**：当用户提供宠物活动视频需要分析时，默认触发本技能进行打喷嚏/咳嗽检测
    2. 当用户明确需要呼吸道行为检测时，提及打喷嚏、咳嗽、干咳、湿咳、犬窝咳、鼻炎、过敏等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史咳嗽报告、历史打喷嚏报告、咳嗽检测报告清单、显示所有呼吸道报告、查询咳嗽事件记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有咳嗽报告"、"显示打喷嚏报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_sneeze_cough_detection_analysis --list --open-id` 参数调用 API
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

**在执行打喷嚏/咳嗽检测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备视频输入**
        - 提供本地宠物活动视频文件路径或网络视频 URL
        - 拍摄建议：固定摄像头拍摄，视角覆盖宠物头部及胸腹部区域，光线充足；含音频更佳
        - 视频时长：建议 ≥ 30 秒，长视频可覆盖更完整的监测时段
        - 支持视频格式：mp4/avi/mov
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行打喷嚏/咳嗽检测**
        - 调用 `-m scripts.smyx_sneeze_cough_detection_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地宠物活动视频（含音频）文件路径
            - `--url`: 网络宠物活动视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示打喷嚏/咳嗽检测历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看检测结果**
        - 接收结构化的打喷嚏/咳嗽检测报告
        - 包含：**喷嚏事件**（次数、时间戳、频次）、**咳嗽事件**（次数、时间戳、频次、类型：干咳/湿咳）、**发作模式判定**（偶发/连续）、**频次统计**（如"过去1小时咳嗽5次"）、**健康建议**（如"狗狗在过去1小时内咳嗽5次，请留意是否有其他症状"）
        - **重要提示**：仅输出基于视觉和音频的客观行为识别结果，**不提供医疗诊断**

## 💨 打喷嚏 vs 咳嗽：动作特征区分

| 特征 | 打喷嚏（Sneeze） | 咳嗽（Cough） |
|------|------------------|----------------|
| 主要部位 | 头部突然前伸抖动 | 颈部前伸 + 胸腹收缩 |
| 嘴巴 | 张开喷气 | 干咳张口、湿咳可能闭合 |
| 音频特征 | 短促喷气声 | 干咳：短促刺耳；湿咳：含痰低沉 |
| 持续时间 | 极短（<1秒） | 稍长（1-3秒） |
| 常见原因 | 灰尘、过敏、鼻炎 | 犬窝咳、肺炎、气管炎、异物 |

## 🏥 咳嗽类型参考

| 咳嗽类型 | 特征 | 可能原因 |
|----------|------|----------|
| 🌬️ 干咳 | 无痰，声音清脆刺耳 | 犬窝咳、气管塌陷、过敏 |
| 💧 湿咳 | 有痰音，声音低沉浑浊 | 肺炎、支气管炎 |
| 🪶 鹅鸣咳 | 类似鹅叫声 | 气管塌陷（小型犬常见） |
| 🌙 夜间咳 | 仅在夜间或躺下时咳嗽 | 心脏病（二尖瓣疾病） |

## 🚨 预警分级

| 等级 | 触发条件 | 建议 |
|------|----------|------|
| 🟢 偶发 | 单次打喷嚏/咳嗽，无连续 | 正常清理呼吸道，继续观察 |
| 🟡 轻度 | 连续打喷嚏 ≥3次/分钟 或 咳嗽 2-3次/小时 | 留意环境粉尘、香水等刺激源 |
| 🟠 频繁 | 打喷嚏频繁或 咳嗽 ≥5次/小时 | 建议预约兽医检查呼吸道 |
| 🔴 严重 | 咳嗽持续不断、伴喘息/呼吸困难 | ⚠️ 立即就医，警惕肺炎、心衰 |

## 💡 高风险品种与场景

| 类别 | 重点关注原因 |
|------|--------------|
| 短鼻犬（巴哥、法斗、英斗等） | 气管塌陷风险高，鹅鸣咳常见 |
| 幼犬（未完成疫苗接种） | 犬窝咳传染性强，需隔离观察 |
| 猫咪（多猫环境） | 猫疱疹病毒、杯状病毒易传播 |
| 老年犬 | 慢性支气管炎、心脏病（夜间咳嗽） |
| 换季/花粉季 | 过敏性喷嚏频发 |

## 资源索引

- 必要脚本：见 [scripts/smyx_sneeze_cough_detection_analysis.py](scripts/smyx_sneeze_cough_detection_analysis.py)(用途：调用 API 进行打喷嚏/咳嗽检测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 30 秒
- **含音频的视频可大幅提升检测准确率**，建议使用带麦克风的摄像头拍摄
- 摄像头需固定，视角覆盖宠物头部及胸腹部，移动拍摄可能影响检测效果
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **检测结果仅供行为观察参考，不提供医疗诊断**；频繁发作建议及时就医
- 宠物打哈欠、伸懒腰等动作可能产生误检，建议结合频次和连续性综合判断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史检测报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`打喷嚏咳嗽检测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 打喷嚏咳嗽检测报告-20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物活动视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_sneeze_cough_detection_analysis --input /path/to/pet_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络宠物活动视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_sneeze_cough_detection_analysis --url https://example.com/pet_video.mp4 --pet-type dog --open-id your-open-id

# 显示历史检测报告/显示报告清单列表（自动触发关键词：查看历史咳嗽报告、打喷嚏报告清单等）
python -m scripts.smyx_sneeze_cough_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_sneeze_cough_detection_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_sneeze_cough_detection_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
