#!/usr/bin/env node
// 百科虾知识库同步脚本 v16
// 支持更多飞书文档block类型：bullet, ordered, callout, code, grid, grid_column, view, board
// v16: 凭证从 openclaw.json 读取，不再用单独配置文件

const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');
const { URL } = require('url');
const os = require('os');

// 路径基于 skill 目录（不接受外部硬编码路径）
const SKILL_DIR = path.join(__dirname, '..');

// Agent name：从命令行 --agent=<name> 传入
const agentArg = process.argv.find(arg => arg.startsWith('--agent='));
const AGENT_NAME = agentArg ? agentArg.split('=')[1] : null;

if (!AGENT_NAME) {
    console.error('错误：需要通过 --agent=<name> 指定 agent 名称');
    console.error('示例：node sync.js --agent=baikexia');
    process.exit(1);
}

// Agent workspace 下的缓存目录
const WORKSPACE_DIR = path.join(SKILL_DIR, '..', '..', '..', `workspace-${AGENT_NAME}`);
const CACHE_DIR = path.join(WORKSPACE_DIR, 'cache');
const IMAGES_DIR = path.join(CACHE_DIR, 'images');
const FILES_DIR = path.join(CACHE_DIR, 'files');
const BOARDS_DIR = path.join(CACHE_DIR, 'boards');

// 全局累积的用户名映射（从 block 数据直接提取，不调 API）
let globalUserIdToName = new Map();

// 凭证从 openclaw.json 读取
function loadFeishuConfig() {
    // 尝试多个可能的 openclaw.json 位置
    const homeDir = os.homedir();
    const possiblePaths = [
        path.join(homeDir, '.openclaw', 'openclaw.json'),
        path.join(homeDir, '.openclaw', 'openclaw.local.json'),
    ];

    let openclawConfig = null;
    for (const configPath of possiblePaths) {
        if (fs.existsSync(configPath)) {
            try {
                openclawConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
                break;
            } catch (e) {
                // continue
            }
        }
    }

    if (!openclawConfig) {
        throw new Error(`找不到 openclaw.json，请确认 OpenClaw 已正确配置`);
    }

    // 从 channels.feishu.accounts[agentName] 获取凭证
    const feishuAccounts = openclawConfig?.channels?.feishu?.accounts;
    if (!feishuAccounts || !feishuAccounts[AGENT_NAME]) {
        throw new Error(`openclaw.json 中未找到 agent '${AGENT_NAME}' 的飞书凭证`);
    }

    const account = feishuAccounts[AGENT_NAME];
    if (!account.appId || !account.appSecret) {
        throw new Error(`agent '${AGENT_NAME}' 的飞书凭证不完整（缺少 appId 或 appSecret）`);
    }

    return { appId: account.appId, appSecret: account.appSecret };
}

// 多 Wiki 配置
const WIKI_LIST_PATH = path.join(__dirname, 'wiki_list.json');
const wikiConfig = JSON.parse(fs.readFileSync(WIKI_LIST_PATH, 'utf8'));

// 解析 Wiki URL，自动提取 token 和 domain
function parseWikiUrl(url) {
    try {
        const urlObj = new URL(url);
        const parts = urlObj.pathname.split('/');
        const token = parts[parts.length - 1] || parts[parts.length - 2];
        const domain = urlObj.hostname;
        return { domain, token };
    } catch (e) {
        return null;
    }
}

// 标准化 Wiki 配置
const WIKIS = wikiConfig.wikis.map(w => {
    // 如果 url 存在，解析 token 和 domain
    if (w.url) {
        const parsed = parseWikiUrl(w.url);
        if (parsed) {
            return {
                name: w.name || w.token,
                token: parsed.token,
                domain: parsed.domain,
                spaceId: w.spaceId || null
            };
        }
    }
    // 否则使用直接配置
    return {
        name: w.name || w.token,
        token: w.token,
        domain: w.domain || 'campsnail.feishu.cn',
        spaceId: w.spaceId || null
    };
});

const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

const { appId: APP_ID, appSecret: APP_SECRET } = loadFeishuConfig();

let accessToken = '';

function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

