---
name: "smyx-gait-analysis-lameness-analysis"
description: "Triggers when a user provides a pet side-view walking video URL or file for analysis; uses AI pose estimation to track limb joint trajectories, analyzes stride length, stance phase / swing phase duration, and left-right symmetry indicators, and identifies abnormal gait such as lameness or restricted joint mobility. Helps early detection of orthopedic conditions (arthritis, hip dysplasia, ligament injury) in pets. Application: home daily health monitoring, senior pet arthritis screening, vet clinic initial assessment, post-op rehab tracking. Does NOT provide medical diagnosis — only outputs vision-based gait analysis results. | 当用户提供宠物侧面行走视频URL或文件时，触发本技能进行步态分析；利用AI姿态估计检测四肢关节点的运动轨迹，分析步幅长度、支撑相时长、摆动相时长以及左右对称性指标，识别是否存在跛行、关节活动受限等异常步态；有助于早期发现骨科疾病（关节炎、髋关节发育不良、韧带损伤）。应用场景：宠物家庭日常健康监测、老年宠物关节炎筛查、宠物医院初诊评估、术后康复效果跟踪。仅输出基于视觉的步态分析结果，不提供医疗诊断。"
version: "1.0.0"
---

# Pet Gait Analysis (Lameness / Arthritis) | 宠物步态分析（跛行/关节炎）

Triggers when a user provides a pet side-view walking video URL or file for analysis; uses AI pose estimation to track limb joint trajectories, analyzes stride length, stance phase / swing phase duration, and left-right symmetry indicators, and identifies abnormal gait such as lameness or restricted joint mobility. Helps early detection of orthopedic conditions (arthritis, hip dysplasia, ligament injury) in pets. Application: home daily health monitoring, senior pet arthritis screening, vet clinic initial assessment, post-op rehab tracking. Does NOT provide medical diagnosis — only outputs vision-based gait analysis results.

当用户提供宠物侧面行走视频URL或文件时，触发本技能进行步态分析；利用AI姿态估计检测四肢关节点的运动轨迹，分析步幅长度、支撑相时长、摆动相时长以及左右对称性指标，识别是否存在跛行、关节活动受限等异常步态；有助于早期发现骨科疾病（关节炎、髋关节发育不良、韧带损伤）。应用场景：宠物家庭日常健康监测、老年宠物关节炎筛查、宠物医院初诊评估、术后康复效果跟踪。仅输出基于视觉的步态分析结果，不提供医疗诊断。


## 🎯 AI 角色

**你是一个专业的宠物骨科健康AI。你的任务是分析宠物直线行走的侧面视频，通过检测四肢关节点的运动参数，评估步态的对称性和协调性，识别跛行或关节活动异常。不要提供医疗诊断，仅输出基于视觉的步态分析结果。**

## 任务目标

- 本 Skill 用于：通过宠物侧面行走视频进行步态分析，检测四肢关节运动参数，评估对称性并识别跛行/关节受限等异常
- 能力包含：AI姿态估计（四肢关节点检测）、步幅长度测量、支撑相/摆动相时长计算、左右对称性指标（SI）分析、跛行判定、关节活动范围评估、步态评分输出
- 触发条件:
    1. **默认触发**：当用户提供宠物行走侧面视频 URL 或文件需要做步态分析时，默认触发本技能
    2. 当用户明确需要检查步态时，提及跛行、关节炎、瘸腿、步态异常、走路姿势、髋关节、韧带损伤、老年犬走路等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史步态报告、历史步态分析、步态分析报告清单、查询跛行分析记录、显示所有步态报告、术后康复跟踪报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有步态报告"、"显示历史步态分析"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_gait_analysis_lameness_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行步态分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备行走视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 拍摄要求：侧面视角、宠物直线行走至少 3～5 步、全身入镜、地面平坦、光线充足、无遮挡
        - 建议视频帧率 ≥ 30fps 以保证关节点追踪精度
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行步态分析**
        - 调用 `-m scripts.smyx_gait_analysis_lameness_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示步态分析历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的步态分析报告
        - 包含：步态评分（0-10）、各肢步幅长度（cm）、支撑相/摆动相时长比、左右对称性指数（SI，0=完全对称）、跛行判定（无/轻微/明显/严重）、异常肢体定位（左前/右前/左后/右后）、关节活动范围评估、建议就医提示
        - **重要提示**：仅输出基于视觉的步态分析客观结果，不提供医疗诊断或治疗建议

## 资源索引

- 必要脚本：见 [scripts/smyx_gait_analysis_lameness_analysis.py](scripts/smyx_gait_analysis_lameness_analysis.py)（用途：调用 API 进行宠物步态分析，本地文件上传，网络 URL 由 API 服务自动下载）
- 配置文件：见 [scripts/config.py](scripts/config.py)（用途：配置 API 地址、默认参数和视频格式限制）
- 领域参考：见 [references/api_doc.md](references/api_doc.md)（何时读取：需要了解 API 接口详细规范和错误码时）

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议侧面视角、≥30fps、宠物直线行走 3～5 步
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 若视频角度不佳或宠物未完整行走，可能返回 "insufficient_gait_data"
- 分析结果仅作步态参考，不替代兽医骨科专业检查
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物步态分析报告-{记录id}`形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物步态分析报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物行走视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_gait_analysis_lameness_analysis --input /path/to/dog_walking.mp4 --pet-type dog --open-id your-open-id

# 分析网络宠物行走视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_gait_analysis_lameness_analysis --url https://example.com/dog_walking.mp4 --pet-type dog --open-id your-open-id

# 显示历史步态分析报告/分析报告清单列表（自动触发关键词：查看历史步态报告、步态分析清单等）
python -m scripts.smyx_gait_analysis_lameness_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_gait_analysis_lameness_analysis --input walking.mp4 --pet-type dog --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_gait_analysis_lameness_analysis --input walking.mp4 --pet-type dog --open-id your-open-id --output result.json
```
