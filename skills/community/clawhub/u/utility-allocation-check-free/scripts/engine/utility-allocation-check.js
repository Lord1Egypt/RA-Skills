#!/usr/bin/env node
/**
 * utility-allocation-check.js —— 公共费用分摊核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**写字楼 / 园区 / 厂房把公共电费、水费、物业费按面积分摊给各租户，每月都要对一次**。
 * 租户会质疑"凭什么我这么多"，物业要能逐户复算：面积占比对不对、各项分摊加起来等不等于应缴、
 * 分摊金额与占比是否吻合。单量一多（几十上百户），人眼核不动；而这些**全是算术**。
 *
 * 与已有能力的区别：本能力核「**物业 ↔ 租户的费用分摊表**」，不是平台结算、不是课时核销。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用大模型；材料不足不给结论；不判断分摊规则是否合理。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐户应缴勾稽（电费分摊 + 水费分摊 + 物业费 = 应缴合计）',
  '合计行复核（每一列的合计是否等于各户之和）',
  '重复租户检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '分摊金额与面积占比是否吻合（分摊 ÷ 该项总额 vs 占比）',
  '占比异常检测（≤0 或 >100%）',
  '应缴合计为负检测',
  '逐户占比与面积比例是否一致（面积 ÷ 总面积 vs 占比）',
];

const OUT_OF_SCOPE = [
  '判断分摊规则（按面积 / 按用量 / 按人头）是否合理（那是租赁合同与业委会的事）',
  '核对实际用电用水量（那要拿抄表记录来比）',
  '处理欠费、滞纳金与减免（本工具只核你给出的这张表算得对不对）',
  '给出税务或法律意见',
  '读取 .xlsx（需要你先从系统导出、复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '租户\t计费面积\t面积占比\t电费分摊\t水费分摊\t物业费\t应缴合计',
  '甲公司\t500\t50%\t4000.00\t1000.00\t1500.00\t6500.00',
  '乙公司\t300\t30%\t2400.00\t600.00\t900.00\t3900.00',
  '丙公司\t200\t20%\t1600.00\t400.00\t600.00\t2600.00',
  '合计\t1000\t100%\t8000.00\t2000.00\t3000.00\t13000.00',
].join('\n');

const TOL = 0.01;
const PCT_TOL = 0.5; // 百分点容差（四舍五入到整数占比时常见）

const ROLE_LABELS = {
  tenant: '租户', area: '计费面积', share: '面积占比',
  elec: '电费分摊', water: '水费分摊', property: '物业费', total: '应缴合计',
};
const labelOf = (r) => ROLE_LABELS[r] || r;
const SUM_ROLES = ['area', 'elec', 'water', 'property', 'total'];

const COLUMN_ROLES = [
  [/租户|商户|业主|房号|客户名称|单位名称|公司/, 'tenant'],
  // ⚠️ 顺序要紧：「面积占比」必须排在「面积」之前，否则会被面积规则先吃掉，
  //    导致 share 永远为空 —— 而那条付费检查（分摊 ÷ 总额 vs 占比）就**永不执行**。
  [/面积占比|占比|比例|分摊比例/, 'share'],
  [/计费面积|建筑面积|使用面积|面积/, 'area'],
  [/电费|电费分摊/, 'elec'],
  [/水费|水费分摊/, 'water'],
  [/物业费|物业管理费|管理费/, 'property'],
  [/应缴合计|应缴|合计金额|应收|小计/, 'total'],
];

const NON_AMOUNT_KWS = /备注|状态|日期|月份|楼层|联系人|电话|抄表/;

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t');
  if (line.indexOf(',') >= 0) return line.split(',');
  return line.trim().split(/\s{2,}|\s+/);
}

function roleOf(header) {
  const h = String(header || '').replace(/\s/g, '');
  if (!h) return 'skip';
  if (NON_AMOUNT_KWS.test(h)) return 'skip';
  for (const pair of COLUMN_ROLES) if (pair[0].test(h)) return pair[1];
  return 'extra';
}

function normAmount(v) {
  if (v === null || v === undefined) return null;
  let s = String(v).trim();
  if (!s) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  s = s.replace(/[¥￥,\s]/g, '').replace(/元$/, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return neg ? -n : n;
}

/** 占比支持「50%」「0.5」「50」三种写法 → 统一成百分数（50 表示 50%）。 */
function normPct(v) {
  if (v === null || v === undefined) return null;
  const s = String(v).trim().replace(/％/g, '%');
  if (!s) return null;
  if (s.endsWith('%')) {
    const n = Number(s.slice(0, -1));
    return Number.isFinite(n) ? n : null;
  }
  const n = Number(s.replace(/[,\s]/g, ''));
  if (!Number.isFinite(n)) return null;
  return n <= 1 ? n * 100 : n;
}

function isBlank(v) {
  const s = String(v === null || v === undefined ? '' : v).trim();
  if (!s) return true;
  return /^(--+|\?\?+|N\/?A|na|待填|TODO|xxx|\*\*\*?)$/i.test(s);
}

