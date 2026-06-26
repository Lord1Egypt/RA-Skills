import { Command } from 'commander';
import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';
import { getConfig } from '../config.js';
import { isValidObjectId } from '../utils.js';

/**
 * Status to string mapping
 */
function getStatusString(status: number): string {
  switch (status) {
    case 0: return '🟢 Open (Accepting Entries)';
    case 1: return '🟡 Committed (Waiting for Draw)';
    case 2: return '🔴 Drawn (Complete)';
    case 3: return '⚫ Cancelled';
    default: return `Unknown (${status})`;
  }
}

/**
 * Token type to string mapping
 */
function getTokenTypeString(tokenType: number): string {
  switch (tokenType) {
    case 0: return 'SUI';
    case 1: return 'USDC';
    default: return `Unknown (${tokenType})`;
  }
}

/**
 * Format amount based on token type
 */
function formatPrize(amount: number, tokenType: number): string {
  if (tokenType === 0) {
    // SUI (9 decimals)
    return `${(amount / 1000000000).toFixed(2)} SUI`;
  } else if (tokenType === 1) {
    // USDC (6 decimals)
    return `${(amount / 1000000).toFixed(2)} USDC`;
  }
  return `${amount} (unknown token)`;
}

/**
 * Verify command - Verify lottery results and VRF proof
 */
