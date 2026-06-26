#!/usr/bin/env node
/**
 * 密钥扫描脚本
 * 扫描文件中的敏感信息，防止同步时泄露
 * 
 * 用法:
 *   node secret-scan.js <文件路径>
 *   node secret-scan.js --dir <目录路径>
 */

const fs = require('fs');
const path = require('path');

// 密钥模式
const SECRET_PATTERNS = [
  { name: 'AWS Access Key', regex: /AKIA[0-9A-Z]{16}/ },
  { name: '阿里云 AccessKey', regex: /LTAI[0-9A-Za-z]{12,20}/ },
  { name: '私钥', regex: /-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----/ },
  { name: 'Bearer Token', regex: /Bearer [a-zA-Z0-9\-_]{20,}/ },
  { name: 'API Key (通用)', regex: /(?:api[_-]?key|apikey)\s*[:=]\s*['"]?[a-zA-Z0-9\-_]{16,}/i },
  { name: '密码赋值', regex: /(?:password|passwd|pwd)\s*[:=]\s*['"][^'"]{4,}['"]/i },
  { name: '数据库连接串', regex: /(?:mysql|mongodb|redis|postgres):\/\/[^\s]+:[^\s]+@/i },
  { name: 'sk- 开头的 Key', regex: /sk-[a-zA-Z0-9\-_]{20,}/ },
  { name: 'ghp_ GitHub Token', regex: /ghp_[a-zA-Z0-9]{36}/ },
  { name: 'xoxb_ Slack Token', regex: /xoxb-[a-zA-Z0-9\-]+/ },
];

function scanContent(content, filepath) {
  const found = [];
  
  for (const pattern of SECRET_PATTERNS) {
    const matches = content.match(pattern.regex);
    if (matches) {
      for (const match of matches) {
        // 脱敏显示
        const masked = match.length > 10 ? match.substring(0, 6) + '***' + match.substring(match.length - 4) : '***';
        found.push({
          type: pattern.name,
          match: masked,
          line: content.substring(0, content.indexOf(match)).split('\n').length
        });
      }
    }
  }
  
  return found;
}

function scanFile(filepath) {
  try {
    const content = fs.readFileSync(filepath, 'utf8');
    const secrets = scanContent(content, filepath);
    return { filepath, secrets, safe: secrets.length === 0 };
  } catch (e) {
    return { filepath, error: e.message, safe: false };
  }
}

function scanDir(dirPath) {
  const results = [];
  
  function walk(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullpath = path.join(dir, entry.name);
      
      if (entry.name.startsWith('.')) continue; // 跳过隐藏文件
      
      if (entry.isDirectory()) {
        walk(fullpath);
      } else if (entry.isFile() && /\.(md|json|js|ts|yaml|yml|env|conf|cfg|ini|txt|sh|py)$/i.test(entry.name)) {
        results.push(scanFile(fullpath));
      }
    }
  }
  
  walk(dirPath);
  return results;
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法: node secret-scan.js <文件路径>');
    console.log('      node secret-scan.js --dir <目录路径>');
    process.exit(1);
  }
  
  if (args[0] === '--dir' && args[1]) {
    console.log(`=== 扫描目录: ${args[1]} ===\n`);
    const results = scanDir(args[1]);
    
    const unsafe = results.filter(r => !r.safe);
    const safe = results.filter(r => r.safe);
    
    console.log(`扫描完成: ${results.length} 个文件`);
    console.log(`  安全: ${safe.length}`);
    console.log(`  ⚠️  含密钥: ${unsafe.length}\n`);
    
    for (const result of unsafe) {
      console.log(`❌ ${result.filepath}`);
      for (const secret of result.secrets) {
        console.log(`   ${secret.type}: ${secret.match} (第 ${secret.line} 行)`);
      }
    }
    
    process.exit(unsafe.length > 0 ? 1 : 0);
    return;
  }
  
  // 扫描单个文件
  const filepath = args[0];
  console.log(`=== 扫描文件: ${filepath} ===\n`);
  const result = scanFile(filepath);
  
  if (result.error) {
    console.error(`错误: ${result.error}`);
    process.exit(1);
  }
  
  if (result.safe) {
    console.log('✅ 未检测到密钥');
  } else {
    console.log(`⚠️  检测到 ${result.secrets.length} 个密钥:\n`);
    for (const secret of result.secrets) {
      console.log(`   ${secret.type}: ${secret.match} (第 ${secret.line} 行)`);
    }
    process.exit(1);
  }
}

main();
