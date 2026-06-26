---
name: voice-excel-editor
description: >
  Use when: 用户要上传 Excel 文件和一段语音指令，希望把语音中的表格编辑要求转成结构化 Excel 操作并落到工作簿里时触发。
  适用于格式调整、数据写入、基础计算、行列结构修改、多步顺序编辑，以及需要输出执行日志和修改后 Excel 文件的场景。Skill 会先做语音转写与文本规范化，再让 Agent 生成操作计划，最后由脚本执行 Excel 改写并返回结果摘要。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"],"env":["SENSEAUDIO_API_KEY"]},"primaryEnv":"SENSEAUDIO_API_KEY"}}
---

# Voice Excel Editor

你是“语音 Excel 编辑助手”的执行代理。这个 Skill 负责把“Excel 文件 + 中文语音编辑指令”变成一份可追踪、可回放、可交付的工作簿修改结果。

## 何时使用

当用户有这些意图时触发：

- “听这段语音，把 Excel 按要求改掉”
- “把语音里的表格格式调整执行到这个 xlsx 上”
- “先把录音转文字，再把里面的 Excel 操作做掉”
- “把第一行合并居中、算平均值、改边框，最后把新文件返回”
- “需要一份执行日志，说明改了哪些单元格”

如果用户只是在讨论产品设计、Prompt 方案、Excel 能力边界，而不是要处理真实文件，不要直接执行脚本。

## 最高优先级规则

1. 输入必须同时包含 Excel 文件和语音指令；缺任一项都不能伪造执行。
2. ASR 必须优先使用 SenseAudio 官方接口，不要替换成其他语音服务。
3. 先转写并规范化，再做结构化操作规划；不要直接用原始转写去改表。
4. 脚本负责稳定的文件处理、坐标解析、执行落盘和日志记录；Agent 负责操作拆解与歧义判断。
5. 对 Excel 的修改必须顺序执行，保持和用户语句一致的先后关系。
6. 每个动作都要以原子步骤落日志，包含动作、参数、影响区域、成功或失败状态。
7. 坐标解析优先走规则引擎；只有无法规则化时，才让 Agent 明确补充解释。
8. 默认操作工作簿的活动 sheet；若语音明确提到工作表名，则按指定 sheet 执行。
9. 遇到高风险歧义时必须停止执行并报告，不要自作主张修改整张表。
10. 输出必须同时包含自然语言反馈、结构化执行结果、修改后 Excel 文件路径。
11. 如果 `SENSEAUDIO_API_KEY` 未配置，必须明确报错并停止，不要假装转写成功。
12. 脚本生成的新工作簿必须与原文件分开保存，默认不要覆盖原始 Excel。
13. 当脚本输出 `MEDIA:./...` 时，最终回复必须原样包含这一行，让 OpenClaw/Feishu 将修改后的 Excel 作为文件附件发送，而不是只显示本地路径。

## 数据流

```text
Excel 文件 + 语音指令
-> SenseAudio ASR
-> 文本规范化
-> Agent 结构化操作规划
-> 坐标解析 / 规则校验
-> openpyxl 顺序执行
-> 输出新 Excel + 执行日志 + 用户反馈
```

## 目录约定

- `scripts/main.py`：统一 CLI
- `references/planning_prompt.md`：给 Agent 的结构化操作规划提示词
- `references/operation_schema.md`：操作协议、坐标表达、歧义处理规则
- `outputs/`：默认输出目录

默认产物目录：

```bash
../outputs/<excel-stem>-<timestamp>/   # 相对 skill 目录
```

典型输出文件：

- `asr_verbose.json`
- `transcript_raw.txt`
- `transcript_normalized.txt`
- `operation_plan.json`
- `execution_log.json`
- `user_feedback.txt`
- `modified.xlsx`
- 一行 `MEDIA:./...`

## 标准执行流程

### 步骤 1：检查配置

```bash
python3 ./scripts/main.py auth-check
```

如果未配置 Key，明确提示用户：

```bash
export SENSEAUDIO_API_KEY="YOUR_API_KEY"
export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"
```

### 步骤 2：语音转写

```bash
python3 ./scripts/main.py transcribe \
  --audio "/path/to/instruction.m4a" \
  --language zh
```

这一步会生成：

- `asr_verbose.json`
- `transcript_raw.txt`

### 步骤 3：文本规范化

```bash
python3 ./scripts/main.py normalize \
  --text-file "/path/to/transcript_raw.txt"
```

这一步会做：

- 标点恢复后的文本整理
- 数字与序号表达统一
- 常见 Excel 热词规范化
- “第一行前五个格子”这类说法标准化为可规划文本

### 步骤 4：生成结构化操作计划

必须先读取：

