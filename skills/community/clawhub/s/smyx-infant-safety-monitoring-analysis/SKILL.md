---
name: "infant_safety_monitoring_analysis"
description: "Monitors infant behavior via visual AI, automatically identifying high-risk actions like rolling over, mouth/nose obstruction, climbing, or falling from bed, and triggers instant safety warnings. | 婴儿智能安全看护技能，基于视觉AI实时监测婴儿行为，自动识别翻身、口鼻遮挡、攀爬、翻越围栏、坠床等高风险动作，即时触发安全预警，守护婴幼儿睡眠与活动安全"
version: "1.0.5"
---

# Smart Baby Safety Care Skill | 婴儿智能安全看护技能

Leveraging high-precision sensors and AI vision algorithms, this feature conducts comprehensive, real-time monitoring of
infant sleep and activity states. The system automatically identifies sleep hazards such as turning over or nose and
mouth occlusion, as well as dynamic dangerous behaviors like climbing, fence crossing, and falling from bed. Upon
detecting these high-risk actions, the device instantly triggers safety alerts to notify parents, achieving a shift from
passive supervision to active protection, and building a solid safety line of defense for infant sleep and activity.

该功能通过高精度传感器与AI视觉算法，对婴幼儿的睡眠及活动状态进行全方位实时监测。系统能够自动识别翻身、口鼻遮挡等睡眠隐患，以及攀爬、翻越围栏、坠床等动态危险行为。一旦检测到上述高风险动作，设备将即时触发安全预警通知家长，实现从被动看护到主动防护的转变，为婴幼儿构建一道坚实的睡眠与活动安全防线

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过婴儿活动视频进行智能安全看护分析，识别高风险动作，生成安全看护预警报告
- 能力包含：视频分析、翻身监测、口鼻遮挡识别、攀爬行为检测、围栏翻越识别、坠床风险预警、安全看护建议生成
- 触发条件:
    1. **默认触发**：当用户提供婴儿活动视频 URL 或文件需要进行安全监测分析时，默认触发本技能进行婴儿安全看护分析
    2. 当用户明确需要进行婴儿安全看护、婴儿行为监测、风险预警，提及婴儿安全、看护分析、翻身监测、坠床预警、口鼻遮挡等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史安全报告、历史看护报告、婴儿安全报告清单、查询历史报告、查看看护报告列表、显示所有安全报告、显示婴儿安全分析报告，查询婴儿安全看护报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有安全报告"、"显示所有看护报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.infant_safety_monitoring_analysis --list --open-id` 参数调用 API
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

**在执行婴儿安全看护分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、infant123、baby456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询婴儿安全看护报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示婴儿活动区域，画面稳定，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行婴儿安全看护分析**
        - 调用 `-m scripts.infant_safety_monitoring_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--infant-age-group`: 婴儿年龄段，可选值：newborn(0-3个月), infant(3-12个月), toddler(1-3岁), other，默认
              other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示婴儿安全看护历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的婴儿安全看护预警报告
        - 包含：婴儿基本信息、监测场景、风险行为识别结果、高风险动作预警、安全看护建议

## 资源索引

- 必要脚本：见 [scripts/infant_safety_monitoring_analysis.py](scripts/infant_safety_monitoring_analysis.py)(用途：调用 API
  进行婴儿安全看护分析，本地文件使用
  支持文件上传 方式上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供安全参考，不能替代专业看护和家长实时监护
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"婴儿年龄段"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`婴儿安全看护分析报告-{记录id}`形式拼接, "
  点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 婴儿年龄段 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 婴儿安全看护分析报告 -20260312172200001 | 3-12个月 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地新生儿视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_safety_monitoring_analysis --input /path/to/baby_video.mp4 --infant-age-group newborn --open-id openclaw-control-ui

# 分析网络婴儿视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_safety_monitoring_analysis --url https://example.com/baby_video.mp4 --infant-age-group infant --open-id openclaw-control-ui

# 分析本地学步期宝宝视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_safety_monitoring_analysis --input /path/to/toddler_video.mp4 --infant-age-group toddler --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史看护报告（自动触发关键词：查看历史安全报告、历史报告、安全报告清单等）
python -m scripts.infant_safety_monitoring_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.infant_safety_monitoring_analysis --input video.mp4 --infant-age-group infant --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.infant_safety_monitoring_analysis --input video.mp4 --infant-age-group toddler --open-id your-open-id --output result.json
```
