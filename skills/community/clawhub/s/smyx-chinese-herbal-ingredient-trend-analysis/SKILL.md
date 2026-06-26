---
name: "smyx-chinese-herbal-ingredient-trend-analysis"
description: "AI-powered active-ingredient accumulation trend assessment for medicinal herbs (e.g. honeysuckle, wolfberry, astragalus, danshen). Uses high-resolution leaf images captured by fixed cameras or drones in TCM cultivation bases, analyzes leaf color saturation, hue angle, relative chlorophyll content (estimated via color indices) and leaf thickness (inferred from edge focus / silhouette), and compares against the cultivar's standard reference atlas (typical features at peak active-ingredient stage) to output an accumulation trend level (Low / Medium / High / Peak). Helps determine the optimal harvest window and improve herb quality. Scenarios: TCM planting bases, GAP bases, herb cooperatives, raw-material bases for pharmaceutical companies. | 通过中药种植基地的固定摄像头或无人机拍摄药用植物（如金银花、枸杞、黄芪、丹参等）叶片的高清图像，利用AI视觉分析技术评估叶片颜色饱和度、色相角、叶绿素相对含量（通过颜色指数估算）以及叶片厚度（通过边缘聚焦或侧影估算），与品种标准图谱（特定生长阶段/有效成分积累峰值期的典型特征）进行对比，输出有效成分积累趋势等级（低/中/高/峰值）。该技能有助于确定最佳采收期，提高药材品质。应用场景：中药种植基地、GAP种植基地、中药材合作社、药企原料基地。"
version: "1.0.2"
license: "MIT-0"
---

# Chinese Herbal Active Ingredient Trend Analysis | 中草药有效成分积累趋势评估

AI-powered active-ingredient accumulation trend assessment for medicinal herbs (e.g. honeysuckle, wolfberry, astragalus,
danshen). Uses high-resolution leaf images captured by fixed cameras or drones in TCM cultivation bases, analyzes leaf
color saturation, hue angle, relative chlorophyll content (estimated via color indices) and leaf thickness (inferred
from edge focus / silhouette), and compares against the cultivar's standard reference atlas (typical features at peak
active-ingredient stage) to output an accumulation trend level (Low / Medium / High / Peak). Helps determine the optimal
harvest window and improve herb quality. Scenarios: TCM planting bases, GAP bases, herb cooperatives, raw-material bases
for pharmaceutical companies.

通过中药种植基地的固定摄像头或无人机拍摄药用植物（如金银花、枸杞、黄芪、丹参等）叶片的高清图像，利用AI视觉分析技术评估叶片颜色饱和度、色相角、叶绿素相对含量（通过颜色指数估算）以及叶片厚度（通过边缘聚焦或侧影估算），与品种标准图谱（特定生长阶段/有效成分积累峰值期的典型特征）进行对比，输出有效成分积累趋势等级（低/中/高/峰值）。该技能有助于确定最佳采收期，提高药材品质。应用场景：中药种植基地、GAP种植基地、中药材合作社、药企原料基地。

## 🎯 AI 角色

**假设你是一个专业的中草药栽培与质量评价
AI。你的任务是分析药用植物叶片的高清图像，评估叶片颜色饱和度、绿色深度（或红/黄/蓝色相）、叶绿素指数（如归一化植被指数模拟值）以及叶片厚度（可通过叶缘清晰度/聚焦深度间接推断），并与该品种的标准参考图谱（含有效成分积累高峰期的典型特征）进行比对，输出当前有效成分积累趋势等级。不要提供化学检测数据，仅基于视觉特征给出预测。
**

## 任务目标

- 本 Skill 用于：通过药用植物叶片的高清图像/视频进行有效成分积累趋势评估，输出趋势等级与采收时机建议
-

能力包含：叶片颜色饱和度评估、色相角分析、叶绿素相对含量估算（颜色指数模拟）、叶片厚度间接推断（边缘聚焦/侧影）、与品种标准图谱比对、有效成分积累趋势等级判定（低 /
中 / 高 / 峰值）、最佳采收期建议

- 触发条件:
    1. **默认触发**：当用户提供药用植物（金银花 / 枸杞 / 黄芪 / 丹参 / 三七 / 黄芩 / 板蓝根等）叶片的图像或视频需要趋势评估时，默认触发本技能
    2. 当用户明确需要采收时机评估时，提及中药材、药用植物、有效成分、采收期、GAP
       基地、金银花、枸杞、黄芪、丹参、叶绿素含量、品质趋势、最佳采收等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史中药趋势报告、历史有效成分报告、中药材趋势清单、显示所有采收期评估报告、查询药材趋势记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有中药趋势报告"、"
       显示有效成分评估报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --list --open-id` 参数调用 API
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

**在执行有效成分趋势评估前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备药用植物叶片图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保画面清晰展示药用植物代表性叶片（高分辨率，自然光下拍摄优先）
        - 同一基地建议固定机位、固定时间段采集，便于跨期趋势对比
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行趋势评估分析**
        - 调用 `-m scripts.smyx_chinese_herbal_ingredient_trend_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本
          **）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，中药材场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示有效成分趋势历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的有效成分趋势评估报告
        - 包含：叶片颜色饱和度、色相角、叶绿素相对含量指数、叶片厚度推断、与品种标准图谱的偏差、有效成分积累趋势等级（低 / 中 /
          高 / 峰值）、最佳采收期建议（如"金银花有效成分积累已达峰值，建议未来 3 天内采收"）
        - **重要提示**：仅基于视觉特征给出预测，不提供化学检测数据；正式上市前请配合 HPLC 等专业检测复核

## 资源索引

-

必要脚本：见 [scripts/smyx_chinese_herbal_ingredient_trend_analysis.py](scripts/smyx_chinese_herbal_ingredient_trend_analysis.py)(
用途：调用 API 进行有效成分趋势评估，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：建议在晴朗自然光下、避免强反光，叶片正面平展、聚焦清晰；同一植株多期对比效果最佳
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供采收决策参考，正式品质评定请配合 HPLC / 国标 / 药典等专业化学检测
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"药材品种"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`中草药有效成分趋势报告-{记录id}`
  形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 药材品种 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 中草药有效成分趋势报告-20260522230400001 | 金银花 | 2026-05-22 23:04:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地药用植物叶片图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --input /path/to/herb_leaf.jpg --open-id your-open-id

# 分析网络药用植物叶片图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --url https://example.com/herb_leaf.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史中药趋势报告（自动触发关键词：查看历史中药趋势报告、历史报告、有效成分趋势清单等）
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --input herb.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --input herb.jpg --open-id your-open-id --output result.json
```
