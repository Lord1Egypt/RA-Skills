#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原文理解测验页生成器
生成阅读理解页：贴近原文的单选题和判断题。
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import wrap_html, esc_html


def generate_reading_quiz_html(questions):
    """生成原文理解测验的 body + JS"""
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
    .q-card {
      background: #fff;
      border-radius: 14px;
      padding: 24px;
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
    .q-type.choice { background: #e8f4fd; color: #1a73e8; }
    .q-type.judge { background: #e8f9ee; color: #1a7f37; }
    .q-card .q-text {
      font-size: 1.1em;
      margin-bottom: 16px;
      line-height: 1.7;
    }
    .q-options {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .q-option {
      padding: 14px 18px;
      border: 2px solid #e9ecef;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 1em;
      line-height: 1.5;
    }
    .q-option:hover { border-color: #667eea; background: #f8f6ff; }
    .q-option.correct {
      border-color: #34c759; background: #e8f9ee; color: #1a7f37;
      animation: pulse 0.3s ease;
    }
    .q-option.wrong {
      border-color: #ff3b30; background: #fff0f0; color: #c41e3a;
      animation: shake 0.4s ease;
    }
    .q-option.disabled { pointer-events: none; opacity: 0.5; }
    .q-option.show-correct {
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
    .retry-btn:hover { transform: scale(1.05); }'''

    js = f'''
    const QUESTIONS = {questions_json};
    let curIdx = 0;
    let score = 0;

    function renderAll() {{
      const container = document.querySelector('.main-content');
      container.innerHTML = `
        <div class="quiz-header">
          <h1>📚 原文理解测验</h1>
          <div class="score-badge">得分：<span id="scoreNum">0</span> / <span id="totalQ">0</span></div>
        </div>
        <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
        <div id="quizBody"></div>
      `;
      renderQuestions();
    }}

    function renderQuestions() {{
      const body = document.getElementById('quizBody');
      let html = '';
      QUESTIONS.forEach((q, i) => {{
        const typeLabel = q.type === 'choice' ? '单选题' : '判断题';
        const typeClass = q.type;
        html += `<div class="q-card" id="q${{i}}" style="display:none">
          <span class="q-type ${{typeClass}}">${{typeLabel}}</span>
          <div class="q-text">${{q.question}}</div>
          <div class="q-options" id="opts${{i}}"></div>
          <div class="q-explanation" id="exp${{i}}"></div>
        </div>`;
      }});
      html += `<div id="resultArea"></div>`;
      body.innerHTML = html;

      // 显示第一题
      showQuestion(0);
      document.getElementById('totalQ').textContent = QUESTIONS.length;
    }}

    function showQuestion(idx) {{
      if (idx >= QUESTIONS.length) {{
        showResult();
        return;
      }}
      curIdx = idx;
      // 隐藏所有
      QUESTIONS.forEach((_, i) => {{
        const el = document.getElementById('q' + i);
        if (el) el.style.display = 'none';
      }});
      const card = document.getElementById('q' + idx);
      card.style.display = 'block';
      const q = QUESTIONS[idx];
      const optsEl = document.getElementById('opts' + idx);

      let optsHtml = '';
      q.options.forEach((opt, oi) => {{
        optsHtml += `<div class="q-option" onclick="selectAnswer(${{idx}}, ${{oi}})">${{opt}}</div>`;
      }});
      optsEl.innerHTML = optsHtml;
      updateProgress();
    }}

    function selectAnswer(qIdx, optIdx) {{
      const q = QUESTIONS[qIdx];
      const optsEl = document.getElementById('opts' + qIdx);
      const opts = optsEl.querySelectorAll('.q-option');
      const expEl = document.getElementById('exp' + qIdx);

      opts.forEach(o => o.classList.add('disabled'));

      if (optIdx === q.answer) {{
        opts[optIdx].classList.add('correct');
        score++;
      }} else {{
        opts[optIdx].classList.add('wrong');
        opts[q.answer].classList.add('show-correct');
      }}

      if (q.explanation) {{
        expEl.textContent = q.explanation;
        expEl.classList.add('show');
      }}
      updateProgress();

      setTimeout(() => showQuestion(qIdx + 1), 1500);
    }}

    function updateProgress() {{
      document.getElementById('scoreNum').textContent = score;
      const pct = QUESTIONS.length > 0 ? ((curIdx + 1) / QUESTIONS.length * 100) : 0;
      document.getElementById('progressFill').style.width = pct + '%';
    }}

    function showResult() {{
      const area = document.getElementById('resultArea');
      const pct = Math.round(score / QUESTIONS.length * 100);
      let emoji = pct >= 90 ? '🎉' : pct >= 70 ? '👍' : pct >= 50 ? '💪' : '📚';
      area.innerHTML = `
        <div class="result-card">
          <div class="big-score">${{pct}}%</div>
          <p>${{emoji}} 答对 ${{score}} / ${{QUESTIONS.length}} 题</p>
          <p>${{pct >= 90 ? '理解得很透彻！' : pct >= 70 ? '不错哦！' : pct >= 50 ? '再读一遍课文吧！' : '需要再仔细读读原文哦！'}}</p>
          <button class="retry-btn" onclick="startOver()">再来一次</button>
        </div>`;
      document.getElementById('progressFill').style.width = '100%';
    }}

    function startOver() {{
      score = 0;
      curIdx = 0;
      renderAll();
    }}

    renderAll();'''

    body = '<div id="app"></div>'
    return body, css, js


def main():
    parser = argparse.ArgumentParser(
        description="原文理解测验页生成器：生成贴近原文的单选题和判断题"
    )
    parser.add_argument("-q", "--questions", required=True,
                        help="题目 JSON 文件路径")
    parser.add_argument("-o", "--output", default="reading_quiz.html",
                        help="输出 HTML 文件路径 (默认: reading_quiz.html)")
    args = parser.parse_args()

    qpath = Path(args.questions)
    if not qpath.exists():
        print(f"错误：题目文件不存在：{args.questions}", file=sys.stderr)
        sys.exit(1)

    questions = json.loads(qpath.read_text(encoding="utf-8"))
    if not questions:
        print("错误：题目列表为空", file=sys.stderr)
        sys.exit(1)

    print(f"题目数量: {len(questions)}")

    body, css, js = generate_reading_quiz_html(questions)
    html = wrap_html("原文理解测验", "reading_quiz.html", body, css, js)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"[OK] 原文理解测验页已保存：{output_path}（{output_path.stat().st_size / 1024:.1f} KB）")


if __name__ == "__main__":
    main()
