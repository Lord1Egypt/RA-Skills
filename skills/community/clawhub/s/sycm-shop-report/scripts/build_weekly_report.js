/*
 * 本脚本是 sycm-shop-report 流水线的【第 3 步 · docx 装配（周报）】。
 * 职责范围：读 weekly_data.json（或 example）与已生成的 PNG，产出中文 .docx 到 output_dir
 * 不做：不 fetch 网络、不调 MCP、不生成图表、不上传任何数据
 * 完整端到端流程见 SKILL.md 的「流水线」段与「工作流」清单。
 */
/* 周报 docx 生成器（数据驱动）。
 * 读取同目录 weekly_data.json（不存在则用 weekly_data.example.json），
 * 图表读 <output_dir>/<charts_subdir>/*.png（先跑 build_weekly_charts.py）。
 * 布局/配色/字体锁死在此文件；换店铺换周期只改 JSON。
 * 用法： NODE_PATH="<全局node_modules>" node build_weekly_report.js [数据json路径]
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
const dataPath = arg || (fs.existsSync(path.join(HERE, "weekly_data.json")) ? path.join(HERE, "weekly_data.json") : path.join(HERE, "weekly_data.example.json"));
const D = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const SHOP = D.shop_name;
const OUTDIR = D.output_dir;
const CH = path.join(OUTDIR, D.charts_subdir || "charts_week").replace(/\\/g, "/");
const OUT = `${OUTDIR}/${SHOP}-店铺经营周报-${D.period.file_range}.docx`;
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
function chgPP(cur, base) { const d = (cur - base) * 100; return { text: (d >= 0 ? "+" : "−") + Math.abs(d).toFixed(2) + "pp", color: d >= 0 ? GOOD : BAD, bold: true, align: AlignmentType.RIGHT }; }
function growthPct(cur, base) { return base ? cur / base - 1 : null; }

const SP = { before: 60, after: 60, line: 300 };
function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 140 }, children: [new TextRun({ text, bold: true, size: 30, color: PRI, font: F })] }); }
function h2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 220, after: 100 }, children: [new TextRun({ text, bold: true, size: 24, color: "2E5496", font: F })] }); }
function P(runs, align) { return new Paragraph({ spacing: SP, alignment: align || AlignmentType.JUSTIFIED, children: (typeof runs === "string" ? [{ text: runs }] : runs).map((r) => new TextRun({ text: r.text, size: r.size || 21, bold: !!r.bold, italics: !!r.italics, color: colOf(r), font: F })) }); }
function bullet(runs) { const children = (typeof runs === "string" ? [{ text: runs }] : runs).map((r) => new TextRun({ text: r.text, size: r.size || 21, bold: !!r.bold, color: colOf(r), font: F })); return new Paragraph({ numbering: { reference: "wr-b", level: 0 }, spacing: { before: 40, after: 40, line: 300 }, alignment: AlignmentType.JUSTIFIED, children }); }
function note(text) { return new Paragraph({ spacing: { before: 80, after: 120, line: 280 }, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text, size: 18, italics: true, color: "808080", font: F })] }); }
function img(file, w, h, cap) {
  const p = `${CH}/${file}`; if (!fs.existsSync(p)) return [];
  const items = [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: cap ? 40 : 160 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(p), transformation: { width: w, height: h } })] })];
  if (cap) items.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 180, line: 260 }, children: [new TextRun({ text: cap, size: 18, italics: true, color: "7A7A7A", font: F })] }));
  return items;
}

const CONTENT_W = 9638;
function table(headers, rows, widths) {
  if (!widths) widths = headers.map(() => 100 / headers.length);
  const scale = CONTENT_W / widths.reduce((a, b) => a + b, 0);
  const cw = widths.map((w) => Math.round(w * scale)); cw[cw.length - 1] += CONTENT_W - cw.reduce((a, b) => a + b, 0);
  const head = new TableRow({ tableHeader: true, children: headers.map((t, i) => new TableCell({ width: { size: cw[i], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "1F3864" }, margins: { top: 70, bottom: 70, left: 90, right: 90 }, children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: { before: 0, after: 0, line: 240 }, children: [new TextRun({ text: t, bold: true, size: 19, color: "FFFFFF", font: F })] })] })) });
  const body = rows.map((row, ri) => new TableRow({ children: row.map((cell, ci) => { const m = typeof cell === "object" && cell !== null ? cell : { text: String(cell) }; return new TableCell({ width: { size: cw[ci], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: m.fill || (ri % 2 ? "F2F5FA" : "FFFFFF") }, margins: { top: 60, bottom: 60, left: 90, right: 90 }, children: [new Paragraph({ alignment: m.align || (ci === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT), spacing: { before: 0, after: 0, line: 240 }, children: [new TextRun({ text: m.text, size: m.size || 19, bold: !!m.bold, italics: !!m.italics, color: m.color || "333333", font: F })] })] }); }) }));
  return new Table({ columnWidths: cw, width: { size: CONTENT_W, type: WidthType.DXA }, borders: { top: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, left: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, right: { style: BorderStyle.SINGLE, size: 4, color: "BFC9D9" }, insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "DCE3ED" }, insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "DCE3ED" } }, rows: [head, ...body] });
}
const TOT = "E8EEF7";

function kpiCard(card) {
  return new TableCell({ width: { size: Math.round(CONTENT_W / 4), type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "FFFFFF" }, margins: { top: 160, bottom: 160, left: 160, right: 160 }, verticalAlign: VerticalAlign.CENTER,
    borders: { top: { style: BorderStyle.SINGLE, size: 20, color: card.accent, space: 0 }, left: { style: BorderStyle.SINGLE, size: 4, color: "E5E9F0" }, right: { style: BorderStyle.SINGLE, size: 4, color: "E5E9F0" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "E5E9F0" } },
    children: [
      new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 30 }, children: [new TextRun({ text: card.label, size: 18, color: "666666", font: F })] }),
      new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 40 }, children: [new TextRun({ text: card.value, size: 36, bold: true, color: PRI, font: F })] }),
      ...card.deltas.map((d) => new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 14 }, children: [new TextRun({ text: d.k + "  ", size: 16, color: "888888", font: F }), new TextRun({ text: d.v, size: 17, bold: true, color: d.dir === "up" ? GOOD : d.dir === "down" ? BAD : PRI, font: F })] })),
    ] });
}
function kpiDashboard() { return new Table({ columnWidths: D.kpi_cards.map(() => Math.round(CONTENT_W / 4)), width: { size: CONTENT_W, type: WidthType.DXA }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.SINGLE, size: 8, color: "FFFFFF" } }, rows: [new TableRow({ children: D.kpi_cards.map(kpiCard) })] }); }

/* ================= 正文 ================= */
const M = D.metrics, SELF = M.self, PREV = M.prev, LY = M.last_year;
const c = [];
c.push(new Paragraph({ spacing: { before: 0, after: 60 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${SHOP} · 店铺经营周报`, bold: true, size: 40, color: PRI, font: F })] }));
c.push(new Paragraph({ spacing: { before: 0, after: 40 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: `统计周期：${D.period.start}（周一）— ${D.period.end}（周日）　环比：${D.period.prev_start} ~ ${D.period.prev_end}　同比：${D.period.yoy_start} ~ ${D.period.yoy_end}`, size: 20, color: "444444", font: F })] }));
c.push(new Paragraph({ spacing: { before: 0, after: 200 }, alignment: AlignmentType.CENTER, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: PRI, space: 8 } }, children: [new TextRun({ text: `${D.period.data_source_line}　报告生成：${D.generated_at}`, size: 18, color: "888888", font: F })] }));

/* 一、结论 */
c.push(h1("一、这周卖得怎么样"));
c.push(kpiDashboard());
c.push(new Paragraph({ spacing: { before: 60, after: 200 }, children: [new TextRun({ text: "", font: F })] }));
c.push(P(D.headline));
c.push(P([{ text: D.signals_title, bold: true }]));
D.signals.forEach((s) => c.push(bullet([{ text: s.lead, bold: true, color: s.color || "BAD" }, { text: s.body }])));

/* 二、行动建议 */
c.push(h1(D.actions_title));
c.push(P(D.actions_intro));
D.actions.forEach((a) => {
  c.push(h2(a.title));
  c.push(bullet([{ text: "为什么要做：", bold: true }, { text: a.why }]));
  c.push(bullet([{ text: "怎么做：", bold: true }, { text: a.how }]));
  c.push(bullet([{ text: "目标：", bold: true }, { text: a.goal }]));
});
if (D.actions_table && D.actions_table.length) {
  c.push(new Paragraph({ spacing: { before: 160, after: 80 }, children: [new TextRun({ text: "责任与截止时间一览", bold: true, size: 22, color: "2E5496", font: F })] }));
  c.push(table(["#", "事项", "负责人", "截止时间", "交付物 / 验收标准"],
    D.actions_table.map((r, i) => [String(i + 1), { text: r.task, align: AlignmentType.LEFT }, { text: r.owner, align: AlignmentType.LEFT }, { text: r.deadline, align: AlignmentType.LEFT }, { text: r.deliverable, align: AlignmentType.LEFT }]),
    [5, 26, 14, 16, 39]));
}

/* 三、三期对比 */
const c3 = D.compare3;
c.push(h1(c3.title)); c.push(P(c3.intro)); c.push(...img("week_compare_3.png", 620, 300, c3.chart_caption));
c.push(table(["核心指标", "本周", "环比上周", "去年同周", "同比去年"], [
  ["支付金额（元）", money(SELF.payAmt), chgByCrc(growthPct(SELF.payAmt, PREV.payAmt)), money(LY.payAmt), chgByCrc(growthPct(SELF.payAmt, LY.payAmt))],
  ["进店人数", n0(SELF.uv), chgByCrc(growthPct(SELF.uv, PREV.uv)), n0(LY.uv), chgByCrc(growthPct(SELF.uv, LY.uv))],
  ["买东西的人数", n0(SELF.payByrCnt), chgByCrc(growthPct(SELF.payByrCnt, PREV.payByrCnt)), n0(LY.payByrCnt), chgByCrc(growthPct(SELF.payByrCnt, LY.payByrCnt))],
  ["成交转化率", dec(pct(SELF.payRate)) + "%", chgPP(SELF.payRate, PREV.payRate), dec(pct(LY.payRate)) + "%", chgPP(SELF.payRate, LY.payRate)],
  ["客单价（元）", money(SELF.payPct), chgByCrc(growthPct(SELF.payPct, PREV.payPct)), money(LY.payPct), chgByCrc(growthPct(SELF.payPct, LY.payPct))],
  ["净销售额（元）", money(SELF.realPayAmt), chgByCrc(growthPct(SELF.realPayAmt, PREV.realPayAmt)), money(LY.realPayAmt), chgByCrc(growthPct(SELF.realPayAmt, LY.realPayAmt))],
  ["退款金额（元）", money(SELF.rfdAmt), chgByCrc(growthPct(SELF.rfdAmt, PREV.rfdAmt), true), money(LY.rfdAmt), chgByCrc(growthPct(SELF.rfdAmt, LY.rfdAmt), true)],
  ["退款率", dec(pct(SELF.rfdAmt / SELF.payAmt)) + "%", chgPP(SELF.rfdAmt / SELF.payAmt, PREV.rfdAmt / PREV.payAmt), dec(pct(LY.rfdAmt / LY.payAmt)) + "%", chgPP(SELF.rfdAmt / SELF.payAmt, LY.rfdAmt / LY.payAmt)],
], [24, 20, 18, 20, 18]));
if (c3.note) c.push(note(c3.note));

/* 四、环比 vs 同比 */
const gs = D.growth_story; c.push(h1(gs.title)); c.push(P(gs.intro)); c.push(...img("week_growth_story.png", 620, 300, gs.chart_caption));

/* 五、每日走势 */
const wt = D.week_trend; c.push(h1(wt.title)); c.push(P(wt.intro)); c.push(...img("week_trend.png", 620, 300, wt.chart_caption));

/* 六、流量与转化 */
const tt = D.traffic_table; c.push(h1(tt.title)); c.push(P(tt.intro));
c.push(table(["指标", "本周", "环比上周", "去年同周", "同比去年"], [
  ["进店人数", n0(SELF.uv), chgByCrc(growthPct(SELF.uv, PREV.uv)), n0(LY.uv), chgByCrc(growthPct(SELF.uv, LY.uv))],
  ["浏览量", n0(SELF.pv), chgByCrc(growthPct(SELF.pv, PREV.pv)), n0(LY.pv), chgByCrc(growthPct(SELF.pv, LY.pv))],
  ["商品页进店", n0(SELF.itmUv), chgByCrc(growthPct(SELF.itmUv, PREV.itmUv)), n0(LY.itmUv), chgByCrc(growthPct(SELF.itmUv, LY.itmUv))],
  ["新客人", n0(SELF.newUv), chgByCrc(growthPct(SELF.newUv, PREV.newUv)), n0(LY.newUv), chgByCrc(growthPct(SELF.newUv, LY.newUv))],
  ["老客人", n0(SELF.oldUv), chgByCrc(growthPct(SELF.oldUv, PREV.oldUv)), n0(LY.oldUv), chgByCrc(growthPct(SELF.oldUv, LY.oldUv))],
  ["加购人数", n0(SELF.cartByr), chgByCrc(growthPct(SELF.cartByr, PREV.cartByr)), n0(LY.cartByr), chgByCrc(growthPct(SELF.cartByr, LY.cartByr))],
  ["直播间人数", n0(SELF.liveUv), chgByCrc(growthPct(SELF.liveUv, PREV.liveUv)), n0(LY.liveUv), chgByCrc(growthPct(SELF.liveUv, LY.liveUv))],
  ["短视频人数", n0(SELF.svUv), chgByCrc(growthPct(SELF.svUv, PREV.svUv)), n0(LY.svUv), chgByCrc(growthPct(SELF.svUv, LY.svUv))],
  ["跳失率", dec(pct(SELF.bounceRate)) + "%", chgPP(SELF.bounceRate, PREV.bounceRate), { text: "—", color: FLAT }, { text: "—", color: FLAT }],
], [22, 16, 18, 16, 18]));

/* 七、渠道 */
const chs = D.channels; c.push(h1(chs.title)); c.push(P(chs.intro)); c.push(...img("week_channel_donut.png", 500, 370, chs.donut_caption));
const srcRows = chs.rows.map((s) => [
  s.name, { text: n0(s.uv), align: AlignmentType.RIGHT }, chgByCrc(growthPct(s.uv, s.uv_prev)), chgByCrc(growthPct(s.uv, s.uv_ly)),
  { text: money(s.pay), align: AlignmentType.RIGHT }, chgByCrc(growthPct(s.pay, s.pay_prev)), chgByCrc(growthPct(s.pay, s.pay_ly)),
]);
srcRows.push([
  { text: "全店合计（周去重）", bold: true, fill: TOT }, { text: n0(SELF.uv), bold: true, fill: TOT, align: AlignmentType.RIGHT },
  { ...chgByCrc(growthPct(SELF.uv, PREV.uv)), fill: TOT }, { ...chgByCrc(growthPct(SELF.uv, LY.uv)), fill: TOT },
  { text: money(SELF.payAmt), bold: true, fill: TOT, align: AlignmentType.RIGHT }, { ...chgByCrc(growthPct(SELF.payAmt, PREV.payAmt)), fill: TOT }, { ...chgByCrc(growthPct(SELF.payAmt, LY.payAmt)), fill: TOT },
]);
c.push(table(["入口", "本周人数", "比上周", "比去年", "带动成交（元）", "比上周", "比去年"], srcRows, [16, 13, 12, 12, 17, 12, 12]));
if (chs.note) c.push(note(chs.note));
c.push(...img("week_channel_yoy.png", 620, 300, chs.chart2_caption));

/* 八、退款 */
const rf = D.refund; c.push(h1(rf.title)); c.push(P(rf.intro)); c.push(...img("week_refund.png", 620, 260, rf.chart_caption));

/* 九、同行 */
const pe = D.peer; c.push(h1(pe.title)); c.push(P(pe.intro));
c.push(table(["七天累加起来看", "本店", "同行平均", "同行优秀", "我们/平均"], [
  ["进店人数（人次）", n0(pe.uv_sum.self), n0(pe.uv_sum.avg), n0(pe.uv_sum.good), dec(pe.uv_sum.self / pe.uv_sum.avg * 100, 1) + "%"],
  ["销售额（元）", money(pe.pay_sum.self), money(pe.pay_sum.avg), money(pe.pay_sum.good), dec(pe.pay_sum.self / pe.pay_sum.avg * 100, 1) + "%"],
  ["买东西的人数", n0(pe.byr_sum.self), n0(pe.byr_sum.avg), n0(pe.byr_sum.good), dec(pe.byr_sum.self / pe.byr_sum.avg * 100, 1) + "%"],
  ["成交转化率", dec(pct(SELF.payRate)) + "%", dec(pct(pe.rate_avg)) + "%", dec(pct(pe.rate_good)) + "%", { text: chgPP(SELF.payRate, pe.rate_avg).text, color: BAD, bold: true, align: AlignmentType.RIGHT }],
], [24, 18, 18, 18, 12]));
if (pe.note) c.push(note(pe.note));

/* 十、坑 */
c.push(h1(D.pitfalls_title));
D.pitfalls.forEach((p) => c.push(bullet([{ text: p.lead, bold: true, color: "WARN" }, { text: p.body }])));

/* 十一、口径 */
c.push(h1(D.caliber_title));
D.caliber.forEach((t) => c.push(bullet(t)));

const doc = new Document({
  creator: SHOP, title: `${SHOP} 店铺经营周报 ${D.period.start} ~ ${D.period.end}`,
  styles: { default: { document: { run: { font: F, size: 21 } } }, paragraphStyles: [
    { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, color: PRI, font: F }, paragraph: { spacing: { before: 320, after: 140 } } },
    { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, color: "2E5496", font: F }, paragraph: { spacing: { before: 220, after: 100 } } } ] },
  numbering: { config: [{ reference: "wr-b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
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
