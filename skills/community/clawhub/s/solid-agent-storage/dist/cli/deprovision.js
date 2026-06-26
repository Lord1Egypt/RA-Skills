import { loginWithPassword, deleteAccount } from '../bootstrap/css-client.js';
import { initStore, loadCredentials, deleteAgentCredentials } from './credentials-store.js';
import { requireArg, getServerUrl, getPassphrase } from './args.js';
const name = requireArg('name', 'Usage: deprovision --name <agent-name>');
const serverUrl = getServerUrl();
initStore(getPassphrase());
async function deprovision() {
    const warnings = [];
    let accountDeleted = false;
    // 1. Load credentials
    const creds = loadCredentials(name);
    // 2. Attempt full CSS account deletion if email+password are available
    if (creds.email && creds.password) {
        try {
            const cookie = await loginWithPassword(serverUrl, creds.email, creds.password);
            await deleteAccount(serverUrl, cookie);
            accountDeleted = true;
        }
        catch (err) {
            warnings.push(`Could not delete CSS account: ${err.message}`);
        }
    }
    else {
        warnings.push('No email/password stored (legacy provision). '
            + 'CSS account was not touched — remove it manually via the server admin.');
    }
    // 3. Delete local credential files
    deleteAgentCredentials(name);
    const result = {
        status: accountDeleted ? 'ok' : 'partial',
        agent: name,
        accountDeleted,
        credentialsDeleted: true,
    };
    if (warnings.length > 0) {
        result.warnings = warnings;
    }
    return result;
}
deprovision()
    .then((result) => {
    console.log(JSON.stringify(result));
})
    .catch((err) => {
    console.error(JSON.stringify({ error: String(err.message ?? err) }));
    process.exit(1);
});
//# sourceMappingURL=deprovision.js.map