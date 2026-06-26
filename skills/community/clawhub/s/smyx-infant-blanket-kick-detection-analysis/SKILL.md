---
name: "smyx-infant-blanket-kick-detection-analysis"
description: "Using a night-time camera (infrared or low-light) above the crib, the system analyzes in real time the coverage of the blanket on the infant's body. It checks whether the blanket coverage is below a preset threshold (e.g., 50%) or recognizes the kicking motions that cause the blanket to slip off, then outputs an alert. The skill can interoperate with smart-home devices (e.g., automatically raising the room temperature, pushing reminders to parents' phones) to help prevent the baby from getting cold. Application scenarios: infant bedrooms, neonatal monitoring rooms. The system monitors continuously at night; when the blanket is kicked off, it automatically issues an alert and advises parents to re-cover or raise the room temperature. Skill features: night-time kicking off the blanket can lead to colds, and parents need to get up frequently to check. AI automatic monitoring relieves parents and helps keep the baby comfortable. A practical add-on feature for smart baby-monitoring products. | 通过婴儿床夜间摄像头（红外或微光），实时分析婴儿身体及被子的覆盖情况。检测被子覆盖面积是否小于预设阈值（如50%），或识别婴儿的踢腿动作导致被子滑落，输出预警信息。可联动智能家居设备（如自动调高室温、推送提醒至父母手机），预防婴儿着凉。应用场景：婴儿卧室、新生儿监护室。系统夜间持续监测，当被子大面积踢开时，自动发出预警并建议家长盖被或提高室温。技能特点：婴儿夜间踢被容易导致着凉感冒，家长需频繁起夜检查。通过AI自动监测，可减轻父母负担，保障婴儿睡眠舒适。该技能是智能婴儿监护产品的实用附加功能。"
version: "1.0.0"
---

# Infant Blanket Kick Detection | 婴幼儿踢被/蹬被识别

Using a night-time camera (infrared or low-light) above the crib, the system analyzes in real time the coverage of the blanket on the infant's body. It checks whether the blanket coverage is below a preset threshold (e.g., 50%) or recognizes the kicking motions that cause the blanket to slip off, then outputs an alert. The skill can interoperate with smart-home devices (e.g., automatically raising the room temperature, pushing reminders to parents' phones) to help prevent the baby from getting cold. Application scenarios: infant bedrooms, neonatal monitoring rooms. The system monitors continuously at night; when the blanket is kicked off, it automatically issues an alert and advises parents to re-cover or raise the room temperature. Skill features: night-time kicking off the blanket can lead to colds, and parents need to get up frequently to check. AI automatic monitoring relieves parents and helps keep the baby comfortable. A practical add-on feature for smart baby-monitoring products.

通过婴儿床夜间摄像头（红外或微光），实时分析婴儿身体及被子的覆盖情况。检测被子覆盖面积是否小于预设阈值（如50%），或识别婴儿的踢腿动作导致被子滑落，输出预警信息。可联动智能家居设备（如自动调高室温、推送提醒至父母手机），预防婴儿着凉。应用场景：婴儿卧室、新生儿监护室。系统夜间持续监测，当被子大面积踢开时，自动发出预警并建议家长盖被或提高室温。技能特点：婴儿夜间踢被容易导致着凉感冒，家长需频繁起夜检查。通过AI自动监测，可减轻父母负担，保障婴儿睡眠舒适。该技能是智能婴儿监护产品的实用附加功能。

## 🎯 AI 角色

**假设你是一个专业的婴儿睡眠安全 AI。你的任务是分析婴儿床区域的夜间视频，检测婴儿身体上被子的覆盖面积比例，识别踢被/蹬被动作。当被子覆盖面积小于预设阈值（默认 50%），或连续踢腿动作导致被子明显滑落时，输出预警。不要提供医疗建议或具体处置方案，仅输出基于视觉的被子覆盖状态与踢被事件。**

## 任务目标

