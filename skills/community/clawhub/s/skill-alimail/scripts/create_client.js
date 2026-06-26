#!/usr/bin/env node

const { AliMailClient } = require('alimail-node-sdk');
const fs = require('fs');
const path = require('path');

/**
 * 创建阿里邮箱客户端
 * 
 * 授权方式: OAuth2 client_credentials（由 SDK 内部处理令牌申请）
 * 凭证环境变量: ALMAIL_APP_ID, ALMAIL_SECRET
 */
function createClient() {
    // 1. 获取凭证
    const appId = process.env.ALMAIL_APP_ID;
    const appSecret = process.env.ALMAIL_SECRET;

    if (!appId || !appSecret) {
        throw new Error('缺少阿里邮箱凭证配置，请检查环境变量 ALMAIL_APP_ID 和 ALMAIL_SECRET');
    }

    // 2. 创建客户端
    const client = new AliMailClient({
        appId,
        appSecret,
        baseUrl: 'https://alimail-cn.aliyuncs.com',
        timeoutMs: 30000,
        maxRetries: 3,
    });

    return client;
}

module.exports = { createClient };

// 如果直接运行此脚本，输出客户端信息
if (require.main === module) {
    try {
        const client = createClient();
        console.log('阿里邮箱客户端创建成功');
    } catch (error) {
        console.error('创建客户端失败:', error.message);
        process.exit(1);
    }
}
