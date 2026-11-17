/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * vat-input-transfer-out-check.js —— 进项税额转出核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月申报前**。免税项目、集体福利/个人消费、非正常损失等
 * **不得抵扣**情形对应的进项税额必须转出；无法划分的按销售额比例分摊：
 *
 *   应转出进项税额 = 对应销售额 ÷ 全部销售额 × 当期进项税额
 *
 * 漏转就是**少缴税** —— 会被要求补税并按日加收滞纳金；多转则是白占资金。
 * 这张表的每一格都能手算复现，所以"对不对"是完全可以机械核出来的。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应转出进项税额 = 对应销售额 ÷ 全部销售额 × 当期进项税额
 *   转出比例       = 对应销售额 ÷ 全部销售额
 *   转出合计       = 本期间各转出项目之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某一项进项到底该不该转出（那属于税务判断）：项目名里出现
 *    免税 / 集体福利 / 非正常损失等字样只当作**提示**依据，比例与口径一律以表里给的为准。
 */

const CHECKS_GIVEN = [
  '应转出额复算（对应销售额 ÷ 全部销售额 × 当期进项税额 = 应转出进项税额）',
  '转出合计与各项目之和不符检测',
  '合计行逐列复核',
  '同一期间同一项目重复行检测',
  '空白与占位符检测',
  '金额或比例为负检测',
];

const CHECKS_WITHHELD = [
  '转出比例与销售额占比不符提示（差超容差）',
  '转出额超过当期进项税额检测',
  '不得抵扣项目未转出提示',
  '转出比例大于 100% 异常提示',
  '分摊基数（全部销售额）为零却算出转出额提示',
];

const OUT_OF_SCOPE = [
  '判断某一项进项税额到底该不该转出、按哪条政策转出（那属于税务判断，请咨询税务师）',
  '核对增值税申报表附列资料（二）里转出栏次的逐栏数据与申报口径',
  '处理免税项目与简易计税项目的划分口径、无法划分进项的分摊顺序与年度清算',
  '读取发票勾选平台或财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t转出项目\t对应销售额\t全部销售额\t当期进项税额\t转出比例\t应转出进项税额\t转出合计',
  '2026-01\t免税项目\t50000.00\t1000000.00\t130000.00\t5%\t6500.00\t6500.00',
  '2026-02\t集体福利\t40000.00\t1250000.00\t162500.00\t3.2%\t5200.00\t5200.00',
  '2026-03\t非正常损失\t20000.00\t800000.00\t104000.00\t2.5%\t2600.00\t2600.00',
  '合计\t\t110000.00\t3050000.00\t396500.00\t\t14300.00\t14300.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;                    // 比例容差：0.05 个百分点
/* 提示用：项目名里出现这些字样 = 属于"通常要转出"的情形（只作提示依据，不作税务判断） */
const NON_DEDUCTIBLE_RE = /免税|集体福利|个人消费|职工福利|福利费|非正常损失|简易计税|简易办法/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「全部销售额」不能被「销售额」抢走）
  period: ['期间', '税款所属期', '所属期', '月份', '月度'],
  item: ['转出项目', '不得抵扣项目', '转出原因', '项目名称', '项目'],
  totalSales: ['全部销售额', '当期全部销售额', '全部销售'],
  sales: ['对应销售额', '不得抵扣对应销售额', '销售额'],
  inputTax: ['当期进项税额', '当期无法划分的全部进项税额', '无法划分的进项税额'],
  ratio: ['转出比例', '不得抵扣比例', '分摊比例', '比例'],
  transferTotal: ['转出合计', '合计转出', '转出小计'],
  transferOut: ['应转出进项税额', '应转出税额', '不得抵扣转出税额', '应转出'],
};

const LABELS = {
  period: '期间', item: '转出项目', sales: '对应销售额', totalSales: '全部销售额',
  inputTax: '当期进项税额', ratio: '转出比例', transferOut: '应转出进项税额', transferTotal: '转出合计',
};

