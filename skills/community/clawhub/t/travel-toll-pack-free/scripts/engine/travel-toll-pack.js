'use strict';
/**
 * travel-toll-pack.js —— 差旅与通行费技能包（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须用它：**有大量出差的销售/工程型公司的费用会计**，在**每月报销审核与费用入账之前**。
 * 差旅与通行费是最"碎"的一类费用：**差旅标准**要按职级与城市核住宿/交通/补贴上限，
 * **通行费与过路过桥**要核票据类型、抵扣口径与行程匹配，
 * 每一项都要逐单核，**逐部门手核既慢又容易漏**，而且月月重复。
 * 一家公司往往同时管着**好几个部门/项目组**，真正要做的是"**一次跑完所有部门，每个部门一行结论**"。
 *
 * 这个包做的事**只有一件**：把 2 个差旅与通行检查项装进一个批量壳里，`--input <目录>`
 * （每个子目录 = 一家部门 / 一套材料）一次跑完所有部门，**每家部门一行结论**。
 *   检查项：差旅费标准与超标核对、通行费与过路过桥核对。
 *   规则来源：`scripts/engine/parts/<检查项>/` ——
 *     · 差旅费标准与超标核对：**逐字节拷贝**自免费包 `travel-standard-check-free`，一行都没改；
 *     · 通行费与过路过桥核对：`toll-fee-check`，**本包原生实现**（上游从来没有过通行费引擎）。
 *       ⚠️ 这一项此前被接到 `toll-processing-manual-check` —— 一个**只因为 slug 里同样含 "toll"
 *       就被误选**的海关手册类工具（手册备案耗用、余料结转、内销补税）。买家装到的"通行费核对"
 *       实际在核海关手册，表头、业务与结论全都对不上。换成本文件引用的组件后，
 *       `parts/toll-processing-manual-check/` 已整个删除，两个包里都不再引用它。
 *   本包只做"目录 → 部门 → 逐项派发"的编排与汇总，外加完整档的跨部门汇总台账。
 * * ⚠️ 本文件在**免费壳**里是子集：付费实现会被 `strip_free_engine.py` 剥掉；
 * `CHECKS_WITHHELD` 只是"未执行的能力"的**说明文本**，不是实现。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单部门：这家部门的一套材料文本（每项用 `=== 检查项 ===` 分段）
 *     payload.objects[]       多部门：{name, files:[{name, text}]} —— 每个子目录 = 一家部门
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某家部门没材料就单独标"未执行"，一家部门都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替做账/审计/纳税申报、不出鉴证意见**，也不判断业务实质该怎么定。
 */

/* 2 个成员检查项的**中文名 / 组件 id / 引擎**：差旅标准成员逐字节复用上游免费包
   `travel-standard-check-free`；通行费成员是**本包原生实现**（文件头写了根因：
   上游那个同含 "toll" 的海关手册类组件已被整个删除）。 */
const MEMBERS = [
  {
    label: '差旅费标准与超标核对',
    id: 'travel-standard-check',
    entry: require('./parts/travel-standard-check/travel-standard-check.js'),
  },
  {
    label: '通行费与过路过桥核对',
    id: 'toll-fee-check',
    entry: require('./parts/toll-fee-check/toll-fee-check.js'),
  },
];

/* 免费档执行：2 个差旅与通行检查项，逐家部门全跑一遍（免费层的核心产出：一次跑完所有部门） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 完整档追加（**多一种能力**，不是多几个数）：跨部门汇总台账 —— 单部门结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨部门汇总台账（全部部门 × 全部 2 项核对合并成一张总表）',
  '费用风险排序清单（按 P0/P1/P2 排序，带部门名与原文文件行号）',
  '跨部门共性问题归类（同一个问题命中 2 个及以上部门时合并成一条共性项）',
  '差旅台账导出（Markdown 与 CSV 文本，直接用于月度费用复核说明）',
];

/* 如实列出**每个成员检查包自己**声明的未执行子检查 —— 免费包里两个成员都有未执行项；
   买断包里的通行费成员把它那 5 项真的做了（它的 CHECKS_WITHHELD 是空数组），所以这里会自动少 5 条。
   声明一律取自成员引擎自己，本文件不写死那 5 条的行文，免得两边不一致。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断某项支出该不该报、能不能税前扣除（属于**公司制度与税务判断**，请按制度与主管口径执行）',
  '代替审批流程或出具鉴证意见（只做表内/表间的算术与勾稽核对）',
  '核对发票与通行费电子票据的真伪，或比对差旅平台与报销系统的逐行明细',
  '读取差旅平台 / 报销系统的导出文件（需要你先导出成文本，每个部门一个目录）',
  '判断各地差旅标准的口径是否最新（本工具只核你给的表内数字与表间勾稽关系）',
];

/* 样例 = 2 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。
   这 2 份样例**都是干净稿**（生成时逐项自证过 0 条发现，见 SAMPLE_HAS_FINDINGS）。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「通行费与过路过桥核对」的合计行里 `505.00`（票面金额合计）改成 `605.00`
   （各明细行相加 ≠ 合计）⇒ 必须报出来，并带**原文行号**。 */
