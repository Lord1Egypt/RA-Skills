'use strict';
/**
 * utility-meter-reading-check.js —— 水电抄表与账单核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月抄表出账前后**，物业 / 园区 / 工厂要把
 * 「上期读数 → 本期读数 → 用量 → 单价 → 应收金额 → 账单金额」**逐户勾稽**一遍，
 * 再拿账单金额与应收金额对上。抄错一位数就是钱：用量、金额、账单三者必须闭合，
 * 而这些关系**全都是纯算术，能一条条手算复现**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   用量     = 本期读数 − 上期读数
 *   应收金额 = 用量 × 单价 + 基本费
 *   合计行   = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**水价/电价标准：单价以合同与供水供电公司账单为准，
 *    只对"明显偏离常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '用量勾稽（用量 = 本期读数 − 上期读数）',
  '应收金额勾稽（应收金额 = 用量 × 单价 + 基本费）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '同一表号同一期间重复行检测',
  '关键字段缺失与占位符检测（期间/表号/上期读数/本期读数/用量/单价/应收金额）',
  '读数或金额为负检测（上期读数/本期读数/应收金额/账单金额）',
];

const CHECKS_WITHHELD = [
  '本期读数小于上期读数（倒走）检测',
  '账单金额与应收金额不符提示（含差额）',
  '单价偏离参考区间提示（参考口径）',
  '用量异常偏高提示（超过同表历史均值 50%）',
  '换表未标注或底度未结转提示',
];

const OUT_OF_SCOPE = [
  '判断你当地的水价/电价标准、阶梯加价与政府性基金（请以供水/供电公司账单与合同为准）',
  '核对抄表读数是否与现场表盘一致（那需要现场抄表记录或照片）',
  '处理滞纳金、违约金、补收与退款（请把它们单列成一行再核对）',
  '分摊总表与分表之间的损耗（请先算出分摊结果再填进本表）',
  '读取 .xlsx 或物业收费系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显偏离"时提示，单位 元/吨、元/度 */
const PRICE_REF = {
  water: [1.0, 10.0],
  electricity: [0.2, 2.5],
  other: [0.2, 12.0],
};

const SAMPLE_HEAD = ['期间', '户号', '表号', '表类型', '上期读数', '本期读数', '用量',
  '单价', '基本费', '应收金额', '账单金额', '历史平均用量', '是否换表', '换表底度'];

const SAMPLE_ROWS = [
  ['2026-01', 'A-001', 'W-1001', '水表', '1000.00', '1050.00', '50.00', '4.20', '0.00', '210.00', '210.00', '50.00', '否', ''],
  ['2026-02', 'A-001', 'W-1001', '水表', '1050.00', '1112.00', '62.00', '4.20', '0.00', '260.40', '260.40', '50.00', '否', ''],
  ['2026-01', 'A-002', 'E-2001', '电表', '20000.00', '21400.00', '1400.00', '0.85', '300.00', '1490.00', '1490.00', '1400.00', '否', ''],
  ['2026-02', 'A-002', 'E-2001', '电表', '21400.00', '22900.00', '1500.00', '0.85', '300.00', '1575.00', '1575.00', '1400.00', '否', ''],
];

/* 合计行 = 各列之和（只对"可加"的列求和：用量 / 基本费 / 应收金额 / 账单金额） */
const SAMPLE_TOTAL = ['合计', '', '', '', '', '', '3012.00', '', '600.00', '3535.40', '3535.40', '', '', ''];

const SAMPLE_TEXT = [SAMPLE_HEAD].concat(SAMPLE_ROWS, [SAMPLE_TOTAL])
  .map((r) => r.join('\t')).join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名必须排在更宽泛的前面**。
  //    实测过的抢列：`历史平均用量` 会被宽泛的 `用量` 抢走（历史列变成用量列）；
  //    `换表底度` 会被宽泛的 `换表` 抢走（底度列变成换表标记列）。
  //    被抢走的列不会报错，只会**静默地不参与检查 / 算错**，所以顺序是硬要求。
  period: ['抄表期间', '所属期间', '期间', '月份', '抄表期', '账单期', '账期', '帐期'],
  account: ['户号', '用户号', '用户编号', '户名', '用户名称', '租户'],
  meter: ['表号', '表编号', '表具编号', '水表号', '电表号'],
  meterType: ['表类型', '计费类型', '表计类型', '介质类型', '类型', '介质'],
  histAvg: ['历史平均用量', '历史均值', '往期均值', '平均用量', '上月用量', '去年同期用量'],
  prev: ['上期读数', '上期示数', '上期抄见', '期初读数', '上月读数', '上期底度'],
  curr: ['本期读数', '本期示数', '本期抄见', '期末读数', '本月读数', '本期底度'],
  usage: ['用量', '用水量', '用电量', '消耗量', '抄见用量'],
  price: ['单价', '水价', '电价', '计费单价', '综合单价'],
  baseFee: ['基本费', '基本电费', '基本水费', '固定费用', '容量费'],
  due: ['应收金额', '应收电费', '应收水费', '应缴金额', '应收'],
  bill: ['账单金额', '账单应收', '发票金额', '实收金额', '账单'],
  swapBase: ['换表底度', '结转底度', '新表底度', '换表起度', '底度'],
  swap: ['是否换表', '换表标记', '换表情况', '换表说明', '换表'],
};

