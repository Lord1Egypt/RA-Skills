---
name: "smyx-elderly-toilet-time-abnormal-analysis"
description: "Using a camera installed at the bathroom doorway (or inside the bathroom only detecting human silhouettes, without capturing private details), the system uses human detection and entry/exit tracking to identify when an elderly person enters or leaves the toilet and calculates the continuous occupancy time. | 通过在卫生间门口（或内部仅检测人体，不采集隐私细节）安装的摄像头，利用人体检测和进出跟踪技术，识别老年人进入和离开卫生间的时刻，计算连续占用时间。当占用时间超过预设安全阈值（默认30分钟）时，输出异常预警，通知家属或护理人员及时查看，预防老年人因跌倒、突发疾病（如中风、心梗）或体力不支导致的无法自主移动等意外。"
version: "1.0.1"
license: "MIT-0"
---

# Elderly Toilet Time Abnormal Detection (>30 min) | 老年人如厕时间异常（超30分钟）识别

Using a camera installed at the bathroom doorway (or inside the bathroom only detecting human silhouettes, without capturing private details), the system uses human detection and entry/exit tracking to identify when an elderly person enters or leaves the toilet and calculates the continuous occupancy time. When occupancy exceeds a preset safety threshold (default 30 minutes), the system outputs an abnormal alert and notifies family members or caregivers to check in time, preventing accidents such as falls, sudden illness (stroke, heart attack) or exhaustion that may prevent the elderly from moving by themselves. Application scenarios: solo-living elder households, nursing homes, senior apartments. The system runs automatically; if the elderly stay in the toilet for more than 30 minutes without coming out, urgent reminders are pushed via app suggesting an on-site check. Skill features: sudden illness or falls during toileting that prevent the elderly from calling for help is a common safety risk. Automatic occupancy-time monitoring helps detect anomalies in time and gain rescue time. Can be integrated into nursing-home management systems or home-security platforms to enhance elderly safety.

通过在卫生间门口（或内部仅检测人体，不采集隐私细节）安装的摄像头，利用人体检测和进出跟踪技术，识别老年人进入和离开卫生间的时刻，计算连续占用时间。当占用时间超过预设安全阈值（默认30分钟）时，输出异常预警，通知家属或护理人员及时查看，预防老年人因跌倒、突发疾病（如中风、心梗）或体力不支导致的无法自主移动等意外。应用场景：独居老人家庭、养老院、老年公寓。系统自动监测，若老人进入卫生间超过30分钟未出，通过APP推送紧急提醒并建议上门查看。技能特点：老年人如厕时突发疾病或跌倒后无法呼救是常见安全隐患。通过自动监测停留时间，可及时发现异常，争取救援时间。该技能可集成到养老院管理系统或居家安防平台中，提升老人安全保障水平。

## 🎯 AI 角色

**假设你是一个专业的老年人安全监测 AI。你的任务是分析卫生间门口（或内部仅检测人体轮廓）固定摄像头的视频，检测老年人的进入和离开事件，计算每次在卫生间内的连续停留时间。当停留时间超过预设阈值（默认 30 分钟）时，输出异常预警。为保护隐私，系统可对画面进行模糊化处理，仅识别人体进出。不要提供医疗诊断或具体救援操作方案，仅输出基于人体进出的统计与预警结果。**

## 任务目标

- 本 Skill 用于：基于卫生间门口/内部隐私化人体监控视频，识别老人进出事件并统计连续停留时长，按阈值输出异常预警
- 能力包含：人体检测与跟踪（隐私化处理：模糊化/像素化/仅轮廓）、进入/离开事件识别、连续停留时长统计、当日如厕会话历史、阈值判定（默认 30 分钟，可覆盖）、分级预警（none / info / warning / critical）、紧急联系人通知建议
- 触发条件:
    1. **默认触发**：当用户提供卫生间门口/内部隐私化人体监控视频 URL 或文件需要分析时，默认触发本技能进行如厕停留时间监测
    2. 当用户明确提及如厕、卫生间、洗手间、马桶、老人如厕时间长、卫生间跌倒、独居老人安全、长时间未出、停留时间监测等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看如厕时间历史报告、卫生间停留报告清单、老人如厕监护报告清单、查询历史如厕异常记录、显示所有如厕监测报告、显示老人卫生间监护诊断报告，查询如厕异常预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有如厕监测报告"、"
       显示所有卫生间停留报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --list --open-id` 参数调用 API
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

**在执行老年人如厕时间异常识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备卫生间门口/内部隐私化监控视频输入**
        - 提供本地视频文件路径或网络 URL
        - 摄像头推荐安装于卫生间门口（首选）；如必须在内部，**仅检测人体轮廓**，画面建议做模糊化/像素化处理
        - 24 小时全天候采集（含红外夜视）；视频帧率建议 ≥ 10 FPS
        - 可选附带：被监护人姓名、阈值覆盖（toilet_duration_threshold_min）、紧急联系人列表
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老年人如厕时间异常识别**
        - 调用 `-m scripts.smyx_elderly_toilet_time_abnormal_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地卫生间门口/内部隐私化人体监控视频文件路径
            - `--url`: 网络卫生间门口/内部隐私化人体监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老人居家安全场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老人如厕时间异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的如厕停留监测报告
        - 包含：是否检测到人体（person_detected）、当前是否在卫生间内（is_in_toilet）、本次进入时间（enter_time）、本次停留时长（current_duration_min）、当日如厕会话历史（occupancy_history）、异常预警标志（abnormal_alert）、预警等级（none / info / warning / critical）、预警文本（如"老人已在卫生间停留 35 分钟，建议立即上门查看"）、建议通知的联系人
        - **重要提示**：仅基于人体进出与停留时长输出统计与预警，不提供医疗诊断或具体救援操作方案

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_toilet_time_abnormal_analysis.py](scripts/smyx_elderly_toilet_time_abnormal_analysis.py)(
  用途：调用 API 进行老年人如厕时间异常（超 30 分钟）识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议安装于门口或在内部启用画面模糊化
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 触发紧急预警时，请立即通过电话/上门方式人工核实，本工具仅作辅助监测
- 隐私合规：卫生间是高度敏感区域，强烈推荐安装于门口；如必须在内部，应仅检测人体轮廓并对原始画面做模糊化/像素化处理，避免采集任何隐私细节；使用前需取得被监护人或家属知情同意
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"被监护人"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`如厕时间异常监测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 被监护人 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 如厕时间异常监测报告-20260312172200001 | 独居张爷爷（停留 35 分钟） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地卫生间门口监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --input /path/to/toilet_door.mp4 --open-id your-open-id

# 分析网络卫生间门口监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --url https://example.com/toilet_door.mp4 --open-id your-open-id

# 显示历史如厕监测报告（自动触发关键词：查看如厕时间历史报告、卫生间停留报告清单等）
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --input toilet.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --input toilet.mp4 --open-id your-open-id --output result.json
```
