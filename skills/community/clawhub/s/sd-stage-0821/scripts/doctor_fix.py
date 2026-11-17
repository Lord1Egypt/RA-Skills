#!/usr/bin/env python3
"""
Space Duck — THE DOCTOR: diagnose → treat → verify, one command.

INTENT: doctor.sh diagnoses (read-only doctrine) and heal.sh treats a
        fixed 2026-06 checklist — neither catches the rails that actually
        died in production (2026-07-16 audit): a mute telegram listener
        (no --on-message brain), a missing owner_chat_id, a dead pulse
        loop, cross-duck pgrep contamination. This script is the R1–R7
        recipe loop from the zero-touch design (Josh #25917/#25945):

          R1  pulse rail dead        → SAFE   start supervised 240s loop
          R2  peck rail dead         → SAFE   start listener + responder
          R3  Claude auth missing    → GATED  symlink recipe (never auto)
          R4  stale workspace URL    → GATED  flip-endpoint recipe
          R5  ephemeral ingress      → GATED  warn + rebind recipe
          R6  never paired           → HUMAN  pair.py (browser click)
          R7  verify pass            → re-diagnose after treatment
          +   mute TG rail / no owner_chat_id / SOUL.md stub (2026-07-16)

AUTONOMY TIERS
        SAFE   — fixed automatically under --fix, no human.
        GATED  — printed as a proposal with the exact command; never run.
        HUMAN  — browser-click steps; instructions only.

SCOPE   Everything is HOME-scoped: process probes match only processes
        whose env HOME (or inline cmdline HOME=) equals this duck's HOME.
        Multi-duck hosts never bleed into each other's diagnosis.

CALLS   GET <api>/beak/spaceducks (own row: last_seen / binding state).
        Space Duck's own backend only. Beak Key from ~/.space-duck/config.json.

USAGE   python3 doctor_fix.py            # diagnose only (read-only)
        python3 doctor_fix.py --fix      # diagnose → treat SAFE → verify
        python3 doctor_fix.py --json     # machine-readable to stdout
        --tg-port N      port for the telegram listener if none is running
        --owner-chat ID  owner Telegram chat id (enables SAFE config write)
        --deep           also live-test Claude auth (slow, ~20-60s)

EXIT    0 all green · 1 warnings only · 2 any rail red after treatment

Report card JSON is always written to ~/.space-duck/doctor_report.json.
Idempotent: a second run after a successful --fix takes zero actions.
Authored 2026-07-16 — per Josh #25945 ("space-duck-doctor / -fix").
"""
import argparse, json, os, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

# 0.8.17 — one resolver for the claude CLI, shared with peck_responder /
# peck_critic / pulse so doctor probes the same binary the responder execs.
try:
    from _claudebin import resolve_claude
except Exception:
    def resolve_claude():
        return shutil.which('claude') or str(Path.home() / '.npm-global' / 'bin' / 'claude')

HOME = Path(os.environ.get('HOME', str(Path.home())))
SD_DIR = HOME / '.space-duck'
CONFIG = SD_DIR / 'config.json'
SCRIPTS = Path(__file__).resolve().parent
REPORT_PATH = SD_DIR / 'doctor_report.json'
PULSE_INTERVAL = 240

OK, WARN, FAIL = 'ok', 'warn', 'fail'
GLYPH = {OK: '✓', WARN: '⚠', FAIL: '✗'}


# ── HOME-scoped process probe ─────────────────────────────────────────────────
def procs_for_home(needle):
    """PIDs whose cmdline contains `needle` AND belong to THIS duck's HOME.

    Ownership = env HOME equals this HOME, or the cmdline itself carries an
    inline `HOME=<this home> ...` override (the sh-loop pulse pattern).
    This is the fix for the cross-duck pgrep contamination bug.
    """
    hits = []
    me = str(os.getpid())
    for pid in os.listdir('/proc'):
        if not pid.isdigit() or pid == me:
            continue
        try:
            cmd = Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace')
            if needle not in cmd or 'doctor_fix.py' in cmd:
                continue
            env_home = ''
            try:
                for kv in Path(f'/proc/{pid}/environ').read_bytes().split(b'\0'):
                    if kv.startswith(b'HOME='):
                        env_home = kv[5:].decode(errors='replace')
                        break
            except (PermissionError, FileNotFoundError):
                pass
            if env_home == str(HOME) or f'HOME={HOME} ' in cmd:
                hits.append((int(pid), cmd.strip()))
        except (FileNotFoundError, ProcessLookupError):
            continue
    return hits


