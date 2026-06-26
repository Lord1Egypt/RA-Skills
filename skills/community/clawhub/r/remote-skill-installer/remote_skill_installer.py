#!/usr/bin/env python3
"""
远程技能安装助手
从 URL 安装、管理 OpenClaw Skills

Usage:
  python3 remote_skill_installer.py add --agent <id> --name <name> --source <url>
  python3 remote_skill_installer.py list
  python3 remote_skill_installer.py update --agent <id> --name <name>
  python3 remote_skill_installer.py remove --agent <id> --name <name>
  python3 remote_skill_installer.py import --agents <ids>
"""
import sys
import json
import pathlib
import argparse
import os
import urllib.request
import urllib.error
import hashlib
import re
import time
from pathlib import Path

OCLAW_HOME = Path.home() / '.openclaw'
OFFICIAL_SKILLS_HUB_BASE = 'https://raw.githubusercontent.com/openclaw-ai/skills-hub/main'
_FALLBACK_HUB_BASES = [
    'https://ghproxy.com/https://raw.githubusercontent.com/openclaw-ai/skills-hub/main',
    'https://raw.gitmirror.com/openclaw-ai/skills-hub/main',
]


def now_iso():
    """返回 UTC ISO 8601 时间字符串"""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def safe_name(s: str) -> bool:
    """检查名称是否只含安全字符"""
    return bool(re.match(r'^[a-zA-Z0-9_\\-\u4e00-\u9fff]+$', s))


def validate_url(url: str) -> bool:
    """校验 URL 合法性，防 SSRF"""
    from urllib.parse import urlparse
    import ipaddress
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('https', 'http'):
            return False
        if not parsed.hostname:
            return False
        # 禁止内网地址
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback or ip.is_reserved:
                return False
        except ValueError:
            pass
        return True
    except Exception:
        return False


def _download_file(url: str, timeout: int = 30, retries: int = 3) -> str:
    """从 URL 下载文件内容，支持重试"""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-SkillInstaller/1.0'})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                content = resp.read(10 * 1024 * 1024)
                return content.decode('utf-8')
        except urllib.error.HTTPError as e:
            last_error = f'HTTP {e.code}: {e.reason}'
            if e.code in (404, 403):
                break
        except urllib.error.URLError as e:
            last_error = f'网络错误: {e.reason}'
        except Exception as e:
            last_error = f'{type(e).__name__}: {e}'
        
        if attempt < retries:
            wait = attempt * 3
            print(f'   ⚠️ 第 {attempt} 次下载失败({last_error})，{wait}秒后重试...')
            time.sleep(wait)
    
    hint = ''
    if 'timed out' in str(last_error).lower() or '超时' in str(last_error):
        hint = '\n   💡 提示: 请设置代理 export https_proxy=http://proxy:port'
    elif '404' in str(last_error):
        hint = '\n   💡 提示: 官方 Skills Hub 可能尚未发布该 skill'
    raise Exception(f'{last_error} (已重试 {retries} 次){hint}')


