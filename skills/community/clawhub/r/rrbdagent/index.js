#!/usr/bin/env node
/**
 * RRBD Admin项目智能助手技能
 * 
 * 本技能支持用户通过自然语言输入标题和文案，自动创建视频并返回视频URL
 * 同时添加记忆模块，记住用户的偏好设置
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const APIClient = require('./api_client');

class RRBDAgent {
    constructor() {
        this.client = null;
        this.isLoggedIn = false;
        this.memory = this.loadMemory();
        this.conversationContext = {};
    }
    
    loadMemory() {
        // 加载记忆模块
        const memoryFile = path.join(__dirname, 'memory.json');
        if (fs.existsSync(memoryFile)) {
            try {
                const content = fs.readFileSync(memoryFile, 'utf8');
                return JSON.parse(content);
            } catch (error) {
                console.log(`加载记忆失败: ${error.message}`);
                return {};
            }
        }
        return {
            userPreferences: {},
            recentVideos: [],
            lastLogin: null
        };
    }
    
    saveMemory() {
        // 保存记忆模块
        const memoryFile = path.join(__dirname, 'memory.json');
        try {
            fs.writeFileSync(memoryFile, JSON.stringify(this.memory, null, 2), 'utf8');
        } catch (error) {
            console.log(`保存记忆失败: ${error.message}`);
        }
    }
    
    async login(username, password) {
        // 用户登录
        if (!this.client) {
            this.client = new APIClient();
        }
        
        const result = await this.client.login(username, password);
        if (result) {
            this.isLoggedIn = true;
            this.memory.lastLogin = new Date().toISOString();
            this.saveMemory();
            return true;
        }
        return false;
    }
    
    async createVideo(title, script) {
        // 创建视频
        if (!this.isLoggedIn) {
            return { success: false, message: "请先登录系统" };
        }
        
        // 获取用户信息，检查算力余额
        console.log('正在检查算力余额...');
        const userInfo = await this.client.get_user_info();
        if (!userInfo || !userInfo.data) {
            return { success: false, message: "获取用户信息失败" };
        }
        
        const computingAmount = userInfo.data.computingAmount || 0;
        console.log(`当前算力余额: ${computingAmount}`);
        
        if (computingAmount < 100) {
            return { success: false, message: `算力不足！当前算力余额: ${computingAmount}，需要至少100算力` };
        }
        console.log('算力检查通过！');
        
        // 获取数字人形象列表
        const virtualManList = await this.client.get_virtual_man_list();
        if (!virtualManList) {
            return { success: false, message: "获取数字人形象列表失败" };
        }
        
        // 选择第一个数字人（使用 virtualmanId 字段）
        let figureId = null;
        if (virtualManList.data) {
            if (Array.isArray(virtualManList.data) && virtualManList.data.length > 0) {
                figureId = virtualManList.data[0].virtualmanId || virtualManList.data[0].id;
            } else if (virtualManList.data.records && virtualManList.data.records.length > 0) {
                figureId = virtualManList.data.records[0].virtualmanId || virtualManList.data.records[0].id;
            }
        }
        
        if (!figureId) {
            return { success: false, message: "未找到数字人形象" };
        }
        console.log(`选择数字人ID: ${figureId}`);
        
        // 获取声音列表
        const voiceList = await this.client.get_voice_list();
        if (!voiceList) {
            return { success: false, message: "获取声音列表失败" };
        }
        
        // 选择第一个声音（使用 speakerId 字段）
        let speakerId = null;
        if (voiceList.data) {
            if (Array.isArray(voiceList.data) && voiceList.data.length > 0) {
                speakerId = voiceList.data[0].speakerId || voiceList.data[0].id;
            } else if (voiceList.data.records && voiceList.data.records.length > 0) {
                speakerId = voiceList.data.records[0].speakerId || voiceList.data.records[0].id;
            }
        }
        
        if (!speakerId) {
            return { success: false, message: "未找到声音" };
        }
        console.log(`选择声音ID: ${speakerId}`);
        
        // 获取模板列表
        const templateList = await this.client.get_template_list();
        if (!templateList) {
            return { success: false, message: "获取模板列表失败" };
        }
        
        // 选择第一个模板
        let templateId = null;
        if (templateList.data && templateList.data.results && templateList.data.results.length > 0) {
            templateId = templateList.data.results[0].id;
        }
        
        if (!templateId) {
            return { success: false, message: "未找到模板" };
        }
        
        // 创建视频
        const result = await this.client.create_video(figureId, speakerId, script, templateId, title);
        if (!result) {
            return { success: false, message: "视频创建失败" };
        }
        
        // 获取视频ID
        let videoId = null;
        if (result.data) {
            if (typeof result.data === 'object') {
                videoId = result.data.id || result.data.videoId;
            } else {
                videoId = result.data;
            }
        }
        
        if (!videoId) {
            return { success: false, message: "获取视频ID失败" };
        }
        
        // 等待视频创建完成
        const maxRetries = 30; // 最多检查30次，约3分钟
        const retryInterval = 6000; // 每6秒检查一次
        
        for (let i = 0; i < maxRetries; i++) {
            await new Promise(resolve => setTimeout(resolve, retryInterval));
            const statusResponse = await this.client.get_video_status(videoId, title);
            
            if (statusResponse && statusResponse.data) {
                const videoData = statusResponse.data;
                if (videoData) {
                    const status = videoData.status;
                    const videoUrl = videoData.videoUrl;
                    
                    if (status === 'succeed' && videoUrl) {
                        // 保存到记忆中
                        this.memory.recentVideos.push({
                            id: videoId,
                            title: title,
                            createdAt: new Date().toISOString(),
                            videoUrl: videoUrl
                        });
                        // 只保留最近10个视频
                        if (this.memory.recentVideos.length > 10) {
                            this.memory.recentVideos = this.memory.recentVideos.slice(-10);
                        }
                        this.saveMemory();
                        return { success: true, videoUrl: videoUrl };
                    } else if (status === 'failed') {
                        return { success: false, message: "视频创建失败" };
                    }
                }
            }
        }
        
        return { success: false, message: "视频创建超时" };
    }
    
    handleUserInput(userInput) {
        // 处理用户输入
        userInput = userInput.trim();
        
        // 解析用户输入
        if (userInput.includes('登录')) {
            // 提取账号密码
            const usernameMatch = userInput.match(/账号是(\d+)/);
            const passwordMatch = userInput.match(/密码是(\w+)/);
            
            if (usernameMatch && passwordMatch) {
                const username = usernameMatch[1];
                const password = passwordMatch[1];
                return {
                    type: 'login',
                    username: username,
                    password: password
                };
            } else {
                // 需要询问账号密码
                this.conversationContext.intent = 'login';
                return {
                    type: 'ask',
                    message: "请提供您的账号（手机号）"
                };
            }
        }
        
        // 处理登录上下文
        if (this.conversationContext.intent === 'login') {
            if (!this.conversationContext.username) {
                this.conversationContext.username = userInput;
                return {
                    type: 'ask',
                    message: "请提供您的密码"
                };
            } else {
                const username = this.conversationContext.username;
                const password = userInput;
                this.conversationContext = {};
                return {
                    type: 'login',
                    username: username,
                    password: password
                };
            }
        }
        
        // 处理视频创建
        if (userInput.includes('创建视频') || userInput.includes('生成视频')) {
            // 提取文案
            const scriptMatch = userInput.match(/文案是：([^，。]+)/);
            if (scriptMatch) {
                const script = scriptMatch[1];
                // 提取标题
                const titleMatch = userInput.match(/标题是：([^，。]+)/);
                const title = titleMatch ? titleMatch[1] : `视频_${Date.now()}`;
                
                // 检查是否已登录
                if (!this.isLoggedIn) {
                    this.conversationContext.intent = 'createVideo';
                    this.conversationContext.title = title;
                    this.conversationContext.script = script;
                    return {
                        type: 'ask',
                        message: "请提供您的账号（手机号）"
                    };
                } else {
                    return {
                        type: 'createVideo',
                        title: title,
                        script: script
                    };
                }
            } else {
                // 需要询问标题和文案
                this.conversationContext.intent = 'askVideoInfo';
                return {
                    type: 'ask',
                    message: "请提供视频标题和文案，例如：标题是：测试视频，文案是：这是一个测试视频"
                };
            }
        }
        
        // 处理视频创建上下文
        if (this.conversationContext.intent === 'createVideo') {
            if (!this.conversationContext.username) {
                this.conversationContext.username = userInput;
                return {
                    type: 'ask',
                    message: "请提供您的密码"
                };
            } else {
                const username = this.conversationContext.username;
                const password = userInput;
                const title = this.conversationContext.title;
                const script = this.conversationContext.script;
                this.conversationContext = {};
                return {
                    type: 'loginAndCreateVideo',
                    username: username,
                    password: password,
                    title: title,
                    script: script
                };
            }
        }
        
        // 处理询问视频信息上下文
        if (this.conversationContext.intent === 'askVideoInfo') {
            // 提取标题和文案
            const titleMatch = userInput.match(/标题是：([^，。]+)/);
            const scriptMatch = userInput.match(/文案是：([^，。]+)/);
            
            if (titleMatch && scriptMatch) {
                const title = titleMatch[1];
                const script = scriptMatch[1];
                
                // 检查是否已登录
                if (!this.isLoggedIn) {
                    this.conversationContext.intent = 'createVideo';
                    this.conversationContext.title = title;
                    this.conversationContext.script = script;
                    return {
                        type: 'ask',
                        message: "请提供您的账号（手机号）"
                    };
                } else {
                    return {
                        type: 'createVideo',
                        title: title,
                        script: script
                    };
                }
            } else {
                return {
                    type: 'ask',
                    message: "请正确提供视频标题和文案，例如：标题是：测试视频，文案是：这是一个测试视频"
                };
            }
        }
        
        // 处理其他指令
        if (userInput.includes('最近视频')) {
            if (this.memory.recentVideos && this.memory.recentVideos.length > 0) {
                let response = "您最近创建的视频：\n";
                this.memory.recentVideos.slice(-5).forEach((video, index) => {
                    const date = new Date(video.createdAt).toLocaleDateString();
                    response += `${index + 1}. ${video.title} (创建时间：${date})\n`;
                });
                return {
                    type: 'response',
                    message: response
                };
            } else {
                return {
                    type: 'response',
                    message: "您还没有创建过视频"
                };
            }
        }
        
        if (userInput.includes('帮助') || userInput.includes('使用方法')) {
            return {
                type: 'response',
                message: "您可以使用以下指令：\n" +
                       "1. 登录系统，账号是18098901246，密码是123456\n" +
                       "2. 创建视频，标题是：测试视频，文案是：这是一个测试视频\n" +
                       "3. 查看最近视频"
            };
        }
        
        // 默认响应
        return {
            type: 'response',
            message: "您好！我是RRBD智能助手，可以帮您创建视频。请告诉我视频的标题和文案，例如：创建视频，标题是：测试视频，文案是：这是一个测试视频"
        };
    }
}

async function main() {
    const agent = new RRBDAgent();
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    console.log("RRBD智能助手已启动，输入'退出'结束对话");
    console.log("您可以输入：创建视频，标题是：测试视频，文案是：这是一个测试视频");
    
    function askQuestion() {
        rl.question("用户：", async (userInput) => {
            if (userInput === '退出') {
                rl.close();
                return;
            }
            
            const result = agent.handleUserInput(userInput);
            
            if (result.type === 'ask') {
                console.log(`助手：${result.message}`);
                askQuestion();
            } else if (result.type === 'response') {
                console.log(`助手：${result.message}`);
                askQuestion();
            } else if (result.type === 'login') {
                const success = await agent.login(result.username, result.password);
                if (success) {
                    console.log('助手：登录成功！');
                } else {
                    console.log('助手：登录失败，请检查账号密码');
                }
                askQuestion();
            } else if (result.type === 'createVideo') {
                const videoResult = await agent.createVideo(result.title, result.script);
                if (videoResult.success) {
                    console.log(`助手：视频创建成功！视频URL：${videoResult.videoUrl}`);
                } else {
                    console.log(`助手：视频创建失败：${videoResult.message}`);
                }
                askQuestion();
            } else if (result.type === 'loginAndCreateVideo') {
                const loginSuccess = await agent.login(result.username, result.password);
                if (loginSuccess) {
                    console.log('助手：登录成功！');
                    const videoResult = await agent.createVideo(result.title, result.script);
                    if (videoResult.success) {
                        console.log(`助手：视频创建成功！视频URL：${videoResult.videoUrl}`);
                    } else {
                        console.log(`助手：视频创建失败：${videoResult.message}`);
                    }
                } else {
                    console.log('助手：登录失败，请检查账号密码');
                }
                askQuestion();
            }
        });
    }
    
    askQuestion();
}

if (require.main === module) {
    main();
}

module.exports = RRBDAgent;
