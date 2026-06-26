const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const DEFAULT_AUTHOR = 'AI源来如此';
const DEFAULT_COMMENT_FLAG = 1;

/**
 * 微信公众号零依赖上传草稿脚本
 * 兼容低版本 Node.js (使用原生 http/https 模块)
 */

function loadEnv() {
    try {
        const skillDir = path.resolve(__dirname, '..');
        const candidates = [
            path.resolve(skillDir, '.env'),
            path.resolve(process.cwd(), '.env'),
            path.resolve(skillDir, '..', '..', '..', '.env'),
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

function getTransport(targetUrl) {
    return targetUrl.startsWith('https:') ? https : http;
}

function requestRaw(url, options = {}) {
    return new Promise((resolve, reject) => {
        const req = getTransport(url).request(url, options, (res) => {
            const chunks = [];
            res.on('data', chunk => { chunks.push(chunk); });
            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode || 0,
                    headers: res.headers || {},
                    body: Buffer.concat(chunks)
                });
            });
        });
        req.on('error', reject);
        if (options.body) {
            req.write(options.body);
        }
        if (options.bodyBuffers) {
            options.bodyBuffers.forEach(buf => req.write(buf));
        }
        req.end();
    });
}

function requestJson(url, options = {}) {
    return new Promise((resolve, reject) => {
        requestRaw(url, options).then(({ body }) => {
            const data = body.toString('utf8');
            try {
                resolve(JSON.parse(data));
            } catch (e) {
                reject(new Error(`解析 JSON 失败: ${e.message}, 返回内容: ${data}`));
            }
        }).catch(reject);
    });
}

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].substring(2);
            parsed[key] = args[i + 1] || '';
            i++;
        }
    }
    return parsed;
}

function parseCommentFlag(value, fallback) {
    if (value === undefined || value === null || value === '') return fallback;
    if (value === '0' || value === 0) return 0;
    if (value === '1' || value === 1) return 1;
    throw new Error(`评论开关参数只能是 0 或 1，收到: ${value}`);
}

function buildArticlePayload(args, env = process.env) {
    const article = {
        title: args.title,
        content: args.content,
        author: args.author || env.WECHAT_DEFAULT_AUTHOR || DEFAULT_AUTHOR,
        need_open_comment: parseCommentFlag(args['need-open-comment'], DEFAULT_COMMENT_FLAG),
        only_fans_can_comment: parseCommentFlag(args['only-fans-can-comment'], DEFAULT_COMMENT_FLAG)
    };

    if (args.digest) article.digest = args.digest;
    if (args.thumb) article.thumb_media_id = args.thumb;
    if (args['source-url']) article.content_source_url = args['source-url'];

    if (!article.thumb_media_id && env.WECHAT_DEFAULT_THUMB_MEDIA_ID) {
        article.thumb_media_id = env.WECHAT_DEFAULT_THUMB_MEDIA_ID;
    }

    return article;
}

async function getAccessToken(appId, appSecret) {
    const url = `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`;
    const data = await requestJson(url, { method: 'GET' });
    if (data.errcode) {
        throw new Error(`获取 Access Token 失败: [${data.errcode}] ${data.errmsg}`);
    }
    return data.access_token;
}

async function uploadDraft(token, articleData) {
    const url = `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${token}`;
    const bodyData = Buffer.from(JSON.stringify(articleData), 'utf8');

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': bodyData.length
        },
        body: bodyData
    };

    const data = await requestJson(url, options);
    if (data.errcode) {
        throw new Error(`上传草稿失败: [${data.errcode}] ${data.errmsg}`);
    }
    return data.media_id;
}

function inferMimeType(fileName, fallback) {
    const ext = path.extname(fileName || '').toLowerCase();
    const mimeMap = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp'
    };
    return mimeMap[ext] || fallback || 'application/octet-stream';
}

async function downloadBinary(url, redirects = 3) {
    const { statusCode, headers, body } = await requestRaw(url, { method: 'GET' });
    if ([301, 302, 303, 307, 308].includes(statusCode) && headers.location && redirects > 0) {
        const nextUrl = new URL(headers.location, url).toString();
        return downloadBinary(nextUrl, redirects - 1);
    }
    if (statusCode < 200 || statusCode >= 300) {
        throw new Error(`下载图片失败: HTTP ${statusCode}`);
    }
    return {
        data: body,
        contentType: headers['content-type'] || 'application/octet-stream'
    };
}

function resolveCssVariables(html) {
    const sectionMatch = html.match(/<section id="MdWechat" style="([^"]*)">/);
    if (!sectionMatch) return html;

    const styleText = sectionMatch[1];
    const vars = {};
    const styleParts = [];

    styleText.split(';').forEach(part => {
        const trimmed = part.trim();
        if (!trimmed) return;
        const idx = trimmed.indexOf(':');
        if (idx < 0) return;
        const key = trimmed.slice(0, idx).trim();
        const value = trimmed.slice(idx + 1).trim();
        if (key.startsWith('--')) {
            vars[key] = value;
        } else {
            styleParts.push(`${key}: ${value}`);
        }
    });

    let output = html.replace(/var\((--[\w-]+)\)/g, (_, name) => vars[name] || _);
    output = output.replace(sectionMatch[0], `<section id="MdWechat" style="${styleParts.join('; ')}">`);
    return output;
}

