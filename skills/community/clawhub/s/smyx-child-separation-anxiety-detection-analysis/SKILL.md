---
name: "smyx-child-separation-anxiety-detection-analysis"
description: "Using a fixed camera at the home entrance or kindergarten gate, the system analyzes pre-school videos and detects crying facial expressions (frowning, open-mouth crying, tearing), physical clinging actions (grabbing parent's clothes, hugging parent's leg, pulling door frame), and resistance behaviors (stepping back, lying on the ground), then comprehensively evaluates the separation-anxiety level (mild / moderate / severe). | 通过家庭或幼儿园门口固定摄像头，分析儿童上学前的视频，检测哭闹面部表情（皱眉、张嘴哭泣、流泪）、肢体抓拽动作（抓住家长衣服、抱住家长腿、拉扯门框）以及抗拒行为（后退、躺地）等，综合评估分离焦虑等级（轻度/中度/重度）。该技能可辅助家长和教师了解儿童情绪状态，及时进行安抚或心理疏导。"
version: "1.0.1"
license: "MIT-0"
---

# Child Separation Anxiety Detection (Pre-School Crying) | 儿童分离焦虑识别（上学前哭闹）

Using a fixed camera at the home entrance or kindergarten gate, the system analyzes pre-school videos and detects crying facial expressions (frowning, open-mouth crying, tearing), physical clinging actions (grabbing parent's clothes, hugging parent's leg, pulling door frame), and resistance behaviors (stepping back, lying on the ground), then comprehensively evaluates the separation-anxiety level (mild / moderate / severe). The skill helps parents and teachers understand the child's emotional state and timely provide comfort or psychological guidance. Application scenarios: home drop-off, kindergarten morning reception. Daily monitoring; when the separation-anxiety level reaches moderate or above, the system pushes reminders to parents or teachers, recommending soothing measures or adjusting the separation routine. Skill features: separation anxiety is a common kindergarten / school adaptation issue, and severe cases may affect mental health and social development. AI automatic recognition helps parents and teachers pay early attention and take intervention measures to reduce children's anxiety. Can be integrated into smart cameras or kindergarten management systems.

通过家庭或幼儿园门口固定摄像头，分析儿童上学前的视频，检测哭闹面部表情（皱眉、张嘴哭泣、流泪）、肢体抓拽动作（抓住家长衣服、抱住家长腿、拉扯门框）以及抗拒行为（后退、躺地）等，综合评估分离焦虑等级（轻度/中度/重度）。该技能可辅助家长和教师了解儿童情绪状态，及时进行安抚或心理疏导。应用场景：家庭送学场景、幼儿园晨间接待。系统每日监测，当分离焦虑等级为中度以上时，推送提醒给家长或老师，建议采取安抚措施或调整分离方式。技能特点：儿童分离焦虑是常见的入园/入学适应问题，严重的可能影响心理健康和社交发展。通过AI自动识别，可帮助家长和老师早期关注并采取干预措施，减轻儿童焦虑。该技能可集成到智能摄像头或幼儿园管理系统中。

## 🎯 AI 角色

**假设你是一个专业的儿童情绪行为分析 AI。你的任务是分析上学前儿童与家长互动区域的视频，检测儿童的哭闹表情、肢体抓拽动作及抗拒行为，评估分离焦虑等级。不要提供心理诊断或处方，仅输出基于视觉的行为分析结果与友好提醒。**

## 任务目标

