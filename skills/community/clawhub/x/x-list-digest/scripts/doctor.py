"""Local structural readiness; does not execute external commands or inspect credentials."""
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from config import load

ROOT = Path(__file__).resolve().parents[1]

def native_hermes_checks():
    home=Path.home()/'.hermes'
    return {'browser_preflight_argv':[str(home/'hermes-agent/.venv/bin/python'),str(ROOT/'scripts/browser_preflight.py')],
            'browser_endpoint':'http://127.0.0.1:9234','browser_profile':str(home/'chrome-debug'),
            'browser_profile_exists':(home/'chrome-debug').is_dir(),
            'hermes_python_exists':(home/'hermes-agent/.venv/bin/python').exists(),
            'x_login':'requires_native_browser_list_check',
            'scheduler':'requires_running_gateway_and_awake_host'}

def native_feishu_checks(config):
    """Return explicit native read-only commands; never use the default identity."""
    feishu=config.get('feishu')
    if not feishu:return None
    profile=feishu.get('profile')
    if not isinstance(profile,str) or not profile.strip():raise ValueError('feishu.profile is required for native auth checks')
    executable=feishu.get('executable','lark-cli')
    # lark-cli auto-selects Hermes' channel binding when HERMES_HOME is inherited.
    # Remove that signal only in the native CLI child; preserve the host environment.
    prefix=['/usr/bin/env','-u','HERMES_HOME',executable]
    checks={'profile':profile,'identity':'user','native_cli_prefix':prefix,'auth_status_argv':prefix+['auth','status','--json','--verify','--profile',profile]}
    if feishu.get('root_folder_token'):
        checks['folder_read_argv']=prefix+['drive','files','list','--params',json.dumps({'folder_token':feishu['root_folder_token'],'page_size':200}),'--as','user','--profile',profile]
    return checks

if __name__ == '__main__':
    config = load(ROOT / 'config.yaml')
    print(json.dumps({
        'python': sys.version.split()[0],
        'dependencies': {name: bool(importlib.util.find_spec(name)) for name in ('yaml', 'croniter')},
        'lists': config['lists'],
        'data_dir_default': str(Path.home() / '.local/share/x-list-digest'),
        'lark_cli_found': bool(shutil.which((config.get('feishu') or {}).get('executable', 'lark-cli'))),
        'feishu_auth': 'requires_native_status_check',
        'native_feishu_checks': native_feishu_checks(config),
        'native_hermes_checks': native_hermes_checks(),
        'browser': 'requires_host_login_and_list_access_check',
        'hosts': {name: (Path.home() / directory / 'x-list-digest/SKILL.md').exists()
                  for name, directory in {'codex': '.agents/skills', 'hermes': '.hermes/skills'}.items()},
    }, ensure_ascii=False, indent=2))
