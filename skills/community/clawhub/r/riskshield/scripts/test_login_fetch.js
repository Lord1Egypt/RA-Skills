/**
 * 调试脚本 - 直接发送登录请求测试
 */

const fetch = require('node:http');

// 手动发送登录请求测试
const loginData = JSON.stringify({
    username: 'taskAccount',
    password: 'ZIdongshenpi1.'
});

const url = new URL('https://riskshield.dcsuat.com/auth/login');

// 使用 node-fetch 或原生 https
const https = require('https');

const data = JSON.stringify({
    username: 'taskAccount',
    password: 'ZIdongshenpi1.'
});

const options = {
    hostname: 'riskshield.dcsuat.com',
    port: 443,
    path: '/auth/login',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
};

const req = https.request(options, (res) => {
    console.log('状态码:', res.statusCode);
    console.log('响应头:', JSON.stringify(res.headers));

    let body = '';
    res.on('data', (chunk) => body += chunk);
    res.on('end', () => {
        console.log('响应体:', body.substring(0, 500));
    });
});

req.on('error', (e) => console.error('请求错误:', e.message));
req.write(data);
req.end();

console.log('请求已发送');