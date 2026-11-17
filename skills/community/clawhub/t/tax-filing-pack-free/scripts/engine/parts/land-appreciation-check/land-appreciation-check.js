#!/usr/bin/env node
/**
 * land-appreciation-check.js —— 土地增值税预缴与清算核对（免费档 / 完整档共用源码；确定性、纯 Node 标准库）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**。
 *
 * 真实痛点：**房地产/建筑企业的项目会计，每次预缴与清算都要做这张表**，而它是串行的六步算术：
 *   ① 扣除项目合计 = 土地成本 + 开发成本 + 开发费用 + 税金
 *   ② 增值额 = 转让收入 − 扣除项目合计
 *   ③ 增值率 = 增值额 ÷ 扣除项目合计
 *   ④ 应纳土地增值税 = 增值额 × 档位税率 − 扣除项目合计 × 速算扣除系数
 *   ⑤ 应预缴税额 = 预收收入 × 预征率
 *   ⑥ 清算应补（退） = 应纳土地增值税 − 已预缴税额
 * 扣除项目漏计一项、增值率跨档时档位看错行（30% / 40% / 50% / 60% 与对应速算扣除系数），
 * 差额就是几十上百万 —— 这也是税企争议最集中的一张表。
 *
 * 与已有能力的区别：`property-tax-land-use-check` 核的是城镇土地使用税与房产税的计税依据；
 * `cit-prepay-check` 核的是企业所得税季度预缴。本能力核的是**土地增值税**这一条独立的
 * 预缴/清算链条（扣除项目 → 增值额 → 增值率 → 档位应纳税额 → 预缴 → 应补退）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查税率文库、不套用任何地区政策（**档位税率、速算扣除系数、预征率
 * 一律取自你表里的数或入参**）、不调用大模型、不给税务意见、不做清算筹划；材料不足不给结论。
 *
 * ⚠️ 付费项用**形态 B**：先在 run() 里声明开关常量 paid（读入参上的 full / credit / token
 *    三个标记，任一为真即视为完整档），再把付费检查整体包进以 paid 为条件的块；
 *    **不要**再留「完整档才执行的检查」那类 MARKER —— 两个形态同时存在时
 *    `strip_free_engine` 会走形态 A 把免费检查也整块删掉（第 236 轮踩过）。
 */
'use strict';

const CHECKS_GIVEN = [
  '扣除项目合计勾稽（土地成本 + 开发成本 + 开发费用 + 税金）',
  '增值额勾稽（转让收入 − 扣除项目合计）',
  '增值率勾稽（增值额 ÷ 扣除项目合计）',
  '应纳土地增值税勾稽（增值额 × 档位税率 − 扣除项目合计 × 速算扣除系数）',
  '应预缴税额勾稽（预收收入 × 预征率）',
  '已预缴与应预缴税额差异检测',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复项目检测',
  '关键字段空缺与占位符检测',
  '按口径不应为负的列出现负值检测',
];

const CHECKS_WITHHELD = [
  '增值率档位与表内档位税率/速算扣除系数不匹配判定',
  '扣除项目口径与表内多数项目不一致判定',
  '预征率与约定（或表内多数项目）不符判定',
  '清算单位划分重复或遗漏判定',
  '已预缴与清算应纳土地增值税比较（应补/可退金额复算）判定',
  '同一项目重复清算判定',
  '按金额排序的处理清单（每条带行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断某项支出能不能计入扣除项目（那是税前扣除凭证与项目归属的认定）',
  '套用某个地区的预征率、普通住宅优惠或清算单位划分细则'
    + '（预征率、档位税率、速算扣除系数一律按你表里的数或入参给，本工具不写死任何地方政策）',
  '给出税务意见或做清算筹划（本工具只做口径一致的算术与表内一致性判定）',
  '读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '项目\t清算单位\t清算状态\t转让收入\t预收收入\t预征率\t应预缴税额\t已预缴税额\t土地成本\t开发成本\t开发费用\t税金\t扣除项目合计\t增值额\t增值率\t档位税率\t速算扣除系数\t应纳土地增值税\t清算应补退税额',
  'A花园一期\t住宅\t已清算\t22000000.00\t20000000.00\t1.5%\t300000.00\t300000.00\t5000000.00\t3000000.00\t800000.00\t1200000.00\t10000000.00\t12000000.00\t120.00%\t50%\t15%\t4500000.00\t4200000.00',
  'A花园二期\t商业\t已清算\t12000000.00\t12000000.00\t1.5%\t180000.00\t180000.00\t4000000.00\t2000000.00\t600000.00\t900000.00\t7500000.00\t4500000.00\t60.00%\t40%\t5%\t1425000.00\t1245000.00',
  'B公馆\t综合\t清算中\t6000000.00\t6000000.00\t1.5%\t90000.00\t90000.00\t3000000.00\t1000000.00\t400000.00\t600000.00\t5000000.00\t1000000.00\t20.00%\t30%\t0%\t300000.00\t210000.00',
  '合计\t\t\t40000000.00\t38000000.00\t\t570000.00\t570000.00\t12000000.00\t6000000.00\t1800000.00\t2700000.00\t22500000.00\t17500000.00\t\t\t\t6225000.00\t5655000.00',
].join('\n');

