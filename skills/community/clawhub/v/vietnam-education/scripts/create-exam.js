#!/usr/bin/env node
/**
 * TẠO BỘ ĐỀ KIỂM TRA CHUẨN CV 7991/BGDĐT-GDTrH
 * Xuất 3 file .docx riêng biệt, có đánh số trang:
 *   File 1: Ma trận + Bản đặc tả
 *   File 2: Đề kiểm tra
 *   File 3: Đáp án + Hướng dẫn chấm
 *
 * Cài đặt: npm install -g docx
 * Chạy:    node create-exam.js
 */
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak,
  TabStopType, Footer, PageNumber, NumberFormat } = require("docx");

// ══ CẤU HÌNH ══
const CONFIG = {
  school: "TRƯỜNG THPT ...", dept: "TỔ TOÁN",
  examType: "GIỮA HỌC KÌ I", year: "2025-2026",
  subject: "TOÁN", grade: "10", duration: "90", totalPages: "03",
};

// ══ CHỦ ĐỀ + MA TRẬN ══
const topics = [
  { name: "Mệnh đề và tập hợp", lessons: "Bài 1, 2, 3", tiets: 12,
    nlc_nb: 4, nlc_th: 2, nlc_vd: 0, ds_count: 1, tln_vd: 2,
    tl: [{ level: "vd", points: 1.0 }],
    yccd: ["Nhận biết được khái niệm mệnh đề, tập hợp, tập hợp con.",
           "Xác định được tính đúng/sai của mệnh đề; liệt kê phần tử tập hợp.",
           "Vận dụng kiến thức mệnh đề, tập hợp giải bài toán."] },
  { name: "Các phép toán tập hợp", lessons: "Bài 4, 5, 6", tiets: 10,
    nlc_nb: 2, nlc_th: 2, nlc_vd: 2, ds_count: 1, tln_vd: 2,
    tl: [{ level: "vd", points: 1.0 }, { level: "vdc", points: 1.0 }],
    yccd: ["Nhận biết được phép giao, hợp, hiệu, phần bù.",
           "Thực hiện được phép toán tập hợp; biểu diễn trên trục số.",
           "Vận dụng phép toán tập hợp giải bất phương trình, bài toán thực tế."] },
];

