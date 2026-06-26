import { Command } from 'commander';
import { Payment, PaymentDelete } from 'xero-node';
import { getAuthenticatedClient, getActiveTenantId, formatApiError } from '../auth/index.js';

export function registerPaymentCommands(program: Command): void {
  const payments = program
    .command('payments')
    .description('Manage payments for invoices');

  payments
    .command('list')
    .description('List payments')
    .option('-i, --invoice <invoiceId>', 'Filter by invoice ID')
    .option('-r, --reconciled <boolean>', 'Filter by reconciled status (true/false)')
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
        
        if (options.invoice) {
          filters.push(`Invoice.InvoiceID==Guid("${options.invoice}")`);
        }
        if (options.reconciled !== undefined) {
          filters.push(`IsReconciled==${options.reconciled.toLowerCase() === 'true'}`);
        }
        
        const whereFilter = filters.length > 0 ? filters.join(' AND ') : undefined;

        const response = await xero.accountingApi.getPayments(
          tenantId,
          undefined,
          whereFilter,
          'Date DESC',
          parseInt(options.page)
        );

        const paymentList = response.body.payments?.map(pmt => ({
          paymentId: pmt.paymentID,
          date: pmt.date,
          amount: pmt.amount,
          reference: pmt.reference,
          isReconciled: pmt.isReconciled,
          status: pmt.status,
          paymentType: pmt.paymentType,
          invoice: pmt.invoice ? {
            invoiceId: pmt.invoice.invoiceID,
            invoiceNumber: pmt.invoice.invoiceNumber,
          } : null,
          account: pmt.account ? {
            accountId: pmt.account.accountID,
            name: pmt.account.name,
            code: pmt.account.code,
          } : null,
        })) || [];

        console.log(JSON.stringify({ payments: paymentList, count: paymentList.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  payments
    .command('get <paymentId>')
    .description('Get payment details')
    .action(async (paymentId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        const response = await xero.accountingApi.getPayment(tenantId, paymentId);

        const pmt = response.body.payments?.[0];
        if (!pmt) {
          console.error(JSON.stringify({ error: 'Payment not found' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          paymentId: pmt.paymentID,
          date: pmt.date,
          amount: pmt.amount,
          reference: pmt.reference,
          isReconciled: pmt.isReconciled,
          status: pmt.status,
          paymentType: pmt.paymentType,
          invoice: pmt.invoice ? {
            invoiceId: pmt.invoice.invoiceID,
            invoiceNumber: pmt.invoice.invoiceNumber,
            type: pmt.invoice.type,
            contact: pmt.invoice.contact?.name,
          } : null,
          account: pmt.account ? {
            accountId: pmt.account.accountID,
            name: pmt.account.name,
            code: pmt.account.code,
          } : null,
          updatedDateUTC: pmt.updatedDateUTC,
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  payments
    .command('create')
    .description('Create a payment for an invoice')
    .requiredOption('-i, --invoice <invoiceId>', 'Invoice ID to apply payment to')
    .requiredOption('-a, --account <accountId>', 'Bank account ID for the payment')
    .requiredOption('-m, --amount <amount>', 'Payment amount')
    .option('-d, --date <date>', 'Payment date (YYYY-MM-DD)')
    .option('-r, --reference <reference>', 'Reference text')
    .option('--reconciled', 'Mark payment as already reconciled')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const payment: Payment = {
          invoice: { invoiceID: options.invoice },
          account: { accountID: options.account },
          amount: parseFloat(options.amount),
          date: options.date || new Date().toISOString().split('T')[0],
          reference: options.reference,
          isReconciled: options.reconciled || false,
        };

        const response = await xero.accountingApi.createPayment(
          tenantId,
          payment
        );

        const created = response.body.payments?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create payment' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          payment: {
            paymentId: created.paymentID,
            amount: created.amount,
            date: created.date,
            isReconciled: created.isReconciled,
            status: created.status,
            invoiceId: created.invoice?.invoiceID,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  payments
    .command('delete <paymentId>')
    .description('Delete/void a payment')
    .action(async (paymentId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const paymentDelete: PaymentDelete = {
          status: 'DELETED',
        };

        const response = await xero.accountingApi.deletePayment(
          tenantId,
          paymentId,
          paymentDelete
        );

        const deleted = response.body.payments?.[0];
        console.log(JSON.stringify({
          success: true,
          payment: {
            paymentId: deleted?.paymentID,
            status: deleted?.status,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });
}
