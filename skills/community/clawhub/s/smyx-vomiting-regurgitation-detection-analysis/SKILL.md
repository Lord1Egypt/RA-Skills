---
name: "smyx-vomiting-regurgitation-detection-analysis"
description: "AI-powered pet vomiting and regurgitation detection from indoor fixed-camera video. Identifies rhythmic abdominal contractions, head-forward extension, and mouth opening actions, plus detects vomitus on the floor (food, hairball, bile). Records event time, frequency, and vomitus characteristics for early digestive issue discovery. Scenarios: daily home health monitoring, multi-pet households, senior pet care, animal hospital inpatient observation. | 通过室内固定摄像头分析宠物活动区域的连续视频，利用动作识别技术检测宠物的呕吐或反流行为（包括腹部节律性收缩、口部张合、头部前伸等典型动作），同时识别地面是否出现呕吐物（食物残渣、毛球、黄色胆汁等），记录发生时间、频次以及呕吐物特征。有助于主人及早发现宠物的消化系统问题，避免延误治疗。应用场景：宠物家庭日常健康监护、多宠家庭、老年宠物护理、宠物医院住院观察。"
version: "1.0.3"
license: "MIT-0"
---

# Pet Vomiting / Regurgitation Detection | 宠物呕吐/反流行为识别

AI-powered pet vomiting and regurgitation detection from indoor fixed-camera video. Identifies rhythmic abdominal contractions, head-forward extension, and mouth opening actions, plus detects vomitus on the floor (food, hairball, bile). Records event time, frequency, and vomitus characteristics for early digestive issue discovery. Scenarios: daily home health monitoring, multi-pet households, senior pet care, animal hospital inpatient observation.

通过室内固定摄像头分析宠物活动区域的连续视频，利用动作识别技术检测宠物的呕吐或反流行为（包括腹部节律性收缩、口部张合、头部前伸等典型动作），同时识别地面是否出现呕吐物（食物残渣、毛球、黄色胆汁等），记录发生时间、频次以及呕吐物特征。有助于主人及早发现宠物的消化系统问题，避免延误治疗。应用场景：宠物家庭日常健康监护、多宠家庭、老年宠物护理、宠物医院住院观察。

## 🎯 AI 角色

**假设你是一个专业的宠物消化健康AI。你的任务是分析室内固定摄像头的连续视频，检测宠物是否发生呕吐或反流行为，识别呕吐动作特征以及地面呕吐物出现情况，记录事件发生时间和频次。不要提供医疗诊断，仅输出基于视觉的行为观察结果。**

## 任务目标

