---
name: "elderly-fall-detection-analysis"
description: "Utilizes vision and radar technology for contactless detection of falls. It triggers alarms within seconds and is suitable for home safety monitoring of elderly people living alone. | 老人跌倒检测技能，视觉/雷达无感识别摔倒倒地，秒级触发报警，适用于独居老人居家安全监测场景"
version: "1.0.4"
license: "MIT-0"
---

# Elderly Fall Detection Skill | 老人跌倒检测技能

By fusing advanced computer vision with millimeter-wave radar technology, this solution achieves imperceptible yet
precise monitoring of accidents such as falls for seniors living alone. The system automatically identifies abnormal
postures and triggers an instant alarm within seconds. Providing 24/7, high-reliability safety protection for home care
scenarios, it operates without requiring the elderly to wear any devices and strictly preserves their privacy. This
effectively shortens emergency response times and safeguards the lives of the elderly.

该方案通过融合先进的计算机视觉与毫米波雷达技术，实现了对独居老人摔倒、倒地等意外事件的无感化精准监测。系统能够在秒级时间内自动识别异常姿态并即时触发报警机制，在完全无需老人佩戴任何设备、不侵犯隐私的前提下，为居家养老场景提供全天候、高可靠的安全守护，有效缩短救援响应时间，保障老年人的生命安全

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：在监控画面中识别老人跌倒、摔倒、倒地不起异常事件
- 能力包含：人体检测、姿态判断、跌倒识别、异常秒级报警
- 技术支持：视觉视频检测 + 雷达辅助无感识别，无需穿戴设备
- **响应速度**：秒级检测识别，发现异常立即触发报警
- **适用场景**：独居老人居家安全监测、养老院老人活动区域监测
- 触发条件:
    1. **默认触发**：当用户提供监控图片/视频需要检测老人跌倒时，默认触发本技能
    2. 当用户明确需要跌倒检测、老人安全监测时，提及老人跌倒、摔倒检测、倒地报警、跌倒报警等关键词，并且上传了图片/视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史跌倒报告、跌倒检测报告清单、检测报告列表、查询历史跌倒报告、显示所有跌倒报告、老人跌倒分析报告，查询老人跌倒检测分析报告
- 自动行为：
    1. 如果用户上传了附件或者图片/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有跌倒报告"、"显示所有报警记录"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.elderly_fall_detection_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 监测要求（获得准确结果的前提）

为了获得准确及时的跌倒检测，请确保：

1. **摄像头覆盖完整活动区域**，老人活动范围在监控画面内
2. **光线充足**，避免大面积阴影遮挡
3. 支持固定角度摄像头，最适合浴室、客厅、卧室等老人常活动区域

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行老人跌倒检测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、fall123、elderly456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询跌倒检测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备监控输入**
        - 提供本地图片/短视频文件路径或网络 URL
        - 确保摄像头覆盖完整活动区域
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老人跌倒检测分析**
        - 调用 `-m scripts.elderly_fall_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图片/视频文件路径
            - `--url`: 网络图片/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史老人跌倒检测分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的老人跌倒检测分析报告
        - 包含：监控基本信息、检测结果、是否跌倒、跌倒位置、置信度、报警等级、应急建议

## 资源索引

- 必要脚本：见 [scripts/elderly_fall_detection_analysis.py](scripts/elderly_fall_detection_analysis.py)(用途：调用 API
  进行老人跌倒检测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png/mp4/avi/mov，视频推荐短时连续帧，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **⚠️ 重要提示**：本检测结果仅供安全预警参考，不能替代人工确认，发现跌倒报警请立即电话联系核实并应急处理
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"输入类型"、"分析时间"、"检测结果"、"报警等级"、"点击查看"六列，其中"报告名称"列使用`老人跌倒检测报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 输入类型 | 分析时间 | 检测结果 | 报警等级 | 点击查看 |
  |----------|----------|----------|----------|----------|----------|
  | 老人跌倒检测报告 -20260328221000001 | 视频 | 2026-03-28 22:10:00 | 未检测到跌倒 |
  安全 | [🔗 查看报告](https://example.com/report?id=xxx) |
  | 老人跌倒检测报告 -20260328221500001 | 图片 | 2026-03-28 22:15:00 | 检测到跌倒 |
  紧急报警 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地监控图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.elderly_fall_detection_analysis --input /path/to/room.jpg --open-id openclaw-control-ui

# 分析本地监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.elderly_fall_detection_analysis --input /path/to/living_room.mp4 --open-id openclaw-control-ui

# 分析网络视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.elderly_fall_detection_analysis --url https://example.com/monitor.mp4 --open-id openclaw-control-ui

# 显示历史跌倒检测报告/显示检测报告清单列表/显示历史跌倒报警（自动触发关键词：查看历史跌倒报告、历史报告、跌倒报告清单等）
python -m scripts.elderly_fall_detection_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.elderly_fall_detection_analysis --input monitor.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.elderly_fall_detection_analysis --input monitor.mp4 --open-id your-open-id --output result.json
```