// 下载二进制文件
function downloadBinary(url, destPath, token) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const opts = {
            hostname: urlObj.hostname,
            path: urlObj.pathname + urlObj.search,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'image/*,*/*'
            }
        };

        const req = https.request(opts, (res) => {
            if (res.statusCode === 301 || res.statusCode === 302) {
                const redirectUrl = res.headers.location;
                if (redirectUrl) {
                    downloadBinary(redirectUrl, destPath, token).then(resolve).catch(reject);
                    return;
                }
            }

            if (res.statusCode !== 200) {
                reject(new Error(`下载失败: HTTP ${res.statusCode}`));
                return;
            }

            const stream = fs.createWriteStream(destPath);
            res.pipe(stream);
            stream.on('finish', () => resolve(destPath));
            stream.on('error', reject);
        });

        req.on('error', reject);
        req.end();
    });
}

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
        if (options.body) req.write(JSON.stringify(options.body));
        req.end();
    });
}

async function getToken() {
    const resp = await fetchJson(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { app_id: APP_ID, app_secret: APP_SECRET }
    });
    if (!resp.tenant_access_token) throw new Error(`获取token失败`);
    return resp.tenant_access_token;
}

// 获取 wiki 的最后编辑时间
async function getWikiEditTime(token, wiki) {
    try {
        const resp = await fetchJson(`${FEISHU_BASE}/wiki/v2/spaces/get_node?token=${wiki.token}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (resp.data?.node?.obj_edit_time) {
            return resp.data.node.obj_edit_time;
        }
    } catch (err) {
        log(`获取wiki编辑时间失败: ${err.message}`);
    }
    return null;
}

// 收集文档中所有 mention_user 的 user_id 和 name（直接从 block 数据取，不调 API）
function collectUserIdsAndNames(blocksData) {
    const userIds = [];  // 改为数组，保持顺序
    const userIdToName = new Map();
    const blocks = blocksData.data?.items || [];

    function traverse(obj) {
        if (typeof obj !== 'object' || obj === null) return;
        if (obj.mention_user && obj.mention_user.user_id) {
            const userId = obj.mention_user.user_id;
            const name = obj.mention_user.name || userId;
            if (!userIdToName.has(userId)) {
                userIds.push(userId);
                userIdToName.set(userId, name);
            }
        }
        for (const key of Object.keys(obj)) {
            traverse(obj[key]);
        }
    }

    traverse(blocks);
    return { userIds, userIdToName };
}

// 批量获取用户信息
async function fetchUserNames(userIds, token) {
    const userMap = new Map();

    for (const userId of userIds) {
        try {
            const url = `${FEISHU_BASE}/contact/v3/users/${userId}?user_id_type=open_id`;
            const resp = await fetchJson(url, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            log(`获取用户 ${userId} API响应: ${JSON.stringify(resp)}`);
            if (resp.data?.user?.name) {
                userMap.set(userId, resp.data.user.name);
                log(`获取用户: ${resp.data.user.name} (${userId})`);
            }
        } catch (err) {
            log(`获取用户 ${userId} 失败: ${err.message}`);
            // 调试：打印完整响应
            try {
                const debugUrl = `${FEISHU_BASE}/contact/v3/users/${userId}?user_id_type=open_id`;
                const debugResp = await fetchJson(debugUrl, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                log(`调试响应: ${JSON.stringify(debugResp)}`);
            } catch (e) {
                log(`调试请求也失败: ${e.message}`);
            }
        }
    }

    return userMap;
}

// 处理 @提及格式
function replaceMentionUsers(content, userMap) {
    if (!userMap || userMap.size === 0) return content;
    return content.replace(/<at user_id="([^"]+)">([^<]*)<\/at>/g, (match, userId, oldName) => {
        const newName = userMap.get(userId);
        if (newName) {
            return `<at user_id="${userId}">${newName}</at>`;
        }
        return match;
    });
}

// 增强 Q&A 内容的搜索友好性
function enhanceQAContent(content) {
    let result = content;

    const qaRegex = /(Q\d+[^\n？]*\？[^\n]*\n)(?!相关关键词)/gi;
    result = result.replace(qaRegex, (match) => {
        const qText = match.toLowerCase();
        let keywords = [];

        if (qText.includes('wifi')) keywords.push('wifi');
        if (qText.includes('打印机')) keywords.push('打印机');
        if (qText.includes('会议室')) keywords.push('会议室');
        if (qText.includes('打卡')) keywords.push('打卡');
        if (qText.includes('快递')) keywords.push('快递');
        if (qText.includes('停车')) keywords.push('停车');
        if (qText.includes('电梯')) keywords.push('电梯');
        if (qText.includes('门禁')) keywords.push('门禁');
        if (qText.includes('猫')) keywords.push('猫');
        if (qText.includes('团建')) keywords.push('团建');
        if (qText.includes('体检')) keywords.push('体检');
        if (qText.includes('补贴')) keywords.push('补贴');
        if (qText.includes('下午茶')) keywords.push('下午茶');
        if (qText.includes('报销')) keywords.push('报销');
        if (qText.includes('密码')) keywords.push('密码');
        if (qText.includes('账号')) keywords.push('账号');

        if (keywords.length > 0) {
            return match + '相关关键词：' + keywords.join('、') + '\n';
        }
        return match;
    });

    const searchRegex = /(Q\d+[^\n？]*\？[^\n]*\n相关关键词[：:][^\n]*\n)/gi;
    result = result.replace(searchRegex, (match) => {
        const qText = match.toLowerCase();
        let topic = '';

        if (qText.includes('wifi')) topic = 'wifi wifi密码 wifi账号 无线网';
        else if (qText.includes('打印机')) topic = '打印机 打印 复印';
        else if (qText.includes('会议室')) topic = '会议室 开会 预定';
        else if (qText.includes('打卡')) topic = '打卡 考勤 上班';
        else if (qText.includes('快递')) topic = '快递 寄件 收件';
        else if (qText.includes('停车')) topic = '停车 车位 车库';
        else if (qText.includes('电梯')) topic = '电梯 梯控';
        else if (qText.includes('门禁')) topic = '门禁 刷脸 通行';
        else if (qText.includes('猫')) topic = '猫 猫咪 宠物';
        else if (qText.includes('团建')) topic = '团建 旅游';
        else if (qText.includes('体检')) topic = '体检 健康';
        else if (qText.includes('补贴')) topic = '补贴 租房 应届生';
        else if (qText.includes('下午茶')) topic = '下午茶 零食 饮料';
        else if (qText.includes('报销')) topic = '报销 发票 财务';
        else if (qText.includes('福利')) topic = '福利 节假日 活动';

        if (topic) {
            return `【搜索词：${topic}】\n` + match;
        }
        return match;
    });

    result = result.replace(
        /(【搜索词：wifi wifi密码 wifi账号 无线网】[^\n]*\nQ1[^\n]*\n[^\n]*\n)(无线网账号[：:]?\n📷[^\n]*\n)/gi,
        '$1$2实际WiFi账号：Future Studio-2.4G 或 Future Studio-5G\n'
    );

    return result;
}

async function getWikiNode(token, wiki) {
    const resp = await fetchJson(`${FEISHU_BASE}/wiki/v2/spaces/get_node?token=${wiki.token}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    // 如果没有 spaceId，从响应中提取（API 返回的是 space_id）
    if (!wiki.spaceId && resp.data?.node?.space_id) {
        wiki.spaceId = String(resp.data.node.space_id);
    }
    return resp;
}

async function listNodes(token, wiki, parentToken) {
    if (!wiki.spaceId) {
        log(`ERROR: wiki.spaceId is null, cannot list nodes`);
        return { data: { items: [], has_more: false } };
    }
    let url = `${FEISHU_BASE}/wiki/v2/spaces/${wiki.spaceId}/nodes?page_size=50`;
    if (parentToken) url += `&parent_node_token=${parentToken}`;
    return await fetchJson(url, { headers: { 'Authorization': `Bearer ${token}` } });
}

async function readDocBlocks(token, docToken) {
    try {
        const resp = await fetchJson(
            `${FEISHU_BASE}/docx/v1/documents/${docToken}/blocks?page_size=500&document_revision_id=-1`,
            { headers: { 'Authorization': `Bearer ${token}` } }
        );
        if (resp.code === 0 || resp.data) {
            return resp;
        }
    } catch (e) { /* continue */ }

    try {
        const resp = await fetchJson(
            `${FEISHU_BASE}/doc/v1/documents/${docToken}/blocks?page_size=500`,
            { headers: { 'Authorization': `Bearer ${token}` } }
        );
        if (resp.code === 0 || resp.data) {
            return resp;
        }
    } catch (e) { /* continue */ }

    return await fetchJson(
        `${FEISHU_BASE}/wiki/v2/spaces/${SPACE_ID}/nodes/${docToken}/blocks?page_size=500`,
        { headers: { 'Authorization': `Bearer ${token}` } }
    );
}

function applyStyle(text, style) {
    if (!style) return text;
    const styles = [];
    if (style.bold) styles.push('**');
    if (style.italic) styles.push('_');
    if (style.strikethrough) styles.push('~~');
    if (style.underline) styles.push('++');
    if (style.inline_code) styles.push('`');

    if (styles.length === 0) return text;

    const order = ['`', '~~', '_', '**', '++'];
    const ordered = styles.sort((a, b) => order.indexOf(a) - order.indexOf(b));
    return ordered.join('') + text + ordered.reverse().join('');
}

function extractElement(el) {
    if (!el) return '';

    if (el.text_run) {
        const tr = el.text_run;
        let text = tr.content || '';
        const linkUrl = tr.link?.url || tr.text_element_style?.link?.url;
        if (linkUrl) {
            const decodedUrl = decodeURIComponent(linkUrl);
            return `[${text}](${decodedUrl})`;
        }
        return applyStyle(text, tr.text_element_style);
    }

    if (el.mention_doc) {
        const md = el.mention_doc;
        const title = md.title || '文档链接';
        const url = md.url || '';
        return `[${title}](${url})`;
    }

    if (el.mention_user) {
        const mu = el.mention_user;
        const userId = mu.user_id || '';
        const name = mu.name || mu.user_id || '未知';
        if (userId) {
            return `<at user_id="${userId}">${name}</at>`;
        }
        return `@${name}`;
    }

    if (el.mention_channel) {
        const mc = el.mention_channel;
        const name = mc.name || mc.channel_id || '频道';
        return `#${name}`;
    }

    return '';
}

function getBlockElementKey(block) {
    const typeToKey = {
        1: 'page', 2: 'text', 3: 'heading1', 4: 'heading2', 5: 'heading3',
        6: 'heading4', 7: 'heading5', 8: 'heading6', 9: 'heading7',
        10: 'heading8', 11: 'heading9', 12: 'bullet', 13: 'ordered',
        19: 'callout', 23: 'code', 27: 'image',
    };
    return typeToKey[block.block_type];
}

function extractBlockTextRecursive(block, blocksMap, indent = '') {
    let result = '';

    const elementsKey = getBlockElementKey(block);
    if (elementsKey && block[elementsKey]?.elements) {
        for (const el of block[elementsKey].elements) {
            result += extractElement(el);
        }
    }

    if (block.children && block.children.length > 0) {
        if (block.block_type === 12 || block.block_type === 13) {
            result += '\n';
        }

        for (const childId of block.children) {
            const childBlock = blocksMap.get(childId);
            if (childBlock) {
                result += extractBlockTextRecursive(childBlock, blocksMap, indent);
            }
        }
    }

    return result;
}

function getImageContext(blockIndex, blocks) {
    for (let i = blockIndex - 1; i >= 0; i--) {
        const b = blocks[i];
        if (b.block_type === 3 || b.block_type === 4 || b.block_type === 5) {
            const text = extractBlockTextRecursive(b, new Map(blocks.map(block => [block.block_id, block]))).trim();
            if (text && text.length < 100) return text;
        }
        if (b.block_type === 2) {
            const text = extractBlockTextRecursive(b, new Map(blocks.map(block => [block.block_id, block]))).trim();
            if (text && text.length < 50) return text;
        }
        if (b.block_type === 27) break;
    }
    return '';
}

function detectImageType(buffer) {
    if (buffer[0] === 0xFF && buffer[1] === 0xD8) return 'jpg';
    if (buffer[0] === 0x89 && buffer[1] === 0x50 && buffer[2] === 0x4E && buffer[3] === 0x47) return 'png';
    if (buffer[0] === 0x47 && buffer[1] === 0x49 && buffer[2] === 0x46) return 'gif';
    if (buffer[0] === 0x42 && buffer[1] === 0x4D) return 'bmp';
    if (buffer[0] === 0x49 && buffer[1] === 0x49 && buffer[2] === 0x2A) return 'tif';
    if (buffer[0] === 0x4D && buffer[1] === 0x4D && buffer[2] === 0x2B) return 'tif';
    return 'jpg';
}

async function processImagesInBlocks(blocksData, docToken, token) {
    const blocks = blocksData.data?.items || [];
    const imageMap = new Map();

    for (let i = 0; i < blocks.length; i++) {
        const block = blocks[i];
        if (block.block_type === 27 && block.image && block.image.token) {
            const imgToken = block.image.token;

            // 只使用 token 作为文件名，避免中文命名错误
            const fileName = `${imgToken}.jpg`;
            const localPath = path.join(IMAGES_DIR, fileName);

            if (!fs.existsSync(localPath)) {
                log(`下载图片: ${imgToken}`);

                try {
                    const downloadUrl = `${FEISHU_BASE}/drive/v1/medias/${imgToken}/download`;
                    await downloadBinary(downloadUrl, localPath + '.tmp', token);

                    const buffer = fs.readFileSync(localPath + '.tmp');
                    const ext = detectImageType(buffer);
                    const finalPath = localPath.replace('.jpg', `.${ext}`);
                    fs.renameSync(localPath + '.tmp', finalPath);

                    imageMap.set(imgToken, finalPath);
                    log(`图片已保存: ${path.basename(finalPath)}`);
                } catch (err) {
                    log(`下载图片失败: ${err.message}`);
                    imageMap.set(imgToken, null);
                }
            } else {
                imageMap.set(imgToken, localPath);
            }
        }
    }

    return imageMap;
}

// 处理文件附件块（block_type 23）
async function processFileBlocks(blocksData, docToken, token) {
    const blocks = blocksData.data?.items || [];
    const fileMap = new Map();

    for (let i = 0; i < blocks.length; i++) {
        const block = blocks[i];
        if (block.block_type === 23 && block.file && block.file.token) {
            const fileToken = block.file.token;
            const fileName = block.file.name || `file_${fileToken.substring(0, 8)}`;
            
            // 获取文件扩展名
            const ext = fileName.split('.').pop() || 'bin';
            const safeName = fileName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5.-]/g, '_');
            const localPath = path.join(FILES_DIR, `${safeName}_${fileToken.substring(0, 8)}.${ext}`);

            if (!fs.existsSync(localPath)) {
                log(`下载文件: ${fileName}`);

                try {
                    const downloadUrl = `${FEISHU_BASE}/drive/v1/medias/${fileToken}/download`;
                    await downloadBinary(downloadUrl, localPath, token);
                    log(`文件已保存: ${path.basename(localPath)}`);
                    fileMap.set(fileToken, localPath);
                } catch (err) {
                    log(`下载文件失败: ${err.message}`);
                    fileMap.set(fileToken, null);
                }
            } else {
                fileMap.set(fileToken, localPath);
            }
        }
    }

    return fileMap;
}

