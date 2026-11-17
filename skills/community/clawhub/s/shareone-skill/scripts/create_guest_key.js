const {
    printShareOneScriptError,
    emitError,
    CREDENTIAL_MODE_SUDOWORK_PROXY,
    detectCredentialMode,
    isSudowork,
    requestPublicShareOneJson,
    saveLocalApiKey,
    saveSudoworkApiKey,
} = require('./shareone_client');

let noSave = false;
for (const arg of process.argv.slice(2)) {
    if (arg === '--no-save') {
        noSave = true;
    } else {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${arg}`, ['Usage: node create_guest_key.js [--no-save]'].join('\n'));
    }
}

async function createGuestKey() {
    try {
        const credentialMode = await detectCredentialMode({ refresh: true });
        const result = await requestPublicShareOneJson('/api/v1/agent-guest-key', {
            method: 'POST',
            authRequired: false,
        });
        if (!result.api_key) {
            emitError('INVALID_RESPONSE', 'The guest credential response contains no key.');
        }

        if (noSave) {
            console.log(`GUEST_KEY_CREATED:${result.api_key}`);
            console.log("NOTE:NOT_SAVED");
            return;
        }

        if (credentialMode.mode === CREDENTIAL_MODE_SUDOWORK_PROXY) {
            try {
                await saveSudoworkApiKey(result.api_key);
            } catch (error) {
                try {
                    saveLocalApiKey(result.api_key);
                } catch (saveError) {
                    if (saveError.code === 'EXISTING_KEY_CONFLICT') {
                        console.log(`GUEST_KEY_CREATED:${result.api_key}`);
                        console.log(`NOTE:EXISTING_KEY_KEPT:${saveError.existingKeyHint}`);
                        return;
                    }
                    throw saveError;
                }
                console.log(`GUEST_KEY_CREATED:${result.api_key}`);
                console.log("SUDOWORK_FALLBACK_KEY_SAVED");
                console.log("Auth Proxy 设置 ShareOne API Key 失败，已暂时保存到 ShareOne 本地 fallback 凭证。");
                if (error && error.message) {
                    console.log(`DETAIL:${error.message}`);
                }
                return;
            }
        } else {
            try {
                saveLocalApiKey(result.api_key);
            } catch (saveError) {
                if (saveError.code === 'EXISTING_KEY_CONFLICT') {
                    console.log(`GUEST_KEY_CREATED:${result.api_key}`);
                    console.log(`NOTE:EXISTING_KEY_KEPT:${saveError.existingKeyHint}`);
                    return;
                }
                throw saveError;
            }
        }
        console.log(`GUEST_KEY_CREATED:${result.api_key}`);
        if (isSudowork() && credentialMode.mode !== CREDENTIAL_MODE_SUDOWORK_PROXY) {
            console.log("SUDOWORK_FALLBACK_KEY_SAVED");
            console.log("Sudowork Auth Proxy 当前不可用，已保存到 ShareOne 本地 fallback 凭证。");
        }
    } catch (error) {
        process.exit(printShareOneScriptError(error));
    }
}

createGuestKey();