- 本 Skill 用于：通过室内摄像头视频进行宠物呕吐/反流行为检测，识别典型呕吐动作和地面呕吐物，记录事件时间、频次和呕吐物特征
- 能力包含：呕吐动作识别（腹部收缩、头部前伸、口部张合）、反流行为区分、地面呕吐物检测与分类、事件时间戳记录、频次统计、呕吐物特征描述
- 触发条件:
    1. **默认触发**：当用户提供宠物活动区域视频需要分析时，默认触发本技能进行呕吐/反流行为识别
    2. 当用户明确需要呕吐监测时，提及呕吐、吐毛球、反流、干呕、消化异常等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史呕吐报告、历史呕吐监测报告、呕吐行为报告清单、显示所有呕吐报告、查询呕吐事件记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有呕吐报告"、"显示呕吐监测报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_vomiting_regurgitation_detection_analysis --list` 调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔐 用户身份处理（内部自动完成）

用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

- 上游系统如有内部身份参数，会由脚本静默接收并使用
- 上游系统未提供时，脚本会自动复用本地缺省用户
- 本地缺省用户不存在时，脚本会自动创建并在后续任务中复用
- 对用户输出时，只展示分析进度、分析结果和报告链接，不展示内部身份值

**关键约束：**

- 不得提示用户输入用户名、手机号或任何内部身份参数
- 不得在回复、报告、示例、错误提示中暴露内部身份值
- 不得把内部身份参数列为用户需要理解或传入的参数
- 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地宠物活动区域视频文件路径或网络视频 URL
        - 拍摄建议：固定摄像头拍摄，视角覆盖宠物常活动区域及地面，光线充足
        - 视频时长：建议 ≥ 30 秒，长视频可覆盖更完整的监测时段
        - 支持视频格式：mp4/avi/mov
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行呕吐/反流行为识别**
        - 调用 `-m scripts.smyx_vomiting_regurgitation_detection_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地宠物活动区域视频文件路径
            - `--url`: 网络宠物活动区域视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--list`: 显示呕吐/反流行为识别历史报告列表清单
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看识别结果**
        - 接收结构化的呕吐/反流行为识别报告
        - 包含：**呕吐行为检测**（是否检测到呕吐动作）、**动作特征描述**（腹部收缩/头部前伸/口部张合）、**呕吐物识别**（有无/类型：食物残渣/毛球/黄色胆汁/泡沫/液体）、**事件时间戳**、**频次统计**、**健康建议**（如"猫咪于 15:30 发生呕吐，呕吐物为毛球，建议观察后续状态"）
        - **重要提示**：仅输出基于视觉的行为观察结果，**不提供医疗诊断**；频繁呕吐建议及时就医

## 🤢 呕吐 vs 反流：关键区别

| 特征 | 呕吐（Vomiting） | 反流（Regurgitation） |
|------|------------------|----------------------|
| 触发机制 | 主动，涉及腹部强烈收缩 | 被动，无明显腹部用力 |
| 动作特征 | 干呕→腹部节律收缩→头部前伸→排出 | 食管被动排出，动作较轻 |
| 排出物 | 部分消化食物、胆汁、泡沫 | 未消化食物、黏液 |
| 时间 | 可在进食后数小时 | 通常在进食后不久 |
| 常见原因 | 胃肠炎、中毒、胰腺炎、毛球 | 食管扩张、食管异物 |

> **区分意义**：呕吐和反流涉及不同疾病方向，准确区分有助于兽医初步判断。

## 🟡 呕吐物类型与可能提示

| 呕吐物类型 | 外观特征 | 可能原因 |
|------------|----------|----------|
| 🐛 毛球 | 圆柱形，主要为毛发 | 猫咪正常排毛球；频繁则需关注 |
| 🍖 食物残渣 | 可辨认的未消化食物 | 进食过快、食物不耐受 |
| 💛 黄色胆汁 | 黄色液体，空腹常见 | 空腹呕吐、胆汁性呕吐综合征 |
| 🤍 白色泡沫 | 白色黏稠泡沫 | 胃酸过多、空腹干呕 |
| 🔴 带血 | 红色或咖啡色 | ⚠️ 胃出血、溃疡、异物划伤，需立即就医 |
| 🟫 异物 | 含塑料、线绳等 | ⚠️ 误食异物，需立即就医 |

## 🚨 预警分级

| 等级 | 触发条件 | 建议 |
|------|----------|------|
| 🟢 偶发 | 24小时内 1 次，呕吐物为毛球或食物 | 观察，注意饮食和饮水量 |
| 🟡 频发 | 24小时内 2-3 次，或连续两天呕吐 | 建议预约兽医检查 |
| 🟠 严重 | 24小时内 ≥4 次，呕吐物含胆汁或泡沫 | 尽快就医，注意补充水分 |
| 🔴 危急 | 呕吐物带血，或伴精神萎靡/拒食 | ⚠️ 立即就医，警惕中毒、肠梗阻 |

## 💡 高风险群体关注

| 类别 | 重点关注原因 |
|------|--------------|
| 多宠家庭 | 难以及时发现哪个宠物呕吐，AI 可区分个体 |
| 老年宠物 | 慢性肾病、肿瘤等可表现为频繁呕吐 |
| 幼宠 | 易误食异物，呕吐后脱水风险更高 |
| 长毛猫 | 毛球症高发，需定期梳毛辅助 |

## 资源索引

- 必要脚本：见 [scripts/smyx_vomiting_regurgitation_detection_analysis.py](scripts/smyx_vomiting_regurgitation_detection_analysis.py)(用途：调用 API 进行呕吐/反流行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 30 秒
- 摄像头需固定且视角覆盖宠物活动区域及地面，移动/手持拍摄可能影响检测效果
- **识别结果仅供行为观察参考，不提供医疗诊断**；频繁呕吐或呕吐物带血建议立即就医
- 宠物可能做出类似呕吐的伸懒腰、咳嗽等动作，存在一定误检可能，建议结合呕吐物确认
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史识别报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`呕吐反流行为识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 呕吐反流行为识别报告-20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物活动区域视频
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --input /path/to/pet_room.mp4 --pet-type cat

# 分析网络宠物活动区域视频
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --url https://example.com/pet_room.mp4 --pet-type cat

# 显示历史识别报告/显示报告清单列表（自动触发关键词：查看历史呕吐报告、呕吐报告清单等）
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --input video.mp4 --pet-type cat --output result.json
```