async function processBoardBlocks(blocksData, docToken, token) {
    const blocks = blocksData.data?.items || [];
    const boardMap = new Map();

    for (const block of blocks) {
        if (block.block_type === 43 && block.board && block.board.token) {
            const boardToken = block.board.token;
            const boardPath = path.join(BOARDS_DIR, `${boardToken}.json`);

            log(`发现画板: ${boardToken}`);

            if (!fs.existsSync(boardPath)) {
                try {
                    boardMap.set(boardToken, {
                        token: boardToken,
                        note: '画板内容需手动访问飞书查看'
                    });
                    fs.mkdirSync(BOARDS_DIR, { recursive: true });
                    fs.writeFileSync(boardPath, JSON.stringify({
                        token: boardToken,
                        doc_token: docToken,
                        note: '画板内容同步时间: ' + new Date().toISOString()
                    }, null, 2));
                } catch (err) {
                    log(`处理画板失败: ${err.message}`);
                }
            }
        }
    }

    return boardMap;
}

function extractTextFromBlocks(blocksData, imageMap, fileMap, docToken, docTitle) {
    const blocks = blocksData.data?.items || [];
    const blocksMap = new Map(blocks.map(b => [b.block_id, b]));
    const childrenMap = new Map();

    for (const block of blocks) {
        if (block.parent_id) {
            if (!childrenMap.has(block.parent_id)) {
                childrenMap.set(block.parent_id, []);
            }
            childrenMap.get(block.parent_id).push(block);
        }
    }

    function processBlock(block, depth = 0) {
        let text = '';

        if (block.block_type === 27 && block.image?.token) {
            const imgToken = block.image.token;
            const localPath = imageMap.get(imgToken);
            if (localPath && fs.existsSync(localPath)) {
                const relativePath = path.relative(path.join(SKILL_DIR, 'workspace'), localPath);
                text += `MEDIA:${relativePath}\n`;
            }
            return text;
        }

        // 处理文件附件块（block_type 23）- 输出为飞书云文档链接
        if (block.block_type === 23 && block.file?.token) {
            const fileToken = block.file.token;
            const fileName = block.file.name || fileToken;
            // 使用 wiki 链接格式，指向该文件所在页面
            text += `[📎 ${fileName}](https://campsnail.feishu.cn/wiki/${WIKI_TOKEN}#${block.block_id})\n`;
            return text;
        }

        if (block.block_type === 43 && block.board?.token) {
            // 使用 wiki 链接 + block_id 定位到画板
            text += `[画板](https://campsnail.feishu.cn/wiki/${WIKI_TOKEN}#${block.block_id})\n`;
            return text;
        }

        if (block.block_type === 10) {
            return '\n---\n';
        }

        const elementsKey = getBlockElementKey(block);
        if (elementsKey && block[elementsKey]?.elements) {
            for (const el of block[elementsKey].elements) {
                text += extractElement(el);
            }
        }

        const children = childrenMap.get(block.block_id) || [];
        for (const child of children) {
            if (child.block_type === 13) text += '\n1. ';
            if (child.block_type === 12) text += '\n- ';

            const childText = processBlock(child, depth + 1);
            text += childText;
        }

        return text;
    }

    let result = '';
    const rootBlock = blocks.find(b => b.block_type === 1);

    if (rootBlock) {
        const rootElementsKey = getBlockElementKey(rootBlock);
        if (rootElementsKey && rootBlock[rootElementsKey]?.elements) {
            for (const el of rootBlock[rootElementsKey].elements) {
                result += extractElement(el);
            }
            result += '\n';
        }

        const rootChildren = childrenMap.get(rootBlock.block_id) || [];

        for (const child of rootChildren) {
            if (child.block_type === 13) {
                result += `\n1. `;
            } else if (child.block_type === 12) {
                result += '\n- ';
                if (child.bullet?.elements) {
                    for (const el of child.bullet.elements) {
                        result += extractElement(el);
                    }
                }
                result += '\n';
            } else if (child.block_type === 10) {
                result += '\n---\n';
            } else if (child.block_type === 43) {
                if (child.board?.token) {
                    result += `[画板](https://campsnail.feishu.cn/wiki/${WIKI_TOKEN}#${child.block_id})\n`;
                }
            } else if (child.block_type === 27) {
                if (child.image?.token) {
                    const imgToken = child.image.token;
                    const localPath = imageMap.get(imgToken);
                    if (localPath && fs.existsSync(localPath)) {
                        const relativePath = path.relative(path.join(SKILL_DIR, 'workspace'), localPath);
                        result += `MEDIA:${relativePath}\n`;
                    }
                }
            } else {
                const childText = processBlock(child);
                result += childText;
            }

            if ((child.block_type === 12 || child.block_type === 13) && child.children) {
                for (const childId of child.children) {
                    const subChild = blocksMap.get(childId);
                    if (subChild) {
                        const subText = processBlock(subChild);
                        result += subText;
                    }
                }
                result += '\n';
            }

            if (child.block_type !== 12 && child.block_type !== 13 && child.block_type !== 10) {
                result += '\n';
            }
        }
    }

    return result;
}

