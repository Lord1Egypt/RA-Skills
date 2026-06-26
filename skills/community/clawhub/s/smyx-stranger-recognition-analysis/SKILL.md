---
name: "stranger-recognition-analysis"
description: "Identifies strangers appearing in surveillance areas through facial comparison; supports video stream and image detection, suitable for stranger warnings in residential communities, units, access control, and other scenarios. | 陌生人识别技能，通过人脸比对识别监控区域出现的陌生人员，支持视频流和图片检测，适用于小区、单位、门禁等场景的陌生人预警"
version: "1.0.3"
license: "MIT-0"
---

# Stranger Recognition Skill | 陌生人识别技能

Based on high-precision facial recognition algorithms and feature vector comparison technology, this skill constructs an
intelligent stranger early warning mechanism for surveillance areas. The system supports dual-mode input via real-time
video stream analysis and static image detection, capable of performing millisecond-level feature matching between
captured facial information and a preset whitelist database (such as residents, employees, and regular visitors). Once
an unauthorized陌生 face is detected in scenarios like community entrances, key enterprise areas, or smart access
control points, the system immediately triggers a warning, automatically captures and stores the image, and pushes alert
information to the management terminal. This realizes a security upgrade from passive monitoring to active defense,
effectively safeguarding area security and privacy.

本技能基于高精度人脸识别算法与特征向量比对技术，构建了一套针对监控区域的智能陌生人预警机制。系统支持实时视频流分析与静态图片检测双模态输入，能够将采集到的人脸信息与预设的白名单数据库（如业主、员工、常客）进行毫秒级特征匹配。一旦在小区出入口、企事业单位重点区域或智能门禁场景中检测到未授权的陌生面孔，系统将立即触发预警，自动抓拍留存并推送告警信息至管理端，实现从被动监控到主动防御的安防升级，有效保障区域安全与隐私

## 演示案例

- [🔗 通过网路视频进行识别分析](https://www.coze.cn/s/K1Wbs5IrgAU/)
- [🔗 通过上传视频进行识别分析](https://www.coze.cn/s/RAPPmv1O2bw/)
- [🔗 显示历史分析报告](https://www.coze.cn/s/J0bDIMTBae8/)

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史识别报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过视频流/图片进行陌生人识别，比对底库中已知人脸，识别出陌生人员，输出结构化的陌生人识别报告
- 能力包含：人脸检测、人脸比对、陌生人员识别、已知人员身份确认、陌生人预警
- 触发条件:
    1. **默认触发**：当用户提供监控视频/图片 URL 或文件需要进行陌生人识别时，默认触发本技能
    2. 当用户明确需要进行陌生人识别、人脸比对、来访人员识别时，提及陌生人识别、人脸比对、陌生人员预警等关键词，并且上传了视频或图片
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史识别报告、陌生人识别报告清单、识别报告列表、查询历史报告、显示所有识别报告、陌生人识别历史记录，查询陌生人识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有识别报告"、"
       显示所有陌生人报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.stranger_recognition_analysis --list --open-id` 参数调用 API
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

**在执行陌生人识别前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、stranger123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询陌生人识别报告记录），并询问是否继续

---

- 标准流程:
    1. **准备媒体输入**
        - 提供监控视频文件路径、网络视频 URL 或人脸图片
        - 确保人脸清晰可见，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行陌生人识别**
        - 调用 `-m scripts.stranger_recognition_analysis` 处理素材（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--media-type`: 媒体类型，可选值：video/image，默认 video
            - `--threshold`: 人脸比对相似度阈值，默认 0.6，分值越高要求越严格
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--enroll`: 是否录入新人员到人脸识别底库，yes/no，默认 no
            - `--person-name`: 人员姓名，录入底库时必须提供
            - `--person-id`: 人员ID，录入底库时可选
            - `--list`: 显示陌生人识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 识别：接收结构化的陌生人识别报告，包含：已知人员识别结果、陌生人员数量、相似度评分、陌生人预警
        - 录入：接收底库录入结果反馈，确认人员信息已存入底库

## 资源索引

- 必要脚本：见 [scripts/stranger_recognition_analysis.py](scripts/stranger_recognition_analysis.py)(用途：调用 API
  进行陌生人识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和媒体格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB
- 底库数据保存在云端，同一 open-id 下的底库数据共享
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供安全管理参考，具体处置请按单位相关规定执行
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史识别报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"识别时间"、"识别结果"、"点击查看"四列，其中"报告名称"列使用`陌生人识别分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 识别时间 | 识别结果 | 点击查看 |
  |----------|----------|----------|----------|
  | 陌生人识别分析报告-20260312172200001 | 2026-03-12 17:22:00 |
  检测到1名陌生人 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 识别本地监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.stranger_recognition_analysis --input /path/to/monitor.mp4 --media-type video --open-id openclaw-control-ui

# 识别本地图片，设置 stricter 阈值（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.stranger_recognition_analysis --input /path/to/capture.jpg --media-type image --threshold 0.7 --open-id openclaw-control-ui

# 录入新人脸到人脸识别底库（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.stranger_recognition_analysis --input /path/to/zhangsan.jpg --media-type image --enroll yes --person-name "张三" --open-id openclaw-control-ui

# 显示历史识别报告/显示识别报告清单列表/显示历史陌生人报告（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.stranger_recognition_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.stranger_recognition_analysis --input video.mp4 --media-type video --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.stranger_recognition_analysis --input video.mp4 --media-type video --open-id your-open-id --output result.json
```