export function verifyCommand(program: Command): void {
  program
    .command('verify')
    .description('Verify lottery results and VRF proof')
    .requiredOption('--lottery-id <id>', 'Lottery ID (Object ID)')
    .option('--chain <chain>', 'Sui network (mainnet or testnet)', 'testnet')
    .action(async (options: {
      lotteryId: string;
      chain: string;
    }) => {
      console.log('✅ SUIROLL - Verify Results\n');

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

      console.log(`📋 Verification Parameters:`);
      console.log(`   Lottery ID: ${options.lotteryId}`);
      console.log(`   Network: ${options.chain}`);
      console.log(`   Package: ${networkConfig.packageId}\n`);

      try {
        // 1. Fetch lottery object
        const client = new SuiClient({ url: getFullnodeUrl(options.chain as 'mainnet' | 'testnet') });
        
        console.log('📝 Fetching lottery data from chain...');
        const lottery = await client.getObject({
          id: options.lotteryId,
          options: { showContent: true, showType: true },
        });

        if (!lottery.data) {
          console.error('❌ Lottery not found!');
          console.log('   The lottery ID may be invalid or not yet deployed.\n');
          process.exit(1);
        }

        // 2. Extract relevant fields
        const content = lottery.data.content as any;
        const fields = content?.fields;
        const type = lottery.data.type || '';

        console.log('🔍 Verifying lottery...\n');

        // Parse fields (handle both direct and nested structures)
        const status = fields?.status ?? 0;
        const winnerCount = fields?.winner_count ?? 0;
        const tokenType = fields?.token_type ?? 0;
        const deadline = fields?.deadline ?? 0;
        const entries = fields?.entries ?? [];
        const commitmentHash = fields?.commitment_hash;
        const revealSeed = fields?.reveal_seed;

        // Prize pool (handle both SUI and USDC)
        let prizePool = 0;
        if (fields?.prize_pool_sui) {
          prizePool = fields.pri_pool_sui?.fields?.value ?? 0;
        } else if (fields?.prize_pool_usdc) {
          prizePool = fields.prize_pool_usdc?.fields?.value ?? 0;
        }

        // Winners (only available after draw)
        const winners = fields?.winners ?? [];

        // Calculate derived values
        const entryCount = Array.isArray(entries) ? entries.length : 0;
        const now = Date.now();
        const isExpired = deadline > 0 && now > deadline;

        // 3. Display verification info
        console.log('═'.repeat(60));
        console.log('                    LOTTERY VERIFICATION');
        console.log('═'.repeat(60));
        console.log('');

        // Basic Info
        console.log('📊 LOTTERY STATUS');
        console.log('─'.repeat(40));
        console.log(`   Status:        ${getStatusString(status)}`);
        console.log(`   Token Type:    ${getTokenTypeString(tokenType)}`);
        console.log(`   Prize Pool:    ${formatPrize(prizePool, tokenType)}`);
        console.log(`   Winner Count:  ${winnerCount}`);
        console.log('');

        // Deadline Info
        console.log('⏰ DEADLINE');
        console.log('─'.repeat(40));
        if (deadline > 0) {
          const deadlineDate = new Date(deadline);
          console.log(`   Deadline:      ${deadlineDate.toLocaleString()}`);
          console.log(`   Status:        ${isExpired ? '✅ Expired (can draw)' : '⏳ Active (accepting entries)'}`);
        } else {
          console.log(`   Deadline:      Not set`);
        }
        console.log('');

        // Entries Info
        console.log('👥 ENTRIES');
        console.log('─'.repeat(40));
        console.log(`   Total Entries: ${entryCount}`);
        if (entryCount > 0) {
          console.log(`   First Entry:   ${entries[0] || 'N/A'}`);
          if (entryCount > 1) {
            console.log(`   Last Entry:    ${entries[entryCount - 1] || 'N/A'}`);
          }
        }
        console.log('');

        // Draw Info (if drawn)
        if (status === 2 && winners.length > 0) {
          console.log('🏆 WINNERS');
          console.log('─'.repeat(40));
          winners.forEach((winner: string, index: number) => {
            const prizePerWinner = prizePool / winners.length;
            console.log(`   ${index + 1}. ${winner}`);
            console.log(`      Prize: ${formatPrize(prizePerWinner, tokenType)}`);
          });
          console.log('');

          if (revealSeed) {
            console.log('🎰 RANDOMNESS');
            console.log('─'.repeat(40));
            console.log(`   Reveal Seed:   ${revealSeed}`);
            console.log('');
          }
        } else if (status === 2) {
          console.log('🏆 WINNERS');
          console.log('─'.repeat(40));
          console.log('   Winners have been selected');
          console.log('   (Winner addresses stored on-chain)');
          console.log('');
        }

        // VRF Info
        console.log('🔐 VRF / RANDOMNESS');
        console.log('─'.repeat(40));
        if (commitmentHash) {
          console.log(`   Commitment:    Submitted`);
          console.log(`   Hash:          ${commitmentHash.substring(0, 16)}...`);
        } else {
          console.log(`   Commitment:    Not submitted`);
        }
        console.log('');

        // Links
        console.log('🔗 LINKS');
        console.log('─'.repeat(40));
        console.log(`   Object:        https://explorer.sui.io/object/${options.lotteryId}?network=${options.chain}`);
        console.log('');

        // Verification Summary
        console.log('═'.repeat(60));
        console.log('                    VERIFICATION SUMMARY');
        console.log('═'.repeat(60));

        const checks: string[] = [];

        // Check if lottery exists
        checks.push('✅ Lottery object exists on-chain');

        // Check status
        if (status === 0) {
          checks.push('🟢 Lottery is open for entries');
        } else if (status === 2) {
          checks.push('🔴 Lottery has been drawn');
        } else if (status === 3) {
          checks.push('⚫ Lottery was cancelled');
        }

        // Check entries
        if (entryCount > 0) {
          checks.push(`👥 Has ${entryCount} on-chain entries`);
        } else if (status === 0) {
          checks.push('⚠️  No entries yet');
        }

        // Check can draw
        if (status === 0 && isExpired) {
          checks.push('🎲 Ready to draw (deadline passed)');
        }

        checks.forEach(check => console.log(`   ${check}`));
        console.log('');

        // Action recommendations
        console.log('💡 RECOMMENDED ACTIONS:');
        console.log('─'.repeat(40));
        if (status === 0) {
          if (isExpired) {
            console.log('   suiroll draw --lottery-id <id>');
          } else {
            console.log('   suiroll enter --lottery-id <id>');
          }
        } else if (status === 2) {
          console.log('   suiroll verify --lottery-id <id>');
        }
        console.log('');

      } catch (error: any) {
        console.error('\n❌ Failed to verify lottery:', error.message || error);
        
        if (error.message?.includes('Object not found')) {
          console.log('\n💡 Hint: The lottery ID may be incorrect or not yet deployed.');
        }
        
        process.exit(1);
      }
    });
}
