/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * sales-rebate-check.js —— 销售返利与渠道返点核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**给经销商 / 连锁客户 / 电商平台发返利的销售与渠道财务**，
 * 在**每季度或每年度返利结账、以及返利实际兑付之前**。销售返利与渠道返点是
 * 「先计提、后兑付」的负债：本期计提多少、本期兑付多少、期末还挂着多少没兑付，
 * 必须与返利政策（计算基数 × 返利比例）逐行对得上；渠道返点（平台返点 / 连锁返点）
 * 同理，只是兑付方式换成了抵扣货款或平台账单抵扣。
 *
 * 核心可算关系（都能手算复现）：
 *   应计返利         = 计算基数 × 返利比例
 *   期末已计提未兑付 = 期初已计提 + 本期计提 − 本期实际兑付
 *   本期实际兑付     ≤ 期初已计提 + 本期计提（不能超兑）
 *   合计行           = 明细逐行相加（计算基数 / 应计返利 / 期初已计提 / 本期计提 /
 *                      本期实际兑付 / 期末已计提未兑付）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**返利政策本身是否合理、该按哪一档比例、以及该不该计提（属于商务政策与会计判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库踩过 6 次的坑）。
   若把裸词 `计提` / `兑付` 排在前面，`期初已计提`、`本期计提`、`期末已计提未兑付`、
   `本期实际兑付` 都会被抢走（同一个 role 被后一列**覆盖**）⇒ 那几列永远读到 0，
   而 `header_map_check` 会判定"识别出的表头数 > 解析出的列数"。
   同理**不能**在 `current` 里放裸词 `本期`：那样 `本期实际兑付` 会被 `current` 抢走，
   `paidOut` 永远认不出来。所以裸词（期初 / 本期 / 期末 / 计提 / 兑付）只做**最后的兜底**。 */
const ROLES = {
  party: ['客户/渠道', '客户渠道', '经销商/渠道', '客户', '渠道', '经销商', '平台'],
  policy: ['返利政策', '返点政策', '返利类型', '返利方式', '政策'],
  base: ['计算基数', '计提基数', '返利基数', '销售基数', '基数'],
  rate: ['返利比例', '返点比例', '返利率', '返点率', '比例', '比率'],
  accrued: ['应计返利', '应计提返利', '应计返点', '应计返利额'],
  /* —— 带限定语的三列：期初 / 本期 / 期末，整体排在裸词之前 —— */
  opening: ['期初已计提', '期初计提', '期初已计'],
  current: ['本期计提', '本期应计提', '本期已计提'],
  closing: ['期末已计提未兑付', '期末未兑付', '期末已计提'],
  paidOut: ['本期实际兑付', '本期已兑付', '实际兑付', '本期兑付', '兑付金额'],
  payMethod: ['兑付方式', '兑付形式', '兑付渠道', '支付方式'],
  /* —— 兜底裸词：只有前面的带限定语列一个都没命中时才轮到它们 —— */
  openingAny: ['期初'],
  currentAny: ['本期'],
  closingAny: ['期末'],
  accrualAny: ['计提'],
  cashAny: ['兑付'],
};

const LABELS = {
  party: '客户/渠道', policy: '返利政策', base: '计算基数', rate: '返利比例',
  accrued: '应计返利', opening: '期初已计提', current: '本期计提',
  paidOut: '本期实际兑付', closing: '期末已计提未兑付', payMethod: '兑付方式',
};

