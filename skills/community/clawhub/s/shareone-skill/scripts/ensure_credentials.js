#!/usr/bin/env node

// 凭据流程编排脚本：检查 → 保存 → 复查 → 核对 的状态机全部在此执行。
// 模型只需按输出 token 行动，并把分隔线之后的话术原样转发给用户。

const {
    printShareOneScriptError,
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    CREDENTIAL_MODE_DIRECT_FALLBACK,
    detectCredentialMode,
    getBaseUrl,
    isSudowork,
    readLocalApiKey,
    requestPublicShareOneJson,
    saveLocalApiKey,
    saveSudoworkApiKey,
} = require('./shareone_client');

const SEPARATOR = '--- 请将以下内容原样发给用户 ---';

function usage() {
    console.error('Usage: node ensure_credentials.js            # 检查凭据状态');
    console.error('       node ensure_credentials.js --key <用户提供的KEY>   # 保存用户已有的 API Key 并复查');
    console.error('       node ensure_credentials.js --create-guest        # 创建临时 API Key 并保存');
}

function modeName(credentialMode) {
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) return 'sudowork';
    if (credentialMode.mode === CREDENTIAL_MODE_DIRECT_FALLBACK) return 'sudowork_fallback';
    return 'direct';
}

function hasDirectKey() {
    return Boolean(process.env.SHAREONE_API_KEY || readLocalApiKey());
}

function isReady(credentialMode) {
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) return credentialMode.hasSudoworkKey;
    return hasDirectKey();
}

function askForKeyPrompt(credentialMode) {
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
        return [
            '我检测到当前运行在 Sudowork 中，且 Sudowork 凭证环境可用，但还没有设置 ShareOne API Key。',
            '请问您是否已经拥有 API Key？',
            '',
            '- 如果有，请直接回复您的 API Key（例如 `sk-xxx`），我会通过 Sudowork 安全保存并继续。',
            '- 如果没有，请回复“没有”或“创建”，我会自动为您创建一个临时 API Key，并保存到 Sudowork。',
        ].join('\n');
    }
    if (credentialMode.mode === CREDENTIAL_MODE_DIRECT_FALLBACK) {
        return [
            '我检测到当前运行在 Sudowork 中，但 Sudowork Auth Proxy/secrets 当前不可用，因此会暂时回退到 ShareOne 普通凭据流程。',
            '请问您是否已经拥有 API Key？',
            '',
            '- 如果有，请直接回复您的 API Key（例如 `sk-xxx`），我将保存到 ShareOne fallback 本地凭证并继续。',
            '- 如果没有，请回复“没有”或“创建”，我可以为您创建一个临时 API Key。',
        ].join('\n');
    }
    return [
        '我没有找到您的 ShareOne API Key。',
        '请问您是否已经拥有 API Key？',
        '',
        '- 如果有，请直接回复您的 API Key（例如 `sk-xxx`），我将为您保存并继续。',
        '- 如果没有，请回复“没有”或“创建”，我可以为您创建一个临时 API Key。',
    ].join('\n');
}

function printSudoworkWriteBroken() {
    emitError('SUDOWORK_WRITE_BROKEN', 'Configure service:shareone / X-API-Key in Sudowork or restore the Auth Proxy write connection.');
}

function guestKeyNotification(apiKey) {
    return [
        `已为您自动分配临时 API Key：\`${apiKey}\``,
        `绑定账号链接：${getBaseUrl()}/?key=${apiKey}`,
        '请妥善保存此 API Key。为了方便您后续管理分享的链接，请尽快打开上面的链接绑定您的永久账号。',
    ].join('\n');
}

async function saveKeyAndRecheck(apiKey) {
    let credentialMode = await detectCredentialMode({ refresh: true });

    // User explicitly provided a key via --key, so force overwrite is acceptable.
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
        let savedToSudowork = false;
        try {
            await saveSudoworkApiKey(apiKey);
            savedToSudowork = true;
        } catch (error) {
            credentialMode = await detectCredentialMode({ refresh: true });
            if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
                printSudoworkWriteBroken();
            }
            saveLocalApiKey(apiKey, { force: true });
        }

        credentialMode = await detectCredentialMode({ refresh: true });
        if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
            if (credentialMode.hasSudoworkKey) {
                console.log('READY');
                console.log(`MODE:${modeName(credentialMode)}`);
                return;
            }
            // 保存声称成功（或失败回退本地）但 secrets 列表里仍然没有：可读不可写。
            printSudoworkWriteBroken();
        }
        // 复查时 proxy 已不可用，走 fallback；key 已存本地。
        console.log('READY');
        console.log(`MODE:${modeName(credentialMode)}`);
        if (!savedToSudowork) console.log('NOTE:SUDOWORK_FALLBACK_KEY_SAVED');
        return;
    }

    saveLocalApiKey(apiKey, { force: true });
    console.log('READY');
    console.log(`MODE:${modeName(credentialMode)}`);
    if (isSudowork()) console.log('NOTE:SUDOWORK_FALLBACK_KEY_SAVED');
}

