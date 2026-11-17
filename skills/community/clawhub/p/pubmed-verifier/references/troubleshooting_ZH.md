# troubleshooting_ZH.md — 一条报错，一行对策

> **何时读我**：终端出现 `[ERROR]`/`[WARN]`、判定全是「待确认」、或结果与预期不符时。
> 每行：报错原文 → 原因 → 一条命令的修复。深度背景见各条指向的文档。
> **回** [INDEX.md](INDEX.md)

## 先分清三种退出码

| 退出码 | 含义 | 第一反应 |
|---|---|---|
| 0 | 干净 | — |
| 1 | 发现问题（无效/不匹配/撤稿/DOI 拼接/arXiv 声称 DOI 不符），或用法错误（claims 文件坏、`--source` 路径不存在） | 看报告 `details` 或 stderr 那一行 |
| 2 | 没验成（网络不可达）**或**旗标值非法 | 先 `--check-net`；再对照下行报错表 |

## 报错速查（原文 → 修复）

| 你看到 | 原因 | 修复 |
|---|---|---|
| `--stdin received no input (nothing on stdin)` | 管道是空的 | 粘贴参考文献表，或改用 `--parse-text 文件` |
| `--stdin and --parse-text are mutually exclusive` | 两个文本输入互斥 | 只留一个 |
| `both --pmids and --source given; --source is ignored` | 优先级规则而非 bug | 不想被忽略就别传 `--source` |
| `parsing --claims JSON: ...` / `reading claims file: ...` | JSON/CSV 格式坏 | 先离线体检 `--lint-claims claims.json` |
| `--threshold is a 0..1 similarity cutoff (got 1.5)` | 旗标校验（v5.8.0）：运行拒绝启动 | 传 0..1 之间的值 |
| `--timeout must be a positive number of seconds` | 旗标校验 | 传秒数，如 `--timeout 60` |
| `--workers 99 exceeds the polite ceiling; clamping to 8` | 软钳制——按 8 继续运行 | 无需处理；调低可消除 `[WARN]` |
| `无法连接 <主机>（已连续 N 次传输失败）` / `circuit breaker skipped N call(s)` | 某主机连续失败，后续调用被跳过以免硬打 | 稍后重跑（unknown 不写缓存）；`--meta-source europepmc` 换元数据源；`--check-net` 看哪条路通 |
| `[NOTE] <文件>: structured parse produced no text — reading as plain text` | 结构化文件（docx/pptx/html/JATS）解析失败已回退纯文本——来自它的结果可能不完整 | 导出为文本/HTML 重跑；或该文件本就是纯文本则忽略 |
| `{source} not found` | `--source` 路径不存在 | 核对路径 |
| `text#N: no routable ID and no usable title — skipped (...)` | 该行无 PMID/DOI/arXiv ID 且过短无法标题检索（括号内引用其前 48 字符） | 补 ID，或 `--claims-file` 提供精确元数据 |

## 判定不符合预期

- **全是 ❓ 待确认**——是网络问题不是文献问题：跑 `--check-net`（v5.6.0 起逐源测直连+代理两路）。有代理就设 `HTTPS_PROXY`；NCBI 被墙 → `--meta-source europepmc`。unknown 不写缓存，网络好了原命令重跑只补这些；同一次运行内 `--retries` 已自动补跑过一轮。
- **⚠ 不匹配但标题看着一样**——看 `details` 里哪个字段不符（作者/期刊/年也在比对）。要决定性判定用 `--claims-file` 提供期望元数据。
- **封顶 ⚠ partial**——某声称字段无法核验（最常见：claims 缺 `title`），或论文已撤稿（设计如此，附人工复核提示）。
- **中文文献几乎不解析**——无 ID 中文行只要 ≥12 字符即路由 OpenAlex 中文标题检索；判定要求注册标题逐字出现于条目原文（给了年份则须吻合；刊名非必要）。短碎片与散文段停留「待确认」——用 `--claims-file`（与语言无关的完整判定）或补 ID。
- **`.docx` 没有输出**——文档没有可提取文本层（扫描图片）：先导出为文本/HTML。

## 混合意图（本工具还是 cite-holmes？）

| 请求形态 | 路由 |
|---|---|
| 「验证这几条引用」/ 附了列表 | 本工具（`--parse-text`/`--stdin`） |
| 「帮我写 X 主题的文献综述」 | 先 cite-holmes，成稿后回来审计参考文献表 |
| 「查这个 DOI 对不对」+ 核验意图 | 本工具（`--dois`） |
| 「排版我的参考文献」（已验证） | 本工具（`--format-references`） |
| 「排版这些引用」（从未验证） | 也是本工具——`--format-references` 设计上先验证再排版 |

## 国内/受限网络速修

1. `--check-net`——看四数据源+arXiv 各在哪条路（直连/代理）可达。
2. 设 `HTTPS_PROXY`/`HTTP_PROXY`（死代理要 unset——残留死代理会**伪装成断网**）。
3. NCBI 持续被墙用 `--meta-source europepmc`。
4. 慢链路加 `--timeout 60`；缓存（30 天）吸收重复运行。

完整手册：[operations.md](operations.md)。
