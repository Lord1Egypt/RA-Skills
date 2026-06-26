const fs = require('fs');
const path = require('path');
const https = require('https');

/**
 * 微信公众号零依赖上传永久图片素材脚本
 * 用于获取封面图的 media_id
 */

function loadEnv() {
    try {
        const skillDir = path.resolve(__dirname, '..');  // .claude/skills/wechat-draft/
        const candidates = [
            path.resolve(skillDir, '.env'),               // Skill 目录（最优先）
            path.resolve(process.cwd(), '.env'),          // 当前工作目录
            path.resolve(skillDir, '..', '..', '..', '.env'), // 项目根目录
        ];
        for (const envPath of candidates) {
            if (fs.existsSync(envPath)) {
                const content = fs.readFileSync(envPath, 'utf8');
                content.split('\n').forEach(line => {
                    const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
                    if (match) {
                        const key = match[1];
                        let value = (match[2] || '').trim();
                        value = value.replace(/^['"]|['"]$/g, '');
                        if (!process.env[key]) {
                            process.env[key] = value;
                        }
                    }
                });
                break;
            }
        }
    } catch (e) {
        // 忽略加载错误
    }
}

function requestJson(url, options = {}) {
    return new Promise((resolve, reject) => {
        const req = https.request(url, options, (res) => {
            let data = '';
            res.on('data', chunk => { data += chunk; });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(new Error(`解析 JSON 失败: ${e.message}, 返回内容: ${data}`));
                }
            });
        });
        req.on('error', reject);
        if (options.bodyBuffers) {
            options.bodyBuffers.forEach(buf => req.write(buf));
        }
        req.end();
    });
}

function parseCli() {
    return {
        fileToUpload: process.argv[2],
        autoWriteEnv: process.argv.includes('--write-env'),
        json: process.argv.includes('--json')
    };
}

async function getAccessToken(appId, appSecret) {
    const url = `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`;
    const data = await requestJson(url, { method: 'GET' });
    if (data.errcode) {
        throw new Error(`获取 Access Token 失败: [${data.errcode}] ${data.errmsg}`);
    }
    return data.access_token;
}

async function uploadMaterial(token, filePath) {
    const url = `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${token}&type=image`;

    if (!fs.existsSync(filePath)) {
        throw new Error(`找不到图片文件: ${filePath}`);
    }

    const fileName = path.basename(filePath);
    const fileData = fs.readFileSync(filePath);
    const boundary = '----WeChatBoundary' + Date.now().toString(16);

    const header = `--${boundary}\r\nContent-Disposition: form-data; name="media"; filename="${fileName}"\r\nContent-Type: application/octet-stream\r\n\r\n`;
    const footer = `\r\n--${boundary}--\r\n`;

    const headerBuffer = Buffer.from(header, 'utf8');
    const footerBuffer = Buffer.from(footer, 'utf8');
    const totalLength = headerBuffer.length + fileData.length + footerBuffer.length;

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': `multipart/form-data; boundary=${boundary}`,
            'Content-Length': totalLength
        },
        bodyBuffers: [headerBuffer, fileData, footerBuffer]
    };

    const data = await requestJson(url, options);
    if (data.errcode) {
        throw new Error(`上传图片失败: [${data.errcode}] ${data.errmsg}`);
    }
    return data;
}

async function main() {
    loadEnv();

    const { fileToUpload, autoWriteEnv, json } = parseCli();

    const appId = process.env.WECHAT_APP_ID;
    const appSecret = process.env.WECHAT_APP_SECRET;

    if (!appId || !appSecret) {
        console.error('错误: 未找到微信 API 凭证。请检查 .env 文件。');
        process.exit(1);
    }

    if (!fileToUpload) {
        console.error('使用方法:');
        console.error('  node upload_image.js <本地图片路径> [--write-env] [--json]');
        console.error('');
        console.error('参数:');
        console.error('  --write-env  上传成功后自动将 media_id 写入 .env 的 WECHAT_DEFAULT_THUMB_MEDIA_ID');
        console.error('  --json       输出 JSON，便于其他脚本解析');
        process.exit(1);
    }

    try {
        console.log('1. 获取 access_token...');
        const token = await getAccessToken(appId, appSecret);
        console.log('   获取成功!');

        const resolvedPath = path.resolve(process.cwd(), fileToUpload);
        console.log(`2. 正在上传图片: [${fileToUpload}] 到永久素材库...`);
        const result = await uploadMaterial(token, resolvedPath);

        console.log('\n==============================');
        console.log('图片上传成功!');
        console.log(`media_id: ${result.media_id}`);
        console.log('==============================\n');

        if (json) {
            console.log(JSON.stringify({
                success: true,
                media_id: result.media_id,
                url: result.url || null,
                name: result.name || path.basename(resolvedPath)
            }));
        }

        if (autoWriteEnv) {
            // 寻找 .env 文件并回写（优先写入 Skill 目录）
            const skillDir = path.resolve(__dirname, '..');
            const candidates = [
                path.resolve(skillDir, '.env'),
                path.resolve(process.cwd(), '.env'),
                path.resolve(skillDir, '..', '..', '..', '.env'),
            ];
            for (const envPath of candidates) {
                if (fs.existsSync(envPath)) {
                    let content = fs.readFileSync(envPath, 'utf8');
                    if (content.includes('WECHAT_DEFAULT_THUMB_MEDIA_ID=')) {
                        content = content.replace(/WECHAT_DEFAULT_THUMB_MEDIA_ID=.*/, `WECHAT_DEFAULT_THUMB_MEDIA_ID=${result.media_id}`);
                    } else {
                        content += `\nWECHAT_DEFAULT_THUMB_MEDIA_ID=${result.media_id}\n`;
                    }
                    fs.writeFileSync(envPath, content, 'utf8');
                    console.log(`已自动将 media_id 写入 ${envPath}`);
                    break;
                }
            }
        }
    } catch (err) {
        console.error('\n--- 发生错误 ---');
        console.error(err.message);
        if (process.argv.includes('--json')) {
            console.log(JSON.stringify({ success: false, error: err.message }));
        }
        process.exit(1);
    }
}

module.exports = {
    loadEnv,
    requestJson,
    getAccessToken,
    uploadMaterial,
    parseCli,
    main
};

if (require.main === module) {
    main();
}
