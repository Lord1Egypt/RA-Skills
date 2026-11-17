#!/usr/bin/env node
/**
 * tower-crane-inspection-check.js —— 塔式起重机备案与检测核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：塔式起重机（塔机）是**建筑起重机械**，总包、租赁单位、监理与安监四方手里都有一本
 * 「塔机台账」。安监来项目上查的第一份资料就是它，而每月必须核一遍的硬项是：检测有效期覆盖、
 * 使用登记与持证、检测结论、重复登记、合计勾稽与字段合法性 ——
 * 核错一项就可能让一台超期塔机继续吊装，出事故是停工整改 + 责任追究级的问题。
 *
 * ⚠️ 本文件是**免费档子集**：只实现下面这六项**表内逐行算术与台账勾稽**：
 *     ① 检测有效期覆盖；② 使用登记证与特种作业人员证覆盖；③ 检测结论核对（不合格 / 复检未闭环）；
 *     ④ 同一设备编号重复登记；⑤ 合计行逐列复核（设备台数 / 检测台数）；⑥ 字段合法性与空缺。
 *    **完整档（买断版）的实现不在这个包里** —— 超期未检仍在用、停用 / 已拆除塔机仍出现在使用运行记录、
 *    无证上岗、顶升加节与附着验收断档、分产权单位与分使用项目的汇总清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现；
 *    每次运行都会在 `checks_not_run` 与输出里把它如实列出来 —— **未执行就是未执行，绝不当成"没问题"**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定这台塔机该不该检、不判定检测报告与证件本身的真伪、不判定现场是否真的停用或拆除、
 *          不读 .xlsx / .pdf 原件、不联网核验备案与证件；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '检测有效期覆盖（核对基准日 ≤ 下次检测日期；超期逐台给出已超期天数）',
  '使用登记证与特种作业人员证覆盖（使用登记证号不得为空；司机 / 信号工都要填，且「证件有效期」要覆盖核对基准日；缺证 / 过期逐台点名）',
  '检测结论核对（结论非「合格」逐台点名：写「不合格」按 P0，只写「复检」视为复检未闭环）',
  '同一设备编号重复登记（一本塔机台账里设备编号唯一）',
  '合计行逐列复核（数量类列：设备台数、检测台数）',
  '字段合法性（关键字段缺失、日期格式非法、数值为负或非法、运行状态与检测结论取值非法）',
];

const CHECKS_WITHHELD = [
  '超期未检仍在用（下次检测日期已过且运行状态=在用；按超期天数降序点名并附已超期天数）',
  '停用 / 已拆除塔机仍出现在使用运行记录（跨表交叉核对：台账运行状态为停用或已拆除，却在「塔机使用运行记录」段里出现，逐条点出记录原文行号）',
  '无证上岗（使用运行记录里的当班司机 / 当班信号工不在「特种作业人员持证名单」里、工种与岗位不符、或证件有效期早于当次作业记录日期）',
  '顶升加节与附着验收记录断档（按设备把顶升次序与验收记录逐次配对，缺哪一次就点哪一次）',
  '分产权单位与分使用项目的汇总清单（按超期天数降序，每组给出可整改动作，并附逐台整改清单）',
];

const OUT_OF_SCOPE = [
  '判定这台塔机该不该检、该做定期检测还是安装（拆卸）告知、该不该办理使用登记（那是检验检测机构、总包与住建主管部门的法定口径，本工具只核台账日期与结论字段是否自洽）',
  '判定检测报告本身的真实性、检测机构资质与检测结论的技术依据是否成立（那是检验检测机构与监管部门的判定权）',
  '判定现场是否真的停了 / 拆了、顶升加节作业是否真的做过（本工具只核台账与使用运行记录 / 验收记录的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验使用登记证 / 特种作业操作证 / 检测报告的真伪，替代项目安全员或安监部门的认定',
];

// 样例：一本**干净**的塔机备案与检测台账 —— 四台塔机、两个在建项目、两家产权单位，
// 检测有效期覆盖核对基准日、备案号与司机 / 信号工证件都在有效期内、检测结论都是「合格」、
// 设备编号不重复、合计行与明细一致；三段跨表材料（使用运行记录 / 持证名单 / 顶升验收）
// 也逐条自洽：没有停用设备在跑、没有无证上岗、顶升次序连续。**全表零命中**。
const SAMPLE_TEXT = [
  '设备编号\t设备名称\t产权单位\t使用项目\t使用登记证号\t检测日期\t检测结论\t下次检测日期\t司机\t信号工\t证件有效期\t运行状态\t设备台数\t检测台数\t核对基准日\t备注',
  'TC-2026-001\t塔式起重机 QTZ80\t华远机械租赁\t云锦花园1号楼项目\t苏建登字2026-0101\t2025-06-20\t合格\t2026-06-20\t赵大勇\t钱小梅\t2027-03-15\t在用\t1\t1\t2026-04-30\t检测合格',
  'TC-2026-002\t塔式起重机 QTZ63\t华远机械租赁\t云锦花园1号楼项目\t苏建登字2026-0102\t2025-07-05\t合格\t2026-07-05\t孙志强\t李桂芳\t2027-05-20\t在用\t1\t1\t2026-04-30\t检测合格',
  'TC-2026-003\t塔式起重机 QTZ125\t恒达设备租赁\t星港商务中心项目\t苏建登字2026-0203\t2025-09-12\t合格\t2026-09-12\t周建华\t吴秀英\t2028-01-10\t在用\t1\t1\t2026-04-30\t检测合格',
  'TC-2026-004\t塔式起重机 QTZ80\t恒达设备租赁\t星港商务中心项目\t苏建登字2026-0204\t2025-05-18\t合格\t2026-05-18\t郑海峰\t王丽娟\t2027-11-30\t在用\t1\t1\t2026-04-30\t检测合格',
  '合计\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t4\t4\t—\t4 台塔机、4 台已检测由明细行加总',
  '--- 塔机使用运行记录 ---',
  '设备编号\t记录日期\t当班司机\t当班信号工',
  'TC-2026-001\t2026-04-01\t赵大勇\t钱小梅',
  'TC-2026-001\t2026-04-02\t赵大勇\t钱小梅',
  'TC-2026-002\t2026-04-01\t孙志强\t李桂芳',
  'TC-2026-003\t2026-04-03\t周建华\t吴秀英',
  'TC-2026-004\t2026-04-04\t郑海峰\t王丽娟',
  '--- 特种作业人员持证名单 ---',
  '人员姓名\t工种\t证件有效期',
  '赵大勇\t塔式起重机司机\t2027-03-15',
  '钱小梅\t信号司索工\t2027-06-30',
  '孙志强\t塔式起重机司机\t2027-05-20',
  '李桂芳\t信号司索工\t2028-02-28',
  '周建华\t塔式起重机司机\t2028-01-10',
  '吴秀英\t信号司索工\t2028-09-30',
  '郑海峰\t塔式起重机司机\t2027-11-30',
  '王丽娟\t信号司索工\t2029-01-31',
  '--- 顶升加节与附着验收记录 ---',
  '设备编号\t顶升次序\t验收日期\t验收结论',
  'TC-2026-001\t1\t2026-03-05\t合格',
  'TC-2026-002\t1\t2026-03-08\t合格',
  'TC-2026-003\t1\t2026-03-20\t合格',
  'TC-2026-003\t2\t2026-04-10\t合格',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'deviceNo', 'deviceName', 'ownerUnit', 'regCertNo', 'inspectDate', 'inspectConclusion',
  'nextInspectDate', 'driver', 'signaler', 'certExpiry', 'runStatus', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['deviceNo', '设备编号'],
  ['deviceName', '设备名称/型号'],
  ['ownerUnit', '产权单位'],
  ['regCertNo', '使用登记证号'],
  ['inspectDate', '检测日期'],
  ['inspectConclusion', '检测结论'],
  ['nextInspectDate', '下次检测日期'],
  ['driver', '司机'],
  ['signaler', '信号工'],
  ['certExpiry', '证件有效期'],
  ['runStatus', '运行状态'],
  ['checkDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['inspectDate', '检测日期'],
  ['nextInspectDate', '下次检测日期'],
  ['certExpiry', '证件有效期'],
  ['checkDate', '核对基准日'],
];

// 数值列（为负 / 无法解析逐格点名）
const NUMBER_FIELDS = [
  ['deviceCount', '设备台数'],
  ['inspectCount', '检测台数'],
];

// 运行状态只认这四个值（建筑起重机械台账口径）
const RUN_STATUSES = ['在用', '停用', '已拆除', '检修'];

// 检测结论只认这四个值：合格 / 不合格 / 复检 / 复检合格
const CONCLUSION_PASS = '合格';
const CONCLUSION_FAIL = '不合格';
const CONCLUSION_RECHECK = '复检';
const CONCLUSION_RECHECK_PASS = '复检合格';
const CONCLUSIONS = [CONCLUSION_PASS, CONCLUSION_FAIL, CONCLUSION_RECHECK, CONCLUSION_RECHECK_PASS];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位有三处，都必须按「更具体 → 更宽泛」排：
//      ① 日期列：下次检测日期 / 检测日期 / 验收日期 / 记录日期 —— 兜底的 '日期' 只能放在最后；
//      ② 岗位列：当班司机 / 当班信号工 必须排在 司机 / 信号工 前面；
//      ③ 结论列：验收结论 排在 检测结论 前面。
const ROLES = {
  deviceNo: ['设备编号', '备案编号', '设备代码', '设备备案号', '塔机编号'],
  deviceName: ['设备名称', '设备型号', '塔机型号', '规格型号', '设备名'],
  regCertNo: ['使用登记证号', '登记证号', '使用登记编号', '产权备案号'],
  nextInspectDate: ['下次检测日期', '下次检测日', '下次检验日期', '下次检测'],
  inspectDate: ['检测日期', '检测日', '检验日期', '上次检测日期'],
  acceptConclusion: ['验收结论', '附着验收结论'],
  inspectConclusion: ['检测结论', '检测评定', '检验结论'],
  liftSeq: ['顶升次序', '顶升次数', '加节次序', '顶升序号', '次序'],
  acceptDate: ['验收日期', '验收日', '附着验收日期'],
  recordDate: ['记录日期', '使用记录日期', '运行日期', '作业日期', '日期'],
  driverOnDuty: ['当班司机', '当班塔机司机'],
  signalerOnDuty: ['当班信号工', '当班司索信号工'],
  driver: ['司机', '塔机司机', '起重司机'],
  signaler: ['信号工', '司索信号工', '信号司索工', '指挥工'],
  personName: ['人员姓名', '姓名', '持证人'],
  jobType: ['工种', '作业类别', '作业种类'],
  certExpiry: ['证件有效期', '证件到期日', '人员证有效期', '有效期至'],
  ownerUnit: ['产权单位', '产权方', '出租单位', '使用单位', '所属单位', '单位'],
  project: ['使用项目', '项目名称', '工程项目', '项目', '工地'],
  runStatus: ['运行状态', '使用状态', '塔机状态', '机械状态'],
  // ⚠️ 检测台数 必须排在 设备台数 前面：否则「设备台数」里的兜底关键词 '台数'
  //    会把「检测台数」抢走（两列落到同一个角色 ⇒ 检测台数整列静默不参与合计复核）。
  inspectCount: ['检测台数', '检测数量', '已检测台数'],
  deviceCount: ['设备台数', '设备数量', '台数'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  deviceNo: '设备编号',
  deviceName: '设备名称/型号',
  ownerUnit: '产权单位',
  project: '使用项目',
  regCertNo: '使用登记证号',
  inspectDate: '检测日期',
  inspectConclusion: '检测结论',
  nextInspectDate: '下次检测日期',
  driver: '司机',
  signaler: '信号工',
  certExpiry: '证件有效期',
  runStatus: '运行状态',
  deviceCount: '设备台数',
  inspectCount: '检测台数',
  checkDate: '核对基准日',
  recordDate: '记录日期',
  driverOnDuty: '当班司机',
  signalerOnDuty: '当班信号工',
  personName: '人员姓名',
  jobType: '工种',
  liftSeq: '顶升次序',
  acceptDate: '验收日期',
  acceptConclusion: '验收结论',
  note: '备注',
};

const SUM_ROLES = ['deviceCount', 'inspectCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这本塔机台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）；'
      + '跨表材料（使用运行记录 / 持证名单 / 顶升验收记录）用 `--- 段名 ---` 单独起段。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「覆盖」，也不说「超期」。',
  };
}

/** 全角 → 半角（Excel 导出的台账里 ０-９ 与 ．－％ 经常是全角） */
function toHalfWidth(raw) {
  return String(raw == null ? '' : raw)
    .replace(/[\uFF01-\uFF5E]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0xFEE0))
    .replace(/\u3000/g, ' ');
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalfWidth(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^[-+]?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace(/[+%]/g, ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = toHalfWidth(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|暂无)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = toHalfWidth(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
  if (/^\d{8}$/.test(s)) s = s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return m[1] + '-' + String(mo).padStart(2, '0') + '-' + String(d).padStart(2, '0');
}

const DAY_MS = 86400000;
function dayNum(iso) {
  const p = iso.split('-').map(Number);
  return Date.UTC(p[0], p[1] - 1, p[2]) / DAY_MS;
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}

const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = toHalfWidth(header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是设备明细：逐台检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const no = String(it.deviceNo == null ? '' : it.deviceNo).trim();
  const name = String(it.deviceName == null ? '' : it.deviceName).trim();
  return TOTAL_LABEL.test(no) || TOTAL_LABEL.test(name);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detail: [], totalRows: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    it.isTotal = isTotalRow(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detail.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

function who(it) {
  const name = String(it.deviceName == null ? '' : it.deviceName).trim();
  const no = String(it.deviceNo == null ? '' : it.deviceNo).trim();
  return `第 ${it.line} 行「${name || no || '未命名塔机'}${name && no ? ' / ' + no : ''}」`;
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

/** 每条结论都带原文依据：行号 + 设备编号 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    device_no: String(it.deviceNo == null ? '' : it.deviceNo).trim(),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 台账里第一个能认出来的核对基准日（逐行没填时兜底；逐行填了就以逐行为准） */
function baseDateOf(items) {
  for (const it of items) {
    const d = normDate(it.checkDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.checkDate) || base;

/* ============================ 免费档检查（六项） ============================ */

function checkInspectionValidity(items, base) {
  // ① 检测有效期覆盖：核对基准日 ≤ 下次检测日期；不覆盖就报超期天数（逐台）
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const next = normDate(it.nextInspectDate);
    const b = baseOf(it, base);
    if (!next || !b) continue;                    // 缺字段 / 格式非法交给第 ⑥ 项点名
    const over = daysBetween(next, b);
    if (over <= 0) continue;
    const status = cell(it, 'runStatus');
    out.push(finding(status === '在用' ? 'P0' : 'P1', '检测超期', it, over,
      `${who(it)}：核对基准日 ${b} 已晚于下次检测日期 ${next}，**已超期 ${over} 天**`
      + `（检测日期 ${cell(it, 'inspectDate') || '(未填)'}，运行状态 ${status || '(未填)'}，`
      + `产权单位 ${cell(it, 'ownerUnit') || '(未填)'}）。`,
      '建筑起重机械检测超期仍在用是停工整改项：先按上面天数把定期检测排进本月计划，'
      + '在用塔机要先停用挂牌；检测合格并把新的下次检测日期填回台账后再恢复吊装。别只改台账日期。'));
  }
  return out;
}

function checkRegistrationAndCertificates(items, base) {
  // ② 使用登记证 + 特种作业人员证：登记证号不得为空；司机 / 信号工都要填，证件有效期要覆盖核对基准日
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const b = baseOf(it, base);

    const no = cell(it, 'regCertNo');
    if (isBlank(no)) {
      out.push(finding('P1', '使用登记证缺失', it, undefined,
        `${who(it)}：使用登记证号是空的 —— 塔机投入使用前要办理使用登记（有的地方是产权备案 + 使用登记两道），`
        + `缺证就说不上"已备案"（产权单位 ${cell(it, 'ownerUnit') || '(未填)'}）。`,
        '去工程所在地住建主管部门的起重机械备案 / 使用登记窗口补办，把证号与办理日期填回台账；'
        + '这一步不做，后面所有"台账齐不齐"的结论都站不住。'));
    }

    const drv = cell(it, 'driver');
    const sig = cell(it, 'signaler');
    const missingPeople = [];
    if (isBlank(drv)) missingPeople.push('司机');
    if (isBlank(sig)) missingPeople.push('信号工');
    if (missingPeople.length) {
      out.push(finding('P1', '特种作业人员证过期或缺失', it, undefined,
        `${who(it)}：${missingPeople.join('、')}这一栏是空的 —— 塔式起重机司机与信号司索工都必须持证上岗，`
        + '人名空着这一项就永远核不了（缺的是人，不是"没问题"）。',
        '把本台塔机当班司机与信号工的姓名逐台补进台账（并与持证名单对得上），再补各自的证件有效期。'));
    }

    const exp = cell(it, 'certExpiry');
    if (isBlank(exp)) {
      out.push(finding('P1', '特种作业人员证过期或缺失', it, undefined,
        `${who(it)}：证件有效期是空的 —— 司机 ${drv || '(未填)'} / 信号工 ${sig || '(未填)'} 的证件到期日没有填，`
        + `无法判断是否覆盖核对基准日 ${b || '(未填)'}。`,
        '「证件有效期」按**本台塔机当班司机与信号工中较早到期的那一个**填写（从严口径）；'
        + '两人各自的到期日在持证名单里逐人维护。证件在别处的也必须在台账里能点到。'));
    } else {
      const d = normDate(exp);
      if (d && b && daysBetween(d, b) > 0) {
        const over = daysBetween(d, b);
        out.push(finding('P0', '特种作业人员证过期或缺失', it, over,
          `${who(it)}：证件有效期 ${d}，早于核对基准日 ${b}，**已过期 ${over} 天**`
          + `（司机 ${drv || '(未填)'} / 信号工 ${sig || '(未填)'}）。`,
          '证件过期期间不得独立操作：先安排复审或换人，复审通过后再把这台塔机交回原持证人；'
          + '台账上的「证件有效期」要跟着持证名单一起更新。'));
      }
    }
  }
  return out;
}

function checkConclusions(items) {
  // ③ 检测结论：非「合格」逐台点名 —— 不合格 P0，只写「复检」视为复检未闭环
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const c = cell(it, 'inspectConclusion');
    if (isBlank(c)) continue;                    // 缺结论交给第 ⑥ 项点名
    const idate = cell(it, 'inspectDate') || '(未填)';
    const ndate = cell(it, 'nextInspectDate') || '(未填)';
    if (c === CONCLUSION_FAIL) {
      out.push(finding('P0', '检测结论不合格', it, undefined,
        `${who(it)}：检测结论写的是「不合格」（检测日期 ${idate}，下次检测日期 ${ndate}）—— `
        + '不合格的塔机不得继续使用；台账上留着这一行、运行状态还写着「'
        + (cell(it, 'runStatus') || '(未填)') + '」更危险。',
        '不合格塔机立即停用挂牌、撤离或整修：整修后重新做检测并拿到合格报告，'
        + '再把结论改成「合格」并更新下次检测日期；整修期间不得安排吊装作业。'));
    } else if (c === CONCLUSION_RECHECK) {
      out.push(finding('P1', '复检未闭环', it, undefined,
        `${who(it)}：检测结论只写了「复检」（检测日期 ${idate}，下次检测日期 ${ndate}）—— `
        + '说明首检没通过、要复检，而**复检结论还没有写回台账**，这一行现在等于没有可用的检测结论。',
        '复检做完后把结论改成「合格」或「复检合格」，并把复检报告归档；'
        + '复检未出结论前该塔机不得投入吊装作业，这一条要写进整改单闭环。'));
    }
  }
  return out;
}

function checkDuplicateDevice(items) {
  // ④ 同一设备编号重复登记：一本台账里设备编号唯一
  const out = [];
  const first = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'deviceNo');
    if (!no) continue;
    if (first.has(no)) {
      out.push(finding('P0', '设备重复登记', it, undefined,
        `${who(it)}：设备编号「${no}」在第 ${first.get(no)} 行已经出现过 —— 同一台塔机重复登记。`
        + `本次这行名称是「${cell(it, 'deviceName') || '(未填)'}」，产权单位「${cell(it, 'ownerUnit') || '(未填)'}」。`,
        '一台塔机在一本台账里只应有一行：重复登记会让两个检测周期、两套证件各算一套，'
        + '极容易出现"其中一行超期了却没人发现"。合并成一行，历史检测记录写进备注。'));
    } else {
      first.set(no, it.line);
    }
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：数量类列（设备台数、检测台数）的合计行必须等于明细行加总
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字；请核对是否把单位（台）写进了单元格里，或写成了「4台」这种带文字的形态。'));
        continue;
      }
      const actual = round2(detail.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但上面 ${detail.length} 行明细逐行加总是 ${actual}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须等于明细行逐列加总：先看有没有明细行被隐藏 / 筛选掉了，'
        + '再看是不是把停用、已拆除的塔机漏统计或少统计了。'
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 空白 / 占位符 / 日期格式 / 数值为负 / 运行状态与检测结论取值非法
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如下次检测日期空着就判不了检测覆盖，司机空着就判不了持证）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-04-30 / 2026/4/30 / 2026年4月30日 / 20260430 这几种形态）。',
          '把日期改成 2026-04-30 这种形态再跑；日期认不出来时本工具不会拿它去算超期天数。'));
      }
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '台数必须是纯数字（如 1）；写成「一台」「壹」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 台账里的台数出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      }
    }

    const status = cell(it, 'runStatus');
    if (status && RUN_STATUSES.indexOf(status) < 0) {
      out.push(finding('P1', '运行状态非法', it, undefined,
        `${who(it)}：运行状态写的是「${status}」，不在允许的四个值里（${RUN_STATUSES.join(' / ')}）。`,
        '运行状态会直接决定"超期未检仍在用"与"停用塔机还在跑"这两类结论：'
        + '按实际情况改成 在用 / 停用 / 已拆除 / 检修 之一（拆掉的写「已拆除」，别写「拆除完成」「已拆」）。'));
    }

    const concl = cell(it, 'inspectConclusion');
    if (concl && CONCLUSIONS.indexOf(concl) < 0) {
      out.push(finding('P1', '检测结论非法', it, undefined,
        `${who(it)}：检测结论写的是「${concl}」，不在允许的四个值里（${CONCLUSIONS.join(' / ')}）。`,
        '检测结论必须是这四个值之一：合格 / 不合格 / 复检 / 复检合格。'
        + '写成「基本合格」「合格（附条件）」这类自由文本，本工具无法判断它算不算通过。'));
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function sourceLabel() {
  return '一本含表头的塔机台账（设备编号 / 设备名称 / 产权单位 / 使用登记证号 / 检测日期 / 检测结论 / '
    + '下次检测日期 / 司机 / 信号工 / 证件有效期 / 运行状态 / 核对基准日）';
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：' + sourceLabel()]);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：' + sourceLabel()]);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的塔机台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行塔机明细（现在只有表头或只有合计行，没有可核对的塔机）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];

  for (const f of checkInspectionValidity(t.items, base)) findings.push(f);
  for (const f of checkRegistrationAndCertificates(t.items, base)) findings.push(f);
  for (const f of checkConclusions(t.items)) findings.push(f);
  for (const f of checkDuplicateDevice(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档追加的那五项检查一项都不执行，这里如实记下来（只记「没做」，绝不伪造结论）。
  // 材料里即使带了 `--- 塔机使用运行记录 ---` 这类跨表段，本版本也只做表内核对、不会去交叉核对。
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const deviceTotal = t.totals.deviceCount;
  const inspectTotal = t.totals.inspectCount;
  const overdueRows = findings.filter((f) => f.category === '检测超期');
  const overdueMax = overdueRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      device_count_total: deviceTotal,
      inspect_count_total: inspectTotal,
      overdue_devices: overdueRows.length,
      overdue_days_max: overdueMax,
      check_date: base,
      basis: '核对基准日（表内「核对基准日」，逐行为准、缺行用表内第一个能认出的）≤ 下次检测日期才算检测有效期被覆盖；'
        + '使用登记证号不得为空，司机 / 信号工都必须填，且「证件有效期」（本台塔机当班司机与信号工中较早到期的那一个）'
        + '要覆盖核对基准日；检测结论只认 合格 / 不合格 / 复检 / 复检合格（不合格按 P0，只写「复检」视为复检未闭环）；'
        + '同一设备编号在一本台账里唯一；合计行（设备台数、检测台数）必须等于明细行逐列加总；'
        + '运行状态只认 在用 / 停用 / 已拆除 / 检修 四个值。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本塔机台账按上面写明的口径算得对、'
      + '备案与检测日期和检测结论字段都自洽**，不代表这台塔机的检测结论本身合规、'
      + '不代表现场隐患已经整改闭环、也不代表使用登记证与特种作业操作证的真伪已经核验 —— 那些不在本工具范围内。'
      + '（注意：完整档追加的五项检查本次没有执行，结果里 checks_not_run 已如实列出。）';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    device_count_total: deviceTotal,
    inspect_count_total: inspectTotal,
    check_date: base,
  };
  result.scope = scope;

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
