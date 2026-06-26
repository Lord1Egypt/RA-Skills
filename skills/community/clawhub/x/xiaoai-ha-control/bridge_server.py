#!/usr/bin/env python3
import json
import os
import subprocess
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

HOST = '0.0.0.0'
PORT = 8765
BASE_DIR = Path(__file__).resolve().parent
BASE_DIR.mkdir(parents=True, exist_ok=True)
LAST_FILE = BASE_DIR / 'xiaoai_to_butler_last_message.txt'
REPLY_FILE = BASE_DIR / 'xiaoai_to_butler_reply.txt'
ERROR_FILE = BASE_DIR / 'xiaoai_to_butler_error.txt'
RAW_FILE = BASE_DIR / 'ha_conversation_content.txt'
STATUS_FILE = BASE_DIR / 'status.json'
REQUEST_LOG = BASE_DIR / 'requests.log'
OPENCLAW_BIN = os.environ.get('OPENCLAW_BIN', 'openclaw')
XIAOAI_BIN = BASE_DIR / 'scripts' / 'xiaoai.sh'
OPENCLAW_TIMEOUT = 180
XIAOAI_TIMEOUT = 60

# Default constants (used as fallback when whitelist.json is not present)
_DEFAULT_MAX_SPOKEN_LEN = 60
_DEFAULT_DEDUP_WINDOW_SEC = 10
_DEFAULT_QUESTION_MARKERS = ['吗', '呢', '怎么', '怎么样', '如何', '几点', '多少', '有没有', '是否', '什么', '问', '问下', '问一下', '问问', '？', '?']
_DEFAULT_BRIDGE_WHITELIST_TARGETS = ['管家', '研究员', '邮差', '码农', '产品', '运维', '教练', '运营', 'QQ小助手', 'QQ助手']
_DEFAULT_BRIDGE_WHITELIST_VERBS = ['让', '转告', '发给', '发送给', '告诉', '交给', '通知', '转达', '传达', '帮我通知', '帮我转告', '帮我告诉', '帮我问下', '问一下', '问下', '帮我问问', '去问问', '帮我发给', '帮我发送给', '帮我转达给', '帮我传达给']
_DEFAULT_SUBAGENT_TARGETS = ['研究员', '邮差', '码农', '产品', '运维', '教练', '运营', 'QQ小助手', 'QQ助手']

# Load whitelist config (user-customizable via whitelist.json)
_WHITELIST_FILE = BASE_DIR / 'whitelist.json'


