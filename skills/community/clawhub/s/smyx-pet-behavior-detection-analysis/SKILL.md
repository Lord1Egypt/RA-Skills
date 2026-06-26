---
name: "pet-behavior-detection-analysis"
description: "Identifies common abnormal pet behaviors such as scratching, biting, destructive chewing, jumping, digging, chasing, and separation anxiety, helping owners understand their pet's habits. | 宠物行为识别技能，识别抓挠、啃咬、拆家、跳跃、刨地、追逐、独处焦虑等常见宠物异常行为，帮助主人了解宠物行为习惯"
version: "1.0.6"
license: "MIT-0"
---

# Pet Behavior Recognition Skill | 宠物行为识别技能

This feature is an intelligent pet health diagnostic system based on deep learning, supporting analysis triggered by
uploading local video files or inputting online video URLs. The system calls high-performance server-side APIs to
perform frame-by-frame analysis of video data for various pets including cats, dogs, and birds, focusing on
multi-dimensional feature extraction of fur condition, body posture, and facial characteristics. By comparing against a
massive veterinary clinical database, the system automatically identifies potential health risks and disease symptoms,
ultimately generating a detailed "Pet Safety Guardian Health Report" to provide pet owners with scientific, intuitive
health references and medical advice.

本技能是一款基于深度学习的宠物健康智能诊断系统，支持通过上传本地视频文件或输入网络视频URL的方式触发分析流程。系统调用服务端高性能API，对猫、狗、鸟等多种宠物的视频数据进行逐帧解析，重点针对毛发状态、身体体态及面部特征进行多维度特征提取。通过比对海量兽医临床数据库，系统能够自动识别潜在的健康风险与疾病征兆，并最终生成一份详尽的“宠安卫士健康报告”，为宠物主人提供科学、直观的健康参考与就医建议

## 任务目标

- 本 Skill 用于：通过视频/监控对宠物进行行为识别分析，识别常见宠物行为尤其是异常行为，输出结构化的宠物行为分析报告
- 支持识别行为：
    - 正常行为：安静休息、正常进食、互动玩耍、慢走散步
    - 异常/问题行为：抓挠家具、啃咬物品、拆家破坏、跳跃、刨地、追逐、独处焦虑（过度舔舐、来回踱步）
- 触发条件:
    1. **默认触发**：当用户提供宠物监控视频 URL 或文件需要进行宠物行为识别时，默认触发本技能
    2. 当用户明确需要进行宠物行为识别，提及抓挠、啃咬、拆家、焦虑行为、宠物行为分析等关键词，并且上传了视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史行为报告、宠物行为分析报告清单、行为识别报告列表、查询历史行为分析
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词，**必须**：
        - 直接使用 `python -m scripts.pet_behavior_detection_analysis --list --open-id` 参数调用 API
          查询云端的历史行为数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行宠物行为识别前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 2 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析

---

- 标准流程:
    1. **准备视频输入**
        - 提供宠物活动监控视频，建议持续时间不少于 1 分钟以统计行为
        - 确保监控画面稳定，完整覆盖宠物活动区域
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行宠物行为识别**
        - 调用 `-m scripts.pet_behavior_detection_analysis` 处理视频（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--duration-min`: 统计时长（分钟），默认自动识别
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示宠物行为识别历史分析报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的宠物行为分析报告
        - 包含：行为统计、异常行为次数、行为时长占比、行为建议

## 资源索引

- 必要脚本：见 [scripts/pet_behavior_detection_analysis.py](scripts/pet_behavior_detection_analysis.py)(用途：调用 API
  进行宠物行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：视频支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供参考，行为矫正建议请咨询专业宠物训练师
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析时间"、"异常行为次数"、"点击查看"四列，其中"报告名称"列使用`宠物行为分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 异常行为次数 | 点击查看 |
  |----------|----------|--------------|----------|
  | 宠物行为分析报告-20260312172200001 | 2026-03-12 17:22:00 | 3 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 📝 隐私与数据安全声明

本技能在处理用户上传的视频时，严格遵守数据安全规范：

- **数据保密处理**：
    - 系统基于 用户名/手机号 生成的标识仅作为用户关联信息，**不保存任何可直接识别个人身份的明文信息**。
- **安全传输**：
    - 所有数据（包括视频文件及关联标识）均通过 **HTTPS/TLS 加密通道** 发送至云端 API 进行分析，防止数据在传输过程中被窃取或篡改。
- **数据留存策略**：
    - 云端服务器遵循“最小必要原则”，**分析任务完成后即刻删除原始视频数据，不进行持久化存储**，确保用户隐私数据不被留存或滥用。

## 使用示例

```bash
# 分析本地监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_behavior_detection_analysis --input /path/to/monitor.mp4 --duration-min 10 --open-id your-open-id

# 分析网络监控视频（以下只是示例，禁止直接使用your-open-id 作为 open-id）
python -m scripts.pet_behavior_detection_analysis --url https://example.com/pet_monitor.mp4 --open-id your-open-id

# 显示历史行为分析报告（自动触发关键词：查看历史行为报告、历史报告、行为报告清单等）
python -m scripts.pet_behavior_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.pet_behavior_detection_analysis --input video.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.pet_behavior_detection_analysis --input video.mp4 --open-id your-open-id --output result.json
```
