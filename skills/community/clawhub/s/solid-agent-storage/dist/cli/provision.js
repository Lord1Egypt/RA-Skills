import { provisionAgent } from '../bootstrap/agent-provisioner.js';
import { initStore, saveCredentials } from './credentials-store.js';
import { requireArg, getArg, getServerUrl, getPassphrase } from './args.js';
const name = requireArg('name', 'Usage: provision --name <name> [--displayName <name>]');
const displayName = getArg('displayName') ?? name;
const serverUrl = getServerUrl();
initStore(getPassphrase());
provisionAgent({ name, displayName, serverUrl })
    .then((agent) => {
    saveCredentials(name, {
        webId: agent.webId,
        podUrl: agent.podUrl,
        id: agent.clientCredentials.id,
        secret: agent.clientCredentials.secret,
        email: agent.email,
        password: agent.password,
    });
    console.log(JSON.stringify({
        status: 'ok',
        agent: name,
        webId: agent.webId,
        podUrl: agent.podUrl,
    }));
})
    .catch((err) => {
    console.error(JSON.stringify({ error: String(err.message ?? err) }));
    process.exit(1);
});
//# sourceMappingURL=provision.js.map