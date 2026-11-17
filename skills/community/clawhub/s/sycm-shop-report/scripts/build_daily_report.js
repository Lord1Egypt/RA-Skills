/*
 * 本脚本是 sycm-shop-report 流水线的【第 3 步 · docx 装配（日报）】。
 * 职责范围：读 daily_data.json（或 example）与已生成的 PNG，产出中文 .docx 到 output_dir
 * 不做：不 fetch 网络、不调 MCP、不生成图表、不上传任何数据
 * 完整端到端流程见 SKILL.md 的「流水线」段与「工作流」清单。
 */
/* 日报 docx 生成器（数据驱动）。
 * 读取同目录 daily_data.json（不存在则用 daily_data.example.json），
 * 图表读 <output_dir>/<charts_subdir>/*.png（先跑 build_daily_charts.py）。
 * 布局/配色/字体锁死在此文件；换店铺换日期只改 JSON。
 * 用法： NODE_PATH="<全局node_modules>" node build_daily_report.js [数据json路径]
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle, ShadingType,
  LevelFormat, Footer, PageNumber, VerticalAlign,
} = require("docx");

const HERE = __dirname;
const arg = process.argv[2];
const dataPath = arg || (fs.existsSync(path.join(HERE, "daily_data.json")) ? path.join(HERE, "daily_data.json") : path.join(HERE, "daily_data.example.json"));
const D = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const SHOP = D.shop_name;
const OUTDIR = D.output_dir;
const CH = path.join(OUTDIR, D.charts_subdir || "charts").replace(/\\/g, "/");
const OUT = `${OUTDIR}/${SHOP}-店铺经营日报-${D.period.title_date}.docx`;
const EA = D.font || "Microsoft YaHei";
const F = { ascii: EA, eastAsia: EA, hAnsi: EA };

const GOOD = "1E7B34", BAD = "C0392B", FLAT = "666666", WARN = "D68910", PRI = "1F3864";
const CMAP = { GOOD, BAD, WARN, PRI, FLAT };
const colOf = (t) => (t && CMAP[t.color]) ? CMAP[t.color] : (t && t.color) || "333333";

const pct = (v) => v * 100;
const n0 = (v) => Math.round(v).toLocaleString("en-US");
const money = (v) => v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const dec = (v, d = 2) => v.toFixed(d);

function chgByCrc(crc, invert) {
  if (crc === null || crc === undefined || !isFinite(crc)) return { text: "—", color: FLAT, align: AlignmentType.RIGHT };
  const r = crc > 0 ? 1 : crc < 0 ? -1 : 0;
  const col = invert ? (r < 0 ? GOOD : r > 0 ? BAD : FLAT) : (r > 0 ? GOOD : r < 0 ? BAD : FLAT);
  return { text: (crc >= 0 ? "+" : "−") + Math.abs(crc * 100).toFixed(1) + "%", color: col, bold: true, align: AlignmentType.RIGHT };
}
function chgPP(cur, base) {
  const d = (cur - base) * 100;
  return { text: (d >= 0 ? "+" : "−") + Math.abs(d).toFixed(2) + "pp", color: d >= 0 ? GOOD : BAD, bold: true, align: AlignmentType.RIGHT };
}

const SP = { before: 60, after: 60, line: 300 };
function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 140 }, children: [new TextRun({ text, bold: true, size: 30, color: PRI, font: F })] }); }
function P(runs, align) {
  return new Paragraph({ spacing: SP, alignment: align || AlignmentType.JUSTIFIED,
    children: (typeof runs === "string" ? [{ text: runs }] : runs).map((r) => new TextRun({ text: r.text, size: r.size || 21, bold: !!r.bold, italics: !!r.italics, color: colOf(r), font: F })) });
}
function bullet(runs) {
  const children = (typeof runs === "string" ? [{ text: runs }] : runs).map((r) => new TextRun({ text: r.text, size: r.size || 21, bold: !!r.bold, color: colOf(r), font: F }));
  return new Paragraph({ numbering: { reference: "dr-b", level: 0 }, spacing: { before: 40, after: 40, line: 300 }, alignment: AlignmentType.JUSTIFIED, children });
}
function note(text) { return new Paragraph({ spacing: { before: 80, after: 120, line: 280 }, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text, size: 18, italics: true, color: "808080", font: F })] }); }
function img(file, w, h, cap) {
  const p = `${CH}/${file}`;
  if (!fs.existsSync(p)) return [];
  const items = [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: cap ? 40 : 160 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(p), transformation: { width: w, height: h } })] })];
  if (cap) items.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 180, line: 260 }, children: [new TextRun({ text: cap, size: 18, italics: true, color: "7A7A7A", font: F })] }));
  return items;
}

const CONTENT_W = 9638;
function table(headers, rows, widths) {
  if (!widths) widths = headers.map(() => 100 / headers.length);
  const scale = CONTENT_W / widths.reduce((a, b) => a + b, 0);
  const cw = widths.map((w) => Math.round(w * scale)); cw[cw.length - 1] += CONTENT_W - cw.reduce((a, b) => a + b, 0);
  const head = new TableRow({ tableHeader: true, children: headers.map((t, i) => new TableCell({
    width: { size: cw[i], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "1F3864" }, margins: { top: 70, bottom: 70, left: 90, right: 90 },
    children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: { before: 0, after: 0, line: 240 }, children: [new TextRun({ text: t, bold: true, size: 19, color: "FFFFFF", font: F })] })] })) });
  const body = rows.map((row, ri) => new TableRow({ children: row.map((cell, ci) => {
    const m = typeof cell === "object" && cell !== null ? cell : { text: String(cell) };
    return new TableCell({ width: { size: cw[ci], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: m.fill || (ri % 2 ? "F2F5FA" : "FFFFFF") }, margins: { top: 60, bottom: 60, left: 90, right: 90 },
      children: [new Paragraph({ alignment: m.align || (ci === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT), spacing: { before: 0, after: 0, line: 240 }, children: [new TextRun({ text: m.text, size: m.size || 19, bold: !!m.bold, italics: !!m.italics, color: m.color || "333333", font: F })] })] }); }) }));
  return new Table({ columnWidths: cw, width: { size: CONTENT_W, type: WidthType.DXA },
    borders: { top: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, left: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, right: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "DCE3ED" }, insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "DCE3ED" } },
    rows: [head, ...body] });
}
const TOT = "E8EEF7";

function kpiCard(card) {
  return new TableCell({ width: { size: Math.round(CONTENT_W / 4), type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "FFFFFF" }, margins: { top: 160, bottom: 160, left: 160, right: 160 }, verticalAlign: VerticalAlign.CENTER,
    borders: { top: { style: BorderStyle.SINGLE, size: 20, color: card.accent, space: 0 }, left: { style: BorderStyle.SINGLE, size: 4, color: "E5E9F0" }, right: { style: BorderStyle.SINGLE, size: 4, color: "E5E9F0" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "E5E9F0" } },
    children: [
      new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 30 }, children: [new TextRun({ text: card.label, size: 18, color: "666666", font: F })] }),
      new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 40 }, children: [new TextRun({ text: card.value, size: 36, bold: true, color: PRI, font: F })] }),
      ...card.deltas.map((d) => new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 14 }, children: [
        new TextRun({ text: d.k + "  ", size: 16, color: "888888", font: F }),
        new TextRun({ text: d.v, size: 17, bold: true, color: d.dir === "up" ? GOOD : d.dir === "down" ? BAD : FLAT, font: F }) ] })),
    ] });
}
function kpiDashboard() {
  return new Table({ columnWidths: D.kpi_cards.map(() => Math.round(CONTENT_W / 4)), width: { size: CONTENT_W, type: WidthType.DXA },
    borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.SINGLE, size: 8, color: "FFFFFF" } },
    rows: [new TableRow({ children: D.kpi_cards.map(kpiCard) })] });
}

/* ================= 正文 ================= */
const M = D.metrics, today = M.today, LY = M.last_year, PW = M.prev_week, peer = D.peer;
const c = [];
c.push(new Paragraph({ spacing: { before: 0, after: 60 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${SHOP} · 店铺经营日报`, bold: true, size: 40, color: PRI, font: F })] }));
c.push(new Paragraph({ spacing: { before: 0, after: 40 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: `统计日：${D.period.title_date}（${D.period.weekday}）　环比：${D.period.prev_date}　上周同日：${D.period.prev_week_date}　去年同日：${D.period.yoy_date}（${D.period.yoy_weekday}）`, size: 20, color: "444444", font: F })] }));
c.push(new Paragraph({ spacing: { before: 0, after: 200 }, alignment: AlignmentType.CENTER, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: PRI, space: 8 } }, children: [new TextRun({ text: `${D.period.data_source_line}　报告生成：${D.generated_at}`, size: 18, color: "888888", font: F })] }));

/* 一、结论 */
c.push(h1("一、昨天卖得怎么样"));
c.push(kpiDashboard());
c.push(new Paragraph({ spacing: { before: 60, after: 200 }, children: [new TextRun({ text: "", font: F })] }));
c.push(P(D.headline));
c.push(P([{ text: D.signals_title, bold: true }]));
D.signals.forEach((s) => c.push(bullet([{ text: s.lead, bold: true, color: s.color || "BAD" }, { text: s.body }])));

/* 二、行动建议 */
c.push(h1(D.actions_title));
c.push(P(D.actions_intro));
D.actions.forEach((a) => {
  c.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 220, after: 100 }, children: [new TextRun({ text: a.title, bold: true, size: 24, color: "2E5496", font: F })] }));
  c.push(bullet([{ text: "为什么要做：", bold: true }, { text: a.why }]));
  c.push(bullet([{ text: "怎么做：", bold: true }, { text: a.how }]));
  c.push(bullet([{ text: "目标：", bold: true }, { text: a.goal }]));
});
if (D.actions_table && D.actions_table.length) {
  c.push(new Paragraph({ spacing: { before: 160, after: 80 }, children: [new TextRun({ text: "责任与截止时间一览", bold: true, size: 22, color: "2E5496", font: F })] }));
  c.push(table(["#", "事项", "负责人", "截止时间", "交付物 / 验收标准"],
    D.actions_table.map((r, i) => [String(i + 1), { text: r.task, align: AlignmentType.LEFT }, { text: r.owner, align: AlignmentType.LEFT }, { text: r.deadline, align: AlignmentType.LEFT }, { text: r.deliverable, align: AlignmentType.LEFT }]),
    [5, 26, 14, 18, 37]));
}
if (D.actions_extra) c.push(P([{ text: "另外：", bold: true }, { text: D.actions_extra }]));

/* 三、同比对照 */
const ys = D.yoy_section;
c.push(h1(ys.title));
c.push(P(ys.intro));
c.push(...img(ys.chart, 620, 290, ys.chart_caption));
c.push(table(["指标", `去年同日`, "昨天", "我们同比", "同行同比"], [
  ["进店人数", n0(LY.uv), n0(today.uv), chgByCrc(today.uv / LY.uv - 1), chgByCrc(peer.peer_ly ? peer.avg.uv / peer.peer_ly.avg.uv - 1 : null)],
  ["浏览量", n0(LY.pv), n0(today.pv), chgByCrc(today.pv / LY.pv - 1), chgByCrc(peer.peer_ly ? peer.avg.pv / peer.peer_ly.avg.pv - 1 : null)],
  ["销售额（元）", money(LY.payAmt), money(today.payAmt), chgByCrc(today.payAmt / LY.payAmt - 1), chgByCrc(peer.peer_ly ? peer.avg.payAmt / peer.peer_ly.avg.payAmt - 1 : null)],
  ["买东西的人数", n0(LY.payByrCnt), n0(today.payByrCnt), chgByCrc(LY.payByrCnt ? today.payByrCnt / LY.payByrCnt - 1 : null), chgByCrc(peer.peer_ly ? peer.avg.payUsr / peer.peer_ly.avg.payUsr - 1 : null)],
  ["成交转化率", dec(pct(LY.payRate)) + "%", dec(pct(today.payRate)) + "%", chgPP(today.payRate, LY.payRate), peer.peer_ly ? chgPP(peer.avg.tcr, peer.peer_ly.avg.tcr) : { text: "—", color: FLAT }],
], [22, 20, 20, 19, 19]));
if (ys.note) c.push(note(ys.note));

/* 四、近 7 日走势 */
const t7 = D.trend7;
c.push(h1(t7.title));
c.push(P(t7.intro));
c.push(...img("trend_7d.png", 620, 290, t7.chart_caption));

/* 五、漏斗 + 流量指标 */
const fn = D.funnel;
c.push(h1(fn.title));
c.push(P(fn.intro));
c.push(...img("funnel.png", 620, 270, fn.chart_caption));
const crc = M.crc;
c.push(table(["指标", "昨天", "环比昨天", "上周同日", "去年同日", "同比"], [
  ["进店人数", n0(today.uv), chgByCrc(crc.uv), n0(PW.uv), n0(LY.uv), chgByCrc(today.uv / LY.uv - 1)],
  ["浏览量", n0(today.pv), chgByCrc(crc.pv), n0(PW.pv), n0(LY.pv), chgByCrc(today.pv / LY.pv - 1)],
  ["商品页进店", n0(today.itmUv), chgByCrc(crc.itmUv), { text: "—", color: FLAT }, n0(LY.itmUv), chgByCrc(today.itmUv / LY.itmUv - 1)],
  ["新客人", n0(today.newUv), chgByCrc(crc.newUv), { text: "—", color: FLAT }, n0(LY.newUv), chgByCrc(today.newUv / LY.newUv - 1)],
  ["老客人", n0(today.oldUv), chgByCrc(crc.oldUv), { text: "—", color: FLAT }, n0(LY.oldUv), chgByCrc(today.oldUv / LY.oldUv - 1)],
  ["直播间人数", n0(today.liveUv), chgByCrc(crc.liveUv), n0(PW.liveUv), n0(LY.liveUv), chgByCrc(today.liveUv / LY.liveUv - 1)],
  ["短视频人数", n0(today.svUv), chgByCrc(crc.svUv), n0(PW.svUv), n0(LY.svUv), chgByCrc(today.svUv / LY.svUv - 1)],
  ["加购人数", n0(today.cartByr), chgByCrc(crc.cartByr), { text: "—", color: FLAT }, n0(LY.cartByr), chgByCrc(today.cartByr / LY.cartByr - 1)],
  ["跳失率", dec(pct(today.bounceRate)) + "%", chgByCrc(crc.bounceRate, true), { text: "—", color: FLAT }, dec(pct(LY.bounceRate)) + "%", chgPP(today.bounceRate, LY.bounceRate)],
], [20, 13, 15, 13, 13, 14]));

/* 六、渠道 */
const chs = D.channels;
c.push(h1(chs.title));
c.push(P(chs.intro));
c.push(...img("channel_donut.png", 500, 370, chs.donut_caption));
const srcRows = chs.rows.map((s) => [
  s.name, { text: n0(s.uv), align: AlignmentType.RIGHT }, chgByCrc(s.uv_wow_crc),
  { text: n0(s.uv_ly), align: AlignmentType.RIGHT }, chgByCrc(s.uv / s.uv_ly - 1),
  { text: money(s.pay), align: AlignmentType.RIGHT }, chgByCrc(s.pay_wow_crc),
  { text: s.pay_ly > 0 ? money(s.pay_ly) : "0.00", align: AlignmentType.RIGHT }, s.pay_ly > 0 ? chgByCrc(s.pay / s.pay_ly - 1) : { text: "新增", color: GOOD, bold: true, align: AlignmentType.RIGHT },
]);
const tt = chs.total;
srcRows.push([
  { text: "全店合计（去重）", bold: true, fill: TOT }, { text: n0(tt.uv), bold: true, fill: TOT, align: AlignmentType.RIGHT }, { ...chgByCrc(tt.uv_wow_crc), fill: TOT },
  { text: n0(tt.uv_ly), bold: true, fill: TOT, align: AlignmentType.RIGHT }, { ...chgByCrc(tt.uv / tt.uv_ly - 1), fill: TOT },
  { text: money(tt.pay), bold: true, fill: TOT, align: AlignmentType.RIGHT }, { ...chgByCrc(tt.pay_wow_crc), fill: TOT },
  { text: money(tt.pay_ly), bold: true, fill: TOT, align: AlignmentType.RIGHT }, { ...chgByCrc(tt.pay / tt.pay_ly - 1), fill: TOT },
]);
c.push(table(["入口", "进店人数", "比上周同日", "去年人数", "比去年", "带动成交（元）", "比上周同日", "去年成交", "比去年"], srcRows, [15, 9, 11, 9, 10, 13, 11, 11, 11]));
if (chs.note) c.push(note(chs.note));

/* 七、商品 */
const it = D.items;
c.push(h1(it.title));
c.push(P(it.intro));
c.push(...img("item_top.png", 620, 260, it.chart_caption));
c.push(...img(it.chart2, 620, 300, it.chart2_caption));

/* 八、同行 */
c.push(h1(peer.title));
c.push(P(peer.intro));
c.push(...img("peer_compare.png", 620, 290, peer.chart_caption));
c.push(table(["指标", "本店", "同行平均", "同行优秀", "本店/平均"], [
  ["进店人数", n0(peer.self.uv), n0(peer.avg.uv), n0(peer.good.uv), dec(peer.self.uv / peer.avg.uv * 100, 1) + "%"],
  ["浏览量", n0(peer.self.pv), n0(peer.avg.pv), n0(peer.good.pv), dec(peer.self.pv / peer.avg.pv * 100, 1) + "%"],
  ["销售额（元）", money(peer.self.payAmt), money(peer.avg.payAmt), money(peer.good.payAmt), dec(peer.self.payAmt / peer.avg.payAmt * 100, 1) + "%"],
  ["买东西的人数", n0(peer.self.payUsr), n0(peer.avg.payUsr), n0(peer.good.payUsr), dec(peer.self.payUsr / peer.avg.payUsr * 100, 1) + "%"],
  ["成交转化率", dec(pct(peer.self.tcr)) + "%", dec(pct(peer.avg.tcr)) + "%", dec(pct(peer.good.tcr)) + "%", { text: ((peer.self.tcr - peer.avg.tcr) * 100).toFixed(2) + "pp", color: BAD, bold: true, align: AlignmentType.RIGHT }],
  ["退款（元）", money(peer.self.rfd), money(peer.avg.rfd), money(peer.good.rfd), { text: "越低越好", color: FLAT, italics: true, align: AlignmentType.RIGHT }],
], [24, 18, 18, 18, 12]));

/* 九、坑 */
c.push(h1(D.pitfalls_title));
D.pitfalls.forEach((p) => c.push(bullet([{ text: p.lead, bold: true, color: "WARN" }, { text: p.body }])));

/* 十、口径 */
c.push(h1(D.caliber_title));
D.caliber.forEach((t) => c.push(bullet(t)));

const doc = new Document({
  styles: { default: { document: { run: { font: F, size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, color: PRI, font: F }, paragraph: { spacing: { before: 320, after: 140 } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, color: "2E5496", font: F }, paragraph: { spacing: { before: 220, after: 100 } } },
    ] },
  numbering: { config: [{ reference: "dr-b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "第 ", size: 18, color: "808080", font: F }), new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: F }),
      new TextRun({ text: " 页 / 共 ", size: 18, color: "808080", font: F }), new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: "808080", font: F }),
      new TextRun({ text: " 页", size: 18, color: "808080", font: F }) ] })] }) },
    children: c }],
});
Packer.toBuffer(doc).then((buf) => {
  // 即将在本地创建/覆盖 .docx 报表文件——不上传、不外发。
  if (fs.existsSync(OUT)) console.log("[write] 已存在，将被覆盖 ->", OUT);
  else console.log("[write] 新建 ->", OUT);
  fs.writeFileSync(OUT, buf);
  console.log("OK", OUT, buf.length, "bytes");
}).catch((e) => { console.error("FAIL", e); process.exit(1); });
