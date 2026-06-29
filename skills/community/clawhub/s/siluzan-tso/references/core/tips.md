# CLI 脚本食谱：`--json-out` 落盘 + Node.js 精准查询

> 通用纪律（加载纪律、数据处理协议「摘要 → outline → 脚本读 JSON」、币种、交付自检）**只在** `references/core/agent-conventions.md` 维护，本文件是配套**脚本示例集**。
> 核心约定一句话：凡需结构化数据，一律 **`--json-out <路径>`** 落盘，**用 `node -e` / 脚本**读 JSON 筛选聚合；**禁止**用宿主 Read 工具打开落盘业务 `*.json`；唯一允许 Read 的数据结构文件是 `*.outline.txt`。

---

## 文件命名规则

当一条命令具备明确的"查询 id"（mediaCustomerId / entityId / ruleId / auditId 等）时，目录模式落盘的 `*.json`、`*.outline.txt` 与对应 manifest **都会带上 `-<查询id>` 后缀**（全小写）：

- 业务文件：`<section>-<查询id>.json`、`<section>-<查询id>.outline.txt`（如 `overview-9526903813.json`、`balance-google.json`）
- 清单文件：`manifest-<accountId>.json`（google-analysis）/ `report-manifest-<accountId>.json`（report 分析类）/ `cli-manifest-<查询id>.json`（通用业务命令）
- section 已以同一 slug 结尾时不重复追加（如 `list-accounts-google`）。**读文件以 stdout 摘要里的 `writtenFiles[]` / `manifestFile` 为准**，不要把 `<section>.json` 当成不变的硬编码。

此命名对三类快照统一生效：通用业务命令（`cli-manifest[-<id>].json`）、`google-analysis`（`manifest-<accountId>.json`）、`report …` 分析（`report-manifest[-<accountId>].json`）；三种 stdout summary 都带 `outlineFile`、`agentHint` 字段。

### outline 文件格式

- 前 3 行为 `//` 注释（schema-only 声明、用法、类型推断口径），其后**可能**还有若干行 `//` 字段提示。
- **类型字面量**是最后一个不以 `//` 开头的行；提取写法：`outlineRaw.trimEnd().split('\n').filter(l => !l.startsWith('//')).pop()`。
- 例外提示：`google-analysis` 的 `campaigns-*.outline.txt` 在标准头注释后多 2 行中文 `//` 提示（金额字段已统一为元：`budgetAmountYuan`、`campaignTargetCpaYuan` 等，无需换算；详见 `references/analytics/account-analytics.md`「金额单位」）。

---

## 已有 JSON 时（不必先重跑 CLI）

用户已保存输出或只问「怎么从一大坨 JSON 里筛字段」时：直接用**本地文件**喂给 `node -e` 即可，不必为示例再执行 `list-accounts` 等业务命令（字段路径以实际响应为准；列表类命令多为 `items[]` 外层分页结构）。

---

## 基础模式：`--json-out` + 读文件 + `node -e`

约定示例目录 **`./snap-cli`**（可换任意空目录）。文件名以当次 `cli-manifest[-<查询id>].json` → `artifacts[].file` 为准。

### 过滤特定字段（Google 账户列表）

`list-accounts` 的 `items[]` 元素多为 `{ ma: { mediaCustomerId, mediaCustomerName, ... } }` 结构：

```bash
mkdir -p ./snap-cli
siluzan-tso list-accounts -m Google --json-out ./snap-cli
node -e "
const path = require('path');
const snap = './snap-cli';
const d = require(path.join(snap, 'list-accounts-google.json'));
const rows = Array.isArray(d.items) ? d.items.map((x) => x.ma ?? x) : [];
rows.forEach((ma) => console.log(ma.mediaCustomerId, ma.mediaCustomerName));
"
```

Windows PowerShell（避免管道传 JSON）：

```powershell
$SNAP = ".\snap-cli"; New-Item -ItemType Directory -Force -Path $SNAP | Out-Null
siluzan-tso list-accounts -m Google --json-out $SNAP
node -e "const d=require('./snap-cli/list-accounts-google.json'); const rows=(d.items||[]).map(x=>x.ma||x); rows.forEach(ma=>console.log(ma.mediaCustomerId, ma.mediaCustomerName));"
```

---

## 常用场景示例

以下均假设 `mkdir -p ./snap-cli` 已执行，且在同一工作目录下。

### 1. 从账户列表提取特定账户的 ID

```bash
siluzan-tso list-accounts -m Google --json-out ./snap-cli
node -e "
const d = require('./snap-cli/list-accounts-google.json');
const rows = (d.items || []).map((x) => x.ma || x);
const target = rows.find((ma) => String(ma.mediaCustomerName || '').includes('Brand A'));
console.log(target ? target.mediaCustomerId : 'not found');
"
```

