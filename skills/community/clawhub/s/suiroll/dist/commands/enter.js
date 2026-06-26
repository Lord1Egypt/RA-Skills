import { Transaction } from '@mysten/sui/transactions';
import { getConfig } from '../config.js';
import { isValidObjectId } from '../utils.js';
import { getMoltbookApiKey, generateIdentityToken, verifyIdentityToken, } from '../utils/moltbook.js';
import { executeTransaction } from '../utils/signer.js';
/**
 * Load saved session from file
 */
async function loadSession() {
    try {
        const fs = await import('fs');
        const path = await import('path');
        const sessionPath = path.join(process.env.HOME || '~', '.config', 'suiroll', 'moltbook-session.json');
        if (fs.existsSync(sessionPath)) {
            const session = JSON.parse(fs.readFileSync(sessionPath, 'utf-8'));
            return session;
        }
    }
    catch (error) {
        // Ignore errors
    }
    return null;
}
/**
 * Save session to file
 */
async function saveSession(apiKey, agent) {
    try {
        const fs = await import('fs');
        const path = await import('path');
        const sessionDir = path.join(process.env.HOME || '~', '.config', 'suiroll');
        const sessionPath = path.join(sessionDir, 'moltbook-session.json');
        // Ensure directory exists
        if (!fs.existsSync(sessionDir)) {
            fs.mkdirSync(sessionDir, { recursive: true });
        }
        fs.writeFileSync(sessionPath, JSON.stringify({ apiKey, agent }, null, 2));
    }
    catch (error) {
        console.error('⚠️  Failed to save session:', error);
    }
}
/**
 * Get agent authentication
 */
async function authenticateAgent() {
    // Try saved session first
    const session = await loadSession();
    if (session) {
        console.log('✓ Found saved Moltbook session');
        console.log(`  Agent: ${session.agent.name}\n`);
        return session;
    }
    // Try environment variable
    const envApiKey = getMoltbookApiKey();
    if (envApiKey) {
        console.log('✓ Using Moltbook API key from environment');
        const identityData = await generateIdentityToken(envApiKey);
        const agent = await verifyIdentityToken(identityData.identity_token);
        console.log(`  Agent: ${agent.name}\n`);
        // Save session for future use
        await saveSession(envApiKey, agent);
        return { apiKey: envApiKey, agent };
    }
    // Interactive prompt
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
        console.log('\n🔐 Moltbook Authentication Required');
        console.log('   Your agent needs to authenticate to enter the lottery.\n');
        const apiKey = await question('Enter your Moltbook API key (moltbook_...): ');
        if (!apiKey.startsWith('moltbook_')) {
            throw new Error('Invalid API key format. Key should start with "moltbook_"');
        }
        console.log('\n✓ Authenticating with Moltbook...');
        const identityData = await generateIdentityToken(apiKey);
        const agent = await verifyIdentityToken(identityData.identity_token);
        console.log(`✓ Authenticated as: ${agent.name} (ID: ${agent.id})`);
        console.log(`  Karma: ${agent.karma} | Followers: ${agent.follower_count}\n`);
        // Save session
        await saveSession(apiKey, agent);
        rl.close();
        return { apiKey, agent };
    }
    catch (error) {
        rl.close();
        throw error;
    }
}
/**
 * Enter command - Enter a lottery/giveaway
 */
export function enterCommand(program) {
    program
        .command('enter')
        .description('Enter a lottery/giveaway')
        .requiredOption('--lottery-id <id>', 'Lottery ID (Object ID)')
        .requiredOption('--agent', 'Moltbook agent authentication (REQUIRED for fair entry)')
        .option('--chain <chain>', 'Sui network (mainnet or testnet)', 'testnet')
        .option('--gas-budget <amount>', 'Gas budget in MIST', '10000000')
        .action(async (options) => {
        console.log('🎟️  SUIROLL - Enter Lottery\n');
        // Validate lottery ID
        if (!isValidObjectId(options.lotteryId)) {
            console.error('❌ Invalid lottery ID format. Must be a valid Sui Object ID (0x...)');
            process.exit(1);
        }
        const networkConfig = getConfig(options.chain);
        // Check if contract is deployed
        if (networkConfig.packageId === '0x0000000000000000000000000000000000000000000000000000000000000000') {
            console.log('⚠️  WARNING: Contract not yet deployed on ' + options.chain + '!');
            console.log('   Please deploy the contract first.\n');
            process.exit(1);
        }
        console.log(`🌐 Network: ${networkConfig.network}`);
        console.log(`📦 Package: ${networkConfig.packageId}\n`);
        // ===== MOLTBOOK AUTHENTICATION REQUIRED =====
        // Dual enforcement: agent_id required to prevent Sybil attacks
        console.log('🔐 Authenticating with Moltbook (REQUIRED for fair entry)...\n');
        let agentInfo;
        let agentId;
        try {
            agentInfo = await authenticateAgent();
            agentId = agentInfo.agent.id;
        }
        catch (error) {
            console.error('❌ Moltbook authentication failed!');
            console.error('   Error:', error);
            console.error('\n💡 To authenticate:');
            console.error('   1. Get API key from: https://www.moltbook.com/developers');
            console.error('   2. Set environment variable:');
            console.error('      export MOLTBOOK_API_KEY="moltbook_your_api_key"\n');
            process.exit(1);
        }
        // Display entry parameters
        console.log('📋 Entry Parameters:');
        console.log(`   Lottery ID: ${options.lotteryId}`);
        console.log(`   Auth Method: Moltbook Agent (REQUIRED)`);
        console.log(`   Agent ID: ${agentInfo.agent.id}`);
        console.log(`   Agent Name: ${agentInfo.agent.name}`);
        console.log(`   Network: ${options.chain}`);
        console.log(`   Gas Budget: ${options.gasBudget} MIST\n`);
        try {
            // 1. Create Transaction Block
            const tx = new Transaction();
            const packageId = networkConfig.packageId;
            // 2. Call enter_lottery (agent_id is REQUIRED, not optional)
            tx.moveCall({
                target: `${packageId}::lottery::enter_lottery`,
                arguments: [
                    tx.object(options.lotteryId),
                    tx.pure.string(agentId), // REQUIRED - no longer optional
                ],
            });
            // 3. Set gas budget
            const gasBudget = parseInt(options.gasBudget, 10);
            tx.setGasBudget(gasBudget);
            // 4. Execute transaction
            console.log('📝 Submitting entry to lottery...');
            const result = await executeTransaction(tx, options.chain);
            console.log('\n✅ Successfully entered lottery!');
            console.log('🛡️  Sybil Protection: One entry per agent enforced\n');
            // Print events
            if (result.events && result.events.length > 0) {
                console.log('📊 Events:');
                result.events.forEach((event, i) => {
                    console.log(`   ${i + 1}. ${event.type}`);
                });
                console.log('');
            }
            console.log(`🔗 Transaction: https://explorer.sui.io/txblock/${result.digest}?network=${options.chain}\n`);
        }
        catch (error) {
            console.error('\n❌ Failed to enter lottery:', error);
            process.exit(1);
        }
        console.log('💡 Next Steps:');
        console.log(`   suiroll verify --lottery-id ${options.lotteryId} --chain ${options.chain}`);
        console.log('   Wait for lottery deadline, then creator will draw winners\n');
    });
}
//# sourceMappingURL=enter.js.map