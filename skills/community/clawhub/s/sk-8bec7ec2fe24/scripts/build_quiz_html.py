#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分院帽 Skill 交互式答题页生成器。

把 data/questions.json（题库）+ data/papers.json（试卷库）+ data/houses.json（文案）
+ data/glossary.json（麻瓜词典）渲染成一个**自包含的单文件 HTML**：
打开时随机抽一张卷、一屏一题、点选作答、自动记忆、全部答完点「提交判定」出结果卡。
不需要服务器、不需要联网、双击即可打开、可直接发给别人。

设计边界（重要）：
  · 计分、排序、平局兜底、编号、文字版卡片渲染，全部在 JS 里**逐行对齐**
    sorting_hat.py 的实现；--verify 用 node 分四段证明它们没走偏：
      1) 编译对拍：26 张卷（全部）的「题库 -> 卷」编译结果逐字段比对；
      2) 组合对拍：抽若干张卷遍历全部 3^11 = 177147 种作答，比对汇总校验和（--verify-papers）；
      3) 文字卡对拍：全部试卷 × 五种结局，逐字比对；
      4) 界面链路：用最小 DOM 桩驱动页面脚本，随机抽卷后四条作答路径跑到出卡，
         并检查词典标注与「麻瓜词典」抽屉。
  · 运行期不做任何随机抽题：卷是从 papers.json 里**读**的，页面只随机决定「用哪一张」。
    所以同一份答案 + 同一张卷，在页面里和文本里是同一个编号，可以互相复现。
  · 页面里出现的「帽子说的话」一律原样取自 houses.json，生成器与 JS 里不含任何一句判词。
  · 只有界面按钮文案（开始 / 上一题 / 提交判定 …）属于界面层，写在 UI_LABELS 里；
    词典解释属于资料层，写在 data/glossary.json 里。

用法：
    python scripts/build_quiz_html.py --out 分院帽.html
    python scripts/build_quiz_html.py --config alt --out 择堂冠.html
    python scripts/build_quiz_html.py --verify --node <node 可执行文件路径> [--verify-papers 8]
"""

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")

if HERE not in sys.path:
    sys.path.insert(0, HERE)
import sorting_hat as core  # noqa: E402  复用加载/编译/计分/渲染，保证单一数据源

EXIT_OK = 0
EXIT_CONFIG = 1
EXIT_USAGE = 3
EXIT_VERIFY = 4

# 界面层文案：只描述按钮与状态，不是帽子的台词，也不是词典的解释。
UI_LABELS = {
    "lang": "zh-CN",
    "start": "把帽子戴上",
    "restart": "再测一次（换一套题）",
    "prev": "上一题",
    "next": "下一题",
    "submit": "提交判定",
    "copy": "复制文字版",
    "copied": "已复制",
    "abstain": "你替我定",
    "progress": "第 {n} / {total} 题",
    "remain": "还有 {n} 题没答，答完才能提交。",
    "ready": "十一题齐了，交给我。",
    "picked": "已选",
    "skip_to": "跳到第 {n} 题",
    "degrade_note": "直接双击这个 HTML 文件就能作答；不用联网，也不用装任何东西。",
    "paper_badge": "卷号 {id}",
    "paper_note": "这一套题是从题库里随机抽的，每次打开都不一样。卷号是复现的唯一依据，卡片上也会印。",
    "dict_button": "麻瓜词典",
    "dict_button_alt": "名词表",
    "annot_on": "注释：开",
    "annot_off": "注释：关",
    "dict_close": "收起来",
    "pop_close": "知道了",
}


# ---------------------------------------------------------------- 宽度表

def build_wide_chars(*payloads):
    """把配置里出现的每个字符的终端显示宽度算好并嵌进页面。

    这样 JS 的 dwidth 与 Python unicodedata.east_asian_width 完全同源，
    不需要在 JS 里手写一套 CJK 区间猜测。
    """
    chars = set()
    for payload in payloads:
        for _, text in core.iter_strings(payload):
            chars.update(text)
    # 渲染器里直接拼进卡片的装饰字符
    chars.update("◆·─═　")

    wide = []
    narrow_zero = []
    for ch in sorted(chars):
        width = core.dwidth(ch)
        if width == 2:
            wide.append(ch)
        elif width == 0:
            narrow_zero.append(ch)
    return wide, narrow_zero


def build_glossary_payload(glossary):
    """词典进页面时同时给出两份顺序：

    · terms  —— 原文件顺序，用于「麻瓜词典」抽屉（作者按主题排列，读起来顺）；
    · match  —— 按词长降序的下标，用于正文标注（长词优先，避免「格兰芬多」被
                 「戈德里克·格兰芬多」这类长词切碎，也避免短词抢占长词的匹配位置）。
    排序在 Python 侧一次算好，页面只按给定顺序用，省掉一份可能分叉的排序实现。
    """
    if not glossary:
        return {"meta": {}, "terms": [], "match": []}
    terms = [{"term": t["term"], "gloss": t["gloss"], "house": bool(t.get("house"))}
             for t in glossary.get("terms", [])]
    order = sorted(range(len(terms)),
                   key=lambda i: (-len(terms[i]["term"]), terms[i]["term"]))
    return {"meta": glossary.get("meta", {}), "terms": terms, "match": order}


# ---------------------------------------------------------------- JS 芯

JS_CORE = r"""
/* ===== 数据（由 build_quiz_html.py 从 data/*.json 注入，单一数据源）===== */
const QUIZ = __QUIZ_JSON__;
const WIDE_CHARS = new Set(__WIDE_CHARS__);
const ZERO_WIDTH_CHARS = new Set(__ZERO_WIDTH_CHARS__);

/* ===== 宽度 / 折行 / 补白：对齐 sorting_hat.py ===== */
function dwidth(s) {
  let w = 0;
  for (const ch of s) {
    if (ZERO_WIDTH_CHARS.has(ch)) continue;
    w += WIDE_CHARS.has(ch) ? 2 : 1;
  }
  return w;
}
function padText(text, width, align) {
  const gap = Math.max(0, width - dwidth(text));
  if (align === 'right') return ' '.repeat(gap) + text;
  if (align === 'center') {
    const left = Math.floor(gap / 2);
    return ' '.repeat(left) + text + ' '.repeat(gap - left);
  }
  return text + ' '.repeat(gap);
}
function wrapText(text, limit) {
  const lines = [];
  let cur = '';
  for (const ch of text) {
    if (dwidth(cur + ch) > limit && cur) { lines.push(cur); cur = ch; }
    else cur += ch;
  }
  if (cur) lines.push(cur);
  return lines;
}

/* ===== 卷编译：逐行对齐 core.compile_paper =====
   slot.order[0..2] 依次展示为 A/B/C，权重跟着选项一起搬运；
   default 的位置也随选项顺序一起搬家。 */
const PAPER_CACHE = {};
function compilePaper(paperId) {
  if (PAPER_CACHE[paperId]) return PAPER_CACHE[paperId];
  const paper = QUIZ.papersById[String(paperId)];
  if (!paper) return null;
  const letters = 'ABCDEFGH';
  const out = [];
  for (let i = 0; i < paper.slots.length; i++) {
    const slot = paper.slots[i];
    const src = QUIZ.pool[String(slot.qid)];
    const byKey = {};
    src.options.forEach(o => { byKey[o.key] = o; });
    const options = slot.order.map((k, idx) => ({
      key: letters[idx], text: byKey[k].text, weights: byKey[k].weights,
    }));
    const want = src.default !== undefined ? src.default : (QUIZ.meta.default_option || 'B');
    const ord = slot.order.indexOf(want);
    out.push({
      id: i + 1, scene: src.scene, stem: src.stem,
      default: ord >= 0 ? letters[ord] : letters[0], options: options,
    });
  }
  PAPER_CACHE[paperId] = out;
  return out;
}

/* ===== 计分：对齐 compute_caps / score_answers / rank_houses / index_id ===== */
function round6(v) { return Math.round(v * 1e6) / 1e6; }

function computeCaps(questions, houseKeys) {
  const caps = {};
  houseKeys.forEach(h => caps[h] = 0);
  for (const q of questions) {
    const best = {};
    houseKeys.forEach(h => best[h] = 0);
    for (const opt of q.options) {
      for (const h in opt.weights) {
        if (h in best) best[h] = Math.max(best[h], opt.weights[h]);
      }
    }
    houseKeys.forEach(h => caps[h] += best[h]);
  }
  return caps;
}

