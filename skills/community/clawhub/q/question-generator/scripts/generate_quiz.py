#!/usr/bin/env python3
"""
Question Generator - HTML Quiz Renderer
Renders quiz JSON data into an interactive HTML quiz page.

Usage:
  python generate_quiz.py --data '{"title":"...", "questions":[...]}' --output quiz.html
  cat quiz.json | python generate_quiz.py --output quiz.html
"""

import argparse
import json
import sys
import os
from datetime import datetime
from html import escape


def load_data(args):
    """Load quiz data from --data argument or stdin."""
    if args.data:
        return json.loads(args.data)
    if args.stdin:
        return json.load(sys.stdin)
    # Try reading from stdin if available
    if not sys.stdin.isatty():
        return json.load(sys.stdin)
    print("Error: No data provided. Use --data or pipe JSON via stdin.", file=sys.stderr)
    sys.exit(1)


def render_options(question):
    """Render options for choice questions."""
    qid = question["id"]
    qtype = question.get("type", "")
    options = question.get("options", [])

    if not options:
        return ""

    is_multiple = "多选" in qtype
    input_type = "checkbox" if is_multiple else "radio"

    html_parts = ['<div class="options">']
    for i, opt in enumerate(options):
        # Extract letter (A, B, C, D...) from option text
        letter = chr(65 + i)
        opt_text = opt
        if len(opt) > 2 and opt[1] in ".．、":
            opt_text = opt[2:].strip()
        elif len(opt) > 2 and opt[0].isalpha() and opt[1] in ".．、 ":
            opt_text = opt[2:].strip()

        html_parts.append(f"""
        <label class="option" data-qid="{qid}" data-letter="{letter}">
            <input type="{input_type}" name="q{qid}" value="{letter}" onchange="checkAnswer('{qid}')">
            <span class="option-letter">{letter}</span>
            <span class="option-text">{escape(opt_text)}</span>
        </label>""")
    html_parts.append("</div>")
    return "\n".join(html_parts)


def render_blanks(question):
    """Render fill-in-the-blank input fields."""
    qid = question["id"]
    stem = question.get("stem", "")
    # Count blanks (____)
    blank_count = stem.count("____")
    if blank_count == 0:
        return ""

    parts = []
    parts.append('<div class="blanks">')
    for i in range(blank_count):
        parts.append(f"""
        <div class="blank-input">
            <span>空{i+1}：</span>
            <input type="text" class="fill-blank" data-qid="{qid}" data-blank="{i+1}" placeholder="填写答案">
        </div>""")
    parts.append("</div>")
    return "\n".join(parts)


def render_judgment(question):
    """Render true/false buttons."""
    qid = question["id"]
    return f"""
    <div class="judgment">
        <label class="option" data-qid="{qid}" data-letter="对">
            <input type="radio" name="q{qid}" value="对" onchange="checkAnswer('{qid}')">
            <span class="option-letter">✓</span>
            <span class="option-text">正确</span>
        </label>
        <label class="option" data-qid="{qid}" data-letter="错">
            <input type="radio" name="q{qid}" value="错" onchange="checkAnswer('{qid}')">
            <span class="option-letter">✗</span>
            <span class="option-text">错误</span>
        </label>
    </div>"""


def render_matching(question):
    """Render matching question."""
    qid = question["id"]
    left = question.get("match_left", [])
    right = question.get("match_right", [])
    if not left or not right:
        return ""

    html_parts = ['<div class="matching">']
    html_parts.append('<table class="match-table"><thead><tr><th>左列</th><th>→</th><th>右列</th></tr></thead><tbody>')
    for i, l_item in enumerate(left):
        right_options = "".join(
            f'<option value="{j}">{escape(r)}</option>' for j, r in enumerate(right)
        )
        html_parts.append(f"""
        <tr>
            <td class="match-left">{i+1}. {escape(l_item)}</td>
            <td>→</td>
            <td><select class="match-select" data-qid="{qid}" data-left="{i}" onchange="checkAnswer('{qid}')">
                <option value="-1">选择匹配项</option>
                {right_options}
            </select></td>
        </tr>""")
    html_parts.append("</tbody></table></div>")
    return "\n".join(html_parts)


