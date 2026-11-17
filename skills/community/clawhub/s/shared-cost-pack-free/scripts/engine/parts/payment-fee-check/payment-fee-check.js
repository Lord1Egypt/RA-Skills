#!/usr/bin/env node
/**
 * payment-fee-check.js —— 收款手续费核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**只要收钱就有手续费**（微信/支付宝/银联/信用卡/PayPal…），
 * 而每个渠道的费率、固定费、以及"账单上的手续费"和"自己算出来的手续费"经常对不上：
 *   ① 应收手续费 = 交易金额 × 费率 + 固定费
 *   ② 差异       = 账单手续费 − 应收手续费（这几块钱的差额，一个月累积下来是真金白银）
 *   ③ 结算金额   = 交易金额 − 账单手续费
 * 财务每月对账时要么逐笔核（几十上百行核不动），要么干脆不看（那就一直在漏）。
 *
 * 与已有能力的区别：`bank-reconciliation` 核的是**银行流水与账面**的逐笔配对（未达账项）；
 * 本能力核的是**渠道手续费本身算得对不对**（费率 × 金额 + 固定费 vs 账单），口径完全不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用渠道接口、不调用大模型；材料不足不给结论。
 */
'use strict';

const CHECKS_GIVEN = [
  '应收手续费勾稽（交易金额 × 费率 + 固定费）',
  '差异勾稽（账单手续费 − 应收手续费）',
  '结算金额勾稽（交易金额 − 账单手续费）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复渠道检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '费率超出 0~5% 合理区间检测',
  '固定费为负检测',
  '结算金额为负或超过交易金额检测',
  '差异超过给定阈值检测（阈值由入参 tolerance 给出，默认 0.01 元）',
];

const OUT_OF_SCOPE = [
  '判断渠道费率是否符合合同约定（那是商务条款的事）',
  '处理阶梯费率、月度封顶、退款冲正与跨境汇兑',
  '处理渠道补贴、返佣与营销活动抵扣',
  '判断手续费能否税前扣除；给出税务意见',
  '读取 .xlsx 或渠道账单文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '渠道\t交易金额\t费率\t固定费\t应收手续费\t账单手续费\t结算金额\t差异',
  '微信支付\t1000000.00\t0.6%\t0.00\t6000.00\t6000.00\t994000.00\t0.00',
  '支付宝\t500000.00\t0.55%\t0.00\t2750.00\t2750.00\t497250.00\t0.00',
  '银联POS\t200000.00\t0.5%\t0.20\t1000.20\t1000.20\t198999.80\t0.00',
  '合计\t1700000.00\t\t\t9750.20\t9750.20\t1690249.80\t0.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['渠道', '收款渠道', '支付方式', '通道'],
  // ⚠️ 别名里**不能放裸「金额」**：它会把「结算金额」抢走（第三次踩这类坑）。
  amount: ['交易金额', '交易额', '收款金额'],
  rate: ['费率', '手续费率'],
  fixed: ['固定费', '每笔固定', '单笔费用'],
  feeDue: ['应收手续费', '应计手续费', '计算手续费'],
  feeBill: ['账单手续费', '实收手续费', '渠道手续费'],
  settle: ['结算金额', '到账金额', '净额'],
  diff: ['差异', '差额'],
};

const LABELS = {
  party: '渠道', amount: '交易金额', rate: '费率', fixed: '固定费',
  feeDue: '应收手续费', feeBill: '账单手续费', settle: '结算金额', diff: '差异',
};

const REQUIRED = ['party', 'amount', 'rate', 'fixed', 'feeDue', 'feeBill', 'settle', 'diff'];
const SUM_ROLES = ['amount', 'fixed', 'feeDue', 'feeBill', 'settle', 'diff'];

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
  // 「应收手续费」必须排在「账单手续费」的宽泛别名之前；「费率」不能被「手续费」类关键词抢走。
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
const who = (it) => `渠道「${it.byRole.party || '(未命名)'}」`;

function checkFeeDue(it) {
  const amount = num(it, 'amount');
  const rate = num(it, 'rate');
  const fixed = num(it, 'fixed');
  const stated = num(it, 'feeDue');
  if (amount === null || rate === null || fixed === null || stated === null) return null;
  const expect = round2(amount * rate / 100 + fixed);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应收手续费与复算不符', line: it.line,
    message: `${who(it)}的应收手续费是 ${stated.toFixed(2)}，`
      + `按 交易金额 ${amount.toFixed(2)} × ${rate}% + 固定费 ${fixed.toFixed(2)} 复算应为 ${expect.toFixed(2)}。`,
    advice: '费率或固定费录错是最常见原因；也可能是把渠道费率记成了"年化"或其他口径。',
  };
}

function checkDiff(it) {
  const bill = num(it, 'feeBill');
  const due = num(it, 'feeDue');
  const stated = num(it, 'diff');
  if (bill === null || due === null || stated === null) return null;
  const expect = round2(bill - due);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差异与复算不符', line: it.line,
    message: `${who(it)}的差异是 ${stated.toFixed(2)}，按 账单手续费 ${bill.toFixed(2)} − 应收手续费 ${due.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差异 = 账单 − 应收；符号写反会让"多收"和"少收"完全颠倒。',
  };
}

function checkSettle(it) {
  const amount = num(it, 'amount');
  const bill = num(it, 'feeBill');
  const stated = num(it, 'settle');
  if (amount === null || bill === null || stated === null) return null;
  const expect = round2(amount - bill);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结算金额与复算不符', line: it.line,
    message: `${who(it)}的结算金额是 ${stated.toFixed(2)}，`
      + `按 交易金额 ${amount.toFixed(2)} − 账单手续费 ${bill.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '结算金额要用**账单上的**手续费扣；若还扣了保证金、退款，应在本表显式列示。',
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
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了渠道，要么合计行没跟着更新。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一渠道出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一渠道按日/按期分行是正常的；但若本表按渠道汇总，重复行会让金额与手续费一起翻倍。',
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
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔手续费就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
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
      '含表头的收款手续费核对表（要能认出「交易金额」「费率」「固定费」「应收手续费」'
      + '「账单手续费」「结算金额」「差异」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从渠道账单导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个渠道的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkFeeDue(it); if (a) findings.push(a);
    const b = checkDiff(it); if (b) findings.push(b);
    const c = checkSettle(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      channels: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      amount_total: sumOf('amount'),
      fee_due_total: sumOf('feeDue'),
      fee_bill_total: sumOf('feeBill'),
      settle_total: sumOf('settle'),
      diff_total: sumOf('diff'),
      basis: '应收手续费 = 交易金额 × 费率 + 固定费；差异 = 账单手续费 − 应收手续费；'
        + '结算金额 = 交易金额 − 账单手续费；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表渠道费率符合合同、也不代表没有其他未列示的扣款 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
