#!/usr/bin/env node
/**
 * 影刀RPA技能核心逻辑
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

class YingdaoRPA {
    constructor() {
        // 数据文件路径
        this.dataDir = path.join(__dirname, '../data');
        if (!fs.existsSync(this.dataDir)) {
            fs.mkdirSync(this.dataDir, { recursive: true });
        }
        this.userBindingsFile = path.join(this.dataDir, 'user.json');
        
        // 加载用户绑定信息
        this.userBindings = this.loadUserBindings();
    }
    
    loadUserBindings() {
        try {
            if (fs.existsSync(this.userBindingsFile)) {
                const data = fs.readFileSync(this.userBindingsFile, 'utf-8');
                return JSON.parse(data);
            }
        } catch (e) {
            console.error('加载用户绑定信息失败:', e);
        }
        return {};
    }
    
    saveUserBindings() {
        try {
            fs.writeFileSync(this.userBindingsFile, JSON.stringify(this.userBindings, null, 2), 'utf-8');
        } catch (e) {
            console.error('保存用户绑定信息失败:', e);
        }
    }
    
    extractUuidFromLink(link) {
        const match = link.match(/userUuid=([^&]+)/);
        return match ? match[1] : null;
    }
    
    async validateUuid(uuid) {
        try {
            const apiUrl = `https://api.yingdao.com/api/noauth/v1/sns/forum/user/query?userUuid=${uuid}`;
            
            const result = await this.httpGet(apiUrl, {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            });
            
            if (result.success === true && result.code === 200) {
                const userName = result.data?.userName || '未知用户';
                console.log(`UUID ${uuid} 验证成功，用户名: ${userName}`);
                return { valid: true, userName };
            }
            return { valid: false, userName: '' };
        } catch (e) {
            console.error('验证UUID异常:', e);
            return { valid: false, userName: '' };
        }
    }
    
    bindUser(userId, uuid) {
        if (this.userBindings[userId] && typeof this.userBindings[userId] === 'object') {
            this.userBindings[userId].uuid = uuid;
            // 重置personalId，确保下次查询时重新获取
            delete this.userBindings[userId].personalId;
        } else {
            this.userBindings[userId] = { uuid };
        }
        this.saveUserBindings();
    }
    
    getUserUuid(userId) {
        const binding = this.userBindings[userId];
        if (binding && typeof binding === 'object') {
            return binding.uuid || '';
        }
        return binding || '';
    }
    
    async queryUserInfo(uuid) {
        const apiUrl = `https://api.yingdao.com/api/noauth/v1/sns/forum/user/query?userUuid=${uuid}`;
        
        try {
            const result = await this.httpGet(apiUrl, {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            });
            
            return result;
        } catch (e) {
            console.error('查询用户信息失败:', e);
            return null;
        }
    }
    
    async queryAppSnsData(personalId) {
        const url = `https://api.yingdao.com/api/eco/noauth/v1/achieve/info/query/appSnsData?personalId=${personalId}`;
        
        try {
            const result = await this.httpGet(url, {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            });
            
            return result;
        } catch (e) {
            console.error('查询应用和社区统计数据失败:', e);
            return null;
        }
    }
    
    formatUserInfo(userData, uuid, userId = null) {
        const data = userData.data || {};
        
        // 获取基本信息
        const userName = data.userName || '未知';
        const joinTime = data.joinTime || '未知';
        
        // 获取统计数据
        const questionCount = data.publishQuestionCount || 0;
        const articleCount = data.publishArticleCount || 0;
        const answerCount = data.answerCount || 0;
        const acceptCount = data.acceptCount || 0;
        const likeCount = data.likeCount || 0;
        const collectedCount = data.beCollectedCount || 0;
        
        // 获取货币信息
        const pointBalance = data.pointBalance || 0;
        const knifeCoinBalance = data.knifeCoinBalance;
        
        // 获取成就信息
        const achieveLevel = data.achieveLevel;
        let achieveLevelName, personalId;
        
        if (achieveLevel) {
            achieveLevelName = achieveLevel.achieveLevelName || '未知';
            // 从personalHomePageLink中提取personalId
            const personalHomePageLink = achieveLevel.personalHomePageLink || '';
            if (personalHomePageLink) {
                // 从链接中提取personalId
                personalId = personalHomePageLink.split('/').pop();
                // 存储personalId
                if (personalId && userId) {
                    if (this.userBindings[userId] && typeof this.userBindings[userId] === 'object') {
                        this.userBindings[userId].personalId = personalId;
                        this.saveUserBindings();
                    }
                }
            } else {
                personalId = '';
            }
        } else {
            achieveLevelName = '暂无成就';
            personalId = '';
        }
        
        // 检查是否为认证工程师
        const engineerBadge = data.isFreelanceSolvers ? '🏆 影刀认证工程师' : '';
        
        // 格式化货币信息
        const currencyInfo = knifeCoinBalance !== undefined 
            ? `🥜 刀豆：${pointBalance}   💰 刀币：${knifeCoinBalance}`
            : `🥜 刀豆：${pointBalance}`;
        
        // 格式化消息
        const messageParts = [
            `👤 用户名：${userName}`,
            `🔢 UUID:${uuid}`,
            `⏰ 注册时间：${joinTime}`,
            `❓ 提问：${questionCount} 📄 文章：${articleCount} 💬 回复：${answerCount}`,
            `✅ 被采纳：${acceptCount} 👍 获赞：${likeCount} ⭐ 被收藏：${collectedCount}`,
            currencyInfo,
            `🏅 成就：🔵 ${achieveLevelName}   ${engineerBadge}`
        ];
        
        // 添加开发统计数据
        if (personalId) {
            // 由于JavaScript是异步的，这里需要特殊处理
            // 在实际使用时，应该在processRequest中处理
            messageParts.push('\n📊 开发统计：\n正在获取开发统计数据...');
        } else {
            messageParts.push('\n📊 开发统计：\n❌ 账号未绑定成就，无法获取开发统计数据');
        }
        
        return messageParts.join('\n');
    }
    
    async formatUserInfoWithStats(userData, uuid, userId = null) {
        const data = userData.data || {};
        
        // 获取基本信息
        const userName = data.userName || '未知';
        const joinTime = data.joinTime || '未知';
        
        // 获取统计数据
        const questionCount = data.publishQuestionCount || 0;
        const articleCount = data.publishArticleCount || 0;
        const answerCount = data.answerCount || 0;
        const acceptCount = data.acceptCount || 0;
        const likeCount = data.likeCount || 0;
        const collectedCount = data.beCollectedCount || 0;
        
        // 获取货币信息
        const pointBalance = data.pointBalance || 0;
        const knifeCoinBalance = data.knifeCoinBalance;
        
        // 获取成就信息
        const achieveLevel = data.achieveLevel;
        let achieveLevelName, personalId;
        
        if (achieveLevel) {
            achieveLevelName = achieveLevel.achieveLevelName || '未知';
            // 从personalHomePageLink中提取personalId
            const personalHomePageLink = achieveLevel.personalHomePageLink || '';
            if (personalHomePageLink) {
                // 从链接中提取personalId
                personalId = personalHomePageLink.split('/').pop();
                // 存储personalId
                if (personalId && userId) {
                    if (this.userBindings[userId] && typeof this.userBindings[userId] === 'object') {
                        this.userBindings[userId].personalId = personalId;
                        this.saveUserBindings();
                    }
                }
            } else {
                personalId = '';
            }
        } else {
            achieveLevelName = '暂无成就';
            personalId = '';
        }
        
        // 检查是否为认证工程师
        const engineerBadge = data.isFreelanceSolvers ? '🏆 影刀认证工程师' : '';
        
        // 格式化货币信息
        const currencyInfo = knifeCoinBalance !== undefined 
            ? `🥜 刀豆：${pointBalance}   💰 刀币：${knifeCoinBalance}`
            : `🥜 刀豆：${pointBalance}`;
        
        // 格式化消息
        const messageParts = [
            `👤 用户名：${userName}`,
            `🔢 UUID:${uuid}`,
            `⏰ 注册时间：${joinTime}`,
            `❓ 提问：${questionCount} 📄 文章：${articleCount} 💬 回复：${answerCount}`,
            `✅ 被采纳：${acceptCount} 👍 获赞：${likeCount} ⭐ 被收藏：${collectedCount}`,
            currencyInfo,
            `🏅 成就：🔵 ${achieveLevelName}   ${engineerBadge}`
        ];
        
        // 添加开发统计数据
        if (personalId) {
            const appSnsData = await this.queryAppSnsData(personalId);
            if (appSnsData && appSnsData.code === 200) {
                const appSnsInfo = appSnsData.data || {};
                
                // 开发统计
                const appDevelopStat = appSnsInfo.appDevelopStat || {};
                const snsStat = appSnsInfo.snsStat || {};
                
                // 开发指令行数统计
                const developBlockStat = appDevelopStat.developBlockStat || {};
                const monthDevelopBlocks = developBlockStat.monthStatList || [];
                const totalDevelopBlocks = developBlockStat.totalStatVal || 0;
                const currentMonthDevelopBlocks = monthDevelopBlocks[0]?.statVal || 0;
                
                // 开发应用数统计
                const developAppStat = appDevelopStat.developAppStat || {};
                const monthApps = developAppStat.monthStatList || [];
                const totalApps = developAppStat.totalStatVal || 0;
                const currentMonthApps = monthApps[0]?.statVal || 0;
                
                // 运行时长统计
                const runTimeStat = appDevelopStat.ownerAppRunTimeStat || {};
                const monthRunTimes = runTimeStat.monthStatList || [];
                const totalRunTime = runTimeStat.totalStatVal || 0;
                const currentMonthRunTimeHours = monthRunTimes[0]?.statVal 
                    ? Math.round(monthRunTimes[0].statVal / 3600 * 10) / 10 
                    : 0;
                const totalRunTimeHours = Math.round(totalRunTime / 3600 * 10) / 10;
                
                // 社区采纳
                const acceptedStat = snsStat.acceptedStat || {};
                const monthAccepted = acceptedStat.monthStatList || [];
                const totalAccepted = acceptedStat.totalStatVal || 0;
                const currentMonthAccepted = monthAccepted[0]?.statVal || 0;
                
                const appStatsMsg = [
                    '\n📊 开发统计：',
                    `💻 本月开发指令行数：${currentMonthDevelopBlocks}  总计：${totalDevelopBlocks}`,
                    `📱 本月开发应用数：${currentMonthApps}  总计：${totalApps}`,
                    `⏱️ 本月运行时长：${currentMonthRunTimeHours}小时  总计：${totalRunTimeHours}小时`,
                    `✅ 本月社区采纳数量：${currentMonthAccepted}  总计：${totalAccepted}`
                ].join('\n');
                
                messageParts.push(appStatsMsg);
            }
        } else {
            messageParts.push('\n📊 开发统计：\n❌ 账号未绑定成就，无法获取开发统计数据');
        }
        
        return messageParts.join('\n');
    }
    
    async processRequest(userId, requestType, data = null) {
        if (requestType === 'bind') {
            // 绑定用户
            const link = data;
            const uuid = this.extractUuidFromLink(link);
            if (!uuid) {
                return '❌ 无法从链接中提取UUID，请检查链接格式是否正确。';
            }
            
            const { valid, userName } = await this.validateUuid(uuid);
            if (!valid) {
                return '❌ UUID验证失败，请检查链接是否正确。';
            }
            
            this.bindUser(userId, uuid);
            return `✅ 绑定成功！用户名：${userName}`;
        }
        
        else if (requestType === 'query') {
            // 查询信息
            const uuid = this.getUserUuid(userId);
            if (!uuid) {
                return '❌ 您还未绑定UUID，请先发送影刀社区个人主页链接进行绑定。';
            }
            
            const userData = await this.queryUserInfo(uuid);
            if (!userData || userData.code !== 200) {
                return '❌ 查询失败，请稍后重试。';
            }
            
            return await this.formatUserInfoWithStats(userData, uuid, userId);
        }
        
        else if (requestType === 'tutorial') {
            // 获取教程
            return '📚 获取个人主页链接教程：\n1. 打开 https://www.yingdao.com/community/homePage\n2. 登录你的影刀账号\n3. 点击页面右上角的头像\n4. 复制跳转后的页面链接';
        }
        
        else {
            return '❌ 未知请求类型。';
        }
    }
    
    httpGet(url, headers) {
        return new Promise((resolve, reject) => {
            const options = {
                method: 'GET',
                headers: headers
            };
            
            const req = https.get(url, options, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    try {
                        const jsonData = JSON.parse(data);
                        resolve(jsonData);
                    } catch (e) {
                        reject(e);
                    }
                });
            });
            
            req.on('error', (e) => {
                reject(e);
            });
            
            req.setTimeout(10000, () => {
                req.destroy();
                reject(new Error('请求超时'));
            });
        });
    }
}

// 导出模块
module.exports = YingdaoRPA;