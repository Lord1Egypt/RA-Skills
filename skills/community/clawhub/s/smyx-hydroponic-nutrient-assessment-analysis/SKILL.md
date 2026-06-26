---
name: "smyx-hydroponic-nutrient-assessment-analysis"
description: "Using fixed cameras on a hydroponic growing rack to capture high-resolution images of plant roots (in transparent containers) and leaves (young and old), AI vision analysis identifies root color (white = healthy, yellow = early stress, brown = severe stress, black = rotting) and leaf morphology (tip burn, leaf-margin scorch, yellowing, curling) to judge whether the nutrient solution is too concentrated or too dilute, and outputs adjustment advice (dilute with fresh water or add concentrated nutrient solution). This skill lets hydroponic growers quickly assess nutrient solution status without an EC meter. Application scenarios: hydroponic growing racks, home hydroponic vegetables, plant factories, research hydroponic systems. The system periodically (e.g., weekly) captures root and leaf images, automatically analyzes them and pushes alerts (e.g., 'roots are turning yellow, leaf tips are burned, nutrient concentration may be too high, suggest adding fresh water to dilute'). Skill features: hydroponic beginners often suffer from burnt seedlings or nutrient deficiency due to wrong nutrient concentration. AI visual assessment lets users judge quickly without instruments, lowering the learning curve. Can be integrated into hydroponic racks or mobile apps to improve user experience and success rate. | 通过水培种植架的固定摄像头拍摄植物根系（透明容器）和叶片（新叶、老叶）的高清图像，利用AI视觉分析技术识别根须颜色（白色健康、黄色初期胁迫、褐色严重胁迫、黑色腐烂）、叶片形态（叶尖灼伤、叶缘焦枯、叶片黄化、卷曲）等特征，判断营养液浓度是否过浓或过稀，并输出调整建议（增加清水稀释或补充浓缩营养液）。该技能帮助水培种植者在不使用EC计的情况下，快速评估营养液状态。应用场景：水培种植架、家庭水培蔬菜、植物工厂、科研水培装置。系统定期（如每周）拍摄根部和叶部图像，自动分析并推送提醒（如'根系变黄，叶尖灼伤，营养液浓度可能过高，建议加入清水稀释'）。技能特点：水培新手常因营养液浓度不当导致烧苗或缺素。通过AI视觉评估，用户无需仪器即可快速判断，降低种植门槛。该技能可集成到水培种植架或手机APP中，提升用户体验和成功率。"
version: "1.0.0"
---

# Hydroponic Nutrient Concentration Visual Assessment | 水培植物营养液浓度视觉评估

