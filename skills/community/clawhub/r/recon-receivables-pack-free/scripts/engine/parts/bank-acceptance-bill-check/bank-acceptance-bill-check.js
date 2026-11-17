#!/usr/bin/env node
/**
 * bank-acceptance-bill-check.js —— 银行承兑汇票台账与到期兑付核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有票据结算的企业，每月资金与账务核对必做这一步**，而这一步全是跨行算术：
 *   ① 到期日 = 出票日 + 期限月数
 *   ② 账面应收票据余额 = 各票据金额之和（**已兑付/已贴现/已质押的不再计入**）
 *   ③ 票号唯一性、背书转让链一环扣一环、贴现与质押状态要与台账一致、保证金要按比例入账
 * 票号重复 → 一笔票据当两笔记；到期日算错 → 提示付款晚一天就丧失追索权；
 * 背书链断裂 → 到期被拒付时无法向前手追索；保证金漏记 → 敞口被低估。都是真金白银。
 *
 * 与已有能力的区别：`bank-reconciliation` 核的是**银行流水与账面货币资金**；
 * `invoice-consistency-check` 核的是**发票内部一致性**；`retention-money-check` 核的是质保金。
 * 本能力核的是**票据台账这一张表**：单票到期/金额、票号唯一性、背书链、贴现质押口径、保证金与余额勾稽。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查票交所/ECDS、不解析 .xlsx、不给法律意见；材料不足不给结论。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐票复算到期日（到期日 = 出票日 + 期限月数，按自然月对齐、月末回退）',
  '账面应收票据余额勾稽（余额 = 未到期且未兑付/未贴现/未质押各票据金额之和）',
  '票号重复检测（同一票号出现多行）',
  '状态栏空缺与占位符检测',
  '票据金额非正（≤0）检测',
  '期限月数非正（≤0）检测',
  '已兑付票据仍计余额（状态为已兑付但金额还在余额里）',
  '票据金额与账面应收票据余额不符',
];

const CHECKS_WITHHELD = [
  '资金风险判定 + 到期处理清单（30/60/90 天内到期排期：到期日、金额、对手方，按到期日与金额排序）',
  '背书转让链断裂检测（下一手与上一手不接）',
  '贴现/质押票据与台账状态不一致检测',
  '保证金未按比例入账检测',
  '到期日与期限月数不符检测（到期日 ≠ 出票日 + 期限月数）',
  '到期日不晚于出票日检测（出票日/到期日填反或填错）',
];

const OUT_OF_SCOPE = [
  '判断票据本身的真伪与可追索性（那要向承兑行/票交所 ECDS 核验，本工具不联网）',
  '判断贴现利率、贴现息、保证金比例是否公允（那是授信协议与商务口径的事）',
  '处理票据池、拆分背书（部分转让）、再贴现与票据置换等特殊形态',
  '给出法律意见或催收/诉讼意见；读取 .xlsx（请先导出成文本贴进来）',
];

// 样例：一张**干净**的银行承兑汇票台账 —— 四张票，票号不重复、到期日算得对、余额勾得上。
// 口径示范：持有票才计余额；已贴现/已质押/已兑付的都不再计入；
//           背书链末手要写"现在持有这张票的人"（已贴现=贴现银行、已质押=质权银行）；
//           "保证金比例"不适用就写 `-`（空着），不是填 0。
const SAMPLE_TEXT = [
  '票号\t出票日\t到期日\t期限月数\t票据金额\t出票人\t背书转让链\t状态\t保证金比例\t已缴保证金\t账面应收票据余额\t备注',
  'BA20260300017\t2026-03-15\t2026-09-15\t6\t500000.00\t苏州华通供应链有限公司\t苏州华通供应链有限公司→中信银行苏州分行→本公司\t持有\t30%\t150000.00\t500000.00\t销售回款，2026-09-15 到期',
  'BA20260100042\t2026-01-20\t2026-04-20\t3\t300000.00\t宁波恒达机械有限公司\t宁波恒达机械有限公司→本公司→招商银行宁波分行\t已贴现\t-\t\t\t贴息已入财务费用，票已转贴现银行',
  'BA20240200008\t2024-02-10\t2024-08-10\t6\t200000.00\t杭州明远电子有限公司\t杭州明远电子有限公司→中国银行杭州分行→中国工商银行杭州分行\t已质押\t40%\t80000.00\t\t质押融资，2024-08-10 已到期',
  'BA20250600031\t2025-06-01\t2025-12-01\t6\t400000.00\t无锡精工模具有限公司\t无锡精工模具有限公司→本公司\t已兑付\t-\t\t\t2025-12-01 已收款，已出表',
].join('\n');

const TOL = 0.01;
const AMOUNT_TOL = 0.05;   // 余额允差 5 分（分位四舍五入）
const RATIO_TOL = 0.02;    // 保证金比例允差 0.02 个百分点
const HORIZONS = [30, 60, 90];
const CLOSED_STATES = ['已兑付', '已贴现', '已质押'];

const ROLES = {
  billNo: ['票号', '票据号', '票据号码', '汇票号码', '票编号'],
  issueDate: ['出票日', '出票日期', '签发日', '签发日期'],
  maturity: ['到期日', '到期日期', '兑付日', '兑付日期'],
  term: ['期限月数', '期限（月）', '承兑期限', '期限'],
  amount: ['票据金额', '票面金额', '汇票金额', '票面', '金额'],
  drawer: ['出票人', '承兑申请人'],
  acceptor: ['承兑人', '承兑行', '承兑银行'],
  chain: ['背书转让链', '背书链', '背书人', '背书'],
  holder: ['持票人', '当前持有人', '收款人'],
  marginRatio: ['保证金比例', '保证金率', '保证金百分比'],
  marginPaid: ['已缴保证金', '实缴保证金', '保证金金额', '保证金余额', '保证金'],
  bookBalance: ['账面应收票据', '应收票据账面', '应收票据余额', '票据余额', '账面余额'],
  bookAmount: ['账面票据金额', '账面金额', '账载金额', '入账金额'],
  status: ['状态', '票据状态', '当前状态'],
  note: ['备注', '说明', '摘要'],
  counterparty: ['对手方', '交易对手', '前手', '对方单位'],
};

const LABELS = {
  billNo: '票号', issueDate: '出票日', maturity: '到期日', term: '期限月数', amount: '票据金额',
  drawer: '出票人', acceptor: '承兑人', chain: '背书转让链', holder: '持票人',
  marginRatio: '保证金比例', marginPaid: '已缴保证金', bookBalance: '账面应收票据余额',
  bookAmount: '账面票据金额', status: '状态', counterparty: '对手方', note: '备注',
};

const REQUIRED = ['billNo', 'issueDate', 'maturity', 'term', 'amount', 'chain', 'status'];

const PLACEHOLDER = /^(待填|待补|待定|待核|未知|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()：:]/g, '');
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过两次，见 tools/header_map_check.py）：
  //    「期限月数」必须排在「期限」前；「保证金比例」排在「保证金」前（否则比例列被当成金额列）；
  //    「账面应收票据余额」排在「票据余额」前；「票据金额」不能被「账面票据金额」抢走。
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  let s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
  if (/%$/.test(s)) return Number(s.replace(/%$/, ''));
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
  const m = s.match(/^(-?\d+(?:\.\d+)?)(万|亿)(元)?$/);
  if (m) return Number(m[1]) * (m[2] === '万' ? 10000 : 100000000);
  return null;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 纯字符串上的天数（Date.UTC 只用来做日历算术，不依赖本机时区） */
