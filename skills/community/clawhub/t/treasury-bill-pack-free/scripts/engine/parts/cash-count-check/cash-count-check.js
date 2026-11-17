#!/usr/bin/env node
/**
 * cash-count-check.js —— 现金盘点差异（长短款）核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有收银的企业每天（甚至每班）都要盘点现金**：
 *   ① 应有现金 = 期初备用金 + 销售现金收入 − 现金支出
 *   ② 差异     = 实盘现金 − 应有现金（**正=长款、负=短款**）
 *   ③ 差异类型要与差异符号一致
 * 长短款几十块看着小，但**它是收银舞弊与流程漏洞的最早信号**；而连锁门店几十上百个班次，
 * 人眼核不动；这些全是**纯算术**。
 *
 * 与已有能力的区别：`bank-reconciliation` 核**银行流水与账面**、`invoice-consistency` 核**发票**；
 * 本能力核的是**门店/收银台的现金盘点**（备用金 + 现金销售 − 支出 vs 实盘），场景与口径都不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判现金真伪、不调用大模型；材料不足不给结论；不给审计意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应有现金勾稽（期初备用金 + 销售现金收入 − 现金支出）',
  '差异勾稽（实盘现金 − 应有现金）',
  '差异类型与差异符号一致性（正=长款 / 负=短款 / 0=平）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复门店/班次检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '差异绝对值超出阈值检测（阈值由入参 tolerance 给出，默认 100 元）',
  '实盘现金或销售现金收入为负检测',
  '期初备用金为负检测',
  '差异类型取值合法性检测（只允许 长款 / 短款 / 平）',
  '销售现金收入为 0 却出现差异检测',
];

const OUT_OF_SCOPE = [
  '判断长短款的原因（那是门店管理与监控的事）',
  '处理移动支付、刷卡与代金券（本表只核现金部分）',
  '处理跨班次交接的现金移交与途中押运',
  '判断是否构成舞弊；给出审计或法律意见',
  '读取 .xlsx 或收银系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '门店班次\t期初备用金\t销售现金收入\t现金支出\t应有现金\t实盘现金\t差异\t差异类型',
  'A店-早班\t500.00\t8000.00\t200.00\t8300.00\t8300.00\t0.00\t平',
  'A店-晚班\t500.00\t9500.00\t100.00\t9900.00\t9880.00\t-20.00\t短款',
  '合计\t1000.00\t17500.00\t300.00\t18200.00\t18180.00\t-20.00\t',
].join('\n');

const TOL = 0.01;
const DIFF_TOL = 100;          // 差异阈值默认值（元）

const ROLES = {
  party: ['门店班次', '门店', '班次', '收银台'],
  opening: ['期初备用金', '备用金', '期初现金'],
  sales: ['销售现金收入', '现金收入', '现金销售'],
  payout: ['现金支出', '支出', '现金付出'],
  should: ['应有现金', '应有金额', '账面现金'],
  actual: ['实盘现金', '实盘', '实点现金'],
  // ⚠️ 「差异类型」必须排在「差异」之前：否则 `差异` 会把类型列整列抢走，
  //    导致必需列 diffType 永远认不出来（发版前守卫第四次拦下这类错）。
  diffType: ['差异类型', '长短款类型', '类型'],
  diff: ['差异', '长短款', '差额'],
};

const LABELS = {
  party: '门店班次', opening: '期初备用金', sales: '销售现金收入', payout: '现金支出',
  should: '应有现金', actual: '实盘现金', diff: '差异', diffType: '差异类型',
};

const REQUIRED = ['party', 'opening', 'sales', 'payout', 'should', 'actual', 'diff', 'diffType'];
const SUM_ROLES = ['opening', 'sales', 'payout', 'should', 'actual', 'diff'];

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
  // ⚠️ 顺序即优先级（更具体在前）：「差异类型」要排在「差异」之前（否则类型列被当金额解析）；
  //    「销售现金收入」要排在「现金支出」等宽泛词之前；「应有现金/实盘现金」互不包含。
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
const who = (it) => `「${it.byRole.party || '(未命名)'}」`;

function checkShould(it) {
  const opening = num(it, 'opening'); const sales = num(it, 'sales'); const payout = num(it, 'payout');
  const stated = num(it, 'should');
  if (opening === null || sales === null || payout === null || stated === null) return null;
  const expect = round2(opening + sales - payout);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应有现金与复算不符', line: it.line,
    message: `${who(it)}的应有现金是 ${stated.toFixed(2)}，`
      + `按 期初备用金 ${opening.toFixed(2)} + 销售现金收入 ${sales.toFixed(2)} − 现金支出 ${payout.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '应有现金 = 备用金 + 现金销售 − 现金支出；**现金支出最容易漏记**（临时采购、退款、押金）。',
  };
}

function checkDiff(it) {
  const actual = num(it, 'actual'); const should = num(it, 'should'); const stated = num(it, 'diff');
  if (actual === null || should === null || stated === null) return null;
  const expect = round2(actual - should);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差异与复算不符', line: it.line,
    message: `${who(it)}的差异是 ${stated.toFixed(2)}，按 实盘现金 ${actual.toFixed(2)} − 应有现金 ${should.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差异 = 实盘 − 应有；**正=长款、负=短款**，符号反了会把长短款说反。',
  };
}

function expectedType(diff) {
  if (Math.abs(diff) <= TOL) return '平';
  return diff > 0 ? '长款' : '短款';
}

function checkDiffType(it) {
  const diff = num(it, 'diff');
  const stated = String(it.byRole.diffType || '').trim();
  if (diff === null || !stated) return null;
  const expect = expectedType(diff);
  if (stated === expect) return null;
  return {
    level: 'P0', category: '差异类型与差异符号不一致', line: it.line,
    message: `${who(it)}的差异是 ${diff.toFixed(2)}（应为「${expect}」），但差异类型填的是「${stated}」。`,
    advice: '差异类型必须由差异符号推出：正=长款、负=短款、0=平；类型写反会误导后续追查方向。',
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
        advice: '注意：**差异类型是文字，不参与求和**（合计行里应为空）。',
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
        level: 'P1', category: '同一门店班次出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一班次重复行会让备用金与销售一起翻倍；若是交接补录，请加"时段"区分。',
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
          advice: '缺这一格这个班次就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的现金盘点表（要能认出「期初备用金」「销售现金收入」「现金支出」「应有现金」'
      + '「实盘现金」「差异」「差异类型」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从收银/门店系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个班次的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkShould(it); if (a) findings.push(a);
    const b = checkDiff(it); if (b) findings.push(b);
    const c = checkDiffType(it); if (c) findings.push(c);
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
  const diffs = t.items.map((it) => num(it, 'diff')).filter((v) => v !== null);

  const result = {
    findings,
    summary: {
      shifts: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      sales_cash_total: sumOf('sales'),
      should_total: sumOf('should'),
      actual_total: sumOf('actual'),
      diff_total: sumOf('diff'),
      short_shifts: diffs.filter((v) => v < -TOL).length,
      over_shifts: diffs.filter((v) => v > TOL).length,
      basis: '应有现金 = 期初备用金 + 销售现金收入 − 现金支出；差异 = 实盘现金 − 应有现金；'
        + '差异类型由差异符号推出（正=长款 / 负=短款 / 0=平）；合计行逐列复核。',
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
      + '不代表现金真实、也不代表没有未记录的收支 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, expectedType, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, DIFF_TOL,
};
