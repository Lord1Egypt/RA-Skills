import { Command } from 'commander';
import { createCommand } from './commands/create.js';
import { enterCommand } from './commands/enter.js';
import { drawCommand } from './commands/draw.js';
import { verifyCommand } from './commands/verify.js';
import { listCommand } from './commands/list.js';
const program = new Command();
program
    .name('suiroll')
    .description('SUIROLL - Provably Fair Giveaway Tool for AI Agents on Sui\n' +
    'Uses Sui native VRF randomness for transparent winner selection')
    .version('1.0.0');
// Create lottery command
createCommand(program);
// Enter lottery command
enterCommand(program);
// Draw winner command
drawCommand(program);
// Verify results command
verifyCommand(program);
// List lotteries command
listCommand(program);
// Default command - show help
program.action(() => {
    program.help();
});
program.parse(process.argv);
//# sourceMappingURL=cli.js.map