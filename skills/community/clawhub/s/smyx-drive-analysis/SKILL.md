---
name: "drive-analysis"
description: "Analyzes videos of vehicle drivers to identify unsafe driving behaviors. It generates professional analysis reports to help enhance road safety awareness. | 安全驾驶行为分析工具，针对机动车驾驶人员的驾驶行为进行视频分析，识别不安全驾驶行为，输出专业分析报告，提升道路交通安全意识"
version: "1.0.0"
---

# Safe Driving Behavior Analyzer | 安全驾驶行为分析工具

This tool is an intelligent safe driving behavior analysis system specifically designed for motor vehicle operators. By
deeply analyzing video data captured during driving, it precisely identifies unsafe behaviors such as distracted
driving, fatigued driving, and speeding. Based on the analysis results, it generates professional and detailed driving
behavior assessment reports. The system aims to help drivers promptly identify and correct poor driving habits,
comprehensively enhance road safety awareness, and provide technical support for building a safer traffic environment.

本工具是一款专为机动车驾驶人员设计的智能安全驾驶行为分析系统，通过对驾驶过程中的视频数据进行深度解析，精准识别如分心驾驶、疲劳驾驶、超速行驶等不安全行为，并基于分析结果生成专业、详尽的驾驶行为评估报告，旨在帮助驾驶人员及时发现并纠正不良驾驶习惯，全面提升道路交通安全意识，为构建更安全的交通环境提供技术支撑

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过视频分析对驾驶行为进行安全评估，识别不安全驾驶行为模式，提供结构化分析报告和安全驾驶改进建议
- 能力包含：视频分析、疲劳驾驶识别、分心驾驶识别、安全带使用检查、驾驶姿势评估、不良驾驶习惯识别、交通安全建议生成
- 触发条件:
    1. **默认触发**：当用户提供需要分析的驾驶行为视频 URL 或文件需要进行安全驾驶分析时，默认触发本技能
    2. 当用户明确需要进行安全驾驶分析、驾驶行为评估、不良驾驶习惯检查时，提及驾驶分析、安全驾驶、疲劳驾驶、分心驾驶、安全带检查等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史驾驶报告、安全驾驶分析报告清单、驾驶行为分析列表、显示所有驾驶报告，查询安全驾驶分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存到技能目录下 attachments
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有驾驶报告"、"
       显示所有安全驾驶分析报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.drive_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 安全驾驶行为分析维度

本技能重点评估以下安全驾驶行为维度：

### 1. **驾驶员状态评估**

- **疲劳驾驶风险**
    - 正常：精神饱满，眼睛睁开，头部稳定
    - 轻度疲劳：频繁眨眼，打哈欠，头部轻微晃动
    - 中度疲劳：眼睛半闭，点头打瞌睡，反应变慢
    - 重度疲劳：闭眼睡觉，头部严重下垂，完全失去对车辆控制

- **注意力集中度**
    - 专注驾驶：视线持续关注前方道路，注意力集中
    - 轻度分心：偶尔扫视车内仪表盘、后视镜
    - 中度分心：频繁看向左右两侧或车内其他位置
    - 严重分心：长时间不看前方道路

### 2. **关键安全操作检查**

- **安全带使用检查**
    - 正确佩戴：驾驶员全程系好安全带
    - 佩戴不规范：安全带位置错误或未完全系好
    - 未佩戴：全程未系安全带

- **手持设备使用检查**
    - 未使用：双手正常握方向盘，不操作手机
    - 偶尔操作：短时间操作手机/导航
    - 频繁操作：长时间看手机/打字/通话

### 3. **驾驶姿势评估**

- 正常驾驶姿势：坐姿端正，双手正确握持方向盘
- 不良驾驶姿势：
    - 单手握方向盘（单手搭在车窗等）
    - 坐姿倾斜/半躺半坐
    - 身体前倾过度/后仰过度
    - 脚部位置不正确影响操控

### 4. **不良驾驶行为识别**

- **分心类行为**
    - 开车刷短视频/看信息/玩游戏
    - 开车接打电话
    - 频繁调整导航/音乐
    - 与乘车人员过度交谈互动

- **危险类行为**
    - 超速行驶（可识别明显加速超车行为）
    - 频繁变道不打转向灯
    - 跟车过近（车距过近）
    - 抢黄灯/闯红灯行为识别

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行安全驾驶分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、driveC113、drive123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询安全驾驶分析报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示驾驶员状态、操作动作，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行安全驾驶行为分析**
        - 调用 `-m scripts.drive_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径（使用 multipart/form-data 方式上传）
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--analysis-type`: 分析类型，可选值：comprehensive/fatigue/distraction/seatbelt/risk，默认
              comprehensive（综合分析）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示安全驾驶分析历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的安全驾驶分析报告
        - 包含：整体安全评分、各维度评估结果、不良驾驶行为识别、风险预警、安全驾驶改进建议

## 资源索引

- 必要脚本：见 [scripts/drive_analysis.py](scripts/drive_analysis.py)(用途：调用 API 进行安全驾驶分析，本地文件使用
  multipart/form-data 方式上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- **重要声明**：本分析仅供交通安全教育参考，不能替代专业驾驶培训。道路千万条，安全第一条，行车不规范，亲人两行泪！
- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 100MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"分析类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`安全驾驶分析报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 安全驾驶分析报告-20260312172200001 | 综合分析 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 综合安全驾驶行为分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.drive_analysis --input /path/to/drive_video.mp4 --analysis-type comprehensive --open-id openclaw-control-ui

# 疲劳驾驶专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.drive_analysis --url https://example.com/drive_video.mp4 --analysis-type fatigue --open-id openclaw-control-ui

# 分心驾驶专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.drive_analysis --input /path/to/distraction_video.mp4 --analysis-type distraction --open-id openclaw-control-ui

# 安全带专项检查（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.drive_analysis --input /path/to/seatbelt_check.mp4 --analysis-type seatbelt --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史驾驶报告（自动触发关键词：查看历史驾驶报告、历史报告、驾驶报告清单等）
python -m scripts.drive_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.drive_analysis --input video.mp4 --analysis-type comprehensive --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.drive_analysis --input video.mp4 --analysis-type comprehensive --open-id your-open-id --output result.json
```
