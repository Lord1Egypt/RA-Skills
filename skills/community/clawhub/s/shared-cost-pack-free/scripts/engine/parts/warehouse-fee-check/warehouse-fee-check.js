#!/usr/bin/env node
/**
 * warehouse-fee-check.js —— 仓储费与超期费核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**用第三方仓（或自有仓对外收费）的企业每月都要核仓储费账单**：
 *   ① 仓储费 = 计费数量 × 单价 × 计费天数（体积/托数/件数，按合同口径）
 *   ② 超期费 = 计费数量 × 超期费率 × 超期天数（免费仓储期之外的部分）
 *   ③ 应结合计 = 仓储费 + 超期费
 * 天数按自然日还是工作日、免费期天数有没有扣干净、超期费率分档 —— 每一处都能少结或多付几千块；
 * 一个月几十上百个批次，人眼核不动；而这些都是**纯算术**。
 *
 * 与已有能力的区别：`freight-reconciliation` 核的是**运费**（重量 × 单价 + 附加费）；
 * `inventory-check` 核**账实一致**；本能力核的是**仓储占用费与超期费**，口径完全不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判实物、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '仓储费勾稽（计费数量 × 单价 × 计费天数）',
  '超期费勾稽（计费数量 × 超期费率 × 超期天数）',
  '应结合计勾稽（仓储费 + 超期费）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复客户/批次检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '单价或超期费率为负检测',
  '计费数量非正检测',
  '计费天数超出 0~366 检测',
  '超期天数大于计费天数（逻辑倒挂）检测',
  '应结合计为负或小于仓储费检测',
];

const OUT_OF_SCOPE = [
  '判断仓储费率是否符合合同、免租期（免费仓储期）是否已包含在计费天数里',
  '处理入库/出库操作费、装卸费、贴标费等一次性费用（请另行列示）',
  '处理按体积重与实重取大的计费规则（请先在表里把计费数量算好）',
  '判断损耗与赔偿；给出法律意见',
  '读取 .xlsx 或 WMS 账单文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户\t计费数量\t单价\t计费天数\t仓储费\t超期天数\t超期费率\t超期费\t应结合计',
  '甲公司\t1000\t0.50\t30\t15000.00\t5\t1.00\t5000.00\t20000.00',
  '乙公司\t500\t0.60\t30\t9000.00\t0\t1.20\t0.00\t9000.00',
  '合计\t1500\t\t60\t24000.00\t5\t\t5000.00\t29000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['客户', '批次', '租户', '货主'],
  qty: ['计费数量', '数量', '计费单位'],
  // ⚠️ 顺序即优先级：更**具体**的关键词必须排在更**宽泛**的前面。
  //    这里「超期天数/超期费率/超期费」都排在「天数/单价/仓储费」之前 ——
  //    否则 `天数` 会把「超期天数」抢走（发版前的守卫当场抓到，本仓库第五次踩这类坑）。
  overdueDays: ['超期天数', '逾期天数'],
  overdueRate: ['超期费率', '超期单价', '逾期费率'],
  overdueFee: ['超期费', '逾期费'],
  price: ['单价', '仓储单价', '费率单价'],
  days: ['计费天数', '仓储天数', '天数'],
  fee: ['仓储费', '仓储费用'],
  total: ['应结合计', '应结合计费', '合计金额'],
};

const LABELS = {
  party: '客户', qty: '计费数量', price: '单价', days: '计费天数', fee: '仓储费',
  overdueDays: '超期天数', overdueRate: '超期费率', overdueFee: '超期费', total: '应结合计',
};

const REQUIRED = ['party', 'qty', 'price', 'days', 'fee', 'overdueDays', 'overdueRate', 'overdueFee', 'total'];
const SUM_ROLES = ['qty', 'days', 'fee', 'overdueDays', 'overdueFee', 'total'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库四次踩过的坑，见 tools/header_map_check.py）：
  //    「超期费率」必须排在「单价」类宽泛别名之前；「应结合计」不能被「合计」类抢走。
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
const who = (it) => `客户/批次「${it.byRole.party || '(未命名)'}」`;

function checkFee(it) {
  const qty = num(it, 'qty');
  const price = num(it, 'price');
  const days = num(it, 'days');
  const stated = num(it, 'fee');
  if (qty === null || price === null || days === null || stated === null) return null;
  const expect = round2(qty * price * days);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '仓储费与复算不符', line: it.line,
    message: `${who(it)}的仓储费是 ${stated.toFixed(2)}，`
      + `按 计费数量 ${qty} × 单价 ${price} × 计费天数 ${days} 复算应为 ${expect.toFixed(2)}。`,
    advice: '三个因子任一录错都会直接放大；合同里的"免费仓储期"应在计费天数里扣掉。',
  };
}

function checkOverdueFee(it) {
  const qty = num(it, 'qty');
  const rate = num(it, 'overdueRate');
  const od = num(it, 'overdueDays');
  const stated = num(it, 'overdueFee');
  if (qty === null || rate === null || od === null || stated === null) return null;
  const expect = round2(qty * rate * od);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '超期费与复算不符', line: it.line,
    message: `${who(it)}的超期费是 ${stated.toFixed(2)}，`
      + `按 计费数量 ${qty} × 超期费率 ${rate} × 超期天数 ${od} 复算应为 ${expect.toFixed(2)}。`,
    advice: '超期费率通常高于正常单价（有惩罚性）；用成正常单价会少收，反之会多收。',
  };
}

function checkTotal(it) {
  const fee = num(it, 'fee');
  const od = num(it, 'overdueFee');
  const stated = num(it, 'total');
  if (fee === null || od === null || stated === null) return null;
  const expect = round2(fee + od);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应结合计与复算不符', line: it.line,
    message: `${who(it)}的应结合计是 ${stated.toFixed(2)}，按 仓储费 ${fee.toFixed(2)} + 超期费 ${od.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '应结合计 = 仓储费 + 超期费；若还有操作费、装卸费，应在本表显式列示。',
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
        advice: '要么明细行漏了批次，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一客户/批次出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '多批次分行是正常的；但若本表按客户汇总，重复行会让数量与费用一起翻倍。',
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
          advice: '缺这一格这笔仓储费就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的仓储费结算表（要能认出「计费数量」「单价」「计费天数」「仓储费」'
      + '「超期天数」「超期费率」「超期费」「应结合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从 WMS 或仓储账单导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个批次的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkFee(it); if (a) findings.push(a);
    const b = checkOverdueFee(it); if (b) findings.push(b);
    const c = checkTotal(it); if (c) findings.push(c);
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
      batches: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      qty_total: sumOf('qty'),
      storage_fee_total: sumOf('fee'),
      overdue_fee_total: sumOf('overdueFee'),
      grand_total: sumOf('total'),
      basis: '仓储费 = 计费数量 × 单价 × 计费天数；超期费 = 计费数量 × 超期费率 × 超期天数；'
        + '应结合计 = 仓储费 + 超期费；合计行逐列复核。',
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
      + '不代表费率符合合同、也不代表免费仓储期已扣干净 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