- 本 Skill 用于：基于家庭门口/幼儿园门口固定摄像头视频，识别儿童在与家长分别时的哭闹/抓拽/抗拒行为 → 综合评估分离焦虑等级（mild/moderate/severe）→ 输出家长与老师的安抚建议
- 能力包含：人体检测与家长在场判定（parent_present）、哭闹面部表情评分（皱眉 + 张嘴哭泣 + 流泪综合）、肢体抓拽事件识别（抓家长衣服 / 抱腿 / 拉扯门框）、抗拒行为识别（后退 / 躺地 / 推开）、当次送别时长与峰值哭闹强度统计、是否最终完成分离判定（successful_separation）、连续多日中/重度趋势预警、面向家长/老师的友好提醒与安抚建议生成
- 触发条件:
    1. **默认触发**：当用户提供家庭门口/幼儿园门口固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行儿童分离焦虑识别
    2. 当用户明确提及儿童哭闹、入园焦虑、分离焦虑、上学哭、抱腿不放、躺地不走、幼儿园晨间接待、入学适应等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看分离焦虑历史报告、儿童入园焦虑报告清单、上学哭闹报告清单、查询历史分离焦虑事件、显示所有儿童分离焦虑报告、显示入园适应诊断报告，查询分离焦虑预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有儿童分离焦虑报告"、"
       显示所有上学哭闹报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_separation_anxiety_detection_analysis --list --open-id` 参数调用 API
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

**在执行儿童分离焦虑识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备家庭/幼儿园门口固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议覆盖儿童与家长完整送别过程（建议含分离前、分离瞬间、分离后 3 分钟）
        - 摄像头建议：家庭入户门口 / 幼儿园门口 / 晨间接待区固定摄像头，覆盖儿童与家长互动区域，**能看到儿童面部表情 + 双手 + 下肢**
        - 帧率 ≥ 10 FPS（推荐 15-30 FPS）、分辨率 ≥ 480p、光照稳定
        - 多儿童同时送学场景下需按区域跟踪，避免目标串扰；隐私敏感场景可启用人体轮廓 + 面部马赛克模式
        - 可选附带：儿童姓名、年龄、入园天数（首次入园/转园/适应期等）、阈值覆盖（mild/moderate/severe 边界）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童分离焦虑识别**
        - 调用 `-m scripts.smyx_child_separation_anxiety_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地家庭/幼儿园门口固定摄像头视频文件路径
            - `--url`: 网络家庭/幼儿园门口固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童情绪行为分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童分离焦虑识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童分离焦虑识别报告
        - 包含：是否检测到儿童（subject_detected）、是否有家长在场（parent_present）、最终是否完成分离（successful_separation）、当次行为统计（behavior_metrics：crying_face_score / grab_event_count / resistance_event_count / event_duration_sec / peak_crying_intensity）、连续中/重度天数（consecutive_moderate_severe_days）、分离焦虑等级（separation_anxiety_level：mild / moderate / severe）、提醒类型（alert_type：separation_anxiety_moderate / separation_anxiety_severe / improving / normal）、提醒级别（alert_level：info / notice / warning）、推送给家长/老师的友好文本（如"宝宝今早分离时哭泣约 4 分钟、抱腿 3 次，焦虑等级中度，建议家长今晚多陪伴或与老师沟通入园适应方案"）、建议动作（recommend_action：push_parent_notice / notify_teacher / suggest_gradual_separation / suggest_transition_object / observe_only）、家长安抚 tip（tip_for_parent）
        - **重要提示**：仅输出基于视觉的客观行为统计与友好提醒，**不提供分离焦虑障碍（Separation Anxiety Disorder）等心理诊断或处方**；若儿童哭闹影响入园 ≥ 3-4 周或伴随躯体化症状（呕吐、入睡困难等）请咨询儿童心理医生

## 资源索引

- 必要脚本：见 [scripts/smyx_child_separation_anxiety_detection_analysis.py](scripts/smyx_child_separation_anxiety_detection_analysis.py)(
  用途：调用 API 进行儿童分离焦虑识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、哭闹/抓拽/抗拒阈值与分离焦虑等级定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须能看到儿童面部 + 双手 + 下肢
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 儿童撒娇、玩耍中假哭、被风吹眼流泪等情形可能被误识别为哭闹，建议结合持续时长与抓拽/抗拒动作综合判定
- 多孩家庭、多名儿童同时送学时需按区域跟踪，避免身份混淆；幼儿园场景建议每个班级配独立摄像头
- 本工具**不替代**儿童心理医生评估；适用于辅助记录与早期觉察，重度情况请寻求专业帮助
- 隐私合规：儿童及家长面部视频涉及未成年人高度敏感隐私，使用前需取得家长明确知情同意并向幼儿园报备，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"焦虑等级/主要表现"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童分离焦虑识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 焦虑等级/主要表现 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童分离焦虑识别报告-20260312172200001 | moderate（哭泣 4min + 抱腿 3 次） | 2026-03-12 07:50:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地家庭/幼儿园门口送学视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_separation_anxiety_detection_analysis --input /path/to/dropoff.mp4 --open-id your-open-id

# 分析网络家庭/幼儿园门口送学视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_separation_anxiety_detection_analysis --url https://example.com/dropoff.mp4 --open-id your-open-id

# 显示历史儿童分离焦虑识别报告（自动触发关键词：查看分离焦虑历史报告、儿童入园焦虑报告清单等）
python -m scripts.smyx_child_separation_anxiety_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_separation_anxiety_detection_analysis --input dropoff.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_separation_anxiety_detection_analysis --input dropoff.mp4 --open-id your-open-id --output result.json
```