const TOL = 0.01;        // 金额容差（元）
const PCT_TOL = 0.02;    // 百分数容差（百分点；增值率保留两位小数）

// ⚠️ 角色顺序 = 匹配优先级，**更具体的词必须排在更宽泛的前面**
//    （见 tools/header_map_check.py：顺序错会让一列被另一列抢走，而且不报错、只是静默算错）：
//    · 「扣除项目合计」必须排在「项目」之前，否则被 party 的「项目」抢走；
//    · 「已预缴税额」必须排在「应预缴税额」之前（后者含子串「预缴税额」）；
//    · 「速算扣除系数」不能被任何「扣除」别名抢走（所以 deduct 里不写裸「扣除」）。
const ROLES = {
  unit: ['清算单位', '核算单位', '单位名称'],
  status: ['清算状态', '清算进度', '状态'],
  deduct: ['扣除项目合计', '扣除项目金额', '扣除合计'],
  quick: ['速算扣除系数', '速算扣除率', '速算扣除'],
  rate: ['档位税率', '适用税率', '税率'],
  preRate: ['预征率', '预征比例'],
  prePaid: ['已预缴税额', '已预缴', '已缴税额', '已交税额'],
  preDue: ['应预缴税额', '应预缴', '预缴税额'],
  settle: ['清算应补退税额', '清算应补退', '应补退税额', '应补退税'],
  payable: ['应纳土地增值税', '应纳增值税', '应纳税额'],
  income: ['转让收入', '销售收入', '转让房地产收入'],
  pre: ['预收收入', '预售收入', '预收款'],
  appr: ['增值额'],
  apprRate: ['增值率'],
  land: ['土地成本', '土地价款', '取得土地使用权支付的金额'],
  dev: ['开发成本', '房地产开发成本'],
  devFee: ['开发费用', '开发间接费用'],
  tax: ['税金', '转让环节税金'],
  party: ['项目名称', '项目', '工程名称'],
};

const LABELS = {
  party: '项目', unit: '清算单位', status: '清算状态', income: '转让收入', pre: '预收收入',
  preRate: '预征率', preDue: '应预缴税额', prePaid: '已预缴税额', land: '土地成本',
  dev: '开发成本', devFee: '开发费用', tax: '税金', deduct: '扣除项目合计', appr: '增值额',
  apprRate: '增值率', rate: '档位税率', quick: '速算扣除系数', payable: '应纳土地增值税',
  settle: '清算应补退税额',
};

const REQUIRED = ['party', 'unit', 'status', 'income', 'pre', 'preRate', 'preDue', 'prePaid',
  'land', 'dev', 'devFee', 'tax', 'deduct', 'appr', 'apprRate', 'rate', 'quick', 'payable', 'settle'];
const SUM_ROLES = ['income', 'pre', 'preDue', 'prePaid', 'land', 'dev', 'devFee', 'tax',
  'deduct', 'appr', 'payable', 'settle'];
// 按口径不会为负的列（增值额/增值率可以为负：项目亏损时增值额本就是负的，不在这里判）
const NON_NEGATIVE = ['income', 'pre', 'preDue', 'prePaid', 'land', 'dev', 'devFee', 'tax', 'deduct'];

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

const round2 = (n) => Math.round(n * 100) / 100;
const round4 = (n) => Math.round(n * 10000) / 10000;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const unmapped = cols.filter((c) => !c.role).map((c) => c.header);
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
  return { cols, items, totals, unmapped };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `项目「${it.byRole.party || '(未命名)'}」`;

