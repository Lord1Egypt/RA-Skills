---
name: "child-dangerous-behavior-recognition-analysis"
description: "Detects climbing, playing with fire, touching power sources, and dangerous actions near windows, providing real-time alerts. It is suitable for child safety supervision in scenarios such as homes, kindergartens, and nurseries. | 儿童危险行为识别技能，识别攀爬、玩火、触电源、窗边危险动作并实时预警，适用于家庭、幼儿园、托儿所等场景儿童安全监护"
version: "1.0.4"
license: "MIT-0"
---

# Child Hazardous Behavior Recognition Tool | 儿童危险行为识别分析工具

This capability enables real-time recognition of hazardous actions by children—such as climbing, playing with fire,
touching electrical sources, or lingering near windows—in settings like homes, kindergartens, or nurseries. By analyzing
human skeletal keypoints and behavioral trajectories from video streams, the system instantly triggers local or remote
alerts upon detecting high-risk behaviors, prompting guardians to intervene immediately. Ideal for 24/7 safety
monitoring in indoor and semi-open areas, it effectively reduces the risk of accidental injuries and enhances
supervision efficiency.

本技能可实时识别儿童在家庭、幼儿园或托儿所等场景中的攀爬、玩火、触电源及窗边逗留等危险动作。系统通过视频流分析人体骨骼关键点与行为轨迹，一旦检测到高风险行为，立即触发本地或远程预警，提示监护人员及时干预。适用于室内及半开放区域的24小时安全监护，有效降低儿童意外伤害风险，提升监护效率。

## 演示案例

- [🔗 通过网路视频进行识别分析](https://www.coze.cn/s/sMvvU3SH91I/)
- [🔗 通过上传视频进行识别分析](https://www.coze.cn/s/UpBqceESLCg/)
- [🔗 显示历史分析报告](https://www.coze.cn/s/6ih74qbetoE/)

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史识别报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过监控视频对儿童活动进行危险行为识别，获取结构化的儿童危险行为识别报告
- 能力包含：危险动作识别、实时危险预警、危险行为频次统计
- 支持识别危险行为：攀爬、玩火、触碰电源、窗边危险动作
- 触发条件:
    1. **默认触发**：当用户提供监控视频 URL 或文件需要进行儿童危险行为识别时，默认触发本技能
    2. 当用户明确需要进行儿童安全监护、危险行为识别，提及攀爬、玩火、触电、窗边危险、儿童安全等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史识别报告、危险行为识别报告清单、识别报告列表、查询历史报告、显示所有识别报告、儿童危险行为识别历史记录，查询儿童危险行为识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有识别报告"、"
       显示所有儿童安全报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.child_dangerous_behavior_recognition_analysis --list --open-id`
          参数调用 API
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

**在执行儿童危险行为识别前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、child123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询儿童危险行为识别报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供监控视频文件路径或网络视频 URL
        - 确保摄像头固定位置，完整覆盖儿童活动区域，画面稳定
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童危险行为识别**
        - 调用 `-m scripts.child_dangerous_behavior_recognition_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--alert-threshold`: 危险行为预警阈值，高于该分值发出预警，默认 0.6
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童危险行为识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童危险行为识别报告
        - 包含：监测基本信息、各类危险行为统计、危险预警提示

## 资源索引

-

必要脚本：见 [scripts/child_dangerous_behavior_recognition_analysis.py](scripts/child_dangerous_behavior_recognition_analysis.py)(
用途：调用 API 进行儿童危险行为识别，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- 本技能仅作儿童安全监护辅助，发现危险预警请立即确认
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史识别报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"识别时间"、"危险次数"、"点击查看"四列，其中"报告名称"列使用`儿童危险行为识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 识别时间 | 危险次数 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童危险行为识别报告-20260312172200001 | 2026-03-12 17:22:00 | 2 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.child_dangerous_behavior_recognition_analysis --input /path/to/monitor.mp4 --alert-threshold 0.6 --open-id openclaw-control-ui

# 分析网络监控视频，调整预警阈值（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.child_dangerous_behavior_recognition_analysis --url https://example.com/monitor.mp4 --alert-threshold 0.5 --open-id openclaw-control-ui

# 显示历史识别报告/显示识别报告清单列表/显示历史儿童危险行为报告（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.child_dangerous_behavior_recognition_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.child_dangerous_behavior_recognition_analysis --input video.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.child_dangerous_behavior_recognition_analysis --input video.mp4 --open-id your-open-id --output result.json
```
