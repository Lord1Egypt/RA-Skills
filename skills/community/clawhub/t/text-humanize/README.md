# Text Humanize

中英文清晰表达与风格润色 · **1.5.1**

改善清晰度、冗余、结构、语气、节奏、修辞和排版，保留原意、事实、引语、引用和必要披露。支持诊断与对照改写，以及短文、长文、文学体裁适配。正常 AI 草稿也可以润色；不判断作者来源，不以绕检测、规避审核或隐藏必要披露为目标，不承诺过审。

完整流程见 [SKILL.md](SKILL.md)，中文与英文风格分别见 [style-patterns-cn.md](references/style-patterns-cn.md)、[style-patterns-en.md](references/style-patterns-en.md)，修辞见 [rhetoric-cn.md](references/rhetoric-cn.md)、[lyrical-appositive.md](references/lyrical-appositive.md)。旧版目录名和行为已废弃，历史记录不作为当前指令。

使用示例：

- 「帮我删掉这段的重复表达，保留日期和引用。」
- 「保持正式语气，把这篇文章的层次理清楚。」
- 「检查这段抒情文字的意象是否连贯，不添加亲历。」
- “Edit this draft for clarity; keep the AI-use disclosure and citations.”

标题、编号列表、平衡观点、正确语法和破折号都允许。没有固定错字量、语气词量、句数或段数要求。存疑事实在编辑说明中交作者核实，不模糊日期或编造出处。

## 获取与使用

从 GitHub 获取仓库，将 `skills/text-humanize/` 作为 agent skill 加载；更新已有安装时，请同步整个目录，避免入口、参考和脚本版本不一致。

```bash
git clone https://github.com/Songhonglei/better-office-work-flow.git
```

GitHub 与 ClawHub 的发布状态独立；本次更新不包含 ClawHub 发布。

## 检查脚本

Python 3 标准库，无依赖，读取文件且不改正文。以下命令在本技能目录执行：

```bash
python3 scripts/preflight-check.py draft.md
python3 scripts/preflight-check.py draft.md --tier literary --json
python3 scripts/preflight-check.py revised.md --cut '## 本轮改动'
# 用户明确选定格式约束后才启用：
python3 scripts/preflight-check.py revised.md --lang zh --strict --check spacing
# 对改前改后用相同参数，比较真实输出：
python3 scripts/preflight-check.py tests/fixtures/original.md --lang zh --strict --check spacing --json
python3 scripts/preflight-check.py tests/fixtures/revised.md --lang zh --strict --check spacing --json
```

| 级别 | 含义 | 影响退出码 |
|---|---|---|
| INFO | 原始统计，不设质量阈值 | 否 |
| WARN | 可选格式或段长提示，须结合语境 | 否，`--strict` 也不把一般 WARN 算失败 |
| FAIL | `--strict` 下显式选定格式约束的超限项 | 是 |

默认所有输出均为 INFO / WARN。`--strict` 不选择 `--check` 时也不会因文风失败，并明确提示。`--check` 可重复：

| 参数值 | 含义 |
|---|---|
| quotes | 未保护区域的半角引号体例（可识别成对引语已排除，不强改引文） |
| punctuation | 中文后半角逗号/句点、三点省略号体例 |
| spacing | 中文标点和破折号周边空格体例 |
| dashes | 中文正文使用双 em dash 的体例，仅检查形态、不禁止破折号 |
| numbered-headings | 禁用编号行的显式格式要求（粗计包含编号标题和列表，选择前确认范围） |

标点约束只在中文模式适用；`--lang auto` 的口径为 CJK / (CJK + Latin) **>50%**，等于 50% 不启用，`--lang zh|en` 可覆盖。无字母时不作语言推断。英文片段、URL、代码、Markdown 引用及可识别的成对行内引语被保护，不因 apostrophe 或英文标点失败。JSON 保留 `file/tier/cjk/cjk_ratio/zh_mode/rows/fail/warn`，新增 `strict/checks/cut_found/notes` 与逐行 `check`，支持机器读取。

`--para-max` 默认 70，仅供段长提示，不影响严格模式；必须为正整数。`--lyrical` 加修辞统计；`--tier long|literary` 加 SS-CN8 节奏观察，`short` 不加。R 类和 SS-CN8 全为 INFO，不设质量阈值。20/22 CJK 仅为段尾和多逗号短句的统计分组，不能解释为质量阈值；详见 [中文参考](references/style-patterns-cn.md)。

退出码：`0` 无选定格式失败，`1` 有选定格式失败，`2` 参数或文件读取错误。`0` 不证明文稿质量、作者来源、事实准确或审核通过。引号计数只能提示核对原文件，不能断定转录污染。

## 解析范围与限制

- 支持三个及以上反引号或波浪线围栏，同字符且至少原长度才闭合；未闭合围栏保护到文件结尾。支持多反引号行内代码和缩进代码。
- 屏蔽 URL、Markdown 链接目标、引用定义、引用块及其懒续行、成对行内引语，保留链接标签。原始引号统计保留行内引语的分隔符，但不用于失败判断。
- 正文段落以空行划分，段内软换行合并，标题、列表、引用、表格不算正文。中英文软换行的处理用于统计，不写回原文。诗歌的分行需要人工阅读。
- 这是保守的 Markdown/语言启发式，非完整解析器。复杂嵌套引用、HTML、深层括号链接或中英标点混合可能漏计或误计；保护范围也可能让检查漏掉格式问题。对引文内的排版要求应人工核对，不能为了清零损伤原文。
- 同位语和多逗号句粗计不识别语法，词频不等于冗余。脚本不自动润色、不校验事实、不调用模型。
- `--cut` 按原文件首个字面标记截断，包括标记若出现在代码中的情况；未找到则统计全文并提示。

## 测试与历史

运行：`python3 -m unittest discover -s tests -p 'test_*.py' -v`。具体覆盖、行为验收与状态见 [tests/README.md](tests/README.md)。脚本测试和静态文档检查可以自动执行；模型行为用例没有模型运行配置时只登记为未运行，不能宣称行为实测通过。

[CHANGELOG.md](CHANGELOG.md) 保留历史，1.5.0 明确废弃旧的伪装与来源判定规则。MIT，见 [LICENSE](LICENSE)。Evan Song · [GitHub](https://github.com/Songhonglei)。
