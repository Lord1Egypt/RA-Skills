#!/usr/bin/env bash
# reply_with_claude.sh — telegram_listener.py --on-message hook for plain
# human DMs to a BYOB duck's Telegram bot.
#
# WHY THIS EXISTS: peck_responder.py only handles duck-to-duck peck envelopes
# (it hard-requires peck_id + sender_spaceduck_id and drops anything else).
# A human DM ("hey") carries neither, so it was silently dropped. This is the
# hook SKILL.md always referenced but nobody had written.
#
# CRITICAL — ASYNC BY DESIGN: the Lambda's forward to your tunnel has a hard
# 10s urlopen timeout (lambda_function.py:15633), and the listener runs this
# hook synchronously before answering. A `claude` turn takes far longer than
# 10s, so a synchronous reply would trip that timeout every message and flap
# the binding to DEGRADED. Therefore this hook RETURNS IMMEDIATELY and sends
# the reply from a detached background worker via tg_send.py.
#
# WIRING (note: NO --auto-reply — this hook sends its own reply):
#   python3 scripts/telegram_listener.py \
#       --on-message "$(pwd)/scripts/reply_with_claude.sh" \
#       --owner-approval --verbose
#
# BRAIN RESOLUTION — TWO STAGES (native Lane A first, portable chain second):
#
#   Stage 1 — NATIVE Lane A brain (the duck's OWN agent: openclaw today, or
#   whatever agent it runs now / a future agent not yet built). This brain owns
#   its own rules, memory, tools, auto-respond and approval logic — the hook
#   DELEGATES to it, it does not second-guess it. The native brain is tried
#   FIRST and exhausted before any fallback. A native brain that cannot handle
#   the message signals "no capacity" by printing the reserved sentinel
#   __NO_CAPACITY__ (or exiting non-zero / empty / timing out); the hook then
#   falls through to Stage 2.
#       SPACEDUCK_NATIVE_BRAIN_CMD  explicit native brain command. Unset →
#                                   auto-detect a local `openclaw` agent; if no
#                                   openclaw on PATH, Stage 1 is skipped.
#
#   Stage 2 — PORTABLE fallback chain (only if Stage 1 declined). An ordered
#   list of opaque brain commands, tried in order; first that returns wins.
#   Contract for every brain (native and chain): the full composed prompt
#   arrives on STDIN, the reply text is printed to STDOUT, exit 0. Brains are
#   opaque commands — no model-name concept, no provider SDK. A future agent
#   works the day it ships by being named in one of these knobs.
#       SPACEDUCK_BRAIN_CMD    single brain (back-compat shorthand; tried first
#                              in the chain). Wrap any provider:
#                                'python3 /opt/brain_openai.py' | 'ollama run llama3'
#       SPACEDUCK_BRAIN_CHAIN  ordered brains separated by ||| , e.g.
#                                'python3 /opt/openrouter.py|||ollama run llama3'
#   Effective chain = [BRAIN_CMD] + BRAIN_CHAIN entries + [local claude CLI],
#   de-duplicated, order preserved. All exhausted → send nothing.
#
# ENV KNOBS (shared with peck_responder.py for consistency):
#   SPACEDUCK_NATIVE_BRAIN_CMD   Stage-1 native brain (stdin->reply, exit 0).
#                                Unset → skip to Stage 2. For openclaw, point it
#                                at a wrapper running `openclaw agent --local
#                                --json -m "$(cat)"` (openclaw takes -m, not stdin).
#   SPACEDUCK_BRAIN_CMD          Stage-2 single brain (first chain link).
#   SPACEDUCK_BRAIN_CHAIN        Stage-2 |||-separated brain list.
#   SPACEDUCK_RESPONDER_MODEL    default: claude-sonnet-4-6 (claude CLI link only)
#   SPACEDUCK_RESPONDER_TIMEOUT  default: 90 (seconds, per brain attempt)
#   SPACEDUCK_REPLY_MAX_ROUNDS   loop guard: max auto-replies per chat inside a
#                                rolling 120s window (default 6, 0 = uncapped).
#                                Mirrors peck_responder's max_rounds rotation cap
#                                so two bots / a repetitive human cannot pin the
#                                brain in an endless auto-reply loop.
#   SPACEDUCK_REPLY_DISABLED     owner sign-out / kill-switch: 1 = answer
#                                nothing. Also honored via config.json
#                                {"auto_reply_enabled": false} or the presence
#                                of ~/.space-duck/REPLIES_OFF. A payload whose
#                                _binding_state is REVOKED is also dropped.
#   SPACEDUCK_RESPONDER_LOG      default: ~/.space-duck/responder.log
#   SPACEDUCK_RESPONDER_DRY      dry-run: compose + log, send nothing
#
# SAFETY GUARDS (default = answer the owner only, in private chats, never bots):
#   SPACEDUCK_REPLY_ALLOW_CHATS  comma-separated chat-id allowlist. Empty (the
#                                default) = owner-only: the only chat answered
#                                is the owner chat_id resolved from
#                                ~/.space-duck/config.json / forward.json (same
#                                source peck_responder uses). Set a list to
#                                widen, or "*" to answer any chat (public duck).
#                                TRUST TIER: owner + explicitly-named chats are
#                                trusted and get full context (SOUL + MEMORY +
#                                CONNECTIONS). Strangers admitted via "*" are
#                                UNTRUSTED — persona only (SOUL.md), never the
#                                private MEMORY/CONNECTIONS files. Closes the
#                                memory-exfil path for public-facing ducks.
#   SPACEDUCK_REPLY_ALLOW_GROUPS set to 1 to also answer group/supergroup/
#                                channel chats. Default: private chats only.
#   (bot senders — msg.from.is_bot — are always dropped, no knob.)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="${SPACEDUCK_RESPONDER_LOG:-$HOME/.space-duck/responder.log}"