def _compute_checksum(content: str) -> str:
    """计算内容校验和"""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def cmd_add(agent_id: str, name: str, source_url: str, description: str = '') -> bool:
    """从远程 URL 安装 skill"""
    if not safe_name(agent_id) or not safe_name(name):
        print(f'❌ 错误：agent_id 或 skill 名称含非法字符')
        return False
    
    if not validate_url(source_url):
        print(f'❌ 错误：URL 不合法或指向内网地址')
        return False
    
    workspace = OCLAW_HOME / f'workspace-{agent_id}' / 'skills' / name
    workspace.mkdir(parents=True, exist_ok=True)
    skill_md = workspace / 'SKILL.md'
    
    print(f'⏳ 正在从 {source_url} 下载...')
    try:
        content = _download_file(source_url)
    except Exception as e:
        print(f'❌ 下载失败：{e}')
        return False
    
    if len(content.strip()) < 10:
        print(f'❌ 文件内容过短或为空')
        return False
    
    skill_md.write_text(content, encoding='utf-8')
    
    source_info = {
        'skillName': name,
        'sourceUrl': source_url,
        'description': description,
        'addedAt': now_iso(),
        'lastUpdated': now_iso(),
        'checksum': _compute_checksum(content),
        'status': 'valid',
    }
    source_json = workspace / '.source.json'
    source_json.write_text(json.dumps(source_info, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f'✅ 技能 {name} 已添加到 {agent_id}')
    print(f'   路径: {skill_md}')
    print(f'   大小: {len(content)} 字节')
    return True


def cmd_list() -> bool:
    """列出所有已安装的远程 skills"""
    if not OCLAW_HOME.exists():
        print('❌ OCLAW_HOME 不存在')
        return False
    
    remote_skills = []
    
    for ws_dir in OCLAW_HOME.glob('workspace-*'):
        agent_id = ws_dir.name.replace('workspace-', '')
        skills_dir = ws_dir / 'skills'
        if not skills_dir.exists():
            continue
        
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_name = skill_dir.name
            source_json = skill_dir / '.source.json'
            
            if not source_json.exists():
                continue
            
            try:
                source_info = json.loads(source_json.read_text(encoding='utf-8'))
                remote_skills.append({
                    'agent': agent_id,
                    'skill': skill_name,
                    'source': source_info.get('sourceUrl', 'N/A'),
                    'desc': source_info.get('description', ''),
                    'added': source_info.get('addedAt', 'N/A'),
                })
            except Exception:
                pass
    
    if not remote_skills:
        print('📭 暂无远程 skills')
        print('   使用 `add` 命令安装第一个远程 skill！')
        return True
    
    print(f'📋 共 {len(remote_skills)} 个远程 skills：\n')
    print(f'{"Agent":<12} | {"Skill 名称":<20} | {"描述":<30} | 添加时间')
    print('-' * 100)
    
    for sk in remote_skills:
        desc = (sk['desc'] or sk['source'])[:30].ljust(30)
        print(f"{sk['agent']:<12} | {sk['skill']:<20} | {desc} | {sk['added'][:10]}")
    
    print()
    return True


def cmd_update(agent_id: str, name: str) -> bool:
    """更新远程 skill"""
    if not safe_name(agent_id) or not safe_name(name):
        print(f'❌ 错误：agent_id 或 skill 名称含非法字符')
        return False
    
    workspace = OCLAW_HOME / f'workspace-{agent_id}' / 'skills' / name
    source_json = workspace / '.source.json'
    
    if not source_json.exists():
        print(f'❌ 技能不存在或不是远程 skill: {name}')
        return False
    
    try:
        source_info = json.loads(source_json.read_text(encoding='utf-8'))
        source_url = source_info.get('sourceUrl')
        if not source_url:
            print(f'❌ 无效的源 URL')
            return False
        
        return cmd_add(agent_id, name, source_url, source_info.get('description', ''))
    except Exception as e:
        print(f'❌ 更新失败：{e}')
        return False


def cmd_remove(agent_id: str, name: str) -> bool:
    """移除远程 skill"""
    if not safe_name(agent_id) or not safe_name(name):
        print(f'❌ 错误：agent_id 或 skill 名称含非法字符')
        return False
    
    workspace = OCLAW_HOME / f'workspace-{agent_id}' / 'skills' / name
    source_json = workspace / '.source.json'
    
    if not source_json.exists():
        print(f'❌ 技能不存在或不是远程 skill: {name}')
        return False
    
    try:
        import shutil
        shutil.rmtree(workspace)
        print(f'✅ 技能 {name} 已从 {agent_id} 移除')
        return True
    except Exception as e:
        print(f'❌ 移除失败：{e}')
        return False


def _get_hub_url(skill_name):
    """获取 skill 的 Hub URL"""
    custom = OCLAW_HOME / 'skills-hub-url'
    if custom.exists():
        base = custom.read_text().strip()
    else:
        base = os.environ.get('OPENCLAW_SKILLS_HUB_BASE', OFFICIAL_SKILLS_HUB_BASE)
    return f'{base.rstrip("/")}/{skill_name}/SKILL.md'


OFFICIAL_SKILLS = {
    'code_review': _get_hub_url('code_review'),
    'api_design': _get_hub_url('api_design'),
    'security_audit': _get_hub_url('security_audit'),
    'data_analysis': _get_hub_url('data_analysis'),
    'doc_generation': _get_hub_url('doc_generation'),
    'test_framework': _get_hub_url('test_framework'),
}


def cmd_import(agent_ids: list) -> bool:
    """从官方 Skills Hub 批量导入"""
    if not agent_ids:
        print('❌ 请指定目标 Agent：')
        print('   python3 remote_skill_installer.py import --agents <agent1>,<agent2>')
        print('   示例：python3 remote_skill_installer.py import --agents dev,test,prod')
        return False
    
    total = 0
    success = 0
    failed = []
    
    for skill_name, url in OFFICIAL_SKILLS.items():
        for agent_id in agent_ids:
            total += 1
            effective_url = url
            
            # 主 URL 失败则尝试镜像
            for try_url in [url] + [f'{fb.rstrip("/")}/{skill_name}/SKILL.md' for fb in _FALLBACK_HUB_BASES]:
                ok = cmd_add(agent_id, skill_name, try_url, f'官方 skill：{skill_name}')
                if ok:
                    success += 1
                    break
                if try_url == url:
                    print(f'   🔄 尝试备用镜像...')
            else:
                failed.append(f'{agent_id}/{skill_name}')
    
    print(f'\n📊 导入完成：{success}/{total} 个 skills 成功')
    if failed:
        print(f'\n❌ 失败列表:')
        for f in failed:
            print(f'   - {f}')
        print(f'\n💡 排查建议:')
        print(f'   1. 设置代理: export https_proxy=http://your-proxy:port')
        print(f'   2. 使用镜像: export OPENCLAW_SKILLS_HUB_BASE=https://ghproxy.com/{OFFICIAL_SKILLS_HUB_BASE}')
    
    return success == total


def main():
    parser = argparse.ArgumentParser(
        description='🛠️ 远程技能安装助手 - 从 URL 安装和管理 OpenClaw Skills',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='cmd', help='命令')
    
    # add
    add_parser = subparsers.add_parser('add', help='从远程 URL 添加 skill')
    add_parser.add_argument('--agent', required=True, help='目标 Agent ID')
    add_parser.add_argument('--name', required=True, help='Skill 内部名称')
    add_parser.add_argument('--source', required=True, help='远程 URL')
    add_parser.add_argument('--desc', default='', help='Skill 描述')
    
    # list
    subparsers.add_parser('list', help='列出所有远程 skills')
    
    # update
    update_parser = subparsers.add_parser('update', help='更新远程 skill')
    update_parser.add_argument('--agent', required=True, help='Agent ID')
    update_parser.add_argument('--name', required=True, help='Skill 名称')
    
    # remove
    remove_parser = subparsers.add_parser('remove', help='移除远程 skill')
    remove_parser.add_argument('--agent', required=True, help='Agent ID')
    remove_parser.add_argument('--name', required=True, help='Skill 名称')
    
    # import
    import_parser = subparsers.add_parser('import', help='从官方库导入 skills')
    import_parser.add_argument('--agents', default='', help='逗号分隔的 Agent IDs')
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return
    
    if args.cmd == 'add':
        ok = cmd_add(args.agent, args.name, args.source, args.desc)
        sys.exit(0 if ok else 1)
    elif args.cmd == 'list':
        ok = cmd_list()
        sys.exit(0 if ok else 1)
    elif args.cmd == 'update':
        ok = cmd_update(args.agent, args.name)
        sys.exit(0 if ok else 1)
    elif args.cmd == 'remove':
        ok = cmd_remove(args.agent, args.name)
        sys.exit(0 if ok else 1)
    elif args.cmd == 'import':
        agent_list = [a.strip() for a in args.agents.split(',') if a.strip()]
        ok = cmd_import(agent_list)
        sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
