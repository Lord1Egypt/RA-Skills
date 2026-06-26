#!/usr/bin/env python3

import sys
import os
import re
import json
import zipfile
import tempfile
import urllib.request
from pathlib import Path


DEFAULT_DOWNLOAD_URL = "https://wry-manatee-359.convex.site/api/v1/download?slug="
DOWNLOAD_TIMEOUT = 30
SCRIPT_MAX_BYTES = 50000
CONFIG_FILE = "skillwiki.ini"
ALLOWED_CONFIG_KEYS = {'CLAWHUB_DOWNLOAD_URL', 'SKILLWIKI_LANG'}

NOISE_DIRS = {'__pycache__', '.git', '__MACOSX', '.svn', '.hg', 'node_modules'}
NOISE_SUFFIXES = {'.pyc', '.pyo', '.DS_Store', '.gitkeep'}

ENV_VAR_PATTERNS = [
    re.compile(r'os\.environ\.get\s*\(\s*["\'](\w+)["\']'),
    re.compile(r'os\.getenv\s*\(\s*["\'](\w+)["\']'),
    re.compile(r'os\.environ\s*\[\s*["\'](\w+)["\']\s*\]'),
    re.compile(r'\$\{(\w+)\}'),
    re.compile(r'process\.env\.(\w+)'),
]

URL_PATTERN = re.compile(r'https?://[^\s"\'`<>\]\)}#,]+')


def _config_path():
    return Path(__file__).resolve().parent.parent / CONFIG_FILE


def _load_config():
    config_path = _config_path()
    config = {}
    lines = []
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and '=' in stripped:
                    key, _, value = stripped.partition('=')
                    config[key.strip()] = value.strip()
        except Exception:
            pass
    return config, lines


def _save_config(config, original_lines):
    config_path = _config_path()
    new_lines = []
    updated_keys = set()
    for line in original_lines:
        stripped = line.strip()
        is_commented = stripped.startswith('#') and '=' in stripped
        is_active = stripped and not stripped.startswith('#') and '=' in stripped
        if is_active or is_commented:
            key = stripped.lstrip('#').strip().partition('=')[0].strip()
            if key in config:
                new_lines.append(f"{key}={config[key]}\n")
                updated_keys.add(key)
            elif is_commented:
                new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    for key, value in config.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}\n")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def _get_config(key, default=''):
    config, _ = _load_config()
    return config.get(key, '') or default


def _set_config(key, value):
    config, lines = _load_config()
    config[key] = value
    _save_config(config, lines)


def parse_yaml_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    body = match.group(2).strip()
    frontmatter = {}
    current_key = None
    json_buffer = []
    in_json_block = False
    json_start_key = None
    json_brace_depth = 0
    folded_key = None
    folded_lines = []

    lines = frontmatter_str.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        if in_json_block:
            json_buffer.append(line)
            json_brace_depth += line.count('{') - line.count('}')
            if json_brace_depth <= 0:
                in_json_block = False
                json_str = '\n'.join(json_buffer)
                try:
                    frontmatter[json_start_key] = _parse_json_lenient(json_str)
                except json.JSONDecodeError:
                    frontmatter[json_start_key] = json_str
                json_buffer = []
                json_start_key = None
            i += 1
            continue

        if folded_key is not None:
            if line and not line[0].isspace():
                frontmatter[folded_key] = ' '.join(folded_lines)
                folded_key = None
                folded_lines = []
            else:
                stripped = line.strip()
                if stripped:
                    folded_lines.append(stripped)
                i += 1
                continue

        if not line.strip():
            i += 1
            continue

        if line.startswith('  ') and current_key:
            stripped = line.strip()
            if stripped.startswith('{'):
                json_brace_depth = stripped.count('{') - stripped.count('}')
                if json_brace_depth > 0:
                    in_json_block = True
                    json_buffer = [stripped]
                    json_start_key = current_key
                    frontmatter.pop(current_key, None)
                    current_key = None
                else:
                    try:
                        frontmatter[current_key] = _parse_json_lenient(stripped)
                    except json.JSONDecodeError:
                        frontmatter[current_key] = stripped
                    current_key = None
                i += 1
                continue
            if isinstance(frontmatter.get(current_key), list):
                item = stripped
                if item.startswith('- '):
                    item = item[2:].strip()
                frontmatter[current_key].append(item)
            i += 1
            continue

        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            if not value:
                frontmatter[key] = []
                current_key = key
            elif value in ('>', '|'):
                folded_key = key
                folded_lines = []
                current_key = None
            elif value.startswith('{'):
                json_brace_depth = value.count('{') - value.count('}')
                if json_brace_depth > 0:
                    in_json_block = True
                    json_buffer = [value]
                    json_start_key = key
                    current_key = None
                else:
                    try:
                        frontmatter[key] = _parse_json_lenient(value)
                    except json.JSONDecodeError:
                        frontmatter[key] = value
                    current_key = None
            elif value.startswith('[') and value.endswith(']'):
                items = [x.strip().strip('"').strip("'") for x in value[1:-1].split(',')]
                frontmatter[key] = [x for x in items if x]
                current_key = None
            else:
                frontmatter[key] = value.strip('"').strip("'")
                current_key = None

        i += 1

    if folded_key is not None:
        frontmatter[folded_key] = ' '.join(folded_lines)

    return frontmatter, body


