#!/usr/bin/env node
/**
 * Vibbit OpenAPI CLI client.
 *
 * Wraps POST /openapi/v1/tasks + GET /openapi/v1/tasks/{taskId} with task-specific
 * subcommands. All wire JSON is snake_case. Sync tasks return the result directly
 * from submit; async tasks are polled until COMPLETED / FAILED.
 *
 * Env vars:
 *   VIBBIT_BASE_URL  e.g. https://app.vibbit.ai  (no trailing slash)
 *   VIBBIT_API_KEY   bearer token
 *
 * Usage:
 *   vibbit.js gen_image --prompt "a cute cat" [--ref-url URL]
 *   vibbit.js parse_url --url https://v.douyin.com/xxxxx
 *   vibbit.js breakdown --video-url URL --sub-tasks asr,hot [--prompt P] [--zone Z]
 *   vibbit.js list_digital_humans
 *   vibbit.js oral_broadcast --message "..." --digital-human-id 123 \
 *       [--material-url URL ...]
 *
 * Output: a JSON object on stdout with {"result": ...} (and "task_id" for async).
 * Exit code 0 on success, non-zero on failure.
 *
 * Pure Node stdlib — no npm install needed. Requires Node 18+ for global fetch.
 */

'use strict';

const POLL_INTERVAL_MS = 3000;
const POLL_TIMEOUT_MS = 10 * 60 * 1000; // 10 minutes
const ALLOWED_SUB_TASKS = ['asr', 'transition', 'hot', 'bgm', 'decorate', 'cut_script'];
const DEFAULT_BASE_URL = 'https://openapi.vibbit.cn';
const FILE_INFO_API = 'https://tools.vibbit.ai/api/file-info';

const path = require('path');

const MIME = {
    jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', gif: 'image/gif',
    webp: 'image/webp', bmp: 'image/bmp', svg: 'image/svg+xml', heic: 'image/heic',
    mp4: 'video/mp4', mov: 'video/quicktime', webm: 'video/webm',
    mkv: 'video/x-matroska', avi: 'video/x-msvideo', m4v: 'video/x-m4v',
    mp3: 'audio/mpeg', wav: 'audio/wav', aac: 'audio/aac', m4a: 'audio/mp4',
    flac: 'audio/flac', ogg: 'audio/ogg',
};

const IMAGE_EXTS = new Set(['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']);
const MP4_EXTS = new Set(['mp4', 'mov', 'm4v']);

function parseImageSize(buf) {
    // PNG: 8-byte sig, IHDR chunk at offset 16 (4B width, 4B height)
    if (buf.length >= 24 && buf[0] === 0x89 && buf[1] === 0x50) {
        return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
    }
    // GIF: 'GIF8', width/height at offset 6 as LE 16-bit
    if (buf.length >= 10 && buf[0] === 0x47 && buf[1] === 0x49 && buf[2] === 0x46) {
        return { width: buf.readUInt16LE(6), height: buf.readUInt16LE(8) };
    }
    // BMP: 'BM', width/height at offset 18 as LE 32-bit
    if (buf.length >= 26 && buf[0] === 0x42 && buf[1] === 0x4D) {
        return { width: buf.readInt32LE(18), height: Math.abs(buf.readInt32LE(22)) };
    }
    // WebP: 'RIFF....WEBP', VP8 /VP8L/VP8X
    if (buf.length >= 30 && buf.slice(0, 4).toString() === 'RIFF' && buf.slice(8, 12).toString() === 'WEBP') {
        const chunk = buf.slice(12, 16).toString();
        if (chunk === 'VP8 ' && buf.length >= 30) {
            return { width: buf.readUInt16LE(26) & 0x3FFF, height: buf.readUInt16LE(28) & 0x3FFF };
        }
        if (chunk === 'VP8L' && buf.length >= 25) {
            const bits = buf.readUInt32LE(21);
            return { width: (bits & 0x3FFF) + 1, height: ((bits >> 14) & 0x3FFF) + 1 };
        }
        if (chunk === 'VP8X' && buf.length >= 30) {
            const w = (buf[24] | (buf[25] << 8) | (buf[26] << 16)) + 1;
            const h = (buf[27] | (buf[28] << 8) | (buf[29] << 16)) + 1;
            return { width: w, height: h };
        }
    }
    // JPEG: scan for SOF0/SOF2 markers
    if (buf.length >= 2 && buf[0] === 0xFF && buf[1] === 0xD8) {
        let off = 2;
        while (off + 9 < buf.length) {
            if (buf[off] !== 0xFF) break;
            const marker = buf[off + 1];
            if (marker === 0xC0 || marker === 0xC2) {
                return { width: buf.readUInt16BE(off + 7), height: buf.readUInt16BE(off + 5) };
            }
            const segLen = buf.readUInt16BE(off + 2);
            off += 2 + segLen;
        }
    }
    return null;
}

