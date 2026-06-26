---
name: "smyx-rose-pest-disease-detection-analysis"
description: "AI-powered pest & disease detection for roses (Rosa spp.). From garden cameras or mobile phone images of leaves, young shoots and flower buds, detects common rose enemies including black spot (black round/irregular spots with yellow halo), powdery mildew (white powdery layer on leaves/shoots), spider mites (tiny red/white dots on leaf back with webbing in severe cases) and aphids (green/black clustered tiny insects on shoots and buds). Outputs pest/disease type, severity grade and general control suggestions. Helps gardeners detect issues early and act in time. Scenarios: home gardens, rose specialty gardens, courtyard landscaping, cut-flower production bases. | 通过庭院摄像头或手机拍摄月季/玫瑰的叶片、嫩芽、花苞图像，利用AI视觉分析技术检测黑斑病（叶面黑色圆形或不规则斑点，周围黄晕）、白粉病（叶片、嫩芽表面白色粉状霉层）、红蜘蛛（叶片背面细小红色或白色点状螨虫，严重时结网）、蚜虫（嫩芽、花苞上绿色或黑色聚集的小虫）等常见病虫害，输出病虫害类型及严重程度，并提供防治建议。该技能有助于月季种植者早期发现问题，及时采取措施。应用场景：家庭花园、月季专类园、庭院绿化、切花生产基地。"
version: "1.0.3"
license: "MIT-0"
---

# Rose Pest & Disease Detection | 月季/玫瑰常见病虫害识别

AI-powered pest & disease detection for roses (Rosa spp.). From garden cameras or mobile phone images of leaves, young shoots and flower buds, detects common rose enemies including black spot (black round/irregular spots with yellow halo), powdery mildew (white powdery layer on leaves/shoots), spider mites (tiny red/white dots on leaf back with webbing in severe cases) and aphids (green/black clustered tiny insects on shoots and buds). Outputs pest/disease type, severity grade and general control suggestions. Helps gardeners detect issues early and act in time. Scenarios: home gardens, rose specialty gardens, courtyard landscaping, cut-flower production bases.

通过庭院摄像头或手机拍摄月季/玫瑰的叶片、嫩芽、花苞图像，利用AI视觉分析技术检测黑斑病（叶面黑色圆形或不规则斑点，周围黄晕）、白粉病（叶片、嫩芽表面白色粉状霉层）、红蜘蛛（叶片背面细小红色或白色点状螨虫，严重时结网）、蚜虫（嫩芽、花苞上绿色或黑色聚集的小虫）等常见病虫害，输出病虫害类型及严重程度，并提供防治建议。该技能有助于月季种植者早期发现问题，及时采取措施。应用场景：家庭花园、月季专类园、庭院绿化、切花生产基地。

## 🎯 AI 角色

**假设你是一个专业的园艺植物保护 AI。你的任务是分析月季或玫瑰的叶片、嫩芽、花苞的高清图像，检测典型病虫害症状（黑斑病、白粉病、红蜘蛛、蚜虫等），识别病虫害类型，评估严重程度（无 / 初期 / 中度 / 严重）。不要提供具体农药商品名，仅输出基于视觉的识别结果和通用防治建议（剪除病叶、改善通风、生物防治方向等）。**

## 任务目标

- 本 Skill 用于：通过月季 / 玫瑰叶片、嫩芽、花苞的图像/视频进行病虫害识别，输出病虫害类型、严重程度及通用防治建议
- 能力包含：黑斑病识别（黑色圆形或不规则斑点 + 黄晕）、白粉病识别（白色粉状霉层）、红蜘蛛识别（叶背细点 + 蛛网）、蚜虫识别（嫩芽 / 花苞密集小虫群）、其他常见症状提示（霜霉、锈病、蓟马等）、严重程度分级（无 / 初期 / 中度 / 严重）、通用防治方向建议（机械防治 / 改善环境 / 生物天敌 / 通用化学防治方向）
- 触发条件:
    1. **默认触发**：当用户提供月季 / 玫瑰叶片、嫩芽、花苞的图像或视频需要病虫害诊断时，默认触发本技能
    2. 当用户明确需要病虫害诊断时，提及月季病害、玫瑰生病、黑斑病、白粉病、红蜘蛛、蚜虫、月季叶子发黄、月季叶子掉、月季虫害、玫瑰防治等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史月季病虫害报告、历史玫瑰报告、月季病虫害报告清单、显示所有月季防治报告、查询玫瑰病害诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有月季病虫害报告"、"显示玫瑰防治报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_rose_pest_disease_detection_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行月季/玫瑰病虫害分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备月季/玫瑰图像/视频输入**
        - 提供本地图像/视频文件路径或网络 URL
        - 建议同时拍摄叶面、叶背、嫩芽、花苞特写，便于识别黑斑、白粉、红蜘蛛、蚜虫等不同位置的症状
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行月季病虫害分析**
        - 调用 `-m scripts.smyx_rose_pest_disease_detection_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，花卉场景使用 other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示月季病虫害历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的月季/玫瑰病虫害分析报告
        - 包含：识别到的病虫害类型（黑斑病 / 白粉病 / 红蜘蛛 / 蚜虫 / 其他可疑症状）、各项严重程度（无 / 初期 / 中度 / 严重）、受害部位（叶面 / 叶背 / 嫩芽 / 花苞）、通用防治建议（如"检测到白粉病初期，建议剪除病叶、改善通风、可选用硫磺类生物制剂喷洒"）
        - **重要提示**：仅输出基于视觉的判断与通用防治方向，不推荐具体农药商品名；大面积或严重虫害建议咨询当地植保部门

## 资源索引

- 必要脚本：见 [scripts/smyx_rose_pest_disease_detection_analysis.py](scripts/smyx_rose_pest_disease_detection_analysis.py)(用途：调用 API 进行月季病虫害识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图像/视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- 拍摄要求：建议在自然光下、距离 20-50 cm 拍摄特写；红蜘蛛需补拍叶背近景，蚜虫需对准嫩芽/花苞聚集区
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供园艺养护参考，不推荐具体农药商品；严重虫害或大面积扩散请咨询当地植保 / 农技部门
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"植物类别"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`月季病虫害识别报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 植物类别 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 月季病虫害识别报告-20260522232400001 | 月季 | 2026-05-22 23:24:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地月季/玫瑰图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_rose_pest_disease_detection_analysis --input /path/to/rose_leaf.jpg --open-id your-open-id

# 分析网络月季/玫瑰图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_rose_pest_disease_detection_analysis --url https://example.com/rose.jpg --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史月季病虫害报告（自动触发关键词：查看历史月季病虫害报告、历史报告、月季防治报告清单等）
python -m scripts.smyx_rose_pest_disease_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_rose_pest_disease_detection_analysis --input rose.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_rose_pest_disease_detection_analysis --input rose.jpg --open-id your-open-id --output result.json
```
