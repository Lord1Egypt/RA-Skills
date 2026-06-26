---
name: "diet-analysis"
description: "Analyzes videos to evaluate human eating behaviors, habits, and dietary patterns. It identifies tendencies towards unhealthy eating and provides structured analysis reports along with nutritional improvement recommendations. | 饮食行为健康分析工具，针对人的饮食行为、进食习惯、饮食结构进行视频分析，识别不良饮食行为倾向，提供结构化分析报告和营养改善建议"
version: "1.0.1"
---

# Dietary Behavior Health Analyzer | 饮食行为健康分析工具

Powered by advanced computer vision technology, this personal health management assistant is dedicated to deeply
analyzing users' dietary behaviors and habits through video streams. When users upload dining videos or start real-time
recording, the system automatically tracks and analyzes the entire eating process. It precisely identifies undesirable
behaviors such as wolfing down food, picky eating, and improper posture, while simultaneously performing an intelligent
breakdown of the food types, portion proportions, and nutritional structure on the plate.

本工具是一款基于先进计算机视觉技术的个人健康管理助手，专注于通过视频流深度解析用户的饮食行为与习惯。当用户上传用餐视频或开启实时录制时，系统会自动追踪并分析进食全过程，精准识别狼吞虎咽、挑食偏食、进食姿势不当等不良行为，同时对餐盘中的食物种类、分量比例及营养结构进行智能化拆解。

## 任务目标

- 本 Skill 用于：通过视频分析对饮食行为进行健康评估，识别不良饮食行为模式，提供结构化分析报告和营养改善建议
- 能力包含：视频分析、进食速度评估、进食频率观察、饮食结构识别、进餐习惯评分、不良饮食习惯识别、营养建议生成
- 触发条件:
    1. **默认触发**：当用户提供需要分析的饮食行为视频 URL 或文件需要进行饮食健康分析时，默认触发本技能
    2. 当用户明确需要进行饮食行为分析、进食习惯评估、饮食健康检查时，提及饮食分析、进食习惯、饮食行为、营养评估等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史饮食报告、饮食分析报告清单、饮食行为分析列表、显示所有饮食报告，查询饮食行为分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有饮食报告"、"
       显示所有饮食分析报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.diet_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 饮食行为分析维度

本技能重点评估以下饮食行为维度：

1. **进食速度评估**
    - 过快进食：短时间内大量进食，狼吞虎咽
    - 适中进食：咀嚼充分，节奏均匀
    - 过慢进食：进食时间过长，咀嚼过度

2. **进餐习惯评估**
    - 专注进食：专注用餐，不边吃边玩手机/看电视
    - 分心进食：同时进行多个活动，注意力不集中
    - 进食姿势：坐姿端正/走动进食/其他异常姿势

3. **食物选择与结构**
    - 食物种类识别：主食/蛋白质/蔬菜/油脂分配比例
    - 烹饪方式识别：油炸/清蒸/红烧/生食
    - 份量评估：份量过大/适中/不足

4. **不良饮食行为识别**
    - 暴饮暴食：短时间内摄入大量食物
    - 进食不规律：进餐时间不固定
    - 挑食偏食：明显偏好某类食物，拒绝其他食物
    - 过度节食：进食量明显低于正常需求

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行饮食行为分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 2 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、dietC113、diet123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示进食过程、食物种类、进食动作，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行饮食行为分析**
        - 调用 `-m scripts.diet_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--analysis-type`: 分析类型，可选值：comprehensive/speed/habit/structure/risk，默认 comprehensive（综合分析）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取, 再通过 SHA-256 算法生成唯一标识传入）
            - `--list`: 显示饮食行为分析历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的饮食行为分析报告
        - 包含：整体饮食健康评分、各维度评分、不良饮食习惯识别、风险预警、营养改善建议

## 资源索引

- 必要脚本：见 [scripts/diet_analysis.py](scripts/diet_analysis.py)(用途：调用 API 进行饮食行为分析，本地文件上传(
  https)，网络 URL
  由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- **重要声明**：本分析仅供饮食健康参考，不能替代专业营养师或医师诊断。明确营养问题请尽早咨询专业人士
- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`饮食分析报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 饮食分析报告-20260312172200001 | 综合分析 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 📝 隐私与数据安全声明

本技能在处理用户上传的视频时，严格遵守数据安全规范：

- **数据脱敏处理**：
    - 系统基于用户名/手机号生成的 SHA-256 标识仅作为匿名化脱敏处理后的用户关联信息，**不包含任何可直接识别个人身份的明文信息
      **。
- **安全传输**：
    - 所有数据（包括视频文件及关联标识）均通过 **HTTPS/TLS 加密通道** 发送至云端 API 进行分析，防止数据在传输过程中被窃取或篡改。
- **数据留存策略**：
    - 云端服务器遵循“最小必要原则”，**分析任务完成后即刻删除原始视频数据，不进行持久化存储**，确保用户隐私数据不被留存或滥用。

## 使用示例

```bash
# 综合饮食行为分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.diet_analysis --input /path/to/meal_video.mp4 --analysis-type comprehensive --open-id {SHA-256 算法生成 open-id}

# 进食速度专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.diet_analysis --url https://example.com/meal_video.mp4 --analysis-type speed --open-id {SHA-256 算法生成 open-id}

# 进餐习惯专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.diet_analysis --input /path/to/habit_video.mp4 --analysis-type habit --open-id {SHA-256 算法生成 open-id}

# 显示历史分析报告/显示分析报告清单列表/显示历史饮食报告（自动触发关键词：查看历史饮食报告、历史报告、饮食报告清单等）
python -m scripts.diet_analysis --list --open-id {SHA-256 算法生成 open-id}

# 输出精简报告
python -m scripts.diet_analysis --input video.mp4 --analysis-type comprehensive --open-id {SHA-256 算法生成 open-id} --detail basic

# 保存结果到文件
python -m scripts.diet_analysis --input video.mp4 --analysis-type comprehensive --open-id {SHA-256 算法生成 open-id} --output result.json
```
