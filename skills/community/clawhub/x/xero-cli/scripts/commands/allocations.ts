import { Command } from 'commander';
import { Allocation } from 'xero-node';
import { getAuthenticatedClient, getActiveTenantId, formatApiError } from '../auth/index.js';

export function registerAllocationCommands(program: Command): void {
  const allocations = program
    .command('allocations')
    .description('Allocate overpayments, prepayments, and credit notes to invoices');

  allocations
    .command('overpayment')
    .description('Allocate an overpayment to an invoice')
    .requiredOption('-o, --overpayment <overpaymentId>', 'Overpayment ID')
    .requiredOption('-i, --invoice <invoiceId>', 'Invoice ID to allocate to')
    .requiredOption('-a, --amount <amount>', 'Amount to allocate')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const allocation: Allocation = {
          invoice: { invoiceID: options.invoice },
          amount: parseFloat(options.amount),
          date: new Date().toISOString().split('T')[0],
        };

        const response = await xero.accountingApi.createOverpaymentAllocations(
          tenantId,
          options.overpayment,
          { allocations: [allocation] }
        );

        const created = response.body.allocations?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create allocation' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          allocation: {
            amount: created.amount,
            date: created.date,
            invoiceId: created.invoice?.invoiceID,
            invoiceNumber: created.invoice?.invoiceNumber,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  allocations
    .command('prepayment')
    .description('Allocate a prepayment to an invoice')
    .requiredOption('-p, --prepayment <prepaymentId>', 'Prepayment ID')
    .requiredOption('-i, --invoice <invoiceId>', 'Invoice ID to allocate to')
    .requiredOption('-a, --amount <amount>', 'Amount to allocate')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const allocation: Allocation = {
          invoice: { invoiceID: options.invoice },
          amount: parseFloat(options.amount),
          date: new Date().toISOString().split('T')[0],
        };

        const response = await xero.accountingApi.createPrepaymentAllocations(
          tenantId,
          options.prepayment,
          { allocations: [allocation] }
        );

        const created = response.body.allocations?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create allocation' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          allocation: {
            amount: created.amount,
            date: created.date,
            invoiceId: created.invoice?.invoiceID,
            invoiceNumber: created.invoice?.invoiceNumber,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  allocations
    .command('creditnote')
    .description('Allocate a credit note to an invoice')
    .requiredOption('-c, --creditnote <creditNoteId>', 'Credit Note ID')
    .requiredOption('-i, --invoice <invoiceId>', 'Invoice ID to allocate to')
    .requiredOption('-a, --amount <amount>', 'Amount to allocate')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const allocation: Allocation = {
          invoice: { invoiceID: options.invoice },
          amount: parseFloat(options.amount),
          date: new Date().toISOString().split('T')[0],
        };

        const response = await xero.accountingApi.createCreditNoteAllocation(
          tenantId,
          options.creditnote,
          { allocations: [allocation] }
        );

        const created = response.body.allocations?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create allocation' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          allocation: {
            amount: created.amount,
            date: created.date,
            invoiceId: created.invoice?.invoiceID,
            invoiceNumber: created.invoice?.invoiceNumber,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  allocations
    .command('list-overpayments')
    .description('List overpayments')
    .option('-c, --contact <contactId>', 'Filter by contact ID')
    .option('-p, --page <page>', 'Page number', '1')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        
        let whereFilter: string | undefined;
        if (options.contact) {
          whereFilter = `Contact.ContactID==Guid("${options.contact}")`;
        }

        const response = await xero.accountingApi.getOverpayments(
          tenantId,
          undefined,
          whereFilter,
          'Date DESC',
          parseInt(options.page)
        );

        const overpayments = response.body.overpayments?.map(op => ({
          overpaymentId: op.overpaymentID,
          type: op.type,
          status: op.status,
          contact: op.contact?.name,
          contactId: op.contact?.contactID,
          date: op.date,
          total: op.total,
          remainingCredit: op.remainingCredit,
          currencyCode: op.currencyCode,
          allocations: op.allocations?.map(a => ({
            amount: a.amount,
            invoiceId: a.invoice?.invoiceID,
            invoiceNumber: a.invoice?.invoiceNumber,
          })),
        })) || [];

        console.log(JSON.stringify({ overpayments, count: overpayments.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  allocations
    .command('list-prepayments')
    .description('List prepayments')
    .option('-c, --contact <contactId>', 'Filter by contact ID')
    .option('-p, --page <page>', 'Page number', '1')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        
        let whereFilter: string | undefined;
        if (options.contact) {
          whereFilter = `Contact.ContactID==Guid("${options.contact}")`;
        }

        const response = await xero.accountingApi.getPrepayments(
          tenantId,
          undefined,
          whereFilter,
          'Date DESC',
          parseInt(options.page)
        );

        const prepayments = response.body.prepayments?.map(pp => ({
          prepaymentId: pp.prepaymentID,
          type: pp.type,
          status: pp.status,
          contact: pp.contact?.name,
          contactId: pp.contact?.contactID,
          date: pp.date,
          total: pp.total,
          remainingCredit: pp.remainingCredit,
          currencyCode: pp.currencyCode,
          allocations: pp.allocations?.map(a => ({
            amount: a.amount,
            invoiceId: a.invoice?.invoiceID,
            invoiceNumber: a.invoice?.invoiceNumber,
          })),
        })) || [];

        console.log(JSON.stringify({ prepayments, count: prepayments.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  allocations
    .command('list-creditnotes')
    .description('List credit notes')
    .option('-c, --contact <contactId>', 'Filter by contact ID')
    .option('-s, --status <status>', 'Filter by status (AUTHORISED, PAID, VOIDED)')
    .option('-p, --page <page>', 'Page number', '1')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        
        const filters: string[] = [];
        if (options.contact) {
          filters.push(`Contact.ContactID==Guid("${options.contact}")`);
        }
        if (options.status) {
          filters.push(`Status=="${options.status.toUpperCase()}"`);
        }
        
        const whereFilter = filters.length > 0 ? filters.join(' AND ') : undefined;

        const response = await xero.accountingApi.getCreditNotes(
          tenantId,
          undefined,
          whereFilter,
          'Date DESC',
          parseInt(options.page)
        );

        const creditNotes = response.body.creditNotes?.map(cn => ({
          creditNoteId: cn.creditNoteID,
          creditNoteNumber: cn.creditNoteNumber,
          type: cn.type,
          status: cn.status,
          contact: cn.contact?.name,
          contactId: cn.contact?.contactID,
          date: cn.date,
          total: cn.total,
          remainingCredit: cn.remainingCredit,
          currencyCode: cn.currencyCode,
          allocations: cn.allocations?.map(a => ({
            amount: a.amount,
            invoiceId: a.invoice?.invoiceID,
            invoiceNumber: a.invoice?.invoiceNumber,
          })),
        })) || [];

        console.log(JSON.stringify({ creditNotes, count: creditNotes.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });
}