function getStyleMap(styleText) {
    const map = {};
    styleText.split(';').forEach(part => {
        const trimmed = part.trim();
        if (!trimmed) return;
        const idx = trimmed.indexOf(':');
        if (idx < 0) return;
        const key = trimmed.slice(0, idx).trim().toLowerCase();
        const value = trimmed.slice(idx + 1).trim();
        map[key] = value;
    });
    return map;
}

function styleMapToString(styleMap, preferredOrder = []) {
    const emitted = new Set();
    const parts = [];
    preferredOrder.forEach((key) => {
        if (styleMap[key]) {
            parts.push(`${key}: ${styleMap[key]}`);
            emitted.add(key);
        }
    });
    Object.keys(styleMap).forEach((key) => {
        if (!emitted.has(key) && styleMap[key]) {
            parts.push(`${key}: ${styleMap[key]}`);
        }
    });
    return parts.join('; ');
}

function normalizeWechatSectionBackground(html) {
    const sectionMatch = html.match(/<section id="MdWechat" style="([^"]*)">/);
    if (!sectionMatch) return html;

    const styleText = sectionMatch[1];
    const styleMap = getStyleMap(styleText);
    if (!styleMap['background-image']) return html;

    const normalized = {
        ...styleMap,
        'background-attachment': styleMap['background-attachment'] || 'scroll',
        'background-clip': styleMap['background-clip'] || 'border-box',
        'background-origin': styleMap['background-origin'] || 'padding-box',
        'background-color': styleMap['background-color'] || 'rgba(0, 0, 0, 0)',
        'width': styleMap['width'] || 'auto'
    };

    if (styleMap['background-position']) {
        normalized['background-position-x'] = 'left';
        normalized['background-position-y'] = 'top';
        delete normalized['background-position'];
    }

    const preferredOrder = [
        'margin-top', 'margin-bottom', 'margin-left', 'margin-right',
        'padding-top', 'padding-bottom', 'padding-left', 'padding-right',
        'padding',
        'background-attachment', 'background-clip', 'background-color', 'background-image', 'background-origin',
        'background-position-x', 'background-position-y', 'background-repeat', 'background-size',
        'width', 'font-family', 'font-size', 'color', 'line-height', 'word-spacing', 'letter-spacing',
        'word-break', 'overflow-wrap', 'text-align'
    ];

    const styleString = styleMapToString(normalized, preferredOrder);

    return html.replace(sectionMatch[0], `<section id="MdWechat" style="${styleString}">`);
}

function convertListBlock(listInner, markerFactory) {
        const liRegex = /<li\b([^>]*)>([\s\S]*?)<\/li>/gi;
        const items = [];
        let match;
        let index = 0;
        while ((match = liRegex.exec(listInner)) !== null) {
            const inner = match[2].trim();
            if (!inner) continue;
            index += 1;
            const normalizedInner = inner
                .replace(/^<p\b[^>]*>([\s\S]*?)<\/p>$/i, '$1')
                .replace(/^<section\b[^>]*>([\s\S]*?)<\/section>$/i, '$1')
                .trim();

            items.push(`<p style="color: rgb(89, 89, 89); font-size: 14px; line-height: 1.8em; letter-spacing: 0em; text-align: left; font-weight: normal; margin-top: 5px; margin-bottom: 5px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; text-indent: 0em;">${markerFactory(index)}&nbsp;&nbsp;${normalizedInner}</p>`);
        }

        if (!items.length) return '';
        return items.join('');
}

function convertListsToWechatParagraphs(html) {
    let output = html.replace(/<ul\b[^>]*>([\s\S]*?)<\/ul>/gi, (full, listInner) => {
        return convertListBlock(listInner, () => '&#9675;');
    });

    output = output.replace(/<ol\b[^>]*>([\s\S]*?)<\/ol>/gi, (full, listInner) => {
        return convertListBlock(listInner, (index) => `${index}.`);
    });

    return output;
}

function stripLeadingH1(html) {
    return html.replace(/^\s*<section id="MdWechat"([^>]*)>\s*<h1\b[^>]*>.*?<\/h1>/is, '<section id="MdWechat"$1>');
}

