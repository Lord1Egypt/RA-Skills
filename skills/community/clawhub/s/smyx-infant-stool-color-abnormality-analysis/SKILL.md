---
name: "smyx-infant-stool-color-abnormality-analysis"
description: "Using a fixed camera above the baby-changing table or a smartphone, the system captures high-resolution images of the diaper area (or the stool itself), and uses AI visual analysis to identify stool color: normal yellow / yellow-green, abnormal clay-pale (white/clay-like, suggesting biliary obstruction), bright red (lower-GI bleeding), dark red / tarry black (upper-GI bleeding), etc. When abnormal colors are detected, it outputs risk reminders and recommends parents to seek medical care. The skill helps with early detection of infant hepato-biliary disease or GI bleeding. Application scenarios: newborn families, pediatric clinics, postpartum care centers. When changing diapers, parents take a photo with the camera and the system automatically analyzes and pushes results. Skill features: abnormal infant stool color (especially clay-pale) is an early signal of severe diseases such as biliary atresia; early detection and surgery can save lives. AI auto-recognition helps parents stay alert in time and avoid delayed treatment. Can be integrated into parenting apps or smart infant-care devices, becoming a safety net for newborn families. | 通过婴儿护理台上方固定摄像头或手机拍摄尿不湿区域（或直接拍摄排泄物）的高清图像，利用AI视觉分析技术识别大便颜色，包括正常黄色/黄绿色、异常陶土色（白陶土样，提示胆道梗阻）、鲜红色（下消化道出血）、暗红色/黑色（上消化道出血）等。当检测到异常颜色时，输出风险提醒，建议家长及时就医。该技能有助于早期发现婴儿肝胆疾病或消化道出血。应用场景：新生儿家庭、儿科门诊、月子中心。家长在更换尿不湿时用摄像头拍照，系统自动分析并推送结果。技能特点：婴儿大便颜色异常（尤其是陶土色）是胆道闭锁等严重疾病的早期信号，若能早期发现并手术，可挽救生命。通过AI自动识别，可帮助家长及时警觉，避免延误病情。该技能可集成到育儿APP或智能婴儿护理设备中，成为新生儿家庭的安全保障。"
version: "1.0.0"
---

# Infant Stool Color Abnormality (Clay-Pale / Bloody) | 婴儿大便颜色识别（陶土色/血便）

Using a fixed camera above the baby-changing table or a smartphone, the system captures high-resolution images of the diaper area (or the stool itself), and uses AI visual analysis to identify stool color: normal yellow / yellow-green, abnormal clay-pale (white/clay-like, suggesting biliary obstruction), bright red (lower-GI bleeding), dark red / tarry black (upper-GI bleeding), etc. When abnormal colors are detected, it outputs risk reminders and recommends parents to seek medical care. The skill helps with early detection of infant hepato-biliary disease or GI bleeding. Application scenarios: newborn families, pediatric clinics, postpartum care centers. When changing diapers, parents take a photo with the camera and the system automatically analyzes and pushes results. Skill features: abnormal infant stool color (especially clay-pale) is an early signal of severe diseases such as biliary atresia; early detection and surgery can save lives. AI auto-recognition helps parents stay alert in time and avoid delayed treatment. Can be integrated into parenting apps or smart infant-care devices, becoming a safety net for newborn families.

通过婴儿护理台上方固定摄像头或手机拍摄尿不湿区域（或直接拍摄排泄物）的高清图像，利用AI视觉分析技术识别大便颜色，包括正常黄色/黄绿色、异常陶土色（白陶土样，提示胆道梗阻）、鲜红色（下消化道出血）、暗红色/黑色（上消化道出血）等。当检测到异常颜色时，输出风险提醒，建议家长及时就医。该技能有助于早期发现婴儿肝胆疾病或消化道出血。应用场景：新生儿家庭、儿科门诊、月子中心。家长在更换尿不湿时用摄像头拍照，系统自动分析并推送结果。技能特点：婴儿大便颜色异常（尤其是陶土色）是胆道闭锁等严重疾病的早期信号，若能早期发现并手术，可挽救生命。通过AI自动识别，可帮助家长及时警觉，避免延误病情。该技能可集成到育儿APP或智能婴儿护理设备中，成为新生儿家庭的安全保障。

## 🎯 AI 角色

**假设你是一个专业的婴儿健康筛查 AI。你的任务是分析尿不湿区域或排泄物的高清图像，检测大便颜色，区分正常与异常（陶土色、血便等）。不要提供医疗诊断或临床结论，仅输出基于视觉的颜色分类与方向性风险提示；对疑似 `clay_pale` 必须强烈建议尽快就医，警惕胆道闭锁等危及生命的疾病。**

## 任务目标

