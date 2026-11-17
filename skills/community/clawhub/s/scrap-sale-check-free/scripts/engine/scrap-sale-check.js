#!/usr/bin/env node
/**
 * scrap-sale-check.js —— 废料边角料销售与回收结算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**制造业 / 建筑业每月结账、每年审计都必须核一遍废料台账**。
 * 废料收入是"账外资金"的高发区，而回收商结算是半个黑箱：过磅数对不上、扣杂率被抬高、
 * 单价低于合同价、收入不入账 —— 这几件事**都能用台账与结算单上的数字算出来对错**：
 *
 *   结算数量 = 过磅净重 − 扣杂量 − 水分扣量
 *   结算金额 = 结算数量 × 结算单价
 *   台账废料收入 = 结算金额
 *   上期结存 + 本期产出 − 本期出库 = 期末结存
 *
 * 免费档只做**逐行复算 + 合计逐列勾稽 + 重复过磅单号 / 空缺 / 负值**（见 CHECKS_GIVEN）；
 * 完整档（付费）在此之上多出**一种能力：少收与异常判定 + 追收处理清单**（见 CHECKS_WITHHELD）——
 * 单价低于合同价、扣杂或水分超约定上限、过磅数大于台账可解释量、出库无对应结算单、
 * 结算金额与实收金额不符，并按差额金额排序给出带行号与建议动作的清单。
 *
 * 与已有能力的区别：`production-yield-scrap-check` 核的是**车间投入产出与报废率**（料去哪了）；
 * `inventory-scrap-approval-check` 核的是**报废审批权限与流程**；本能力核的是
 * **废料卖出以后与回收商的结算**（货过磅了、价与量对不对、钱收够了没有）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查合同与法规文库、不调用大模型；材料不足不给结论；不给法律或审计意见。
 *
 * 说明：完整档的付费实现集中在一个开关块里，免费包由 tools/strip_free_engine.py 摘掉，
 *       所以**不要把开关字面量写进注释**（守卫会把注释也算成残留）。
 */
'use strict';

const CHECKS_GIVEN = [
  '结算数量勾稽复算（结算数量 = 过磅净重 − 扣杂量 − 水分扣量）',
  '结算金额勾稽复算（结算金额 = 结算数量 × 结算单价）',
  '废料收入与台账勾稽（逐行：结算金额 = 台账废料收入）',
  '结存数量勾稽复算（上期结存 + 本期产出 − 本期出库 = 期末结存）',
  '合计行逐列复核（数量列与金额列的合计是否等于各行之和）',
  '重复过磅单号检测',
  '关键字段空缺与占位符检测',
  '数量与金额为负检测',
];

const CHECKS_WITHHELD = [
  '结算单价低于合同/协议价检测（并按结算数量算出差额）',
  '扣杂量超出约定上限检测（按多扣量折价）',
  '水分扣量超出约定上限检测（按多扣量折价）',
  '过磅净重大于台账可解释量检测（上期结存 + 本期产出）',
  '出库无对应结算单检测（可能未入账）',
  '结算金额与实收金额不符检测（应收未收）',
  '少收与异常按差额金额排序的追收处理清单',
];

const OUT_OF_SCOPE = [
  '判断合同/协议价本身是否合理，也不核合同原件（本工具只按你台账里的合同价列比对）',
  '判断扣杂率与水分率的行业合理水平（各料别差异大，请按合同约定与历史水平核）',
  '核对磅秤是否按期检定、磅单签字与照片等凭据',
  '处理含税/不含税的换算与废料收入的增值税申报（请把口径统一成一种再贴进来）',
  '读取 .xlsx / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t废料类别\t回收商\t过磅单号\t结算单号\t上期结存数量\t本期产出数量\t本期出库数量\t期末结存数量\t过磅净重\t扣杂量\t水分扣量\t结算数量\t结算单价\t结算金额\t合同单价\t扣杂上限\t水分上限\t台账废料收入\t实收金额',
  '2026-06\t废钢\t华鑫再生资源\tWB-2606-001\tJS-2606-001\t5000.00\t42000.00\t41000.00\t6000.00\t41000.00\t410.00\t205.00\t40385.00\t2.35\t94904.75\t2.30\t3%\t2%\t94904.75\t94904.75',
  '2026-06\t铜屑\t江南金属回收\tWB-2606-002\tJS-2606-002\t800.00\t6000.00\t6300.00\t500.00\t6300.00\t126.00\t94.50\t6079.50\t42.80\t260202.60\t42.00\t2%\t1.5%\t260202.60\t260202.60',
  '2026-06\t铝边角料\t华鑫再生资源\tWB-2606-003\tJS-2606-003\t1200.00\t9800.00\t10000.00\t1000.00\t10000.00\t200.00\t100.00\t9700.00\t15.60\t151320.00\t15.00\t4%\t2.5%\t151320.00\t151320.00',
  '合计\t\t\t\t\t7000.00\t57800.00\t57300.00\t7500.00\t57300.00\t736.00\t399.50\t56164.50\t\t506427.35\t\t\t\t506427.35\t506427.35',
].join('\n');

