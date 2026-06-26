---
name: "smyx-fruit-ripeness-grading-analysis"
description: "AI-powered fruit ripeness grading for tomatoes / strawberries. From smart grow-boxes or mobile phone images, uses AI vision to detect fruit color (green / light green / orange / red / dark red), colored-area ratio, gloss, and relative fruit size (against a reference object), and outputs a ripeness grade (Mature-Green / Turning / Ripe / Over-Ripe) based on preset standards. Helps growers identify the optimal harvest window and ensures flavor and shelf quality. Scenarios: smart grow-boxes, greenhouses, home vegetable gardens, fruit & vegetable cooperatives. | 通过智能种植箱或手机拍摄的果实图像，利用AI视觉分析技术检测果实的颜色（绿/浅绿/橙/红/暗红）、着色面积比例、光泽度以及果实大小（相对于参照物），根据预设的成熟度分级标准输出等级（青熟期/转色期/成熟期/过熟期）。该技能帮助种植者确定最佳采收时机，保证果实口感和商品性。应用场景：智能种植箱、温室大棚、家庭菜园、果蔬合作社。"
version: "1.0.0"
---

# Fruit Ripeness Grading | 番茄/草莓果实成熟度分级

AI-powered fruit ripeness grading for tomatoes / strawberries. From smart grow-boxes or mobile phone images, uses AI vision to detect fruit color (green / light green / orange / red / dark red), colored-area ratio, gloss, and relative fruit size (against a reference object), and outputs a ripeness grade (Mature-Green / Turning / Ripe / Over-Ripe) based on preset standards. Helps growers identify the optimal harvest window and ensures flavor and shelf quality. Scenarios: smart grow-boxes, greenhouses, home vegetable gardens, fruit & vegetable cooperatives.

通过智能种植箱或手机拍摄的果实图像，利用AI视觉分析技术检测果实的颜色（绿/浅绿/橙/红/暗红）、着色面积比例、光泽度以及果实大小（相对于参照物），根据预设的成熟度分级标准输出等级（青熟期/转色期/成熟期/过熟期）。该技能帮助种植者确定最佳采收时机，保证果实口感和商品性。应用场景：智能种植箱、温室大棚、家庭菜园、果蔬合作社。

## 🎯 AI 角色

**假设你是一个专业的园艺作物采收 AI。你的任务是分析番茄或草莓果实的图像，检测果实颜色、着色面积、光泽度及大小，根据预设的分级规则输出成熟度等级（青熟期 / 转色期 / 成熟期 / 过熟期）。不要提供具体的采收后处理建议（贮藏温度、保鲜剂等），仅输出基于视觉的成熟度分级。**

## 任务目标

- 本 Skill 用于：通过番茄 / 草莓果实图像或视频进行成熟度分级，输出每颗果实的成熟度等级及整体采收建议
- 能力包含：果实定位与计数、主色调识别（绿 / 浅绿 / 橙 / 红 / 暗红）、着色面积比例计算、光泽度评估、果实相对大小估算、按预设规则的成熟度分级（青熟期 / 转色期 / 成熟期 / 过熟期）、整体采收建议（继续养果 / 准备采收 / 立即采收 / 已过最佳采收期）
- 触发条件:
    1. **默认触发**：当用户提供番茄、草莓等果实的图像或视频需要成熟度分级时，默认触发本技能
    2. 当用户明确需要成熟度判断时，提及番茄成熟度、草莓成熟度、果实采收、转色期、青熟、红熟、采收时机、果实分级、果蔬分拣等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史成熟度报告、历史果实分级报告、采收报告清单、显示所有成熟度分级报告、查询果实采收记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有成熟度报告"、"显示果实分级报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_fruit_ripeness_grading_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行果实成熟度分级前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备果实图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保画面清晰展示果实正面或代表性面，光照均匀；如条件允许可在画面中放置参照物（硬币 / 标尺）以便估算果实大小
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行果实成熟度分级**
        - 调用 `-m scripts.smyx_fruit_ripeness_grading_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，果蔬场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示果实成熟度历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的果实成熟度分级报告
        - 包含：检出果实数量、各果实主色调与着色面积比例、光泽度评估、相对大小评估、单果成熟度等级、整体成熟度分布占比、采收建议（如"60% 进入成熟期、20% 转色期、20% 青熟期，建议 1-2 天内采收成熟期果实，转色期果实再观察 2-3 天"）
        - **重要提示**：仅输出基于视觉的成熟度分级与采收方向，不提供具体贮藏温度 / 保鲜剂等采后处理方案

## 资源索引

- 必要脚本：见 [scripts/smyx_fruit_ripeness_grading_analysis.py](scripts/smyx_fruit_ripeness_grading_analysis.py)(用途：调用 API 进行果实成熟度分级，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：自然光下、避免强反光与高对比阴影；尽量正面拍摄果实，多角度补拍可提升精度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供采收决策参考，不提供采后贮藏 / 保鲜方案；商品化分级请配合企业标准复核
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"作物品种"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`果实成熟度分级报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 作物品种 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 果实成熟度分级报告-20260523001600001 | 番茄 | 2026-05-23 00:16:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地番茄/草莓果实图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fruit_ripeness_grading_analysis --input /path/to/tomato.jpg --open-id your-open-id

# 分析网络果实图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_fruit_ripeness_grading_analysis --url https://example.com/strawberry.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史成熟度报告（自动触发关键词：查看历史成熟度报告、历史报告、果实分级清单等）
python -m scripts.smyx_fruit_ripeness_grading_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_fruit_ripeness_grading_analysis --input fruit.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_fruit_ripeness_grading_analysis --input fruit.jpg --open-id your-open-id --output result.json
```
