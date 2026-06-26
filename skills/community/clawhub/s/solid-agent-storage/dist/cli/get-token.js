import { initStore, loadCredentials } from './credentials-store.js';
import { requireArg, getServerUrl, getPassphrase } from './args.js';
const agent = requireArg('agent', 'Usage: get-token --agent <name>');
const serverUrl = getServerUrl();
initStore(getPassphrase());
(async () => {
    const creds = loadCredentials(agent);
    const tokenUrl = `${serverUrl}/.oidc/token`;
    const authString = Buffer.from(`${creds.id}:${creds.secret}`).toString('base64');
    const res = await fetch(tokenUrl, {
        method: 'POST',
        headers: {
            authorization: `Basic ${authString}`,
            'content-type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            grant_type: 'client_credentials',
            scope: 'webid',
        }),
    });
    if (!res.ok) {
        console.error(JSON.stringify({ error: `Token request failed: ${res.status} ${await res.text()}` }));
        process.exit(1);
    }
    const json = await res.json();
    console.log(JSON.stringify({
        token: json.access_token,
        expiresIn: json.expires_in,
        serverUrl,
        podUrl: creds.podUrl,
        webId: creds.webId,
    }));
})().catch((err) => {
    console.error(JSON.stringify({ error: String(err.message ?? err) }));
    process.exit(1);
});
//# sourceMappingURL=get-token.js.map