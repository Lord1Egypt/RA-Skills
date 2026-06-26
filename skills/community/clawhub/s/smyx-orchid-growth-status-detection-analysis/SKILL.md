---
name: "smyx-orchid-growth-status-detection-analysis"
description: "AI-powered orchid growth-status detection from HD images (including roots visible through transparent pots) via orchid cameras or smartphones. Measures new-shoot count, flower-spike length, and root color/condition (white = healthy, brown = aged, black = rotten) to deliver a holistic vitality assessment (vigorous / normal / weak) plus care guidance such as 'three new shoots, healthy roots, increase phosphorus-potassium to promote spike growth'. Helps orchid hobbyists pinpoint repotting and feeding timing. Scenarios: home orchid care, orchid greenhouses, horticulture studios. | 通过兰花栽培专用摄像头或手机拍摄的高清图像（包括透明兰盆内的根系），利用AI视觉分析技术检测兰花新芽萌发数量、花梗（花箭）生长长度以及根系颜色（白色健康、褐色老化、黑色腐烂），综合输出兰花的生长状态评估（旺盛/正常/衰弱）及养护建议（如\"新芽萌发3个，根系健康，可适当增加磷钾肥促进花梗生长\"）。有助于兰花爱好者精准掌握植株生长节奏，及时调整水肥管理。应用场景：兰花家庭养护、兰花大棚、兰花园艺工作室。"
version: "1.0.0"
---

# Orchid Growth Status Detection (Shoots / Spike / Roots) | 兰花新芽/花梗/根系状态识别

AI-powered orchid growth-status detection from HD images (including roots visible through transparent pots) via orchid cameras or smartphones. Measures new-shoot count, flower-spike length, and root color/condition (white = healthy, brown = aged, black = rotten) to deliver a holistic vitality assessment (vigorous / normal / weak) plus care guidance such as 'three new shoots, healthy roots, increase phosphorus-potassium to promote spike growth'. Helps orchid hobbyists pinpoint repotting and feeding timing. Scenarios: home orchid care, orchid greenhouses, horticulture studios.

通过兰花栽培专用摄像头或手机拍摄的高清图像（包括透明兰盆内的根系），利用AI视觉分析技术检测兰花新芽萌发数量、花梗（花箭）生长长度以及根系颜色（白色健康、褐色老化、黑色腐烂），综合输出兰花的生长状态评估（旺盛/正常/衰弱）及养护建议（如"新芽萌发3个，根系健康，可适当增加磷钾肥促进花梗生长"）。有助于兰花爱好者精准掌握植株生长节奏，及时调整水肥管理。应用场景：兰花家庭养护、兰花大棚、兰花园艺工作室。

## 🎯 AI 角色

**假设你是一个专业的兰花栽培AI。你的任务是分析兰花的整体图像（包括假鳞茎、叶片、花梗）以及透明盆内的根系图像，检测新芽萌发数量、花梗长度、根系颜色和状态，综合评估兰花当前生长活力。不要提供具体的施肥或用药剂量，仅输出基于视觉的生长状态指标。**

## 任务目标

- 本 Skill 用于：通过兰花植株图像及透明盆内根系图像，检测新芽/花梗/根系三大核心指标，综合评估生长活力
- 能力包含：新芽萌发数量统计、花梗（花箭）长度评估、根系颜色识别（白/绿/褐/黑）、根系健康度评估、生长活力综合评级（旺盛/正常/衰弱）、养护方向参考
- 触发条件:
    1. **默认触发**：当用户提供兰花植株或根系图像/视频需要分析时，默认触发本技能进行生长状态识别
    2. 当用户明确需要兰花生长状态检测时，提及兰花新芽、花箭、花梗、兰花根、根系颜色、兰花换盆、兰花施肥等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史兰花报告、历史兰花状态报告、兰花报告清单、显示所有兰花报告、查询兰花生长记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有兰花报告"、"显示兰花状态报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_orchid_growth_status_detection_analysis --list --open-id` 参数调用 API
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

**在执行兰花生长状态识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备图像/视频输入**
        - 提供本地兰花图像/视频文件路径或网络 URL
        - 拍摄建议：
          - **建议拍摄两张**：植株整体（看新芽/花梗）+ 透明盆侧面（看根系）
          - 高清近景，光线充足均匀
          - 透明盆拍摄根系时贴近盆壁
          - 固定角度定期拍摄，便于跟踪生长变化
        - 支持图像（jpg/png）和视频（mp4/avi/mov）格式
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行生长状态识别**
        - 调用 `-m scripts.smyx_orchid_growth_status_detection_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地兰花图像/视频文件路径
            - `--url`: 网络兰花图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 对象类型，植物场景默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示兰花生长状态识别历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看识别结果**
        - 接收结构化的兰花生长状态报告
        - 包含：**新芽萌发数量**、**花梗（花箭）长度估计**、**根系颜色分布**（白/绿/褐/黑各占比）、**根系健康度**、**综合生长活力评级**（旺盛/正常/衰弱）、**养护方向参考**
        - **重要提示**：仅输出基于视觉的生长状态指标，**不提供具体的施肥或用药剂量**

