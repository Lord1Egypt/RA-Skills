# 产物落盘细则

> 按需读取：需要确认目录结构、命名规则、某类产物该存哪里、收尾自检时读。
> 每次交互都要落盘的总原则在 SKILL.md §产物落盘，这里是可查的细节。

## 目录骨架

```
OwlWrite/<YYYY-MM-DD>_<清洗后的标题>/
├── owl-assets.json    # 资产清单（唯一索引，恢复上下文先读它）
├── README.md          # 给用户看的项目总览（产物导航 + 累计花费）
├── 00-账单/runs.jsonl # 每次任务一行：run_id / 动作 / 积分 / 耗时
├── 01-开题/           # 开题报告、提纲各版本
├── 02-文献/           # references.csv 总清单、references.bib、search-<runid>.json、fulltexts/（含 OA 免费全文）
├── 03-稿件/           # 正文-draft<N>.md（只增不覆盖）、正文-final.md、references.md
├── 04-图/             # 配图产物：<序号>-<图说明>.png（tikz 代码同存 .tex）
├── 05-检测/           # 查重 / AIGC / 格式 / 智评 / 图像 / 文献质量 / 校对，按「品名-日期」归档
├── 06-核验/           # 核验报告 HTML（report_url 下载）+ verify-<runid>.json
└── 07-交付/           # 定稿 + 报告提交包
```

## 各时机动作

| 时机 | 动作 |
|---|---|
| 项目首次交互 | 建目录骨架 + 初始化 owl-assets.json、README.md |
| 检索之后 | 存 `02-文献/search-<runid>.json`，题录合并进 references.csv（按 DOI / 题名去重）；要全文的 PDF 下载进 `02-文献/fulltexts/` |
| 写作成功后 | 存 `03-稿件/正文-draft<N>.md` + `references.md`，**并把参考文献并入 references.csv**（供下次续写免检索） |
| 检测完成后 | 报告归档 `05-检测/<品名>-<日期>/` |
| 核验完成后 | 报告存 `06-核验/`，回写 references.csv 的 verified 列 |
| 每次收尾 | 更新 owl-assets.json 与 README，向用户报「新增了哪些文件 / 花了多少点 / 余额多少」 |

## 硬规则与自检

- 每写一个文件立即登记；manifest 损坏按目录实际内容重建；`aigc` 元数据与报告标识原样保留，不得删除。
- 收尾自检三步：
  1. `owl-assets.json` 里每个路径都真实存在（不一致以磁盘为准回写清单）；
  2. 文件名**不含空格**（落盘前空白一律转 `-`，Windows / 同步盘对空格路径最易读回失败）；
  3. `references.csv` 的 `verified` 列只用 `pass` / `retracted` / `concern` / `unverified` 四个词，别发明同义词。

## 命名规则

- 日期固定 `YYYY-MM-DD`；标题去掉 `《》〈〉` 与 Windows 非法字符 `\ / : * ? " < > |`，
  空白转 `-`，超过 40 字符截断（保留前 40 字，不加省略号）。
- 例：`《城市垃圾分类：政策执行困境》` → `2026-10-26_城市垃圾分类-政策执行困境`。

## 续接已有项目（用户说「接着上次写」）

1. 先读 `owl-assets.json`：检索过什么、写到第几稿、上次检测 / 核验结果。
2. 参考文献**先查 references.csv**，命中就不重复检索（省积分）。
3. 新稿版本号递增，绝不覆盖用户可能已手改的文件。
