---
name: "focus-analysis"
description: "Real-time detection of gaze direction and facial pose to quantify states of focus, distraction, or mind-wandering. Suitable for scenarios such as classroom learning, office meetings, and driving attention monitoring. | 专注度分析技能，实时检测视线方向、面部姿态，量化专注/分心/走神状态，适用于课堂学习、办公会议、驾驶专注度监测等场景"
version: "1.0.5"
---

# Concentration Analysis Skill | 专注度分析技能

By analyzing gaze direction, head pose, and facial landmarks in real-time video, this capability quantifies attention
states such as focus, distraction, or mind-wandering. The system identifies behaviors like gaze deviation from the
screen or task area, frequent head turning, and abnormal posture, generating attention scores and trend curves. It is
applicable to scenarios such as classroom teaching, office meetings, and vehicle cockpits, helping teachers, managers,
or safety officers monitor participants' attention levels, optimize interaction strategies, or warn of potential
operational risks.

本技能通过实时分析视频中人员的视线方向、头部姿态及面部关键点，量化评估专注、分心或走神状态。系统可识别视线偏离屏幕或任务区域、头部频繁转动、姿态异常等行为，生成专注度评分与趋势曲线。适用于课堂教学、办公会议、驾驶舱等场景，帮助教师、管理者或安全员及时了解参与者注意力状态，优化互动策略或预警潜在操作风险。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史分析报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过摄像头视频分析人员专注度，识别视线方向、面部姿态，量化专注/分心/走神状态，输出结构化的专注度分析报告
- 能力包含：人脸跟踪、视线方向检测、头部姿态估计、专注度评分、分心走神统计、专注度趋势分析
- 触发条件:
    1. **默认触发**：当用户提供监控视频 URL 或文件需要进行专注度分析时，默认触发本技能
    2. 当用户明确需要进行专注度分析，提及专注度、分心、走神、课堂专注、办公专注、驾驶专注等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史分析报告、专注度分析报告清单、分析报告列表、查询历史报告、显示所有分析报告、专注度分析历史记录，查询专注度分析分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有分析报告"、"
       显示所有专注度报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.focus_analysis --list --open-id` 参数调用 API
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

**在执行专注度分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、focus123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询专注度分析报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供监控视频文件路径或网络视频 URL
        - 确保摄像头固定位置，完整拍摄到正面面部，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行专注度分析**
        - 调用 `-m scripts.focus_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--analyze-duration`: 分析视频时长，单位：分钟，默认 30
            - `--focus-threshold`: 专注度阈值，低于该分值判定为分心，默认 0.6
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--scene`: 应用场景，可选：classroom/office/driving，默认 classroom
            - `--list`: 显示专注度分析历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的专注度分析报告
        - 包含：基本信息、整体专注度评分、专注/分心时长统计、走神频次、专注度趋势变化、改善建议

## 资源索引

- 必要脚本：见 [scripts/focus_analysis.py](scripts/focus_analysis.py)(用途：调用 API 进行专注度分析，本地文件上传，网络 URL
  由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB，建议视频时长不少于 5 分钟以反映真实专注度变化
- 不同场景默认判定标准有差异，可通过参数调整阈值
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供参考，不能替代人工评估，具体改善方案请结合实际情况调整
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析时间"、"平均专注度"、"点击查看"四列，其中"报告名称"列使用`专注度分析报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 平均专注度 | 点击查看 |
  |----------|----------|------------|----------|
  | 专注度分析报告-20260312172200001 | 2026-03-12 17:22:00 | 0.85 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析课堂视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.focus_analysis --input /path/to/classroom.mp4 --scene classroom --analyze-duration 45 --open-id openclaw-control-ui

# 分析办公会议视频，设置专注度阈值（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.focus_analysis --input /path/to/meeting.mp4 --scene office --focus-threshold 0.55 --open-id openclaw-control-ui

# 分析驾驶视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.focus_analysis --input /path/to/driving.mp4 --scene driving --analyze-duration 120 --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史专注度报告（自动触发关键词：查看历史分析报告、历史报告、分析报告清单等）
python -m scripts.focus_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.focus_analysis --input video.mp4 --scene classroom --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.focus_analysis --input video.mp4 --scene classroom --open-id your-open-id --output result.json
```