const LABELS = {
  period: '期间', account: '户号', meter: '表号', meterType: '表类型',
  histAvg: '历史平均用量', prev: '上期读数', curr: '本期读数', usage: '用量',
  price: '单价', baseFee: '基本费', due: '应收金额', bill: '账单金额',
  swapBase: '换表底度', swap: '是否换表',
};

/* 必需列：缺了就没法做"逐户勾稽"，直接判定材料不足（绝不套默认值） */
const REQUIRED = ['period', 'meter', 'prev', 'curr', 'usage', 'price', 'due'];
/* 可加的列：合计行逐列复核只对它们做 */
const SUM_ROLES = ['usage', 'baseFee', 'due', 'bill'];
/* 不该为负的列 */
const NEG_ROLES = ['prev', 'curr', 'due', 'bill'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|总和|全部合计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|未填)$/i.test(s);
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
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, headers: [] };
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
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns, headers };
}

function who(it) {
  const meter = it && it.meter ? String(it.meter).trim() : '';
  const period = it && it.period ? String(it.period).trim() : '';
  const head = meter ? `表号 ${meter}` : `第 ${it && it.line} 行`;
  return period ? `${head}（${period}）` : head;
}

/* ================================ 免费档检查项 ================================ */

function checkUsageRecompute(it) {
  const out = [];
  const prev = normNumber(it.prev);
  const curr = normNumber(it.curr);
  const usage = normNumber(it.usage);
  if (prev === null || curr === null || usage === null) return out;
  const expect = round2(curr - prev);
  if (Math.abs(expect - usage) <= TOL) return out;
  out.push({
    level: 'P0', category: '用量与读数不符', line: it.line,
    message: `${who(it)}：本期读数 ${curr.toFixed(2)} − 上期读数 ${prev.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里用量写的是 ${usage.toFixed(2)}，相差 ${round2(usage - expect).toFixed(2)}。`,
  });
  return out;
}

function checkAmountRecompute(it) {
  const out = [];
  const usage = normNumber(it.usage);
  const price = normNumber(it.price);
  const due = normNumber(it.due);
  if (usage === null || price === null || due === null) return out;
  const baseRaw = normNumber(it.baseFee);
  const base = baseRaw === null ? 0 : baseRaw;
  const expect = round2(usage * price + base);
  if (Math.abs(expect - due) <= TOL) return out;
  out.push({
    level: 'P0', category: '应收金额与复算不符', line: it.line,
    message: `${who(it)}：用量 ${usage.toFixed(2)} × 单价 ${price.toFixed(2)} + 基本费 ${base.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里应收金额是 ${due.toFixed(2)}，相差 ${round2(due - expect).toFixed(2)}`
      + `${baseRaw === null ? '（基本费没填，按 0 参与复算）' : ''}。`,
  });
  return out;
}

function checkTotals(totals, items, role) {
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${n} 条明细相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const meter = String(it.meter === undefined ? '' : it.meter).trim();
    const period = String(it.period === undefined ? '' : it.period).trim();
    if (!meter || !period) continue;
    const key = `${meter}|${period}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一表号同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次 —— `
          + '同一块表同一期的用量与金额会被重复计入。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一户没法勾稽。`,
        });
      }
    }
  }
  return out;
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '读数或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 抄表读数与账单金额都不该为负，`
        + '先确认是抄错表、抄错位，还是把红字冲回填进了这一列。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof payload}）—— 请用 {"text": "抄表账单表"} 的形式传进来。`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到抄表账单表正文（text）—— 请把「期间 / 表号 / 上期读数 / 本期读数 / 用量 / 单价 / 应收金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `抄表账单表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何抄表明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkUsageRecompute(it)) findings.push(f);
    for (const f of checkAmountRecompute(it)) findings.push(f);
    for (const f of checkNegatives(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotals(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const rows = t.items.length;
  const periods = new Set(t.items
    .map((it) => String(it.period === undefined ? '' : it.period).trim())
    .filter((s) => s !== '')).size;

  const result = {
    status: 'success',
    service_type: 'UTILITY_METER_READING_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows,
      periods,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows,
      periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '本版本只执行免费档检查项；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核「用量 = 本期读数 − 上期读数」「应收金额 = 用量 × 单价 + 基本费」「合计 = 各行相加」'
      + '这类内部勾稽，**不规定水价/电价标准**（以合同与供水供电公司账单为准）；'
      + '结论都带原文行号，可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
