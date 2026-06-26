/**
 * Moltbook API Integration
 * Authentication and identity verification for AI agents
 */
// Configuration
const MOLTBOOK_API_BASE = 'https://www.moltbook.com/api/v1';
const DEFAULT_AUDIENCE = 'suiroll.app';
/**
 * Get Moltbook API key from environment or credentials file
 */
export function getMoltbookApiKey() {
    // Check environment variable first
    const envKey = process.env.MOLTBOOK_API_KEY;
    if (envKey) {
        return envKey;
    }
    return null;
}
/**
 * Get Moltbook app key (developer API key) for verification
 */
export function getMoltbookAppKey() {
    return process.env.MOLTBOOK_APP_KEY || null;
}
/**
 * Get the audience value for token verification
 */
export function getAudience() {
    return process.env.MOLTBOOK_AUDIENCE || DEFAULT_AUDIENCE;
}
/**
 * Generate a temporary identity token for the agent
 * This is called by the bot to get a token to authenticate with external services
 */
export async function generateIdentityToken(apiKey, audience) {
    const targetAudience = audience || getAudience();
    const response = await fetch(`${MOLTBOOK_API_BASE}/agents/me/identity-token`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            audience: targetAudience,
        }),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `Failed to generate identity token: ${response.statusText}`);
    }
    return response.json();
}
/**
 * Verify an identity token and get agent information
 * This is called by the external service to verify the bot's identity
 */
export async function verifyIdentityToken(token, audience) {
    const appKey = getMoltbookAppKey();
    if (!appKey) {
        throw new Error('MOLTBOOK_APP_KEY not configured. ' +
            'Set it in environment variables or configure in your app settings.');
    }
    const targetAudience = audience || getAudience();
    const response = await fetch(`${MOLTBOOK_API_BASE}/agents/verify-identity`, {
        method: 'POST',
        headers: {
            'X-Moltbook-App-Key': appKey,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            token,
            audience: targetAudience,
        }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || !data.valid) {
        throw new Error(data.error || `Token verification failed: ${response.statusText}`);
    }
    return data.agent;
}
/**
 * Interactive login - prompt for credentials and get API key
 * For CLI use when no saved credentials exist
 */
export async function interactiveLogin() {
    const readline = await import('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    const question = (prompt) => {
        return new Promise((resolve) => {
            rl.question(prompt, (answer) => {
                resolve(answer);
            });
        });
    };
    try {
        console.log('\n🔐 Moltbook Authentication\n');
        // Note: For CLI, users typically already have their API key
        // This is a simplified flow - in practice, users would provide their API key directly
        const apiKey = await question('Enter your Moltbook API key (moltbook_...): ');
        if (!apiKey.startsWith('moltbook_')) {
            throw new Error('Invalid API key format. Key should start with "moltbook_"');
        }
        // Generate and verify identity token
        console.log('\n✓ Authenticating...');
        const identityData = await generateIdentityToken(apiKey);
        const agent = await verifyIdentityToken(identityData.identity_token);
        console.log(`✓ Authenticated as: ${agent.name} (ID: ${agent.id})`);
        console.log(`  Karma: ${agent.karma} | Followers: ${agent.follower_count}\n`);
        rl.close();
        return { apiKey, agent };
    }
    catch (error) {
        rl.close();
        throw error;
    }
}
/**
 * Get agent information from stored credentials
 * Reads from ~/.config/moltbook/credentials.json
 */
export async function getAgentFromCredentials() {
    const apiKey = getMoltbookApiKey();
    if (!apiKey) {
        return null;
    }
    try {
        // Generate and verify token to get agent info
        const identityData = await generateIdentityToken(apiKey);
        const agent = await verifyIdentityToken(identityData.identity_token);
        return { apiKey, agent };
    }
    catch (error) {
        console.error('⚠️  Failed to authenticate with stored credentials:', error);
        return null;
    }
}
/**
 * Format agent information for display
 */
export function formatAgentInfo(agent) {
    let output = `🤖 **${agent.name}**`;
    output += `\n   ID: \`${agent.id}\``;
    output += `\n   Karma: ${agent.karma}`;
    output += `\n   Followers: ${agent.follower_count}`;
    output += `\n   Posts: ${agent.stats.posts}`;
    output += `\n   Comments: ${agent.stats.comments}`;
    if (agent.owner) {
        output += `\n   Owner: @${agent.owner.x_handle}`;
        if (agent.owner.x_verified) {
            output += ' ✓';
        }
    }
    if (agent.is_claimed) {
        output += '\n   ✅ Claimed';
    }
    return output;
}
//# sourceMappingURL=moltbook.js.map