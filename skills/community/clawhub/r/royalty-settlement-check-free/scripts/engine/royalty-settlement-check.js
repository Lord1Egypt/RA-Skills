/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * royalty-settlement-check.js —— 版税与授权金结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每季度（或每半年）结算版税与授权金的时候**。出版社 / IP 方 /
 * 内容公司每到结算节点都要按合同逐笔算版税（按印数或按实际销售、退货冲减、阶梯费率）
 * 与授权金，再把预付（保底）冲抵干净。这张表算错，方向只有两个 ——
 * **少收钱**（该收的版税没收到）或**多付钱**（预付没冲、费率用错档），
 * 两条都会在作者/版权方对账、审计抽样和收入确认上暴露出来。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   净销售数量 = 销售数量 − 退货数量
 *   应付版税   = 净销售数量 × 定价 × 版税率        （表里有「定价」列时，按码洋口径）
 *              = 净销售数量 × 每册/每件固定版税    （表里没有「定价」列时，按每册/每件口径）
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**合同约定的版税率 / 阶梯档位 / 预付（保底）条款本身是否合理
 *    （那属于合同与商务判断）：表里给的定价、版税率、合同约定版税率、阶梯费率一律
 *    **以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '净销售数量复算（销售数量 − 退货数量 = 净销售数量）',
  '应付版税复算（净销售数量 × 定价 × 版税率 = 应付版税）',
  '合计行逐列复核',
  '同一书号/授权标的同一期间重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '退货数量超过销售数量提示（退货冲减后净销量为负）',
  '版税率与合同约定版税率不一致提示',
  '阶梯费率未按累计销售数量切换提示',
  '预付版税未冲抵提示（预付余额大于本期应付版税）',
  '同一授权标的同一期间重复结算提示（不同书号、同一标的）',
];

const OUT_OF_SCOPE = [
  '判断合同约定的版税率、阶梯档位、保底（预付）条款本身是否合理或是否到期调整（属于合同与商务判断，请咨询合约 / 法务）',
  '核对「按印数计提」与「按实际销售计提」两种口径之争（由合同条款约定，本工具只核表内勾稽，不替你选口径）',
  '处理版税预提、暂估、跨期分摊与收入确认的会计处理（以企业会计准则与会计师口径为准）',
  '处理代扣代缴个人所得税、增值税与跨境付汇的税务处理（请咨询税务师）',
  '读取出版业务系统 / ERP / 电商后台的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t书号\t授权标的\t销售数量\t退货数量\t净销售数量\t定价\t版税率\t合同约定版税率\t阶梯费率\t累计销售数量\t应付版税\t预付版税余额',
  '2026Q1\t978-7-101-00001-1\t《长夜书》\t30000\t2000\t28000\t45.00\t8%\t8%\t8%\t28000\t100800.00\t0.00',
  '2026Q2\t978-7-101-00001-1\t《长夜书》\t35000\t1000\t34000\t45.00\t10%\t8%\t10%\t62000\t153000.00\t0.00',
  '2026Q1\t978-7-101-00002-8\t《山海图志》\t12000\t500\t11500\t68.00\t6%\t6%\t6%\t11500\t46920.00\t0.00',
  '2026Q2\t978-7-101-00002-8\t《山海图志》\t9000\t0\t9000\t68.00\t7%\t6%\t7%\t20500\t42840.00\t0.00',
  '2026Q1\tIP-2026-007\t《山海图志》文创授权\t2000\t0\t2000\t\t2.50\t2.50\t\t2000\t5000.00\t0.00',
  '合计\t\t\t88000\t3500\t84500\t\t\t\t\t124000\t348560.00\t0.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;      // 费率容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    必须排在前面的（否则宽泛别名会把更具体的那列抢走，抢走不报错、只会算错）：
  //      「累计销售数量」在「净销售数量」「销售数量」之前；
  //      「净销售数量」在「销售数量」之前；
  //      「应付版税」在「版税率」之前；
  //      「阶梯费率」「合同约定版税率」在「版税率」之前。
  period: ['所属期间', '结算期间', '所属期', '期间', '季度', '月份'],
  isbn: ['书号', 'ISBN', '国际标准书号', '统一书号', '授权编号', '标的编号'],
  title: ['授权标的', '标的名称', '作品名称', '书名', '品名'],
  cumQty: ['累计销售数量', '累计销量', '累计销售数', '累计数量'],
  netQty: ['净销售数量', '净销量', '净销售数', '实际销售数量'],
  returnQty: ['退货数量', '退货册数', '退回数量', '退货数'],
  soldQty: ['销售数量', '销售册数', '销售数', '销售'],
  price: ['码洋单价', '图书定价', '定价', '单价'],
  payable: ['应付版税', '应结版税', '本期应付版权金', '版税金额', '应付授权金'],
  prepaid: ['预付版税余额', '预付版税', '预付余额', '已预付版税'],
  tierRate: ['阶梯费率', '阶梯版税率', '阶梯比例'],
  contractRate: ['合同约定版税率', '合同版税率', '约定版税率', '合同约定费率'],
  rate: ['版税率', '版权费率', '费率'],
};

