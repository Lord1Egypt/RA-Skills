---
name: "smyx-plant-growth-stage-detection-analysis"
description: "AI-powered plant growth stage auto-detection from periodic full-plant images via smart pot / greenhouse fixed cameras. Recognizes key phenological features—cotyledon emergence, true-leaf count, flower bud differentiation, blooming, fruit setting, fruit ripening—and identifies the current developmental stage (germination, seedling, vegetative, flowering, fruiting, ripening), enabling precision irrigation/fertilization/lighting control and personalized growing guidance. Scenarios: smart pots, home grow boxes, greenhouses, plant factories. | 通过智能花盆或温室内固定摄像头，定期拍摄植物整体图像，利用AI视觉分析技术识别子叶展开、真叶数量、花芽分化、开花、结果、果实成熟等关键物候特征，自动判定植物当前所处的生长发育阶段（如发芽期、幼苗期、生长期、开花期、结果期、成熟期）。有助于精准农业管理，实现自动化灌溉、施肥、光照调节，并为用户提供种植指导。应用场景：智能花盆、家庭种植机、温室大棚、植物工厂。"
version: "1.0.0"
---

# Plant Growth Stage Detection | 植物生长阶段自动判定

AI-powered plant growth stage auto-detection from periodic full-plant images via smart pot / greenhouse fixed cameras. Recognizes key phenological features—cotyledon emergence, true-leaf count, flower bud differentiation, blooming, fruit setting, fruit ripening—and identifies the current developmental stage (germination, seedling, vegetative, flowering, fruiting, ripening), enabling precision irrigation/fertilization/lighting control and personalized growing guidance. Scenarios: smart pots, home grow boxes, greenhouses, plant factories.

通过智能花盆或温室内固定摄像头，定期拍摄植物整体图像，利用AI视觉分析技术识别子叶展开、真叶数量、花芽分化、开花、结果、果实成熟等关键物候特征，自动判定植物当前所处的生长发育阶段（如发芽期、幼苗期、生长期、开花期、结果期、成熟期）。有助于精准农业管理，实现自动化灌溉、施肥、光照调节，并为用户提供种植指导。应用场景：智能花盆、家庭种植机、温室大棚、植物工厂。

## 🎯 AI 角色

**假设你是一个专业的植物发育学AI。你的任务是分析植物整体或局部器官（茎、叶、花、果）的连续或单张图像，识别关键发育特征，判定当前生长阶段。不要提供农业操作具体细节，仅输出阶段判断及置信度。**

## 任务目标

- 本 Skill 用于：通过植物整体或局部器官图像/视频判定当前生长发育阶段，输出阶段名称、置信度和阶段性通用养护方向
- 能力包含：物候特征识别（子叶/真叶/花芽/花朵/果实）、生长阶段分类（发芽期/幼苗期/生长期/开花期/结果期/成熟期）、置信度评分、阶段通用养护方向建议
- 触发条件:
    1. **默认触发**：当用户提供植物整体或局部器官图像/视频需要分析时，默认触发本技能进行生长阶段判定
    2. 当用户明确需要植物生长阶段判定时，提及生长阶段、发芽、开花、结果、物候、植物发育等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史生长阶段报告、历史植物发育报告、生长阶段报告清单、显示所有阶段报告、查询植物物候记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有生长阶段报告"、"显示植物发育报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_plant_growth_stage_detection_analysis --list --open-id` 参数调用 API
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

**在执行植物生长阶段判定前，必须按以下优先级顺序获取 open-id：**

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
        - 提供本地植物整体图像/视频文件路径或网络 URL
        - 拍摄建议：
          - 拍摄**植物整体**（根茎叶花果均可见最佳）
          - 光线充足（自然光最佳），避免逆光
          - 固定角度定期拍摄便于对比生长变化
          - 近景补充拍摄关键器官（花芽、幼果等）
        - 支持图像（jpg/png）和视频（mp4/avi/mov）格式
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行生长阶段判定**
        - 调用 `-m scripts.smyx_plant_growth_stage_detection_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地植物图像/视频文件路径
            - `--url`: 网络植物图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 对象类型，植物场景默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示生长阶段判定历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看判定结果**
        - 接收结构化的植物生长阶段判定报告
        - 包含：**当前生长阶段**（发芽期/幼苗期/生长期/开花期/结果期/成熟期）、**关键物候特征**（识别到的发育特征描述）、**置信度评分**、**阶段通用养护方向**（如"开花期建议增加磷钾肥"）
        - **重要提示**：仅输出阶段判断及置信度，**不提供农业操作具体细节**

