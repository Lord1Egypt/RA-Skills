---
name: "sport-analysis"
description: "Conducts video safety risk analysis for participants in outdoor sports competitions, long-distance running, marathons, etc.; identifies sports injuries and sudden health risks, outputs professional analysis reports, and provides timely warnings to ensure sports safety. | 户外体育赛事风险分析工具，针对户外体育比赛、长跑马拉松等运动项目的参赛人员进行视频安全风险分析，识别运动损伤和突发健康风险，输出专业分析报告，及时预警保障运动安全"
version: "1.0.2"
---

# Outdoor Sports Event Risk Analysis Tool | 户外体育赛事风险分析工具

Designed specifically for outdoor sports events and long-distance endurance activities such as marathons, this feature
utilizes computer vision and human pose estimation algorithms to conduct real-time video safety risk analysis on
participants. By capturing runners' gait characteristics, body movements, and facial expressions, the system accurately
identifies sports injuries (such as muscle strains and falls) and sudden health risks (such as physical exhaustion and
gait abnormalities). It further conducts comprehensive assessments by integrating physiological data like heart rate
when wearable devices are connected. The system automatically generates professional reports detailing risk levels,
abnormal behavior records, and trend analysis. Upon detecting high-risk conditions, it triggers real-time alerts to
provide a basis for rapid response by event medical teams, comprehensively safeguarding the safety of all participants.

本功能基于先进的计算机视觉与深度学习算法，能够对目标区域内的吸烟行为进行全天候、高精度的自动化监测。系统支持接入实时视频流、静态图片及本地视频文件进行多重检测，通过识别香烟物体、烟雾形态及“手持-口部”的动作特征，有效过滤环境干扰，精准判定违规吸烟行为。一旦检测到异常，系统将立即触发预警机制，通过声光报警或消息推送通知管理人员，实现从被动监控到主动干预的转变，为园区、社区及企事业单位的控烟管理与消防安全提供强有力的技术支撑。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过视频分析对户外体育赛事参赛人员进行运动安全风险评估，识别运动损伤、突发健康不适、意外摔倒等风险情况，提供结构化分析报告和应急处理建议
- 能力包含：视频分析、摔倒损伤识别、身体不适状态识别、伤口出血识别、运动姿态评估、突发风险预警、急救处理建议
- 触发条件:
    1. **默认触发**：当用户提供需要分析的户外体育运动视频 URL 或文件需要进行运动安全风险分析时，默认触发本技能
    2. 当用户明确需要进行户外赛事风险分析、运动损伤识别、跑步安全检查时，提及体育分析、户外运动、赛事风险、运动损伤、跑步摔倒等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史赛事报告、体育风险分析报告清单、运动分析列表、显示所有体育报告，查询户外体育风险分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有体育报告"、"
       显示所有户外赛事风险分析报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.sport_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 户外体育赛事风险分析维度

本技能重点评估以下运动安全风险维度：

### 1. **意外损伤识别**

- **摔倒/跌倒损伤**
    - 正常：运动姿态正常，无摔倒情况
    - 轻度摔倒：失去平衡但快速起身，无明显伤害
    - 中度摔倒：摔倒后无法立即站起，可能有扭伤拉伤
    - 重度摔倒：摔倒后无法站起，需要外界帮助

- **开放性伤口识别**
    - 无伤口：身体表面无明显开放性损伤
    - 轻微擦伤：皮肤表面轻微擦伤，少量渗血
    - 中度伤口：可见明显伤口，持续性流血
    - 重度伤口：大量出血，需要立即急救处理

### 2. **身体不适状态识别**

- **心肺功能异常表现**
    - 正常：呼吸平稳，面色正常，能保持正常运动节奏
    - 轻度不适：呼吸急促，面色稍显苍白，仍能继续运动
    - 中度不适：手扶胸部/胸闷气短，行走困难，需要停下休息
    - 重度不适：胸痛胸闷明显，呼吸困难，无法站立，需要立即急救

- **头晕乏力表现**
    - 正常：步态稳定，精神状态良好
    - 轻度头晕：步伐稍显不稳，仍能自我控制
    - 中度头晕：需要停下休息，无法继续运动
    - 重度头晕：站立不稳，即将或已经跌倒

### 3. **运动姿态与体能评估**

- 跑步姿态评估：正确/膝盖内扣/脚掌着地错误/骨盆倾斜
- 步频步幅分析：合理/步幅过大/步频过低容易疲劳
- 体能透支判断：正常/轻度疲劳/中度疲劳/明显体能透支

### 4. **环境相关风险识别**

- 高温中暑表现：面色潮红/大量出汗/四肢湿冷/意识模糊
- 低温失温表现：全身颤抖/言语不清/肢体麻木
- 地形相关风险：路面湿滑/障碍物绊倒/上坡超负荷/下坡失控

### 5. **常见运动损伤识别**

- 扭伤拉伤：关节异常扭动，疼痛无法继续运动
- 肌肉抽筋：肌肉突然僵硬疼痛，无法正常伸展
- 关节扭伤：踝关节/膝关节扭伤后无法负重
- 脱臼骨折：关节变形，剧痛无法活动

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行户外体育风险分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、sportC113、sport123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询体育风险分析报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示运动员状态、动作表现，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行户外体育赛事风险分析**
        - 调用 `-m scripts.sport_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--analysis-type`: 分析类型，可选值：comprehensive/injury/discomfort/posture/environment，默认
              comprehensive（综合分析）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示户外体育风险分析历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的户外体育赛事风险分析报告
        - 包含：整体运动安全评分、各维度风险等级、损伤风险识别、风险预警、应急处理建议

## 资源索引

- 必要脚本：见 [scripts/sport_analysis.py](scripts/sport_analysis.py)(用途：调用 API 进行户外体育风险分析，本地文件上传，网络
  URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- **重要声明**：本分析仅供运动安全参考，不能替代专业医护人员诊断。运动过程中如遇突发不适请立即停止运动，并及时寻求专业医疗救助。生命安全重于一切！
- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`户外体育风险分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 户外体育风险分析报告-20260312172200001 | 综合分析 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 综合户外体育风险分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sport_analysis --input /path/to/sport_video.mp4 --analysis-type comprehensive --open-id openclaw-control-ui

# 损伤专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sport_analysis --url https://example.com/sport_video.mp4 --analysis-type injury --open-id openclaw-control-ui

# 身体不适专项评估（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sport_analysis --input /path/to/discomfort_video.mp4 --analysis-type discomfort --open-id openclaw-control-ui

# 运动姿态专项评估（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sport_analysis --input /path/to/posture_video.mp4 --analysis-type posture --open-id openclaw-control-ui

# 环境风险专项分析（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.sport_analysis --input /path/to/environment_video.mp4 --analysis-type environment --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史体育报告（自动触发关键词：查看历史体育报告、历史报告、体育报告清单等）
python -m scripts.sport_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.sport_analysis --input video.mp4 --analysis-type comprehensive --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.sport_analysis --input video.mp4 --analysis-type comprehensive --open-id your-open-id --output result.json
```
