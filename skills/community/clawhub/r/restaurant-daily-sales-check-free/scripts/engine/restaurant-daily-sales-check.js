/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * restaurant-daily-sales-check.js —— 餐饮门店日营业款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**餐饮门店每天打烊后、营业款交账之前**，店长与出纳必须把当天的
 * 营业款对上五路钱 —— 收银机流水（现金/刷卡）、外卖平台订单与到账、折扣与免单、挂账。
 * 这五路钱的来源不同、入账时点不同，**差一分钱都要查**：完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应收合计 = 营业额 − 折扣 − 免单
 *   实收合计 = 现金 + 刷卡 + 平台到账 + 挂账
 *   平台到账 = 平台流水 − 平台扣点（完整档还核：平台扣点 = 平台流水 × 平台扣点率）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**平台的扣点率、也不判断折扣/免单政策本身是否合理：
 *    以表里给的数字为准，只对"明显超出常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '实收合计复算（现金 + 刷卡 + 平台到账 + 挂账 = 实收合计）',
  '应收合计复算（营业额 − 折扣 − 免单 = 应收合计）',
  '合计行逐列复核',
  '同一门店同一营业日重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '平台扣点与「平台流水 × 平台扣点率」不符检测',
  '实收合计超过应收合计（多收 / 重复入账）检测',
  '折扣率超出常见区间（0~50%）提示（参考口径）',
  '挂账金额超过应收合计检测',
  '营业额为零却有实收检测',
];

const OUT_OF_SCOPE = [
  '判断平台扣点率、佣金政策、折扣与免单政策本身是否合理（各家平台与各店政策不同，请以合同与门店制度为准）',
  '核对收银机 / 外卖平台导出的原始流水（需要你先导出成文本贴进来）',
  '处理跨日到账、T+1 结算、月结挂账的时间性差异（本表只核同一营业日内的口径）',
  '处理退款、撤销、抹零产生的跨日或跨月冲销',
  '做税务与收入确认判断（发票、增值税、收入截止性）',
];

/* 参考区间：仅供"明显超出"时提示，不是判定标准 */
const DISCOUNT_RATE_REF = [0, 0.5];

const SAMPLE_TEXT = [
  '门店\t营业日\t营业额\t折扣\t免单\t应收合计\t现金\t刷卡\t平台流水\t平台扣点率\t平台扣点\t平台到账\t挂账\t实收合计',
  '望江路店\t2026-06-01\t20000.00\t1000.00\t200.00\t18800.00\t3000.00\t6000.00\t10000.00\t20%\t2000.00\t8000.00\t1800.00\t18800.00',
  '望江路店\t2026-06-02\t15000.00\t500.00\t0.00\t14500.00\t2500.00\t4000.00\t8000.00\t18%\t1440.00\t6560.00\t1440.00\t14500.00',
  '社区店\t2026-06-01\t8000.00\t400.00\t100.00\t7500.00\t1500.00\t2000.00\t4000.00\t15%\t600.00\t3400.00\t600.00\t7500.00',
  '合计\t\t43000.00\t1900.00\t300.00\t40800.00\t7000.00\t12000.00\t22000.00\t\t4040.00\t17960.00\t3840.00\t40800.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的词前面。
  //   反例：「平台扣点率」会被更宽泛的「平台扣点」抢走（两列落到同一个角色、后一列覆盖前一列），
  //   不报错但**整列静默不参与检查** —— 所以 platformRate 必须排在 platformFee 前面。
  store: ['门店名称', '门店编号', '门店', '店铺', '分店', '店名'],
  period: ['营业日期', '营业日', '业务日期', '日期', '账期'],
  revenue: ['营业额', '营业收入', '营业总额', '销售总额', '销售额'],
  discount: ['折扣金额', '折扣', '折让'],
  comp: ['免单金额', '免单', '赠送金额', '招待费'],
  receivable: ['应收合计', '应收金额', '应收'],
  cash: ['现金收入', '现金收款', '现金'],
  card: ['刷卡到账', '刷卡金额', '刷卡', '银行卡'],
  platformGross: ['平台流水', '平台订单流水', '外卖流水', '外卖订单金额'],
  platformRate: ['平台扣点率', '扣点率', '平台佣金率', '佣金率', '扣点比例'],
  platformFee: ['平台扣点', '平台佣金', '扣点金额', '佣金'],
  platformNet: ['平台到账', '平台结算到账', '外卖到账'],
  credit: ['挂账金额', '挂账', '赊账', '签单挂账'],
  paidIn: ['实收合计', '实收金额', '实收', '入账合计'],
};

