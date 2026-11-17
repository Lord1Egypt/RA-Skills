#!/usr/bin/env node
/**
 * school-bus-safety-check.js —— 校车运行与安全检查记录核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：有校车的学校与校车服务公司，**每月**必须把这一摞出车检查记录核一遍（校车安全管理条例要求）：
 *   ① 校车要**每半年检验一次**、**每日出车前检查**（制动 / 灯光 / 轮胎 / 灭火器 / 逃生锤），
 *      记录必须能证明「哪台车哪一天检了、检了几项」
 *   ② 驾驶员要有**校车驾驶资格**与**无犯罪记录 / 体检证明**，资格过期当天就不能再出车
 *   ③ 随车照管人员要**每趟交接点名**；超载、超速、非固定线路运行都是**直接处罚项**
 *   ④ 一旦出事，学校与校车服务公司**都要担责** —— 安全管理员手里的记录必须经得起事后逐条复核
 * 本引擎只做**表内字面与算术的确定性核对**：每条结论都带原文行号与出处，材料不足一律不给结论。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现下面这六项**逐行 / 逐列核对**；
 *    **完整档（买断）的实现不在这个包里** —— 超载点名（按超载人数降序）、照管人员交接缺失、
 *    非固定线路运行、车辆检验有效期覆盖、分车辆 / 分驾驶员 / 分照管人员汇总清单与
 *    consolidated_actions 都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *    本版本**只做**出车检查记录、驾驶员资格、照管交接以外的表内核对，
 *    **不做**安全主体责任与"记录是否真实发生"的判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定学校与校车公司的主体责任与行政处罚、不判定记录是否**真实发生**（不去现场、不查 GPS/视频）、
 *          不判定驾驶员实际驾驶能力与照管人员是否培训合格、不读 .xlsx/.pdf 扫描件、
 *          不联网核验驾驶证 / 校车标牌 / 检验报告真伪、不替代交警或教育主管部门的检查结论；
 *          材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '出车检查记录覆盖（按 车辆 × 出车日期 核对：以本表出现的全部出车日期为应检日历，逐台车点名缺哪一天）',
  '检查项目齐全性（检查项目数 ≥ 规定检查项目数，不足即给出差额）',
  '驾驶员资格有效期（出车日期 ≤ 驾驶证到期日 / 校车驾驶资格到期日 / 体检证明到期日，超期给出天数）',
  '同一车辆同一日期重复登记（按 车辆牌照 + 出车日期 判重，点名重复的行）',
  '合计行逐列复核（合计行的 趟次 / 核载人数 / 实际乘坐人数 / 里程 / 油耗 与明细逐列比对）',
  '空白与格式检测（关键字段空白或占位符、日期与时间格式、数值为负或无法解析、检查结果状态值非法、出车时间晚于收车时间）',
];

const CHECKS_WITHHELD = [
  '超载（实际乘坐人数 > 核载人数 ⇒ 点名车辆 / 日期 / 超载人数，overloads 按超载人数降序）',
  '照管人员交接缺失（有趟次记录但照管人员为空或照管交接记录缺失 ⇒ 逐行点名）',
  '非固定线路运行（是否固定线路=否 且缺线路审批记录 ⇒ 逐行点名）',
  '车辆检验有效期覆盖（出车日期 ≤ 半年检验有效期至，超期给出天数）',
  '分车辆 × 分驾驶员 / 分照管人员汇总清单与 consolidated_actions（按超载 / 超期 / 缺检次数排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定学校与校车服务公司的安全主体责任、行政处罚与事故责任（那是教育、交通运输与公安交管部门的认定权，本工具不做）',
  '判定出车检查与交接点名是否**真实发生**（本工具只核记录的字面完整与算术勾稽，不去现场、不查 GPS 轨迹与随车视频）',
  '判定驾驶员是否具备实际驾驶能力、随车照管人员是否培训合格（那是资格认定与年审的职责）',
  '读取 .xlsx / .pdf 扫描件、联网核验驾驶证 / 校车标牌 / 检验报告真伪、替代交警或教育主管部门的检查结论',
];

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'plate', 'vin', 'ratedSeats', 'actualRiders', 'tripDate', 'departTime', 'returnTime',
  'checkItems', 'requiredItems', 'checkResult', 'driverName', 'licenseExpiry',
  'busQualExpiry', 'medicalExpiry', 'attendant', 'trips', 'mileage', 'fixedRoute',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
// ⚠️ 故意**不含** attendant / handoverRecord / routeApproval / inspectionExpiry ——
//    那几列的空缺属于完整档的追加口径，免费档不许替它出结论。
const REQUIRED_FIELDS = [
  ['plate', '车辆牌照'],
  ['vin', '车辆识别代号'],
  ['tripDate', '出车日期'],
  ['departTime', '出车时间'],
  ['returnTime', '收车时间'],
  ['checkItems', '检查项目数'],
  ['requiredItems', '规定检查项目数'],
  ['checkResult', '检查结果'],
  ['driverName', '驾驶员姓名'],
  ['ratedSeats', '核载人数'],
  ['actualRiders', '实际乘坐人数'],
  ['trips', '趟次'],
  ['mileage', '里程(km)'],
];

// 数量列（用于「为负 / 无法解析」判定，也是合计行要逐列复核的列）
const NUMBER_FIELDS = [
  ['ratedSeats', '核载人数'],
  ['actualRiders', '实际乘坐人数'],
  ['checkItems', '检查项目数'],
  ['requiredItems', '规定检查项目数'],
  ['trips', '趟次'],
  ['mileage', '里程(km)'],
  ['fuel', '油耗(L)'],
];

const DATE_FIELDS = [
  ['tripDate', '出车日期'],
  ['licenseExpiry', '驾驶证到期日'],
  ['busQualExpiry', '校车驾驶资格到期日'],
  ['medicalExpiry', '体检证明到期日'],
];

const TIME_FIELDS = [
  ['departTime', '出车时间'],
  ['returnTime', '收车时间'],
];

// 检查结果的允许取值（状态值非法检测的口径，写在结论里，可被第三方复算）
const ALLOWED_RESULTS = ['合格', '不合格', '正常', '异常', '通过', '不通过', '有隐患'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过多次，见 tools/header_map_check.py）。
//    这里最要命的一组是日期 / 时间与三种到期日：
//      出车日期 / 出车时间 / 收车时间 / 驾驶证到期日 / 校车驾驶资格到期日 / 体检证明到期日
//    ——「出车日」类前缀与「驾驶证」类前缀必须各自排在自己的泛化别名之前。
const ROLES = {
  plate: ['车辆牌照', '车牌号码', '车牌号', '号牌号码', '车牌'],
  vin: ['车辆识别代号', '车辆识别码', '车架号', 'VIN'],
  ratedSeats: ['核载人数', '核定载客人数', '核定载客', '核定人数', '核载'],
  actualRiders: ['实际乘坐人数', '实际载客人数', '实际载客', '实载人数', '乘坐人数', '实际人数'],
  tripDate: ['出车日期', '行车日期', '运行日期', '出车日'],
  departTime: ['出车时间', '发车时间', '始发时间', '出车时刻'],
  returnTime: ['收车时间', '回场时间', '收班时间', '归场时间', '收车时刻'],
  requiredItems: ['规定检查项目数', '规定项目数', '应检项目数', '规定检查项目', '规定项数'],
  checkItems: ['检查项目数', '实检项目数', '已检项目数', '检查项数', '检查项目'],
  checkResult: ['检查结果', '检查结论', '检查情况', '检查状态', '检查评定'],
  driverName: ['驾驶员姓名', '司机姓名', '驾驶员', '司机'],
  licenseExpiry: ['驾驶证到期日', '驾驶证有效期至', '驾驶证有效期', '驾驶证'],
  busQualExpiry: ['校车驾驶资格到期日', '校车驾驶资格有效期至', '校车驾驶资格有效期', '校车驾驶资格', '驾驶资格到期日', '驾驶资格'],
  medicalExpiry: ['体检证明到期日', '体检证明有效期至', '体检证明有效期', '体检证明', '健康证明到期日', '体检合格证'],
  handoverRecord: ['照管交接记录', '交接记录', '交接签字', '交接签名', '交接单'],
  attendant: ['照管人员', '随车照管人员', '随车照管', '照管员', '跟车人员'],
  trips: ['趟次', '运行趟次', '趟数', '班次'],
  mileage: ['里程km', '行驶里程', '里程', '公里数'],
  fuel: ['油耗L', '百公里油耗', '油耗', '燃油消耗', '用油量'],
  fixedRoute: ['是否固定线路', '固定线路', '是否固定班线', '固定班线'],
  inspectionExpiry: ['半年检验有效期至', '检验有效期至', '半年检验有效期', '检验有效期', '年检有效期至', '检验合格有效期'],
  routeApproval: ['线路审批记录', '线路审批', '审批记录', '线路批复', '线路许可'],
};

const LABELS = {
  plate: '车辆牌照',
  vin: '车辆识别代号',
  ratedSeats: '核载人数',
  actualRiders: '实际乘坐人数',
  tripDate: '出车日期',
  departTime: '出车时间',
  returnTime: '收车时间',
  requiredItems: '规定检查项目数',
  checkItems: '检查项目数',
  checkResult: '检查结果',
  driverName: '驾驶员姓名',
  licenseExpiry: '驾驶证到期日',
  busQualExpiry: '校车驾驶资格到期日',
  medicalExpiry: '体检证明到期日',
  handoverRecord: '照管交接记录',
  attendant: '照管人员',
  trips: '趟次',
  mileage: '里程(km)',
  fuel: '油耗(L)',
  fixedRoute: '是否固定线路',
  inspectionExpiry: '半年检验有效期至',
  routeApproval: '线路审批记录',
};

// 合计行要逐列复核的数量列
const SUM_ROLES = ['ratedSeats', 'actualRiders', 'trips', 'mileage', 'fuel'];

/* ============================ 样例 ============================ */
// 一张**干净**的校车运行与安全检查记录：两台车 × 三个出车日，出车检查记录一天不缺、
// 检查项目数不少于规定项数、三种证件都在有效期内、同一车辆同一日期只登记一次、
// 没有超载、照管人员与交接记录齐全、全部固定线路、半年检验有效期覆盖全部出车日、合计行逐列对得上。
const SAMPLE_HEAD = [
  '车辆牌照', '车辆识别代号（VIN）', '核载人数', '实际乘坐人数', '出车日期', '出车时间', '收车时间',
  '检查项目数', '规定检查项目数', '检查结果', '驾驶员姓名', '驾驶证到期日', '校车驾驶资格到期日',
  '体检证明到期日', '照管人员', '趟次', '里程(km)', '油耗(L)', '是否固定线路', '半年检验有效期至',
  '线路审批记录', '照管交接记录',
].join('\t');

