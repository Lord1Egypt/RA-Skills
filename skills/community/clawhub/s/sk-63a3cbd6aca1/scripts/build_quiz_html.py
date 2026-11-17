# -*- coding: utf-8 -*-
"""UI 模式：生成点选式单文件答题页「魔杖商店」。

  python scripts/build_quiz_html.py --out 魔杖商店.html
  python scripts/build_quiz_html.py --verify [--node <node.exe 路径>]

产出自包含 HTML：无外链、无依赖，双击即开。
页面 JS 引擎与 wand_shop.py 逻辑同源；--verify 用 node 对拍抽样作答与相照判定。

形象版插画：页内 canvas 按杖特（木色/芯色/纹路 seed）现画，每根杖独一张；
    同答案同 seed 必然同图。另有 scripts/make_wand_art.py（Pillow）离线出图，
    两者视觉口径一致；canvas 不可用时回退 assets/wand_hero.png。
"""
import argparse
import base64
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HERO = ROOT / "assets" / "wand_hero.png"
DEFAULT_NODE = r"C:\Users\yangduo\.workbuddy\binaries\node\versions\22.22.2-3\node.exe"


def load(name):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)


def hero_data_uri():
    if HERO.exists():
        return "data:image/png;base64," + base64.b64encode(HERO.read_bytes()).decode()
    return ""


def build_html():
    meta = load("meta.json")
    questions = load("questions.json")
    woods = load("woods.json")
    cores = load("cores.json")
    papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))
    blob = json.dumps({"meta": meta, "questions": questions, "woods": woods,
                       "cores": cores, "papers": papers}, ensure_ascii=False)

    html = (TEMPLATE.replace("__DATA__", blob)
            .replace("__ENGINE__", ENGINE_JS)
            .replace("__WAND_IMG__", hero_data_uri()))
    return html


