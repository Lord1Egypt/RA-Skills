---
name: tts-cleanup-checklist
description: 统一的 TTS 文本清洗与可选章节拆分技能。用于将 Markdown/TXT 清洗为可朗读版本，支持批量处理、可配置清洗档位、质检检查与报告输出。只要用户提到“清洗文本用于 TTS”“按清洗规则处理章节”“去参考文献/引用”“做可朗读稿”“批量清洗章节”，就应优先调用本技能。
---

# tts-cleanup-checklist

用于把 Markdown/TXT 文本清洗为适合语音合成（TTS）朗读的版本。核心目标是：不改变原意、提升可读性、提高朗读自然度。

## 使用方式
当用户要求“清洗用于朗读”时，Agent 直接按本技能执行，不讨论技能制作过程。

## 硬约束（默认始终生效）
- 不压缩内容，不做总结式改写
- 不新增观点，不删除正文有效信息
- 对不确定项做“最小改动”

## 处理模式
- `clean_only`：仅清洗（默认）
- `split_only`：仅章节拆分（无压缩）
- `both`：先章节拆分，再按规则清洗

## 可配置清洗档位
- `reference_trim`: `off` | `tail_only` | `aggressive`（默认 `tail_only`）
- `punctuation_tune`: `off` | `mild` | `strong`（默认 `mild`）
- `number_style`: `keep` | `mixed` | `spoken_cn`（默认 `mixed`）
- `english_alias_policy`: `keep` | `remove_parenthetical` | `transliterate_common`（默认 `remove_parenthetical`）
- `long_sentence_threshold`: 整数，默认 `120`

## 清洗方向（按优先级）

### P0 结构清理（默认必做）
- 去除引用标记（如 `[1]`、`[^2]`）
- 去除 URL 裸链与尾部参考资料区（按 `reference_trim` 档位）
- 去除不参与朗读的目录/导航/分隔符噪声

### P1 噪声修复（默认必做）
- 清理 OCR 噪声（乱码、异常重复符号）
- 修复异常空格（多空格、错位空格、断裂换行）
- 规范标点（连串标点收敛，中英文标点统一）

### P2 可读性转换（默认开启）
- 中英混排降噪，减少朗读卡顿
- 常见缩写转可读表达（按 `english_alias_policy`）
- 保留必要术语，不做过度改写

### P3 数字口语化（默认开启）
- 日期、时间、百分比、数量统一为自然口语读法（按 `number_style`）
- 避免机械逐字符读数字

### P4 韵律优化（默认开启）
- 长句按语义断句（按 `punctuation_tune`）
- 在并列、转折、因果处增加停顿边界
- 断句只优化可听性，不改变语义逻辑

## 可选章节拆分规则（长文推荐）
优先级从高到低：
1. 中文：`序言/前言/引言`、`第X章`、`后记/结语/尾声/致谢`
2. 英文：`Preface/Introduction`、`Chapter X`、`Epilogue/Acknowledgments`
3. 若标题不完整（如单独行 `12` 下一行是标题），自动拼接为章节名
4. 若目录中的章节名与正文冲突，优先正文首次有效出现位置
5. 若无法可靠识别章节，回退为“按语义分段”，并在报告中标注

## Agent 执行步骤
1. 读取输入文本（md/txt，支持单文件或目录批量）。
2. 若模式为 `split_only/both`，先执行章节识别与拆分。
3. 依次执行 P0→P4 清洗（按配置档位）。
4. 生成输出文件。
5. 生成“清洗说明/批量汇总报告”。
6. 执行质检并在报告中记录结果。

## 质检清单（默认必做）
- 是否残留参考文献段（关键词/编号检测）
- 是否存在异常长句（超过 `long_sentence_threshold`）
- 章节连续性（是否漏章/重复章，仅拆分模式）
- 每文件字符数统计（不含空白）

## 单文件输出格式（固定）

```markdown
# 清洗后文本
（正文）

---

# 清洗说明
- 输入文件：<path>
- 模式：<clean_only|split_only|both>
- 应用清洗项：
  - P0: ...
  - P1: ...
  - P2: ...
  - P3: ...
  - P4: ...
- 参数：
  - reference_trim: ...
  - punctuation_tune: ...
  - number_style: ...
  - english_alias_policy: ...
  - long_sentence_threshold: ...
- 质检结果：
  - 参考文献残留：<通过|告警>
  - 异常长句：<数量>
  - 字符数（去空白）：<count>
- 备注：<如有未处理项或不确定项>
```

## 批量输出要求
- 按文件名顺序处理
- 每个文件产出对应清洗稿
- 追加汇总报告，至少包含：成功数/失败数/跳过数、失败原因分类、清洗项命中统计、质检汇总

## 给 Agent 的提示词模板

```text
请按 tts-cleanup-checklist 规则清洗以下文本用于 TTS 朗读：

输入文件：<input_path>
输出文件：<output_path>
模式：<clean_only|split_only|both>
参数：
- reference_trim=<tail_only>
- punctuation_tune=<mild>
- number_style=<mixed>
- english_alias_policy=<remove_parenthetical>
- long_sentence_threshold=<120>

要求：
1) 按 P0→P4 顺序执行清洗。
2) 不改变原意，不压缩内容，不新增观点。
3) 输出“清洗后文本”+“清洗说明”。
4) 若存在不确定处理，采用最小改动并在备注中说明。
5) 输出质检结果。
```

## 批量任务提示词模板

```text
请按 tts-cleanup-checklist 规则批量清洗目录中的章节文件用于 TTS：

输入目录：<input_dir>
匹配：<glob>
输出目录：<output_dir>
模式：both
参数：
- reference_trim=tail_only
- punctuation_tune=mild
- number_style=mixed
- english_alias_policy=remove_parenthetical
- long_sentence_threshold=120

要求：
1) 按文件名顺序处理。
2) 每个文件执行 P0→P4 清洗。
3) 每个文件输出对应清洗稿，并生成汇总报告（成功/失败/跳过、失败原因、清洗项统计、质检统计）。
4) 不改写原意，不压缩正文。
```