const TOL = 0.01;   // 金额与数量都保留两位小数，容差 0.01

// ⚠️ 表头角色映射：**更具体的词必须排在更宽泛的前面**（这是本仓库踩过两次的坑，
//    见 tools/header_map_check.py）。这里的三处顺序是刻意的：
//      · 结存单号 settleDoc 在 settledQty 前（"结算单号"不能被"结算数量"的别名抢走，反之亦然）；
//      · 合同单价 contractPrice 在 结算单价 price 前（否则"合同单价"会被"单价"抢走）；
//      · 实收金额 received 在 结算金额 amount 前（否则"实收金额"会被"金额"抢走）；
//      · 扣杂上限 / 水分上限 在 扣杂量 / 水分扣量 前（否则"扣杂上限"会被"扣杂"抢走）。
const ROLES = {
  period: ['期间', '月份', '所属期', '账期'],
  category: ['废料类别', '废料名称', '料别', '类别', '品名'],
  buyer: ['回收商', '收购方', '回收单位', '客户'],
  docId: ['过磅单号', '磅单号', '过磅单'],
  settleDoc: ['结算单号', '结算单编号', '结算单据号', '结算凭证号'],
  open: ['上期结存数量', '上期结存', '期初结存'],
  produced: ['本期产出数量', '本期产出', '产出数量'],
  outbound: ['本期出库数量', '本期出库', '出库数量'],
  close: ['期末结存数量', '期末结存'],
  netWeight: ['过磅净重', '磅单净重', '净重'],
  impurityCap: ['扣杂上限', '扣杂率上限', '约定扣杂'],
  impurity: ['扣杂量', '扣杂重量', '扣杂'],
  moistureCap: ['水分上限', '水分率上限', '约定水分'],
  moisture: ['水分扣量', '水分重量', '水分'],
  settledQty: ['结算数量', '结算重量', '结算量'],
  contractPrice: ['合同单价', '协议单价', '合同价', '协议价'],
  price: ['结算单价', '单价'],
  received: ['实收金额', '已收金额', '实收'],
  amount: ['结算金额', '结算额', '金额'],
  ledgerRev: ['台账废料收入', '废料收入', '台账收入'],
};

const LABELS = {
  period: '期间', category: '废料类别', buyer: '回收商', docId: '过磅单号', settleDoc: '结算单号',
  open: '上期结存数量', produced: '本期产出数量', outbound: '本期出库数量', close: '期末结存数量',
  netWeight: '过磅净重', impurity: '扣杂量', moisture: '水分扣量', settledQty: '结算数量',
  contractPrice: '合同单价', price: '结算单价', received: '实收金额', amount: '结算金额',
  impurityCap: '扣杂上限', moistureCap: '水分上限', ledgerRev: '台账废料收入',
};

// 缺了这些列就算不出结算，直接不给结论（材料不足绝不给结论）
const REQUIRED = ['period', 'category', 'buyer', 'docId', 'settleDoc', 'open', 'produced', 'outbound',
  'close', 'netWeight', 'impurity', 'moisture', 'settledQty', 'contractPrice', 'price', 'received',
  'amount', 'impurityCap', 'moistureCap', 'ledgerRev'];

// 结算单号**允许为空**（出库无结算单正是完整档要抓的异常），所以不参与"空缺"检查
const VALUE_ROLES = REQUIRED.filter((r) => r !== 'settleDoc');

const SUM_ROLES = ['open', 'produced', 'outbound', 'close', 'netWeight', 'impurity', 'moisture',
  'settledQty', 'amount', 'ledgerRev', 'received'];

const NEG_ROLES = ['open', 'produced', 'outbound', 'close', 'netWeight', 'impurity', 'moisture',
  'settledQty', 'price', 'amount', 'ledgerRev', 'received'];

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
  const s = String(raw).trim()
    .replace(/[,，\s¥￥$]/g, '')
    .replace(/(公斤|千克|kg|KG|吨|t)$/, '')
    .replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

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
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `第 ${it.line} 行（期间 ${it.byRole.period || '未填'}／类别 ${it.byRole.category || '未填'}／过磅单号 ${it.byRole.docId || '未填'}）`;

function checkSettledQty(it) {
  const net = num(it, 'netWeight');
  const impurity = num(it, 'impurity');
  const moisture = num(it, 'moisture');
  const stated = num(it, 'settledQty');
  if (net === null || impurity === null || moisture === null || stated === null) return null;
  const expect = round2(net - impurity - moisture);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结算数量与复算不符', line: it.line,
    message: `${who(it)}的结算数量是 ${stated.toFixed(2)}，按 过磅净重 ${net.toFixed(2)} − 扣杂量 ${impurity.toFixed(2)} `
      + `− 水分扣量 ${moisture.toFixed(2)}，应为 ${expect.toFixed(2)}。`,
    advice: '结算数量是"扣杂扣水之后"的净结算量：过磅净重先减扣杂、再减水分扣量，少减一边就等于少算钱。',
  };
}