# ---------------------------------------------------------------- 引擎 JS（与 wand_shop.py 同源，两侧必须同步修改）
ENGINE_JS = r"""
/*ENGINE-START*/
function crc32(str) {
  function utf8(s) {
    var out = [], i, c;
    for (i = 0; i < s.length; i++) {
      c = s.codePointAt(i);
      if (c > 0xffff) i++;
      if (c < 0x80) out.push(c);
      else if (c < 0x800) { out.push(0xc0 | (c >> 6), 0x80 | (c & 63)); }
      else if (c < 0x10000) { out.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63)); }
      else { out.push(0xf0 | (c >> 18), 0x80 | ((c >> 12) & 63), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63)); }
    }
    return out;
  }
  var table = crc32.table;
  if (!table) {
    table = crc32.table = [];
    for (var n = 0; n < 256; n++) {
      var cc = n;
      for (var k = 0; k < 8; k++) cc = (cc & 1) ? (0xedb88320 ^ (cc >>> 1)) : (cc >>> 1);
      table[n] = cc >>> 0;
    }
  }
  var crc = 0xffffffff;
  var bytes = utf8(str);
  for (var i = 0; i < bytes.length; i++)
    crc = (table[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8)) >>> 0;
  return (crc ^ 0xffffffff) >>> 0;
}
function dwidth(s) {
  var w = 0;
  for (var i = 0; i < s.length; i++) {
    var cp = s.codePointAt(i);
    if (cp > 0xffff) i++;
    w += cp >= 0x2e80 ? 2 : 1;
  }
  return w;
}
function wrapText(text, width) {
  var lines = [], cur = "", curW = 0;
  for (var i = 0; i < text.length; i++) {
    var ch = text[i], w = dwidth(ch);
    if (curW + w > width) { lines.push(cur); cur = ch; curW = w; }
    else { cur += ch; curW += w; }
  }
  if (cur) lines.push(cur);
  return lines;
}
function fracStr(x) {
  var q = Math.round(x * 4), whole = Math.floor(q / 4), rem = q % 4;
  return whole + ["", "\u00bc", "\u00bd", "\u00be"][rem];
}
var GROUPS = ["wood", "core", "len", "flex"];
var FLEX_OPP = { light: "hard", hard: "light", supple: "firm", firm: "supple" };
var LEN_OPP = { short: "long", long: "short" };
function validIds(g) {
  if (g === "wood") return DATA.woods.woods.map(function (w) { return w.id; });
  if (g === "core") return DATA.cores.cores.map(function (c) { return c.id; });
  if (g === "len") return DATA.meta.length_bands.map(function (b) { return b.id; });
  return DATA.meta.flex_bands.map(function (b) { return b.id; });
}
var WOODS = {}, CORES = {}, LEN_BANDS = {}, FLEX_BANDS = {}, Q_BY_ID = {};
DATA.woods.woods.forEach(function (w) { WOODS[w.id] = w; });
DATA.cores.cores.forEach(function (c) { CORES[c.id] = c; });
DATA.meta.length_bands.forEach(function (b) { LEN_BANDS[b.id] = b; });
DATA.meta.flex_bands.forEach(function (b) { FLEX_BANDS[b.id] = b; });
DATA.questions.questions.forEach(function (q) { Q_BY_ID[q.id] = q; });
var CAPS = (function () {
  var caps = {};
  GROUPS.forEach(function (g) {
    caps[g] = {};
    validIds(g).forEach(function (vid) {
      var total = 0;
      DATA.questions.questions.forEach(function (q) {
        if (q.group !== g) return;
        var best = 0;
        q.options.forEach(function (o) { best = Math.max(best, o.weights[vid] || 0); });
        total += best;
      });
      caps[g][vid] = total;
    });
  });
  return caps;
})();
function scoreAnswers(no, letters) {
  var paper = DATA.papers.papers[no - 1];
  var raw = { wood: {}, core: {}, len: {}, flex: {} };
  letters.forEach(function (ch, i) {
    var q = DATA.questions.questions[paper.order[i]];
    var di = paper.opts[q.id]["ABC".indexOf(ch)];
    var w = q.options[di].weights;
    Object.keys(w).forEach(function (vid) {
      raw[q.group][vid] = (raw[q.group][vid] || 0) + w[vid];
    });
  });
  var result = {};
  GROUPS.forEach(function (g) {
    var norm = {};
    validIds(g).forEach(function (vid) {
      var cap = CAPS[g][vid];
      norm[vid] = cap ? (raw[g][vid] || 0) / cap : 0;
    });
    var order = DATA.meta.tie_break[g];
    var ranked = validIds(g).slice().sort(function (a, b) {
      return (norm[b] - norm[a]) || (order.indexOf(a) - order.indexOf(b));
    });
    var sortedNorm = validIds(g).slice().sort(function (a, b) { return norm[b] - norm[a]; });
    result[g] = { winner: ranked[0], raw: raw[g], norm: norm,
                  margin: norm[ranked[0]] - norm[sortedNorm[1]] };
  });
  return result;
}
function pickWand(no, letters) {
  var sc = scoreAnswers(no, letters);
  var s = letters.join("");
  return {
    sc: sc,
    wood: WOODS[sc.wood.winner], core: CORES[sc.core.winner],
    len: LEN_BANDS[sc.len.winner], flex: FLEX_BANDS[sc.flex.winner],
    tree: crc32(no + ":" + s) % 10000 + 1,
    inch: LEN_BANDS[sc.len.winner].inches[crc32("inch:" + no + ":" + s) % LEN_BANDS[sc.len.winner].inches.length],
    letters: s
  };
}
function cnNum2(n) {
  var d = "\u3007\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d";
  if (n <= 10) return n === 10 ? "\u5341" : d[n - 1];
  if (n < 20) return "\u5341" + d[n - 11];
  return "\u4e8c\u5341";
}
function wandNameLine(p) {
  return p.wood.name + " \u00b7 " + p.core.name + " \u00b7 " + fracStr(p.inch) + " \u82f1\u5bf8 \u00b7 " + p.flex.name;
}
function cardLines(p, no, missing, early, answered) {
  var L = [], bar = "\u2550".repeat(64), thin = "-".repeat(64);
  var title = DATA.meta.shop_name + " \u00b7 \u5b83\u9009\u4e86\u4f60";
  var pad = Math.floor((64 - dwidth(title)) / 2);
  L.push(bar);
  L.push(" ".repeat(pad) + title);
  L.push(bar);
  L.push(wandNameLine(p));
  L.push(p.wood.grove + " \u7b2c " + p.tree + " \u68f5 \u00b7 \u6756\u5386" + cnNum2(no) + "\u5e74\u62e3\u9009");
  L.push("\u5377\u53f7 " + ("0" + no).slice(-2) + " \u00b7 \u590d\u73b0\u4e32 #" + ("0" + no).slice(-2) + ":" + p.letters);
  if (early && missing && missing.length) {
    L.push(DATA.meta.early_exit_card_line.replace("{n}", answered));
  } else if (missing && missing.length) {
    var ids = missing.map(function (i) { return DATA.questions.questions[DATA.papers.papers[no - 1].order[i]].id; });
    L.push("\uff08\u7b2c " + ids.join(", ") + " \u9898\u672a\u4f5c\u7b54\uff0c\u5df2\u6309\u4e2d\u95f4\u9879\u8865\u5165\uff09");
  }
  L.push(thin);
  p.wood.verse.concat(p.core.verse).concat([p.len.line, p.flex.line]).forEach(function (v) {
    wrapText(v, 62).forEach(function (ln) { L.push(ln); });
  });
  L.push(thin);
  L.push("\u8fd9\u6839\u6756\u600e\u4e48\u770b\u4f60");
  wrapText(p.wood.profile, 60).forEach(function (ln) { L.push("  " + ln); });
  L.push("\u5b83\u548c\u4f60\u5728\u4e00\u8d77");
  wrapText(p.core.companion, 60).forEach(function (ln) { L.push("  " + ln); });
  L.push("\u5e97\u4e3b\u7684\u6700\u540e\u4e00\u53e5");
  var ci = crc32("c" + no + ":" + p.letters) % DATA.meta.closing_lines.length;
  wrapText(DATA.meta.closing_lines[ci], 60).forEach(function (ln) { L.push("  " + ln); });
  L.push(thin);
  var fwd = DATA.meta.forward_template
    .replace("{wood}", p.wood.name).replace("{core}", p.core.name)
    .replace("{grove}", p.wood.grove).replace("{tree}", p.tree);
  wrapText("\u8f6c\u53d1\u8bed\uff1a" + fwd, 62).forEach(function (ln) { L.push(ln); });
  wrapText(DATA.meta.declaration, 62).forEach(function (ln) { L.push(ln); });
  return L;
}
function tryParseWandName(raw) {
  var s = raw;
  var wood = null, core = null, fb = null, inch = null, lb = null;
  DATA.woods.woods.forEach(function (w) { if (!wood && s.indexOf(w.name) >= 0) wood = w; });
  DATA.cores.cores.forEach(function (c) { if (!core && s.indexOf(c.name) >= 0) core = c; });
  DATA.meta.flex_bands.forEach(function (b) { if (!fb && s.indexOf(b.name) >= 0) fb = b; });
  var m = s.match(/(\d+)([\u00bc\u00bd\u00be]?)/);
  if (m) {
    var f = { "\u00bc": 0.25, "\u00bd": 0.5, "\u00be": 0.75 }[m[2]] || 0;
    inch = parseInt(m[1], 10) + f;
    DATA.meta.length_bands.forEach(function (b) {
      if (!lb && inch >= Math.min.apply(null, b.inches) && inch <= Math.max.apply(null, b.inches)) lb = b;
    });
  }
  if (!(wood && core && lb && fb)) return null;
  return { wood: wood, core: core, len: lb, flex: fb, tree: null, letters: null, inch: inch };
}
function normalizeStr(s) { return (s || "").trim(); }
function parseAnswers(raw, paperNo) {
  var s = normalizeStr(raw);
  if (!s) throw "EMPTY";
  var no = null, m = s.match(/[#\uff03]\s*(\d{1,3})/);
  if (m) no = parseInt(m[1], 10);
  if (no == null) { m = s.match(/\u5377\u53f7\s*(\d{1,3})/); if (m) no = parseInt(m[1], 10); }
  if (no == null) no = paperNo;
  if (no == null) throw "NO_PAPER";
  var paper = DATA.papers.papers[no - 1];
  if (!paper) throw "BAD_PAPER:" + no;
  s = s.replace(/--\s*paper\s*\d+/g, "");
  var letters = [];
  var numbered = s.match(/\d{1,2}\s*[A-Da-d\uff21-\uff24]/g);
  if (numbered) {
    numbered.forEach(function (tok) {
      var mm = tok.match(/(\d{1,2})\s*([A-Da-d\uff21-\uff24])/);
      var qid = parseInt(mm[1], 10), ch = mm[2].toUpperCase();
      ch = "\uff21\uff22\uff23".indexOf(ch) >= 0 ? "ABC"["\uff21\uff22\uff23".indexOf(ch)] : ch;
      var q = Q_BY_ID[qid];
      if (!q) throw "BAD_QNUM:" + qid;
      var disp = paper.opts[qid];
      if ("ABC".indexOf(ch) >= disp.length) throw "BAD_LETTER:" + qid + ch;
      letters[paper.order.indexOf(qid - 1)] = ch;
    });
  } else {
    var seq = (s.match(/[A-Da-d\uff21-\uff24]/g) || []).map(function (c) {
      var u = c.toUpperCase();
      return "\uff21\uff22\uff23".indexOf(u) >= 0 ? "ABC"["\uff21\uff22\uff23".indexOf(u)] : u;
    });
    if (!seq.length) throw "NO_ANSWERS";
    if (seq.length > DATA.questions.questions.length) throw "TOO_MANY";
    seq.forEach(function (ch, i) {
      var q = DATA.questions.questions[paper.order[i]];
      if ("ABC".indexOf(ch) >= paper.opts[q.id].length) throw "BAD_LETTER:" + q.id + ch;
      letters[i] = ch;
    });
  }
  var missing = [];
  for (var i = 0; i < DATA.questions.questions.length; i++) {
    if (!letters[i]) {
      var q = DATA.questions.questions[paper.order[i]];
      var disp = paper.opts[q.id];
      letters[i] = "ABC"[disp.indexOf(q["default"] == null ? 1 : q["default"])];
      missing.push(i);
    }
  }
  return { no: no, letters: letters, missing: missing };
}
function resolveSide(raw) {
  try {
    var r = parseAnswers(raw, null);
    var p = pickWand(r.no, r.letters);
    p.missingFill = true;
    return p;
  } catch (e) {
    var w = tryParseWandName(raw);
    if (w) return w;
    throw e;
  }
}
function compareWands(a, b) {
  var env = {
    wood_same: a.wood.id === b.wood.id,
    core_same: a.core.id === b.core.id,
    tree_same: a.tree != null && b.tree != null && a.tree === b.tree,
    core_clash: CORES[a.core.id].clash === b.core.id,
    flex_opposite: FLEX_OPP[a.flex.id] === b.flex.id,
    len_opposite: LEN_OPP[a.len.id] === b.len.id
  };
  env.all_same = env.wood_same && env.core_same && a.len.id === b.len.id && a.flex.id === b.flex.id;
  for (var i = 0; i < DATA.meta.compare_rules.length; i++) {
    var rule = DATA.meta.compare_rules[i];
    var ks = rule.when.split(" AND ");
    var ok = true;
    ks.forEach(function (k) { if (!env[k.trim()]) ok = false; });
    if (ok) return { rule: rule, env: env };
  }
  return { rule: null, env: env };
}
/*ENGINE-END*/
"""

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>魔杖商店 · 它选了你</title>
<style>
:root { --ink:#2b2440; --muted:#7a7290; --paper:#faf7f0; --card:#ffffff; --line:#e4ddcf;
        --accent:#5a4aa3; --accent-soft:#eeedfe; --gold:#854f0b; --gold-soft:#faeeda; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--paper); color:var(--ink); font-family:"Source Han Serif SC","Noto Serif SC",Georgia,"Microsoft YaHei",serif;
       min-height:100vh; display:flex; justify-content:center; padding:24px 16px; }
