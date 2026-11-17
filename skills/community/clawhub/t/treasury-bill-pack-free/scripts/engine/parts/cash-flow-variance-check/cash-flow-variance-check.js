/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cash-flow-variance-check.js —— 现金流预测与实际差异核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月资金例会之前**（以及滚动预测上会前），财务 / 资金岗
 * 要按**项目 × 期间**把这张表逐项核一遍 —— 预测流入流出、实际流入流出、两者差异，
 * 以及当期回款。资金例会上的每一句「差异原因是……」「下期滚动预测是……」都建立在这张表上；
 * 预测不准会直接影响**资金链安全**（该融资时没融、该付款时账上没钱）。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   预测净流量 = 预测流入 − 预测流出
 *   实际净流量 = 实际流入 − 实际流出
 *   差异       = 实际 − 预测（流入差异、流出差异、净流量差异**各自**都要成立）
 *   合计行各列 = 各明细行之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**差异原因是否成立、不评价预测方法：差异率阈值只是**参考口径**，
 *    超阈值只做**提示**并明确标注是参考，不是认定。
 */

const CHECKS_GIVEN = [
  '净流量复算（预测净流量 = 预测流入 − 预测流出；实际净流量 = 实际流入 − 实际流出）',
  '差异复算（差异 = 实际 − 预测，流入/流出/净流量三列各自复核）',
  '合计行逐列复核',
  '同一项目同一期重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '差异率超过参考阈值（如 10%）提示（参考口径）',
  '净流量方向与预测相反提示（预测净流入却实际净流出，或反之）',
  '流入为负或流出为负（方向填反）提示',
  '实际流入与应收账款回款不匹配提示',
  '预测为 0 却有实际发生额提示',
];

const OUT_OF_SCOPE = [
  '判断差异原因说明是否成立、是否讲清了业务动因（请以业务与资金例会结论为准）',
  '评价预测方法、滚动预测口径与预算编制质量（本工具只核表内算术与勾稽）',
  '确定差异率阈值、重要性水平与是否需上报（以本单位资金管理制度为准）',
  '核对应收账款回款数据本身的准确性（是否已扣手续费、是否含票据贴现，需与银行流水核对）',
  '读取财务系统 / 资金系统导出文件（需要你先导出成文本贴进来）',
];

/* 差异率参考阈值：10%（**参考口径**，仅供"明显超出"时提示，不是认定） */
const VARIANCE_RATE_REF = 0.10;

const SAMPLE_TEXT = [
  '期间\t项目名称\t预测流入\t预测流出\t实际流入\t实际流出\t流入差异\t流出差异\t净流量差异\t应收账款回款',
  '2026-01\t华东销售回款\t1200000.00\t800000.00\t1180000.00\t790000.00\t-20000.00\t-10000.00\t-10000.00\t1180000.00',
  '2026-02\t华东销售回款\t1300000.00\t850000.00\t1320000.00\t860000.00\t20000.00\t10000.00\t10000.00\t1320000.00',
  '2026-03\t华东销售回款\t1400000.00\t900000.00\t1370000.00\t890000.00\t-30000.00\t-10000.00\t-20000.00\t1370000.00',
  '2026-01\t华南采购付款\t0.00\t300000.00\t0.00\t310000.00\t0.00\t10000.00\t-10000.00\t',
  '合计\t\t3900000.00\t2850000.00\t3870000.00\t2850000.00\t-30000.00\t0.00\t-30000.00\t3870000.00',
].join('\n');