// ══ DỮ LIỆU ĐỀ ══
const MC = [
  { q: "Tập hợp nào sau đây có đúng một phần tử?", a: "{0}", b: "∅", c: "{∅}", d: "{0; 1}", da: "A" },
  { q: "Cho tập hợp A = {1; 2; 3; 4; 5}. Số tập hợp con của A có 2 phần tử là:", a: "5", b: "10", c: "15", d: "20", da: "B" },
  { q: "Mệnh đề nào sau đây là mệnh đề đúng?", a: "2 + 3 = 6", b: "√4 = ±2", c: "π là số vô tỉ", d: "0 là số tự nhiên lẻ", da: "C" },
  { q: "Phủ định của mệnh đề \"∀x ∈ ℝ: x² ≥ 0\" là:", a: "∀x ∈ ℝ: x² < 0", b: "∃x ∈ ℝ: x² < 0", c: "∃x ∈ ℝ: x² > 0", d: "∀x ∈ ℝ: x² ≤ 0", da: "B" },
  { q: "Cho A = {x ∈ ℤ | -2 < x ≤ 3}. Tập A bằng:", a: "{-2; -1; 0; 1; 2; 3}", b: "{-1; 0; 1; 2; 3}", c: "{-2; -1; 0; 1; 2}", d: "{-1; 0; 1; 2}", da: "B" },
  { q: "Tập hợp A ∩ B là tập hợp gồm các phần tử:", a: "thuộc A hoặc thuộc B", b: "thuộc A và thuộc B", c: "thuộc A mà không thuộc B", d: "không thuộc A và B", da: "B" },
  { q: "Cho A = {1; 2; 3}, B = {2; 3; 4; 5}. Tập A \\ B bằng:", a: "{1}", b: "{4; 5}", c: "{1; 2; 3; 4; 5}", d: "{2; 3}", da: "A" },
  { q: "Khoảng (-∞; 3) là tập hợp:", a: "{x ∈ ℝ | x ≤ 3}", b: "{x ∈ ℝ | x < 3}", c: "{x ∈ ℝ | x > 3}", d: "{x ∈ ℝ | x ≥ 3}", da: "B" },
  { q: "Tập hợp A ∪ B = ∅ khi và chỉ khi:", a: "A = ∅ và B = ∅", b: "A = ∅ hoặc B = ∅", c: "A ⊂ B", d: "A ∩ B = ∅", da: "A" },
  { q: "Cho A = (-1; 5], B = [3; 7). Tập A ∩ B bằng:", a: "[3; 5]", b: "(3; 5]", c: "[3; 5)", d: "(3; 5)", da: "A" },
  { q: "Số phần tử của tập hợp {x ∈ ℕ | x² - 5x + 6 = 0} là:", a: "0", b: "1", c: "2", d: "3", da: "C" },
  { q: "Mệnh đề \"Nếu n chia hết cho 6 thì n chia hết cho 3\" có mệnh đề đảo là:", a: "Nếu n không chia hết cho 6 thì n không chia hết cho 3", b: "Nếu n chia hết cho 3 thì n chia hết cho 6", c: "Nếu n không chia hết cho 3 thì n không chia hết cho 6", d: "n chia hết cho 6 khi và chỉ khi n chia hết cho 3", da: "B" },
];
const DS = [
  { stem: "Cho A = {1; 2; 3; 4; 5; 6}, B = {2; 4; 6; 8}. Xét tính đúng sai của các mệnh đề sau:",
    items: [{ t: "A ∩ B = {2; 4; 6}", ok: true }, { t: "A ∪ B = {1; 2; 3; 4; 5; 6; 8}", ok: true },
            { t: "A \\ B = {1; 3; 5; 8}", ok: false }, { t: "Tập B có đúng 15 tập hợp con", ok: false }] },
  { stem: "Xét tính đúng sai của các mệnh đề sau về tập hợp số:",
    items: [{ t: "ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ", ok: true }, { t: "√2 là số hữu tỉ", ok: false },
            { t: "Mọi số nguyên đều là số hữu tỉ", ok: true }, { t: "Tồn tại số thực x sao cho x² = -1", ok: false }] },
];
const TLN = [
  { q: "Cho A = {1; 2; 3; 4; 5}. Số tập hợp con của A là bao nhiêu?", da: "32" },
  { q: "Cho A = (-3; 5), B = [1; 7]. Tập A ∩ B = [a; b). Giá trị của a + b bằng bao nhiêu?", da: "6" },
  { q: "Phương trình x² - 7x + 12 = 0 có hai nghiệm x₁, x₂ (x₁ < x₂). Giá trị x₂ - x₁ bằng bao nhiêu?", da: "1" },
  { q: "Tập hợp {x ∈ ℤ | |x| ≤ 3} có bao nhiêu phần tử?", da: "7" },
];
const TL = [
  { q: "Cho A = {x ∈ ℝ | x² - 4x + 3 ≤ 0} và B = {x ∈ ℝ | x > 2}.\na) Xác định tập A.\nb) Tìm A ∩ B.", pt: "1,0",
    ans: [{ t: "a) x² - 4x + 3 ≤ 0 ⟺ (x - 1)(x - 3) ≤ 0 ⟺ 1 ≤ x ≤ 3.\nVậy A = [1; 3].", d: 0.5 },
          { t: "b) A ∩ B = [1; 3] ∩ (2; +∞) = (2; 3].", d: 0.5 }] },
  { q: "Cho hai tập hợp A = {x ∈ ℝ | 2x - 1 > 0} và B = (-∞; 3].\na) Xác định tập A.\nb) Tìm A \\ B.", pt: "1,0",
    ans: [{ t: "a) 2x - 1 > 0 ⟺ x > 1/2.\nVậy A = (1/2; +∞).", d: 0.5 },
          { t: "b) A \\ B = (1/2; +∞) \\ (-∞; 3] = (3; +∞).", d: 0.5 }] },
  { q: "Một lớp có 40 học sinh, trong đó 25 em thích môn Toán, 20 em thích môn Vật lí, 10 em thích cả hai môn. Hỏi có bao nhiêu em không thích môn nào trong hai môn trên?", pt: "1,0",
    ans: [{ t: "Gọi A là tập học sinh thích Toán, B là tập học sinh thích Vật lí.\n|A ∪ B| = |A| + |B| - |A ∩ B| = 25 + 20 - 10 = 35.", d: 0.5 },
          { t: "Số học sinh không thích môn nào = 40 - 35 = 5 (em).", d: 0.5 }] },
];