function scoreAnswers(answers, questions, houseKeys, defaultOption) {
  const caps = computeCaps(questions, houseKeys);
  const raw = {}, missing = [], applied = [];
  houseKeys.forEach(h => raw[h] = 0);
  for (let pos = 0; pos < questions.length; pos++) {
    const q = questions[pos];
    let letter = answers[pos];
    if (letter === null || letter === undefined) {
      letter = q.default !== undefined ? q.default : defaultOption;
      missing.push(q.id);
    }
    let chosen = null;
    for (const opt of q.options) { if (opt.key === letter) { chosen = opt; break; } }
    if (chosen === null) return null;
    applied.push(letter);
    for (const h in chosen.weights) { if (h in raw) raw[h] += chosen.weights[h]; }
  }
  const score = {};
  houseKeys.forEach(h => score[h] = caps[h] ? raw[h] / caps[h] : 0.0);
  return { raw: raw, cap: caps, score: score, missing: missing, applied: applied };
}

function rankHouses(score, priority) {
  const prio = {};
  priority.forEach((h, i) => prio[h] = i);
  return Object.keys(score).sort((a, b) => {
    const ra = round6(score[a]), rb = round6(score[b]);
    if (ra !== rb) return rb - ra;
    return (prio[a] === undefined ? 99 : prio[a]) - (prio[b] === undefined ? 99 : prio[b]);
  });
}

