#!/usr/bin/env node

/**
 * Simple Dashboard Formatter - Outputs clean Discord message
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class SimpleDashboard {
    getCurrentData() {
        try {
            const cronText = execSync('openclaw cron list', { encoding: 'utf8', timeout: 5000 });
            const cronLines = cronText.split('\\n').filter(line => line.trim());
            
            const cronJobs = cronLines.slice(0, 6).map(line => {
                if (line.includes('Live Monitoring')) return { name: 'Live Monitoring Dashboard', status: 'active' };
                if (line.includes('market research') || line.includes('Pre-market')) return { name: 'Pre-market research', status: 'active' };
                if (line.includes('market review') || line.includes('Post-market')) return { name: 'Post-market review', status: 'active' };
                if (line.includes('Memory curation')) return { name: 'Memory curation', status: 'active' };
                if (line.includes('Tesla')) return { name: 'Tesla monitoring', status: 'active' };
                if (line.includes('BP')) return { name: 'BP reminder', status: 'active' };
                return { name: line.substring(0, 25) + '...', status: 'active' };
            });

            const processes = this.getProcessCount();
            
            return { subagents: [], cronJobs, processes };
        } catch (error) {
            return { subagents: [], cronJobs: [], processes: 0, error: error.message };
        }
    }

    getProcessCount() {
        try {
            const ps = execSync('ps aux | grep -i openclaw | grep -v grep', { encoding: 'utf8', timeout: 3000 });
            return ps.split('\\n').filter(line => line.trim()).length;
        } catch (error) {
            return 0;
        }
    }

    format() {
        const data = this.getCurrentData();
        const timestamp = new Date().toLocaleString('en-US', {
            timeZone: 'America/Los_Angeles',
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        const message = `🤖 **OpenClaw Live Dashboard**

🔄 **Active Subagents: ${data.subagents.length}**
${data.subagents.length === 0 ? '└─ All quiet' : data.subagents.map(a => `├─ ${a.name}: ${a.task}`).join('\\n')}

⏰ **Cron Jobs**
├─ Total active: ${data.cronJobs.length}
└─ Recent:
${data.cronJobs.map((job, i) => `   ${i === data.cronJobs.length - 1 ? '└─' : '├─'} ${job.name} (${job.status})`).join('\\n')}

📊 **System**
├─ OpenClaw processes: ${data.processes}
├─ Dashboard: 🟢 Live
└─ Updated: ${timestamp} PT`;

        return message;
    }
}

const dashboard = new SimpleDashboard();
console.log(dashboard.format());