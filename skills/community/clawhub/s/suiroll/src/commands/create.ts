import { Command } from 'commander';
import { Transaction } from '@mysten/sui/transactions';
import { TokenType, getCreateFunctionName, getMinPrize, parsePrizeAmount } from '../utils/coin.js';
import { getConfig } from '../config.js';
import { isValidObjectId } from '../utils.js';
import { executeTransaction } from '../utils/signer.js';

/**
 * Create command - Create a new lottery/giveaway
 */
export function createCommand(program: Command): void {
  program
    .command('create')
    .description('Create a new lottery/giveaway')
    .requiredOption('--name <name>', 'Lottery name (e.g., "Weekly Giveaway")')
    .requiredOption('--prize <amount>', 'Prize amount')
    .requiredOption('--days <number>', 'Number of days until deadline')
    .requiredOption('--winners <number>', 'Number of winners')
    .option('--token <token>', 'Token type (SUI or USDC)', 'USDC')
    .option('--chain <chain>', 'Sui network (mainnet or testnet)', 'testnet')
    .option('--gas-budget <amount>', 'Gas budget in MIST', '10000000')
    .action(async (options: {
      name: string;
      prize: string;
      days: string;
      winners: string;
      token: TokenType;
      chain: string;
      gasBudget: string;
    }) => {
      console.log('🚀 SUIROLL - Create Lottery\n');

      // Validate token type
      const validTokens: TokenType[] = ['SUI', 'USDC'];
      if (!validTokens.includes(options.token)) {
        console.error(`❌ Error: Invalid token type "${options.token}". Must be SUI or USDC.`);
        process.exit(1);
      }

      // Parse and validate prize amount
      const prizeAmount = parseFloat(options.prize);
      if (isNaN(prizeAmount) || prizeAmount <= 0) {
        console.error(`❌ Error: Invalid prize amount "${options.prize}". Must be a positive number.`);
        process.exit(1);
      }

      const minPrize = getMinPrize(options.token);
      const prizeInSmallestUnits = parsePrizeAmount(prizeAmount, options.token);

      if (prizeInSmallestUnits < minPrize) {
        console.error(`❌ Error: Minimum prize for ${options.token} is ${minPrize / (options.token === 'USDC' ? 1000000 : 1000000000)} ${options.token}`);
        process.exit(1);
      }

      // Parse other parameters
      const days = parseInt(options.days, 10);
      const winners = parseInt(options.winners, 10);

      if (isNaN(days) || days < 0) {
        console.error(`❌ Error: Invalid days "${options.days}". Must be a non-negative integer.`);
        process.exit(1);
      }

      if (isNaN(winners) || winners < 1 || winners > 100) {
        console.error(`❌ Error: Invalid winner count "${options.winners}". Must be between 1 and 100.`);
        process.exit(1);
      }

      const networkConfig = getConfig(options.chain as 'mainnet' | 'testnet');
      
      console.log('📋 Lottery Parameters:');
      console.log(`   Name: ${options.name}`);
      console.log(`   Prize: ${prizeAmount} ${options.token}`);
      console.log(`   Duration: ${days} days`);
      console.log(`   Winners: ${winners}`);
      console.log(`   Token: ${options.token}`);
      console.log(`   Network: ${options.chain}`);
      console.log(`   Gas Budget: ${options.gasBudget} MIST\n`);

      // Check if contract is deployed
      if (networkConfig.packageId === '0x0000000000000000000000000000000000000000000000000000000000000000') {
        console.log('⚠️  WARNING: Contract not yet deployed on ' + options.chain + '!');
        console.log('   Please deploy the contract first.\n');
        process.exit(1);
      }

      try {
        // 1. Parse prize amount
        const parsedAmount = parsePrizeAmount(prizeAmount, options.token);

        // 2. Create Transaction Block
        const tx = new Transaction();
        const packageId = networkConfig.packageId;

        // 3. Split prize coin from wallet
        const [prizeCoin] = tx.splitCoins(tx.gas, [tx.pure.u64(parsedAmount)]);

        // 4. Call contract function
        const functionName = getCreateFunctionName(options.token); // create_lottery_sui or create_lottery_usdc
        tx.moveCall({
          target: `${packageId}::lottery::${functionName}`,
          arguments: [
            tx.pure.string(options.name),
            prizeCoin,
            tx.pure.u64(days),
            tx.pure.u64(winners),
            tx.object(networkConfig.registryObjectId),
          ],
        });

        // 5. Set gas budget
        const gasBudget = parseInt(options.gasBudget, 10);
        tx.setGasBudget(gasBudget);

        // 6. Sign and execute
        console.log('📝 Creating lottery on-chain...');
        const result = await executeTransaction(tx, options.chain as 'mainnet' | 'testnet');

        // 7. Print result
        console.log('\n✅ Lottery created successfully!\n');
        
        // The transaction digest
        console.log(`🔗 Transaction: https://explorer.sui.io/txblock/${result.digest}?network=${options.chain}`);
        
        // Print events
        if (result.events && result.events.length > 0) {
          console.log('\n📊 Events:');
          result.events.forEach((event, i) => {
            console.log(`   ${i + 1}. ${event.type}`);
          });
        }

      } catch (error) {
        console.error('\n❌ Failed to create lottery:', error);
        process.exit(1);
      }

      console.log('\n💡 Next Steps:');
      console.log(`   suiroll enter --lottery-id <id> --chain ${options.chain}`);
      console.log(`   suiroll verify --lottery-id <id> --chain ${options.chain}\n`);
    });
}
