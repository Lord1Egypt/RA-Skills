#!/usr/bin/env python3
"""setup_crons.py — self-improvement-loop v4.6.11: --force mode, no interactive prompts."""
import json, subprocess, sys, os, urllib.request, urllib.error, re, datetime, pathlib, argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOADS_FILE = os.path.join(SCRIPT_DIR, 'cron-payloads.json')
OPENCLAW_JSON = os.path.expanduser('~/.openclaw/openclaw.json')

# Per-agent support: Load agents from openclaw.json
def load_agent_config():
    """Load agent configurations from openclaw.json.

    Returns:
        List of dicts with 'id', 'workspace', 'channel', 'account', 'user_id' keys.
        Auto-detects first available channel from openclaw.json.
    """
    try:
        with open(OPENCLAW_JSON) as f:
            config = json.load(f)
        agents = config.get('agents', {}).get('list', [])
        channels_cfg = config.get('channels', {})

        # Auto-detect first available channel
        first_channel = None
        first_channel_account = None
        for channel_name, cfg in channels_cfg.items():
            if isinstance(cfg, dict):
                accounts = cfg.get('accounts', {})
                if accounts:
                    first_channel = channel_name
                    first_channel_account = list(accounts.keys())[0]
                    break

        if not first_channel:
            first_channel = 'telegram'
            first_channel_account = 'default'

        if agents:
            # Extract user_id from first channel's first account
            user_id = ''
            first_account_cfg = channels_cfg.get(first_channel, {}).get('accounts', {}).get(first_channel_account, {})
            user_ids = first_account_cfg.get('allowFrom', [])
            if user_ids:
                user_id = user_ids[0]

            result = []
            for a in agents:
                agent_id = a.get('id', 'main')
                # Use per-agent channel config if available
                # Read bindings for per-agent accountId routing
                bindings_list = config.get('bindings', [])
                binding_by_agent = {b.get('agentId'): b.get('match', {}).get('accountId')
                                    for b in bindings_list}

                agent_channel_cfg = a.get('channel', {}).get(first_channel, {})
                agent_channel = agent_channel_cfg.get('channel', first_channel)
                # Prefer binding's accountId over agent config (v4.6.13: fix cron delivery routing)
                agent_account = binding_by_agent.get(agent_id) or agent_channel_cfg.get('account', first_channel_account)

                result.append({
                    'id': agent_id,
                    'workspace': a.get('workspace', os.path.expanduser('~/.openclaw/workspace')),
                    'channel': agent_channel,
                    'account': agent_account,
                    'user_id': user_id,  # v4.6.11: populate from first channel's allowFrom
                })
            return result
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass

    # Fallback: main agent only
    return [{'id': 'main', 'workspace': os.path.expanduser('~/.openclaw/workspace'),
             'channel': 'telegram', 'account': 'default', 'user_id': ''}]

# Alias for backwards compatibility
AGENTS = None  # Deprecated, use load_agent_config()

# Auto-detect user ID from first available channel
def detect_user_id():
    """Detect user ID from first available channel (channel-agnostic)."""
    path = os.path.expanduser('~/.openclaw/openclaw.json')
    if not os.path.exists(path):
        return os.environ.get('TELEGRAM_ID', '')
    with open(path) as f:
        d = json.load(f)
        channels = d.get('channels', {})
        # Use first available channel
        for channel_name, cfg in channels.items():
            if isinstance(cfg, dict):
                accounts = cfg.get('accounts', {})
                for account_name in (list(accounts.keys()) if accounts else ['default']):
                    if account_name in accounts:
                        ids = accounts[account_name].get('allowFrom', [])
                        if ids:
                            return ids[0]
                ids = cfg.get('allowFrom', [])
                if ids:
                    return ids[0]
    return os.environ.get('TELEGRAM_ID', '')

def read_payloads():
    """Read cron payloads (no global injection — per-agent values set later)."""
    with open(PAYLOADS_FILE) as f:
        payloads = json.load(f)

    # Warn if sessionTarget=current but using CLI (CLI only supports main/isolated)
    for name, job in payloads.items():
        if job.get('sessionTarget') == 'current':
            print(f"  ⚠ {name}: sessionTarget=current (requires API, not CLI)")
    return payloads

