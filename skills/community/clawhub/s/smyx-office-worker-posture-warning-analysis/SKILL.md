---
name: "smyx-office-worker-posture-warning-analysis"
description: "Using a fixed camera in the office (aimed at the workstation), the system analyzes office workers' sitting-posture video in real time, detecting continuous sitting duration, neck forward angle (head offset relative to shoulders), and back curvature (hunchback degree). | 通过办公区固定摄像头（对准工位）实时分析办公人员的坐姿视频，检测连续坐姿时间、颈部前倾角度（头部相对于肩部的偏移）、背部弯曲度（驼背程度）。当久坐时间超过预设阈值（默认1小时）且未起身活动时，输出'久坐提醒'；当颈部前倾角>20°或背部弯曲超过阈值时，输出'姿态异常提醒'。"
version: "1.0.2"
license: "MIT-0"
---

# Office Prolonged Sitting & Posture Warning | 成人久坐/姿态预警（办公室）

Using a fixed camera in the office (aimed at the workstation), the system analyzes office workers' sitting-posture video in real time, detecting continuous sitting duration, neck forward angle (head offset relative to shoulders), and back curvature (hunchback degree). When the sitting duration exceeds a preset threshold (default 1 hour) without standing up, the system outputs a 'prolonged sitting' alert; when the neck forward angle exceeds 20° or back curvature exceeds the threshold, it outputs a 'posture abnormal' alert. The skill helps prevent occupational diseases such as cervical spondylosis and lumbar muscle strain. Application scenarios: office workstations, home-office areas, public coworking spaces. The system monitors in real time and pushes alerts via PC popup, smart speaker, or mobile app (e.g., 'sitting for 1 hour, please stand up' or 'straighten your back'). Skill features: prolonged sitting and poor posture are major causes of cervical/lumbar disorders among white-collar workers. AI real-time monitoring + alerts effectively change employee habits, reduce occupational disease risks, and elevate corporate health management. Can be integrated into enterprise security cameras or health SaaS platforms as an innovative feature for employee benefits and EAP.

通过办公区固定摄像头（对准工位）实时分析办公人员的坐姿视频，检测连续坐姿时间、颈部前倾角度（头部相对于肩部的偏移）、背部弯曲度（驼背程度）。当久坐时间超过预设阈值（默认1小时）且未起身活动时，输出'久坐提醒'；当颈部前倾角>20°或背部弯曲超过阈值时，输出'姿态异常提醒'。该技能有助于预防颈椎病、腰肌劳损等办公室职业病。应用场景：办公室工位、居家办公区、公共办公空间。系统实时监测，通过PC弹窗、智能音箱或手机APP推送提醒（如'已坐1小时，请起身活动'或'请直起腰背'）。技能特点：久坐和不良坐姿是白领阶层颈椎、腰椎病高发的主要原因。通过AI自动监测并实时提醒，可有效改变员工行为习惯，降低职业病风险，提升企业健康管理水平。该技能可集成到企业安防摄像头或健康SaaS平台中，成为员工福利和EAP（员工援助计划）的创新功能。

## 🎯 AI 角色

**假设你是一个专业的职场健康管理 AI。你的任务是分析办公人员坐姿的实时视频，检测连续坐姿时长、颈部前倾角以及背部弯曲度。当久坐时间超过阈值或姿态异常时，输出健康提醒。不要提供医疗诊断或具体康复方案，仅输出基于视觉的坐姿和活动监测结果与方向性提醒。**

## 任务目标

- 本 Skill 用于：基于办公工位摄像头视频，实时监测办公人员连续坐姿时长 + 颈部前倾角 + 背部弯曲度 + 双肩偏差 + 眼-屏距离，按阈值输出久坐/姿态异常提醒
- 能力包含：办公人员检测、上半身姿态关键点估计、连续坐姿时长统计、起身次数统计、颈部前倾角估算、背部弯曲度（驼背）估算、双肩高度差、眼-屏距离估算、预警类型分类（prolonged_sitting / forward_head_posture / hunchback_posture / shoulder_asymmetry / too_close_to_screen）、PC 弹窗 / 智能音箱 / APP 提醒文本生成
- 触发条件:
    1. **默认触发**：当用户提供办公工位监控视频 URL 或文件需要分析时，默认触发本技能进行久坐/姿态预警
    2. 当用户明确提及久坐、坐姿、颈椎病、腰肌劳损、办公室健康、低头办公、驼背、屏幕距离、起身提醒、办公人员健康等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看办公人员久坐历史报告、坐姿提醒报告清单、办公健康报告清单、查询历史坐姿记录、显示所有办公久坐报告、显示职场健康诊断报告，查询职场健康预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有办公久坐报告"、"
       显示所有坐姿提醒报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_office_worker_posture_warning_analysis --list` 调用 API
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
    1. **准备办公工位监控视频输入**
        - 提供本地办公工位监控视频路径或网络 URL
        - 摄像头建议对准工位侧前方，覆盖头部、颈部、肩部及背部；帧率建议 ≥ 10 FPS，光照均匀
        - 可选附带：员工姓名、阈值覆盖（continuous_sit_threshold_min / neck_forward_threshold_deg / back_curvature_threshold_deg）
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行成人久坐/姿态预警**
        - 调用 `-m scripts.smyx_office_worker_posture_warning_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地办公工位监控视频文件路径
            - `--url`: 网络办公工位监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，职场健康管理场景默认 `other`
            - `--list`: 显示成人久坐/姿态预警历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的久坐/姿态预警报告
        - 包含：是否检测到办公人员（person_detected）、姿态参数（posture_metrics：neck_forward_angle_deg / back_curvature_deg / shoulder_drop_diff_deg / eye_to_screen_distance_cm）、连续坐姿时长（continuous_sit_duration_min）、每小时起身次数（stand_up_count_per_hour）、预警类型（warning_type：prolonged_sitting / forward_head_posture / hunchback_posture / shoulder_asymmetry / too_close_to_screen）、预警提示文本（如"已连续坐 65 分钟，请起身活动 5 分钟"、"颈部前倾 25°，请直颈调整屏幕高度"）、当次会话统计摘要（summary）
        - **重要提示**：仅输出基于视觉的坐姿与活动监测结果与方向性提醒，不提供医学诊断或具体康复方案

## 资源索引

- 必要脚本：见 [scripts/smyx_office_worker_posture_warning_analysis.py](scripts/smyx_office_worker_posture_warning_analysis.py)(
  用途：调用 API 进行成人久坐/姿态预警（办公室）分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、预警类型/阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议对准工位侧前方、覆盖上半身
- 预警结果仅作为职场健康行为引导，本工具不替代专业康复/骨科诊断；已有颈腰椎不适请就医
- 隐私合规：办公场景视频涉及个人隐私，使用前需取得员工知情同意，企业部署应遵循当地隐私法规并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"预警类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`办公久坐姿态预警报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 预警类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 办公久坐姿态预警报告-20260312172200001 | prolonged_sitting + forward_head_posture | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地办公工位视频
python -m scripts.smyx_office_worker_posture_warning_analysis --input /path/to/desk.mp4

# 分析网络办公工位视频
python -m scripts.smyx_office_worker_posture_warning_analysis --url https://example.com/desk.mp4

# 显示历史久坐/姿态预警报告（自动触发关键词：查看办公人员久坐历史报告、坐姿提醒报告清单等）
python -m scripts.smyx_office_worker_posture_warning_analysis --list

# 输出精简报告
python -m scripts.smyx_office_worker_posture_warning_analysis --input desk.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_office_worker_posture_warning_analysis --input desk.mp4 --output result.json
```
