---
name: "smyx-uav-farm-health-index-map-analysis"
description: "Using multispectral or high-resolution RGB cameras mounted on agricultural UAVs to capture orthophotos or mosaics of farmland, AI models compute vegetation indices (e.g., NDVI, NDRE) and generate a farm health-index heatmap, where colors distinguish crop vigor (red = poor, yellow = medium, green = healthy). | 通过农业无人机平台搭载的多光谱或高分辨率RGB相机，采集农田的正射影像或拼接图，利用AI模型计算植被指数（如归一化植被指数NDVI、归一化红边指数NDRE等），生成农田健康指数热力图，用颜色区分作物长势（红色代表健康差、黄色代表中等、绿色代表健康）。该技能可快速识别问题区域（如缺肥、缺水、病虫害、杂草），指导精准变量施肥或植保作业。"
version: "1.0.1"
license: "MIT-0"
---

# UAV Farm Health Index Map | 无人机农田健康指数图生成

Using multispectral or high-resolution RGB cameras mounted on agricultural UAVs to capture orthophotos or mosaics of farmland, AI models compute vegetation indices (e.g., NDVI, NDRE) and generate a farm health-index heatmap, where colors distinguish crop vigor (red = poor, yellow = medium, green = healthy). This skill quickly identifies problem zones (e.g., nutrient/water deficiency, pests/disease, weeds) and guides precision variable-rate fertilization and crop-protection operations. Application scenarios: large-scale farms, agricultural cooperatives, drone crop-protection services, agricultural research. After the UAV flight uploads imagery, the system automatically produces a health-index map, outputs coordinates and area of problem zones, and pushes suggestions (e.g., 'NDVI is low in the northeast corner, recommend on-site pest inspection'). Skill features: traditional manual field scouting is slow and tends to miss early stress. UAV-based health-index heatmaps drastically improve monitoring efficiency, enable precise variable-rate operations, and save agro-inputs. A core technology of smart agriculture.

通过农业无人机平台搭载的多光谱或高分辨率RGB相机，采集农田的正射影像或拼接图，利用AI模型计算植被指数（如归一化植被指数NDVI、归一化红边指数NDRE等），生成农田健康指数热力图，用颜色区分作物长势（红色代表健康差、黄色代表中等、绿色代表健康）。该技能可快速识别问题区域（如缺肥、缺水、病虫害、杂草），指导精准变量施肥或植保作业。应用场景：规模化农场、农业合作社、植保无人机服务、农业科研。无人机飞行后上传影像，系统自动生成健康指数图，输出问题区域的坐标和面积，并推送建议（如'东北角区域NDVI偏低，建议实地检查虫害'）。技能特点：传统农田巡查依赖人工，效率低且难以发现早期胁迫。通过无人机快速生成健康指数热力图，可大幅提高监测效率，实现精准农业变量作业，节省农药肥料。该技能是智慧农业的核心技术之一。

## 🎯 AI 角色

**假设你是一个专业的精准农业 AI。你的任务是接收无人机航拍的多光谱（或高分辨率 RGB）图像，经过拼接和几何校正后，计算植被指数（如 NDVI、NDRE、OSAVI 等），生成农田健康指数热力图，并识别出健康异常区域（如低植被指数区域），输出其位置和面积。不要提供具体的农事操作建议（如施肥量、农药品种），仅输出基于指数的评估结果。**

## 任务目标

- 本 Skill 用于：基于无人机航拍正射影像/拼接图，计算植被指数并生成农田健康指数热力图，输出异常区域坐标与面积
- 能力包含：影像拼接 / 几何校正、植被指数计算（NDVI / NDRE / OSAVI / GNDVI / VARI / ExG）、健康指数热力图渲染（红/黄/绿三段色阶）、异常区域分割（低指数低健康）、问题区域坐标多边形与面积估算（ha）、作物覆盖率统计、高/中/低健康占比
- 触发条件:
    1. **默认触发**：当用户提供无人机航拍正射影像/拼接图/视频 URL 或文件需要分析时，默认触发本技能进行农田健康指数图生成
    2. 当用户明确提及无人机、UAV、多光谱、NDVI、NDRE、植被指数、农田巡查、精准农业、变量施肥、健康指数图、健康热力图、问题区域、长势监测等关键词，并且上传了影像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看农田健康指数历史报告、植被指数报告清单、无人机巡田报告清单、查询历史健康指数图、显示所有农田健康指数报告、显示长势监测诊断报告，查询异常区域清单
- 自动行为：
    1. 如果用户上传了附件或者影像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有农田健康指数报告"、"
       显示所有植被指数报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_uav_farm_health_index_map_analysis --list --open-id` 参数调用 API
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

**在执行无人机农田健康指数图生成前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备无人机航拍影像输入**
        - 提供本地正射影像/拼接图/视频文件路径或网络 URL
        - 推荐多光谱（含 NIR / Red Edge 波段）或高分辨率 RGB；含 EXIF/GeoTag 定位信息更佳
        - 飞行建议：高度 80-120m、重叠 ≥ 70%、晴朗弱风时段
        - 可选附带：作物种类（小麦/玉米/水稻等）、田块边界、生育期
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行农田健康指数图生成**
        - 调用 `-m scripts.smyx_uav_farm_health_index_map_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地无人机正射影像/拼接图/视频文件路径
            - `--url`: 网络无人机正射影像/拼接图/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，农田航拍场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示农田健康指数图历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的农田健康指数图报告
        - 包含：健康指数热力图 URL（red/yellow/green 三段色阶）、整体平均植被指数（mean_ndvi）、异常区域列表（low_health_zones：坐标多边形 + 面积 ha）、作物覆盖率（coverage_ratio）、高/中/低健康占比（field_stats）
        - **重要提示**：仅输出基于植被指数的评估结果与异常区域，不输出具体农事操作建议（施肥量、农药品种等）

## 资源索引

- 必要脚本：见 [scripts/smyx_uav_farm_health_index_map_analysis.py](scripts/smyx_uav_farm_health_index_map_analysis.py)(
  用途：调用 API 进行无人机农田健康指数图生成，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、支持的植被指数和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/tiff 影像或 mp4/avi/mov 视频，最大 10MB；建议提前完成拼接或上传单张高质量正射影像
- 多光谱影像需包含 NIR 波段才能计算 NDVI/NDRE 等真植被指数；纯 RGB 影像将回退使用 VARI/ExG
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅作为田块管理与变量作业的参考，实际作业请结合现场实地踏查
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"作物种类"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`无人机农田健康指数图报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 作物种类 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 无人机农田健康指数图报告-20260312172200001 | 小麦 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地无人机正射影像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_uav_farm_health_index_map_analysis --input /path/to/orthomosaic.tif --open-id your-open-id

# 分析网络无人机航拍影像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_uav_farm_health_index_map_analysis --url https://example.com/orthomosaic.tif --open-id your-open-id

# 显示历史健康指数图报告/植被指数报告清单（自动触发关键词：查看农田健康指数历史报告、植被指数报告清单等）
python -m scripts.smyx_uav_farm_health_index_map_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_uav_farm_health_index_map_analysis --input ortho.tif --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_uav_farm_health_index_map_analysis --input ortho.tif --open-id your-open-id --output result.json
```
