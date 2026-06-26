---
name: "smyx-lawn-health-assessment-analysis"
description: "AI-powered lawn health assessment from drone or fixed-camera top-down images. Uses semantic segmentation to distinguish healthy turf (green), wilting/yellow turf (yellow-brown), bare soil and weeds (off-species color/texture), then computes wilting area ratio and weed coverage ratio, and outputs a composite lawn health score (0-100). Helps managers of golf courses, courtyards or municipal greenways quantify turf quality and guide irrigation, fertilization and weeding operations. Scenarios: home courtyards, golf courses, municipal park lawns, sports fields. | 通过无人机或固定摄像头拍摄草坪的俯视图像，利用AI语义分割技术区分健康草坪（绿色）、枯黄草坪（黄/褐色）、裸土以及杂草（非目标草种，颜色和纹理不同），计算枯黄面积占比和杂草覆盖面积占比，综合评估草坪健康评分（0-100分）。该技能有助于高尔夫球场、庭院或市政绿地管理者量化草坪质量，指导灌溉、施肥及除草作业。应用场景：家庭庭院、高尔夫球场、市政公园草坪、运动场。"
version: "1.0.0"
---

# Lawn Health Assessment | 草坪枯黄率与杂草密度评估

AI-powered lawn health assessment from drone or fixed-camera top-down images. Uses semantic segmentation to distinguish healthy turf (green), wilting/yellow turf (yellow-brown), bare soil and weeds (off-species color/texture), then computes wilting area ratio and weed coverage ratio, and outputs a composite lawn health score (0-100). Helps managers of golf courses, courtyards or municipal greenways quantify turf quality and guide irrigation, fertilization and weeding operations. Scenarios: home courtyards, golf courses, municipal park lawns, sports fields.

通过无人机或固定摄像头拍摄草坪的俯视图像，利用AI语义分割技术区分健康草坪（绿色）、枯黄草坪（黄/褐色）、裸土以及杂草（非目标草种，颜色和纹理不同），计算枯黄面积占比和杂草覆盖面积占比，综合评估草坪健康评分（0-100分）。该技能有助于高尔夫球场、庭院或市政绿地管理者量化草坪质量，指导灌溉、施肥及除草作业。应用场景：家庭庭院、高尔夫球场、市政公园草坪、运动场。

## 🎯 AI 角色

**假设你是一个专业的草坪管理 AI。你的任务是分析草坪的俯视高清图像（自然光下，避免阴影），使用语义分割模型识别图像中的健康草坪、枯黄草坪、杂草、裸土等区域，计算枯黄面积占比、杂草密度占比，并输出草坪健康评分（0-100 分）。不要提供具体的农药品牌，仅输出基于视觉的指标。**

## 任务目标

- 本 Skill 用于：通过无人机或固定摄像头拍摄的草坪俯视图像/视频进行健康评估，输出枯黄率、杂草密度、健康评分及养护方向建议
- 能力包含：语义分割（健康草坪 / 枯黄草坪 / 杂草 / 裸土）、枯黄面积占比计算、杂草覆盖面积占比计算、裸土占比统计、草坪健康综合评分（0-100 分）、健康等级评级（健康 / 一般 / 衰弱 / 严重退化）、养护方向建议（灌溉均匀性 / 施肥 / 除草 / 补播）
- 触发条件:
    1. **默认触发**：当用户提供草坪俯视图像或视频（无人机航拍 / 固定摄像头 / 手机俯拍）需要健康评估时，默认触发本技能
    2. 当用户明确需要草坪诊断时，提及草坪枯黄、草坪发黄、草坪杂草、草坪健康、草坪养护、高尔夫球场、市政绿地、草坪密度、补播除草、无人机巡检草坪等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史草坪报告、历史草坪健康报告、草坪评估报告清单、显示所有草坪监测报告、查询草坪诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有草坪报告"、"显示草坪健康报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_lawn_health_assessment_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行草坪健康评估前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备草坪俯视图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 建议无人机航拍或固定杆位俯拍，避免人 / 树影遮挡，保证光照均匀
        - 同一区域固定机位定期采集，便于跨期趋势对比
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行草坪健康评估**
        - 调用 `-m scripts.smyx_lawn_health_assessment_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，绿地场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示草坪健康历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的草坪健康评估报告
        - 包含：健康草坪占比、枯黄草坪占比、杂草覆盖占比、裸土占比、草坪健康综合评分（0-100 分）、健康等级（健康 / 一般 / 衰弱 / 严重退化）、养护方向建议（如"枯黄率偏高 32%，建议检查浇水均匀性、增加补水频次；杂草密度 18%，建议人工除草或选用阔叶草除草剂"）
        - **重要提示**：仅输出基于视觉的指标和通用养护方向，不推荐具体农药品牌；大面积病害或退化建议联系专业草坪养护机构

## 资源索引

- 必要脚本：见 [scripts/smyx_lawn_health_assessment_analysis.py](scripts/smyx_lawn_health_assessment_analysis.py)(用途：调用 API 进行草坪健康评估，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：俯视角度（建议 70°-90°），自然光下避免大片阴影；尽量保持镜头垂直地面，便于面积估算
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供养护决策参考，不推荐具体农药品牌；专业场地（如高尔夫果岭）的精细养护请联系草坪专业团队
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"草坪类别"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`草坪健康评估报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 草坪类别 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 草坪健康评估报告-20260522235500001 | 庭院草坪 | 2026-05-22 23:55:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地草坪俯视图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_lawn_health_assessment_analysis --input /path/to/lawn_top.jpg --open-id your-open-id

# 分析网络草坪图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_lawn_health_assessment_analysis --url https://example.com/lawn.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史草坪报告（自动触发关键词：查看历史草坪报告、历史报告、草坪评估清单等）
python -m scripts.smyx_lawn_health_assessment_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_lawn_health_assessment_analysis --input lawn.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_lawn_health_assessment_analysis --input lawn.jpg --open-id your-open-id --output result.json
```
