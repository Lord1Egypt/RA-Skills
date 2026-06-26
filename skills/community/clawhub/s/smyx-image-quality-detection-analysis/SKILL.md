---
name: "image-quality-detection-analysis"
description: "Detects quality issues in camera footage such as black/white screens, color cast, stripes, noise, and blurriness. Suitable for security surveillance and camera self-check scenarios. | 图像质量检测分析工具，检测摄像头画面出现的全黑、全白、偏色、条纹、雪花、模糊等质量问题，适用于安防监控、摄像头自检等场景"
version: "1.0.1"
---

# Image Quality Assessment Analysis Tool | 图像质量检测分析工具

This capability automatically detects typical image quality issues in camera feeds, such as blackouts, overexposure,
color casts, stripes, snow noise, and blurriness, supporting real-time video stream analysis. Through brightness
histogram analysis, spectral analysis, and color distribution modeling, the system rapidly identifies screen anomalies
and pinpoints the specific problem type. It is suitable for scenarios like daily self-checks of security monitoring
systems and camera operation and maintenance inspections, helping managers promptly identify equipment failures or
environmental interference to ensure the availability and integrity of monitoring data.

本技能可自动检测摄像头画面中出现的全黑、全白、偏色、条纹、雪花、模糊等典型图像质量问题，支持实时视频流分析。系统通过亮度直方图、频谱分析与色彩分布模型，快速识别画面异常并定位问题类型。适用于安防监控系统的日常自检、摄像头运维巡检等场景，帮助管理人员及时发现设备故障或环境干扰，保障监控数据的可用性与完整性。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过摄像头抓拍图片/监控视频帧进行图像质量检测分析，识别各类画面质量问题
- 能力包含：全黑检测、全白检测、偏色检测、条纹干扰、雪花噪声、模糊检测、清晰度评分、质量问题分类
- 触发条件:
    1. **默认触发**：当用户提供图片/视频帧需要检测图像质量时，默认触发本技能进行图像质量分析
    2. 当用户明确需要进行图像质量检测、摄像头自检时，提及图像质量、画面模糊、摄像头黑屏、偏色检测、雪花干扰等关键词，并且上传了图片或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史质量检测报告、图像质量检测报告清单、检测报告列表、查询历史检测报告、显示所有检测报告、图像质量分析报告，查询图像质量检测分析报告
- 自动行为：
    1. 如果用户上传了附件或者图片/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有检测报告"、"显示所有质量报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.image_quality_detection_analysis --list --open-id` 参数调用
          API
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

**在执行图像质量检测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、quality123、camera456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询检测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备图片输入**
        - 提供本地图片/视频文件路径或网络 URL
        - 确保输入为摄像头原始抓拍画面，便于准确检测
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行图像质量检测分析**
        - 调用 `-m scripts.image_quality_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图片/视频文件路径
            - `--url`: 网络图片/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史图像质量检测分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的图像质量检测分析报告
        - 包含：图像基本信息、整体质量评分、检测出的质量问题类型、问题严重程度、校准建议

## 资源索引

- 必要脚本：见 [scripts/image_quality_detection_analysis.py](scripts/image_quality_detection_analysis.py)(用途：调用 API
  进行图像质量检测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供设备维护参考，不能替代专业硬件检修
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"输入类型"、"分析时间"、"质量评分"、"点击查看"五列，其中"报告名称"列使用`图像质量检测分析报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 输入类型 | 分析时间 | 质量评分 | 点击查看 |
  |----------|----------|----------|----------|----------|
  | 图像质量检测分析报告 -20260328221000001 | 图片 | 2026-03-28 22:10:00 |
  85/100 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.image_quality_detection_analysis --input /path/to/capture.jpg --open-id openclaw-control-ui

# 分析网络图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.image_quality_detection_analysis --url https://example.com/camera.jpg --open-id openclaw-control-ui

# 分析监控视频帧（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.image_quality_detection_analysis --input /path/to/monitor.mp4 --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史检测报告（自动触发关键词：查看历史检测报告、历史报告、检测报告清单等）
python -m scripts.image_quality_detection_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.image_quality_detection_analysis --input capture.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.image_quality_detection_analysis --input capture.jpg --open-id your-open-id --output result.json
```