const TOL = 0.01;              // 金额容差（分）
const RATE_TOL = 0.0001;       // 差异率容差（0.01 个百分点）

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**，否则列会被抢走（静默算错）。
  //    实测坑：若 `forecastIn` 写成 ['预测流入','流入']，则「实际流入」会先被裸「流入」抢走，
  //    两列落到同一个 role、后一列把前一列**覆盖**（合计行照旧"对"，但复算全错）。
  //    「实际X」必须整体排在「预测X」与裸「X」之前；「净流量差异」必须排在「净流量」之前。
  period: ['期间', '所属期', '账期月份', '月份'],
  project: ['项目名称', '项目', '资金项目', '业务板块', '往来单位'],
  forecastIn: ['预测流入', '预计流入', '预测现金流入', '计划流入'],
  forecastOut: ['预测流出', '预计流出', '预测现金流出', '计划流出'],
  actualIn: ['实际流入', '实际现金流入', '本期实际流入'],
  actualOut: ['实际流出', '实际现金流出', '本期实际流出'],
  netDiff: ['净流量差异', '净额差异', '净现金流差异'],
  inDiff: ['流入差异', '流入差额'],
  outDiff: ['流出差异', '流出差额'],
  collected: ['应收账款回款', '实际回款', '回款金额', '已回款'],
};

const LABELS = {
  period: '期间', project: '项目名称', forecastIn: '预测流入', forecastOut: '预测流出',
  actualIn: '实际流入', actualOut: '实际流出', inDiff: '流入差异', outDiff: '流出差异',
  netDiff: '净流量差异', collected: '应收账款回款',
};

const REQUIRED = ['period', 'project', 'forecastIn', 'forecastOut', 'actualIn', 'actualOut'];
// ⚠️ 「金额为负」只查**流入 / 流出**四列：差异列（流入差异 / 流出差异 / 净流量差异）
//    本身**允许为负**（实际低于预测就是负差异）——把差异列也算进来会全表误报（本轮踩过）。
const FLOW_ROLES = ['forecastIn', 'forecastOut', 'actualIn', 'actualOut'];
const SUM_ROLES = ['forecastIn', 'forecastOut', 'actualIn', 'actualOut',
                   'inDiff', 'outDiff', 'netDiff', 'collected'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计|本年累计|累计)$/;
const PLACEHOLDER = /^(n\/?a|无|待填|待补|待定|暂无|--|-—–|\/)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || PLACEHOLDER.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 金额显示：统一两位小数并保留负号（round2 后为 0 的不显示 -0.00） */
const money = (n) => {
  const r = round2(n);
  return (r < 0 ? '-' : '') + Math.abs(r).toFixed(2);
};

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      // 合计行判定：只要「期间」或「项目名称」列写着合计/总计就算
      if ((role === 'period' || role === 'project') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.project ? String(it.project).trim() : '';
  const d = it && it.period ? String(it.period).trim() : '';
  if (p && d) return `${p} ${d} 期`;
  if (d) return `${d} 期`;
  if (p) return `${p}（第 ${it && it.line} 行）`;
  return `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

/** 净流量复算：差异列必须等于「实际净流量 − 预测净流量」 */
function checkNetFlow(it) {
  const out = [];
  const fin = normNumber(it.forecastIn);
  const fout = normNumber(it.forecastOut);
  const ain = normNumber(it.actualIn);
  const aout = normNumber(it.actualOut);
  const netDiff = normNumber(it.netDiff);
  if (fin === null || fout === null || ain === null || aout === null) return out;
  if (netDiff === null) return out;
  const netF = round2(fin - fout);
  const netA = round2(ain - aout);
  const expect = round2(netA - netF);
  if (Math.abs(expect - netDiff) <= TOL) return out;
  out.push({
    level: 'P0', category: '净流量差异与预测实际不符', line: it.line,
    message: `${who(it)}：实际净流量 ${money(netA)}（实际流入 ${money(ain)} − 实际流出 ${money(aout)}）`
      + ` − 预测净流量 ${money(netF)}（预测流入 ${money(fin)} − 预测流出 ${money(fout)}）`
      + ` = ${money(expect)}，但表里净流量差异是 ${money(netDiff)}，相差 ${money(netDiff - expect)}。`,
  });
  return out;
}

/** 差异复算：差异 = 实际 − 预测（流入差异、流出差异**两列各自**复核） */
function checkVariance(it) {
  const out = [];
  const fin = normNumber(it.forecastIn);
  const fout = normNumber(it.forecastOut);
  const ain = normNumber(it.actualIn);
  const aout = normNumber(it.actualOut);
  const inDiff = normNumber(it.inDiff);
  const outDiff = normNumber(it.outDiff);
  if (fin !== null && ain !== null && inDiff !== null) {
    const expect = round2(ain - fin);
    if (Math.abs(expect - inDiff) > TOL) {
      out.push({
        level: 'P0', category: '流入差异与预测实际不符', line: it.line,
        message: `${who(it)}：实际流入 ${money(ain)} − 预测流入 ${money(fin)} = ${money(expect)}，`
          + `但表里流入差异是 ${money(inDiff)}，相差 ${money(inDiff - expect)}。`,
      });
    }
  }
  if (fout !== null && aout !== null && outDiff !== null) {
    const expect = round2(aout - fout);
    if (Math.abs(expect - outDiff) > TOL) {
      out.push({
        level: 'P0', category: '流出差异与预测实际不符', line: it.line,
        message: `${who(it)}：实际流出 ${money(aout)} − 预测流出 ${money(fout)} = ${money(expect)}，`
          + `但表里流出差异是 ${money(outDiff)}，相差 ${money(outDiff - expect)}。`,
      });
    }
  }
  return out;
}

/** 合计行逐列复核：合计行每一列都必须等于各明细行之和 */
function totalRowFindings(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，`
      + `相差 ${money(stated - sum)}。`,
  });
  return out;
}

