/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * rd-auxiliary-ledger-check.js —— 研发费用辅助账与高新指标核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有研发投入、要享加计扣除或申报高新技术企业的公司**，
 * 在**每月/每季归集研发费用、年度汇算清缴、以及高新认定申报前**。
 * 辅助账是研发费用的**唯一底稿**：项目、费用类别、本年归集金额与五项明细必须逐列勾稽；
 * 高新口径还额外要求「其他费用」不超过总额的 20%、且研发费用里必须有人工。
 *
 * 核心可算关系（都能手算复现）：
 *   本年归集金额 = 人员人工 + 直接投入 + 折旧摊销 + 设计试验费 + 其他费用（容差 0.02）
 *   明细逐行相加 = 合计行（本年归集金额 / 人员人工 / 直接投入 / 折旧摊销 / 设计试验费 / 其他费用）
 *   其他费用占比 = 其他费用 ÷ 本年归集金额（**按研发项目汇总后计算**，不是逐行算）
 *   其他费用占比 ≤ 其他费用占比上限（表里没写或写占位符时按高新口径 20%）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某项支出能不能归集、属于哪个费用类别、能不能享受高新或加计扣除
 *   （那属于会计与税务判断）；只做**表内可复算**的算术与口径核对。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不读环境变量、不写文件**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库踩过多次的坑）。
   · `其他费用占比上限` 里含 `其他费用` ⇒ `otherCap` 必须排在 `other` **前面**，
     否则上限那一列会被「其他费用」抢走（全表都读成占比上限）。
   · `本年归集金额` 里含 `金额` ⇒ 它也必须在同一个角色的别名数组里**排在 `金额` 前面**。
   · `其中：人员人工` / `直接投入` / `折旧摊销` / `设计试验费` 各自独立成角色，不共用宽泛别名。 */
const ROLES = {
  costType: ['费用类别', '费用类型', '费用项目', '费用科目'],
  project: ['研发项目', '项目名称', '项目'],
  amount: ['本年归集金额', '归集金额', '本年归集', '金额'],
  otherCap: ['其他费用占比上限', '费用占比上限', '占比上限'],
  labor: ['人员人工', '人工费用', '人员费用'],
  direct: ['直接投入', '直接材料', '材料投入'],
  depreciation: ['折旧摊销', '折旧费用', '摊销费用'],
  designTest: ['设计试验费', '设计试验', '试验费', '设计费'],
  other: ['其他费用', '其他支出'],
  hiTech: ['是否用于高新指标', '用于高新指标', '高新指标', '是否高新'],
  note: ['备注', '说明'],
};

const LABELS = {
  project: '研发项目', costType: '费用类别', amount: '本年归集金额', labor: '其中：人员人工',
  direct: '直接投入', depreciation: '折旧摊销', designTest: '设计试验费', other: '其他费用',
  otherCap: '其他费用占比上限', hiTech: '是否用于高新指标', note: '备注',
};

const REQUIRED = ['project', 'costType', 'amount', 'labor', 'direct', 'depreciation',
  'designTest', 'other', 'note'];
const SUM_ROLES = ['amount', 'labor', 'direct', 'depreciation', 'designTest', 'other'];
const DETAIL_ROLES = ['labor', 'direct', 'depreciation', 'designTest', 'other'];
/* 备注由第 6 项（checkNote）单独报，所以逐格空白扫描里不再重复扫它 —— 否则同一格报两次。 */
const BLANK_ROLES = REQUIRED.filter((r) => r !== 'note');
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.02;
const DEFAULT_OTHER_CAP = 20;                 // 高新口径：其他费用一般不超过 20%

const CHECKS_GIVEN = [
  '合计行逐列复核（本年归集金额 / 人员人工 / 直接投入 / 折旧摊销 / 设计试验费 / 其他费用）',
  '同一「研发项目 + 费用类别」重复行检测',
  '本年归集金额 = 人员人工 + 直接投入 + 折旧摊销 + 设计试验费 + 其他费用（容差 0.02）',
  '其他费用占比 = 其他费用 ÷ 本年归集金额，超过上限（默认 20%）报 P0',
  '任一项明细为负检测',
  '备注为空或占位符检测',
  '空白与占位符检测（含必需列缺失；缺个别列仍照常给结论并报「列缺失」）',
];