async function createGuestKey() {
    const credentialMode = await detectCredentialMode({ refresh: true });
    const result = await requestPublicShareOneJson('/api/v1/agent-guest-key', {
            method: 'POST',
            authRequired: false,
        });

    if (!result || !result.api_key) {
        emitError('INVALID_RESPONSE', 'The guest credential response contains no key.');
    }

    let fallbackSaved = false;
    if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
        try {
            await saveSudoworkApiKey(result.api_key);
        } catch (error) {
            const refreshedMode = await detectCredentialMode({ refresh: true });
            if (refreshedMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
                printSudoworkWriteBroken();
            }
            try {
                saveLocalApiKey(result.api_key);
            } catch (saveError) {
                if (saveError.code === 'EXISTING_KEY_CONFLICT') {
                    // Guest key created on server but NOT saved — existing key preserved.
                    console.log(`GUEST_KEY_CREATED_NOT_SAVED:${result.api_key}`);
                    console.log(SEPARATOR);
                    console.log(`已创建临时 API Key：\`${result.api_key}\``);
                    console.log(`但您已有一个不同的 API Key（${saveError.existingKeyHint}），为避免覆盖，新 key 未保存。`);
                    console.log('如果您想为协作者创建 key，请把上面的 key 发给对方。');
                    console.log('如果您想替换当前 key，请使用 --key <新key> 显式替换。');
                    return;
                }
                throw saveError;
            }
            fallbackSaved = true;
        }
    } else {
        try {
            saveLocalApiKey(result.api_key);
        } catch (saveError) {
            if (saveError.code === 'EXISTING_KEY_CONFLICT') {
                console.log(`GUEST_KEY_CREATED_NOT_SAVED:${result.api_key}`);
                console.log(SEPARATOR);
                console.log(`已创建临时 API Key：\`${result.api_key}\``);
                console.log(`但您已有一个不同的 API Key（${saveError.existingKeyHint}），为避免覆盖，新 key 未保存。`);
                console.log('如果您想为协作者创建 key，请把上面的 key 发给对方。');
                console.log('如果您想替换当前 key，请使用 --key <新key> 显式替换。');
                return;
            }
            throw saveError;
        }
        fallbackSaved = isSudowork();
    }

    console.log(`GUEST_KEY_CREATED:${result.api_key}`);
    if (fallbackSaved) console.log('NOTE:SUDOWORK_FALLBACK_KEY_SAVED');
    console.log(SEPARATOR);
    console.log(guestKeyNotification(result.api_key));
    if (fallbackSaved) {
        console.log('');
        console.log('另外说明：Sudowork Auth Proxy/secrets 当前不可用或保存失败，该 API Key 已暂时保存到 ShareOne skill 安装目录下的本地 fallback 凭证（`.shareone_credentials`），不是 Sudowork Secret Store。');
    }
}

(async () => {
    const args = process.argv.slice(2);

    if (args[0] === '--key') {
        const apiKey = args[1];
        if (!apiKey) {
            emitError('ERROR:MISSING_VALUE:--key');
        }
        await saveKeyAndRecheck(apiKey);
        return;
    }

    if (args[0] === '--create-guest') {
        await createGuestKey();
        return;
    }

    if (args.length > 0) {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${args[0]}`);
    }

    const credentialMode = await detectCredentialMode({ refresh: true });
    if (isReady(credentialMode)) {
        console.log('READY');
        console.log(`MODE:${modeName(credentialMode)}`);
        return;
    }
    console.log('NEED_USER_INPUT');
    console.log(`MODE:${modeName(credentialMode)}`);
    console.log(SEPARATOR);
    console.log(askForKeyPrompt(credentialMode));
})().catch((error) => {
    process.exit(printShareOneScriptError(error));
});