# Slurp the forward JSON the listener pipes to us, then hand it to a detached
# worker via env (not stdin — the backgrounded heredoc owns this process'
# stdin). Return in milliseconds so the Lambda's 10s timeout never trips.
payload="$(cat)"

SD_PAYLOAD="$payload" SD_SCRIPT_DIR="$SCRIPT_DIR" \
SPACEDUCK_NATIVE_BRAIN_CMD="${SPACEDUCK_NATIVE_BRAIN_CMD:-}" \
SPACEDUCK_BRAIN_CMD="${SPACEDUCK_BRAIN_CMD:-}" \
SPACEDUCK_BRAIN_CHAIN="${SPACEDUCK_BRAIN_CHAIN:-}" \
SPACEDUCK_RESPONDER_MODEL="${SPACEDUCK_RESPONDER_MODEL:-claude-sonnet-4-6}" \
SPACEDUCK_RESPONDER_TIMEOUT="${SPACEDUCK_RESPONDER_TIMEOUT:-90}" \
SPACEDUCK_REPLY_MAX_ROUNDS="${SPACEDUCK_REPLY_MAX_ROUNDS:-6}" \
SPACEDUCK_REPLY_DISABLED="${SPACEDUCK_REPLY_DISABLED:-}" \
SPACEDUCK_RESPONDER_LOG="$LOG" \
SPACEDUCK_RESPONDER_DRY="${SPACEDUCK_RESPONDER_DRY:-}" \
SPACEDUCK_REPLY_ALLOW_CHATS="${SPACEDUCK_REPLY_ALLOW_CHATS:-}" \
SPACEDUCK_REPLY_ALLOW_GROUPS="${SPACEDUCK_REPLY_ALLOW_GROUPS:-}" \
nohup python3 - >>"$LOG" 2>&1 <<'PY' &
import json, os, re, shlex, shutil, subprocess, sys, time
from pathlib import Path

SD_DIR      = Path.home() / '.space-duck'
SCRIPT_DIR  = Path(os.environ['SD_SCRIPT_DIR'])
MODEL       = os.environ.get('SPACEDUCK_RESPONDER_MODEL', 'claude-sonnet-4-6')