const SAMPLE_DETAILS = [
  ['苏A7K2Q9', 'LVIN2026XXXXX0001', '19', '16', '2026-03-02', '06:40', '17:20', '10', '10', '合格', '张校安', '2027-08-31', '2027-05-31', '2026-12-31', '李照容', '2', '86.5', '12.40', '是', '2026-06-30', '', '已交接'],
  ['苏A7K2Q9', 'LVIN2026XXXXX0001', '19', '18', '2026-03-03', '06:35', '17:35', '10', '10', '合格', '张校安', '2027-08-31', '2027-05-31', '2026-12-31', '李照容', '2', '88.0', '12.80', '是', '2026-06-30', '', '已交接'],
  ['苏A7K2Q9', 'LVIN2026XXXXX0001', '19', '15', '2026-03-04', '06:45', '17:15', '11', '10', '合格', '张校安', '2027-08-31', '2027-05-31', '2026-12-31', '李照容', '2', '84.0', '12.10', '是', '2026-06-30', '', '已交接'],
  ['苏B3M8T5', 'LVIN2026XXXXX0002', '41', '35', '2026-03-02', '06:20', '17:50', '10', '10', '合格', '王行安', '2027-03-31', '2026-11-30', '2027-01-31', '赵随车', '2', '152.0', '22.30', '是', '2026-06-30', '', '已交接'],
  ['苏B3M8T5', 'LVIN2026XXXXX0002', '41', '38', '2026-03-03', '06:25', '18:00', '10', '10', '合格', '王行安', '2027-03-31', '2026-11-30', '2027-01-31', '赵随车', '2', '149.5', '21.90', '是', '2026-06-30', '', '已交接'],
  ['苏B3M8T5', 'LVIN2026XXXXX0002', '41', '40', '2026-03-04', '06:30', '17:55', '10', '10', '合格', '王行安', '2027-03-31', '2026-11-30', '2027-01-31', '赵随车', '2', '155.0', '22.60', '是', '2026-06-30', '', '已交接'],
].map((cells) => cells.join('\t'));