const CHECKS_WITHHELD = [
  '本年归集金额超过「其他费用 ÷ 20%」理论上限的 10 倍（异常放大）',
  '是否用于高新指标为「是」但费用类别不在常见高新口径提示',
  '折旧摊销超过本年归集金额的 50%（费用结构异常）',
  '人员人工为 0 但本年归集金额大于 0（高新口径要求研发费用中有人工）',
  '合计行其他费用占比超过 20%（与逐行口径一致地再查一次合计）',
];

const OUT_OF_SCOPE = [
  '判断某笔支出**能不能**归集为研发费用、属于哪个费用类别（那是会计与税务判断）',
  '判断本企业**是否满足**高新技术企业认定条件或加计扣除条件，也不出具鉴证意见',
  '核对发票、工资表、领料单等原始凭证的**真伪**，或与 ERP / 研发管理系统的逐笔明细比对',
  '读取 ERP / 财务系统 / 辅助账软件的导出文件（需要你先导出成文本贴进来）',
  '判断其他费用占比上限在**当年当地**到底是多少（本工具按你填的上限、没填时按 20% 参考口径核对）',
];

const SAMPLE_TEXT = [
  '研发项目\t费用类别\t本年归集金额\t其中：人员人工\t直接投入\t折旧摊销\t设计试验费\t其他费用\t其他费用占比上限\t是否用于高新指标\t备注',
  '项目A\t人员人工\t1200000\t1200000\t0\t0\t0\t0\t无\t是\t研发人员工资与社保',
  '项目A\t直接投入\t300000\t0\t300000\t0\t0\t0\t无\t是\t材料与试制费',
  '项目A\t折旧摊销\t200000\t0\t0\t200000\t0\t0\t无\t是\t研发设备折旧',
  '项目A\t其他费用\t100000\t0\t0\t0\t0\t100000\t20%\t是\t差旅与资料费',
  '合计\t\t1800000\t1200000\t300000\t200000\t0\t100000\t\t\t',
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
const pct = (n) => `${(n * 100).toFixed(2)}%`;
const who = (it) => {
  const p = String(it.project || '').trim();
  const c = String(it.costType || '').trim();
  if (p) return c ? `${p}·${c}` : p;
  return `第 ${it.line} 行`;
};

function groupByProject(items) {
  const m = new Map();
  for (const it of items) {
    const k = String(it.project || '').trim();
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(it);
  }
  return m;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: REQUIRED.slice(), header: [], recognised: 0 };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const recognised = cols.filter((c) => c.role).length;
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
  return { items, totals, missingColumns, header, recognised };
}

/* ================================ 免费档检查项 ================================ */

