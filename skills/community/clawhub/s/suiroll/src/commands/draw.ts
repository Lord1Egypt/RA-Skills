import { Command } from 'commander';
import { Transaction } from '@mysten/sui/transactions';
import { getConfig } from '../config.js';
import { isValidObjectId } from '../utils.js';
import { executeTransaction } from '../utils/signer.js';

/**
 * Draw command - Draw winners for a lottery
 */
export function drawCommand(program: Command): void {
  program
    .command('draw')
    .description('Draw winners for a lottery (creator only)')
    .requiredOption('--lottery-id <id>', 'Lottery ID (Object ID)')
    .option('--seed <number>', 'Random seed for winner selection (optional)')
    .option('--chain <chain>', 'Sui network (mainnet or testnet)', 'testnet')
    .option('--gas-budget <amount>', 'Gas budget in MIST', '50000000')
    .action(async (options: {
      lotteryId: string;
      seed: string;
      chain: string;
      gasBudget: string;
    }) => {
      console.log('🎲 SUIROLL - Draw Winners\n');

      // Validate lottery ID
      if (!isValidObjectId(options.lotteryId)) {
        console.error('❌ Invalid lottery ID format. Must be a valid Sui Object ID (0x...)');
        process.exit(1);
      }

      const networkConfig = getConfig(options.chain as 'mainnet' | 'testnet');
      
      // Check if contract is deployed
      if (networkConfig.packageId === '0x0000000000000000000000000000000000000000000000000000000000000000') {
        console.log('⚠️  WARNING: Contract not yet deployed on ' + options.chain + '!');
        console.log('   Please deploy the contract first.\n');
        process.exit(1);
      }

      console.log('📋 Draw Parameters:');
      console.log(`   Lottery ID: ${options.lotteryId}`);
      console.log(`   Network: ${options.chain}`);
      console.log(`   Gas Budget: ${options.gasBudget} MIST\n`);

      try {
        // 1. Generate random seed (or use provided)
        const revealSeed = options.seed 
          ? parseInt(options.seed, 10) 
          : Math.floor(Math.random() * 1000000);

        console.log(`🎰 Using reveal seed: ${revealSeed}`);

        // 2. Create Transaction Block
        const tx = new Transaction();
        const packageId = networkConfig.packageId;

        // 3. Call draw_winners
        tx.moveCall({
          target: `${packageId}::lottery::draw_winners`,
          arguments: [
            tx.object(options.lotteryId),
            tx.pure.u64(revealSeed),
          ],
        });

        // 4. Set gas budget
        const gasBudget = parseInt(options.gasBudget, 10);
        tx.setGasBudget(gasBudget);

        // 5. Execute transaction
        console.log('📝 Drawing winners on-chain...');
        const result = await executeTransaction(tx, options.chain as 'mainnet' | 'testnet');

        console.log('\n✅ Winners drawn successfully!\n');

        // Print events
        if (result.events && result.events.length > 0) {
          const winnersEvent = result.events.find(e => 
            e.type.includes('WinnersDrawn') || e.type.includes('lottery::WinnersDrawn')
          );
          
          if (winnersEvent) {
            console.log('📊 Draw Results:');
            // Parse the event data
            try {
              const eventData = winnersEvent.parsedJson as any;
              if (eventData) {
                const winners = eventData.winners || [];
                const totalPrize = eventData.total_prize || 0;
                const randomSeed = eventData.random_seed || revealSeed;
                
                console.log(`   Winners: ${winners.length > 0 ? winners.join(', ') : 'N/A'}`);
                console.log(`   Total Prize: ${totalPrize}`);
                console.log(`   Random Seed: ${randomSeed}`);
              }
            } catch (e) {
              // Ignore parsing errors
              console.log(`   Event: ${JSON.stringify(winnersEvent.parsedJson)}`);
            }
          }

          result.events.forEach((event, i) => {
            if (event.type.includes('lottery::')) {
              console.log(`   ${i + 1}. ${event.type.split('::').pop()}`);
            }
          });
          console.log('');
        }

        console.log(`🔗 Transaction: https://explorer.sui.io/txblock/${result.digest}?network=${options.chain}\n`);

        // Verify the results
        console.log('💡 Verify Results:');
        console.log(`   suiroll verify --lottery-id ${options.lotteryId} --chain ${options.chain}\n`);

      } catch (error: any) {
        console.error('\n❌ Failed to draw winners:', error.message || error);
        
        // Provide helpful error messages
        if (error.message?.includes('ERR_NOT_CREATOR')) {
          console.log('\n💡 Hint: Only the lottery creator can draw winners.');
        } else if (error.message?.includes('ERR_DEADLINE_NOT_REACHED')) {
          console.log('\n💡 Hint: The lottery deadline has not been reached yet.');
        } else if (error.message?.includes('ERR_NO_ENTRIES')) {
          console.log('\n💡 Hint: There are no entries in this lottery yet.');
        } else if (error.message?.includes('ERR_ALREADY_DRAWN')) {
          console.log('\n💡 Hint: Winners have already been drawn for this lottery.');
        }
        
        process.exit(1);
      }
    });
}
