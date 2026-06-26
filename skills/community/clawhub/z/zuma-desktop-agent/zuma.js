#!/usr/bin/env node
/**
 * zuma.js — Zuma Desktop Agent CLI
 *
 * 直接与 Zuma Robot HTTP Server 通信，无需 Bridge 中间层。
 *
 * 用法：
 *   node zuma.js <command> [-Key value ...]
 * 
 * 接口路径 | 请求方法 |
 * `/cron/status` | GET |
 * `/check_log` | GET |
 * `/cron/list` | GET |
 * `/cron/start` | POST |
 * `/cron/stop` | POST |
 * `/cron/preview` | GET |
 * `/app/list` | GET |
 * `/app/start` | POST |
 * 
 * 命令：
 *   setup
 *   cron-status
 *   cron-list
 *   cron-start 参数说明:
 *      必填：-cronid <cron_id> 
 *      可选：[-name <名称>], [-interval <每N分钟>], [-appid <appid>]
 *   cron-stop        -cronid <cron_id>
 *   cron-preview     -cronid <cron_id> -interval <每N分钟>
 *   cron-batch-start -cronids <cron_id1,cron_id2,...>
 *   cron-batch-stop  -cronids <cron_id1,cron_id2,...>
 *   check-log   -linesnumber <行数>
 *   app-start -appid <appid> [-name <名称>]
 *   app-list
 *   take-screenshot -output -clipboard
 */

import { readFileSync, existsSync, copyFileSync, mkdirSync } from 'fs';
import path, { join, dirname }                    from 'path';
import { fileURLToPath }                          from 'url';
import { execSync, spawn }                        from 'child_process';
import os                                         from 'os';
import { uploadToQClawCOS }                          from './upload.js';

const __dir = dirname(fileURLToPath(import.meta.url));

// ── 工具函数 ─────────────────────────────────────────────────────────────────

/**
 * 获取 QClaw 工作区目录路径
 * @returns {string} 工作区目录路径
 */
function getQclawWorkspace() {
    return path.join(os.homedir(), '.qclaw', 'workspace');
}

function getOpenclawWorkspace() {
    return path.join(os.homedir(), '.openclaw', 'workspace');
}

function getZumaWorkspace() {
    return path.join(os.homedir(), '.zuma-agent', 'workspace');
}

/**
 * 确保目录存在（不存在则递归创建）
 * @param {string} dirPath - 目录路径
 * @returns {string} 目录路径
 */
function ensureDir(dirPath) {
    mkdirSync(dirPath, { recursive: true });
    return dirPath;
}

// ── 配置 ──────────────────────────────────────────────────────────────────────
// token从服务端获取。准备用于连接验证。暂未使用。
function loadConfig() {
    const defaults = {
        ZUMA_SERVER_URL:     'http://127.0.0.1:53030',
        REQUEST_TIMEOUT:     '30000',
        API_KEY:             'ZUMAOPENCLAWCLIENT',
        TOKEN:               '',
        DOWNLOAD_LINKS_PAGE: ['https://docs.qq.com/doc/p/1578acc2fb00d12246bcad39e29367e5f3fa5dd9', 'https://zumaai.top/download-links'],
        DOWNLOAD_LINKS: ['https://gitee.com/biglobin/zuma_desktop_executor/releases/download/latest/ZUMAROBOT_RELEASE_STANDARD.zip', 'https://github.com/biglobin/zuma_desktop_executor/releases/download/latest/ZUMAROBOT_RELEASE_STANDARD.zip'],
        IMGBB_API_KEY:       '669ae31e56af5f66402d9ff239f1980d',
    };
    const envPath = join(__dir, '..', '.env');
    if (existsSync(envPath)) {
        for (const line of readFileSync(envPath, 'utf8').split('\n')) {
            const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*)/);
            if (m) defaults[m[1]] = m[2].trim();
        }
    }
    return {
        server:            process.env.ZUMA_SERVER_URL     || defaults.ZUMA_SERVER_URL,
        timeout:           parseInt(process.env.REQUEST_TIMEOUT || defaults.REQUEST_TIMEOUT),
        apiKey:            process.env.API_KEY              || defaults.API_KEY,
        token:             process.env.TOKEN              || defaults.TOKEN,
        downloadLinksPage: process.env.DOWNLOAD_LINKS_PAGE  || defaults.DOWNLOAD_LINKS_PAGE,
        downloadLinks: process.env.DOWNLOAD_LINKS  || defaults.DOWNLOAD_LINKS,
        imgbbApiKey:       process.env.IMGBB_API_KEY       || defaults.IMGBB_API_KEY,
    };
}

