---
name: "child-emotion-recognition-analysis"
description: "Identifies negative emotions such as crying, anger, fear, and distress through surveillance footage. It actively issues soothing reminders and notifies parents, making it suitable for homes, kindergartens, and daycare centers. | 儿童情绪识别分析技能，通过监控画面识别儿童哭闹、愤怒、恐惧、委屈等负面情绪，主动发出安抚提醒并通知家长，适用于家庭、幼儿园、托管场所等场景"
version: "1.0.4"
license: "MIT-0"
---

# Child Emotion Recognition Analyzer | 儿童情绪识别分析工具

By analyzing facial expressions, vocal characteristics, and body movements in surveillance footage, this capability
identifies negative emotions in children—such as crying, anger, fear, and distress—in real time. Upon detecting
emotional anomalies, the system actively issues verbal soothing prompts and synchronizes alert notifications to parents'
or caregivers' mobile devices. Ideal for homes, kindergartens, and care centers, it helps caregivers stay informed about
children's psychological states, enhancing both emotional care and safety assurance.

本技能通过分析监控画面中儿童的面部表情、声音特征及肢体动作，实时识别哭闹、愤怒、恐惧、委屈等负面情绪。识别到异常情绪后，系统可主动发出语音安抚提示，并同步推送预警信息至家长或看护人员手机端。适用于家庭、幼儿园、托管场所等场景，帮助照护者及时了解儿童心理状态，提升情感关怀与安全保障能力。

## 演示案例

- [🔗 通过网路视频进行识别分析](https://www.coze.cn/s/1C7uyv2vnck/)
- [🔗 通过上传视频进行识别分析](https://www.coze.cn/s/BXP4CW3eI3o/)
- [🔗 显示历史分析报告](https://www.coze.cn/s/Tjtdye1Hwo8/)

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过监控视频/图片分析，识别儿童的情绪状态，特别关注哭闹、愤怒、恐惧、委屈等负面情绪
- 能力包含：面部表情识别、情绪分类、负面情绪检测、异常情绪预警、自动提醒通知
- 触发条件:
    1. **默认触发**：当用户提供监控视频/图片需要识别儿童情绪时，默认触发本技能进行情绪分析
    2. 当用户明确需要进行儿童情绪识别、情绪监测时，提及儿童情绪、哭闹识别、宝宝哭闹、情绪预警等关键词，并且上传了视频或图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史情绪报告、儿童情绪识别报告清单、情绪报告列表、查询历史情绪报告、显示所有情绪报告、儿童情绪分析报告，查询儿童情绪识别分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有情绪报告"、"显示所有检测报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.child_emotion_recognition_analysis --list`
          参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔐 用户身份处理（内部自动完成）

用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

- 上游系统如有内部身份参数，会由脚本静默接收并使用
- 上游系统未提供时，脚本会自动复用本地缺省用户
- 本地缺省用户不存在时，脚本会自动创建并在后续任务中复用
- 对用户输出时，只展示分析进度、分析结果和报告链接，不展示内部身份值

**关键约束：**

- 不得提示用户输入用户名、手机号或任何内部身份参数
- 不得在回复、报告、示例、错误提示中暴露内部身份值
- 不得把内部身份参数列为用户需要理解或传入的参数
- 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图

---

- 标准流程:
    1. **准备视频/图片输入**
        - 提供本地视频/图片文件路径或网络 URL
        - 确保儿童面部清晰可见，光线充足
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行儿童情绪识别分析**
        - 调用 `-m scripts.child_emotion_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--list`: 显示历史儿童情绪识别分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童情绪识别分析报告
        - 包含：监控基本信息、识别到的情绪类型、情绪强度、是否负面情绪、安抚建议、通知提醒建议

## 资源索引

- 必要脚本：见 [scripts/child_emotion_recognition_analysis.py](scripts/child_emotion_recognition_analysis.py)(用途：调用
  API 进行儿童情绪识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB
- 分析结果仅供参考，不能替代成人看护，紧急情况请及时现场处理
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"输入类型"、"分析时间"、"情绪类型"、"风险等级"、"点击查看"六列，其中"报告名称"列使用`儿童情绪识别分析报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 输入类型 | 分析时间 | 情绪类型 | 风险等级 | 点击查看 |
  |----------|----------|----------|----------|----------|----------|
  | 儿童情绪识别分析报告 -20260328221000001 | 视频 | 2026-03-28 22:10:00 | 哭闹 |
  中风险 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地图片
python -m scripts.child_emotion_recognition_analysis --input /path/to/child.jpg

# 分析网络视频
python -m scripts.child_emotion_recognition_analysis --url https://example.com/monitor.mp4

# 分析监控视频
python -m scripts.child_emotion_recognition_analysis --input /path/to/camera.mp4

# 显示历史分析报告/显示分析报告清单列表/显示历史情绪报告（自动触发关键词：查看历史情绪报告、历史报告、情绪报告清单等）
python -m scripts.child_emotion_recognition_analysis --list

# 输出精简报告
python -m scripts.child_emotion_recognition_analysis --input capture.jpg --detail basic

# 保存结果到文件
python -m scripts.child_emotion_recognition_analysis --input capture.jpg --output result.json
```