def _parse_json_lenient(json_str):
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    return json.loads(json_str)


def extract_openclaw_requires(frontmatter):
    metadata = frontmatter.get('metadata', {})
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except json.JSONDecodeError:
            metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}

    openclaw = metadata.get('openclaw', {})
    if not isinstance(openclaw, dict):
        openclaw = {}

    requires = openclaw.get('requires', {})
    if not isinstance(requires, dict):
        requires = {}

    env_vars = requires.get('env', [])
    bins = requires.get('bins', [])

    if not isinstance(env_vars, list):
        env_vars = []
    if not isinstance(bins, list):
        bins = []

    return env_vars, bins


def scan_scripts_for_env_vars(scripts_content):
    found = set()
    for script_text in scripts_content.values():
        if not isinstance(script_text, str):
            continue
        for pattern in ENV_VAR_PATTERNS:
            for m in pattern.finditer(script_text):
                found.add(m.group(1))
    return sorted(found)


def scan_scripts_for_urls(scripts_content):
    found = set()
    for script_text in scripts_content.values():
        if not isinstance(script_text, str):
            continue
        for m in URL_PATTERN.finditer(script_text):
            found.add(m.group(0).rstrip('.,;:'))
    return sorted(found)


def _is_noise(path_obj):
    name = path_obj.name
    if name in NOISE_DIRS:
        return True
    if name in ('.DS_Store', 'Thumbs.db'):
        return True
    if any(name.endswith(s) for s in NOISE_SUFFIXES):
        return True
    return False


def _scan_skill_dir(skill_dir, frontmatter, body, env_vars, bins, extra_fields):
    files = []
    scripts_content = {}
    truncated_scripts = []
    for root, dirs, filenames in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in NOISE_DIRS]
        for filename in filenames:
            filepath = Path(root) / filename
            if _is_noise(filepath):
                continue
            rel = str(filepath.relative_to(skill_dir))
            files.append(rel)

            if filepath.suffix in ('.py', '.sh', '.bash', '.js', '.ts') or 'scripts' in rel:
                try:
                    script_text = filepath.read_text(encoding='utf-8')
                    if len(script_text.encode('utf-8')) <= SCRIPT_MAX_BYTES:
                        scripts_content[rel] = script_text
                    else:
                        scripts_content[rel] = f"(truncated, {len(script_text)} chars)"
                        truncated_scripts.append(rel)
                except:
                    pass

    detected_env = scan_scripts_for_env_vars(scripts_content)
    detected_urls = scan_scripts_for_urls(scripts_content)

    declared_env_set = set(env_vars) if isinstance(env_vars, list) else set()
    undeclared_env = sorted(set(detected_env) - declared_env_set)

    result = {
        "name": frontmatter.get('name', extra_fields.get('name_default', '')),
        "author": frontmatter.get('author', extra_fields.get('author', '')),
        "description": frontmatter.get('description', ''),
        "version": frontmatter.get('version', '') or extra_fields.get('extracted_version', ''),
        "license": frontmatter.get('license', '') or 'MIT-0',
        "homepage": frontmatter.get('homepage', ''),
        "env_vars": env_vars,
        "bins": bins,
        "undeclared_env_vars": undeclared_env,
        "detected_urls": detected_urls,
        "files": sorted(files),
        "scripts": scripts_content,
        "truncated_scripts": truncated_scripts,
        "body": body,
        "source": extra_fields.get('source', 'unknown'),
        "lang": _get_config('SKILLWIKI_LANG', 'en'),
    }
    if extra_fields.get('local_path'):
        result["local_path"] = extra_fields['local_path']
    if extra_fields.get('download_url'):
        result["download_url"] = extra_fields['download_url']
    return result


