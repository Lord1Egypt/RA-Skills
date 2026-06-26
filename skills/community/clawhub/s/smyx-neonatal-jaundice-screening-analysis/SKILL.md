---
name: "smyx-neonatal-jaundice-screening-analysis"
description: "Using a neonatal monitor or baby camera, the system captures high-resolution facial images of the newborn and uses AI visual analysis to detect sclera color (white in normal babies, yellow when jaundiced) and facial skin yellowness index (based on skin-color chromatic spaces, e.g., mapping the skin region to estimated clinical bilirubin levels). It outputs a jaundice-risk hint (low / medium / high risk). | 通过新生儿监护器或婴儿摄像头拍摄新生儿面部高清图像，利用AI视觉分析技术检测巩膜（眼白）的颜色（正常白色，黄疸时呈黄色）以及面部皮肤的黄染指数（基于肤色色度空间，如将皮肤区域映射到临床胆红素水平估算），输出黄疸风险提示（低风险/中风险/高风险）。该技能可辅助家长及医护人员早期发现新生儿高胆红素血症，及时就医干预。"
version: "1.0.1"
license: "MIT-0"
---

# Neonatal Jaundice Screening (Facial Skin Color) | 新生儿黄疸筛查（面部皮肤颜色）

Using a neonatal monitor or baby camera, the system captures high-resolution facial images of the newborn and uses AI visual analysis to detect sclera color (white in normal babies, yellow when jaundiced) and facial skin yellowness index (based on skin-color chromatic spaces, e.g., mapping the skin region to estimated clinical bilirubin levels). It outputs a jaundice-risk hint (low / medium / high risk). The skill assists parents and medical staff in the early detection of neonatal hyperbilirubinemia for timely medical intervention. Application scenarios: newborn families, mother-baby rooming-in, neonatology wards, postpartum care centers. The system captures and analyzes images on a daily schedule or on demand, outputting a jaundice-risk level and pushing reminders when medium or high risk is reached. Skill features: neonatal jaundice has a high incidence; if severe, it can lead to kernicterus and brain injury. AI visual pre-screening helps parents monitor changes at home and recognize signs that require medical attention. Can be integrated into smart baby monitors or maternal/infant apps, becoming a practical health assistant for newborn families.

通过新生儿监护器或婴儿摄像头拍摄新生儿面部高清图像，利用AI视觉分析技术检测巩膜（眼白）的颜色（正常白色，黄疸时呈黄色）以及面部皮肤的黄染指数（基于肤色色度空间，如将皮肤区域映射到临床胆红素水平估算），输出黄疸风险提示（低风险/中风险/高风险）。该技能可辅助家长及医护人员早期发现新生儿高胆红素血症，及时就医干预。应用场景：新生儿家庭、母婴同室、新生儿科、月子中心。系统每日定时或按需拍照分析，输出黄疸风险等级，当达到中高风险时推送提醒。技能特点：新生儿黄疸发病率高，严重时可导致核黄疸，造成脑损伤。通过AI视觉初筛，可帮助家长在家监测黄疸变化，及时识别需要就医的迹象。该技能可集成到智能婴儿监护器或母婴APP中，提升产品实用性，成为新生儿家庭的健康助手。

## 🎯 AI 角色

**假设你是一个专业的新生儿健康筛查 AI。你的任务是分析新生儿面部高清图像，检测巩膜颜色（眼白部分）和面部皮肤黄染程度，估算黄疸风险等级。不要提供医疗诊断或临床胆红素结论，仅输出基于视觉的黄疸风险初筛提示，并明确建议中高风险尽快由专业医生进行经皮/血清胆红素测定确认。**

## 任务目标