const LABELS = {
  store: '门店', period: '营业日', revenue: '营业额', discount: '折扣', comp: '免单',
  receivable: '应收合计', cash: '现金', card: '刷卡', platformGross: '平台流水',
  platformRate: '平台扣点率', platformFee: '平台扣点', platformNet: '平台到账',
  credit: '挂账', paidIn: '实收合计',
};

const REQUIRED = ['store', 'period', 'revenue', 'discount', 'comp', 'receivable',
  'cash', 'card', 'platformNet', 'credit', 'paidIn'];
/* 合计行要逐列复核的列（比率列不求和） */
const SUM_ROLES = ['revenue', 'discount', 'comp', 'receivable', 'cash', 'card',
  'platformGross', 'platformFee', 'platformNet', 'credit', 'paidIn'];
/* 金额为负检测覆盖的列（含扣点率，比率为负同样是脏数据） */
const MONEY_ROLES = ['revenue', 'discount', 'comp', 'receivable', 'cash', 'card',
  'platformGross', 'platformRate', 'platformFee', 'platformNet', 'credit', 'paidIn'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|当日合计|全店合计)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值，更不会输出「未发现问题」。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|null)$/i.test(s);
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

/** 比率归一化成小数：`20%` ⇒ 0.2；`0.2` ⇒ 0.2；`20` ⇒ 0.2 */
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
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, cols: [] };
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
      if ((role === 'period' || role === 'store') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return {
    items,
    totals,
    missingColumns,
    cols: headers.map((h, i) => [h, roles[i]]).filter(([, r]) => r),
  };
}

const who = (it) => {
  const s = it && it.store ? String(it.store).trim() : '';
  const p = it && it.period ? String(it.period).trim() : '';
  if (s && p) return `${s} ${p}`;
  if (p) return `${p}`;
  if (s) return `${s}`;
  return `第 ${it && it.line} 行`;
};

const show = (role, v) => (role === 'platformRate' ? `${(v * 100).toFixed(3)}%` : v.toFixed(2));

/* ================================ 免费档检查项 ================================ */

/** ① 实收合计 = 现金 + 刷卡 + 平台到账 + 挂账 */
function checkPaidInRecompute(it) {
  const paidIn = normNumber(it.paidIn);
  const cash = normNumber(it.cash);
  const card = normNumber(it.card);
  const net = normNumber(it.platformNet);
  const credit = normNumber(it.credit);
  if (paidIn === null || cash === null || card === null || net === null || credit === null) return null;
  const sum = round2(cash + card + net + credit);
  if (Math.abs(sum - paidIn) <= TOL) return null;
  return {
    level: 'P0', category: '实收合计复算不符', line: it.line,
    message: `${who(it)}：现金 ${cash.toFixed(2)} + 刷卡 ${card.toFixed(2)} + 平台到账 ${net.toFixed(2)}`
      + ` + 挂账 ${credit.toFixed(2)} = ${sum.toFixed(2)}，但实收合计填的是 ${paidIn.toFixed(2)}，`
      + `相差 ${round2(paidIn - sum).toFixed(2)} —— 这四路钱是实收合计的全部来源，必须相等。`,
  };
}