async function collectDocs(token) {
    const allContent = [];
    const allUserIds = [];

    log('获取wiki根节点...');
    const rootNodeResp = await getWikiNode(token, wiki);
    const rootNode = rootNodeResp.data?.node;

    if (!rootNode) throw new Error(`无法获取wiki根节点`);
    log(`根节点: ${rootNode.title} (${rootNode.obj_token})`);

    if (rootNode.obj_type === 'docx' && rootNode.obj_token) {
        log(`读取文档: ${rootNode.title}`);
        const blocksResp = await readDocBlocks(token, rootNode.obj_token);
        const imageMap = await processImagesInBlocks(blocksResp, rootNode.obj_token, token);
        await processBoardBlocks(blocksResp, rootNode.obj_token, token);
        const fileMap = await processFileBlocks(blocksResp, rootNode.obj_token, token);
        const { userIds, userIdToName } = collectUserIdsAndNames(blocksResp);
        allUserIds.push(...userIds);
        for (const [uid, name] of userIdToName) {
            globalUserIdToName.set(uid, name);
        }
        const text = extractTextFromBlocks(blocksResp, imageMap, fileMap, rootNode.obj_token, rootNode.title);
        if (text) allContent.push(`===== ${rootNode.title} =====\n${text}`);
    }

    if (rootNode.has_child) {
        log('获取子节点...');
        const nodesResp = await listNodes(token, '');
        const items = nodesResp.data?.items || [];

        for (const item of items) {
            if (item.obj_type === 'docx' && item.obj_token) {
                log(`读取文档: ${item.title}`);
                const blocksResp = await readDocBlocks(token, item.obj_token);
                const imageMap = await processImagesInBlocks(blocksResp, item.obj_token, token);
                const fileMap = await processFileBlocks(blocksResp, item.obj_token, token);
                await processBoardBlocks(blocksResp, item.obj_token, token);
                const { userIds, userIdToName } = collectUserIdsAndNames(blocksResp);
                allUserIds.push(...userIds);
                for (const [uid, name] of userIdToName) {
                    globalUserIdToName.set(uid, name);
                }
                const text = extractTextFromBlocks(blocksResp, imageMap, fileMap, item.obj_token, item.title);
                if (text) allContent.push(`===== ${item.title} =====\n${text}`);
            }

            if (item.has_child && item.node_token) {
                await collectChildNodes(token, item.node_token, allContent, allUserIds);
            }
        }
    }

    const contentText = allContent.join('\n\n');
    await syncWikiLinksFromText(token, contentText, allContent, allUserIds);

    return { content: allContent.join('\n\n'), userIds: [...new Set(allUserIds)] };
}

