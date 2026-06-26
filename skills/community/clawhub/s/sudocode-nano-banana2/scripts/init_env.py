#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

ENV_PATH = Path.home() / '.openclaw' / '.env'
REQUIRED_KEYS = ['SUDOCODE_IMAGE_API_KEY']
OPTIONAL_DEFAULTS = {
    'SUDOCODE_BASE_URL': 'https://sudocode.run',
}


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        values[key] = value
    return values


def quote_env_value(value: str) -> str:
    escaped = value.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'


def write_env_file(path: Path, env_map: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f'{key}={quote_env_value(env_map[key])}' for key in sorted(env_map.keys())]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def prompt_value(key: str, current: str | None, prompt_text: str) -> str:
    suffix = f' [{current}]' if current else ''
    while True:
        entered = input(f'{prompt_text}{suffix}: ').strip()
        if entered:
            return entered
        if current:
            return current
        print(f'{key} 不能为空，请重试。')


def main() -> int:
    parser = argparse.ArgumentParser(description='Initialize Sudocode Nano Banana2 environment variables.')
    parser.add_argument('--check-only', action='store_true', help='Only check whether required variables exist.')
    parser.add_argument('--force', action='store_true', help='Prompt even if values already exist in .env or process env.')
    args = parser.parse_args()

    file_env = parse_env_file(ENV_PATH)
    effective_env = dict(file_env)
    for key in REQUIRED_KEYS + list(OPTIONAL_DEFAULTS.keys()):
        if os.getenv(key):
            effective_env[key] = os.getenv(key, '')

    missing = [key for key in REQUIRED_KEYS if not effective_env.get(key)]
    if args.check_only:
        if missing:
            print('缺少环境变量: ' + ', '.join(missing))
            print('请先前往 https://sudocode.us 注册并申请 API Key。')
            print(f'然后运行: uv run python {Path(__file__).resolve()}')
            return 1
        print(f'环境变量已就绪，来源文件: {ENV_PATH}')
        return 0

    needs_prompt = args.force or bool(missing)
    if not needs_prompt:
        print(f'环境变量已存在，无需初始化: {ENV_PATH}')
        return 0

    print('初始化 Sudocode Nano Banana2 环境变量')
    print(f'将写入: {ENV_PATH}')
    print('如果你还没有 API Key，请先前往 https://sudocode.us 注册并申请。')

    merged = dict(file_env)
    current_api_key = effective_env.get('SUDOCODE_IMAGE_API_KEY')
    merged['SUDOCODE_IMAGE_API_KEY'] = prompt_value(
        'SUDOCODE_IMAGE_API_KEY',
        current_api_key if args.force else None,
        '请输入 SUDOCODE_IMAGE_API_KEY'
    )

    current_base_url = effective_env.get('SUDOCODE_BASE_URL') or OPTIONAL_DEFAULTS['SUDOCODE_BASE_URL']
    base_url = input(f'请输入 SUDOCODE_BASE_URL [{current_base_url}]: ').strip()
    merged['SUDOCODE_BASE_URL'] = base_url or current_base_url

    write_env_file(ENV_PATH, merged)
    print(f'已写入环境变量文件: {ENV_PATH}')
    print('请重新打开会话，或在当前命令前临时 export 后再运行技能脚本。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
