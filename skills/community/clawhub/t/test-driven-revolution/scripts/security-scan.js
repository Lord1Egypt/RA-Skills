#!/usr/bin/env node
/**
 * security-scan.js - 执行指令安全扫描
 * 检测危险命令模式，防止恶意/错误代码执行
 */

const fs = require('fs');
const path = require('path');

// 危险命令黑名单（正则表达式）
const DANGEROUS_PATTERNS = [
  { pattern: /rm\s+-rf\s+\/\s*$/, reason: '删除根目录' },
  { pattern: /rm\s+-rf\s+~\s*$/, reason: '删除用户主目录' },
  { pattern: /rm\s+-rf\s+\/\*/, reason: '删除所有根目录文件' },
  { pattern: /curl\s+[^|]+\|\s*(ba)?sh/, reason: '远程代码执行（curl | sh）' },
  { pattern: /wget\s+[^|]+\|\s*(ba)?sh/, reason: '远程代码执行（wget | sh）' },
  { pattern: /chmod\s+777/, reason: '设置全权限（chmod 777）' },
  { pattern: /\bsudo\b/, reason: '提权操作（sudo）' },
  { pattern: /dd\s+if=\/dev\/zero/, reason: '磁盘写入操作' },
  { pattern: /:\(\)\s*\{\s*:\|:&\s*\}\s*;/, reason: 'Fork Bomb' },
  { pattern: /\bmkfs\b/, reason: '格式化文件系统' },
  { pattern: /\bfdisk\b/, reason: '磁盘分区操作' },
  { pattern: /echo\s+[^>]+>\s+(\/etc|\/proc|\/sys)/, reason: '写入系统目录' },
  { pattern: /rm\s+-rf\s+\*\s*$/, reason: '删除当前目录所有文件' },
  { pattern: />\s*\/dev\/sd[a-z]/, reason: '直接写入磁盘设备' },
  { pattern: /nc\s+-e\s+(ba)?sh/, reason: '反向 Shell' },
  { pattern: /python\s+-c\s+['"].*socket/, reason: 'Python Socket 操作（可能为反向 Shell）' },
  { pattern: /base64\s+-d\s*\|\s*(ba)?sh/, reason: 'Base64 解码执行' },
  { pattern: /eval\s+\$/, reason: '动态执行变量内容' },
  { pattern: /`\$[^`]+`/, reason: '命令替换执行变量' },
];

// 允许的命令白名单（可选，严格模式下使用）
const ALLOWED_COMMANDS = [
  'node', 'npm', 'npx',
  'python', 'python3', 'pip', 'pip3',
  'bash', 'sh', 'zsh',
  'echo', 'cat', 'ls', 'pwd', 'mkdir', 'cp', 'mv',
  'grep', 'sed', 'awk', 'head', 'tail', 'wc',
  'git', 'diff', 'patch',
  'jq', 'node -e',
];

/**
 * 扫描指令中的危险模式
 * @param {string} instructions - 执行指令
 * @returns {{ safe: boolean, flags: Array<{pattern: string, reason: string, line: string}> }}
 */
function scanInstructions(instructions) {
  const flags = [];
  const lines = instructions.split('\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 跳过空行和注释
    if (!trimmed || trimmed.startsWith('#')) {
      continue;
    }
    
    for (const { pattern, reason } of DANGEROUS_PATTERNS) {
      if (pattern.test(trimmed)) {
        flags.push({
          pattern: pattern.source,
          reason,
          line: trimmed,
          severity: getSeverity(reason)
        });
      }
    }
  }
  
  return {
    safe: flags.length === 0,
    flags
  };
}

/**
 * 获取危险等级
 */
function getSeverity(reason) {
  const critical = ['删除根目录', '删除用户主目录', '远程代码执行', 'Fork Bomb', '格式化文件系统', '直接写入磁盘设备', '反向 Shell'];
  const high = ['提权操作', '磁盘分区操作', '写入系统目录', '动态执行'];
  
  if (critical.some(c => reason.includes(c))) {
    return 'CRITICAL';
  } else if (high.some(h => reason.includes(h))) {
    return 'HIGH';
  } else {
    return 'MEDIUM';
  }
}

/**
 * 扫描任务文件
 * @param {string} taskFile - 任务文件路径
 */
function scanTaskFile(taskFile) {
  if (!fs.existsSync(taskFile)) {
    console.error(`❌ 任务文件不存在：${taskFile}`);
    process.exit(1);
  }
  
  const task = JSON.parse(fs.readFileSync(taskFile, 'utf8'));
  
  if (!task.review || !task.review.next_instructions) {
    console.log('⚠️ 任务没有审阅指令，跳过扫描');
    console.log(JSON.stringify({
      task_id: task.task_id,
      safe: true,
      flags: [],
      message: 'No instructions to scan'
    }, null, 2));
    return;
  }
  
  const result = scanInstructions(task.review.next_instructions);
  
  const output = {
    task_id: task.task_id,
    safe: result.safe,
    flags: result.flags,
    scanned_at: new Date().toISOString()
  };
  
  console.log(JSON.stringify(output, null, 2));
  
  // 发现危险命令时返回非零退出码
  if (!result.safe) {
    process.exit(1);
  }
}

/**
 * 扫描字符串（管道输入）
 */
function scanStdin() {
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('readable', () => {
    let chunk;
    while ((chunk = process.stdin.read()) !== null) {
      input += chunk;
    }
  });
  process.stdin.on('end', () => {
    const result = scanInstructions(input);
    console.log(JSON.stringify(result, null, 2));
    if (!result.safe) {
      process.exit(1);
    }
  });
}

// 主程序
const args = process.argv.slice(2);

if (args.includes('--stdin') || args.includes('-')) {
  scanStdin();
} else if (args.length > 0) {
  const taskFile = args[0];
  scanTaskFile(taskFile);
} else {
  console.log('用法：');
  console.log('  node security-scan.js <task-file.json>   # 扫描任务文件');
  console.log('  node security-scan.js --stdin            # 从 stdin 读取指令');
  console.log('  echo "rm -rf /" | node security-scan.js --stdin');
  console.log('');
  console.log('退出码：');
  console.log('  0 - 安全，无危险命令');
  console.log('  1 - 发现危险命令');
  process.exit(0);
}
