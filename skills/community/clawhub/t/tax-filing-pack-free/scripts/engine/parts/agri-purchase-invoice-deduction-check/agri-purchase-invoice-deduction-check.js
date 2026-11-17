/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * agri-purchase-invoice-deduction-check.js —— 农产品收购发票与进项抵扣核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**农产品加工 / 食品企业的财务，每月申报前**。
 * 企业向农户收购农产品，自己给自己开「农产品收购发票」，进项税额按 **买价 × 扣除率** 计算，
 * 用于生产销售或委托加工 13% 税率货物的，还要再算一笔**加计扣除**。
 * 这张表算错，方向只有两个 —— **少抵**（多缴税，白扔钱）或 **多抵**（被查出来要补税 + 滞纳金），
 * 两条都是税务风险。所以每一笔都必须逐笔复算，不能靠抄上个月。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   可抵扣进项 = 买价 × 扣除率
 *   加计扣除额 = 可抵扣进项 × 加计比例
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该按什么口径抵扣（扣除率该用 9% 还是 10%、加计扣除该按什么基数与时间点、
 *    核定扣除试点是否适用）：表里给的买价、扣除率、加计比例一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '可抵扣进项复算（买价 × 扣除率 = 可抵扣进项）',
  '加计扣除额复算（可抵扣进项 × 加计比例 = 加计扣除额）',
  '合计行逐列复核',
  '同一收购凭证号重复行检测',
  '空白与占位符检测',
  '金额或比例为负检测',
];

const CHECKS_WITHHELD = [
  '扣除率与政策参考口径不一致提示（参考区间 9% / 10%）',
  '加计比例超出参考区间提示（参考区间 0~1%）',
  '收购金额与发票金额不符提示',
  '同一农户同一日大额多笔拆分提示（单笔参考上限 10 万元）',
  '已抵扣但无收购发票号提示',
];

const OUT_OF_SCOPE = [
  '判断该笔农产品该用 9% 还是 10% 扣除率、能否加计扣除（用途是否属于生产销售或委托加工 13% 税率货物，属于税务判断，请咨询税务师或主管税务机关）',
  '判断加计扣除的口径与时间点（按买价还是按已抵扣进项加计、领用当期加计还是购进当期加计）',
  '判断农产品进项税额核定扣除（投入产出法 / 成本法 / 参照法）是否适用及其计算结果',
  '核对收购发票本身的合规性（票面项目、收购对象是否属于农业生产者、现金支付限额、发票领用与缴销）',
  '处理增值税申报表填列、进项税额转出、免税农产品，以及企业所得税税前扣除',
  '读取开票系统 / 财务软件 / 电子税务局导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t收购日期\t收购凭证号\t农户名称\t收购发票号\t农产品名称\t买价\t扣除率\t可抵扣进项\t加计比例\t加计扣除额\t已抵扣进项税额\t发票金额',
  '2026-01\t2026-01-05\tSG2026-001\t张建国\tFP202601001\t玉米\t100000.00\t9%\t9000.00\t1%\t90.00\t9090.00\t100000.00',
  '2026-01\t2026-01-12\tSG2026-002\t李秀兰\tFP202601002\t小麦\t80000.00\t9%\t7200.00\t0%\t0.00\t7200.00\t80000.00',
  '2026-02\t2026-02-08\tSG2026-003\t王大山\tFP202602001\t大豆\t120000.00\t10%\t12000.00\t1%\t120.00\t12120.00\t120000.00',
  '2026-02\t2026-02-20\tSG2026-004\t张建国\tFP202602002\t玉米\t50000.00\t9%\t4500.00\t0%\t0.00\t4500.00\t50000.00',
  '2026-02\t2026-02-20\tSG2026-005\t张建国\tFP202602003\t玉米\t30000.00\t9%\t2700.00\t0%\t0.00\t2700.00\t30000.00',
  '合计\t\t\t\t\t\t380000.00\t\t35400.00\t\t210.00\t35610.00\t380000.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;        // 比例容差：0.05 个百分点
const REF_RATES = [0.09, 0.10]; // 农产品收购发票扣除率的参考口径：9% / 10%
const ADD_RATE_MAX = 0.01;      // 加计比例参考区间上限：1%
const SPLIT_LIMIT = 100000;     // 单笔收购参考上限：10 万元

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「加计扣除比例」不能被「扣除比例」抢走、「已抵扣进项税额」不能被「进项税额」抢走、
  //      「收购发票金额」不能被「收购金额」抢走、「收购发票号」不能被「发票金额」抢走）
  period: ['所属期间', '所属期', '会计期间', '纳税期间', '收购月份', '月份', '期间'],
  date: ['收购日期', '开票日期', '收购时间', '业务日期', '日期'],
  voucher: ['收购凭证编号', '收购凭证号', '收购单号', '收购凭证', '凭证编号', '凭证号'],
  farmer: ['出售人名称', '投售人名称', '农户名称', '农户姓名', '出售人', '投售人', '交售人', '农户', '出售方'],
  invoice: ['收购发票号码', '收购发票号', '发票号码', '发票号'],
  product: ['农产品名称', '货物名称', '商品名称', '品名'],
  invoiceAmount: ['收购发票金额', '发票金额', '发票价税合计', '发票总额'],
  price: ['买价', '收购金额', '收购价款', '收购价', '支付金额', '价款'],
  addRate: ['加计扣除比例', '加计比例', '加计扣除率', '加计率'],
  addAmount: ['加计扣除额', '加计扣除金额', '加计抵减额', '加计扣除'],
  rate: ['扣除率', '扣除比例', '进项扣除率'],
  deducted: ['已抵扣进项税额', '已认证抵扣税额', '已抵扣税额', '已抵扣'],
  inputVat: ['可抵扣进项税额', '可抵扣进项', '准予抵扣进项', '可抵扣税额', '进项税额'],
  note: ['备注', '说明', '摘要'],
};