def render_answer_area(question):
    """Render the appropriate answer area based on question type."""
    qtype = question.get("type", "")

    if "单选" in qtype or "多选" in qtype:
        return render_options(question)
    elif "判断" in qtype:
        return render_judgment(question)
    elif "填空" in qtype:
        return render_blanks(question)
    elif "匹配" in qtype or "连线" in qtype:
        return render_matching(question)
    else:
        # Short answer, essay, calculation, application, case analysis
        qid = question["id"]
        return f'<textarea class="text-answer" data-qid="{qid}" placeholder="请在此作答..." rows="5"></textarea>'


def render_answer_block(question):
    """Render the answer and explanation block (collapsible)."""
    answer = question.get("answer", "")
    explanation = question.get("explanation", "")
    common_mistake = question.get("common_mistake", "")

    html = '<div class="answer-block">'
    html += f'<div class="answer-header" onclick="toggleAnswer(this)">'
    html += '<span class="toggle-icon">▶</span> 查看答案与解析</div>'
    html += '<div class="answer-content" style="display:none;">'
    html += f'<div class="answer-row"><span class="label">答案</span><span class="answer-value">{escape(str(answer))}</span></div>'
    if explanation:
        html += f'<div class="answer-row"><span class="label">解析</span><span class="explanation-value">{escape(explanation)}</span></div>'
    if common_mistake:
        html += f'<div class="answer-row"><span class="label">易错点</span><span class="mistake-value">{escape(common_mistake)}</span></div>'
    html += "</div></div>"
    return html


def get_difficulty_class(difficulty):
    """Map difficulty to CSS class."""
    d = (difficulty or "").lower()
    if "基础" in d or "basic" in d:
        return "diff-easy"
    elif "挑战" in d or "challenge" in d:
        return "diff-hard"
    else:
        return "diff-medium"


def render_question(question, index):
    """Render a single question."""
    qid = question.get("id", f"Q{index+1:02d}")
    qtype = question.get("type", "单选题")
    bloom = question.get("bloom_level", "")
    difficulty = question.get("difficulty", "进阶")
    kp = question.get("knowledge_point", "")
    score = question.get("score", 0)
    stem = question.get("stem", "")
    diff_class = get_difficulty_class(difficulty)

    answer_area = render_answer_area(question)
    answer_block = render_answer_block(question)

    return f"""
    <div class="question" id="q{qid}" data-type="{qtype}" data-difficulty="{difficulty}">
        <div class="q-header">
            <span class="q-number">{index+1}</span>
            <span class="q-type-badge">{qtype}</span>
            <span class="bloom-badge">{escape(bloom)}</span>
            <span class="diff-badge {diff_class}">{difficulty}</span>
            <span class="q-score">{score}分</span>
        </div>
        <div class="q-stem">{escape(stem)}</div>
        {answer_area}
        {answer_block}
    </div>"""


def render_answer_card(questions):
    """Render the answer card sidebar."""
    html_parts = ['<div class="answer-card">', '<h3>答题卡</h3>', '<div class="card-grid">']
    for i, q in enumerate(questions):
        qid = q.get("id", f"Q{i+1:02d}")
        html_parts.append(f'<a href="#q{qid}" class="card-item" data-qid="{qid}">{i+1}</a>')
    html_parts.append("</div>")
    html_parts.append('<div class="card-stats" id="cardStats">未作答: 0</div>')

    # Score summary
    total = sum(q.get("score", 0) for q in questions)
    html_parts.append(f'<div class="total-score">总分: {total}分</div>')
    html_parts.append("</div>")
    return "\n".join(html_parts)