function checkAmount(it) {
  const qty = num(it, 'settledQty');
  const price = num(it, 'price');
  const stated = num(it, 'amount');
  if (qty === null || price === null || stated === null) return null;
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结算金额与复算不符', line: it.line,
    message: `${who(it)}的结算金额是 ${stated.toFixed(2)}，按 结算数量 ${qty.toFixed(2)} × 结算单价 ${price} 应为 ${expect.toFixed(2)}。`,
    advice: '结算金额 = 结算数量 × 结算单价；单价含税/不含税混用、或数量用错（用了过磅净重）都会在这里暴露。',
  };
}

function checkRevenue(it) {
  const amount = num(it, 'amount');
  const ledger = num(it, 'ledgerRev');
  if (amount === null || ledger === null) return null;
  if (Math.abs(amount - ledger) <= TOL) return null;
  return {
    level: 'P0', category: '废料收入与台账不符', line: it.line,
    message: `${who(it)}的结算金额是 ${amount.toFixed(2)}，台账废料收入是 ${ledger.toFixed(2)}，相差 ${round2(amount - ledger).toFixed(2)}。`,
    advice: '台账收入必须等于结算金额：两边不等通常是一边漏记（这笔收入没入账，或台账混进了别的单）。',
  };
}

function checkBalance(it) {
  const open = num(it, 'open');
  const produced = num(it, 'produced');
  const outbound = num(it, 'outbound');
  const close = num(it, 'close');
  if (open === null || produced === null || outbound === null || close === null) return null;
  const expect = round2(open + produced - outbound);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0', category: '结存数量勾稽不符', line: it.line,
    message: `${who(it)}的期末结存数量是 ${close.toFixed(2)}，按 上期结存 ${open.toFixed(2)} + 本期产出 ${produced.toFixed(2)} `
      + `− 本期出库 ${outbound.toFixed(2)}，应为 ${expect.toFixed(2)}。`,
    advice: '上期结存 + 本期产出 − 本期出库 = 期末结存；对不上说明有产出或出库没记账，废料"凭空消失"正是审计要问的。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `第 ${t.line} 行 合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了单，要么合计行没跟着更新；合计行是给管理层与审计看的那一行。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.docId || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复过磅单号', line: it.line,
        message: `过磅单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一张磅单只应结算一次；重复行会让出库量与收入一起翻倍（也常是重复付款/重复入账的来源）。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of VALUE_ROLES) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔结算就不完整；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of NEG_ROLES) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '数量或金额为负', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}。`,
          advice: '这几列按口径都不会为负：退货/冲销请单独列行，别用负数混在台账里（会让合计与结存看不出来）。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下函数只在完整档被调用（免费包里没有这些实现，它们的结论也不在免费档输出里） ===== */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的废料/边角料台账（要能认出「过磅净重」「扣杂量」「水分扣量」「结算数量」「结算单价」'
      + '「结算金额」「合同单价」「扣杂上限」「水分上限」「实收金额」「台账废料收入」'
      + '「上期结存数量」「本期产出数量」「本期出库数量」「期末结存数量」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从废料台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行废料台账明细行（合计行不算明细）']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkSettledQty(it); if (a) findings.push(a);
    const b = checkAmount(it); if (b) findings.push(b);
    const c = checkRevenue(it); if (c) findings.push(c);
    const d = checkBalance(it); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegatives(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const amountTotal = sumOf('amount');
  const receivedTotal = sumOf('received');
  const shortfallTotal = round2(findings.reduce((s, f) => s + (typeof f.amount === 'number' ? f.amount : 0), 0));

  const result = {
    findings,
    recovery_actions: [],
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      settled_qty_total: sumOf('settledQty'),
      amount_total: amountTotal,
      ledger_revenue_total: sumOf('ledgerRev'),
      received_total: receivedTotal,
      outstanding_total: round2(Math.max(0, amountTotal - receivedTotal)),
      shortfall_total: shortfallTotal,
      basis: '结算数量 = 过磅净重 − 扣杂量 − 水分扣量；结算金额 = 结算数量 × 结算单价；'
        + '台账废料收入 = 结算金额；上期结存 + 本期产出 − 本期出库 = 期末结存；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      rows: t.items.length,
      checks: CHECKS_GIVEN,
      withheld: CHECKS_WITHHELD,
      checks_not_run: notRun,
      settled_amount_total: amountTotal,
      paid_in_total: receivedTotal,
      outstanding_total: round2(Math.max(0, amountTotal - receivedTotal)),
      shortfall_total: shortfallTotal,
    },
  };
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表废料收入已全额入账、也不代表与回收商的合同约定本身合规 —— 那些不在本工具范围内。';
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, VALUE_ROLES,
};
