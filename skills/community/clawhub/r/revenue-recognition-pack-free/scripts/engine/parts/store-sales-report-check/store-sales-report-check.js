#!/usr/bin/env node
/**
 * store-sales-report-check.js —— 门店营收上报核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**连锁门店每天/每月要向上报营业额**，而门店的数字来自多个渠道：
 *   POS 现金、POS 刷卡、移动支付（微信/支付宝）、外卖平台、团购券核销 —— 五路来源。
 *   ① 渠道合计 = 五路之和
 *   ② 差异     = 上报营业额 − 渠道合计（**门店手工凑数、漏报某个渠道、把外卖算重** 都会暴露在这里）
 * 总部核不上账，往往只能等审计或等门店自己说；几十上百家门店 × 每天，人眼核不动。
 *
 * 与已有能力的区别：`cash-count-check` 只核**现金**（备用金/实盘/长短款）；
 * `platform-settlement-check` 核的是**与平台的对账**（成交/退款/技术服务费）；
 * 本能力核的是**门店上报营业额与各收款渠道之和是否一致**（内部上报口径）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查平台账单、不调用大模型；材料不足不给结论；不给审计意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '渠道合计勾稽（POS现金 + POS刷卡 + 移动支付 + 外卖平台 + 团购券）',
  '差异勾稽（上报营业额 − 渠道合计）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复门店/日期检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '任一渠道金额为负检测',
  '差异绝对值超过给定阈值检测（阈值由入参 tolerance 给出；未给出则本项不执行）',
  '上报营业额为负检测',
  '渠道合计为 0 但上报营业额非 0 检测',
  '差异率（|差异| ÷ 渠道合计）超过 1% 检测',
];

const OUT_OF_SCOPE = [
  '判断门店是否瞒报（那要结合库存、监控与巡店）',
  '与外卖/团购平台账单逐笔对账（那需要平台结算单，请用平台结算类工具）',
  '处理跨日结账、跨店调拨与预售卡券',
  '判断收入确认时点；给出审计意见',
  '读取 .xlsx 或 POS/外卖平台导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '门店日期\tPOS现金\tPOS刷卡\t移动支付\t外卖平台\t团购券\t渠道合计\t上报营业额\t差异',
  'A店-0901\t5000.00\t12000.00\t8000.00\t3000.00\t2000.00\t30000.00\t30000.00\t0.00',
  'B店-0901\t3000.00\t9000.00\t6000.00\t2000.00\t1000.00\t21000.00\t21000.00\t0.00',
  '合计\t8000.00\t21000.00\t14000.00\t5000.00\t3000.00\t51000.00\t51000.00\t0.00',
].join('\n');

const TOL = 0.01;
const DIFF_RATE_CAP = 0.01;      // 差异率上限 1%

const ROLES = {
  party: ['门店日期', '门店', '日期', '班次'],
  cash: ['POS现金', '现金'],
  card: ['POS刷卡', '刷卡', '银行卡'],
  mobile: ['移动支付', '微信支付宝', '扫码'],
  delivery: ['外卖平台', '外卖'],
  coupon: ['团购券', '券核销', '团购'],
  channelTotal: ['渠道合计', '渠道小计', '合计渠道'],
  reported: ['上报营业额', '上报金额', '营业额'],
  diff: ['差异', '差额'],
};

const LABELS = {
  party: '门店日期', cash: 'POS现金', card: 'POS刷卡', mobile: '移动支付',
  delivery: '外卖平台', coupon: '团购券', channelTotal: '渠道合计',
  reported: '上报营业额', diff: '差异',
};

const CHANNELS = ['cash', 'card', 'mobile', 'delivery', 'coupon'];
const REQUIRED = ['party'].concat(CHANNELS, ['channelTotal', 'reported', 'diff']);
const SUM_ROLES = CHANNELS.concat(['channelTotal', 'reported', 'diff']);

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
  // ⚠️ 顺序即优先级（更具体在前）：「POS现金」要排在「POS刷卡」/「现金」的宽泛别名之前；
  //    「渠道合计」「上报营业额」不能被「差异」或「合计」类词抢走。
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

function channelSum(it) {
  let sum = 0;
  let any = false;
  for (const r of CHANNELS) {
    const v = num(it, r);
    if (v !== null) { sum += v; any = true; }
  }
  return any ? round2(sum) : null;
}

function checkChannelTotal(it) {
  const stated = num(it, 'channelTotal');
  const sum = channelSum(it);
  if (sum === null || stated === null) return null;
  if (Math.abs(sum - stated) <= TOL) return null;
  const parts = CHANNELS.map((r) => `${LABELS[r]} ${(num(it, r) || 0).toFixed(2)}`).join(' + ');
  return {
    level: 'P0', category: '渠道合计与各渠道之和不符', line: it.line,
    message: `${who(it)}的渠道合计是 ${stated.toFixed(2)}，按 ${parts} 相加应为 ${sum.toFixed(2)}。`,
    advice: '渠道合计是"五路收款之和"；漏写一路（常见是团购券核销或外卖）会让后面的差异凭空出现。',
  };
}

function checkDiff(it) {
  const reported = num(it, 'reported'); const total = num(it, 'channelTotal'); const stated = num(it, 'diff');
  if (reported === null || total === null || stated === null) return null;
  const expect = round2(reported - total);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '差异与复算不符', line: it.line,
    message: `${who(it)}的差异是 ${stated.toFixed(2)}，按 上报营业额 ${reported.toFixed(2)} − 渠道合计 ${total.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '差异 = 上报 − 渠道合计；**方向别写反**（正=上报比渠道多，可能是重复上报或渠道漏记）。',
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
        advice: '要么明细行漏了门店，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一门店日期出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '重复行会让上报与渠道一起翻倍；若是分时段补录，请把时段写进"门店日期"列。',
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
          advice: '缺这一格这天的营收就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的门店营收上报表（要能认出「POS现金」「POS刷卡」「移动支付」「外卖平台」「团购券」'
      + '「渠道合计」「上报营业额」「差异」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从 POS/外卖平台导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一家门店的明细行']);

  const tolParam = normNumber(payload && payload.tolerance);
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkChannelTotal(it); if (a) findings.push(a);
    const b = checkDiff(it); if (b) findings.push(b);
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
  const offStores = t.items.filter((it) => {
    const v = num(it, 'diff');
    return v !== null && Math.abs(v) > TOL;
  }).length;

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      channel_total: sumOf('channelTotal'),
      reported_total: sumOf('reported'),
      diff_total: sumOf('diff'),
      stores_with_diff: offStores,
      basis: '渠道合计 = POS现金 + POS刷卡 + 移动支付 + 外卖平台 + 团购券；'
        + '差异 = 上报营业额 − 渠道合计；合计行逐列复核。',
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
      + '不代表各渠道数据本身真实、也不代表没有未入表的收款 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHANNELS,
};
