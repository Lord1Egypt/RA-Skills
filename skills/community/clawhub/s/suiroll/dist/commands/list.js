/**
 * List command - List all lotteries
 */
export function listCommand(program) {
    program
        .command('list')
        .description('List all lotteries (optional command)')
        .option('--status <status>', 'Filter by status (open, drawn, cancelled)', 'all')
        .option('--chain <chain>', 'Sui network (mainnet or testnet)', 'testnet')
        .option('--limit <number>', 'Number of lotteries to show', '20')
        .action(async (options) => {
        console.log('📋 SUIROLL - List Lotteries\n');
        console.log('⚠️  WARNING: Contract not yet deployed!');
        console.log('   This feature requires Phase 1 completion.\n');
        console.log('List parameters:');
        console.log(`   Status Filter: ${options.status}`);
        console.log(`   Network: ${options.chain}`);
        console.log(`   Limit: ${options.limit}\n`);
        console.log('📋 Next Steps:');
        console.log('   1. Complete Phase 1: Deploy Sui Move contract');
        console.log('   2. Implement lottery indexing');
        console.log('   3. Update src/config.ts with contract PACKAGE_ID\n');
        console.log('💡 Alternative:');
        console.log('   View on Sui Explorer:');
        console.log('   https://explorer.sui.io/');
        console.log('   (Search for package published by your address)\n');
        process.exit(0);
    });
}
//# sourceMappingURL=list.js.map