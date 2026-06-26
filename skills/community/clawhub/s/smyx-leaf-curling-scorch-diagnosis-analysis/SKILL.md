---
name: "smyx-leaf-curling-scorch-diagnosis-analysis"
description: "Using agricultural cameras to capture high-resolution images of plant leaves, AI vision techniques detect leaf curling direction (up-curling or down-curling) and the distribution of leaf-margin scorch (old vs new leaves, tip vs margin). | 通过农业摄像头拍摄植物叶片的高清图像，利用AI视觉分析技术检测叶片卷曲方向（上卷或下卷）、焦边（叶缘干枯）的分布特征（老叶/新叶、叶尖/叶缘），并可结合土壤湿度传感器数据（可选），综合判断卷叶/焦边的主要原因（干旱胁迫、病害如白粉病/病毒病、药害、肥害等）。系统定期巡检，发现卷叶或焦边时自动分析原因，输出诊断及建议（如'叶片上卷、叶缘焦枯，土壤湿度偏低，可能干旱，建议灌溉'）。"
version: "1.0.4"
license: "MIT-0"
---

# Leaf Curling & Margin Scorch Diagnosis | 植物卷叶/焦边识别（干旱/病害）

Using agricultural cameras to capture high-resolution images of plant leaves, AI vision techniques detect leaf curling
direction (up-curling or down-curling) and the distribution of leaf-margin scorch (old vs new leaves, tip vs margin).
Combined with optional soil-moisture sensor data, the system jointly judges the most likely cause of curling/scorching (
drought stress, diseases such as powdery mildew or virus, pesticide damage, fertilizer burn, etc.). This helps farmers
quickly locate the problem and take targeted action. Application scenarios: open-field crops, greenhouse vegetables,
orchards. The system periodically inspects fields; when curling or scorching is detected it automatically analyzes the
cause and issues a diagnosis (e.g., 'leaves curled upward with margin scorch, soil moisture low — likely drought,
suggest irrigation'). Skill features: leaf curling and margin scorch are common but easy to misjudge because drought,
diseases and chemical damage share similar symptoms. AI-assisted visual diagnosis helps farmers respond correctly in
time and reduce losses. Can be integrated into agricultural IoT systems, UAV inspection platforms, or mobile apps.

通过农业摄像头拍摄植物叶片的高清图像，利用AI视觉分析技术检测叶片卷曲方向（上卷或下卷）、焦边（叶缘干枯）的分布特征（老叶/新叶、叶尖/叶缘），并可结合土壤湿度传感器数据（可选），综合判断卷叶/焦边的主要原因（干旱胁迫、病害如白粉病/病毒病、药害、肥害等）。该技能有助于农民快速定位问题，采取针对性措施。应用场景：大田作物、温室蔬菜、果园。系统定期巡检，发现卷叶或焦边时自动分析原因，输出诊断及建议（如'叶片上卷、叶缘焦枯，土壤湿度偏低，可能干旱，建议灌溉'
）。技能特点：卷叶和焦边是农民常遇到的问题，但干旱、病害、药害症状相似，易误判。通过AI视觉辅助诊断，可帮助农民早期采取正确措施，减少损失。该技能可集成到农业物联网系统、无人机巡检平台或手机APP中。

## 🎯 AI 角色

**假设你是一个专业的植物逆境诊断
AI。你的任务是分析植物叶片的图像，识别卷曲方向（上卷/下卷）、焦边分布（叶尖/叶缘、老叶/新叶），并可结合土壤湿度数据（若提供），判断引起卷叶/焦边的主要原因。不要提供具体的农药或肥料名称、剂量，仅输出基于视觉（及可选土壤湿度）的可能原因排序与方向性建议。
**

## 任务目标

- 本 Skill 用于：基于叶片高清图像（可选叠加土壤湿度等环境数据），识别卷曲方向与焦边分布特征，并给出干旱/病害/药害/肥害等原因的可能性排序
- 能力包含：卷曲方向识别（上卷 / 下卷 / 混合 / 无）、焦边分布检测（叶尖灼烧 / 叶缘焦枯 / 整叶干枯）、受害叶层定位（老叶 / 新叶 /
  顶端嫩叶 / 全株）、伴随症状识别（黄化、紫红、白粉、坏死斑、水浸状斑）、可能原因排序（干旱 / 白粉病 / 病毒病 / 药害 / 肥害 /
  冷害等）+ 置信度、方向性养护建议
- 触发条件:
    1. **默认触发**：当用户提供植物叶片图像或视频 URL/文件需要分析时，默认触发本技能进行卷叶/焦边诊断
    2. 当用户明确提及卷叶、卷曲、上卷、下卷、焦边、叶缘焦枯、叶尖灼烧、干旱胁迫、白粉病、病毒病、药害、肥害、冷害、叶片干枯等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看卷叶焦边历史报告、叶片诊断报告清单、卷叶诊断清单、查询历史卷叶焦边诊断、显示所有卷叶焦边报告、显示叶片逆境诊断报告，查询卷叶焦边建议清单
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有卷叶焦边报告"、"
       显示所有叶片诊断报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_leaf_curling_scorch_diagnosis_analysis --list` 调用 API
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
    1. **准备叶片图像输入**
        - 提供本地叶片图像/视频路径或网络 URL
        - 建议拍摄叶片整体形态（区分新叶/老叶）以及叶尖/叶缘特写，光照均匀、聚焦清晰
        - 可选附带：作物种类、土壤湿度 %、空气湿度 %、近期施药/施肥记录
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行卷叶/焦边诊断**
        - 调用 `-m scripts.smyx_leaf_curling_scorch_diagnosis_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地叶片图像或视频文件路径
            - `--url`: 网络叶片图像或视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，植物逆境诊断场景默认 `other`
            - `--list`: 显示卷叶/焦边历史诊断报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的卷叶/焦边诊断报告
        -
        包含：卷曲方向（上卷/下卷/混合/无）、焦边分布（叶尖/叶缘/整叶）、受害叶层（老叶/新叶/顶端嫩叶/全株）、可能原因排序（干旱 /
        白粉病 / 病毒病 / 药害 / 肥害 / 冷害等）及置信度、关键视觉证据描述、方向性建议（如"建议灌溉"、"建议复查近期用药"）
        - **重要提示**：仅输出基于视觉（及可选土壤湿度）的可能原因排序与方向性建议，不输出具体农药/肥料名称或剂量

## 资源索引

-
必要脚本：见 [scripts/smyx_leaf_curling_scorch_diagnosis_analysis.py](scripts/smyx_leaf_curling_scorch_diagnosis_analysis.py)(
用途：调用 API 进行植物卷叶/焦边识别（干旱/病害）诊断分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、输出字段和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 图像或 mp4/avi/mov 视频，最大 10MB；建议同时上传整体形态与叶缘特写各一张
- 诊断结果仅作为植物逆境识别参考，疑似病害严重时建议结合实地踏查或专业植保咨询
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"作物种类"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`卷叶焦边诊断报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 作物种类 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 卷叶焦边诊断报告-20260312172200001 | 番茄 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地叶片图像
python -m scripts.smyx_leaf_curling_scorch_diagnosis_analysis --input /path/to/leaf.jpg

# 分析网络叶片图像/视频
python -m scripts.smyx_leaf_curling_scorch_diagnosis_analysis --url https://example.com/leaf.jpg

# 显示历史诊断报告/卷叶焦边诊断清单（自动触发关键词：查看卷叶焦边历史报告、叶片诊断报告清单等）
python -m scripts.smyx_leaf_curling_scorch_diagnosis_analysis --list

# 输出精简报告
python -m scripts.smyx_leaf_curling_scorch_diagnosis_analysis --input leaf.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_leaf_curling_scorch_diagnosis_analysis --input leaf.jpg --output result.json
```
