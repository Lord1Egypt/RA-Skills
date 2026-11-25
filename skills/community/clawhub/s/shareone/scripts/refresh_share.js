#!/usr/bin/env node

// 强制刷新一个 remote-url auto-follow 分享的源内容（owner-only，需凭据）。
// 用于源站（GitHub 等）刚 push 后立即拉取最新内容——remote 页面的刷新是懒的、
// 只在打开渲染页时触发且有节流，`download`/`/file` 只服务缓存，不会 refetch。
// 本命令调用 POST /api/v1/pages/<ref>/refresh，绕过节流立即拉取。
// 接受完整链接、/s/<ref> 路径、裸 share_id 或 slug。

const {
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    extractShareRef,
    printShareOneScriptError,
    requestShareOneJson,
    resolveDirectApiKey,
} = require('./shareone_client');

const {commandLine} = require('./cli_args');
const {values, positional: ref} = commandLine({
    summary: 'refetch an owner-managed remote-bound share now. A pinned GitLab/GitHub commit remains pinned; use upload_page to select another source commit.',
    result: 'JSON with remote_fetch_status, accepted revision/digest and source error. error/busy exits nonzero; updated/not_modified confirms the fetch. Static shares return NOT_REMOTE_BOUND.',
    positional: 'share_link_or_ref', options: {'--api-key': true},
});
const apiKey = values['api-key'];

(async () => {
    const shareRef = encodeURIComponent(extractShareRef(ref));
    const credentialMode = await detectCredentialMode();
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY && apiKey) {
        emitError('ERROR:SUDOWORK_MANAGED_KEY', ['Sudowork 模式下不要传 --api-key；请通过本 skill 的 save_api_key.js 或 create_guest_key.js 设置 ShareOne API Key。'].join('\n'));
    }
    if (credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY && !resolveDirectApiKey(apiKey)) {
        emitError('ERROR:KEY_NOT_FOUND');
    }

    const result = await requestShareOneJson(`/api/v1/pages/${shareRef}/refresh`, {
        method: 'POST',
        apiKey,
    });
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    if (result.remote_fetch_status === 'error' || result.remote_fetch_status === 'busy' || result.remote_last_error) {
        emitError(result.remote_error_code || (result.remote_fetch_status === 'busy' ? 'REMOTE_SOURCE_BUSY' : 'REMOTE_SOURCE_UNAVAILABLE'),
            result.remote_last_error || 'The source was not refreshed; the accepted cache remains unchanged.');
    }
    console.error(`SHARE_REFRESHED:${extractShareRef(ref)}`);
})().catch((error) => {
    process.exit(printShareOneScriptError(error));
});
