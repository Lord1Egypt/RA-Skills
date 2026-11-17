#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课文学习页生成器
生成带侧边栏导航的课文学习 HTML：原文 + 音频播放 + 中文翻译。
"""

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import wrap_html, esc_html


def read_file(filepath):
    """读取文件内容"""
    path = Path(filepath)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def generate_lesson_body(lesson_text, translation_text, audio_path):
    """生成课文学习页的 body 内容"""
    # 音频嵌入
    audio_html = ""
    if audio_path:
        apath = Path(audio_path)
        if apath.exists():
            with open(apath, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("ascii")
            audio_html = f'''
    <div class="card audio-card">
      <h2>🔊 课文朗读</h2>
      <audio controls style="width:100%">
        <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
        您的浏览器不支持音频播放。
      </audio>
      <div class="speed-controls">
        <button class="speed-btn" data-speed="0.75">0.75x</button>
        <button class="speed-btn active" data-speed="1">1x</button>
        <button class="speed-btn" data-speed="1.25">1.25x</button>
        <button class="speed-btn" data-speed="1.5">1.5x</button>
      </div>
    </div>'''

    # 课文段落
    paragraphs = [p.strip() for p in lesson_text.split('\n\n') if p.strip()]
    if not paragraphs:
        paragraphs = [lesson_text]
    lesson_html = '\n'.join(f'      <p>{esc_html(p)}</p>' for p in paragraphs)

    # 翻译段落
    translation_html = ""
    if translation_text:
        trans_paragraphs = [p.strip() for p in translation_text.split('\n\n') if p.strip()]
        if not trans_paragraphs:
            trans_paragraphs = [translation_text]
        translation_html = f'''
    <div class="card">
      <h2>📖 中文翻译</h2>
      <div class="content translation">
        {''.join(f"<p>{esc_html(p)}</p>" for p in trans_paragraphs)}
      </div>
    </div>'''

    body = f'''
    <h1 class="page-title">📖 课文学习</h1>
{audio_html}
    <div class="card">
      <h2>🔤 英文原文</h2>
      <div class="content lesson">
{lesson_html}
      </div>
    </div>
{translation_html}'''

    return body


def generate_lesson_css():
    """课文学习页额外 CSS"""
    return '''
    .content p {
      margin-bottom: 12px;
      font-size: 1.1em;
      line-height: 1.8;
    }
    .content.lesson p {
      font-size: 1.15em;
    }
    .content.translation p {
      color: #666;
      font-size: 1.05em;
    }
    .audio-card audio {
      margin: 10px 0;
    }
    .speed-controls {
      margin-top: 10px;
      text-align: center;
    }
    .speed-controls button {
      padding: 6px 14px;
      margin: 4px;
      border: 1px solid #ddd;
      border-radius: 6px;
      background: #fff;
      cursor: pointer;
      font-size: 0.9em;
      transition: all 0.2s;
    }
    .speed-controls button.active {
      background: #667eea;
      color: #fff;
      border-color: #667eea;
    }'''


def generate_lesson_js():
    """课文学习页 JS"""
    return '''
    const audio = document.querySelector('audio');
    if (audio) {
      document.querySelectorAll('.speed-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          audio.playbackRate = parseFloat(btn.dataset.speed);
          document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        });
      });
    }'''


def main():
    parser = argparse.ArgumentParser(
        description="课文学习页生成器：生成带侧边栏导航的课文学习 HTML"
    )
    parser.add_argument("-t", "--text", required=True, help="课文文本文件路径")
    parser.add_argument("-a", "--audio", help="课文音频文件路径")
    parser.add_argument("--translation", help="中文翻译文件路径（可选）")
    parser.add_argument("-o", "--output", default="lesson.html", help="输出 HTML 文件路径 (默认: lesson.html)")
    args = parser.parse_args()

    lesson_text = read_file(args.text)
    if not lesson_text:
        print(f"错误：课文文件不存在或为空：{args.text}", file=sys.stderr)
        sys.exit(1)

    translation_text = None
    if args.translation:
        translation_text = read_file(args.translation)
        if not translation_text:
            print(f"警告：翻译文件不存在或为空：{args.translation}")

    print(f"课文长度: {len(lesson_text)} 字符")
    if translation_text:
        print(f"翻译长度: {len(translation_text)} 字符")
    if args.audio:
        audio_size = Path(args.audio).stat().st_size if Path(args.audio).exists() else 0
        print(f"音频大小: {audio_size / 1024:.1f} KB")

    body = generate_lesson_body(lesson_text, translation_text, args.audio)
    css = generate_lesson_css()
    js = generate_lesson_js()
    html = wrap_html("课文学习", "lesson.html", body, css, js)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"[OK] 课文学习页已保存：{output_path}（{output_path.stat().st_size / 1024:.1f} KB）")


if __name__ == "__main__":
    main()