// ══ HELPERS ══
const F = "Times New Roman", SZ = 26, ST = 28, SS = 24, SX = 20;
const CW = 9354;
const nb = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const nbs = { top: nb, bottom: nb, left: nb, right: nb };
const bd = (() => { const b = { style: BorderStyle.SINGLE, size: 1, color: "000000" }; return { top:b, bottom:b, left:b, right:b }; })();
const sh = { fill: "D9E2F3", type: ShadingType.CLEAR };
const sl = { fill: "F2F2F2", type: ShadingType.CLEAR };

function P(text, o={}) {
  const runs = typeof text === "string"
    ? [new TextRun({ text, font: F, size: o.s||SZ, bold: !!o.b, italics: !!o.i })]
    : text.map(t => new TextRun({ text: t.t, font: F, size: t.s||o.s||SZ, bold: !!t.b, italics: !!t.i }));
  return new Paragraph({ alignment: o.a||AlignmentType.LEFT,
    spacing: { before: o.bf||0, after: o.af||0, line: o.ln||276 },
    tabStops: o.tabs, children: runs });
}
function C(ch, w, o={}) {
  const children = typeof ch === "string" ? [P(ch, { a: o.a, s: o.s||SX, b: o.b })] : ch;
  return new TableCell({ width: { size: w, type: WidthType.DXA },
    borders: o.nb ? nbs : bd, margins: { top: 30, bottom: 30, left: 60, right: 60 },
    verticalAlign: "center", shading: o.sh, children });
}
function pp(n=1) {
  return {
    page: { size: { width: 11906, height: 16838 },
            margin: { top: 1134, bottom: 1134, left: 1418, right: 1134 } },
    footers: { default: new Footer({ children: [
      new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ children: [PageNumber.CURRENT], font: F, size: SS }) ] }) ] }) },
    pageNumberStart: n, pageNumberFormatType: NumberFormat.DECIMAL,
  };
}
async function save(ch, fn, pg=1) {
  const doc = new Document({ styles: { default: { document: { run: { font: F, size: SZ } } } },
    sections: [{ properties: pp(pg), children: ch }] });
  fs.writeFileSync(fn, await Packer.toBuffer(doc));
  return fn;
}

