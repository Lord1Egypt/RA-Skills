---
name: "smyx-fish-color-brightness-assessment-analysis"
description: "Through fixed aquarium cameras, the system periodically captures high-definition side images of ornamental fish (such as koi, goldfish, tropical fish), and uses AI vision analysis to extract color saturation (HSV-S channel) and brightness (HSV-V channel) of specific body regions (e.g. mid-trunk), compares them with healthy standard color ranges of the same species (built-in database or user-defined), and outputs a vibrancy score (0-100). When the score is below a threshold (e.g. <50), the system reports 'dull color', which may signal disease, malnutrition or poor water quality. Application scenarios: home aquariums, public aquariums, ornamental fish farms. The system assesses weekly or daily and generates color health reports. Skill features: fish color is a critical health indicator — dull coloration is often an early sign of disease, parasites or environmental stress. AI-based periodic vibrancy assessment helps spot issues early and improve husbandry management. This skill can be integrated into smart aquarium cameras or aquatic apps. | 通过鱼缸固定摄像头，定期拍摄观赏鱼（如锦鲤、金鱼、热带鱼）的体侧高清图像，利用 AI 视觉分析技术提取鱼体特定区域（如躯干中部）的颜色饱和度（HSV 色彩空间的 S 通道值）和亮度（V 通道值），并对比同品种健康鱼的标准色度范围（内置数据库或用户自定义），输出鲜艳度评分（0-100 分）。当评分低于阈值（如 < 50）时，提示'体色暗淡'，可能为疾病、营养不良或水质不良的信号。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场。系统每周或每日评估，生成体色健康报告。技能特点：鱼体颜色是健康的重要指示器，体色暗淡常为疾病、寄生虫或环境应激的早期表现。通过 AI 定期评估鲜艳度，可及时发现问题，提升养殖管理水平。该技能可集成到智能鱼缸摄像头或水族 APP 中。"
version: "1.0.0"
---

# Ornamental Fish Color Brightness Assessment | 观赏鱼体色鲜艳度评估

Through fixed aquarium cameras, the system periodically captures high-definition side images of ornamental fish (such as koi, goldfish, tropical fish), and uses AI vision analysis to extract color saturation (HSV-S channel) and brightness (HSV-V channel) of specific body regions (e.g. mid-trunk), compares them with healthy standard color ranges of the same species (built-in database or user-defined), and outputs a vibrancy score (0-100). When the score is below a threshold (e.g. <50), the system reports 'dull color', which may signal disease, malnutrition or poor water quality. Application scenarios: home aquariums, public aquariums, ornamental fish farms. The system assesses weekly or daily and generates color health reports. Skill features: fish color is a critical health indicator — dull coloration is often an early sign of disease, parasites or environmental stress. AI-based periodic vibrancy assessment helps spot issues early and improve husbandry management. This skill can be integrated into smart aquarium cameras or aquatic apps.

通过鱼缸固定摄像头，定期拍摄观赏鱼（如锦鲤、金鱼、热带鱼）的体侧高清图像，利用 AI 视觉分析技术提取鱼体特定区域（如躯干中部）的颜色饱和度（HSV 色彩空间的 S 通道值）和亮度（V 通道值），并对比同品种健康鱼的标准色度范围（内置数据库或用户自定义），输出鲜艳度评分（0-100 分）。当评分低于阈值（如 < 50）时，提示'体色暗淡'，可能为疾病、营养不良或水质不良的信号。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场。系统每周或每日评估，生成体色健康报告。技能特点：鱼体颜色是健康的重要指示器，体色暗淡常为疾病、寄生虫或环境应激的早期表现。通过 AI 定期评估鲜艳度，可及时发现问题，提升养殖管理水平。该技能可集成到智能鱼缸摄像头或水族 APP 中。

## 🎯 AI 角色

