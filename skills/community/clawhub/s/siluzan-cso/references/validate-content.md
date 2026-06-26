# workflow validate — 文案校验（字数限制 + 内部内容泄漏）

> 对文案做**本地**校验：统计字数、按字数限制检查上下限、并检查三库编码 / 溯源 / SOP 等内部骨架资产是否泄漏到成稿。
> 纯本地操作，不调用任何接口、不需要鉴权。校验**通过 exit 0，不通过 exit 1**，便于在工作流中卡点。

## 文案来源（三选一）

优先级：`--text` > `-f/--file` > stdin（管道）。**宿主没有文件读写工具时**，用后两种方式直接把对话里的文案传进来，无需落盘：

```bash
# 1) 文件（宿主有文件工具时最常用）
siluzan-cso workflow validate -f draft.md --max 800

# 2) 管道 / heredoc（推荐：长文不受命令行长度限制）
cat <<'EOF' | siluzan-cso workflow validate --max 800
这里是要校验的整篇文案……
可以包含多行、markdown 等。
EOF

# 3) 行内文本（短文案；过长会受 shell 参数长度限制）
siluzan-cso workflow validate --text "这里是文案内容" --max 280
```

> 三者都没提供且 stdin 非管道时，命令会报错并打印上述三种用法指引。

---

## 何时使用

- 生成口播稿 / 公众号文章 / 博客等成稿并**落盘后**，交付给用户**之前**做一次质检。
- 用户给出了**字数限制**（如「不超过 800 字」「至少 1500 字」「标题 ≤ 20 字」）时，用 `--min` / `--max` 核对。
- 担心内部骨架资产（三库内部编码 `TF-/PA-/MF-`、`三库溯源`、`SOP执行`、三库名称、`焊点` 等过程内容）误写进成稿时（默认开启该检查）。

---

## 用法

```bash
# 最简：只统计字数 + 默认泄漏检查
siluzan-cso workflow validate -f draft.md

# 字数上限 800（默认按「不含空白字符数」口径）
siluzan-cso workflow validate -f draft.md --max 800

# 字数区间 1500~3000，按汉字数统计
siluzan-cso workflow validate -f article.md --min 1500 --max 3000 --count-by cjk

# 去除 markdown 语法后再统计（更贴近用户感知的正文字数）
siluzan-cso workflow validate -f article.md --max 800 --strip-markdown

# 关闭内部内容泄漏检查（仅看字数）
siluzan-cso workflow validate -f draft.md --max 280 --no-check-leak

# 追加自定义禁用词（命中即不通过）
siluzan-cso workflow validate -f draft.md --forbidden "竞品名,内部代号,占位符"

# 脚本/自动化：JSON 输出 + 退出码判定
siluzan-cso workflow validate -f draft.md --max 800 --json
```

---

## 参数

| 参数                  | 说明                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------- |
| `-f, --file <path>`   | 待校验文案文件（`.md` / `.txt`）；与 `--text` / stdin 三选一                                            |
| `--text <content>`    | 直接传入文案正文（宿主无文件工具时用）；优先级最高                                                      |
| `--min <n>`           | 字数下限（按 `--count-by` 口径）                                                                        |
| `--max <n>`           | 字数上限（按 `--count-by` 口径）                                                                        |
| `--count-by <mode>`   | 限制口径：`chars-no-space`（不含空白，**默认**）· `chars`（含空白）· `cjk`（汉字）· `words`（英文单词） |
| `--strip-markdown`    | 统计前去除 markdown 语法与 frontmatter，默认 `false`                                                    |
| `--no-check-leak`     | 跳过内部骨架资产泄漏检查（默认开启检查）                                                                |
| `--forbidden <words>` | 额外禁用子串，逗号分隔，命中即校验不通过                                                                |
| `--json`              | JSON 输出（含全部指标、问题列表、`passed`）                                                             |

---

## 字数口径选择建议

- **中文成稿（公众号 / 博客 / 口播）**：默认 `chars-no-space` 或 `cjk` 都可；用户说「字数」一般指不含空白的字符数。
- **标题 / 简介等带英文混排**：`chars-no-space`。
- **纯英文内容**：用 `words` 统计单词数。
- **平台硬上限（如 X/Twitter 280 字符）**：用 `chars`（含空白）最贴近平台计数。

> markdown 文件里 `#`、`*`、`>` 等符号会被计入原始字符数。需要「正文字数」时加 `--strip-markdown`。

---

## 泄漏检查命中项

默认检查并视为**不应出现在成稿**的内部内容（与 `three-lib-content-workflow` 第 2 步「内容保密」一致）：

- 三库内部编码：`TF-xxxx` / `PA-xxxx` / `MF-xxxx`
- `三库溯源`、`SOP执行 / SOP步骤 / SOP记录`、`焊点`
- 三库名称：`流量因子库` / `产品资产库` / `烹调方法库`

命中后会逐条列出片段与原因；AI 应据此删改成稿后重新校验，**不要**把这些内部内容交付给用户。

---

## 退出码

| 退出码 | 含义                                         |
| ------ | -------------------------------------------- |
| `0`    | 校验通过（字数在范围内 + 无泄漏 / 禁用词）   |
| `1`    | 文件不存在、字数超/欠限、或命中泄漏 / 禁用词 |

---

## 交叉引用

- 成稿创作流程 → `three-lib-content-workflow/content-writer.workflow.md`
- 成稿落盘与呈现约定 → 同上「输出」一节