# 2026-09-02 — same two failure modes the peck responder hits under
# supervision: (1) minimal PATH hides a user-local claude, (2) an inherited
# cwd whose directory has since been deleted makes the claude CLI exit 1
# ("current working directory was deleted") before it reads a byte of prompt.
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from _claudebin import resolve_claude, safe_cwd, ensure_cwd
except Exception:
    def resolve_claude():
        return 'claude'

    def safe_cwd():
        return os.path.expanduser('~')

    def ensure_cwd():
        try:
            return os.getcwd()
        except Exception:
            d = os.path.expanduser('~')
            try:
                os.chdir(d)
            except Exception:
                pass
            return d
ensure_cwd()
SAFE_CWD = safe_cwd()
def _envint(name, default):
    try:
        return int(str(os.environ.get(name, '')).strip() or default)
    except ValueError:
        return default
TIMEOUT     = _envint('SPACEDUCK_RESPONDER_TIMEOUT', 90)
DRY         = os.environ.get('SPACEDUCK_RESPONDER_DRY', '').lower() in ('1', 'true', 'yes')
MAX_ROUNDS  = _envint('SPACEDUCK_REPLY_MAX_ROUNDS', 6)
NO_CAPACITY = '__NO_CAPACITY__'   # native brain prints this to decline → fall through
ROUNDS_WINDOW = 120               # seconds; rolling window for the loop guard


def log(msg):
    sys.stderr.write(f'[{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}] reply_with_claude: {msg}\n')


def load_md(name):
    p = SD_DIR / name
    if p.is_file():
        try:
            return p.read_text()[:6000]
        except Exception:
            return ''
    return ''


def replies_disabled():
    """Owner sign-out / kill-switch. Any of these silences auto-reply without
    tearing down the binding:
      • env SPACEDUCK_REPLY_DISABLED in (1/true/yes)
      • ~/.space-duck/REPLIES_OFF sentinel file present
      • config.json {"auto_reply_enabled": false}
    """
    if os.environ.get('SPACEDUCK_REPLY_DISABLED', '').lower() in ('1', 'true', 'yes'):
        return 'env SPACEDUCK_REPLY_DISABLED'
    if (SD_DIR / 'REPLIES_OFF').exists():
        return '~/.space-duck/REPLIES_OFF present'
    cfg_p = SD_DIR / 'config.json'
    if cfg_p.is_file():
        try:
            if json.loads(cfg_p.read_text()).get('auto_reply_enabled') is False:
                return 'config.json auto_reply_enabled=false'
        except Exception:
            pass
    return ''


try:
    payload = json.loads(os.environ['SD_PAYLOAD'])
except Exception as e:
    log(f'bad payload: {e}')
    sys.exit(0)

# Stage 0a — owner sign-out / kill-switch.
_off = replies_disabled()
if _off:
    log(f'auto-reply disabled ({_off}) — drop')
    sys.exit(0)

# Stage 0b — binding revoked. The platform stops forwarding once a duck is
# REVOKED, so this rarely fires from the forward path, but honor it defensively
# if the listener stamped the state into the payload.
_bind_state = str(payload.get('_binding_state') or payload.get('binding_state') or '').upper()
if _bind_state == 'REVOKED':
    log('binding REVOKED — owner signed the duck out, drop')
    sys.exit(0)

tg   = payload.get('telegram_update', {}) or {}
msg  = tg.get('message') or {}
text = (msg.get('text') or '').strip()
chat = msg.get('chat') or {}
chat_id = chat.get('id')
chat_type = (chat.get('type') or '').lower()
frm = msg.get('from') or {}
reply_to = msg.get('message_id')
sender = (frm.get('first_name') or frm.get('username') or 'a user')

# Only handle plain text DMs. No text (sticker / photo / service msg) → drop.
if not text or chat_id in (None, ''):
    log(f'no usable text (chat={chat_id!r}) — drop')
    sys.exit(0)


