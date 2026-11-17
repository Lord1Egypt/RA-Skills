"""
rules.py - Anomaly detection over captured runtime behaviors.

Turns raw behaviors (network/file/process/env/exec) into normalized findings
with a severity. Findings mirror the static ScanResult shape so audit.py can
merge them into the same report and scoring pipeline.

High-risk signals:
  - Access to sensitive paths (~/.ssh, /etc/passwd, /etc/shadow, .aws, .env ...)
  - Outbound network to a non-whitelisted host/IP
  - Download-then-execute (network activity + exec/compile in the same run)
  - Spawning shells / interpreters (bash, sh, powershell, cmd)
  - Reading credential-like environment variables
"""

import re

# Sensitive filesystem paths (substring match, case-insensitive).
SENSITIVE_PATHS = [
    '/.ssh', '\\.ssh',
    '/etc/passwd', '/etc/shadow',
    '/.aws', '\\.aws',
    '/.docker/config', '\\.docker\\config',
    '/.kube', '\\.kube',
    'id_rsa', 'id_ed25519',
    '.env', '.netrc', '.git-credentials',
    'wallet.dat', '.gnupg',
]

# Shell / interpreter spawns worth flagging.
SHELL_TOKENS = ['bash', '/sh', 'sh ', 'powershell', 'cmd.exe', 'cmd /', '/bin/sh', 'zsh']

# Environment variables that often hold secrets.
SECRET_ENV_HINTS = [
    'token', 'secret', 'password', 'passwd', 'apikey', 'api_key',
    'access_key', 'private', 'credential',
]


def _finding(category, severity, message, suggestion, detail=None):
    return {
        'category': category,
        'severity': severity,
        'file': '<runtime>',
        'line': 0,
        'message': message,
        'pattern': 'dynamic',
        'suggestion': suggestion,
        'source': 'sandbox',
        'detail': detail or {},
    }


def _host_from_address(address):
    """Extract a host/ip token from a captured address string."""
    if not address:
        return None
    m = re.search(r"['\"]?([\w\.\-:]+)['\"]?\s*,\s*(\d+)", address)
    if m:
        return m.group(1)
    m = re.search(r'([0-9]{1,3}(?:\.[0-9]{1,3}){3})', address)
    if m:
        return m.group(1)
    m = re.search(r'([a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,})', address)
    if m:
        return m.group(1)
    return address


def _is_whitelisted(host, whitelist):
    if not host:
        return False
    for w in (whitelist or []):
        if w and w.lower() in host.lower():
            return True
    return False


def evaluate(behaviors, options=None):
    """Evaluate behaviors -> list of finding dicts."""
    whitelist = getattr(options, 'whitelist_domains', []) if options else []
    findings = []

    saw_network = False
    saw_exec = False

    for b in behaviors:
        btype = b.get('type')
        detail = b.get('detail', {})

        if btype == 'file':
            path = str(detail.get('path', ''))
            low = path.lower()
            for sp in SENSITIVE_PATHS:
                if sp.lower() in low:
                    findings.append(_finding(
                        'dynamic_sensitive_path', 'critical',
                        f'运行时访问敏感路径: {path[:80]}',
                        '确认脚本是否需要读取该敏感文件；若非必要请移除相关代码',
                        detail={'path': path},
                    ))
                    break

        elif btype == 'network':
            saw_network = True
            addr = detail.get('address') or detail.get('url') or ''
            host = _host_from_address(str(addr))
            if not _is_whitelisted(host, whitelist):
                findings.append(_finding(
                    'dynamic_network_egress', 'high',
                    f'运行时向未知目标发起网络连接: {str(addr)[:80]}',
                    '确认外联目标是否可信；沙箱默认断网，仅放行白名单域名',
                    detail={'target': str(addr)},
                ))

        elif btype == 'process':
            saw_exec = True
            cmd = str(detail.get('cmd', ''))
            low = cmd.lower()
            for tok in SHELL_TOKENS:
                if tok in low:
                    findings.append(_finding(
                        'dynamic_shell_spawn', 'high',
                        f'运行时创建 shell/解释器进程: {cmd[:80]}',
                        '避免运行时拼接命令调用 shell，改用参数化调用',
                        detail={'cmd': cmd},
                    ))
                    break

        elif btype == 'exec':
            saw_exec = True

        elif btype == 'env':
            key = str(detail.get('key', ''))
            low = key.lower()
            for hint in SECRET_ENV_HINTS:
                if hint in low:
                    findings.append(_finding(
                        'dynamic_secret_env_read', 'medium',
                        f'运行时读取疑似密钥环境变量: {key[:60]}',
                        '确认是否需要读取该环境变量；避免将密钥外传',
                        detail={'key': key},
                    ))
                    break

    # Correlation rule: download-then-execute in the same run.
    if saw_network and saw_exec:
        findings.append(_finding(
            'dynamic_download_and_execute', 'critical',
            '运行时同时出现网络活动与动态代码执行，疑似下载并执行远程载荷',
            '严禁下载后直接执行远程代码；如确有需要请校验来源与签名',
        ))

    return findings
