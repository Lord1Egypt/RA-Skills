---
name: "package-detection-analysis"
description: "Detects the presence of delivery packages within the target surveillance area; suitable for inventory checks and unattended alerts at community stations, residential entrances, and office building lobbies. | 包裹检测技能，检测目标监控区域内是否出现快递包裹，适用于社区驿站、小区门口、写字楼前台快递盘点和无人值守提醒"
version: "1.0.2"
license: "MIT-0"
---

# Package Detection Skill | 包裹检测技能

Equipped with advanced video analysis algorithms, this feature conducts non-contact intelligent monitoring of daily
activities for patients with chronic diseases such as Parkinson's disease. By capturing and analyzing typical motor
features like limb tremors, convulsions, muscle rigidity, and gait abnormalities, the system automatically identifies
disease fluctuations or potential risks. This technology extends professional clinical observation into the home
setting, helping doctors remotely grasp symptom changes and providing objective evidence for adjusting treatment plans,
thereby achieving a shift from passive medical treatment to active health management.

本功能基于先进的计算机视觉技术，能够对社区驿站、小区门口及写字楼前台等指定监控区域进行全天候智能扫描。系统可精准识别区域内出现的快递包裹，自动判断包裹的有无及滞留状态。该功能完美适配快递盘点与无人值守提醒场景，一旦检测到新包裹到达或异常滞留，即刻触发通知，有效解决了传统人工巡查效率低、易漏件的问题，显著提升了物流末端的管理效率与安全性

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：检测图片/视频监控场景中的快递包裹，统计包裹数量，长时间未取件触发提醒
- 能力包含：包裹检测、数量统计、位置标定、超时未取提醒
- **适用场景**：社区驿站包裹盘点、小区门口快递监测、写字楼前台快递管理、家门口无人值守快递提醒
- 支持检测：快递盒、包裹袋、信封等各类快递包裹
- 触发条件:
    1. **默认触发**：当用户提供监控图片/视频需要检测快递包裹时，默认触发本技能
    2. 当用户明确需要包裹检测、快递盘点时，提及包裹检测、快递识别、驿站盘点、未取包裹等关键词，并且上传了图片/视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史检测报告、包裹检测报告清单、检测报告列表、查询历史检测报告、显示所有检测报告、包裹分析报告，查询包裹检测分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有检测报告"、"显示历史包裹记录"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.package_detection_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 检测要求（获得准确结果的前提）

为了获得准确的包裹检测，请确保：

1. **监控摄像头固定位置**，覆盖驿站/门口/前台指定摆放区域
2. **光线充足清晰**，包裹完整可见，避免被桌椅和杂物大面积遮挡
3. 定期盘点场景建议固定时段拍摄，便于统计对比

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行包裹检测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、package123、express456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询检测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备监控图片/视频输入**
        - 提供本地文件路径或网络 URL
        - 确保包裹摆放区域完整可见
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行包裹检测分析**
        - 调用 `-m scripts.package_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图片/视频文件路径
            - `--url`: 网络图片/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史包裹检测分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的包裹检测分析报告
        - 包含：输入基本信息、检测到的包裹数量、每个包裹位置标注、是否有超时未取件、管理建议

## 资源索引

- 必要脚本：见 [scripts/package_detection_analysis.py](scripts/package_detection_analysis.py)(用途：调用 API
  进行包裹检测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"包裹数量"、"检测时间"、"是否有超时"、"点击查看"五列，其中"报告名称"列使用`包裹检测报告-{记录id}`形式拼接, "
  点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 包裹数量 | 检测时间 | 是否有超时 | 点击查看 |
  |----------|----------|----------|------------|----------|
  | 包裹检测报告 -20260329001400001 | 3件 | 2026-03-29 00:14 |
  1件超24小时 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 检测本地驿站监控图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.package_detection_analysis --input /path/to/station.jpg --open-id openclaw-control-ui

# 检测本地监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.package_detection_analysis --input /path/to/entrance.mp4 --open-id openclaw-control-ui

# 检测网络图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.package_detection_analysis --url https://example.com/front_desk.jpg --open-id openclaw-control-ui

# 显示历史检测报告/显示检测报告清单列表/显示历史包裹检测（自动触发关键词：查看历史检测报告、历史报告、检测报告清单等）
python -m scripts.package_detection_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.package_detection_analysis --input station.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.package_detection_analysis --input station.jpg --open-id your-open-id --output result.json
```
