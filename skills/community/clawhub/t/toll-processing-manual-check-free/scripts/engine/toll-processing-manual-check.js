/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * toll-processing-manual-check.js —— 加工贸易手册与保税料件核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月（以及每本手册核销前）**。加工贸易企业用手册保税进口料件、
 * 出口成品，海关按"备案单耗"核销：进口保税料件、出口成品、单耗、余料结转、内销补税
 * 必须与手册备案数逐项勾稽。对不上就是**手册核销不了**（要补税、缓税利息，重的还有处罚）；
 * 看着对上了的，也常常是同一本手册里的料件被重复算了一次。
 *
 * 好消息是这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   理论耗用 = 出口成品数量 × 单耗
 *   期末结存 = 期初结存 + 进口料件 − 理论耗用 − 余料结转 − 内销补税数量
 *   合计行各列 = 明细行逐列相加（单耗是比率，不参与加总）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某本手册该按什么单耗/损耗率备案、内销补税该按什么完税价格与税率、
 *    展期后新旧备案数该如何衔接（那些属于海关加工贸易监管与关务判断）：表里的备案数量、
 *    单耗、期初结存一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的档位开关算成一个布尔常量，再把付费检查包进以该常量为
 *    条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER —— 两个形态同时存在时
 *    `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包跳过（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '理论耗用复算（出口成品数量 × 单耗 = 理论耗用数量）',
  '期末结存滚动复算（期初结存 + 进口料件 − 理论耗用 − 余料结转 − 内销补税数量 = 期末结存）',
  '合计行逐列复核',
  '同一手册号同一料件同一期间重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '实际耗用超过理论耗用提示（实际耗用大于出口成品数量 × 单耗，超容差才报）',
  '期末结存为负提示（结存倒挂，说明耗用与进出口对不上）',
  '内销补税数量占总进口比例超过参考上限（10%）提示',
  '同一手册同一料件重复申报出口提示（同一出口报关单号出现在多行）',
  '余料结转数量超过期初加进口提示',
];

const OUT_OF_SCOPE = [
  '判断某本手册该按什么单耗、什么损耗率备案（备案单耗的申报口径属于海关加工贸易监管核定，请以海关备案数据与报关员口径为准）',
  '核对实际进出口报关单是否已全部申报（本工具只核你贴进来的这张表，不去查海关单一窗口 / 金关二期数据）',
  '判断内销补税该按什么完税价格、什么税率、什么汇率补（属于海关与税务判断）',
  '处理手册展期 / 变更 / 余料结转的审批流程是否合规（展期后新旧备案数的合法衔接由海关手册审批决定）',
  '读取 ERP / 关务系统 / Excel 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t手册号\t料件名称\t单位\t备案数量\t期初结存数量\t进口料件数量\t出口成品数量\t单耗\t理论耗用数量\t实际耗用数量\t余料结转数量\t内销补税数量\t期末结存数量\t保税料件金额\t出口报关单号',
  '2026-01\tB2202512345678\t聚酯薄膜\t千克\t10000\t1200\t5000\t2000\t1.05\t2100\t2100\t0\t100\t4000\t40000.00\t5316202600001',
  '2026-01\tB2202512345678\t铝箔\t千克\t8000\t800\t3000\t1000\t1.20\t1200\t1200\t200\t0\t2400\t24000.00\t5316202600002',
  '2026-01\tB2202598765432\t铜箔\t千克\t5000\t500\t2500\t1500\t1.00\t1500\t1500\t0\t0\t1500\t15000.00\t5316202600003',
  '2026-02\tB2202512345678\t聚酯薄膜\t千克\t10000\t4000\t3000\t2000\t1.05\t2100\t2050\t0\t150\t4750\t47500.00\t5316202600004',
  '2026-02\tB2202512345678\t铝箔\t千克\t8000\t2400\t2000\t1000\t1.20\t1200\t1200\t100\t0\t3100\t31000.00\t5316202600005',
  '2026-02\tB2202598765432\t铜箔\t千克\t5000\t1500\t1500\t1500\t1.00\t1500\t1400\t0\t0\t1500\t15000.00\t5316202600006',
  '合计\t\t\t\t46000\t10400\t17000\t9000\t\t9600\t9450\t300\t250\t17250\t172500.00\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「手册备案数量」不能被「手册」抢走（所以手册号一类别名里**不放**裸的「手册」）；
  //    「进口料件数量」「出口成品数量」「余料结转数量」「期末结存数量」「备案数量」
  //    统统要排在兜底的「数量」**前面**；「实际耗用数量」也不能被「耗用数量」抢走。
  period: ['所属期间', '所属期', '会计期间', '所属月份', '期间', '月份', '月度'],
  manual: ['加工贸易手册号', '电子手册号', '手册编号', '手册代码', '手册号'],
  item: ['料件名称', '料件编号', '料件编码', '商品名称', '商品编码', '成品名称', '品名', '货品名称'],
  unit: ['计量单位', '单位', '计量'],
  filedQty: ['手册备案数量', '备案数量', '备案料件数量', '备案数'],
  begin: ['期初结存数量', '期初库存数量', '上期结存数量', '期初结存', '期初数量'],
  importQty: ['进口料件数量', '进口保税料件数量', '保税进口数量', '进口数量'],
  exportQty: ['出口成品数量', '成品出口数量', '出口数量'],
  unitUsage: ['单耗', '单耗量'],
  actualUsage: ['实际耗用数量', '实际耗用量', '实际耗用'],
  theoryUsage: ['理论耗用数量', '理论耗用量', '理论耗用', '耗用数量', '耗料数量'],
  carryOver: ['余料结转数量', '余料结转量', '结转数量', '余料结转'],
  domesticQty: ['内销补税数量', '内销数量', '补税数量', '内销补税'],
  end: ['期末结存数量', '期末库存数量', '期末结存', '期末数量'],
  amount: ['保税料件金额', '料件金额', '保税金额', '金额'],
  declNo: ['出口报关单号', '出口报关单', '报关单号'],
  qty: ['数量'],
};

const LABELS = {
  period: '所属期间', manual: '手册号', item: '料件名称', unit: '单位', filedQty: '备案数量',
  begin: '期初结存数量', importQty: '进口料件数量', exportQty: '出口成品数量', unitUsage: '单耗',
  actualUsage: '实际耗用数量', theoryUsage: '理论耗用数量', carryOver: '余料结转数量',
  domesticQty: '内销补税数量', end: '期末结存数量', amount: '保税料件金额', declNo: '出口报关单号',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'manual', 'item', 'filedQty', 'begin', 'importQty', 'exportQty',
  'unitUsage', 'theoryUsage', 'carryOver', 'domesticQty', 'end'];
/** 合计行逐列复核的列（**不含单耗**：单耗是"每单位成品的耗用量"这种比率，加总没有意义） */
const SUM_ROLES = ['filedQty', 'begin', 'importQty', 'exportQty', 'theoryUsage', 'actualUsage',
  'carryOver', 'domesticQty', 'end', 'amount'];
/**
 * 免费档负值检测覆盖的列：**数量与金额**。
 * ⚠️ 刻意**不含期末结存数量** —— "结存为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出结存为负就等于把付费结论送出去了（与参考引擎不报"期末本金为负"同一个道理）。
 */
const NEGATIVE_ROLES = ['filedQty', 'begin', 'importQty', 'exportQty', 'unitUsage', 'actualUsage',
  'theoryUsage', 'carryOver', 'domesticQty', 'amount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;

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

const round2 = (n) => Math.round(n * 100) / 100;

/** 数量显示：整数就不带小数点，避免同一格在结论里 2100 与 2100.00 两种写法来回跳 */
const showQty = (n) => String(round2(n));

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
  const n = [it && it.manual, it && it.item]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const manualKeyOf = (it) => {
  const m = it && it.manual !== undefined ? String(it.manual).trim() : '';
  return m || `第 ${it && it.line} 行`;
};

const itemKeyOf = (it) => {
  const v = it && it.item !== undefined ? String(it.item).trim() : '';
  return v || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkTheoryRecompute(it) {
  const out = [];
  const exportQty = normNumber(it.exportQty);
  const usage = normNumber(it.unitUsage);
  const stated = normNumber(it.theoryUsage);
  if (exportQty === null || usage === null || stated === null) return out;
  const expect = round2(exportQty * usage);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '理论耗用复算不符', line: it.line,
    message: `${who(it)}：出口成品数量 ${showQty(exportQty)} × 单耗 ${showQty(usage)} = ${showQty(expect)}，`
      + `表里「理论耗用数量」是 ${showQty(stated)}，相差 ${showQty(stated - expect)}。`
      + '单耗是"每单位出口成品耗用多少保税料件"，理论耗用就靠它撑起来：'
      + '这一格错，后面的期末结存与手册核销数会全跟着错（耗用报大了就是料件对不上，报小了就是结存虚增）。',
  });
  return out;
}

function checkBalanceRolling(it) {
  const out = [];
  const begin = normNumber(it.begin);
  const importQty = normNumber(it.importQty);
  const theory = normNumber(it.theoryUsage);
  const carry = normNumber(it.carryOver);
  const domestic = normNumber(it.domesticQty);
  const stated = normNumber(it.end);
  if (begin === null || importQty === null || theory === null || carry === null
    || domestic === null || stated === null) return out;
  const expect = round2(begin + importQty - theory - carry - domestic);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末结存滚动复算不符', line: it.line,
    message: `${who(it)}：期初结存 ${showQty(begin)} + 进口料件 ${showQty(importQty)} − 理论耗用 ${showQty(theory)}`
      + ` − 余料结转 ${showQty(carry)} − 内销补税数量 ${showQty(domestic)} = ${showQty(expect)}，`
      + `表里「期末结存数量」是 ${showQty(stated)}，相差 ${showQty(stated - expect)}。`
      + '保税料件的账就是这么滚的：结存对不上，要么是进出口 / 耗用漏了一笔，'
      + '要么是余料结转或内销补税没有在这个料件上体现 —— 核销时海关就是拿这一格对账的。',
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
      message: `合计行的「${LABELS[role]}」是 ${showQty(stated)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${showQty(expect)}，`
        + `相差 ${showQty(stated - expect)}。合计行就是手册核销表的取数口径（也是交给海关的汇总数）：`
        + '对不上说明有一边错，而核销时这一列是要逐项对得上的。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const m = it.manual !== undefined ? String(it.manual).trim() : '';
    const i = it.item !== undefined ? String(it.item).trim() : '';
    if (!p || !m || !i) continue;
    const key = `${p}|${m}|${i}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一手册号同一料件同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一手册、同一料件再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一料件的两次进口/出口各建了一行（比如按报关单拆行）。'
          + '多出来的那一行会把进口、耗用与结存都重复算一遍：手册余额当场虚增，核销必卡。'
          + '若确实是两笔业务，请按报关单分行并在备注里写明来源，别让同一口径出现两遍。',
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
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查'
            + '（手册核销时海关不会接受"这一列先空着"）。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${showQty(v)}（负数）—— `
        + '保税料件的备案、进口、出口、单耗、耗用、结转与内销数量，以及保税料件金额都不该为负。'
        + '红字冲回 / 退运 / 退料应单独列示并在备注里说明来源；负数往往意味着"减项被填成了一张独立行"、'
        + '符号掉了、或者把结转写成了 −（本工具不接受"用负数表示方向"这种填法）。',
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
    return insufficient('没有收到加工贸易手册与保税料件核对表正文（text）—— 请把「所属期间 / 手册号 / 料件名称 / 备案数量 / 期初结存数量 / 进口料件数量 / 出口成品数量 / 单耗 / 理论耗用数量 / 余料结转数量 / 内销补税数量 / 期末结存数量」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `加工贸易手册与保税料件核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何料件明细行');
  }

  const periods = new Set();
  for (const it of t.items) periods.add(periodKeyOf(it));

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkTheoryRecompute(it));
    findings.push(...checkBalanceRolling(it));
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

  let importTotal = 0;
  let exportTotal = 0;
  let domesticTotal = 0;
  for (const it of t.items) {
    const i = normNumber(it.importQty);
    if (i !== null) importTotal += i;
    const e = normNumber(it.exportQty);
    if (e !== null) exportTotal += e;
    const d = normNumber(it.domesticQty);
    if (d !== null) domesticTotal += d;
  }

  const result = {
    status: 'success',
    service_type: 'TOLL_PROCESSING_MANUAL_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      totals_row: Boolean(t.totals && t.totals.row),
      import_qty_total: round2(importTotal),
      export_qty_total: round2(exportTotal),
      domestic_qty_total: round2(domesticTotal),
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
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"出口成品数量 × 单耗 = 理论耗用数量"与"期初结存 + 进口料件 − 理论耗用 − 余料结转 − 内销补税数量 = 期末结存"'
      + '这类**表内勾稽**与档位提示，**不判断某本手册该按什么单耗备案、内销补税该按什么完税价格与税率**'
      + '（以海关备案数据、报关员与关务口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
