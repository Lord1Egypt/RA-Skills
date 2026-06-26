#!/usr/bin/env node

/**
 * 知识星球自动化发布文章脚本
 * 使用 Node.js 内置模块，无需额外依赖
 * 
 * 原理：
 * 知识星球的签名算法通过分析前端 JS 得出：
 * x-timestamp = 当前 Unix 时间戳（秒）
 * x-signature = SHA1(x-timestamp + request_body_md5)
 * 
 * 使用方法:
 *   node zsxq-auto-post-article.js --cookie "YOUR_COOKIE" --title "文章标题" --content "文章内容"
 * 
 *   # 发布到草稿箱（默认）
 *   node zsxq-auto-post-article.js --cookie "xxx" --title "标题" --content "<p>内容</p>" --publish false
 * 
 *   # 直接发布文章
 *   node zsxq-auto-post-article.js --cookie "xxx" --title "标题" --content "<p>内容</p>" --publish true
 */

const https = require('https');
const crypto = require('crypto');

// 解析命令行参数
function parseArgs() {
    const args = process.argv.slice(2);
    const params = {};
    for (let i = 0; i < args.length; i += 2) {
        const key = args[i].replace('--', '');
        params[key] = args[i + 1];
    }
    return params;
}

// 从 cookie 中提取 token
function extractToken(cookie) {
    const match = cookie.match(/zsxq_access_token=([^;]+)/);
    return match ? match[1].trim() : null;
}

// 生成签名
// 知识星球签名算法：SHA1(timestamp + MD5(body))
function generateSignature(timestamp, body) {
    const bodyMd5 = crypto.createHash('md5').update(body).digest('hex');
    const signStr = timestamp + bodyMd5;
    const signature = crypto.createHash('sha1').update(signStr).digest('hex');
    return signature;
}

// 生成 UUID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// 发送 HTTP 请求
function sendRequest(options, body) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    resolve({ raw: data });
                }
            });
        });
        req.on('error', reject);
        req.write(body);
        req.end();
    });
}

// 确认发布文章（调用 topics 接口）
async function confirmPublish(cookie, groupId, articleId, title, content) {
    const apiPath = `/v2/groups/${groupId}/topics`;
    
    // 提取纯文本内容（去掉HTML标签）
    const plainContent = content.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim();
    const summary = plainContent.length > 80 ? plainContent.substring(0, 80) + '...' : plainContent;
    
    // URL编码title
    const encodedTitle = encodeURIComponent(title);
    const text = `<e type="text_bold" title="${encodedTitle}" />\n\n${summary}`;
    
    const body = JSON.stringify({
        req_data: {
            type: "talk",
            text: text,
            article_id: articleId
        }
    });

    const timestamp = Math.floor(Date.now() / 1000).toString();
    const signature = generateSignature(timestamp, body);
    const requestId = generateUUID();

    const options = {
        hostname: 'api.zsxq.com',
        path: apiPath,
        method: 'POST',
        headers: {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'content-length': Buffer.byteLength(body),
            'dnt': '1',
            'origin': 'https://wx.zsxq.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://wx.zsxq.com/',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'x-request-id': requestId,
            'x-signature': signature,
            'x-timestamp': timestamp,
            'x-version': '2.89.0',
            'cookie': cookie
        }
    };

    const result = await sendRequest(options, body);

    if (result.succeeded) {
        console.log('✅ 文章确认发布成功！');
        console.error('响应:', JSON.stringify(result, null, 2));
    } else {
        console.error('❌ 文章确认发布失败');
        console.error('响应:', JSON.stringify(result, null, 2));
    }
}

// 主函数
async function main() {
    const { cookie, title, content, group = '48885154455258', article = '', publish = 'false' } = parseArgs();

    if (!cookie) {
        console.error('❌ 错误: 缺少 --cookie 参数');
        process.exit(1);
    }
    if (!title) {
        console.error('❌ 错误: 缺少 --title 参数');
        process.exit(1);
    }
    if (!content) {
        console.error('❌ 错误: 缺少 --content 参数');
        process.exit(1);
    }

    const isPublish = publish === 'true';
    const apiPath = isPublish ? '/v2/articles' : '/v2/articles/drafts';
    const actionName = isPublish ? '发布' : '发布到草稿箱';

    // 提取 token
    const token = extractToken(cookie);
    if (!token) {
        console.error('❌ 无法从 cookie 中提取 zsxq_access_token');
        process.exit(1);
    }
    console.log('✓ 已提取 access_token');

    // 构建请求体
    const body = JSON.stringify({
        req_data: {
            group_id: group,
            article_id: article,
            title: title,
            content: content,
            image_ids: []
        }
    });

    // 生成签名
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const signature = generateSignature(timestamp, body);
    const requestId = generateUUID();

    console.log('✓ 已生成签名');
    console.log(`🚀 正在${actionName}文章...`);

    // 发送请求
    const options = {
        hostname: 'api.zsxq.com',
        path: apiPath,
        method: 'POST',
        headers: {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'content-length': Buffer.byteLength(body),
            'dnt': '1',
            'origin': 'https://wx.zsxq.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://wx.zsxq.com/',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'x-request-id': requestId,
            'x-signature': signature,
            'x-timestamp': timestamp,
            'x-version': '2.89.0',
            'cookie': cookie
        }
    };

    const result = await sendRequest(options, body);

    if (result.succeeded) {
        const articleId = result.resp_data?.article_id || article;
        console.log(`✅ 文章${actionName}成功！`);
        console.log(`📌 文章ID: ${articleId}`);
        console.log(`🔗 文章链接: ${result.resp_data?.article_url || '未知'}`);

        if (isPublish) {
            console.log('🚀 正在确认发布文章...');
            await confirmPublish(cookie, group, articleId, title, content);
        }
    } else {
        console.error(`❌ 文章${actionName}失败`);
        console.error('响应:', JSON.stringify(result, null, 2));

        if (result.code === 401) {
            console.error('\n⚠️  Cookie 已过期，请重新获取：');
            console.error('  1. 访问 https://wx.zsxq.com');
            console.error('  2. 按 F12 → Network → 复制 Cookie');
        }
    }
}

main().catch(console.error);