/** 样例的合计行：**从明细逐列相加**得到（样例自己就必须是「合计对得上」的干净稿） */
function sampleTotalRow(header, details) {
  const cols = String(header).split('\t');
  const cells = cols.map(() => '');
  cells[0] = '合计';
  for (const role of SUM_ROLES) {
    const i = cols.indexOf(LABELS[role]);
    if (i < 0) continue;
    cells[i] = String(round2(details.reduce((acc, line) => {
      const n = normNumber(String(line).split('\t')[i]);
      return acc + (n === null ? 0 : n);
    }, 0)));
  }
  return cells.join('\t');
}

const SAMPLE_TEXT = [SAMPLE_HEAD].concat(SAMPLE_DETAILS)
  .concat([sampleTotalRow(SAMPLE_HEAD, SAMPLE_DETAILS)]).join('\n');

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「记录齐全」，也不说「记录有问题」。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|未知)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 字符串化 + 去空白 */
function str(v) {
  return String(v == null ? '' : v).trim();
}

/** 「第 N 行「车牌 日期」」——每条结论都靠它指回原文 */
function who(it) {
  const tag = [str(it.plate), str(it.tripDate)].filter(Boolean).join(' ');
  return `第 ${it.line} 行「${tag || '未填车辆/日期'}」`;
}

