/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * vat-deduction-addon-check.js —— 增值税加计抵减核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**适用增值税加计抵减政策的一般纳税人（生产、生活性服务业等）**，
 * 在**每月（或每季）申报增值税、填写加计抵减台账之前**。
 * 会计要把"当期可抵扣进项税额 × 加计抵减比例"计提为本期加计抵减额，并逐期维护
 * "期初余额 / 本期计提 / 本期调减 / 本期实际抵减 / 期末余额"这几列；
 * 税务与审计盯的就是它们能不能**逐期滚动对上**。
 *
 * 核心可算关系（都能手算复现）：
 *   本期计提额   = 当期可抵扣进项税额 × 加计抵减比例
 *   期末余额     = 期初余额 + 本期计提 − 本期调减 − 本期实际抵减
 *   本期实际抵减 ≤ 抵减前应纳税额（抵减不能超过当期应纳税额）
 *   期末余额     ≥ 0（余额不应为负）
 *   合计行       = 明细逐行相加（销售额 / 四项服务销售额 / 进项税额 / 计提 / 调减 / 实际抵减；余额列不相加）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**你适用哪一档比例、是否属于适用行业、政策在某地某期是否仍有效（那属于税收政策判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**（本仓库踩过 6 次的坑）。
   `四项服务销售额` 里含 `销售额` —— 若 `sales` 排在前面，四项服务那一列会被抢走，
   `fourServiceSales` 永远认不出来 ⇒ 所有输入都缺必需列（`header_map_check` 会拦）。 */
const ROLES = {
  period: ['税款所属期', '所属期', '所属期间'],
  fourServiceSales: ['四项服务销售额', '四项服务销售额合计', '四项服务收入'],
  sales: ['销售额合计', '全部销售额', '销售额'],
  inputVat: ['当期可抵扣进项税额', '可抵扣进项税额', '进项税额'],
  ratio: ['加计抵减比例', '抵减比例', '加计比例'],
  openBalance: ['期初加计抵减余额', '期初余额', '期初可用余额'],
  provision: ['本期计提加计抵减额', '本期计提额', '本期计提'],
  reduction: ['本期调减额', '本期调减加计抵减额', '调减额'],
  actualCredit: ['本期实际抵减额', '本期实际抵减', '实际抵减额'],
  closeBalance: ['期末加计抵减余额', '期末余额', '期末可用余额'],
  vatBefore: ['抵减前应纳税额', '抵减前应纳税额额', '应纳税额'],
};

const LABELS = {
  period: '税款所属期', fourServiceSales: '四项服务销售额', sales: '销售额合计',
  inputVat: '当期可抵扣进项税额', ratio: '加计抵减比例', openBalance: '期初加计抵减余额',
  provision: '本期计提加计抵减额', reduction: '本期调减额', actualCredit: '本期实际抵减额',
  closeBalance: '期末加计抵减余额', vatBefore: '抵减前应纳税额',
};

const REQUIRED = ['sales', 'inputVat', 'ratio', 'openBalance', 'provision', 'actualCredit', 'closeBalance'];
/* ⚠️ 期初/期末是**时点余额**，不能相加；合计行只核这几列 */
const SUM_ROLES = ['sales', 'fourServiceSales', 'inputVat', 'provision', 'reduction', 'actualCredit'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按「`const paid` + `Boolean(`」这一行识别并摘掉付费语句；
   写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本轮实测踩到）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（明细逐行相加 = 合计；余额列不相加）',
  '期末余额 = 期初余额 + 本期计提 − 本期调减 − 本期实际抵减',
  '本期实际抵减 ≤ 抵减前应纳税额（抵减不能超过当期应纳税额）',
  '期末余额为负检测',
  '同一所属期重复行检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '本期计提 = 当期可抵扣进项税额 × 加计抵减比例 复算',
  '四项服务销售额占比低于 50% 却计提加计抵减（资格存疑）提示',
  '本期实际抵减超过可用额度（期初 + 计提 − 调减）检测',
  '加计抵减比例不在政策档位（5% / 10% / 15%）提示',
  '抵减前应纳税额为 0 或负数却仍有实际抵减提示',
];

