#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Pipeline - 自然语言一键生成短视频

自然语言用法:
  python pipeline.py "帮我做一个零售业AI智能推荐的短视频"
  python pipeline.py "医疗AI如何改变诊断？做一个3分钟科普视频" --size 1920x1080

传统用法:
  python pipeline.py --lesson 1 --action all
  python pipeline.py --lesson 1 --action render --size 1080x1920

流程(8步):
  1. gen_outline.py   - AI生成大纲
  2. gen_narration.py - AI生成逐字稿
  3. gen_html.py      - 生成HTML课件
  4. gen_tsx.py       - 生成TSX组件
  5. gen_tts.py       - 生成TTS音频
  6. Composition生成  - 生成Composition + 注册Root.tsx
  7. timing_align.py  - 时序对齐验证（音画同步/帧对齐/字幕）
  8. remotion render  - 渲染视频
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Windows GBK workaround: force UTF-8 stdout/stderr
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
try:
    if sys.stdout and hasattr(sys.stdout, 'buffer'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr and hasattr(sys.stderr, 'buffer'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ─── 常量 ───────────────────────────────────────────────────────────────────
PROJECT_DIR = Path.home() / "course-video-remotion"
SCRIPTS_DIR = Path(__file__).parent
DASHSCOPE_CONFIG_PATH = Path.home() / '.openclaw/workspace/credentials/dashscope.json'
DESKTOP_OUTPUT = Path.home() / 'Desktop' / '02_课程产品' / '成品视频'


# ─── DashScope API 调用 ─────────────────────────────────────────────────────
def call_dashscope(prompt: str) -> str:
    """调用DashScope qwen-max API，返回原始文本内容"""
    import requests

    config = json.loads(DASHSCOPE_CONFIG_PATH.read_text(encoding='utf-8'))
    api_key = config['api_key']
    base_url = config.get('base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "qwen-max",
        "input": {
            "messages": [{"role": "user", "content": prompt}]
        },
        "parameters": {
            "result_format": "message",
            "temperature": 0.7
        }
    }

    if 'compatible-mode' in base_url:
        api_endpoint = f'{base_url}/chat/completions'
    else:
        api_endpoint = f'{base_url}/services/aigc/text-generation/generation'

    resp = requests.post(api_endpoint, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    return result['output']['choices'][0]['message']['content']


def parse_json_from_text(text: str):
    """从LLM回复中提取JSON"""
    # 尝试 ```json ... ``` 代码块
    m = re.search(r'```(?:json)?\s*\n([\s\S]*?)```', text)
    if m:
        return json.loads(m.group(1).strip())
    # 尝试直接解析
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # 尝试找 { ... } 块（贪婪匹配最外层）
    m = re.search(r'(\{[\s\S]*\})', text)
    if m:
        return json.loads(m.group(1))
    # 尝试找 [ ... ] 块
    m = re.search(r'(\[[\s\S]*\])', text)
    if m:
        return json.loads(m.group(1))
    raise ValueError(f'无法从文本中提取JSON: {text[:200]}')


# ─── Step 0: 自然语言解析 ────────────────────────────────────────────────────
def extract_info_from_prompt(user_prompt: str) -> dict:
    """从自然语言中提取 topic/industry/audience/lesson_name"""
    extraction_prompt = (
        '从以下需求中提取：主题(topic)、行业(industry)、受众(audience)、'
        '课名(lesson_name，英文小写+下划线，简短)。\n'
        '返回纯JSON，不要解释：\n'
        '{"topic": "", "industry": "", "audience": "", "lesson_name": ""}\n\n'
        f'需求：{user_prompt}'
    )
    try:
        raw = call_dashscope(extraction_prompt)
        info = parse_json_from_text(raw)
        # 确保lesson_name合法
        ln = info.get('lesson_name', 'ai_video')
        ln = re.sub(r'[^a-z0-9_]', '_', ln.lower())
        ln = re.sub(r'_+', '_', ln).strip('_')
        info['lesson_name'] = ln or 'ai_video'
        return info
    except Exception as e:
        print(f'[WARN] LLM解析失败，使用默认值: {e}')
        return {
            "topic": "AI应用",
            "industry": "通用",
            "audience": "普通观众",
            "lesson_name": "ai_application"
        }


# ─── 子脚本执行 ─────────────────────────────────────────────────────────────
def run_step(script_name: str, args: list, step_label: str) -> bool:
    """执行子脚本，打印状态和耗时"""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"  [ERROR] 脚本不存在: {script_path}")
        return False

    cmd = ["python", str(script_path)] + args
    print(f"  CMD: {' '.join(cmd)}")

    t0 = time.time()
    result = subprocess.run(
        cmd, cwd=str(PROJECT_DIR),
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    elapsed = time.time() - t0

    if result.stdout.strip():
        for line in result.stdout.strip().split('\n'):
            print(f"    {line}")
    if result.stderr.strip():
        for line in result.stderr.strip().split('\n'):
            print(f"    [stderr] {line}")

    if result.returncode != 0:
        print(f"  [{step_label}] FAILED (exit={result.returncode}, {elapsed:.1f}s)")
        return False

    print(f"  [{step_label}] OK ({elapsed:.1f}s)")
    return True


# ─── 验证函数 ────────────────────────────────────────────────────────────────
def verify_file(path: Path, min_size=0, label="文件"):
    """验证文件存在且大于最小尺寸"""
    if not path.exists():
        return False, f"{label}不存在: {path}"
    sz = path.stat().st_size
    if sz < min_size:
        return False, f"{label}太小: {sz} bytes < {min_size}"
    return True, f"{label} OK ({sz} bytes)"


def verify_step(label, path, min_size=0):
    ok, msg = verify_file(path, min_size, label)
    print(f"  [VERIFY] {msg}")
    return ok


# ─── Step 6: Composition 生成 + Root.tsx 注册 ────────────────────────────────
def generate_composition(lesson_name: str) -> tuple:
    """
    读取 slide_map.json, 生成 Composition TSX, 返回 (comp_name, comp_path)
    """
    slide_map_path = PROJECT_DIR / 'src' / 'slides' / lesson_name / 'slide_map.json'
    if not slide_map_path.exists():
        raise FileNotFoundError(f'slide_map.json not found: {slide_map_path}')

    sm = json.loads(slide_map_path.read_text(encoding='utf-8'))

    # 生成 import 和 SLIDES 数组
    imports = []
    slides_entries = []
    for entry in sm:
        tsx = entry['component']
        imports.append(f"import {{ {tsx} }} from '../slides/{lesson_name}/{tsx}';")

        audio = entry.get('audioFile')
        audio_str = f"'{audio}'" if audio else 'null'
        is_cover = str(entry.get('isCover', False)).lower()
        slides_entries.append(
            f"  {{ id: '{entry['id']}', component: {tsx}, "
            f"audioFile: {audio_str}, isCover: {is_cover} }},"
        )

    # PascalCase composition name
    comp_name = ''.join(w.capitalize() for w in lesson_name.split('_')) + 'Composition'

    # 使用列表拼接避免f-string与隐式拼接的转义问题
    content_lines = [
        "import React from 'react';",
        "import { Audio, Sequence, staticFile, useVideoConfig } from 'remotion';",
        "import { VIDEO_CONFIG, COVER_DURATION, ENDING_DURATION } from '../utils/constants';",
        "import { BackCover } from '../components/BackCover';",
        "",
    ]
    content_lines.extend(imports)
    content_lines.extend([
        "",
        "interface Props {",
        "  lessonId: string;",
        "  durations?: Record<string, number>;",
        "}",
        "",
        "const SLIDES = [",
    ])
    content_lines.extend(slides_entries)
    content_lines.extend([
        "];",
        "",
        f"export const {comp_name}: React.FC<Props> = ({{ lessonId, durations }}) => {{",
        "  const { fps } = useVideoConfig();",
        "  const dirName = lessonId.replace(/-/g, '_');",
        "",
        "  let currentFrame = 0;",
        "  const timeline = SLIDES.map((slide) => {",
        "    let frames: number;",
        "    if (slide.isCover) {",
        "      frames = Math.ceil(COVER_DURATION * fps);",
        "    } else {",
        "      const dur = durations?.[slide.audioFile!] || 5;",
        "      frames = Math.ceil(dur * fps);",
        "    }",
        "    const start = currentFrame;",
        "    currentFrame += frames;",
        "    return { ...slide, start, frames };",
        "  });",
        "",
        "  const backCoverStart = currentFrame;",
        "  const backCoverFrames = Math.ceil(ENDING_DURATION * fps);",
        "",
        "  return (",
        "    <div style={{ position: 'relative', width: VIDEO_CONFIG.width, height: VIDEO_CONFIG.height }}>",
        "      {timeline.map((slide) => {",
        "        const SlideComponent = slide.component;",
        "        return (",
        "          <Sequence key={slide.id} from={slide.start} durationInFrames={slide.frames} name={String(slide.id)}>",
        "            <SlideComponent />",
        "            {!slide.isCover && slide.audioFile && (",
        "              <Audio src={staticFile(`audio/${dirName}/${slide.audioFile}`)} />",
        "            )}",
        "          </Sequence>",
        "        );",
        "      })}",
        '      <Sequence from={backCoverStart} durationInFrames={backCoverFrames} name="back-cover">',
        "        <BackCover />",
        "      </Sequence>",
        "    </div>",
        "  );",
        "};",
        "",
    ])
    content = '\n'.join(content_lines)

    comp_dir = PROJECT_DIR / 'src' / 'compositions'
    comp_dir.mkdir(parents=True, exist_ok=True)
    comp_path = comp_dir / f'{comp_name}.tsx'
    comp_path.write_text(content, encoding='utf-8')

    print(f"  Generated {comp_name}.tsx ({len(sm)} slides)")
    return comp_name, comp_path


def register_in_root_tsx(lesson_name: str, comp_name: str):
    """在 Root.tsx 中注册 Composition（如果尚未注册）"""
    root_path = PROJECT_DIR / 'src' / 'Root.tsx'
    if not root_path.exists():
        print(f"  [WARN] Root.tsx 不存在: {root_path}")
        return False

    root = root_path.read_text(encoding='utf-8')

    if comp_name in root:
        print(f"  {comp_name} 已在 Root.tsx 中注册")
        return True

    lesson_id = lesson_name.replace('_', '-')
    import_line = f"import {{ {comp_name} }} from './compositions/{comp_name}';"
    entry_line = f"  {{ id: '{lesson_id}', component: {comp_name} }},"

    # 在最后一个 import 行之后插入 import
    lines = root.split('\n')
    new_lines = []
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.startswith('import '):
            last_import_idx = i

    for i, line in enumerate(lines):
        new_lines.append(line)
        if i == last_import_idx:
            new_lines.append(import_line)

    root = '\n'.join(new_lines)

    # 在 LESSONS 数组的 ]; 之前插入 entry
    root = root.replace('\n];', f'\n{entry_line}\n];')

    root_path.write_text(root, encoding='utf-8')
    print(f"  Registered {comp_name} in Root.tsx (id='{lesson_id}')")
    return True


# ─── render.py 的修复版本（内联，避免 render.py 的 emoji/编码 bug）───────────
def do_render(lesson_name: str, size: str) -> Path:
    """执行 remotion render，返回输出视频路径"""
    lesson_id = lesson_name.replace('_', '-')
    width, height = map(int, size.split('x'))

    output_dir = PROJECT_DIR / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'{lesson_name}_{width}x{height}.mp4'

    cmd = [
        'npx', 'remotion', 'render',
        'src/index.ts',
        lesson_id,
        str(output_path),
        '--codec', 'h264',
        # '--config', 'src/config.ts',  # 使用默认配置
    ]

    print(f"  CMD: {' '.join(cmd)}")
    t0 = time.time()
    # shell=True needed on Windows so npx.cmd can be found
    result = subprocess.run(' '.join(cmd), cwd=str(PROJECT_DIR), shell=True)
    elapsed = time.time() - t0

    if result.returncode != 0:
        print(f"  [RENDER] FAILED (exit={result.returncode}, {elapsed:.1f}s)")
        return None

    print(f"  [RENDER] OK ({elapsed:.1f}s)")
    return output_path


# ─── 主流程 ──────────────────────────────────────────────────────────────────
def run_natural_language_pipeline(user_prompt: str, size: str):
    """自然语言一键生成完整流程"""
    total_start = time.time()

    # ── Step 0: 解析自然语言 ──
    print("=" * 60)
    print("Step 0: 解析自然语言输入")
    print("=" * 60)
    info = extract_info_from_prompt(user_prompt)
    topic = info['topic']
    industry = info['industry']
    audience = info['audience']
    lesson_name = info['lesson_name']
    print(f"  topic       = {topic}")
    print(f"  industry    = {industry}")
    print(f"  audience    = {audience}")
    print(f"  lesson_name = {lesson_name}")

    lesson_dir = PROJECT_DIR / 'src' / 'slides' / lesson_name
    narration_path = lesson_dir / 'narration.json'
    outline_path = lesson_dir / 'outline.json'

    # ── Step 1: 生成大纲 ──
    print("\n" + "=" * 60)
    print("Step 1: 生成大纲 (gen_outline.py)")
    print("=" * 60)
    ok = run_step('gen_outline.py', [
        '--topic', topic,
        '--industry', industry,
        '--audience', audience,
        '--slides', '7',
        '--project', str(PROJECT_DIR),
        '--lesson', lesson_name,
    ], 'OUTLINE')
    if not ok:
        sys.exit(1)
    if not verify_step('outline.json', outline_path, 100):
        sys.exit(1)

    # ── Step 2: 生成逐字稿 ──
    print("\n" + "=" * 60)
    print("Step 2: 生成逐字稿 (gen_narration.py)")
    print("=" * 60)
    ok = run_step('gen_narration.py', [
        '--outline', str(outline_path),
        '--project', str(PROJECT_DIR),
        '--lesson', lesson_name,
    ], 'NARRATION')
    if not ok:
        sys.exit(1)
    if not verify_step('narration.json', narration_path, 200):
        sys.exit(1)

    # ── Step 3: 生成HTML ──
    print("\n" + "=" * 60)
    print("Step 3: 生成HTML (gen_html.py)")
    print("=" * 60)
    ok = run_step('gen_html.py', [
        '--narration', str(narration_path),
        '--project', str(PROJECT_DIR),
        '--lesson', lesson_name,
    ], 'HTML')
    if not ok:
        sys.exit(1)
    html_path = PROJECT_DIR / 'course_html' / f'{lesson_name}.html'
    verify_step('HTML', html_path, 10000)

    # ── Step 4: 生成TSX组件 ──
    print("\n" + "=" * 60)
    print("Step 4: 生成TSX组件 (gen_tsx.py)")
    print("=" * 60)
    ok = run_step('gen_tsx.py', [
        '--narration', str(narration_path),
        '--project', str(PROJECT_DIR),
        '--lesson', lesson_name,
    ], 'TSX')
    if not ok:
        sys.exit(1)
    slide_map_path = lesson_dir / 'slide_map.json'
    if not verify_step('slide_map.json', slide_map_path, 50):
        sys.exit(1)

    # ── Step 5: 生成TTS音频 ──
    print("\n" + "=" * 60)
    print("Step 5: 生成TTS音频 (gen_tts.py)")
    print("=" * 60)
    ok = run_step('gen_tts.py', [
        '--narration', str(narration_path),
        '--project', str(PROJECT_DIR),
        '--lesson', lesson_name,
    ], 'TTS')
    if not ok:
        sys.exit(1)
    audio_dir = PROJECT_DIR / 'public' / 'audio' / lesson_name
    audio_count = len(list(audio_dir.glob('audio_*.mp3'))) if audio_dir.exists() else 0
    print(f"  [VERIFY] 音频文件数: {audio_count}")
    if audio_count == 0:
        print("  [ERROR] 没有生成任何音频文件!")
        sys.exit(1)

    # ── Step 6: 生成Composition + 注册Root.tsx ──
    print("\n" + "=" * 60)
    print("Step 6: 生成Composition + 注册Root.tsx")
    print("=" * 60)
    try:
        # 先确保所有现有课程的Composition都存在（generate_compositions.py）
        gen_comp_script = PROJECT_DIR / 'scripts' / 'generate_compositions.py'
        if gen_comp_script.exists():
            print("  [PRE] 同步所有现有Composition...")
            result = subprocess.run(
                ['python', str(gen_comp_script)],
                cwd=str(PROJECT_DIR),
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            if result.returncode == 0:
                print("  [PRE] 现有Composition同步完成")
            else:
                print(f"  [WARN] 现有Composition同步失败，继续...")
        # 生成新课程的Composition
        comp_name, comp_path = generate_composition(lesson_name)
        register_in_root_tsx(lesson_name, comp_name)
    except Exception as e:
        print(f"  [ERROR] Composition生成失败: {e}")
        sys.exit(1)
    if not verify_step('Composition', comp_path, 500):
        sys.exit(1)

    # ── Step 7: 时序对齐验证 ──
    print("\n" + "=" * 60)
    print("Step 7: 时序对齐验证 (timing_align.py)")
    print("=" * 60)
    timing_script = SCRIPTS_DIR / 'timing_align.py'
    if timing_script.exists():
        timing_result = subprocess.run(
            ['python', str(timing_script),
             '--lesson', lesson_name,
             '--project', str(PROJECT_DIR),
             '--fix'],
            cwd=str(PROJECT_DIR),
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        if timing_result.stdout.strip():
            for line in timing_result.stdout.strip().split('\n'):
                print(f"    {line}")
        if timing_result.stderr.strip():
            for line in timing_result.stderr.strip().split('\n'):
                print(f"    [stderr] {line}")
        if timing_result.returncode != 0:
            print(f"  [TIMING] 时序对齐检查失败（存在critical问题），但继续渲染")
            print(f"  [TIMING] 退出码: {timing_result.returncode}")
        else:
            print(f"  [TIMING] 时序对齐验证通过")
    else:
        print(f"  [WARN] timing_align.py 不存在，跳过时序验证")

    # ── Step 8: Remotion 渲染 ──
    print("\n" + "=" * 60)
    print("Step 8: Remotion 渲染")
    print("=" * 60)
    video_path = do_render(lesson_name, size)
    if video_path is None or not video_path.exists():
        print("  [ERROR] 渲染失败，未生成视频文件")
        sys.exit(1)
    video_size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"  [VERIFY] 视频文件: {video_path} ({video_size_mb:.1f} MB)")

    # ── 复制到桌面 ──
    print("\n" + "=" * 60)
    print("复制成品到桌面")
    print("=" * 60)
    DESKTOP_OUTPUT.mkdir(parents=True, exist_ok=True)
    dest = DESKTOP_OUTPUT / video_path.name
    shutil.copy2(video_path, dest)
    print(f"  已复制: {dest}")

    # ── 成品报告 ──
    total_elapsed = time.time() - total_start
    print("\n" + "=" * 60)
    print("成品报告")
    print("=" * 60)
    print(f"  主题:     {topic}")
    print(f"  行业:     {industry}")
    print(f"  受众:     {audience}")
    print(f"  课名:     {lesson_name}")
    print(f"  视频尺寸: {size}")
    print(f"  音频数:   {audio_count} 段")
    print(f"  视频大小: {video_size_mb:.1f} MB")
    print(f"  成品位置: {dest}")
    print(f"  项目位置: {lesson_dir}")
    print(f"  总耗时:   {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)")
    print("=" * 60)
    print("Pipeline 执行成功!")
    print("=" * 60)


# ─── 传统模式 ────────────────────────────────────────────────────────────────
def run_legacy_pipeline(lesson_num: int, action: str, size: str):
    """传统模式（兼容旧用法）"""
    lesson = f"lesson_{lesson_num:02d}"
    print(f"Pipeline启动: {lesson}, action={action}, size={size}")

    if action in ('all', 'gen_html'):
        narration_path = PROJECT_DIR / 'src' / 'slides' / lesson / 'narration.json'
        ok = run_step('gen_html.py', [
            '--narration', str(narration_path),
            '--project', str(PROJECT_DIR),
            '--lesson', lesson,
        ], 'HTML')
        if not ok:
            sys.exit(1)

    if action in ('all', 'gen_compositions'):
        ok = run_step('gen_compositions.py', [
            '--lessons', str(lesson_num),
        ], 'COMPOSITIONS')
        if not ok:
            sys.exit(1)

    if action in ('all', 'render'):
        video_path = do_render(lesson, size)
        if video_path is None:
            sys.exit(1)

    print(f"\nPipeline执行成功: {lesson}")


# ─── main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Video Pipeline - 自然语言一键生成短视频',
        epilog='示例:\n'
               '  python pipeline.py "帮我做一个零售业AI智能推荐的短视频"\n'
               '  python pipeline.py "医疗AI如何改变诊断" --size 1920x1080\n'
               '  python pipeline.py --lesson 1 --action all',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'natural_language', nargs='?',
        help='自然语言描述，例如: "帮我做一个零售业AI智能推荐的短视频"',
    )
    parser.add_argument('--lesson', type=int, help='课程编号 (传统模式)')
    parser.add_argument(
        '--action', default='all',
        choices=['all', 'gen_html', 'gen_compositions', 'render'],
        help='执行动作 (传统模式)',
    )
    parser.add_argument(
        '--size', default='1080x1920',
        help='视频尺寸, 如 1080x1920(竖屏) 1920x1080(横屏)',
    )
    args = parser.parse_args()

    if args.natural_language:
        run_natural_language_pipeline(args.natural_language, args.size)
    elif args.lesson is not None:
        run_legacy_pipeline(args.lesson, args.action, args.size)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
