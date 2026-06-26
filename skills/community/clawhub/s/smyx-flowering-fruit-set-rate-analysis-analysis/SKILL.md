---
name: "smyx-flowering-fruit-set-rate-analysis-analysis"
description: "AI-powered flowering and fruit-set rate analysis for tomato / chili plants. From home grow-box or mobile phone images of flowering/fruit clusters, uses object-detection models to count open flowers (fully-opened corolla with visible stamens) and successfully-set young fruits (enlarged ovary, ~0.5-1cm green baby fruits), and computes fruit-set rate = young fruits / flowers × 100%. Helps growers evaluate pollination, nutrition and environmental adaptability, and guides hand-assisted pollination or water/fertilizer adjustment. Scenarios: home smart grow-boxes, greenhouses, balcony vegetable gardens. | 通过家庭种植箱或手机拍摄的植株花果图像（包含花穗、果实区域），利用AI视觉目标检测模型识别开放花朵（花冠完全展开、雄蕊可见）的数量以及已坐果的小果（子房膨大、直径约0.5-1cm的绿色幼果）数量，计算坐果率（小果数/花朵数 × 100%）。该技能帮助种植者评估授粉效果、营养状况及环境适应性，指导人工辅助授粉或调整水肥管理。应用场景：家庭智能种植箱、温室大棚、阳台菜园。"
version: "1.0.0"
---

# Flowering & Fruit Set Rate Analysis | 番茄/辣椒开花坐果率分析

AI-powered flowering and fruit-set rate analysis for tomato / chili plants. From home grow-box or mobile phone images of flowering/fruit clusters, uses object-detection models to count open flowers (fully-opened corolla with visible stamens) and successfully-set young fruits (enlarged ovary, ~0.5-1cm green baby fruits), and computes fruit-set rate = young fruits / flowers × 100%. Helps growers evaluate pollination, nutrition and environmental adaptability, and guides hand-assisted pollination or water/fertilizer adjustment. Scenarios: home smart grow-boxes, greenhouses, balcony vegetable gardens.

通过家庭种植箱或手机拍摄的植株花果图像（包含花穗、果实区域），利用AI视觉目标检测模型识别开放花朵（花冠完全展开、雄蕊可见）的数量以及已坐果的小果（子房膨大、直径约0.5-1cm的绿色幼果）数量，计算坐果率（小果数/花朵数 × 100%）。该技能帮助种植者评估授粉效果、营养状况及环境适应性，指导人工辅助授粉或调整水肥管理。应用场景：家庭智能种植箱、温室大棚、阳台菜园。

## 🎯 AI 角色

**假设你是一个专业的园艺作物生产 AI。你的任务是分析番茄或辣椒植株的花果区域图像，检测并计数开放花朵（花冠完全展开、雄蕊可见）和已坐果的小果（子房膨大、直径约 0.5–1 cm 的绿色幼果），计算坐果率（小果数 / 花朵数 × 100%）。不要提供具体化肥用量，仅输出数量和比率。**

## 任务目标

- 本 Skill 用于：通过番茄 / 辣椒花果区域图像或视频进行开花及坐果率分析，输出花朵 / 幼果计数与坐果率
- 能力包含：开放花朵识别与计数、已坐果小果识别与计数（子房膨大、绿色幼果）、坐果率计算（小果数 / 花朵数 × 100%）、坐果率等级评估（低 / 中 / 高 / 优秀）、授粉与水肥调整方向建议（人工辅助授粉 / 振动授粉 / 调整温度湿度等）
- 触发条件:
    1. **默认触发**：当用户提供番茄、辣椒、茄子等花果类蔬菜的花果区域图像或视频时，默认触发本技能
    2. 当用户明确需要坐果率评估时，提及番茄坐果率、辣椒坐果率、落花、授粉不良、坐果差、幼果掉落、花朵数量、人工授粉、振动授粉、坐果监测等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史坐果率报告、历史开花报告、坐果率趋势清单、显示所有坐果分析报告、查询花果监测记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有坐果率报告"、"显示开花坐果报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行开花坐果率分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备花果区域图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保画面清晰展示植株花穗、果实区域，每张图建议包含完整的一个或多个花序
        - 同一植株建议固定机位、定期采集，便于跨期对比
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行开花坐果率分析**
        - 调用 `-m scripts.smyx_flowering_fruit_set_rate_analysis_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，蔬果场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示开花坐果历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的开花坐果分析报告
        - 包含：开放花朵数量、已坐果小果数量、坐果率（百分比）、坐果率等级（低 / 中 / 高 / 优秀）、改进方向建议（如"坐果率仅 45%，建议盛花期人工摇动植株或使用电动授粉棒辅助授粉，并保持温度 20-28℃、相对湿度 60-70%"）
        - **重要提示**：仅输出基于视觉的数量与比率，不提供具体化肥用量；严重落花/坐果差建议咨询当地农技师

## 资源索引

- 必要脚本：见 [scripts/smyx_flowering_fruit_set_rate_analysis_analysis.py](scripts/smyx_flowering_fruit_set_rate_analysis_analysis.py)(用途：调用 API 进行开花坐果率分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：建议自然光下、距离 30-60 cm 正面拍摄花穗 / 果序，避免重叠遮挡；多角度补拍可提升计数精度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供种植决策参考，不提供具体化肥用量与农药使用方案
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"作物品种"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`开花坐果率分析报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 作物品种 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 开花坐果率分析报告-20260522231900001 | 番茄 | 2026-05-22 23:19:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地番茄/辣椒花果图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --input /path/to/tomato_flower.jpg --open-id your-open-id

# 分析网络花果图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --url https://example.com/chili_flower.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史坐果率报告（自动触发关键词：查看历史坐果率报告、历史报告、开花坐果报告清单等）
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --input tomato.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --input tomato.jpg --open-id your-open-id --output result.json
```
