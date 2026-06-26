---
name: "smyx-public-place-group-emotion-index-analysis"
description: "Using fixed cameras in malls, exhibition halls, scenic areas and other public places, the system analyzes facial expressions of multiple people in the scene in real time (with anonymized expression recognition only), aggregates the distribution of emotions (happy, calm, irritated, surprised, sad, fearful, etc.), and computes an overall group-emotion index (0-100; higher = more positive). | 通过商场、展览馆、景区等公共场所的固定摄像头，实时分析场景中多人的面部表情（使用匿名化表情识别），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤等）的分布比例，计算整体情绪指数（0-100，数值越高代表群体情绪越积极）。该技能可帮助运营方了解顾客满意度、优化服务布局，或用于公共安全预警（如烦躁情绪比例过高可能预示冲突风险）。"
version: "1.0.2"
license: "MIT-0"
---

# Public Place Group Emotion Index (Exhibition / Mall) | 公共场所群体情绪指数（展览/商场）

Using fixed cameras in malls, exhibition halls, scenic areas and other public places, the system analyzes facial expressions of multiple people in the scene in real time (with anonymized expression recognition only), aggregates the distribution of emotions (happy, calm, irritated, surprised, sad, fearful, etc.), and computes an overall group-emotion index (0-100; higher = more positive). This skill helps operators understand customer satisfaction, optimize service layout, or trigger public-safety warnings (e.g., a high irritation ratio may indicate conflict risk). Application scenarios: shopping malls, exhibition halls, museums, theme parks, airport waiting halls. The system periodically generates group-emotion reports to support management decisions. Skill features: understanding customer emotions enables malls to promptly adjust services (e.g., open more checkouts, improve air conditioning, optimize traffic flow) and boost satisfaction; for exhibitions, it assesses exhibit appeal; for public safety, it warns against group irritation that may escalate into conflict. AI anonymous analysis delivers valuable insights while protecting privacy and is an essential capability of smart malls and smart scenic areas. Can be integrated into existing security systems or business-analytics platforms.

通过商场、展览馆、景区等公共场所的固定摄像头，实时分析场景中多人的面部表情（使用匿名化表情识别），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤等）的分布比例，计算整体情绪指数（0-100，数值越高代表群体情绪越积极）。该技能可帮助运营方了解顾客满意度、优化服务布局，或用于公共安全预警（如烦躁情绪比例过高可能预示冲突风险）。应用场景：购物中心、展览馆、博物馆、主题公园、机场候机厅。系统定期生成群体情绪报告，辅助管理决策。技能特点：了解顾客情绪能帮助商场及时调整服务（如增加收银台、改善空调、优化动线），提升满意度；对展览馆可评估展品吸引力；对公共安全可预警群体暴躁可能引发的冲突。通过AI匿名分析，在保护隐私的前提下获取有价值的数据洞察，是智慧商场、智慧景区的重要功能。该技能可集成到现有安防系统或商业分析平台中。

## 🎯 AI 角色

**假设你是一个专业的公共场所群体情绪分析 AI。你的任务是分析固定摄像头的视频，检测画面中多个人的面部表情（匿名化处理，不识别个人身份），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤、恐惧等）的出现频率，计算整体情绪指数，并按区域输出运营优化与安全预警建议。不要识别或存储个人特征，仅输出群体层面的匿名统计。**

## 任务目标