def create_via_api(name, job_config):
    """Create cron via gateway API (preferred — supports sessionTarget=current)."""
    gateway_url = os.environ.get('OPENCLAW_GATEWAY_URL', 'http://localhost:18789')

    # Read token from environment (OPENCLAW_AUTH_TOKEN is what gateway uses)
    token = os.environ.get('OPENCLAW_GATEWAY_TOKEN', '')
    if not token:
        # Also check the actual env var that gateway uses
        token = os.environ.get('OPENCLAW_AUTH_TOKEN', '')

    api_payload = {
        'name': name,
        'schedule': job_config.get('schedule', {}),
        'sessionTarget': job_config.get('sessionTarget', 'isolated'),
        'payload': job_config.get('payload', {}),
        'delivery': job_config.get('delivery', {}),
        'enabled': job_config.get('enabled', True),
    }

    req = urllib.request.Request(
        f'{gateway_url}/api/cron/jobs',
        data=json.dumps(api_payload).encode(),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(f"  ✓ {name} created (API)")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"  ⚠ {name} API error {e.code}: {body}")
        return False
    except Exception as e:
        print(f"  ⚠ {name} API error: {e}")
        return False

def create_via_cli(name, job_config, agent_id=None):
    """Create cron via openclaw CLI (fallback — does NOT support sessionTarget=current)."""
    schedule = job_config.get('schedule', {})
    schedule_kind = schedule.get('kind', 'every')
    payload = job_config.get('payload', {})
    delivery = job_config.get('delivery', {})
    session_target = job_config.get('sessionTarget', 'isolated')

    # CLI only supports main|isolated — warn if current
    if session_target == 'current':
        print(f"  ⚠ {name}: CLI does not support sessionTarget=current, using isolated")
        session_target = 'isolated'

    # Extract agent_id from job name if not provided (e.g., "self-improvement-code-dev" → "code-dev")
    if not agent_id:
        agent_id = name.replace('self-improvement-', '') if name.startswith('self-improvement-') else ''

    # Resolve openclaw CLI path — it's node_modules/openclaw/openclaw.mjs
    import shutil
    openclaw_path = shutil.which('openclaw') or '/home/morav/.local/share/lib/node_modules/openclaw/openclaw.mjs'

    cmd = [
        'node', openclaw_path, 'cron', 'add',
        '--name', name,
        '--session', session_target,
        '--agent', agent_id,
    ]

    if schedule_kind == 'every':
        every_ms = schedule.get('everyMs', 1800000)
        # Convert ms to human-readable format for CLI
        if every_ms >= 3600000 and every_ms % 3600000 == 0:
            cmd += ['--every', f'{every_ms // 3600000}h']
        elif every_ms >= 60000 and every_ms % 60000 == 0:
            cmd += ['--every', f'{every_ms // 60000}m']
        else:
            cmd += ['--every', f'{every_ms}ms']
    elif schedule_kind == 'cron':
        cmd += ['--cron', schedule.get('expr', '')]
        if 'tz' in schedule:
            cmd += ['--tz', schedule['tz']]

    # CLI uses --timeout-seconds for agent jobs, --timeout for system events
    timeout_sec = payload.get('timeoutSeconds', 300)
    payload_kind = payload.get('kind', 'agentTurn')
    message_text = payload.get('message', '')

    # CLI uses --message for agentTurn, --system-event for systemEvent
    if payload_kind == 'agentTurn':
        cmd += ['--timeout-seconds', str(timeout_sec)]
        if message_text:
            cmd += ['--message', message_text]
    elif payload_kind == 'systemEvent':
        cmd += ['--timeout', str(timeout_sec)]
        cmd += ['--system-event', message_text or payload.get('text', '')]

    # Tools allow-list
    for tool in payload.get('toolsAllow', []):
        cmd += ['--tools', tool]

    # Delivery
    cmd += ['--deliver']
    cmd += ['--channel', delivery.get('channel', 'telegram')]
    if delivery.get('accountId'):
        cmd += ['--account', delivery['accountId']]
    if delivery.get('to'):
        cmd += ['--to', delivery['to']]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )

    if proc.returncode == 0:
        print(f"  ✓ {name} created (CLI)")
        return True
    else:
        print(f"  ✗ {name} CLI failed: {proc.stderr[:200]}")
        return False