function checkDeduct(it) {
  const land = num(it, 'land');
  const dev = num(it, 'dev');
  const fee = num(it, 'devFee');
  const tax = num(it, 'tax');
  const stated = num(it, 'deduct');
  if (land === null || dev === null || fee === null || tax === null || stated === null) return null;
  const expect = round2(land + dev + fee + tax);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '扣除项目合计与复算不符', line: it.line,
    amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}的扣除项目合计是 ${stated.toFixed(2)}，按 土地成本 ${land.toFixed(2)}`
      + ` + 开发成本 ${dev.toFixed(2)} + 开发费用 ${fee.toFixed(2)} + 税金 ${tax.toFixed(2)}`
      + ` = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}。`,
    advice: '扣除项目要逐项加齐（土地成本 / 开发成本 / 开发费用 / 税金四类）；'
      + '漏一项就少扣一大笔，增值额与税额会跟着全错。',
  };
}

function checkAppr(it) {
  const income = num(it, 'income');
  const deduct = num(it, 'deduct');
  const stated = num(it, 'appr');
  if (income === null || deduct === null || stated === null) return null;
  const expect = round2(income - deduct);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '增值额与复算不符', line: it.line,
    amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}的增值额是 ${stated.toFixed(2)}，按 转让收入 ${income.toFixed(2)}`
      + ` − 扣除项目合计 ${deduct.toFixed(2)} = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}。`,
    advice: '增值额 = 转让收入 − 扣除项目合计（两者必须是同一口径的金额）；'
      + '收入要含货币、实物与其他经济利益，不能只填开票金额。',
  };
}

function checkApprRate(it) {
  const deduct = num(it, 'deduct');
  const appr = num(it, 'appr');
  const stated = num(it, 'apprRate');
  if (deduct === null || appr === null || stated === null) return null;
  if (Math.abs(deduct) <= 1e-9) return null;
  const expect = round2(appr / deduct * 100);
  if (Math.abs(expect - stated) <= PCT_TOL) return null;
  return {
    level: 'P1', category: '增值率与复算不符', line: it.line,
    amount: 0,
    message: `${who(it)}的增值率是 ${stated}%，按 增值额 ${appr.toFixed(2)}`
      + ` ÷ 扣除项目合计 ${deduct.toFixed(2)} = ${expect}%。`,
    advice: '增值率的分母是扣除项目合计（不是转让收入）；分母用错会直接跨档，'
      + '把本该 30% 的项目算进 40% 的档。',
  };
}

function checkPayable(it) {
  const appr = num(it, 'appr');
  const deduct = num(it, 'deduct');
  const rate = num(it, 'rate');
  const quick = num(it, 'quick');
  const stated = num(it, 'payable');
  if (appr === null || deduct === null || rate === null || quick === null || stated === null) return null;
  const expect = round2(appr * rate / 100 - deduct * quick / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应纳土地增值税与复算不符', line: it.line,
    amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}的应纳土地增值税是 ${stated.toFixed(2)}，按 增值额 ${appr.toFixed(2)}`
      + ` × ${rate}% − 扣除项目合计 ${deduct.toFixed(2)} × ${quick}% = ${expect.toFixed(2)}，`
      + `应为 ${expect.toFixed(2)}。`,
    advice: '档位税率与速算扣除系数是**成对**用的：速算扣除系数乘的也是扣除项目合计，'
      + '不是增值额；乘错基数是这里最常见的一种错。',
  };
}

function checkPreDue(it) {
  const pre = num(it, 'pre');
  const rate = num(it, 'preRate');
  const stated = num(it, 'preDue');
  if (pre === null || rate === null || stated === null) return null;
  const expect = round2(pre * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应预缴税额与复算不符', line: it.line,
    amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}的应预缴税额是 ${stated.toFixed(2)}，按 预收收入 ${pre.toFixed(2)}`
      + ` × 预征率 ${rate}% = ${expect.toFixed(2)}，应为 ${expect.toFixed(2)}。`,
    advice: '预缴口径是「预收收入 × 预征率」；预收收入按实际收到（含定金、首付、按揭到账）'
      + '确认，不能拿全口径的转让收入去乘预征率。',
  };
}

