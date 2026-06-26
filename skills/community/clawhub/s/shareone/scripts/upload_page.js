const fs = require('fs');
const path = require('path');
const {
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    printShareOneScriptError,
    requestShareOneBuffer,
    resolveDirectApiKey,
} = require('./shareone_client');

const ACTIVE_TASK_FILENAME = '.shareone_active_task';

const args = process.argv.slice(2);
let filePath = null;
let apiKey = null;
let filename = null;
let password = null;
let watermark = null;
let shareId = null;
let allowComments = null;
let slug = null;
let forceNew = false;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--api-key') {
        apiKey = args[++i];
    } else if (args[i] === '--base-url') {
        process.env.SHAREONE_BASE_URL = args[++i];
    } else if (args[i] === '--filename') {
        filename = args[++i];
    } else if (args[i] === '--password') {
        password = args[++i];
    } else if (args[i] === '--watermark') {
        watermark = args[++i];
    } else if (args[i] === '--share-id') {
        shareId = args[++i];
    } else if (args[i] === '--slug') {
        slug = args[++i];
    } else if (args[i] === '--allow-comments') {
        allowComments = args[++i] === 'true';
    } else if (args[i] === '--force-new') {
        forceNew = true;
    } else if (!args[i].startsWith('--')) {
        filePath = args[i];
    }
}

if (!filePath) {
    console.error("Usage: node upload_page.js <file_path> [--api-key <key>] [--base-url <url>] [--filename <name>] [--password <pwd>] [--watermark <wm>] [--share-id <id>] [--slug <slug>] [--allow-comments <true|false>] [--force-new]");
    process.exit(1);
}

if (!shareId && !forceNew && fs.existsSync(ACTIVE_TASK_FILENAME)) {
    const activeShareId = fs.readFileSync(ACTIVE_TASK_FILENAME, 'utf-8').trim();
    console.error("ERROR:ACTIVE_SHARE_TASK");
    console.error(`检测到进行中的评论处理任务（目标 share: ${activeShareId}）。请使用 --share-id ${activeShareId} 执行 PUT 更新原链接，不要创建新链接。只有确认要创建全新链接时，才删除 ${ACTIVE_TASK_FILENAME} 文件或追加 --force-new。`);
    process.exit(1);
}

const HISTORY_FILENAME = '.shareone_history.json';
const absFilePath = path.resolve(filePath);

function readHistory() {
    try {
        const data = JSON.parse(fs.readFileSync(HISTORY_FILENAME, 'utf-8'));
        return data && typeof data === 'object' ? data : {};
    } catch (_) {
        return {};
    }
}

if (!shareId && !forceNew) {
    const previous = readHistory()[absFilePath];
    if (previous && previous.share_id) {
        console.error("ERROR:FILE_PREVIOUSLY_PUBLISHED");
        console.error(`该文件之前已发布过（share_id: ${previous.share_id}${previous.share_url ? `，链接: ${previous.share_url}` : ''}）。请使用 --share-id ${previous.share_id} 执行 PUT 更新原链接；只有确认用户要为同一文件创建全新链接时，才追加 --force-new。`);
        process.exit(1);
    }
}

function recordHistory(responseText) {
    try {
        const parsed = JSON.parse(responseText);
        if (!parsed || !parsed.share_id) return;
        const history = readHistory();
        history[absFilePath] = { share_id: parsed.share_id, share_url: parsed.share_url };
        fs.writeFileSync(HISTORY_FILENAME, JSON.stringify(history, null, 2));
    } catch (_) {
        // History is best-effort; never fail the upload because of it.
    }
}

if (!filename) {
    filename = path.basename(filePath);
}

async function uploadPage() {
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey) {
        console.error("ERROR:SUDOWORK_MANAGED_KEY");
        console.error("Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。");
        process.exit(1);
    }

    if (credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        console.error("ERROR:KEY_NOT_FOUND");
        process.exit(1);
    }

    const content = fs.readFileSync(filePath, "utf-8");

    const payload = {
        filename: filename,
        html_content: content
    };

    if (password !== null) payload.password = password;
    if (watermark !== null) payload.watermark = watermark;
    if (slug !== null) payload.custom_slug = slug;

    if (allowComments !== null) {
        payload.allow_comments = allowComments;
    }

    const data = JSON.stringify(payload);
    const urlPath = shareId
        ? `/api/v1/pages/${shareId}`
        : '/api/v1/pages';

    const method = shareId ? 'PUT' : 'POST';

    const res = await requestShareOneBuffer(urlPath, {
        method: method,
        apiKey,
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data)
        }
    }, data);

    console.log(res.text);
    recordHistory(res.text);

    if (shareId) {
        await verifyUpdatedContent(shareId, content);
    }
}

async function verifyUpdatedContent(updatedShareId, expectedContent) {
    const res = await requestShareOneBuffer(`/api/v1/shares/${encodeURIComponent(updatedShareId)}/download`, {
        method: 'GET',
        apiKey,
        headers: {
            Accept: '*/*',
        },
    });

    if (res.data.toString('utf8') !== expectedContent) {
        throw new Error('UPDATE_VERIFY_FAILED: server accepted the update but source content did not match the uploaded file');
    }
}

uploadPage().catch((error) => {
    printShareOneScriptError(error);
    process.exit(1);
});
