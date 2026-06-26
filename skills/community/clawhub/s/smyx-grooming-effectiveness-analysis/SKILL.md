---
name: "smyx-grooming-effectiveness-analysis"
description: "Triggers when a user provides a pet grooming area video or image URL/file for analysis; supports local uploads or network URLs to call server-side APIs for coat condition and shed hair recognition, detecting matting area ratio and shed hair volume to output hairball risk level, helping prevent hairball syndrome. Application scenarios: smart grooming tools, long-haired pet care, pet health management. | 当用户提供梳毛器区域的视频/图像URL或文件时，触发本技能进行毛发表面状态分析；支持通过上传本地视频/图片或网络URL，调用服务端API进行识别，检测打结面积占比、梳下毛发量（堆积面积），输出毛球风险等级，帮助预防毛球症。应用场景：智能梳毛器、长毛宠物护理、宠物健康管理。"
version: "1.0.2"
license: "MIT-0"
---

# Pet Grooming Effectiveness & Hairball Risk Analysis | 宠物梳毛器梳理效果与毛球风险分析

Triggers when a user provides a pet grooming area video or image URL/file for analysis; supports local uploads or
network URLs to call server-side APIs for coat condition and shed hair recognition, detecting matting area ratio and
shed hair volume to output hairball risk level, helping prevent hairball syndrome. Application scenarios: smart grooming
tools, long-haired pet care, pet health management.

当用户提供梳毛器区域的视频/图像URL或文件时，触发本技能进行毛发表面状态分析；支持通过上传本地视频/图片或网络URL，调用服务端API进行识别，检测打结面积占比、梳下毛发量（堆积面积），输出毛球风险等级，帮助预防毛球症。应用场景：智能梳毛器、长毛宠物护理、宠物健康管理。

## 🎯 AI 角色

假设你是一个专业的宠物护理分析AI。你的任务是基于梳毛器区域的视频/图像（梳毛前后），分析宠物毛发的打结程度和梳下的毛发量，评估毛球症风险等级。不要提供医疗诊断或治疗方案，仅客观描述观察到的毛发状态。

## 任务目标

- 本 Skill 用于：通过梳毛器区域视频/图像进行宠物毛发状态分析，获取标准化的梳理效果评估和毛球风险等级
- 能力包含：视频/图像分析、毛发打结面积检测、梳下毛发量估算、毛球风险等级评估、梳理效果评分、历史趋势对比
- 触发条件:
    1. **默认触发**：当用户提供梳毛器区域视频/图像 URL 或文件需要分析时，默认触发本技能进行梳理效果与毛球风险分析
    2. 当用户明确需要进行毛发/梳毛监测时，提及梳毛、毛发打结、掉毛量、毛球症、毛球风险、梳理效果、长毛护理、换毛期等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史梳毛报告、历史梳理报告、毛球风险报告清单、梳毛分析报告清单、查询历史毛发报告、显示所有梳毛报告、显示毛球风险报告，查询健康风险提示报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有梳毛报告"、"
       显示所有毛球风险报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_grooming_effectiveness_analysis --list` 调用 API
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
    1. **准备视频/图像输入**
        - 提供本地视频/图片文件路径或网络 URL
        - 确保画面清晰展示梳毛器区域，能看到宠物毛发表面状态和梳下的毛发堆积，光线充足，无遮挡
        - 建议提供梳毛前后的对比画面，以获得更准确的梳理效果评估
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行梳理效果与毛球风险分析**
        - 调用 `-m scripts.smyx_grooming_effectiveness_analysis 处理视频/图像文件（**必须在技能根目录下运行脚本
          **）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/bird/other，默认 cat
            - `--list`: 显示梳毛历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的梳理效果与毛球风险观察报告
        -
       包含：毛发打结面积占比（体表可见打结区域面积与总体表面积的比例）、打结严重程度分级（轻度/中度/重度）、梳下毛发量估算（堆积面积或视觉体积评估）、梳理效果评分（基于梳毛前后对比的改善程度）、毛球风险等级（低/中/高/极高）、历史趋势对比（与近期梳毛报告的打结/掉毛趋势变化）
        - **重要提示**：仅客观描述观察到的毛发状态，不提供医疗诊断或治疗方案

## 📊 分析指标说明

| 指标     | 说明                     | 风险参考                                   |
|--------|------------------------|----------------------------------------|
| 打结面积占比 | 毛发表面可见打结/缠结区域占总体表面积的比例 | <5% 低风险；5-15% 中风险；15-30% 高风险；>30% 极高风险 |
| 打结严重程度 | 基于打结密度和深度的综合分级         | 轻度（表面浮毛纠缠）/ 中度（形成毛片）/ 重度（贴皮毛毡化）        |
| 梳下毛发量  | 梳毛后脱落在梳毛器/周围的毛发堆积量     | 少量（正常代谢）/ 中量（换毛期）/ 大量（异常脱毛需关注）         |
| 梳理效果评分 | 梳毛前后毛发平整度改善程度（0-100）   | >80 梳理充分；60-80 基本到位；<60 需补充梳理          |
| 毛球风险等级 | 基于打结程度、掉毛量和宠物品种的综合评估   | 低 / 中 / 高 / 极高                         |
| 历史趋势   | 与近期报告对比的打结和掉毛变化趋势      | 持续加重需关注换毛期或皮肤问题                        |

## 🐱 毛球风险等级定义

| 风险等级  | 判定条件                  | 建议措施              |
|-------|-----------------------|-------------------|
| 🟢 低  | 打结<5%，梳下毛量少，短毛或已充分梳理  | 维持当前梳理频率即可        |
| 🟡 中  | 打结5-15%，梳下毛量中等，轻度缠结   | 适当增加梳理频次，关注换毛期    |
| 🟠 高  | 打结15-30%，梳下毛量较大，有明显毛片 | 增加每日梳理，考虑化毛膏辅助    |
| 🔴 极高 | 打结>30%，梳下毛量很大，贴皮毡化    | 需专业美容处理，高度关注毛球症风险 |

## 资源索引

-

必要脚本：见 [scripts/smyx_grooming_effectiveness_analysis.py](scripts/smyx_grooming_effectiveness_analysis.py)(
用途：调用 API 进行梳理效果与毛球风险分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；图片支持 jpg/png 格式
- 分析结果仅供护理参考，不提供医疗诊断或治疗方案
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 梳下毛发量评估基于视觉面积/体积估算，非精确称重，仅供参考
- 长毛品种（波斯猫、布偶猫、金毛犬等）建议适当提高梳理频率和关注等级
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`梳毛器梳理效果分析报告-{记录id}`
  形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 梳毛器梳理效果分析报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地梳毛器视频
python -m scripts.smyx_grooming_effectiveness_analysis --input /path/to/grooming_video.mp4 --pet-type cat

# 分析网络梳毛器视频
python -m scripts.smyx_grooming_effectiveness_analysis --url https://example.com/grooming_video.mp4 --pet-type cat

# 显示历史分析报告/显示分析报告清单列表/显示历史梳毛报告（自动触发关键词：查看历史梳毛报告、历史报告、梳毛报告清单等）
python -m scripts.smyx_grooming_effectiveness_analysis --list

# 输出精简报告
python -m scripts.smyx_grooming_effectiveness_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_grooming_effectiveness_analysis --input video.mp4 --pet-type cat --output result.json
```
