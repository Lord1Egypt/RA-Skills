#!/usr/bin/env node
/**
 * Security Audit Assistant - Core Scanner
 * Runs CIS-inspired baseline checks on managed nodes
 * Output: Human-readable report + fix commands
 */

// OpenClaw node.exec interface
// This script is meant to be run via: openclaw skill run security-audit-assistant

const checks = [
  {
    id: 'ssh_password_auth',
    name: 'SSH Password Authentication',
    risk: 'high',
    command: 'grep -E "^PasswordAuthentication" /etc/ssh/sshd_config | awk \'{print $2}\'',
    expected: 'no',
    fix: "sudo sed -i 's/PasswordAuthentication yes/no/' /etc/ssh/sshd_config && sudo systemctl restart sshd",
    os: ['ubuntu', 'debian', 'centos']
  },
  {
    id: 'ssh_root_login',
    name: 'SSH Root Login',
    risk: 'high',
    command: 'grep -E "^PermitRootLogin" /etc/ssh/sshd_config | awk \'{print $2}\'',
    expected: 'no',
    fix: "sudo sed -i 's/PermitRootLogin yes/no/' /etc/ssh/sshd_config && sudo systemctl restart sshd",
    os: ['ubuntu', 'debian', 'centos']
  },
  {
    id: 'ufw_enabled',
    name: 'Firewall (UFW) Enabled',
    risk: 'high',
    command: 'systemctl is-active ufw || echo "inactive"',
    expected: 'active',
    fix: "sudo ufw enable && sudo ufw default deny incoming",
    os: ['ubuntu', 'debian']
  },
  {
    id: 'firewalld_enabled',
    name: 'Firewall (firewalld) Enabled',
    risk: 'high',
    command: 'systemctl is-active firewalld || echo "inactive"',
    expected: 'active',
    fix: "sudo systemctl enable --now firewalld && sudo firewall-cmd --set-default-zone=drop",
    os: ['centos', 'rhel']
  },
  {
    id: 'security_updates',
    name: 'Pending Security Updates',
    risk: 'medium',
    command: 'apt list --upgradable 2>/dev/null | grep -i security || echo "none"',
    expected: 'none',
    fix: "sudo apt update && sudo apt upgrade -y",
    os: ['ubuntu', 'debian']
  },
  {
    id: 'password_aging',
    name: 'Password Aging Enabled',
    risk: 'medium',
    command: 'grep -E "^\s*PASS_MAX_DAYS\s+90" /etc/login.defs || echo "not_set"',
    expected: 'PASS_MAX_DAYS',
    fix: "sudo sed -i 's/^#*PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs",
    os: ['ubuntu', 'debian', 'centos']
  },
  {
    id: 'auditd_running',
    name: 'Audit Daemon (auditd)',
    risk: 'medium',
    command: 'systemctl is-active auditd || echo "inactive"',
    expected: 'active',
    fix: "sudo apt install auditd audispd-plugins -y && sudo systemctl enable --now auditd",
    os: ['ubuntu', 'debian']
  },
  {
    id: 'rsyslog_running',
    name: 'System Logging (rsyslog)',
    risk: 'medium',
    command: 'systemctl is-active rsyslog || echo "inactive"',
    expected: 'active',
    fix: "sudo systemctl enable --now rsyslog",
    os: ['ubuntu', 'debian']
  },
  {
    id: 'ssh_protocol',
    name: 'SSH Protocol 2 Only',
    risk: 'high',
    command: 'grep -E "^Protocol" /etc/ssh/sshd_config | awk \'{print $2}\'',
    expected: '2',
    fix: "sudo sed -i 's/^Protocol.*/Protocol 2/' /etc/ssh/sshd_config && sudo systemctl restart sshd",
    os: ['ubuntu', 'debian', 'centos']
  },
  {
    id: 'permissions_passwd',
    name: '/etc/passwd Permissions',
    risk: 'high',
    command: 'stat -c %a /etc/passwd',
    expected: '644',
    fix: "sudo chmod 644 /etc/passwd",
    os: ['ubuntu', 'debian', 'centos']
  },
  {
    id: 'permissions_shadow',
    name: '/etc/shadow Permissions',
    risk: 'high',
    command: 'stat -c %a /etc/shadow',
    expected: '640',
    fix: "sudo chmod 640 /etc/shadow",
    os: ['ubuntu', 'debian', 'centos']
  }
];

// Mock node.exec for local testing (OpenClaw provides real one)
async function runCommand(cmd) {
  // In real execution, this uses OpenClaw's node.exec API
  // For now, simulate success
  return { stdout: '', stderr: '', code: 0 };
}

async function auditNode(nodeInfo) {
  const results = [];
  const os = await detectOS();

  for (const check of checks) {
    if (!check.os.includes(os)) continue;

    const { stdout } = await runCommand(check.command);
    const passed = stdout.trim() === check.expected || (check.expected === 'none' && stdout === 'none');

    results.push({
      ...check,
      passed,
      actual: stdout.trim(),
      recommendation: passed ? null : check.fix
    });
  }

  return { node: nodeInfo.name, os, results };
}

async function detectOS() {
  const { stdout } = await runCommand('cat /etc/os-release | grep ^ID= | cut -d= -f2 | tr -d \'"\'');
  const id = stdout.trim();
  if (id.includes('ubuntu') || id.includes('debian')) return 'ubuntu';
  if (id.includes('centos') || id.includes('rhel')) return 'centos';
  return 'unknown';
}

function generateReport(audit) {
  const passed = audit.results.filter(r => r.passed).length;
  const failed = audit.results.filter(r => !r.passed).length;
  const total = audit.results.length;

  let out = `\n🔍 Security Audit Report - ${audit.node} (${new Date().toISOString().split('T')[0]})\n\n`;
  out += `✅ PASS: ${passed}\n`;
  out += `❌ FAIL: ${failed}\n`;
  out += `📊 Total: ${total} checks\n\n`;

  if (failed > 0) {
    out += `🚨 HIGH RISK ISSUES:\n`;
    audit.results.filter(r => !r.passed && r.risk === 'high').forEach(r => {
      out += `${r.id}. ${r.name}\n`;
      out += `   Actual: ${r.actual}\n`;
      out += `   Fix: ${r.recommendation}\n\n`;
    });

    out += `⚠️  MEDIUM RISK ISSUES:\n`;
    audit.results.filter(r => !r.passed && r.risk === 'medium').forEach(r => {
      out += `${r.id}. ${r.name}\n`;
      out += `   Actual: ${r.actual}\n`;
      out += `   Fix: ${r.recommendation}\n\n`;
    });
  } else {
    out += `🎉 All checks passed! Your node meets basic security baseline.\n`;
  }

  out += `\n---\nReport generated by Security Audit Assistant (v1.0)\n`;
  return out;
}

// Main entry point (OpenClaw skill runtime)
(async () => {
  const nodeName = process.argv[2] || 'localhost';
  const audit = await auditNode({ name: nodeName });
  console.log(generateReport(audit));
})().catch(console.error);