/**
 * Parse MP4/MOV box structure to extract duration and dimensions.
 * Walks top-level boxes → finds 'moov' → scans children for 'mvhd' (duration)
 * and 'trak' → 'tkhd' (width/height of the first video track).
 */
function parseMp4Info(buf) {
    const result = { duration: null, width: null, height: null };
    const moov = findBox(buf, 0, buf.length, 'moov');
    if (!moov) return result;

    // mvhd: version(1) + flags(3) + created(4/8) + modified(4/8) + timescale(4) + duration(4/8)
    const mvhd = findBox(buf, moov.dataStart, moov.end, 'mvhd');
    if (mvhd) {
        const ver = buf[mvhd.dataStart];
        if (ver === 0) {
            const timescale = buf.readUInt32BE(mvhd.dataStart + 12);
            const dur = buf.readUInt32BE(mvhd.dataStart + 16);
            if (timescale > 0) result.duration = dur / timescale;
        } else {
            // version 1: 8-byte fields
            const timescale = buf.readUInt32BE(mvhd.dataStart + 20);
            // duration is 8 bytes at offset 24; read high+low as Number (safe for < 2^53)
            const durHi = buf.readUInt32BE(mvhd.dataStart + 24);
            const durLo = buf.readUInt32BE(mvhd.dataStart + 28);
            const dur = durHi * 0x100000000 + durLo;
            if (timescale > 0) result.duration = dur / timescale;
        }
    }

    // Find first trak with tkhd that has non-zero width/height
    let off = moov.dataStart;
    while (off < moov.end) {
        const trak = findBox(buf, off, moov.end, 'trak');
        if (!trak) break;
        const tkhd = findBox(buf, trak.dataStart, trak.end, 'tkhd');
        if (tkhd) {
            const ver = buf[tkhd.dataStart];
            // width/height are fixed-point 16.16, last 8 bytes of tkhd
            const whOff = ver === 0 ? tkhd.dataStart + 76 : tkhd.dataStart + 88;
            if (whOff + 8 <= tkhd.end) {
                const w = buf.readUInt32BE(whOff) >> 16;
                const h = buf.readUInt32BE(whOff + 4) >> 16;
                if (w > 0 && h > 0) {
                    result.width = w;
                    result.height = h;
                    break;
                }
            }
        }
        off = trak.end;
    }
    return result;
}

/** Find a box by type within [start, end). Returns { dataStart, end } or null. */
function findBox(buf, start, end, type) {
    let off = start;
    while (off + 8 <= end) {
        let size = buf.readUInt32BE(off);
        const boxType = buf.slice(off + 4, off + 8).toString('latin1');
        let headerSize = 8;
        if (size === 1 && off + 16 <= end) {
            // 64-bit extended size
            const hi = buf.readUInt32BE(off + 8);
            const lo = buf.readUInt32BE(off + 12);
            size = hi * 0x100000000 + lo;
            headerSize = 16;
        }
        if (size < 8) break; // invalid
        const boxEnd = off + size;
        if (boxType === type) {
            return { dataStart: off + headerSize, end: Math.min(boxEnd, end) };
        }
        off = boxEnd;
    }
    return null;
}

async function buildFileInfoViaDownload(url, fileName) {
    const resp = await fetch(url, { redirect: 'follow' });
    if (!resp.ok) throw new Error(`Download failed: HTTP ${resp.status}`);
    const buf = Buffer.from(await resp.arrayBuffer());
    const clean = url.split('?')[0].split('#')[0];
    const ext = (path.extname(clean).slice(1) || '').toLowerCase() || null;
    const ct = (resp.headers.get('content-type') || '').split(';')[0].trim();

    let width = null, height = null, duration = null;
    if (ext && IMAGE_EXTS.has(ext)) {
        const dims = parseImageSize(buf);
        if (dims) { width = dims.width; height = dims.height; }
    } else if (ext && MP4_EXTS.has(ext)) {
        const info = parseMp4Info(buf);
        width = info.width;
        height = info.height;
        duration = info.duration;
    }

    return {
        url,
        file_name: fileName || path.basename(clean),
        file_size: buf.length,
        file_type: ext,
        mime_type: (ext && MIME[ext]) || ct || null,
        upload_time: String(Date.now()),
        duration,
        width,
        height,
    };
}

