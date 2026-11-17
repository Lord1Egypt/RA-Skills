/**
 * 通用 Excel 样式套件（零依赖，纯 Node.js，无需 npm install）。
 *
 * 用途：Agent 写「广告方案」「周期报告」等 .xlsx 时，直接 import 本文件，
 * 用高层组件（标题条/副标题条/分区条/表头/数据行/键值行）拼版面，
 * 不必从零手写单元格与颜色，也不会出现"只有裸文字、无样式"的简陋效果。
 *
 * 设计规范见同目录 `excel-style-guide.md`（色板、字号、组件说明）。
 *
 * 用法：
 *   import { createExcelWorkbook } from "./excel-style-kit.mjs";
 *   const wb = createExcelWorkbook({ accent: "facebook" }); // 平台强调色，见 PLATFORM_ACCENTS
 *   const sheet = wb.addSheet("方案总览");
 *   sheet.setColWidths([20, 60]);
 *   sheet.titleBar("客户名 — 广告投放方案");
 *   sheet.subtitleBar("原生表单询盘 ｜ 四大洲覆盖");
 *   sheet.blankRow();
 *   sheet.sectionBar("一、公司基本信息");
 *   sheet.kvRow("客户名称", "XXX有限公司");
 *   sheet.kvRow("官网", "https://example.com", { hyperlink: "https://example.com" });
 *   wb.writeFile("./plan.xlsx");
 *
 * 数据表（多列）用法：
 *   const t = wb.addSheet("日趋势");
 *   t.setColWidths([14, 12, 12, 14]);
 *   t.tableHeader(["日期", "展示次数", "点击", "花费"]);
 *   t.dataRow(["2025-01-01", 1000, 50, "12.30"]);
 *   t.dataRow(["2025-01-02", 980, 44, "11.80"]);
 *
 * ID 列（账户/系列/关键词等）务必用 { textColumns: [0] } 强制文本格式，
 * 防止 Excel 把长数字 ID 转成科学计数法或丢精度。
 */

import fs from "node:fs";
import path from "node:path";

// ───────────────────────── 平台强调色（分区条 / 表头背景） ─────────────────────────

export const PLATFORM_ACCENTS = {
  default: "1F4E79", // 深藏青，无明确平台时的通用色
  facebook: "1877F2", // Meta / Facebook 蓝
  metaad: "1877F2",
  google: "1A73E8", // Google 蓝
  tiktok: "FE2C55", // TikTok 品牌红
  yandex: "FC3F1D", // Yandex 品牌红
  bingv2: "0078D4", // Bing / Microsoft 蓝
  bing: "0078D4",
};

const NEUTRAL = {
  titleFill: "1F2937", // 主标题条固定深灰蓝，版式统一，不随平台变化
  subtitleFill: "DEEAF6",
  subtitleText: "404040",
  zebraFill: "F2F2F2",
  border: "BFBFBF",
  textDark: "262626",
  textMuted: "595959",
  white: "FFFFFF",
};

const FONT_NAME = "微软雅黑";

