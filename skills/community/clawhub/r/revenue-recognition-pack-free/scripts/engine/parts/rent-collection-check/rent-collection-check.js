/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * rent-collection-check.js —— 租金收缴与欠租台账核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月收租之后、月报出具之前**。商办 / 产业园的物业或资产管理岗
 * 每个月都要把「应收租金、已收、欠租、滞纳金、免租期」逐户勾稽一遍 —— 欠租台账对不上，
 * 钱收不回来，责任也说不清（是租户没交、台账记错、还是免租期与计租期重叠，全糊在一起）。
 *
 * 好消息是这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应收租金 = 计租面积 × 租金单价 × 计租月数（没有面积与单价时按「合同月租金 × 计租月数」）
 *   欠租金额 = 应收租金 + 滞纳金 − 已收金额
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**应收租金该按含税还是不含税口径确认、免租期该怎么分摊、递增租金怎么切年度
 *    （那属于合同与会计判断）：表里的面积、单价、月数、合同月租金一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成「没删干净」而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应收租金复算（计租面积 × 租金单价 × 计租月数，或合同月租金 × 计租月数）',
  '欠租金额复算（应收租金 + 滞纳金 − 已收金额）',
  '合计行逐列复核',
  '同一房号同一期间重复行检测',
  '空白与占位符检测',
  '金额或面积为负检测',
];

const CHECKS_WITHHELD = [
  '已收金额超过应收租金加滞纳金提示（多收 / 预收挂账、租户退款）',
  '免租期内仍计租提示（同一行既有免租期天数又有计租月数，免租期与计租期重叠）',
  '欠租超过参考月数（3 个月）提示',
  '同一房号重复计租同一期间提示（换租户 / 双合同把同一期间算了两遍）',
  '滞纳金比例与合同约定不一致提示',
];

const OUT_OF_SCOPE = [
  '判断应收租金该按什么口径确认（含税 / 不含税、租金递增条款怎么切年度、免租期怎么分摊到各期、跨期收款如何挂账，属于合同与会计判断，请咨询会计师）',
  '核对租赁合同条款本身（递增率、免租期起止日、押金抵租、滞纳金基数与上限、违约金）对台账的影响',
  '判断滞纳金该按含税租金还是不含税租金为基数计提（基数口径属于合同与税务判断）',
  '处理增值税、房产税、印花税与租赁收入跨期分摊的会计与税务处理',
  '读取物业管理系统 / 收费系统 / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t项目名称\t房号\t租户名称\t合同编号\t计租面积\t租金单价\t计租月数\t合同月租金\t应收租金\t已收金额\t欠租金额\t滞纳金\t滞纳金比例\t合同约定滞纳金比例\t免租期天数',
  '2026-01\t星辰大厦\tA-101\t云图科技\tHT-2026-101\t120.00\t85.00\t1\t10200.00\t10200.00\t10200.00\t0.00\t0.00\t0.05%\t0.05%\t0',
  '2026-02\t星辰大厦\tA-101\t云图科技\tHT-2026-101\t120.00\t85.00\t1\t10200.00\t10200.00\t8000.00\t2200.00\t0.00\t0.05%\t0.05%\t0',
  '2026-03\t星辰大厦\tA-101\t云图科技\tHT-2026-101\t120.00\t85.00\t1\t10200.00\t10200.00\t4000.00\t6220.00\t20.00\t0.05%\t0.05%\t0',
  '2026-01\t星辰大厦\tA-102\t弘毅咨询\tHT-2026-102\t80.00\t95.00\t1\t7600.00\t7600.00\t7600.00\t0.00\t0.00\t0.05%\t0.05%\t0',
  '2026-02\t星辰大厦\tA-102\t弘毅咨询\tHT-2026-102\t80.00\t95.00\t1\t7600.00\t7600.00\t7600.00\t0.00\t0.00\t0.05%\t0.05%\t0',
  '2026-03\t星辰大厦\tA-102\t弘毅咨询\tHT-2026-102\t80.00\t95.00\t1\t7600.00\t7600.00\t7600.00\t0.00\t0.00\t0.05%\t0.05%\t0',
  '2026-01\t产业园\tB-201\t恒达物流\tHT-2026-201\t300.00\t32.00\t1\t9600.00\t9600.00\t9600.00\t0.00\t0.00\t0.05%\t0.05%\t0',
  '合计\t\t\t\t\t900.00\t\t\t\t63000.00\t54600.00\t8420.00\t20.00\t\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.00005;      // 比例容差：0.005 个百分点
const ARREARS_MONTHS = 3;      // 欠租参考月数：欠租合计超过月租金的 3 倍就提示

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    ·「合同约定滞纳金比例」必须排在「滞纳金比例」与「滞纳金」前面，否则比例列会互相覆盖；
  //    ·「免租期天数」必须排在「天数」前面（否则天数列被更宽泛的别名抢走）；
  //    ·「滞纳金」「已收金额」「欠租金额」「应收租金」都必须排在兜底的「金额」前面。
  period: ['所属期间', '会计期间', '账单期间', '所属月份', '所属期', '期间'],
  project: ['项目名称', '园区名称', '楼盘名称', '管理处名称', '项目', '园区', '楼盘'],
  room: ['房号', '房间号', '铺位号', '单元号', '商铺号', '物业编号'],
  tenant: ['租户名称', '承租方名称', '承租方', '客户名称', '商户名称', '租户', '业户名称'],
  contract: ['租赁合同编号', '租赁合同号', '合同编号', '合同号', '租约编号'],
  area: ['计租面积', '建筑面积', '租赁面积', '面积'],
  unitPrice: ['租金单价', '月租金单价', '单位租金', '每平方米单价', '单价'],
  contractRent: ['合同月租金', '标准月租金', '合同租金', '月租金'],
  months: ['计租月数', '计租月份', '计租期数', '计租月', '月数'],
  freeDays: ['免租期天数', '免租天数', '装修期天数', '免租期', '免租月数'],
  billingDays: ['计租天数', '计费天数', '实际计租天数', '天数'],
  receivable: ['应收租金', '本期应收租金', '应收金额', '应计租金', '应收'],
  received: ['已收金额', '本期已收金额', '实收金额', '已收租金', '收款金额', '已收'],
  arrears: ['欠租金额', '欠收金额', '欠租余额', '欠租', '欠费'],
  contractLateRate: ['合同约定滞纳金比例', '合同滞纳金比例', '约定滞纳金比例'],
  lateFeeRate: ['滞纳金比例', '滞纳金费率', '违约金比例'],
  lateFee: ['滞纳金', '违约金', '逾期违约金'],
  amount: ['金额', '发生额'],
};