def render_statistics(questions):
    """Render knowledge point and difficulty statistics."""
    # Difficulty distribution
    diff_counts = {}
    for q in questions:
        d = q.get("difficulty", "进阶")
        diff_counts[d] = diff_counts.get(d, 0) + 1

    # Bloom distribution
    bloom_counts = {}
    for q in questions:
        b = q.get("bloom_level", "未知")
        bloom_counts[b] = bloom_counts.get(b, 0) + 1

    # Knowledge points
    kp_counts = {}
    for q in questions:
        kp = q.get("knowledge_point", "未分类")
        kp_counts[kp] = kp_counts.get(kp, 0) + 1

    # Type distribution
    type_counts = {}
    for q in questions:
        t = q.get("type", "未知")
        type_counts[t] = type_counts.get(t, 0) + 1

    html = '<div class="statistics-section">'
    html += '<h2>试卷统计</h2>'

    # Difficulty chart
    html += '<div class="stat-block"><h3>难度分布</h3><div class="bar-chart">'
    for d, count in sorted(diff_counts.items()):
        pct = count / len(questions) * 100
        diff_cls = get_difficulty_class(d)
        html += f'<div class="bar-row"><span class="bar-label">{d}</span><div class="bar-track"><div class="bar-fill {diff_cls}" style="width:{pct}%"></div></div><span class="bar-value">{count}题 ({pct:.0f}%)</span></div>'
    html += '</div></div>'

    # Type distribution
    html += '<div class="stat-block"><h3>题型分布</h3><div class="type-list">'
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        html += f'<span class="type-tag">{t} ×{count}</span>'
    html += '</div></div>'

    # Bloom distribution
    html += '<div class="stat-block"><h3>认知层次分布</h3><div class="bloom-list">'
    for b, count in sorted(bloom_counts.items()):
        html += f'<span class="bloom-tag">{b} ×{count}</span>'
    html += '</div></div>'

    # Knowledge point coverage
    html += '<div class="stat-block"><h3>知识点覆盖</h3><div class="kp-list">'
    for kp, count in sorted(kp_counts.items(), key=lambda x: -x[1]):
        html += f'<span class="kp-tag">{kp} ×{count}</span>'
    html += '</div></div>'

    html += '</div>'
    return html


def group_questions(questions):
    """Group questions by type, preserving original order within groups."""
    groups = {}
    order = []
    for q in questions:
        t = q.get("type", "其他")
        if t not in groups:
            groups[t] = []
            order.append(t)
        groups[t].append(q)
    return order, groups


def generate_html(data):
    """Generate the complete HTML quiz page."""
    title = data.get("title", "智能试卷")
    subject = data.get("subject", "")
    grade = data.get("grade", "")
    total_time = data.get("duration", "90分钟")
    questions = data.get("questions", [])
    meta_info = data.get("meta", {})

    now = datetime.now().strftime("%Y年%m月%d日")

    # Group questions by type
    type_order, grouped = group_questions(questions)

    # Render question sections
    sections_html = ""
    global_index = 0
    for qtype in type_order:
        group = grouped[qtype]
        group_score = sum(q.get("score", 0) for q in group)
        sections_html += f'<div class="section"><div class="section-header"><h2>{qtype}</h2><span class="section-info">共{len(group)}题，{group_score}分</span></div>'
        for q in group:
            sections_html += render_question(q, global_index)
            global_index += 1
        sections_html += '</div>'

    answer_card = render_answer_card(questions)
    statistics = render_statistics(questions)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, "Microsoft YaHei", "Segoe UI", sans-serif; background: #f0f2f5; color: #333; line-height: 1.8; }}

/* Header */
.quiz-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 40px; text-align: center; }}
.quiz-header h1 {{ font-size: 28px; margin-bottom: 10px; }}
.quiz-meta {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; font-size: 14px; opacity: 0.9; }}
.quiz-meta span {{ background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; }}

/* Layout */
.main-container {{ display: flex; max-width: 1200px; margin: 0 auto; gap: 20px; padding: 20px; }}
.content-area {{ flex: 1; min-width: 0; }}

