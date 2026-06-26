#!/usr/bin/env node
/**
 * Safe Shell Executor v1.0.1
 * 只允许执行纯读取和查询类命令
 * 禁止：删除、修改、执行、下载、网络下载、提权等所有危险操作
 */

const ALLOWED_COMMANDS = [
  // 文件查看（只读）
  'ls', 'pwd', 'cat', 'head', 'tail', 'less', 'more', 'which', 'whereis',
  // 系统状态（只读）
  'ps', 'df', 'du', 'free', 'uptime', 'date', 'cal',
  // 网络诊断（只读）
  'ping', 'ifconfig', 'ip', 'netstat', 'ss', 'traceroute', 'nslookup', 'dig',
  // 信息查询
  'whoami', 'hostname', 'uname', 'id', 'env', 'locale'
];

// 危险模式检测
const BLOCKED_PATTERNS = [
  // 任何删除操作
  /rm\s+/i, /del\s+/i, /unlink/i, /rmdir/i,
  // 任何修改操作
  /chmod\s+/i, /chown\s+/i, /touch\s+/i, /mkdir\s+/i,
  // 关机重启
  /shutdown/i, /reboot/i, /halt/i, /poweroff/i,
  // 进程控制
  /kill\s+/i, /pkill/i, /killall/i,
  // 管道执行（危险）
  /\|\s*(sh|bash|zsh|python|node|ruby|perl)/i,
  // 任何下载
  /curl\s+/i, /wget\s+/i, /fetch\s+/i,
  // 远程连接
  /ssh\s+/i, /scp\s+/i, /rsync\s+/i, /sftp/i,
  // 提权
  /sudo\s+/i, /su\s+/i,
  // 任何执行
  /python/i, /python3/i, /node/i, /perl/i, /ruby/i, /php/i,
  /bash\s+/i, /sh\s+/i, /zsh\s+/i,
  // 包管理
  /brew\s+install/i, /apt\s+/i, /yum\s+/i, /dnf\s+/i, /pip\s+install/i,
  /npm\s+install/i, /yarn\s+add/i, /gem\s+install/i,
  // Git 危险操作
  /git\s+reset/i, /git\s+push/i, /git\s+checkout/i,
  // 任何重定向写入
  />\s*\//i, />>\s*\//i,
  // 其他危险操作
  /mkfs/i, /dd\s+/i, /fdisk/i, /parted/i
];

function isCommandSafe(command) {
  const trimmed = command.trim().toLowerCase();
  
  // 检查危险模式
  for (const pattern of BLOCKED_PATTERNS) {
    if (pattern.test(trimmed)) {
      return { 
        safe: false, 
        reason: `危险命令模式: ${pattern.toString()}`,
        blocked: true
      };
    }
  }
  
  // 检查白名单（必须是命令开头）
  const isAllowed = ALLOWED_COMMANDS.some(cmd => 
    trimmed === cmd || 
    trimmed.startsWith(cmd + ' ') ||
    trimmed.startsWith(cmd + '\t')
  );
  
  if (!isAllowed) {
    return { 
      safe: false, 
      reason: '命令不在白名单中（仅允许读取/查询类命令）',
      blocked: false
    };
  }
  
  return { safe: true };
}

// 主函数
const args = process.argv.slice(2);
const command = args.join(' ');

if (!command) {
  console.error('请输入要执行的命令');
  process.exit(1);
}

const result = isCommandSafe(command);

if (!result.safe) {
  if (result.blocked) {
    console.error('⛔ 安全拦截（危险操作）');
  } else {
    console.error('⛔ 安全拦截（未在白名单）');
  }
  console.error(`原因: ${result.reason}`);
  console.error('Safe Shell v1.0.1 - 仅允许读取和查询类命令');
  process.exit(1);
}

console.log(`✅ 执行命令: ${command}`);
console.log('（实际执行需通过 exec 工具）');