def spawn_detached(argv_or_sh, log_path):
    log = open(log_path, 'ab')
    kwargs = dict(stdout=log, stderr=log, stdin=subprocess.DEVNULL,
                  start_new_session=True, cwd=str(SCRIPTS),
                  env={**os.environ, 'HOME': str(HOME)})
    if isinstance(argv_or_sh, str):
        return subprocess.Popen(['/bin/sh', '-c', argv_or_sh], **kwargs)
    return subprocess.Popen(argv_or_sh, **kwargs)


# ── The check/recipe registry ─────────────────────────────────────────────────
class Card:
    def __init__(self):
        self.checks, self.actions, self.proposals = [], [], []

    def add(self, rid, name, status, detail, tier=None, proposal=None):
        self.checks.append({'id': rid, 'name': name, 'status': status,
                            'detail': detail, 'tier': tier})
        if proposal and status != OK:
            self.proposals.append({'id': rid, 'tier': tier, 'action': proposal})

    def worst(self):
        s = [c['status'] for c in self.checks]
        return FAIL if FAIL in s else (WARN if WARN in s else OK)


def load_cfg():
    try:
        cfg = json.loads(CONFIG.read_text())
    except Exception:
        return None
    from _apiguard import check_api_base  # [HARDEN-071]
    check_api_base(cfg)
    return cfg


def check_identity(card, cfg):
    """R6 — never paired. HUMAN-ONLY fix (browser click)."""
    if cfg and cfg.get('beak_key') and cfg.get('spaceduck_id'):
        card.add('R6', 'identity (paired)', OK,
                 f"{cfg.get('agent_name', '?')} · {cfg.get('spaceduck_id')}")
        return True
    card.add('R6', 'identity (paired)', FAIL,
             f'no beak_key in {CONFIG}', tier='HUMAN',
             proposal=f'cd {SCRIPTS} && HOME={HOME} python3 pair.py --start '
                      '# then the human clicks the 6-digit URL, then --confirm')
    return False