Using fixed cameras on a hydroponic growing rack to capture high-resolution images of plant roots (in transparent
containers) and leaves (young and old), AI vision analysis identifies root color (white = healthy, yellow = early
stress, brown = severe stress, black = rotting) and leaf morphology (tip burn, leaf-margin scorch, yellowing, curling)
to judge whether the nutrient solution is too concentrated or too dilute, and outputs adjustment advice (dilute with
fresh water or add concentrated nutrient solution). This skill lets hydroponic growers quickly assess nutrient solution
status without an EC meter. Application scenarios: hydroponic growing racks, home hydroponic vegetables, plant
factories, research hydroponic systems. The system periodically (e.g., weekly) captures root and leaf images,
automatically analyzes them and pushes alerts (e.g., 'roots are turning yellow, leaf tips are burned, nutrient
concentration may be too high, suggest adding fresh water to dilute'). Skill features: hydroponic beginners often suffer
from burnt seedlings or nutrient deficiency due to wrong nutrient concentration. AI visual assessment lets users judge
quickly without instruments, lowering the learning curve. Can be integrated into hydroponic racks or mobile apps to
improve user experience and success rate.

通过水培种植架的固定摄像头拍摄植物根系（透明容器）和叶片（新叶、老叶）的高清图像，利用AI视觉分析技术识别根须颜色（白色健康、黄色初期胁迫、褐色严重胁迫、黑色腐烂）、叶片形态（叶尖灼伤、叶缘焦枯、叶片黄化、卷曲）等特征，判断营养液浓度是否过浓或过稀，并输出调整建议（增加清水稀释或补充浓缩营养液）。该技能帮助水培种植者在不使用EC计的情况下，快速评估营养液状态。应用场景：水培种植架、家庭水培蔬菜、植物工厂、科研水培装置。系统定期（如每周）拍摄根部和叶部图像，自动分析并推送提醒（如'根系变黄，叶尖灼伤，营养液浓度可能过高，建议加入清水稀释'
）。技能特点：水培新手常因营养液浓度不当导致烧苗或缺素。通过AI视觉评估，用户无需仪器即可快速判断，降低种植门槛。该技能可集成到水培种植架或手机APP中，提升用户体验和成功率。

## 🎯 AI 角色

**假设你是一个专业的水培植物营养 AI。你的任务是分析水培植物的根系图像（透明容器内）和叶片图像，识别根须颜色、根尖状态、叶片灼伤和黄化等特征，判断营养液浓度是否适宜，输出调整建议。不要提供具体的
EC 值或 ppm 数值，仅基于视觉特征给出定性结论与方向性调整建议。**

## 任务目标

- 本 Skill 用于：基于水培种植架根系（透明容器）+ 叶片高清图像，定性评估营养液浓度状态，输出调整建议
- 能力包含：根须颜色分级（健康白 / 初期胁迫黄 / 严重胁迫褐 / 腐烂黑）、根尖状态识别（饱满白尖 / 萎缩 /
  发黑）、叶片灼伤识别（叶尖灼伤 / 叶缘焦枯）、叶片黄化与卷曲识别、营养液浓度判断（适宜 / 偏浓 / 偏稀 / 严重过浓 /
  严重过稀）、调整建议（稀释 / 补充浓缩液 / 换液 / 清洗根系）
- 触发条件:
    1. **默认触发**：当用户提供水培植物根系/叶片图像或视频 URL/文件需要分析时，默认触发本技能进行营养液浓度视觉评估
    2. 当用户明确提及水培、营养液、EC、烧苗、根系发黄、根系发黑、根腐、叶尖灼伤、叶缘焦枯、水培蔬菜、种植架、营养液浓度、稀释、换液等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看水培营养液历史报告、营养液浓度评估清单、水培诊断报告清单、查询历史水培评估、显示所有水培报告、显示根系健康诊断报告，查询营养液调整建议清单
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有水培营养液报告"、"
       显示所有营养液浓度报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis --list --open-id` 参数调用
          API
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

**在执行水培营养液浓度视觉评估前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备根系/叶片图像输入**
        - 提供本地水培根系/叶片图像/视频路径或网络 URL
        - 建议分别拍摄根系（透明容器内全貌）与叶片（新叶 + 老叶），光照均匀、无水雾反光
        - 可选附带：植物名称（生菜/小番茄/绿萝等）、营养液种类、上次换液时间
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行营养液浓度视觉评估**
        - 调用 `-m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis` 处理输入（**必须在技能根目录下运行脚本
          **）
        - 参数说明:
            - `--input`: 本地水培根系/叶片图像或视频文件路径
            - `--url`: 网络水培根系/叶片图像或视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，水培植物场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示水培营养液浓度评估历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的水培营养液浓度评估报告
        - 包含：根系颜色分级（白健康 / 黄初期胁迫 / 褐严重胁迫 / 黑腐烂）、根尖状态、叶片灼伤体征（叶尖灼伤 / 叶缘焦枯 /
          黄化 / 卷曲）、营养液浓度判定（适宜 / 偏浓 / 偏稀 / 严重过浓 / 严重过稀）、调整建议（稀释 / 补充浓缩液 / 换液 /
          清洗根系等）
        - **重要提示**：仅基于视觉特征给出定性结论，不输出具体 EC / ppm 数值

## 资源索引

-
必要脚本：见 [scripts/smyx_hydroponic_nutrient_concentration_assessment_analysis.py](scripts/smyx_hydroponic_nutrient_concentration_assessment_analysis.py)(
用途：调用 API 进行水培营养液浓度视觉评估分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、输出字段和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 图像或 mp4/avi/mov 视频，最大 10MB；建议根部与叶部分别拍摄
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 评估结果仅供水培养护参考，严重过浓/严重过稀建议立即换液并观察 24 小时
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"水培作物"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`水培营养液浓度评估报告-{记录id}`形式拼接, "
  点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 水培作物 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 水培营养液浓度评估报告-20260312172200001 | 生菜 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地水培根系/叶片图像或视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis --input /path/to/hydroponic_root.jpg --open-id your-open-id

# 分析网络水培图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis --url https://example.com/hydroponic_root.jpg --open-id your-open-id

# 显示历史评估报告/营养液浓度评估清单（自动触发关键词：查看水培营养液历史报告、营养液浓度评估清单等）
python -m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis --input root.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_hydroponic_nutrient_concentration_assessment_analysis --input root.jpg --open-id your-open-id --output result.json
```
