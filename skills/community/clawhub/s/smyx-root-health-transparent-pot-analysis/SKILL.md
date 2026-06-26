---
name: "smyx-root-health-transparent-pot-analysis"
description: "AI-powered plant root health analysis from transparent pots or smart seedling boxes. Uses fixed cameras to capture images/videos of plant roots, identifies root tip color (white=active, brown=aging, black=rotten), root hair density, branching structure, and detects root rot symptoms (softness, mucus, blackish-brown color). Outputs a root health score (0-100) and vitality grade (Healthy/Normal/Weak/Rotten). Helps early detection of root issues (overwatering rot, fertilizer burn, pathogen infection) and guides care adjustments. Scenarios: smart seedling boxes, transparent pots, plant factories, hydroponic systems. | 通过智能育苗箱或透明花盆的固定摄像头，拍摄植物根系图像或视频，利用AI视觉分析技术识别根尖颜色（白色为活性强、褐色为老化、黑色为腐烂）、根毛密度、根系分支情况以及是否存在根腐病（软烂、粘液、黑褐色）。综合评估根系健康评分（0-100分），输出根系活力等级（健康/一般/衰弱/腐烂）。该技能有助于及早发现根部问题（如浇水过多引起的烂根、肥害、病菌感染），指导用户调整养护措施。应用场景：智能育苗箱、透明花盆、植物工厂、水培系统。"
version: "1.0.2"
license: "MIT-0"
---

# Plant Root Health Analysis (Transparent Pot) | 植物根系健康状况（透明盆）

AI-powered plant root health analysis from transparent pots or smart seedling boxes. Uses fixed cameras to capture images/videos of plant roots, identifies root tip color (white=active, brown=aging, black=rotten), root hair density, branching structure, and detects root rot symptoms (softness, mucus, blackish-brown color). Outputs a root health score (0-100) and vitality grade (Healthy/Normal/Weak/Rotten). Helps early detection of root issues (overwatering rot, fertilizer burn, pathogen infection) and guides care adjustments. Scenarios: smart seedling boxes, transparent pots, plant factories, hydroponic systems.

通过智能育苗箱或透明花盆的固定摄像头，拍摄植物根系图像或视频，利用AI视觉分析技术识别根尖颜色（白色为活性强、褐色为老化、黑色为腐烂）、根毛密度、根系分支情况以及是否存在根腐病（软烂、粘液、黑褐色）。综合评估根系健康评分（0-100分），输出根系活力等级（健康/一般/衰弱/腐烂）。该技能有助于及早发现根部问题（如浇水过多引起的烂根、肥害、病菌感染），指导用户调整养护措施。应用场景：智能育苗箱、透明花盆、植物工厂、水培系统。

## 🎯 AI 角色

**假设你是一个专业的植物根系健康AI。你的任务是分析透明盆或育苗箱中植物根系的图像/视频，检测根尖颜色、根系分支、根毛密度以及腐烂迹象，输出根系健康评分（0-100分）及活力等级（健康/一般/衰弱/腐烂）。不要提供具体的药物使用建议，仅输出基于视觉的评估。**

## 任务目标

- 本 Skill 用于：通过透明花盆或智能育苗箱拍摄的根系图像/视频进行植物根系健康分析，输出健康评分、活力等级及养护方向建议
- 能力包含：根尖颜色识别（白色活性/褐色老化/黑色腐烂）、根毛密度评估、根系分支结构分析、根腐病迹象检测（软烂/粘液/黑褐色）、综合健康评分（0-100分）、根系活力等级评级（健康/一般/衰弱/腐烂）、养护方向建议（浇水/通风/换土/降肥）
- 触发条件:
    1. **默认触发**：当用户提供透明花盆、育苗箱或水培系统中的植物根系图像/视频需要分析时，默认触发本技能
    2. 当用户明确需要根系健康诊断时，提及烂根、根系发黑、根尖褐变、根腐病、根毛稀疏、根系老化、透明盆观察、水培根系、育苗箱根系等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史根系报告、历史根系健康报告、根系分析报告清单、显示所有根系监测报告、查询根系诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有根系报告"、"显示根系监测报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_root_health_transparent_pot_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行根系健康分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备根系图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保透明盆或育苗箱画面清晰展示植物根系，光线充足，无遮挡，能直接观察根尖颜色和根毛形态
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行根系健康分析**
        - 调用 `-m scripts.smyx_root_health_transparent_pot_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 植物类别标识，可选值：other/cat/dog，默认 other（植物场景使用 other）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示根系健康历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的根系健康分析报告
        - 包含：根尖颜色分布（白色活性 / 褐色老化 / 黑色腐烂的占比）、根毛密度评估（密集 / 中等 / 稀疏）、根系分支情况（发达 / 一般 / 稀疏）、根腐病迹象（无 / 疑似 / 明显，含软烂、粘液、黑褐色等表征）、综合健康评分（0-100 分）、根系活力等级（健康 / 一般 / 衰弱 / 腐烂）、养护方向建议（如减少浇水、增加通风、检查肥料浓度、换土换水等）
        - **重要提示**：仅输出基于视觉的客观评估，不提供具体药物或杀菌剂使用方案，必要时建议联系农艺师或植物医院

## 资源索引

- 必要脚本：见 [scripts/smyx_root_health_transparent_pot_analysis.py](scripts/smyx_root_health_transparent_pot_analysis.py)(用途：调用 API 进行根系健康分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：透明花盆或育苗箱侧面/底部摄像头需直接观察根系，避免土壤遮挡导致误判
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供养护参考，不提供具体药物使用建议；严重根腐病建议线下处理或咨询专业农艺师
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"植物类别"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`根系健康分析报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 植物类别 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 根系健康分析报告-20260522172200001 | 透明盆植物 | 2026-05-22 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地透明盆根系图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_root_health_transparent_pot_analysis --input /path/to/root_image.jpg --open-id your-open-id

# 分析网络根系图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_root_health_transparent_pot_analysis --url https://example.com/root_video.mp4 --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史根系报告（自动触发关键词：查看历史根系报告、历史报告、根系报告清单等）
python -m scripts.smyx_root_health_transparent_pot_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_root_health_transparent_pot_analysis --input root.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_root_health_transparent_pot_analysis --input root.jpg --open-id your-open-id --output result.json
```
