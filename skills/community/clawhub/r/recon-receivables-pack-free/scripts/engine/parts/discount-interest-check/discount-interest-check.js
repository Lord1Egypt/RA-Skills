#!/usr/bin/env node
/**
 * discount-interest-check.js —— 票据贴现利息核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**手里有银行承兑/商业承兑票据的企业，贴现时都要核一遍贴现行给的数字**：
 *   ① 贴现利息 = 票面金额 × 年贴现率 ÷ **360** × 计息天数
 *   ② 实付金额 = 票面金额 − 贴现利息
 * 计息天数的口径（算头不算尾 / 算尾不算头）、除数是 360 还是 365、起止日填错一天 ——
 * 每一项都会直接变成钱，而且**贴现是一次性交割，签完就改不了**。
 *
 * 与已有能力的区别：`overdue-interest-check` 算的是**逾期利息**（谁欠我钱要计息）；
 * 本能力算的是**票据贴现**（我拿未到期票据换现金，银行向我收息），口径与方向都不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查贴现率报价、不调用大模型；材料不足不给结论；不给金融/法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '贴现利息勾稽（票面金额 × 年贴现率 ÷ 360 × 计息天数）',
  '实付金额勾稽（票面金额 − 贴现利息）',
  '计息天数与起止日勾稽（按算头不算尾复算，并给出算尾不算头的口径）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复票据号检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '年贴现率超出合理区间检测（不在 0~24%）',
  '到期日不晚于贴现日检测（日期倒挂）',
  '票面金额非正检测',
  '实付金额为负或超过票面金额检测',
  '计息天数超过 365 天检测（跨期或日期填错）',
];

const OUT_OF_SCOPE = [
  '判断贴现率报价是否合理（那是市场与银行报价的事）',
  '处理商业承兑与银行承兑的信用差异、以及票据是否可贴现',
  '处理跨到期日违约、追索与票据瑕疵',
  '处理按实际天数/365 计息的口径（若合同如此约定，请先按 360 折算或在表里直接给出利息）',
  '给出金融或法律意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '票据号\t票面金额\t年贴现率\t贴现日\t到期日\t计息天数\t贴现利息\t实付金额',
  'P001\t1000000.00\t3.6%\t2026-03-01\t2026-09-01\t184\t18400.00\t981600.00',
  'P002\t500000.00\t4.2%\t2026-04-15\t2026-10-15\t183\t10675.00\t489325.00',
  '合计\t1500000.00\t\t\t\t\t29075.00\t1470925.00',
].join('\n');

const TOL = 0.01;
const DAY_BASIS = 360;

const ROLES = {
  party: ['票据号', '票号', '票据编号', '单号'],
  face: ['票面金额', '票面', '面值'],
  rate: ['年贴现率', '贴现率', '年利率'],
  start: ['贴现日', '贴现日期', '起息日'],
  end: ['到期日', '到期日期', '兑付日'],
  days: ['计息天数', '天数', '贴现天数'],
  interest: ['贴现利息', '利息'],
  net: ['实付金额', '实付', '贴现金额'],
};

const LABELS = {
  party: '票据号', face: '票面金额', rate: '年贴现率', start: '贴现日', end: '到期日',
  days: '计息天数', interest: '贴现利息', net: '实付金额',
};

const REQUIRED = ['party', 'face', 'rate', 'start', 'end', 'days', 'interest', 'net'];
const SUM_ROLES = ['face', 'interest', 'net'];

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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 日期 -> UTC 毫秒（只认 YYYY-MM-DD / YYYY/M/D / YYYY.M.D；不认的返回 null，绝不猜）。 */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '').replace(/[./]/g, '-');
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]); const mo = Number(m[2]); const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const t = Date.UTC(y, mo - 1, d);
  const b = new Date(t);
  if (b.getUTCFullYear() !== y || b.getUTCMonth() !== mo - 1 || b.getUTCDate() !== d) return null;
  return t;
}

const DAY = 86400000;
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
const who = (it) => `票据「${it.byRole.party || '(未命名)'}」`;

/** 天数真值：算头不算尾 = 差值；算尾不算头 = 差值 + 1（银行口径不完全一致，两者都接受）。 */
function dayTruth(it) {
  const a = normDate(it.byRole.start);
  const b = normDate(it.byRole.end);
  if (a === null || b === null) return null;
  const diff = Math.round((b - a) / DAY);
  return { headNoTail: diff, tailNoHead: diff + 1, inverted: diff <= 0 };
}

function checkDays(it) {
  const t = dayTruth(it);
  if (!t) return null;
  const stated = num(it, 'days');
  if (stated === null) return null;
  if (stated === t.headNoTail || stated === t.tailNoHead) return null;
  return {
    level: 'P0', category: '计息天数与起止日不符', line: it.line,
    message: `${who(it)}的计息天数是 ${stated} 天，但按贴现日（${it.byRole.start}）到到期日（${it.byRole.end}）`
      + `算头不算尾应为 ${t.headNoTail} 天、算尾不算头应为 ${t.tailNoHead} 天。`,
    advice: '天数错一天，利息就错一天；请先与贴现行确认天数口径。',
  };
}

function checkInterest(it) {
  const face = num(it, 'face');
  const rate = num(it, 'rate');
  const stated = num(it, 'interest');
  if (face === null || rate === null || stated === null) return null;
  let days = num(it, 'days');
  if (days === null) {
    const t = dayTruth(it);
    days = t ? t.headNoTail : null;
  }
  if (days === null) return null;
  const expect = round2(face * rate / 100 / DAY_BASIS * days);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '贴现利息与复算不符', line: it.line,
    message: `${who(it)}的贴现利息是 ${stated.toFixed(2)}，`
      + `按 ${face.toFixed(2)} × ${rate}% ÷ ${DAY_BASIS} × ${days} 天复算应为 ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)} 元。`,
    advice: `确认三件事：票面金额、年贴现率、以及**除数是 ${DAY_BASIS} 还是 365**（银行承兑常用 360）。`,
  };
}

function checkNet(it) {
  const face = num(it, 'face');
  const interest = num(it, 'interest');
  const stated = num(it, 'net');
  if (face === null || interest === null || stated === null) return null;
  const expect = round2(face - interest);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '实付金额与复算不符', line: it.line,
    message: `${who(it)}的实付金额是 ${stated.toFixed(2)}，`
      + `按 票面金额 ${face.toFixed(2)} − 贴现利息 ${interest.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '实付 = 票面 − 利息（若另有手续费、印花税，应在本表里显式列出来）。',
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
        advice: '要么明细行漏了票，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一票据号出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一票据一般只贴现一次；重复行可能是**重复申请贴现**，请务必核对。',
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
          advice: '缺这一格这笔贴现就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的票据贴现计算表（要能认出「票面金额」「年贴现率」「贴现日」「到期日」'
      + '「计息天数」「贴现利息」「实付金额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从贴现台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一张票的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkDays(it); if (a) findings.push(a);
    const b = checkInterest(it); if (b) findings.push(b);
    const c = checkNet(it); if (c) findings.push(c);
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
      notes: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      face_total: sumOf('face'),
      interest_total: sumOf('interest'),
      net_total: sumOf('net'),
      basis: `贴现利息 = 票面金额 × 年贴现率 ÷ ${DAY_BASIS} × 计息天数；实付金额 = 票面金额 − 贴现利息；`
        + '计息天数与起止日勾稽（算头不算尾 / 算尾不算头两种口径都接受）；合计行逐列复核。',
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
      + '不代表贴现率报价合理、也不代表票据本身可贴现 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, dayTruth, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, DAY_BASIS,
};