/* Answer Card */
.answer-card {{ width: 220px; position: sticky; top: 20px; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); height: fit-content; }}
.answer-card h3 {{ font-size: 16px; margin-bottom: 12px; color: #667eea; }}
.card-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-bottom: 12px; }}
.card-item {{ display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: #f0f2f5; color: #666; text-decoration: none; font-size: 13px; font-weight: 600; transition: all 0.2s; }}
.card-item:hover {{ background: #667eea; color: white; }}
.card-item.answered {{ background: #52c41a; color: white; }}
.card-stats {{ font-size: 12px; color: #999; text-align: center; margin-top: 8px; }}
.total-score {{ text-align: center; font-size: 14px; font-weight: 600; color: #667eea; margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; }}

/* Section */
.section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.section-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #667eea; }}
.section-header h2 {{ font-size: 18px; color: #333; }}
.section-info {{ font-size: 13px; color: #999; }}

/* Question */
.question {{ padding: 20px 0; border-bottom: 1px solid #f0f0f0; }}
.question:last-child {{ border-bottom: none; }}
.q-header {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }}
.q-number {{ display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: #667eea; color: white; border-radius: 50%; font-size: 14px; font-weight: 700; }}
.q-type-badge {{ background: #e6e9ff; color: #667eea; font-size: 12px; padding: 2px 8px; border-radius: 4px; }}
.bloom-badge {{ background: #fff7e6; color: #fa8c16; font-size: 12px; padding: 2px 8px; border-radius: 4px; }}
.diff-badge {{ font-size: 12px; padding: 2px 8px; border-radius: 4px; }}
.diff-easy {{ background: #f6ffed; color: #52c41a; border: 1px solid #b7eb8f; }}
.diff-medium {{ background: #fff7e6; color: #fa8c16; border: 1px solid #ffd591; }}
.diff-hard {{ background: #fff2f0; color: #ff4d4f; border: 1px solid #ffccc7; }}
.q-score {{ margin-left: auto; font-size: 13px; color: #999; }}
.q-stem {{ font-size: 15px; margin-bottom: 12px; white-space: pre-wrap; }}

/* Options */
.options {{ margin-left: 20px; }}
.option {{ display: flex; align-items: flex-start; gap: 8px; padding: 8px 12px; margin-bottom: 6px; border-radius: 8px; cursor: pointer; transition: background 0.2s; }}
.option:hover {{ background: #f5f7ff; }}
.option.correct {{ background: #f6ffed; border: 1px solid #b7eb8f; }}
.option.wrong {{ background: #fff2f0; border: 1px solid #ffccc7; }}
.option input {{ margin-top: 5px; }}
.option-letter {{ font-weight: 700; color: #667eea; min-width: 20px; }}
.option-text {{ flex: 1; font-size: 14px; }}

/* Judgment */
.judgment {{ margin-left: 20px; display: flex; gap: 20px; }}
.judgment .option {{ flex: 0 0 auto; }}

/* Blanks */
.blanks {{ margin-left: 20px; }}
.blank-input {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
.blank-input span {{ font-size: 14px; color: #666; }}
.fill-blank {{ border: 1px solid #d9d9d9; border-radius: 6px; padding: 6px 12px; font-size: 14px; width: 200px; }}
.fill-blank:focus {{ border-color: #667eea; outline: none; box-shadow: 0 0 0 2px rgba(102,126,234,0.2); }}

/* Matching */
.matching {{ margin-left: 20px; }}
.match-table {{ width: 100%; max-width: 500px; border-collapse: collapse; }}
.match-table th {{ text-align: left; padding: 8px; font-size: 13px; color: #999; border-bottom: 1px solid #eee; }}
.match-table td {{ padding: 8px; font-size: 14px; }}
.match-left {{ font-weight: 500; }}
.match-select {{ padding: 4px 8px; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 13px; }}

/* Text answer */
.text-answer {{ width: 100%; max-width: 600px; border: 1px solid #d9d9d9; border-radius: 8px; padding: 12px; font-size: 14px; font-family: inherit; resize: vertical; line-height: 1.8; }}
.text-answer:focus {{ border-color: #667eea; outline: none; box-shadow: 0 0 0 2px rgba(102,126,234,0.2); }}

/* Answer Block */
.answer-block {{ margin-top: 12px; margin-left: 20px; border: 1px solid #e8e8e8; border-radius: 8px; overflow: hidden; }}
.answer-header {{ background: #fafafa; padding: 8px 12px; cursor: pointer; font-size: 13px; color: #667eea; font-weight: 500; user-select: none; }}
.answer-header:hover {{ background: #f0f2ff; }}
.toggle-icon {{ display: inline-block; transition: transform 0.2s; }}
.answer-block.open .toggle-icon {{ transform: rotate(90deg); }}
.answer-content {{ padding: 12px 16px; }}
.answer-row {{ margin-bottom: 8px; font-size: 14px; }}
.answer-row:last-child {{ margin-bottom: 0; }}
.label {{ display: inline-block; background: #667eea; color: white; font-size: 12px; padding: 1px 6px; border-radius: 4px; margin-right: 8px; }}
.answer-value {{ font-weight: 700; color: #52c41a; }}
.explanation-value {{ color: #555; white-space: pre-wrap; }}
.mistake-value {{ color: #ff4d4f; }}

/* Statistics */
.statistics-section {{ max-width: 1200px; margin: 0 auto 20px; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.statistics-section h2 {{ font-size: 20px; margin-bottom: 16px; color: #333; }}
.stat-block {{ margin-bottom: 20px; }}
.stat-block h3 {{ font-size: 15px; color: #666; margin-bottom: 10px; }}
.bar-chart {{ max-width: 600px; }}
.bar-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }}
.bar-label {{ width: 60px; font-size: 13px; text-align: right; }}
.bar-track {{ flex: 1; height: 24px; background: #f0f2f5; border-radius: 12px; overflow: hidden; }}
.bar-fill {{ height: 100%; border-radius: 12px; transition: width 0.5s ease; }}
.bar-fill.diff-easy {{ background: linear-gradient(90deg, #b7eb8f, #52c41a); }}
.bar-fill.diff-medium {{ background: linear-gradient(90deg, #ffd591, #fa8c16); }}
.bar-fill.diff-hard {{ background: linear-gradient(90deg, #ffccc7, #ff4d4f); }}
.bar-value {{ font-size: 12px; color: #999; width: 100px; }}
.type-list, .bloom-list, .kp-list {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.type-tag {{ background: #e6e9ff; color: #667eea; font-size: 13px; padding: 4px 12px; border-radius: 16px; }}
.bloom-tag {{ background: #fff7e6; color: #fa8c16; font-size: 13px; padding: 4px 12px; border-radius: 16px; }}
.kp-tag {{ background: #e6fffb; color: #13c2c2; font-size: 13px; padding: 4px 12px; border-radius: 16px; }}

/* Controls */
.controls {{ max-width: 1200px; margin: 0 auto 20px; display: flex; gap: 12px; padding: 0 20px; flex-wrap: wrap; }}
.btn {{ padding: 10px 24px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }}
.btn-primary {{ background: #667eea; color: white; }}
.btn-primary:hover {{ background: #5a6fd6; }}
.btn-outline {{ background: white; color: #667eea; border: 1px solid #667eea; }}
.btn-outline:hover {{ background: #f5f7ff; }}
.btn-warning {{ background: #fa8c16; color: white; }}

/* Print mode */
@media print {{
    body {{ background: white; }}
    .answer-card, .controls {{ display: none; }}
    .answer-content {{ display: block !important; }}
    .answer-header {{ display: none; }}
    .section, .statistics-section {{ box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }}
    .quiz-header {{ background: #333 !important; -webkit-print-color-adjust: exact; }}
}}

/* Responsive */
@media (max-width: 768px) {{
    .main-container {{ flex-direction: column; padding: 10px; }}
    .answer-card {{ width: 100%; position: static; }}
    .answer-card .card-grid {{ grid-template-columns: repeat(10, 1fr); }}
    .quiz-header h1 {{ font-size: 20px; }}
    .q-stem {{ font-size: 14px; }}
}}
</style>
</head>
<body>

<div class="quiz-header">
    <h1>{escape(title)}</h1>
    <div class="quiz-meta">
        {f'<span>学科：{escape(subject)}</span>' if subject else ''}
        {f'<span>学段：{escape(grade)}</span>' if grade else ''}
        <span>题数：{len(questions)}题</span>
        <span>建议时长：{escape(str(total_time))}</span>
        <span>生成日期：{now}</span>
    </div>
</div>

<div class="controls">
    <button class="btn btn-primary" onclick="submitQuiz()">提交判分</button>
    <button class="btn btn-outline" onclick="showAllAnswers()">显示全部答案</button>
    <button class="btn btn-outline" onclick="hideAllAnswers()">隐藏全部答案</button>
    <button class="btn btn-outline" onclick="window.print()">打印试卷</button>
    <button class="btn btn-warning" onclick="resetQuiz()">重置</button>
</div>

<div class="main-container">
    <div class="content-area">
        {sections_html}
    </div>
    {answer_card}
</div>

{statistics}

<script>
const quizData = {json.dumps(data, ensure_ascii=False)};
let answered = {{}};

function checkAnswer(qid) {{
    // Mark as answered in answer card
    answered[qid] = true;
    const card = document.querySelector(`.card-item[data-qid="${{qid}}"]`);
    if (card) card.classList.add('answered');
    updateStats();
}}

function updateStats() {{
    const total = Object.keys(quizData.questions || {{}}).length;
    const done = Object.keys(answered).length;
    const stats = document.getElementById('cardStats');
    if (stats) stats.textContent = `已作答: ${{done}} / ${{total}}`;
}}

function toggleAnswer(header) {{
    const block = header.parentElement;
    const content = block.querySelector('.answer-content');
    block.classList.toggle('open');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}}

function showAllAnswers() {{
    document.querySelectorAll('.answer-block').forEach(b => {{
        b.classList.add('open');
        b.querySelector('.answer-content').style.display = 'block';
    }});
}}

function hideAllAnswers() {{
    document.querySelectorAll('.answer-block').forEach(b => {{
        b.classList.remove('open');
        b.querySelector('.answer-content').style.display = 'none';
    }});
}}

function submitQuiz() {{
    let correct = 0;
    let total = 0;
    let totalScore = 0;
    let earnedScore = 0;

    (quizData.questions || []).forEach((q, i) => {{
        const qid = q.id || `Q${{String(i+1).padStart(2,'0')}}`;
        const type = q.type || '';
        const correctAnswer = String(q.answer || '').trim();

        if (type.includes('单选') || type.includes('判断')) {{
            total++;
            totalScore += q.score || 0;
            const selected = document.querySelector(`input[name="q${{qid}}"]:checked`);
            if (selected) {{
                const val = selected.value;
                if (val === correctAnswer) {{
                    correct++;
                    earnedScore += q.score || 0;
                    markOption(qid, val, 'correct');
                }} else {{
                    markOption(qid, val, 'wrong');
                    markOption(qid, correctAnswer, 'correct');
                }}
            }}
        }} else if (type.includes('多选')) {{
            total++;
            totalScore += q.score || 0;
            const selected = Array.from(document.querySelectorAll(`input[name="q${{qid}}"]:checked`)).map(s => s.value).sort().join('');
            const correctArr = correctAnswer.split('').sort().join('');
            if (selected === correctArr) {{
                correct++;
                earnedScore += q.score || 0;
                selected.split('').forEach(v => markOption(qid, v, 'correct'));
            }} else {{
                correctAnswer.split('').forEach(v => markOption(qid, v, 'correct'));
            }}
        }}
    }});

    if (total === 0) {{
        alert('客观题已全部展开，主观题请自行对照答案评分。');
        showAllAnswers();
        return;
    }}

    const pct = total > 0 ? Math.round(correct / total * 100) : 0;
    alert(`客观题判分完成！\\n正确：${{correct}} / ${{total}}  正确率：${{pct}}%\\n客观题得分：${{earnedScore}} / ${{totalScore}}\\n\\n主观题请对照答案自行评分。`);
    showAllAnswers();
}}

function markOption(qid, letter, cls) {{
    const opt = document.querySelector(`.option[data-qid="${{qid}}"][data-letter="${{letter}}"]`);
    if (opt) opt.classList.add(cls);
}}

function resetQuiz() {{
    if (!confirm('确定要重置所有答案吗？')) return;
    document.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(i => i.checked = false);
    document.querySelectorAll('input[type="text"], textarea').forEach(i => i.value = '');
    document.querySelectorAll('select').forEach(s => s.selectedIndex = 0);
    document.querySelectorAll('.option').forEach(o => o.classList.remove('correct', 'wrong'));
    document.querySelectorAll('.card-item').forEach(c => c.classList.remove('answered'));
    answered = {{}};
    hideAllAnswers();
    updateStats();
}}

// Initialize
updateStats();
</script>

</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate interactive HTML quiz from JSON data")
    parser.add_argument("--data", type=str, help="Quiz JSON data string")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--output", "-o", type=str, default="quiz.html", help="Output HTML file path")
    args = parser.parse_args()

    data = load_data(args)
    html = generate_html(data)

    output_path = os.path.abspath(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Quiz HTML generated: {output_path}")
    print(f"Questions: {len(data.get('questions', []))}")


if __name__ == "__main__":
    main()