function extractWikiTokens(text) {
    const tokens = new Set();
    const wikiUrlRegex = /https:\/\/[^\/]+\.feishu\.cn\/wiki\/([a-zA-Z0-9]+)/g;
    let match;
    while ((match = wikiUrlRegex.exec(text)) !== null) {
        tokens.add(match[1]);
    }
    const directTokenRegex = /wikcn[a-zA-Z0-9]+/g;
    while ((match = directTokenRegex.exec(text)) !== null) {
        tokens.add(match[0]);
    }
    return [...tokens];
}

async function syncWikiPageByToken(token, wikiToken, allContent, allUserIds, syncedTokens = new Set()) {
    if (syncedTokens.has(wikiToken)) return;
    syncedTokens.add(wikiToken);

    try {
        const nodeResp = await fetchJson(
            `${FEISHU_BASE}/wiki/v2/spaces/get_node?token=${wikiToken}`,
            { headers: { 'Authorization': `Bearer ${token}` } }
        );

        const node = nodeResp.data?.node;
        if (!node) {
            log(`无法获取 wiki 节点: ${wikiToken}`);
            return;
        }

        if (node.obj_type === 'docx' && node.obj_token) {
            log(`[Wiki链接] 读取文档: ${node.title}`);
            const blocksResp = await readDocBlocks(token, node.obj_token);
            const imageMap = await processImagesInBlocks(blocksResp, node.obj_token, token);
            const fileMap = await processFileBlocks(blocksResp, node.obj_token, token);
            const { userIds, userIdToName } = collectUserIdsAndNames(blocksResp);
            allUserIds.push(...userIds);
            for (const [uid, name] of userIdToName) {
                globalUserIdToName.set(uid, name);
            }
            const text = extractTextFromBlocks(blocksResp, imageMap, fileMap, node.obj_token, node.title);
            if (text) {
                allContent.push(`===== ${node.title} =====\n${text}`);
                await syncWikiLinksFromText(token, text, allContent, allUserIds, syncedTokens);
            }
        }
    } catch (e) {
        log(`同步 wiki 页面失败 ${wikiToken}: ${e.message}`);
    }
}

