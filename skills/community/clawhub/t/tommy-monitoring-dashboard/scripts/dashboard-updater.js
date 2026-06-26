#!/usr/bin/env node

/**
 * Live Dashboard Updater - Fixed formatting version
 * Ensures clean message formatting without corruption
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class LiveDashboardUpdater {
    constructor() {
        this.stateFile = path.join(__dirname, '../config/live-state.json');
        this.state = this.loadState();
    }

    loadState() {
        try {
            const data = fs.readFileSync(this.stateFile, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            console.error('❌ No state file found. Run initial setup first.');
            return null;
        }
    }

    saveState() {
        fs.writeFileSync(this.stateFile, JSON.stringify(this.state, null, 2));
    }

    getCurrentData() {
        try {
            // Get cron jobs
            const cronText = execSync('openclaw cron list', { 
                encoding: 'utf8',
                timeout: 5000
            });
            
            const cronLines = cronText.split('\\n').filter(line => line.trim());
            const cronJobs = cronLines.slice(0, 5).map(line => {
                return {
                    name: this.extractJobName(line),
                    status: 'active'
                };
            });

            // Get system processes
            const processes = this.getOpenClawProcesses();

            // Subagents (placeholder for now)
            const subagents = [];

            return {
                subagents,
                cronJobs,
                processes,
                timestamp: new Date()
            };
        } catch (error) {
            return {
                subagents: [],
                cronJobs: [],
                processes: 0,
                timestamp: new Date(),
                error: error.message
            };
        }
    }

    extractJobName(cronLine) {
        // Clean job name extraction
        if (cronLine.length < 30) return cronLine.trim();
        
        // Look for meaningful job names
        const patterns = [
            /Live Monitoring Dashboard/i,
            /Pre-market research/i,
            /Post-market review/i,
            /Memory curation/i,
            /Tesla monitoring/i,
            /BP reminder/i,
            /Content pipeline/i,
            /([a-zA-Z][a-zA-Z ]*(?:research|review|curation|monitoring|reminder|pipeline))/i,
            /([A-Z][a-zA-Z ]{5,25})/
        ];
        
        for (const pattern of patterns) {
            const match = cronLine.match(pattern);
            if (match) {
                const name = match[1] || match[0];
                return name.trim().length > 25 ? name.trim().substring(0, 22) + '...' : name.trim();
            }
        }
        
        return cronLine.substring(0, 22) + '...';
    }

    getOpenClawProcesses() {
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

    formatDashboard(data) {
        const timestamp = new Date().toLocaleString('en-US', {
            timeZone: 'America/Los_Angeles',
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        // Build clean message parts
        const parts = [];
        
        parts.push('🤖 **OpenClaw Live Dashboard**');
        parts.push(''); // blank line

        // Subagents section
        if (data.subagents && data.subagents.length > 0) {
            parts.push(`🔄 **Active Subagents: ${data.subagents.length}**`);
            data.subagents.forEach(agent => {
                parts.push(`├─ ${agent.name}: ${agent.task}`);
            });
        } else {
            parts.push('🔄 **Active Subagents: 0**');
            parts.push('└─ All quiet');
        }
        
        parts.push(''); // blank line

        // Cron Jobs section
        parts.push('⏰ **Cron Jobs**');
        if (data.cronJobs && data.cronJobs.length > 0) {
            parts.push(`├─ Total active: ${data.cronJobs.length}`);
            parts.push('└─ Recent:');
            
            data.cronJobs.forEach((job, index) => {
                const isLast = index === data.cronJobs.length - 1;
                const prefix = isLast ? '   └─' : '   ├─';
                parts.push(`${prefix} ${job.name} (${job.status})`);
            });
        } else {
            parts.push('└─ No jobs found');
        }

        parts.push(''); // blank line

        // System section
        parts.push('📊 **System**');
        parts.push(`├─ OpenClaw processes: ${data.processes}`);
        parts.push('├─ Dashboard: 🟢 Live');
        parts.push(`└─ Updated: ${timestamp} PT`);

        // Join with proper newlines - no escaping needed
        return parts.join('\\n');
    }

    generateUpdate() {
        const data = this.getCurrentData();
        return this.formatDashboard(data);
    }

    updateState() {
        this.state.lastUpdate = new Date().toISOString();
        this.state.updateCount = (this.state.updateCount || 1) + 1;
        this.saveState();
    }
}

// CLI interface
if (require.main === module) {
    const updater = new LiveDashboardUpdater();
    
    if (!updater.state) {
        console.error('❌ Dashboard not initialized.');
        process.exit(1);
    }

    const updateMessage = updater.generateUpdate();
    updater.updateState();

    console.log('📊 Dashboard update ready:');
    console.log('─'.repeat(50));
    console.log(updateMessage);
    console.log('─'.repeat(50));
    console.log(`Message ID: ${updater.state.messageId}`);
}

module.exports = LiveDashboardUpdater;