def job_exists(name):
    """Check if a cron job with this name already exists."""
    r = subprocess.run(
        ['openclaw', 'cron', 'list', '--json'],
        capture_output=True, text=True, timeout=15
    )
    if r.returncode != 0:
        return False
    try:
        data = json.loads(r.stdout)
        for job in data.get('jobs', []):
            if job.get('name') == name:
                return True
    except:
        pass
    return False


def get_existing_job_message(name):
    """Return the raw payload.message of an existing job (no user ID injection)."""
    r = subprocess.run(
        ['openclaw', 'cron', 'list', '--json'],
        capture_output=True, text=True, timeout=15
    )
    if r.returncode != 0:
        return None
    try:
        data = json.loads(r.stdout)
        for job in data.get('jobs', []):
            if job.get('name') == name:
                return job.get('payload', {}).get('message', '')
    except:
        pass
    return None


def payloads_differ(canonical_msg, stored_msg):
    """Compare messages after stripping user ID placeholder AND injected numeric ID.
    canonical has <USER_ID>, stored has real numeric ID. Both must be normalized."""
    def strip(msg):
        msg = msg or ''
        msg = re.sub(r'<USER_ID>', '', msg)
        msg = re.sub(r'\d{6,}', '', msg)   # strip injected numeric user IDs
        return msg
    return strip(canonical_msg) != strip(stored_msg)


def write_stale_flag(name, canonical_msg, stored_msg):
    """Append a stale job entry to .stale_crons.json."""
    flag_path = pathlib.Path(os.path.expanduser('~/.openclaw/workspace/.learnings/.stale_crons.json'))
    flag_path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        'name': name,
        'detected_at': datetime.datetime.utcnow().isoformat() + 'Z',
        'reason': 'payload_stale',
        'canonical_msg': canonical_msg,
        'stored_msg': stored_msg,
    }

    if flag_path.exists():
        try:
            data = json.loads(flag_path.read_text())
        except Exception:
            data = {'jobs': [], 'action_required': 'FORCE_UPDATE=1 to sync, or ask your agent'}
        # De-duplicate by name
        names_in_file = {j['name'] for j in data.get('jobs', [])}
        if name not in names_in_file:
            data['jobs'].append(entry)
    else:
        data = {
            'jobs': [entry],
            'action_required': 'FORCE_UPDATE=1 to sync, or ask your agent'
        }

    flag_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def remove_job(name):
    """Delete an existing cron job by name."""
    r = subprocess.run(
        ['openclaw', 'cron', 'remove', name],
        capture_output=True, text=True, timeout=15
    )
    if r.returncode == 0:
        print(f"  ✓ {name} removed.")
        return True
    else:
        print(f"  ⚠ {name} remove failed: {r.stderr[:200]}")
        return False


def inject_learnings_dir(message, learnings_dir):
    """Inject LEARNINGS_DIR into all per-agent commands in the cron message.

    Handles:
    1. distill.sh --check-only (standalone and with output redirect)
    2. archive.sh --write-notified (needs LEARNINGS_DIR env var)
    3. PENDING_DIR (needs to be per-agent)
    """
    import re

    # 1. distill.sh commands - add LEARNINGS_DIR prefix
    # Matches: bash ~/.openclaw/.../distill.sh --check-only [> ...]
    pattern = r'(bash [^\s]+distill\.sh --check-only(?: > [^\n]+)?)'

    def replace_with_env(match):
        cmd = match.group(1)
        return f'LEARNINGS_DIR="{learnings_dir}" {cmd}'

    message = re.sub(pattern, replace_with_env, message)

    # 2. archive.sh - needs LEARNINGS_DIR
    # Matches: bash ~/.openclaw/.../archive.sh --write-notified
    pattern2 = r'(bash [^\s]+archive\.sh --write-notified)'

    def replace_archive(match):
        cmd = match.group(1)
        return f'LEARNINGS_DIR="{learnings_dir}" {cmd}'

    message = re.sub(pattern2, replace_archive, message)

    # 3. PENDING_DIR - per-agent path
    # Changes: PENDING_DIR="~/.openclaw/workspace/.learnings/.pending_notifications"
    # To: PENDING_DIR="~/.openclaw/workspace/agents/code-dev/.learnings/.pending_notifications"
    pending_dir = f'"{learnings_dir}/.pending_notifications"'
    message = message.replace(
        '"~/.openclaw/workspace/.learnings/.pending_notifications"',
        pending_dir
    )

    return message