async function syncWikiLinksFromText(token, text, allContent, allUserIds, syncedTokens = new Set()) {
    const tokens = extractWikiTokens(text);
    for (const wikiToken of tokens) {
        await syncWikiPageByToken(token, wikiToken, allContent, allUserIds, syncedTokens);
    }
}

async function collectChildNodes(token, parentToken, allContent, allUserIds) {
    const nodesResp = await listNodes(token, parentToken);
    const items = nodesResp.data?.items || [];

    for (const item of items) {
        if (item.obj_type === 'docx' && item.obj_token) {
            log(`读取文档: ${item.title}`);
            const blocksResp = await readDocBlocks(token, item.obj_token);
            const imageMap = await processImagesInBlocks(blocksResp, item.obj_token, token);
            const fileMap = await processFileBlocks(blocksResp, item.obj_token, token);
            await processBoardBlocks(blocksResp, item.obj_token, token);
            const { userIds, userIdToName } = collectUserIdsAndNames(blocksResp);
            allUserIds.push(...userIds);
            for (const [uid, name] of userIdToName) {
                globalUserIdToName.set(uid, name);
            }
            const text = extractTextFromBlocks(blocksResp, imageMap, fileMap, item.obj_token, item.title);
            if (text) allContent.push(`===== ${item.title} =====\n${text}`);
        }

        if (item.has_child && item.node_token) {
            await collectChildNodes(token, item.node_token, allContent, allUserIds);
        }
    }
}

