const { emitError } = require('./shareone_client');
const fs = require('fs');
const path = require('path');
const {
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    printShareOneScriptError,
    parseShareOneResponse,
    requestShareOneBuffer,
    resolveDirectApiKey,
} = require('./shareone_client');

const ACTIVE_TASK_FILENAME = '.shareone_active_task';
const {commandLine} = require('./cli_args');
const {values, positional: filePath} = commandLine({
    summary: 'publish a local text artifact or bind a remote source on a new/original share. GitLab requires a full immutable commit and operator setup for private sources.',
    result: 'the server publication JSON (share_id/share_url/settings) or an explicit pending review record. An invalid response is an unconfirmed operation; retain the same intent key.',
    positional: 'file_path', optional: true,
    options: {'--remote-url': {value: 'url', description: 'Complete HTML/Markdown/text source, at most 16 MiB. Use instead of a local file; refresh_share refetches an existing binding.'},
        '--viewer-scope': true, '--api-key': true, '--base-url': true, '--filename': true,
        '--password': true, '--watermark': true, '--share-id': true, '--slug': true,
        '--allow-comments': true, '--allow-data': true, '--force-new': true, '--idempotency-key': true},
});
const apiKey = values['api-key'];
let filename = values.filename;
const password = values.password ?? null, watermark = values.watermark ?? null;
const shareId = values['share-id'];
const allowComments = values['allow-comments'] ?? null, allowData = values['allow-data'] ?? null;
const slug = values.slug ?? null, remoteUrl = values['remote-url'];
const viewerScope = values['viewer-scope'] ?? null, forceNew = values['force-new'];
const idempotencyKey = values['idempotency-key'];
const unbind = remoteUrl === '' && Boolean(filePath) && Boolean(shareId);
if (remoteUrl === '' && !unbind) emitError('BAD_ARGS', 'Detaching a source requires a local file and --share-id. See --help.');
if (!unbind && Boolean(filePath) === Boolean(remoteUrl)) emitError('BAD_ARGS', 'Provide exactly one local file or --remote-url. See --help.');

if (!shareId && !forceNew && fs.existsSync(ACTIVE_TASK_FILENAME)) {
    const activeShareId = fs.readFileSync(ACTIVE_TASK_FILENAME, 'utf-8').trim();
    emitError("ERROR:ACTIVE_SHARE_TASK", [`检测到进行中的评论处理任务（目标 share: ${activeShareId}）。请使用 --share-id ${activeShareId} 执行 PUT 更新原链接，不要创建新链接。只有确认要创建全新链接时，才删除 ${ACTIVE_TASK_FILENAME} 文件或追加 --force-new。`].join('\n'));
}

const HISTORY_FILENAME = '.shareone_history.json';
const absFilePath = filePath ? path.resolve(filePath) : null;

function readHistory() {
    try {
        const data = JSON.parse(fs.readFileSync(HISTORY_FILENAME, 'utf-8'));
        return data && typeof data === 'object' ? data : {};
    } catch (_) {
        return {};
    }
}

if (!shareId && !forceNew && absFilePath) {
    const previous = readHistory()[absFilePath];
    if (previous && previous.share_id && !(idempotencyKey && previous.idempotency_key === idempotencyKey)) {
        emitError("ERROR:FILE_PREVIOUSLY_PUBLISHED", [`该文件之前已发布过（share_id: ${previous.share_id}${previous.share_url ? `，链接: ${previous.share_url}` : ''}）。请使用 --share-id ${previous.share_id} 执行 PUT 更新原链接；只有确认用户要为同一文件创建全新链接时，才追加 --force-new。`].join('\n'));
    }
}

function recordHistory(parsed) {
    if (!absFilePath) return; // remote URL mode has no local file to track
    try {
        if (!parsed || !parsed.share_id) return;
        const history = readHistory();
        history[absFilePath] = { share_id: parsed.share_id, share_url: parsed.share_url,
            ...(!shareId && idempotencyKey ? {idempotency_key: idempotencyKey} : {}) };
        fs.writeFileSync(HISTORY_FILENAME, JSON.stringify(history, null, 2));
    } catch (_) {
        // History is best-effort; never fail the upload because of it.
    }
}

if (!filename && filePath) {
    filename = path.basename(filePath);
}

async function uploadPage() {
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey) {
        emitError("ERROR:SUDOWORK_MANAGED_KEY", ["Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。"].join('\n'));
    }

    if (credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError("ERROR:KEY_NOT_FOUND");
    }

    let payload;

    if (remoteUrl) {
        // Remote URL mode: server fetches content from the URL
        payload = { remote_url: remoteUrl };
        if (filename) payload.filename = filename;
    } else {
        // Local file mode: read and upload content
        const content = fs.readFileSync(filePath, "utf-8");
        payload = {
            filename: filename,
            html_content: content,
            ...(unbind ? {remote_url: ''} : {}),
        };
    }

    if (password !== null) payload.password = password;
    if (viewerScope !== null) payload.viewer_scope = viewerScope;
    if (watermark !== null) payload.watermark = watermark;
    if (slug !== null) payload.custom_slug = slug;

    if (allowComments !== null) {
        payload.allow_comments = allowComments;
    } else if (!shareId) {
        payload.allow_comments = false;
    }
    if (allowData !== null) {
        payload.allow_data = allowData;
    }

    const data = JSON.stringify(payload);
    const urlPath = shareId
        ? `/api/v1/pages/${encodeURIComponent(shareId)}`
        : '/api/v1/pages';

    const method = shareId ? 'PUT' : 'POST';

    const requestOptions = {
        method: method,
        apiKey,
        headers: {
            ...(!shareId && idempotencyKey ? {'Idempotency-Key': idempotencyKey} : {}),
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data)
        }
    };
    const res = await requestShareOneBuffer(urlPath, requestOptions, data);
    const pendingStatuses = require('./api_contract.json').publication_pending_statuses;
    const nonempty = value => typeof value === 'string' && value.trim().length > 0;
    const result = parseShareOneResponse(res, urlPath, requestOptions, value => value && !Array.isArray(value) && (
        nonempty(value.share_id) && nonempty(value.share_url) ||
        res.statusCode === 202 && pendingStatuses.includes(value.status) && nonempty(value.review_id)));
    console.log(JSON.stringify(result));
    recordHistory(result);

    // cli-steering: the instant an AI turns on page storage is the right moment
    // to surface the sensitivity choice + the data-local compute pattern — not a
    // static prompt it may never read. One line on stderr (stdout stays clean JSON).
    if (allowData === true && result.settings?.allow_data === true) {
        console.error(
            'HINT:PAGE_DATA_ENABLED:This page can store data. '
            + 'Public/shared → window.__SHAREONE__.putShared (server, cross-device); '
            + 'sensitive → window.__SHAREONE__.putPrivate (this device+browser only, never uploaded). '
            + 'Private data can still be computed on: keep the model public and run inference in the page '
            + 'so bytes never leave the device — reference: templates/client-side-inference.html'
        );
    }

    if (shareId && !remoteUrl && result.share_id) {
        await verifyUpdatedContent(shareId, payload.html_content);
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
    process.exit(printShareOneScriptError(error));
});