const REQUIRED = ['period', 'item', 'sales', 'totalSales', 'inputTax', 'transferOut'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['sales', 'totalSales', 'inputTax', 'transferOut', 'transferTotal'];
/** 这几列是**按期间**的口径（同一期间内多行是同一笔，如合并单元格复制出来会重复）⇒ 合计按期间去重后相加 */
const PER_PERIOD_ROLES = ['totalSales', 'inputTax'];
/** 负值检测覆盖的列（ratio 另按比例解析） */
const NEGATIVE_ROLES = ['sales', 'totalSales', 'inputTax', 'transferOut', 'transferTotal', 'ratio'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|全年合计)$/;

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

/** 比率归一化成小数：`5%` ⇒ 0.05；`0.05` ⇒ 0.05；`5` ⇒ 0.05 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
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
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = it && it.item !== undefined && String(it.item).trim() !== '' ? String(it.item).trim() : '';
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkTransferOutRecompute(it) {
  const out = [];
  const sales = normNumber(it.sales);
  const base = normNumber(it.totalSales);
  const tax = normNumber(it.inputTax);
  const stated = normNumber(it.transferOut);
  if (sales === null || base === null || tax === null || stated === null) return out;
  if (Math.abs(base) <= TOL) return out;      // 分摊基数为零：复算无从算起（完整档单独提示）
  const expect = round2(sales / base * tax);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应转出额与复算不符', line: it.line,
    message: `${who(it)}：对应销售额 ${sales.toFixed(2)} ÷ 全部销售额 ${base.toFixed(2)} × 当期进项税额 ${tax.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「应转出进项税额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  });
  return out;
}

function checkPeriodTransferTotal(group) {
  const out = [];
  let sum = 0;
  let n = 0;
  let stated = null;
  let statedLine = null;
  for (const it of group.rows) {
    const v = normNumber(it.transferOut);
    if (v !== null) { sum += v; n += 1; }
    if (stated === null) {
      const t = normNumber(it.transferTotal);
      if (t !== null) { stated = t; statedLine = it.line; }
    }
  }
  if (stated === null || !n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '转出合计与各项目之和不符', line: statedLine,
    message: `${group.period}：表里「转出合计」填的是 ${stated.toFixed(2)}，本期间 ${n} 个转出项目的「应转出进项税额」相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 转出合计就是各项目之和，两者必须相等。`,
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    if (PER_PERIOD_ROLES.indexOf(role) >= 0) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null && !first.has(periodKeyOf(it))) first.set(periodKeyOf(it), v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
    } else {
      let sum = 0;
      let n = 0;
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null) { sum += v; n += 1; }
      }
      if (!n) continue;
      expect = round2(sum);
    }
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，按本表口径相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const n = it.item !== undefined ? String(it.item).trim() : '';
    if (!p || !n) continue;
    const key = `${p}|${n}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一期间同一项目出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 这一笔转出会被重复计算。`,
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

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'ratio' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'ratio' ? `${(v * 100).toFixed(3)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 转出额与分摊基数都不该为负，冲回应单独列示。`,
    });
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
    return insufficient('没有收到转出计算表正文（text）—— 请把「期间 / 转出项目 / 对应销售额 / 全部销售额 / 当期进项税额 / 应转出进项税额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `转出计算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何转出项目明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkTransferOutRecompute(it));
    findings.push(...checkNegative(it));

  }
  for (const g of groups.values()) findings.push(...checkPeriodTransferTotal(g));
  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let transferTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.transferOut);
    if (v !== null) transferTotal += v;
  }

  const result = {
    status: 'success',
    service_type: 'VAT_INPUT_TRANSFER_OUT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      transfer_out_total: round2(transferTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"对应销售额 ÷ 全部销售额 × 当期进项税额 = 应转出"这类**表内勾稽**与档位提示，'
      + '**不判断某项进项该不该转出**（以税法与主管税务机关口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