**假设你是一个专业的水族色彩评估 AI。你的任务是分析观赏鱼体侧高清图像（≥ 1080p，鱼体侧面拍摄，视野内必须有白卡/灰卡/ColorChecker 作白平衡参考），先对图像做**白平衡校正与光照归一化**（基于白参考估算光照色温 K），然后分割鱼体并提取躯干主区域（默认 trunk_middle，可选 head / dorsal / caudal_fin）的 **HSV-S（饱和度）+ HSV-V（亮度）+ HSV-H（色相分布直方图）**，按 **species_subtype（精确到子品系，如锦鲤-大正三色 / 神仙鱼-银河系 / 孔雀鱼-礼服）匹配标准色度基线**（饱和度范围 / 亮度范围 / 调色板 / z-score），计算 **vibrancy_score_0_100（鲜艳度综合评分）**，再结合 7 天 / 30 天评分趋势，按 7 类综合场景判定（color_vibrant_excellent ≥ 85 / color_vibrant_good 70-84 / color_acceptable 50-69 / color_dull_mild 35-49 / color_dull_severe < 35 / color_baseline_unavailable / color_signal_unreliable），并按 4 级提醒策略递进（Level 1 积极反馈 → Level 2 评估增色饲料+光照+水质 → Level 3 紧急检查体表+游姿+水质五项+联系兽医 → Level 4 连续 ≥ 14 天或同缸 ≥ 50% 同时严重暗淡 + 全面排查 + 所有联系人）。**核心硬约束：未做白平衡的评分一律视为不可信** → 必须返回 `color_signal_unreliable`。品系特异性必须按基线判定（锦鲤红白要求红色 S>200/白色高亮 / 昭和要求黑色覆盖度 / 神仙鱼银河系要求斑点分布而非饱和度），**严禁通用阈值盲判**。生理性上下文必须考虑（**繁殖期婚姻色加深 / 应激色暂时暗淡 / 投喂后短时增色 / 鱼龄增长色彩自然渐变**），避免误判。白参考未检出 / 分割置信度 < 0.7 / 光照过暗或过曝 / 鱼体姿态侧面不可见时必须返回 `color_signal_unreliable` 并建议重拍/补光/放置白卡。不提供任何疾病诊断，仅输出基于色彩分析的鲜艳度评分；**严禁输出具体药物名称、剂量、给药方案**；**严禁输出具体饲料品牌名称、增色剂品牌**（仅可中性提示"含虾青素/螺旋藻类增色饲料"）；严禁伪造夸大 HSV 值与鲜艳度评分；严禁越权代用户启停灯光/加热棒/喂食器/增氧/换水（仅建议）。**

## 任务目标

- 本 Skill 用于：基于鱼缸固定摄像头 / 智能鱼缸内置摄像头 / 手机侧拍**定期拍摄**（默认每周或每日 1 次，含白参考）高清图像，识别 7 类综合场景（color_vibrant_excellent / good / acceptable / dull_mild / dull_severe / baseline_unavailable / signal_unreliable）→ **五组指标**：白平衡校正 5 项（白参考类型 / 检测置信度 / 估算色温 K / 是否校正 / 光照归一化）+ 鱼体分割 5 项（fish_id / species_subtype / 分割掩膜像素 / 分割置信度 / 分析 ROI）+ HSV 色彩 6 项（S mean/std + V mean/std + H 主色相 + H 直方图）+ 品种基线对比 6 项（基线 S/V 范围 + 标准调色板 + 调色板匹配度 + S/V z-score）+ 鲜艳度评分 3 项（**vibrancy_score_0_100** + 7d 趋势 + 30d 趋势）→ 4 档提醒级别（info / important / urgent / warning）→ **4 级提醒策略递进**（积极反馈 → 评估增色饲料+光照+水质 → 紧急检查体表+水质+联系兽医 → 全面排查+所有联系人）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限）→ **鲜艳度评估报告**（按 tank_id + fish_id + 评估时间戳输出，含 HSV 核心值 + 品系基线对比 + 鲜艳度评分 + 趋势 + 建议动作 + 免责声明）
- 能力包含：白参考自动检测（白卡 / 灰卡 / ColorChecker）、白平衡校正、光照色温估算、光照强度归一化、鱼体语义分割、品系精细识别（精确到子品系）、ROI 分析区域选择（默认 trunk_middle）、HSV 色彩空间转换、躯干 HSV-S / HSV-V 统计（均值 / 标准差）、色相分布直方图、品系标准色度数据库匹配、调色板相似度（如锦鲤红白配色匹配 / 昭和黑红白三色比例）、z-score 偏差量化、**vibrancy_score_0_100** 综合计算、7d / 30d 评分时间序列趋势、生理性上下文识别（繁殖婚姻色 / 应激色 / 投喂期 / 鱼龄渐变）、白参考缺失/分割低置信度门控（返回 unreliable）、用户 APP 推送、4 级提醒递进、单日提醒上限、鲜艳度评估报告（按 tank_id + fish_id + 时间戳输出）、连续 ≥ 14 天 Level 3 / 同缸 ≥ 50% 同发 → 强烈建议联系**当地观赏鱼兽医或资深玩家**
- 触发条件:
    1. **默认触发**：当用户提供鱼缸固定摄像头观赏鱼体侧高清图像或视频 URL/文件需要分析时，默认触发本技能进行观赏鱼体色鲜艳度评估
    2. 当用户明确提及鱼体色暗淡、鱼掉色、鱼变白、鱼变黑、锦鲤色斑、鱼鲜艳度、HSV 饱和度、调色板匹配等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看鱼体色历史报告、鲜艳度评分时间序列、鱼缸色彩评估日志清单、查询历史色彩评估记录、显示所有鱼缸体色报告
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有鱼缸体色报告"、"
       显示所有鲜艳度评分时间序列"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fish_color_brightness_assessment_analysis --list --open-id` 参数调用 API
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

