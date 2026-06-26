/**
 * ValueScan API 签名 + 请求工具 (Node.js)
 * 依赖: Node.js 16+（内置crypto/fetch/url/fs，无需额外安装依赖）
 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { URL } = require('url');

const BASE_URL = 'https://api.valuescan.io';

/**
 * 从配置文件读取 API Key 和 Secret Key
 * @returns {object} 包含 valuescanApiKey 和 valuescanSecretKey 的对象
 */
function loadCredentials() {
    const credPath = path.join(os.homedir(), '.openclaw', 'credentials', 'valuescan.json');
    
    if (!fs.existsSync(credPath)) {
        throw new Error(`配置文件不存在: ${credPath}，请先创建该文件并配置 valuescanApiKey 和 valuescanSecretKey`);
    }
    
    try {
        const content = fs.readFileSync(credPath, 'utf8');
        const creds = JSON.parse(content);
        
        if (!creds.valuescanApiKey || !creds.valuescanSecretKey) {
            throw new Error('配置文件中缺少 valuescanApiKey 或 valuescanSecretKey 字段');
        }
        
        return creds;
    } catch (error) {
        if (error instanceof SyntaxError) {
            throw new Error(`配置文件 JSON 格式错误: ${credPath}`);
        }
        throw error;
    }
}

/**
 * 生成符合规范的签名请求头
 * @param {string} rawBody POST原始请求体字符串（保持原始格式）
 * @returns {object} 包含X-API-KEY、X-TIMESTAMP、X-SIGN的请求头字典
 */
function buildSignHeader(rawBody) {
    const creds = loadCredentials();
    const apiKey = creds.valuescanApiKey;
    const secretKey = creds.valuescanSecretKey;

    const timestamp = Date.now().toString();
    const signContent = timestamp + rawBody;

    const hmac = crypto.createHmac('sha256', secretKey);
    hmac.update(signContent, 'utf8');
    const sign = hmac.digest('hex');

    return {
        'X-API-KEY': apiKey,
        'X-TIMESTAMP': timestamp,
        'X-SIGN': sign,
        'Content-Type': 'application/json; charset=utf-8'
    };
}

/**
 * 发送带签名的POST请求
 * @param {string} path API接口相对路径（如/api/open/v1/vs-token/list）
 * @param {object|string} data 请求数据（JSON对象/原始字符串）
 * @param {number} timeout 超时时间（毫秒），默认10000毫秒
 * @returns {Promise<object>} API响应结果（JSON对象）
 */
async function vsPost(path, data, timeout = 10000) {
    const rawBody = typeof data === 'object' ? JSON.stringify(data) : data;
    const fullUrl = new URL(path, BASE_URL).href;
    const headers = buildSignHeader(rawBody);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(fullUrl, {
            method: 'POST',
            headers: headers,
            body: rawBody,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP请求失败，状态码：${response.status}`);
        }

        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error(`请求超时（${timeout}ms）：${fullUrl}`);
        }
        throw new Error(`请求失败：${error.message}`);
    }
}

module.exports = { buildSignHeader, vsPost };

// 调用示例
if (require.main === module) {
    const apiPath = '/api/open/v1/vs-token/list';
    const requestData = { search: 'BTC' };

    vsPost(apiPath, requestData)
        .then(result => {
            console.log('请求成功:', JSON.stringify(result, null, 2));
        })
        .catch(error => {
            console.error('请求失败:', error.message);
        });
}
