#!/usr/bin/env python3
"""VPS Security Hardener — audit, harden, and monitor your Ubuntu VPS."""
import json, subprocess, os, sys

def audit():
    """Run security audit without making changes (FREE tier)"""
    results = {'ufw': False, 'fail2ban': False, 'sshd': {}, 'cve': []}
    
    # UFW check
    r = subprocess.run(['ufw', 'status'], capture_output=True, text=True, timeout=5)
    results['ufw'] = 'active' in r.stdout
    
    # fail2ban check
    r = subprocess.run(['fail2ban-client', 'status', 'sshd'], capture_output=True, text=True, timeout=5)
    results['fail2ban'] = r.returncode == 0
    
    # SSH config check
    for param in ['PermitRootLogin no', 'PasswordAuthentication no', 'PubkeyAuthentication yes']:
        key = param.split()[0]
        r = subprocess.run(['grep', '-E', f'^{key}', '/etc/ssh/sshd_config'], capture_output=True, text=True, timeout=5)
        results['sshd'][key] = param in r.stdout
    
    return results

def harden():
    """Apply full hardening (PAID tier)"""
    changes = []
    
    # UFW
    subprocess.run(['ufw', 'default', 'deny', 'incoming'], check=False)
    subprocess.run(['ufw', 'default', 'allow', 'outgoing'], check=False)
    changes.append('ufw: default deny incoming')
    
    # fail2ban
    with open('/etc/fail2ban/jail.local', 'w') as f:
        f.write('[sshd]\nenabled = true\nport = ssh\nfilter = sshd\nlogpath = /var/log/auth.log\nmaxretry = 3\nbantime = -1\nfindtime = 10m\n')
    subprocess.run(['systemctl', 'restart', 'fail2ban'], check=False)
    changes.append('fail2ban: bantime=-1 configured')
    
    # sysctl
    with open('/etc/sysctl.d/99-security.conf', 'w') as f:
        f.write('net.ipv4.conf.all.rp_filter = 1\nnet.ipv4.conf.all.accept_redirects = 0\nnet.ipv4.tcp_syncookies = 1\nnet.ipv4.icmp_echo_ignore_broadcasts = 1\n')
    subprocess.run(['sysctl', '-p', '/etc/sysctl.d/99-security.conf'], check=False)
    changes.append('sysctl: kernel hardened')
    
    return {'status': 'hardened', 'changes_applied': changes}

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if '--report' in args:
        result = audit()
    elif '--dry-run' in args:
        result = audit()
        result['would_change'] = ['ufw deny incoming', 'fail2ban bantime=-1', 'sysctl hardening']
    else:
        result = harden()
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
