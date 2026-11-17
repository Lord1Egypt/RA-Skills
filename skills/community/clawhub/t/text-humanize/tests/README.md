# 验收说明

## 自动化脚本与静态文档测试

在技能目录运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

`test_preflight.py` 实际调用 CLI 和解析函数，覆盖：标题/破折号、默认提示、显式格式约束、strict 退出码、JSON、cut、混合语言引号及 apostrophe、各类代码围栏/行内代码、URL/引用、软换行、语言边界、参数/文件错误、改前改后统计和输入文件不被改动。

`test_documents.py` 只做静态检查：当前 Markdown 链接、参考改名、版本/历史边界、标准库依赖以及行为用例清单结构。它不证明模型遵守指令。

`fixtures/original.md` 与 `fixtures/revised.md` 为手写编辑样例，测试验证同一组 spacing 约束下的真实脚本结果，及样例中披露/引用/精确事实保持不变；它们不是模型行为实测输出。

本次实际执行结果见下方记录。

## 模型行为验收（尚未运行）

[behavior-cases.json](behavior-cases.json) 含 12 个输入与人工判据：正常中英文润色、AI 草稿、披露与引用保留、拒绝伪装错字、拒绝隐藏必要披露、不捏造亲历、保留事实精度、事实冲突待核实、不输出来源概率/过审保证、允许正常结构与标点、虚构标识、只诊断模式。

**状态：NOT RUN。** 本任务未配置模型评测 runner，也未调用付费模型/API。自动化测试通过或清单解析通过都不代表行为实测通过。

后续运行方式：在获授权且配置好模型的独立会话中加载当前 SKILL.md 及所需参考，把每个 prompt 当用户输入，保存模型/版本、参数、输入、实际输出、日期和逐项人工判定；不能用预写答案冒充模型输出。发生未通过时记录问题再修复。此处不预填结果，不承诺平台审核效果。

## 实际运行记录

2026-10-17，用户 Mac，Python 3.13.2，仓库基线 `c04981b21c2bd66233db8c680f9c20f47778dc58`（交付前只读核对远程 main 相同）。

实际命令（仓库根目录）：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/text-humanize/tests -p 'test_*.py' -v
git diff --check
```

真实结果：**44 tests，OK，6.231s**（38 项脚本测试、6 项静态文档测试）；`git diff --check` 无输出，退出码 0。在新增保护区不会制造空格误报的回归后运行了此套完整测试。以上为实际脚本与静态检查结果，未包含模型行为测试。

改前改后样例实际命令（仓库根目录）：

```bash
python3 skills/text-humanize/scripts/preflight-check.py skills/text-humanize/tests/fixtures/original.md --lang zh --strict --check spacing --json
python3 skills/text-humanize/scripts/preflight-check.py skills/text-humanize/tests/fixtures/revised.md --lang zh --strict --check spacing --json
```

| 样例 | 退出码 | FAIL | WARN | 说明 |
|---|---|---|---|---|
| original.md | 1 | 1 | 1 | 显式 spacing 约束检测到标点后空格 |
| revised.md | 0 | 0 | 1 | spacing 已修正；编号标题仅为可选提示 |

样例中的 AI 辅助披露、精确日期 `2026-10-16`、`12 次`、来源链接和引用均保留。该结论只针对手写样例和脚本检查。

另完成：核对本地链接与参考改名；人工扫描当前指令中的旧目标，相关词只出现在禁止/废弃说明或待运行验收输入；程序逐字核对新条目前的历史 CHANGELOG 内容未被改写；程序确认 diff 仅涉及根 README/CHANGELOG 及 skills/text-humanize。后续已同步本地安装目录，修复旧入口与新版参考混用的问题，安装目录完整测试 44/44 通过。

本版本用于 GitHub 仓库更新，不包含 ClawHub 发布、平台申诉或其他 skill 的修改；没有独立模型行为实测、账号恢复或审核通过的结论。
