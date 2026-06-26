// index.js - OpenClaw Skill for 小红书爬虫
const path = require('path');
const { exec } = require('child_process');

class XhsCrawlerSkill {
    constructor(engine, config) {
        this.engine = engine;
        this.config = config || {};
        this.name = 'xhs-crawler';
        this.version = '1.0.0';
        
        // Python脚本路径 - 指向主程序
        this.pythonScript = path.join(__dirname, 'example_openclaw_skill.py');
        this.pythonEnv = config.pythonEnv || 'python';
        
        console.log('✅ XHS爬虫Skill加载成功');
        console.log('📁 Python脚本路径:', this.pythonScript);
        console.log('🔧 配置:', JSON.stringify(config));
    }
    
    // 辅助方法：发送回复消息
    async reply(context, message) {
        if (context && context.reply) {
            await context.reply(message);
        }
    }
    
    // 处理消息的主入口（OpenClaw 调用）
    async onMessage(message, context) {
        console.log('📨 Skill收到消息:', message);
        
        // 检查是否是 run-xhs 指令
        let text = message.text || message.content || '';
        
        // 去除 @提及 前缀（如 @openclaw5.0）
        text = text.replace(/^@\S+\s*/, '').trim();
        
        console.log('处理后文本:', text);
        
        if (text.match(/^run-xhs[：:\s]/i)) {
            // 提取关键词
            const match = text.match(/^run-xhs[：:\s]+(.+)/i);
            const keyword = match ? match[1].trim() : '';
            
            console.log('提取关键词:', keyword);
            
            if (!keyword) {
                return '❌ 请指定搜索关键词\n使用示例: run-xhs 新燕宝2025';
            }
            
            return await this.runCrawler([keyword], context);
        }
        
        // 不处理其他消息
        return null;
    }

    getCommands() {
        return [
            {
                name: 'run-xhs',
                description: '执行小红书关键词爬取',
                args: '<关键词>',
                handler: this.runCrawler.bind(this)
            },
            {
                name: 'xhs-help',
                description: '显示小红书爬虫帮助信息',
                args: '',
                handler: this.showHelp.bind(this)
            }
        ];
    }

    async runCrawler(params, context) {
        // 检查参数
        if (params.length === 0) {
            return '❌ 请指定搜索关键词\n使用示例: run-xhs 新燕宝2025';
        }
        
        // 合并参数作为关键词（支持多词）
        let keyword = params.join(' ');
        
        // 去除可能的 @提及 前缀（如 @openclaw5.0）
        keyword = keyword.replace(/^@\S+\s*/, '').trim();
        
        // 如果关键词为空，返回错误
        if (!keyword) {
            return '❌ 请指定搜索关键词\n使用示例: run-xhs 新燕宝2025';
        }
        
        // 构建指令格式（与Python程序一致）
        const command = `run-xhs：${keyword}`;
        
        console.log('提取的关键词:', keyword);
        console.log('构建的命令:', command);
        
        // 发送开始消息
        await this.reply(context, `🔍 开始搜索小红书: ${keyword}`);

        try {
            // 执行Python脚本
            const result = await this.runPythonScript(command);
            
            if (result.success) {
                // Python程序已直接发送结果到飞书，这里只返回简单提示
                return `✅ 搜索完成！结果已发送到飞书群。`;
            } else {
                return `❌ 搜索失败:\n${result.error}`;
            }
        } catch (error) {
            console.error('执行爬虫出错:', error);
            return `❌ 执行出错: ${error.message}`;
        }
    }

    runPythonScript(command) {
        return new Promise((resolve) => {
            // 构建命令（注意: command已经包含"run-xhs：关键词"）
            const cmd = `"${this.pythonEnv}" "${this.pythonScript}" "${command}"`;
            
            console.log('执行命令:', cmd);

            exec(cmd, {
                cwd: __dirname,
                encoding: 'utf8',
                timeout: 120000, // 2分钟超时（浏览器搜索需要时间）
                maxBuffer: 1024 * 1024 * 10 // 10MB buffer
            }, (error, stdout, stderr) => {
                if (error) {
                    console.error('执行错误:', error);
                    resolve({
                        success: false,
                        error: stderr || error.message
                    });
                } else {
                    console.log('执行成功，输出:', stdout);
                    resolve({
                        success: true,
                        output: stdout
                    });
                }
            });
        });
    }

    async showHelp(params, context) {
        const help = `
📱 **小红书爬虫使用帮助**

**命令格式:**
\`run-xhs <关键词>\`

**参数说明:**
- \`<关键词>\`: 要搜索的内容（必填）

**使用示例:**
- \`run-xhs 新燕宝2025\` - 搜索"新燕宝2025"
- \`run-xhs 中间带新燕宝\` - 搜索"中间带新燕宝"

**功能特性:**
✅ Cookie自动管理（过期自动二维码登录）
✅ 浏览器模拟搜索（绕过API限制）
✅ 结果自动推送到飞书群

**注意事项:**
- 搜索需要10-30秒，请耐心等待
- 如果Cookie过期，会自动发送二维码到飞书群
- 请使用手机扫码登录后继续
        `;
        return help;
    }
}

module.exports = XhsCrawlerSkill;
