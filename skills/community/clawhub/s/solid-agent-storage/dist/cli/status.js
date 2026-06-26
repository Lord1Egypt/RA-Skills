import { initStore, listAgents, loadCredentials } from './credentials-store.js';
import { getPassphrase } from './args.js';
initStore(getPassphrase());
const agents = listAgents();
const result = agents.map((name) => {
    try {
        const creds = loadCredentials(name);
        return { name, webId: creds.webId, podUrl: creds.podUrl };
    }
    catch {
        return { name, error: 'Could not decrypt credentials' };
    }
});
console.log(JSON.stringify({ status: 'ok', agents: result }, null, 2));
//# sourceMappingURL=status.js.map