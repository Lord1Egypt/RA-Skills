---
name: "smyx-cutting-rooting-status-detection-analysis"
description: "AI-powered non-invasive rooting-stage detection for plant cuttings in transparent containers. From smart propagation boxes or transparent cutting containers, periodically captures images of the cutting base (water roots or substrate roots visible through the transparent wall), uses AI vision to detect white root primordia (tiny white callus dots) and count/locate them, and outputs the rooting stage (No Roots / Few Primordia / Many Primordia / Well-Developed Roots). Helps propagators monitor cutting-rooting progress without disturbing the cutting and choose the optimal transplant time. Scenarios: smart propagation boxes, home cutting propagation, tissue-culture rooms, agricultural research. | 通过智能育苗箱或透明扦插容器的固定摄像头，定期拍摄枝条基部的水生根或土培根系（通过透明壁观察），利用AI视觉分析技术识别枝条基部是否出现白色凸起根点（根原基发育形成的白色小点）以及根点的数量和分布，输出生根阶段（无生根/少量根点/大量根点/根系发达）。该技能帮助育苗者在不干扰枝条的情况下，无创监测扦插生根进度，判断移栽时机。应用场景：智能育苗箱、家庭扦插繁殖、植物组培室、农业科研。"
version: "1.0.0"
---

# Cutting Rooting Status Detection (Transparent Container) | 扦插枝条生根状态（透明容器）

AI-powered non-invasive rooting-stage detection for plant cuttings in transparent containers. From smart propagation boxes or transparent cutting containers, periodically captures images of the cutting base (water roots or substrate roots visible through the transparent wall), uses AI vision to detect white root primordia (tiny white callus dots) and count/locate them, and outputs the rooting stage (No Roots / Few Primordia / Many Primordia / Well-Developed Roots). Helps propagators monitor cutting-rooting progress without disturbing the cutting and choose the optimal transplant time. Scenarios: smart propagation boxes, home cutting propagation, tissue-culture rooms, agricultural research.

通过智能育苗箱或透明扦插容器的固定摄像头，定期拍摄枝条基部的水生根或土培根系（通过透明壁观察），利用AI视觉分析技术识别枝条基部是否出现白色凸起根点（根原基发育形成的白色小点）以及根点的数量和分布，输出生根阶段（无生根/少量根点/大量根点/根系发达）。该技能帮助育苗者在不干扰枝条的情况下，无创监测扦插生根进度，判断移栽时机。应用场景：智能育苗箱、家庭扦插繁殖、植物组培室、农业科研。

## 🎯 AI 角色

**假设你是一个专业的植物繁殖 AI。你的任务是分析透明扦插容器（水培或土培）中枝条基部的图像/视频，检测白色根点（根原基或初生根）的数量和分布，输出生根阶段（无生根 / 少量根点 / 大量根点 / 根系发达）。不要提供具体的激素处理建议，仅输出基于视觉的生根评估。**

## 任务目标

- 本 Skill 用于：通过透明扦插容器拍摄的枝条基部图像/视频进行扦插生根进度监测，输出生根阶段、根点数量分布及移栽时机建议
- 能力包含：白色根点（根原基）识别与计数、根点分布评估（基部集中 / 沿茎分布 / 不均）、初生根长度粗略估算、生根阶段划分（无生根 / 少量根点 / 大量根点 / 根系发达）、移栽时机建议（继续观察 / 准备移栽 / 可立即移栽）
- 触发条件:
    1. **默认触发**：当用户提供透明扦插容器（水培瓶 / 透明育苗杯 / 水插玻璃瓶）中枝条基部的图像或视频时，默认触发本技能
    2. 当用户明确需要生根状态评估时，提及扦插、生根、根原基、根点、水插、水培生根、扦插繁殖、月季扦插、绿萝水插、移栽时机等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史扦插生根报告、历史生根报告、扦插报告清单、显示所有生根监测报告、查询扦插诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有扦插报告"、"显示生根监测报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_cutting_rooting_status_detection_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行扦插生根分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备透明容器枝条基部图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保画面清晰对准枝条基部，透明壁干净无水垢 / 苔藓 / 反光
        - 同一容器固定机位、定期采集（如每 24-48 小时一次），便于跨期对比生根进度
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行扦插生根分析**
        - 调用 `-m scripts.smyx_cutting_rooting_status_detection_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，植物场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示扦插生根历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的扦插生根分析报告
        - 包含：白色根点数量、根点分布描述、初生根粗略长度评估、生根阶段（无生根 / 少量根点 / 大量根点 / 根系发达）、移栽时机建议（如"已出现大量白色根点，建议再过 3-5 天移栽至常规基质，并保持高湿度环境以减少移栽缓苗损失"）
        - **重要提示**：仅输出基于视觉的客观评估与移栽方向建议，不提供具体生根激素（如 IBA、NAA）使用浓度方案

## 资源索引

- 必要脚本：见 [scripts/smyx_cutting_rooting_status_detection_analysis.py](scripts/smyx_cutting_rooting_status_detection_analysis.py)(用途：调用 API 进行扦插生根识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：透明容器干净无水垢、反光，背景建议深色衬底以增强白色根点对比度；自然光或柔和侧光优于强直射光
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供繁殖管理参考，不提供具体生根激素配方；多次未生根建议检查母枝状态、水质、温度等
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"植物类别"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`扦插生根状态报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 植物类别 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 扦插生根状态报告-20260523000600001 | 月季扦插 | 2026-05-23 00:06:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地透明容器扦插图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_cutting_rooting_status_detection_analysis --input /path/to/cutting_base.jpg --open-id your-open-id

# 分析网络扦插图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_cutting_rooting_status_detection_analysis --url https://example.com/cutting.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史扦插报告（自动触发关键词：查看历史扦插报告、历史报告、生根监测清单等）
python -m scripts.smyx_cutting_rooting_status_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_cutting_rooting_status_detection_analysis --input cutting.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_cutting_rooting_status_detection_analysis --input cutting.jpg --open-id your-open-id --output result.json
```