## 🌱 植物生长阶段分类体系

| 阶段 | 英文 | 关键识别特征 | 典型时长 |
|------|------|--------------|----------|
| 🌰 发芽期 | Germination | 种子萌发、子叶展开 | 3-14 天 |
| 🌿 幼苗期 | Seedling | 子叶→真叶转换、1-3片真叶 | 1-4 周 |
| 📈 生长期 | Vegetative | 真叶数量增加、茎干拔高、枝叶茂盛 | 数周-数月 |
| 🌸 开花期 | Flowering | 花芽分化、花苞形成、花朵开放 | 1-8 周 |
| 🍅 结果期 | Fruiting | 花后坐果、幼果膨大 | 数周-数月 |
| 🍎 成熟期 | Ripening | 果实转色、糖度上升、可采收 | 1-4 周 |

## 🔍 关键物候特征识别对照

| 物候特征 | 视觉表现 | 标志性阶段转换 |
|----------|----------|----------------|
| 子叶展开 | 两片对称小叶从种壳中展开 | 发芽期 → 幼苗期 |
| 第一真叶 | 子叶上方出现不同于子叶形态的真叶 | 进入幼苗期 |
| 叶片数量激增 | 真叶快速增长、茎节伸长 | 幼苗期 → 生长期 |
| 花芽分化 | 叶腋或顶端出现膨大的花芽 | 生长期 → 开花期 |
| 花朵开放 | 花苞绽放，花瓣可见 | 开花期标志 |
| 幼果坐果 | 花后子房膨大形成幼果 | 开花期 → 结果期 |
| 果实膨大 | 果实体积增大、形状渐趋完满 | 结果期进行中 |
| 果实转色 | 由绿转红/黄/橙等成熟色 | 结果期 → 成熟期 |

## 📊 置信度说明

| 置信度区间 | 可靠性 | 说明 |
|------------|--------|------|
| 80%-100% | 🟢 高 | 特征明确，阶段判定可靠 |
| 60%-79% | 🟡 中 | 部分特征可见，建议补充更多图像 |
| <60% | 🟠 低 | 特征模糊，可能处于阶段过渡期，建议隔天再次拍摄 |

## 💡 各阶段通用养护方向参考

| 阶段 | 水分 | 养分重点 | 光照 | 特殊提示 |
|------|------|----------|------|----------|
| 🌰 发芽期 | 保持湿润 | 无需施肥 | 弱光散射光 | 覆膜保湿 |
| 🌿 幼苗期 | 适度浇水 | 稀薄氮肥 | 逐步增加光照 | 防止徒长 |
| 📈 生长期 | 充足浇水 | 氮肥为主，适量磷钾 | 充足日照 | 番茄等需搭架 |
| 🌸 开花期 | 适度控水 | 磷钾肥为主 | 充足日照 | 建议人工辅助授粉 |
| 🍅 结果期 | 均匀浇水 | 钾肥为主 | 充足日照 | 避免水分剧烈波动 |
| 🍎 成熟期 | 减少浇水 | 停止施肥 | 保持光照 | 适时采收 |

> ⚠️ 以上仅为通用方向参考，**不构成具体农业操作方案**；具体施肥/灌溉需根据植物种类、环境条件调整。

## 资源索引

- 必要脚本：见 [scripts/smyx_plant_growth_stage_detection_analysis.py](scripts/smyx_plant_growth_stage_detection_analysis.py)(用途：调用 API 进行植物生长阶段判定，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- **拍摄建议**：整体 + 关键器官近景；固定角度定期拍摄便于对比
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **判定结果仅供生长阶段参考，不提供农业操作具体细节**
- 不同植物物候周期差异大，判定需结合植物种类信息
- 阶段过渡期（如开花初期）特征可能不明确，置信度会偏低
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史判定报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"对象类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`植物生长阶段判定报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 对象类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 植物生长阶段判定报告-20260312172200001 | 植物 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地植物图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_growth_stage_detection_analysis --input /path/to/plant.jpg --open-id your-open-id

# 分析网络植物图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_growth_stage_detection_analysis --url https://example.com/plant.jpg --open-id your-open-id

# 显示历史判定报告/显示报告清单列表
python -m scripts.smyx_plant_growth_stage_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_plant_growth_stage_detection_analysis --input plant.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_growth_stage_detection_analysis --input plant.jpg --open-id your-open-id --output result.json
```