def create_per_agent_job(agent, payloads, force=False):
    """Create per-agent self-improvement cron job with agent-specific LEARNINGS_DIR.

    Args:
        agent: dict with 'id', 'workspace', 'channel', 'account', 'user_id' keys
        payloads: dict of base payloads from cron-payloads.json
        force: if True, auto-replace stale jobs

    Returns:
        bool: True if job created successfully
    """
    agent_id = agent['id']
    workspace = agent.get('workspace', os.path.expanduser('~/.openclaw/workspace'))
    learnings_dir = f"{workspace}/.learnings"
    job_name = f"self-improvement-{agent_id}"

    print(f"\n  [{agent_id}] Setting up per-agent cron...")

    # Use the base payload (self-improvement-check) as template
    base_payload_name = 'self-improvement-check'
    if base_payload_name not in payloads:
        print(f"  ⚠ [{agent_id}] Base payload '{base_payload_name}' not found")
        return False

    import copy
    job_config = copy.deepcopy(payloads[base_payload_name])

    # Inject LEARNINGS_DIR into distill command
    original_msg = job_config['payload']['message']
    modified_msg = inject_learnings_dir(original_msg, learnings_dir)
    job_config['payload']['message'] = modified_msg

    # Update job name
    job_config['name'] = job_name

    # Per-agent delivery: use agent's channel/account
    agent_channel = agent.get('channel', 'telegram')
    agent_account = agent.get('account', 'default')
    agent_user_id = agent.get('user_id', '')  # v4.6.11: was 'telegram_id'

    job_config.setdefault('delivery', {})['channel'] = agent_channel
    if agent_account:
        job_config['delivery']['accountId'] = agent_account
    if agent_user_id:
        job_config['delivery']['to'] = agent_user_id
        modified_msg = modified_msg.replace('<USER_ID>', agent_user_id)
        job_config['payload']['message'] = modified_msg

    # Create the job
    if create_via_api(job_name, job_config):
        print(f"  ✓ [{agent_id}] Created {job_name} with LEARNINGS_DIR={learnings_dir}, channel={agent_channel}/{agent_account}")
        return True
    else:
        # Fallback to CLI
        print(f"  → [{agent_id}] Retrying via CLI...")
        return create_via_cli(job_name, job_config, agent_id)

def main():
    parser = argparse.ArgumentParser(description='Setup self-improvement-loop cron jobs')
    parser.add_argument('--force', action='store_true',
                        help='Auto-update stale jobs without prompting')
    parser.add_argument('--agent', action='store', default=None,
                        help='Create cron for specific agent only (default: all agents)')
    args = parser.parse_args()
    force = args.force
    target_agent = args.agent

    if force:
        print("Setting up cron jobs (--force mode)...")
    else:
        print("Setting up cron jobs...")

    channel = os.environ.get('CHANNEL', 'telegram')
    channel_account = os.environ.get('CHANNEL_ACCOUNT', '')
    user_id = os.environ.get('TELEGRAM_ID', '') or detect_user_id()

    print(f"  ✓ Channel: {channel}" + (f" (account: {channel_account})" if channel_account else ""))
    if user_id:
        print(f"  ✓ User ID detected: {user_id}")
    else:
        print("  ⚠ User ID not detected — set TELEGRAM_ID env var or check openclaw.json")

    # Load agents
    agents = load_agent_config()

    # Filter to specific agent if requested
    if target_agent:
        agents = [a for a in agents if a['id'] == target_agent]
        if not agents:
            print(f"  ⚠ Agent '{target_agent}' not found in openclaw.json")
            return

    print(f"  ✓ Found {len(agents)} agent(s): {[a['id'] for a in agents]}")

    # Read base payloads
    payloads = read_payloads()

    # Create per-agent cron jobs
    success_count = 0
    for agent in agents:
        try:
            if create_per_agent_job(agent, payloads, force):
                success_count += 1
        except Exception as e:
            print(f"  ⚠ [{agent['id']}] Error: {e}")

    print(f"\n✓ Created {success_count}/{len(agents)} per-agent cron jobs")

    print("\nCron setup complete.")

if __name__ == '__main__':
    main()
