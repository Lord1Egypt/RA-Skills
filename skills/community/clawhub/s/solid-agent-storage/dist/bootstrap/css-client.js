/**
 * Low-level HTTP client for the CSS v7 Account API.
 *
 * CSS v7 flow:
 * 1. POST /.account/account/ → creates account, returns cookie + controls
 * 2. POST controls.password.create → adds email/password login
 * 3. POST controls.account.pod → creates pod, returns pod URL + WebID
 * 4. POST controls.account.clientCredentials → creates client credentials
 */
export async function createAccount(serverUrl) {
    const res = await fetch(`${serverUrl}/.account/account/`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: '{}',
    });
    if (!res.ok) {
        throw new Error(`Failed to create account: ${res.status} ${await res.text()}`);
    }
    const cookie = res.headers.get('set-cookie');
    if (!cookie) {
        throw new Error('No cookie returned from account creation');
    }
    const json = await res.json();
    return { cookie, accountUrl: `${serverUrl}/.account/` };
}
export async function addPasswordLogin(serverUrl, cookie, email, password) {
    const controls = await getControls(serverUrl, cookie);
    const passwordUrl = controls.password?.create;
    if (!passwordUrl) {
        throw new Error('Password creation endpoint not found in controls');
    }
    const res = await fetch(passwordUrl, {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
            cookie,
        },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
        throw new Error(`Failed to add password login: ${res.status} ${await res.text()}`);
    }
}
export async function createPod(serverUrl, cookie, name) {
    const controls = await getControls(serverUrl, cookie);
    const podUrl = controls.account?.pod;
    if (!podUrl) {
        throw new Error('Pod creation endpoint not found in controls');
    }
    const res = await fetch(podUrl, {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
            cookie,
        },
        body: JSON.stringify({ name }),
    });
    if (!res.ok) {
        throw new Error(`Failed to create pod: ${res.status} ${await res.text()}`);
    }
    const json = await res.json();
    return { pod: json.pod, webId: json.webId };
}
export async function createClientCredentials(serverUrl, cookie, name, webId) {
    const controls = await getControls(serverUrl, cookie);
    const credUrl = controls.account?.clientCredentials;
    if (!credUrl) {
        throw new Error('Client credentials endpoint not found in controls');
    }
    const res = await fetch(credUrl, {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
            cookie,
        },
        body: JSON.stringify({ name, webId }),
    });
    if (!res.ok) {
        throw new Error(`Failed to create client credentials: ${res.status} ${await res.text()}`);
    }
    const json = await res.json();
    return { id: json.id, secret: json.secret };
}
export async function loginWithPassword(serverUrl, email, password) {
    const res = await fetch(`${serverUrl}/.account/login/password/`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
        throw new Error(`Failed to login: ${res.status} ${await res.text()}`);
    }
    const cookie = res.headers.get('set-cookie');
    if (!cookie) {
        throw new Error('No cookie returned from login');
    }
    return cookie;
}
/**
 * Fully dismantles a CSS account by deleting all its components.
 *
 * CSS v7 has no single "delete account" endpoint. Instead, you delete
 * each component individually via resource URLs returned by GET on the
 * list endpoints:
 *   1. DELETE each client credential
 *   2. DELETE each pod
 *   3. DELETE each WebID link
 *   4. DELETE each password login
 *   5. POST logout to invalidate the session
 */
export async function deleteAccount(serverUrl, cookie) {
    const controls = await getControls(serverUrl, cookie);
    // 1. Delete all client credentials
    if (controls.account?.clientCredentials) {
        await deleteAllResources(controls.account.clientCredentials, cookie);
    }
    // 2. Delete all pods
    if (controls.account?.pod) {
        await deleteAllResources(controls.account.pod, cookie);
    }
    // 3. Unlink all WebIDs
    if (controls.account?.webId) {
        await deleteAllResources(controls.account.webId, cookie);
    }
    // 4. Delete all password logins
    if (controls.password?.create) {
        await deleteAllResources(controls.password.create, cookie);
    }
    // 5. Delete the account itself
    if (controls.account?.account) {
        const res = await fetch(controls.account.account, {
            method: 'DELETE',
            headers: { cookie },
        });
        if (!res.ok) {
            throw new Error(`Failed to delete account: ${res.status} ${await res.text()}`);
        }
    }
}
/**
 * GET a list endpoint to discover individual resource URLs, then DELETE each one.
 * CSS list endpoints return objects like { "id1": "http://.../resource/id1", "id2": "http://.../resource/id2" }.
 */
async function deleteAllResources(listUrl, cookie) {
    const res = await fetch(listUrl, { headers: { cookie } });
    if (!res.ok)
        return;
    const json = await res.json();
    for (const deleteUrl of Object.values(json)) {
        if (typeof deleteUrl === 'string' && deleteUrl.startsWith('http')) {
            const delRes = await fetch(deleteUrl, { method: 'DELETE', headers: { cookie } });
            if (!delRes.ok) {
                const body = await delRes.text();
                throw new Error(`Failed to delete ${deleteUrl}: ${delRes.status} ${body}`);
            }
        }
    }
}
async function getControls(serverUrl, cookie) {
    const res = await fetch(`${serverUrl}/.account/`, {
        headers: { cookie },
    });
    if (!res.ok) {
        throw new Error(`Failed to get account controls: ${res.status}`);
    }
    const json = await res.json();
    return json.controls ?? json;
}
//# sourceMappingURL=css-client.js.map