async function uploadArticleImage(token, fileName, fileData, contentType) {
    const url = `https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=${token}`;
    const boundary = '----WeChatDraftBoundary' + Date.now().toString(16);
    const header = `--${boundary}\r\nContent-Disposition: form-data; name="media"; filename="${fileName}"\r\nContent-Type: ${contentType}\r\n\r\n`;
    const footer = `\r\n--${boundary}--\r\n`;
    const headerBuffer = Buffer.from(header, 'utf8');
    const footerBuffer = Buffer.from(footer, 'utf8');
    const totalLength = headerBuffer.length + fileData.length + footerBuffer.length;

    const data = await requestJson(url, {
        method: 'POST',
        headers: {
            'Content-Type': `multipart/form-data; boundary=${boundary}`,
            'Content-Length': totalLength
        },
        bodyBuffers: [headerBuffer, fileData, footerBuffer]
    });

    if (data.errcode) {
        throw new Error(`上传正文图片失败: [${data.errcode}] ${data.errmsg}`);
    }
    if (!data.url) {
        throw new Error('上传正文图片失败: 微信未返回图片 URL');
    }
    return data.url;
}

async function rewriteImagesForWechat(token, html, htmlFilePath) {
    const imgRegex = /<img\b([^>]*?)\bsrc="([^"]+)"([^>]*)>/g;
    const matches = [...html.matchAll(imgRegex)];
    if (!matches.length) return html;

    const srcMap = new Map();
    for (const match of matches) {
        const src = match[2];
        if (srcMap.has(src) || src.startsWith('data:')) continue;

        let fileName = 'image.png';
        let fileData;
        let contentType = 'application/octet-stream';

        if (/^https?:\/\//i.test(src)) {
            const downloaded = await downloadBinary(src);
            fileData = downloaded.data;
            const urlObj = new URL(src);
            fileName = path.basename(urlObj.pathname) || fileName;
            contentType = inferMimeType(fileName, downloaded.contentType);
        } else {
            const localPath = path.resolve(path.dirname(htmlFilePath), src);
            if (!fs.existsSync(localPath)) {
                throw new Error(`正文图片不存在: ${localPath}`);
            }
            fileData = fs.readFileSync(localPath);
            fileName = path.basename(localPath);
            contentType = inferMimeType(fileName);
        }

        const wechatUrl = await uploadArticleImage(token, fileName, fileData, contentType);
        srcMap.set(src, wechatUrl);
    }

    let output = html;
    for (const [src, uploaded] of srcMap.entries()) {
        output = output.split(`src="${src}"`).join(`src="${uploaded}"`);
    }
    return output;
}

async function main() {
    loadEnv();
    const args = parseArgs();

    const appId = process.env.WECHAT_APP_ID;
    const appSecret = process.env.WECHAT_APP_SECRET;

    if (!appId || !appSecret) {
        console.error('错误: 未找到微信 API 凭证。');
        console.error('请配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量，或者放在当前技能目录的 .env 文件中。');
        process.exit(1);
    }

    if (!args.title || !args.file) {
        console.error('使用方法:');
        console.error('  node wechat_draft.js --title "文章标题" --file "content.html" [--author "作者"] [--digest "摘要"] [--thumb "素材媒体ID"] [--source-url "原文链接"] [--need-open-comment "1"] [--only-fans-can-comment "1"]');
        process.exit(1);
    }

    let content = '';
    let htmlFilePath = '';
    try {
        htmlFilePath = path.resolve(process.cwd(), args.file);
        content = fs.readFileSync(htmlFilePath, 'utf8');
    } catch (e) {
        console.error(`读取文件出错 ${args.file}:`, e.message);
        process.exit(1);
    }

    try {
        console.log('1. 正在获取 access_token...');
        const token = await getAccessToken(appId, appSecret);
        console.log('   获取成功!');

        console.log('2. 正在处理正文样式与图片...');
        content = resolveCssVariables(content);
        content = normalizeWechatSectionBackground(content);
        content = stripLeadingH1(content);
        content = convertListsToWechatParagraphs(content);
        content = await rewriteImagesForWechat(token, content, htmlFilePath);

        const article = buildArticlePayload({
            ...args,
            content
        });

        if (!article.thumb_media_id) {
            console.warn('警告: 未指定封面图(--thumb)且未设置 WECHAT_DEFAULT_THUMB_MEDIA_ID。微信接口可能返回 40007 错误。');
        }

        const payload = { articles: [article] };

        console.log(`3. 正在上传草稿: "${args.title}"...`);
        const mediaId = await uploadDraft(token, payload);
        console.log('\n==============================');
        console.log('上传草稿成功!');
        console.log(`草稿 MEDIA_ID: ${mediaId}`);
        console.log('==============================\n');
    } catch (error) {
        console.error('\n--- 发生错误 ---');
        console.error(error.message);
        process.exit(1);
    }
}

module.exports = {
    loadEnv,
    parseArgs,
    parseCommentFlag,
    buildArticlePayload,
    resolveCssVariables,
    normalizeWechatSectionBackground,
    stripLeadingH1,
    convertListsToWechatParagraphs,
    rewriteImagesForWechat,
    uploadDraft,
    getAccessToken,
    main
};

if (require.main === module) {
    main();
}
