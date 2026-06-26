---
name: "smyx-seed-germination-rate-prediction-analysis"
description: "Triggers when a user provides a seedling tray image or video for analysis; uses AI object detection to identify emerged seedlings (cotyledons breaking through soil or fully expanded), counts germinated seeds, and compares with total sown seeds to estimate germination rate. Application scenarios: smart seedling incubators, greenhouse nursery trays, home planting pots, seed company germination tests. | 通过育苗盘上方的固定摄像头，播种后连续采集土壤表面图像，利用AI目标检测模型识别出土幼苗，计数已发芽的种子数量，并与播种总数对比估算发芽率。应用场景：智能育苗箱、温室育苗盘、家庭播种盆、种子公司发芽试验。"
version: "1.0.2"
license: "MIT-0"
---

# Seed Germination Rate Prediction Analysis | 种子发芽率早期预测

Triggers when a user provides a seedling tray image or video for analysis; uses AI object detection to identify emerged seedlings (cotyledons breaking through soil or fully expanded), counts germinated seeds, and compares with total sown seeds to estimate germination rate. Application scenarios: smart seedling incubators, greenhouse nursery trays, home planting pots, seed company germination tests.

通过育苗盘上方的固定摄像头，播种后连续采集土壤表面图像，利用AI目标检测模型识别出土幼苗，计数已发芽的种子数量，并与播种总数对比估算发芽率。应用场景：智能育苗箱、温室育苗盘、家庭播种盆、种子公司发芽试验。

## 🎯 AI 角色

**你是一个专业的种子检测AI。你的任务是分析育苗盘（或播种盆）土壤表面的高清图像，识别已出土的幼苗（子叶展开或刚刚破土），统计发芽数量，并根据输入的总播种粒数计算当前发芽率。不要提供农业建议，仅输出基于视觉的计数和发芽率估算。**

## 任务目标

- 本 Skill 用于：通过育苗盘土壤表面图像/视频进行种子发芽率早期预测分析，获取标准化的观察结果和发芽率估算
- 能力包含：图像分析、出土幼苗识别、发芽数量统计、发芽率计算（已发芽数/播种总数×100%）、发芽率趋势追踪、低发芽率预警
- 触发条件:
    1. **默认触发**：当用户提供育苗盘土壤表面图像/视频 URL 或文件需要分析时，默认触发本技能进行发芽率预测
    2. 当用户明确需要进行种子发芽率检测时，提及发芽率、出苗率、育苗盘、种子质量、发芽试验、幼苗识别等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史发芽率报告、历史育苗报告、发芽分析报告清单、发芽报告清单、查询历史发芽报告、显示所有育苗报告、显示发芽率分析报告，查询低发芽率预警报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有发芽率报告"、"显示发芽分析报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_seed_germination_rate_prediction_analysis --list` 调用 API
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
    1. **准备图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保图像清晰展示育苗盘土壤表面，光线充足，无遮挡，能辨别幼苗出土状态
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行发芽率预测分析**
        - 调用 `-m scripts.smyx_seed_germination_rate_prediction_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地育苗盘图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，固定为 other（农业场景默认）
            - `--list`: 显示发芽率视频历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的发芽率预测观察报告
        - 包含：出土幼苗计数、发芽率估算（已发芽数/播种总数×100%）、幼苗发育阶段评估（子叶破土/子叶展开/真叶出现）、发芽率趋势（对比历史数据）、低发芽率预警提示
        - **重要提示**：仅客观描述观察到的现象和计算结果，不提供农业种植建议

## 资源索引

- 必要脚本：见 [scripts/smyx_seed_germination_rate_prediction_analysis.py](scripts/smyx_seed_germination_rate_prediction_analysis.py)(用途：调用 API 进行发芽率预测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 图像/视频要求：支持 mp4/avi/mov/jpg/png 格式，最大 10MB
- 分析结果仅供种子质量参考，不提供农业种植建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"分析类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`种子发芽率分析报告-{记录id}`形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 种子发芽率分析报告-20260312172200001 | 发芽率预测 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地育苗盘图像
python -m scripts.smyx_seed_germination_rate_prediction_analysis --input /path/to/seedling_tray.jpg --pet-type other

# 分析网络育苗盘视频
python -m scripts.smyx_seed_germination_rate_prediction_analysis --url https://example.com/seedling_tray.mp4 --pet-type other

# 显示历史分析报告/显示分析报告清单列表/显示历史发芽率报告（自动触发关键词：查看历史发芽率报告、历史报告、发芽率报告清单等）
python -m scripts.smyx_seed_germination_rate_prediction_analysis --list

# 输出精简报告
python -m scripts.smyx_seed_germination_rate_prediction_analysis --input tray.jpg --pet-type other --detail basic

# 保存结果到文件
python -m scripts.smyx_seed_germination_rate_prediction_analysis --input tray.jpg --pet-type other --output result.json
```