// ══ FILE 1: MA TRẬN + ĐẶC TẢ ══
function f1() {
  const ch = [];
  ch.push(P("MA TRẬN ĐỀ KIỂM TRA " + CONFIG.examType.toUpperCase(), { a: AlignmentType.CENTER, b: true, s: ST, af: 30 }));
  ch.push(P(`Môn: ${CONFIG.subject} – Lớp: ${CONFIG.grade}`, { a: AlignmentType.CENTER, b: true, af: 20 }));
  ch.push(P(`Thời gian làm bài: ${CONFIG.duration} phút (không kể thời gian phát đề)`, { a: AlignmentType.CENTER, i: true, s: SS, af: 60 }));

  const w = [2200, 900, 700, 700, 700, 700, 700, 700, 700, 700, 654];
  const H = (t,ww,o={}) => C([P(t,{a:AlignmentType.CENTER,s:SX,b:true})],ww,{sh,...o});
  const hr1 = new TableRow({ children: [H("Nội dung",w[0]), H("Số tiết",w[1]),
    H("Nhận biết",w[2]+w[3]), H("Thông hiểu",w[4]+w[5]),
    H("Vận dụng",w[6]+w[7]), H("VD cao",w[8]+w[9]), H("Tổng số câu\n/Tổng điểm",w[10])] });
  const hr2 = new TableRow({ children: [C("",w[0],{sh:sl}), C("",w[1],{sh:sl}),
    H("TN",w[2],{sh:sl}),H("TL",w[3],{sh:sl}),H("TN",w[4],{sh:sl}),H("TL",w[5],{sh:sl}),
    H("TN",w[6],{sh:sl}),H("TL",w[7],{sh:sl}),H("TN",w[8],{sh:sl}),H("TL",w[9],{sh:sl}),
    C("",w[10],{sh:sl})] });

  const trs = topics.map(t => {
    const numNLC = t.nlc_nb+t.nlc_th+t.nlc_vd;
    const numTL = t.tl?t.tl.length:0;
    const totalQ = numNLC + (t.ds_count||0) + (t.tln_vd||0) + numTL;
    const ptNLC = numNLC*0.25, ptDS = (t.ds_count||0)*1.0, ptTLN = (t.tln_vd||0)*0.5;
    const ptTL = t.tl?t.tl.reduce((s,x)=>s+x.points,0):0;
    const totalPt = ptNLC+ptDS+ptTLN+ptTL;
    const vdTL = t.tl?t.tl.filter(x=>x.level==="vd").length:0;
    const vdcTL = t.tl?t.tl.filter(x=>x.level==="vdc").length:0;
    return new TableRow({ children: [
      C([P(t.name,{s:SX,b:true})],w[0]), C(String(t.tiets),w[1],{a:AlignmentType.CENTER}),
      C(t.nlc_nb?String(t.nlc_nb):"",w[2],{a:AlignmentType.CENTER}), C("",w[3],{a:AlignmentType.CENTER}),
      C(t.nlc_th||(t.ds_count||0)?String(t.nlc_th+(t.ds_count||0)*2):"",w[4],{a:AlignmentType.CENTER}),
      C("",w[5],{a:AlignmentType.CENTER}),
      C(t.nlc_vd||(t.tln_vd||0)?String(t.nlc_vd+(t.tln_vd||0)+(t.ds_count||0)*2):"",w[6],{a:AlignmentType.CENTER}),
      C(vdTL?String(vdTL):"",w[7],{a:AlignmentType.CENTER}),
      C("",w[8],{a:AlignmentType.CENTER}),
      C(vdcTL?String(vdcTL):"",w[9],{a:AlignmentType.CENTER}),
      C([P(`${totalQ} câu`,{a:AlignmentType.CENTER,s:SX,b:true}),P(`${totalPt.toFixed(1)} điểm`,{a:AlignmentType.CENTER,s:18,i:true})],w[10]),
    ]});
  });

  const totalQ = MC.length+DS.length+TLN.length+TL.length;
  const sumR = new TableRow({ children: [
    C([P("Tổng",{a:AlignmentType.CENTER,s:SX,b:true})],w[0],{sh:sl}), C("",w[1],{sh:sl}),
    C([P("~40%",{a:AlignmentType.CENTER,s:SX,b:true})],w[2]+w[3],{sh:sl}),
    C([P("~30%",{a:AlignmentType.CENTER,s:SX,b:true})],w[4]+w[5],{sh:sl}),
    C([P("~20%",{a:AlignmentType.CENTER,s:SX,b:true})],w[6]+w[7],{sh:sl}),
    C([P("~10%",{a:AlignmentType.CENTER,s:SX,b:true})],w[8]+w[9],{sh:sl}),
    C([P(`${totalQ} câu\n10,0 điểm`,{a:AlignmentType.CENTER,s:SX,b:true})],w[10],{sh:sl}),
  ]});
  ch.push(new Table({ width:{size:CW,type:WidthType.DXA}, columnWidths:w, rows:[hr1,hr2,...trs,sumR] }));
  ch.push(P("",{bf:200}));

  // ── ĐẶC TẢ ──
  ch.push(P("BẢN ĐẶC TẢ ĐỀ KIỂM TRA " + CONFIG.examType.toUpperCase(), { a: AlignmentType.CENTER, b: true, s: ST, af: 30 }));
  ch.push(P(`Môn: ${CONFIG.subject} – Lớp: ${CONFIG.grade}`, { a: AlignmentType.CENTER, b: true, af: 60 }));

  const sw = [1800, 4200, 800, 800, 800, 954];
  const shr = new TableRow({ children: [H("Nội dung kiến thức",sw[0]),H("Yêu cầu cần đạt",sw[1]),
    H("NB",sw[2]),H("TH",sw[3]),H("VD + VDC",sw[4]),H("Câu hỏi",sw[5])] });
  let qi = 1;
  const srs = topics.map(t => {
    const yc = (t.yccd||[]).map(y => P("– "+y, {s:SX}));
    const numQ = (t.nlc_nb+t.nlc_th+t.nlc_vd)+(t.ds_count||0)+(t.tln_vd||0)+(t.tl?t.tl.length:0);
    const rng = numQ>1?`C${qi}–C${qi+numQ-1}`:`C${qi}`;
    qi += numQ;
    return new TableRow({ children: [
      C([P(t.name,{s:SX,b:true})],sw[0]),
      C(yc.length?yc:[P("[Yêu cầu cần đạt]",{s:SX,i:true})],sw[1]),
      C(String(t.nlc_nb),sw[2],{a:AlignmentType.CENTER}),
      C(String(t.nlc_th+(t.ds_count||0)),sw[3],{a:AlignmentType.CENTER}),
      C(String(t.nlc_vd+(t.tln_vd||0)+(t.tl?t.tl.length:0)),sw[4],{a:AlignmentType.CENTER}),
      C(rng,sw[5],{a:AlignmentType.CENTER}),
    ]});
  });
  ch.push(new Table({ width:{size:CW,type:WidthType.DXA}, columnWidths:sw, rows:[shr,...srs] }));
  return ch;
}

