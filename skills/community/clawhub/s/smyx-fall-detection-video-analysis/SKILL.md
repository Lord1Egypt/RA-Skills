---
name: "fall-detection-video-analysis"
description: "Detects whether anyone has fallen within a target area. Supports video stream analysis and is suitable for real-time safety monitoring of elderly people living alone. | 跌倒检测视频版技能，检测目标区域内是否有人跌倒，支持视频流检测，适用于独居老人居家安全监测"
version: "1.0.3"
license: "MIT-0"
---

# Video-based Fall Detection Skill | 跌倒检测视频版技能

By analyzing changes in human posture and motion trajectories within video streams, this capability detects fall events
in target areas in real-time. Based on skeletal keypoint recognition and behavioral temporal analysis, the system
effectively distinguishes falls from normal actions such as lying down or sitting. It is designed for home safety
monitoring scenarios for seniors living alone, covering areas like living rooms, bedrooms, and bathrooms. Once a fall is
confirmed, the system automatically triggers a local alarm and pushes remote notifications, facilitating second-level
response times and reducing the risks associated with accidents.

本技能通过分析视频流中人体姿态变化与运动轨迹，实时检测目标区域内是否发生人员跌倒事件。系统基于骨骼关键点识别与行为时序分析，能够有效区分跌倒与正常躺卧、坐下等动作。适用于独居老人居家安全监测场景，如客厅、卧室、卫生间等区域。一旦确认跌倒，系统将自动触发本地预警并远程推送告警信息，助力实现秒级响应，降低意外风险。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：视频流检测目标区域内是否有人跌倒，及时触发报警
- 能力包含：人形检测、跌倒行为识别、摔倒/跌倒判断、异常报警触发
- **适用场景**：独居老人居家安全监测、养老院走廊公共区域监测、行动不便人员看护
- **适用范围**（按照要求）：
    - 推荐视频长度：5秒以内
    - 条件：单人全部身体露出且无遮挡
    - 检测距离：3-5米
- 触发条件:
    1. **默认触发**：当用户提供视频需要检测老人跌倒时，默认触发本技能
    2. 当用户明确需要跌倒检测、摔倒识别时，提及跌倒检测、老人摔倒、视频跌倒检测等关键词，并且上传了视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史检测报告、跌倒检测报告清单、检测报告列表、查询历史检测、显示所有检测报告、跌倒分析报告，查询跌倒检测视频分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有检测报告"、"显示历史跌倒"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.fall_detection_video_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 检测要求（获得准确结果的前提）

为了获得准确的跌倒检测，请确保：

1. **摄像头固定位置**，覆盖目标监测区域（如客厅、走廊、卫生间）
2. **检测距离保持在 3-5 米**，目标人物全身完整出镜
3. **单人场景**，避免多人重叠遮挡，保证跌倒行为清晰可见
4. 建议视频长度在 **5秒以内**，过长视频建议分段检测

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行跌倒检测视频分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、fallvideo123、detectfall456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询检测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备监控视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保符合：5秒以内、单人全身出镜、无遮挡、3-5米距离
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行跌倒检测视频分析**
        - 调用 `-m scripts.fall_detection_video_analysis` 处理视频（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史跌倒检测视频分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的跌倒检测视频分析报告
        - 包含：视频基本信息、检测结果、是否跌倒、跌倒位置、置信度、是否需要报警

## 资源索引

- 必要脚本：见 [scripts/fall_detection_video_analysis.py](scripts/fall_detection_video_analysis.py)(用途：调用 API
  进行跌倒检测视频分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **⚠️ 重要提醒**：本检测结果仅供安全预警参考，不能替代人工确认，发现跌倒报警请立即联系家人或医护人员现场确认
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"检测结果"、"是否报警"、"检测时间"、"点击查看"五列，其中"报告名称"列使用`跌倒检测视频报告-{记录id}`形式拼接, "
  点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 检测结果 | 是否报警 | 检测时间 | 点击查看 |
  |----------|----------|----------|----------|----------|
  | 跌倒检测视频报告 -20260329003600001 | 未检测到跌倒 | 否 | 2026-03-29 00:
  36 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 检测本地监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.fall_detection_video_analysis --input /path/to/fall_detect.mp4 --open-id openclaw-control-ui

# 检测网络视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.fall_detection_video_analysis --url https://example.com/detect.mp4 --open-id openclaw-control-ui

# 显示历史检测报告/显示检测报告清单列表/显示历史跌倒检测（自动触发关键词：查看历史检测报告、历史报告、检测报告清单等）
python -m scripts.fall_detection_video_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.fall_detection_video_analysis --input fall_detect.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.fall_detection_video_analysis --input fall_detect.mp4 --open-id your-open-id --output result.json
```
