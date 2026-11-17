#!/usr/bin/env node
/**
 * rd-expense-check.js —— 研发费用加计扣除归集核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有研发投入的企业每年汇算清缴（以及季度预缴）都要归集研发费用做加计扣除**，
 * 而这套归集最容易错的两处都是**明文规则**：
 *   ① 「其他相关费用」有限额，且**必须按全部研发项目统一计算**
 *      （限额 = 前五项费用之和 × 10% ÷ (1 − 10%)）—— 逐项目各算一遍是最常见的错法；
 *   ② 委托研发按**实际发生额的 80%** 计入。
 * 归集错一点，少的是**加计扣除额（真金白银的税）**，多的是**税务风险**。
 *
 * 与已有能力的区别：`expense-compliance` 核的是**报销单合规**（发票/标准/审批）；
 * `depreciation-check` 核固定资产折旧；本能力核的是**研发费用归集与加计扣除口径**，互不重叠。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '归集合计勾稽（各项费用之和 = 归集合计）',
  '「其他相关费用」限额勾稽（按**全部项目统一计算**：前五项之和 × 10% ÷ (1 − 10%)）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复项目检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '委托研发计入额勾稽（实际发生额 × 80%）',
  '加计扣除额勾稽（允许加计扣除额 × 比例，比例由入参给出，默认 100%）',
  '各项费用为负检测',
  '单项「其他相关费用」占比超过 10% 的口径提示',
];

const OUT_OF_SCOPE = [
  '判断某项支出是否属于研发活动（那是研发项目管理与税务判定的事）',
  '判断企业适用 100% 还是 75% 加计扣除比例（请用入参 ratio 明确给出）',
  '处理不适用加计扣除的行业负面清单、以及失败的研发活动',
  '处理资本化与费用化的分摊（请分别在表里列明）',
  '给出税务意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '研发项目\t人员人工费用\t直接投入费用\t折旧费用\t无形资产摊销\t新产品设计费\t其他相关费用\t归集合计',
  '项目甲\t600000.00\t200000.00\t80000.00\t40000.00\t50000.00\t10000.00\t980000.00',
  '项目乙\t400000.00\t150000.00\t60000.00\t20000.00\t30000.00\t20000.00\t680000.00',
  '合计\t1000000.00\t350000.00\t140000.00\t60000.00\t80000.00\t30000.00\t1660000.00',
].join('\n');

const TOL = 0.01;
const OTHER_CAP_RATE = 0.10;      // 「其他相关费用」限额比例（10%）

const ROLES = {
  party: ['研发项目', '项目名称', '项目'],
  staff: ['人员人工费用', '人员人工', '人工费用'],
  material: ['直接投入费用', '直接投入'],
  depreciation: ['折旧费用', '折旧'],
  amortization: ['无形资产摊销', '摊销'],
  design: ['新产品设计费', '设计费', '新工艺规程制定费'],
  other: ['其他相关费用', '其他费用'],
  total: ['归集合计', '合计', '研发费用合计'],
  entrustPaid: ['委托研发实际发生额', '委托研发发生额'],
  entrustIn: ['委托研发计入额', '委托研发计入'],
  superDeduction: ['加计扣除额', '加计扣除'],
};

const LABELS = {
  party: '研发项目', staff: '人员人工费用', material: '直接投入费用', depreciation: '折旧费用',
  amortization: '无形资产摊销', design: '新产品设计费', other: '其他相关费用', total: '归集合计',
  entrustPaid: '委托研发实际发生额', entrustIn: '委托研发计入额', superDeduction: '加计扣除额',
};

// 「前五项」= 人员人工 / 直接投入 / 折旧 / 无形资产摊销 / 新产品设计费
const FIRST_FIVE = ['staff', 'material', 'depreciation', 'amortization', 'design'];
const REQUIRED = ['party'].concat(FIRST_FIVE, ['other', 'total']);
const SUM_ROLES = ['staff', 'material', 'depreciation', 'amortization', 'design', 'other',
  'entrustPaid', 'entrustIn', 'superDeduction', 'total'];

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
  if (h === '合计' || h === '总计') return 'total';      // 表头的"合计"列
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

function label(it) {
  return `研发项目「${it.byRole.party || '(未命名)'}」`;
}

function checkRowTotal(it, hasEntrust) {
  const stated = num(it, 'total');
  if (stated === null) return null;
  const roles = FIRST_FIVE.concat(['other']);
  if (hasEntrust) roles.push('entrustIn');
  const parts = roles.map((r) => num(it, r));
  if (parts.some((p) => p === null)) return null;
  const sum = round2(parts.reduce((s, p) => s + p, 0));
  if (Math.abs(sum - stated) <= TOL) return null;
  const formula = roles.map((r) => LABELS[r]).join(' + ');
  return {
    level: 'P0', category: '归集合计与各项之和不符', line: it.line,
    message: `${label(it)}的归集合计是 ${stated.toFixed(2)}，`
      + `${hasEntrust ? '（含委托研发计入额）' : ''}按「${formula}」相加应为 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} 元。`,
    advice: '归集合计必须等于各项之和；漏项或重复计入都会让后续限额与加计扣除额一起错。',
  };
}

/** 「其他相关费用」限额：**按全部项目统一计算**（逐项目各算一遍是最常见的错法）。 */
function checkOtherCap(items) {
  const five = round2(items.reduce((s, it) => {
    return s + FIRST_FIVE.reduce((t, r) => {
      const n = num(it, r);
      return t + (n === null ? 0 : n);
    }, 0);
  }, 0));
  const other = round2(items.reduce((s, it) => {
    const n = num(it, 'other');
    return s + (n === null ? 0 : n);
  }, 0));
  const cap = round2(five * OTHER_CAP_RATE / (1 - OTHER_CAP_RATE));
  if (other <= cap + TOL) return [];
  return [{
    level: 'P0', category: '其他相关费用超过限额', line: items[0] ? items[0].line : 1,
    message: `全部项目的「其他相关费用」合计 ${other.toFixed(2)}，`
      + `超过按全部项目统一计算的限额 ${cap.toFixed(2)}`
      + `（= 前五项合计 ${five.toFixed(2)} × 10% ÷ (1 − 10%)），超出 ${round2(other - cap).toFixed(2)} 元。`,
    advice: '限额是**按全部研发项目统一计算**的，不是逐项目各算一次；'
      + '超限部分不能加计扣除，请按项目分摊调减。',
  }];
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
        advice: '要么明细行漏了项目，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一项目出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一项目分多行归集是正常的；但若本表按项目汇总，重复行会让合计翻倍，也会把统一限额算错。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items, hasEntrust) {
  const out = [];
  const roles = REQUIRED.concat(hasEntrust ? ['entrustPaid', 'entrustIn'] : []);
  for (const it of items) {
    for (const role of roles) {
      if (it.byRole[role] === undefined) continue;
      const s = String(it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${label(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔归集就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的研发费用归集表（要能认出「研发项目」「人员人工费用」「直接投入费用」「折旧费用」'
      + '「无形资产摊销」「新产品设计费」「其他相关费用」「归集合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从研发费用辅助账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个项目的明细行']);

  const hasEntrust = t.cols.some((c) => c.role === 'entrustPaid') && t.cols.some((c) => c.role === 'entrustIn');
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkRowTotal(it, hasEntrust); if (a) findings.push(a);
  }
  for (const f of checkOtherCap(t.items)) findings.push(f);
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items, hasEntrust)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const five = round2(FIRST_FIVE.reduce((s, r) => s + sumOf(r), 0));
  const other = sumOf('other');

  const result = {
    findings,
    summary: {
      projects: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      first_five_total: five,
      other_total: other,
      other_cap: round2(five * OTHER_CAP_RATE / (1 - OTHER_CAP_RATE)),
      collection_total: sumOf('total'),
      basis: '归集合计 = 前五项 + 其他相关费用（有委托研发列时再加委托研发计入额）；'
        + '其他相关费用限额 = 前五项之和 × 10% ÷ (1 − 10%)，**按全部项目统一计算**；'
        + '委托研发按实际发生额 80% 计入；合计行逐列复核。',
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
      + '不代表这些支出都被认定为研发活动、也不代表适用比例正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, OTHER_CAP_RATE,
};
