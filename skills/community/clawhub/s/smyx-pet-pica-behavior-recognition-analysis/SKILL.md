---
name: "smyx-pet-pica-behavior-recognition-analysis"
description: "Triggers when a user provides an indoor camera video for analysis; supports local uploads or network URLs to call server-side APIs for pet pica-behavior recognition, detecting contact between the pet's mouth and non-food hazardous items (electric wires, plastic bags, socks, tissues, toy fragments, etc.); when the contact lasts ≥ 2 seconds, outputs a warning signal to help prevent intestinal obstruction, electric shock and other dangers (without diagnosing diseases). Application scenarios: indoor cameras, pet safety monitoring, smart-home security. | 当用户提供室内监控视频时，触发本技能进行异食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物嘴部与电线、塑料袋、袜子、纸巾、玩具碎片等非食物物品的接触动作；持续接触 ≥ 2 秒时输出预警信号，预防肠梗阻、触电等危险（不诊断疾病）。应用场景：室内摄像头、宠物安全监控、智能家居安防。"
version: "1.0.3"
license: "MIT-0"
---

# Pet Pica Behavior Recognition | 宠物异食行为识别（啃咬电线/塑料）

Triggers when a user provides an indoor camera video for analysis; supports local uploads or network URLs to call
server-side APIs for pet pica-behavior recognition, detecting contact between the pet's mouth and non-food hazardous
items (electric wires, plastic bags, socks, tissues, toy fragments, etc.); when the contact lasts ≥ 2 seconds, outputs a
warning signal to help prevent intestinal obstruction, electric shock and other dangers (without diagnosing diseases).
Application scenarios: indoor cameras, pet safety monitoring, smart-home security.

当用户提供室内监控视频时，触发本技能进行异食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物嘴部与电线、塑料袋、袜子、纸巾、玩具碎片等非食物物品的接触动作；持续接触 ≥
2 秒时输出预警信号，预防肠梗阻、触电等危险（不诊断疾病）。应用场景：室内摄像头、宠物安全监控、智能家居安防。

## 🎯 AI 角色

**你是一个专业的宠物安全监测AI。你的任务是基于室内环境的连续视频，检测宠物是否有啃咬或咀嚼非食物物品（如电线、塑料制品、袜子、纸巾、玩具碎片等）的行为。当检测到宠物嘴部与危险物品接触并持续超过
2 秒时，输出预警信号。不要提供疾病诊断，仅客观描述行为和风险等级。**

## 任务目标

- 本 Skill 用于：通过室内监控视频识别宠物异食行为（嘴部与危险物品接触），持续 ≥ 2 秒时输出预警，预防肠梗阻、触电、中毒等危险
-
能力包含：视频分析、宠物嘴部定位、危险物品识别（电线/塑料/袜子/纸巾/玩具碎片等）、接触动作检测、持续时长统计（秒）、风险等级判定、预警信号输出、外部干预建议（声光劝阻 /
推送告警）
- 触发条件:
    1. **默认触发**：当用户提供室内监控视频 URL 或文件需要分析时，默认触发本技能进行异食行为识别
    2. 当用户明确需要进行宠物安全监控时，提及啃电线、咬塑料、吞袜子、误食、肠梗阻、触电、宠物乱咬、异食癖、宠物安全监控等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史异食报告、历史误食预警报告、异食行为报告清单、查询误食记录、显示所有宠物安全报告、显示异食识别报告，查询宠物安全风险提示报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有异食报告"、"
       显示所有误食预警报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_pica_behavior_recognition_analysis --list` 调用 API
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
        - 提供本地视频文件路径或网络视频 URL
        - 视频应清晰展示宠物活动区域，光线充足、无明显遮挡
        - 建议覆盖宠物嘴部能被识别的角度（不要全程纯背影）
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行异食行为识别分析**
        - 调用 `-m scripts.smyx_pet_pica_behavior_recognition_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--list`: 显示异食行为识别历史分析报告列表清单（可输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的异食行为观察报告
        - 包含：危险物品类别识别（电线/塑料/袜子/纸巾/玩具碎片等）、接触开始时间、接触持续时长（秒）、是否超阈值（默认 ≥ 2
          秒判定为预警）、风险等级（中/高/紧急）、外部干预建议（声光劝阻 / 推送告警 / 紧急联系主人）
        - **重要提示**：仅客观描述行为与风险等级，不提供疾病诊断

## 危险物品 & 风险等级参考

| 风险等级  | 物品示例                            | 危险类型            | 默认接触阈值 | 建议干预                 |
|-------|---------------------------------|-----------------|--------|----------------------|
| 🚨 紧急 | 通电电线 / 充电中数据线 / 化学清洁剂瓶 / 药品     | 触电 / 烧伤 / 中毒    | ≥ 1 秒  | 立即声光劝阻 + 推送主人 + 紧急联系 |
| ⚠️ 高  | 塑料袋 / 袜子 / 内衣 / 橡皮筋 / 发圈 / 玩具碎片 | 窒息 / 肠梗阻 / 线性异物 | ≥ 2 秒  | 声光劝阻 + 推送告警          |
| ⚠️ 中  | 纸巾 / 厕纸 / 包装盒纸片                 | 消化道堵塞           | ≥ 3 秒  | 声音温和提醒 + 记录          |
| ℹ️ 关注 | 自身玩具 / 磨牙棒                      | 正常啃咬            | —      | 无需干预                 |

> 注：以上参考标准仅供视觉判定参考，最终判定以 API 输出结果为准。幼宠、好奇心强的猎犬种（拉布拉多、金毛、比格等）天然异食风险更高，需更频繁监测。

## 资源索引

-
必要脚本：见 [scripts/smyx_pet_pica_behavior_recognition_analysis.py](scripts/smyx_pet_pica_behavior_recognition_analysis.py)(
用途：调用 API 进行室内监控视频的异食行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、危险物品类别和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- 推荐结果仅供安全监测参考，不提供疾病诊断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 预警信号由智能家居安防设备（智能音箱 / 宠物摄像头）基于本技能输出结果触发，本技能仅负责输出干预建议
- 幼宠、好奇心强的猎犬种（拉布拉多、金毛、比格等）天然异食风险更高，AI 角色在输出时需主动提醒
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 `reportImageUrl` 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`异食行为识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 异食行为识别报告-20260522024900001 | 狗 | 2026-05-22 02:49:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地室内监控视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --input /path/to/indoor_video.mp4 --pet-type dog

# 分析网络室内监控视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --url https://example.com/indoor_video.mp4 --pet-type dog

# 显示历史分析报告清单（自动触发关键词：查看历史异食报告、误食预警报告清单等）
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --list

# 输出精简报告
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --input indoor_video.mp4 --pet-type dog --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --input indoor_video.mp4 --pet-type dog --output result.json
```