## 🌱 新芽萌发评估

| 新芽数量 | 评级 | 说明 |
|----------|------|------|
| 3+ | 🟢 旺盛 | 生长活力极佳，株型扩展能力强 |
| 1-2 | 🟡 正常 | 健康生长，符合正常分蘖节奏 |
| 0 | 🟠 静止 | 处于休眠或养分储备期；若长期无芽需关注 |

## 🌸 花梗（花箭）长度评估

| 长度阶段 | 视觉表现 | 养护方向参考 |
|----------|----------|--------------|
| 萌动期（<5cm） | 假鳞茎旁出现绿色尖锥状突起 | 保持稳定环境，避免移动 |
| 拔节期（5-20cm） | 花箭快速伸长，节间明显 | 注意支撑，防倒伏 |
| 花苞期（>20cm） | 花箭顶端出现花苞 | 增加磷钾肥方向，准备开花 |
| 无花梗 | 仅见叶片和新芽 | 可能营养未达开花条件，或非花期 |

## 🌿 根系颜色识别与健康度

| 根系颜色 | 健康度 | 视觉表现 | 含义 |
|----------|--------|----------|------|
| ⚪ 银白色 | 🟢 极佳 | 根尖饱满有水雾感，外层覆盖银白色根被 | 充水后呈现，活跃健康根系 |
| 🟢 翠绿色 | 🟢 优秀 | 透明盆中可见的健康吸水根 | 正在光合作用与吸水，活力强 |
| 🟡 浅黄色 | 🟡 普通 | 较老的根系 | 老化但仍具功能 |
| 🟠 褐色 | 🟠 衰退 | 干瘪、表皮褐变 | 老化或缺水，需关注 |
| ⚫ 黑色 | 🔴 腐烂 | 软烂发黑、有臭味 | 烂根，需紧急处理 |

## 📊 生长活力综合评级

| 评级 | 综合特征 | 养护方向 |
|------|----------|----------|
| 🟢 旺盛 | 新芽 ≥2，根系以白/绿为主（>70%健康根） | 维持当前养护，可适当增肥促进开花 |
| 🟡 正常 | 新芽 1-2，根系健康根占 40-70% | 保持稳定，关注水肥平衡 |
| 🟠 衰弱 | 无新芽，褐/黑根超 50% | 需检查浇水/通风/植料，必要时换盆 |
| 🔴 危重 | 假鳞茎萎缩、烂根超过 70% | 紧急处理：剪除烂根、消毒、重新上盆 |

## 📅 兰花养护关键节点参考

| 季节 | 重点观察指标 | 常见问题 |
|------|--------------|----------|
| 🌸 春季 | 新芽萌发数量、花梗抽出 | 春化不足导致无花 |
| 🌞 夏季 | 根系颜色（防烂根） | 高温烂根、叶片晒伤 |
| 🍂 秋季 | 花梗发育、株型饱满度 | 花苞败育、新芽不健壮 |
| ❄️ 冬季 | 假鳞茎饱满度、根系状态 | 低温烂根、冻害 |

## 资源索引

- 必要脚本：见 [scripts/smyx_orchid_growth_status_detection_analysis.py](scripts/smyx_orchid_growth_status_detection_analysis.py)(用途：调用 API 进行兰花生长状态识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- **拍摄要求**：建议整体+根系两张图；根系拍摄必须为透明盆且贴近盆壁
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **仅输出基于视觉的生长状态指标，不提供具体施肥或用药剂量**
- 不透明盆无法识别根系，仅能评估新芽和花梗
- 兰花品种繁多（蝴蝶兰/卡特兰/石斛/国兰/万代等），不同品种根系/花梗形态差异大
- 根系刚浇水会呈翠绿色（吸水状态），干燥时呈银白色（根被显露），均为健康
- 长期无新芽不一定是衰弱，可能处于休眠/养分储备期，需结合季节判断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史识别报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"对象类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`兰花生长状态报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 对象类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 兰花生长状态报告-20260312172200001 | 植物 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地兰花图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_orchid_growth_status_detection_analysis --input /path/to/orchid.jpg --open-id your-open-id

# 分析网络兰花图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_orchid_growth_status_detection_analysis --url https://example.com/orchid.jpg --open-id your-open-id

# 显示历史识别报告/显示报告清单列表
python -m scripts.smyx_orchid_growth_status_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_orchid_growth_status_detection_analysis --input orchid.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_orchid_growth_status_detection_analysis --input orchid.jpg --open-id your-open-id --output result.json
```
