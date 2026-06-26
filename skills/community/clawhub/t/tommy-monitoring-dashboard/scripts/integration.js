#!/usr/bin/env node

/**
 * OpenClaw Integration Layer for Live Monitoring Dashboard
 * Interfaces with OpenClaw's native tools
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');

class OpenClawIntegration {
    constructor(userId = '311529658695024640') {
        this.userId = userId;
    }

    /**
     * Get current subagent information via OpenClaw
     */
    async getSubagents() {
        try {
            // We need to call OpenClaw's process tool
            // This would be done via the OpenClaw session, not directly
            // For now, simulate the structure we expect
            return [];
        } catch (error) {
            console.error('Error getting subagents:', error);
            return [];
        }
    }

    /**
     * Get cron job information
     */
    async getCronJobs() {
        try {
            const cronList = execSync('openclaw cron list --json', { 
                encoding: 'utf8',
                timeout: 5000
            });
            
            // Parse the JSON output
            const jobs = JSON.parse(cronList);
            
            // Transform to our format
            return jobs.map(job => ({
                id: job.id,
                name: job.name || 'Unknown Job',
                status: job.enabled ? 'active' : 'disabled',
                schedule: job.schedule,
                lastRun: job.lastRun,
                nextRun: job.nextRun
            }));
            
        } catch (error) {
            // Fallback to text parsing if JSON not available
            try {
                const cronText = execSync('openclaw cron list', { 
                    encoding: 'utf8',
                    timeout: 5000
                });
                
                // Basic text parsing - this would need refinement
                const lines = cronText.split('\n').filter(line => line.trim());
                return lines.slice(0, 5).map((line, index) => ({
                    id: `job_${index}`,
                    name: line.substring(0, 30) + '...',
                    status: 'active',
                    schedule: 'unknown',
                    lastRun: 'unknown'
                }));
                
            } catch (textError) {
                console.error('Error getting cron jobs:', textError);
                return [];
            }
        }
    }

    /**
     * Create Discord channel via OpenClaw message tool
     */
    async createChannel(channelName = '#monitoring') {
        try {
            // This would need to be implemented via OpenClaw's message tool
            // For now, we'll return a simulated channel ID
            console.log(`📺 Would create channel: ${channelName}`);
            return 'simulated_channel_id';
        } catch (error) {
            console.error('Error creating channel:', error);
            return null;
        }
    }

    /**
     * Post message to Discord via OpenClaw
     */
    async postMessage(content, channelId = null) {
        try {
            // This would use OpenClaw's message tool
            console.log(`📝 Would post message to ${channelId || 'default channel'}`);
            console.log('Content preview:', content.substring(0, 100) + '...');
            
            // Return simulated message ID
            return 'simulated_message_id';
        } catch (error) {
            console.error('Error posting message:', error);
            return null;
        }
    }

    /**
     * Update existing Discord message
     */
    async updateMessage(messageId, content) {
        try {
            // This would use OpenClaw's message tool to edit
            console.log(`✏️ Would update message ${messageId}`);
            return true;
        } catch (error) {
            console.error('Error updating message:', error);
            return false;
        }
    }

    /**
     * Test OpenClaw connectivity
     */
    async testConnectivity() {
        const tests = [];

        // Test OpenClaw CLI
        try {
            execSync('openclaw --version', { timeout: 3000, stdio: 'pipe' });
            tests.push({ name: 'OpenClaw CLI', status: '✅ Available' });
        } catch (error) {
            tests.push({ name: 'OpenClaw CLI', status: '❌ Not found' });
        }

        // Test cron command
        try {
            execSync('openclaw cron list', { timeout: 5000, stdio: 'pipe' });
            tests.push({ name: 'Cron monitoring', status: '✅ Available' });
        } catch (error) {
            tests.push({ name: 'Cron monitoring', status: '❌ Error' });
        }

        // Test system commands
        try {
            execSync('ps aux', { timeout: 3000, stdio: 'pipe' });
            tests.push({ name: 'System monitoring', status: '✅ Available' });
        } catch (error) {
            tests.push({ name: 'System monitoring', status: '❌ Error' });
        }

        return tests;
    }
}

// Test connectivity if run directly
if (require.main === module) {
    const integration = new OpenClawIntegration();
    
    console.log('🔧 Testing OpenClaw Integration...\n');
    
    integration.testConnectivity().then(tests => {
        tests.forEach(test => {
            console.log(`${test.status} ${test.name}`);
        });
        
        console.log('\n🎯 Testing cron job fetching...');
        return integration.getCronJobs();
    }).then(jobs => {
        console.log(`Found ${jobs.length} cron jobs:`);
        jobs.slice(0, 3).forEach(job => {
            console.log(`  - ${job.name} (${job.status})`);
        });
        
    }).catch(error => {
        console.error('Integration test failed:', error);
    });
}

module.exports = OpenClawIntegration;