const OUT_OF_SCOPE = [
  '判断你**是否属于**生产、生活性服务业或其它适用加计抵减的行业，以及适用哪一档比例（属于税收政策判断）',
  '代替增值税申报、代填申报表，或出具鉴证意见与税务意见',
  '核对进项发票真伪、勾选认证情况，或比对开票系统与勾选平台的逐行明细',
  '读取电子税务局 / 开票系统的导出文件（需要你先导出成文本贴进来）',
  '判断加计抵减政策在某地某期是否仍然有效（本工具只核你给的表内数字与勾稽关系）',
];

const SAMPLE_TEXT = [
  '税款所属期\t销售额合计\t四项服务销售额\t当期可抵扣进项税额\t加计抵减比例\t期初加计抵减余额\t本期计提加计抵减额\t本期调减额\t本期实际抵减额\t期末加计抵减余额\t抵减前应纳税额',
  '2026-01\t1000000.00\t700000.00\t60000.00\t10%\t0.00\t6000.00\t0.00\t6000.00\t0.00\t50000.00',
  '2026-02\t800000.00\t600000.00\t50000.00\t10%\t0.00\t5000.00\t0.00\t3000.00\t2000.00\t3000.00',
  '合计\t1800000.00\t1300000.00\t110000.00\t\t\t11000.00\t0.00\t9000.00\t\t',
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

const round2 = (n) => Math.round(n * 100) / 100;
/** 比例列：`10%` 与 `0.1` 都要认（按填法换算成小数）。 */
const who = (it) => { const p = String(it.period || '').trim(); return p ? `所属期 ${p}` : `第 ${it.line} 行`; };

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

function checkCloseVsBalance(it) {
  const open = normNumber(it.openBalance);
  const prov = normNumber(it.provision);
  const red = normNumber(it.reduction);
  const act = normNumber(it.actualCredit);
  const close = normNumber(it.closeBalance);
  if (open === null || prov === null || act === null || close === null) return null;
  const reduction = red === null ? 0 : red;
  const want = round2(open + prov - reduction - act);
  if (Math.abs(want - close) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末余额与滚动关系不符',
      message: `${who(it)} 期末余额 ${close} ≠ 期初 ${open} + 计提 ${prov} − 调减 ${reduction} − 实际抵减 ${act} = ${want}`,
      evidence: `期初余额=${open}；本期计提=${prov}；本期调减=${reduction}；本期实际抵减=${act}；期末余额=${close}；应为 ${want}`,
    };
  }
  return null;
}

function checkCreditVsVat(it) {
  const act = normNumber(it.actualCredit);
  const vat = normNumber(it.vatBefore);
  if (act === null || vat === null) return null;
  if (act - vat > TOL) {
    return {
      line: it.line, level: 'P0', category: '实际抵减超过应纳税额',
      message: `${who(it)} 本期实际抵减 ${act} > 抵减前应纳税额 ${vat} —— 抵减不能超过当期应纳税额`,
      evidence: `本期实际抵减=${act}；抵减前应纳税额=${vat}；超出=${round2(act - vat)}`,
    };
  }
  return null;
}

function checkNegativeClose(it) {
  const close = normNumber(it.closeBalance);
  if (close === null || close >= 0) return null;
  return {
    line: it.line, level: 'P0', category: '期末余额为负',
    message: `${who(it)} 期末加计抵减余额为 ${close}（负数）—— 余额不应为负`,
    evidence: `期末加计抵减余额=${close}`,
  };
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.period || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「税款所属期」完全相同 —— 可能重复计入`,
        evidence: `税款所属期=${it.period}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
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
  if (text.trim() === '') return insufficient(['材料文本为空：请把增值税加计抵减台账（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkCloseVsBalance(it), checkCreditVsVat(it), checkNegativeClose(it)];
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
        provision_total: round2(items.reduce((n, it) => n + (normNumber(it.provision) || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
