# 小红书发布前检测

发布前一次性过完 4 组检查的文本合规自查工具 —— 一条命令 + 一个退出码，直接告诉你：
**能不能发、哪一条要改、改成什么。**

纯本地、不调用付费 API、无第三方 Python 包。

> ⚠️ **先说一件事：本 skill 依赖 `xiaohongshu-prohibited-words`，要先装它。**
> ```bash
> clawhub install xiaohongshu-prohibited-words
> ```
> 违禁词库与解析逻辑都归那个 skill（单一真相源），本 skill 运行时去读它。
> **没装的话，本 skill 会一直返回退出码 `3`（这是有意的 fail-closed，不是坏了）** ——
> 宁可报「查不了」，也不装作「查过了、没问题」。

## 它查什么

| # | 检查组 | 典型命中 |
|---|---|---|
| 1 | 违禁词·敏感词·限流词 | 「白嫖」这类实测硬词、营销高危组合、极限词、账号级禁区词 |
| 2 | 标题与篇幅规范 | 标题超 20 字符、无结果感钩子、感叹号堆叠；正文超 1000 字符 |
| 3 | AI 声明与强制标注 | 命中 AI 生成信号时提醒勾选声明；列出平台强制标注项 |
| 4 | 导流风险 | 手机号、邮箱、扫码话术、私域话术 |

## 用法

```bash
python3 scripts/preflight.py --file 笔记终稿.md
python3 scripts/preflight.py --title "标题" --body "正文" --tags "#标签1 #标签2"
python3 scripts/preflight.py --file 笔记终稿.md --json     # 机器可读
```

退出码：`0` 通过 / `1` 有 P0 禁止发布 / `2` 只有 P1 建议 / `3` fail-closed（依赖缺失或输入不全）。

## 为什么退出码要留一档 `3`

「没查出来」和「查不了」必须是两件事。词库读不到、格式变了、输入为空 —— 一律 `3`，
**绝不等价于「通过」**。一条会静默放行的发布前闸门，比没有更危险。

## 词库只有一份（本 skill 的硬依赖）

违禁词库与解析逻辑的单一真相源是 skill **`xiaohongshu-prohibited-words`**：

```bash
clawhub install xiaohongshu-prohibited-words     # ← 必须先装这个
```

本 skill 运行时不复制它，只取「词 / 级别 / 替代建议」三列，
解析器（`scripts/wordlist.py`）也归那个 skill，运行时按它的安装位置载入。

要用别的词库：`--wordlist <路径>` 或环境变量 `XHS_WORDLIST=<路径>` ——
**指定了却找不到会直接返回 `3`**，不会静默回落到默认词库。

## 加平台

v1 只做小红书。平台规则按文件分放在 `references/platforms/`，
加公众号 / 抖音只需新增一个 `<platform>.json`，用 `--platform <name>` 切换 —— 不改代码。

## 自测

```bash
bash scripts/selftest.sh
```

## License

MIT
