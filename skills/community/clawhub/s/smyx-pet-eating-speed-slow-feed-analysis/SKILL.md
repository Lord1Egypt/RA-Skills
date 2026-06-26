---
name: "smyx-pet-eating-speed-slow-feed-analysis"
description: "Triggers when a user provides a video of the pet food-bowl area for analysis; supports local uploads or network URLs to call server-side APIs for eating-speed detection, recording start/end timestamps of feeding, estimating eating speed (g/s and seconds-per-bowl), and when the speed falls below the safety threshold (e.g. < 30 sec/bowl) emitting an intervention signal (slow-feed baffle pop-up or voice prompt) to prevent choking and vomiting (without diagnosing diseases). Application scenarios: smart slow-feeder bowls, pet health management, canine care. | 当用户提供食盆区域视频时，触发本技能进行进食速度检测分析；支持通过上传本地视频或网络视频URL，调用服务端API记录进食开始/结束时间，计算进食速度（克/秒），当低于安全阈值（例如 < 30 秒/碗）时触发外部干预信号（智能慢食碗隔板弹出、语音提醒），预防噎食与呕吐（不诊断疾病）。应用场景：智能慢食碗、宠物健康管理、犬类护理。"
version: "1.0.3"
license: "MIT-0"
---

# Pet Eating Speed Slow Feed Analysis | 宠物进食速度检测与慢食干预

Triggers when a user provides a video of the pet food-bowl area for analysis; supports local uploads or network URLs to
call server-side APIs for eating-speed detection, recording start/end timestamps of feeding, estimating eating speed (
g/s and seconds-per-bowl), and when the speed falls below the safety threshold (e.g. < 30 sec/bowl) emitting an
intervention signal (slow-feed baffle pop-up or voice prompt) to prevent choking and vomiting (without diagnosing
diseases). Application scenarios: smart slow-feeder bowls, pet health management, canine care.

当用户提供食盆区域视频时，触发本技能进行进食速度检测分析；支持通过上传本地视频或网络视频URL，调用服务端API记录进食开始/结束时间，计算进食速度（克/秒），当低于安全阈值（例如 <
30 秒/碗）时触发外部干预信号（智能慢食碗隔板弹出、语音提醒），预防噎食与呕吐（不诊断疾病）。应用场景：智能慢食碗、宠物健康管理、犬类护理。

## 🎯 AI 角色

**你是一个专业的宠物健康行为分析AI。你的任务是基于食盆区域的连续视频，检测宠物进食的开始和结束时间，估算进食速度，并根据预设安全阈值判断是否存在进食过快风险，输出分析结果及干预建议。不要提供疾病诊断，仅客观描述进食行为数据。
**

## 任务目标

- 本 Skill 用于：通过食盆区域视频进行宠物进食速度检测与慢食干预分析，获取标准化的进食时长、进食速度（克/秒）数据，并对进食过快情况输出干预建议，帮助预防噎食与呕吐
- 能力包含：视频分析、进食开始/结束时间检测、进食时长统计、进食速度估算（克/秒）、安全阈值对比（默认 < 30 秒/碗
  触发干预）、噎食/呕吐风险提示、慢食干预建议输出（隔板弹出、语音提醒）
- 触发条件:
    1. **默认触发**：当用户提供食盆区域视频 URL 或文件需要分析时，默认触发本技能进行进食速度检测
    2. 当用户明确需要进行进食行为监测时，提及食盆、慢食碗、进食速度、吃饭太快、噎食、干呕、暴饮暴食、慢食干预等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史进食报告、历史慢食干预报告、进食速度报告清单、查询进食记录、显示所有食盆监测报告、显示进食速度分析报告，查询慢食干预报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有进食报告"、"
       显示所有慢食干预报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_eating_speed_slow_feed_analysis --list` 调用 API
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
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示食盆区域与宠物进食姿态，光线充足、无明显遮挡
        - 建议覆盖完整进食过程（从宠物靠近食盆到离开食盆），便于精准计算进食时长
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行进食速度检测分析**
        - 调用 `-m scripts.smyx_pet_eating_speed_slow_feed_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--list`: 显示进食速度历史分析报告列表清单（可输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的进食行为观察报告
        - 包含：进食开始时间、进食结束时间、进食总时长（秒）、进食速度（克/秒）、是否超阈值（默认 < 30 秒/碗
          判定为过快）、风险等级、慢食干预建议（隔板弹出 / 语音提醒）
        - **重要提示**：仅客观描述进食行为数据与干预建议，不提供疾病诊断或治疗方案

## 进食速度安全参考阈值

| 等级         | 进食时长（每碗）   | 状态描述     | 建议干预          |
|------------|------------|----------|---------------|
| 🚨 过快（高风险） | < 30 秒     | 噎食/呕吐风险高 | 弹出慢食隔板 + 语音提醒 |
| ⚠️ 偏快      | 30 ~ 60 秒  | 需关注      | 语音温和提醒        |
| ✅ 正常       | 60 ~ 300 秒 | 安全       | 无需干预          |
| 💤 偏慢      | > 300 秒    | 关注食欲变化   | 无需干预，但建议记录食欲  |

> 注：以上阈值仅供参考，幼犬/大型犬/部分品种（拉布拉多、金毛等贪食型犬种）天然进食速度偏快，需结合品种与体重综合判断。

## 资源索引

-
必要脚本：见 [scripts/smyx_pet_eating_speed_slow_feed_analysis.py](scripts/smyx_pet_eating_speed_slow_feed_analysis.py)(
用途：调用 API 进行进食速度检测与慢食干预分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB，建议覆盖完整进食过程
- 分析结果仅供健康参考，不提供疾病诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 干预信号（慢食隔板弹出 / 语音提醒）由设备端基于本技能的输出结果实施，本技能仅负责输出干预建议
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 `reportImageUrl` 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`进食速度慢食干预报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 进食速度慢食干预报告-20260522020400001 | 狗 | 2026-05-22 02:04:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地食盆视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_eating_speed_slow_feed_analysis --input /path/to/eating_video.mp4 --pet-type dog

# 分析网络食盆视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_eating_speed_slow_feed_analysis --url https://example.com/eating_video.mp4 --pet-type dog

# 显示历史分析报告清单（自动触发关键词：查看历史进食报告、慢食干预报告清单等）
python -m scripts.smyx_pet_eating_speed_slow_feed_analysis --list

# 输出精简报告
python -m scripts.smyx_pet_eating_speed_slow_feed_analysis --input eating_video.mp4 --pet-type dog --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_eating_speed_slow_feed_analysis --input eating_video.mp4 --pet-type dog --output result.json
```
