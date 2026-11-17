/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * subcontract-settlement-check.js —— 分包结算与产值核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**建筑总包每月给分包结算时**，逐家分包把
 * **合同额、已完成产值、本期产值、质保金/代扣款、本期应付、累计已付、未付余额**勾一遍。
 * 这些都是加减法，算错就是钱 —— 完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   本期应付 = 本期产值 − 质保金 − 代扣款
 *   累计产值 = 累计已付 + 未付余额
 *   合计行   = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**结算单价、工程量计量口径与质保金比例：比例、计量以合同与现场为准，
 *    只对"明显偏离常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '本期应付勾稽（本期产值 − 质保金 − 代扣款 = 本期应付）',
  '累计已付与未付余额勾稽（累计已付 + 未付余额 = 累计产值）',
  '合计行逐列复核',
  '同一分包同一期重复行检测',
  '空白与占位符检测',
  '金额或产值为负检测',
];

const CHECKS_WITHHELD = [
  '本期产值超过合同额减已完成产值（超结算）提示',
  '未付余额为负（多付）检测',
  '质保金比例偏离参考区间（0%~10%）提示（参考口径）',
  '代扣款超过本期应付提示',
  '合同额为零却有产值检测',
];

const OUT_OF_SCOPE = [
  '判断结算单价、工程量计量与变更签证是否成立（以合同约定与现场计量为准）',
  '认定质保金退还条件、缺陷责任期与保修责任',
  '核对发票开具、税率与增值税进项抵扣',
  '读取结算软件或 ERP 导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显偏离"时提示 */
const RETENTION_RATE_REF = [0, 0.10];

const SAMPLE_TEXT = [
  '期间\t分包单位\t合同额\t已完成产值\t本期产值\t质保金\t代扣款\t本期应付\t累计已付\t未付余额\t累计产值',
  '2026-01\t中建劳务\t1200000.00\t0.00\t300000.00\t9000.00\t3000.00\t288000.00\t288000.00\t12000.00\t300000.00',
  '2026-02\t中建劳务\t1200000.00\t300000.00\t400000.00\t12000.00\t4000.00\t384000.00\t672000.00\t28000.00\t700000.00',
  '2026-02\t宏基分包\t800000.00\t0.00\t200000.00\t6000.00\t2000.00\t192000.00\t100000.00\t100000.00\t200000.00',
  '合计\t\t3200000.00\t300000.00\t900000.00\t27000.00\t9000.00\t864000.00\t1060000.00\t140000.00\t1200000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名排在更宽泛的前面
  //    （「结算期间」不能被「期间」抢走、「已完成产值」不能被「累计产值」抢走）
  period: ['结算期间', '所属期间', '期间', '期次', '月份'],
  subcontractor: ['分包单位名称', '分包单位', '分包商', '供应商名称', '供应商'],
  contractAmount: ['合同金额', '合同总额', '合同额', '签约合同价'],
  completedValue: ['已完成产值', '已完产值', '前期累计产值'],
  currentValue: ['本期产值', '本期完成产值', '本期结算产值'],
  retention: ['质量保证金', '质保金', '保修金'],
  deduction: ['代扣款项', '代扣款', '其他代扣'],
  payable: ['本期应付金额', '本期应付', '本期应付结算款'],
  paidCumulative: ['累计已付款', '累计已付', '累计支付'],
  unpaidBalance: ['未付款余额', '未付余额', '应付余额'],
  cumulativeValue: ['累计结算产值', '累计产值'],
};

const LABELS = {
  period: '期间', subcontractor: '分包单位', contractAmount: '合同额', completedValue: '已完成产值',
  currentValue: '本期产值', retention: '质保金', deduction: '代扣款', payable: '本期应付',
  paidCumulative: '累计已付', unpaidBalance: '未付余额', cumulativeValue: '累计产值',
};

const REQUIRED = ['period', 'subcontractor', 'contractAmount', 'currentValue', 'retention',
  'deduction', 'payable', 'paidCumulative', 'unpaidBalance', 'cumulativeValue'];
const SUM_ROLES = ['contractAmount', 'completedValue', 'currentValue', 'retention', 'deduction',
  'payable', 'paidCumulative', 'unpaidBalance', 'cumulativeValue'];
/* 免费档的"金额为负"只看这些列；**未付余额**留给完整档的"多付"判断，避免两档重复报同一件事 */
const NEGATIVE_ROLES = ['contractAmount', 'currentValue', 'cumulativeValue', 'payable',
  'paidCumulative', 'retention', 'deduction'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|本期合计|合计金额)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
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
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  if (!it) return '该行';
  const sub = it.subcontractor ? String(it.subcontractor).trim() : '';
  const per = it.period ? String(it.period).trim() : '';
  if (sub && per) return `${sub} ${per} 期`;
  if (sub) return `${sub}（第 ${it.line} 行）`;
  if (per) return `${per} 期（第 ${it.line} 行）`;
  return `第 ${it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkPayable(it) {
  const cv = normNumber(it.currentValue);
  const ret = normNumber(it.retention);
  const ded = normNumber(it.deduction);
  const stated = normNumber(it.payable);
  if (cv === null || ret === null || ded === null || stated === null) return null;
  const expect = round2(cv - ret - ded);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应付勾稽不符', line: it.line,
    message: `${who(it)}：本期产值 ${cv.toFixed(2)} − 质保金 ${ret.toFixed(2)} − 代扣款 ${ded.toFixed(2)} 应为 ${expect.toFixed(2)}，表里本期应付是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkCumulative(it) {
  // ⚠️ 局部变量**不能**叫 `paid`：泄漏守卫的静态判据是 `\bconst paid\s*=`，
  //    会把这个普通局部变量误判成"免费包里还留着付费开关"（第 236 轮记录过同一个坑）。
  const paidAmt = normNumber(it.paidCumulative);
  const unpaid = normNumber(it.unpaidBalance);
  const cum = normNumber(it.cumulativeValue);
  if (paidAmt === null || unpaid === null || cum === null) return null;
  const sum = round2(paidAmt + unpaid);
  if (Math.abs(sum - cum) <= TOL) return null;
  return {
    level: 'P0', category: '累计已付与未付余额之和不符', line: it.line,
    message: `${who(it)}：累计已付 ${paidAmt.toFixed(2)} + 未付余额 ${unpaid.toFixed(2)} = ${sum.toFixed(2)}，但累计产值是 ${cum.toFixed(2)}，相差 ${round2(sum - cum).toFixed(2)} —— 未付余额就是累计产值的未付部分，必须相等。`,
  };
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额或产值为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字请单独列示，不要混进结算表。`,
      });
    }
  }
  return out;
}

function checkTotalRow(totals, items, role) {
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const sub = String(it.subcontractor || '').trim();
    const per = String(it.period || '').trim();
    if (!sub || !per) continue;
    const key = `${sub}|${per}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一分包同一期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现过，第 ${it.line} 行再次出现 —— 同一家分包同一期的结算会被重复计算。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到结算表正文（text）—— 请把「期间 / 分包单位 / 合同额 / 本期产值 / 质保金 / 代扣款 / 本期应付 / 累计已付 / 未付余额 / 累计产值」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `结算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何分包结算明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkPayable(it); if (a) findings.push(a);
    const b = checkCumulative(it); if (b) findings.push(b);
    for (const c of checkNegatives(it)) findings.push(c);

  }
  for (const role of SUM_ROLES) {
    for (const x of checkTotalRow(t.totals, t.items, role)) findings.push(x);
  }
  for (const x of checkDuplicates(t.items)) findings.push(x);
  for (const x of checkBlanks(t.items)) findings.push(x);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let contractTotal = 0;
  let payableTotal = 0;
  const periodSet = new Set();
  for (const it of t.items) {
    const a = normNumber(it.contractAmount); if (a !== null) contractTotal += a;
    const b = normNumber(it.payable); if (b !== null) payableTotal += b;
    const p = String(it.period || '').trim();
    if (p) periodSet.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'SUBCONTRACT_SETTLEMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodSet.size,
      contract_total: round2(contractTotal),
      payable_total: round2(payableTotal),
      retention_rate_ref: RETENTION_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodSet.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"本期应付 = 本期产值 − 质保金 − 代扣款""累计已付 + 未付余额 = 累计产值"这类内部勾稽，'
      + '**不规定结算单价、工程量计量口径与质保金比例**（以合同约定与现场计量为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