def _load_whitelist() -> dict:
    if _WHITELIST_FILE.exists():
        try:
            return json.loads(_WHITELIST_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {}


def _get(cfg: dict, key: str, default: Any) -> Any:
    val = cfg.get(key)
    return val if val is not None else default


_cfg = _load_whitelist()
MAX_SPOKEN_LEN = _get(_cfg, 'max_spoken_len', _DEFAULT_MAX_SPOKEN_LEN)
DEDUP_WINDOW_SEC = _get(_cfg, 'dedup_window_sec', _DEFAULT_DEDUP_WINDOW_SEC)
BRIDGE_AUTO_SAY_ENABLED = _get(_cfg, 'bridge_auto_say_enabled', False)
QUESTION_MARKERS = _get(_cfg, 'question_markers', _DEFAULT_QUESTION_MARKERS)
BRIDGE_WHITELIST_TARGETS = _get(_cfg, 'whitelist_targets', _DEFAULT_BRIDGE_WHITELIST_TARGETS)
BRIDGE_WHITELIST_VERBS = _get(_cfg, 'whitelist_verbs', _DEFAULT_BRIDGE_WHITELIST_VERBS)
SUBAGENT_TARGETS = _get(_cfg, 'subagent_targets', _DEFAULT_SUBAGENT_TARGETS)



def now_str() -> str:
    return datetime.now().isoformat(timespec='seconds')


def ensure_debug_files() -> None:
    for path in [LAST_FILE, REPLY_FILE, ERROR_FILE, RAW_FILE, STATUS_FILE, REQUEST_LOG]:
        if not path.exists():
            path.write_text('' if path != STATUS_FILE else '{}', encoding='utf-8')


def append_log(line: str) -> None:
    REQUEST_LOG.open('a', encoding='utf-8').write(line + '\n')


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def write_status(**patch: Any) -> None:
    data = {
        'service': 'xiaoai-ha-control-bridge',
        'host': HOST,
        'port': PORT,
        'healthy': True,
        'last_text': '',
        'reply': '',
        'spoken': '',
        'error': '',
        'forwarded': False,
        'last_request_at': '',
        'last_worker_at': '',
        'updated_at': now_str(),
    }
    data.update(read_json(STATUS_FILE))
    data.update(patch)
    data['updated_at'] = now_str()
    STATUS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def save_error(err: str) -> None:
    ERROR_FILE.write_text(err or '', encoding='utf-8')


def save_reply(reply: str) -> None:
    REPLY_FILE.write_text(reply or '', encoding='utf-8')


def extract_final_reply(stdout: str) -> str:
    ignored = {'NO_REPLY', 'completed', 'done', 'success', 'ok'}
    lines = [line.strip() for line in (stdout or '').splitlines() if line.strip()]
    if not lines:
        return ''
    for line in reversed(lines):
        if line.lower() not in ignored:
            return line
    return ''


def is_question_text(text: str) -> bool:
    return any(marker in text for marker in QUESTION_MARKERS)


def normalize_text(text: str) -> str:
    return (
        (text or '')
        .strip()
        .replace('，', '')
        .replace('。', '')
        .replace('？', '')
        .replace('?', '')
        .replace('！', '')
        .replace('!', '')
        .replace(' ', '')
    )


def detect_named_subagent(text: str) -> str:
    normalized = normalize_text(text)
    for target in SUBAGENT_TARGETS:
        if target in normalized:
            return target
    return ''


def should_forward_to_openclaw(text: str, source: str) -> tuple[bool, str, str]:
    normalized = normalize_text(text)
    if not normalized:
        return False, 'empty_text', ''

    matched_subagent = detect_named_subagent(text)

    if source != 'xiaoai-speaker':
        return True, 'non_xiaoai_source', matched_subagent

    has_target = any(target in normalized for target in BRIDGE_WHITELIST_TARGETS)
    has_verb = any(verb in normalized for verb in BRIDGE_WHITELIST_VERBS)
    direct_target = any(normalized.startswith(target) for target in BRIDGE_WHITELIST_TARGETS)

    if has_target and (has_verb or direct_target):
        return True, 'matched_bridge_whitelist', matched_subagent

    return False, 'not_in_bridge_whitelist', matched_subagent


def normalize_spoken(user_text: str, assistant_reply: str) -> str:
    assistant_reply = (assistant_reply or '').strip()
    normalized_user = normalize_text(user_text)

    handoff_markers = ['正在帮你问', '正在帮你查', '正在帮你看', '已收到，正在帮你']
    if assistant_reply and any(marker in assistant_reply for marker in handoff_markers):
        return assistant_reply

    if is_question_text(user_text) and assistant_reply and len(assistant_reply) <= MAX_SPOKEN_LEN:
        return assistant_reply

    if any(marker in normalized_user for marker in ['问', '问下', '问一下', '问问']) and assistant_reply and len(assistant_reply) <= MAX_SPOKEN_LEN:
        return assistant_reply

    return '管家已处理完成，结果已发到聊天里。'


def build_prompt(text: str, source: str, matched_subagent: str) -> str:
    subagent_hint = ''
    if matched_subagent:
        subagent_hint = (
            f'命中目标子 agent：{matched_subagent}。'
            '若该消息带小爱来源标识且文本中明确点名了该子 agent，main 必须将任务分配给对应子 agent；'
            '子 agent 完成后结果必须先回到 main，再由 main 统一负责聊天回复与小爱口播。'
        )

    return (
        f"【来自小爱语音】\n消息来源：{source}\n用户原话：{text}\n\n"
        '这是来自小爱音箱/语音桥的上行请求。'
        '请优先按“来源是小爱”的语义来理解，而不是按普通聊天消息理解。'
        '如果原话中出现“告诉小爱同学”“让小爱”这类说法，先判断是否只是口语包壳或自指表达，必要时做语义纠偏后再处理。'
        + subagent_hint +
        '请按 AGENTS.md 中的小爱语音桥处理规则执行：'
        '由管家统一调度，必要时分配给子 agent；'
        '聊天窗口保留完整结果；'
        '若需要语音回播，请按 AGENTS.md 中的长期规则执行。'
        '不要输出 markdown，不要分点，不要带多余解释。'
    )


def run_openclaw(prompt: str) -> tuple[str, str, int]:
    proc = subprocess.run(
        [OPENCLAW_BIN, 'agent', '--agent', 'main', '--message', prompt],
        capture_output=True,
        text=True,
        timeout=OPENCLAW_TIMEOUT,
    )
    return (proc.stdout or '').strip(), (proc.stderr or '').strip(), proc.returncode



def speak_reply(spoken: str) -> tuple[str, int]:
    proc = subprocess.run(
        ['bash', XIAOAI_BIN, 'say', spoken],
        capture_output=True,
        text=True,
        timeout=XIAOAI_TIMEOUT,
    )
    return (proc.stderr or '').strip(), proc.returncode


_seen_lock = threading.Lock()
_seen: dict[str, float] = {}  # normalized_text -> last seen timestamp


def worker(text: str, source: str, matched_subagent: str, immediate_reply: str, request_at: str) -> None:
    normalized = normalize_text(text)
    skip_speak = False
    with _seen_lock:
        last_ts = _seen.get(normalized, 0.0)
        if normalized and (time.time() - last_ts) < DEDUP_WINDOW_SEC:
            skip_speak = True
        else:
            _seen[normalized] = time.time()

    try:
        stdout, stderr, returncode = run_openclaw(build_prompt(text, source, matched_subagent))
        final_reply = extract_final_reply(stdout)
        spoken = normalize_spoken(text, final_reply)

        bridge_say_executed = False
        say_stderr = ''
        say_returncode = 0

        if skip_speak:
            append_log(f'[{now_str()}] DEDUP_SKIP text={text!r}')
        elif BRIDGE_AUTO_SAY_ENABLED:
            say_stderr, say_returncode = speak_reply(spoken)
            bridge_say_executed = True

        errors = []
        healthy = True
        if returncode != 0:
            errors.append(f'openclaw_exit={returncode}')
            healthy = False
        if stderr:
            errors.append(stderr)
        if bridge_say_executed and say_returncode != 0:
            errors.append(f'xiaoai_say_exit={say_returncode}')
            healthy = False
        if bridge_say_executed and say_stderr:
            errors.append(say_stderr)

        error_text = '\n'.join(part for part in errors if part).strip()
        save_reply(final_reply or immediate_reply)
        save_error(error_text)
        write_status(
            healthy=healthy,
            last_text=text,
            reply=final_reply or immediate_reply,
            spoken=spoken,
            bridge_auto_say=BRIDGE_AUTO_SAY_ENABLED,
            bridge_say_executed=bridge_say_executed,
            error=error_text,
            forwarded=True,
            last_request_at=request_at,
            last_worker_at=now_str(),
        )
        append_log(
            f"[{now_str()}] WORKER_DONE "
            f"final_reply={final_reply!r} spoken={spoken!r} "
            f"bridge_auto_say={BRIDGE_AUTO_SAY_ENABLED} "
            f"bridge_say_executed={bridge_say_executed} "
            f"healthy={healthy} openclaw_exit={returncode}"
        )
    except Exception as e:
        err = f'{type(e).__name__}: {e}'
        save_error(err)
        save_reply(immediate_reply)
        write_status(
            healthy=False,
            last_text=text,
            reply=immediate_reply,
            spoken='',
            bridge_auto_say=BRIDGE_AUTO_SAY_ENABLED,
            bridge_say_executed=False,
            error=err,
            forwarded=True,
            last_request_at=request_at,
            last_worker_at=now_str(),
        )
        append_log(f'[{now_str()}] WORKER_EXCEPTION error={err!r}')


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == '/health':
            status = read_json(STATUS_FILE)
            if not status:
                status = {
                    'service': 'xiaoai-ha-control-bridge',
                    'healthy': True,
                    'updated_at': now_str(),
                }
            self._send(200, {'ok': True, 'status': status})
            return
        self._send(404, {'ok': False, 'error': 'not_found'})

    def do_POST(self) -> None:
        if self.path != '/xiaoai-to-butler':
            self._send(404, {'ok': False, 'error': 'not_found'})
            return

        request_at = now_str()
        try:
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length) if length > 0 else b'{}'
            payload = json.loads(body.decode('utf-8') or '{}')
            text = str(payload.get('text', '')).strip()
            source = str(payload.get('source', 'xiaoai-speaker')).strip() or 'xiaoai-speaker'

            append_log(f'[{request_at}] RECEIVED source={source!r} text={text!r}')
            RAW_FILE.write_text(text, encoding='utf-8')
            LAST_FILE.write_text(text, encoding='utf-8')
            save_error('')
            write_status(
                healthy=True,
                last_text=text,
                reply='',
                spoken='',
                error='',
                forwarded=False,
                last_request_at=request_at,
            )

            allowed, reason, matched_subagent = should_forward_to_openclaw(text, source)
            if not allowed:
                reply = '这条内容保留给小爱原生处理。'
                save_reply(reply)
                save_error(reason)
                write_status(
                    healthy=True,
                    last_text=text,
                    reply=reply,
                    spoken='',
                    error=reason,
                    forwarded=False,
                    last_request_at=request_at,
                )
                append_log(f'[{request_at}] DROP source={source!r} reason={reason!r} matched_subagent={matched_subagent!r} text={text!r}')
                self._send(200, {'ok': True, 'reply': reply, 'forwarded': False, 'reason': reason})
                return

            immediate_reply = '已转告管家。'
            save_reply(immediate_reply)
            write_status(
                healthy=True,
                last_text=text,
                reply=immediate_reply,
                spoken='',
                error='',
                forwarded=True,
                last_request_at=request_at,
            )
            append_log(f'[{request_at}] FORWARDED immediate_reply={immediate_reply!r} matched_subagent={matched_subagent!r}')

            threading.Thread(target=worker, args=(text, source, matched_subagent, immediate_reply, request_at), daemon=True).start()
            self._send(200, {'ok': True, 'reply': immediate_reply})

        except Exception as e:
            err = f'{type(e).__name__}: {e}'
            save_error(err)
            save_reply('转告管家失败，请稍后再试。')
            write_status(
                healthy=False,
                last_text='',
                reply='转告管家失败，请稍后再试。',
                spoken='',
                error=err,
                forwarded=False,
                last_request_at=request_at,
            )
            append_log(f'[{request_at}] REQUEST_EXCEPTION error={err!r}')
            self._send(500, {'ok': False, 'reply': '转告管家失败，请稍后再试。', 'error': err})

    def log_message(self, format: str, *args) -> None:
        return


def daemonize() -> None:
    """Fork the process to run in background (Unix only)."""
    try:
        pid = os.fork()
        if pid > 0:
            # Parent exits
            print(f'Bridge started in background, PID={pid}', file=sys.stdout)
            sys.exit(0)
    except OSError as e:
        print(f'Fork failed: {e}', file=sys.stderr)
        sys.exit(1)
    # Child continues in new session
    os.chdir('/')
    os.setsid()
    os.umask(0)


if __name__ == '__main__':
    import sys

    daemon = '--daemon' in sys.argv
    if daemon:
        daemonize()

    ensure_debug_files()
    cfg_source = 'whitelist.json' if _WHITELIST_FILE.exists() else 'builtin_defaults'
    append_log(f'[{now_str()}] SERVER_START host={HOST} port={PORT} daemon={daemon} whitelist={cfg_source}')
    write_status()
    server = HTTPServer((HOST, PORT), Handler)
    server.serve_forever()