def resolve_owner_chat():
    """Owner chat_id — mirrors peck_responder._notify_owner_silent_skip
    resolution order exactly:
      1. forward.json -> .telegram.chat_id  (preferred, nested)
      2. config.json  -> owner_chat_id | telegram_chat_id  (top-level)
      3. env SPACEDUCK_FWD_TG_CHAT
    """
    fwd = SD_DIR / 'forward.json'
    if fwd.is_file():
        try:
            tg = (json.loads(fwd.read_text()).get('telegram') or {})
            v = str(tg.get('chat_id') or '').strip()
            if v:
                return v
        except Exception:
            pass
    cfg_p = SD_DIR / 'config.json'
    if cfg_p.is_file():
        try:
            cfg = json.loads(cfg_p.read_text())
            v = str(cfg.get('owner_chat_id') or cfg.get('telegram_chat_id') or '').strip()
            if v:
                return v
        except Exception:
            pass
    return os.environ.get('SPACEDUCK_FWD_TG_CHAT', '').strip()


# Guard 1 — bot senders are never answered (avoids duck↔bot reply loops).
if frm.get('is_bot'):
    log(f'sender is_bot (chat={chat_id!r}) — drop')
    sys.exit(0)

# Guard 2 — chat-type gate. Private only unless groups explicitly allowed.
allow_groups = os.environ.get('SPACEDUCK_REPLY_ALLOW_GROUPS', '').lower() in ('1', 'true', 'yes')
if chat_type and chat_type != 'private' and not allow_groups:
    log(f'non-private chat type={chat_type!r} (chat={chat_id!r}) — drop (set SPACEDUCK_REPLY_ALLOW_GROUPS=1 to allow)')
    sys.exit(0)

# Guard 3 — chat allowlist + trust tier.
# `trusted` = owner or an explicitly-named allowlist chat. '*' (public) admits
# strangers but they are NOT trusted: they get the persona (SOUL.md) only, never
# the private MEMORY.md / CONNECTIONS.md — closes the memory-exfil path while
# still letting a public-facing duck answer anyone.
owner = resolve_owner_chat()
allow_raw = os.environ.get('SPACEDUCK_REPLY_ALLOW_CHATS', '').strip()
named = {c.strip() for c in allow_raw.split(',') if c.strip() and c.strip() != '*'}
trusted_set = set(named)
if owner:
    trusted_set.add(owner)

if allow_raw == '*':
    pass  # answer any chat (strangers untrusted — persona-only context below)
elif named:
    if str(chat_id) not in trusted_set:
        log(f'chat={chat_id!r} not in allowlist {sorted(trusted_set)!r} — drop')
        sys.exit(0)
else:
    # owner-only mode
    if not owner:
        # Misconfig, not abuse: the duck bound but never recorded an owner
        # chat_id, so it silently ignores everyone and *looks dead*. Drop the
        # message (we can't safely treat an unknown sender as owner), but leave
        # a loud breadcrumb + a dormancy marker a health check / heartbeat can
        # sweep, so this is diagnosable instead of a mystery silence.
        log('DORMANT: owner-only mode but no owner chat_id resolvable from '
            'config.json (owner_chat_id|telegram_chat_id) / forward.json '
            '(.telegram.chat_id) / env SPACEDUCK_FWD_TG_CHAT — ignoring ALL '
            'inbound. Set one, or SPACEDUCK_REPLY_ALLOW_CHATS, to recover.')
        try:
            (SD_DIR / 'DORMANT_NO_OWNER').write_text(
                json.dumps({'since': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                            'reason': 'owner-only mode, no owner chat_id resolvable',
                            'last_seen_chat_id': chat_id}))
        except Exception:
            pass
        sys.exit(0)
    # Owner is configured — clear any stale dormancy marker.
    try:
        (SD_DIR / 'DORMANT_NO_OWNER').unlink()
    except Exception:
        pass
    if str(chat_id) != owner:
        log(f'chat={chat_id!r} not owner ({owner!r}) — drop')
        sys.exit(0)

trusted = str(chat_id) in trusted_set

# Stage 0c — loop / rotation cap. Mirrors peck_responder's max_rounds idea for
# plain DMs: count auto-replies per chat in a rolling window. A repetitive human
# or a bot-to-bot ping-pong cannot pin the brain in an endless reply loop. The
# Jaccard novelty check folds a near-duplicate inbound into the same window so
# "stuck" repeats burn the budget faster.
def _tokens(s):
    return set(re.findall(r'[a-z0-9]+', (s or '').lower()))