/* CRC32，对齐 zlib.crc32 */
let CRC_TABLE = null;
function crcTable() {
  if (CRC_TABLE) return CRC_TABLE;
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  CRC_TABLE = t;
  return t;
}
function crc32(str) {
  const bytes = new TextEncoder().encode(str);
  const t = crcTable();
  let c = 0xFFFFFFFF;
  for (let i = 0; i < bytes.length; i++) c = t[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
function indexId(applied, paperId) {
  const seed = applied.join('') + '|' + QUIZ.profileStr + '|p' + paperId;
  return ('00000000' + crc32(seed).toString(16).toUpperCase()).slice(-8);
}

function analyze(answers, paperId) {
  const questions = compilePaper(paperId);
  const meta = QUIZ.meta, houseKeys = meta.houses;
  const result = scoreAnswers(answers, questions, houseKeys, meta.default_option || 'B');
  if (!result) return null;
  result.order = rankHouses(result.score, meta.tie_break_priority || houseKeys);
  result.top1 = result.order[0];
  result.top2 = result.order[1];
  result.gap = round6(result.score[result.top1] - result.score[result.top2]);
  const threshold = meta.threshold === undefined ? 0.12 : Number(meta.threshold);
  result.hesitate = result.gap <= threshold;
  result.paperId = paperId;
  result.id = indexId(result.applied, paperId);
  return result;
}

/* ===== 文字版卡片渲染：逐行对齐 render_card ===== */
function renderCard(result, optical) {
  const card = QUIZ.card;
  const cfg = card.lines;
  const labels = card.labels;
  const arch = card.archive_labels;
  const sep = card.identity_separator;
  const width = card.width;
  const houses = QUIZ.houses;
  const house = houses[result.house];
  const body = [];

  body.push('\u2550'.repeat(width));
  body.push(padText(card.title, width, 'center').replace(/\s+$/, ''));
  body.push('\u2550'.repeat(width));
  body.push(paperTag(result.paperId) + sep + card.index_label + ' ' + result.id);
  body.push('');

  body.push('\u25C6 ' + labels.house);
  let identity = house.name + sep + house.colors;
  if (optical.forced === 'user') identity += '\u3000' + cfg.yield_note;
  body.push('  ' + identity);
  body.push('');

  body.push('\u25C6 ' + labels.verdict);
  house.verdict.forEach(seg => body.push('  ' + seg));
  if (optical.abstain) {
    wrapText(cfg.abstain_tease, width - 2).forEach(seg => body.push('  ' + seg));
  }
  body.push('');

  body.push('\u25C6 ' + labels.founder);
  body.push('  ' + house.founder + sep + house.relic);
  body.push('');

  body.push('\u25C6 ' + labels.archive);
  const rows = [
    [arch.colors, house.colors],
    [arch.animal, house.animal],
    [arch.element, house.element],
    [arch.ghost, house.ghost],
    [arch.entry, house.entry],
  ];
  let labelW = 0;
  rows.forEach(r => labelW = Math.max(labelW, dwidth(r[0])));
  rows.forEach(r => body.push('  ' + padText(r[0], labelW) + '  ' + r[1]));
  body.push('');

  body.push('\u25C6 ' + labels.glow);
  house.glow.forEach(item => {
    const segs = wrapText(item, width - 4);
    body.push('  \u00B7 ' + segs[0]);
    segs.slice(1).forEach(seg => body.push('    ' + seg));
  });
  body.push('');

  body.push('\u25C6 ' + labels.roommate);
  house.roommate.forEach(item => {
    const segs = wrapText(item, width - 4);
    body.push('  \u00B7 ' + segs[0]);
    segs.slice(1).forEach(seg => body.push('    ' + seg));
  });
  body.push('');

  const pairWords = labels.affinity.split('/').map(s => s.trim());
  body.push('\u25C6 ' + labels.affinity);
  [[pairWords[0], 'affinity'], [pairWords[pairWords.length - 1], 'clash']].forEach(pair => {
    const item = house[pair[1]];
    const other = houses[item.house].name;
    const segs = wrapText(pair[0] + '\uFF1A' + other + sep + item.why, width - 2);
    body.push('  ' + segs[0]);
    segs.slice(1).forEach(seg => body.push('    ' + seg));
  });
  body.push('');

  body.push('\u25C6 ' + labels.last_word);
  wrapText(house.last_word, width - 2).forEach(seg => body.push('  ' + seg));
  body.push('');

  if (result.missing && result.missing.length) {
    const note = cfg.missing_note.replace('{ids}', result.missing.join('\u3001'));
    wrapText(note, width - 2).forEach(seg => body.push('  ' + seg));
  }

  body.push('\u2500'.repeat(width));
  body.push(cfg.share.replace('{house}', house.name));
  body.push('');
  cfg.declaration.forEach(item => {
    wrapText(item, width).forEach(seg => body.push(seg));
  });
  return body.join('\n');
}

function paperTag(paperId) {
  return QUIZ.card.paper_label + ' ' + String(paperId).padStart(2, '0');
}

/* ===== 对拍用：汇总校验和 + 编译结果签名 =====
   两段都由 node 驱动，Python 侧算同一串东西。 */
function fnv1a(str, seed) {
  let h = seed >>> 0;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}
function fnvLine(hash, line) { return fnv1a(line, hash); }

function enumSignature(paperId) {
  const questions = compilePaper(paperId);
  const n = questions.length;
  const picks = new Array(n).fill(0);
  let hash = 0x811C9DC5, count = 0;
  while (true) {
    const answers = picks.map((p, i) => questions[i].options[p].key);
    const r = analyze(answers, paperId);
    const line = answers.join('') + '|' + r.top1 + '|' + r.top2 + '|' + Math.round(r.gap * 1e6) +
                 '|' + (r.hesitate ? 1 : 0) + '|' + r.id;
    hash = fnvLine(hash, line);
    count++;
    let pos = n - 1;
    while (pos >= 0) {
      picks[pos]++;
      if (picks[pos] < questions[pos].options.length) break;
      picks[pos] = 0;
      pos--;
    }
    if (pos < 0) break;
  }
  return { hash: hash >>> 0, count: count };
}

function compiledSignature(paperId) {
  const questions = compilePaper(paperId);
  const parts = [];
  for (const q of questions) {
    const opts = q.options.map(o =>
      [o.key, o.text, QUIZ.meta.houses.map(h => o.weights[h] || 0).join(',')].join('~')
    ).join('~');
    parts.push([q.id, q.scene, q.stem, q.default, opts].join('\u0001'));
  }
  return parts.join('\u0002');
}
"""


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__PAGE_TITLE__</title>
<style>
  :root{
    --bg:#f5f2ea; --panel:#ffffff; --panel-2:#fbf9f4;
    --ink:#26221c; --ink-soft:#5d564a; --muted:#8b8375;
    --line:#e4ddcd; --line-2:#efe9dc;
    --accent:#8a6a2f; --accent-soft:#f2e8d3;
    --shadow:0 1px 2px rgba(60,48,24,.05), 0 12px 32px -12px rgba(60,48,24,.18);
    --gryffindor:#8b1a1a; --slytherin:#1f4d34; --ravenclaw:#1d3557; --hufflepuff:#8a6a2f;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{
    background:var(--bg); color:var(--ink);
    font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    -webkit-font-smoothing:antialiased;
    padding:28px 16px 80px;
  }
  .wrap{max-width:720px;margin:0 auto}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow)}
  .pad{padding:26px 28px}
  .muted{color:var(--muted)}
  .soft{color:var(--ink-soft)}
  .hidden{display:none !important}

  /* 顶部进度 */
  .bar{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:10px;padding:0 4px}
  .bar .label{font-size:13px;letter-spacing:.06em;color:var(--muted);font-variant-numeric:tabular-nums}
  .dots{display:flex;gap:6px;flex-wrap:wrap}
  .dot{width:22px;height:6px;border-radius:99px;background:var(--line);border:0;padding:0;cursor:pointer;transition:background .18s}
  .dot.done{background:var(--accent)}
  .dot.cur{background:var(--ink);}

  /* 工具行：麻瓜词典 + 注释开关 */
  .tools{display:flex;gap:8px;justify-content:flex-end;margin-bottom:14px;padding:0 4px}
  .btn.tiny{font-size:13px;padding:5px 12px;border-radius:99px;color:var(--ink-soft)}
  .btn.tiny.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}

  /* 歌谣 */
  .song{white-space:pre-wrap;font-size:15px;line-height:2;color:var(--ink-soft)}
  .song .intro{color:var(--muted);font-size:14px}
  h1.title{margin:0 0 10px;font-size:20px;letter-spacing:.04em}
  hr.rule{border:0;border-top:1px solid var(--line-2);margin:20px 0}
  .paperline{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 14px}
  .badge{display:inline-block;font-size:13px;letter-spacing:.1em;font-variant-numeric:tabular-nums;
         background:var(--accent-soft);color:var(--accent);border-radius:99px;padding:3px 12px}
  .paperline .why{font-size:12px;color:var(--muted)}

  /* 题目 */
  .scene{display:inline-flex;align-items:center;gap:8px;font-size:13px;letter-spacing:.08em;color:var(--accent);
         background:var(--accent-soft);border-radius:99px;padding:4px 12px;margin-bottom:14px}
  .stem{font-size:17px;line-height:1.9;margin:0 0 20px}
  .opts{display:flex;flex-direction:column;gap:10px}
  .opt{
    display:flex;gap:14px;align-items:flex-start;width:100%;text-align:left;
    background:var(--panel);border:1px solid var(--line);border-radius:12px;
    padding:14px 16px;cursor:pointer;font:inherit;color:var(--ink);
    transition:border-color .16s, background .16s, transform .16s;
  }
  .opt:hover{border-color:var(--accent);transform:translateY(-1px)}
  .opt .key{
    flex:0 0 26px;height:26px;border-radius:8px;background:var(--accent-soft);color:var(--accent);
    display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;
  }
  .opt .txt{flex:1}
  .opt.on{border-color:var(--accent);background:var(--accent-soft)}
  .opt.on .key{background:var(--accent);color:#fff}
  .opt.on .txt::after{content:"__PICKED__";font-size:12px;color:var(--accent);margin-left:8px}

  /* 词典标注 */
  .gl{
    font:inherit;color:inherit;background:none;border:0;padding:0 1px;margin:0;cursor:help;
    border-bottom:1px dashed var(--accent);text-decoration:none;line-height:inherit;
  }
  .gl:hover{background:var(--accent-soft)}
  .gl[data-h="1"]{border-bottom-color:var(--gryffindor)}

  /* 词典抽屉 */
  .drawer{position:fixed;left:0;right:0;bottom:0;z-index:40;background:var(--panel);
          border-top:1px solid var(--line);box-shadow:0 -12px 40px -18px rgba(60,48,24,.35);
          max-height:72vh;overflow:auto;transform:translateY(102%);transition:transform .22s ease}
  .drawer.open{transform:translateY(0)}
  .drawer .inner{max-width:720px;margin:0 auto;padding:22px 24px 34px}
  .drawer h2{font-size:13px;letter-spacing:.16em;color:var(--accent);margin:0 0 6px}
  .drawer .lead{font-size:14px;color:var(--ink-soft);margin:0 0 4px}
  .drawer .scope{font-size:12px;color:var(--muted);margin:0 0 16px}
  .gloss-list{border-top:1px solid var(--line-2)}
  .gloss-list .row{padding:11px 2px;border-bottom:1px solid var(--line-2)}
  .gloss-list .t{font-weight:600}
  .gloss-list .g{font-size:14px;color:var(--ink-soft);line-height:1.8}
  .drawer .foot{display:flex;justify-content:flex-end;margin-top:18px}

  /* 点词弹层 */
  .pop{position:fixed;left:12px;right:12px;bottom:14px;z-index:50;background:var(--panel);
       border:1px solid var(--accent);border-radius:14px;box-shadow:var(--shadow);
       max-width:640px;margin:0 auto;padding:16px 18px}
  .pop .t{font-weight:600;margin:0 0 4px;color:var(--accent)}
  .pop .g{margin:0;font-size:15px;line-height:1.85}
  .pop .x{position:absolute;top:10px;right:12px}

  /* 底部导航 */
  .nav{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:22px}
  .btn{
    border:1px solid var(--line);background:var(--panel);color:var(--ink);
    border-radius:10px;padding:10px 18px;font:inherit;cursor:pointer;transition:.16s;
  }
  .btn:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
  .btn:disabled{opacity:.45;cursor:not-allowed}
  .btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
  .btn.primary:hover:not(:disabled){filter:brightness(1.08);color:#fff}
  .hint{font-size:13px;color:var(--muted);text-align:center;margin-top:12px;min-height:20px}

  /* 结果 */
  .card-head{border-bottom:1px solid var(--line-2);padding-bottom:18px;margin-bottom:20px}
  .id{font-size:12px;letter-spacing:.14em;color:var(--muted);font-variant-numeric:tabular-nums}
  .house-name{font-size:30px;font-weight:700;letter-spacing:.02em;margin:6px 0 4px}
  .house-colors{font-size:14px;color:var(--muted)}
  .sec{margin:0 0 20px}
  .sec h2{font-size:12px;letter-spacing:.16em;color:var(--accent);margin:0 0 8px;font-weight:600}
  .sec p{margin:0 0 4px;line-height:1.95}
  .sec ul{margin:0;padding-left:18px}
  .sec li{margin:0 0 6px;line-height:1.9}
  .kv{display:grid;grid-template-columns:96px 1fr;gap:4px 14px;font-size:15px}
  .kv .k{color:var(--muted)}
  .verdict{font-size:17px;line-height:2.05}
  .tease{color:var(--accent);font-size:15px}
  .yield{font-size:13px;color:var(--muted);margin-left:6px}
  .hatsays{background:var(--panel-2);border:1px solid var(--line-2);border-left:3px solid var(--accent);
           border-radius:10px;padding:14px 18px;margin-bottom:18px}
  .hatsays p{margin:0;line-height:1.9}
  .share{text-align:center;font-size:17px;letter-spacing:.02em;margin:22px 0 6px}
  .decl{font-size:12px;line-height:1.8;color:var(--muted);border-top:1px solid var(--line-2);padding-top:14px}
  .row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:20px}
</style>
</head>
<body>
<div class="wrap">

  <div class="bar">
    <span class="label" id="progress"></span>
    <div class="dots" id="dots"></div>
  </div>
  <div class="tools">
    <button class="btn tiny" id="btn-dict">__UI_DICT__</button>
    <button class="btn tiny on" id="btn-annot">__UI_ANNOT_ON__</button>
  </div>

  <!-- 封面：歌谣 -->
  <section class="panel pad" id="screen-intro">
    <h1 class="title">__PAGE_TITLE__</h1>
    <div class="paperline">
      <span class="badge" id="paper-badge"></span>
      <span class="why" id="paper-why"></span>
    </div>
    <div class="song" id="song"></div>
    <hr class="rule">
    <div class="muted" id="fallback-note" style="font-size:13px"></div>
    <div class="row" style="justify-content:flex-start">
      <button class="btn primary" id="btn-start">__UI_START__</button>
    </div>
  </section>

  <!-- 答题 -->
  <section class="panel pad hidden" id="screen-quiz">
    <div class="scene" id="scene"></div>
    <p class="stem" id="stem"></p>
    <div class="opts" id="opts"></div>
    <div class="nav">
      <button class="btn" id="btn-prev">__UI_PREV__</button>
      <button class="btn primary" id="btn-next">__UI_NEXT__</button>
    </div>
    <div class="hint" id="hint"></div>
  </section>

  <!-- 第三轮：帽子问你想去哪 -->
  <section class="panel pad hidden" id="screen-will">
    <div class="hatsays" id="will-words"></div>
    <div class="opts" id="will-opts"></div>
    <div class="hint" id="will-hint"></div>
  </section>

  <!-- 结果 -->
  <section class="panel pad hidden" id="screen-result">
    <div id="result-body"></div>
  </section>

</div>

<!-- 点词弹层 -->
<div class="pop hidden" id="pop">
  <button class="btn tiny x" id="pop-close">__UI_POP_CLOSE__</button>
  <p class="t" id="pop-term"></p>
  <p class="g" id="pop-gloss"></p>
</div>

<!-- 麻瓜词典 -->
<div class="drawer" id="drawer">
  <div class="inner">
    <h2 id="dict-title"></h2>
    <p class="lead" id="dict-intro"></p>
    <p class="scope" id="dict-scope"></p>
    <div class="gloss-list" id="dict-list"></div>
    <div class="foot"><button class="btn primary" id="dict-close">__UI_DICT_CLOSE__</button></div>
  </div>
</div>

<script>
__JS_CORE__

/* ================================================================
   界面层
   ================================================================ */
const UI = QUIZ.ui;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* ---------- 词典标注 ---------- */
const GLOSS = QUIZ.glossary || { meta: {}, terms: [], match: [] };
const GLOSS_TERMS = GLOSS.terms;
const GLOSS_MATCH = GLOSS.match;
let annotOn = true;

/* 把一段纯文本里的词条包成可点的按钮。
   allowHouses=false 时不标注带学院信息的词条——题干与选项必须干净，
   否则答题的人还没选就先被剧透了。同一个词条在同一段里只标第一处。 */
function annotate(text, allowHouses) {
  const src = String(text);
  if (!annotOn || !GLOSS_MATCH.length) return esc(src);
  const marks = [];
  for (const gi of GLOSS_MATCH) {
    const g = GLOSS_TERMS[gi];
    if (!g || (g.house && !allowHouses)) continue;
    let from = 0;
    while (true) {
      const at = src.indexOf(g.term, from);
      if (at < 0) break;
      const end = at + g.term.length;
      let clash = false;
      for (const m of marks) { if (at < m.end && end > m.start) { clash = true; break; } }
      if (!clash) { marks.push({ start: at, end: end, g: g }); break; }
      from = at + 1;
    }
  }
  if (!marks.length) return esc(src);
  marks.sort((a, b) => a.start - b.start);
  let out = '', pos = 0;
  for (const m of marks) {
    out += esc(src.slice(pos, m.start));
    out += '<button type="button" class="gl" data-h="' + (m.g.house ? '1' : '0') +
           '" data-t="' + esc(m.g.term) + '">' + esc(src.slice(m.start, m.end)) + '</button>';
    pos = m.end;
  }
  out += esc(src.slice(pos));
  return out;
}

function showGloss(term) {
  const g = GLOSS_TERMS.find(t => t.term === term);
  if (!g) return;
  $('pop-term').textContent = g.term;
  $('pop-gloss').textContent = g.gloss;
  $('pop').classList.remove('hidden');
}
function closeGloss() { $('pop').classList.add('hidden'); }

function setAnnot(on) {
  annotOn = !!on;
  const b = $('btn-annot');
  b.textContent = annotOn ? UI.annot_on : UI.annot_off;
  if (annotOn) b.classList.add('on'); else b.classList.remove('on');
  if (!$('screen-quiz').classList.contains('hidden')) renderQuestion();
  else if (!$('screen-result').classList.contains('hidden') && state.optical) showResult(state.optical);
  else renderIntro();
}

function openDict() { $('drawer').classList.add('open'); }
function closeDict() { $('drawer').classList.remove('open'); }

function renderDict() {
  $('dict-title').textContent = GLOSS.meta.title || UI.dict_button;
  $('dict-intro').textContent = GLOSS.meta.intro || GLOSS.meta.empty || '';
  $('dict-scope').textContent = GLOSS.meta.scope_note || '';
  const box = $('dict-list');
  box.innerHTML = GLOSS_TERMS.map(g =>
    '<div class="row"><div class="t">' + esc(g.term) + '</div>' +
    '<div class="g">' + esc(g.gloss) + '</div></div>').join('');
}

/* ---------- 状态 ---------- */
const state = {
  paperId: null,
  answers: [],
  index: 0,
  result: null,
  optical: null,
};
let TOTAL = 0;
let advanceTimer = null;

/* 抽一张卷：真随机（crypto 优先），抽完把卷号摆到台面上。
   抽卷是运行期唯一的随机动作，且只影响"用哪张卷"，不影响任何一题的计分。 */
function pickPaperId() {
  const ids = QUIZ.papers;
  let k = 0;
  try {
    const buf = new Uint32Array(1);
    (window.crypto || window.msCrypto).getRandomValues(buf);
    k = buf[0];
  } catch (e) {
    k = Math.floor(Math.random() * 4294967296);
  }
  return ids[k % ids.length];
}

function newPaper(paperId) {
  state.paperId = paperId === undefined ? pickPaperId() : paperId;
  TOTAL = compilePaper(state.paperId).length;
  state.answers = new Array(TOTAL).fill(null);
  state.index = 0;
  state.result = null;
  state.optical = null;
}
function setPaperId(paperId) { newPaper(paperId); }

/* ---------- 封面 ---------- */
function renderIntro() {
  $('paper-badge').textContent = UI.paper_badge.replace('{id}', pad2(state.paperId));
  $('paper-why').textContent = UI.paper_note;
  $('song').innerHTML =
    '<span class="intro">' + annotate(QUIZ.card.song_intro, true) + '</span>\n\n' +
    QUIZ.card.song.map(l => annotate(l, true)).join('\n');
  $('fallback-note').textContent = UI.degrade_note;
  $('screen-intro').classList.remove('hidden');
  $('screen-quiz').classList.add('hidden');
  $('screen-will').classList.add('hidden');
  $('screen-result').classList.add('hidden');
  $('progress').textContent = '';
  renderDots();
}
function pad2(n) { return String(n).padStart(2, '0'); }

/* ---------- 进度点 ---------- */
function renderDots() {
  const box = $('dots');
  box.innerHTML = '';
  if ($('screen-quiz').classList.contains('hidden')) return;
  for (let i = 0; i < TOTAL; i++) {
    const b = document.createElement('button');
    b.className = 'dot' + (state.answers[i] ? ' done' : '') + (i === state.index ? ' cur' : '');
    b.title = UI.skip_to.replace('{n}', i + 1);
    b.onclick = () => { state.index = i; renderQuestion(); };
    box.appendChild(b);
  }
}

/* ---------- 答题屏 ---------- */
function renderQuestion() {
  const q = compilePaper(state.paperId)[state.index];
  $('screen-intro').classList.add('hidden');
  $('screen-will').classList.add('hidden');
  $('screen-result').classList.add('hidden');
  $('screen-quiz').classList.remove('hidden');

  $('progress').textContent = UI.progress.replace('{n}', state.index + 1).replace('{total}', TOTAL);
  $('scene').innerHTML = '\u3010' + q.id + '\u3011' + annotate(q.scene, false);
  $('stem').innerHTML = annotate(q.stem, false);

  const box = $('opts');
  box.innerHTML = '';
  q.options.forEach(opt => {
    const b = document.createElement('button');
    b.className = 'opt' + (state.answers[state.index] === opt.key ? ' on' : '');
    b.innerHTML = '<span class="key">' + esc(opt.key) + '</span><span class="txt">' +
      annotate(opt.text, false) + '</span>';
    b.onclick = () => choose(opt.key);
    box.appendChild(b);
  });

  $('btn-prev').disabled = state.index === 0;
  const last = state.index === TOTAL - 1;
  $('btn-next').textContent = last ? UI.submit : UI.next;
  $('btn-next').disabled = last ? !allAnswered() : false;
  $('hint').textContent = last
    ? (allAnswered() ? UI.ready : UI.remain.replace('{n}', TOTAL - answeredCount()))
    : '';
  renderDots();
}

function answeredCount() { return state.answers.filter(a => a).length; }
function allAnswered() { return answeredCount() === TOTAL; }

function choose(key) {
  state.answers[state.index] = key;
  renderQuestion();
  if (state.index < TOTAL - 1) {
    clearTimeout(advanceTimer);
    advanceTimer = setTimeout(() => {
      if (state.index < TOTAL - 1 && state.answers[state.index]) {
        state.index++;
        renderQuestion();
      }
    }, 220);
  }
}

function submit() {
  if (!allAnswered()) return;
  state.result = analyze(state.answers.slice(), state.paperId);
  if (state.result.hesitate) renderWill();
  else showResult({ house: state.result.top1, forced: null, abstain: false });
}

/* ---------- 第三轮 ---------- */
function renderWill() {
  $('screen-quiz').classList.add('hidden');
  $('screen-result').classList.add('hidden');
  $('screen-will').classList.remove('hidden');

  const r = state.result;
  const words = [].concat(QUIZ.card.focus_comment[r.top1], [''],
    [QUIZ.card.lines.hesitate_1, QUIZ.card.lines.hesitate_2, QUIZ.card.lines.round3_hint]);
  $('will-words').innerHTML = words.map(w => '<p>' + annotate(w, true) + '</p>').join('');

  const box = $('will-opts');
  box.innerHTML = '';
  QUIZ.meta.houses.forEach((key, i) => {
    const b = document.createElement('button');
    b.className = 'opt';
    b.innerHTML = '<span class="key">' + String.fromCharCode(65 + i) + '</span><span class="txt">' +
      esc(QUIZ.houses[key].name) + '</span>';
    b.onclick = () => showResult({ house: key, forced: key === r.top1 ? null : 'user', abstain: false });
    box.appendChild(b);
  });
  const b = document.createElement('button');
  b.className = 'opt';
  b.innerHTML = '<span class="key">\u00B7</span><span class="txt">' + esc(UI.abstain) + '</span>';
  b.onclick = () => showResult({ house: r.order[0], forced: null, abstain: true });
  box.appendChild(b);

  $('will-hint').textContent = '';
  $('progress').textContent = '';
}

/* ---------- 结果 ---------- */
function houseAccent(key) { return getComputedStyle(document.documentElement).getPropertyValue('--' + key) || 'var(--accent)'; }

function showResult(optical) {
  const r = state.result;
  r.house = optical.house;
  state.optical = optical;
  const house = QUIZ.houses[r.house];
  const labels = QUIZ.card.labels, arch = QUIZ.card.archive_labels, sep = QUIZ.card.identity_separator;

  const parts = [];
  parts.push('<div class="card-head">');
  parts.push('<div class="id">' + esc(paperTag(r.paperId) + sep + QUIZ.card.index_label + ' ' + r.id) + '</div>');
  parts.push('<div class="house-name" style="color:' + houseAccent(r.house) + '">' + esc(house.name) +
    (optical.forced === 'user' ? '<span class="yield">' + esc(QUIZ.card.lines.yield_note) + '</span>' : '') + '</div>');
  parts.push('<div class="house-colors">' + esc(house.colors) + '</div>');
  parts.push('</div>');

  const hatWords = QUIZ.card.focus_comment[r.top1].slice();
  if (optical.forced === 'user') hatWords.push('', QUIZ.card.lines.yield_tease);
  if (optical.abstain) hatWords.push('', QUIZ.card.lines.abstain_tease);
  parts.push('<div class="hatsays">' + hatWords.map(w => '<p>' + annotate(w || '\u00A0', true) + '</p>').join('') + '</div>');

  parts.push('<div class="sec"><h2>' + annotate(labels.verdict, true) + '</h2><div class="verdict">' +
    house.verdict.map(t => annotate(t, true)).join('<br>') + '</div></div>');

  parts.push('<div class="sec"><h2>' + annotate(labels.founder, true) + '</h2><p>' +
    annotate(house.founder + sep + house.relic, true) + '</p></div>');

  parts.push('<div class="sec"><h2>' + annotate(labels.archive, true) + '</h2><div class="kv">' +
    [[arch.colors, house.colors], [arch.animal, house.animal], [arch.element, house.element],
     [arch.ghost, house.ghost], [arch.entry, house.entry]]
      .map(row => '<div class="k">' + annotate(row[0], true) + '</div><div>' + annotate(row[1], true) + '</div>').join('') +
    '</div></div>');

  parts.push('<div class="sec"><h2>' + annotate(labels.glow, true) + '</h2><ul>' +
    house.glow.map(t => '<li>' + annotate(t, true) + '</li>').join('') + '</ul></div>');

  parts.push('<div class="sec"><h2>' + annotate(labels.roommate, true) + '</h2><ul>' +
    house.roommate.map(t => '<li>' + annotate(t, true) + '</li>').join('') + '</ul></div>');

  const pairWords = labels.affinity.split('/').map(s => s.trim());
  parts.push('<div class="sec"><h2>' + annotate(labels.affinity, true) + '</h2>' +
    [[pairWords[0], 'affinity'], [pairWords[pairWords.length - 1], 'clash']].map(pair => {
      const item = house[pair[1]];
      return '<p>' + annotate(pair[0] + '\uFF1A' + QUIZ.houses[item.house].name + sep + item.why, true) + '</p>';
    }).join('') + '</div>');

  parts.push('<div class="sec"><h2>' + annotate(labels.last_word, true) + '</h2><p class="verdict">' +
    annotate(house.last_word, true) + '</p></div>');

  parts.push('<div class="share">' + esc(QUIZ.card.lines.share.replace('{house}', house.name)) + '</div>');
  parts.push('<div class="decl">' + QUIZ.card.lines.declaration.map(esc).join('<br>') + '</div>');
  parts.push('<div class="row"><button class="btn" id="btn-copy">' + esc(UI.copy) +
    '</button><button class="btn primary" id="btn-restart">' + esc(UI.restart) + '</button></div>');

  $('result-body').innerHTML = parts.join('');
  $('screen-intro').classList.add('hidden');
  $('screen-quiz').classList.add('hidden');
  $('screen-will').classList.add('hidden');
  $('screen-result').classList.remove('hidden');
  $('progress').textContent = '';
  $('dots').innerHTML = '';
  if (window.scrollTo) window.scrollTo({ top: 0, behavior: 'smooth' });

  $('btn-restart').onclick = reset;
  $('btn-copy').onclick = copyText;
}

function textVersion() {
  const r = state.result, o = state.optical;
  const head = QUIZ.card.focus_comment[r.top1].join('\n');
  let out = head + '\n\n';
  if (o.forced === 'user') out += QUIZ.card.lines.yield_tease + '\n\n';
  return out + renderCard(r, o);
}

function copyText() {
  const text = textVersion();
  const done = () => { $('btn-copy').textContent = UI.copied; setTimeout(() => { $('btn-copy').textContent = UI.copy; }, 1600); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  } else fallbackCopy(text, done);
}
function fallbackCopy(text, done) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); done(); } catch (e) {}
  document.body.removeChild(ta);
}

/* 再测一次 = 换一套题。卷号跟着换，编号也跟着换。 */
function reset() {
  closeGloss();
  newPaper();
  renderIntro();
}

/* ---------- 交互绑定 ---------- */
document.addEventListener('click', ev => {
  const hit = ev.target && ev.target.closest ? ev.target.closest('.gl') : null;
  if (hit) { showGloss(hit.getAttribute('data-t')); return; }
  const pop = $('pop');
  if (!pop.classList.contains('hidden') && !pop.contains(ev.target)) closeGloss();
});

document.addEventListener('keydown', ev => {
  if (!$('screen-quiz').classList.contains('hidden')) {
    const k = ev.key.toUpperCase();
    const q = compilePaper(state.paperId)[state.index];
    let hit = null;
    if (/^[A-Z]$/.test(k)) hit = q.options.find(o => o.key === k);
    if (!hit && /^[1-9]$/.test(ev.key)) hit = q.options[Number(ev.key) - 1];
    if (hit) { ev.preventDefault(); choose(hit.key); return; }
    if (ev.key === 'ArrowLeft') { ev.preventDefault(); $('btn-prev').click(); }
    if (ev.key === 'ArrowRight' || ev.key === 'Enter') { ev.preventDefault(); if (!$('btn-next').disabled) $('btn-next').click(); }
  } else if (!$('screen-result').classList.contains('hidden') && ev.key === 'Enter') {
    reset();
  }
  if (ev.key === 'Escape') { closeGloss(); closeDict(); }
});

$('btn-start').onclick = () => { state.index = 0; renderQuestion(); };
$('btn-prev').onclick = () => { if (state.index > 0) { state.index--; renderQuestion(); } };
$('btn-next').onclick = () => {
  if (state.index === TOTAL - 1) submit();
  else if (state.answers[state.index]) { state.index++; renderQuestion(); }
};
$('btn-dict').onclick = openDict;
$('dict-close').onclick = closeDict;
$('pop-close').onclick = closeGloss;
$('btn-annot').onclick = () => setAnnot(!annotOn);

renderDict();
newPaper();
renderIntro();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- 组装

def build_quiz_payload(houses_data, questions_data, papers_data, glossary_data, config_label="canon"):
    wide, zero = build_wide_chars(houses_data, questions_data, papers_data, glossary_data or {})
    meta = questions_data["meta"]
    pool = {}
    for q in questions_data["questions"]:
        pool[str(q["id"])] = {
            "scene": q["scene"],
            "stem": q["stem"],
            "default": q.get("default"),
            "options": [{"key": o["key"], "text": o["text"], "weights": o["weights"]} for o in q["options"]],
        }
    ui = dict(UI_LABELS)
    if config_label == "alt":
        ui["dict_button"] = UI_LABELS["dict_button_alt"]
    payload = {
        "meta": meta,
        "pool": pool,
        "papers": [p["id"] for p in papers_data["papers"]],
        "papersById": {str(p["id"]): p for p in papers_data["papers"]},
        "card": houses_data["card"],
        "houses": houses_data["houses"],
        "glossary": build_glossary_payload(glossary_data),
        # 与 Python index_id 完全一致：str(meta["houses"]) + "|p" + 卷号
        "profileStr": str(meta.get("houses")),
        "ui": ui,
    }
    return payload, wide, zero


def render_html(houses_data, questions_data, papers_data, glossary_data, config_label="canon"):
    payload, wide, zero = build_quiz_payload(houses_data, questions_data, papers_data,
                                            glossary_data, config_label)
    title = houses_data["card"]["title"]
    page_title = "%s · %s" % (title, config_label) if config_label not in ("canon", "main") else title

    js = (JS_CORE
          .replace("__QUIZ_JSON__", json.dumps(payload, ensure_ascii=False, indent=None, separators=(",", ":")))
          .replace("__WIDE_CHARS__", json.dumps(wide, ensure_ascii=False))
          .replace("__ZERO_WIDTH_CHARS__", json.dumps(zero, ensure_ascii=False)))

    html = (HTML_TEMPLATE
            .replace("__LANG__", UI_LABELS["lang"])
            .replace("__PAGE_TITLE__", page_title)
            .replace("__UI_START__", UI_LABELS["start"])
            .replace("__UI_PREV__", UI_LABELS["prev"])
            .replace("__UI_NEXT__", UI_LABELS["next"])
            .replace("__UI_DICT__", UI_LABELS["dict_button_alt"] if config_label == "alt" else UI_LABELS["dict_button"])
            .replace("__UI_ANNOT_ON__", UI_LABELS["annot_on"])
            .replace("__UI_POP_CLOSE__", UI_LABELS["pop_close"])
            .replace("__UI_DICT_CLOSE__", UI_LABELS["dict_close"])
            .replace("__PICKED__", "·" + UI_LABELS["picked"])
            .replace("__JS_CORE__", js))
    return html


# ---------------------------------------------------------------- 对拍

def py_enum_signature(paper_id, questions_data, papers_data):
    """Python 侧：遍历全部组合算同一个 FNV-1a 校验和。"""
    meta = questions_data["meta"]
    questions = core.paper_questions(papers_data, questions_data, paper_id)
    n = len(questions)
    picks = [0] * n
    hashv = 0x811C9DC5
    count = 0
    while True:
        answers = [questions[i]["options"][picks[i]]["key"] for i in range(n)]
        r = core.analyze(answers, questions, meta, paper_id)
        line = "%s|%s|%s|%d|%d|%s" % (
            "".join(answers), r["top1"], r["top2"],
            int(round(r["gap"] * 1e6)), 1 if r["hesitate"] else 0, r["id"])
        for ch in line:
            hashv ^= ord(ch)
            hashv = (hashv * 0x01000193) & 0xFFFFFFFF
        count += 1
        pos = n - 1
        while pos >= 0:
            picks[pos] += 1
            if picks[pos] < len(questions[pos]["options"]):
                break
            picks[pos] = 0
            pos -= 1
        if pos < 0:
            break
    return {"hash": hashv, "count": count}


def py_compiled_signature(paper_id, questions_data, papers_data):
    """与 JS compiledSignature 逐字段一致：选项内用 ~，题内用 \\u0001，题间用 \\u0002。"""
    meta = questions_data["meta"]
    questions = core.paper_questions(papers_data, questions_data, paper_id)
    parts = []
    for q in questions:
        opts = "~".join("%s~%s~%s" % (
            o["key"], o["text"], ",".join(str(o["weights"].get(h, 0)) for h in meta["houses"]))
            for o in q["options"])
        parts.append("\u0001".join([str(q["id"]), q["scene"], q["stem"], q["default"], opts]))
    return "\u0002".join(parts)


# 文字卡对拍用的固定作答串：不依赖枚举，任何一张卷都能跑
CARD_CASE_ANSWERS = ["AAAAAAAAAAA", "ABCABCABCAB"]


def py_card_cases(houses_data, questions_data, papers_data, paper_ids):
    """每一张卷 × 五种结局的文字卡，全部逐字比对。

    刻意用固定作答串而不是枚举出来的组合：枚举已经由组合对拍那一段守住，
    这一段要守的是「渲染」，尤其是缺答补默认项——默认项的位置随选项顺序搬过家，
    是最容易悄悄写死成 B 的地方。
    """
    meta = questions_data["meta"]
    specs = []
    for pid in paper_ids:
        questions = core.paper_questions(papers_data, questions_data, pid)
        for letters in CARD_CASE_ANSWERS:
            r = core.analyze(list(letters), questions, meta, pid)
            specs.append(("卷%02d/正常-%s" % (pid, letters), pid, letters, r["top1"], None, False))
        r0 = core.analyze(list(CARD_CASE_ANSWERS[0]), questions, meta, pid)
        specs.append(("卷%02d/让步" % pid, pid, CARD_CASE_ANSWERS[0], r0["order"][-1], "user", False))
        specs.append(("卷%02d/弃权" % pid, pid, CARD_CASE_ANSWERS[0], r0["order"][0], None, True))
    specs.append(("卷%02d/缺答补默认项" % paper_ids[0], paper_ids[0], "1A 2B",
                  None, None, False))

    cases = []
    hyp = []
    for name, pid, letters, house, forced, abstain in specs:
        questions = core.paper_questions(papers_data, questions_data, pid)
        parsed, _, err = core.parse_answers(letters, questions)
        if err:
            raise RuntimeError("对拍用例答案串解析失败：%s -> %s" % (letters, err))
        res = core.analyze(parsed, questions, meta, pid)
        res["house"] = house if house else res["top1"]
        # answers 直接给数组、缺项给 null：页面侧的 analyze() 认的就是 null，
        # 换成空串或空格会被当成一个非法字母位而返回 null（整条链路静默炸掉）
        hyp.append({"name": name, "paperId": pid, "answers": list(parsed),
                    "house": res["house"], "forced": forced, "abstain": abstain})
        cases.append((name, core.render_card(res, houses_data, forced=forced, abstain=abstain)))
    return hyp, cases


def find_node(explicit):
    if explicit:
        return explicit if os.path.exists(explicit) else None
    for cand in (os.environ.get("NODE_BIN"), shutil.which("node"), shutil.which("node.exe")):
        if cand and os.path.exists(cand):
            return cand
    return None


# 交互链路冒烟驱动：用最小 DOM 桩跑页面里的真实脚本，
# 模拟「点选项 → 翻页 → 提交判定 → 出结果」，并把页面产出的文字卡回传比对。
UI_DRIVER_JS = r"""
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const plan = JSON.parse(process.argv[3]);

const code = html.match(/<script>([\s\S]*?)<\/script>/)[1];

const els = {};
function mkEl(id) {
  const el = {
    id: id || '', _cls: new Set(), children: [], onclick: null,
    disabled: false, title: '', textContent: '', style: {}, _html: '',
    // className 与 classList 在浏览器里是同一份东西，桩里也必须同源
    get className() { return [...el._cls].join(' '); },
    set className(v) { el._cls = new Set(String(v).split(/\s+/).filter(Boolean)); },
    classList: {
      add: (...c) => c.forEach(x => el._cls.add(x)),
      remove: (...c) => c.forEach(x => el._cls.delete(x)),
      contains: c => el._cls.has(c),
    },
    appendChild(c) { el.children.push(c); return c; },
    get innerHTML() { return el._html; },
    set innerHTML(v) { el._html = v; el.children.length = 0; },
    contains() { return false; },
    select() {},
  };
  return el;
}
const getEl = id => (els[id] || (els[id] = mkEl(id)));
['screen-quiz', 'screen-will', 'screen-result'].forEach(id => getEl(id).classList.add('hidden'));

global.document = {
  getElementById: getEl,
  createElement: () => mkEl(),
  addEventListener: () => {},
  body: mkEl('body'),
  documentElement: mkEl('root'),
  execCommand: () => true,
};
global.window = { scrollTo() {}, crypto: null };
global.getComputedStyle = () => ({ getPropertyValue: () => '#8a6a2f' });
global.navigator = {};
// 同步驱动全部点击，不跑自动翻页定时器（它只是手感优化，与结果无关）
global.setTimeout = () => 0;
global.clearTimeout = () => {};

let captured = null;
eval(code + '\n;captured = { textVersion, state, QUIZ, $, renderQuestion, setPaperId, ' +
     'annotate, showGloss, setAnnot, renderDict, compilePaper, analyze, pad2 };');
const t = captured;

/* —— 卷由外部指定，界面链路要可复现 —— */
t.setPaperId(plan.paperId);
const paperId = t.state.paperId;
if (paperId !== plan.paperId) throw new Error('卷号没有生效：' + paperId);
const total = t.QUIZ.papersById[String(paperId)].slots.length;
if (t.state.answers.length !== total) throw new Error('题数与卷不符');

/* —— 词典：抽屉内容 + 标注范围 —— */
const terms = t.QUIZ.glossary.terms;
t.renderDict();
const drawerHtml = t.$('dict-list').innerHTML;
if (terms.length) {
  for (const g of terms) {
    if (drawerHtml.indexOf(g.term) < 0) throw new Error('词典抽屉缺少词条：' + g.term);
  }
  if (t.$('dict-title').textContent !== t.QUIZ.glossary.meta.title) throw new Error('词典标题不对');
  // 用例从词典自己身上取，别写死某个配置的词条（canon / alt 的词条完全不同）
  const anyTerm = terms[0];
  const houseTerm = terms.find(g => g.house);
  if (t.annotate(anyTerm.term, false).indexOf('class="gl"') < 0) throw new Error('普通词条没有被标注');
  if (houseTerm) {
    // 题干与选项里绝不能出现带学院信息的标注，否则答题前就被剧透了
    if (t.annotate(houseTerm.term, false).indexOf('data-h="1"') >= 0) {
      throw new Error('题干里出现了学院类标注（会泄题）');
    }
    if (t.annotate(houseTerm.term, true).indexOf('data-h="1"') < 0) {
      throw new Error('结果页没有出现学院类标注');
    }
  }
  t.showGloss(anyTerm.term);
  if (t.$('pop-term').textContent !== anyTerm.term) throw new Error('点词弹层没显示词条名');
  if (t.$('pop-gloss').textContent !== anyTerm.gloss) throw new Error('点词弹层没显示解释');
  if (t.$('pop').classList.contains('hidden')) throw new Error('点词弹层没打开');
  t.setAnnot(false);
  if (t.annotate(anyTerm.term, true).indexOf('class="gl"') >= 0) throw new Error('关掉注释后仍在标注');
  t.setAnnot(true);
}

/* —— 逐题点选 —— */
t.$('btn-start').onclick();
const picked = [];
const questions = t.compilePaper(paperId);
for (let i = 0; i < total; i++) {
  t.state.index = i;
  t.renderQuestion();
  const opts = t.$('opts').children;
  if (opts.length !== 3) throw new Error('第 ' + (i + 1) + ' 题选项数不是 3：' + opts.length);
  if (t.$('stem').innerHTML.indexOf('data-h="1"') >= 0) throw new Error('第 ' + (i + 1) + ' 题题干出现学院类标注');
  const want = plan.picks[i];
  picked.push(questions[i].options[want].key);
  opts[want].onclick();
}
t.state.index = total - 1;
t.renderQuestion();

if (t.$('btn-next').textContent !== t.QUIZ.ui.submit) throw new Error('最后一题没有变成「提交判定」');
if (t.$('btn-next').disabled) throw new Error('十一题答完，提交按钮却是禁用的');
if (!t.state.answers.every(a => a)) throw new Error('答案没有被记住：' + JSON.stringify(t.state.answers));
if (t.$('dots').children.filter(d => d._cls.has('done')).length !== total) throw new Error('进度点没有全部标成已答');

t.$('btn-next').onclick();

const r = t.state.result;
if (r.paperId !== paperId) throw new Error('结算用的卷号不对：' + r.paperId);
if (r.hesitate) {
  const willBtns = t.$('will-opts').children;
  if (willBtns.length !== t.QUIZ.meta.houses.length + 1) throw new Error('第三轮按钮数不对：' + willBtns.length);
  if (plan.will === 'abstain') willBtns[willBtns.length - 1].onclick();
  else if (plan.will === 'other') willBtns[t.QUIZ.meta.houses.findIndex(h => h !== r.top1)].onclick();
  else willBtns[t.QUIZ.meta.houses.indexOf(r.top1)].onclick();
} else if (plan.result === 'hesitate') {
  throw new Error('这道题本该触发第三轮，却没有触发');
}

const optical = t.state.optical;
const body = t.$('result-body').innerHTML;
if (t.$('screen-result').classList.contains('hidden')) throw new Error('结果屏没有显示');
const houseName = t.QUIZ.houses[optical.house].name;
if (body.indexOf(houseName) < 0) throw new Error('结果卡里找不到学院名');
const share = t.QUIZ.card.lines.share.replace('{house}', houseName);
if (body.indexOf(share) < 0) throw new Error('结果卡里没有转发语');
if (optical.forced === 'user' && body.indexOf(t.QUIZ.card.lines.yield_note) < 0) throw new Error('让步标注没出现');
if (optical.abstain && body.indexOf(t.QUIZ.card.lines.abstain_tease) < 0) throw new Error('弃权吐槽没出现');
const tag = t.QUIZ.card.paper_label + ' ' + t.pad2(paperId);
if (body.indexOf(tag) < 0) throw new Error('结果页没有印卷号：' + tag);

process.stdout.write(JSON.stringify({
  paperId: paperId,
  answers: picked.join(''),
  house: optical.house,
  forced: optical.forced,
  abstain: optical.abstain,
  hesitate: r.hesitate,
  id: r.id,
  card: t.textVersion(),
}));
"""


def run_verify_ui(houses_data, questions_data, papers_data, glossary_data, node_path, quiet=False):
    """交互链路冒烟：两张不同卷 × 四条作答路径，页面产出的文字卡必须逐字等于 Python 渲染。"""
    node = find_node(node_path)
    if not node:
        print("[跳过] 找不到 node，--verify 需要对拍；用 --node 指定 node 可执行文件路径。")
        return None

    meta = questions_data["meta"]
    all_ids = [p["id"] for p in papers_data["papers"]]
    ui_papers = sorted({all_ids[0], all_ids[len(all_ids) // 2]})

    def picks_for(pid, letters):
        questions = core.paper_questions(papers_data, questions_data, pid)
        return [next(i for i, o in enumerate(q["options"]) if o["key"] == ch)
                for q, ch in zip(questions, letters)]

    plans = []
    for pid in ui_papers:
        questions = core.paper_questions(papers_data, questions_data, pid)
        _, normal, hesitate, _ = core._combo_scores(questions, meta["houses"], meta, pid)
        if hesitate is None:           # 该卷任何组合都不触发第三轮，退回到用正常串测路径
            hesitate = normal
        plans.append(("卷%02d 正常判定" % pid,
                      {"paperId": pid, "picks": picks_for(pid, normal[0]), "will": None, "result": "normal"}))
        plans.append(("卷%02d 让步" % pid,
                      {"paperId": pid, "picks": picks_for(pid, hesitate[0]), "will": "other", "result": "hesitate"}))
        plans.append(("卷%02d 弃权" % pid,
                      {"paperId": pid, "picks": picks_for(pid, hesitate[0]), "will": "abstain", "result": "hesitate"}))

    page = render_html(houses_data, questions_data, papers_data, glossary_data)

    tmpdir = tempfile.mkdtemp(prefix="sorting_hat_ui_")
    page_path = os.path.join(tmpdir, "page.html")
    js_path = os.path.join(tmpdir, "driver.js")
    with io.open(page_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    with io.open(js_path, "w", encoding="utf-8") as fh:
        fh.write(UI_DRIVER_JS)

    if not quiet:
        print("[界面链路] 用 DOM 桩驱动页面脚本：%d 张卷 × 3 条作答路径" % len(ui_papers))

    failed = 0
    for name, plan in plans:
        proc = subprocess.run([node, js_path, page_path, json.dumps(plan, ensure_ascii=False)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tmpdir)
        if proc.returncode != 0:
            failed += 1
            err_lines = [ln for ln in proc.stderr.decode("utf-8", "replace").splitlines()
                         if ln.strip() and not ln.strip().startswith("at ")
                         and "Node.js v" not in ln and "CategoryInfo" not in ln
                         and "FullyQualifiedErrorId" not in ln and "所在位置" not in ln]
            print("[FAIL] %s：页面脚本抛错\n       %s" % (name, "\n       ".join(err_lines[:3])))
            continue
        got = json.loads(proc.stdout.decode("utf-8"))
        questions = core.paper_questions(papers_data, questions_data, got["paperId"])
        want_answers = "".join(questions[i]["options"][p]["key"] for i, p in enumerate(plan["picks"]))
        if got["answers"] != want_answers:
            failed += 1
            print("[FAIL] %s：点击记下的答案不对（%s != %s）" % (name, got["answers"], want_answers))
            continue

        res = core.analyze(list(got["answers"]), questions, meta, got["paperId"])
        res["house"] = got["house"]
        head = "\n".join(houses_data["card"]["focus_comment"][res["top1"]]) + "\n\n"
        if got["forced"] == "user":
            head += houses_data["card"]["lines"]["yield_tease"] + "\n\n"
        expect = head + core.render_card(res, houses_data, forced=got["forced"], abstain=got["abstain"])

        if expect != got["card"]:
            failed += 1
            print("[FAIL] %s：页面文字卡与 Python 不一致" % name)
            a, b = expect.split("\n"), got["card"].split("\n")
            for i in range(max(len(a), len(b))):
                x = a[i] if i < len(a) else "<缺行>"
                y = b[i] if i < len(b) else "<缺行>"
                if x != y:
                    print("       行 %d\n       Python: %r\n       页面  : %r" % (i + 1, x, y))
                    break
        else:
            print("[PASS] %s（卷%02d / %s / house=%s / forced=%s / abstain=%s）" %
                  (name, got["paperId"], got["answers"], got["house"], got["forced"], got["abstain"]))

    print("[汇总] 交互链路 %d/%d 条通过" % (len(plans) - failed, len(plans)))
    return EXIT_OK if failed == 0 else EXIT_VERIFY


def run_verify(houses_data, questions_data, papers_data, glossary_data, node_path, verify_papers=4,
               verify_all=False):
    node = find_node(node_path)
    if not node:
        print("[跳过] 找不到 node，--verify 需要对拍；用 --node 指定 node 可执行文件路径。")
        return None

    payload, wide, zero = build_quiz_payload(houses_data, questions_data, papers_data, glossary_data)
    all_ids = [p["id"] for p in papers_data["papers"]]
    enum_ids = all_ids if verify_all else (
        sorted({all_ids[0], all_ids[-1]} |
               {all_ids[min(int(i * len(all_ids) / float(verify_papers)), len(all_ids) - 1)]
                for i in range(verify_papers)}))
    hyp, py_cases = py_card_cases(houses_data, questions_data, papers_data, all_ids)
    ids_json = json.dumps(all_ids)

    driver = """
const mode = process.argv[2];
if (mode === 'compile') {
  const ids = %s;
  const out = {};
  ids.forEach(id => { out[String(id)] = compiledSignature(id); });
  process.stdout.write(JSON.stringify(out));
} else if (mode === 'enum') {
  const ids = %s;
  const out = {};
  ids.forEach(id => { out[String(id)] = enumSignature(id); });
  process.stdout.write(JSON.stringify(out));
} else {
  const hyp = %s;
  const out = hyp.map(h => {
    const r = analyze(h.answers, h.paperId);
    if (!r) throw new Error('对拍用例计分失败：' + h.name);
    r.house = h.house;
    return { name: h.name, forced: h.forced, abstain: h.abstain, card: renderCard(r, h) };
  });
  process.stdout.write(JSON.stringify(out));
}
""" % (ids_json, json.dumps(enum_ids), json.dumps(hyp, ensure_ascii=False))

    js = (JS_CORE
          .replace("__QUIZ_JSON__", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
          .replace("__WIDE_CHARS__", json.dumps(wide, ensure_ascii=False))
          .replace("__ZERO_WIDTH_CHARS__", json.dumps(zero, ensure_ascii=False))) + driver

    tmpdir = tempfile.mkdtemp(prefix="sorting_hat_verify_")
    js_path = os.path.join(tmpdir, "harness.js")
    with io.open(js_path, "w", encoding="utf-8") as fh:
        fh.write(js)

    def run(mode):
        proc = subprocess.run([node, js_path, mode], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, cwd=tmpdir)
        if proc.returncode != 0:
            raise RuntimeError("node 执行失败(%s)：%s" % (mode, proc.stderr.decode("utf-8", "replace")[:800]))
        return json.loads(proc.stdout.decode("utf-8"))

    print("[对拍] node = %s" % node)

    # 第 1 段：全部试卷的编译结果逐字段比对
    js_compiled = run("compile")
    bad = [pid for pid in all_ids
           if js_compiled[str(pid)] != py_compiled_signature(pid, questions_data, papers_data)]
    print("  · 编译对拍 %d 张卷：%s" % (len(all_ids), "全部一致" if not bad else "不一致 -> %s" % bad))
    compile_ok = not bad

    # 第 2 段：抽样试卷遍历全部 3^11 组合
    js_sig = run("enum")
    enum_bad = []
    for pid in enum_ids:
        js_one = js_sig[str(pid)]
        py_one = py_enum_signature(pid, questions_data, papers_data)
        if js_one != py_one:
            enum_bad.append(pid)
            print("[FAIL] 卷%02d 组合签名不一致：JS %08X/%d vs Python %08X/%d"
                  % (pid, js_one["hash"], js_one["count"], py_one["hash"], py_one["count"]))
    if not enum_bad:
        print("  · 组合对拍 卷%s：每卷 3^11 = 177147 组，签名全部一致"
              % "、".join("%02d" % p for p in enum_ids))
    enum_ok = not enum_bad

    # 第 3 段：全部试卷 × 五种结局的文字卡
    js_cards = run("cards")
    card_ok = True
    mismatch = 0
    for expected, got in zip(py_cases, js_cards):
        name, py_text = expected
        if py_text != got["card"]:
            card_ok = False
            mismatch += 1
            if mismatch <= 3:
                print("[FAIL] 文字卡不一致：%s" % name)
                p_lines, j_lines = py_text.split("\n"), got["card"].split("\n")
                for i in range(max(len(p_lines), len(j_lines))):
                    a = p_lines[i] if i < len(p_lines) else "<缺行>"
                    b = j_lines[i] if i < len(j_lines) else "<缺行>"
                    if a != b:
                        print("       行 %d\n       Python: %r\n       JS    : %r" % (i + 1, a, b))
                        break
    print("  · 文字卡对拍 全部 %d 张卷（每张 4 种结局）＋ 缺答补默认项 1 例，共 %d 张：%s"
          % (len(all_ids), len(py_cases),
             "全部逐字一致" if card_ok else "%d 处不一致" % mismatch))

    print("[汇总] 编译 %s，计分签名 %s，文字卡 %s"
          % ("一致" if compile_ok else "不一致",
             "一致" if enum_ok else "不一致",
             "一致" if card_ok else "不一致"))
    return EXIT_OK if (compile_ok and enum_ok and card_ok) else EXIT_VERIFY


# ---------------------------------------------------------------- 主流程

def main(argv=None):
    core.setup_stdout()
    parser = argparse.ArgumentParser(prog="build_quiz_html.py",
                                     description="生成分院帽交互式答题页（单文件、可离线、可分享）")
    parser.add_argument("--out", default=None, help="输出 HTML 路径（默认：当前目录 sorting-hat-quiz.html）")
    parser.add_argument("--config", default="canon", help="数据配置：canon | alt | 自定义路径")
    parser.add_argument("--houses", default=core.DEFAULT_HOUSES, help="指定 houses.json 路径")
    parser.add_argument("--questions-file", default=core.DEFAULT_QUESTIONS, help="指定题库 questions.json 路径")
    parser.add_argument("--papers-file", default=None, help="指定试卷库 papers.json 路径")
    parser.add_argument("--glossary", default=None, help="指定麻瓜词典路径（默认随 --config 自动选）")
    parser.add_argument("--verify", action="store_true", help="用 node 对拍 JS 与 Python 的编译/计分/文字卡/界面链路")
    parser.add_argument("--node", default=None, help="node 可执行文件路径（--verify 用）")
    parser.add_argument("--verify-papers", type=int, default=4,
                        help="--verify 组合枚举抽几张卷全跑 3^11（默认 4）")
    parser.add_argument("--verify-all", action="store_true", help="--verify 组合枚举把全部试卷都跑一遍")
    args = parser.parse_args(argv)

    houses, questions, papers, houses_path, glossary = core.load_configs(args)

    # 生成前先过一遍结构自检：结构坏了就不要产出页面
    blocking = core.check_pool(questions)
    paper_problems, _ = core.check_papers(papers, questions)
    gloss_problems, _ = core.check_glossary(glossary, questions, houses)
    blocking = blocking + paper_problems + gloss_problems
    if blocking:
        for item in blocking:
            core.err("[配置错误] " + item)
        return EXIT_CONFIG

    if args.verify:
        codes = [run_verify(houses, questions, papers, glossary, args.node,
                            verify_papers=args.verify_papers, verify_all=args.verify_all),
                 run_verify_ui(houses, questions, papers, glossary, args.node)]
        codes = [c for c in codes if c is not None]
        if codes and any(c != EXIT_OK for c in codes):
            return EXIT_VERIFY
        return EXIT_OK

    out_path = args.out or os.path.join(os.getcwd(), "sorting-hat-quiz.html")
    out_path = os.path.abspath(out_path)
    parent = os.path.dirname(out_path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)

    html = render_html(houses, questions, papers, glossary, args.config if args.config else houses_path)
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    print("[生成] %s" % out_path)
    print("  · 题库 %d 题 / 试卷 %d 张，每张 %d 题，配置 = %s"
          % (len(questions["questions"]), len(papers["papers"]),
             papers["meta"].get("paper_size", "?"), args.config))
    print("  · 麻瓜词典 %d 条，页面随机抽卷，卷号印在封面与卡片上"
          % len((glossary or {}).get("terms", [])))
    print("  · 单文件、无外链、无网络请求，双击即可作答")
    print("  · 校验：python scripts/build_quiz_html.py --verify --node <node 路径>")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
