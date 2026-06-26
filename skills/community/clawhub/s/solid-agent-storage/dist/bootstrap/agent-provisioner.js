import { createAccount, addPasswordLogin, createPod, createClientCredentials } from './css-client.js';
import { buildProfilePatch } from './webid-profile.js';
import { createPodContainers } from './pod-structure.js';
import { getAuthenticatedFetch } from '../auth/client-credentials.js';
/**
 * Full agent provisioning flow:
 * 1. Create CSS account
 * 2. Add password login
 * 3. Create pod at /agents/{name}/
 * 4. Create client credentials
 * 5. Patch WebID profile with agent metadata
 * 6. Create standard container structure
 */
export async function provisionAgent(config) {
    const { serverUrl, name, displayName } = config;
    console.log(`[bootstrap] Creating account for agent "${name}"...`);
    const account = await createAccount(serverUrl);
    const email = `${name}@agents.interition.local`;
    const password = `agent-${name}-${Date.now()}`;
    console.log(`[bootstrap] Adding password login...`);
    await addPasswordLogin(serverUrl, account.cookie, email, password);
    console.log(`[bootstrap] Creating pod at /agents/${name}/...`);
    const { pod: podUrl, webId } = await createPod(serverUrl, account.cookie, name);
    console.log(`[bootstrap] Creating client credentials...`);
    const creds = await createClientCredentials(serverUrl, account.cookie, name, webId);
    console.log(`[bootstrap] Patching WebID profile with agent metadata...`);
    const authFetch = await getAuthenticatedFetch(serverUrl, creds.id, creds.secret);
    const profileUrl = webId.replace(/#me$/, '');
    const patchBody = buildProfilePatch(config, webId);
    const patchRes = await authFetch(profileUrl, {
        method: 'PATCH',
        headers: { 'content-type': 'application/sparql-update' },
        body: patchBody,
    });
    if (!patchRes.ok) {
        console.warn(`[bootstrap] Warning: WebID profile patch returned ${patchRes.status}: ${await patchRes.text()}`);
    }
    console.log(`[bootstrap] Creating pod container structure...`);
    await createPodContainers(podUrl, authFetch);
    console.log(`[bootstrap] Agent "${name}" provisioned successfully!`);
    console.log(`  WebID: ${webId}`);
    console.log(`  Pod:   ${podUrl}`);
    return {
        webId,
        podUrl,
        email,
        password,
        clientCredentials: { id: creds.id, secret: creds.secret },
        config,
    };
}
//# sourceMappingURL=agent-provisioner.js.map