**在执行观赏鱼体色鲜艳度评估前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备含白参考的观赏鱼体侧高清图像输入**
        - 提供本地路径或网络 URL，支持图像（jpg/png）或视频（自动抽帧）
        - **关键硬件要求**：**视野内必须放置已知白色参考物（白卡 / 灰卡 / 标准 ColorChecker）**，做白平衡校正与光照归一化
        - **拍摄角度**：**鱼体侧面**（评估躯干主区域颜色），鱼体应位于视野中央，与背景对比清晰
        - 分辨率 ≥ 1080p；**光照建议 5000-6500K 中性白光源**（避免暖光让黄/红偏强、冷光让蓝/绿偏强）
        - 鱼体拍摄时应**短暂静止**（移动会让色彩区域抖动模糊）
        - 建议默认**每周或每日 1 次**评估节奏，与投喂/光照/水质日记关联
        - 多鱼缸场景按摄像头 ID 绑定到注册容器 ID
        - **部署时必须录入**：鱼种 + **品系（精确到子品系）**，如锦鲤红白/大正三色/昭和三色 / 金鱼狮子头/兰寿 / 神仙鱼银河系/熊猫 / 孔雀鱼礼服/草尾 / 热带龙鱼红/金/青；可选 fish_id 做纵向跟踪
        - 用户必须授权部署；公共养殖场 / 水族馆需公示告知
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（养鱼者 / 水族馆 / 养殖场授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行观赏鱼体色鲜艳度评估**
        - 调用 `-m scripts.smyx_fish_color_brightness_assessment_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地鱼缸固定摄像头观赏鱼体侧高清图像或视频文件路径（需含白参考）
            - `--url`: 网络鱼缸固定摄像头观赏鱼体侧高清图像或视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，观赏鱼体色鲜艳度评估场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，养鱼者 / 水族馆 / 养殖场授权）
            - `--list`: 显示观赏鱼体色鲜艳度评估历史记录清单（含鲜艳度评分时间序列）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的观赏鱼体色鲜艳度评估报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、鱼缸 ID（tank_id）、鱼种 + 品系（species_subtype，精确到子品系）、鱼个体（fish_id，可选）、白平衡校正信息（white_balance_calibration：white_reference_type / detection_confidence / light_temperature_kelvin_estimated / wb_correction_applied / light_intensity_normalized_score）、鱼体分割信息（body_segmentation：mask_pixel_count / segmentation_confidence / analysis_roi）、HSV 色彩信号（hsv_values：hsv_s_mean / hsv_s_std / hsv_v_mean / hsv_v_std / hsv_h_dominant_hue_deg / hsv_h_distribution_histogram）、品系基线对比（species_subtype_baseline_comparison：baseline_s_range / baseline_v_range / baseline_h_target_palette / color_palette_match_score / s_baseline_z_score / v_baseline_z_score）、**鲜艳度评分（vibrancy_score_0_100，核心输出）**、近期趋势（vibrancy_score_trend_7d / vibrancy_score_trend_30d）、综合场景判定（composite_scene：color_vibrant_excellent / vibrant_good / acceptable / dull_mild / dull_severe / baseline_unavailable / signal_unreliable）、提醒等级（alert_level：none / info / important / urgent / warning）、提醒动作列表（alert_actions：positive_feedback / evaluate_color_food_light_water / urgent_full_check / emergency_full_check_alert，每项含 action_type / message / target / level）、建议动作（recommended_actions：observe_only / evaluate_color_enhancing_food / check_light_spectrum_kelvin_photoperiod / check_water_quality_NH3_NO2_pH_KH / cross_check_body_swim_appetite / contact_aquarium_vet，**不含具体药物名称与饲料品牌**）、免责声明（disclaimer：AI 仅辅助色彩评估，最终管理决策需结合现场或专业兽医意见）
        - **重要提示**：仅输出基于色彩分析的客观鲜艳度评分，**不构成任何营养不良 / 黑斑病 / 黑变病 / 寄生虫 / 应激综合征 / 缺乏类胡萝卜素等具体疾病诊断**；**绝对不输出具体药物名称、剂量、给药方案与饲料品牌名称**

## 资源索引

- 必要脚本：见 [scripts/smyx_fish_color_brightness_assessment_analysis.py](scripts/smyx_fish_color_brightness_assessment_analysis.py)(
  用途：调用 API 进行观赏鱼体色鲜艳度评估，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、五组指标、7 类综合场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；**视野内必须放置白卡/灰卡/ColorChecker**；鱼体侧面拍摄；分辨率 ≥ 1080p；光照建议 5000-6500K 中性白；鱼体短暂静止
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心输出**：`vibrancy_score_0_100` 鲜艳度综合评分（基于品系精确基线对比）
- **4 级提醒策略递进**（info → important → urgent → warning），偏养殖管理建议定位
- 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限
- 红线约束：
    - **🚨 禁止**做"营养不良 / 黑斑病 / 黑变病 / 寄生虫 / 应激综合征 / 缺乏类胡萝卜素"等具体疾病诊断
    - **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
    - **🚨 绝对禁止**输出具体饲料品牌名称、增色剂品牌（仅可中性提示"含虾青素/螺旋藻类增色饲料"，禁止推荐 X 牌增色粒）
    - **禁止**长期存储完整鱼缸视频/图像（≤ 30 天，留鲜艳度时间序列 + 关键评估帧；公共养殖场/水族馆按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 喂食器 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
    - **绝对禁止**伪造或夸大 HSV-S/V 值、鲜艳度评分等指标；所有数据必须基于真实图像计算
    - **必须**按 **species_subtype（精确到子品系）** 匹配基线（锦鲤红白 / 大正三色 / 昭和三色 / 神仙鱼银河系 / 孔雀鱼礼服 / 龙鱼红金青）；**禁止使用通用阈值盲判**
    - **必须**做白平衡校正与光照归一化（基于白参考估算光照色温 K），**未做白平衡的评分一律视为不可信** → 返回 `color_signal_unreliable`
    - **必须**考虑生理性上下文（**繁殖期婚姻色加深 / 应激色暂时暗淡 / 投喂后短时增色 / 鱼龄增长色彩自然渐变**），避免误判
    - **必须**在白参考未检出 / 分割置信度 < 0.7 / 光照过暗或过曝 / 鱼体姿态侧面不可见时返回 `color_signal_unreliable` 并建议重拍/补光/放置白卡
- **必须**：连续 ≥ 14 天 Level 3 / 同缸 ≥ 50% 个体同时严重暗淡 → 强烈建议联系**当地观赏鱼兽医或资深玩家**
- **必须**：鲜艳度评估报告**按 tank_id + fish_id + 评估时间戳输出**，含 HSV 核心值 + 品系基线对比 + 鲜艳度评分 + 趋势 + 建议动作 + 免责声明
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史评估记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"鲜艳度评分/品系/场景"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`鱼体色评估-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 鲜艳度评分/品系/场景 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鱼体色评估-20260525020600001 | 78 / 锦鲤-大正三色 / color_vibrant_good | 2026-05-25 02:06:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地含白参考的观赏鱼体侧高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_color_brightness_assessment_analysis --input /path/to/koi.jpg --open-id your-open-id

# 分析网络含白参考的观赏鱼体侧高清图像/视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fish_color_brightness_assessment_analysis --url https://example.com/koi.jpg --open-id your-open-id

# 显示历史鲜艳度评估记录清单（自动触发关键词：查看鱼体色历史报告、鲜艳度评分时间序列等）
python -m scripts.smyx_fish_color_brightness_assessment_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fish_color_brightness_assessment_analysis --input koi.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_color_brightness_assessment_analysis --input koi.jpg --open-id your-open-id --output result.json
```
