---
name: "bird-recognition-analysis"
description: "Identifies bird species in images/videos of target areas. Supports recognition of no less than 500 common bird species, supports customized model training, suitable for ecological observation, garden bird watching and other scenarios. | 鸟类识别工具，识别目标区域图片/视频中的鸟类种类，支持不低于500种常见鸟类识别，支持定制化模型训练，适用于生态观测、庭院观鸟等场景"
version: "1.0.3"
license: "MIT-0"
---

# Bird Recognition Tool | 鸟类识别工具

This capability supports automatic bird identification in images or video streams, covering over 500 common species and
capable of distinguishing between similar species and subspecies. Powered by deep learning visual models, the system can
be deployed in ecological observation stations, nature reserves, or home backyards to enable real-time monitoring and
recording of bird species. It also supports customized model training to optimize recognition performance based on
specific regional or species requirements, providing intelligent assistance for bird diversity surveys, birdwatching
hobbies, and ecological conservation.

本技能支持对图片或视频流中的鸟类进行自动识别，覆盖不低于500种常见鸟类，可区分相似种与亚种。系统基于深度学习视觉模型，可部署于生态观测站、自然保护区或家庭庭院等场景，实现鸟种实时监测与记录。同时支持定制化模型训练，根据特定区域或物种需求优化识别效果，为鸟类多样性调查、观鸟爱好及生态保护提供智能辅助。

## 演示案例

- [🔗 通过网路视频进行识别分析](https://www.coze.cn/s/G1iKtMlxvnY/)
- [🔗 通过上传视频进行识别分析](https://www.coze.cn/s/m2Jpzccg5eI/)
- [🔗 显示历史分析报告](https://www.coze.cn/s/3KFhb2lfjd0/)

## 任务目标

- 本 Skill 用于：识别图片/视频中出现的鸟类，准确判定鸟类品种
- 能力包含：鸟类检测、品种分类、置信度评定
- **能力范围**：支持不低于 500 种常见鸟类识别，支持定制化模型训练
- **适用场景**：庭院观鸟、生态观测、野生动物监测、相机陷阱图片识别
- 触发条件:
    1. **默认触发**：当用户提供图片/视频需要识别鸟类品种时，默认触发本技能
    2. 当用户明确需要鸟类识别、鸟种类鉴定时，提及观鸟、鸟类识别、鸟种类识别等关键词，并且上传了图片/视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史识别报告、鸟类识别报告清单、识别报告列表、查询历史识别报告、显示所有识别报告、鸟类分析报告，查询鸟类识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者图片/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有识别报告"、"显示历史鸟类识别"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.bird_recognition_analysis --list --open-id` 参数调用
          API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 识别要求（获得准确结果的前提）

为了获得准确的鸟类识别，请确保：

1. **鸟类完整清晰可见**，避免过度遮挡和远距离模糊拍摄
2. **光照充足**，色彩自然，便于品种特征识别

- 如果是视频，建议截取鸟类清晰停留的片段上传

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行鸟类识别分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备鸟类图片/视频输入**
        - 提供本地文件路径或网络 URL
        - 确保鸟类清晰可见
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行鸟类识别分析**
        - 调用 `-m scripts.bird_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图片/视频文件路径
            - `--url`: 网络图片/视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史鸟类识别分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的鸟类识别分析报告
        - 包含：输入基本信息、检测到的鸟类数量、每个鸟类品种、置信度、科普小知识

## 资源索引

- 必要脚本：见 [scripts/bird_recognition_analysis.py](scripts/bird_recognition_analysis.py)(用途：调用 API
  进行鸟类识别分析，本地文件上传(https)，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 识别结果仅供自然观察参考，物种保护请遵循当地法律法规
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"识别鸟类数"、识别时间"、"点击查看"四列，其中"报告名称"列使用`鸟类识别报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 识别鸟类数 | 识别时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 鸟类识别报告 -20260329005000001 | 3种 | 2026-03-29 00:50 | [🔗 查看报告](https://example.com/report?id=xxx) |

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
# 识别本地鸟类图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.bird_recognition_analysis --input /path/to/bird.jpg --open-id your-open-id

# 识别本地视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.bird_recognition_analysis --input /path/to/forest.mp4 --open-id your-open-id

# 识别网络图片（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.bird_recognition_analysis --url https://example.com/bird.jpg --open-id your-open-id

# 显示历史识别报告/显示识别报告清单列表/显示历史鸟类识别（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.bird_recognition_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.bird_recognition_analysis --input bird.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.bird_recognition_analysis --input bird.jpg --open-id your-open-id --output result.json
```
