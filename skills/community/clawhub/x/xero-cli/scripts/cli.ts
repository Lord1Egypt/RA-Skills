#!/usr/bin/env node
import { Command } from 'commander';
import {
  registerAuthCommands,
  registerTenantCommands,
  registerInvoiceCommands,
  registerContactCommands,
  registerAccountCommands,
  registerBankTransactionCommands,
  registerPaymentCommands,
  registerAllocationCommands,
} from './commands/index.js';

const program = new Command();

program
  .name('xero-cli')
  .description('CLI for interacting with Xero accounting API')
  .version('1.0.0');

registerAuthCommands(program);
registerTenantCommands(program);
registerInvoiceCommands(program);
registerContactCommands(program);
registerAccountCommands(program);
registerBankTransactionCommands(program);
registerPaymentCommands(program);
registerAllocationCommands(program);

program.parse();
