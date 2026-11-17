#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
句子测验页生成器
生成搭配填空和句型替换练习页面。
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import wrap_html, esc_html


def generate_sentence_quiz_html(questions):
    """生成句子测验的 body + CSS + JS"""
    questions_json = json.dumps(questions, ensure_ascii=False)

    css = '''
    .quiz-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    .quiz-header h1 { font-size: 1.5em; color: #1a73e8; border: none; margin: 0; padding: 0; }
    .score-badge {
      padding: 8px 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 20px;
      font-weight: 700;
      font-size: 1.1em;
    }
    .progress-track {
      width: 100%;
      height: 8px;
      background: #e9ecef;
      border-radius: 4px;
      margin-bottom: 24px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      border-radius: 4px;
      transition: width 0.4s ease;
    }
    .mode-tabs {
      display: flex;
      background: #fff;
      border-radius: 12px;
      padding: 4px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .mode-tab {
      flex: 1;
      padding: 12px 8px;
      text-align: center;
      cursor: pointer;
      border-radius: 8px;
      font-size: 0.95em;
      transition: all 0.2s;
      font-weight: 500;
    }
    .mode-tab:hover { background: #f8f9fa; }
    .mode-tab.active {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .q-card {
      background: #fff;
      border-radius: 14px;
      padding: 28px 24px;
      margin-bottom: 20px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .q-card .q-type {
      display: inline-block;
      padding: 3px 10px;
      border-radius: 10px;
      font-size: 0.8em;
      font-weight: 600;
      margin-bottom: 10px;
    }
    .q-type.fill { background: #fff3e0; color: #e65100; }
    .q-type.transform { background: #e8eaf6; color: #283593; }
    .q-card .q-text {
      font-size: 1.15em;
      margin-bottom: 18px;
      line-height: 1.8;
    }
    /* ── 填空模式 ── */
    .blank-sentence {
      font-size: 1.2em;
      line-height: 2;
      margin-bottom: 16px;
    }
    .blank-slot {
      display: inline-block;
      min-width: 80px;
      padding: 2px 12px;
      border-bottom: 2px dashed #667eea;
      margin: 0 4px;
      text-align: center;
      font-weight: 600;
      color: #667eea;
    }
    .blank-slot.correct { border-bottom-color: #34c759; color: #34c759; }
    .blank-slot.wrong { border-bottom-color: #ff3b30; color: #ff3b30; }
    .word-bank {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 12px;
    }
    .word-chip {
      padding: 10px 18px;
      border: 2px solid #e9ecef;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 1em;
      background: #fff;
    }
    .word-chip:hover { border-color: #667eea; background: #f8f6ff; }
    .word-chip.used { opacity: 0.3; pointer-events: none; }
    .word-chip.selected {
      border-color: #667eea;
      background: #667eea;
      color: white;
    }
    /* ── 句型替换模式 ── */
    .transform-original {
      padding: 16px;
      background: #f8f9fa;
      border-radius: 8px;
      font-size: 1.05em;
      margin-bottom: 12px;
      border-left: 4px solid #667eea;
    }
    .transform-hint {
      font-size: 0.95em;
      color: #666;
      margin-bottom: 16px;
    }
    .transform-options {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .transform-option {
      padding: 14px 18px;
      border: 2px solid #e9ecef;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 1em;
      line-height: 1.5;
    }
    .transform-option:hover { border-color: #667eea; background: #f8f6ff; }
    .transform-option.correct {
      border-color: #34c759; background: #e8f9ee; color: #1a7f37;
      animation: pulse 0.3s ease;
    }
    .transform-option.wrong {
      border-color: #ff3b30; background: #fff0f0; color: #c41e3a;
      animation: shake 0.4s ease;
    }
    .transform-option.disabled { pointer-events: none; opacity: 0.5; }
    .transform-option.show-correct {
      border-color: #34c759; background: #e8f9ee; color: #1a7f37;
    }
    @keyframes pulse {
      0%,100% { transform: scale(1); }
      50% { transform: scale(1.02); }
    }
    @keyframes shake {
      0%,100% { transform: translateX(0); }
      25% { transform: translateX(-5px); }
      75% { transform: translateX(5px); }
    }
    .q-explanation {
      margin-top: 14px;
      padding: 12px 16px;
      background: #f8f9fa;
      border-radius: 8px;
      font-size: 0.95em;
      color: #555;
      display: none;
    }
    .q-explanation.show { display: block; }
    .result-card {
      text-align: center;
      padding: 40px 20px;
      background: #fff;
      border-radius: 14px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .big-score {
      font-size: 3.5em;
      font-weight: 800;
      background: linear-gradient(135deg, #667eea, #764ba2);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .result-card p { margin: 12px 0; color: #666; font-size: 1.1em; }
    .retry-btn {
      margin-top: 20px;
      padding: 14px 40px;
      border: none;
      border-radius: 30px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      font-size: 1.1em;
      cursor: pointer;
    }
    .next-btn {
      margin-top: 16px;
      padding: 10px 30px;
      border: none;
      border-radius: 20px;
      background: #667eea;
      color: white;
      font-size: 0.95em;
      cursor: pointer;
      display: none;
    }
    .next-btn.show { display: inline-block; }'''

    js = f'''
    const ALL_QUESTIONS = {questions_json};
    let mode = 'fill';
    let questions = [];
    let curIdx = 0;
    let score = 0;

    function filterQuestions() {{
      questions = ALL_QUESTIONS.filter(q => q.type === mode);
      curIdx = 0;
      score = 0;
    }}

    function renderAll() {{
      filterQuestions();
      const container = document.querySelector('.main-content');
      container.innerHTML = `
        <div class="quiz-header">
          <h1>✏️ 句子测验</h1>
          <div class="score-badge">得分：<span id="scoreNum">0</span> / <span id="totalQ">0</span></div>
        </div>
        <div class="mode-tabs">
          <div class="mode-tab ${{mode==='fill'?'active':''}}" onclick="switchMode('fill')">🧩 搭配填空</div>
          <div class="mode-tab ${{mode==='transform'?'active':''}}" onclick="switchMode('transform')">🔄 句型替换</div>
        </div>
        <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
        <div id="quizBody"></div>
      `;
      renderQuestion();
    }}

    function switchMode(m) {{
      mode = m;
      renderAll();
    }}

    function renderQuestion() {{
      const body = document.getElementById('quizBody');
      if (curIdx >= questions.length) {{
        showResult();
        return;
      }}
      document.getElementById('totalQ').textContent = questions.length;
      document.getElementById('scoreNum').textContent = score;
      const pct = questions.length > 0 ? ((curIdx + 1) / questions.length * 100) : 0;
      document.getElementById('progressFill').style.width = pct + '%';

      const q = questions[curIdx];
      if (q.type === 'fill') renderFill(q, body);
      else renderTransform(q, body);
    }}

    // ── 搭配填空 ──
    function renderFill(q, body) {{
      let sentenceHtml = q.sentence;
      // 替换 ___ 为填空位
      let blankIdx = 0;
      sentenceHtml = sentenceHtml.replace(/___/g, () => {{
        const slot = `<span class="blank-slot" id="slot${{blankIdx}}" data-idx="${{blankIdx}}"></span>`;
        blankIdx++;
        return slot;
      }});

      const shuffledWords = shuffle([...q.word_bank]);
      let bankHtml = shuffledWords.map((w, i) =>
        `<div class="word-chip" onclick="pickWord(this, '${{w}}')" id="chip${{i}}">${{w}}</div>`
      ).join('');

      body.innerHTML = `
        <div class="q-card">
          <span class="q-type fill">搭配填空</span>
          <div class="blank-sentence">${{sentenceHtml}}</div>
          <div class="word-bank">${{bankHtml}}</div>
          <div class="q-explanation" id="expArea"></div>
          <button class="next-btn" id="nextBtn" onclick="nextQuestion()">下一题 →</button>
        </div>`;

      window._fillAnswer = [...q.answer];
      window._fillCurrent = 0;
    }}

    function pickWord(chipEl, word) {{
      const slot = document.getElementById('slot' + window._fillCurrent);
      if (!slot) return;

      slot.textContent = word;
      chipEl.classList.add('used');

      const correct = window._fillAnswer[window._fillCurrent];
      if (word === correct) {{
        slot.classList.add('correct');
      }} else {{
        slot.classList.add('wrong');
        slot.textContent = word + ' → ' + correct;
      }}

      window._fillCurrent++;

      // 所有填空完成
      if (window._fillCurrent >= window._fillAnswer.length) {{
        let allCorrect = true;
        document.querySelectorAll('.blank-slot').forEach(s => {{
          if (s.classList.contains('wrong')) allCorrect = false;
        }});
        if (allCorrect) score++;
        document.querySelectorAll('.word-chip').forEach(c => c.classList.add('used'));

        const q = questions[curIdx];
        if (q.explanation) {{
          const exp = document.getElementById('expArea');
          exp.textContent = q.explanation;
          exp.classList.add('show');
        }}
        updateProgress();
        document.getElementById('nextBtn').classList.add('show');
      }}
    }}

    // ── 句型替换 ──
    function renderTransform(q, body) {{
      let optsHtml = '';
      const shuffled = shuffle(q.options.map((o, i) => ({{text: o, idx: i}})));
      shuffled.forEach(o => {{
        optsHtml += `<div class="transform-option" onclick="selectTransform(this, ${{o.idx}})">${{o.text}}</div>`;
      }});

      body.innerHTML = `
        <div class="q-card">
          <span class="q-type transform">句型替换</span>
          <div class="transform-original">${{q.original}}</div>
          <div class="transform-hint">${{q.hint || '请选择正确的改写句子：'}}</div>
          <div class="transform-options">${{optsHtml}}</div>
          <div class="q-explanation" id="expArea"></div>
        </div>`;
    }}

    function selectTransform(optEl, idx) {{
      const q = questions[curIdx];
      const allOpts = document.querySelectorAll('.transform-option');
      allOpts.forEach(o => o.classList.add('disabled'));

      if (idx === q.answer) {{
        optEl.classList.add('correct');
        score++;
      }} else {{
        optEl.classList.add('wrong');
        allOpts.forEach(o => {{
          // find the correct one
          const text = o.textContent;
          if (text === q.options[q.answer]) o.classList.add('show-correct');
        }});
      }}

      if (q.explanation) {{
        const exp = document.getElementById('expArea');
        exp.textContent = q.explanation;
        exp.classList.add('show');
      }}
      updateProgress();
      setTimeout(() => nextQuestion(), 1800);
    }}

    function nextQuestion() {{
      curIdx++;
      renderQuestion();
    }}

    function updateProgress() {{
      document.getElementById('scoreNum').textContent = score;
      document.getElementById('totalQ').textContent = questions.length;
      const pct = questions.length > 0 ? ((curIdx + 1) / questions.length * 100) : 0;
      document.getElementById('progressFill').style.width = pct + '%';
    }}

    function showResult() {{
      const body = document.getElementById('quizBody');
      const pct = questions.length > 0 ? Math.round(score / questions.length * 100) : 0;
      let emoji = pct >= 90 ? '🎉' : pct >= 70 ? '👍' : pct >= 50 ? '💪' : '📚';
      body.innerHTML = `
        <div class="result-card">
          <div class="big-score">${{pct}}%</div>
          <p>${{emoji}} 答对 ${{score}} / ${{questions.length}} 题</p>
          <p>${{pct >= 90 ? '太棒了！' : pct >= 70 ? '不错哦！' : pct >= 50 ? '继续加油！' : '多练习几遍吧！'}}</p>
          <button class="retry-btn" onclick="renderAll()">再来一次</button>
        </div>`;
      document.getElementById('progressFill').style.width = '100%';
    }}

    function shuffle(arr) {{
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }}
      return a;
    }}

    renderAll();'''

    body = '<div id="app"></div>'
    return body, css, js


def main():
    parser = argparse.ArgumentParser(
        description="句子测验页生成器：搭配填空和句型替换练习"
    )
    parser.add_argument("-q", "--questions", required=True,
                        help="题目 JSON 文件路径")
    parser.add_argument("-o", "--output", default="sentence_quiz.html",
                        help="输出 HTML 文件路径 (默认: sentence_quiz.html)")
    args = parser.parse_args()

    qpath = Path(args.questions)
    if not qpath.exists():
        print(f"错误：题目文件不存在：{args.questions}", file=sys.stderr)
        sys.exit(1)

    questions = json.loads(qpath.read_text(encoding="utf-8"))
    if not questions:
        print("错误：题目列表为空", file=sys.stderr)
        sys.exit(1)

    fill_count = sum(1 for q in questions if q["type"] == "fill")
    transform_count = sum(1 for q in questions if q["type"] == "transform")
    print(f"搭配填空: {fill_count} 题，句型替换: {transform_count} 题")

    body, css, js = generate_sentence_quiz_html(questions)
    html = wrap_html("句子测验", "sentence_quiz.html", body, css, js)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"[OK] 句子测验页已保存：{output_path}（{output_path.stat().st_size / 1024:.1f} KB）")


if __name__ == "__main__":
    main()