const DIRTY_FROM = '合计\t\t\t\t505.00\t21.00\t484.00\t484.00\t';
const DIRTY_TO = '合计\t\t\t\t605.00\t21.00\t484.00\t484.00\t';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 1 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 1 项"说成"2 项都核过了"。 */
const PARTIAL_TITLES = [
  '差旅费标准与超标核对',
];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 家部门（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有部门"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州销售一部（2026-04 报销）', files: [{ name: '差旅材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳工程二部（2026-04 报销）', files: [{ name: '差旅材料.txt', text: DIRTY_TEXT }] },
  { name: '缺料部门（只登记未交材料）', files: [] },
];

/** 内置样例**不含发现**（2 份成员样例都是干净稿，生成时逐项自证过 0 条发现）。
 *  这个常量是给守卫读的**显式声明**，不是放水。 */
const SAMPLE_HAS_FINDINGS = false;

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice
      || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（认不出表头就不出结论）。',
  };
}

function countLevels(list) {
  const out = { p0: 0, p1: 0, p2: 0 };
  for (const f of list) {
    if (f.level === 'P0') out.p0 += 1;
    else if (f.level === 'P1') out.p1 += 1;
    else if (f.level === 'P2') out.p2 += 1;
  }
  return out;
}

/** 把一份材料按 `=== 检查项 ===` 分段，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。
 *  成员引擎内部都把空行过滤掉、行号按过滤后的顺序算，所以这里也先过滤空行再交给引擎，
 *  并同步保留原始行号 —— 否则回原文件时会错行。 */
function sectionsOfFile(f) {
  const lines = String(f.text === undefined || f.text === null ? '' : f.text).split(/\r?\n/);
  const out = [];
  let cur = { title: '', lines: [], lineNos: [] };
  const flush = () => {
    const keep = [];
    const nos = [];
    for (let i = 0; i < cur.lines.length; i += 1) {
      if (String(cur.lines[i]).trim() !== '') {
        keep.push(cur.lines[i]);
        nos.push(cur.lineNos[i]);
      }
    }
    if (keep.length) {
      out.push({
        title: cur.title, file: f.name, text: keep.join('\n'),
        lineNos: nos, startLine: nos[0],
      });
    }
  };
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^\s*===\s*(.+?)\s*===\s*$/);
    if (m) {
      flush();
      cur = { title: m[1].trim(), lines: [], lineNos: [] };
      continue;
    }
    cur.lines.push(lines[i]);
    cur.lineNos.push(i + 1);
  }
  flush();
  return out;
}

function coerceFiles(o) {
  const files = [];
  if (Array.isArray(o.files)) {
    for (const f of o.files) {
      if (!f) continue;
      const t = f.text !== undefined ? f.text : f.content;
      files.push({
        name: String(f.name || f.file || '材料'),
        text: t === undefined || t === null ? '' : String(t),
      });
    }
    return files;
  }
  const t = o.text !== undefined ? o.text : o.content;
  if (t !== undefined && t !== null) {
    files.push({ name: String(o.file || o.file_name || '材料'), text: String(t) });
  }
  return files;
}

/** 入参归一化成"部门列表"：`{text}` 是单部门，`{objects:[…]}`（或 `{orgs/clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.orgs) ? payload.orgs
      : (Array.isArray(payload.clients) ? payload.clients : null));
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({
        name: String(o.name || o.object || o.org || o.client || '').trim(),
        files: coerceFiles(o),
      });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.org_name || payload.org
        || payload.client_name || payload.client || payload.name || '单部门').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `部门${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：部门交了材料，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 2 项都核过了。整份材料都没交的部门不在这里报（那是部门级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `部门「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个差旅与通行检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 把成员引擎报的行号**落回原文文件行**（用于结论里的"原文文件与行号"）。
 *
 *  为什么不能直接 `lineNos[f.line - 1]`：成员引擎的行号口径**实测不统一**（有的把行号记成原文里的
 *  行位置、含表头，有的只算数据行），而本包的分段恰好把空行与 `=== 检查项 ===` 标题行去掉了 ⇒
 *  直接查表会**整体错位**。错行号比没有行号更糟 —— 买家按行号找回原文会看到别的记录。
 *
 *  所以落位**以原文内容为准**：成员给的 evidence 行首片段必须在原文里真的能对上。
 *    ① 用 evidence 片段按**行首**在原文里找出所有候选行；
 *    ② 候选唯一 ⇒ 直接用它；
 *    ③ 候选多行（同一片段重复出现）⇒ 取距"成员行号所对应的分段行"最近的那一行；
 *    ④ 片段缺失或对不上（部门级/汇总级结论）⇒ 如实退回该分段的首行。
 *  这样"对得上"的成员行为完全不变，只有口径不同的成员被纠正到原文行，且绝不编造行号。 */
