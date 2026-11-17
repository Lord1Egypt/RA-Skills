# -*- coding: utf-8 -*-
"""build_quiz_html.py — UI 模式：生成单文件点选页（宣纸风，一屏一题，答完出卡）。

用法：
  python build_quiz_html.py --out linggen.html
  python build_quiz_html.py --verify     # node 对拍：JS 引擎 vs Python 引擎
"""
import json
import subprocess
import sys
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NODE = r"C:\Users\yangduo\.workbuddy\binaries\node\versions\22.22.2-3\node.exe"

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>本命灵根测试 · 测灵摊</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #efe9db;
    font-family: "Noto Serif SC", "Source Han Serif SC", "SimSun", serif;
    color: #2b2620; min-height: 100vh;
    display: flex; justify-content: center; padding: 24px 12px;
  }
  .sheet {
    width: 100%; max-width: 460px; background: #fbf7ec;
    border: 1px solid #d8c9a3; border-radius: 6px;
    padding: 28px 26px; position: relative;
  }
  .seal { position: absolute; top: 18px; right: 20px; width: 44px; height: 44px;
    border: 2px solid #a83a2e; border-radius: 4px; color: #a83a2e;
    font-size: 13px; line-height: 1.15; display: flex; align-items: center;
    justify-content: center; text-align: center; opacity: .85; padding: 3px; }
  h1 { font-size: 21px; font-weight: 600; letter-spacing: 6px; text-align: center; }
  .sub { text-align: center; font-size: 12px; color: #8a7f6a; margin-top: 6px; letter-spacing: 2px; }
  .dots { display: flex; gap: 7px; justify-content: center; margin: 22px 0 18px; }
  .dots i { width: 7px; height: 7px; border-radius: 50%; background: #ddd0b0; }
  .dots i.on { background: #a83a2e; }
  .opening { font-size: 15px; line-height: 2; white-space: pre-line; text-align: center; padding: 26px 4px; }
  .qtext { font-size: 17px; line-height: 1.7; margin: 8px 0 20px; text-align: center; }
  .opt {
    display: block; width: 100%; text-align: left; cursor: pointer;
    background: #fffdf7; border: 1px solid #d8c9a3; border-radius: 4px;
    padding: 14px 16px; margin-bottom: 12px; font-size: 14.5px; line-height: 1.65;
    font-family: inherit; color: #2b2620; transition: background .12s;
  }
  .opt:hover { background: #f4ecd8; border-color: #a83a2e; }
  .opt b { color: #a83a2e; margin-right: 8px; font-weight: 600; }
  .btn {
    display: block; margin: 26px auto 0; padding: 11px 44px; cursor: pointer;
    background: #a83a2e; color: #fbf7ec; border: none; border-radius: 4px;
    font-size: 15px; letter-spacing: 4px; font-family: inherit;
  }
  .btn:hover { background: #8f2f25; }
  .btn.ghost { background: transparent; color: #a83a2e; border: 1px solid #a83a2e; }
  .card { border-top: 2px solid #a83a2e; border-bottom: 2px solid #a83a2e; padding: 18px 2px; }
  .card .row { display: flex; font-size: 14.5px; line-height: 2.1; }
  .card .row .k { width: 76px; color: #8a7f6a; flex-shrink: 0; }
  .card .dao { cursor: pointer; border-bottom: 1px dashed #b3a582; }
  .verse { font-size: 14px; line-height: 2; padding: 16px 4px; color: #3d362c; text-align: center; }
  .post { margin-top: 18px; border: 1px dashed #c9b98e; border-radius: 4px; padding: 14px 16px; font-size: 13.5px; line-height: 2; }
  .post .t { color: #a83a2e; font-size: 12.5px; letter-spacing: 2px; margin-bottom: 2px; }
  .copy { text-align: center; margin-top: 14px; }
  .note { text-align: center; font-size: 11px; color: #a09478; margin-top: 18px; line-height: 1.8; }
  .hidden { display: none; }
  input.daoin { font-family: inherit; font-size: 14.5px; border: none; border-bottom: 1px solid #a83a2e;
    background: transparent; width: 120px; color: #2b2620; outline: none; }
</style>
</head>
<body>
<div class="sheet">
  <div class="seal">测灵<br>之印</div>
  <h1>本命灵根</h1>
  <div class="sub">测灵摊 · 今日之卷 <span id="paper-tag"></span></div>
  <div class="dots" id="dots"></div>
  <div id="stage"></div>
</div>
<script id="lg-data" type="application/json">__DATA_JSON__</script>
<script>__ENGINE_JS__</script>
<script>
(function () {
  "use strict";
  var DATA = JSON.parse(document.getElementById("lg-data").textContent);
  var E = window.LingGenEngine;
  var paperNo = __PAPER_NO__;
  var letters = [];
  var step = -1;
  var stage = document.getElementById("stage");
  var dots = document.getElementById("dots");
  var customDao = null;
  document.getElementById("paper-tag").textContent = DATA.papers.papers[paperNo - 1].paper_id;

  function cnNum(x) {
    var m = {1:"与天灵根相同",1.5:"天灵根的一点五倍",2:"天灵根的二倍",3:"天灵根的三倍",
             5:"天灵根的五倍",6:"天灵根的六倍",9:"天灵根的九倍",25:"天灵根的二十五倍",36:"天灵根的三十六倍"};
    return m[x] || ("天灵根的" + x + "倍");
  }

  function renderDots() {
    var h = "";
    for (var i = 0; i < 8; i++) h += "<i class='" + (i < letters.length || step >= 8 ? "on" : "") + "'></i>";
    dots.innerHTML = h;
  }

  function el(html) { var d = document.createElement("div"); d.innerHTML = html; return d; }

  function renderOpening() {
    renderDots();
    stage.innerHTML = "";
    var box = el("<div class='opening'>" + DATA.meta.opening + "</div>" +
      "<button class='btn' id='go'>开始测灵</button>");
    stage.appendChild(box);
    box.querySelector("#go").onclick = function () { step = 0; render(); };
  }

  function renderQuestion() {
    renderDots();
    var paper = DATA.papers.papers[paperNo - 1];
    var qid = paper.order[step];
    var q = null;
    DATA.questions.questions.forEach(function (x) { if (x.id === qid) q = x; });
    var oidOrder = paper.opt_orders[qid];
    var h = "<div class='qtext'>" + (step + 1) + " / 8　" + q.text + "</div>";
    for (var j = 0; j < oidOrder.length; j++) {
      var oid = oidOrder[j], opt = null;
      q.options.forEach(function (o) { if (o.id === oid) opt = o; });
      h += "<button class='opt' data-l='" + j + "'><b>" + "ABC"[j] + "</b>" + opt.text + "</button>";
    }
    stage.innerHTML = h;
    Array.prototype.forEach.call(stage.querySelectorAll(".opt"), function (b) {
      b.onclick = function () {
        letters[step] = "ABC"[parseInt(b.getAttribute("data-l"), 10)];
        step++;
        if (step >= 8) { step = 8; renderCard(); } else { render(); }
      };
    });
  }

  function renderCard() {
    renderDots();
    var r = E.compute(DATA, letters.join(""), paperNo, "alt");
    var dao = customDao || r.dao;
    var rows = [
      ["道号", "<span class='dao' id='dao-edit'>" + dao + "</span>"],
      ["灵根", r.display_attrs.join(" · ")],
      ["品质", r.quality_name],
      ["修炼速度", "× " + r.speed.toFixed(1)],
      ["筑基", cnNum(r.foundation)],
      ["结丹", cnNum(r.core)]
    ];
    var h = "<div class='card'>";
    rows.forEach(function (rw) { h += "<div class='row'><span class='k'>" + rw[0] + "</span><span>" + rw[1] + "</span></div>"; });
    h += "<div class='row'><span class='k'>契合宗门</span><span>" + r.sects.join(" · ") + "</span></div>";
    h += "</div><div class='verse'>" + r.verse.replace(/\n/g, "<br>") + "</div>";
    h += "<div class='post'><div class='t'>── 道友帖 ──</div>" +
         "道号：" + dao + "<br>灵根：" + r.attr_str + " · " + r.quality_name +
         "<br>契合：" + r.sects.join(" · ") + "<br>帖码：" + r.talisman + "</div>";
    h += "<div class='copy'><button class='btn ghost' id='copy'>复制转发语</button> " +
         "<button class='btn ghost' id='retry'>换张卷再测</button></div>";
    h += "<div class='note'>" + DATA.meta.disclaimer + "</div>";
    stage.innerHTML = h;
    var forward = "我的灵根是" + r.attr_str + "，" + r.quality_name + "。你的呢？（" + r.talisman + "）";
    document.getElementById("copy").onclick = function () {
      var done = function () { this.textContent = "已复制"; }.bind(this);
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(forward).then(done, function () {});
      } else {
        var t = document.createElement("textarea");
        t.value = forward; document.body.appendChild(t); t.select();
        document.execCommand("copy"); document.body.removeChild(t); done.call(document.getElementById("copy"));
      }
    };
    document.getElementById("retry").onclick = function () {
      paperNo = paperNo % DATA.papers.papers.length + 1;
      letters = []; step = -1; customDao = null;
      document.getElementById("paper-tag").textContent = DATA.papers.papers[paperNo - 1].paper_id;
      render();
    };
    document.getElementById("dao-edit").onclick = function () {
      var span = this;
      var input = document.createElement("input");
      input.className = "daoin"; input.maxLength = 6; input.value = dao;
      span.replaceWith(input); input.focus(); input.select();
      function commit() {
        customDao = input.value.trim() || r.dao;
        renderCard();
      }
      input.onblur = commit;
      input.onkeydown = function (e) { if (e.key === "Enter") input.blur(); };
    };
  }

  function render() {
    if (step === -1) renderOpening();
    else if (step < 8) renderQuestion();
  }
  render();
})();
</script>
</body>
</html>
"""


def day_paper_no():
    return date.today().timetuple().tm_yday % 20 + 1


def load_all():
    d = {}
    for name in ["questions", "papers", "meta", "attrs", "tiers"]:
        d[name] = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
    return d


def check_html_syntax(out_path):
    """生成的 HTML 里所有内联 JS 必须过 node --check，JSON 块必须可解析。

    背景：曾出现 class='t"> 这种引号笔误把 JS 字符串提前截断，
    整个 UI 脚本静默失效（页面能打开但所有按钮无反应）。此检查是硬门禁。
    """
    import re
    import tempfile
    html = Path(out_path).read_text(encoding="utf-8")
    inline = [m.group(1) for m in
              re.finditer(r"<script(?![^>]*type=)[^>]*>([\s\S]*?)</script>", html)]
    m = re.search(r'<script id="lg-data" type="application/json">([\s\S]*?)</script>', html)
    if m:
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            print(f"语法门禁 FAILED：lg-data JSON 解析失败：{e}")
            sys.exit(1)
    ok = 0
    for i, js in enumerate(inline):
        with tempfile.NamedTemporaryFile(
                "w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(js)
            tmp = f.name
        try:
            proc = subprocess.run([NODE, "--check", tmp],
                                  capture_output=True, text=True, encoding="utf-8")
        finally:
            Path(tmp).unlink(missing_ok=True)
        if proc.returncode != 0:
            print(f"语法门禁 FAILED：内联脚本 #{i} 语法错误")
            print(proc.stderr)
            sys.exit(1)
        ok += 1
    print(f"语法门禁 PASSED：{ok} 段内联 JS + JSON 可解析")


def build(out_path, paper_no=None):
    data = load_all()
    engine_js = (ROOT / "scripts" / "engine.js").read_text(encoding="utf-8")
    data_json = json.dumps(
        {k: data[k] for k in ["questions", "papers", "meta", "attrs", "tiers"]},
        ensure_ascii=False).replace("</", "<\\/")
    pn = paper_no if paper_no else day_paper_no()
    html = (HTML.replace("__DATA_JSON__", data_json)
                .replace("__ENGINE_JS__", engine_js)
                .replace("__PAPER_NO__", str(pn)))
    Path(out_path).write_text(html, encoding="utf-8")
    tag = data["papers"]["papers"][pn - 1]["paper_id"]
    print(f"已生成 {out_path}（卷 {tag}）")
    check_html_syntax(out_path)


def verify():
    sys.path.insert(0, str(ROOT / "scripts"))
    from linggen import load, evaluate, FIVE
    cfg = load()
    qmap = {q["id"]: q for q in cfg["questions"]["questions"]}
    cases = []
    expects = []
    for paper_no in [1, 7, 20]:
        paper = cfg["papers"]["papers"][paper_no - 1]
        for letters in ["AAAAAAAA", "BBBBBBBB", "CCCCCCCC", "ABABCBCA", "BCAABCCA", "CCBBAABB"]:
            answers = {}
            for i, letter in enumerate(letters):
                qid = paper["order"][i]
                answers[qid] = paper["opt_orders"][qid]["ABC".index(letter)]
            res = evaluate(answers, paper, cfg)
            cases.append({"paper": paper_no, "letters": letters})
            expects.append((res["talisman"], res["dao"]))
    cases_path = ROOT / "_verify_cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(ROOT / "scripts" / "verify_js.js"), str(DATA), str(cases_path)],
        capture_output=True, text=True, encoding="utf-8")
    cases_path.unlink()
    if proc.returncode != 0:
        print("node 执行失败：")
        print(proc.stderr)
        sys.exit(1)
    got = json.loads(proc.stdout)
    bad = 0
    for c, (t_exp, d_exp), g in zip(cases, expects, got):
        if g["talisman"] != t_exp or g["dao"] != d_exp:
            bad += 1
            print(f"  ✗ P{c['paper']:02d} {c['letters']}: 期望 {t_exp}/{d_exp}，JS 得 {g['talisman']}/{g['dao']}")
    if bad:
        print(f"VERIFY FAILED：{bad}/{len(cases)} 不一致")
        sys.exit(1)
    print(f"VERIFY PASSED：{len(cases)} 个用例，JS 与 Python 引擎完全一致")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        verify()
    else:
        out_path = "linggen-test.html"
        paper_no = None
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == "--out" and i + 1 < len(sys.argv):
                out_path = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--paper" and i + 1 < len(sys.argv):
                paper_no = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        build(out_path, paper_no)