### 2. 余额低于阈值的账户告警

`balance` 列表在 `items[]` 中，常用字段含 `remainingAccountBudget`、`name`、`currencyCode`：

```bash
siluzan-tso balance -m Google --json-out ./snap-cli
node -e "
const d = require('./snap-cli/balance-google.json');
const rows = d.items || [];
const low = rows.filter((a) => Number(a.remainingAccountBudget) < 100);
if (low.length === 0) { console.log('所有账户余额充足'); process.exit(0); }
console.log('余额不足账户：');
low.forEach((a) => console.log(' ', a.mediaCustomerId, a.name, '余额:', a.remainingAccountBudget, a.currencyCode));
"
```

### 3. 汇总消耗数据

`stats` 的 `AccountOverviewItem` 使用 **`spend`**（非 `cost`）：

```bash
siluzan-tso stats -m Google --days 7 --json-out ./snap-cli
node -e "
const d = require('./snap-cli/stats-google.json');
const list = d.items || [];
const total = list.reduce((s, a) => s + Number(a.spend ?? 0), 0);
const clicks = list.reduce((s, a) => s + Number(a.clicks ?? 0), 0);
console.log('总消耗:', total.toFixed(2), '  总点击:', clicks);
list
  .slice()
  .sort((a, b) => Number(b.spend) - Number(a.spend))
  .slice(0, 5)
  .forEach((a) => console.log(' ', a.mediaCustomerId, a.mediaCustomerName, a.spend));
"
```

### 3b. 多账户投放画像（`accounts-digest`）

多账户汇总消耗/点击/转化时**优先** `accounts-digest`（见工作流 P3、`references/accounts/accounts.md` § accounts-digest），不要对每个账户循环 `stats`：

```bash
siluzan-tso accounts-digest -m Google -a id1,id2,id3 \
  --start 2026-04-01 --end 2026-04-15 \
  --json-out ./snap-p3
node -e "
const path = require('path');
const snap = './snap-p3';
const d = require(path.join(snap, 'accounts-digest-google.json'));
const rows = d.data?.items || [];
const meta = d.meta || {};
console.log('区间:', meta.window?.startDate, '~', meta.window?.endDate);
console.log('返回', rows.length, '户，扫描', meta.scanned);
rows.slice(0, 10).forEach((r) =>
  console.log(' ', r.mediaCustomerId, r.spend, r.currencyCode, 'CTR%', r.ctr),
);
"
```

### 4. 从广告系列列表提取 ID

```bash
siluzan-tso ad campaigns -a <mediaCustomerId> --json-out ./snap-cli
node -e "
const d = require('./snap-cli/ad-campaigns-<mediaCustomerId>.json');
const list = d.items || [];
list.filter((c) => c.status === 'ENABLED').forEach((c) => console.log(c.id, c.name));
"
```

（将文件名中的 `<mediaCustomerId>` 换成实际数字 ID；若不确定文件名，先看 stdout 摘要的 `manifestFile` 字段或 `./snap-cli/cli-manifest-<查询id>.json` 的 `artifacts`，老快照可能为 `cli-manifest.json`。）

### 5. 检查预警规则是否已存在

```bash
siluzan-tso forewarning list -m Google --json-out ./snap-cli
node -e "
const d = require('./snap-cli/forewarning-list-google.json');
const rules = d.items || [];
const name = '日消耗预警';
const exists = rules.some((r) => (r.data && r.data.name) === name);
console.log(exists ? '已存在，跳过创建' : '不存在，可以创建');
"
```

### 6. 关键字推荐结果

```bash
siluzan-tso keyword -k "running shoes" --json-out ./snap-cli
node -e "
const d = require('./snap-cli/keyword-suggest.json');
const items = d.items || [];
const top = items
  .slice()
  .sort((a, b) => (b.montlySearch ?? 0) - (a.montlySearch ?? 0))
  .slice(0, 15)
  .map((k) => k.keyword);
console.log(top.join(','));
"
```

### 7. 根据地区预算比例（分析 JSON 文件）

若上游步骤已生成包含 `budgetProportions` 的快照 JSON（例如自建脚本或历史 `google-analysis` 落盘），直接读该文件：

```bash
node -e "
const data = require('./snap-cli/my-budget-proportions.json');
const totalBudget = 200;
const currency = data.account?.currencyCode ?? 'USD';
console.log('地区预算分配（总预算', totalBudget, currency + '）：');
(data.budgetProportions || []).forEach((bp) => {
  const budget = (totalBudget * bp.budgetProportion).toFixed(2);
  console.log(' ', bp.areaCode, budget, currency);
});
"
```

