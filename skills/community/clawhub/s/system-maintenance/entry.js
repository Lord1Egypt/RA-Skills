/**
 * 系统清理与优化维护技能 - 入口点
 * 提供命令行接口调用维护功能
 */

const { execSync } = require('child_process');
const path = require('path');

class SystemMaintenanceSkill {
  constructor() {
    this.scriptsDir = path.join(__dirname, 'scripts');
  }

  /**
   * 运行日常维护优化
   */
  runDailyMaintenance() {
    console.log('🚀 开始日常维护优化...');
    const scriptPath = path.join(this.scriptsDir, 'daily-maintenance-optimization.sh');
    
    try {
      execSync(`bash "${scriptPath}"`, { stdio: 'inherit' });
      console.log('✅ 日常维护优化完成');
    } catch (error) {
      console.error('❌ 维护执行失败:', error.message);
      throw error;
    }
  }

  /**
   * 快速清理（轻量级）
   */
  runQuickCleanup() {
    console.log('🧹 开始快速清理...');
    
    // 清理3天前的日志
    execSync('find /tmp/openclaw -name "*.log" -mtime +3 -delete 2>/dev/null || true');
    
    // 清理临时文件
    execSync('find /tmp -name "cron_test*.log" -mtime +1 -delete 2>/dev/null || true');
    execSync('find /tmp -name "*news_summary*.md" -mtime +1 -delete 2>/dev/null || true');
    
    console.log('✅ 快速清理完成');
  }

  /**
   * 检查系统状态
   */
  checkSystemStatus() {
    console.log('🔍 检查系统状态...');
    
    // 检查 Gateway
    try {
      execSync('curl -s --max-time 5 http://localhost:18789/ > /dev/null', { stdio: 'ignore' });
      console.log('✅ Gateway: 运行正常');
    } catch {
      console.log('❌ Gateway: 无响应');
    }

    // 检查磁盘空间
    const diskUsage = execSync('df -h / | tail -1', { encoding: 'utf8' });
    console.log(`💾 磁盘使用: ${diskUsage.trim()}`);

    // 检查工作区大小
    try {
      const workspaceSize = execSync('du -sh ~/.openclaw/workspace/ 2>/dev/null', { encoding: 'utf8' });
      console.log(`📁 工作区大小: ${workspaceSize.trim()}`);
    } catch {
      console.log('📁 工作区: 无法获取大小');
    }
  }

  /**
   * 安装定时任务
   */
  installCronJob() {
    console.log('⏰ 安装定时维护任务...');
    
    const cronLine = '30 3 * * * ~/.openclaw/skills/system-maintenance/scripts/daily-maintenance-optimization.sh >> /tmp/openclaw-maintenance.log 2>&1';
    
    try {
      // 获取当前 crontab
      let currentCron = '';
      try {
        currentCron = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
      } catch {
        currentCron = '';
      }

      // 检查是否已存在
      if (currentCron.includes('daily-maintenance-optimization.sh')) {
        console.log('ℹ️  定时任务已存在');
        return;
      }

      // 添加新任务
      const newCron = currentCron + '\n' + cronLine + '\n';
      execSync(`echo "${newCron.trim()}" | crontab -`);
      
      console.log('✅ 定时任务安装完成 (每天 3:30)');
    } catch (error) {
      console.error('❌ 定时任务安装失败:', error.message);
    }
  }
}

// 命令行接口
if (require.main === module) {
  const skill = new SystemMaintenanceSkill();
  const command = process.argv[2];

  switch (command) {
    case 'daily':
      skill.runDailyMaintenance();
      break;
    case 'quick':
      skill.runQuickCleanup();
      break;
    case 'status':
      skill.checkSystemStatus();
      break;
    case 'install-cron':
      skill.installCronJob();
      break;
    default:
      console.log(`
系统清理与优化维护技能

用法:
  node entry.js [command]

命令:
  daily       运行完整的日常维护优化
  quick       运行快速清理
  status      检查系统状态
  install-cron 安装定时维护任务

示例:
  node entry.js daily      # 运行日常维护
  node entry.js status     # 检查系统状态
      `);
  }
}

module.exports = SystemMaintenanceSkill;

  /**
   * 安装统一维护系统
   */
  installUnifiedSystem() {
    console.log('🚀 安装统一维护系统...');
    
    const installScript = path.join(__dirname, 'maintenance-system', 'scripts', 'install-maintenance-system.sh');
    
    if (!fs.existsSync(installScript)) {
      console.log('❌ 安装脚本不存在，请先更新技能');
      return;
    }
    
    try {
      execSync(`bash "${installScript}"`, { stdio: 'inherit' });
      console.log('✅ 统一维护系统安装完成');
    } catch (error) {
      console.error('❌ 安装失败:', error.message);
    }
  }

  /**
   * 检查统一系统状态
   */
  checkUnifiedSystem() {
    console.log('🔍 检查统一维护系统状态...');
    
    const maintenanceDir = path.join(__dirname, 'maintenance-system');
    
    if (!fs.existsSync(maintenanceDir)) {
      console.log('❌ 统一系统未安装');
      return;
    }
    
    // 检查目录结构
    const dirs = fs.readdirSync(maintenanceDir);
    console.log('📁 系统目录:');
    dirs.forEach(dir => {
      const stat = fs.statSync(path.join(maintenanceDir, dir));
      console.log(`  ${dir} (${stat.isDirectory() ? '目录' : '文件'})`);
    });
    
    // 检查定时任务
    try {
      const cronOutput = execSync('crontab -l | grep -i "openclaw.*maintenance"', { encoding: 'utf8' });
      console.log('⏰ 定时任务:');
      console.log(cronOutput);
    } catch {
      console.log('⏰ 定时任务: 未找到');
    }
  }
}

// 更新命令行接口
if (require.main === module) {
  const skill = new SystemMaintenanceSkill();
  const command = process.argv[2];

  switch (command) {
    case 'daily':
      skill.runDailyMaintenance();
      break;
    case 'quick':
      skill.runQuickCleanup();
      break;
    case 'status':
      skill.checkSystemStatus();
      break;
    case 'install-cron':
      skill.installCronJob();
      break;
    case 'install-system':  // 新增
      skill.installUnifiedSystem();
      break;
    case 'check-system':    // 新增
      skill.checkUnifiedSystem();
      break;
    default:
      console.log(`
系统清理与优化维护技能 v1.1.0

用法:
  node entry.js [command]

命令:
  daily          运行日常维护
  quick          运行快速清理
  status         检查系统状态
  install-cron   安装定时任务 (旧版)
  install-system 安装统一维护系统 (新版)
  check-system   检查统一系统状态

示例:
  node entry.js install-system  # 安装统一维护系统
  node entry.js check-system    # 检查系统状态
      `);
  }
}