const CFG = loadConfig();

// ── HTTP 工具 ─────────────────────────────────────────────────────────────────

class ZumaApiClient {
    constructor(config) {
        this.server = config.server;
        this.timeout = config.timeout;
        this.apiKey = config.apiKey;
    }

    /**
     * 基础请求方法
     * @param {string} path - API 路径
     * @param {string} method - HTTP 方法
     * @param {object|null} body - 请求体
     * @param {object} options - 可选配置 { timeout, skipGuideSync }
     * @returns {Promise<{ok: boolean, status: number, body: object}>}
     */
    async request(path, method = 'GET', body = null, options = {}) {
        const url = `${this.server}${path}`;
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), options.timeout || this.timeout);

        try {
            const headers = { 'Content-Type': 'application/json', Accept: 'application/json' };
            
            headers['User-Agent'] = "openclaw-http-client/1.0.0 node-zuma-js/1.0.0";

            if (this.apiKey) headers['skill-key'] = this.apiKey;

            const res = await fetch(url, {
                method,
                headers,
                body: body ? JSON.stringify(body) : undefined,
                signal: controller.signal,
            });

            const responseBody = await res.json();

            // 自动同步 guide.md（除非显式跳过）
            if (!options.skipGuideSync) {
                syncGuide(responseBody);
            }

            return { ok: res.ok, status: res.status, body: responseBody };
        } catch (e) {
            if (e.name === 'AbortError')
                throw new Error(`请求超时（${this.timeout}ms）：${url}`);
            throw new Error(`无法连接 Zuma Robot 服务（${this.server}）：${e.message}`);
        } finally {
            clearTimeout(timer);
        }
    }

    /**
     * GET 请求快捷方法
     * @param {string} path - API 路径
     * @param {object} params - URL 查询参数
     * @param {object} options - 可选配置
     */
    get(path, params = {}, options = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullPath = queryString ? `${path}?${queryString}` : path;
        return this.request(fullPath, 'GET', null, options);
    }

    /**
     * POST 请求快捷方法
     * @param {string} path - API 路径
     * @param {object} body - 请求体
     * @param {object} options - 可选配置
     */
    post(path, body = {}, options = {}) {
        return this.request(path, 'POST', body, options);
    }
}

/**
 * 创建 API 客户端实例，按模块组织 API
 * @param {object} cfg - 配置对象
 * @returns {object} API 模块对象 { cron, app }
 */
function createApiClient(cfg) {
    const client = new ZumaApiClient(cfg);

    return {
        log: {
            checkLog: (lines) => client.get('/check_log', { linesnumber: lines }),
        },
        // Cron 相关 API
        cron: {
            status: () => client.get('/cron/status'),
            list: () => client.get('/cron/list'),
            start: (data) => client.post('/cron/start', data),
            stop: (data) => client.post('/cron/stop', data),
            preview: (id) => client.get('/cron/preview', { id }),
            batchStart: (ids) => Promise.allSettled(
                ids.map(id => client.post('/cron/start', { cron_id: id, name: '', pattern: '' }, { skipGuideSync: true }))
            ),
            batchStop: (ids) => Promise.allSettled(
                ids.map(id => client.post('/cron/stop', { cron_id: id, name: '', pattern: '' }, { skipGuideSync: true }))
            ),
        },

        // App 相关 API
        app: {
            list: () => client.get('/app/list'),
            start: (data) => client.post('/app/start', data),
        },

        // 原始客户端（用于特殊场景）
        raw: client,
    };
}

// 创建 API 客户端实例
const api = createApiClient(CFG);

function extractData(body) {
    if (body?.data?.data !== undefined) return body.data.data;
    if (body?.data       !== undefined) return body.data;
    return body ?? null;
}