/** 同一项目同一期重复行检测（重复行会让合计翻倍、差异原因说不清） */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = String(it.project === undefined ? '' : it.project).trim();
    const d = String(it.period === undefined ? '' : it.period).trim();
    if (!p && !d) continue;
    const key = `${p}||${d}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目同一期重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— `
          + '数字会被重复计算，也没法逐项说明差异原因。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 空白与占位符检测：必需列不能空、不能是占位符 —— 空的差异根本没法解释 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 例会要逐项说明，先补齐。`,
        });
      }
    }
  }
  return out;
}

/** 金额为负检测：**流入/流出**都必须是非负数，负号说明方向或冲回没处理好 */
function checkNegatives(it) {
  const out = [];
  for (const role of FLOW_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${money(v)}（负数）—— 流入流出都应为非负；`
          + '冲回、红字或方向填反请单独列示并说明。',
      });
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 差异率超过参考阈值（如 10%）提示：**参考口径**，只提示不认定 */
/** 净流量方向与预测相反提示：预测净流入却实际净流出（或反之）—— 资金链最危险的一种偏离 */
/** 流入为负或流出为负（方向填反）提示：负数流入/流出几乎总是把方向填反了 */
/** 实际流入与应收账款回款不匹配提示：回款是实际流入里最能对上账的那一块 */
/** 预测为 0 却有实际发生额提示：说明这笔资金动作**完全没进预测** */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到差异表正文（text）—— 请把「期间 / 项目名称 / 预测流入 / 预测流出 / 实际流入 / 实际流出 / 差异」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `差异表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何项目期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const a of checkNetFlow(it)) findings.push(a);
    for (const b of checkVariance(it)) findings.push(b);
    for (const c of checkNegatives(it)) findings.push(c);

  }
  for (const role of SUM_ROLES) {
    for (const f of totalRowFindings(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const colTotals = {};
  for (const role of SUM_ROLES) {
    let sum = 0;
    for (const it of t.items) {
      const v = normNumber(it[role]);
      if (v !== null) sum += v;
    }
    colTotals[role] = round2(sum);
  }
  const periods = new Set();
  for (const it of t.items) {
    const v = String(it.period === undefined ? '' : it.period).trim();
    if (v) periods.add(v);
  }

  const result = {
    status: 'success',
    service_type: 'CASH_FLOW_VARIANCE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      col_totals: colTotals,
      variance_rate_ref: VARIANCE_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    // ⚠️ 这里必须是**单行三元**：`strip_free_engine.py` 只把单行 `B` 改写成 `B`；
    //    写成换行的多行三元时，免费包里会留下没人定义的 `paid` ⇒ 烟测当场 ReferenceError（本轮踩过）。
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核「净流量 = 流入 − 流出」「差异 = 实际 − 预测」「合计 = 各明细之和」这类内部勾稽，'
      + '**不判断差异原因是否成立、不评价预测方法**；差异率阈值是参考口径。结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