def _jaccard(a, b):
    if not a and not b:
        return 1.0
    u = a | b
    return (len(a & b) / len(u)) if u else 0.0

def rotation_blocked():
    if MAX_ROUNDS <= 0:
        return False
    rd = SD_DIR / 'reply_rounds'
    try:
        rd.mkdir(parents=True, exist_ok=True)
    except Exception:
        return False  # cannot track → fail open (never block a real reply on IO)
    safe = re.sub(r'[^0-9A-Za-z_-]', '_', str(chat_id))
    f = rd / (safe + '.json')
    # Serialize the read-modify-write per chat so concurrent forwards from one
    # chat can't read-before-write and overshoot the cap. flock held across the
    # whole critical section; released on close.
    lockf = rd / (safe + '.lock')
    lock_fh = None
    try:
        import fcntl
        lock_fh = open(lockf, 'w')
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
    except Exception:
        lock_fh = None  # no fcntl (rare) → proceed unlocked, still fail-open
    try:
        now = time.time()
        st = {'window_start': now, 'count': 0, 'last_text': ''}
        if f.is_file():
            try:
                st = json.loads(f.read_text())
            except Exception:
                pass
        if now - float(st.get('window_start', 0)) > ROUNDS_WINDOW:
            st = {'window_start': now, 'count': 0, 'last_text': ''}
        near_dup = _jaccard(_tokens(text), _tokens(st.get('last_text', ''))) >= 0.9
        if st.get('count', 0) >= MAX_ROUNDS:
            log(f'rotation cap ({MAX_ROUNDS}/{ROUNDS_WINDOW}s) reached for chat={chat_id!r}'
                f'{" [near-dup loop]" if near_dup else ""} — drop')
            return True
        st['count'] = int(st.get('count', 0)) + 1
        st['last_text'] = text
        try:
            f.write_text(json.dumps(st))
        except Exception:
            pass
        return False
    finally:
        if lock_fh is not None:
            try:
                lock_fh.close()
            except Exception:
                pass

if rotation_blocked():
    sys.exit(0)

soul = load_md('SOUL.md')
memory = load_md('MEMORY.md') if trusted else ''
connections = load_md('CONNECTIONS.md') if trusted else ''
if not trusted:
    log(f'untrusted chat={chat_id!r} — persona-only context (no MEMORY/CONNECTIONS)')

parts = []
if soul.strip():
    parts.append('# Who you are (SOUL.md)\n' + soul.strip())
if memory.strip():
    parts.append('# What you remember (MEMORY.md)\n' + memory.strip())
if connections.strip():
    parts.append('# Your Network (CONNECTIONS.md — auto-synced)\n' + connections.strip())
parts.append(
    f'# Incoming Telegram message from {sender}\n'
    f'> {text}\n\n'
    f'Reply as that duck — concise, in-character, factual. '
    f'This is a direct human chat, not a duck-to-duck peck. '
    f'Reply only with the message body — no preamble, no markers.'
)
prompt = '\n\n---\n\n'.join(parts)

# ── Brain resolution: native Lane A first, then portable fallback chain ──
# Every brain obeys the same contract: prompt on stdin, reply on stdout, exit 0.
# run_brain returns (status, value) where status is:
#   'ok'           → value is the reply text
#   'no_capacity'  → native brain declined (sentinel); fall through to chain
#   'fail'         → value is a short reason; try the next brain
def run_brain(cmd, label, allow_sentinel):
    try:
        out = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                             timeout=TIMEOUT, cwd=SAFE_CWD)
    except subprocess.TimeoutExpired:
        return ('fail', f'timeout after {TIMEOUT}s')
    except FileNotFoundError:
        return ('fail', 'not found on PATH')
    except Exception as e:
        return ('fail', str(e)[:200])
    if out.returncode != 0:
        return ('fail', f'exit {out.returncode}: {(out.stderr or "").strip()[:200]}')
    reply = (out.stdout or '').strip()
    if allow_sentinel and reply == NO_CAPACITY:
        return ('no_capacity', 'sentinel __NO_CAPACITY__')
    if not reply:
        return ('fail', 'empty reply')
    return ('ok', reply)


reply = None