/** 认日期：只认 YYYY-MM-DD / YYYY/MM/DD / YYYY.MM.DD / YYYY年M月D日（不做任何猜测） */
function parseDate(raw) {
  const s = str(raw);
  const m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const ms = Date.UTC(y, mo - 1, d);
  const back = new Date(ms);
  if (back.getUTCFullYear() !== y || back.getUTCMonth() !== mo - 1 || back.getUTCDate() !== d) return null;
  return { y, m: mo, d, ms };
}

function fmtDate(dt) {
  const p = (n) => (n < 10 ? `0${n}` : String(n));
  return `${dt.y}-${p(dt.m)}-${p(dt.d)}`;
}

/** 相差天数（b - a），正数表示 b 在 a 之后 */
function dayDiff(a, b) {
  return Math.round((b.ms - a.ms) / 86400000);
}

/** 认时间：只认 24 小时制 HH:MM 或 HH:MM:SS，返回当日分钟数（不做任何猜测） */
function parseTime(raw) {
  const m = /^(\d{1,2}):(\d{2})(?::(\d{2}))?$/.exec(str(raw));
  if (!m) return null;
  const h = Number(m[1]);
  const mi = Number(m[2]);
  if (h > 23 || mi > 59) return null;
  return h * 60 + mi;
}

function num(it, role) {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
}

/** 合计行识别：**第一个非空单元格**是「合计 / 总计 / 小计」这类字样 */
function isTotalRow(it) {
  for (const c of splitRow(str(it.raw))) {
    const v = str(c);
    if (!v) continue;
    return /^(合计|总计|小计|合计数|总计数|共计)$/.test(v);
  }
  return false;
}