def fetch_skill(slug):
    download_url = _get_config('CLAWHUB_DOWNLOAD_URL', DEFAULT_DOWNLOAD_URL)
    url = f"{download_url}{slug}"

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "skill.zip")
        extracted_version = None

        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'SkillWiki/1.0')]
            urllib.request.install_opener(opener)
            with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT) as response:
                content_disp = response.headers.get('Content-Disposition', '')
                filename_match = re.search(r'filename[^;=\n]*=?[\'"]?([^\'";\n]+)', content_disp)
                if filename_match:
                    fname = filename_match.group(1).strip()
                    version_match = re.search(r'[-_@](\d+\.\d+(?:\.\d+)?)', fname)
                    if version_match:
                        extracted_version = version_match.group(1)
                with open(zip_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
        except Exception as e:
            return {"error": f"Failed to download skill: {e}"}

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(tmpdir)
        except Exception as e:
            return {"error": f"Failed to extract skill: {e}"}

        skill_dir = Path(tmpdir)
        if not (skill_dir / 'SKILL.md').exists() and not (skill_dir / 'skill.md').exists():
            for item in sorted(Path(tmpdir).iterdir()):
                if item.is_dir() and item.name not in NOISE_DIRS:
                    if (item / 'SKILL.md').exists() or (item / 'skill.md').exists():
                        skill_dir = item
                        break

        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            skill_md = skill_dir / 'skill.md'
        if not skill_md.exists():
            return {"error": "SKILL.md not found in skill package"}

        content = skill_md.read_text(encoding='utf-8')
        frontmatter, body = parse_yaml_frontmatter(content)
        env_vars, bins = extract_openclaw_requires(frontmatter)

        return _scan_skill_dir(
            skill_dir, frontmatter, body, env_vars, bins,
            {
                "source": "clawhub",
                "name_default": slug,
                "extracted_version": extracted_version or '',
                "download_url": url,
            }
        )


def main():
    config_cmd = None
    for i, a in enumerate(sys.argv[1:], 1):
        if a == '--config' and i + 1 < len(sys.argv):
            config_cmd = sys.argv[i + 1]
            break
        elif a.startswith('--config='):
            config_cmd = a.split('=', 1)[1]

    if config_cmd:
        if '=' not in config_cmd:
            print(f"Error: Invalid config format '{config_cmd}'. Use KEY=VALUE")
            sys.exit(1)
        key, _, value = config_cmd.partition('=')
        key = key.strip()
        value = value.strip()
        if key not in ALLOWED_CONFIG_KEYS:
            print(f"Error: Unknown config key '{key}'. Allowed: {', '.join(sorted(ALLOWED_CONFIG_KEYS))}")
            sys.exit(1)
        _set_config(key, value)
        print(f"Config updated: {key}={value}")
        sys.exit(0)

    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python fetch_skill.py <skill-slug> [output-file] [--lang CODE] [--config KEY=VALUE]")
        print()
        print("Downloads a skill from ClawHub and extracts structured data for LLM analysis.")
        print()
        print("Arguments:")
        print("  skill-slug      ClawHub skill slug (e.g. x-search)")
        print("  output-file     Optional: save JSON to file instead of stdout")
        print("  --lang CODE     Report language (e.g. en, zh, ja). Overrides config")
        print("  --config K=V    Set config key in skillwiki.conf (e.g., --config SKILLWIKI_LANG=zh)")
        print()
        print("Configuration (skillwiki.conf):")
        print("  CLAWHUB_DOWNLOAD_URL   Custom ClawHub API URL (default: builtin)")
        print("  SKILLWIKI_LANG         Report language (default: en)")
        sys.exit(0 if len(sys.argv) < 2 else 0)

    lang_arg = None
    args = []
    skip_next = False
    for a in sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if a.startswith('--lang'):
            if '=' in a:
                lang_arg = a.split('=', 1)[1]
            else:
                idx = sys.argv.index(a)
                if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith('-'):
                    lang_arg = sys.argv[idx + 1]
                    skip_next = True
        elif a.startswith('--config'):
            if '=' in a:
                pass
            else:
                idx = sys.argv.index(a)
                if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith('-'):
                    skip_next = True
        else:
            args.append(a)

    arg = args[0] if args else None
    output_file = args[1] if len(args) > 1 else None

    if not arg:
        print("Error: skill-slug required")
        sys.exit(1)

    result = fetch_skill(arg)

    if lang_arg:
        result["lang"] = lang_arg

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Data saved to: {output_file}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