- 本 Skill 用于：基于商场/展览馆/景区/机场/博物馆/主题公园等公共场所固定摄像头视频，匿名统计 6 类情绪分布 + 群体情绪指数（0-100）+ 按区域输出指数 → 输出运营优化建议（收银/空调/动线/展品吸引力）与公共安全预警（烦躁占比过高可能预示冲突风险）
- 能力包含：匿名人脸表情检测（**不做身份识别/比对/跟踪**）、6 类情绪分类（happy / calm / irritated / surprised / sad / fearful）、积极/消极/烦躁比例计算、人群密度估计、平均停留时长估计、区域 ROI 划分与区域级情绪指数（region_breakdown）、与上一时间窗对比、4 档情绪等级判定（positive ≥ 70 / neutral 50-69 / low 30-49 / negative < 30 或烦躁 > 25%）、最小样本保护（face_detected_count < 5 输出 insufficient_sample）、运营优化与安全预警双通道建议、区域级情绪指数热力图
- 触发条件:
    1. **默认触发**：当用户提供商场/展览馆/景区等公共场所固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行公共场所群体情绪指数分析
    2. 当用户明确提及商场顾客情绪、展品吸引力、景区满意度、群体暴躁、安全预警、智慧商场、智慧景区、客流情绪洞察等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看群体情绪历史报告、群体情绪指数报告清单、商场/展览/景区情绪报告清单、查询历史群体情绪记录、显示所有群体情绪分析报告、显示客流情绪洞察报告，查询群体情绪预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有群体情绪报告"、"
       显示所有商场/展览/景区情绪报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_public_place_group_emotion_index_analysis --list --open-id` 参数调用 API
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

**在执行公共场所群体情绪指数分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备公共场所固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议时长 ≥ 10 分钟
        - 摄像头建议：商场出入口/收银区/主动线/展厅/候机厅等高位固定摄像头，能拍到顾客**正面或斜侧脸**
        - 帧率 ≥ 5 FPS（推荐 10 FPS）、分辨率 ≥ 720p、光照稳定
        - 部署前完成区域 ROI 标定（入口 / 收银 / 展品 A 等）
        - **强匿名约束**：禁止启用人脸识别 / 人脸比对 / 身份绑定 / 跨摄像头跟踪
        - 必须以**显著标识**告知公众使用了匿名情绪分析摄像头
        - 可选附带：场所类型（mall/exhibition/scenic_area/airport/museum/theme_park/other）、区域名称、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行公共场所群体情绪指数分析**
        - 调用 `-m scripts.smyx_public_place_group_emotion_index_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地公共场所固定摄像头视频文件路径
            - `--url`: 网络公共场所固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，公共场所群体情绪分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示公共场所群体情绪指数历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的公共场所群体情绪指数报告
        - 包含：时间窗（time_window）、场所类型（place_type：mall / exhibition / scenic_area / airport / museum / theme_park / other）、检测到的人脸数（face_detected_count）、人群密度估计（crowd_density_estimate）、平均停留时长估计（dwell_time_estimate_sec）、6 类情绪分布（emotion_distribution：happy / calm / irritated / surprised / sad / fearful）、积极/消极/烦躁比例（positive_ratio / negative_ratio / irritation_ratio）、群体情绪指数（group_emotion_index：0-100）、情绪等级（emotion_level：positive / neutral / low / negative）、区域级情绪指数数组（region_breakdown：[{region_name, group_emotion_index, irritation_ratio, ...}]）、与上一时间窗变化（trend_vs_last_window：delta_pct）、提醒类型（alert_type：operation_optimize / safety_warning / improving / normal）、提醒级别（alert_level：info / notice / warning）、运营建议（operation_suggestion，如"收银区烦躁占比 32%、平均停留 4 分钟，建议增开 1 个收银台"）、安全建议（safety_suggestion，如"入口区域烦躁占比 38% 且密度偏高，建议增派 1 名安保安抚分流"）、区域情绪指数热力图（emotion_heatmap_image_url）
        - **重要提示**：仅输出基于视觉的群体情绪聚合统计与运营/安全辅助参考，**不构成对任何个体顾客的情绪诊断或行为评价**；任何针对个体的服务调整必须经过当事人本人主动反馈与同意

## 资源索引

- 必要脚本：见 [scripts/smyx_public_place_group_emotion_index_analysis.py](scripts/smyx_public_place_group_emotion_index_analysis.py)(
  用途：调用 API 进行公共场所群体情绪指数分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、6 类情绪/群体情绪指数阈值/最小样本保护/匿名红线和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：能拍到顾客正面或斜侧脸、覆盖目标区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 戴口罩、戴墨镜、低头看手机、背对摄像头等情形会显著降低可识别人脸数，建议在指标中标注 `face_detected_count` 以便解读
- 短时局部表情（如顾客接电话短暂皱眉）不应单独触发负面预警，建议使用时间窗均值
- 最小样本保护：`face_detected_count < 5` 时输出 `insufficient_sample`，**禁止**发布群体指数
- 红线约束：**禁止**人脸识别 / 人脸比对 / 身份绑定 / 跨摄像头跟踪；**禁止**长期存储顾客原始视频或人脸特征向量；**禁止**将群体情绪用于针对个体顾客的差异化定价或服务歧视
- 合规要点：部署场所必须以**显著标识**告知公众使用了匿名情绪分析摄像头，并提供咨询联系方式；数据保存期限建议 ≤ 30 天，仅保留聚合指标
- 安全预警仅作为人工值守的辅助参考，**禁止**单纯依据情绪指数自动触发警报或干预
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"情绪指数/场所/主要建议"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`群体情绪指数报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 情绪指数/场所/主要建议 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 群体情绪指数报告-20260312172200001 | 58 (neutral) / mall / 收银区烦躁 32% 建议加开收银台 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地公共场所视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_public_place_group_emotion_index_analysis --input /path/to/mall.mp4 --open-id your-open-id

# 分析网络公共场所视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_public_place_group_emotion_index_analysis --url https://example.com/mall.mp4 --open-id your-open-id

# 显示历史公共场所群体情绪指数报告（自动触发关键词：查看群体情绪历史报告、群体情绪指数报告清单等）
python -m scripts.smyx_public_place_group_emotion_index_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_public_place_group_emotion_index_analysis --input mall.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_public_place_group_emotion_index_analysis --input mall.mp4 --open-id your-open-id --output result.json
```