/** 解析成 {header, cols, items, detailItems, totalRows, totals, missingRoles, missingColumns, error}；
 *  行是**扁平**对象：{line, raw, 角色:值…}；合计行不算明细，也不进 totals 的加总。 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detailItems: [], totalRows: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  const detailItems = [];
  const totalRows = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
    if (isTotalRow(it)) totalRows.push(it);
    else detailItems.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detailItems.reduce((acc, it) => acc + num(it, role), 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detailItems,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  if (it.raw !== undefined && it.raw !== null && str(it.raw) !== '') f.evidence = str(it.raw);
  return f;
}

/** 本表出现过的全部出车日期（升序）—— 覆盖核对与汇总都用它当「应检日历」 */
function calendarDays(items) {
  const set = new Set();
  for (const it of items) {
    const dt = parseDate(it.tripDate);
    if (dt) set.add(fmtDate(dt));
  }
  return [...set].sort();
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 出车检查记录覆盖：以本表出现的全部出车日期为应检日历，逐台车点名缺哪一天 */
function coverageGaps(items) {
  const days = calendarDays(items);
  if (days.length < 2) return [];         // 只有一天 ⇒ 覆盖无可比口径，不出结论
  const byVehicle = new Map();
  for (const it of items) {
    const plate = str(it.plate);
    const dt = parseDate(it.tripDate);
    if (!plate || !dt) continue;          // 空 / 坏值交给「空白与格式检测」
    if (!byVehicle.has(plate)) byVehicle.set(plate, { plate, first: it, seen: new Set() });
    byVehicle.get(plate).seen.add(fmtDate(dt));
  }
  const out = [];
  for (const v of byVehicle.values()) {
    const missing = days.filter((d) => !v.seen.has(d));
    if (!missing.length) continue;
    out.push({ plate: v.plate, first: v.first, calendar: days, have: v.seen.size, missing });
  }
  out.sort((a, b) => String(a.plate).localeCompare(String(b.plate)));
  return out;
}

function checkTripCoverage(items) {
  const out = [];
  for (const g of coverageGaps(items)) {
    const named = g.missing.slice(0, 15).join('、')
      + (g.missing.length > 15 ? ` 等共 ${g.missing.length} 天` : '');
    out.push(finding('P1', '出车检查记录覆盖不足', g.first, -g.missing.length,
      `第 ${g.first.line} 行「${g.plate}」：本表覆盖的应检出车日为 ${g.calendar.length} 天`
      + `（${g.calendar[0]} ~ ${g.calendar[g.calendar.length - 1]}），该车只有 ${g.have} 天有出车检查记录，`
      + `缺 ${g.missing.length} 天：${named}。`,
      '逐日补齐该车的出车检查记录（制动 / 灯光 / 轮胎 / 灭火器 / 逃生锤逐项签认）；'
      + '确属停运的当天请在备注里写明停运，别留空档 —— 事后倒查时「没有记录」与「没有检查」是分不清的。'));
  }
  return out;
}

/** 2. 检查项目齐全性：检查项目数 ≥ 规定检查项目数 */
function checkItemCount(items) {
  const out = [];
  for (const it of items) {
    const got = normNumber(it.checkItems);
    const need = normNumber(it.requiredItems);
    if (got === null || need === null) continue;        // 缺失 / 解析不了交给「空白与格式检测」
    if (got < 0 || need < 0) continue;                  // 负数由「数值为负」逐处点名，不重复报
    if (got >= need) continue;
    out.push(finding('P1', '检查项目不齐全', it, round2(got - need),
      `${who(it)}：检查项目数 ${got} 项 < 规定检查项目数 ${need} 项，缺 ${round2(need - got)} 项 —— `
      + '出车检查必须覆盖制动 / 灯光 / 轮胎 / 灭火器 / 逃生锤这些规定项目。',
      '按本校（本公司）的出车检查表逐项重检并补记缺的那几项；缺项的意思是「这天这项没人签认」，不是「没检查」。'));
  }
  return out;
}

/** 3. 驾驶员资格有效期：出车日期 ≤ 驾驶证 / 校车驾驶资格 / 体检证明到期日 */
function checkQualificationExpiry(items) {
  const out = [];
  const CERTS = [
    ['licenseExpiry', '驾驶证到期日'],
    ['busQualExpiry', '校车驾驶资格到期日'],
    ['medicalExpiry', '体检证明到期日'],
  ];
  for (const it of items) {
    const trip = parseDate(it.tripDate);
    if (!trip) continue;
    for (const [role, label] of CERTS) {
      const exp = parseDate(it[role]);
      if (!exp) continue;                     // 空白 / 坏格式交给「空白与格式检测」
      const over = dayDiff(exp, trip);
      if (over <= 0) continue;                // 出车日期 = 到期日 视为当天仍有效
      out.push(finding('P0', '驾驶员资格超期', it, over,
        `${who(it)}：${label} ${fmtDate(exp)} 在出车日期 ${fmtDate(trip)} 之前已经到期，超期 ${over} 天`
        + `（驾驶员：${str(it.driverName) || '(未填)'}）。`,
        '资格过期当天就必须停班换人：先查这一趟是谁派的班，再补办换证 / 体检并把有效期录回台账；'
        + '无校车驾驶资格或体检证明过期上路属直接处罚项。'));
    }
  }
  return out;
}

/** 4. 同一车辆同一日期重复登记 */
function checkDuplicateVehicleDate(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const plate = str(it.plate);
    const dt = parseDate(it.tripDate);
    if (!plate || !dt) continue;
    const day = fmtDate(dt);
    const key = `${plate}|${day}`;
    if (seen.has(key)) {
      out.push(finding('P0', '同一车辆同一日期重复登记', it, undefined,
        `第 ${it.line} 行「${plate} ${day}」：这一台车这一天的出车检查记录在第 ${seen.get(key)} 行已经登记过一次 —— `
        + '同车同日重复登记，说明当天的检查记录被记了两遍。',
        '一台车一天只应有一条出车检查记录；若是补录或改录，请把作废的那条划掉并注明原因，别留两条并存。'));
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 5. 合计行逐列复核：合计行的数量列必须等于明细逐列相加 */
function checkTotalRows(detailItems, totalRows) {
  const out = [];
  if (!totalRows.length) return out;
  const sums = {};
  for (const role of SUM_ROLES) {
    sums[role] = round2(detailItems.reduce((acc, it) => acc + num(it, role), 0));
  }
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const v = normNumber(raw);
      if (v === null) {
        out.push(finding('P1', '数值无法解析', tr, undefined,
          `${who(tr)}（合计行）：「${LABELS[role]}」的值「${str(raw)}」不是可识别的数字。`,
          '把合计行的数量改成纯数字形态再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      const diff = round2(v - sums[role]);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行与明细不符', tr, diff,
        `${who(tr)}（合计行）：「${LABELS[role]}」填 ${v}，而明细逐行相加应为 ${sums[role]}，差额 ${round2(diff)}。`,
        '要么明细漏行、要么合计行是手改过的：先按明细重算一遍合计，再核对是不是有整台车整天的记录被落下了。'));
    }
  }
  return out;
}

/** 6. 空白与格式检测：关键字段、日期与时间格式、数值为负 / 无法解析、状态值非法、时间的先后顺序 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${str(raw)}」不是可识别的数字（只认数字、千分位、¥、括号负数）。`,
          '把数量改成纯数字形态（如 19 / 86.5）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 校车运行记录里出现负数通常是填反了方向或写成了红字冲销。`,
          '确认是冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      }
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (parseDate(raw)) continue;
      out.push(finding('P1', '日期格式无法识别', it, undefined,
        `${who(it)}：「${label}」的值「${str(raw)}」不是可识别的日期（只认 YYYY-MM-DD / YYYY/MM/DD / YYYY年M月D日）。`,
        '把日期统一成 2026-03-02 这种形态再跑；本工具不会猜一个日期来替你算超期天数。'));
    }

    for (const [role, label] of TIME_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (parseTime(raw) !== null) continue;
      out.push(finding('P1', '时间格式无法识别', it, undefined,
        `${who(it)}：「${label}」的值「${str(raw)}」不是可识别的时间（只认 24 小时制 HH:MM 或 HH:MM:SS）。`,
        '把时间统一成 06:40 这种 24 小时制再跑；别写「早上六点」这类描述。'));
    }

    const dept = parseTime(it.departTime);
    const ret = parseTime(it.returnTime);
    if (dept !== null && ret !== null && ret < dept) {
      out.push(finding('P1', '出车时间晚于收车时间', it, round2(ret - dept),
        `${who(it)}：出车时间 ${str(it.departTime)} 晚于收车时间 ${str(it.returnTime)} —— `
        + '要么这一趟的时间跨了午夜，要么两个时间填反了。',
        '夜班跨午夜的请把收车时间写到次日并加注日期；确属填反的直接改正后重跑。'));
    }

    const result = str(it.checkResult);
    if (result && ALLOWED_RESULTS.indexOf(result) < 0) {
      out.push(finding('P1', '状态值非法', it, undefined,
        `${who(it)}：「检查结果」的值「${result}」不在允许取值里（只认 ${ALLOWED_RESULTS.join(' / ')}）。`,
        '把检查结果改成允许的取值之一；本工具不会替你把「大概合格」判成合格。'));
    }
  }
  return out;
}

/* ---------- 完整档（买断版）追加的核对实现：免费包里没有这些函数 ---------- */

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的校车运行与安全检查记录（出车检查 / 驾驶员资格 / 照管交接 / 趟次里程）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的校车运行与安全检查记录（出车检查 / 驾驶员资格 / 照管交接 / 趟次里程）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的校车运行与安全检查记录（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }



  if (!t.items.length) {
    return insufficient(['至少一行出车明细（现在只有表头，没有可核对的明细行）']);
  }
  const details = t.detailItems;
  if (!details.length) {
    return insufficient(['至少一行出车明细（现在只有表头与「合计」行，没有可核对的明细行）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkTripCoverage(details)) findings.push(f);
  for (const f of checkItemCount(details)) findings.push(f);
  for (const f of checkQualificationExpiry(details)) findings.push(f);
  for (const f of checkDuplicateVehicleDate(details)) findings.push(f);
  for (const f of checkTotalRows(details, t.totalRows)) findings.push(f);
  for (const f of checkFieldIntegrity(details)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  
  if (!t.totalRows.length) {
    notRun.push('合计行逐列复核（本次表里没有「合计」行，逐列复核做不了 —— 请把合计行一起复制进来）');
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const days = calendarDays(details);
  const result = {
    findings,
    summary: {
      rows: details.length,
      total_rows: t.totalRows.length,
      vehicles: new Set(details.map((it) => str(it.plate) || '(未填车辆)')).size,
      calendar_days: days.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      rated_seats_total: t.totals.ratedSeats,
      riders_total: t.totals.actualRiders,
      trips_total: t.totals.trips,
      mileage_total: t.totals.mileage,
      fuel_total: t.totals.fuel,
      basis: '出车检查记录按「车辆 × 出车日期」核对：以本表出现的全部出车日期为应检日历，逐台车点名缺哪一天；'
        + '检查项目数须不小于规定检查项目数；出车日期不得晚于驾驶证 / 校车驾驶资格 / 体检证明到期日；'
        + '同一车辆同一日期只能登记一次；合计行的 趟次 / 核载人数 / 实际乘坐人数 / 里程 / 油耗 须等于明细逐列相加；'
        + '关键字段不得空白或占位符，日期用 YYYY-MM-DD、时间用 24 小时制 HH:MM，数值不得为负或无法解析，'
        + `检查结果只认 ${ALLOWED_RESULTS.join(' / ')}。`,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张记录表按上面写明的口径算得对、字面齐全**，'
      + '不代表出车检查真的做过、车辆与驾驶员实际合规，也不代表学校与校车公司的主体责任已经过关 —— '
      + '那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: details.length,
    total_rows: t.totalRows.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    vehicles: result.summary.vehicles,
    calendar_days: days.length,
    rated_seats_total: t.totals.ratedSeats,
    riders_total: t.totals.actualRiders,
    trips_total: t.totals.trips,
    mileage_total: t.totals.mileage,
    fuel_total: t.totals.fuel,
  };
  result.scope = scope;



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
