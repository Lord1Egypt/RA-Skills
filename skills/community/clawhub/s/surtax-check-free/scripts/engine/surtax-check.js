#!/usr/bin/env node
/**
 * surtax-check.js —— 增值税附加税费核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每个一般纳税人每月都要按增值税税额再算三项附加**：
 *   ① 城建税       = 增值税税额 × 城建税率（市区 7% / 县镇 5% / 其他 1%）
 *   ② 教育费附加   = 增值税税额 × 3%
 *   ③ 地方教育附加 = 增值税税额 × 2%
 *   ④ 附加合计     = 三项之和
 * 算式极简，但**税率档次用错（7/5/1 按注册地）、留抵月份把 0 当成"没填"、
 * 三项里漏一项**，都是每月都在发生的错；而且附加税是**跟着增值税走的**，主税错它必错。
 *
 * 与已有能力的区别：`vat-burden-check` 核的是**增值税本体**（销项 − 进项 − 留抵、税负率）；
 * 本能力核的是**以增值税为计税依据的三项附加税费**，层级不同、税率表也不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查政策文库、不调用大模型；材料不足不给结论；不给税务意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '城建税勾稽（增值税税额 × 城建税率）',
  '教育费附加勾稽（增值税税额 × 教育费附加率）',
  '地方教育附加勾稽（增值税税额 × 地方教育附加率）',
  '附加合计勾稽（三项之和）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复期间检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '增值税税额为负检测（留抵月份通常无附加税基）',
  '城建税率不在 1% / 5% / 7% 之列检测',
  '教育费附加率异常检测（通常为 3%）',
  '地方教育附加率异常检测（通常为 2%）',
  '附加合计为负检测',
];

const OUT_OF_SCOPE = [
  '判断城建税适用哪一档税率（按纳税人所在地：市区 7%、县镇 5%、其他 1%）',
  '处理小规模纳税人减半征收、以及增值税减免对附加税的影响',
  '处理消费税对应的附加税费（如涉及，请把消费税并入"增值税税额"列并注明）',
  '给出税务意见或做税负测算；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t增值税税额\t城建税率\t城建税\t教育费附加率\t教育费附加\t地方教育附加率\t地方教育附加\t附加合计',
  '2026-01\t40000.00\t7%\t2800.00\t3%\t1200.00\t2%\t800.00\t4800.00',
  '2026-02\t0.00\t7%\t0.00\t3%\t0.00\t2%\t0.00\t0.00',
  '合计\t40000.00\t\t2800.00\t\t1200.00\t\t800.00\t4800.00',
].join('\n');

const TOL = 0.01;
const CITY_RATES = [1, 5, 7];
const EDU_RATE = 3;
const LOCAL_EDU_RATE = 2;

const ROLES = {
  party: ['期间', '月份', '所属期', '纳税期间'],
  vat: ['增值税税额', '增值税', '计税依据', '主税'],
  cityRate: ['城建税率', '城市维护建设税率'],
  cityTax: ['城建税', '城市维护建设税'],
  eduRate: ['教育费附加率'],
  eduTax: ['教育费附加'],
  localRate: ['地方教育附加率', '地方教育附加费率'],
  localTax: ['地方教育附加'],
  total: ['附加合计', '合计附加', '附加税费合计'],
};

const LABELS = {
  party: '期间', vat: '增值税税额', cityRate: '城建税率', cityTax: '城建税',
  eduRate: '教育费附加率', eduTax: '教育费附加', localRate: '地方教育附加率',
  localTax: '地方教育附加', total: '附加合计',
};

const REQUIRED = ['party', 'vat', 'cityRate', 'cityTax', 'eduRate', 'eduTax', 'localRate', 'localTax', 'total'];
const SUM_ROLES = ['vat', 'cityTax', 'eduTax', 'localTax', 'total'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库五次踩过的坑）：
  //    「地方教育附加率」要排在「地方教育附加」之前、「教育费附加率」要排在「教育费附加」之前；
  //    且「地方教育附加」必须排在「教育费附加」之前（否则"教育附加"会把"地方教育附加"抢走）。
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

function checkOne(it, rateRole, taxRole, name) {
  const base = num(it, 'vat');
  const rate = num(it, rateRole);
  const stated = num(it, taxRole);
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: `${name}与复算不符`, line: it.line,
    message: `${who(it)}的${name}是 ${stated.toFixed(2)}，按 增值税税额 ${base.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: `${name}以**实际缴纳的增值税税额**为计税依据；主税一变，这三项都要跟着变。`,
  };
}

function checkTotal(it) {
  const parts = ['cityTax', 'eduTax', 'localTax'].map((r) => num(it, r));
  const stated = num(it, 'total');
  if (stated === null || parts.some((p) => p === null)) return null;
  const sum = round2(parts.reduce((s, p) => s + p, 0));
  if (Math.abs(sum - stated) <= TOL) return null;
  return {
    level: 'P0', category: '附加合计与三项之和不符', line: it.line,
    message: `${who(it)}的附加合计是 ${stated.toFixed(2)}，三项相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
    advice: '漏一项（最常见是漏"地方教育附加"）或多加一项都会在这里暴露。',
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
        advice: '要么明细行漏了月份，要么合计行没跟着更新。',
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
        advice: '不同税率分行列示是正常的；但若本表按期间汇总，重复行会让税额与附加一起翻倍。',
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
          advice: '缺这一格这笔附加税就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的附加税费计算表（要能认出「增值税税额」「城建税率」「城建税」'
      + '「教育费附加率」「教育费附加」「地方教育附加率」「地方教育附加」「附加合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从申报底稿导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个期间的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkOne(it, 'cityRate', 'cityTax', '城建税'); if (a) findings.push(a);
    const b = checkOne(it, 'eduRate', 'eduTax', '教育费附加'); if (b) findings.push(b);
    const c = checkOne(it, 'localRate', 'localTax', '地方教育附加'); if (c) findings.push(c);
    const d = checkTotal(it); if (d) findings.push(d);
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
      vat_total: sumOf('vat'),
      city_tax_total: sumOf('cityTax'),
      edu_total: sumOf('eduTax'),
      local_edu_total: sumOf('localTax'),
      surtax_total: sumOf('total'),
      surtax_ratio_pct: sumOf('vat') > 0 ? round2(sumOf('total') / sumOf('vat') * 100) : null,
      basis: '城建税 = 增值税税额 × 城建税率（1/5/7%）；教育费附加 = 增值税税额 × 3%；'
        + '地方教育附加 = 增值税税额 × 2%；附加合计 = 三项之和；合计行逐列复核。',
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
      + '不代表适用档次与减免政策判断正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