#app { width:100%; max-width:640px; }
.screen { display:none; background:var(--card); border:1px solid var(--line); border-radius:16px;
          padding:28px 26px; animation:fadein .35s ease; }
.screen.on { display:block; }
@keyframes fadein { from { opacity:0; transform:translateY(6px);} to { opacity:1; transform:none;} }
.shop-tag { font-size:13px; letter-spacing:.35em; color:var(--gold); text-align:center; }
h1 { font-size:24px; font-weight:500; text-align:center; margin:8px 0 4px; }
.sub { text-align:center; color:var(--muted); font-size:14px; margin-bottom:20px; }
.opline { font-size:15px; line-height:1.9; margin:10px 0; }
.btn { display:block; width:100%; border:none; border-radius:12px; background:var(--accent); color:#fff;
       font-size:16px; padding:13px; cursor:pointer; margin-top:14px; font-family:inherit; }
.btn:disabled { background:#c9c4dd; cursor:not-allowed; }
.btn.ghost { background:var(--accent-soft); color:var(--accent); }
.btn.small { width:auto; display:inline-block; padding:8px 18px; font-size:14px; }
.qnum { font-size:13px; color:var(--gold); letter-spacing:.2em; }
.qtext { font-size:18px; line-height:1.7; margin:10px 0 18px; }
.opt { border:1px solid var(--line); border-radius:12px; padding:14px 16px; margin:10px 0;
       font-size:15px; line-height:1.6; cursor:pointer; transition:all .15s; }
.opt:hover { border-color:var(--accent); background:var(--accent-soft); }
.opt.sel { border-color:var(--accent); background:var(--accent-soft); font-weight:500; }
.opt .k { display:inline-block; width:22px; color:var(--gold); }
.progress { display:flex; gap:5px; margin:4px 0 14px; flex-wrap:wrap; }
.dot { width:9px; height:9px; border-radius:50%; background:var(--line); cursor:pointer; }
.dot.done { background:var(--accent); }
.dot.cur { background:var(--gold); outline:2px solid var(--gold-soft); }
.navrow { display:flex; justify-content:space-between; margin-top:14px; }
.trial { font-size:16px; line-height:2; text-align:center; padding:26px 6px; }
.cardbox { white-space:pre-wrap; font-family:Consolas,"Courier New",monospace; font-size:12.5px;
           line-height:1.55; background:#fbfaf6; border:1px solid var(--line); border-radius:12px;
           padding:16px 14px; overflow-x:auto; }
.compare-row { margin:12px 0; }
.compare-row textarea { width:100%; height:64px; border:1px solid var(--line); border-radius:10px;
                        padding:10px; font-size:14px; font-family:inherit; resize:vertical; background:#fbfaf6; }
.msg { color:var(--muted); font-size:13px; margin-top:8px; min-height:18px; }
.hintline { color:var(--muted); font-size:12.5px; text-align:center; margin:2px 0 10px; }
.decl { color:var(--muted); font-size:12px; text-align:center; margin-top:16px; }
.wandcard { position:relative; background:linear-gradient(180deg,#fffdf8,#f8f2e6); border:1px solid #e3d9c6;
            border-radius:16px; padding:24px 22px 18px; overflow:hidden; }
.wc-corner { position:absolute; color:#c9a85c; font-size:12px; user-select:none; }
.wc-corner.tl { top:8px; left:13px; } .wc-corner.tr { top:8px; right:13px; }
.wc-corner.bl { bottom:8px; left:13px; } .wc-corner.br { bottom:8px; right:13px; }
.wc-hero { text-align:center; line-height:0; }
.wc-hero img { width:100%; max-width:520px; border-radius:14px; border:1px solid #e8ddc7; box-shadow:0 2px 10px rgba(90,74,163,.08); }
.wc-name { text-align:center; font-size:21px; letter-spacing:.04em; margin-top:8px; }
.wc-grove { text-align:center; color:var(--gold); font-size:13px; letter-spacing:.16em; margin-top:7px; }
.wc-note { text-align:center; color:var(--muted); font-size:12.5px; margin-top:6px; }
.wc-div { display:flex; align-items:center; gap:10px; margin:15px 0 13px; color:#c9a85c; font-size:11px; }
.wc-div::before, .wc-div::after { content:""; flex:1; height:1px; }
.wc-div::before { background:linear-gradient(90deg,transparent,#d9cba9); }
.wc-div::after { background:linear-gradient(90deg,#d9cba9,transparent); }
.wc-verse { text-align:center; font-size:14px; line-height:2.05; color:#3a3355; }
.wc-sec { margin-top:15px; }
.wc-sec h4 { font-size:12.5px; color:var(--gold); letter-spacing:.22em; font-weight:500; margin-bottom:5px; }
.wc-sec p { font-size:14px; line-height:1.95; margin:0; }
.wc-fwd { margin-top:16px; background:var(--accent-soft); border-radius:10px; padding:10px 13px;
          font-size:13px; line-height:1.8; color:var(--accent); }
.wc-decl { margin-top:11px; text-align:center; color:var(--muted); font-size:11.5px; }
.style-pick { margin:16px 0 4px; border:1px dashed var(--line); border-radius:12px; padding:12px 14px; }
.sp-title { font-size:12.5px; color:var(--gold); letter-spacing:.25em; text-align:center; }
.sp-row { display:flex; gap:10px; margin-top:9px; }
.sp-opt { flex:1; border:1.5px solid var(--line); border-radius:10px; padding:9px 6px; text-align:center;
          font-size:14.5px; cursor:pointer; transition:all .15s; }
.sp-opt span { display:block; font-size:11.5px; color:var(--muted); margin-top:3px; }
.sp-opt.sel { border-color:var(--accent); background:var(--accent-soft); color:var(--accent); font-weight:500; }
.sp-note { font-size:11.5px; color:var(--muted); line-height:1.7; margin-top:9px; }
.linklike { background:none; border:none; color:var(--accent); text-decoration:underline; cursor:pointer;
            font-size:14px; font-family:inherit; }
.center { text-align:center; }
</style>
</head>
<body>
<div id="app">

<div class="screen on" id="sc-cover">
  <div class="shop-tag">THE WAND SHOP</div>
  <h1>魔杖商店</h1>
  <div class="sub">它选了你</div>
  <div id="opening"></div>
  <button class="btn" id="btn-start">进店量杖</button>
  <button class="btn ghost" id="btn-compare-cover">两杖相照（已有杖码？来对照）</button>
  <div class="decl" id="decl1"></div>
</div>

<div class="screen" id="sc-quiz">
  <div class="progress" id="progress"></div>
  <div class="hintline" id="early-hint"></div>
  <div class="qnum" id="qnum"></div>
  <div class="qtext" id="qtext"></div>
  <div id="opts"></div>
  <div class="navrow">
    <button class="linklike" id="btn-prev">← 上一题</button>
    <button class="linklike" id="btn-quit">不测了，出店</button>
  </div>
  <button class="btn ghost" id="btn-early" style="display:none">就到这里，先看杖</button>
  <button class="btn" id="btn-submit" disabled>提交判定</button>
</div>

<div class="screen" id="sc-trial">
  <div class="trial" id="trial-text"></div>
  <div class="style-pick" id="style-pick" style="display:none">
    <div class="sp-title"></div>
    <div class="sp-row">
      <div class="sp-opt sel" data-style="rich"></div>
      <div class="sp-opt" data-style="plain"></div>
    </div>
    <div class="sp-note"></div>
  </div>
  <button class="btn" id="btn-trial-next">继续</button>
</div>

<div class="screen" id="sc-card">
  <div id="card-rich"></div>
  <pre id="card-out" style="display:none"></pre>
  <button class="btn" id="btn-copy-card">复制完整杖卡（含复现串）</button>
  <button class="btn ghost" id="btn-copy-tree">只复制树籍一行</button>
  <button class="btn ghost" id="btn-again">再测一次（换一套题）</button>
  <button class="linklike" id="btn-style-toggle" style="display:block;margin:10px auto 0;"></button>
  <div class="msg" id="copy-msg"></div>
</div>

<div class="screen" id="sc-compare">
  <h1>两杖相照</h1>
  <div class="sub">把两根杖的复现串（#7:ABC…）或杖名行粘进来</div>
  <div class="compare-row"><textarea id="cmp-a" placeholder="甲的复现串或杖名，例如：#04:ACBA… 或 紫杉 · 雾露晶 · 11½ 英寸 · 微韧"></textarea></div>
  <div class="compare-row"><textarea id="cmp-b" placeholder="乙的复现串或杖名"></textarea></div>
  <button class="btn" id="btn-cmp-run">出判定</button>
  <div class="cardbox" id="cmp-out" style="display:none"></div>
  <button class="btn ghost" id="btn-cmp-back">回到店门口</button>
</div>

</div>
<script>
var DATA = __DATA__;</script>
<script>
var WAND_IMG = "__WAND_IMG__";
</script>
<script>
/* ===== 形象版插画：canvas 按杖特现画（与 make_wand_art.py 同视觉口径） ===== */
var ART = (function () {
  var W = 1000, H = 656;
  var WOOD_HEX = { "橡木": "#A9784B", "山楂木": "#B08258", "桦木": "#D8C39E", "紫杉": "#6E4A4A",
    "樱桃木": "#B4664A", "胡桃木": "#7B5230", "白蜡木": "#CDB183", "枫木": "#C08F5A" };
  var CORE_RGB = { "星陨砂": [142,124,216], "萤火绒": [232,197,106], "雷纹羽": [110,116,200],
    "潮汐珠": [78,147,184], "炉心泥": [193,107,74], "雾露晶": [159,182,216] };
  var FLEX_TXT = { "轻盈": "打断来了先退一步，退完发现路还在", "微韧": "弯而不折，有底线",
    "挺韧": "顶得住，不绕路", "坚硬": "宁折不弯，认死理但纯粹" };

  function shade(rgb, k) { return rgb.map(function (c) { return Math.max(0, Math.min(255, Math.round(c * k))); }); }
  function hex2rgb(h) { h = h.replace("#", ""); return [0, 2, 4].map(function (i) { return parseInt(h.slice(i, i + 2), 16); }); }
  function rgbCss(c) { return "rgb(" + c[0] + "," + c[1] + "," + c[2] + ")"; }

  /* 种子随机（mulberry32）：同 seed 同序列，保证「同杖同图」 */
  function rng(seed) {
    var t = seed >>> 0;
    return function () {
      t += 0x6D2B79F5;
      var r = Math.imul(t ^ (t >>> 15), 1 | t);
      r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }

  function star(ctx, cx, cy, r, col) {
    ctx.beginPath();
    for (var i = 0; i < 8; i++) {
      var a = i * Math.PI / 4, rr = i % 2 ? r * 0.26 : r;
      ctx[i ? "lineTo" : "moveTo"](cx + rr * Math.sin(a), cy - rr * Math.cos(a));
    }
    ctx.closePath(); ctx.fillStyle = col; ctx.fill();
  }

  function draw(cfg, canvas) {
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = "100%"; canvas.style.height = "auto";
    var ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    var r = rng(cfg.seed);

    var wood = hex2rgb(WOOD_HEX[cfg.wood] || "#A9784B");
    var core = CORE_RGB[cfg.core] || [142, 124, 216];
    var woodD = shade(wood, 0.60), woodDD = shade(wood, 0.42);

    /* 背景 */
    ctx.fillStyle = "rgb(255,253,248)"; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "rgb(248,242,230)"; ctx.fillRect(0, 0, W, 104);
    ctx.fillStyle = "rgb(133,79,11)"; ctx.font = "24px sans-serif";
    ctx.fillText(DATA.meta.shop_name, 46, 44);
    ctx.fillStyle = "rgb(58,51,85)"; ctx.font = "32px sans-serif";
    ctx.fillText("它选了你", 46, 86);
    [wood, woodD, core].forEach(function (c, i) {
      var x = W - 196 + i * 46;
      ctx.fillStyle = rgbCss(c);
      ctx.beginPath();
      if (ctx.roundRect) { ctx.roundRect(x, 32, 34, 40, 9); ctx.fill(); }
      else ctx.fillRect(x, 32, 34, 40);
    });

    /* 杖身（斜放，由粗到细） */
    var x0 = 90, y0 = 600, x1 = 905, y1 = 128, steps = 380, wT = 19, wTip = 6;
    var pts = [];
    for (var i = 0; i <= steps; i++) {
      var t = i / steps;
      pts.push([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + Math.sin(t * 3.1) * 6,
                wT + (wTip - wT) * t]);
    }
    ctx.fillStyle = rgbCss(wood);
    pts.forEach(function (p) { ctx.beginPath(); ctx.arc(p[0], p[1], p[2] / 2, 0, 7); ctx.fill(); });
    ctx.fillStyle = rgbCss(woodD);
    pts.forEach(function (p) { ctx.beginPath(); ctx.arc(p[0], p[1] + p[2] * 0.26, p[2] / 2, 0, 7); ctx.fill(); });
    ctx.fillStyle = "rgb(255,250,238)";
    for (var j = 0; j < pts.length; j += 2) {
      var p = pts[j];
      ctx.beginPath(); ctx.arc(p[0], p[1] - p[2] * 0.32, p[2] * 0.18, 0, 7); ctx.fill();
    }
    var ang = Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2;
    var coils = 12 + Math.floor(r() * 9), phase = r() * Math.PI;
    ctx.strokeStyle = rgbCss(woodDD); ctx.lineWidth = 1.7;
    for (var k = 0; k < coils; k++) {
      var tt = 0.09 + 0.84 * (k / Math.max(1, coils - 1));
      var p = pts[Math.floor(tt * steps)], rr = p[2] * 0.66;
      var a0 = ang * 180 / Math.PI + 18 + 34 * Math.sin(phase + k * 0.9);
      ctx.beginPath(); ctx.arc(p[0], p[1], rr, a0 * Math.PI / 180, (a0 + 128) * Math.PI / 180); ctx.stroke();
    }
    /* 握把缠线 */
    ctx.strokeStyle = "rgb(90,74,163)"; ctx.lineWidth = 2.0;
    for (var g = Math.floor(steps * 0.07); g < steps * 0.33; g += 3) {
      var p = pts[g], rr = p[2] * 0.74;
      ctx.beginPath(); ctx.arc(p[0], p[1], rr, ang - 10 * Math.PI / 180, ang + 190 * Math.PI / 180); ctx.stroke();
    }
    var pg = pts[Math.floor(steps * 0.33)];
    ctx.fillStyle = "rgb(90,74,163)";
    ctx.beginPath(); ctx.arc(pg[0], pg[1], pg[2] * 0.46, 0, 7); ctx.fill();
    /* 心材线 */
    ctx.fillStyle = rgbCss(core);
    for (var m = Math.floor(steps * 0.16); m < steps * 0.975; m += 2) {
      var p = pts[m];
      ctx.beginPath(); ctx.arc(p[0], p[1], Math.max(1.3, p[2] * 0.095), 0, 7); ctx.fill();
    }
    /* 杖尖 + 星芒 */
    var pt = pts[steps];
    ctx.fillStyle = rgbCss(core);
    ctx.beginPath(); ctx.arc(pt[0], pt[1], pt[2] * 0.8, 0, 7); ctx.fill();
    ctx.fillStyle = "rgb(255,250,238)";
    ctx.beginPath(); ctx.arc(pt[0], pt[1], pt[2] * 0.45, 0, 7); ctx.fill();
    ctx.strokeStyle = "rgb(201,168,92)"; ctx.fillStyle = "rgb(201,168,92)"; ctx.lineWidth = 2.6;
    [[1,0,72],[0.87,0.5,46],[0.5,0.87,34],[0,1,30],[-0.5,0.87,28],[-0.87,0.5,24],
     [-0.87,-0.5,28],[-0.5,-0.87,32],[0,-1,40],[0.5,-0.87,46],[0.87,-0.5,56]].forEach(function (v) {
      var ex = pt[0] + v[0] * v[2], ey = pt[1] + v[1] * v[2];
      ctx.beginPath(); ctx.moveTo(pt[0], pt[1]); ctx.lineTo(ex, ey); ctx.stroke();
      ctx.beginPath(); ctx.arc(ex, ey, 4, 0, 7); ctx.fill();
    });
    /* 背景星点（seed 决定位置） */
    for (var s = 0; s < 4 + Math.floor(r() * 4); s++) {
      star(ctx, 470 + r() * 460, 120 + r() * 210, [5, 7, 9][Math.floor(r() * 3)], "rgb(201,168,92)");
    }

    /* 特性面板 */
    var pw = W - 88, ph = 236, px = 44, py = H - ph - 36;
    ctx.fillStyle = "#fff"; ctx.strokeStyle = "rgb(238,228,209)"; ctx.lineWidth = 2;
    ctx.beginPath();
    if (ctx.roundRect) { ctx.roundRect(px, py, pw, ph, 20); ctx.fill(); ctx.stroke(); }
    else { ctx.fillRect(px, py, pw, ph); ctx.strokeRect(px, py, pw, ph); }
    ctx.fillStyle = "rgb(201,168,92)";
    ctx.beginPath();
    if (ctx.roundRect) { ctx.roundRect(px, py, 10, ph, 5); ctx.fill(); } else ctx.fillRect(px, py, 10, ph);
    var tx = px + 34, ty = py + 58;
    ctx.fillStyle = "rgb(58,51,85)"; ctx.font = "38px sans-serif";
    ctx.fillText(cfg.wandName, tx, ty);
    ty += 40;
    ctx.fillStyle = "rgb(133,79,11)"; ctx.font = "20px sans-serif";
    ctx.fillText(cfg.groveLine, tx, ty);
    ty += 34;
    ctx.strokeStyle = "rgb(238,228,209)";
    ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(px + pw - 34, ty); ctx.stroke();
    ty += 34;
    ctx.fillStyle = "rgb(58,51,85)"; ctx.font = "21px sans-serif";
    ctx.fillText("芯 · " + cfg.core + "（" + cfg.coreDrive + "）　　长 · " + cfg.lenTxt + " 英寸 · " +
      cfg.lenName + "　　韧 · " + cfg.flex + "　" + (FLEX_TXT[cfg.flex] || ""), tx, ty);
    ty += 40;
    ctx.fillStyle = rgbCss(core);
    ctx.beginPath();
    if (ctx.roundRect) { ctx.roundRect(tx, ty, 96, 20, 10); ctx.fill(); } else ctx.fillRect(tx, ty, 96, 20);
    ctx.fillStyle = "rgb(138,128,116)"; ctx.font = "18px sans-serif";
    ctx.fillText(cfg.coreLabel, tx + 112, ty + 16);
    /* 底部声明 */
    ctx.font = "15px sans-serif";
    ctx.fillText(DATA.meta.declaration, 46, H - 20);
  }

  return { draw: draw };
})();
</script>
<script>
__ENGINE__
</script>
<script>
var state = { paperNo: 0, answers: [], idx: 0, trialStep: 0, trialLines: [], wand: null, missing: [], earlyExit: false, answered: 0, cardStyle: "rich" };
var ART_URLS = {};   /* keyOf(wand) -> dataURL，每根杖一张专属图 */
function $(id) { return document.getElementById(id); }
function show(id) {
  document.querySelectorAll(".screen").forEach(function (s) { s.classList.remove("on"); });
  $(id).classList.add("on");
  window.scrollTo(0, 0);
}
function pickPaper() {
  return 1 + Math.floor(Math.random() * DATA.papers.papers.length);
}
function renderOpening() {
  $("opening").innerHTML = DATA.meta.opening.map(function (l) {
    return '<div class="opline">' + l + "</div>";
  }).join("");
  $("decl1").textContent = DATA.meta.declaration;
  var m = DATA.meta;
  document.querySelector("#style-pick .sp-title").textContent = "✦ " + m.style_choice_title + " ✦";
  document.querySelector('.sp-opt[data-style="rich"]').innerHTML =
    esc(m.style_choice_rich) + "<span>" + esc(m.style_choice_rich_sub) + "</span>";
  document.querySelector('.sp-opt[data-style="plain"]').innerHTML =
    esc(m.style_choice_plain) + "<span>" + esc(m.style_choice_plain_sub) + "</span>";
  document.querySelector("#style-pick .sp-note").textContent = m.style_choice_note;
}
function pickStyle(el) {
  document.querySelectorAll(".sp-opt").forEach(function (o) { o.classList.remove("sel"); });
  el.classList.add("sel");
  state.cardStyle = el.getAttribute("data-style");
}
function startQuiz() {
  state.paperNo = pickPaper();
  state.answers = [];
  state.idx = 0;
  state.earlyExit = false;
  state.missing = [];
  state.answered = 0;
  renderQuiz();
  show("sc-quiz");
}
function renderQuiz() {
  var paper = DATA.papers.papers[state.paperNo - 1];
  var qi = paper.order[state.idx];
  var q = DATA.questions.questions[qi];
  var disp = paper.opts[q.id];
  $("qnum").textContent = "第 " + (state.idx + 1) + " 题 / 共 27 题";
  $("qtext").textContent = q.text;
  var box = $("opts");
  box.innerHTML = "";
  disp.forEach(function (di, j) {
    var d = document.createElement("div");
    d.className = "opt" + (state.answers[state.idx] === "ABC"[j] ? " sel" : "");
    d.innerHTML = '<span class="k">' + "ABC"[j] + "</span>" + q.options[di].text;
    d.onclick = function () {
      state.answers[state.idx] = "ABC"[j];
      renderProgress();
      if (state.idx < 26) { state.idx++; setTimeout(function () { renderQuiz(); }, 200); }
      else renderQuiz();
    };
    box.appendChild(d);
  });
  renderProgress();
  var answeredN = state.answers.filter(Boolean).length;
  var canEarly = answeredN >= DATA.meta.early_exit_min;
  $("early-hint").textContent = canEarly ? "" : DATA.meta.early_exit_quiz_line;
  $("btn-early").style.display = canEarly ? "block" : "none";
  if (canEarly) $("btn-early").textContent = "就到这里，先看杖（已答 " + answeredN + " 题）";
  $("btn-submit").disabled = answeredN < 27;
  $("btn-submit").textContent = answeredN < 27
    ? "还差 " + (27 - answeredN) + " 题" : "提交判定";
}
function renderProgress() {
  var pr = $("progress");
  pr.innerHTML = "";
  for (var i = 0; i < 27; i++) {
    (function (i) {
      var d = document.createElement("span");
      d.className = "dot" + (state.answers[i] ? " done" : "") + (i === state.idx ? " cur" : "");
      if (state.answers[i] || i < state.idx) d.onclick = function () { state.idx = i; renderQuiz(); };
      pr.appendChild(d);
    })(i);
  }
}
function startTrial() {
  var pool = DATA.meta.failure_pool.slice();
  state.trialLines = [];
  for (var i = 0; i < 3; i++) {
    state.trialLines.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
  }
  state.trialStep = 0;
  state.wand = pickWand(state.paperNo, state.answers.slice());
  renderTrial();
  show("sc-trial");
}
function renderTrial() {
  var atEnd = state.trialStep >= state.trialLines.length;
  if (!atEnd) {
    $("trial-text").textContent = state.trialLines[state.trialStep];
    $("btn-trial-next").textContent = "继续";
  } else {
    $("trial-text").textContent = DATA.meta.chosen_line + "\n" + DATA.meta.keeper_line;
    $("btn-trial-next").textContent = "领取杖卡";
  }
  /* 结果样式只在「准备领卡」这一刻出现——不在进店时就打断节奏 */
  $("style-pick").style.display = atEnd ? "block" : "none";
  if (atEnd) syncStylePick();
}
function syncStylePick() {
  document.querySelectorAll(".sp-opt").forEach(function (o) {
    o.classList.toggle("sel", o.getAttribute("data-style") === state.cardStyle);
  });
}
function esc(s) {
  return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
/* 每根杖一把 seed：木/芯/长/韧/树号/卷号共同决定，同杖必同图 */
function keyOf(p, no) {
  return [p.wood.id, p.core.id, p.len.id, p.flex.id, no, p.tree].join("|");
}
function ensureArt(p, no, cb) {
  var key = keyOf(p, no);
  if (ART_URLS[key]) { cb(); return; }
  var cv = document.createElement("canvas");
  if (!cv.getContext) { cb(); return; }
  try {
    ART.draw({
      seed: crc32("art:" + key),
      wood: p.wood.name, core: p.core.name,
      coreDrive: p.core.drive,
      wandName: wandNameLine(p),
      groveLine: p.wood.grove + " · " + p.wood.grove_line,
      lenTxt: fracStr(p.inch), lenName: p.len.name,
      flex: p.flex.name,
      coreLabel: p.core.origin.split("，")[0].slice(0, 22)
    }, cv);
    ART_URLS[key] = cv.toDataURL("image/png");
  } catch (e) { /* 静默：无 canvas 就走兜底静态图 */ }
  cb();
}
function renderRichCard(p, no, early, answered) {
  var artUrl = ART_URLS[keyOf(p, no)];
  if (!artUrl && WAND_IMG) artUrl = WAND_IMG;   /* canvas 不可用时的兜底 */
  var wantHero = state.cardStyle === "rich" && artUrl;
  var hero = wantHero ? '<div class="wc-hero"><img src="' + artUrl + '" alt=""></div>' : "";
  var verses = p.wood.verse.concat(p.core.verse).concat([p.len.line, p.flex.line])
    .map(function (v) { return "<div>" + esc(v) + "</div>"; }).join("");
  var fwd = DATA.meta.forward_template
    .replace("{wood}", p.wood.name).replace("{core}", p.core.name)
    .replace("{grove}", p.wood.grove).replace("{tree}", p.tree);
  var note = early ? '<div class="wc-note">' +
    esc(DATA.meta.early_exit_card_line.replace("{n}", answered)) + "</div>" : "";
  var ci = crc32("c" + no + ":" + p.letters) % DATA.meta.closing_lines.length;
  return '<div class="wandcard">'
    + '<div class="wc-corner tl">\u2726</div><div class="wc-corner tr">\u2726</div>'
    + '<div class="wc-corner bl">\u2726</div><div class="wc-corner br">\u2726</div>'
    + hero
    + '<div class="wc-name">' + esc(wandNameLine(p)) + "</div>"
    + '<div class="wc-grove">' + esc(p.wood.grove + " 第 " + p.tree + " 棵 · 杖历" + cnNum2(no) + "年拣选") + "</div>"
    + note
    + '<div class="wc-div"><span>\u2726</span></div>'
    + '<div class="wc-verse">' + verses + "</div>"
    + '<div class="wc-sec"><h4>\u2726 这根杖怎么看你</h4><p>' + esc(p.wood.profile) + "</p></div>"
    + '<div class="wc-sec"><h4>\u2726 它和你在一起</h4><p>' + esc(p.core.companion) + "</p></div>"
    + '<div class="wc-sec"><h4>\u2726 店主的最后一句</h4><p>' + esc(DATA.meta.closing_lines[ci]) + "</p></div>"
    + '<div class="wc-fwd">转发语：' + esc(fwd) + "</div>"
    + '<div class="wc-decl">' + esc(DATA.meta.declaration) + "</div>"
    + "</div>";
}
function showCard() {
  var p = state.wand;
  p.letters = state.answers.join("");
  p.tree = crc32(state.paperNo + ":" + p.letters) % 10000 + 1;
  p.inch = p.len.inches[crc32("inch:" + state.paperNo + ":" + p.letters) % p.len.inches.length];
  var missing = state.earlyExit ? state.missing : [];
  var lines = cardLines(p, state.paperNo, missing, state.earlyExit, state.answered);
  $("card-out").textContent = lines.join("\n");
  ensureArt(p, state.paperNo, function () {
    $("card-rich").innerHTML = renderRichCard(p, state.paperNo, state.earlyExit, state.answered);
    $("btn-style-toggle").textContent = DATA.meta.style_toggle_label;
    $("copy-msg").textContent = "";
    show("sc-card");
  });
}
function copyText(text, msgEl) {
  function done() { $(msgEl).textContent = "已复制，去发给朋友吧。"; }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done, function () { fallback(); });
  } else fallback();
  function fallback() {
    var ta = document.createElement("textarea");
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); done(); } catch (e) { $(msgEl).textContent = "复制失败，请手动选择文本。"; }
    document.body.removeChild(ta);
  }
}
function runCompare() {
  var aRaw = $("cmp-a").value, bRaw = $("cmp-b").value;
  var out = $("cmp-out");
  try {
    var a = resolveSide(aRaw), b = resolveSide(bRaw);
    var r = compareWands(a, b);
    var bar = "=".repeat(64), thin = "-".repeat(64);
    var L = [bar, DATA.meta.shop_name + " · " + DATA.meta.compare_title, bar];
    L.push("甲：" + wandNameLine(a) + (a.tree ? "（" + a.wood.grove + " 第 " + a.tree + " 棵）" : ""));
    L.push("乙：" + wandNameLine(b) + (b.tree ? "（" + b.wood.grove + " 第 " + b.tree + " 棵）" : ""));
    L.push(thin);
    if (r.rule) {
      L.push("判定 · " + r.rule.title);
      wrapText(r.rule.line, 62).forEach(function (ln) { L.push("  " + ln); });
      L.push("");
      L.push("合杖名：" + (a.wood.id === b.wood.id ? a.wood.name : a.wood.name[0] + b.wood.name[0]));
    } else {
      wrapText(DATA.meta.compare_fallback, 62).forEach(function (ln) { L.push(ln); });
    }
    L.push(bar);
    out.textContent = L.join("\n");
    out.style.display = "block";
  } catch (e) {
    out.style.display = "block";
    out.textContent = "有一边我认不出来。请粘复现串（#7:ABC…）或完整的杖名行（木 · 芯 · 英寸 · 韧度）。";
  }
}
$("btn-start").onclick = startQuiz;
$("btn-compare-cover").onclick = function () { $("cmp-out").style.display = "none"; show("sc-compare"); };
$("btn-cmp-back").onclick = function () { show("sc-cover"); };
$("btn-cmp-run").onclick = runCompare;
$("btn-prev").onclick = function () { if (state.idx > 0) { state.idx--; renderQuiz(); } };
$("btn-quit").onclick = function () { show("sc-cover"); };
$("btn-early").onclick = function () {
  if (!confirm(DATA.meta.early_exit_confirm)) return;
  var paper = DATA.papers.papers[state.paperNo - 1];
  state.missing = [];
  for (var i = 0; i < 27; i++) {
    if (!state.answers[i]) {
      var q = DATA.questions.questions[paper.order[i]];
      var disp = paper.opts[q.id];
      state.answers[i] = "ABC"[disp.indexOf(q["default"] == null ? 1 : q["default"])];
      state.missing.push(i);
    }
  }
  state.earlyExit = true;
  state.answered = 27 - state.missing.length;
  renderProgress();
  startTrial();
};
$("btn-submit").onclick = startTrial;
$("btn-trial-next").onclick = function () {
  state.trialStep++;
  if (state.trialStep <= state.trialLines.length) renderTrial(); else showCard();
};
$("btn-again").onclick = startQuiz;
document.querySelectorAll(".sp-opt").forEach(function (o) {
  o.onclick = function () { pickStyle(o); };
});
$("btn-style-toggle").onclick = function () {
  state.cardStyle = state.cardStyle === "rich" ? "plain" : "rich";
  document.querySelectorAll(".sp-opt").forEach(function (o) {
    o.classList.toggle("sel", o.getAttribute("data-style") === state.cardStyle);
  });
  ensureArt(state.wand, state.paperNo, function () {
    $("card-rich").innerHTML = renderRichCard(state.wand, state.paperNo, state.earlyExit, state.answered);
  });
};
$("btn-copy-card").onclick = function () {
  copyText($("card-out").textContent, "copy-msg");
};
$("btn-copy-tree").onclick = function () {
  var lines = $("card-out").textContent.split("\n");
  copyText(lines[3] + "\n" + lines[4], "copy-msg");
};
document.addEventListener("keydown", function (e) {
  if (!$("sc-quiz").classList.contains("on")) return;
  var k = e.key.toUpperCase();
  if ("ABC".indexOf(k) >= 0) {
    var j = "ABC".indexOf(k);
    if (j >= 0 && j < 3) { state.answers[state.idx] = "ABC"[j]; renderProgress(); if (state.idx < 26) { state.idx++; renderQuiz(); } else renderQuiz(); }
  } else if ("123".indexOf(k) >= 0) {
    var j2 = parseInt(k, 10) - 1;
    state.answers[state.idx] = "ABC"[j2]; renderProgress();
    if (state.idx < 26) { state.idx++; renderQuiz(); } else renderQuiz();
  } else if (e.key === "ArrowLeft" && state.idx > 0) { state.idx--; renderQuiz(); }
  else if (e.key === "ArrowRight" && state.idx < 26) { state.idx++; renderQuiz(); }
});
renderOpening();
</script>
</body>
</html>
"""


def compute_expected(cases):
    """Python 侧对拍基准： winners / tree / inch / 判定"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("wand_shop", ROOT / "scripts" / "wand_shop.py")
    ws = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ws)
    out = []
    for case in cases:
        if case["type"] == "score":
            no = case["paper"]
            letters = list(case["letters"])
            p = ws.pick(no, letters)
            out.append({
                "type": "score", "paper": no, "letters": case["letters"],
                "wood": p["wood"]["id"], "core": p["core"]["id"],
                "len": p["len"]["id"], "flex": p["flex"]["id"],
                "tree": p["tree"], "inch": p["inch"],
            })
        elif case["type"] == "compare":
            pa, na = ws.resolve_side(case["a"])
            pb, nb = ws.resolve_side(case["b"])
            rule, _ = ws.compare_wands(pa, pb)
            out.append({"type": "compare", "rule": rule["id"] if rule else None})
    return out


def action_verify(node):
    import subprocess
    import tempfile
    rng = random.Random(20260915)
    cases = []
    for paper in [1, 7, 13]:
        for _ in range(60):
            letters = "".join(rng.choice("ABC") for _ in range(27))
            cases.append({"type": "score", "paper": paper, "letters": letters})
    cases.append({"type": "score", "paper": 1, "letters": "A" * 27})
    cases.append({"type": "score", "paper": 1, "letters": "C" * 27})
    # 提前结束：部分答案串两侧引擎必须同样处理
    cases.append({"type": "score", "paper": 5, "letters": "ABCCBABA"})
    cases.append({"type": "score", "paper": 5, "letters": "A"})
    cases.append({"type": "score", "paper": 13, "letters": "BCABCABCCB"})
    cases.append({"type": "compare", "a": "#1:" + "A" * 27, "b": "#1:" + "A" * 27})
    cases.append({"type": "compare", "a": "#1:" + "A" * 27, "b": "#1:" + "B" * 27})
    cases.append({"type": "compare", "a": "橡木 · 炉心泥 · 11½ 英寸 · 微韧",
                  "b": "山楂木 · 雾露晶 · 10¼ 英寸 · 坚硬"})

    expected = compute_expected(cases)

    html = build_html()
    start = html.index("/*ENGINE-START*/")
    end = html.index("/*ENGINE-END*/") + len("/*ENGINE-END*/")
    engine = html[start:end]
    data_start = html.index("var DATA = ") + len("var DATA = ")
    data_end = html.index(";</script>", data_start)
    data_js = html[data_start:data_end]
    driver = "var DATA = " + data_js + ";\n" + engine + r"""
const cases = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
const out = [];
for (const c of cases) {
  if (c.type === 'score') {
    const p = pickWand(c.paper, c.letters.split(''));
    out.push({ type: 'score', paper: c.paper, letters: c.letters,
      wood: p.wood.id, core: p.core.id, len: p.len.id, flex: p.flex.id,
      tree: p.tree, inch: p.inch });
  } else {
    const a = resolveSide(c.a), b = resolveSide(c.b);
    const r = compareWands(a, b);
    out.push({ type: 'compare', rule: r.rule ? r.rule.id : null });
  }
}
require('fs').writeFileSync(process.argv[3], JSON.stringify(out));
"""
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "cases.json").write_text(json.dumps(cases, ensure_ascii=False), encoding="utf-8")
        (tdp / "driver.js").write_text(driver, encoding="utf-8")
        proc = subprocess.run(
            [node, str(tdp / "driver.js"), str(tdp / "cases.json"), str(tdp / "got.json")],
            capture_output=True, timeout=120)
        if proc.returncode != 0:
            print("[对拍失败] node 执行出错：")
            sys.stdout.flush()
            sys.stderr.buffer.write(proc.stderr)
            sys.exit(1)
        got = json.loads((tdp / "got.json").read_text(encoding="utf-8"))

    bad = 0
    for exp, g in zip(expected, got):
        if exp != g:
            bad += 1
            print("[对拍不一致]", json.dumps(exp, ensure_ascii=False), "≠", json.dumps(g, ensure_ascii=False))
    if bad:
        print(f"对拍失败：{bad}/{len(expected)} 不一致。JS 引擎与 Python 引擎已分叉，禁止发布。")
        sys.exit(1)
    print(f"对拍通过：{len(expected)} 组抽样（计分 {sum(1 for c in cases if c['type']=='score')} + 相照 {sum(1 for c in cases if c['type']=='compare')}）逐字段一致")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", metavar="路径", help="输出 HTML 路径")
    ap.add_argument("--verify", action="store_true", help="node 对拍")
    ap.add_argument("--node", default=DEFAULT_NODE, help="node 可执行文件路径")
    args = ap.parse_args()

    if args.verify:
        action_verify(args.node)
        return
    if not args.out:
        ap.error("需要 --out 或 --verify")
    html = build_html()
    Path(args.out).write_text(html, encoding="utf-8")
    print(f"已生成 {args.out}（自包含单文件，双击即开）")


if __name__ == "__main__":
    main()
