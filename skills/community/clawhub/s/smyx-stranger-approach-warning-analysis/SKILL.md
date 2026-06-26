---
name: "stranger-approach-warning-analysis"
description: "Detects the appearance of strangers near minors and actively issues safety reminder alerts to protect minor safety, suitable for homes, schools, childcare centers, and other scenarios. | 陌生人靠近预警技能，检测未成年人身边出现陌生人员，主动发出安全提醒预警，守护未成年人安全，适用于家庭、学校、托管场所等场景"
version: "1.0.7"
license: "MIT-0"
---

# Stranger Proximity Alert Skill | 陌生人靠近预警技能

Based on advanced facial recognition and behavior analysis algorithms, this feature is specifically designed for the
safety protection of minors. The system utilizes cameras to monitor areas frequented by minors in real-time. It
immediately triggers a multi-level warning mechanism when it detects strangers approaching or loitering for extended
periods. Supporting customizable safety zones and personnel whitelists, the system accurately distinguishes between
authorized individuals—such as parents and teachers—and unknown visitors. Alert notifications are sent in real-time to
guardians' devices via APP push notifications and SMS, while also supporting on-site voice alerts. Suitable for
scenarios including homes, schools, and care institutions, this feature builds a 24/7 safety network for minors.

本功能基于先进的人脸识别与行为分析算法，专为未成年人安全守护设计。系统通过摄像头实时监测未成年人活动区域，当识别到陌生人员靠近或长时间滞留时，立即触发多级预警机制。支持自定义安全区域与人员白名单，可精准区分家长、老师等授权人员与陌生访客。预警信息将通过APP推送、短信等方式实时发送至监护人终端，同时支持现场语音提醒，适用于家庭、学校、托管机构等场景，为未成年人构建全天候的安全防护网。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过监控视频/图片分析，检测未成年人身边是否出现陌生人员，主动发出安全提醒预警
- 能力包含：目标检测、人员识别、陌生人判定、风险等级评估、安全预警提醒
- 触发条件:
    1. **默认触发**：当用户提供监控视频 URL 或本地视频/图片文件需要检测陌生人靠近时，默认触发本技能
    2. 当用户明确需要进行陌生人检测、安全预警时，提及陌生人靠近、未成年人安全、陌生人员预警、入侵检测等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史预警报告、历史陌生人检测、预警报告清单、预警报告列表、查询历史预警报告、显示所有预警报告、陌生人检测报告，查询陌生人靠近预警分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有预警报告"、"显示所有预警报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.stranger_approach_warning_analysis --list`
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
    1. **准备视频/图片输入**
        - 提供本地视频/图片文件路径或网络 URL
        - 确保监控画面清晰，覆盖未成年人活动区域
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行陌生人靠近预警分析**
        - 调用 `-m scripts.stranger_approach_warning_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--list`: 显示历史陌生人靠近预警分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的陌生人靠近预警分析报告
        - 包含：监控基本信息、未成年人检测结果、陌生人检测情况、人员数量、风险等级、安全预警建议

## 资源索引

- 必要脚本：见 [scripts/stranger_approach_warning_analysis.py](scripts/stranger_approach_warning_analysis.py)(用途：调用
  API 进行陌生人靠近预警分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov/jpg/jpeg/png，最大 10MB
- 分析结果仅供安全参考，不能替代专业安保措施，紧急情况请及时报警
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"输入类型"、"分析时间"、"风险等级"、"点击查看"五列，其中"报告名称"列使用`陌生人靠近预警分析报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 输入类型 | 分析时间 | 风险等级 | 点击查看 |
  |----------|----------|----------|----------|----------|
  | 陌生人靠近预警分析报告 -20260328221000001 | 视频 | 2026-03-28 22:10:00 |
  低风险 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地视频
python -m scripts.stranger_approach_warning_analysis --input /path/to/monitor.mp4 分析网络视频
python -m scripts.stranger_approach_warning_analysis --url https://example.com/monitor.mp4 分析监控图片
python -m scripts.stranger_approach_warning_analysis --input /path/to/capture.jpg 显示历史分析报告/显示分析报告清单列表/显示历史预警报告（自动触发关键词：查看历史预警报告、历史报告、预警报告清单等）
python -m scripts.stranger_approach_warning_analysis --list

# 输出精简报告
python -m scripts.stranger_approach_warning_analysis --input monitor.mp4 --detail basic

# 保存结果到文件
python -m scripts.stranger_approach_warning_analysis --input monitor.mp4 --output result.json
```