// ══ FILE 2: ĐỀ KIỂM TRA ══
function f2() {
  const ch = [], hw = Math.floor(CW/2);
  // Header
  ch.push(new Table({ width:{size:CW,type:WidthType.DXA}, columnWidths:[3800,5554], rows:[new TableRow({children:[
    C([P(CONFIG.school,{a:AlignmentType.CENTER,s:SS}),P(CONFIG.dept,{a:AlignmentType.CENTER,s:SS}),
       P("────────",{a:AlignmentType.CENTER,s:SX})],3800,{nb:true}),
    C([P("ĐỀ KIỂM TRA "+CONFIG.examType.toUpperCase(),{a:AlignmentType.CENTER,s:ST,b:true}),
       P("NĂM HỌC: "+CONFIG.year,{a:AlignmentType.CENTER}),
       P(`Môn: ${CONFIG.subject} – Lớp: ${CONFIG.grade}`,{a:AlignmentType.CENTER,b:true}),
       P(`Thời gian làm bài: ${CONFIG.duration} phút (không kể thời gian phát đề)`,{a:AlignmentType.CENTER,i:true,s:SS}),
       P(`(Đề gồm ${CONFIG.totalPages} trang)`,{a:AlignmentType.CENTER,s:SX,i:true})],5554,{nb:true}),
  ]})]}) );
  ch.push(P("",{bf:80}));
  ch.push(P("PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (7,0 điểm)",{b:true,bf:80,af:40}));

  // A
  ch.push(P([{t:"A. Câu trắc nghiệm nhiều lựa chọn ",b:true,i:true},{t:"(Thí sinh chọn một đáp án đúng. Mỗi câu đúng được 0,25 điểm)",i:true,s:SS}],{af:40}));
  MC.forEach((m,i) => {
    ch.push(P([{t:`Câu ${i+1}. `,b:true},{t:m.q}],{bf:50}));
    ch.push(P([{t:`     A. ${m.a}`},{t:`\tB. ${m.b}`}],{tabs:[{type:TabStopType.LEFT,position:hw}]}));
    ch.push(P([{t:`     C. ${m.c}`},{t:`\tD. ${m.d}`}],{tabs:[{type:TabStopType.LEFT,position:hw}]}));
  });
  ch.push(P("",{bf:60}));

  // B
  ch.push(P([{t:"B. Câu trắc nghiệm đúng – sai ",b:true,i:true},{t:"(Mỗi câu có 4 ý a, b, c, d. Học sinh chọn Đúng hoặc Sai. Mỗi ý đúng được 0,25 điểm)",i:true,s:SS}],{af:40}));
  DS.forEach((d,i) => {
    const qn = MC.length+i+1;
    ch.push(P([{t:`Câu ${qn}. `,b:true},{t:d.stem}],{bf:50}));
    const cw = [5854,1750,1750];
    ch.push(new Table({ width:{size:CW,type:WidthType.DXA}, columnWidths:cw, rows:[
      new TableRow({children:[C([P("Mệnh đề",{a:AlignmentType.CENTER,s:SS,b:true})],cw[0]),
        C([P("Đúng",{a:AlignmentType.CENTER,s:SS,b:true})],cw[1]),
        C([P("Sai",{a:AlignmentType.CENTER,s:SS,b:true})],cw[2])]}),
      ...d.items.map((it,j) => new TableRow({children:[
        C(`${String.fromCharCode(97+j)}) ${it.t}`,cw[0],{s:SS}),
        C([P("☐",{a:AlignmentType.CENTER,s:ST})],cw[1]),
        C([P("☐",{a:AlignmentType.CENTER,s:ST})],cw[2])]}))
    ]}));
  });
  ch.push(P("",{bf:60}));

  // C
  ch.push(P([{t:"C. Câu trắc nghiệm trả lời ngắn ",b:true,i:true},{t:"(Thí sinh ghi đáp án vào chỗ trống. Mỗi câu đúng được 0,5 điểm)",i:true,s:SS}],{af:40}));
  TLN.forEach((s,i) => {
    const qn = MC.length+DS.length+i+1;
    ch.push(P([{t:`Câu ${qn} `,b:true},{t:`(0,5 điểm). `,i:true,s:SS},{t:s.q}],{bf:50}));
    ch.push(P("     Trả lời: ................................................................",{bf:20}));
  });
  ch.push(P("",{bf:80}));

  // Phần II
  ch.push(P("PHẦN II. TỰ LUẬN (3,0 điểm)",{b:true,bf:80,af:40}));
  TL.forEach((e,i) => {
    const qn = MC.length+DS.length+TLN.length+i+1;
    ch.push(P([{t:`Câu ${qn} `,b:true},{t:`(${e.pt} điểm). `,b:true},{t:e.q}],{bf:60}));
    ch.push(P("",{bf:180}));
  });
  ch.push(P("",{bf:100}));
  ch.push(P("—— HẾT ——",{a:AlignmentType.CENTER,b:true,bf:100}));
  return ch;
}