/** ① 合计行逐列复核：明细逐行相加 = 合计（六列都查一遍） */
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
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}（差 ${round2(stated - sum)}）`,
        evidence: `合计=${stated}；明细合计=${sum}；差额=${round2(stated - sum)}（${n} 行）`,
      });
    }
  }
  return out;
}

/** ② 同一「研发项目 + 费用类别」重复行检测 */
function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const p = String(it.project || '').trim();
    const c = String(it.costType || '').trim();
    if (!p && !c) continue;
    const key = `${p}\u0001${c}`;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '同一项目与费用类别重复',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「研发项目 + 费用类别」完全相同 —— 可能重复归集`,
        evidence: `研发项目=${p}；费用类别=${c}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** ③ 本年归集金额 = 五项明细之和（容差 0.02） */
function checkAmountParts(it) {
  const amt = normNumber(it.amount);
  if (amt === null) return null;
  let sum = 0;
  for (const role of DETAIL_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) return null;   // 明细列缺失/为空 ⇒ 交给「空白或占位符」那一项，这里不下结论
    sum += v;
  }
  sum = round2(sum);
  if (Math.abs(sum - amt) > TOL) {
    return {
      line: it.line, level: 'P0', category: '归集金额与五项明细不符',
      message: `${who(it)} 本年归集金额 ${amt} ≠ 人员人工 + 直接投入 + 折旧摊销 + 设计试验费 + 其他费用 = ${sum}（差 ${round2(amt - sum)}）`,
      evidence: `本年归集金额=${amt}；五项明细合计=${sum}；差额=${round2(amt - sum)}；容差=${TOL}`,
    };
  }
  return null;
}

/** ④ 其他费用占比 = 其他费用 ÷ 本年归集金额（按研发项目汇总），超过上限报 P0 */
function checkOtherCap(items) {
  const out = [];
  for (const [name, rows] of groupByProject(items)) {
    let other = 0;
    let amount = 0;
    let cap = null;
    for (const it of rows) {
      other += normNumber(it.other) || 0;
      amount += normNumber(it.amount) || 0;
      if (cap === null) {
        const c = normNumber(it.otherCap);
        if (c !== null && c > 0) cap = c;
      }
    }
    if (cap === null || cap <= 0) cap = DEFAULT_OTHER_CAP;
    if (amount <= 0) continue;
    other = round2(other);
    amount = round2(amount);
    const share = (other / amount) * 100;
    if (share - cap > 1e-9) {
      out.push({
        line: rows[0].line, level: 'P0', category: '其他费用占比超上限',
        message: `${name || `第 ${rows[0].line} 行起`} 其他费用 ${other} ÷ 本年归集金额 ${amount} = ${share.toFixed(2)}%，超过上限 ${cap}%（高新口径其他费用一般不超过 20%）`,
        evidence: `其他费用=${other}；本年归集金额=${amount}；占比=${share.toFixed(2)}%；上限=${cap}%`,
      });
    }
  }
  return out;
}

/** ⑤ 任一项明细为负 */
function checkNegative(it) {
  const out = [];
  for (const role of SUM_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < 0) {
      out.push({
        line: it.line, level: 'P0', category: '明细为负',
        message: `${who(it)} 的「${LABELS[role]}」填 ${v}（负数）—— 归集金额不允许为负`,
        evidence: `${LABELS[role]}=${v}`,
      });
    }
  }
  return out;
}

/** ⑥ 备注为空或占位符（备注列整列缺失时由「列缺失」代表，不逐行重复报） */
function checkNote(it, missingColumns) {
  if ((missingColumns || []).indexOf('note') >= 0) return null;
  if (!isBlank(it.note)) return null;
  return {
    line: it.line, level: 'P1', category: '备注缺失或占位符',
    message: `${who(it)} 的「备注」是空白或占位符 —— 归集依据无法追溯`,
    evidence: `备注=${it.note === undefined ? '(空)' : it.note}`,
  };
}

/** ⑦ 空白与占位符检测（含必需列缺失；缺个别列仍照常给结论） */
function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')} —— 这些列不参与检查，其余列照常核对`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of BLANK_ROLES) {
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

/** 只有买断档用得到「是否 = 是」这一判断；写成 function 声明，摘付费块时会被一并摘掉。 */
/** 买断项：标了「用于高新指标」却是非常见高新口径的费用类别 */
/** 买断项：按研发项目汇总后的三项结构判断（金额放大 / 折旧占比 / 缺人工） */
/** 买断项：合计行其他费用占比再查一次（与逐行口径一致） */
/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把研发费用辅助账（含表头）贴进来']);

  const { items, totals, missingColumns, header, recognised } = parseTable(text);
  if (recognised === 0) {
    return insufficient(['认不出表头：第一行必须是表头，且要含「研发项目 / 费用类别 / 本年归集金额」这类列名']);
  }
  if (!items.length) {
    return insufficient(['没有明细行：表头下面至少要有一行非「合计」的明细（合计行可留可无）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const f of checkOtherCap(items)) findings.push(f);
  for (const it of items) {
    const one = [checkAmountParts(it), checkNote(it, missingColumns)];
    for (const f of one) if (f) findings.push(f);
    for (const f of checkNegative(it)) findings.push(f);
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
        amount_total: round2(items.reduce((n, it) => n + (normNumber(it.amount) || 0), 0)),
        other_total: round2(items.reduce((n, it) => n + (normNumber(it.other) || 0), 0)),
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