# Stage 1 — native Lane A brain (the duck's own agent). It owns its own rules,
# permissions, approval and rotation logic; we delegate and only fall through if
# it has no capacity. Requires the explicit knob — see note below on openclaw.
native_raw = os.environ.get('SPACEDUCK_NATIVE_BRAIN_CMD', '').strip()
native_cmd = None
if native_raw:
    try:
        native_cmd = shlex.split(native_raw)
    except Exception as e:
        log(f'SPACEDUCK_NATIVE_BRAIN_CMD not parseable: {e} — skipping native stage')
elif shutil.which('openclaw'):
    # An openclaw is on PATH but the native invocation is NOT auto-guessable:
    # `openclaw agent` takes the prompt as `-m <text>` (not stdin), and the exact
    # wrapper (agent id, channel, --local vs gateway) is operator-specific.
    # Guessing a command that doesn't read stdin would fail on every message, so
    # log a one-time hint and skip to Stage 2 rather than burn a subprocess.
    log('openclaw on PATH but SPACEDUCK_NATIVE_BRAIN_CMD unset — point it at a '
        'stdin->reply wrapper (e.g. a script running `openclaw agent --local '
        '--json -m "$(cat)"`) to enable the native brain; skipping Stage 1')

if native_cmd:
    label = native_cmd[0]
    status, val = run_brain(native_cmd, label, allow_sentinel=True)
    if status == 'ok':
        reply = val
        log(f'native brain {label!r} answered ({len(reply)} chars)')
    else:
        log(f'native brain {label!r} declined ({val}) — falling through to fallback chain')

# Stage 2 — portable fallback chain. Tried only if Stage 1 produced no reply.
if reply is None:
    chain = []
    bc = os.environ.get('SPACEDUCK_BRAIN_CMD', '').strip()
    if bc:
        chain.append(bc)
    for part in os.environ.get('SPACEDUCK_BRAIN_CHAIN', '').split('|||'):
        part = part.strip()
        if part:
            chain.append(part)
    # de-dup, preserve order
    seen = set()
    chain = [c for c in chain if not (c in seen or seen.add(c))]

    attempts = []
    for raw in chain:
        try:
            cmd = shlex.split(raw)
        except Exception as e:
            log(f"brain {raw!r} not parseable: {e}")
            continue
        if not cmd:
            continue
        attempts.append((cmd, cmd[0]))
    # implicit final link: local claude CLI (zero-config default)
    if not any(a[1] == 'claude' for a in attempts):
        # 0.4.25 — no bypassPermissions: it trips the CLI's root/sudo guard
        # (exit 1 = silent reply death on root installs) and composing a
        # reply needs no tools anyway (same rationale as the 0.4.23
        # peck_responder fix).
        attempts.append(([resolve_claude(), '--print', '--model', MODEL], 'claude'))

    for cmd, label in attempts:
        status, val = run_brain(cmd, label, allow_sentinel=False)
        if status == 'ok':
            reply = val
            log(f'brain {label!r} answered ({len(reply)} chars)')
            break
        log(f'brain {label!r} failed: {val}')

    if reply is None:
        log(f'all {len(attempts)} brains exhausted — no reply')
        sys.exit(0)

if DRY:
    log(f'DRY-RUN would reply to chat={chat_id}: {reply[:200]!r}')
    sys.exit(0)

# Send via the same outbound primitive the skill already uses. sd_id + beak_key
# default from ~/.space-duck/config.json; threaded reply_to keeps the chat tidy.
send_cmd = ['python3', str(SCRIPT_DIR / 'tg_send.py'),
            '--chat-id', str(chat_id), '--text', reply]
if reply_to:
    send_cmd += ['--reply-to', str(reply_to)]
try:
    sres = subprocess.run(send_cmd, capture_output=True, text=True, timeout=20)
    if sres.returncode != 0:
        log(f'tg_send exit {sres.returncode}: {(sres.stderr or sres.stdout or "").strip()[:200]!r}')
    else:
        log(f'replied to chat={chat_id} ({len(reply)} chars)')
except Exception as e:
    log(f'tg_send error: {e}')
PY
exit 0