function checkPreDiff(it) {
  const prePaid = num(it, 'prePaid');
  const preDue = num(it, 'preDue');
  if (prePaid === null || preDue === null) return null;
  const diff = round2(prePaid - preDue);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P1', category: '已预缴与应预缴税额不一致', line: it.line,
    amount: Math.abs(diff),
    message: `${who(it)}的已预缴税额是 ${prePaid.toFixed(2)}，按 预收收入 × 预征率 应为 `
      + `${preDue.toFixed(2)}，${diff > 0 ? '多预缴' : '少预缴'} ${Math.abs(diff).toFixed(2)}。`,
    advice: '预缴是逐期申报缴的，逐期对不上通常出在某一期预收收入漏报、预征率用错'
      + '或申报表串期；先把差异落到具体期次，再谈清算时的应补退。',
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
        amount: Math.abs(round2(stated - sum)),
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 `
          + `${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了某个项目/清算单位，要么合计行没跟着更新；'
          + '清算申报表里的合计数要和明细逐列对得上。',
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
        level: 'P1', category: '同一项目出现多行', line: it.line, amount: 0,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '一个项目分几个清算单位分行列示是正常的；但同一个项目名重复出现时，'
          + '收入与扣除项目很容易被算两遍 —— 先确认是分行还是重复。',
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
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line, amount: 0,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这条链就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkNegative(items) {
  const out = [];
  for (const it of items) {
    for (const role of NON_NEGATIVE) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '按口径不应为负的列出现负值', line: it.line,
          amount: Math.abs(v),
          message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}。`,
          advice: '收入、成本、费用、税金、已预缴这些列按口径不会为负：为负多半是方向填反'
            + '或粘贴时带了减号。（增值额为负是正常的亏损项目，本工具不据此报错。）',
        });
      }
    }
  }
  return out;
}

/* ==================================================================== *
 * 以下函数只在完整档（买断版）里执行；免费包里会被 strip_free_engine 整块摘掉。
 * 它们全部只做「表内一致性 + 算术」判定，不套用任何地区政策。
 * ==================================================================== */

/** 增值率档位与表内档位税率/速算扣除系数不匹配 */
/** 扣除项目口径：同一张表里开发费用占「土地成本 + 开发成本」的比率应当一致（以表内多数口径为基准） */
/** 预征率与约定不符：约定从入参取（agreedPreRate）；没给就用表内多数项目的预征率当基准 */
/** 清算单位划分：（项目 + 清算单位）重复列示 = 重复；同一项目下有的行没写清算单位 = 遗漏 */
/** 同一项目重复清算：项目名归一后指向同一清算单位、且两行都标了"已清算" */
/** 已预缴 vs 清算应纳：表内「清算应补退税额」列与复算不符即报 */
/** 逐行算「应纳 − 已预缴」，供处理清单用（本身不进 findings） */
/** 处理清单：所有结论 + 每个清算单位的应补/可退金额，按金额从大到小排（同金额按行号） */
function run(payload) {
  const text = String((payload && (payload.text || payload.content)) || '');
  if (!text.trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的土地增值税预缴与清算表（要能认出「项目」「清算单位」「清算状态」「转让收入」'
      + '「预收收入」「预征率」「应预缴税额」「已预缴税额」「土地成本」「开发成本」「开发费用」'
      + '「税金」「扣除项目合计」「增值额」「增值率」「档位税率」「速算扣除系数」'
      + '「应纳土地增值税」「清算应补退税额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从清算底稿或申报表导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个项目/清算单位的明细行']);

  const agreedPreRate = (() => {
    if (!payload) return null;
    const cands = [payload.agreedPreRate, payload.agreed_pre_rate, payload.pre_rate];
    for (const c of cands) {
      const n = typeof c === 'number' ? c : normNumber(c);
      if (n !== null && Number.isFinite(n)) return n;
    }
    return null;
  })();

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkDeduct(it); if (a) findings.push(a);
    const b = checkAppr(it); if (b) findings.push(b);
    const c = checkApprRate(it); if (c) findings.push(c);
    const d = checkPayable(it); if (d) findings.push(d);
    const e = checkPreDue(it); if (e) findings.push(e);
    const f = checkPreDiff(it); if (f) findings.push(f);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegative(t.items)) findings.push(f);

  let checksRun = CHECKS_GIVEN.length;
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      income_total: sumOf('income'),
      pre_total: sumOf('pre'),
      prepay_due_total: sumOf('preDue'),
      prepaid_total: sumOf('prePaid'),
      deduct_total: sumOf('deduct'),
      appr_total: sumOf('appr'),
      payable_total: sumOf('payable'),
      settlement_total: sumOf('settle'),
      basis: '扣除项目合计 = 土地成本 + 开发成本 + 开发费用 + 税金；增值额 = 转让收入 − 扣除项目合计；'
        + '增值率 = 增值额 ÷ 扣除项目合计；应纳土地增值税 = 增值额 × 档位税率 − 扣除项目合计 × 速算扣除系数；'
        + '应预缴税额 = 预收收入 × 预征率；清算应补退 = 应纳土地增值税 − 已预缴税额。'
        + '（档位税率、速算扣除系数、预征率一律取自你表里的值或入参，本工具不写死任何地方政策。）',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      rows: t.items.length,
      checks_run: checksRun,
      checks_not_run: notRun,
      paid_in_total: sumOf('prePaid'),
      payable_total: sumOf('payable'),
      outstanding_total: round2(sumOf('payable') - sumOf('prePaid')),
    },
  };
  if (t.unmapped && t.unmapped.length) result.unmapped_columns = t.unmapped;
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表扣除项目一定被税务机关认可，也不代表适用普通住宅优惠等特殊口径 —— 那些不在本工具范围内。';
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, round4, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, REQUIRED, NON_NEGATIVE,
};
