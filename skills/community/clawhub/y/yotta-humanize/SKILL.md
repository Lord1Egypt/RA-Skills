---
name: yotta-humanize
slug: yotta-humanize
version: 0.2.5
displayName: 去 AI 味·元真
summary: 粘贴中文草稿，先看 0-100 AI 味评分，再按确定性规则改掉套话、AI 黑话、机械排比和聊天残渣；零依赖、本地运行。
description: '去 AI 味（元真）—— 把像 AI 写的中文改得更自然：粘贴文章、文案、报告或邮件，先得到 0-100 AI 味评分，再定位空泛升华、套话、AI 黑话、同义堆叠、机械排比、聊天残渣和标点滥用，输出可逐条核对的前后改写（词表替换 / 套话删除 / 残渣清理 / 标点限流）。触发：用户说「去 AI 味」「润色」「改写」「太像 AI」「像人写的」。边界：只处理已有文本，不生成内容、不改事实 / 数据 / 专有名词；需要判断的润色只给建议，不调用模型。'
tags: [去AI味, AI味检测, 中文润色, 文案改写, 写作, 公众号, 报告, humanize, AI写作, 文本改写]
category: content-creation
license: MIT
homepage: https://github.com/YottaMeta/yotta-humanize
---
# 元真（yotta-humanize）

把一段像 AI 写的中文粘进来：先用 **0-100 分**标出 AI 味，再定位套话、黑话、同义堆叠、机械排比、聊天残渣和标点滥用，最后按确定性规则给出可核对的前后改写。

零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用；Claude Code / Cursor / Codex / 通用 Agent 均可调用。

## 何时使用

- 编辑 / 润色文本，去掉 AI 味，让文章、文案、回复更像人写的；
- 用户说「这段太像 AI 写的」「帮我自然一点」「润色但别改内容」；
- 给 AI 生成的中文稿件做检测（评分 0-100）与改写；
- 发现文本充斥着 AI 常用词与句式：赋能、闭环、抓手、综上所述、未来可期、值得注意的是、希望对你有所帮助 等。

**Do NOT trigger**：

- 只处理文本，不生成新内容、不补写缺失信息；
- 不改写事实 / 数据 / 专有名词 / 引文；
- 不破坏作者原意与个人语气（正式 / 随意 / 技术向由作者定）；
- 改写是确定性规则（替换 + 删除），需要判断的改写以建议形式给出，不强行自动改。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 评分（0-100，越高越像 AI 写的）
python3 scripts/yotta_humanize.py score -f article.md

# 详细检测报告
python3 scripts/yotta_humanize.py analyze -f article.md

# Markdown 报告
python3 scripts/yotta_humanize.py report -f article.md > report.md

# 按优先级分组的改写建议
python3 scripts/yotta_humanize.py suggest -f article.md

# 确定性改写（替换/删除 AI 腔，输出改写后文本 + 修复清单）
python3 scripts/yotta_humanize.py rewrite -f article.md

# 管道输入
cat article.md | python3 scripts/yotta_humanize.py score --stdin

# CI 拦截：评分 >= 阈值时退出码 1
python3 scripts/yotta_humanize.py score -f article.md --gate --threshold 45
```

退出码（与元安 / 元审 / 元盾家族一致）：0 = 成功；1 = score --gate 且评分达到阈值；4 = 用法错误 / 致命异常。

## 工作流程（AI 智能体编辑文本时）

1. **先检测**：把待编辑文本交给元真 score 或 analyze，看评分与命中规则；
2. **看命中**：analyze / report 给出命中规则与上下文片段；suggest 按优先级给改写建议；
3. **机械改写**：无歧义的 AI 腔（套话、黑话、聊天残渣、同义堆叠等）用 rewrite 直接改；
4. **人工润色**：需要判断的（排比拆句、模糊归因补来源、绝对化软化）按建议手工处理；
5. **复核**：改写后再次 score 对比评分，确认不破坏原意。

## 能力

- **24 类检测规则**：空泛升华 / 套话开头结尾 / 模糊归因 / AI 黑话 / 同义堆叠 / 「我们」滥用 / 排比三连 / 机械列举 / 破折号与感叹号滥用 / 聊天残渣 / 奉承讨好 / 免责回避 / 废话填充 / 重复声明 等（五组：内容 / 语言 / 句式 / 沟通 / 废话），详见 references/patterns.md；
- **统计突发性**：句长均匀度（CV）、突发性、词汇多样性（双字 TTR）、逗号密度，补充规则检测不到的节奏问题，详见 references/scoring.md；
- **确定性改写**：词表替换（赋能→支持、抓手→切入点、闭环→流程…）、套话删除、聊天残渣清理、标点限流，改写后输出修复清单与前后评分，详见 references/rewriting.md；
- **机器可读**：--json 输出纯净 JSON；score --gate 适合接入 CI / 发布前检查。

## 参考文档

- references/patterns.md — 24 类规则目录与命中示例
- references/scoring.md — 评分公式与统计量说明
- references/rewriting.md — 确定性改写规则与 CLI 协议
- references/faq.md — 常见问题速查（输入 / 结果 / 触发 / 安装）
- references/walkthroughs.md — 公众号 / 正式纪要 / 批量门禁三类复杂走查

## 常见问题（速查）

文本传不进去、改写变化不大、触发不灵、安装不上时，先看 references/faq.md。

## 责任声明

本技能只做文本层面的风格编辑，不改写事实与数据；改写结果请作者复核。检测评分仅供参考，不构成对文本来源的绝对判定。
