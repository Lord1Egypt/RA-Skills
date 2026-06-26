# CLI 脚本食谱：`--json-out` 落盘 + Node.js 精准查询

> 通用纪律（加载纪律、数据处理协议「摘要 → outline → 脚本读 JSON」、防死循环、交付自检）**只在** `references/core/agent-conventions.md` 维护，本文件是配套**脚本示例集**。
> 核心约定一句话：凡需结构化数据，一律 **`--json-out <路径>`** 落盘，**用 `node -e` / 脚本**读 JSON 筛选聚合；**禁止**用宿主 Read 工具打开落盘业务 `*.json`；唯一允许 Read 的数据结构文件是 `*.outline.txt`。

---

## 落盘产物与命名

一条 `--json-out` 命令成功后，目标目录下会生成三类文件，stdout 回一行摘要 JSON：

- 业务数据：`<section>[-<查询id>].json`（如 `list-accounts-youtube.json`、`task-detail-<publishId>.json`）
- 结构描述：同名 `<section>[-<查询id>].outline.txt`（schema-only，**先读它**）
- 索引清单：`cli-manifest[-<查询id>].json`（`artifacts[].file` 指向业务 JSON）

**读文件以 stdout 摘要里的 `writtenFiles[]` / `manifestFile` 为准**，不要把 `<section>.json` 当成不变的硬编码。若传入的是 `*.json` 文件路径（而非目录），业务数据写入该文件，outline 为同名 `*.outline.txt`。

### outline 文件格式

- 前几行为 `//` 注释（schema-only 声明、用法、类型推断口径）。
- **类型字面量**是最后一个不以 `//` 开头的行；提取写法：`outlineRaw.trimEnd().split('\n').filter(l => !l.startsWith('//')).pop()`。
- outline 是结构描述，**不是数据**：勿 `require` 当 JSON，勿贴给用户。

---

## 基础模式：`--json-out` + 读文件 + `node -e`

约定示例目录 **`./snap-cso`**（可换任意空目录）。文件名以当次摘要 `writtenFiles[0]` / `cli-manifest*.json` → `artifacts[].file` 为准。

### 1. 账户列表提取特定账号 ID

```bash
mkdir -p ./snap-cso
siluzan-cso list-accounts --media-type YouTube --json-out ./snap-cso
node -e "
const d = require('./snap-cso/list-accounts-youtube.json');
const rows = Array.isArray(d.items) ? d.items : [];
rows.forEach((a) => console.log(a.mediaCustomerId, a.mediaCustomerName));
"
```

Windows PowerShell（避免管道传 JSON）：

```powershell
$SNAP = ".\snap-cso"; New-Item -ItemType Directory -Force -Path $SNAP | Out-Null
siluzan-cso list-accounts --media-type YouTube --json-out $SNAP
node -e "const d=require('./snap-cso/list-accounts-youtube.json'); (d.items||[]).forEach(a=>console.log(a.mediaCustomerId, a.mediaCustomerName));"
```

### 2. RAG 检索结果按 score 取 TopN

```bash
siluzan-cso rag query -q "产品核心卖点 用户使用场景" --folder-id <id> --partition wiki --top-k 12 --json-out ./snap-cso
node -e "
const fs = require('fs'), path = require('path');
const man = JSON.parse(fs.readFileSync('./snap-cso/cli-manifest.json','utf8'));
const art = man.artifacts.find(a => a.section.startsWith('rag-query')) || man.artifacts[0];
const d = require(path.join('./snap-cso', art.file));
const hits = d.results || d.items || [];
hits.slice().sort((a,b)=>(b.score??0)-(a.score??0)).slice(0,8)
  .forEach(h => console.log((h.score??0).toFixed(3), String(h.content||'').slice(0,60)));
"
```

### 3. 人设列表查 styleGuide 字符数 / 取指定人设 id

`persona list` 落盘含 `styleGuide`（通常很长）；脚本只打印需要的字段，避免把长文吐进对话：

```bash
siluzan-cso persona list --json-out ./snap-cso
node -e "
const d = require('./snap-cso/persona-list.json');
const rows = d.items || d.list || [];
rows.forEach(p => console.log(p.id, p.name, '(styleGuide', String(p.styleGuide||'').length, 'chars)'));
"
```

### 4. 任务列表筛失败项 / 汇总状态

```bash
siluzan-cso task list --status -1 --json-out ./snap-cso
node -e "
const d = require('./snap-cso/task-list.json');
const list = d.list || [];
const failed = list.filter(t => t.status === 2);
console.log('共', d.total, '任务；本页中止/异常', failed.length, '个');
failed.forEach(t => console.log(' ', t.publishId, t.taskName));
"
```

### 5. 运营报表汇总

```bash
siluzan-cso report fetch --media Douyin --days 7 --json-out ./snap-cso
node -e "
const fs = require('fs'), path = require('path');
const man = JSON.parse(fs.readFileSync('./snap-cso/cli-manifest.json','utf8'));
const d = require(path.join('./snap-cso', man.artifacts[0].file));
console.log('keys:', Object.keys(d));
"
```

---

## 调试技巧

### 查看原始 API 响应（`--verbose` 打到 stderr）

```bash
siluzan-cso list-accounts --media-type YouTube --json-out ./snap-cso --verbose 2> ./snap-cso/verbose.log
```

### 验证快照 JSON 结构

```bash
siluzan-cso list-accounts --media-type YouTube --json-out ./snap-cso
node -e "
const d = require('./snap-cso/list-accounts-youtube.json');
console.log('keys:', Object.keys(d));
console.log('itemCount:', (d.items||[]).length, 'sample:', d.items && d.items[0] && Object.keys(d.items[0]));
"
```

---

## 脚本编写小贴士

- **用 `process.stdout.write` 而不是 `console.log` 提取单个值**：前者不带换行符，方便直接赋给 shell 变量。
- **节点代码复杂时拆分写法**：不要写超过 10 行的 `node -e` 单行，改用 `.mjs` 脚本文件。
- **不确定文件名时**先看 stdout 摘要的 `manifestFile`，再读 `cli-manifest*.json` 的 `artifacts[]` 找到业务 `*.json`。