- 本 Skill 用于：基于婴儿床夜间监控视频，实时评估被子覆盖比例，识别踢腿/蹬腿动作及被子滑落事件，并按阈值输出预警，预防夜间着凉
- 能力包含：婴儿目标检测、被子区域分割、覆盖比例估算（0-100%）、覆盖状态分类（full_cover / partial_cover / low_cover / no_cover）、踢腿/蹬腿动作识别、被子下滑事件检测、阈值持续判定（默认覆盖率 < 50% 且持续 ≥ 30 秒触发预警）、智能家居联动建议（如自动提高室温）
- 触发条件:
    1. **默认触发**：当用户提供婴儿床夜间监控视频 URL 或文件需要分析时，默认触发本技能进行踢被/蹬被识别
    2. 当用户明确提及婴儿踢被、蹬被、被子滑落、被子覆盖不足、夜间着凉、宝宝盖被、婴儿夜间睡眠监护等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看婴儿踢被历史报告、踢被预警报告清单、婴儿被子覆盖报告清单、查询历史踢被记录、显示所有踢被监测报告、显示婴儿夜间踢被诊断报告，查询踢被预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有婴儿踢被报告"、"
       显示所有踢被预警报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_infant_blanket_kick_detection_analysis --list --open-id` 参数调用 API
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

**在执行婴幼儿踢被/蹬被识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备婴儿床夜间监控视频输入**
        - 提供本地婴儿床夜间监控视频文件路径或网络 URL
        - 摄像头建议固定于婴儿床上方俯视拍摄，覆盖婴儿全身及周边床面；夜间启用红外/微光模式；帧率建议 ≥ 10 FPS
        - 时段建议覆盖夜间睡眠主要时段（如 20:00 - 次日 07:00）
        - 可选附带：婴儿月龄、阈值覆盖（coverage_threshold_pct / low_cover_duration_threshold_sec）、智能家居开关状态
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行婴幼儿踢被/蹬被识别**
        - 调用 `-m scripts.smyx_infant_blanket_kick_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地婴儿床夜间监控视频文件路径
            - `--url`: 网络婴儿床夜间监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，婴儿睡眠安全场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示婴幼儿踢被/蹬被识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的踢被/蹬被识别报告
        - 包含：是否检测到婴儿（infant_detected）、被子覆盖比例（blanket_coverage_pct）、覆盖状态（coverage_state：full_cover / partial_cover / low_cover / no_cover）、踢被事件列表（kick_events：时间戳 + 持续秒数）、当次覆盖不足持续秒数（low_cover_duration_sec）、预警等级（none / info / warning）、预警文本（如"宝宝被子已被踢开，建议盖被或提高室温"）、智能家居联动建议（smart_home_hint）
        - **重要提示**：仅输出基于视觉的被子覆盖状态与踢被事件，不提供医疗建议或具体处置方案

## 资源索引

- 必要脚本：见 [scripts/smyx_infant_blanket_kick_detection_analysis.py](scripts/smyx_infant_blanket_kick_detection_analysis.py)(
  用途：调用 API 进行婴幼儿踢被/蹬被识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、覆盖状态枚举、阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议俯视全身、夜视模式
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 预警结果仅作为辅助监护参考，本工具不替代成人监护；触发预警时请及时上前查看
- 隐私合规：婴儿视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"覆盖状态"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`婴儿踢被识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 覆盖状态 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 婴儿踢被识别报告-20260312172200001 | low_cover（覆盖率 35%） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地婴儿床夜间监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_infant_blanket_kick_detection_analysis --input /path/to/crib_night.mp4 --open-id your-open-id

# 分析网络婴儿床夜间监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_infant_blanket_kick_detection_analysis --url https://example.com/crib_night.mp4 --open-id your-open-id

# 显示历史踢被识别报告（自动触发关键词：查看婴儿踢被历史报告、踢被预警报告清单等）
python -m scripts.smyx_infant_blanket_kick_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_infant_blanket_kick_detection_analysis --input crib.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_infant_blanket_kick_detection_analysis --input crib.mp4 --open-id your-open-id --output result.json
```
