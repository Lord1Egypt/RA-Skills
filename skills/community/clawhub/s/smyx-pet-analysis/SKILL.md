---
name: "pet-analysis"
description: "Triggers when a user provides a video URL or file of a pet (cat/dog/bird) for analysis; supports local video uploads or network URLs to call server-side APIs for health checks, analyzing features like fur, body, and face to identify potential diseases and generate a Pet Safety Guardian health report. | 猫狗宠物健康诊断分析工具，当用户提供猫/狗/鸟等宠物的视频 URL 或文件需要分析时，触发本技能进行宠物健康诊断分析；支持通过上传本地视频或网络视频 URL，调用服务端 API 进行宠物健康检查，分析毛发、身体、脸部等特征，识别潜在疾病并输出宠安卫士健康报告"
---

# Cat & Dog Health Diagnostic Analysis Tool | 猫狗宠物健康诊断分析工具

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过宠物视频进行宠物健康诊断分析，获取结构化的宠安卫士健康报告
- 能力包含：视频分析、毛发特征识别、身体状况评估、面部特征分析、常见疾病预警、健康养护建议生成
- 触发条件:
    1. **默认触发**：当用户提供宠物视频 URL 或文件需要分析时，默认触发本技能进行宠物健康诊断分析
    2. 当用户明确需要进行宠物健康检查时，提及宠物健康、宠物诊断、宠物报告、猫咪健康、狗狗健康、鸟鸟健康等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史宠物报告、历史宠安报告、宠物诊断报告清单、宠物报告清单、查询历史报告、查看宠物报告列表、显示所有宠物报告、显示宠物诊断报告，查询宠安卫士健康报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有宠物报告"、"显示所有宠安报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.pet_analysis --list --open-id` 参数调用 API
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

**在执行宠物健康分析前，必须按以下优先级顺序获取 open-id：**

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
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示宠物整体外观、毛发、面部特征，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行宠物健康分析**
        - 调用 `-m scripts.pet_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/bird/other，默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取, 再通过 SHA-256 算法生成唯一标识传入）
            - `--list`: 显示宠物视频历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的宠安卫士健康报告
        - 包含：宠物基本信息、整体健康状况、毛发分析、身体特征、潜在疾病预警、健康养护建议

## 资源索引

- 必要脚本：见 [scripts/pet_analysis.py](scripts/pet_analysis.py)(用途：调用 API 进行宠物健康分析，本地文件上传(
  https)，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供健康参考，不能替代专业宠医诊断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物健康分析报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物健康分析报告 -20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地猫视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_analysis --input /path/to/cat_video.mp4 --pet-type cat --open-id {SHA-256 算法生成新 open-id}

# 分析网络狗视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_analysis --url https://example.com/dog_video.mp4 --pet-type dog --open-id {SHA-256 算法生成新 open-id}

# 分析本地鹦鹉视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.pet_analysis --input /path/to/bird_video.mp4 --pet-type bird --open-id {SHA-256 算法生成新 open-id}

# 显示历史分析报告/显示分析报告清单列表/显示历史宠安报告（自动触发关键词：查看历史宠物报告、历史报告、宠物报告清单等）
python -m scripts.pet_analysis --list --open-id {SHA-256 算法生成新 open-id}

# 输出精简报告
python -m scripts.pet_analysis --input video.mp4 --pet-type cat --open-id {SHA-256 算法生成新 open-id} --detail basic

# 保存结果到文件
python -m scripts.pet_analysis --input video.mp4 --pet-type dog --open-id {SHA-256 算法生成新 open-id} --output result.json
```
