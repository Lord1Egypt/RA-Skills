/**
 * Skill Security Scanner - Node.js 版本
 * 扫描所有已安装的 skill
 */

const fs = require('fs').promises;
const path = require('path');

// 检测器（从 bash 规则移植）
class SecurityDetector {
    constructor() {
        this.rules = {
            // 命令注入
            cmdInjection: [
                { pattern: /npx|npm\s+exec|yarn\s+exec|pnpm\s+exec/, level: 'critical', score: 30, desc: '命令注入' },
                { pattern: /curl.*\|.*bash|wget.*\|.*bash/, level: 'critical', score: 30, desc: '远程脚本' },
                { pattern: /`.*\$.*`|\$\(.*\)/, level: 'high', score: 15, desc: '命令替换' }
            ],
            // 凭证访问
            credentials: [
                { pattern: /credentials\/|vault\/(?!crypto\/)/, level: 'critical', score: 25, desc: '凭证访问' },
                { pattern: /0x[a-f0-9]{64}/, level: 'critical', score: 30, desc: '私钥' },
                { pattern: /eth\.wallet|web3\.ethers/, level: 'high', score: 20, desc: '钱包' },
                { pattern: /process\.env\.(AWS_|AZURE_|STRIPE_|GOOGLE_)/, level: 'critical', score: 30, desc: 'API密钥' }
            ],
            // 木马/后门
            trojan: [
                { pattern: /net\.createServer|net\.connect|net\.Socket/, level: 'critical', score: 25, desc: '网络后门' },
                { pattern: /http\.createServer|http\.request/, level: 'high', score: 20, desc: 'HTTP服务器' },
                { pattern: /ws\.Server|socket\.io|WebSocketServer/, level: 'high', score: 20, desc: 'WebSocket' },
                { pattern: /fs\.writeFileSync.*process\.env|fs\.writeFile.*password/, level: 'critical', score: 25, desc: '敏感文件写入' },
                { pattern: /fs\.readFile.*\.ssh|fs\.readFile.*credential/, level: 'critical', score: 25, desc: '凭证读取' },
                { pattern: /child_process\.spawn.*sh.*-c|curl.*http/, level: 'critical', score: 25, desc: '远程命令' },
                { pattern: /setInterval.*1000.*60.*24/, level: 'medium', score: 15, desc: '长时间定时' }
            ],
            // AI投毒
            promptPoison: [
                { pattern: /ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?)/, level: 'high', score: 20, desc: '提示注入' },
                { pattern: /disregard\s+(all\s+)?(your\s+)?(instructions?)/, level: 'high', score: 20, desc: '提示注入' },
                { pattern: /\b(jailbreak|bypass|disable\s+safety)\b/, level: 'critical', score: 25, desc: '越狱攻击' },
                { pattern: /\b(DAN|do\s+anything\s+now)\b/, level: 'critical', score: 25, desc: 'DAN越狱' },
                { pattern: /roleplay\s+(as|with)\s+(evil|malicious)/, level: 'critical', score: 25, desc: '恶意角色' },
                { pattern: /(show|tell|reveal).*(system\s+)?prompt/, level: 'high', score: 20, desc: '提示提取' }
            ],
            // 混淆/间接
            obfuscation: [
                { pattern: /Buffer\.from.*base64|atob\(|btoa\(/, level: 'high', score: 20, desc: 'Base64混淆' },
                { pattern: /\\x[0-9a-f]{2}/, level: 'high', score: 20, desc: 'Hex编码' },
                { pattern: /new\s+Function\(|Function\(|eval\(/, level: 'critical', score: 25, desc: '间接执行' },
                { pattern: /if.*NODE_ENV.*production/, level: 'high', score: 20, desc: '生产触发' }
            ]
        };
        
        // 官方技能白名单
        this.officialSkills = [
            'blogwatcher', 'skill-creator', 'github', 'weather', 
            'video-frames', 'openai-whisper', 'healthcheck'
        ];
    }
    
    // 扫描文件
    async scanFile(filePath) {
        const issues = [];
        try {
            const content = await fs.readFile(filePath, 'utf8');
            
            for (const [category, rules] of Object.entries(this.rules)) {
                for (const rule of rules) {
                    if (rule.pattern.test(content)) {
                        issues.push({
                            category,
                            ...rule,
                            file: path.basename(filePath)
                        });
                    }
                }
            }
        } catch (e) {
            // 忽略读取错误
        }
        return issues;
    }
    
    // 扫描 skill 目录
    async scanSkill(skillPath) {
        const skillName = path.basename(skillPath);
        const allIssues = [];
        let filesScanned = 0;
        
        // 递归扫描所有 JS 文件
        const scanDir = async (dir) => {
            try {
                const entries = await fs.readdir(dir, { withFileTypes: true });
                for (const entry of entries) {
                    const fullPath = path.join(dir, entry.name);
                    if (entry.isDirectory() && !entry.name.startsWith('.')) {
                        await scanDir(fullPath);
                    } else if (entry.name.endsWith('.js')) {
                        filesScanned++;
                        const issues = await this.scanFile(fullPath);
                        allIssues.push(...issues);
                    }
                }
            } catch (e) {}
        };
        
        await scanDir(skillPath);
        
        // 计算评分
        let score = 100;
        const criticalCount = allIssues.filter(i => i.level === 'critical').length;
        const highCount = allIssues.filter(i => i.level === 'high').length;
        const mediumCount = allIssues.filter(i => i.level === 'medium').length;
        
        score -= criticalCount * 25;
        score -= highCount * 15;
        score -= mediumCount * 10;
        score = Math.max(0, score);
        
        // 评估可信度
        let trustLevel = 'low';
        if (this.officialSkills.includes(skillName)) {
            trustLevel = 'high';
        } else if (skillPath.includes('.openclaw/workspace/skills')) {
            trustLevel = 'medium';
        }
        
        return {
            skillName,
            skillPath,
            score,
            trustLevel,
            issues: allIssues,
            filesScanned,
            criticalCount,
            highCount,
            mediumCount
        };
    }
    
    // 扫描 skills 目录
    async scanAll(skillsDir) {
        const results = [];
        
        try {
            const entries = await fs.readdir(skillsDir, { withFileTypes: true });
            const skillDirs = entries.filter(e => e.isDirectory() && !e.name.includes('skill-security-scanner'));
            
            console.log(`🔍 扫描目录: ${skillsDir}`);
            console.log(`📦 发现 ${skillDirs.length} 个 skills\n`);
            
            for (const entry of skillDirs) {
                const skillPath = path.join(skillsDir, entry.name);
                const result = await this.scanSkill(skillPath);
                results.push(result);
                
                // 打印进度
                const status = result.score < 70 ? '⚠️' : '✅';
                console.log(`  ${status} ${result.skillName}: ${result.score}/100`);
            }
        } catch (e) {
            console.error('❌ 无法读取目录:', e.message);
        }
        
        return results;
    }
    
    // 生成汇总报告
    generateReport(results) {
        const pass = results.filter(r => r.score >= 70).length;
        const warn = results.filter(r => r.score < 70 && r.score >= 50).length;
        const fail = results.filter(r => r.score < 50).length;
        
        console.log('\n' + '='.repeat(60));
        console.log('                    📊 扫描汇总报告');
        console.log('='.repeat(60));
        console.log(`\n📦 扫描总数: ${results.length}`);
        console.log(`✅ 通过: ${pass}`);
        console.log(`⚠️  建议审查: ${warn}`);
        console.log(`🚫 禁止运行: ${fail}`);
        
        // 高风险列表
        const risky = results.filter(r => r.score < 70).sort((a, b) => a.score - b.score);
        if (risky.length > 0) {
            console.log('\n⚠️  需要关注的 skills:');
            for (const r of risky) {
                const icon = r.score < 50 ? '🚫' : '⚠️';
                console.log(`  ${icon} ${r.skillName}: ${r.score}/100 (${r.issues.length} 个问题)`);
            }
        }
        
        return { pass, warn, fail, results };
    }
}

module.exports = { SecurityDetector };