const LABELS = {
  period: '所属期间', project: '项目名称', room: '房号', tenant: '租户名称', contract: '合同编号',
  area: '计租面积', unitPrice: '租金单价', contractRent: '合同月租金', months: '计租月数',
  freeDays: '免租期天数', billingDays: '计租天数', receivable: '应收租金', received: '已收金额',
  arrears: '欠租金额', contractLateRate: '合同约定滞纳金比例', lateFeeRate: '滞纳金比例',
  lateFee: '滞纳金', amount: '金额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'room', 'months', 'receivable', 'received', 'arrears', 'lateFee'];
/** 合计行逐列复核的列（面积与各金额列；月数、单价、比例、天数不求和） */
const SUM_ROLES = ['area', 'receivable', 'received', 'arrears', 'lateFee'];
/**
 * 免费档负值检测覆盖的列。
 * ⚠️ 刻意**不含欠租金额** —— 欠租为负 = 多收 / 预收挂账，那正是完整档
 *    「已收金额超过应收租金加滞纳金」要出的结论（见 CHECKS_WITHHELD）；
 *    免费档提前报出「欠租金额为负」就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['area', 'unitPrice', 'contractRent', 'receivable', 'received', 'lateFee'];
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

/** 比例归一化成小数：`0.05%` ⇒ 0.0005；`0.0005` ⇒ 0.0005；`5` ⇒ 0.05 */
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

const cellOf = (it, role) => (it && it[role] !== undefined && it[role] !== null
  ? String(it[role]).trim() : '');

const roomKeyOf = (it) => cellOf(it, 'room');
const periodKeyOf = (it) => cellOf(it, 'period');
const contractKeyOf = (it) => cellOf(it, 'contract');
const tenantKeyOf = (it) => cellOf(it, 'tenant');

const who = (it) => {
  const p = periodKeyOf(it) || `第 ${it && it.line} 行`;
  const n = [cellOf(it, 'project'), roomKeyOf(it), tenantKeyOf(it)].filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

/** 该房该期的月租金：优先「计租面积 × 租金单价」，没有就用「合同月租金」 */
/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkReceivableRecompute(it) {
  const out = [];
  const months = normNumber(it.months);
  const stated = normNumber(it.receivable);
  if (months === null || stated === null) return out;
  if (months <= 0) return out;                 // 计租月数填 0 或负：算不出应收租金（负值由负值检测报）
  const area = normNumber(it.area);
  const price = normNumber(it.unitPrice);
  const rent = normNumber(it.contractRent);
  let expect = null;
  let how = '';
  if (area !== null && price !== null) {
    expect = round2(area * price * months);
    how = `计租面积 ${area.toFixed(2)} × 租金单价 ${price.toFixed(2)} × 计租月数 ${months}`;
  } else if (rent !== null) {
    expect = round2(rent * months);
    how = `合同月租金 ${rent.toFixed(2)} × 计租月数 ${months}`;
  }
  if (expect === null) return out;
  if (Math.abs(stated - expect) <= TOL) return out;
  out.push({
    level: 'P0', category: '应收租金复算不符', line: it.line,
    message: `${who(it)}：${how} = ${expect.toFixed(2)}，`
      + `表里「应收租金」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '应收租金是整条收缴链的起点：这里少算就是漏收，多算就是虚增应收（租户拿到账单会直接不认）。',
  });
  return out;
}

function checkArrearsRecompute(it) {
  const out = [];
  const rec = normNumber(it.receivable);
  const pay = normNumber(it.received);
  const fee = normNumber(it.lateFee);
  const stated = normNumber(it.arrears);
  if (rec === null || pay === null || fee === null || stated === null) return out;
  const expect = round2(rec + fee - pay);
  if (Math.abs(stated - expect) <= TOL) return out;
  out.push({
    level: 'P0', category: '欠租金额复算不符', line: it.line,
    message: `${who(it)}：应收租金 ${rec.toFixed(2)} + 滞纳金 ${fee.toFixed(2)} − 已收金额 ${pay.toFixed(2)} `
      + `= ${expect.toFixed(2)}，表里「欠租金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '欠租台账对不上，既收不回钱也说不清责任：是租户少交、还是已收没入账、还是滞纳金没加进去。',
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
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报与催收清单的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const room = roomKeyOf(it);
    const p = periodKeyOf(it);
    if (!room || !p) continue;
    const key = `${room}|${p}|${contractKeyOf(it)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一房号同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一房号、同一期间、同一合同再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔租金被拆成两行登记，多出来的那一行会把应收、已收与欠租都重复计一遍。',
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
        const s = cellOf(it, role);
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
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额或面积为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 计租面积、租金单价、合同月租金、`
        + '应收租金、已收金额与滞纳金都不该为负；冲回 / 红字应单独列示并在备注里说明原因。',
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
    return insufficient('没有收到租金收缴与欠租台账核对表正文（text）—— 请把「所属期间 / 房号 / 计租面积 / 租金单价 / 计租月数 / 合同月租金 / 应收租金 / 已收金额 / 欠租金额 / 滞纳金」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `租金收缴与欠租台账核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  const headerRoles = splitRow(text.split(/\r?\n/)[0]).map((h) => roleOf(h));
  const hasRole = (r) => headerRoles.indexOf(r) >= 0;
  if (!((hasRole('area') && hasRole('unitPrice')) || hasRole('contractRent'))) {
    return insufficient([
      '租金收缴与欠租台账核对表缺少租金基数列：既没有「计租面积 + 租金单价」，也没有「合同月租金」',
      '没有租金基数就算不出应收租金，也核不了欠租 —— 本工具不替你猜月租金。',
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何房号租金明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it) || `第 ${it.line} 行`;
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkReceivableRecompute(it));
    findings.push(...checkArrearsRecompute(it));
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

  let receivableTotal = 0;
  let receivedTotal = 0;
  let arrearsTotal = 0;
  let lateFeeTotal = 0;
  for (const it of t.items) {
    const rec = normNumber(it.receivable);
    if (rec !== null) receivableTotal += rec;
    const pay = normNumber(it.received);
    if (pay !== null) receivedTotal += pay;
    const arr = normNumber(it.arrears);
    if (arr !== null) arrearsTotal += arr;
    const fee = normNumber(it.lateFee);
    if (fee !== null) lateFeeTotal += fee;
  }

  const result = {
    status: 'success',
    service_type: 'RENT_COLLECTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      receivable_total: round2(receivableTotal),
      received_total: round2(receivedTotal),
      arrears_total: round2(arrearsTotal),
      late_fee_total: round2(lateFeeTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      arrears_reference_months: ARREARS_MONTHS,
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
    disclaimer: '只核"计租面积 × 租金单价 × 计租月数（或合同月租金 × 计租月数）= 应收租金"与'
      + '"应收租金 + 滞纳金 − 已收金额 = 欠租金额"这类**表内勾稽**与档位提示，'
      + '**不判断应收租金该按含税还是不含税口径确认、免租期怎么分摊、递增租金怎么切年度**'
      + '（以租赁合同与会计师口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
