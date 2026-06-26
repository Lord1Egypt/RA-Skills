#!/usr/bin/env python3
"""
English Tutor · 环境检测脚本

【安全说明】
本脚本的 subprocess 调用均为"只读诊断"用途：
  - 检测 ffmpeg / piper / espeak-ng 是否安装（仅读版本号）
  - 不执行任何用户输入的参数拼接
  - 不写磁盘、不发网络请求（pip install 是用户主动操作的提示，非自动执行）
  - 用途：帮助用户在安装 skill 前检查环境是否就绪
"""
import sys, subprocess, os, shutil

GREEN  = '\033[92m'
RED    = '\033[91m'
YELLOW = '\033[93m'
RESET  = '\033[0m'

def run(cmd, timeout=10):
    """运行外部命令，cmd 为列表，无 shell=True"""
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        return r.returncode == 0, r.stdout + r.stderr
    except Exception as e:
        return False, str(e)

def can_import(mod):
    try:
        __import__(mod)
        return True
    except ImportError:
        return False

def check(name, ok, detail=''):
    if ok:
        print(f'{GREEN}✅{RESET} {name}{detail}')
        return True
    else:
        print(f'{RED}❌{RESET} {name}{detail}')
        return False

def warn(name, detail=''):
    print(f'{YELLOW}⚠️{RESET} {name}{detail}')

# ─── 检测开始 ───────────────────────────────────────────────
print('='*52)
print('English Tutor · 环境检测')
print('='*52)
print()

issues = []

print('【系统环境】')
check('Python 3.11+',    sys.version_info >= (3, 11))
check('ffmpeg',          run(['ffmpeg', '-version'])[0])
check('curl',            run(['curl', '--version'])[0])
print()

print('【Python 依赖】')
for mod in ['sherpa_onnx', 'numpy']:
    check(f'{mod}', can_import(mod))
print()

print('【ASR 方案】')
model_dir = os.environ.get('SENSE_VOICE_MODEL_DIR',
    os.path.join(os.path.expanduser('~'), '.local', 'share', 'sense-voice-model'))
model_ok  = os.path.exists(os.path.join(model_dir, 'model.onnx'))
tokens_ok = os.path.exists(os.path.join(model_dir, 'tokens.txt'))
if model_ok and tokens_ok:
    sz = os.path.getsize(os.path.join(model_dir, 'model.onnx')) / 1024**2
    check(f'本地 SenseVoice 模型（{sz:.0f}MB）', True)
else:
    check('本地模型', False, ' → 运行 python3 scripts/download_model.py')
    issues.append('asr')

if can_import('sherpa_onnx'):
    check('sherpa-onnx 已安装', True)
else:
    check('sherpa-onnx', False, ' → pip install --user --break-system-packages numpy sherpa-onnx')
    issues.append('dep')
print()

print('【TTS 方案】')
tts_provider = os.environ.get('TTS_PROVIDER', '').lower()
has_tts = False

# ── piper（需完整安装：主程序 + ONNX Runtime + 语音模型）───
piper_bin = os.environ.get('PIPER_BIN', '') or shutil.which('piper_phonemize') or '/tmp/piper/piper_phonemize'
piper_model = os.environ.get('PIPER_MODEL', '')
piper_run_ok = False
if os.path.exists(piper_bin):
    env = os.environ.copy()
    lib_dir = os.path.dirname(piper_bin)
    env['LD_LIBRARY_PATH'] = lib_dir + ('' if not env.get('LD_LIBRARY_PATH') else ':' + env['LD_LIBRARY_PATH'])
    r = subprocess.run([piper_bin, '--version'], capture_output=True, timeout=5, env=env)
    piper_run_ok = r.returncode == 0

if piper_run_ok:
    check(f'piper（可运行）', True, f' · 二进制: {piper_bin}')
    if piper_model:
        check(f'  模型: {piper_model}', os.path.exists(piper_model))
    else:
        warn('  piper 模型', ' → 设置 PIPER_MODEL 环境变量')
    has_tts = True
else:
    warn('piper', f' → 需完整安装（主程序 + ONNX Runtime + 语音模型）')
    warn('  参考', ' → SKILL.md「方案 A1：piper」章节')

# ── espeak-ng ──
espeak_bin = shutil.which('espeak-ng')
espeak_ok = espeak_bin and run([espeak_bin, '--version'])[0]
if espeak_ok:
    check('espeak-ng（系统级）', True)
    has_tts = True
else:
    warn('espeak-ng', ' → 需 root: sudo apt-get install espeak-ng')

# ── MiniMax ──
minimax_key = os.environ.get('MINIMAX_API_KEY', '')
if minimax_key:
    check('MiniMax TTS', True, f'（****{minimax_key[-4:]}）')
    has_tts = True
elif tts_provider == 'minimax':
    check('MiniMax TTS', False, ' → 需配置 MINIMAX_API_KEY')
    issues.append('tts')

# ── OpenAI ──
if tts_provider == 'openai':
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    if openai_key:
        check('OpenAI TTS', True)
        has_tts = True
    else:
        check('OpenAI TTS', False, ' → 需配置 OPENAI_API_KEY')
        issues.append('tts')

# ── Azure ──
if tts_provider == 'azure':
    azure_key = os.environ.get('AZURE_SPEECH_KEY', '')
    if azure_key:
        check('Azure TTS', True)
        has_tts = True
    else:
        check('Azure TTS', False, ' → 需配置 AZURE_SPEECH_KEY')
        issues.append('tts')

if not has_tts:
    warn('当前无可用的 TTS 方案', ' → 请安装上述任一方案')

print()
print('【非必填项】')
for var, desc in [
    ('BITABLE_APP_TOKEN',     '飞书多维表格 App Token'),
    ('BITABLE_WORDS_TABLE_ID','words 表 ID'),
    ('BITABLE_CHAT_TABLE_ID', 'chat_log 表 ID'),
]:
    if os.environ.get(var):
        check(f'{var}', True, f' · {desc}')
    else:
        check(f'{var}', False, f' · {desc}（可选）')
print()

# ─── 总结 ───────────────────────────────────────────────
print('─'*52)
critical = {'asr', 'dep', 'tts'} & set(issues)
if not critical:
    msg = f'{GREEN}✅ 环境检测全部通过！{"TTS 未配置（可选）" if not has_tts else ""}{RESET}'
    print(msg.strip())
    sys.exit(0)
else:
    names = {'asr': 'ASR 方案', 'tts': 'TTS 方案', 'dep': 'Python 依赖'}
    print(f'{RED}❌ 需要修复:{" / ".join(names[i] for i in critical)}{RESET}')
    print()
    print('修复建议:')
    if 'asr' in critical:
        print('  • python3 scripts/download_model.py')
    if 'dep' in critical:
        print('  • pip install --user --break-system-packages numpy sherpa-onnx')
    if 'tts' in critical:
        print('  • 配置 TTS_PROVIDER (piper / espeak / minimax / openai / azure)')
        print('  • 填入对应 API_KEY 环境变量')
        print('  • 参考 SKILL.md 安装本地 TTS（piper / espeak-ng）')
    sys.exit(1)
