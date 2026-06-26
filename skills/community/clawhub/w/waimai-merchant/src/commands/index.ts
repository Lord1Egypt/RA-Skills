import { Command } from 'commander';
import { createMerchantCommands } from './merchant';
import { createProductCommands } from './product';

export function registerCommands(program: Command): void {
  program.addCommand(createMerchantCommands());
  program.addCommand(createProductCommands());
}