const LABELS = {
  period: '所属期间', date: '收购日期', voucher: '收购凭证号', farmer: '农户名称',
  invoice: '收购发票号', product: '农产品名称', invoiceAmount: '发票金额', price: '买价',
  addRate: '加计比例', addAmount: '加计扣除额', rate: '扣除率', deducted: '已抵扣进项税额',
  inputVat: '可抵扣进项', note: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'date', 'voucher', 'farmer', 'price', 'rate', 'inputVat', 'addRate', 'addAmount'];
/** 合计行逐列复核的列（比例列不参与加总） */
const SUM_ROLES = ['price', 'inputVat', 'addAmount', 'deducted', 'invoiceAmount'];
/**
 * 免费档负值检测覆盖的列：金额列 + 两个比例列。
 * ⚠️ 刻意**不含**「发票金额」与「已抵扣进项税额」之外的那些只在完整档参与判断的列 ——
 *    免费档只报"表内不该出现负数"这件事本身，不替完整档下任何结论。
 */
const NEGATIVE_ROLES = ['price', 'inputVat', 'addAmount', 'deducted', 'invoiceAmount', 'rate', 'addRate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

/** 比例归一化成小数：`9%` ⇒ 0.09；`0.09` ⇒ 0.09；`9` ⇒ 0.09；`1%` ⇒ 0.01 */
function ratioValue(raw) {
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
  const n = [it && it.farmer, it && it.voucher]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkInputVatRecompute(it) {
  const out = [];
  const price = normNumber(it.price);
  const rate = ratioValue(it.rate);
  const stated = normNumber(it.inputVat);
  if (price === null || rate === null || stated === null) return out;
  const expect = round2(price * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '可抵扣进项复算不符', line: it.line,
    message: `${who(it)}：买价 ${price.toFixed(2)} × 扣除率 ${(rate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「可抵扣进项」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '农产品收购发票的进项就是"买价 × 扣除率"，填少了要少抵（多缴税），填多了要被要求补税。',
  });
  return out;
}

function checkAddAmountRecompute(it) {
  const out = [];
  const base = normNumber(it.inputVat);
  const addRate = ratioValue(it.addRate);
  const stated = normNumber(it.addAmount);
  if (base === null || addRate === null || stated === null) return out;
  const expect = round2(base * addRate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '加计扣除额复算不符', line: it.line,
    message: `${who(it)}：可抵扣进项 ${base.toFixed(2)} × 加计比例 ${(addRate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「加计扣除额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '加计扣除是另一笔进项，它算错同样会少抵或多抵 —— 两笔都要逐笔复算，不能只核第一笔。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是申报表的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const v = it.voucher !== undefined ? String(it.voucher).trim() : '';
    if (!v) continue;
    if (seen.has(v)) {
      out.push({
        level: 'P1', category: '同一收购凭证号重复行', line: it.line,
        message: `${who(it)}的收购凭证号「${v}」在第 ${seen.get(v)} 行已出现，第 ${it.line} 行再次出现 —— `
          + '要么是重复粘贴了一行，要么是一张收购凭证被拆成两行登记，'
          + '多出来的那一行会把买价与可抵扣进项都重复计一遍（等于凭空多抵一笔进项）。',
      });
    } else seen.set(v, it.line);
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = (role === 'rate' || role === 'addRate') ? ratioValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = (role === 'rate' || role === 'addRate') ? `${(v * 100).toFixed(4)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 买价、进项税额、加计扣除额与扣除率都不该为负，`
        + '冲回 / 红字应单独列示并在备注里说明（负数混在正数里会被加总成一个错的合计）。',
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
    return insufficient('没有收到农产品收购发票与进项抵扣核对表正文（text）—— 请把「所属期间 / 收购日期 / 收购凭证号 / 农户名称 / 买价 / 扣除率 / 可抵扣进项 / 加计比例 / 加计扣除额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `农产品收购发票与进项抵扣核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何收购明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkInputVatRecompute(it));
    findings.push(...checkAddAmountRecompute(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let priceTotal = 0;
  let inputVatTotal = 0;
  let addAmountTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.price);
    if (a !== null) priceTotal += a;
    const b = normNumber(it.inputVat);
    if (b !== null) inputVatTotal += b;
    const c = normNumber(it.addAmount);
    if (c !== null) addAmountTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'AGRI_PURCHASE_INVOICE_DEDUCTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      price_total: round2(priceTotal),
      input_vat_total: round2(inputVatTotal),
      add_amount_total: round2(addAmountTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      split_limit: SPLIT_LIMIT,
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
    disclaimer: '只核"买价 × 扣除率 = 可抵扣进项"与"可抵扣进项 × 加计比例 = 加计扣除额"这类**表内勾稽**与档位提示，'
      + '**不判断该笔农产品该用哪一档扣除率、能否加计扣除**（以主管税务机关口径与税务师意见为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