function evidenceKey(ev) {
  if (Array.isArray(ev)) return String(ev[0] === undefined || ev[0] === null ? '' : ev[0]).trim().slice(0, 15);
  const s = String(ev === undefined || ev === null ? '' : ev).trim();
  if (s.indexOf('\n') >= 0) return s.split('\n')[0].trim().slice(0, 15);
  return s.slice(0, 15);
}

function mapMemberLine(f, cand) {
  const direct = cand.lineNos[f.line - 1];
  const key = evidenceKey(f.evidence);
  const rows = String(cand.text).split('\n');       // 与 lineNos 一一对应（sectionsOfFile 已过滤空行）
  /* 汇总级结论（成员自己把行号记成 0）没有具体行 —— 如实指向本分段的首行，
     不要按 evidence 去挑一行（那会让买家以为那行有问题）。 */
  if (!f.line) return cand.startLine;
  if (!key) return direct === undefined ? cand.startLine : direct;
  const hits = [];
  for (let i = 0; i < rows.length; i += 1) {
    if (String(rows[i]).trim().slice(0, 15) === key) hits.push(i);
  }
  if (!hits.length) return direct === undefined ? cand.startLine : direct;
  if (hits.length === 1) return cand.lineNos[hits[0]];
  let best = hits[0];
  for (const i of hits) {
    const bi = (best + 1) - f.line;
    const ii = (i + 1) - f.line;
    if (Math.abs(ii) < Math.abs(bi) || (Math.abs(ii) === Math.abs(bi) && i < best)) best = i;
  }
  return cand.lineNos[best];
}

/** 一家部门跑完全部 2 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式：把这家部门的每一段材料依次喂给成员引擎，**第一个跑通的段**就是这一项的表；
 *  一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
function runOneObject(object) {
  const live = object.files.filter((f) => String(f.text).trim() !== '');
  const candidates = [];
  for (const f of live) for (const s of sectionsOfFile(f)) candidates.push(s);
  const materialLines = live.reduce(
    (n, f) => n + String(f.text).split(/\r?\n/).filter((l) => l.trim() !== '').length, 0);

  if (!candidates.length || materialLines < 4) {
    return {
      object: object.name, status: 'insufficient_input', files: live.map((f) => f.name),
      material_lines: materialLines,
      checks: MEMBERS.map((m) => ({ check: m.label, status: 'not_run', findings: 0 })),
      findings: [], not_run: MEMBERS.map((m) => m.label),
      total: 0, p0: 0, p1: 0, p2: 0, verdict: 'NOT_RUN',
      reason: '没有收到这家部门的可用材料（材料为空或只有几行）',
    };
  }

  const checks = [];
  const findings = [];
  const notRun = [];
  for (const m of MEMBERS) {
    let hit = null;
    let bestMissing = null;
    for (const cand of candidates) {
      let out = null;
      try { out = m.entry.run({ text: cand.text }); } catch (e) { out = null; }
      if (out && out.status === 'success' && out.result) { hit = { cand: cand, result: out.result }; break; }
      const miss = (out && out.missing) || [];
      if (Array.isArray(miss) && miss.length && (!bestMissing || miss.length < bestMissing.length)) {
        bestMissing = miss;
      }
    }
    if (!hit) {
      notRun.push(m.label);
      checks.push({
        check: m.label, status: 'not_run', findings: 0,
        missing: bestMissing || ['这家部门的材料里没有这一项需要的表头行'],
      });
      continue;
    }
    const per = (hit.result.findings || []).map((f) => {
      const lineNo = mapMemberLine(f, hit.cand);
      return {
        level: f.level,
        category: f.category,
        line: f.line,
        object: object.name,
        check: m.label,
        section: hit.cand.title,
        source_file: hit.cand.file,
        source_line: lineNo,
        evidence: `${hit.cand.file}:${lineNo}`,
        message: f.message,
      };
    });
    for (const f of per) findings.push(f);
    checks.push({
      check: m.label, status: 'ok', findings: per.length,
      section: hit.cand.title || hit.cand.file,
    });
  }

  /* 批量壳自己的检查项：材料只覆盖了一部分检查项时，明确报一条
     （别把"跑了 3 项"说成"2 项都核过了"）。 */
  const cover = checkClientCoverage({ client: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '',
      source_file: '', source_line: 0, evidence: '部门级',
    }));
  }

  const lv = countLevels(findings);
  const anyRan = checks.some((c) => c.status === 'ok');
  const row = {
    object: object.name,
    status: anyRan ? 'ok' : 'insufficient_input',
    files: live.map((f) => f.name),
    material_lines: materialLines,
    checks: checks,
    findings: findings,
    not_run: notRun,
    total: findings.length,
    p0: lv.p0, p1: lv.p1, p2: lv.p2,
    verdict: lv.p0 > 0 ? 'P0_ISSUES' : (findings.length ? 'ISSUES' : (anyRan ? 'NO_ISSUE_FOUND' : 'NOT_RUN')),
    reason: anyRan ? '' : '材料里没有任何一项能被认出的表（每个 `=== 检查项 ===` 分段的第一行要是表头行）',
  };

  /* 这一行有没有被真正核对过（有材料、且至少有一项能跑）⇒ 才够格进跨部门汇总台账。
     免费档与完整档都用它：台账只收"真跑过"的部门行，没交材料的部门不进总表。 */
  row.ledger_member = false;   // 由完整档的台账层置位；免费档恒为 false

  return row;
}

