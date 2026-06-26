import { Command } from 'commander';
import { getAuthenticatedClient, getActiveTenantId, formatApiError } from '../auth/index.js';

export function registerAccountCommands(program: Command): void {
  const accounts = program
    .command('accounts')
    .description('Manage Xero chart of accounts');

  accounts
    .command('list')
    .description('List accounts')
    .option('-t, --type <type>', 'Filter by account type (BANK, REVENUE, EXPENSE, etc.)')
    .option('-c, --class <class>', 'Filter by account class (ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE)')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        
        let whereFilter: string | undefined;
        const filters: string[] = [];
        
        filters.push('Status=="ACTIVE"');
        
        if (options.type) {
          filters.push(`Type=="${options.type.toUpperCase()}"`);
        }
        if (options.class) {
          filters.push(`Class=="${options.class.toUpperCase()}"`);
        }
        
        whereFilter = filters.join(' AND ');

        const response = await xero.accountingApi.getAccounts(
          tenantId,
          undefined,
          whereFilter,
          'Code ASC'
        );

        const accountList = response.body.accounts?.map(a => ({
          accountId: a.accountID,
          code: a.code,
          name: a.name,
          type: a.type,
          class: a._class,
          taxType: a.taxType,
          description: a.description,
          enablePaymentsToAccount: a.enablePaymentsToAccount,
        })) || [];

        console.log(JSON.stringify({ accounts: accountList, count: accountList.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  accounts
    .command('get <accountId>')
    .description('Get account details')
    .action(async (accountId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        const response = await xero.accountingApi.getAccount(tenantId, accountId);

        const a = response.body.accounts?.[0];
        if (!a) {
          console.error(JSON.stringify({ error: 'Account not found' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          accountId: a.accountID,
          code: a.code,
          name: a.name,
          type: a.type,
          class: a._class,
          taxType: a.taxType,
          description: a.description,
          bankAccountNumber: a.bankAccountNumber,
          bankAccountType: a.bankAccountType,
          currencyCode: a.currencyCode,
          enablePaymentsToAccount: a.enablePaymentsToAccount,
          showInExpenseClaims: a.showInExpenseClaims,
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });
}
