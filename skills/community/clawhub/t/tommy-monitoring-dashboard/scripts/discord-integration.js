#!/usr/bin/env node

/**
 * Live Monitoring Dashboard - Discord Integration (Slice 2)
 * Real Discord integration using OpenClaw message tool
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class DiscordLiveMonitoring {
    constructor(config = {}) {
        this.config = {
            channelName: config.channelName || 'tommy-monitoring',
            updateInterval: config.updateInterval || 30000,
            userId: '311529658695024640',
            stateFile: path.join(__dirname, '../config/live-state.json'),
            ...config
        };
        
        this.state = this.loadState();
        this.isRunning = false;
    }

    loadState() {
        try {
            if (fs.existsSync(this.config.stateFile)) {
                const data = fs.readFileSync(this.config.stateFile, 'utf8');
                return JSON.parse(data);
            }
        } catch (error) {
            console.log('No existing state, starting fresh...');
        }
        
        return {
            channelId: null,
            messageId: null,
            lastUpdate: null,
            created: null
        };
    }

    saveState() {
        try {
            fs.mkdirSync(path.dirname(this.config.stateFile), { recursive: true });
            fs.writeFileSync(this.config.stateFile, JSON.stringify(this.state, null, 2));
            console.log('✅ State saved');
        } catch (error) {
            console.error('❌ Error saving state:', error);
        }
    }

    async createMonitoringChannel() {
        console.log('📺 Creating monitoring channel...');
        
        // We'll use the OpenClaw session to create this
        // For now, we'll assume it exists and return a placeholder
        console.log(`✅ Channel ready: #${this.config.channelName}`);
        
        this.state.channelId = 'monitoring_channel';
        this.state.created = new Date().toISOString();
        this.saveState();
        
        return this.state.channelId;
    }

    getCurrentData() {
        try {
            // Get cron jobs
            const cronJobs = this.getCronJobs();
            
            // Get system processes
            const processes = this.getSystemProcesses();
            
            // Get subagents (placeholder for now)
            const subagents = [];
            
            return {
                subagents,
                cronJobs: cronJobs.slice(0, 5), // Top 5
                processes,
                timestamp: new Date()
            };
        } catch (error) {
            console.error('Error getting data:', error);
            return {
                subagents: [],
                cronJobs: [],
                processes: 0,
                timestamp: new Date(),
                error: error.message
            };
        }
    }

    getCronJobs() {
        try {
            const cronText = execSync('openclaw cron list', { 
                encoding: 'utf8',
                timeout: 5000
            });
            
            const lines = cronText.split('\\n').filter(line => line.trim());
            return lines.slice(0, 5).map((line, index) => {
                // Basic parsing - could be enhanced
                const parts = line.trim().split(/\\s+/);
                return {
                    id: parts[0] || `job_${index}`,
                    name: this.truncateName(line),
                    status: 'active',
                    schedule: 'configured'
                };
            });
        } catch (error) {
            return [{
                id: 'error',
                name: 'Cron fetch failed',
                status: 'error',
                schedule: 'unknown'
            }];
        }
    }

    truncateName(fullLine) {
        // Extract a reasonable name from the cron list line
        if (fullLine.length <= 25) return fullLine;
        
        // Try to find a meaningful part
        const parts = fullLine.split(/\\s+/);
        if (parts.length > 1) {
            return parts[1].substring(0, 22) + '...';
        }
        
        return fullLine.substring(0, 22) + '...';
    }

    getSystemProcesses() {
        try {
            const ps = execSync('ps aux | grep -i openclaw | grep -v grep', { 
                encoding: 'utf8',
                timeout: 3000
            });
            return ps.split('\\n').filter(line => line.trim()).length;
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

        let message = `🤖 **OpenClaw Live Dashboard**\\n\\n`;

        // Error handling
        if (data.error) {
            message += `⚠️ **Error:** ${data.error}\\n\\n`;
        }

        // Subagents
        if (data.subagents && data.subagents.length > 0) {
            message += `🔄 **Active Subagents: ${data.subagents.length}**\\n`;
            data.subagents.forEach(agent => {
                message += `├─ ${agent.name}: ${agent.task}\\n`;
            });
        } else {
            message += `🔄 **Active Subagents: 0**\\n└─ All quiet\\n`;
        }

        message += `\\n`;

        // Cron Jobs
        message += `⏰ **Cron Jobs**\\n`;
        if (data.cronJobs && data.cronJobs.length > 0) {
            message += `├─ Total active: ${data.cronJobs.length}\\n`;
            message += `└─ Recent:\\n`;
            
            data.cronJobs.forEach((job, index) => {
                const isLast = index === data.cronJobs.length - 1;
                const prefix = isLast ? '   └─' : '   ├─';
                message += `${prefix} ${job.name} (${job.status})\\n`;
            });
        } else {
            message += `└─ No jobs found\\n`;
        }

        message += `\\n`;

        // System Status
        message += `📊 **System**\\n`;
        message += `├─ OpenClaw processes: ${data.processes}\\n`;
        message += `├─ Dashboard: 🟢 Live\\n`;
        message += `└─ Updated: ${timestamp} PT`;

        return message;
    }

    // This will be called from within an OpenClaw session context
    generateOpenClawScript(data) {
        const message = this.formatDashboardMessage(data);
        
        return `
// OpenClaw session script for Discord integration
const dashboardMessage = \`${message}\`;

if (!process.env.LIVE_MESSAGE_ID) {
    // First time - post new message
    console.log('📝 Posting initial dashboard message...');
    
    const result = message({
        action: 'send',
        target: 'user:311529658695024640',
        message: dashboardMessage
    });
    
    if (result.ok) {
        console.log('✅ Dashboard posted, message ID:', result.result.messageId);
        // Store the message ID for future edits
        process.env.LIVE_MESSAGE_ID = result.result.messageId;
    }
} else {
    // Update existing message
    console.log('✏️ Updating dashboard message...');
    
    const result = message({
        action: 'edit', 
        messageId: process.env.LIVE_MESSAGE_ID,
        message: dashboardMessage
    });
    
    if (result.ok) {
        console.log('✅ Dashboard updated');
    } else {
        console.log('❌ Update failed:', result);
    }
}

console.log('Dashboard message prepared');
`;
    }

    async postInitialDashboard() {
        console.log('🚀 Setting up live Discord dashboard...');
        
        const data = this.getCurrentData();
        const script = this.generateOpenClawScript(data);
        
        console.log('📝 Generated OpenClaw integration script:');
        console.log('─'.repeat(50));
        console.log(script);
        console.log('─'.repeat(50));
        
        // Save the script for manual execution
        const scriptPath = path.join(__dirname, 'discord-post.js');
        fs.writeFileSync(scriptPath, script);
        
        console.log(`✅ Script saved to: ${scriptPath}`);
        console.log('');
        console.log('🎯 Next steps:');
        console.log('1. Run this from an OpenClaw session:');
        console.log(`   exec('node ${scriptPath}')`);
        console.log('2. Or integrate with cron for automatic updates');
        
        return scriptPath;
    }

    async runUpdate() {
        const data = this.getCurrentData();
        console.log('📊 Current dashboard data:');
        console.log('─'.repeat(50));
        console.log(this.formatDashboardMessage(data));
        console.log('─'.repeat(50));
        
        // Generate the script for updating
        const script = this.generateOpenClawScript(data);
        
        const updateScript = path.join(__dirname, 'discord-update.js');
        fs.writeFileSync(updateScript, script);
        
        console.log(`✅ Update script ready: ${updateScript}`);
        return updateScript;
    }
}

// CLI interface
if (require.main === module) {
    const monitor = new DiscordLiveMonitoring();
    const command = process.argv[2];
    
    switch (command) {
        case 'init':
            monitor.postInitialDashboard().catch(console.error);
            break;
            
        case 'update':
            monitor.runUpdate().catch(console.error);
            break;
            
        case 'data':
            const data = monitor.getCurrentData();
            console.log(JSON.stringify(data, null, 2));
            break;
            
        default:
            console.log(`
Live Monitoring Dashboard - Discord Integration

Commands:
  init    - Set up initial Discord dashboard
  update  - Generate update script
  data    - Show current monitoring data

Usage:
  node discord-integration.js init
  node discord-integration.js update
            `);
    }
}

module.exports = DiscordLiveMonitoring;