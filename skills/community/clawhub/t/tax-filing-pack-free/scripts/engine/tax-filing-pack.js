'use strict';
/**
 * tax-filing-pack-full.js —— 税务与涉税申报技能包（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须用它：**企业税务会计 / 代账公司的涉税岗，在每次申报之前**。
 * 一张申报表要核的不是一个数，而是十几张互相关联的底稿：进项认证与抵扣、进项税额转出、
 * 农产品收购发票抵扣、应付暂估与发票未到、增值税附加税费、印花税计税依据、研发费用加计扣除归集、
 * 出口退税单证一致性、企业所得税预缴与纳税调整、递延所得税、房产税与城镇土地使用税、
 * 土地增值税、环境保护税 —— 每张表都有自己的勾稽关系，**逐张手核既慢又容易漏**。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个涉税检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一个客户 / 一套申报材料）一次跑完所有对象，
 * **每个对象一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 对象 → 逐项派发"的编排与汇总）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单对象：该对象的一套申报材料文本（每张表用 `=== 检查名 ===` 分段）
 *     payload.objects[]       多对象：{name, files:[{name, text}]} —— 每个子目录 = 一个对象
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某个对象没材料就单独标"未执行"，一个对象都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替纳税申报、不出鉴证意见、不给税务意见**，也不读电子税务局/开票系统的导出文件。
 */

const MEMBERS = [
  {
    label: '农产品收购发票与进项抵扣核对',
    id: 'agri-purchase-invoice-deduction-check',
    entry: require('./parts/agri-purchase-invoice-deduction-check/agri-purchase-invoice-deduction-check.js'),
  },
  {
    label: '应付暂估与发票未到核对',
    id: 'ap-provisional-check',
    entry: require('./parts/ap-provisional-check/ap-provisional-check.js'),
  },
  {
    label: '增值税进项税额认证与抵扣核对',
    id: 'input-vat-deduction-check',
    entry: require('./parts/input-vat-deduction-check/input-vat-deduction-check.js'),
  },
  {
    label: '进项税额转出核对',
    id: 'vat-input-transfer-out-check',
    entry: require('./parts/vat-input-transfer-out-check/vat-input-transfer-out-check.js'),
  },
  {
    label: '增值税附加税费核对',
    id: 'surtax-check',
    entry: require('./parts/surtax-check/surtax-check.js'),
  },
  {
    label: '印花税计税依据核对',
    id: 'stamp-duty-base-check',
    entry: require('./parts/stamp-duty-base-check/stamp-duty-base-check.js'),
  },
  {
    label: '研发费用加计扣除归集核对',
    id: 'rd-expense-check',
    entry: require('./parts/rd-expense-check/rd-expense-check.js'),
  },
  {
    label: '出口退税申报单证一致性核对',
    id: 'export-rebate-doc-consistency-check',
    entry: require('./parts/export-rebate-doc-consistency-check/export-rebate-doc-consistency-check.js'),
  },
  {
    label: '企业所得税纳税调整核对',
    id: 'cit-adjustment-check',
    entry: require('./parts/cit-adjustment-check/cit-adjustment-check.js'),
  },
  {
    label: '预缴企业所得税核对',
    id: 'cit-prepay-check',
    entry: require('./parts/cit-prepay-check/cit-prepay-check.js'),
  },
  {
    label: '递延所得税与暂时性差异核对',
    id: 'deferred-tax-check',
    entry: require('./parts/deferred-tax-check/deferred-tax-check.js'),
  },
  {
    label: '房产税与城镇土地使用税申报核对',
    id: 'property-tax-land-use-check',
    entry: require('./parts/property-tax-land-use-check/property-tax-land-use-check.js'),
  },
  {
    label: '土地增值税预缴与清算核对',
    id: 'land-appreciation-check',
    entry: require('./parts/land-appreciation-check/land-appreciation-check.js'),
  },
  {
    label: '环境保护税申报核对',
    id: 'environmental-tax-check',
    entry: require('./parts/environmental-tax-check/environmental-tax-check.js'),
  },
];

/* 免费档执行：14 个涉税检查项，逐个对象全跑一遍（这就是免费层的核心产出：一次跑完所有对象） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 完整档追加（**多一种能力**，不是多几个数）：跨对象汇总台账 —— 单对象结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨对象汇总台账（全部对象 × 全部 14 项检查合并成一张总表）',
  '跨对象风险排序处理清单（按 P0/P1/P2 排序，带对象名与原文文件行号）',
  '跨对象共性问题归类（同一问题命中 2 个及以上对象时合并成一条共性项）',
  '申报台账导出（Markdown 与 CSV 文本，直接用于申报前复核说明）',
];

/* 如实列出**每个成员检查包自己**没做的检查项（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断某项支出能不能抵扣、该适用哪档税率/扣除率、税收优惠是否适用（属于税务判断，请咨询税务师或主管税务机关）',
  '代替纳税申报、代填申报表，或出具鉴证意见与税务意见（只做表内/表间的算术与勾稽核对）',
  '核对发票真伪、比对申报表与开票系统/勾选平台的逐行明细',
  '读取电子税务局 / 开票系统 / 财务软件的导出文件（需要你先导出成文本，每个对象一个目录）',
  '判断政策口径是否最新（本工具只核你给的表内数字与表间勾稽关系）',
];

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查名 ===` 分段）。
   它是一份**干净的**申报材料：跑出来 0 条发现 —— 干净样例不误报是最重要的一条。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「增值税附加税费核对」里 2026-01 的附加合计从 4800.00 改成 4900.00
   （三项之和 2800+1200+800 = 4800，与 4900 不符）⇒ 必须报出来，并带**原文行号**。 */