### 8. 查找 entityId（解绑/分享前）

```bash
siluzan-tso list-accounts -m Google --json-out ./snap-cli
node -e "
const d = require('./snap-cli/list-accounts-google.json');
const rows = (d.items || []).map((x) => x.ma || x);
const keyword = 'Brand A';
rows
  .filter((ma) => String(ma.mediaCustomerName || '').includes(keyword))
  .forEach((ma) => {
    console.log('mediaCustomerName:', ma.mediaCustomerName);
    console.log('mediaCustomerId:  ', ma.mediaCustomerId);
    console.log('entityId:         ', ma.entityId ?? ma.id);
    console.log('---');
  });
"
```

---

## 多命令串联（中间结果一律落盘）

```bash
SNAP=./snap-cli
mkdir -p "$SNAP"

siluzan-tso list-accounts -m Google --json-out "$SNAP"
ACCOUNT_ID=$(node -e "
const d = require('./snap-cli/list-accounts-google.json');
const rows = (d.items||[]).map(x=>x.ma||x);
const t = rows.find(ma => String(ma.mediaCustomerName||'').includes('Brand A'));
process.stdout.write(t ? String(t.mediaCustomerId) : '');
")

siluzan-tso ad campaigns -a "$ACCOUNT_ID" --json-out "$SNAP"
# 当次写入的 cli-manifest 文件名带 -<account> 后缀，按 glob 匹配最稳：
CAMPAIGN_ID=$(node -e "
const fs = require('fs');
const path = require('path');
const dir = './snap-cli';
const manName = fs.readdirSync(dir).find(f => /^cli-manifest(-.*)?\.json$/.test(f) && f.includes('${ACCOUNT_ID}')) || 'cli-manifest.json';
const man = JSON.parse(fs.readFileSync(path.join(dir, manName),'utf8'));
const art = (man.artifacts||[]).find(a => String(a.section||'').startsWith('ad-campaigns-'));
if (!art) process.exit(1);
const d = require(path.join(dir, art.file));
const list = d.items || [];
const c = list.find(x => x.status === 'ENABLED');
process.stdout.write(c ? String(c.id) : '');
")

echo "Account: $ACCOUNT_ID  Campaign: $CAMPAIGN_ID"
```

Windows 可两步分别 `siluzan-tso ... --json-out .\snap-cli` 后，用 `node -e` 读 `cli-manifest-<account>.json`（或 stdout 摘要的 `manifestFile`）找到最新 `ad-campaigns-*.json` 文件名（与 bash 示例同理）。

---

## 调试技巧

### 查看原始 API 响应结构（`--verbose`）

`--verbose` 会把请求 URL 和原始响应打到 **stderr**；结构化数据仍以 **`--json-out`** 落盘为准：

```bash
siluzan-tso list-accounts -m Google --json-out ./snap-cli --verbose 2> ./snap-cli/verbose.log
```

### 验证快照 JSON

```bash
siluzan-tso list-accounts -m Google --json-out ./snap-cli
node -e "
const d = require('./snap-cli/list-accounts-google.json');
console.log('keys:', Object.keys(d));
console.log('itemCount:', d.itemCount, 'sample:', d.items && d.items[0] && Object.keys(d.items[0]));
"
```

### 查看 `ad batch list` 字段

```bash
siluzan-tso ad batch list --json-out ./snap-cli
node -e "
const d = require('./snap-cli/ad-batch-list.json');
const first = (d.items || [])[0];
console.log('可用字段：', first && Object.keys(first));
"
```

---

## 通用分页与查询建议

- 绝大多数列表类命令默认每页 20 条记录，数据量较大时须显式指定 `--page-size`。
- **`list-accounts` 列全部 / 数个数**：优先 **`--page-size 999` 一次拉取** + `--json-out` + 脚本读盘（见 `references/accounts/accounts.md` § Agent 意图速查）；**不要**先试默认 20 再翻页。
- 其他列表命令（报告列表、发票列表等）在单页拉不满时，再用 `--page-size`（如 `100`）与 `--page` 组合翻页；读盘确认 `total > itemCount` 后再补下一页。

---

## 脚本编写小贴士

- **用 `process.stdout.write` 而不是 `console.log` 提取单个值**：前者不带换行符，方便直接赋给 shell 变量。
- **节点代码复杂时拆分写法**：不要写超过 10 行的 `node -e` 单行，改用 `node -e "$(cat <<'EOF'\n...\nEOF\n)"` 或多行 `.mjs` 脚本文件。
- 同一运行目录、同一"查询 id"的多次拉数会合并到 `cli-manifest-<id>.json` 的 `artifacts[]`；不同账户/实体写入各自的 manifest，互不覆盖。
