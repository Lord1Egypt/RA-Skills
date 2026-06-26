#!/usr/bin/env node

/**
 * OpenClaw Session Runner for Live Monitoring Dashboard
 * This script is designed to be run within an OpenClaw session context
 * where it has access to the message tool and other OpenClaw capabilities
 */

// This would be the script called from within OpenClaw to actually
// interface with Discord through the message tool

const script = `
// Live Monitoring Dashboard - OpenClaw Session Integration
// This runs within the OpenClaw environment with access to tools

const { execSync } = require('child_process');

class OpenClawDashboard {
    constructor() {
        this.userId = '311529658695024640';
        this.channelName = '#tommy-monitoring';
        this.messageId = null;
    }

    async getCronJobs() {
        try {
            const cronText = execSync('openclaw cron list', { 
                encoding: 'utf8',
                timeout: 5000
            });
            
            const lines = cronText.split('\\n').filter(line => line.trim());
            return lines.slice(0, 5).map((line, index) => {
                // Parse cron list output
                const parts = line.split(/\\s+/);
                return {
                    id: parts[0] || \`job_\${index}\`,
                    name: line.substring(0, 25).trim() + '...',
                    status: 'active'
                };
            });
        } catch (error) {
            return [];
        }
    }

    getSystemInfo() {
        try {
            const processes = execSync('ps aux | grep -i openclaw | grep -v grep', { 
                encoding: 'utf8' 
            }).split('\\n').filter(line => line.trim()).length;
            
            return { processes };
        } catch (error) {
            return { processes: 0 };
        }
    }

    formatDashboard() {
        const cronJobs = this.getCronJobs();
        const systemInfo = this.getSystemInfo();
        
        const timestamp = new Date().toLocaleString('en-US', {
            timeZone: 'America/Los_Angeles',
            weekday: 'short',
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        return \`🤖 **OpenClaw Live Dashboard**

🔄 **Active Subagents: 0**
└─ All quiet

⏰ **Cron Jobs Status**
├─ Total jobs: \${cronJobs.length}
├─ Active: \${cronJobs.length}
└─ Recent:
\${cronJobs.slice(0, 3).map((job, i, arr) => {
    const isLast = i === arr.length - 1;
    const prefix = isLast ? '   └─' : '   ├─';
    return \`\${prefix} \${job.name} (\${job.status})\`;
}).join('\\n')}

📊 **System Status**
├─ OpenClaw processes: \${systemInfo.processes}
├─ Dashboard: 🟢 Active
└─ Last update: \${timestamp} PT\`;
    }

    async postToDashboard() {
        const dashboardMessage = this.formatDashboard();
        
        // This would use the OpenClaw message tool
        return dashboardMessage;
    }
}

// Export the class for OpenClaw to use
const dashboard = new OpenClawDashboard();
dashboard.postToDashboard();
`;

console.log('📝 OpenClaw Session Integration Script:');
console.log('─'.repeat(60));
console.log(script);
console.log('─'.repeat(60));

// Save the integration script
const fs = require('fs');
const path = require('path');

const integrationScript = path.join(__dirname, 'openclaw-session-runner.js');
fs.writeFileSync(integrationScript, script);

console.log(`✅ Integration script saved: ${integrationScript}`);
console.log('');
console.log('🎯 To use from OpenClaw session:');
console.log(`   exec('node ${integrationScript}')`);
console.log('');
console.log('🔧 Or integrate with cron job to run automatically');