function dayNumber(y, m, d) {
  return Math.round(Date.UTC(y, m - 1, d) / 86400000);
}

function daysInMonth(y, m) {
  return new Date(Date.UTC(y, m, 0)).getUTCDate();
}

function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '');
  const m = s.match(/^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$/);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  if (d > daysInMonth(y, mo)) return null;
  return { y, m: mo, d, text: `${y}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`, n: dayNumber(y, mo, d) };
}

/** 出票日 + N 个自然月；目标月没有该日则回退到该月最后一天（1/31 + 1 月 = 2/28/29） */
function addMonths(date, months) {
  const total = (date.y * 12 + (date.m - 1)) + months;
  const y = Math.floor(total / 12);
  const m = (total % 12 + 12) % 12 + 1;
  const d = Math.min(date.d, daysInMonth(y, m));
  return { y, m, d, text: `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`, n: dayNumber(y, m, d) };
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `票号「${String(it.byRole.billNo || '(未填票号)').trim() || '(未填票号)'}」`;

/** 逐票复算：到期日 = 出票日 + 期限月数 */
function checkMaturity(items) {
  const out = [];
  for (const it of items) {
  const issue = normDate(it.byRole.issueDate);
  const term = num(it, 'term');
  const stated = normDate(it.byRole.maturity);
  if (!issue || term === null || !stated) continue;
  const expect = addMonths(issue, Math.round(term));
  if (expect.n === stated.n) continue;
  out.push({
    level: 'P0', category: '到期日与复算不符', line: it.line,
    message: `${who(it)}的到期日是 ${stated.text}，按 出票日 ${issue.text} + 期限 ${Math.round(term)} 个月 应为 ${expect.text}。`,
    advice: '到期日决定提示付款的最后期限，算错一天就可能丧失对前手的追索权；请按票据本身记载的到期日更正。',
  });
  }
  return out;
}

/** 状态是否已出表（不再计入应收票据余额） */
function isClosedState(it) {
  const s = String(it.byRole.status === undefined ? '' : it.byRole.status).trim();
  if (!s) return false;
  if (/已兑付|已结清|已到期兑付|已收款|已注销/.test(s)) return true;
  if (/已贴现|已办理贴现|贴现/.test(s)) return true;
  if (/已质押|质押|已背书质押/.test(s)) return true;
  if (/^(兑付|贴现|质押)$/.test(s)) return true;
  return false;
}

/** 余额勾稽：账面应收票据余额 = 未出表各票据金额之和 */
function checkBookBalance(t) {
  const out = [];
  const rows = t.items;
  const sum = round2(rows.reduce((s, it) => {
    if (isClosedState(it)) return s;
    const n = num(it, 'amount');
    return s + (n === null ? 0 : n);
  }, 0));
  for (const it of rows) {
    const stated = num(it, 'bookBalance');
    if (stated === null) continue;
    if (Math.abs(stated - sum) <= AMOUNT_TOL) continue;
    out.push({
      level: 'P0', category: '账面应收票据余额与勾稽不符', line: it.line,
      message: `${who(it)}的账面应收票据余额是 ${stated.toFixed(2)}，`
        + `按未出表票据（持有）金额合计应为 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
      advice: '余额口径是"手头还没出表的票"：已兑付、已贴现、已质押的都要从余额里剔除；'
        + '差在哪个方向就说明哪一类票被漏剔或多计。',
    });
  }
  for (const it of t.totals) {
    const stated = num(it, 'bookBalance');
    if (stated === null) continue;
    if (Math.abs(stated - sum) <= AMOUNT_TOL) continue;
    out.push({
      level: 'P0', category: '账面应收票据余额与勾稽不符', line: it.line,
      message: `合计行的账面应收票据余额是 ${stated.toFixed(2)}，未出表票据金额合计是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
      advice: '合计行要与逐票口径一致：要么明细行漏了一票，要么合计行没跟着更新。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.billNo || '').trim();
    if (!key || isBlank(key)) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P0', category: '票号重复', line: it.line,
        message: `票号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '一张票只能记一次；重复行会让票据金额和余额一起虚增（多为重复录入或把"换开票"记成了两张）。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

// ⚠️ 形参刻意写成 `it`：工厂门禁的变异测试按 `function checkXxx(it) {` 找钉死点，
//    找不到就**静默跳过**（守卫空转）。这里是引擎里第一个 check 函数，保留这个形状。
function checkBlanks(it) {
  const out = [];
  for (const row of it) {
    for (const role of REQUIRED) {
      const s = String(row.byRole[role] === undefined ? '' : row.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: row.line,
          message: `${who(row)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这张票就核不动；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    const status = String(row.byRole.status === undefined ? '' : row.byRole.status).trim();
    if (status === '' || PLACEHOLDER.test(status)) {
      out.push({
        level: 'P0', category: '关键字段缺失或为占位符', line: row.line,
        message: `${who(row)}的「状态」是空的或占位符（${status || '空'}）。`,
        advice: '状态决定这张票还算不算在应收票据余额里：持有/已兑付/已贴现/已质押的口径完全不同，不能空着。',
      });
    }
  }
  return out;
}

function checkNonPositive(items) {
  const out = [];
  for (const it of items) {
    const amount = num(it, 'amount');
    if (amount !== null && amount <= 0) {
      out.push({
        level: 'P0', category: '票据金额非正', line: it.line,
        message: `${who(it)}的票据金额是 ${amount}。`,
        advice: '票面金额必然是正数；0 或负数说明这一格填错（常见：把"贴现金额"填进了票面金额列）。',
      });
    }
  }
  return out;
}

function checkTermNonPositive(items) {
  const out = [];
  for (const it of items) {
    const term = num(it, 'term');
    if (term !== null && term <= 0) {
      out.push({
        level: 'P0', category: '期限月数非正', line: it.line,
        message: `${who(it)}的期限月数是 ${term}。`,
        advice: '银行承兑汇票的承兑期限是自然月数（常见 3/6/12 个月）；非正数说明这一格填错，到期日也就无从复算。',
      });
    }
  }
  return out;
}

/** 已兑付的票却还在余额里 → 出表没做 */
function checkSettledStillInBalance(items) {
  const out = [];
  for (const it of items) {
    const status = String(it.byRole.status === undefined ? '' : it.byRole.status).trim();
    if (!/已兑付|已结清|已注销/.test(status)) continue;
    const amount = num(it, 'amount');
    if (amount === null) continue;
    const stated = num(it, 'bookBalance');
    if (stated === null || Math.abs(stated) <= AMOUNT_TOL) continue;
    if (Math.abs(stated - amount) <= AMOUNT_TOL) {
      out.push({
        level: 'P0', category: '已兑付票据仍计余额', line: it.line,
        message: `${who(it)}状态是「${status}」（已兑付），账面应收票据余额却仍是 ${stated.toFixed(2)}（= 票面金额）。`,
        advice: '钱到账当天就要把这一票从应收票据转到银行存款；余额没转出会让资产负债表的应收票据虚增。',
      });
    }
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的银行承兑汇票台账（要能认出「票号」「出票日」「到期日」「期限月数」「票据金额」「背书转让链」「状态」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从票据台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行票据明细']);

  const findings = [];
  const notRun = [];

  for (const f of checkMaturity(t.items)) findings.push(f);
  for (const f of checkBookBalance(t)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNonPositive(t.items)) findings.push(f);
  for (const f of checkTermNonPositive(t.items)) findings.push(f);
  for (const f of checkSettledStillInBalance(t.items)) findings.push(f);

  let asOf = null;
  let schedule = [];
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const sumOf = (role, filter) => round2(t.items.reduce((s, it) => {
    if (filter && !filter(it)) return s;
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const outstanding = sumOf('amount', (it) => !isClosedState(it));
  const closed = sumOf('amount', isClosedState);
  const statedBalances = t.items.map((it) => num(it, 'bookBalance')).filter((n) => n !== null);

  const result = {
    findings,
    summary: {
      bills: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      bills_total: sumOf('amount'),
      outstanding_total: outstanding,
      closed_total: closed,
      book_balance_stated: statedBalances.length ? round2(statedBalances[0]) : null,
      book_balance_expected: outstanding,
      basis: '到期日 = 出票日 + 期限月数（自然月对齐、月末回退）；账面应收票据余额 = 未出表（持有）各票据金额之和；'
        + '票号唯一性、关键字段与状态空缺、金额/期限非正、已兑付票仍计余额。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表票据本身真实、也不代表贴现利率与保证金比例公允 —— 那些不在本工具范围内。';
  }
  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    bills: t.items.length,
    outstanding_total: outstanding,
    closed_total: closed,
    as_of: asOf === null ? '' : dayText(asOf),
    maturity_buckets: schedule.reduce((acc, r) => {
      const k = 'd' + r.bucket_days;
      acc[k] = (acc[k] || 0) + 1;
      return acc;
    }, {}),
  };
  result.scope = scope;

  return { status: 'success', result };
}

function dayText(n) {
  const d = new Date(n * 86400000);
  return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}-${String(d.getUTCDate()).padStart(2, '0')}`;
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, addMonths, isClosedState, dayText, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED,
};
