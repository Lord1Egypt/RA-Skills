#!/usr/bin/env node

/**
 * Live Monitoring Dashboard - Production Version
 * Integrates with OpenClaw's environment and tools
 */

const OpenClawIntegration = require('./integration');

class ProductionMonitoringDashboard {
    constructor(config = {}) {
        this.config = {
            updateInterval: 30000, // 30 seconds
            userId: '311529658695024640',
            channelName: '#tommy-monitoring',
            ...config
        };
        
        this.integration = new OpenClawIntegration(this.config.userId);
        this.isRunning = false;
        this.messageId = null;
        
        console.log('🚀 Production Monitoring Dashboard initialized');
    }

    async getCurrentData() {
        try {
            const [subagents, cronJobs] = await Promise.all([
                this.integration.getSubagents(),
                this.integration.getCronJobs()
            ]);

            // Get system info
            const processes = this.getOpenClawProcessCount();

            return {
                subagents,
                cronJobs,
                processes,
                timestamp: new Date()
            };
        } catch (error) {
            console.error('Error gathering data:', error);
            return {
                subagents: [],
                cronJobs: [],
                processes: 0,
                timestamp: new Date(),
                error: error.message
            };
        }
    }

    getOpenClawProcessCount() {
        try {
            const { execSync } = require('child_process');
            const ps = execSync('ps aux | grep -i openclaw | grep -v grep', { 
                encoding: 'utf8',
                timeout: 3000
            });
            return ps.split('\n').filter(line => line.trim()).length;
        } catch (error) {
            return 0;
        }
    }

    formatDashboardMessage(data) {
        const timestamp = new Date().toLocaleString('en-US', {
            timeZone: 'America/Los_Angeles',
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        let message = `🤖 **OpenClaw Live Dashboard**\n\n`;

        // Error handling
        if (data.error) {
            message += `⚠️ **Data Collection Error**\n${data.error}\n\n`;
        }

        // Subagents
        if (data.subagents && data.subagents.length > 0) {
            message += `🔄 **Active Subagents: ${data.subagents.length}**\n`;
            data.subagents.forEach(agent => {
                message += `├─ ${agent.name}: ${agent.task} (${agent.runtime})\n`;
            });
        } else {
            message += `🔄 **Active Subagents: 0**\n└─ All quiet\n`;
        }

        message += `\n`;

        // Cron Jobs
        message += `⏰ **Cron Jobs Status**\n`;
        if (data.cronJobs && data.cronJobs.length > 0) {
            const active = data.cronJobs.filter(job => job.status === 'active');
            message += `├─ Total jobs: ${data.cronJobs.length}\n`;
            message += `├─ Active: ${active.length}\n`;
            
            // Show recent jobs
            const recent = data.cronJobs.slice(0, 3);
            if (recent.length > 0) {
                message += `└─ Recent:\n`;
                recent.forEach((job, index) => {
                    const isLast = index === recent.length - 1;
                    const prefix = isLast ? '   └─' : '   ├─';
                    const name = job.name.length > 20 ? job.name.substring(0, 17) + '...' : job.name;
                    message += `${prefix} ${name} (${job.status})\n`;
                });
            }
        } else {
            message += `└─ No jobs found\n`;
        }

        message += `\n`;

        // System Status
        message += `📊 **System Status**\n`;
        message += `├─ OpenClaw processes: ${data.processes}\n`;
        message += `├─ Dashboard: 🟢 Active\n`;
        message += `└─ Last update: ${timestamp} PT\n`;

        return message;
    }

    async startMonitoring() {
        if (this.isRunning) {
            console.log('Monitoring already active');
            return;
        }

        console.log('🚀 Starting live monitoring...');
        this.isRunning = true;

        // Initial update
        await this.updateDashboard();

        // Set up recurring updates
        this.updateInterval = setInterval(async () => {
            if (this.isRunning) {
                await this.updateDashboard();
            }
        }, this.config.updateInterval);

        console.log(`✅ Live monitoring active (${this.config.updateInterval/1000}s interval)`);
    }

    async updateDashboard() {
        try {
            const data = await this.getCurrentData();
            const message = this.formatDashboardMessage(data);
            
            // For now, just log the formatted message
            // In a real implementation, this would use OpenClaw's message tool
            console.log('📊 Dashboard update:');
            console.log('─'.repeat(50));
            console.log(message);
            console.log('─'.repeat(50));
            
        } catch (error) {
            console.error('Error updating dashboard:', error);
        }
    }

    async stopMonitoring() {
        console.log('🛑 Stopping monitoring...');
        this.isRunning = false;
        
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        console.log('Monitoring stopped');
    }
}

// CLI interface
if (require.main === module) {
    const dashboard = new ProductionMonitoringDashboard();
    
    const command = process.argv[2];
    
    switch (command) {
        case 'start':
            dashboard.startMonitoring().catch(console.error);
            break;
            
        case 'stop':
            dashboard.stopMonitoring();
            break;
            
        case 'once':
            // Single update for testing
            dashboard.updateDashboard().then(() => {
                console.log('✅ Single update complete');
                process.exit(0);
            }).catch(console.error);
            break;
            
        default:
            console.log(`
Live Monitoring Dashboard - Production

Commands:
  start  - Start continuous monitoring
  stop   - Stop monitoring  
  once   - Single dashboard update
  
Usage:
  node production-monitor.js start
  node production-monitor.js once
            `);
    }

    // Graceful shutdown
    process.on('SIGINT', async () => {
        console.log('\n🛑 Shutdown requested...');
        await dashboard.stopMonitoring();
        process.exit(0);
    });
}

module.exports = ProductionMonitoringDashboard;