const DIRTY_FROM = '2026-01\t40000.00\t7%\t2800.00\t3%\t1200.00\t2%\t800.00\t4800.00';
const DIRTY_TO = '2026-01\t40000.00\t7%\t2800.00\t3%\t1200.00\t2%\t800.00\t4900.00';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['增值税附加税费核对', '印花税计税依据核对', '环境保护税申报核对'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 个对象（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有对象"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州商贸有限公司（2026-02 申报）', files: [{ name: '申报材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳建材有限公司（2026-02 申报）', files: [{ name: '申报材料.txt', text: DIRTY_TEXT }] },
  { name: '缺料对象（只登记未交材料）', files: [] },
];

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

/** 把一份材料按 `=== 检查名 ===` 分段，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。
 *  每个成员引擎内部都把空行过滤掉、行号按过滤后的顺序算（本仓库 14 个引擎口径一致），
 *  所以这里也先把空行过滤掉再交给引擎，并同步保留原始行号 —— 否则回原文件时会错行。 */
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

/** 入参归一化成"对象列表"：`{text}` 是单对象，`{objects:[…]}`（或 `{clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.clients) ? payload.clients : null);
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({ name: String(o.name || o.object || o.client || '').trim(), files: coerceFiles(o) });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.client_name || payload.client
        || payload.name || '单对象').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `对象${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：对象交了材料，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 14 项都核过了。整份材料都没交的对象不在这里报（那是对象级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `对象「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个涉税检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 一个对象跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式：把该对象的每一段材料依次喂给成员引擎，**第一个跑通的段**就是这一项的表；
 *  一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
function runOneObject(object) {
  const live = object.files.filter((f) => String(f.text).trim() !== '');
  const candidates = [];
  for (const f of live) for (const s of sectionsOfFile(f)) candidates.push(s);
  const materialLines = live.reduce(
    (n, f) => n + String(f.text).split(/\r?\n/).filter((l) => l.trim() !== '').length, 0);

  if (!candidates.length || materialLines < 5) {
    return {
      object: object.name, status: 'insufficient_input', files: live.map((f) => f.name),
      material_lines: materialLines,
      checks: MEMBERS.map((m) => ({ check: m.label, status: 'not_run', findings: 0 })),
      findings: [], not_run: MEMBERS.map((m) => m.label),
      total: 0, p0: 0, p1: 0, p2: 0, verdict: 'NOT_RUN',
      reason: '没有收到这个对象的可用材料（材料为空或只有几行）',
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
        missing: bestMissing || ['这个对象的材料里没有这一项需要的表头行'],
      });
      continue;
    }
    const per = (hit.result.findings || []).map((f) => {
      const orig = hit.cand.lineNos[f.line - 1];
      const lineNo = orig === undefined ? hit.cand.startLine : orig;
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
     （别把"跑了 3 项"说成"14 项都核过了"）。 */
  const cover = checkClientCoverage({ client: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '',
      source_file: '', source_line: 0, evidence: '对象级',
    }));
  }

  const lv = countLevels(findings);
  const anyRan = checks.some((c) => c.status === 'ok');
  return {
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
    reason: anyRan ? '' : '材料里没有任何一项能被认出的表（每个 `=== 检查名 ===` 分段的第一行要是表头行）',
  };
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一个对象的材料都没收到（objects[] 与 text 都是空）',
      '单对象用 {"text":"…"}；批量用 {"objects":[{"name":"对象名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一个对象的材料都没收到（objects[] 与 text 都是空）',
      '每个对象一个子目录，目录里放该对象的一套申报材料（每张表用 `=== 检查名 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map(runOneObject);
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个对象都没有可用材料（每个对象目录里要有该对象的申报材料，且每张表要有表头行）`]
        .concat(rows.map((r) => `对象「${r.object}」：没有可用材料`)),
      '把每个对象的申报材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'TAX_FILING_PACK',
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
    note: `本次对 ${rows.length} 个对象逐个跑了 ${CHECKS_GIVEN.length} 个涉税检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各对象材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替纳税申报、不出具鉴证意见**，也不判断某笔业务该不该这样处理。',
  };

  /* 本档只报**实际执行**的那 14 项；未执行项如实列在 checks_withheld 里，绝不伪造结论 */
  result.checks_executed = CHECKS_GIVEN.slice();
  result.checks_withheld = CHECKS_WITHHELD.slice();

  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage, CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS,
};
