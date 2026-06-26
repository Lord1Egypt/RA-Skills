import { Command } from 'commander';
import { Invoice, LineItem } from 'xero-node';
import { getAuthenticatedClient, getActiveTenantId, formatApiError } from '../auth/index.js';

export function registerInvoiceCommands(program: Command): void {
  const invoices = program
    .command('invoices')
    .description('Manage Xero invoices');

  invoices
    .command('list')
    .description('List invoices')
    .option('-s, --status <status>', 'Filter by status (DRAFT, AUTHORISED, PAID, VOIDED)')
    .option('-c, --contact <contactId>', 'Filter by contact ID')
    .option('-p, --page <page>', 'Page number', '1')
    .option('-l, --limit <limit>', 'Results per page (max 100)', '50')
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
        
        if (options.status) {
          filters.push(`Status=="${options.status.toUpperCase()}"`);
        }
        if (options.contact) {
          filters.push(`Contact.ContactID==Guid("${options.contact}")`);
        }
        
        if (filters.length > 0) {
          whereFilter = filters.join(' AND ');
        }

        const response = await xero.accountingApi.getInvoices(
          tenantId,
          undefined,
          whereFilter,
          'Date DESC',
          undefined,
          undefined,
          options.contact ? [options.contact] : undefined,
          options.status ? [options.status.toUpperCase()] : undefined,
          parseInt(options.page),
          false,
          false,
          4
        );

        const invoiceList = response.body.invoices?.map(inv => ({
          invoiceId: inv.invoiceID,
          invoiceNumber: inv.invoiceNumber,
          type: inv.type,
          status: inv.status,
          contact: inv.contact?.name,
          contactId: inv.contact?.contactID,
          date: inv.date,
          dueDate: inv.dueDate,
          total: inv.total,
          amountDue: inv.amountDue,
          amountPaid: inv.amountPaid,
          currencyCode: inv.currencyCode,
        })) || [];

        console.log(JSON.stringify({ invoices: invoiceList, count: invoiceList.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  invoices
    .command('get <invoiceId>')
    .description('Get invoice details')
    .action(async (invoiceId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        const response = await xero.accountingApi.getInvoice(tenantId, invoiceId);

        const inv = response.body.invoices?.[0];
        if (!inv) {
          console.error(JSON.stringify({ error: 'Invoice not found' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          invoiceId: inv.invoiceID,
          invoiceNumber: inv.invoiceNumber,
          type: inv.type,
          status: inv.status,
          reference: inv.reference,
          contact: {
            contactId: inv.contact?.contactID,
            name: inv.contact?.name,
          },
          date: inv.date,
          dueDate: inv.dueDate,
          lineItems: inv.lineItems?.map(li => ({
            description: li.description,
            quantity: li.quantity,
            unitAmount: li.unitAmount,
            lineAmount: li.lineAmount,
            accountCode: li.accountCode,
            taxType: li.taxType,
          })),
          subTotal: inv.subTotal,
          totalTax: inv.totalTax,
          total: inv.total,
          amountDue: inv.amountDue,
          amountPaid: inv.amountPaid,
          currencyCode: inv.currencyCode,
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  invoices
    .command('create')
    .description('Create a new invoice')
    .requiredOption('-c, --contact <contactId>', 'Contact ID')
    .requiredOption('-i, --items <json>', 'Line items as JSON array')
    .option('-t, --type <type>', 'Invoice type (ACCREC or ACCPAY)', 'ACCREC')
    .option('-d, --date <date>', 'Invoice date (YYYY-MM-DD)')
    .option('-u, --due-date <dueDate>', 'Due date (YYYY-MM-DD)')
    .option('-r, --reference <reference>', 'Reference text')
    .option('-s, --status <status>', 'Status (DRAFT or AUTHORISED)', 'DRAFT')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        let lineItems: LineItem[];
        try {
          lineItems = JSON.parse(options.items);
        } catch {
          console.error(JSON.stringify({ error: 'Invalid JSON for line items' }));
          process.exit(1);
        }

        const invoiceType = options.type.toUpperCase() === 'ACCPAY' 
          ? Invoice.TypeEnum.ACCPAY 
          : Invoice.TypeEnum.ACCREC;

        const invoiceStatus = options.status.toUpperCase() === 'AUTHORISED'
          ? Invoice.StatusEnum.AUTHORISED
          : Invoice.StatusEnum.DRAFT;

        const invoice: Invoice = {
          type: invoiceType,
          contact: { contactID: options.contact },
          lineItems,
          date: options.date || new Date().toISOString().split('T')[0],
          dueDate: options.dueDate,
          reference: options.reference,
          status: invoiceStatus,
        };

        const response = await xero.accountingApi.createInvoices(
          tenantId,
          { invoices: [invoice] },
          true,
          4
        );

        const created = response.body.invoices?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create invoice' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          invoice: {
            invoiceId: created.invoiceID,
            invoiceNumber: created.invoiceNumber,
            status: created.status,
            total: created.total,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  invoices
    .command('update <invoiceId>')
    .description('Update invoice status')
    .option('-s, --status <status>', 'New status (AUTHORISED, VOIDED)')
    .action(async (invoiceId: string, options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const updateData: Invoice = {
          invoiceID: invoiceId,
        };

        if (options.status) {
          const statusMap: Record<string, Invoice.StatusEnum> = {
            'AUTHORISED': Invoice.StatusEnum.AUTHORISED,
            'VOIDED': Invoice.StatusEnum.VOIDED,
          };
          updateData.status = statusMap[options.status.toUpperCase()];
        }

        const response = await xero.accountingApi.updateInvoice(
          tenantId,
          invoiceId,
          { invoices: [updateData] }
        );

        const updated = response.body.invoices?.[0];
        console.log(JSON.stringify({
          success: true,
          invoice: {
            invoiceId: updated?.invoiceID,
            invoiceNumber: updated?.invoiceNumber,
            status: updated?.status,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });
}
