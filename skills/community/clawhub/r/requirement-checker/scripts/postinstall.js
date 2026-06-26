#!/usr/bin/env node
/**
 * requirement-checker 安装后脚本 v2.4
 * 
 * 自动检测并安装依赖：
 * - Python: >= 3.7（必需）
 * - requests: >= 2.28.0（必需，HTTP请求库）
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// 配置
const PYTHON_DEPS = {
  'requests': {
    name: 'requests',
    description: 'HTTP请求库（必需，~500KB）',
    checkCommand: 'python3 -c "import requests; print(requests.__version__)"',
    installCommand: 'pip3 install --break-system-packages requests',
    fallbackCommand: 'pip3 install requests',
    required: true,
    hint: '用于调用 LLM API 进行智能检查'
  }
};

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 检测命令是否存在
function commandExists(command) {
  try {
    execSync(command, { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

// 检测Python版本
function checkPythonVersion() {
  try {
    const version = execSync('python3 --version', { encoding: 'utf-8' });
    const match = version.match(/Python (\d+)\.(\d+)/);
    if (match) {
      const major = parseInt(match[1]);
      const minor = parseInt(match[2]);
      return {
        version: `${major}.${minor}`,
        valid: major >= 3 && minor >= 7
      };
    }
    return { version: 'unknown', valid: false };
  } catch (error) {
    return { version: 'not found', valid: false };
  }
}

// 安装Python依赖
async function installPythonDependency(name, config) {
  log(`\n📦 安装 ${config.name}...`, 'blue');

  try {
    log(`   执行：${config.installCommand}`, 'yellow');
    execSync(config.installCommand, { stdio: 'inherit' });
    log(`✅ ${config.name} 安装成功！`, 'green');
    return true;
  } catch (error) {
    // 尝试备选命令
    if (config.fallbackCommand) {
      try {
        log(`   重试：${config.fallbackCommand}`, 'yellow');
        execSync(config.fallbackCommand, { stdio: 'inherit' });
        log(`✅ ${config.name} 安装成功！`, 'green');
        return true;
      } catch (error2) {
        // 忽略，继续
      }
    }

    log(`❌ ${config.name} 安装失败：${error.message}`, 'red');
    log(`💡 请手动安装：pip3 install ${config.name}`, 'yellow');
    return false;
  }
}

// 主函数
async function main() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🚀 requirement-checker 安装后配置', 'cyan');
  log('='.repeat(60), 'cyan');

  const results = {
    installed: [],
    skipped: [],
    failed: []
  };

  // ============ Python 版本检测 ============
  log('\n📋 Python 环境检测', 'blue');

  const pythonCheck = checkPythonVersion();
  
  if (pythonCheck.version === 'not found') {
    log('❌ 未找到 Python 3', 'red');
    log('💡 请先安装 Python 3.7 或更高版本', 'yellow');
    log('   macOS: brew install python3', 'yellow');
    log('   Linux: sudo apt-get install python3', 'yellow');
    log('   Windows: https://www.python.org/downloads/', 'yellow');
    process.exit(1);
  }

  log(`✅ Python 版本：${pythonCheck.version}`, 'green');

  if (!pythonCheck.valid) {
    log('❌ Python 版本过低，需要 >= 3.7', 'red');
    log('💡 请升级 Python 到 3.7 或更高版本', 'yellow');
    process.exit(1);
  }

  // ============ Python 依赖检测 ============
  log('\n📋 Python 依赖检测', 'blue');

  for (const [name, config] of Object.entries(PYTHON_DEPS)) {
    log(`\n🔍 检测：${config.name}`, 'blue');
    log(`   说明：${config.description}`, 'blue');
    if (config.hint) {
      log(`   用途：${config.hint}`, 'blue');
    }

    // 检查是否已安装
    if (commandExists(config.checkCommand)) {
      log(`✅ ${config.name} 已安装`, 'green');
      results.installed.push(name);
      continue;
    }

    // 必需依赖：直接安装
    if (config.required) {
      log(`⚠️  ${config.name} 未安装（必需依赖）`, 'yellow');
      log(`📦 正在安装必需依赖...`, 'yellow');

      const success = await installPythonDependency(name, config);
      if (success) {
        results.installed.push(name);
      } else {
        results.failed.push(name);
        log(`❌ 必需依赖安装失败，技能可能无法正常使用`, 'red');
      }
      continue;
    }
  }

  // ============ 安装总结 ============
  log('\n' + '='.repeat(60), 'cyan');
  log('📊 安装总结', 'cyan');
  log('='.repeat(60), 'cyan');

  if (results.installed.length > 0) {
    log(`✅ 已安装：${results.installed.join(', ')}`, 'green');
  }

  if (results.skipped.length > 0) {
    log(`⏭️  已跳过：${results.skipped.join(', ')}`, 'yellow');
  }

  if (results.failed.length > 0) {
    log(`❌ 安装失败：${results.failed.join(', ')}`, 'red');
  }

  // ============ 使用说明 ============
  log('\n📖 使用说明:', 'cyan');
  log('  在 OpenClaw 中说："请检查需求文档"', 'blue');

  log('\n💡 依赖说明:', 'cyan');
  log('  Python: >= 3.7（必需）', 'blue');
  log('  requests: >= 2.28.0（必需，HTTP请求库）', 'blue');
  log('\n  手动安装依赖:', 'cyan');
  log('  pip3 install --break-system-packages requests', 'blue');
  log('  或: pip3 install -r requirements.txt', 'blue');

  log('\n🔧 验证安装:', 'cyan');
  log('  python3 -c "import requests; print(requests.__version__)"', 'blue');

  log('\n' + '='.repeat(60), 'cyan');
  log('✅ requirement-checker 安装完成！', 'green');
  log('='.repeat(60), 'cyan');

  if (results.failed.length > 0) {
    process.exit(1);
  }
}

// 执行
main().catch(error => {
  log(`\n❌ 安装后脚本执行失败：${error.message}`, 'red');
  process.exit(1);
});