async function main() {
    const isForce = process.argv.includes('--force');

    log('开始同步知识库...' + (isForce ? ' (手动全量同步)' : ''));

    try {
        accessToken = await getToken();
        log('获取access token成功');

        fs.mkdirSync(IMAGES_DIR, { recursive: true });
        fs.mkdirSync(FILES_DIR, { recursive: true });
        fs.mkdirSync(BOARDS_DIR, { recursive: true });

        const metadataFile = path.join(CACHE_DIR, 'metadata.json');
        const existingMetadata = fs.existsSync(metadataFile) 
            ? JSON.parse(fs.readFileSync(metadataFile, 'utf8')) 
            : null;

        // 检查 wiki 编辑时间
        const currentWikiEditTime = await getWikiEditTime(accessToken);
        log(`当前wiki编辑时间: ${currentWikiEditTime}`);

        // 如果不是强制同步，且 wiki 时间没变化，跳过内容拉取
        if (!isForce && existingMetadata?.wiki_edit_time) {
            if (currentWikiEditTime && currentWikiEditTime === existingMetadata.wiki_edit_time) {
                log('Wiki内容未变化，跳过同步');
                const metadata = {
                    ...existingMetadata,
                    last_sync: new Date().toISOString(),
                    status: 'no-change'
                };
                fs.writeFileSync(metadataFile, JSON.stringify(metadata, null, 2));
                log('同步流程结束');
                return;
            }
        }

        const { content: allContent, userIds } = await collectDocs(accessToken);

        if (!allContent) {
            log('ERROR: 未能获取到任何文档内容');
            process.exit(1);
        }

        let finalContent = allContent;
        finalContent = enhanceQAContent(finalContent);

        if (globalUserIdToName.size > 0) {
            log(`发现 ${globalUserIdToName.size} 个用户提及，直接使用文档中的用户名...`);
            finalContent = replaceMentionUsers(finalContent, globalUserIdToName);
            log(`用户名替换完成`);
        }

        log(`获取到内容长度: ${finalContent.length} 字符`);

        const newHash = crypto.createHash('sha256').update(finalContent, 'utf8').digest('hex');
        log(`新内容hash: ${newHash}`);

        // 检查内容 hash 是否变化
        let needSync = true;
        if (!isForce && existingMetadata?.content_hash === newHash) {
            log('内容hash未变化，跳过更新');
            needSync = false;
        }

        if (needSync) {
            log('开始更新缓存...');
            fs.writeFileSync(path.join(CACHE_DIR, 'content.json'), finalContent, 'utf8');
            log('缓存更新完成');
        }

        const metadata = {
            wiki_token: WIKI_TOKEN,
            space_id: SPACE_ID,
            wiki_url: `https://campsnail.feishu.cn/wiki/${WIKI_TOKEN}`,
            last_sync: new Date().toISOString(),
            wiki_edit_time: currentWikiEditTime,
            content_hash: newHash,
            status: 'success',
            version: 'v14'
        };
        fs.writeFileSync(metadataFile, JSON.stringify(metadata, null, 2));
        log('同步流程结束');

    } catch (error) {
        log(`ERROR: ${error.message}`);
        console.error(error);
        process.exit(1);
    }
}

main();
