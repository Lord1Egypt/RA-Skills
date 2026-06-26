/**
 * 尸狗·警觉魄 - 安全检测模块
 * 
 * 基于 Claude Code permissionDenials 机制设计
 * 实现：安全检查、报告生成、命令脱敏
 */

const SENSITIVE_PATTERNS = [
  // 密钥/Token
  { pattern: /sk-[a-zA-Z0-9]{20,}/g, replacement: 'sk-***REDACTED***' },
  { pattern: /api[_-]?key["\s]*[=:]["\s]*[a-zA-Z0-9]{10,}/gi, replacement: 'api_key=***REDACTED***' },
  { pattern: /bearer["\s]+[a-zA-Z0-9_-]{20,}/gi, replacement: 'Bearer ***REDACTED***' },
  { pattern: /token["\s]*[=:]["\s]*[a-zA-Z0-9_-]{20,}/gi, replacement: 'token=***REDACTED***' },
  
  // 密码
  { pattern: /password["\s]*[=:]["\s]*[^\s,"]+/gi, replacement: 'password=***REDACTED***' },
  { pattern: /passwd["\s]*[=:]["\s]*[^\s,"]+/gi, replacement: 'passwd=***REDACTED***' },
  
  // IP/端口（内部网络）
  { pattern: /192\.168\.\d{1,3}\.\d{1,3}/g, replacement: '192.168.***.***' },
  { pattern: /10\.\d{1,3}\.\d{1,3}\.\d{1,3}/g, replacement: '10.***.***.***' },
  { pattern: /172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}/g, replacement: '172.***.***.***' },
  
  // 文件路径（脱敏用户目录）
  { pattern: /C:\\Users\\[^\\]+/gi, replacement: 'C:\\Users\\***' },
  { pattern: /\/home\/[^\/]+/g, replacement: '/home/***' },
  { pattern: /\/Users\/[^\/]+/g, replacement: '/Users/***' },
]

// 危险命令关键词
const DANGEROUS_COMMANDS = [
  'rm -rf', 'del /f /s /q', 'format', 'dd if=',
  'drop table', 'delete from', 'truncate', 'alter table',
  'eval(', 'exec(', 'system(', 'shell_exec(',
  '--no-sandbox', '--privileged', 'chmod 777',
]

// 提示词注入模式
const PROMPT_INJECTION_PATTERNS = [
  { pattern: /ignore previous instructions/gi, type: 'prompt_injection' },
  { pattern: /ignore all previous commands/gi, type: 'prompt_injection' },
  { pattern: /disregard your instructions/gi, type: 'prompt_injection' },
  { pattern: /you are now a different/gi, type: 'prompt_injection' },
  { pattern: /forget everything above/gi, type: 'prompt_injection' },
  { pattern: /new instructions:/gi, type: 'prompt_injection' },
  { pattern: /<\|im_start\|>.*<\|im_end\|>/gi, type: 'prompt_injection' },
]

// 路径遍历模式
const PATH_TRAVERSAL_PATTERNS = [
  { pattern: /\.\.\/|\.\.\\/g, type: 'path_traversal' },
  { pattern: /\/etc\//g, type: 'path_traversal' },
  { pattern: /^[A-Z]:\\Windows\\/gi, type: 'path_traversal' },
]

// 严重性等级
const SEVERITY_MAP = {
  'prompt_injection': 'high',
  'dangerous_command': 'critical',
  'path_traversal': 'medium',
}

/**
 * 安全检查主函数
 */
function securityCheck(text, mode = 'full') {
  const threats = []
  
  if (mode === 'full' || mode === 'prompt_injection') {
    for (const { pattern, type } of PROMPT_INJECTION_PATTERNS) {
      const match = text.match(pattern)
      if (match) {
        threats.push({
          type,
          severity: SEVERITY_MAP[type] || 'medium',
          matched: match[0],
          position: text.indexOf(match[0]),
        })
      }
    }
  }
  
  if (mode === 'full' || mode === 'dangerous_command') {
    const lower = text.toLowerCase()
    for (const cmd of DANGEROUS_COMMANDS) {
      if (lower.includes(cmd.toLowerCase())) {
        threats.push({
          type: 'dangerous_command',
          severity: SEVERITY_MAP['dangerous_command'],
          matched: cmd,
        })
      }
    }
  }
  
  if (mode === 'full' || mode === 'path_traversal') {
    for (const { pattern, type } of PATH_TRAVERSAL_PATTERNS) {
      if (pattern.test(text)) {
        threats.push({
          type,
          severity: SEVERITY_MAP[type] || 'medium',
          matched: text.match(pattern)?.[0] || '..',
        })
      }
    }
  }
  
  return {
    safe: threats.length === 0,
    threats,
    summary: threats.length === 0 
      ? '✅ 未检测到威胁' 
      : `⚠️ 检测到 ${threats.length} 个潜在威胁`,
  }
}

/**
 * 脱敏命令
 */
function sanitizeCommand(command) {
  const removed = []
  let sanitized = command
  
  for (const { pattern, replacement } of SENSITIVE_PATTERNS) {
    const matches = sanitized.match(pattern)
    if (matches) {
      for (const match of matches) {
        removed.push({ original: match, pattern: pattern.toString() })
      }
      sanitized = sanitized.replace(pattern, replacement)
    }
  }
  
  return {
    original_length: command.length,
    sanitized,
    removed_patterns: removed.map(r => r.original),
  }
}

/**
 * 生成安全报告
 */
function generateReport(periodHours = 24) {
  const now = Date.now()
  const periodStart = now - periodHours * 60 * 60 * 1000
  
  // 模拟数据（实际应从记忆系统读取）
  return {
    period: {
      start: new Date(periodStart).toISOString(),
      end: new Date(now).toISOString(),
      hours: periodHours,
    },
    total_denials: 0,
    by_severity: { low: 0, medium: 0, high: 0, critical: 0 },
    by_type: {},
    suspicious_patterns: [],
    recommendations: [
      '当前未检测到明显安全威胁，继续保持监控',
      '建议定期检查权限配置是否合规',
    ],
    report_time: new Date(now).toISOString(),
    status: 'operational',
  }
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2)
  const command = args[0]
  
  if (command === 'check') {
    const text = args.slice(1).join(' ')
    const result = securityCheck(text)
    console.log(JSON.stringify(result, null, 2))
  } else if (command === 'sanitize') {
    const cmd = args.slice(1).join(' ')
    const result = sanitizeCommand(cmd)
    console.log(JSON.stringify(result, null, 2))
  } else if (command === 'report') {
    const hours = parseInt(args[1]) || 24
    const result = generateReport(hours)
    console.log(JSON.stringify(result, null, 2))
  } else {
    console.log('Usage:')
    console.log('  node security-check.js check <text>')
    console.log('  node security-check.js sanitize <command>')
    console.log('  node security-check.js report [hours]')
  }
}

module.exports = { securityCheck, sanitizeCommand, generateReport }