- 本 Skill 用于：基于新生儿正面面部高清图像/短视频，提取巩膜与面部皮肤的黄染特征 → 输出 4 级黄疸风险（low_risk / medium_risk / high_risk / inconclusive）并给出明确就医建议
- 能力包含：新生儿面部检测、巩膜（眼白）分割与黄染指数计算、面部皮肤 ROI 颜色分析（Lab b* / YCbCr 偏移）、可见参考色卡的白平衡校准识别、光照质量评分（low / medium / high）、估算胆红素水平（mg/dL，仅参考）、风险等级与置信度判定、家长推送文本与下一步建议（home_observe / clinic_recheck / urgent_hospital_visit / recapture_better_light）
- 触发条件:
    1. **默认触发**：当用户提供新生儿面部高清图像/短视频 URL 或文件需要分析时，默认触发本技能进行黄疸初筛
    2. 当用户明确提及新生儿黄疸、宝宝面色发黄、眼白黄、皮肤黄染、胆红素、母婴同室、新生儿科筛查、月子中心健康监测等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看新生儿黄疸历史报告、黄疸筛查报告清单、宝宝黄染指数报告清单、查询历史黄疸筛查记录、显示所有新生儿黄疸报告、显示母婴健康诊断报告，查询黄疸预警清单
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有新生儿黄疸报告"、"
       显示所有宝宝黄染指数报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_neonatal_jaundice_screening_analysis --list --open-id` 参数调用 API
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

**在执行新生儿黄疸筛查前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备新生儿面部高清图像/短视频输入**
        - 提供本地新生儿面部图像或 3-10 秒短视频路径或网络 URL
        - 设备建议：新生儿监护器 / 婴儿摄像头 / 手机后置摄像头；正面、平视、五官清晰、面部完整
        - **光照要求**：自然白光最佳；**严禁使用偏色 LED 光（黄光夜灯、暖光等会引起严重误判）**；禁用美颜/滤镜
        - 推荐附带可见参考色卡（如标准白卡）放在面颊旁，便于白平衡校正
        - 新生儿建议在喂奶或安静状态下采集；可选附带：宝宝出生日龄、是否早产、出生体重、是否光疗中
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行新生儿黄疸筛查**
        - 调用 `-m scripts.smyx_neonatal_jaundice_screening_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地新生儿面部高清图像/短视频文件路径
            - `--url`: 网络新生儿面部高清图像/短视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，新生儿健康筛查场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示新生儿黄疸筛查历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的新生儿黄疸筛查报告
        - 包含：是否检测到新生儿（infant_detected）、面部/巩膜可见性（face_visible / sclera_visible）、黄染特征（feature_metrics：sclera_yellowness_index / skin_yellowness_index / skin_color_lab_b / estimated_bilirubin_mg_dl）、光照质量评分（light_quality_score）、色卡校准状态（color_card_calibrated）、风险等级（jaundice_risk_level：low_risk / medium_risk / high_risk / inconclusive）、置信度（risk_confidence）、建议动作（recommended_action：home_observe / clinic_recheck / urgent_hospital_visit / recapture_better_light）、推送给家长的文本（如"宝宝面部黄染指数 0.62，巩膜可见明显黄色，建议尽快前往新生儿科复测胆红素"）
        - **重要提示**：仅输出基于视觉的黄疸风险初筛提示，**不替代** 经皮胆红素仪 / 血清胆红素 / 医生面诊；中高风险务必尽快就医，由专业医生评估并制定干预方案

## 资源索引

- 必要脚本：见 [scripts/smyx_neonatal_jaundice_screening_analysis.py](scripts/smyx_neonatal_jaundice_screening_analysis.py)(
  用途：调用 API 进行新生儿黄疸筛查（面部皮肤颜色），本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、黄染指数/风险分级阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 高清图像（建议 1-3 MB）或 mp4/avi/mov 3-10 秒短视频，最大 10MB
- **本工具仅作家庭/初筛参考，不能替代** 经皮胆红素仪 / 血清总胆红素（TSB）/ 新生儿科医生诊断
- 偏色光（黄光夜灯、暖白光）、滤镜美颜、皮肤化妆品/护肤油残留 会导致误判，必须在自然白光下重拍
- 黄疸进展可能很快，新生儿首周内**任何**中高风险结果建议立即就医；本工具结果连续异常时不要等待"系统提醒升级"
- 隐私合规：新生儿面部图像涉及未成年人高度敏感隐私，使用前需取得监护人明确知情同意，妥善加密保管
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"黄疸风险"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`新生儿黄疸筛查报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 黄疸风险 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 新生儿黄疸筛查报告-20260312172200001 | high_risk（皮肤黄染 0.62 / 巩膜黄染 0.45，建议就医复测） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地新生儿面部高清图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_neonatal_jaundice_screening_analysis --input /path/to/baby_face.jpg --open-id your-open-id

# 分析网络新生儿面部高清图像/短视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_neonatal_jaundice_screening_analysis --url https://example.com/baby_face.jpg --open-id your-open-id

# 显示历史新生儿黄疸筛查报告（自动触发关键词：查看新生儿黄疸历史报告、黄疸筛查报告清单等）
python -m scripts.smyx_neonatal_jaundice_screening_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_neonatal_jaundice_screening_analysis --input baby.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_neonatal_jaundice_screening_analysis --input baby.jpg --open-id your-open-id --output result.json
```