function findHeader(lines) {
  for (let i = 0; i < Math.min(lines.length, 10); i += 1) {
    const cells = splitRow(lines[i]).map((c) => c.trim());
    const roles = cells.map(roleOf);
    const known = roles.filter((r) => r !== 'skip' && r !== 'extra');
    const hasKey = known.includes('tenant');
    const money = ['elec', 'water', 'property', 'total'].filter((r) => known.includes(r)).length;
    if (hasKey && money >= 2) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };
  const items = [];
  const totals = [];
  for (let i = header.index + 1; i < lines.length; i += 1) {
    const raw = lines[i];
    if (!raw || !raw.trim()) continue;
    const cells = splitRow(raw).map((c) => c.trim());
    const rec = { line: i + 1, raw: raw.trim(), byRole: {} };
    header.roles.forEach((role, ci) => {
      if (role === 'skip' || role === 'extra') return;
      rec.byRole[role] = cells[ci] === undefined ? '' : cells[ci];
    });
    const nm = String(rec.byRole.tenant || '').trim();
    if (/^(合计|总计|小计|total)/i.test(nm)) totals.push(rec); else items.push(rec);
  }
  return { header, items, totals, cols: header.cells };
}

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

const tag = (rec) => String(rec.byRole.tenant || '（未命名租户）').trim();

function checkTotal(rec) {
  const e = normAmount(rec.byRole.elec);
  const w = normAmount(rec.byRole.water);
  const p = normAmount(rec.byRole.property);
  const t = normAmount(rec.byRole.total);
  if (e === null || w === null || p === null || t === null) return null;
  const expect = Math.round((e + w + p) * 100) / 100;
  if (Math.abs(expect - t) <= TOL) return null;
  return finding('P0', '应缴合计不平', rec.line,
    tag(rec) + ' 的应缴合计是 ' + t.toFixed(2) + '，但「电费 ' + e.toFixed(2) + ' + 水费 '
      + w.toFixed(2) + ' + 物业费 ' + p.toFixed(2) + '」应为 ' + expect.toFixed(2)
      + '（差 ' + (t - expect).toFixed(2) + '）',
    rec.raw, '先确认口径：如果有滞纳金、减免、预收冲抵，请把它们也列成一列再核。');
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals.length) return out;
  const t = totals[0];
  for (const role of SUM_ROLES) {
    const claimed = normAmount(t.byRole[role]);
    if (claimed === null) continue;
    let sum = 0; let ok = true;
    for (const it of items) {
      const n = normAmount(it.byRole[role]);
      if (n === null) { ok = false; break; }
      sum += n;
    }
    if (!ok) continue;
    sum = Math.round(sum * 100) / 100;
    if (Math.abs(sum - claimed) <= TOL) continue;
    out.push(finding('P0', '合计行算错', t.line,
      '合计行的「' + labelOf(role) + '」写的是 ' + claimed + '，但各户相加是 ' + sum
        + '（差 ' + Math.round((claimed - sum) * 100) / 100 + '）',
      t.raw, '合计行是向各户收费的依据，对不上时通常有户被漏加或重复加。'));
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.tenant || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push(finding('P0', '同一租户出现两行', it.line,
        key + ' 出现了两次（上一次在第 ' + seen.get(key) + ' 行）',
        it.raw, '同一租户两行会导致重复收费或漏收，请先合并。'));
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const roles = Object.keys(items[0] ? items[0].byRole : {}).filter((r) => r !== 'tenant');
  for (const it of items) {
    if (!String(it.byRole.tenant || '').trim()) {
      out.push(finding('P0', '租户名称缺失', it.line, '这一行没有租户名称', it.raw,
        '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = it.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', it.line,
          tag(it) + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          it.raw, '分摊表出现空列，通常是从系统导出时漏选。'));
      } else {
        const okNum = normAmount(v) !== null || (r === 'share' && normPct(v) !== null);
        if (!okNum) {
          out.push(finding('P1', '数值无法解析', it.line,
            tag(it) + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的数值',
            it.raw, '请确认列是否串位。'));
        }
      }
    }
  }
  return out;
}

/** 分摊金额应与占比吻合：该项分摊 ÷ 该项总额 ≈ 占比。 */
function insufficient(missing) {
  return { status: 'insufficient_input', missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。' };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['费用分摊表原文（text）']);
  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的分摊表（要能认出「租户」+ 至少两个费用列，例如「电费分摊」「物业费」）',
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一户的明细行']);

  const findings = [];
  const notRun = [];
  const totalsOf = {};
  for (const role of ['elec', 'water']) {
    totalsOf[role] = Math.round(t.items.reduce((s, it) => {
      const n = normAmount(it.byRole[role]);
      return s + (n === null ? 0 : n);
    }, 0) * 100) / 100;
  }
  for (const it of t.items) {
    const a = checkTotal(it); if (a) findings.push(a);

  }
  for (const f of checkTotalRow(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => Math.round(t.items.reduce((s, it) => {
    const n = normAmount(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0) * 100) / 100;

  const result = {
    findings,
    summary: {
      tenants: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      elec_total: sumOf('elec'),
      water_total: sumOf('water'),
      payable_total: sumOf('total'),
      basis: '逐户「电费+水费+物业费=应缴合计」比对；合计行逐列复核；付费档另核分摊与占比是否吻合',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张表**算得对**，'
      + '不代表分摊规则合理、也不代表实际用量真实 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, normPct, isBlank, labelOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, ROLE_LABELS, SUM_ROLES,
};