function resolveAccent(accent) {
  if (!accent) return PLATFORM_ACCENTS.default;
  const hex = String(accent).replace(/^#/, "");
  if (/^[0-9a-fA-F]{6}$/.test(hex)) return hex.toUpperCase();
  const key = String(accent).toLowerCase();
  return (PLATFORM_ACCENTS[key] || PLATFORM_ACCENTS.default).toUpperCase();
}

function relLuminance(hex) {
  const c = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255);
  const lin = (v) => (v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
  return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
}

function textColorFor(bgHex) {
  return relLuminance(bgHex) > 0.55 ? NEUTRAL.textDark : NEUTRAL.white;
}

// ───────────────────────── XML / zip 基础工具（同 write-xlsx.ts 思路，独立实现） ─────────────────────────

function xmlEscape(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function colLetter(index) {
  let n = index + 1;
  let s = "";
  while (n > 0) {
    const rem = (n - 1) % 26;
    s = String.fromCharCode(65 + rem) + s;
    n = Math.floor((n - 1) / 26);
  }
  return s;
}

function crc32(buf) {
  let crc = 0xffffffff;
  for (let i = 0; i < buf.length; i++) {
    crc ^= buf[i];
    for (let j = 0; j < 8; j++) {
      crc = crc & 1 ? (crc >>> 1) ^ 0xedb88320 : crc >>> 1;
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function zipStore(files) {
  const locals = [];
  const centrals = [];
  let offset = 0;
  for (const file of files) {
    const nameBuf = Buffer.from(file.name, "utf8");
    const crc = crc32(file.data);
    const local = Buffer.alloc(30 + nameBuf.length);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(file.data.length, 18);
    local.writeUInt32LE(file.data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    nameBuf.copy(local, 30);
    locals.push(local, file.data);

    const central = Buffer.alloc(46 + nameBuf.length);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(file.data.length, 20);
    central.writeUInt32LE(file.data.length, 24);
    central.writeUInt16LE(nameBuf.length, 28);
    central.writeUInt32LE(offset, 42);
    nameBuf.copy(central, 46);
    centrals.push(central);

    offset += local.length + file.data.length;
  }
  const centralBuf = Buffer.concat(centrals);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(files.length, 8);
  end.writeUInt16LE(files.length, 10);
  end.writeUInt32LE(centralBuf.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, centralBuf, end]);
}

// ───────────────────────── 样式注册表（fonts/fills/borders/numFmts/cellXfs 去重） ─────────────────────────

class StyleRegistry {
  constructor() {
    this.fonts = [{ size: 11, color: "000000", name: "宋体", bold: false }];
    this.fills = [{ kind: "none" }, { kind: "gray125" }];
    this.borders = [{ thin: false }];
    this.xfs = [{ fontId: 0, fillId: 0, borderId: 0, numFmtId: 0, align: null }];
    this._fontCache = new Map();
    this._fillCache = new Map();
    this._borderCache = new Map();
    this._xfCache = new Map();
  }

  fontId({ size = 10, color = NEUTRAL.textDark, bold = false, name = FONT_NAME }) {
    const key = JSON.stringify({ size, color, bold, name });
    if (this._fontCache.has(key)) return this._fontCache.get(key);
    const id = this.fonts.length;
    this.fonts.push({ size, color, bold, name });
    this._fontCache.set(key, id);
    return id;
  }

  fillId(hex) {
    if (!hex) return 0;
    const key = hex.toUpperCase();
    if (this._fillCache.has(key)) return this._fillCache.get(key);
    const id = this.fills.length;
    this.fills.push({ kind: "solid", color: key });
    this._fillCache.set(key, id);
    return id;
  }

  borderId(thin) {
    const key = thin ? "thin" : "none";
    if (this._borderCache.has(key)) return this._borderCache.get(key);
    const id = this.borders.length;
    this.borders.push({ thin });
    this._borderCache.set(key, id);
    return id;
  }

  xfId(spec) {
    const key = JSON.stringify(spec);
    if (this._xfCache.has(key)) return this._xfCache.get(key);
    const id = this.xfs.length;
    this.xfs.push(spec);
    this._xfCache.set(key, id);
    return id;
  }

  /** 组合一个具名样式并返回 xf 索引，供单元格 `s="idx"` 使用。 */
  resolve({
    fontSize = 10,
    fontColor = NEUTRAL.textDark,
    bold = false,
    fill,
    border = true,
    hAlign = "left",
    vAlign = "center",
    wrap = true,
    forceText = false,
  }) {
    const fontId = this.fontId({ size: fontSize, color: fontColor, bold });
    const fillId = fill ? this.fillId(fill) : 0;
    const borderId = this.borderId(border);
    return this.xfId({
      fontId,
      fillId,
      borderId,
      numFmtId: forceText ? 49 : 0,
      align: { h: hAlign, v: vAlign, wrap },
    });
  }
}

// ───────────────────────── styles.xml 序列化 ─────────────────────────

function fontXml(f) {
  const color = `<color rgb="FF${f.color}"/>`;
  return (
    `<font>${f.bold ? "<b/>" : ""}<sz val="${f.size}"/>${color}` +
    `<name val="${xmlEscape(f.name)}"/><charset val="134"/></font>`
  );
}

function fillXml(f) {
  if (f.kind === "none") return `<fill><patternFill patternType="none"/></fill>`;
  if (f.kind === "gray125") return `<fill><patternFill patternType="gray125"/></fill>`;
  return (
    `<fill><patternFill patternType="solid"><fgColor rgb="FF${f.color}"/>` +
    `<bgColor indexed="64"/></patternFill></fill>`
  );
}

function borderXml(b) {
  if (!b.thin) return `<border><left/><right/><top/><bottom/><diagonal/></border>`;
  const side = `<color rgb="FF${NEUTRAL.border}"/>`;
  return (
    `<border><left style="thin">${side}</left><right style="thin">${side}</right>` +
    `<top style="thin">${side}</top><bottom style="thin">${side}</bottom><diagonal/></border>`
  );
}

function xfXml(x) {
  const applies = [];
  let alignXml = "";
  if (x.align) {
    alignXml = `<alignment horizontal="${x.align.h}" vertical="${x.align.v}" wrapText="${x.align.wrap ? 1 : 0}"/>`;
    applies.push('applyAlignment="1"');
  }
  if (x.fontId) applies.push('applyFont="1"');
  if (x.fillId) applies.push('applyFill="1"');
  if (x.borderId) applies.push('applyBorder="1"');
  if (x.numFmtId) applies.push('applyNumberFormat="1"');
  return (
    `<xf numFmtId="${x.numFmtId}" fontId="${x.fontId}" fillId="${x.fillId}" ` +
    `borderId="${x.borderId}" xfId="0" ${applies.join(" ")}>${alignXml}</xf>`
  );
}

function stylesXml(reg) {
  return (
    `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
    `<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">` +
    `<fonts count="${reg.fonts.length}">${reg.fonts.map(fontXml).join("")}</fonts>` +
    `<fills count="${reg.fills.length}">${reg.fills.map(fillXml).join("")}</fills>` +
    `<borders count="${reg.borders.length}">${reg.borders.map(borderXml).join("")}</borders>` +
    `<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>` +
    `<cellXfs count="${reg.xfs.length}">${reg.xfs.map(xfXml).join("")}</cellXfs>` +
    `<cellStyles count="1"><cellStyle name="常规" xfId="0" builtinId="0"/></cellStyles>` +
    `</styleSheet>`
  );
}

// ───────────────────────── worksheet 序列化 ─────────────────────────

function cellXml(ref, cell) {
  if (cell == null) return "";
  const { value, styleId } = cell;
  const sAttr = styleId ? ` s="${styleId}"` : "";
  if (value == null || value === "") {
    return styleId ? `<c r="${ref}"${sAttr}/>` : "";
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return `<c r="${ref}"${sAttr}><v>${value}</v></c>`;
  }
  return `<c r="${ref}"${sAttr} t="inlineStr"><is><t xml:space="preserve">${xmlEscape(String(value))}</t></is></c>`;
}

function sheetXml(sheet) {
  const colsXml = sheet.colWidths.length
    ? `<cols>${sheet.colWidths
        .map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w}" customWidth="1"/>`)
        .join("")}</cols>`
    : "";
  const rowsXml = sheet.rows
    .map((row, i) => {
      const r = i + 1;
      const htAttr = row.height ? ` ht="${row.height}" customHeight="1"` : "";
      const cells = row.cells.map((cell, cIdx) => cellXml(`${colLetter(cIdx)}${r}`, cell)).join("");
      return `<row r="${r}"${htAttr}>${cells}</row>`;
    })
    .join("");
  const mergesXml = sheet.merges.length
    ? `<mergeCells count="${sheet.merges.length}">${sheet.merges
        .map((m) => `<mergeCell ref="${m}"/>`)
        .join("")}</mergeCells>`
    : "";
  const freezeXml = sheet.freeze
    ? `<sheetViews><sheetView workbookViewId="0"><pane ySplit="${sheet.freeze}" topLeftCell="A${sheet.freeze + 1}" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>`
    : "";
  const linkEntries = Object.entries(sheet.hyperlinks);
  const hyperlinksXml = linkEntries.length
    ? `<hyperlinks>${linkEntries
        .map(([ref, i]) => `<hyperlink ref="${ref}" r:id="rIdHlink${i}"/>`)
        .join("")}</hyperlinks>`
    : "";
  return (
    `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
    `<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" ` +
    `xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">` +
    `${freezeXml}${colsXml}<sheetData>${rowsXml}</sheetData>${mergesXml}${hyperlinksXml}` +
    `</worksheet>`
  );
}

function sheetRelsXml(sheet) {
  const entries = Object.entries(sheet.hyperlinks);
  if (!entries.length) return null;
  const rels = entries
    .map(
      ([, i]) =>
        `<Relationship Id="rIdHlink${i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="${xmlEscape(sheet.hyperlinkTargets[i])}" TargetMode="External"/>`,
    )
    .join("");
  return (
    `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
    `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${rels}</Relationships>`
  );
}

// ───────────────────────── 高层 Sheet / Workbook API ─────────────────────────

/** 长文本粗略估算换行后所需行高，避免内容被裁切（参考文件对长段落手动加大过行高）。 */
function estimateWrapHeight(text, colWidthChars) {
  const str = String(text ?? "");
  if (!str) return undefined;
  const lines = str.split("\n").reduce((sum, line) => {
    const width = Math.max(colWidthChars || 20, 8);
    return sum + Math.max(1, Math.ceil(line.length / (width * 1.8)));
  }, 0);
  if (lines <= 1) return undefined;
  return Math.min(400, Math.max(20, lines * 15));
}

class SheetBuilder {
  constructor(name, registry, accentHex) {
    this.name = name.replace(/[\\/?*[\]:]/g, " ").slice(0, 31) || "Sheet";
    this.registry = registry;
    this.accentHex = accentHex;
    this.accentText = textColorFor(accentHex);
    this.rows = [];
    this.merges = [];
    this.colWidths = [];
    this.hyperlinks = {};
    this.hyperlinkTargets = {};
    this._hlSeq = 0;
    this.freeze = 0;
    this._zebra = 0;
  }

  /** 设置列宽（字符数），同时决定标题/分区条默认合并跨度。 */
  setColWidths(widths) {
    this.colWidths = widths;
    return this;
  }

  get colCount() {
    return this.colWidths.length || 1;
  }

  _pushRow(cells, { height } = {}) {
    this.rows.push({ cells, height });
    return this.rows.length; // 1-based 行号
  }

  _mergeCurrentRow(span) {
    const r = this.rows.length;
    if (span > 1) this.merges.push(`A${r}:${colLetter(span - 1)}${r}`);
  }

  blankRow(n = 1) {
    for (let i = 0; i < n; i++) this._pushRow([]);
    return this;
  }

  /** 主标题条：深色底 + 白色大号粗体，整行合并，版式固定不随平台变化。 */
  titleBar(text, { span } = {}) {
    const s = this.registry.resolve({
      fontSize: 16,
      fontColor: textColorFor(NEUTRAL.titleFill),
      bold: true,
      fill: NEUTRAL.titleFill,
      border: false,
      hAlign: "left",
    });
    this._pushRow([{ value: text, styleId: s }], { height: 28 });
    this._mergeCurrentRow(span || this.colCount);
    return this;
  }

  /** 副标题条：浅蓝底 + 深灰文字，用于一句话摘要/标签行。 */
  subtitleBar(text, { span } = {}) {
    const s = this.registry.resolve({
      fontSize: 10.5,
      fontColor: NEUTRAL.subtitleText,
      fill: NEUTRAL.subtitleFill,
      border: false,
      hAlign: "left",
    });
    this._pushRow([{ value: text, styleId: s }], { height: 20 });
    this._mergeCurrentRow(span || this.colCount);
    return this;
  }

  /** 分区条：平台强调色底 + 自动对比文字，居中，用于「一、xxx」大章节标题。 */
  sectionBar(text, { span } = {}) {
    const s = this.registry.resolve({
      fontSize: 11,
      fontColor: this.accentText,
      bold: true,
      fill: this.accentHex,
      border: false,
      hAlign: "center",
    });
    this._pushRow([{ value: text, styleId: s }], { height: 22 });
    this._mergeCurrentRow(span || this.colCount);
    return this;
  }

  /** 说明性小字（灰色备注行），如数据口径、免责声明。 */
  noteRow(text, { span } = {}) {
    const s = this.registry.resolve({
      fontSize: 9,
      fontColor: NEUTRAL.textMuted,
      fill: NEUTRAL.subtitleFill,
      border: true,
      hAlign: "left",
      vAlign: "top",
    });
    const height = estimateWrapHeight(text, this.colWidths.reduce((a, b) => a + b, 0) || 60);
    this._pushRow([{ value: text, styleId: s }], { height });
    this._mergeCurrentRow(span || this.colCount);
    return this;
  }

  /** 数据表表头行：平台强调色底 + 白/深自动对比文字，居中，细边框。重置数据行斑马纹计数。 */
  tableHeader(headers) {
    this._zebra = 0;
    const s = this.registry.resolve({
      fontSize: 10,
      fontColor: this.accentText,
      bold: true,
      fill: this.accentHex,
      border: true,
      hAlign: "center",
    });
    this._pushRow(
      headers.map((h) => ({ value: h, styleId: s })),
      { height: 20 },
    );
    return this;
  }

  /**
   * 数据表一行（斑马纹自动交替）。
   * @param {(string|number|null)[]} cells
   * @param {{textColumns?: number[], centerColumns?: number[]}} [opts]
   *   textColumns：需强制文本格式的列（如 ID），防止科学计数法/精度丢失。
   */
  dataRow(cells, { textColumns = [], centerColumns = [] } = {}) {
    const shaded = this._zebra % 2 === 1;
    this._zebra += 1;
    const fill = shaded ? NEUTRAL.zebraFill : undefined;
    let maxHeight;
    const rowCells = cells.map((value, idx) => {
      const forceText = textColumns.includes(idx);
      const hAlign = centerColumns.includes(idx) ? "center" : "left";
      const s = this.registry.resolve({
        fontSize: 10,
        fontColor: NEUTRAL.textDark,
        fill,
        border: true,
        hAlign,
        forceText,
      });
      const h = estimateWrapHeight(value, this.colWidths[idx]);
      if (h && (!maxHeight || h > maxHeight)) maxHeight = h;
      return { value: forceText && value != null ? String(value) : value, styleId: s };
    });
    this._pushRow(rowCells, { height: maxHeight });
    return this;
  }

  /**
   * 键值行（两列型表格：项目/内容），左列浅蓝底加粗，右列白底，交替底色。
   * 用于「方案总览」「客户画像」这类项目名+说明的表。
   */
  kvRow(label, value, { hyperlink, shaded } = {}) {
    const isShaded = shaded ?? this._zebra % 2 === 1;
    this._zebra += 1;
    const labelStyle = this.registry.resolve({
      fontSize: 10,
      fontColor: NEUTRAL.textDark,
      bold: true,
      fill: isShaded ? NEUTRAL.zebraFill : NEUTRAL.subtitleFill,
      border: true,
      hAlign: "left",
      vAlign: "top",
    });
    const valueStyle = this.registry.resolve({
      fontSize: 10,
      fontColor: NEUTRAL.textDark,
      fill: isShaded ? NEUTRAL.zebraFill : undefined,
      border: true,
      hAlign: "left",
      vAlign: "top",
    });
    const colSpan = this.colCount - 1;
    const height = estimateWrapHeight(value, this.colWidths[1] || 40);
    const rowIndex = this._pushRow(
      [
        { value: label, styleId: labelStyle },
        { value, styleId: valueStyle },
      ],
      { height },
    );
    if (colSpan > 1) {
      this.merges.push(`B${rowIndex}:${colLetter(this.colCount - 1)}${rowIndex}`);
    }
    if (hyperlink) {
      const id = ++this._hlSeq;
      this.hyperlinks[`B${rowIndex}`] = id;
      this.hyperlinkTargets[id] = hyperlink;
    }
    return this;
  }
}

class WorkbookBuilder {
  constructor({ accent } = {}) {
    this.registry = new StyleRegistry();
    this.accentHex = resolveAccent(accent);
    this.sheets = [];
  }

  addSheet(name) {
    const sheet = new SheetBuilder(name, this.registry, this.accentHex);
    this.sheets.push(sheet);
    return sheet;
  }

  toBuffer() {
    if (this.sheets.length === 0) throw new Error("Excel 工作簿至少需要 1 个 Sheet");
    const files = [];
    const sheetOverrides = this.sheets
      .map(
        (_, i) =>
          `<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`,
      )
      .join("");
    files.push({
      name: "[Content_Types].xml",
      data: Buffer.from(
        `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
          `<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">` +
          `<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>` +
          `<Default Extension="xml" ContentType="application/xml"/>` +
          `<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>` +
          `<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>` +
          `${sheetOverrides}</Types>`,
        "utf8",
      ),
    });
    files.push({
      name: "_rels/.rels",
      data: Buffer.from(
        `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
          `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">` +
          `<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>` +
          `</Relationships>`,
        "utf8",
      ),
    });
    const sheetTags = this.sheets
      .map((s, i) => `<sheet name="${xmlEscape(s.name)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`)
      .join("");
    files.push({
      name: "xl/workbook.xml",
      data: Buffer.from(
        `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
          `<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" ` +
          `xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">` +
          `<sheets>${sheetTags}</sheets></workbook>`,
        "utf8",
      ),
    });
    const stylesRid = this.sheets.length + 1;
    const wbRels = this.sheets
      .map(
        (_, i) =>
          `<Relationship Id="rId${i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`,
      )
      .join("");
    files.push({
      name: "xl/_rels/workbook.xml.rels",
      data: Buffer.from(
        `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
          `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${wbRels}` +
          `<Relationship Id="rId${stylesRid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>` +
          `</Relationships>`,
        "utf8",
      ),
    });
    files.push({ name: "xl/styles.xml", data: Buffer.from(stylesXml(this.registry), "utf8") });
    this.sheets.forEach((sheet, i) => {
      files.push({
        name: `xl/worksheets/sheet${i + 1}.xml`,
        data: Buffer.from(sheetXml(sheet), "utf8"),
      });
      const relsXml = sheetRelsXml(sheet);
      if (relsXml) {
        files.push({
          name: `xl/worksheets/_rels/sheet${i + 1}.xml.rels`,
          data: Buffer.from(relsXml, "utf8"),
        });
      }
    });
    return zipStore(files);
  }

  writeFile(filePath) {
    const abs = path.resolve(filePath);
    fs.mkdirSync(path.dirname(abs), { recursive: true });
    fs.writeFileSync(abs, this.toBuffer());
    return abs;
  }
}

/**
 * @param {{accent?: string}} [opts] accent 支持平台名（facebook/google/tiktok/yandex/bingv2）或 "#RRGGBB"
 */
export function createExcelWorkbook(opts) {
  return new WorkbookBuilder(opts);
}
