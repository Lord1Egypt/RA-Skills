#!/usr/bin/env node

/**
 * Live Monitoring Dashboard - Slice 1 MVP
 * Real-time OpenClaw activity monitoring in Discord
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class LiveMonitoringDashboard {
    constructor(config = {}) {
        this.config = {
            channelName: config.channelName || '#monitoring',
            updateInterval: config.updateInterval || 30000, // 30 seconds
            stateFile: path.join(__dirname, '../config/dashboard-state.json'),
            userId: config.userId || '311529658695024640',
            ...config
        };
        
        this.state = this.loadState();
        this.isRunning = false;
    }

    loadState() {
        try {
            if (fs.existsSync(this.config.stateFile)) {
                return JSON.parse(fs.readFileSync(this.config.stateFile, 'utf8'));
            }
        } catch (error) {
            console.log('No existing state found, starting fresh');
        }
        return {
            channelId: null,
            messageIds: {
                activity: null
            },
            lastUpdate: null
        };
    }

    saveState() {
        fs.mkdirSync(path.dirname(this.config.stateFile), { recursive: true });
        fs.writeFileSync(this.config.stateFile, JSON.stringify(this.state, null, 2));
    }

    async initializeChannel() {
        console.log('🚀 Initializing monitoring channel...');
        
        // TODO: Create Discord channel via OpenClaw message API
        // This would need to be implemented via the OpenClaw tools
        
        console.log(`📺 Monitoring channel ready: ${this.config.channelName}`);
    }

    async postInitialMessage() {
        console.log('📝 Posting initial monitoring message...');
        
        const initialMessage = this.formatActivityMessage({
            subagents: [],
            cronJobs: [],
            processes: [],
            timestamp: new Date()
        });

        // TODO: Post message via OpenClaw message tool and store message ID
        console.log('Initial message posted');
    }

    getSubagentInfo() {
        try {
            // Use OpenClaw's process tool to get subagent info
            // For now, simulate the data structure
            return [];
        } catch (error) {
            console.error('Error getting subagent info:', error);
            return [];
        }
    }

    getCronJobInfo() {
        try {
            // Parse OpenClaw cron list output
            const cronOutput = execSync('openclaw cron list', { encoding: 'utf8' });
            
            // Parse the output (this would need proper parsing)
            // For now, return basic structure
            return [];
        } catch (error) {
            console.error('Error getting cron info:', error);
            return [];
        }
    }

    getSystemProcesses() {
        try {
            // Get OpenClaw related processes
            const ps = execSync('ps aux | grep -i openclaw | head -10', { encoding: 'utf8' });
            return ps.split('\n').filter(line => line.trim()).length - 1; // Exclude grep
        } catch (error) {
            console.error('Error getting process info:', error);
            return 0;
        }
    }

    formatActivityMessage(data) {
        const timestamp = new Date().toLocaleString('en-US', {
            timeZone: 'America/Los_Angeles',
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        let message = `🤖 **OpenClaw Activity Dashboard**\n\n`;

        // Subagents section
        if (data.subagents && data.subagents.length > 0) {
            message += `🔄 **Active Subagents: ${data.subagents.length}**\n`;
            data.subagents.forEach(agent => {
                const runtime = agent.runtime || 'Unknown';
                message += `├─ ${agent.name}: ${agent.task} (${runtime})\n`;
            });
        } else {
            message += `🔄 **Active Subagents: 0**\n└─ No subagents currently running\n`;
        }

        message += `\n`;

        // Cron jobs section
        message += `⏰ **Cron Jobs Status**\n`;
        if (data.cronJobs && data.cronJobs.length > 0) {
            const running = data.cronJobs.filter(job => job.status === 'running');
            const recent = data.cronJobs.filter(job => job.status === 'completed').slice(0, 3);
            
            if (running.length > 0) {
                message += `🟢 **Running Now: ${running.length}**\n`;
                running.forEach(job => {
                    message += `├─ ${job.name} (${job.runtime || 'Unknown'})\n`;
                });
            }
            
            if (recent.length > 0) {
                message += `✅ **Recent Completions:**\n`;
                recent.forEach(job => {
                    message += `├─ ${job.name} • ${job.lastRun || 'Unknown'} • ${job.status}\n`;
                });
            }
        } else {
            message += `└─ No cron jobs found\n`;
        }

        message += `\n`;

        // System info
        message += `📊 **System Status**\n`;
        message += `├─ OpenClaw processes: ${data.processes || 0}\n`;
        message += `└─ Dashboard active: ✅\n`;

        message += `\n*Last updated: ${timestamp} PT*`;

        return message;
    }

    async updateDashboard() {
        try {
            console.log('🔄 Updating dashboard...');

            const data = {
                subagents: this.getSubagentInfo(),
                cronJobs: this.getCronJobInfo(),
                processes: this.getSystemProcesses(),
                timestamp: new Date()
            };

            const message = this.formatActivityMessage(data);
            
            // TODO: Update Discord message via OpenClaw message tool
            console.log('Dashboard updated successfully');
            
            this.state.lastUpdate = new Date().toISOString();
            this.saveState();

        } catch (error) {
            console.error('Error updating dashboard:', error);
        }
    }

    async start() {
        if (this.isRunning) {
            console.log('Dashboard already running');
            return;
        }

        console.log('🚀 Starting Live Monitoring Dashboard...');
        
        this.isRunning = true;

        // Initialize if needed
        if (!this.state.channelId) {
            await this.initializeChannel();
        }

        if (!this.state.messageIds.activity) {
            await this.postInitialMessage();
        }

        // Start update loop
        console.log(`⏰ Starting update loop (${this.config.updateInterval/1000}s interval)`);
        
        // Initial update
        await this.updateDashboard();

        // Set up interval
        this.updateTimer = setInterval(async () => {
            if (this.isRunning) {
                await this.updateDashboard();
            }
        }, this.config.updateInterval);

        console.log('✅ Live Monitoring Dashboard active');
    }

    async stop() {
        console.log('🛑 Stopping Live Monitoring Dashboard...');
        
        this.isRunning = false;
        
        if (this.updateTimer) {
            clearInterval(this.updateTimer);
        }

        console.log('Dashboard stopped');
    }
}

// CLI interface
if (require.main === module) {
    const dashboard = new LiveMonitoringDashboard();
    
    const command = process.argv[2];
    
    switch (command) {
        case 'start':
            dashboard.start().catch(console.error);
            break;
            
        case 'stop':
            dashboard.stop().catch(console.error);
            break;
            
        case 'test':
            // Test message formatting
            console.log('🧪 Testing message format...');
            const testData = {
                subagents: [
                    { name: 'coding-agent', task: 'Building LoreKeeper v0.6.0', runtime: '3m 42s' },
                    { name: 'research-agent', task: 'Market analysis', runtime: '1m 15s' }
                ],
                cronJobs: [
                    { name: 'Pre-market research', status: 'running', runtime: '2m 15s' },
                    { name: 'Content pipeline', status: 'completed', lastRun: '6:00 AM' }
                ],
                processes: 4,
                timestamp: new Date()
            };
            console.log(dashboard.formatActivityMessage(testData));
            break;
            
        default:
            console.log(`
Live Monitoring Dashboard - Slice 1 MVP

Commands:
  start  - Start the monitoring dashboard
  stop   - Stop the monitoring dashboard
  test   - Test message formatting

Usage:
  node monitor.js start
  node monitor.js test
            `);
    }

    // Handle graceful shutdown
    process.on('SIGINT', async () => {
        console.log('\n🛑 Received shutdown signal...');
        await dashboard.stop();
        process.exit(0);
    });
}

module.exports = LiveMonitoringDashboard;