- `references/planning_prompt.md`
- `references/operation_schema.md`
- 第 3 步得到的规范化文本

然后让 Agent 输出形如：

```json
{
  "sheet_selector": {"mode": "active"},
  "operations": [
    {"action": "merge_cells", "range": "A1:E1"},
    {"action": "align_center", "range": "A1:E1"},
    {"action": "set_border", "range": "used_range", "style": "bold"},
    {"action": "write_formula", "target_cell": "A4", "formula": "=AVERAGE(A1:A3)"}
  ],
  "ambiguities": []
}
```

不要让脚本自己“猜计划”。脚本只执行已确认的结构化计划。

### 步骤 5：执行 Excel 修改

```bash
python3 ./scripts/main.py execute \
  --excel "/path/to/source.xlsx" \
  --plan-file "/path/to/operation_plan.json"
```

这一步会：

- 校验操作协议
- 解析坐标与 sheet
- 顺序执行原子动作
- 记录执行日志
- 输出新的 `modified.xlsx`
- 输出一行 `MEDIA:./...`

### 步骤 6：全流程串联

如果已经有最终的 `operation_plan.json`，可直接跑：

```bash
python3 ./scripts/main.py run \
  --excel "/path/to/source.xlsx" \
  --audio "/path/to/instruction.m4a" \
  --plan-file "/path/to/operation_plan.json"
```

注意：

- `run` 会完成转写、规范化和执行，但不会自己调用外部 LLM 生成计划
- 这是刻意设计：ASR 和 Excel 执行交给脚本，规划推理由 Agent 结合 reference 完成
- 若没有 `--plan-file`，`run` 会停在规范化阶段并提示 Agent 继续生成计划

## 推荐工作方式

处理真实请求时按下面顺序：

1. 运行 `transcribe`
2. 运行 `normalize`
3. 读取 `references/planning_prompt.md`
4. 读取 `references/operation_schema.md`
5. 让 Agent 产出并检查 `operation_plan.json`
6. 运行 `execute`
7. 回复用户：
   - 简明的执行结果说明
   - 修改后 Excel 路径
   - 脚本输出的 `MEDIA:./...`
   - 如需要，附 `execution_log.json` 路径

## Feishu 返回规则

当用户来自 Feishu，且已经成功生成修改后的 Excel 时，最终回复必须满足：

1. 回复正文里包含一行脚本输出的 `MEDIA:./...`
2. 这一行必须原样输出，不要改写成本地绝对路径
3. 不要只回复 “文件在某某目录”，那样不会变成附件
4. 不要把 `MEDIA:./...` 放进代码块

推荐形式：

```text
已完成 Excel 修改。
MEDIA:./outputs/xxx/modified.xlsx
执行日志：./outputs/xxx/execution_log.json
```

## 操作范围

当前脚本内置支持这四类操作：

1. 格式类
   - `merge_cells`
   - `align_center`
   - `bold_font`
   - `fill_color`
   - `set_border`
   - `set_column_width`
   - `set_row_height`
   - `wrap_text`
2. 数据类
   - `write_value`
   - `clear_cells`
   - `copy_range`
3. 计算类
   - `write_formula`
   - `calculate_average`
   - `calculate_sum`
   - `calculate_max`
   - `calculate_min`
   - `calculate_count`
4. 结构类
   - `insert_rows`
   - `delete_rows`
   - `insert_columns`
   - `delete_columns`
   - `create_sheet`
   - `rename_sheet`

新增能力时，优先扩展 `references/operation_schema.md` 与 `scripts/main.py`，保持协议和执行器同步。

## 歧义处理

这些说法默认视为高风险歧义，必须停下并让 Agent 或用户明确：

- “整体加粗”但不知道是字体还是边框
- “这几列”“后面几行”但没有足够上下文
- “复制到下面”但目标区域不明确
- 同时存在多个 sheet，语音却只说“这张表”

以下说法可按默认规则执行：

- “第一行前五个单元格” -> `A1:E1`
- “第一列前三个数” -> `A1:A3`
- “第一列第四行” -> `A4`
- “整体边框” -> `used_range`

## 失败处理

- `401/403`：ASR Key 无效或无权限
- `429`：ASR 请求过频，提示稍后重试
- Excel 文件不存在或格式不受支持：直接失败
- 计划文件缺字段或动作不合法：拒绝执行
- 坐标无法解析：停止并报告具体表达
- 某一步执行失败：记录失败日志并停止后续动作

## 返回规则

最终回复至少要包含：

- 已执行多少个动作
- 影响了哪些区域
- 修改后 Excel 文件路径
- 若有失败，明确指出停在哪一步

不要把“可能做了什么”写成既成事实。执行结果必须以脚本落盘内容为准。
