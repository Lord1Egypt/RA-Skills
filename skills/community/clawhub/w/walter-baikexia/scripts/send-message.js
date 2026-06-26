/**
 * 百科虾消息发送脚本
 * 功能：
 * 1. 检测回复中的 mention 标签（『AT:...』 或 <at>）
 * 2. 通过飞书 IM API 发送消息，将 mention 信息正确传递
 * 3. 支持发送图片（使用 curl 上传）
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const { URL } = require('url');

// 检测文本是否为乱码（包含大量替换字符或无效 Unicode）
function isMojibake(text) {
    // 检查是否有大量 � (U+FFFD) 替换字符
    const replacementCount = (text.match(/\uFFFD/g) || []).length;
    if (replacementCount > 5) return true;
    
    // 检查是否包含常见的乱码特征（方框+问号组合）
    if (/\ufffd|\u25a1|\u2753/.test(text)) return true;
    
    return false;
}

// 验证文本是否包含有效的中文（排除乱码）
function hasValidChinese(text) {
    // 中文字符范围
    const chineseRegex = /[\u4e00-\u9fff]/;
    return chineseRegex.test(text);
}

const SKILL_DIR = path.join(__dirname, '..');
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 解析 MEDIA 路径为完整路径
function resolveMediaPath(mediaPath) {
    // 如果是绝对路径，直接返回
    if (path.isAbsolute(mediaPath)) {
        return mediaPath;
    }
    // 相对于当前工作目录
    return path.resolve(mediaPath);
}

// 从 openclaw.json 读取飞书凭证
function loadFeishuConfig() {
    const homeDir = os.homedir();
    const possiblePaths = [
        path.join(homeDir, '.openclaw', 'openclaw.json'),
        path.join(homeDir, '.openclaw', 'openclaw.local.json'),
    ];
    
    for (const configPath of possiblePaths) {
        if (fs.existsSync(configPath)) {
            const openclawConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
            const feishuAccounts = openclawConfig?.channels?.feishu?.accounts;
            // 尝试找到 baikexia 或默认的飞书账号
            const agentName = process.env.OPENCLAW_AGENT_NAME || 'baikexia';
            if (feishuAccounts?.[agentName]) {
                return feishuAccounts[agentName];
            }
            // 尝试第一个可用的账号
            const firstAccount = Object.values(feishuAccounts || {})[0];
            if (firstAccount) return firstAccount;
        }
    }
    throw new Error('找不到飞书凭证，请检查 openclaw.json 配置');
}

const feishuConfig = loadFeishuConfig();
const APP_ID = feishuConfig.appId;
const APP_SECRET = feishuConfig.appSecret;

// 使用 Node.js https 模块发送请求
function fetchJson(url, options = {}) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const opts = {
            hostname: urlObj.hostname,
            path: urlObj.pathname + urlObj.search,
            method: options.method || 'GET',
            headers: options.headers || {}
        };

        const req = https.request(opts, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); }
                catch(e) { resolve(data); }
            });
        });

        req.on('error', reject);
        if (options.body) {
            req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
        }
        req.end();
    });
}

// Token 缓存（飞书 token 有效期约 2 小时）
let tokenCache = {
    token: null,
    expiresAt: 0
};

// 获取 token（带缓存）
async function getToken() {
    const now = Date.now();
    // 缓存 1.5 小时，避免接近过期时失效
    if (tokenCache.token && now < tokenCache.expiresAt) {
        return tokenCache.token;
    }
    
    const resp = await fetchJson(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { app_id: APP_ID, app_secret: APP_SECRET }
    });
    if (!resp.tenant_access_token) throw new Error(`获取token失败: ${resp.msg}`);
    
    tokenCache = {
        token: resp.tenant_access_token,
        expiresAt: now + 90 * 60 * 1000  // 90 分钟
    };
    return tokenCache.token;
}

// 发送 HTTP 请求
function sendRequest(url, method, headers, body) {
    // body 可能是字符串（已序列化）或对象，自动处理
    return fetchJson(url, { method, headers, body });
}

// 从文本中提取所有 mention 信息
function extractMentions(text) {
    const mentions = [];
    const patterns = [
        /『AT:([^:]+)』/g,                     // 『AT:user_id』简化格式
        /<at user_id="([^"]+)">([^<]+)<\/at>/g  // <at user_id="...">name</at>
    ];
    
    for (const regex of patterns) {
        let match;
        while ((match = regex.exec(text)) !== null) {
            // 如果是简化格式『AT:user_id』，name 为空
            const name = match[2] || match[1];
            mentions.push({ userId: match[1], name: name });
        }
    }
    return mentions;
}

// 将 mention 格式替换为纯名字
function stripAtTags(text) {
    // 移除『AT:user_id』或『AT:user_id:name』格式，保留 name 部分（如果有）
    text = text.replace(/『AT:([^:]+):([^』]+)』/g, '$2');
    text = text.replace(/『AT:([^』]+)』/g, '');
    text = text.replace(/<at user_id="[^"]+">([^<]+)<\/at>/g, '$1');
    return text;
}

// 上传图片获取 image_key（使用 Node.js https）
async function uploadImage(token, imagePath) {
    const url = `${FEISHU_BASE}/im/v1/images`;
    const urlObj = new URL(url);
    
    const boundary = '----FormBoundary' + Math.random().toString(36).substring(2);
    const fileContent = fs.readFileSync(imagePath);
    const fileName = path.basename(imagePath);
    
    // 构建 multipart body
    const headerPart = Buffer.from(
        `--${boundary}\r
Content-Disposition: form-data; name="image"; filename="${fileName}"\r
Content-Type: image/jpeg\r
\r
`,
        'utf8'
    );
    const footerPart = Buffer.from(
        `\r
--${boundary}\r
Content-Disposition: form-data; name="image_type"\r
\r
message\r
--${boundary}--\r
`,
        'utf8'
    );
    
    const postData = Buffer.concat([headerPart, fileContent, footerPart]);
    
    return new Promise((resolve, reject) => {
        const opts = {
            hostname: urlObj.hostname,
            path: urlObj.pathname,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
                'Content-Length': postData.length
            }
        };
        
        const req = https.request(opts, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.code !== 0) throw new Error(json.msg || '图片上传失败');
                    resolve(json.data.image_key);
                } catch (e) {
                    reject(e);
                }
            });
        });
        
        req.on('error', reject);
        req.write(postData);
        req.end();
    });
}

// 发送文本消息
async function sendTextMessage(token, receiveId, receiveIdType, text, mentions) {
    let processedText = text;
    
    // 如果有 mentions（从占位符『AT:...』提取），替换为飞书原生 at 标签
    if (mentions && mentions.length > 0) {
        for (const m of mentions) {
            processedText = processedText.replace(
                `『AT:${m.userId}』`,
                `<at user_id="${m.userId}">${m.name}</at>`
            );
        }
    } else {
        // 没有 mentions 时，清理残留的『AT:...』格式（可能来自 stripAtTags 遗漏）
        // 保留 <at> 标签因为飞书 API 原生支持
        processedText = processedText.replace(/『AT:[^』]+』/g, '');
    }
    
    const payload = {
        receive_id: receiveId,
        msg_type: 'text',
        content: JSON.stringify({ text: processedText })
    };
    
    const result = await sendRequest(
        `${FEISHU_BASE}/im/v1/messages?receive_id_type=${receiveIdType}`,
        'POST',
        {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        JSON.stringify(payload)
    );
    return result;
}

// 发送图片消息
async function sendImageMessage(token, receiveId, receiveIdType, imageKey) {
    const payload = {
        receive_id: receiveId,
        msg_type: 'image',
        content: JSON.stringify({ image_key: imageKey })
    };
    
    const result = await sendRequest(
        `${FEISHU_BASE}/im/v1/messages?receive_id_type=${receiveIdType}`,
        'POST',
        {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        JSON.stringify(payload)
    );
    return result;
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.error('用法: node send-message.js <receive_id> <receive_id_type> [content_file]');
        process.exit(1);
    }
    
    const receiveId = args[0];
    const receiveIdType = args[1];
    let text;
    
    if (args[2]) {
        text = fs.readFileSync(args[2], 'utf8');
    } else {
        text = fs.readFileSync('/dev/stdin', 'utf8');
    }
    
    text = text.trim();
    if (!text) {
        console.log('消息内容为空，无需发送');
        process.exit(0);
    }
    
    // 检测乱码
    if (isMojibake(text)) {
        console.error('⚠️ 检测到文本可能存在乱码！请勿使用 echo 或 CMD 写入含中文的文本文件。');
        console.error('推荐使用 write 工具或 PowerShell 的 Out-File -Encoding utf8 写入文件。');
        console.error('乱码内容预览:', text.substring(0, 100));
        process.exit(1);
    }
    
    // 检查是否包含图片路径标记
    const imageMatch = text.match(/『IMG:([^』]+)』/);
    const mediaMatch = text.match(/MEDIA:([^\n]+)/);
    const mentions = extractMentions(text);
    const cleanText = stripAtTags(text);
    
    console.log('发送消息...');
    console.log('原始文本:', text);
    console.log('清理后文本:', cleanText);
    console.log('Mentions:', JSON.stringify(mentions));
    console.log('Image match:', imageMatch);
    console.log('Media match:', mediaMatch);
    
    const token = await getToken();
    let result;
    
    if (imageMatch) {
        // 发送图片消息
        const imagePath = imageMatch[1];
        console.log('检测到图片:', imagePath);
        const imageKey = await uploadImage(token, imagePath);
        console.log('image_key:', imageKey);
        result = await sendImageMessage(token, receiveId, receiveIdType, imageKey);
    } else if (mediaMatch) {
        // 有图片也有文字：先发送文字，再发送图片
        // 注意：必须用原始 text，不能用 cleanText，否则『AT:...』会被 stripAtTags 清除
        const textWithoutMedia = text.replace(/MEDIA:[^\n]*/g, '').trim();
        
        // 先发送文字
        if (textWithoutMedia) {
            console.log('检测到文字内容，先发送文字');
            result = await sendTextMessage(token, receiveId, receiveIdType, textWithoutMedia, mentions);
        }
        
        // 提取所有 MEDIA 路径并发送图片
        const mediaMatches = [...text.matchAll(/MEDIA:([^\n]+)/g)];
        for (const match of mediaMatches) {
            const imagePath = resolveMediaPath(match[1].trim());
            console.log('检测到 MEDIA 图片:', imagePath);
            try {
                const imageKey = await uploadImage(token, imagePath);
                console.log('image_key:', imageKey);
                result = await sendImageMessage(token, receiveId, receiveIdType, imageKey);
            } catch (err) {
                console.log('发送图片失败:', err.message);
            }
        }
    } else {
        // 发送文本消息
        result = await sendTextMessage(token, receiveId, receiveIdType, text, mentions);
    }
    
    if (result.code === 0) {
        console.log('消息发送成功');
    } else {
        console.error('消息发送失败:', result.msg);
        process.exit(1);
    }
}

main().catch(err => {
    console.error('错误:', err.message);
    process.exit(1);
});
