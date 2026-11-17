#!/usr/bin/env node
/**
 * vat-burden-check.js —— 增值税进销项与税负率核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每个一般纳税人每月申报前都要算一遍增值税**，而这一步是三条串行算式：
 *   ① 销项税额 = 销售额 × 销项税率
 *   ② 应纳增值税 = 销项税额 − 进项税额 − 上期留抵（**负数则为 0**）
 *   ③ 期末留抵 = 进项税额 + 上期留抵 − 销项税额（**负数则为 0**）
 * 留抵结转错一次，后面每个月都跟着错；税负率异常还是税务预警的常见指标。
 * 财务经理核的就是这三条 —— 纯算术，但月份一多、税率多档时人眼极易错。
 *
 * 与已有能力的区别：`invoice-consistency-check` 核的是**单张发票内部/之间的一致性**（金额、税号、抬头）；
 * 本能力核的是**申报口径的进销项汇总与税负率**（销项 − 进项 − 留抵），层面不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查税率文库、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '应纳增值税勾稽（销项税额 − 进项税额 − 上期留抵，负数按 0）',
  '期末留抵税额勾稽（进项税额 + 上期留抵 − 销项税额，负数按 0）',
  '税负率勾稽（应纳增值税 ÷ 销售额）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复期间检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '销项税额勾稽（销售额 × 销项税率）',
  '税负率超出 0~20% 合理区间检测',
  '销售额非正检测',
  '期末留抵税额为负检测',
  '应纳增值税为负检测',
];

const OUT_OF_SCOPE = [
  '判断进项税额能否抵扣（那是发票合规与用途判定的事）',
  '处理免税、即征即退、简易计税与差额征税等特殊口径',
  '处理多档税率在同一期间的分摊（请把不同税率分行列示）',
  '给出税务意见或做税负筹划；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t销售额\t销项税率\t销项税额\t进项税额\t上期留抵税额\t应纳增值税\t期末留抵税额\t税负率',
  '2026-01\t1000000.00\t13%\t130000.00\t90000.00\t0.00\t40000.00\t0.00\t4.00%',
  '2026-02\t800000.00\t13%\t104000.00\t150000.00\t0.00\t0.00\t46000.00\t0.00%',
  '2026-03\t1200000.00\t13%\t156000.00\t100000.00\t46000.00\t10000.00\t0.00\t0.83%',
  '合计\t3000000.00\t\t390000.00\t340000.00\t46000.00\t50000.00\t46000.00\t',
].join('\n');

const TOL = 0.01;
const PCT_TOL = 0.02;   // 税负率保留两位小数，容差 0.02 个百分点

const ROLES = {
  party: ['期间', '月份', '所属期', '纳税期间'],
  sales: ['销售额', '不含税销售额', '计税销售额'],
  rate: ['销项税率', '税率'],
  output: ['销项税额', '销项'],
  input: ['进项税额', '进项'],
  credit: ['上期留抵税额', '上期留抵', '期初留抵'],
  payable: ['应纳增值税', '应纳税额', '应纳税额'],
  creditEnd: ['期末留抵税额', '期末留抵'],
  burden: ['税负率', '税负'],
};

const LABELS = {
  party: '期间', sales: '销售额', rate: '销项税率', output: '销项税额', input: '进项税额',
  credit: '上期留抵税额', payable: '应纳增值税', creditEnd: '期末留抵税额', burden: '税负率',
};

const REQUIRED = ['party', 'sales', 'output', 'input', 'credit', 'payable', 'creditEnd', 'burden'];
const SUM_ROLES = ['sales', 'output', 'input', 'credit', 'payable', 'creditEnd'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（这是本仓库踩过两次的坑，见 tools/header_map_check.py）：
  //    「期末留抵税额」必须排在「上期留抵税额」的宽泛别名之前；「应纳增值税」不能被「销项税额」抢走。
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
const who = (it) => `期间「${it.byRole.party || '(未命名)'}」`;

function checkPayable(it) {
  const output = num(it, 'output');
  const input = num(it, 'input');
  const credit = num(it, 'credit');
  const stated = num(it, 'payable');
  if (output === null || input === null || credit === null || stated === null) return null;
  const raw = round2(output - input - credit);
  const expect = Math.max(0, raw);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应纳增值税与复算不符', line: it.line,
    message: `${who(it)}的应纳增值税是 ${stated.toFixed(2)}，`
      + `按 销项税额 ${output.toFixed(2)} − 进项税额 ${input.toFixed(2)} − 上期留抵 ${credit.toFixed(2)} = ${raw.toFixed(2)}`
      + `${raw < 0 ? '（负值按 0 计）' : ''}，应为 ${expect.toFixed(2)}。`,
    advice: '留抵不能直接抵成"负数应纳税额"：为负时应为 0，并转入期末留抵。',
  };
}

function checkCreditEnd(it) {
  const output = num(it, 'output');
  const input = num(it, 'input');
  const credit = num(it, 'credit');
  const stated = num(it, 'creditEnd');
  if (output === null || input === null || credit === null || stated === null) return null;
  const raw = round2(input + credit - output);
  const expect = Math.max(0, raw);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '期末留抵税额与复算不符', line: it.line,
    message: `${who(it)}的期末留抵税额是 ${stated.toFixed(2)}，`
      + `按 进项税额 ${input.toFixed(2)} + 上期留抵 ${credit.toFixed(2)} − 销项税额 ${output.toFixed(2)} = ${raw.toFixed(2)}`
      + `${raw < 0 ? '（负值按 0 计）' : ''}，应为 ${expect.toFixed(2)}。`,
    advice: '期末留抵要原样滚到下期的"上期留抵"；这里错了下个月会跟着错。',
  };
}

function checkBurden(it) {
  const sales = num(it, 'sales');
  const payable = num(it, 'payable');
  const stated = num(it, 'burden');
  if (sales === null || payable === null || stated === null) return null;
  if (Math.abs(sales) <= 1e-9) return null;
  const expect = round2(payable / sales * 100);
  if (Math.abs(expect - stated) <= PCT_TOL) return null;
  return {
    level: 'P1', category: '税负率与复算不符', line: it.line,
    message: `${who(it)}的税负率是 ${stated}%，按 应纳增值税 ${payable.toFixed(2)} ÷ 销售额 ${sales.toFixed(2)} 应为 ${expect}%。`,
    advice: '税负率是税务预警的常用指标；口径要与申报表一致（不含税销售额）。',
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
        advice: '要么明细行漏了期间，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一期间出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '多档税率分行列示是正常的；但若本表按期间汇总，重复行会让进销项一起翻倍。',
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
          advice: '缺这一格这笔税额就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的增值税进销项汇总表（要能认出「销售额」「销项税额」「进项税额」'
      + '「上期留抵税额」「应纳增值税」「期末留抵税额」「税负率」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从申报底稿导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个期间的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkPayable(it); if (a) findings.push(a);
    const b = checkCreditEnd(it); if (b) findings.push(b);
    const c = checkBurden(it); if (c) findings.push(c);
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
      periods: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      sales_total: sumOf('sales'),
      output_total: sumOf('output'),
      input_total: sumOf('input'),
      payable_total: sumOf('payable'),
      burden_pct: sumOf('sales') > 0 ? round2(sumOf('payable') / sumOf('sales') * 100) : null,
      basis: '销项税额 = 销售额 × 销项税率；应纳增值税 = 销项税额 − 进项税额 − 上期留抵（负则按 0）；'
        + '期末留抵 = 进项税额 + 上期留抵 − 销项税额（负则按 0）；税负率 = 应纳增值税 ÷ 销售额；合计行逐列复核。',
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
      + '不代表进项都能抵扣、也不代表适用简易计税等特殊口径 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
