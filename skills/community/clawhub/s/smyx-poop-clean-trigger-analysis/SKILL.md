---
name: "smyx-poop-clean-trigger-analysis"
description: "Triggers when a user provides a dog toilet / pet defecation-zone video URL or file for analysis; uses a fixed camera on the dog toilet or designated defecation area to monitor video in real time, detects whether the pet is defecating (presence of feces) and, once the pet leaves the area, automatically outputs a cleaning trigger signal that can drive a robot vacuum to that spot for cleanup. Enables fully automated pet-waste handling, reduces owner workload, and keeps the home hygienic. Application: indoor dog toilets, balcony defecation zones, pet kennels. Does NOT provide medical diagnosis — only outputs vision-based event detection results. | 当用户提供狗厕所或宠物固定排便区域视频URL或文件时，触发本技能进行排便事件检测分析；通过安装在狗厕所或宠物固定排便区域的摄像头实时分析视频，识别宠物是否在该区域排便（粪便出现），并在宠物离开该区域后自动输出清扫触发信号，联动扫地机器人前往清理；实现宠物排泄物的即时自动化处理，减轻主人清理负担，保持居家环境卫生。应用场景：宠物家庭室内狗厕所、阳台排便区、宠物笼舍。仅输出基于视觉的事件检测结果，不进行医疗诊断。"
version: "1.0.0"
---

# Pet Poop Auto-Clean Trigger (Robot Vacuum Integration) | 宠物排便自动清理触发（联动扫地机）

Triggers when a user provides a dog toilet / pet defecation-zone video URL or file for analysis; uses a fixed camera on the dog toilet or designated defecation area to monitor video in real time, detects whether the pet is defecating (presence of feces) and, once the pet leaves the area, automatically outputs a cleaning trigger signal that can drive a robot vacuum to that spot for cleanup. Enables fully automated pet-waste handling, reduces owner workload, and keeps the home hygienic. Application: indoor dog toilets, balcony defecation zones, pet kennels. Does NOT provide medical diagnosis — only outputs vision-based event detection results.

当用户提供狗厕所或宠物固定排便区域视频URL或文件时，触发本技能进行排便事件检测分析；通过安装在狗厕所或宠物固定排便区域的摄像头实时分析视频，识别宠物是否在该区域排便（粪便出现），并在宠物离开该区域后自动输出清扫触发信号，联动扫地机器人前往清理；实现宠物排泄物的即时自动化处理，减轻主人清理负担，保持居家环境卫生。应用场景：宠物家庭室内狗厕所、阳台排便区、宠物笼舍。仅输出基于视觉的事件检测结果，不进行医疗诊断。


## 🎯 AI 角色

**你是一个专业的宠物居家卫生管理AI。你的任务是分析固定在狗厕所或排便区域摄像头的实时视频，检测宠物是否在该区域排便（识别粪便的出现），并在宠物离开该区域后输出清扫触发信号。不进行医疗诊断，仅输出基于视觉的事件检测结果。**

## 任务目标

- 本 Skill 用于：监测狗厕所/固定排便区域视频，识别"宠物进入 → 排便发生 → 宠物离开"完整事件链，并在合适时机输出扫地机清扫触发信号
- 能力包含：宠物入区检测、排便行为识别、粪便目标检出、宠物离区判定、清扫触发信号生成、事件时间戳记录
- 触发条件:
    1. **默认触发**：当用户提供狗厕所/排便区域视频 URL 或文件需要做排便事件检测/自动清扫联动时，默认触发本技能
    2. 当用户明确需要联动扫地机清理时，提及狗厕所、宠物排便、自动清理、扫地机联动、智能家居清洁、宠物粪便检测等关键词，并且上传了视频文件或图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史排便清扫报告、历史清扫触发记录、自动清理报告清单、查询排便事件记录、显示所有清扫触发报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有清扫报告"、"显示历史触发记录"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_poop_clean_trigger_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行排便事件检测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保摄像头固定俯拍狗厕所/排便区域，画面包含整个区域，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行排便事件检测分析**
        - 调用 `-m scripts.smyx_poop_clean_trigger_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示排便清扫触发历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的事件检测报告
        - 包含：宠物入区时间、排便行为开始/结束时间、粪便检出（是/否、估计数量/位置）、宠物离区时间、是否触发清扫信号、清扫触发时间戳、可联动设备建议（扫地机/智能家居平台）
        - **重要提示**：仅输出基于视频的事件检测结果，不提供任何医疗诊断或健康判定

## 资源索引

- 必要脚本：见 [scripts/smyx_poop_clean_trigger_analysis.py](scripts/smyx_poop_clean_trigger_analysis.py)（用途：调用 API 进行排便事件检测与清扫触发分析，本地文件上传，网络 URL 由 API 服务自动下载）
- 配置文件：见 [scripts/config.py](scripts/config.py)（用途：配置 API 地址、默认参数和视频格式限制）
- 领域参考：见 [references/api_doc.md](references/api_doc.md)（何时读取：需要了解 API 接口详细规范和错误码时）

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 清扫触发信号仅为本技能输出的"事件标志"，实际驱动扫地机器人需由用户侧的智能家居网关 / 扫地机 OpenAPI（石头/科沃斯/小米等）实现对接
- 触发去抖：宠物多次进出排便区时，仅在最后一次离开且检出粪便时输出一次清扫触发信号，避免重复派单
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物排便自动清理报告-{记录id}`形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物排便自动清理报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地狗厕所视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_poop_clean_trigger_analysis --input /path/to/dog_toilet.mp4 --pet-type dog --open-id your-open-id

# 分析网络狗厕所视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_poop_clean_trigger_analysis --url https://example.com/dog_toilet.mp4 --pet-type dog --open-id your-open-id

# 显示历史清扫触发报告/分析报告清单列表（自动触发关键词：查看历史清扫报告、清扫触发清单等）
python -m scripts.smyx_poop_clean_trigger_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_poop_clean_trigger_analysis --input toilet.mp4 --pet-type dog --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_poop_clean_trigger_analysis --input toilet.mp4 --pet-type dog --open-id your-open-id --output result.json
```
