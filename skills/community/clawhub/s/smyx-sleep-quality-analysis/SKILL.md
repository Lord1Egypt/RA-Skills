---
name: "sleep-quality-analysis"
description: "Identifies sleep stages including falling asleep, light sleep, deep sleep, and REM; monitors body movement, nighttime awakenings, and sleep apnea, suitable for sleep monitoring scenarios. | 睡眠质量分析技能，识别入睡、浅睡、深睡、快速眼动阶段，监测体动、夜间觉醒、睡眠呼吸暂停，适用于睡眠监测场景"
version: "1.0.2"
---

# Sleep Quality Analysis Skill | 睡眠质量分析技能

Based on advanced contactless vital sign monitoring technology and deep learning algorithms, this feature accurately
identifies and distinguishes four key sleep stages: sleep onset, light sleep (N1/N2), deep sleep (N3), and rapid eye
movement (REM). Utilizing high-sensitivity sensors or visual analysis techniques, the system captures subtle body
movements, nighttime awakenings, and respiratory rhythm changes in real-time, with a specific focus on intelligent
screening and early warning for high-risk abnormalities such as Obstructive Sleep Apnea-Hypopnea Syndrome (OSAHS).
Suitable for sleep monitoring scenarios in both home and medical settings, this feature generates professional analysis
reports covering sleep structure, respiratory health, and movement characteristics without the need for any wearable
devices, providing users with a scientific and comfortable sleep health management solution.

本功能基于先进的非接触式生命体征监测技术与深度学习算法，能够精准识别并区分入睡、浅睡（N1/N2）、深睡（N3）及快速眼动（REM）四个关键睡眠阶段。系统通过高灵敏度传感器或视觉分析技术，实时捕捉人体微细体动、夜间觉醒次数及呼吸节律变化，重点针对睡眠呼吸暂停（OSAHS）等高风险异常进行智能筛查与预警。该功能适用于家庭及医疗机构的睡眠监测场景，无需穿戴任何设备即可生成包含睡眠结构、呼吸健康及体动特征的专业分析报告，为用户提供科学、舒适的睡眠健康管理方案

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史分析报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过睡眠监测摄像头视频分析睡眠质量，识别睡眠阶段，获取结构化的睡眠质量分析报告
- 能力包含：睡眠阶段识别（入睡/浅睡/深睡/快速眼动）、体动统计、夜间觉醒次数统计、睡眠呼吸暂停识别
- 触发条件:
    1. **默认触发**：当用户提供睡眠监测视频 URL 或文件需要进行睡眠质量分析时，默认触发本技能
    2. 当用户明确需要进行睡眠质量分析，提及睡眠监测、睡眠分期、体动监测、睡眠呼吸暂停等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史分析报告、睡眠质量分析报告清单、分析报告列表、查询历史报告、显示所有分析报告、睡眠质量分析历史记录，查询睡眠质量分析分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有分析报告"、"
       显示所有睡眠质量报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.sleep_quality_analysis --list --open-id` 参数调用 API
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

**在执行睡眠质量分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、sleep123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询睡眠质量分析报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供睡眠监测摄像头视频文件路径或网络视频 URL
        - 确保摄像头固定位置，完整拍摄到人体，画面稳定
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行睡眠质量分析**
        - 调用 `-m scripts.sleep_quality_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示睡眠质量分析历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的睡眠质量分析报告
        - 包含：监测基本信息、睡眠阶段分布、体动统计、夜间觉醒、呼吸暂停预警

## 资源索引

- 必要脚本：见 [scripts/sleep_quality_analysis.py](scripts/sleep_quality_analysis.py)(用途：调用 API 进行睡眠质量分析，本地文件上传，网络
  URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- 建议视频时长不少于 30 分钟以反映完整睡眠周期
- 本技能仅作睡眠质量参考，不能替代专业睡眠监测设备和医生诊断
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析时间"、"睡眠评分"、"点击查看"四列，其中"报告名称"列使用`睡眠质量分析报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 睡眠评分 | 点击查看 |
  |----------|----------|----------|----------|
  | 睡眠质量分析报告-20260312172200001 | 2026-03-12 17:22:00 | 85 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地睡眠监测视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sleep_quality_analysis --input /path/to/sleep_monitor.mp4 --open-id openclaw-control-ui

# 分析网络睡眠监测视频，（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sleep_quality_analysis --url https://example.com/sleep_monitor.mp4 --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史睡眠质量报告（自动触发关键词：查看历史分析报告、历史报告、分析报告清单等）
python -m scripts.sleep_quality_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.sleep_quality_analysis --input video.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.sleep_quality_analysis --input video.mp4 --open-id your-open-id --output result.json
```