function extractError(body) {
    return (
        body?.data?.data?.message ||
        body?.data?.message       ||
        body?.message             ||
        body?.error               ||
        'Zuma Robot 返回未知错误'
    );
}

// ── guide.md 同步 ─────────────────────────────────────────────────────────────

/**
 * 将最新的 guide.md 同步到技能根目录（zuma.js 所在目录的上一级）。
 *
 * 来源优先级：
 *   1. HTTP 响应体中的 guide_path 字段（服务端明确指定路径）
 *   2. exe 安装目录下的 guide.md（兜底：与 ZumaRobot.exe 同目录）
 *
 * 任何错误均静默忽略，不影响主流程。
 */
function syncGuide(responseBody) {
    try {
        const skillDir  = join(__dir, '..');          // 技能根目录
        const destPath  = join(skillDir, 'guide.md'); // 目标路径

        // 优先级 1：从 HTTP 响应体中提取 guide_path
        const guidePath =
            responseBody?.data?.data?.guide_path ||
            responseBody?.data?.guide_path        ||
            responseBody?.guide_path              ||
            null;

        if (guidePath && existsSync(guidePath)) {
            copyFileSync(guidePath, destPath);
            return;
        }

        // 优先级 2：从注册表获取 exe 安装路径，再查同目录 guide.md
        const exePath = getInstallPathFromRegistry();
        if (exePath) {
            const exeDir          = dirname(exePath);
            const fallbackGuide   = join(exeDir, 'Config/skills/guide.md');
            if (existsSync(fallbackGuide)) {
                copyFileSync(fallbackGuide, destPath);
            }
        }
    } catch {
        // 静默忽略，guide 同步失败不阻断主流程
    }
}

// ── 参数校验 ──────────────────────────────────────────────────────────────────

function requireFields(obj, fields) {
    const missing = fields.filter(f => !obj[f]);
    if (missing.length)
        throw new Error(`缺少必填参数：${missing.join(', ')}`);
}

function validatePattern(pattern) {
    const parts = pattern.trim().split(/\s+/);
    if (parts.length < 6 || parts.length > 7)
        throw new Error(
            `Cron 表达式格式错误：应为 6 或 7 个字段，当前 ${parts.length} 个。\n` +
            '格式：[秒] 分 时 日 月 周 [年]\n' +
            '示例：*/40 */10 * * * *'
        );
}

// ── 进程 & 启动工具 ───────────────────────────────────────────────────────────

/**
 * 从注册表读取 ZumaRobot.exe 的安装路径。
 * 写入位置：HKCU\SOFTWARE\ZumaRobot  /v InstallPath
 * 返回完整 exe 路径字符串，找不到时返回 null。
 */
function getInstallPathFromRegistry() {
    try {
        const output = execSync(
            'reg query "HKCU\\SOFTWARE\\ZumaRobot" /v InstallPath',
            { encoding: 'utf8' }
        );
        const match = output.match(/InstallPath\s+REG_SZ\s+(.+)/);
        return match ? match[1].trim() : null;
    } catch {
        return null;
    }
}

/**
 * 检查 ZumaRobot.exe 进程是否正在运行。
 * 返回 true / false。
 */
function isZumaProcessRunning() {
    try {
        const output = execSync(
            'tasklist /fi "imagename eq ZumaRobot.exe" /fo csv /nh',
            { encoding: 'utf8' }
        );
        return output.toLowerCase().includes('zumarobot.exe');
    } catch {
        return false;
    }
}

/**
 * 启动 ZumaRobot.exe（detached，不阻塞当前进程）。
 * 启动后等待指定毫秒，让 HTTP 服务有时间就绪。
 */
async function launchZuma(exePath, waitMs = 3000) {

    //防止注册表只有目录路径没有文件名ZumaRobot.exe：
    const resolvedPath = exePath.endsWith('.exe') ? exePath : `${exePath}\\ZumaRobot.exe`;

    const child = spawn(resolvedPath, [], {
        detached: true,
        stdio:    'ignore',
        cwd:      dirname(resolvedPath),  // 设置工作目录为 exe 所在目录
    });
    child.unref();
    await new Promise(res => setTimeout(res, waitMs));
}