const LABELS = {
  period: '所属期间', isbn: '书号 / 授权编号', title: '授权标的', soldQty: '销售数量',
  returnQty: '退货数量', netQty: '净销售数量', price: '定价', rate: '版税率',
  contractRate: '合同约定版税率', tierRate: '阶梯费率', cumQty: '累计销售数量',
  payable: '应付版税', prepaid: '预付版税余额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'isbn', 'title', 'soldQty', 'returnQty', 'netQty', 'rate', 'payable'];
/** 合计行逐列复核的列（都是可加总的流量口径；「预付版税余额」是余额，刻意不参与加总） */
const SUM_ROLES = ['soldQty', 'returnQty', 'netQty', 'cumQty', 'payable'];
/**
 * 免费档负值检测覆盖的列。
 * ⚠️ 刻意**不含**「净销售数量」与「应付版税」：退货数量超过销售数量时这两列必然为负，
 *    而"退货超过销售"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出它们为负就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['soldQty', 'returnQty', 'cumQty', 'price', 'prepaid', 'rate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：)$/;

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

/** 费率归一化成小数：`8%` ⇒ 0.08；`0.08` ⇒ 0.08；`8` ⇒ 0.08 */
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
  const n = [it && it.isbn, it && it.title]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/** 标的名的归一化：去掉书名号/括号/空白，同一部作品的不同写法要能撞上 */
/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkNetQtyRecompute(it) {
  const out = [];
  const sold = normNumber(it.soldQty);
  const back = normNumber(it.returnQty);
  const stated = normNumber(it.netQty);
  if (sold === null || back === null || stated === null) return out;
  const expect = round2(sold - back);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '净销售数量复算不符', line: it.line,
    message: `${who(it)}：销售数量 ${sold} − 退货数量 ${back} = ${expect}，`
      + `表里「净销售数量」是 ${stated}，相差 ${round2(stated - expect)}。`
      + '净销量是全部版税计算的乘数：退货冲减没做、或者只冲了一部分，后面每一笔版税都会跟着错。',
  });
  return out;
}

function checkRoyaltyRecompute(it) {
  const out = [];
  const net = normNumber(it.netQty);
  const stated = normNumber(it.payable);
  if (net === null || stated === null) return out;
  const price = normNumber(it.price);
  let expect = null;
  let how = '';
  if (price !== null) {
    const rate = rateValue(it.rate);
    if (rate === null) return out;
    expect = round2(net * price * rate);
    how = `净销售数量 ${net} × 定价 ${price.toFixed(2)} × 版税率 ${(rate * 100).toFixed(4)}%`;
  } else {
    if (/%/.test(String(it.rate))) return out;      // 百分率却没有「定价」列：算不出基数，不猜
    const flat = normNumber(it.rate);
    if (flat === null) return out;
    expect = round2(net * flat);
    how = `净销售数量 ${net} × 每册/每件版税 ${flat.toFixed(2)}`;
  }
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应付版税复算不符', line: it.line,
    message: `${who(it)}：${how} = ${expect.toFixed(2)}，`
      + `表里「应付版税」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '版税算少了就是少收钱（作者/版权方一定会来对账），算多了就是多付钱；两个方向都要改。',
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
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是开票、对账与收入确认的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const c = it.isbn !== undefined ? String(it.isbn).trim() : '';
    if (!p || !c) continue;
    const key = `${p}|${c}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一书号同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一书号再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔结算被拆成两行（比如按渠道各建一行却忘了标渠道）。'
          + '多出来的那一行会把销量、码洋与版税都重复计一遍，开票金额会直接翻倍。',
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
    const v = role === 'rate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'rate' ? `${(v * 100).toFixed(4)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 销售数量、退货数量、累计销量、定价、版税率与预付余额都不该为负，`
        + '冲回 / 红字应单独列示并在备注里说明。',
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
    return insufficient('没有收到版税与授权金结算核对表正文（text）—— 请把「所属期间 / 书号 / 授权标的 / 销售数量 / 退货数量 / 净销售数量 / 定价 / 版税率 / 应付版税」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `版税与授权金结算核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何结算明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkNetQtyRecompute(it));
    findings.push(...checkRoyaltyRecompute(it));
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

  let royaltyTotal = 0;
  let netQtyTotal = 0;
  for (const it of t.items) {
    const r = normNumber(it.payable);
    if (r !== null) royaltyTotal += r;
    const q = normNumber(it.netQty);
    if (q !== null) netQtyTotal += q;
  }

  const result = {
    status: 'success',
    service_type: 'ROYALTY_SETTLEMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      royalty_total: round2(royaltyTotal),
      net_qty_total: round2(netQtyTotal),
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
    disclaimer: '只核"销售数量 − 退货数量 = 净销售数量"与"净销售数量 × 定价 × 版税率 = 应付版税"这类**表内勾稽**与档位提示，'
      + '**不判断合同约定的版税率、阶梯档位、预付（保底）条款本身是否合理**（以合同与会计师口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
