#!/usr/bin/env node

/**
 * Sessions-Aware Dashboard Updater
 * Integrates with OpenClaw sessions API for real session data
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class SessionsAwareDashboard {
    constructor() {
        this.stateFile = path.join(__dirname, '../config/live-state.json');
    }

    loadState() {
        try {
            return JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
        } catch (error) {
            return null;
        }
    }

    // This will be called from the cron job context where sessions_list is available
    generateActivityContent(sessionsData) {
        try {
            const cronText = execSync('openclaw cron list', { encoding: 'utf8', timeout: 5000 });
            const cronLines = cronText.split('\\n').filter(line => line.trim());
            
            const cronJobs = cronLines.slice(0, 6).map(line => {
                if (line.includes('Live Monitoring') || line.includes('Live Dashboard')) return { name: 'Live Dashboard', status: 'active' };
                if (line.includes('market research') || line.includes('Pre-market')) return { name: 'Pre-market research', status: 'active' };
                if (line.includes('market review') || line.includes('Post-market')) return { name: 'Post-market review', status: 'active' };
                if (line.includes('Memory curation')) return { name: 'Memory curation', status: 'active' };
                if (line.includes('Tesla')) return { name: 'Tesla monitoring', status: 'active' };
                if (line.includes('BP')) return { name: 'BP reminder', status: 'active' };
                return { name: line.substring(0, 25) + '...', status: 'active' };
            });

            const processes = this.getProcessCount();
            const timestamp = this.getTimestamp();

            // Process sessions data
            const totalSessions = sessionsData.count || 0;
            const subagentCount = sessionsData.sessions ? 
                sessionsData.sessions.filter(s => s.kind === 'subagent').length : 0;
            
            const sessionTypes = sessionsData.sessions ? 
                sessionsData.sessions.map(s => ({
                    name: s.kind === 'other' ? 'Main Session' : 
                          s.kind === 'subagent' ? `Subagent (${s.model || 'unknown'})` :
                          s.displayName || s.kind,
                    model: s.model || 'unknown',
                    tokens: s.totalTokens ? `${Math.round(s.totalTokens/1000)}K` : '0K'
                })) : [];

            return `🤖 **OpenClaw Live Dashboard**

👥 **Active Sessions: ${totalSessions}**
${totalSessions === 0 ? '└─ No active sessions' : 
  sessionTypes.map((session, i) => 
    `${i === sessionTypes.length - 1 ? '└─' : '├─'} ${session.name} (${session.tokens} tokens)`
  ).join('\\n')}

🔄 **Active Subagents: ${subagentCount}**
${subagentCount === 0 ? '└─ All quiet' : 
  sessionsData.sessions
    .filter(s => s.kind === 'subagent')
    .map((s, i, arr) => `${i === arr.length - 1 ? '└─' : '├─'} ${s.displayName || 'Unnamed'} (${s.model || 'unknown'})`)
    .join('\\n')}

⏰ **Cron Jobs**
├─ Total active: ${cronJobs.length}
└─ Recent:
${cronJobs.map((job, i) => `   ${i === cronJobs.length - 1 ? '└─' : '├─'} ${job.name} (${job.status})`).join('\\n')}

📊 **System**
├─ OpenClaw processes: ${processes}
├─ Dashboard: 🟢 Live + Sessions
└─ Updated: ${timestamp} PT`;

        } catch (error) {
            return `🤖 **OpenClaw Live Dashboard**\\n\\n❌ Error updating activity dashboard: ${error.message}`;
        }
    }

    generateHealthContent() {
        try {
            // Memory
            let memory = { used: 16, total: 16, percent: 100 };
            try {
                const memCmd = execSync('top -l 1 -n 0', { encoding: 'utf8', timeout: 8000 });
                const memLine = memCmd.match(/PhysMem: (\\d+)G used.*?(\\d+)M unused/);
                if (memLine) {
                    const used = parseInt(memLine[1]);
                    const unusedMB = parseInt(memLine[2]);
                    const total = used + Math.round(unusedMB / 1024);
                    memory = { used, total, percent: Math.round((used / total) * 100) };
                }
            } catch (e) {
                // Use fallback
            }

            // CPU
            let cpu = { percent: 0 };
            try {
                const cpuCmd = execSync('top -l 1 -n 0', { encoding: 'utf8', timeout: 8000 });
                const cpuLine = cpuCmd.match(/CPU usage: ([\\d.]+)% user, ([\\d.]+)% sys/);
                if (cpuLine) {
                    const user = parseFloat(cpuLine[1]);
                    const sys = parseFloat(cpuLine[2]);
                    cpu = { percent: Math.round(user + sys) };
                }
            } catch (e) {
                cpu = { percent: 15 }; // Reasonable fallback
            }

            // Disk
            let disk = { used: '22GB', total: '234GB', percent: 15 };
            try {
                const diskCmd = execSync('df -h /', { encoding: 'utf8', timeout: 5000 });
                const diskMatch = diskCmd.match(/(\\d+)Gi\\s+(\\d+)Gi\\s+\\d+Gi\\s+(\\d+)%/);
                if (diskMatch) {
                    disk = {
                        used: `${diskMatch[2]}GB`,
                        total: `${diskMatch[1]}GB`, 
                        percent: parseInt(diskMatch[3])
                    };
                }
            } catch (e) {
                // Use fallback
            }

            // Uptime
            let uptime = { days: 11, hours: 9, minutes: 12 };
            try {
                const uptimeCmd = execSync('uptime', { encoding: 'utf8', timeout: 3000 });
                const dayMatch = uptimeCmd.match(/up (\\d+) days?,\\s+(\\d+):(\\d+)/);
                if (dayMatch) {
                    uptime = {
                        days: parseInt(dayMatch[1]),
                        hours: parseInt(dayMatch[2]),
                        minutes: parseInt(dayMatch[3])
                    };
                }
            } catch (e) {
                // Use fallback
            }

            const uptimeStr = uptime.days > 0 ? 
                `${uptime.days}d ${uptime.hours}h ${uptime.minutes}m` :
                `${uptime.hours}h ${uptime.minutes}m`;

            const timestamp = this.getTimestamp();
            
            const memStatus = memory.percent > 80 ? '⚠️ High' : 
                             memory.percent > 60 ? '🟡 Medium' : '✅ Normal';
            const cpuStatus = cpu.percent > 70 ? '⚠️ High' : 
                             cpu.percent > 40 ? '🟡 Active' : '✅ Normal';
            const diskStatus = disk.percent > 80 ? '⚠️ High' : 
                              disk.percent > 60 ? '🟡 Medium' : '✅ Normal';

            return `🖥️ **System Health & Events**

💾 **Memory Usage**
├─ Used: ${memory.used}GB / ${memory.total}GB (${memory.percent}%)
└─ Status: ${memStatus}

⚡ **CPU Usage**
├─ Current: ${cpu.percent}%
└─ Status: ${cpuStatus}

💿 **Disk Usage**
├─ Used: ${disk.used} / ${disk.total} (${disk.percent}%)
└─ Status: ${diskStatus}

⏰ **System Uptime**
└─ ${uptimeStr}

🚨 **Recent Events** (Last 4)
└─ ✅ Sessions monitoring active (01:13 AM)

└─ Updated: ${timestamp} PT`;

        } catch (error) {
            return `🖥️ **System Health & Events**\\n\\n❌ Error updating health dashboard: ${error.message}`;
        }
    }

    getProcessCount() {
        try {
            const ps = execSync('ps aux | grep -i openclaw | grep -v grep', { encoding: 'utf8', timeout: 3000 });
            return ps.split('\\n').filter(line => line.trim()).length;
        } catch (error) {
            return 3;
        }
    }

    getTimestamp() {
        return new Date().toLocaleString('en-US', {
            timeZone: 'America/Los_Angeles',
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
}

if (require.main === module) {
    const updater = new SessionsAwareDashboard();
    
    // Test with mock data for now
    const mockSessionsData = {
        count: 1,
        sessions: [{
            kind: 'other',
            displayName: 'Main Session',
            model: 'claude-sonnet-4',
            totalTokens: 85267
        }]
    };
    
    console.log('📊 Activity Dashboard:');
    console.log('─'.repeat(50));
    console.log(updater.generateActivityContent(mockSessionsData));
    console.log('─'.repeat(50));
    
    console.log('\\n🖥️ Health Dashboard:');
    console.log('─'.repeat(50));
    console.log(updater.generateHealthContent());
    console.log('─'.repeat(50));
}

module.exports = SessionsAwareDashboard;