async function buildFileInfoViaApi(url, fileName) {
    const body = { url };
    if (fileName) body.file_name = fileName;
    const resp = await fetch(FILE_INFO_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
    const text = await resp.text();
    if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${text.slice(0, 500)}`);
    const envelope = JSON.parse(text);
    if (envelope.code !== 200 || !envelope.data) {
        throw new Error(envelope.message || text.slice(0, 500));
    }
    return envelope.data;
}

function buildFileInfoStub(url, fileName) {
    const clean = url.split('?')[0].split('#')[0];
    const ext = (path.extname(clean).slice(1) || '').toLowerCase() || null;
    return {
        url,
        file_name: fileName || path.basename(clean),
        file_size: 0,
        file_type: ext,
        mime_type: (ext && MIME[ext]) || null,
        upload_time: String(Date.now()),
        duration: null,
        width: null,
        height: null,
    };
}

async function buildFileInfo(url, fileName) {
    try {
        return await buildFileInfoViaApi(url, fileName);
    } catch (e) {
        process.stderr.write(`[vibbit] file-info API failed (${e.message}), falling back to download...\n`);
        try {
            return await buildFileInfoViaDownload(url, fileName);
        } catch (e2) {
            process.stderr.write(`[vibbit] download failed (${e2.message}), using stub...\n`);
            return buildFileInfoStub(url, fileName);
        }
    }
}

function die(msg) {
    process.stdout.write(JSON.stringify({ error: msg }) + '\n');
    process.exit(1);
}

function getBaseUrl() {
    const v = process.env.VIBBIT_BASE_URL;
    return (v && v.trim() ? v : DEFAULT_BASE_URL).replace(/\/+$/, '');
}

function getApiKey() {
    const v = process.env.VIBBIT_API_KEY;
    if (!v) die('Missing environment variable VIBBIT_API_KEY. Export it before running.');
    return v;
}

async function http(method, path, body) {
    const base = getBaseUrl();
    const key = getApiKey();
    const url = `${base}${path}`;
    let resp;
    try {
        resp = await fetch(url, {
            method,
            headers: {
                'Authorization': `Bearer ${key}`,
                'Content-Type': 'application/json',
            },
            body: body === undefined || body === null ? undefined : JSON.stringify(body),
        });
    } catch (e) {
        die(`Network error calling ${url}: ${e.message}`);
    }
    const text = await resp.text();
    if (!resp.ok) {
        die(`HTTP ${resp.status} ${resp.statusText}: ${text.slice(0, 500)}`);
    }
    let envelope;
    try {
        envelope = JSON.parse(text);
    } catch {
        die(`Non-JSON response from ${url}: ${text.slice(0, 500)}`);
    }
    const code = envelope.code;
    if (code !== 0 && code !== 200 && envelope.data == null) {
        die(`API error: ${envelope.message} (code=${code})`);
    }
    return envelope.data || {};
}

/** task_result.result is a JSON-encoded string; decode it if possible. */
function parseResult(taskResult) {
    if (!taskResult) return null;
    const raw = taskResult.result;
    if (raw == null) return null;
    if (typeof raw !== 'string') return raw;
    try {
        return JSON.parse(raw);
    } catch {
        return raw; // plain string (e.g. chat URL)
    }
}

async function submit(taskType, inputObj) {
    return http('POST', '/openapi/v1/tasks', {
        task_type: taskType,
        input_info: {
            input: JSON.stringify(inputObj || {}),
        },
    });
}

async function getTask(taskId) {
    return http('GET', `/openapi/v1/tasks/${encodeURIComponent(taskId)}`, null);
}

async function runSync(taskType, inputObj) {
    const data = await submit(taskType, inputObj);
    const result = parseResult(data.task_result);
    process.stdout.write(JSON.stringify({ result }, null, 2) + '\n');
}

async function runAsync(taskType, inputObj) {
    const data = await submit(taskType, inputObj);
    const taskId = data.task_id;
    if (!taskId) die(`Submit succeeded but no task_id returned: ${JSON.stringify(data)}`);
    const deadline = Date.now() + POLL_TIMEOUT_MS;
    let lastStatus = null;
    while (Date.now() < deadline) {
        const got = await getTask(taskId);
        const status = got.status;
        if (status !== lastStatus) {
            process.stderr.write(`[vibbit] task_id=${taskId} status=${status}\n`);
            lastStatus = status;
        }
        if (status === 'COMPLETED') {
            const result = parseResult(got.task_result);
            process.stdout.write(JSON.stringify({ task_id: taskId, result }, null, 2) + '\n');
            return;
        }
        if (status === 'FAILED') {
            die(`Task ${taskId} failed: ${JSON.stringify(got)}`);
        }
        await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    }
    die(`Task ${taskId} did not complete within ${POLL_TIMEOUT_MS / 1000}s (last status=${lastStatus})`);
}

// ---------- minimal arg parser ----------

function parseArgs(argv) {
    // argv = subcommand + flags. Supports --flag value and repeatable --flag.
    const [cmd, ...rest] = argv;
    const args = { _: cmd };
    for (let i = 0; i < rest.length; i++) {
        const token = rest[i];
        if (!token.startsWith('--')) die(`Unexpected positional arg: ${token}`);
        const key = token.slice(2);
        const next = rest[i + 1];
        if (next === undefined || next.startsWith('--')) {
            args[key] = true; // boolean flag (none currently used)
        } else {
            if (args[key] === undefined) {
                args[key] = next;
            } else if (Array.isArray(args[key])) {
                args[key].push(next);
            } else {
                args[key] = [args[key], next];
            }
            i++;
        }
    }
    return args;
}

function requireArg(args, key) {
    const v = args[key];
    if (v === undefined || v === true) die(`--${key} is required`);
    return v;
}

function toArray(v) {
    if (v === undefined) return [];
    return Array.isArray(v) ? v : [v];
}

// ---------- subcommands ----------

const COMMANDS = {
    async gen_image(args) {
        const body = { prompt: requireArg(args, 'prompt') };
        if (args['ref-url']) body.reference_image_url = args['ref-url'];
        await runAsync('AIGC_IMAGE_GENERATION', body);
    },

    async parse_url(args) {
        await runAsync('PARSE_CONTENT_URL', { url: requireArg(args, 'url') });
    },

    async breakdown(args) {
        const videoUrl = requireArg(args, 'video-url');
        const subTasksRaw = requireArg(args, 'sub-tasks');
        const subTypes = String(subTasksRaw).split(',').map(s => s.trim()).filter(Boolean);
        const bad = subTypes.filter(s => !ALLOWED_SUB_TASKS.includes(s));
        if (bad.length) die(`Invalid sub-task type(s): ${bad}. Allowed: ${ALLOWED_SUB_TASKS.join(',')}`);
        const body = {
            video_url: videoUrl,
            sub_tasks: subTypes.map(t => ({ task_type: t })),
        };
        if (args.prompt) body.prompt = args.prompt;
        if (args.zone) body.zone = args.zone;
        await runAsync('VIDEO_BREAKDOWN', body);
    },

    async list_digital_humans(_args) {
        await runSync('QUERY_DIGITAL_HUMAN_LIST', null);
    },

    async oral_broadcast(args) {
        const body = {
            message: requireArg(args, 'message'),
            digital_human_id: requireArg(args, 'digital-human-id'),
        };
        if (args.title) body.title = args.title;
        const materials = toArray(args['material-url']);
        const materialNames = toArray(args['material-name']);
        if (materialNames.length && materialNames.length !== materials.length) {
            die(`--material-name count (${materialNames.length}) must match --material-url count (${materials.length}), in corresponding order`);
        }
        if (materials.length) {
            process.stderr.write(`[vibbit] probing ${materials.length} material file(s) via mediainfo...\n`);
            const fileInfos = [];
            for (let i = 0; i < materials.length; i++) {
                const url = materials[i];
                const fileName = materialNames[i] || undefined;
                try {
                    const info = await buildFileInfo(url, fileName);
                    fileInfos.push(info);
                } catch (e) {
                    die(`Failed to probe material ${url}: ${e && e.message ? e.message : String(e)}`);
                }
            }
            body.material_list = fileInfos;
        }
        await runSync('DIGITAL_HUMAN_ORAL_BROADCAST', body);
    },
};

function usage() {
    process.stderr.write(`Usage: vibbit.js <subcommand> [--flags]

Subcommands:
  gen_image            --prompt "..." [--ref-url URL]
  parse_url            --url URL
  breakdown            --video-url URL --sub-tasks asr,hot [--prompt P] [--zone Z]
  list_digital_humans
  oral_broadcast       --message "..." --digital-human-id N [--material-url URL ...]

Env: VIBBIT_BASE_URL, VIBBIT_API_KEY
`);
}

async function main() {
    const argv = process.argv.slice(2);
    if (argv.length === 0 || argv[0] === '-h' || argv[0] === '--help') {
        usage();
        process.exit(argv.length === 0 ? 1 : 0);
    }
    const args = parseArgs(argv);
    const cmd = args._;
    const handler = COMMANDS[cmd];
    if (!handler) {
        usage();
        die(`Unknown subcommand: ${cmd}`);
    }
    try {
        await handler(args);
    } catch (e) {
        die(`Unhandled error: ${e && e.stack ? e.stack : String(e)}`);
    }
}

main();
