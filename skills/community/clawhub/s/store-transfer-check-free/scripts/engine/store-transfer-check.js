/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * store-transfer-check.js —— 连锁门店调拨与库存核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**连锁零售每周（或每日）调拨对账时**，门店与仓库之间来回调货，
 * 一张调拨表上同时有 **调出量、调入量、在途量、期初/期末库存、销售数量**。
 * 这几列之间是**守恒关系**，完全能算出来对错：
 *   调出 − 调入        = 在途（差额就是还在路上的货）
 *   期初 + 调入 − 销售 − 调出 = 期末
 * 对不上就是**货丢了、记错了、或者有一行漏了** —— 账上守恒不代表货真在架上（那要靠实物盘点）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**调拨是否该批、价格是否合理（见 OUT_OF_SCOPE）；
 *    「跨店调拨量差异参考比例」是**参考口径**，只是提示，不是对错判据。
 */

const CHECKS_GIVEN = [
  '调出 − 调入 = 在途 复算',
  '期末库存 = 期初 + 调入 − 销售 − 调出 复算',
  '合计行逐列复核',
  '同一调拨单号重复行检测',
  '空白与占位符检测',
  '数量为负检测（期初 / 调出 / 调入 / 销售）',
];

const CHECKS_WITHHELD = [
  '在途为负或超过调出量检测',
  '期末库存为负检测',
  '调拨量与库存变动不一致（差超阈值）提示',
  '同一商品跨店调拨量差异超过参考比例提示',
  '调出与调入数量不等（超过容差）提示',
];

const OUT_OF_SCOPE = [
  '判断调拨该不该批、有没有超授权额度（那是审批流程的事）',
  '核对调拨单价、调拨成本与内部结算价（表里没有单价就不算）',
  '替代实物盘点：账上守恒**不代表**货真在架上',
  '读取 ERP / WMS / POS 导出的原始文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t调拨单号\t调出门店\t调入门店\t商品编码\t商品名称\t期初库存\t调出数量\t调入数量\t在途数量\t销售数量\t期末库存',
  '2026-06\tDB-20260601\t中心仓\t门店A\tSKU-1001\t矿泉水550ml\t1000\t200\t200\t0\t300\t700',
  '2026-06\tDB-20260602\t中心仓\t门店B\tSKU-1001\t矿泉水550ml\t700\t150\t150\t0\t250\t450',
  '2026-06\tDB-20260603\t区域仓\t门店C\tSKU-2002\t抽纸200抽\t600\t100\t100\t0\t120\t480',
  '合计\t\t\t\t\t\t2300\t450\t450\t0\t670\t1630',
].join('\n');

const TOL = 0.01;                 // 算术复算容差（精确勾稽）
const NEG_ROLES = ['beginStock', 'outQty', 'inQty', 'soldQty'];   // 免费档查负数的列（在途 / 期末归完整档）
const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总)$/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名排在更宽泛的前面。
  //    反例（会静默算错）：把 outQty 的别名放宽成「调出」并排在 fromStore 前面，
  //    「调出门店」这一列就会被 outQty 抢走 —— 不报缺列，只是把它当数量算。
  period: ['期间', '所属期', '月份', '日期'],
  docNo: ['调拨单号', '调拨单编号', '单据号', '单号'],
  fromStore: ['调出门店', '调出方门店', '调出仓', '调出方'],
  toStore: ['调入门店', '调入方门店', '调入仓', '调入方'],
  sku: ['商品编码', '商品代码', '物料编码', '货号', 'SKU'],
  skuName: ['商品名称', '商品品名', '品名'],
  beginStock: ['期初库存', '期初结存', '期初数量', '期初'],
  endStock: ['期末库存', '期末结存', '期末数量', '期末'],
  outQty: ['调出数量', '调出量', '调出'],
  inQty: ['调入数量', '调入量', '调入'],
  inTransit: ['在途数量', '在途量', '在途'],
  soldQty: ['销售数量', '销售出库', '销售'],
};

const LABELS = {
  period: '期间', docNo: '调拨单号', fromStore: '调出门店', toStore: '调入门店',
  sku: '商品编码', skuName: '商品名称', beginStock: '期初库存', endStock: '期末库存',
  outQty: '调出数量', inQty: '调入数量', inTransit: '在途数量', soldQty: '销售数量',
};

