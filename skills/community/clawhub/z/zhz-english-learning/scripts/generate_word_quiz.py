#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词测验页生成器
生成带侧边栏导航的单词测验 HTML，含 4 种测验模式，音频内嵌。
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import wrap_html, esc_html


def parse_words_md(filepath):
    """解析 words.md，返回单词列表"""
    text = Path(filepath).read_text(encoding="utf-8")
    words = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "English" in stripped and "Chinese" in stripped:
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            parts = [p.strip() for p in stripped.split("|")]
            parts = [p for p in parts if p]
            if len(parts) >= 4:
                words.append({
                    "english": parts[0].strip(),
                    "phonetic": parts[1].strip(),
                    "pos": parts[2].strip(),
                    "chinese": parts[3].strip()
                })
        elif in_table and not stripped.startswith("|"):
            break
    return words


def load_audio_b64(sounds_dir, filename):
    """加载音频文件并返回 base64 data URI"""
    path = Path(sounds_dir) / filename
    if path.exists():
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        return f"data:audio/mpeg;base64,{data}"
    return None


def generate_quiz_body_and_code(words, sounds_dir):
    """生成测验页的 body + CSS + JS"""
    audio_map = {}
    for w in words:
        safe = re.sub(r'[^\w\s-]', '', w["english"].lower().strip()).replace(' ', '_')
        audio_map[w["english"]] = {
            "male": load_audio_b64(sounds_dir, f"{safe}_male.mp3"),
            "female": load_audio_b64(sounds_dir, f"{safe}_female.mp3"),
        }

    words_json = json.dumps(words, ensure_ascii=False)
    audio_json = json.dumps(audio_map, ensure_ascii=False)

    css = '''
    .mode-tabs {
      display: flex;
      background: #fff;
      border-radius: 12px;
      padding: 4px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .mode-tab {
      flex: 1;
      padding: 12px 8px;
      text-align: center;
      cursor: pointer;
      border-radius: 8px;
      font-size: 0.9em;
      transition: all 0.2s;
      font-weight: 500;
    }
    .mode-tab:hover { background: #f8f9fa; }
    .mode-tab.active {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .score-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #fff;
      border-radius: 12px;
      padding: 12px 20px;
      margin-bottom: 16px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .score-bar .progress-text { font-size: 0.9em; color: #666; }
    .score-bar .score { font-weight: 700; color: #667eea; font-size: 1.1em; }
    .progress-track {
      width: 100%;
      height: 6px;
      background: #e9ecef;
      border-radius: 3px;
      margin-bottom: 16px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      border-radius: 3px;
      transition: width 0.4s ease;
    }
    .card-quiz {
      background: #fff;
      border-radius: 16px;
      padding: 28px 24px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
      text-align: center;
    }
    .card-quiz .prompt {
      font-size: 1.8em;
      font-weight: 700;
      margin-bottom: 8px;
      color: #333;
    }
    .card-quiz .prompt-sub {
      font-size: 0.9em;
      color: #999;
      margin-bottom: 20px;
    }
    .card-quiz .play-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 28px;
      border: none;
      border-radius: 30px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      font-size: 1em;
      cursor: pointer;
      margin-bottom: 24px;
      transition: transform 0.15s;
    }
    .card-quiz .play-btn:hover { transform: scale(1.05); }
    .card-quiz .play-btn:active { transform: scale(0.97); }
    .card-quiz .play-btn.playing { opacity: 0.7; }
    .options {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 16px;
    }
    .option-btn {
      padding: 16px 12px;
      border: 2px solid #e9ecef;
      border-radius: 12px;
      background: #fff;
      font-size: 1.05em;
      cursor: pointer;
      transition: all 0.2s;
      word-break: break-word;
    }
    .option-btn:hover { border-color: #667eea; background: #f8f6ff; }
    .option-btn.correct {
      border-color: #34c759; background: #e8f9ee; color: #1a7f37;
      animation: pulse 0.3s ease;
    }
    .option-btn.wrong {
      border-color: #ff3b30; background: #fff0f0; color: #c41e3a;
      animation: shake 0.4s ease;
    }
    .option-btn.disabled { pointer-events: none; opacity: 0.6; }
    @keyframes pulse {
      0%,100% { transform: scale(1); }
      50% { transform: scale(1.04); }
    }
    @keyframes shake {
      0%,100% { transform: translateX(0); }
      25% { transform: translateX(-6px); }
      75% { transform: translateX(6px); }
    }
    .spell-input {
      width: 80%;
      padding: 14px;
      font-size: 1.3em;
      text-align: center;
      border: 2px solid #e9ecef;
      border-radius: 12px;
      outline: none;
      transition: border-color 0.2s;
      margin-bottom: 16px;
    }
    .spell-input:focus { border-color: #667eea; }
    .spell-input.correct { border-color: #34c759; background: #e8f9ee; }
    .spell-input.wrong { border-color: #ff3b30; background: #fff0f0; }
    .submit-btn {
      padding: 12px 36px;
      border: none;
      border-radius: 30px;
      background: #667eea;
      color: white;
      font-size: 1em;
      cursor: pointer;
    }
    .submit-btn:hover { background: #5a6fd6; }
    .submit-btn:disabled { background: #ccc; cursor: not-allowed; }
    .feedback {
      margin-top: 16px;
      padding: 12px;
      border-radius: 8px;
      font-size: 1em;
      display: none;
    }
    .feedback.show { display: block; }
    .feedback.correct { background: #e8f9ee; color: #1a7f37; }
    .feedback.wrong { background: #fff0f0; color: #c41e3a; }
    .result-screen {
      text-align: center;
      padding: 40px 20px;
    }
    .result-screen .big-score {
      font-size: 4em;
      font-weight: 800;
      background: linear-gradient(135deg, #667eea, #764ba2);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .result-screen p { margin: 12px 0; color: #666; font-size: 1.1em; }
    .retry-btn {
      margin-top: 20px;
      padding: 14px 40px;
      border: none;
      border-radius: 30px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      font-size: 1.1em;
      cursor: pointer;
    }'''

    js = f'''
    const WORDS = {words_json};
    const AUDIO = {audio_json};
    let mode = "listen";
    let queue = [];
    let curIdx = 0;
    let score = 0;
    let answered = false;

    function playAudio(wordEnglish, times, callback) {{
      const data = AUDIO[wordEnglish];
      if (!data || !data.female) {{ if (callback) callback(); return; }}
      const audio = new Audio(data.female);
      let played = 0;
      audio.addEventListener('ended', () => {{
        played++;
        if (played < times) {{
          setTimeout(() => {{ audio.currentTime = 0; audio.play(); }}, 400);
        }} else {{ if (callback) callback(); }}
      }});
      audio.play().catch(() => {{ if (callback) callback(); }});
    }}

    function playMaleFemale(wordEnglish, callback) {{
      const data = AUDIO[wordEnglish];
      if (!data || !data.male) {{ if (callback) callback(); return; }}
      const male = new Audio(data.male);
      male.addEventListener('ended', () => {{
        setTimeout(() => {{
          if (data.female) {{
            const female = new Audio(data.female);
            female.addEventListener('ended', () => {{ if (callback) callback(); }});
            female.play().catch(() => {{ if (callback) callback(); }});
          }} else {{ if (callback) callback(); }}
        }}, 400);
      }});
      male.play().catch(() => {{ if (callback) callback(); }});
    }}

    function shuffle(arr) {{
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }}
      return a;
    }}

    function pickDistractors(correct, key, n) {{
      const others = WORDS.filter(w => w[key] !== correct[key]);
      return shuffle(others).slice(0, n - 1);
    }}

    function updateProgress() {{
      document.getElementById('curIdxEl').textContent = curIdx + 1;
      document.getElementById('totalQEl').textContent = queue.length;
      document.getElementById('scoreNum').textContent = score;
      const pct = queue.length > 0 ? ((curIdx) / queue.length * 100) : 0;
      document.getElementById('progressFill').style.width = pct + '%';
    }}

    function showResult() {{
      const pct = queue.length > 0 ? Math.round(score / queue.length * 100) : 0;
      let emoji = pct >= 90 ? '🎉' : pct >= 70 ? '👍' : pct >= 50 ? '💪' : '📚';
      document.getElementById('quizContent').innerHTML = `
        <div class="card-quiz result-screen">
          <div class="big-score">${{pct}}%</div>
          <p>${{emoji}} 答对 ${{score}} / ${{queue.length}} 题</p>
          <p>${{pct >= 90 ? '太棒了！' : pct >= 70 ? '不错哦！' : pct >= 50 ? '继续加油！' : '多练习几遍吧！'}}</p>
          <button class="retry-btn" onclick="startQuiz()">再来一轮</button>
        </div>`;
      document.getElementById('progressFill').style.width = '100%';
    }}

    function renderQuestion() {{
      if (curIdx >= queue.length) {{ showResult(); return; }}
      answered = false;
      updateProgress();
      const item = queue[curIdx];
      const container = document.getElementById('quizContent');
      if (mode === 'listen') renderListen(item, container);
      else if (mode === 'en2cn') renderEn2Cn(item, container);
      else if (mode === 'cn2en') renderCn2En(item, container);
      else if (mode === 'spell') renderSpell(item, container);
    }}

    function renderListen(item, container) {{
      container.innerHTML = `
        <div class="card-quiz">
          <p class="prompt-sub">🎧 听发音，选择中文含义</p>
          <button class="play-btn" id="playBtn" onclick="doPlayListen()">▶ 播放发音</button>
          <div class="options" id="options"></div>
        </div>`;
      setTimeout(() => doPlayListen(), 300);
      renderOptions(item, 'chinese');
    }}

    function doPlayListen() {{
      const btn = document.getElementById('playBtn');
      if (btn) {{ btn.classList.add('playing'); btn.textContent = '🔊 播放中...'; }}
      playMaleFemale(queue[curIdx].english, () => {{
        if (btn) {{ btn.classList.remove('playing'); btn.textContent = '▶ 再听一次'; }}
      }});
    }}

    function renderEn2Cn(item, container) {{
      container.innerHTML = `
        <div class="card-quiz">
          <p class="prompt">${{item.english}}</p>
          <p class="prompt-sub">${{item.phonetic || ''}} ${{item.pos || ''}}</p>
          <button class="play-btn" onclick="doPlayEn2Cn()">▶ 播放发音</button>
          <div class="options" id="options"></div>
        </div>`;
      setTimeout(() => doPlayEn2Cn(), 300);
      renderOptions(item, 'chinese');
    }}

    function doPlayEn2Cn() {{ playMaleFemale(queue[curIdx].english, null); }}

    function renderCn2En(item, container) {{
      container.innerHTML = `
        <div class="card-quiz">
          <p class="prompt">${{item.chinese}}</p>
          <p class="prompt-sub">选择对应的英文单词</p>
          <div class="options" id="options"></div>
        </div>`;
      renderOptions(item, 'english');
    }}

    function renderSpell(item, container) {{
      container.innerHTML = `
        <div class="card-quiz">
          <p class="prompt">${{item.chinese}}</p>
          <p class="prompt-sub">${{item.pos || ''}} 输入英文单词</p>
          <input class="spell-input" id="spellInput" type="text" autocomplete="off"
                 placeholder="输入英文..." onkeydown="if(event.key==='Enter')checkSpell()">
          <br>
          <button class="submit-btn" id="submitBtn" onclick="checkSpell()">确认</button>
          <div class="feedback" id="feedback"></div>
        </div>`;
      setTimeout(() => document.getElementById('spellInput')?.focus(), 100);
    }}

    function checkSpell() {{
      if (answered) return;
      const input = document.getElementById('spellInput');
      const feedback = document.getElementById('feedback');
      const item = queue[curIdx];
      const answer = input.value.trim().toLowerCase();
      const correct = item.english.toLowerCase();
      answered = true;
      document.getElementById('submitBtn').disabled = true;
      if (answer === correct) {{
        score++;
        input.classList.add('correct');
        feedback.className = 'feedback show correct';
        feedback.innerHTML = `✅ 正确！<strong>${{item.english}}</strong>`;
      }} else {{
        input.classList.add('wrong');
        feedback.className = 'feedback show wrong';
        feedback.innerHTML = `❌ 正确答案：<strong>${{item.english}}</strong>`;
      }}
      updateProgress();
      setTimeout(() => playMaleFemale(item.english, () => {{
        setTimeout(nextQuestion, 800);
      }}), 500);
    }}

    function renderOptions(item, answerKey) {{
      const distractors = pickDistractors(item, answerKey, 4);
      const options = shuffle([item, ...distractors]);
      const optsEl = document.getElementById('options');
      if (!optsEl) return;
      optsEl.innerHTML = '';
      options.forEach(opt => {{
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = opt[answerKey];
        btn.onclick = () => selectOption(btn, opt, item, answerKey);
        optsEl.appendChild(btn);
      }});
    }}

    function selectOption(btn, selected, correct, answerKey) {{
      if (answered) return;
      answered = true;
      const allBtns = document.querySelectorAll('.option-btn');
      allBtns.forEach(b => b.classList.add('disabled'));
      if (selected[answerKey] === correct[answerKey]) {{
        btn.classList.add('correct');
        score++;
      }} else {{
        btn.classList.add('wrong');
        allBtns.forEach(b => {{
          if (b.textContent === correct[answerKey]) b.classList.add('correct');
        }});
      }}
      updateProgress();
      if (mode === 'cn2en') {{
        setTimeout(() => playMaleFemale(correct.english, () => {{
          setTimeout(nextQuestion, 800);
        }}), 400);
      }} else {{
        setTimeout(nextQuestion, 1000);
      }}
    }}

    function nextQuestion() {{
      curIdx++;
      renderQuestion();
    }}

    document.querySelectorAll('.mode-tab').forEach(tab => {{
      tab.addEventListener('click', () => {{
        document.querySelectorAll('.mode-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        mode = tab.dataset.mode;
        startQuiz();
      }});
    }});

    function startQuiz() {{
      queue = shuffle([...WORDS]);
      curIdx = 0;
      score = 0;
      updateProgress();
      renderQuestion();
    }}

    startQuiz();'''

    body = f'''
    <h1 class="page-title">📝 单词测验</h1>
    <div class="mode-tabs">
      <div class="mode-tab active" data-mode="listen">🎧 听音选义</div>
      <div class="mode-tab" data-mode="en2cn">🔤 英文选义</div>
      <div class="mode-tab" data-mode="cn2en">🈶 中文选义</div>
      <div class="mode-tab" data-mode="spell">✍️ 默写单词</div>
    </div>
    <div class="score-bar">
      <span class="progress-text">第 <span id="curIdxEl">1</span> / <span id="totalQEl">0</span> 题</span>
      <span class="score">得分：<span id="scoreNum">0</span></span>
    </div>
    <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
    <div id="quizContent"></div>'''

    return body, css, js