/* 台账钩子（免费档实现）：什么都不做。
   ⚠️ 完整档在**下面那个付费块里**重新声明同名函数 —— JS 函数声明提升 + 后定义覆盖，
      两档各只有一份生效的实现：免费包里生效的是这个空钩子，付费包里生效的是真台账。
      （`tools/strip_free_engine.py` 会整块删掉付费块，于是免费包只剩这一个空钩子。） */
function ledger_hook() { return false; }

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一家部门的材料都没收到（objects[] 与 text 都是空）',
      '单部门用 {"text":"…"}；批量用 {"objects":[{"name":"部门名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一家部门的材料都没收到（objects[] 与 text 都是空）',
      '每家部门一个子目录，目录里放这家部门的一套材料（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map((o) => runOneObject(o, payload));
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 家部门都没有可用材料（每家部门目录里要有这家部门的材料，且每张表要有表头行）`]
        .concat(rows.map((r) => `部门「${r.object}」：没有可用材料`)),
      '把每家部门的材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'INDUSTRY_VERTICAL_PACK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sub_checks_not_run: SUB_CHECKS_WITHHELD.slice(),
      objects: rows.length,
      objects_ran: usable.length,
      sub_checks_per_object: TOTAL_SUB_CHECKS,
      executed_locally: true,
      network_used: false,
      wrote_files: false,
    },
    objects: rows,
    findings: findings,
    summary: {
      objects: rows.length,
      objects_with_issues: withIssues,
      objects_clean: usable.length - withIssues,
      objects_not_run: notRunObjects,
      total: findings.length,
      p0: lv.p0, p1: lv.p1, p2: lv.p2,
      verdict: lv.p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本次对 ${rows.length} 家部门逐个跑了 ${CHECKS_GIVEN.length} 个差旅与通行检查项（两个成员包内部合计 `
      + `${TOTAL_SUB_CHECKS} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各部门材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替审计、不出具鉴证意见**，也不判断收费/定价/医保政策口径。',
  };

  /* 分层：
     · 免费档（免费包里就是下面这两行 + 再下面那句 return，付费块被整块摘掉）：
       只报**实际执行**的那 2 项，未执行项如实列出（说明文本，不是实现）。
     · 完整档（本文件）：在上面那层之上再挂一层跨部门汇总台账
       （部门 × 检查项总表、差旅与通行风险排序清单、跨部门共性问题归类、Markdown / CSV 导出）。 */
  result.checks_executed = CHECKS_GIVEN.concat();
  result.checks_withheld = CHECKS_WITHHELD.concat();

  /* 分层出口：**同一个调用点**，不在这里判档 ——
     判档在台账钩子内部（免费档的空钩子什么都不做，完整档的真实现自己判开关）。
     这样免费包里的 run() 与付费包逐字相同，分层不靠调用方自觉。 */

  /* 完整档：在上面那层之上再挂一层跨部门汇总台账
     （部门 × 检查项总表、差旅与通行风险排序清单、跨部门共性问题归类、Markdown / CSV 导出）。 */
  const ledgerAttached = ledger_hook(result, findings, rows, payload) === true;

  /* 分档后的"实际执行 / 未执行"：只认**钩子到底挂上台账没有**（免费档返回 false ⇒ 保持 2 项）。
     这样 run() 里不出现任何付费判据函数，免费包里连"该不该挂台账"的分支都没有。 */
  if (ledgerAttached) {
    result.checks_executed = CHECKS_GIVEN.concat(CHECKS_WITHHELD);
    result.checks_withheld = [];
  }

  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage, CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS,
};
