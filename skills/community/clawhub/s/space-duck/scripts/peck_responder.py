#!/usr/bin/env python3
"""
Space Duck — Autonomous peck responder.

INTENT: Close the David ↔ Sam auto-conversation gap. When peck_listener.py
        receives an inbound peck and pipes the envelope JSON into this
        script (via `--on-peck "python3 peck_responder.py"`), this script:

          1. Decodes the envelope.
          2. Checks the connection's `auto_respond` permission server-side.
          3. Honors the session rotation cap (`max_rounds`).
          4. Invokes the local Claude Code CLI to compose a reply
             anchored by the duck's SOUL.md + MEMORY.md + the inbound
             message.
          5. Sends the reply via send_peck.py --reply-to.
          6. Detects `<peck_done/>` marker → terminates the chain.

CALLS:  POST <api>/beak/connection/permissions   — permissions check.
        Local `claude` CLI subprocess — composes the reply text.
        send_peck.py subprocess — outbound reply.
        No third-party hosts contacted directly.

AUTH:   Beak Key in ~/.space-duck/config.json (chmod 600), same as every
        other script in this skill.

DOCTRINE FIT (project_two_lane_architecture):
        Lane A receiver = user infra. The brain that composes the
        autonomous reply runs HERE on the BYOA agent's machine.
        Spaceduckling stays identity + protocol only. Reply travels back
        through the standard peck envelope, the standard send_peck
        primitive, and the standard Telegram echo paths — both surfaces
        see every turn automatically.

USAGE (one-line, on the BYOA agent):
        python3 peck_listener.py \\
            --allow-shell-hook \\
            --on-peck "python3 $(pwd)/peck_responder.py"

ENV KNOBS (optional):
        SPACEDUCK_RESPONDER_MODEL   default: claude-sonnet-4-6
        SPACEDUCK_RESPONDER_TIMEOUT default: 90 (seconds, end-to-end)
        SPACEDUCK_RESPONDER_LOG     default: ~/.space-duck/responder.log
        SPACEDUCK_RESPONDER_DRY     dry-run; print would-be reply, send nothing
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path
import urllib.request, urllib.error

HOME       = Path.home()
SD_DIR     = HOME / '.space-duck'
CFG_PATH   = SD_DIR / 'config.json'
LOG_PATH   = Path(os.environ.get('SPACEDUCK_RESPONDER_LOG',
                                  str(SD_DIR / 'responder.log')))
DEFAULT_MODEL    = os.environ.get('SPACEDUCK_RESPONDER_MODEL', 'claude-sonnet-4-6')
DEFAULT_TIMEOUT  = int(os.environ.get('SPACEDUCK_RESPONDER_TIMEOUT', '90'))
DRY_RUN          = os.environ.get('SPACEDUCK_RESPONDER_DRY', '').lower() in ('1', 'true', 'yes')
CRITIC_REQUEST_RE = __import__('re').compile(r'<critic_request(?:\s+reason="[^"]*")?\s*/?>', __import__('re').IGNORECASE)

DONE_MARKER = '<peck_done/>'

# 0.4.0 — Phase 1 of peck protocol v2 (bilateral termination).
# Spec: coordination/SPEC-PECK-PROTOCOL-V2-TERMINATION-20260611.md
# Receiver-side: parse structured peck_meta if present; fail-safe to v1 logic
# (top-level envelope fields + <peck_done/> marker) when absent or malformed.
PROTOCOL_VERSION_SUPPORTED = 2
VALID_CHAIN_STATES = ('active', 'closing_candidate', 'closed')
# Phase 2 — handoff marker. Agent ends its reply with:
#   <handoff to="A1B2C3D4E5F6...." reason="needs legal review"/>
# When the responder sees it, the original chain terminates and a NEW
# peck is initiated to the handoff target — same task, fresh thread.
import re as _re
HANDOFF_RE = _re.compile(
    r'<handoff\s+to="(?P<sd>[0-9A-Fa-f]{16})"(?:\s+reason="(?P<reason>[^"]*)")?\s*/?>',
    _re.IGNORECASE,
)


def _log(msg):
    line = f'[{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}] {msg}\n'
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, 'a') as f:
            f.write(line)
    except Exception:
        pass
    sys.stderr.write(line)


def _notify_owner_silent_skip(envelope, reason, *, sd_name=None):
    """v0.4.10 (2026-06-17, Josh msg 23431) — close the silent-fail
    pattern Josh flagged: 'sometimes Wayne and Sam don't auto-respond,
    I have to tell them… doing nothing is the wrong option.'

    Every silent-exit path in this script used to log to file and
    `sys.exit(0)` — owner never knew a peck arrived. Now, before every
    silent exit, we push a Telegram message to the owner's chat
    (chat_id pulled from `~/.space-duck/forward.json` or
    `~/.space-duck/config.json`). The notice carries:
      - The sender's name + first ~200 chars of the peck
      - The reason auto-reply skipped
      - A clear "what to do next" line (compose manually / approve /
        or just acknowledge that you've seen it)

    Best-effort and silent on failure (so a TG outage doesn't compound
    the original silent-skip into a fatal crash). NEVER raises.
    """
    try:
        chat_id = ''
        token = ''
        # 1. Try forward.json (preferred — explicit forwarding config)
        fwd = SD_DIR / 'forward.json'
        if fwd.exists():
            try:
                fc = json.loads(fwd.read_text())
                tg = fc.get('telegram') or {}
                chat_id = str(tg.get('chat_id') or '').strip()
                token = str(tg.get('bot_token') or '').strip()
            except Exception:
                pass
        # 2. Fall back to config.json env-style entries
        if not (chat_id and token):
            try:
                cfg = json.loads(CFG_PATH.read_text()) if CFG_PATH.exists() else {}
                chat_id = chat_id or str(cfg.get('owner_chat_id') or
                                         cfg.get('telegram_chat_id') or '').strip()
                token = token or str(cfg.get('telegram_bot_token') or
                                     os.environ.get('SPACEDUCK_FWD_TG_TOKEN') or '').strip()
            except Exception:
                pass
        # 3. Last fallback to env vars
        chat_id = chat_id or os.environ.get('SPACEDUCK_FWD_TG_CHAT', '').strip()
        token = token or os.environ.get('SPACEDUCK_FWD_TG_TOKEN', '').strip()
        if not (chat_id and token):
            _log(f'silent-skip notify: no TG owner chat configured (reason={reason!r})')
            return
        sender = (envelope.get('sender_name') or
                  envelope.get('from_name') or
                  envelope.get('sender_spaceduck_id') or
                  'another duck')
        message_in = (envelope.get('message') or
                      envelope.get('text') or
                      envelope.get('body') or '').strip()
        snippet = message_in[:240] + ('…' if len(message_in) > 240 else '')
        duck_label = sd_name or 'this duck'
        text = (
            f'⚠️ Peck arrived but {duck_label} did NOT auto-reply.\n\n'
            f'From: {sender}\n'
            f'Reason: {reason}\n\n'
            f'> {snippet}\n\n'
            f'Tap to compose manually, or send `/approve` to me here '
            f'so I can try again. Silence is not a valid response.'
        )
        api = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = json.dumps({
            'chat_id': chat_id,
            'text': text,
            'disable_web_page_preview': True,
        }).encode()
        req = urllib.request.Request(api, data=payload,
            headers={'Content-Type': 'application/json'}, method='POST')
        try:
            urllib.request.urlopen(req, timeout=8)
            _log(f'silent-skip TG notify ok: reason={reason!r} sender={sender!r}')
        except Exception as _se:
            _log(f'silent-skip TG notify failed: {_se}')
    except Exception as _ne:
        # Belt-and-braces: any exception here is logged but never propagated.
        _log(f'silent-skip notify internal error: {_ne}')


def _load_cfg():
    if not CFG_PATH.exists():
        _log('no config — skill not paired; abort')
        sys.exit(0)
    return json.loads(CFG_PATH.read_text())


def _read_peck():
    raw = sys.stdin.read()
    if not raw.strip():
        _log('empty stdin — abort')
        sys.exit(0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        _log(f'invalid JSON on stdin: {e}')
        sys.exit(0)


def _check_permissions(cfg, sender_sd, my_sd):
    """Ask the platform for the connection's effective permissions dict.
    Returns (allowed, reason, perms). Defaults to allowed=False (fail-closed).
    `perms` always returned (empty dict on failure) so the caller can read
    secondary fields like critic_mode without a second round-trip.
    """
    api = cfg.get('api') or 'https://beak.spaceduckling.com'
    beak_key = cfg.get('beak_key') or ''
    url = f'{api}/beak/connection/permissions?sender_spaceduck_id={sender_sd}&target_spaceduck_id={my_sd}'
    req = urllib.request.Request(url, headers={'X-Beak-Key': beak_key})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return False, f'http_{e.code}', {}
    except Exception as e:
        return False, f'transport:{e}', {}
    perms = data.get('permissions') or data
    # 0.4.1 (Josh, 2026-06-15) — opt-out semantics: auto-respond is permitted
    # UNLESS the connection explicitly sets `auto_respond=false` (or `auto_reply=false`).
    # Pre-0.4.1 was opt-in (required explicit True), which caused silent
    # auto_respond_off exits on every approved-but-unflagged connection
    # (e.g. McQuacken ↔ Wayne mesh bonds backfilled via v707 with no perms map).
    # Owner can still hard-block by setting the flag to False at the connection
    # level via Mission Control → Connections → <peer> → Auto-respond toggle.
    auto_respond = perms.get('auto_respond')
    auto_reply   = perms.get('auto_reply')
    if auto_respond is False or auto_reply is False:
        return False, 'auto_respond_explicit_off', perms
    return True, 'permitted_default_on', perms


def _parse_peck_meta(envelope):
    """0.4.0 — Phase 1 of peck protocol v2.

    Extract structured peck_meta from envelope and return a normalized dict.
    NEVER raises. Malformed JSON, wrong types, missing fields, future
    versions — all degrade gracefully to v1 semantics (read top-level
    envelope fields; rely on `<peck_done/>` + max_rounds for termination).

    Resolution order per field: peck_meta value → envelope top-level → default.
    This preserves backward compatibility with Phase 0 envelopes that put
    session_id / max_rounds at the top level.

    Returns:
        {
            'protocol_version': 1 | 2,
            'session_id':       str,         # '' if absent
            'root_peck_id':     str,         # '' if absent
            'max_rounds':       int,         # 0 = no cap
            'current_round':    int,         # default 0
            'agent_state':      dict,        # Phase 4 placeholder
            'chain_state':      str,         # Phase 3, one of VALID_CHAIN_STATES
            'meta_present':     bool,        # True iff a usable peck_meta was found
        }
    """
    raw = envelope.get('peck_meta')

    meta = {}
    meta_present = False
    if isinstance(raw, dict):
        meta = raw
        meta_present = True
    elif isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            _log(f'peck_meta malformed JSON — degrading to v1 (raw={raw[:80]!r})')
            parsed = None
        if isinstance(parsed, dict):
            meta = parsed
            meta_present = True
        elif parsed is not None:
            _log(f'peck_meta JSON parsed to {type(parsed).__name__}, not dict — degrading to v1')
    elif raw is not None:
        _log(f'peck_meta has unexpected type {type(raw).__name__} — degrading to v1')

    # 0.4.0 Phase 1 (bugfix 2026-06-12 12:20) — gateway-strip workaround.
    # The BYOB peck forward at lambda_v8.py:7432 has a hardcoded allowlist
    # that DOES forward session_id/current_round/max_rounds (top-level) but
    # DROPS peck_meta dict + peck_protocol_version + root_peck_id. So a v2
    # sender's envelope reaches the receiver in degraded form: top-level
    # chain fields populated, peck_meta absent. Treat that as v2 so Phase
    # 1.5 echo-back fires and the chain keeps the round counter alive.
    # Wayne ↔ Sam log evidence 2026-06-12 03:41Z confirmed this strip.
    workaround_synthesized = False
    if not meta_present:
        has_top_level_chain = (
            (envelope.get('session_id') or '').strip() or
            (envelope.get('_peck_session_id') or '').strip() or
            (int(envelope.get('current_round') or 0)) > 0 or
            (int(envelope.get('max_rounds') or 0)) > 0
        )
        if has_top_level_chain:
            meta_present = True  # synthetic — top-level mirror is the meta source
            workaround_synthesized = True
            _log('peck_meta dict absent but top-level chain fields populated '
                 '— treating as v2 (gateway-strip workaround)')

    # Version: meta wins, top-level next, default v1.
    raw_version = meta.get('protocol_version') if meta_present else None
    if raw_version is None:
        raw_version = envelope.get('peck_protocol_version')
    try:
        version = int(raw_version) if raw_version is not None else 1
    except (TypeError, ValueError):
        version = 1
    if version < 1:
        version = 1
    if version > PROTOCOL_VERSION_SUPPORTED:
        _log(f'peck declared protocol_version={version} > supported='
             f'{PROTOCOL_VERSION_SUPPORTED}; downgrading')
        version = PROTOCOL_VERSION_SUPPORTED
    # 0.4.0 (polish 2026-06-12 14:33) — when the gateway-strip workaround
    # synthesized meta_present=True (because the gateway stripped peck_meta
    # + peck_protocol_version but preserved top-level chain fields), the
    # version parsed from envelope is still 1 (the default) even though
    # we're treating the chain logically as v2. Promote to PROTOCOL_VERSION
    # _SUPPORTED so the log line + reply_meta carry the correct label.
    # Sam flagged this 14:33 GMT+8 — cosmetic, not behavioral.
    if workaround_synthesized and version < PROTOCOL_VERSION_SUPPORTED:
        version = PROTOCOL_VERSION_SUPPORTED

    # Field coalescing helpers — meta wins, then envelope top-level, then default.
    def _coalesce(meta_key, env_keys, default):
        if meta_present and meta.get(meta_key) not in (None, ''):
            return meta[meta_key]
        for k in env_keys:
            v = envelope.get(k)
            if v not in (None, ''):
                return v
        return default

    def _coalesce_int(meta_key, env_keys, default=0):
        v = _coalesce(meta_key, env_keys, default)
        try:
            return int(v)
        except (TypeError, ValueError):
            return default

    session_id   = _coalesce('session_id',   ['session_id', '_peck_session_id'], '')
    root_peck_id = _coalesce('root_peck_id', ['root_peck_id', '_peck_root_id'], '')
    max_rounds   = _coalesce_int('max_rounds',
                                 ['max_rounds', '_peck_max_rounds'], 0)
    current_round = _coalesce_int('current_round',
                                  ['current_round', 'round', '_peck_round'], 0)

    agent_state = meta.get('agent_state') if meta_present else None
    if not isinstance(agent_state, dict):
        agent_state = {}

    chain_state_raw = (meta.get('chain_state') if meta_present else None) or 'active'
    chain_state = chain_state_raw if chain_state_raw in VALID_CHAIN_STATES else 'active'

    return {
        'protocol_version': version,
        'session_id':       str(session_id) if session_id else '',
        'root_peck_id':     str(root_peck_id) if root_peck_id else '',
        'max_rounds':       max_rounds,
        'current_round':    current_round,
        'agent_state':      agent_state,
        'chain_state':      chain_state,
        'meta_present':     meta_present,
    }


def _session_should_terminate(envelope):
    """True if the rotation cap is reached. Single-shot pecks (no session)
    always reply once."""
    sess = envelope.get('session_id') or envelope.get('_peck_session_id')
    if not sess:
        return False
    try:
        current = int(envelope.get('current_round') or envelope.get('round') or
                      envelope.get('_peck_round') or 0)
        max_r   = int(envelope.get('max_rounds') or envelope.get('_peck_max_rounds') or 0)
    except (TypeError, ValueError):
        return False
    if max_r <= 0:
        return False
    return current >= max_r


def _load_soul():
    p = SD_DIR / 'SOUL.md'
    if p.exists():
        try:
            return p.read_text()[:6000]
        except Exception:
            return ''
    return ''


def _load_memory():
    p = SD_DIR / 'MEMORY.md'
    if p.exists():
        try:
            return p.read_text()[:6000]
        except Exception:
            return ''
    return ''


def _compose_reply(envelope, soul, memory):
    """Invoke the local Claude Code CLI with a focused prompt. Returns
    the reply text, stripped. Empty string on failure or refusal."""
    sender_name = (envelope.get('sender_name') or
                   envelope.get('from_name') or
                   envelope.get('sender_spaceduck_id') or
                   'another duck')
    message_in = (envelope.get('message') or
                  envelope.get('text') or
                  envelope.get('body') or
                  '').strip()
    if not message_in:
        _log('no message text in envelope')
        return ''
    parts = []
    if soul.strip():
        parts.append('# Who you are (SOUL.md)\n' + soul.strip())
    if memory.strip():
        parts.append('# What you remember (MEMORY.md)\n' + memory.strip())
    # v0.4.4 — inject CONNECTIONS.md so the brain has the duck directory
    # (peer names + spaceduck_ids) without having to be told each time.
    # Closes the Lane A parity gap surfaced 2026-06-15 when Wayne told
    # Josh he didn't know McQuacken's spaceduck_id despite being bonded.
    # workspace_bridge.py auto-syncs this file every 5 min.
    try:
        connections_path = SD_DIR / 'CONNECTIONS.md'
        if connections_path.is_file():
            connections_text = connections_path.read_text().strip()
            if connections_text:
                parts.append('# Your Network (CONNECTIONS.md — auto-synced)\n'
                             + connections_text)
    except Exception as _ce:
        _log(f'CONNECTIONS.md load skipped: {_ce}')
    parts.append(
        f'# Incoming peck from {sender_name}\n'
        f'> {message_in}\n\n'
        f'Compose your reply as that duck — concise, in-character, factual. '
        f'If the conversation reached a natural close, end your reply with '
        f'`{DONE_MARKER}` on its own line so the auto-responder stops the chain. '
        f'Reply only with the message body — no preamble.'
    )
    prompt = '\n\n---\n\n'.join(parts)
    # 0.4.0 (bugfix 2026-06-12 14:00) — pipe prompt via stdin instead of
    # passing as positional argv. Reasons: avoids argv-length limits on
    # long SOUL+MEMORY+message prompts, eliminates shell-escape edge cases
    # around backticks/dollars in user content, matches the pattern Wayne's
    # one-shot CLI test confirmed working when his per-message subprocess
    # invocation was failing with exit 1.
    cmd = ['claude', '--print', '--permission-mode', 'bypassPermissions',
           '--model', DEFAULT_MODEL]
    try:
        out = subprocess.run(cmd, input=prompt, capture_output=True,
                             text=True, timeout=DEFAULT_TIMEOUT)
        if out.returncode != 0:
            # 0.4.0 — surface BOTH stderr and stdout (claude CLI sometimes
            # prints user-facing errors to stdout when --print is set).
            _err = (out.stderr or '').strip()[:200]
            _out_tail = (out.stdout or '').strip()[:200]
            _log(f'claude CLI exit {out.returncode}: stderr={_err!r} stdout={_out_tail!r}')
            return ''
        return (out.stdout or '').strip()
    except subprocess.TimeoutExpired:
        _log(f'claude CLI timed out after {DEFAULT_TIMEOUT}s')
        return ''
    except FileNotFoundError:
        _log('claude CLI not on PATH — install @anthropic-ai/claude-code')
        return ''
    except Exception as e:
        _log(f'claude CLI error: {e}')
        return ''


def _run_critic(draft_reply, envelope, perms):
    """Invoke peck_critic.py to review the draft before sending.
    Returns (verdict, reason, rewrite). Defaults to PASS on any failure
    so a flaky critic never silently blocks legitimate replies."""
    script = Path(__file__).parent / 'peck_critic.py'
    if not script.exists():
        return 'PASS', 'critic_script_missing', ''
    payload = json.dumps({
        'draft_reply': draft_reply,
        'inbound': envelope,
        'connection': perms,
    })
    try:
        out = subprocess.run(['python3', str(script)],
                             input=payload,
                             capture_output=True, text=True, timeout=60)
        if out.returncode != 0:
            return 'PASS', f'critic_exit_{out.returncode}', ''
        try:
            data = json.loads(out.stdout)
        except json.JSONDecodeError:
            return 'PASS', 'critic_non_json', ''
        verdict = (data.get('verdict') or 'PASS').upper()
        if verdict not in ('PASS', 'REVISE', 'BLOCK'):
            verdict = 'PASS'
        return verdict, data.get('reason', ''), data.get('rewrite', '')
    except Exception as e:
        return 'PASS', f'critic_invoke_error:{e}', ''


def _send_handoff(target_sd, reason, original_envelope, our_take):
    """Fire a NEW peck at a third duck to continue the task there. The
    handoff message carries the original task context plus our take, so
    the target gets enough to pick up cleanly without needing the full
    prior chain."""
    script = Path(__file__).parent / 'send_peck.py'
    if not script.exists():
        _log(f'send_peck.py not found at {script} — cannot handoff')
        return False
    orig_sender = (original_envelope.get('sender_name') or
                   original_envelope.get('from_name') or 'a peer')
    orig_message = (original_envelope.get('message') or
                    original_envelope.get('text') or '').strip()
    handoff_text = (
        f'[Handoff] {orig_sender} asked: "{orig_message[:600]}"\n\n'
        f'My take: {our_take[:600]}\n\n'
        f'Reason for handing off to you: {reason or "(no reason given)"}.\n'
        f'Please continue the conversation with them directly.'
    )
    cmd = ['python3', str(script),
           '--spaceduck-id', target_sd,
           '--message', handoff_text,
           '--purpose', 'handoff']
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            _log(f'handoff send_peck exit {out.returncode}: {out.stderr[:300]}')
            return False
        _log(f'handoff peck sent to {target_sd}')
        return True
    except Exception as e:
        _log(f'handoff send_peck error: {e}')
        return False


def _write_inbox_file(peck_id, envelope):
    """0.3.16 — self-healing inbox write.
    Webhook-bound ducks (TG bot bound, or any non-empty openclaw_webhook_url)
    never see peck_listener.py --poll write inbox/<peck_id>.json — pecks
    arrive via webhook → telegram_listener.py → this responder, bypassing
    the polling queue entirely. send_peck.py --reply-to then fails with
    'no inbox record'. Writing from the responder side (we have the full
    envelope in hand) removes the dependency. Idempotent; safe if a poller
    later writes the same file."""
    try:
        inbox_dir = SD_DIR / 'inbox'
        inbox_dir.mkdir(parents=True, exist_ok=True)
        path = inbox_dir / f'{peck_id}.json'
        path.write_text(json.dumps(envelope))
        _log(f'inbox self-write ok peck_id={peck_id}')
    except Exception as e:
        _log(f'inbox self-write failed peck_id={peck_id}: {e}')


def _tokenize(text):
    """0.4.0 Phase 2 — lowercase, split on non-word chars, return token SET.
    Empty input → empty set. Defensive: never raises."""
    if not text:
        return set()
    return set(__import__('re').findall(r'\w+', str(text).lower()))


def _jaccard(set_a, set_b):
    """0.4.0 Phase 2 — Jaccard similarity of two token sets.
    Returns float in [0.0, 1.0]. Either set empty → 0.0 (no signal)."""
    if not set_a or not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return (inter / union) if union else 0.0


def _chain_history(inbox_dir, root_peck_id, current_peck_id, max_entries=5,
                    session_id=''):
    """0.4.0 Phase 2 — gather message texts from prior pecks in the same chain.

    Walks all *.json files in inbox_dir. Matches a stored envelope to the
    current chain via, in order: peck_meta.root_peck_id, top-level
    envelope.root_peck_id, OR (when root_peck_id is empty) peck_meta.session_id
    / top-level envelope.session_id. The session_id fallback exists because
    the gateway BYOB forward (lambda_v8.py:7432-7452) preserves session_id but
    strips root_peck_id — without the fallback, Phase 2 novelty scoring
    silently no-ops on every live wire peck even with the gateway-strip
    workaround for meta_present.

    Excludes the current peck (avoid self-comparison). Returns list of
    message texts ordered MOST-RECENT FIRST. At most max_entries entries.
    Returns [] on missing dir or any I/O failure. Never raises.
    """
    if (not root_peck_id and not session_id) or not inbox_dir:
        return []
    try:
        paths = list(inbox_dir.glob('*.json'))
    except Exception:
        return []
    entries = []
    for path in paths:
        if path.stem == current_peck_id:
            continue
        try:
            env = json.loads(path.read_text())
        except Exception:
            continue
        # Resolve this envelope's chain identifier (root_peck_id first,
        # session_id fallback per gateway-strip workaround).
        env_root = None
        env_session = None
        pm = env.get('peck_meta') if isinstance(env, dict) else None
        if isinstance(pm, dict):
            env_root = pm.get('root_peck_id')
            env_session = pm.get('session_id')
        if isinstance(env, dict):
            if not env_root:
                env_root = env.get('root_peck_id')
            if not env_session:
                env_session = env.get('session_id') or env.get('_peck_session_id')
        # Match: prefer root_peck_id when both sides have it; otherwise
        # use session_id. Skip if neither identifier matches.
        if root_peck_id and env_root:
            if env_root != root_peck_id:
                continue
        elif session_id and env_session:
            if env_session != session_id:
                continue
        else:
            continue
        text = (env.get('message') or env.get('text')
                or env.get('body') or '') if isinstance(env, dict) else ''
        if not text:
            continue
        # Timestamp for ordering: envelope.timestamp wins, fall back to mtime.
        ts = None
        if isinstance(env, dict):
            ts = env.get('timestamp')
        try:
            ts_val = float(ts) if ts is not None else path.stat().st_mtime
        except (TypeError, ValueError):
            ts_val = path.stat().st_mtime
        entries.append((ts_val, str(text)))
    entries.sort(key=lambda e: e[0], reverse=True)
    return [t for _, t in entries[:max_entries]]


def _compute_novelty_score(draft_reply, history):
    """0.4.0 Phase 2 — deterministic novelty score 0-100.

    Higher = more novel. Score is the inverse of MAX Jaccard similarity
    between the draft and any prior chain message: novelty = round((1 - max_sim) * 100).

    No history → 100 (nothing to compare; treat as fully novel).
    Empty draft → 100 (no signal).
    Identical to prior → 0.

    Honest limitation: word-token Jaccard catches LEXICAL repetition (verbatim
    or near-verbatim). Semantically-equivalent goodbyes with different
    wording ("Catch you later" vs "See you soon") score high novelty even
    though they're closure-equivalent. Pair with Phase 4 (LLM-reported
    completion_status + pending_actions) for semantic closure detection.
    """
    if not draft_reply or not history:
        return 100
    draft_tokens = _tokenize(draft_reply)
    if not draft_tokens:
        return 100
    max_sim = 0.0
    for prior in history:
        sim = _jaccard(draft_tokens, _tokenize(prior))
        if sim > max_sim:
            max_sim = sim
    return int(round((1.0 - max_sim) * 100))


def _build_reply_meta(parsed_inbound_meta, novelty_score=None):
    """0.4.0 Phase 1.5 — echo-mirror meta on reply.

    If inbound was v2 (meta_present=True), produce a v2 meta dict for the
    reply: preserve session_id + root_peck_id + protocol_version + max_rounds,
    increment current_round by 1, set chain_state='active' (Phase 3 will
    refine to closing_candidate transitions). If inbound was v1, return None
    so the reply is also v1 (echo-mirror — don't force-upgrade peers).

    Convention: each peck in the chain bumps current_round by 1. Round 1 =
    initial peck (sender treats their own send as round 1). Receiver of a
    peck with current_round >= max_rounds terminates without replying.
    Phase 0 envelopes without explicit current_round default to 0, which
    yields a 5-message chain at max_rounds=4 instead of 4 — known off-by-one,
    fixed when senders explicitly emit current_round=1 on initial pecks.

    Handoff (`_send_handoff`) does NOT use this — handoffs are new sessions
    to a third duck, not chain continuations.
    """
    if not parsed_inbound_meta or not parsed_inbound_meta.get('meta_present'):
        return None
    out = {
        'protocol_version': parsed_inbound_meta['protocol_version'],
        'session_id':       parsed_inbound_meta['session_id'],
        'root_peck_id':     parsed_inbound_meta['root_peck_id'],
        'max_rounds':       parsed_inbound_meta['max_rounds'],
        'current_round':    parsed_inbound_meta['current_round'] + 1,
        'chain_state':      'active',
    }
    # 0.4.0 Phase 2 — embed novelty_score (0-100) when computed. Receiver
    # treats absent as "not measured", not as 0 or 100. Phase 3 wires this
    # into chain_state transitions; Phase 2 just emits the field.
    if novelty_score is not None:
        try:
            out['novelty_score'] = int(novelty_score)
        except (TypeError, ValueError):
            pass
    return out


def _send_reply(peck_id, reply_text, peck_meta=None):
    """Use send_peck.py --reply-to to send the response back.

    0.4.0 Phase 1.5 — peck_meta (if non-None) is passed to send_peck.py via
    --peck-meta and embedded as a signature-neutral envelope field. This
    propagates protocol_version + session_id + root_peck_id + current_round
    to the peer so v2 chain state survives the round-trip."""
    if not peck_id:
        _log('no peck_id — cannot send reply via --reply-to')
        return False
    script = Path(__file__).parent / 'send_peck.py'
    if not script.exists():
        _log(f'send_peck.py not found at {script}')
        return False
    cmd = ['python3', str(script), '--reply-to', peck_id, '--message', reply_text]
    if peck_meta:
        cmd.extend(['--peck-meta', json.dumps(peck_meta)])
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            # 0.3.15 — send_peck.py prints user-facing errors via print() to
            # STDOUT (not stderr). Pre-0.3.15 we only logged stderr → Wayne
            # saw `send_peck.py exit 1:` with no diagnostic context. Capture
            # both streams so the actual error message (e.g. "no inbox
            # record", "rate limited", "envelope verify failed") is visible.
            _stderr = (out.stderr or '').strip()[:300]
            _stdout = (out.stdout or '').strip()[:300]
            _log(f'send_peck.py exit {out.returncode}: '
                 f'stderr={_stderr!r} stdout={_stdout!r}')
            return False
        _log(f'reply sent for peck_id={peck_id}')
        return True
    except Exception as e:
        _log(f'send_peck.py error: {e}')
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[2])
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Echo decision trail to stderr.')
    args = parser.parse_args()

    cfg = _load_cfg()
    envelope = _read_peck()

    my_sd     = cfg.get('spaceduck_id') or ''
    peck_id   = envelope.get('peck_id') or envelope.get('id') or ''
    sender_sd = (envelope.get('sender_spaceduck_id') or
                 envelope.get('from_spaceduck_id') or
                 envelope.get('from') or '')

    if not peck_id or not sender_sd or not my_sd:
        _log(f'missing ids — peck_id={peck_id} sender={sender_sd} my_sd={my_sd}')
        sys.exit(0)

    # 0.3.16 — write inbox file from the in-hand envelope BEFORE any downstream
    # call to send_peck.py --reply-to. Closes the "no inbox record" failure
    # mode that hit Sam ↔ Wayne on 2026-06-11 when a webhook-bound duck has
    # no polling listener writing the file.
    _write_inbox_file(peck_id, envelope)

    # 0.4.0 Phase 1 — parse structured peck_meta for diagnostics + downstream
    # phases. Termination logic still flows through _session_should_terminate
    # below (top-level envelope reads), so this is observability-only here.
    meta = _parse_peck_meta(envelope)
    _log(
        f'peck_meta v={meta["protocol_version"]} '
        f'present={meta["meta_present"]} '
        f'session={meta["session_id"] or "-"} '
        f'root={meta["root_peck_id"] or "-"} '
        f'round={meta["current_round"]}/{meta["max_rounds"] or "∞"} '
        f'chain_state={meta["chain_state"]}'
    )

    # 0.4.10 — pull a duck name label once for owner notifications.
    _duck_label_for_notify = cfg.get('agent_name') or cfg.get('duck_name') or ''

    if _session_should_terminate(envelope):
        _log(f'rotation cap reached for session — declining to reply (peck_id={peck_id})')
        _notify_owner_silent_skip(envelope, 'session rotation cap reached', sd_name=_duck_label_for_notify)
        sys.exit(0)

    allowed, reason, perms = _check_permissions(cfg, sender_sd, my_sd)
    if not allowed:
        _log(f'auto-respond NOT permitted ({reason}) — peck_id={peck_id} sender={sender_sd}')
        _notify_owner_silent_skip(envelope, f'auto-respond NOT permitted ({reason})', sd_name=_duck_label_for_notify)
        sys.exit(0)

    soul = _load_soul()
    memory = _load_memory()
    reply = _compose_reply(envelope, soul, memory)
    if not reply:
        _log(f'no reply composed — abort peck_id={peck_id}')
        _notify_owner_silent_skip(envelope, 'claude CLI returned no reply (check ~/.space-duck/responder.log)', sd_name=_duck_label_for_notify)
        sys.exit(0)

    # Actor-critic pass — runs when:
    #   (a) connection has critic_mode='alternating', OR
    #   (b) connection has critic_mode='on_request' AND inbound carries
    #       a <critic_request/> marker.
    critic_mode = (perms.get('critic_mode') or 'none').lower()
    inbound_msg = envelope.get('message') or envelope.get('text') or ''
    wants_critic = critic_mode == 'alternating' or (
        critic_mode == 'on_request' and CRITIC_REQUEST_RE.search(inbound_msg))
    if wants_critic:
        verdict, _why, rewrite = _run_critic(reply, envelope, perms)
        _log(f'critic verdict={verdict} reason={_why!r}')
        if verdict == 'BLOCK':
            _log(f'critic BLOCK — aborting reply for peck_id={peck_id}')
            _notify_owner_silent_skip(envelope, f'critic BLOCK: {_why}', sd_name=_duck_label_for_notify)
            sys.exit(0)
        if verdict == 'REVISE' and rewrite:
            reply = rewrite

    has_done = DONE_MARKER in reply
    handoff_match = HANDOFF_RE.search(reply)
    handoff_to = handoff_match.group('sd') if handoff_match else ''
    handoff_reason = (handoff_match.group('reason') or '') if handoff_match else ''

    reply_clean = reply
    reply_clean = reply_clean.replace(DONE_MARKER, '')
    if handoff_match:
        reply_clean = HANDOFF_RE.sub('', reply_clean)
    reply_clean = reply_clean.strip()

    if not reply_clean and not handoff_to:
        _log(f'reply was empty after stripping markers — peck_id={peck_id}')
        _notify_owner_silent_skip(envelope, 'reply was empty after stripping markers (claude likely only emitted <peck_done/> with no body)', sd_name=_duck_label_for_notify)
        sys.exit(0)

    # 0.4.0 Phase 1.5 — echo-mirror peck_meta on reply: v1 in → v1 out
    # (peck_meta=None), v2 in → v2 out with current_round incremented.
    # 0.4.0 Phase 2 — compute deterministic novelty score on the draft vs
    # last N (default 5) prior chain messages. Embeds in reply_meta when
    # v2. Score is observability-only in Phase 2; Phase 3 will gate
    # chain_state transitions on it.
    # Placement: compute BEFORE the DRY_RUN exit so dry runs exercise the
    # full v2 build/embed path and log novelty + reply_meta. Send itself
    # is the only step gated by DRY_RUN. Sam flagged this 2026-06-12 09:37
    # — original placement put these AFTER the DRY exit, so self-tests
    # couldn't observe Phase 2 behavior.
    novelty = None
    if meta.get('meta_present') and (meta.get('root_peck_id') or meta.get('session_id')):
        history = _chain_history(
            SD_DIR / 'inbox',
            meta.get('root_peck_id', ''),
            peck_id,
            max_entries=5,
            session_id=meta.get('session_id', ''),
        )
        novelty = _compute_novelty_score(reply_clean, history)
        _log(f'novelty score={novelty} (vs {len(history)} prior chain entries)')

        # 0.4.12 Phase 3 — receiver-side novelty gate. If our drafted
        # reply contributes <15% new tokens vs the last 5 chain entries
        # AND we're already at round >= 2, we're stuck in a polite loop.
        # Append <peck_done/> so the chain terminates cleanly + mark
        # chain_state=closing_candidate in the outgoing peck_meta.
        # Pairs with platform v838 cross-session pair guard: v838 stops
        # new-session loop revival, Phase 3 stops in-session politeness
        # rallies. Two layers, complementary.
        current_round = int(meta.get('current_round') or 0)
        if (novelty is not None and novelty < 15 and current_round >= 2
                and not has_done):
            _log(f'[PHASE3] novelty={novelty} < 15 at round={current_round} — '
                 f'forcing chain termination (appending <peck_done/>)')
            reply_clean = (reply_clean.rstrip() + '\n\n' + DONE_MARKER).strip()
            reply = reply.rstrip() + '\n\n' + DONE_MARKER
            has_done = True
            meta['chain_state'] = 'closing_candidate'

    reply_meta = _build_reply_meta(meta, novelty_score=novelty)
    if reply_meta:
        _log(f'reply will carry peck_meta v={reply_meta["protocol_version"]} '
             f'round={reply_meta["current_round"]}/{reply_meta["max_rounds"] or "∞"}'
             + (f' novelty={reply_meta.get("novelty_score")}'
                if 'novelty_score' in reply_meta else ''))

    if DRY_RUN:
        _log(f'[DRY] would send reply to peck_id={peck_id}: {reply_clean[:300]}')
        if has_done:
            _log('[DRY] done marker present — chain would terminate')
        if handoff_to:
            _log(f'[DRY] handoff to {handoff_to} reason={handoff_reason!r}')
        sys.exit(0)

    # Send the substantive reply back to the original sender first (so they
    # know we received and what our take was) — then fire a fresh peck at
    # the handoff target so the conversation continues there.
    # 0.3.15 — capture _send_reply's success bool so we don't claim the chain
    # cleanly terminated when the reply actually failed to send. Wayne msg
    # 22571 flagged this — previously `done marker terminates` logged
    # unconditionally, making post-mortem diagnosis harder.
    sent_ok = _send_reply(peck_id, reply_clean, peck_meta=reply_meta) if reply_clean else False
    if handoff_to:
        _send_handoff(handoff_to, handoff_reason,
                      envelope, reply_clean or '(handoff)')
        _log(f'handoff sent to {handoff_to} reason={handoff_reason!r} '
             f'after peck_id={peck_id}')
    if has_done:
        if sent_ok:
            _log(f'done marker present — chain terminates after this reply '
                 f'(peck_id={peck_id})')
        else:
            _log(f'done marker present BUT send failed — chain state '
                 f'ambiguous (peck_id={peck_id})')
    sys.exit(0)


if __name__ == '__main__':
    main()
