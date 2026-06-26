---
name: "smyx-flowering-date-prediction-analysis"
description: "AI-powered flowering-date prediction for ornamental/cut-flower plants. From fixed greenhouse cameras or drones, captures images of flower-bud developmental stages, combines environmental sensor data — cumulative temperature (Growing Degree Days, GDD) and accumulated light (PAR or daylight hours) — and uses a pre-trained phenology model to predict the full-bloom date within the next 3-7 days. Helps growers precisely schedule pollination, harvesting and tourism activities. Scenarios: smart-agriculture greenhouses, cut-flower production bases, botanical gardens, flower tourism parks. | 通过智慧农业温室中的固定摄像头或无人机拍摄植物花蕾发育阶段的图像，并结合环境传感器提供的温度累积（生长度日，GDD）、光照累积（光合有效辐射或日照时长）等数据，利用预训练的物候模型预测未来3-7天内的开花日期（花朵完全开放）。该技能有助于温室种植者精准安排授粉、采收或观光活动。应用场景：智慧农业温室、切花生产基地、植物园、花卉观光园区。"
version: "1.0.2"
license: "MIT-0"
---

# Flowering Date Prediction | 开花植物花期预测

AI-powered flowering-date prediction for ornamental/cut-flower plants. From fixed greenhouse cameras or drones, captures images of flower-bud developmental stages, combines environmental sensor data — cumulative temperature (Growing Degree Days, GDD) and accumulated light (PAR or daylight hours) — and uses a pre-trained phenology model to predict the full-bloom date within the next 3-7 days. Helps growers precisely schedule pollination, harvesting and tourism activities. Scenarios: smart-agriculture greenhouses, cut-flower production bases, botanical gardens, flower tourism parks.

通过智慧农业温室中的固定摄像头或无人机拍摄植物花蕾发育阶段的图像，并结合环境传感器提供的温度累积（生长度日，GDD）、光照累积（光合有效辐射或日照时长）等数据，利用预训练的物候模型预测未来3-7天内的开花日期（花朵完全开放）。该技能有助于温室种植者精准安排授粉、采收或观光活动。应用场景：智慧农业温室、切花生产基地、植物园、花卉观光园区。

## 🎯 AI 角色

**假设你是一个专业的植物物候预测 AI。你的任务是分析花蕾发育阶段的高清图像，结合当前及历史温光数据（生长度日 GDD、光照累积），基于作物物候模型预测未来 3-7 天内的开花日期（花朵完全开放）。不要提供具体的栽培操作（施肥配方、温控参数等），仅输出预测的开花日期与置信度。**

## 任务目标

- 本 Skill 用于：通过花蕾发育阶段图像 + 可选环境温光数据进行花期预测，输出未来 3-7 天内的预计开花日期与物候阶段
- 能力包含：花蕾发育阶段识别（紧蕾期 / 露色期 / 显色期 / 临开放期）、GDD / 光照累积融合（如提供）、未来开花日期预测（日期 + 置信度区间）、物候发育速率提示、生产计划方向建议（授粉 / 采收 / 观光档期）
- 触发条件:
    1. **默认触发**：当用户提供花蕾发育阶段图像或视频（可选附带温光累积数据）需要花期预测时，默认触发本技能
    2. 当用户明确需要花期预测时，提及花期预测、开花时间、几天后开花、花蕾发育、物候、GDD、生长度日、温室花卉、切花生产、采收档期、观花期等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史花期预测报告、历史花期报告、花期预测清单、显示所有花期分析报告、查询花期诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有花期预测报告"、"显示花期分析报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_flowering_date_prediction_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行花期预测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备花蕾图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 确保画面清晰对准代表性花蕾（特写优先），可附带环境温光累积数据（GDD、累积日照时长等）
        - 同一植株建议固定机位、每天同一时段采集，便于物候发育跨期对比
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行花期预测**
        - 调用 `-m scripts.smyx_flowering_date_prediction_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，花卉场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示花期预测历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的花期预测报告
        - 包含：当前花蕾发育阶段、估算累积 GDD、估算累积光照、预测开花日期（如"2026-05-27"）、预测置信度（如 0.82）、未来 3-7 天发育趋势提示、生产计划方向建议（如"预计 4 天后进入盛花期，建议提前安排授粉队伍及切花档期"）
        - **重要提示**：仅输出预测日期与方向建议，不提供具体施肥配方 / 温控参数等栽培操作方案

## 资源索引

- 必要脚本：见 [scripts/smyx_flowering_date_prediction_analysis.py](scripts/smyx_flowering_date_prediction_analysis.py)(用途：调用 API 进行花期预测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：自然光或稳定温室光下、距离 20-50 cm 拍摄花蕾特写；同一植株固定机位定期采集效果最佳
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供生产计划参考，预测日期存在 ±1-2 天误差，正式排产请结合人工巡查与历史经验
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"作物品种"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`花期预测报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 作物品种 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 花期预测报告-20260523000900001 | 切花月季 | 2026-05-23 00:09:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地花蕾图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_flowering_date_prediction_analysis --input /path/to/bud.jpg --open-id your-open-id

# 分析网络花蕾图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_flowering_date_prediction_analysis --url https://example.com/bud.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史花期预测报告（自动触发关键词：查看历史花期预测报告、历史报告、花期预测清单等）
python -m scripts.smyx_flowering_date_prediction_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_flowering_date_prediction_analysis --input bud.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_flowering_date_prediction_analysis --input bud.jpg --open-id your-open-id --output result.json
```
