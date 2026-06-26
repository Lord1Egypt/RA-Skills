---
name: "smyx-leaf-aging-fall-prediction-analysis"
description: "Using a fixed indoor camera to continuously capture leaf images of houseplants from the same angle every day, AI vision techniques detect leaf color changes (green → yellow → brown), loss of glossiness (reduced surface reflectance), and formation of the abscission zone at the petiole base (angle change). | 通过室内绿植固定摄像头连续采集叶片图像（每天同一角度），利用AI视觉分析技术检测叶片颜色变化（从绿到黄再到褐）、光泽度下降（叶面反光减弱）、叶柄基部离层形成（角度变化）等老化进程，并基于历史图像序列的时间序列模型预测未来3-7天内叶片脱落的风险时段。系统每日生成老化报告，当预测即将落叶时推送提醒（如'富贵竹下位叶预计3天后脱落，可提前剪除以保持美观'）。"
version: "1.0.1"
license: "MIT-0"
---

# Leaf Aging Fall Prediction | 室内绿植叶片老化/脱落预测

Using a fixed indoor camera to continuously capture leaf images of houseplants from the same angle every day, AI vision techniques detect leaf color changes (green → yellow → brown), loss of glossiness (reduced surface reflectance), and formation of the abscission zone at the petiole base (angle change). Based on a time-series model over historical images, the skill predicts the risk window for leaf fall within the next 3-7 days. It helps users distinguish natural turnover from stress-induced leaf drop and adjust care in advance (raise humidity, fertilize, prune, etc.). Application scenarios: indoor potted plant care, plant rental companies, botanical garden greenhouses. The system generates a daily aging report and pushes alerts when leaf fall is imminent (e.g., 'lower leaves of lucky bamboo expected to fall in 3 days, prune in advance to keep it tidy'). Skill features: leaf aging and shedding are normal life-cycle events, but early shedding often signals environmental issues. AI fall-time prediction lets users clean up dead leaves proactively, keep plants tidy, and tune care based on predicted speed (e.g., higher humidity slows senescence). Can be integrated into smart planters or gardening apps for refined care recommendations.

通过室内绿植固定摄像头连续采集叶片图像（每天同一角度），利用AI视觉分析技术检测叶片颜色变化（从绿到黄再到褐）、光泽度下降（叶面反光减弱）、叶柄基部离层形成（角度变化）等老化进程，并基于历史图像序列的时间序列模型预测未来3-7天内叶片脱落的风险时段。该技能帮助用户提前了解植物自然更新或胁迫落叶，及时调整养护（如增加湿度、施肥、修剪等）。应用场景：室内盆栽养护、绿植租赁公司、植物园温室。系统每日生成老化报告，当预测即将落叶时推送提醒（如'富贵竹下位叶预计3天后脱落，可提前剪除以保持美观'）。技能特点：叶片老化脱落是植物正常生命周期的一部分，但过早脱落可能提示环境问题。通过AI预测脱落时间，用户可提前清理枯叶，保持美观，并根据预测速度调整养护（如增加湿度可延缓衰老）。该技能可集成到智能花盆、园艺APP中，为用户提供精细化养护建议。

## 🎯 AI 角色

**假设你是一个专业的植物衰老预测 AI。你的任务是分析室内绿植的连续日间图像（至少过去 7 天，每天固定时间拍摄），检测叶片颜色（绿→黄→褐）、光泽度、叶柄角度等指标的变化趋势，基于时间序列模型预测未来数天内即将脱落（自然老化或胁迫导致）的叶片及时间窗口。不要提供具体的化学调控方法（如具体药剂剂量），仅输出预测结果与方向性养护建议。**

## 任务目标

- 本 Skill 用于：基于室内绿植连续叶片图像序列（每日同角度），检测老化进程并预测未来 3-7 天内的脱落风险时段
- 能力包含：叶色变化趋势识别（绿→黄→褐）、叶面光泽度变化检测、叶柄基部离层角度估算、老化指数（0-100%）、脱落风险时间窗口预测、至风险叶片定位/编号、老化原因提示（自然衰老 / 缺水 / 光照不足 / 营养缺乏 / 高温胁迫等）、方向性养护建议
- 触发条件:
    1. **默认触发**：当用户提供室内绿植连续日间叶片图像/视频 URL 或文件需要分析时，默认触发本技能进行叶片老化/脱落预测
    2. 当用户明确提及叶片老化、叶子发黄、落叶预测、叶片脱落、离层、富贵竹掉叶、绿植衰老、盆栽落叶等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看叶片老化历史报告、落叶预测报告清单、叶片衰老报告清单、查询历史落叶预测、显示所有叶片老化报告、显示脱落预测诊断报告，查询养护建议清单
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有叶片老化报告"、"
       显示所有落叶预测报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_leaf_aging_fall_prediction_analysis --list --open-id` 参数调用 API
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

**在执行叶片老化/脱落预测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备叶片图像序列输入**
        - 提供本地连续日间叶片图像/视频路径或网络 URL
        - 建议至少覆盖过去 7 天、每天同一时间、同一角度拍摄，背景与光照尽量一致
        - 可选附带：植物名称/品种、放置环境（光照/湿度）、上次浇水/施肥时间
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行叶片老化/脱落预测**
        - 调用 `-m scripts.smyx_leaf_aging_fall_prediction_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地叶片图像序列/视频文件路径
            - `--url`: 网络叶片图像序列/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，植物场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示叶片老化/脱落预测历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的叶片老化/脱落预测报告
        - 包含：老化指数（0-100%）、叶色 / 光泽度 / 叶柄角度变化趋势、预测脱落时间窗口（如 "未来 3-5 天"）、至风险叶片定位（下位叶/上位叶/编号）、老化原因提示（自然衰老 / 缺水 / 光照不足 / 营养缺乏 / 高温胁迫）、方向性养护建议（如提高湿度、调整光照、修剪建议等）
        - **重要提示**：仅输出预测与方向性建议，不提供具体化学调控方法或药剂剂量

## 资源索引

- 必要脚本：见 [scripts/smyx_leaf_aging_fall_prediction_analysis.py](scripts/smyx_leaf_aging_fall_prediction_analysis.py)(
  用途：调用 API 进行叶片老化/脱落预测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、输出字段和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 图像或 mp4/avi/mov 视频，最大 10MB；建议覆盖至少 7 天的连续日间图像
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 预测结果仅供养护参考，叶片自然老化是植物正常生命周期，过早脱落才是环境/养护问题信号
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"植物种类"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`叶片老化脱落预测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 植物种类 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 叶片老化脱落预测报告-20260312172200001 | 富贵竹 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地叶片图像序列（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_leaf_aging_fall_prediction_analysis --input /path/to/leaf_sequence.mp4 --open-id your-open-id

# 分析网络叶片视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_leaf_aging_fall_prediction_analysis --url https://example.com/leaf_sequence.mp4 --open-id your-open-id

# 显示历史脱落预测报告/落叶预测报告清单（自动触发关键词：查看叶片老化历史报告、落叶预测报告清单等）
python -m scripts.smyx_leaf_aging_fall_prediction_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_leaf_aging_fall_prediction_analysis --input video.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_leaf_aging_fall_prediction_analysis --input video.mp4 --open-id your-open-id --output result.json
```