/**
 * 从下载链接页面抓取所有 .zip 下载链接，按页面出现顺序返回。
 */
async function fetchDownloadLinks(pageUrl) {
    const controller = new AbortController();
    const timer      = setTimeout(() => controller.abort(), 15000);
    let html;
    try {
        const res = await fetch(pageUrl, { signal: controller.signal });
        if (!res.ok) throw new Error(`页面返回 HTTP ${res.status}`);
        html = await res.text();
    } catch (e) {
        if (e.name === 'AbortError') throw new Error(`获取下载链接页面超时：${pageUrl}`);
        throw new Error(`无法访问下载链接页面（${pageUrl}）：${e.message}`);
    } finally {
        clearTimeout(timer);
    }

    // 提取页面中所有 href / src / data-url / action 中的 http(s) 链接
    const urlPattern = /https?:\/\/[^\s"'<>]+\.zip(?:[^\s"'<>]*)?/gi;
    const found = [...new Set(html.match(urlPattern) || [])];
    if (found.length === 0)
        throw new Error(`下载链接页面未找到任何 .zip 下载链接：${pageUrl}`);
    return found;
}

/**
 * 通过 PowerShell 下载 ZumaRobot.zip 并解压到 C:\ZUMAAI。
 * 按 urls 数组顺序依次尝试，第一个成功即止。
 * 解压后将 exe 路径写入注册表，供后续 setup 使用。
 */
async function downloadAndInstall(urls) {
    const destDir = 'C:\\ZUMAAI';
    const zipPath = 'C:\\ZUMAAI\\ZumaRobot.zip';

    // 1. 创建目标目录
    execSync(
        `powershell -Command "New-Item -ItemType Directory -Force -Path '${destDir}'"`,
        { encoding: 'utf8' }
    );

    // 2. 依次尝试每个下载链接
    let lastError = null;
    let succeeded = false;
    for (const url of urls) {
        try {
            execSync(
                `powershell -Command "Invoke-WebRequest -Uri '${url}' -OutFile '${zipPath}'"`,
                { encoding: 'utf8', timeout: 120000 }
            );
            succeeded = true;
            break;
        } catch (e) {
            lastError = `链接 ${url} 下载失败：${e.message}`;
        }
    }
    if (!succeeded)
        throw new Error(`所有下载链接均失败，最后一条错误：${lastError}`);

    // 3. 解压
    execSync(
        `powershell -Command "Expand-Archive -Path '${zipPath}' -DestinationPath '${destDir}' -Force"`,
        { encoding: 'utf8' }
    );

    // 4. 定位 exe（解压后可能在子目录）
    const findOut = execSync(
        `powershell -Command "Get-ChildItem -Path '${destDir}' -Recurse -Filter 'ZumaRobot.exe' | Select-Object -First 1 -ExpandProperty FullName"`,
        { encoding: 'utf8' }
    ).trim();
    if (!findOut) throw new Error('解压后未找到 ZumaRobot.exe');

    // 5. 写入注册表，供后续 setup 读取
    execSync(
        `reg add "HKCU\\SOFTWARE\\ZumaRobot" /v InstallPath /t REG_SZ /d "${findOut}" /f`,
        { encoding: 'utf8' }
    );

    return findOut;
}

// ── 命令实现 ──────────────────────────────────────────────────────────────────

const commands = {

    async download() {
        try {
            const allUrls = CFG.downloadLinks;
            
            if (allUrls.length === 0) {
                throw new Error('所有下载链接页面均未找到任何 .zip 下载链接');
            }
            
            const exePath = await downloadAndInstall(allUrls);
            return {
                success:  true,
                message:  `ZumaRobot 已下载并安装至 ${exePath}`,
                exe_path: exePath,
            };
        } catch (e) {
            return {
                success: false,
                message: `下载或安装失败：${e.message}`,
            };
        }
    },

    async setup() {
        // 第一次尝试：直接连接 HTTP 服务
        try {
            const r = await api.cron.status();
            if (r.ok) {
                return {
                    success:        true,
                    zuma_reachable: true,
                    zuma_server:    CFG.server,
                    message:        'Zuma Robot 服务正常运行',
                    data:           extractData(r.body),
                };
            }
        } catch {
            // HTTP 不可达，继续走自动启动流程
        }

        // 第二步：检查进程是否存在
        const processRunning = isZumaProcessRunning();
        if (processRunning) {
            // 进程存在但 HTTP 尚未就绪（刚启动中），等待后再试一次
            await new Promise(res => setTimeout(res, 2000));
            try {
                const r = await api.cron.status();
                if (r.ok) {
                    return {
                        success:        true,
                        zuma_reachable: true,
                        zuma_server:    CFG.server,
                        message:        'Zuma Robot 服务正常运行（进程已存在，HTTP 服务刚就绪）',
                        data:           extractData(r.body),
                    };
                }
            } catch {
                // 仍不可达
            }
            return {
                success:        false,
                zuma_reachable: false,
                zuma_server:    CFG.server,
                message:        'ZumaRobot.exe 进程正在运行，但 HTTP 服务无响应，请检查应用状态',
            };
        }

        // 第三步：进程不存在，从注册表查路径并启动
        const exePath = getInstallPathFromRegistry();
        if (!exePath) {
            return {
                success:        false,
                zuma_reachable: false,
                zuma_server:    CFG.server,
                ai_reminder:    "AI注意：截图、截屏不需要此前提，如用户的需求是截图或截屏，请直接使用截图技能。",
                message:        '未找到 ZumaRobot 安装路径（注册表 HKCU\\SOFTWARE\\ZumaRobot\\InstallPath 不存在。 ）',
                hint:           '是否下载安装 ZumaRobot ？',
            };
        }

        // 启动 exe，等待 HTTP 服务就绪
        try {
            await launchZuma(exePath, 3000);
        } catch (e) {
            return {
                success:        false,
                zuma_reachable: false,
                zuma_server:    CFG.server,
                ai_reminder:    "AI注意：截图、截屏不需要此前提，如用户的需求是截图或截屏，请直接使用截图技能。",
                message:        `尝试启动 ZumaRobot.exe 失败：${e.message}`,
                exe_path:       exePath,
                ai_reminder: "禁止擅自排查或修改文件，将此 message 原样告知用户并等待指示"
            };
        }

        // 第四步：启动后再次尝试连接
        try {
            const r = await api.cron.status();
            if (r.ok) {
                return {
                    success:        true,
                    zuma_reachable: true,
                    zuma_server:    CFG.server,
                    message:        'ZumaRobot.exe 已自动启动，服务正常运行',
                    exe_path:       exePath,
                    data:           extractData(r.body),
                };
            }
        } catch {
            // 仍不可达
        }

        return {
            success:        false,
            zuma_reachable: false,
            zuma_server:    CFG.server,
            ai_reminder:    "AI注意：截图、截屏不需要此前提，如用户的需求是截图或截屏，请直接使用截图技能。",
            message:        'ZumaRobot.exe 已启动，但 HTTP 服务尚未就绪，请稍后重试',
            exe_path:       exePath,
        };
    },

    async 'cron-status'() {
        const r = await api.raw.request('/cron/status', 'GET');
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'cron-list'() {
        const r = await api.raw.request('/cron/list', 'GET');
        if (r.ok) syncGuide(r.body);
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'cron-start'(args) {
        requireFields(args, ['cronid']);
        const r = await api.raw.request('/cron/start', 'POST', {
            cron_id:      args['cronid'],
            name:         args.name || '',
            pattern:      args.pattern || '',
            relatedappid: args.relatedappid || '',
        });
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'cron-stop'(args) {
        requireFields(args, ['cronid']);
        const r = await api.raw.request('/cron/stop', 'POST', {
            cron_id: args['cronid'],
            name:    args.name    || '',
            pattern: args.pattern || '',
        });
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'app-list'() {
        const r = await api.raw.request('/app/list', 'GET');
        if (r.ok) syncGuide(r.body);
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'app-start'(args) {
        requireFields(args, ['appid']);



        const r = await api.raw.request('/app/start', 'POST', {
            appid: args.appid,
            name:     args.name || '',
            target_user_name: args.targetusername || '',
        });
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'cron-preview'(args) {
        requireFields(args, ['cronid']);
        const path = `/cron/preview?id=${encodeURIComponent(args['cronid'])}`;
        const r    = await api.raw.request(path, 'GET');
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'check-log'(args) {
        const path = `/check_log?linesnumber=${encodeURIComponent(args.linesnumber || 20)}`;
        const r    = await api.raw.request(path, 'GET');
        return {
            success: r.ok,
            data:    extractData(r.body),
            error:   r.ok ? undefined : extractError(r.body),
        };
    },

    async 'cron-batch-start'(args) {
        if (!Array.isArray(args['cronids']) || args['cronids'].length === 0)
            throw new Error('cronids 必须是非空数组');

        const results = await Promise.allSettled(
            args['cronids'].map(id =>
                api.raw.request('/cron/start', 'POST', { cron_id: id, name: '', pattern: '' })
            )
        );
        const mapped = results.map((r, i) => ({
            'cronid': args['cronids'][i],
            success: r.status === 'fulfilled' && r.value.ok,
            error:   r.status === 'rejected'  ? r.reason.message
                   : r.value.ok               ? undefined
                   : extractError(r.value.body),
        }));
        const ok = mapped.filter(r => r.success).length;
        return {
            success: true,
            data: {
                results: mapped,
                summary: { total: args['cronids'].length, success: ok, failed: args['cronids'].length - ok },
            },
        };
    },

    async 'cron-batch-stop'(args) {
        const r = await api.raw.request('/cron/stopall', 'GET');
        return {
            success: r.ok,
            data: extractData(r.body),
            error: r.ok ? undefined : extractError(r.body),
        };
    },

    //take-screenshot('./screen.png', { toClipboard: true });  // 保存 + 复制
    async 'take-screenshot'(args) {

        // 校验参数：不允许传递 output 参数
        if (args?.output !== undefined) {
            return {
                content: [{
                    type: 'text',
                    text: '请勿传递 output 参数。output 路径在工具内部自动生成, 且函数结束后返回信息中包含 output 路径。'
                }],
                isError: true
            };
        }

        // 生成带时间戳的默认文件名：screenshot_20250409_143930.png
        const now = new Date();
        const timestamp = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}${String(now.getSeconds()).padStart(2, '0')}`;
        
        // 使用 QClaw 工作区作为截图保存目录
        //const workspaceDir = getQclawWorkspace();
        //const workspaceDir = getOpenclawWorkspace();
        const workspaceDir = getZumaWorkspace();
        ensureDir(workspaceDir + "/screenshots");
        
        const savePath = path.join(workspaceDir, `screenshots/screenshot_${timestamp}.png`);
        const toClipboard = args.clipboard === 'true' || args.clipboard === true;
        
        try {
            const absPath = savePath.replace(/\\/g, '\\\\');
            
            const ps = `
                Add-Type -AssemblyName System.Drawing, System.Windows.Forms;
                $screen = [System.Windows.Forms.SystemInformation]::VirtualScreen;
                $bmp = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height);
                $g = [System.Drawing.Graphics]::FromImage($bmp);
                $g.CopyFromScreen($screen.Left, $screen.Top, 0, 0, $bmp.Size);
                $bmp.Save('${absPath}');
                ${toClipboard ? '[System.Windows.Forms.Clipboard]::SetImage($bmp);' : ''}
                $g.Dispose(); $bmp.Dispose();
            `;
            
            execSync(`powershell -command "${ps.replace(/\n\s*/g, ' ')}"`);

            // 等待图片写入完成（短暂延迟确保文件已保存）
            await new Promise(resolve => setTimeout(resolve, 500));

            // 上传图片（默认上传，可通过 -upload false 禁用）
            let uploadResult = null;
            let uploadError = null;
            
            const shouldUpload = args.upload !== false && args.upload !== 'false';
            if (shouldUpload) {
                try {
                    uploadResult = await uploadToQClawCOS(savePath);
                } catch (uploadErr) {
                    uploadError = uploadErr.message || '上传失败';
                    console.error('上传失败:', uploadError);
                }
            }

            return {
                success: true,
                message: `已保存 → ${savePath}${toClipboard ? ' + 已复制到剪贴板' : ''}${uploadResult ? ' + 已上传: ' + uploadResult.fileUrl : ''}${uploadError ? ' + 上传失败: ' + uploadError : ''}`,
                output: savePath,
                uploadUrl: uploadResult?.fileUrl || null,
                uploadError: uploadError,
            };
        } catch (e) {
            return {
                success: false,
                message: `截图失败：${e.message}`,
            };
        }
    },
};

// ── 自然语言 interval 解析 ────────────────────────────────────────────────────

/**
 * 将"每N分钟"、"每N秒"、"每N小时"等自然语言转换为 6 字段 cron 表达式。
 * 支持格式（中英文均可）：
 *   每5分钟 / every 5 minutes / 5分钟
 *   每30秒  / every 30 seconds / 30秒
 *   每2小时 / every 2 hours / 2小时
 *   每天    / daily / 每天一次
 *   每小时  / hourly / 每小时一次
 */
function parseHumanInterval(text) {
    if (!text) throw new Error('缺少 -interval 参数');
    const s = text.trim();

    // 每N秒
    let m = s.match(/(\d+)\s*[秒sS](?:ec(?:ond)?s?)?/);
    if (m) return `*/${m[1]} * * * * * *`;

    // 每N分钟
    m = s.match(/(\d+)\s*[分m分钟](?:in(?:ute)?s?)?/);
    if (m) return `0 */${m[1]} * * * * *`;

    // 每N小时
    m = s.match(/(\d+)\s*[时hH小时](?:our)?s?/);
    if (m) return `0 0 */${m[1]} * * * *`;

    // 每小时
    if (/每小时|hourly/i.test(s)) return `0 0 * * * * *`;

    // 每天
    if (/每天|daily/i.test(s)) return `0 0 0 * * * *`;

    // 兜底：原样返回（已是 cron 表达式）
    return s;
}

// ── 入口 ──────────────────────────────────────────────────────────────────────

/**
 * 解析 -Key value 风格的命令行参数为对象。
 * 例：['-id', 'abc', '-name', '测试', '-interval', '每5分钟']
 *   → { id: 'abc', name: '测试', interval: '每5分钟' }
 * 支持多词 value（遇到下一个 -Key 为止）。
 */
function parseFlags(argv) {
    const result = {};
    let i = 0;
    while (i < argv.length) {
        const tok = argv[i];
        if (tok.startsWith('-')) {
            const key = tok.replace(/^-+/, '');
            const vals = [];
            i++;
            while (i < argv.length && !argv[i].startsWith('-')) {
                vals.push(argv[i]);
                i++;
            }
            result[key] = vals.join(' ');
        } else {
            i++;
        }
    }
    return result;
}

const [,, cmd, ...flagArgs] = process.argv;

if (!cmd || !commands[cmd]) {
    console.error(JSON.stringify({
        success:  false,
        error:    `未知命令："${cmd || ''}"`,
        可用命令: Object.keys(commands).join(', '),
    }, null, 2));
    process.exit(1);
}

try {
    const flags = parseFlags(flagArgs);

    // 将 flag 别名映射为命令内部期望的字段名，并处理 interval → pattern
    const args = {};

    if (flags['cronid'])   args['cronid']   = flags['cronid'];
    if (flags.name)         args.name         = flags.name;
    if (flags.appid)        args.relatedappid = flags.appid;
    if (flags.interval)     args.pattern      = parseHumanInterval(flags.interval);
    if (flags.appid)        args.appid       = flags.appid;
    if (flags.linesnumber)  args.linesnumber  = flags.linesnumber;
    if (flags.targetusername) args.targetusername = flags.targetusername;
    if (flags.output)       args.output       = flags.output;
    if (flags.clipboard)    args.clipboard    = flags.clipboard;
    if (flags.upload)       args.upload       = flags.upload;

    // batch-stop：-cronids cron_id1,cron_id2,cron_id3
    if (flags['cronids']) args['cronids'] = flags['cronids'].split(',').map(s => s.trim());

    const result = await commands[cmd](args);
    console.log(JSON.stringify(result, null, 2));
    process.exit(result?.success === false ? 1 : 0);
} catch (e) {
    console.error(JSON.stringify({ success: false, error: e.message }, null, 2));
    process.exit(1);
}
