#!/usr/bin/env node

// 删除一个 ShareOne 分享（软删除，链接立即失效）。owner-only，需凭据。
// 接受完整链接、/s/<ref> 路径、裸 share_id 或自定义 slug；对 HTML/文本页和
// 二进制文件（PDF/PPT/Word 等）通用——服务端 DELETE /api/v1/pages/<ref>
// 按 SharedPage 删除，与内容类型无关。

const {
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    extractShareRef,
    printShareOneScriptError,
    requestShareOneBuffer,
    resolveDirectApiKey,
} = require('./shareone_client');

function usage() {
    console.error('Usage: node delete_share.js <share_link_or_ref> [--api-key <key>]');
    console.error('  删除前请与用户确认——软删除后公开链接立即失效。');
}

const args = process.argv.slice(2);
let ref = null;
let apiKey = null;

for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--api-key') {
        apiKey = args[++i];
    } else if (!arg.startsWith('--') && !ref) {
        ref = arg;
    } else {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${arg}`);
    }
}

if (!ref) {
    usage();
    emitError('BAD_ARGS', 'Required arguments are missing.');
}

(async () => {
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey) {
        emitError('ERROR:SUDOWORK_MANAGED_KEY', ['Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。'].join('\n'));
    }
    if (credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError('ERROR:KEY_NOT_FOUND');
    }

    const shareRef = encodeURIComponent(extractShareRef(ref));
    const raw = await requestShareOneBuffer(`/api/v1/pages/${shareRef}`, { method: 'DELETE', apiKey });
    console.log(`SHARE_DELETED:${extractShareRef(ref)}`);

    // Deleting a share also kills every ShareOne link that pointed at it — those
    // may belong to other people. The user has to be told which ones died; a
    // silent cascade is how someone discovers it from a colleague's broken link.
    let cascaded = [];
    try {
        cascaded = JSON.parse(raw.text).cascaded_pointers || [];
    } catch {
        cascaded = []; // older backend answered 204 with no body
    }
    for (const pointer of cascaded) {
        console.log(`POINTER_INVALIDATED:${pointer.share_url}`);
    }
    if (cascaded.length > 0) {
        console.log(`HINT:POINTERS_INVALIDATED:${cascaded.length}`);
    }
})().catch((error) => {
    process.exit(printShareOneScriptError(error));
});