// ══ FILE 3: ĐÁP ÁN ══
function f3() {
  const ch = [];
  ch.push(P("HƯỚNG DẪN CHẤM ĐỀ KIỂM TRA "+CONFIG.examType.toUpperCase(),{a:AlignmentType.CENTER,b:true,s:ST,af:30}));
  ch.push(P(`Môn: ${CONFIG.subject} – Lớp: ${CONFIG.grade} – Năm học: ${CONFIG.year}`,{a:AlignmentType.CENTER,i:true,s:SS,af:80}));

  ch.push(P("PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (7,0 điểm)",{b:true,bf:60,af:40}));
  ch.push(P("A. Câu trắc nghiệm nhiều lựa chọn (mỗi câu đúng được 0,25 điểm)",{b:true,i:true,af:30}));

  const aw = Array(13).fill(Math.floor(CW/13)); aw[12]=CW-aw[0]*12;
  ch.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:aw,rows:[
    new TableRow({children:["Câu",...Array.from({length:12},(_,i)=>String(i+1))].map((t,j)=>
      C(t,aw[j],{a:AlignmentType.CENTER,b:j===0,sh:j===0?sl:undefined}))}),
    new TableRow({children:["Đáp án",...MC.map(m=>m.da)].map((t,j)=>
      C(t,aw[j],{a:AlignmentType.CENTER,b:true}))})]}));
  ch.push(P("",{bf:60}));

  ch.push(P("B. Câu trắc nghiệm đúng – sai (mỗi ý đúng được 0,25 điểm)",{b:true,i:true,af:30}));
  const dw=[1200,2038,2039,2038,2039];
  ch.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:dw,rows:[
    new TableRow({children:["Câu","a","b","c","d"].map((t,j)=>C(t,dw[j],{a:AlignmentType.CENTER,b:true,sh:sl}))}),
    ...DS.map((d,i)=>new TableRow({children:[
      C(String(MC.length+i+1),dw[0],{a:AlignmentType.CENTER,b:true}),
      ...d.items.map((it,j)=>C(it.ok?"Đúng":"Sai",dw[j+1],{a:AlignmentType.CENTER,b:true}))]}))]}));
  ch.push(P("",{bf:60}));

  ch.push(P("C. Câu trắc nghiệm trả lời ngắn (mỗi câu đúng được 0,5 điểm)",{b:true,i:true,af:30}));
  const tw=[1500,7854];
  ch.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:tw,rows:[
    new TableRow({children:[C("Câu",tw[0],{a:AlignmentType.CENTER,b:true,sh:sl}),C("Đáp án",tw[1],{a:AlignmentType.CENTER,b:true,sh:sl})]}),
    ...TLN.map((s,i)=>new TableRow({children:[
      C(String(MC.length+DS.length+i+1),tw[0],{a:AlignmentType.CENTER}),
      C(s.da,tw[1],{a:AlignmentType.CENTER,b:true})]}))]}));
  ch.push(P("",{bf:80}));

  ch.push(P("PHẦN II. TỰ LUẬN (3,0 điểm)",{b:true,bf:60,af:40}));
  TL.forEach((e,i) => {
    const qn = MC.length+DS.length+TLN.length+i+1;
    ch.push(P([{t:`Câu ${qn} (${e.pt} điểm):`,b:true}],{bf:60}));
    e.ans.forEach(a => {
      a.t.split("\n").forEach(l => ch.push(P("  "+l,{bf:20})));
      ch.push(P(`  → ${a.d.toFixed(1)} điểm`,{i:true,s:SS,bf:10}));
    });
  });
  ch.push(P("",{bf:100}));
  ch.push(P("—— HẾT ——",{a:AlignmentType.CENTER,b:true}));
  return ch;
}

// ══ MAIN ══
async function main() {
  const px = `${CONFIG.subject.toLowerCase()}-${CONFIG.grade}`;
  const r1 = await save(f1(), `01-ma-tran-dac-ta-${px}.docx`);
  const r2 = await save(f2(), `02-de-kiem-tra-${px}.docx`);
  const r3 = await save(f3(), `03-dap-an-huong-dan-cham-${px}.docx`);
  console.log("Đã tạo thành công 3 file:");
  console.log(`  1. ${r1}`);
  console.log(`  2. ${r2}`);
  console.log(`  3. ${r3}`);
  console.log(`\nCấu trúc: ${MC.length} NLC + ${DS.length} ĐS + ${TLN.length} TLN + ${TL.length} TL = ${MC.length+DS.length+TLN.length+TL.length} câu`);
}
main().catch(e=>{console.error("Lỗi:",e.message);process.exit(1);});