const REQUIRED = ['docNo', 'sku', 'beginStock', 'outQty', 'inQty', 'inTransit', 'soldQty', 'endStock'];
const SUM_ROLES = ['beginStock', 'outQty', 'inQty', 'inTransit', 'soldQty', 'endStock'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这些补上再跑；材料不足时本工具不做任何认定，也不套用默认值（不会输出「未发现问题」）。',
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
  const s = String(raw).trim()
    .replace(/[,，\s¥￥$]/g, '')
    .replace(/(件|箱|个|瓶|包|提|套|条|支)$/, '');
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
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    const head = String(cells[0] === undefined ? '' : cells[0]).trim();
    const periodCell = row.period === undefined ? '' : String(row.period).trim();
    const isTotal = TOTAL_WORDS.test(head) || TOTAL_WORDS.test(periodCell);
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const d = it && it.docNo !== undefined ? String(it.docNo).trim() : '';
  return d ? `第 ${it.line} 行（单号 ${d}）` : `第 ${it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

/** 调出 − 调入 = 在途 */
function checkTransitIdentity(it) {
  const out = normNumber(it.outQty);
  const inn = normNumber(it.inQty);
  const tr = normNumber(it.inTransit);
  if (out === null || inn === null || tr === null) return null;
  const expect = round2(out - inn);
  if (Math.abs(expect - tr) <= TOL) return null;
  return {
    level: 'P0', category: '调出调入与在途不符', line: it.line,
    message: `${who(it)}：调出 ${out.toFixed(2)} − 调入 ${inn.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里在途是 ${tr.toFixed(2)}，相差 ${round2(tr - expect).toFixed(2)} —— 差额就是还在路上的货，这一格必须对得上。`,
  };
}

/** 期末库存 = 期初 + 调入 − 销售 − 调出 */
function checkStockIdentity(it) {
  const begin = normNumber(it.beginStock);
  const inn = normNumber(it.inQty);
  const sold = normNumber(it.soldQty);
  const out = normNumber(it.outQty);
  const end = normNumber(it.endStock);
  if (begin === null || inn === null || sold === null || out === null || end === null) return null;
  const expect = round2(begin + inn - sold - out);
  if (Math.abs(expect - end) <= TOL) return null;
  return {
    level: 'P0', category: '期末库存勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${begin.toFixed(2)} + 调入 ${inn.toFixed(2)} − 销售 ${sold.toFixed(2)} `
      + `− 调出 ${out.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末是 ${end.toFixed(2)}，`
      + `相差 ${round2(end - expect).toFixed(2)} —— 要么漏了一笔出入库，要么有一列记错了。`,
  };
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 合计行必须逐列等于明细之和。`,
  });
  return out;
}

/** 同一调拨单号出现多行 */
function checkDuplicateDocs(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.docNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一调拨单号出现多行', line: it.line,
        message: `${who(it)}：调拨单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 `
          + '—— 同一张单被记了两次，调拨量会被重复统计。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 关键列为空或占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一列参与守恒复算，缺了就核不了。`,
        });
      }
    }
  }
  return out;
}

/** 数量为负（期初 / 调出 / 调入 / 销售；在途与期末由完整档单独查） */
function checkNegativeQty(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '数量为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 调拨表里数量不可能是负的，`
          + '负数一般是冲回或反向单，请单独列示。',
      });
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 在途为负，或超过调出量 */
/** 期末库存为负 */
/** 期间守恒：同一门店 + 同一商品，首行期初 + 合计调入 − 合计销售 − 合计调出 = 最后一行期末 */
/** 同一商品在不同调出门店之间的调拨量差异（参考比例，仅提示） */
/** 调出与调入数量不等（差额应当就是这批货的在途量） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到调拨表正文（text）—— 请把「期间 / 调拨单号 / 门店 / 商品 / 期初 / 调出 / 调入 / 在途 / 销售 / 期末」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `调拨表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何调拨明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkTransitIdentity(it); if (a) findings.push(a);
    const b = checkStockIdentity(it); if (b) findings.push(b);
    for (const x of checkNegativeQty(it)) findings.push(x);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicateDocs(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);


  const executed = CHECKS_GIVEN.slice();
  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periods = new Set();
  for (const it of t.items) {
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
  }
  const periodCount = periods.size;

  const result = {
    status: 'success',
    service_type: 'STORE_TRANSFER_CHECK',
    scope: {
      checks: executed,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodCount,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodCount,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"调出 − 调入 = 在途""期初 + 调入 − 销售 − 调出 = 期末"这两条**表内守恒**，'
      + '**不判断**调拨该不该批、价格是否合理（见 checks_out_of_scope）；'
      + '跨店调拨量差异用的是**参考比例**，只作提示。结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