/** ② 应收合计 = 营业额 − 折扣 − 免单 */
function checkReceivableRecompute(it) {
  const revenue = normNumber(it.revenue);
  const discount = normNumber(it.discount);
  const comp = normNumber(it.comp);
  const receivable = normNumber(it.receivable);
  if (revenue === null || discount === null || comp === null || receivable === null) return null;
  const expect = round2(revenue - discount - comp);
  if (Math.abs(expect - receivable) <= TOL) return null;
  return {
    level: 'P0', category: '应收合计复算不符', line: it.line,
    message: `${who(it)}：营业额 ${revenue.toFixed(2)} − 折扣 ${discount.toFixed(2)} − 免单 ${comp.toFixed(2)}`
      + ` = ${expect.toFixed(2)}，但应收合计填的是 ${receivable.toFixed(2)}，`
      + `相差 ${round2(receivable - expect).toFixed(2)} —— 折扣与免单是营业额的减项，必须能对上。`,
  };
}

/** ⑥ 金额为负（含扣点率） */
function checkNegatives(it) {
  const out = [];
  for (const role of MONEY_ROLES) {
    const v = role === 'platformRate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${show(role, v)}（负数）—— 退款、冲红、抹零应单独列示，`
          + '直接填负数会让实收与应收的勾稽全部失真。',
      });
    }
  }
  return out;
}

/** ③ 合计行逐列复核 */
function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = role === 'platformRate' ? rateValue(totals.row[role]) : normNumber(totals.row[role]);
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各门店各营业日相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 合计行必须等于上面每一行的加总。`,
  });
  return out;
}

/** ④ 同一门店同一营业日重复行 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const s = String(it.store === undefined ? '' : it.store).trim();
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (!s || !p) continue;
    const key = `${s}|${p}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一门店同一营业日重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次 ——`
          + '同一门店同一天的营业款只应有一行，重复行会把营业额与实收都算两遍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** ⑤ 空白与占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）——`
            + '这一列不填，对应的勾稽就没法核，交账前必须补齐。',
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** ⑦ 平台扣点 = 平台流水 × 平台扣点率 */
/** ⑧ 实收合计超过应收合计（多收 / 重复入账） */
/** ⑨ 折扣率超出常见区间（参考口径） */
/** ⑩ 挂账金额超过应收合计 */
/** ⑪ 营业额为零却有实收 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到上报表正文（text）—— 请把「门店 / 营业日 / 营业额 / 折扣 / 免单 / 应收合计'
      + ' / 现金 / 刷卡 / 平台流水 / 平台扣点率 / 平台扣点 / 平台到账 / 挂账 / 实收合计」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `上报表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有一行合计），没有任何门店营业日明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkPaidInRecompute(it); if (a) findings.push(a);
    const b = checkReceivableRecompute(it); if (b) findings.push(b);
    for (const c of checkNegatives(it)) findings.push(c);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let paidInTotal = 0;
  let receivableTotal = 0;
  const days = new Set();
  for (const it of t.items) {
    const a = normNumber(it.paidIn); if (a !== null) paidInTotal += a;
    const b = normNumber(it.receivable); if (b !== null) receivableTotal += b;
    const s = String(it.store === undefined ? '' : it.store).trim();
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) days.add(`${s}|${p}`);
  }

  const result = {
    status: 'success',
    service_type: 'RESTAURANT_DAILY_SALES_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: days.size || t.items.length,
      total_row_checked: Boolean(t.totals && t.totals.row),
      paid_in_total: round2(paidInTotal),
      receivable_total: round2(receivableTotal),
      discount_rate_ref: DISCOUNT_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: days.size || t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核表内算术与勾稽（实收合计 = 现金 + 刷卡 + 平台到账 + 挂账；应收合计 = 营业额 − 折扣 − 免单；'
      + '平台扣点 = 平台流水 × 平台扣点率），**不判断扣点率、折扣与免单政策本身是否合理**；'
      + '结论可由第三方用同一份输入复算。跨日到账、退款冲销、税务口径不在本表范围内。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
