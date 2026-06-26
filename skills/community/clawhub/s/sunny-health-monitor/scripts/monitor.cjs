#!/usr/bin/env node

/**
 * System Health Monitor - 系统健康监控工具
 * 
 * 功能：
 * 1. 检查系统资源（CPU/内存/磁盘）
 * 2. 检查定时任务状态
 * 3. 计算健康评分
 * 4. 生成报告
 * 5. 推送到 Discord
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const https = require('https');

// 配置
const CONFIG = {
  statusFile: '/Users/xufan65/.openclaw/workspace/memory/system-health-status.json',
  cronJobsFile: '/Users/xufan65/.openclaw/cron/jobs.json',
  // Discord Webhook URL
  discordWebhookUrl: process.env.SYSTEM_HEALTH_WEBHOOK || 
    'https://discord.com/api/webhooks/1481951256879693866/NQdbpQ8k87m-pi3apgFCMA8SeFYHUli7LquYdCcm2gNYzrYFMhMbL_5aLKgjrci2LzKP'
};

// 阈值配置
const THRESHOLDS = {
  cpu: { warning: 50, critical: 80 },
  memory: { warning: 70, critical: 90 },
  disk: { warning: 70, critical: 90 },
  cronJobs: { 
    warningThreshold: 2, 
    criticalThreshold: 5,
    successRateWarning: 80,
    successRateCritical: 60
  }
};

class SystemHealthMonitor {
  constructor() {
    this.systemMetrics = {};
    this.cronJobsStatus = {};
    this.healthScore = 100;
    this.recommendations = [];
  }

  /**
   * 检查系统资源
   */
  checkSystemResources() {
    console.log('🖥️  检查系统资源...\n');

    try {
      // CPU 使用率
      const cpuOutput = execSync('ps -A -o %cpu | awk \'{s+=$1} END {print s}\'', { encoding: 'utf8' });
      const cpuUsage = parseFloat(cpuOutput.trim());
      this.systemMetrics.cpu = {
        usage: cpuUsage.toFixed(1),
        status: this.getResourceStatus(cpuUsage, 'cpu')
      };
      console.log(`   ✅ CPU: ${cpuUsage.toFixed(1)}%`);

      // 内存使用率
      const memOutput = execSync('vm_stat | head -10', { encoding: 'utf8' });
      const memLines = memOutput.split('\n');
      const pageSize = 4096; // 4KB
      let totalPages = 0;
      let freePages = 0;
      
      memLines.forEach(line => {
        if (line.includes('Pages free')) {
          freePages = parseInt(line.match(/\d+/)[0]);
        }
        if (line.includes('Pages active') || line.includes('Pages inactive') || line.includes('Pages speculative')) {
          totalPages += parseInt(line.match(/\d+/)[0]);
        }
      });

      const totalMemory = 16 * 1024 * 1024 * 1024; // 16GB
      const usedMemory = totalPages * pageSize;
      const memUsage = (usedMemory / totalMemory) * 100;
      
      this.systemMetrics.memory = {
        usage: memUsage.toFixed(1),
        total: '16GB',
        used: (usedMemory / 1024 / 1024 / 1024).toFixed(1) + 'GB',
        status: this.getResourceStatus(memUsage, 'memory')
      };
      console.log(`   ✅ 内存: ${memUsage.toFixed(1)}% (${this.systemMetrics.memory.used} / ${this.systemMetrics.memory.total})`);

      // 磁盘使用率
      const diskOutput = execSync('df -h / | tail -1', { encoding: 'utf8' });
      const diskParts = diskOutput.trim().split(/\s+/);
      const diskUsage = parseInt(diskParts[4].replace('%', ''));
      
      this.systemMetrics.disk = {
        usage: diskUsage,
        total: diskParts[1],
        used: diskParts[2],
        available: diskParts[3],
        status: this.getResourceStatus(diskUsage, 'disk')
      };
      console.log(`   ✅ 磁盘: ${diskUsage}% (${this.systemMetrics.disk.used} / ${this.systemMetrics.disk.total})`);

      // 网络状态
      const networkStatus = this.checkNetworkStatus();
      this.systemMetrics.network = networkStatus;
      console.log(`   ${networkStatus === '正常' ? '✅' : '❌'} 网络: ${networkStatus}\n`);

    } catch (e) {
      console.error('   ❌ 检查系统资源失败:', e.message);
    }
  }

  /**
   * 获取资源状态
   */
  getResourceStatus(value, type) {
    const threshold = THRESHOLDS[type];
    if (value >= threshold.critical) return 'critical';
    if (value >= threshold.warning) return 'warning';
    return 'normal';
  }

  /**
   * 检查网络状态
   */
  checkNetworkStatus() {
    try {
      execSync('ping -c 1 8.8.8.8', { encoding: 'utf8', timeout: 5000 });
      return '正常';
    } catch (e) {
      return '异常';
    }
  }

  /**
   * 检查定时任务
   */
  checkCronJobs() {
    console.log('⏰ 检查定时任务...\n');

    try {
      if (!fs.existsSync(CONFIG.cronJobsFile)) {
        console.log('   ⚠️  Cron jobs 文件不存在\n');
        return;
      }

      const jobs = JSON.parse(fs.readFileSync(CONFIG.cronJobsFile, 'utf8')).jobs || [];
      
      const total = jobs.length;
      let success = 0;
      let failed = 0;
      let timeout = 0;
      const failedJobs = [];
      const timeoutJobs = [];

      jobs.forEach(job => {
        const status = job.state?.lastStatus;
        if (status === 'ok') {
          success++;
        } else if (status === 'error') {
          failed++;
          failedJobs.push({
            name: job.name,
            error: job.state?.lastError || 'Unknown error'
          });
        } else if (status === 'timeout') {
          timeout++;
          timeoutJobs.push(job.name);
        }
      });

      const successRate = total > 0 ? ((success / total) * 100).toFixed(1) : 0;

      this.cronJobsStatus = {
        total,
        success,
        failed,
        timeout,
        successRate: parseFloat(successRate),
        failedJobs,
        timeoutJobs,
        status: this.getCronJobsStatus(failed, successRate)
      };

      console.log(`   总任务: ${total} 个`);
      console.log(`   ✅ 成功: ${success} 个`);
      console.log(`   ❌ 失败: ${failed} 个`);
      console.log(`   ⏱️  超时: ${timeout} 个`);
      console.log(`   成功率: ${successRate}%\n`);

      if (failedJobs.length > 0) {
        console.log('   失败任务:');
        failedJobs.forEach(job => {
          console.log(`      • ${job.name}: ${job.error.substring(0, 50)}...`);
        });
        console.log();
      }

    } catch (e) {
      console.error('   ❌ 检查定时任务失败:', e.message);
    }
  }

  /**
   * 获取定时任务状态
   */
  getCronJobsStatus(failed, successRate) {
    if (failed >= THRESHOLDS.cronJobs.criticalThreshold || successRate < THRESHOLDS.cronJobs.successRateCritical) {
      return 'critical';
    }
    if (failed >= THRESHOLDS.cronJobs.warningThreshold || successRate < THRESHOLDS.cronJobs.successRateWarning) {
      return 'warning';
    }
    return 'normal';
  }

  /**
   * 计算健康评分
   */
  calculateHealthScore() {
    console.log('📊 计算健康评分...\n');

    let score = 100;

    // 系统资源评分 (40 分)
    // CPU (15 分)
    const cpuUsage = parseFloat(this.systemMetrics.cpu?.usage || 0);
    if (cpuUsage > THRESHOLDS.cpu.critical) {
      score -= 15;
    } else if (cpuUsage > THRESHOLDS.cpu.warning) {
      score -= 8;
    }

    // 内存 (15 分)
    const memUsage = parseFloat(this.systemMetrics.memory?.usage || 0);
    if (memUsage > THRESHOLDS.memory.critical) {
      score -= 15;
    } else if (memUsage > THRESHOLDS.memory.warning) {
      score -= 8;
    }

    // 磁盘 (10 分)
    const diskUsage = this.systemMetrics.disk?.usage || 0;
    if (diskUsage > THRESHOLDS.disk.critical) {
      score -= 10;
    } else if (diskUsage > THRESHOLDS.disk.warning) {
      score -= 5;
    }

    // 定时任务评分 (40 分)
    // 成功率 (20 分)
    const successRate = this.cronJobsStatus.successRate || 100;
    if (successRate < THRESHOLDS.cronJobs.successRateCritical) {
      score -= 20;
    } else if (successRate < THRESHOLDS.cronJobs.successRateWarning) {
      score -= 10;
    }

    // 失败任务数 (10 分)
    const failed = this.cronJobsStatus.failed || 0;
    if (failed >= THRESHOLDS.cronJobs.criticalThreshold) {
      score -= 10;
    } else if (failed >= THRESHOLDS.cronJobs.warningThreshold) {
      score -= 5;
    }

    // 超时任务数 (10 分)
    const timeout = this.cronJobsStatus.timeout || 0;
    if (timeout > 0) {
      score -= Math.min(timeout * 3, 10);
    }

    // 系统稳定性 (20 分)
    // 网络状态 (10 分)
    if (this.systemMetrics.network !== '正常') {
      score -= 10;
    }

    // 错误日志 (10 分) - 简化处理
    // 如果有失败任务，扣 5 分
    if (failed > 0) {
      score -= 5;
    }

    this.healthScore = Math.max(0, Math.min(100, score));

    console.log(`   健康评分: ${this.healthScore}/100`);
    console.log(`   等级: ${this.getHealthGrade()}\n`);
  }

  /**
   * 获取健康等级
   */
  getHealthGrade() {
    if (this.healthScore >= 90) return '⭐⭐⭐⭐⭐ 优秀';
    if (this.healthScore >= 80) return '⭐⭐⭐⭐ 良好';
    if (this.healthScore >= 70) return '⭐⭐⭐ 一般';
    if (this.healthScore >= 60) return '⭐⭐ 较差';
    return '⭐ 危险';
  }

  /**
   * 生成建议
   */
  generateRecommendations() {
    this.recommendations = [];

    // CPU 建议
    if (this.systemMetrics.cpu?.status === 'critical') {
      this.recommendations.push('CPU 使用率过高，建议关闭不必要的进程');
    } else if (this.systemMetrics.cpu?.status === 'warning') {
      this.recommendations.push('CPU 使用率较高，建议监控进程');
    }

    // 内存建议
    if (this.systemMetrics.memory?.status === 'critical') {
      this.recommendations.push('内存使用率过高，建议关闭不必要的应用');
    } else if (this.systemMetrics.memory?.status === 'warning') {
      this.recommendations.push('内存使用率较高，建议清理内存');
    }

    // 磁盘建议
    if (this.systemMetrics.disk?.status === 'critical') {
      this.recommendations.push('磁盘空间不足，建议立即清理');
    } else if (this.systemMetrics.disk?.status === 'warning') {
      this.recommendations.push('磁盘空间较少，建议清理不必要的文件');
    }

    // 定时任务建议
    if (this.cronJobsStatus.failed > 0) {
      this.recommendations.push(`修复 ${this.cronJobsStatus.failed} 个失败任务`);
    }
    if (this.cronJobsStatus.timeout > 0) {
      this.recommendations.push(`检查 ${this.cronJobsStatus.timeout} 个超时任务`);
    }
    if (this.cronJobsStatus.successRate < 80) {
      this.recommendations.push('定时任务成功率较低，建议优化');
    }

    // 网络建议
    if (this.systemMetrics.network !== '正常') {
      this.recommendations.push('网络连接异常，建议检查网络');
    }
  }

  /**
   * 生成报告
   */
  generateReport() {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    
    let report = `# 📊 系统健康报告\n\n`;
    report += `**检查时间**: ${timestamp}\n\n`;
    
    report += `---\n\n`;
    
    // 系统资源
    report += `## 🖥️ 系统资源\n\n`;
    
    const cpuIcon = this.systemMetrics.cpu?.status === 'normal' ? '✅' : 
                    (this.systemMetrics.cpu?.status === 'warning' ? '⚠️' : '❌');
    report += `${cpuIcon} **CPU**: ${this.systemMetrics.cpu?.usage || 'N/A'}%\n`;
    
    const memIcon = this.systemMetrics.memory?.status === 'normal' ? '✅' : 
                    (this.systemMetrics.memory?.status === 'warning' ? '⚠️' : '❌');
    report += `${memIcon} **内存**: ${this.systemMetrics.memory?.usage || 'N/A'}% (${this.systemMetrics.memory?.used || 'N/A'} / ${this.systemMetrics.memory?.total || 'N/A'})\n`;
    
    const diskIcon = this.systemMetrics.disk?.status === 'normal' ? '✅' : 
                     (this.systemMetrics.disk?.status === 'warning' ? '⚠️' : '❌');
    report += `${diskIcon} **磁盘**: ${this.systemMetrics.disk?.usage || 'N/A'}% (${this.systemMetrics.disk?.used || 'N/A'} / ${this.systemMetrics.disk?.total || 'N/A'})\n`;
    
    const netIcon = this.systemMetrics.network === '正常' ? '✅' : '❌';
    report += `${netIcon} **网络**: ${this.systemMetrics.network || 'N/A'}\n\n`;
    
    report += `---\n\n`;
    
    // 定时任务
    report += `## ⏰ 定时任务\n\n`;
    report += `**总任务**: ${this.cronJobsStatus.total || 0} 个\n`;
    report += `✅ **成功**: ${this.cronJobsStatus.success || 0} 个\n`;
    report += `❌ **失败**: ${this.cronJobsStatus.failed || 0} 个\n`;
    report += `⏱️ **超时**: ${this.cronJobsStatus.timeout || 0} 个\n\n`;
    report += `**成功率**: ${this.cronJobsStatus.successRate || 0}%\n\n`;
    
    if (this.cronJobsStatus.failedJobs && this.cronJobsStatus.failedJobs.length > 0) {
      report += `**失败任务**:\n`;
      this.cronJobsStatus.failedJobs.forEach(job => {
        report += `- ${job.name}\n`;
      });
      report += `\n`;
    }
    
    report += `---\n\n`;
    
    // 健康评分
    report += `## 📊 健康评分\n\n`;
    report += `**分数**: ${this.healthScore}/100\n`;
    report += `**等级**: ${this.getHealthGrade()}\n\n`;
    
    report += `---\n\n`;
    
    // 建议
    if (this.recommendations.length > 0) {
      report += `## 💡 优化建议\n\n`;
      this.recommendations.forEach((rec, index) => {
        report += `${index + 1}. ${rec}\n`;
      });
      report += `\n`;
    }
    
    return report;
  }

  /**
   * 保存状态
   */
  saveStatus() {
    try {
      const status = {
        lastCheck: new Date().toISOString(),
        healthScore: this.healthScore,
        system: {
          cpu: parseFloat(this.systemMetrics.cpu?.usage || 0),
          memory: parseFloat(this.systemMetrics.memory?.usage || 0),
          disk: this.systemMetrics.disk?.usage || 0
        },
        cronJobs: {
          total: this.cronJobsStatus.total || 0,
          success: this.cronJobsStatus.success || 0,
          failed: this.cronJobsStatus.failed || 0,
          timeout: this.cronJobsStatus.timeout || 0,
          successRate: this.cronJobsStatus.successRate || 0
        },
        status: this.healthScore >= 80 ? 'good' : (this.healthScore >= 60 ? 'warning' : 'critical'),
        recommendations: this.recommendations
      };
      
      fs.writeFileSync(CONFIG.statusFile, JSON.stringify(status, null, 2));
    } catch (e) {
      console.error('保存状态失败:', e.message);
    }
  }

  /**
   * 发送到 Discord（使用 Webhook）
   */
  sendToDiscord(report) {
    if (!CONFIG.discordWebhookUrl) {
      console.log('\n⚠️  Discord Webhook 未配置，跳过推送');
      return;
    }
    
    try {
      const url = new URL(CONFIG.discordWebhookUrl);
      const data = JSON.stringify({
        content: report.substring(0, 1900),
        username: 'System Health Monitor',
        avatar_url: 'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f4ca.png'
      });
      
      const options = {
        hostname: url.hostname,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data)
        }
      };
      
      const req = https.request(options, (res) => {
        if (res.statusCode === 204 || res.statusCode === 200) {
          console.log('\n✅ 报告已推送到 Discord');
        } else {
          console.log(`\n⚠️  Discord 返回状态码: ${res.statusCode}`);
        }
      });
      
      req.on('error', (e) => {
        console.error('\n❌ 推送到 Discord 失败:', e.message);
      });
      
      req.write(data);
      req.end();
    } catch (e) {
      console.error('\n❌ 推送到 Discord 失败:', e.message);
    }
  }

  /**
   * 主运行函数
   */
  run() {
    console.log('🚀 System Health Monitor 启动\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 1. 检查系统资源
    this.checkSystemResources();

    // 2. 检查定时任务
    this.checkCronJobs();

    // 3. 计算健康评分
    this.calculateHealthScore();

    // 4. 生成建议
    this.generateRecommendations();

    // 5. 生成报告
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const report = this.generateReport();
    console.log(report);

    // 6. 保存状态
    this.saveStatus();

    // 7. 发送到 Discord
    this.sendToDiscord(report);

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ System Health Monitor 完成\n');
  }
}

// 运行
if (require.main === module) {
  const monitor = new SystemHealthMonitor();
  monitor.run();
}

module.exports = SystemHealthMonitor;