- 本 Skill 用于：基于婴儿尿不湿/排泄物高清图像，识别大便颜色类别 → 输出风险等级 + 推送家长可执行建议
- 能力包含：尿不湿/排泄物区域检测、图像质量与光照质量评分、参考色卡白平衡校正、主色提取（Lab / RGB）、颜色分类（normal_yellow / normal_yellow_green / normal_brown / clay_pale / bright_red_blood / dark_red_or_black_tarry / dark_green_thin / inconclusive）、风险等级与置信度判定、家长推送文本与建议动作（home_observe / clinic_visit_soon / urgent_hospital_visit / recapture_better_light）
- 触发条件:
    1. **默认触发**：当用户提供婴儿尿不湿/排泄物高清图像 URL 或文件需要分析时，默认触发本技能进行大便颜色识别
    2. 当用户明确提及婴儿大便颜色、陶土色、白陶土、血便、便血、柏油便、胆道闭锁、新生儿肝胆、儿科消化等关键词，并且上传了图像文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看婴儿大便颜色历史报告、陶土色/血便报告清单、婴儿大便筛查报告清单、查询历史婴儿大便记录、显示所有婴儿大便颜色报告、显示母婴健康诊断报告，查询婴儿大便异常预警清单
- 自动行为：
    1. 如果用户上传了附件或者图像文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有婴儿大便颜色报告"、"
       显示所有陶土色/血便报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_infant_stool_color_abnormality_analysis --list --open-id` 参数调用 API
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

**在执行婴儿大便颜色识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备婴儿尿不湿/排泄物高清图像输入**
        - 提供本地图像或网络 URL；建议拍摄 1-3 张不同角度高清图（单张 1-3 MB）
        - 设备建议：婴儿护理台上方固定摄像头 / 智能婴儿护理设备 / 手机后置摄像头；正上方俯拍、距离 15-40 cm
        - **光照要求**：自然白光或冷白 LED 光最佳；**严禁使用偏色光（黄光夜灯、暖光、护肤紫光等会引起严重误判）**；禁用美颜/滤镜
        - 推荐附带可见参考色卡（标准白卡）放在尿不湿旁，便于白平衡校正
        - 可选附带：宝宝出生日龄、是否母乳/配方/混合喂养、近期是否添加辅食、是否服用铁剂/铋剂
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行婴儿大便颜色识别**
        - 调用 `-m scripts.smyx_infant_stool_color_abnormality_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地婴儿尿不湿/排泄物高清图像文件路径
            - `--url`: 网络婴儿尿不湿/排泄物高清图像 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，婴儿健康筛查场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示婴儿大便颜色异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的婴儿大便颜色识别报告
        - 包含：是否检测到尿不湿/排泄物（diaper_or_stool_detected）、图像/光照质量（image_quality / light_quality_score）、色卡校准状态（color_card_calibrated）、主色（dominant_color_lab / dominant_color_rgb）、颜色分类（stool_color_class：normal_yellow / normal_yellow_green / normal_brown / clay_pale / bright_red_blood / dark_red_or_black_tarry / dark_green_thin / inconclusive）、风险等级（risk_level：safe / notice / warning / urgent / recapture）、置信度（confidence）、建议动作（recommended_action：home_observe / clinic_visit_soon / urgent_hospital_visit / recapture_better_light）、推送给家长的文本（如"检测到宝宝大便呈白陶土色，提示可能胆道异常，请立即前往儿科/小儿外科就诊"）
        - **重要提示**：仅输出基于视觉的颜色分类与方向性风险提示，**不替代** 儿科/小儿外科医生面诊；任何 `clay_pale` 即使置信度较低也务必立即就医（胆道闭锁手术黄金窗口期 ≤ 60 天）

## 资源索引

- 必要脚本：见 [scripts/smyx_infant_stool_color_abnormality_analysis.py](scripts/smyx_infant_stool_color_abnormality_analysis.py)(
  用途：调用 API 进行婴儿大便颜色识别（陶土色/血便），本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、颜色分类映射表与强制规则、错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 高清图像（建议 1-3 MB），最大 10MB
- **本工具仅作家庭/初筛参考，不能替代** 儿科 / 小儿外科 / 影像学（B 超等）检查
- 偏色光（黄光夜灯、暖白光、紫光氛围灯）、滤镜美颜会严重误判颜色，必须在自然白光或冷白光下重拍
- 黑色柏油样需排查是否近期服用铁剂/铋剂；鲜红色也可能为食用红心火龙果/红色辅食所致，需结合病史，但**仍建议就医排查**
- **任何 `clay_pale`（白陶土色）结果，无论置信度高低，均必须立即就医**；胆道闭锁手术黄金期 ≤ 60 天，延误可能造成不可逆肝损伤
- 隐私合规：婴儿尿不湿/排泄物图像涉及未成年人隐私，使用前需取得监护人明确知情同意，妥善加密保管
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"颜色分类/风险"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`婴儿大便颜色识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 颜色分类/风险 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 婴儿大便颜色识别报告-20260312172200001 | clay_pale / urgent（疑似胆道异常，立即就医） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地婴儿尿不湿/排泄物高清图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_infant_stool_color_abnormality_analysis --input /path/to/diaper.jpg --open-id your-open-id

# 分析网络婴儿尿不湿/排泄物高清图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_infant_stool_color_abnormality_analysis --url https://example.com/diaper.jpg --open-id your-open-id

# 显示历史婴儿大便颜色识别报告（自动触发关键词：查看婴儿大便颜色历史报告、陶土色/血便报告清单等）
python -m scripts.smyx_infant_stool_color_abnormality_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_infant_stool_color_abnormality_analysis --input diaper.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_infant_stool_color_abnormality_analysis --input diaper.jpg --open-id your-open-id --output result.json
```