def check_platform(card, cfg):
    """Platform view of this duck: last_seen freshness + binding state."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    try:
        req = urllib.request.Request(
            f"{api}/beak/spaceducks?duckling_id={cfg.get('duckling_id', '')}",
            headers={'Accept': 'application/json', 'X-Beak-Key': cfg.get('beak_key', '')})
        with urllib.request.urlopen(req, timeout=10) as r:
            rows = json.loads(r.read())
        rows = rows.get('agents', rows.get('spaceducks', []))
        mine = next((s for s in rows if s.get('spaceduck_id') == cfg.get('spaceduck_id')), None)
        if not mine:
            card.add('PLAT', 'platform row', FAIL, 'own spaceduck row not returned')
            return None
        age = int(time.time()) - int(mine.get('last_seen') or 0)
        st = OK if age < 2 * PULSE_INTERVAL else (WARN if age < 3600 else FAIL)
        card.add('PLAT', 'platform last_seen', st, f'{age}s ago')
        tk = str(mine.get('byob_listener_tunnel_kind', '') or '')
        if 'ephemeral' in tk:  # R5 — never auto-rebind (owner-gated)
            card.add('R5', 'ingress stability', WARN, f'tunnel_kind={tk}', tier='GATED',
                     proposal='rebind to a stable named tunnel / <duck>.spaceduck.bot '
                              f'(bind_telegram.py) — owner approval required')
        return mine
    except Exception as e:
        card.add('PLAT', 'platform reachability', WARN, f'{type(e).__name__}: {e}')
        return None


def check_pulse(card):
    """R1 — persistent pulse loop for THIS HOME."""
    loops = [p for p in procs_for_home('pulse.py') if 'while true' in p[1]]
    if loops:
        card.add('R1', 'pulse rail', OK, f'loop pid {loops[0][0]}')
        return True
    card.add('R1', 'pulse rail', FAIL, 'no supervised pulse loop for this HOME', tier='SAFE')
    return False


def fix_pulse(card):
    cmd = (f'while true; do HOME={HOME} python3 {SCRIPTS}/pulse.py '
           f'>/dev/null 2>&1 || true; sleep {PULSE_INTERVAL}; done')
    spawn_detached(cmd, SD_DIR / 'pulse_daemon.log')
    one = subprocess.run(['python3', str(SCRIPTS / 'pulse.py')], cwd=str(SCRIPTS),
                         env={**os.environ, 'HOME': str(HOME)},
                         capture_output=True, text=True, timeout=30)
    ok = one.returncode == 0
    card.actions.append({'id': 'R1', 'action': 'started 240s pulse loop',
                         'verified': ok, 'detail': (one.stdout or one.stderr).strip()[-120:]})
    return ok


def check_peck(card):
    """R2 — peck listener + responder brain for THIS HOME."""
    ls = procs_for_home('peck_listener.py')
    if ls:
        brained = any('--on-peck' in c for _, c in ls)
        if brained:
            card.add('R2', 'peck rail', OK, f'listener pid {ls[0][0]} (+responder hook)')
            return True
        card.add('R2', 'peck rail', WARN, 'listener up but NO --on-peck responder (mute)', tier='SAFE')
        return False
    card.add('R2', 'peck rail', FAIL, 'no peck_listener for this HOME', tier='SAFE')
    return False


def fix_peck(card):
    for pid, _ in procs_for_home('peck_listener.py'):  # replace mute listener
        try:
            os.kill(pid, 15)
        except OSError:
            pass
    time.sleep(1)
    spawn_detached(['python3', str(SCRIPTS / 'peck_listener.py'), '--poll',
                    '--interval', '3', '--allow-shell-hook', '--on-peck',
                    f'python3 {SCRIPTS}/peck_responder.py'],
                   SD_DIR / 'listener.log')
    time.sleep(2)
    ok = bool(procs_for_home('peck_listener.py'))
    card.actions.append({'id': 'R2', 'action': 'started peck_listener --poll + responder',
                         'verified': ok, 'detail': ''})
    return ok


def check_tg(card, cfg, args):
    """TG rail — listener present, WITH a brain, owner chat configured.

    The 2026-07-16 killer: a listener without --on-message stores forwards
    and never answers; without a resolvable owner chat the responder refuses
    all inbound. Both are silent — chat just goes dead.
    """
    # Mirror reply_with_claude.sh resolve_owner_chat() order exactly:
    # forward.json .telegram.chat_id → config owner_chat_id|telegram_chat_id
    # → env SPACEDUCK_FWD_TG_CHAT.
    owner = ''
    try:
        owner = str((json.loads((SD_DIR / 'forward.json').read_text())
                     .get('telegram') or {}).get('chat_id') or '').strip()
    except Exception:
        pass
    owner = owner or str(cfg.get('owner_chat_id') or cfg.get('telegram_chat_id') or '')
    owner = owner or os.environ.get('SPACEDUCK_FWD_TG_CHAT', '').strip()
    ls = procs_for_home('telegram_listener.py')
    port = args.tg_port
    for _, c in ls:
        if '--port' in c:
            try:
                port = int(c.split('--port')[1].split()[0])
            except (ValueError, IndexError):
                pass
    issues = []
    if not ls:
        issues.append('listener not running')
    elif not any('--on-message' in c for _, c in ls):
        issues.append('listener MUTE (no --on-message brain)')
    if not owner:
        issues.append('no owner_chat_id in config (responder refuses all inbound)')
    if not issues and port:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/healthz', timeout=5) as r:
                json.loads(r.read())
        except Exception as e:
            issues.append(f'healthz on :{port} failed ({type(e).__name__})')
    owner_safe = f'…{owner[-3:]}' if owner else ''  # console is paste-safe; full id lives in the local JSON only
    if not issues:
        card.add('TG', 'telegram rail', OK,
                 f"brained listener on :{port or 'default'}, owner={owner_safe}")
        return True, port, owner
    # SAFE only when fix_tg can actually act: an owner id is resolvable AND
    # either a port is known (restart possible) or the running listener is
    # already brained (config-only write, no restart needed). A missing
    # listener with an unknown port is NOT auto-fixable — never label it SAFE.
    brained = bool(ls) and all('--on-message' in c for _, c in ls)
    fixable = bool(owner or args.owner_chat) and bool(port or brained)
    card.add('TG', 'telegram rail', FAIL, '; '.join(issues),
             tier='SAFE' if fixable else 'GATED',
             proposal=None if fixable else
             'need --tg-port and --owner-chat <id> (cannot invent the owner chat id or port)')
    return False, port, owner


def fix_tg(card, cfg, port, owner, args):
    if not owner and args.owner_chat:
        cfg['owner_chat_id'] = str(args.owner_chat)
        CONFIG.write_text(json.dumps(cfg, indent=2))
        CONFIG.chmod(0o600)
        owner = str(args.owner_chat)
        card.actions.append({'id': 'TG', 'action': f'wrote owner_chat_id={owner}',
                             'verified': True, 'detail': str(CONFIG)})
    if not (port and owner):
        return False
    ls = procs_for_home('telegram_listener.py')
    if ls and all('--on-message' in c for _, c in ls):
        # Listener already brained — the hook re-reads config per message,
        # so a config-only fix needs no restart. Don't bounce healthy rails.
        return True
    keep_flags = ['--owner-approval'] if any('--owner-approval' in c for _, c in ls) else []
    for pid, _ in ls:
        try:
            os.kill(pid, 15)
        except OSError:
            pass
    time.sleep(1)
    spawn_detached(['python3', str(SCRIPTS / 'telegram_listener.py'),
                    '--port', str(port), '--verbose', *keep_flags, '--on-message',
                    f'bash {SCRIPTS}/reply_with_claude.sh'],
                   SD_DIR / 'listener.log')
    time.sleep(3)
    ok = False
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/healthz', timeout=5) as r:
            ok = json.loads(r.read()).get('ok') is True
    except Exception:
        pass
    card.actions.append({'id': 'TG', 'action': f'restarted listener :{port} with --on-message brain',
                         'verified': ok, 'detail': ''})
    return ok


def check_claude(card, deep):
    """R3 — GATED. Detect only; the credential symlink is never automated."""
    cred = HOME / '.claude' / '.credentials.json'
    if not cred.exists():
        card.add('R3', 'claude auth', FAIL, f'{cred} missing', tier='GATED',
                 proposal='GATED symlink recipe (owner ack; only where a shared-host '
                          f'credential source is configured): ln -s <source>/.credentials.json {cred} '
                          "+ set hasCompletedOnboarding in ~/.claude.json — never copy secrets")
        return False
    if not deep:
        card.add('R3', 'claude auth', OK, 'credentials present (use --deep for a live test)')
        return True
    claude = resolve_claude()
    try:
        r = subprocess.run([claude, '-p', 'Reply AUTH_OK only.'], capture_output=True,
                           text=True, timeout=90, cwd='/tmp',
                           env={**os.environ, 'HOME': str(HOME)})
        live = r.returncode == 0 and 'AUTH_OK' in r.stdout
    except Exception:
        live = False
    card.add('R3', 'claude auth (live)', OK if live else FAIL,
             'AUTH_OK' if live else 'live probe failed', tier=None if live else 'GATED')
    return live


def check_soul(card):
    """Cosmetic — missing persona files make responder replies generic."""
    if any((SD_DIR / f).exists() for f in ('SOUL.md', 'doctrine.md')):
        card.add('SOUL', 'persona files', OK, 'present')
        return True
    card.add('SOUL', 'persona files', WARN, 'no SOUL.md/doctrine.md', tier='SAFE')
    return False


def fix_soul(card, cfg):
    SD_DIR.mkdir(mode=0o700, exist_ok=True)
    (SD_DIR / 'SOUL.md').write_text(
        f"# SOUL.md — {cfg.get('agent_name', 'this duck')}\n\n"
        "> ⚠ UNPERSONALIZED STUB — written by doctor_fix.py. Replace with a\n"
        "> real persona. Until then replies are generic.\n\n"
        "Helpful, honest, concise. Answers only what it can verify.\n")
    card.actions.append({'id': 'SOUL', 'action': 'wrote SOUL.md stub (unpersonalized marker)',
                         'verified': True, 'detail': str(SD_DIR / 'SOUL.md')})
    return True


# ── Orchestration: diagnose → treat(SAFE) → verify ────────────────────────────
def diagnose(args, treat=False):
    card = Card()
    cfg = load_cfg()
    if not check_identity(card, cfg):
        return card, cfg  # R6: nothing else is meaningful un-paired
    check_platform(card, cfg)
    if not check_pulse(card) and treat:
        fix_pulse(card)
    if not check_peck(card) and treat:
        fix_peck(card)
    tg_ok, port, owner = check_tg(card, cfg, args)
    if not tg_ok and treat:
        fix_tg(card, cfg, port, owner, args)
    check_claude(card, args.deep)
    if not check_soul(card) and treat:
        fix_soul(card, cfg)
    return card, cfg


def main():
    p = argparse.ArgumentParser(description='Space Duck doctor — diagnose/treat/verify')
    p.add_argument('--fix', action='store_true', help='treat SAFE-tier findings')
    p.add_argument('--json', action='store_true', help='print report card JSON')
    p.add_argument('--deep', action='store_true', help='live Claude auth probe (slow)')
    p.add_argument('--tg-port', type=int, help='telegram listener port if none is running')
    p.add_argument('--owner-chat', help='owner Telegram chat id (enables SAFE config write)')
    args = p.parse_args()

    first, cfg = diagnose(args, treat=args.fix)
    card = first
    if args.fix and first.actions:
        # R7 — the verify pass IS a fresh diagnosis, not a second code path.
        verify, _ = diagnose(args, treat=False)
        verify.actions, verify.proposals = first.actions, verify.proposals or first.proposals
        card = verify

    report = {
        'schema': 'space-duck.doctor_report.v1',
        'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'home': str(HOME),
        'agent': (cfg or {}).get('agent_name'),
        'spaceduck_id': (cfg or {}).get('spaceduck_id'),
        'mode': 'fix' if args.fix else 'diagnose',
        'checks': card.checks,
        'actions': card.actions,
        'proposals': card.proposals,
        'result': card.worst(),
    }
    if card.worst() == FAIL and args.fix:
        report['escalation'] = ('rail(s) still red after treatment — do NOT loop; '
                                'peck/Telegram the owner\'s operator duck')
    try:
        SD_DIR.mkdir(mode=0o700, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2))
    except Exception:
        pass

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        name = report.get('agent') or str(HOME)
        print(f"\n🩺 space-duck doctor — {name} ({report['mode']}) {report['ts']}")
        for c in card.checks:
            tier = f"  [{c['tier']}]" if c['tier'] and c['status'] != OK else ''
            print(f"  {GLYPH[c['status']]} {c['name']:<22} {c['detail']}{tier}")
        for a in card.actions:
            print(f"  → treated {a['id']}: {a['action']} — "
                  f"{'verified ✓' if a['verified'] else 'NOT verified ✗'}")
        for pr in card.proposals:
            print(f"  ▶ proposed [{pr['tier']}] {pr['id']}: {pr['action']}")
        print(f"  ─ result: {card.worst().upper()} · report: {REPORT_PATH}")

    sys.exit(0 if card.worst() == OK else (1 if card.worst() == WARN else 2))


if __name__ == '__main__':
    main()
