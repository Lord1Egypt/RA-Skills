      recommendations.push(`⏳ 距离下次重启还需等待到: ${status.protection.nextRestartAvailable}`);
    }
    
    if (status.system.lockStatus.includes('已锁定')) {
      recommendations.push('🔒 有重启进程正在运行，请等待其完成');
    } else if (status.system.lockStatus.includes('陈旧的锁')) {
      recommendations.push('⚠️ 发现陈旧的锁文件，可安全删除');
    }
    
    if (status.statistics.failedRestarts > 0) {
      recommendations.push('🔧 最近有重启失败记录，建议检查系统状态');
    }
    
    if (recommendations.length === 0) {
      recommendations.push('✅ 系统状态正常，可以安全重启');
    }
    
    return recommendations;
  }
  
  async history(options = {}) {
    const limit = options.limit || 20;
    const restarts = await this.getRestartRecords();
    
    // 按时间倒序排序
    const sorted = restarts.sort((a, b) => b.timestamp - a.timestamp);
    
    return sorted.slice(0, limit).map(record => ({
      timestamp: new Date(record.timestamp * 1000).toISOString(),
      reason: record.reason,
      success: record.success ? '✅' : '❌',
      error: record.error || '',
      pid: record.pid
    }));
  }
  
  async resetProtection(options = {}) {
    const confirm = options.confirm;
    
    if (confirm !== 'EMERGENCY_RESET') {
      throw new Error('重置保护需要确认字符串 "EMERGENCY_RESET"');
    }
    
    await this.log('warn', '紧急重置保护状态', { confirmed: true });
    
    // 备份当前状态
    const backupDir = path.join(this.config.stateDir, 'reset-backups');
    await fs.mkdir(backupDir, { recursive: true });
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFile = path.join(backupDir, `protection-state-${timestamp}.tar`);
    
    try {
      // 创建备份
      const files = ['restarts.log', 'last_restart'];
      for (const file of files) {
        const source = path.join(this.config.stateDir, file);
        if (await this.fileExists(source)) {
          const dest = path.join(backupDir, file);
          await fs.copyFile(source, dest);
        }
      }
      
      // 重置状态
      await fs.writeFile(path.join(this.config.stateDir, 'last_restart'), '0');
      await fs.writeFile(path.join(this.config.stateDir, 'restarts.log'), '');
      
      // 清理锁文件
      await this.releaseLock();
      
      await this.log('info', '保护状态已重置', { backupFile });
      
      return {
        success: true,
        message: '保护状态已重置',
        backupCreated: backupFile,
        resetItems: ['last_restart', 'restarts.log', 'lock_file']
      };
      
    } catch (error) {
      await this.log('error', '重置保护状态失败', { error: error.message });
      throw new Error(`重置失败: ${error.message}`);
    }
  }
  
  async cleanup(options = {}) {
    const keepDays = options.keepDays || 7;
    const cutoffTime = Date.now() - (keepDays * 86400 * 1000);
    
    await this.log('info', '开始清理旧备份', { keepDays });
    
    const backupDir = this.config.backupDir;
    let deletedCount = 0;
    let totalSize = 0;
    
    try {
      const files = await fs.readdir(backupDir);
      
      for (const file of files) {
        const filePath = path.join(backupDir, file);
        
        try {
          const stats = await fs.stat(filePath);
          
          // 检查是否超过保留期限
          if (stats.mtimeMs < cutoffTime) {
            const size = stats.size;
            await fs.unlink(filePath);
            
            // 尝试删除对应的.reason文件
            const reasonFile = `${filePath}.reason`;
            if (await this.fileExists(reasonFile)) {
              await fs.unlink(reasonFile);
            }
            
            deletedCount++;
            totalSize += size;
            
            await this.log('debug', '删除旧备份文件', { file, size, mtime: stats.mtime.toISOString() });
          }
        } catch (error) {
          await this.log('warn', '清理文件失败', { file, error: error.message });
        }
      }
      
      const result = {
        deletedCount,
        totalSize: this.formatBytes(totalSize),
        keepDays,
        message: `清理完成，删除了 ${deletedCount} 个文件`
      };
      
      await this.log('info', '清理完成', result);
      return result;
      
    } catch (error) {
      await this.log('error', '清理失败', { error: error.message });
      throw new Error(`清理失败: ${error.message}`);
    }
  }
  
  async exportReport(options = {}) {
    const format = options.format || 'json';
    
    const status = await this.status();
    const protection = await this.protectionStatus();
    const recentHistory = await this.history({ limit: 10 });
    
    const report = {
      metadata: {
        generatedAt: new Date().toISOString(),
        skill: 'smart-restart-protection',
        version: '1.0.0'
      },
      summary: {
        systemStatus: this.getSystemStatusSummary(status),
        protectionStatus: this.getProtectionSummary(protection),
        recentActivity: recentHistory.length
      },
      details: {
        status,
        protection,
        recentHistory
      },
      recommendations: protection.recommendations
    };
    
    if (format === 'json') {
      return JSON.stringify(report, null, 2);
    } else if (format === 'markdown') {
      return this.generateMarkdownReport(report);
    } else {
      throw new Error(`不支持的格式: ${format}`);
    }
  }
  
  getSystemStatusSummary(status) {
    if (status.system.lockStatus.includes('已锁定')) {
      return '🔒 有进程运行中';
    } else if (status.protection.nextRestartAvailable !== '立即') {
      return '⏳ 等待重启冷却';
    } else if (status.protection.hourLimitAvailable <= 0) {
      return '⚠️ 小时限制用尽';
    } else if (status.protection.dayLimitAvailable <= 0) {
      return '⚠️ 日限制用尽';
    } else {
      return '✅ 系统正常';
    }
  }
  
  getProtectionSummary(protection) {
    const hourUsed = protection.limits.maxRestartsPerHour - protection.limits.hourLimitAvailable;
    const dayUsed = protection.limits.maxRestartsPerDay - protection.limits.dayLimitAvailable;
    
    return {
      hourUsage: `${hourUsed}/${protection.limits.maxRestartsPerHour}`,
      dayUsage: `${dayUsed}/${protection.limits.maxRestartsPerDay}`,
      nextAvailable: protection.nextAvailable
    };
  }
  
  generateMarkdownReport(report) {
    let md = `# Smart Restart Protection 报告\n\n`;
    md += `**生成时间:** ${report.metadata.generatedAt}\n`;
    md += `**系统状态:** ${report.summary.systemStatus}\n\n`;
    
    md += `## 保护状态\n`;
    md += `- 小时使用: ${report.summary.protectionStatus.hourUsage}\n`;
    md += `- 日使用: ${report.summary.protectionStatus.dayUsage}\n`;
    md += `- 下次可重启: ${report.summary.protectionStatus.nextAvailable}\n\n`;
    
    md += `## 最近活动\n`;
    md += `最近 ${report.summary.recentActivity} 次重启记录\n\n`;
    
    if (report.details.recentHistory.length > 0) {
      md += `| 时间 | 原因 | 状态 | 错误 |\n`;
      md += `|------|------|------|------|\n`;
      
      for (const record of report.details.recentHistory) {
        md += `| ${record.timestamp} | ${record.reason} | ${record.success} | ${record.error || ''} |\n`;
      }
      md += `\n`;
    }
    
    md += `## 建议\n`;
    for (const rec of report.recommendations) {
      md += `- ${rec}\n`;
    }
    
    return md;
  }
  
  // 工具方法
  async runCommand(command, returnOutput = false) {
    return new Promise((resolve, reject) => {
      try {
        if (returnOutput) {
          const output = execSync(command, { encoding: 'utf8', stdio: 'pipe' });
          resolve(output.trim());
        } else {
          const child = spawn(command, { shell: true, stdio: 'inherit' });
          child.on('close', (code) => {
            if (code === 0) {
              resolve();
            } else {
              reject(new Error(`命令执行失败，退出码: ${code}`));
            }
          });
          child.on('error', reject);
        }
      } catch (error) {
        reject(error);
      }
    });
  }
  
  async fileExists(filePath) {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }
  
  isProcessRunning(pid) {
    try {
      process.kill(pid, 0);
      return true;
    } catch {
      return false;
    }
  }
  
  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  async log(level, message, data = {}) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      pid: process.pid,
      ...data
    };
    
    // 控制台输出
    const consoleMessage = `[${timestamp}] [${level.toUpperCase()}] ${message}`;
    if (level === 'error') {
      console.error(consoleMessage, data);
    } else if (level === 'warn') {
      console.warn(consoleMessage, data);
    } else if (level === 'info') {
      console.log(consoleMessage);
    } else {
      console.debug(consoleMessage, data);
    }
    
    // 文件日志
    const logFile = path.join(this.config.stateDir, 'logs', `${timestamp.split('T')[0]}.log`);
    try {
      await fs.appendFile(logFile, JSON.stringify(logEntry) + '\n');
    } catch (error) {
      // 如果日志写入失败，不中断主流程
      console.error('日志写入失败:', error.message);
    }
  }
  
  formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// OpenClaw 技能标准接口
module.exports = {
  SmartRestartProtection,
  
  async smart_restart_protection(params = {}) {
    const agent = new SmartRestartProtection();
    
    switch (params.action) {
      case 'restart':
        return await agent.restart(params);
      case 'status':
        return await agent.status();
      case 'protection-status':
        return await agent.protectionStatus();
      case 'history':
        return await agent.history(params);
      case 'reset-protection':
        return await agent.resetProtection(params);
      case 'cleanup':
        return await agent.cleanup(params);
      case 'export-report':
        return await agent.exportReport(params);
      default:
        return {
          error: '未知操作',
          supportedActions: [
            'restart',
            'status', 
            'protection-status',
            'history',
            'reset-protection',
            'cleanup',
            'export-report'
          ]
        };
    }
  }
};