def main():
    parser = argparse.ArgumentParser(
        description="单词测验页生成器：生成 4 种模式的互动测验 HTML"
    )
    parser.add_argument("-w", "--words", required=True, help="单词列表文件路径 (words.md)")
    parser.add_argument("-s", "--sounds", default="sounds", help="音频目录 (默认: sounds)")
    parser.add_argument("-o", "--output", default="quiz.html", help="输出 HTML 文件路径 (默认: quiz.html)")
    args = parser.parse_args()

    words_path = Path(args.words)
    if not words_path.exists():
        print(f"错误：单词列表文件不存在：{args.words}", file=sys.stderr)
        sys.exit(1)

    words = parse_words_md(words_path)
    if not words:
        print("错误：未从单词列表中找到单词", file=sys.stderr)
        sys.exit(1)

    if len(words) < 4:
        print("错误：至少需要 4 个单词才能生成四选一测验", file=sys.stderr)
        sys.exit(1)

    print(f"找到 {len(words)} 个单词")
    sounds_dir = Path(args.sounds)

    found_audio = 0
    for w in words:
        safe = re.sub(r'[^\w\s-]', '', w["english"].lower().strip()).replace(' ', '_')
        if (sounds_dir / f"{safe}_female.mp3").exists():
            found_audio += 1
    print(f"找到音频: {found_audio}/{len(words)} 个单词")

    body, css, js = generate_quiz_body_and_code(words, str(sounds_dir))
    html = wrap_html("单词测验", "quiz.html", body, css, js)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"[OK] 单词测验页已保存：{output_path}（{output_path.stat().st_size / 1024:.1f} KB）")


if __name__ == "__main__":
    main()