const REQUIRED = ['party', 'policy', 'base', 'rate', 'accrued', 'opening', 'current', 'paidOut', 'closing', 'payMethod'];
/* 合计行要逐列复核的 6 个金额列（客户/政策/比例/兑付方式是文本列，不参与求和） */
const SUM_ROLES = ['base', 'accrued', 'opening', 'current', 'paidOut', 'closing'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;              // 合计勾稽、滚动勾稽的容差
const RATE_TOL = 0.02;         // 应计返利 = 基数 × 比例的容差（产品标准给的口径）
const COMMON_RATE_MAX = 0.20;  // 常见返利档位上限：20%
const PAY_METHOD_UNDECIDED = /^(待定|待议|未定|未确定)$/;
/* ⚠️ 付费开关**只声明一次**（形态 B）：`strip_free_engine` 按「以 const paid 开头 + Boolean(」这一行
   识别并摘掉付费语句；写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒
   泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行、以及付费分支判断式的字面量：
   `strip` 的残渣断言是**纯字符串包含**判断，写了就会被当成"没删干净"而整包回滚（本轮实测踩到）。
   形态 A（MARKER 整块删）与形态 B（内联分支）**只能出现一个**，两个同时出现会把免费检查也删光。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（计算基数 / 应计返利 / 期初已计提 / 本期计提 / 本期实际兑付 / 期末已计提未兑付）',
  '同一「客户/渠道 + 返利政策」重复行检测',
  '应计返利 = 计算基数 × 返利比例（不符即报）',
  '期末已计提未兑付 = 期初已计提 + 本期计提 − 本期实际兑付（滚动勾稽）',
  '本期实际兑付为负（负数兑付）检测',
  '应计返利为负（负数计提）检测',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '本期实际兑付超过 期初已计提 + 本期计提（超兑）检测',
  '返利比例不在常见档位（0~20%）提示',
  '期末已计提未兑付为负检测',
  '返利比例为 0 但应计返利 > 0（口径矛盾）检测',
  '兑付方式空白或「待定」提示',
];

const OUT_OF_SCOPE = [
  '判断返利政策本身是否合理、该按哪一档比例计提（属于商务政策判断）',
  '判断返利是否已经满足计提条件（是否已达成销量/回款条件属于会计与业务判断）',
  '代替审计抽凭程序，也不出具审计或鉴证意见',
  '核对返利合同、平台账单、银行回单的**真伪**，或与 CRM / 返利系统的逐行明细比对',
  '读取 ERP / CRM / 电商后台的导出文件（需要你先导出成文本贴进来）',
  '判断返利与返点的税务处理（是否开票、如何抵扣属于税务判断）',
];

const SAMPLE_TEXT = [
  '客户/渠道\t返利政策\t计算基数\t返利比例\t应计返利\t期初已计提\t本期计提\t本期实际兑付\t期末已计提未兑付\t兑付方式',
  '甲经销商\t年度阶梯返利\t1000000\t3%\t30000\t20000\t10000\t5000\t25000\t银行转账',
  '乙连锁\t季度销量返利\t800000\t2%\t16000\t8000\t8000\t4000\t12000\t抵扣货款',
  '丙电商平台\t平台返点\t500000\t5%\t25000\t10000\t15000\t10000\t15000\t平台账单抵扣',
  '合计\t\t2300000\t\t71000\t38000\t33000\t19000\t52000\t',
].join('\n');

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
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

/** 返利比例统一换算成**小数**：`3%` → 0.03；不带百分号的 `3` 也按 3% 处理（人写口径）；
   已经是小数的 `0.03` 原样使用。这样"基数 × 比例"才与台账里的应计返利可比。 */
function normRate(raw) {
  const n = normNumber(raw);
  if (n === null) return null;
  if (String(raw).indexOf('%') >= 0) return n / 100;
  if (Math.abs(n) > 1) return n / 100;
  return n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function who(it) {
  const p = String(it.party || '').trim();
  const pol = String(it.policy || '').trim();
  if (!p) return `第 ${it.line} 行`;
  return pol ? `${p}（${pol}）` : p;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}`,
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const party = String(it.party || '').trim();
    const policy = String(it.policy || '').trim();
    if (!party && !policy) continue;
    const key = `${party}||${policy}`;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「客户/渠道 + 返利政策」完全相同 —— 可能重复计提或重复兑付`,
        evidence: `客户/渠道=${party}；返利政策=${policy}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkAccruedFormula(it) {
  const base = normNumber(it.base);
  const rate = normRate(it.rate);
  const accrued = normNumber(it.accrued);
  if (base === null || rate === null || accrued === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - accrued) > RATE_TOL) {
    return {
      line: it.line, level: 'P0', category: '应计返利与基数比例不符',
      message: `${who(it)} 应计返利填 ${accrued}，但 计算基数 ${base} × 返利比例 ${round2(rate * 100)}% = ${expect}`,
      evidence: `计算基数=${base}；返利比例=${round2(rate * 100)}%（${rate}）；应计返利=${accrued}；应等于=${expect}；差=${round2(accrued - expect)}`,
    };
  }
  return null;
}

function checkRollForward(it) {
  const opening = normNumber(it.opening);
  const current = normNumber(it.current);
  const paidOut = normNumber(it.paidOut);
  const closing = normNumber(it.closing);
  if (opening === null || current === null || paidOut === null || closing === null) return null;
  const expect = round2(opening + current - paidOut);
  if (Math.abs(expect - closing) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末未兑付滚动不符',
      message: `${who(it)} 期末已计提未兑付填 ${closing}，但 期初 ${opening} + 本期计提 ${current} − 本期实际兑付 ${paidOut} = ${expect}`,
      evidence: `期初已计提=${opening}；本期计提=${current}；本期实际兑付=${paidOut}；期末已计提未兑付=${closing}；应等于=${expect}；差=${round2(closing - expect)}`,
    };
  }
  return null;
}

function checkNegativePaidOut(it) {
  const v = normNumber(it.paidOut);
  if (v === null || v >= 0) return null;
  return {
    line: it.line, level: 'P0', category: '本期实际兑付为负',
    message: `${who(it)} 本期实际兑付为 ${v}（负数）—— 兑付不应为负，退回请走单独的红字流程`,
    evidence: `本期实际兑付=${v}`,
  };
}

function checkNegativeAccrued(it) {
  const v = normNumber(it.accrued);
  if (v === null || v >= 0) return null;
  return {
    line: it.line, level: 'P1', category: '应计返利为负',
    message: `${who(it)} 应计返利为 ${v}（负数）—— 请确认是冲回还是返利政策填错`,
    evidence: `应计返利=${v}`,
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把返利台账（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  const recognized = header.map((h) => roleOf(h)).filter(Boolean).length;
  if (recognized < 2) {
    return insufficient(['认不出表头：第一行应是返利台账表头，且至少能认出 2 列（例如 客户/渠道、计算基数、返利比例、应计返利）']);
  }
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [
      checkAccruedFormula(it),
      checkRollForward(it),
      checkNegativePaidOut(it),
      checkNegativeAccrued(it),
    ];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        base_total: round2(items.reduce((n, it) => n + (normNumber(it.base) || 0), 0)),
        accrued_total: round2(items.reduce((n, it) => n + (normNumber(it.accrued) || 0), 0)),
        paid_out_total: round2(items.reduce((n, it) => n + (normNumber(it.paidOut) || 0), 0)),
        tolerance: TOL,
        rate_tolerance: RATE_TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, ROLES, normRate,
};
