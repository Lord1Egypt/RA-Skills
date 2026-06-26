import { Command } from 'commander';
import { BankTransaction, LineItem } from 'xero-node';
import { readFileSync } from 'fs';
import { basename } from 'path';
import { getAuthenticatedClient, getActiveTenantId, formatApiError } from '../auth/index.js';

export function registerBankTransactionCommands(program: Command): void {
  const bankTxns = program
    .command('banktransactions')
    .description('Manage bank transactions (spend/receive money, overpayments, prepayments)');

  bankTxns
    .command('list')
    .description('List bank transactions')
    .option('-t, --type <type>', 'Filter by type (SPEND, RECEIVE, RECEIVE-OVERPAYMENT, SPEND-OVERPAYMENT, RECEIVE-PREPAYMENT, SPEND-PREPAYMENT)')
    .option('-r, --reconciled <boolean>', 'Filter by reconciled status (true/false)')
    .option('-c, --contact <contactId>', 'Filter by contact ID')
    .option('-b, --bank-account <accountId>', 'Filter by bank account ID')
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
        
        if (options.type) {
          filters.push(`Type=="${options.type.toUpperCase()}"`);
        }
        if (options.reconciled !== undefined) {
          filters.push(`IsReconciled==${options.reconciled.toLowerCase() === 'true'}`);
        }
        if (options.contact) {
          filters.push(`Contact.ContactID==Guid("${options.contact}")`);
        }
        if (options.bankAccount) {
          filters.push(`BankAccount.AccountID==Guid("${options.bankAccount}")`);
        }
        
        const whereFilter = filters.length > 0 ? filters.join(' AND ') : undefined;

        const response = await xero.accountingApi.getBankTransactions(
          tenantId,
          undefined,
          whereFilter,
          'Date DESC',
          parseInt(options.page)
        );

        const transactions = response.body.bankTransactions?.map(txn => ({
          bankTransactionId: txn.bankTransactionID,
          type: txn.type,
          status: txn.status,
          contact: txn.contact?.name,
          contactId: txn.contact?.contactID,
          date: txn.date,
          reference: txn.reference,
          total: txn.total,
          isReconciled: txn.isReconciled,
          bankAccount: txn.bankAccount?.name,
          bankAccountId: txn.bankAccount?.accountID,
          currencyCode: txn.currencyCode,
        })) || [];

        console.log(JSON.stringify({ bankTransactions: transactions, count: transactions.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  bankTxns
    .command('get <transactionId>')
    .description('Get bank transaction details')
    .action(async (transactionId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        const response = await xero.accountingApi.getBankTransaction(tenantId, transactionId);

        const txn = response.body.bankTransactions?.[0];
        if (!txn) {
          console.error(JSON.stringify({ error: 'Bank transaction not found' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          bankTransactionId: txn.bankTransactionID,
          type: txn.type,
          status: txn.status,
          reference: txn.reference,
          contact: {
            contactId: txn.contact?.contactID,
            name: txn.contact?.name,
          },
          bankAccount: {
            accountId: txn.bankAccount?.accountID,
            name: txn.bankAccount?.name,
            code: txn.bankAccount?.code,
          },
          date: txn.date,
          lineItems: txn.lineItems?.map(li => ({
            lineItemId: li.lineItemID,
            description: li.description,
            quantity: li.quantity,
            unitAmount: li.unitAmount,
            lineAmount: li.lineAmount,
            accountCode: li.accountCode,
            taxType: li.taxType,
          })),
          subTotal: txn.subTotal,
          totalTax: txn.totalTax,
          total: txn.total,
          isReconciled: txn.isReconciled,
          currencyCode: txn.currencyCode,
          updatedDateUTC: txn.updatedDateUTC,
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  bankTxns
    .command('create')
    .description('Create a bank transaction (spend/receive money)')
    .requiredOption('-t, --type <type>', 'Transaction type: SPEND, RECEIVE, RECEIVE-OVERPAYMENT, SPEND-OVERPAYMENT, RECEIVE-PREPAYMENT, SPEND-PREPAYMENT')
    .requiredOption('-b, --bank-account <accountId>', 'Bank account ID')
    .requiredOption('-c, --contact <contactId>', 'Contact ID')
    .requiredOption('-i, --items <json>', 'Line items as JSON array')
    .option('-d, --date <date>', 'Transaction date (YYYY-MM-DD)')
    .option('-r, --reference <reference>', 'Reference text')
    .option('--reconciled', 'Mark as reconciled')
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

        const typeMap: Record<string, BankTransaction.TypeEnum> = {
          'SPEND': BankTransaction.TypeEnum.SPEND,
          'RECEIVE': BankTransaction.TypeEnum.RECEIVE,
          'RECEIVE-OVERPAYMENT': BankTransaction.TypeEnum.RECEIVEOVERPAYMENT,
          'SPEND-OVERPAYMENT': BankTransaction.TypeEnum.SPENDOVERPAYMENT,
          'RECEIVE-PREPAYMENT': BankTransaction.TypeEnum.RECEIVEPREPAYMENT,
          'SPEND-PREPAYMENT': BankTransaction.TypeEnum.SPENDPREPAYMENT,
        };

        const txnType = typeMap[options.type.toUpperCase()];
        if (!txnType) {
          console.error(JSON.stringify({ 
            error: `Invalid type. Must be one of: ${Object.keys(typeMap).join(', ')}` 
          }));
          process.exit(1);
        }

        const bankTransaction: BankTransaction = {
          type: txnType,
          contact: { contactID: options.contact },
          bankAccount: { accountID: options.bankAccount },
          lineItems,
          date: options.date || new Date().toISOString().split('T')[0],
          reference: options.reference,
          isReconciled: options.reconciled || false,
        };

        const response = await xero.accountingApi.createBankTransactions(
          tenantId,
          { bankTransactions: [bankTransaction] }
        );

        const created = response.body.bankTransactions?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create bank transaction' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          bankTransaction: {
            bankTransactionId: created.bankTransactionID,
            type: created.type,
            status: created.status,
            total: created.total,
            isReconciled: created.isReconciled,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  bankTxns
    .command('update <transactionId>')
    .description('Update a bank transaction')
    .option('-i, --items <json>', 'Line items as JSON array (replaces existing)')
    .option('-d, --date <date>', 'Transaction date (YYYY-MM-DD)')
    .option('-r, --reference <reference>', 'Reference text')
    .option('-c, --contact <contactId>', 'Contact ID')
    .action(async (transactionId: string, options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        // First get existing transaction to preserve type and bank account
        const existing = await xero.accountingApi.getBankTransaction(tenantId, transactionId);
        const existingTxn = existing.body.bankTransactions?.[0];
        if (!existingTxn) {
          console.error(JSON.stringify({ error: 'Bank transaction not found' }));
          process.exit(1);
        }

        const updateData: BankTransaction = {
          bankTransactionID: transactionId,
          type: existingTxn.type,
          bankAccount: existingTxn.bankAccount,
          lineItems: existingTxn.lineItems || [],
        };

        if (options.items) {
          try {
            updateData.lineItems = JSON.parse(options.items);
          } catch {
            console.error(JSON.stringify({ error: 'Invalid JSON for line items' }));
            process.exit(1);
          }
        }

        if (options.date) {
          updateData.date = options.date;
        }

        if (options.reference) {
          updateData.reference = options.reference;
        }

        if (options.contact) {
          updateData.contact = { contactID: options.contact };
        }

        const response = await xero.accountingApi.updateBankTransaction(
          tenantId,
          transactionId,
          { bankTransactions: [updateData] }
        );

        const updated = response.body.bankTransactions?.[0];
        console.log(JSON.stringify({
          success: true,
          bankTransaction: {
            bankTransactionId: updated?.bankTransactionID,
            type: updated?.type,
            status: updated?.status,
            total: updated?.total,
            reference: updated?.reference,
            isReconciled: updated?.isReconciled,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  bankTxns
    .command('attach <transactionId> <filePath>')
    .description('Attach a file to a bank transaction')
    .action(async (transactionId: string, filePath: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        let fileContent: Buffer;
        try {
          fileContent = readFileSync(filePath);
        } catch {
          console.error(JSON.stringify({ error: `Cannot read file: ${filePath}` }));
          process.exit(1);
        }

        const fileName = basename(filePath);
        const mimeTypes: Record<string, string> = {
          '.pdf': 'application/pdf',
          '.png': 'image/png',
          '.jpg': 'image/jpeg',
          '.jpeg': 'image/jpeg',
          '.gif': 'image/gif',
          '.doc': 'application/msword',
          '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          '.xls': 'application/vnd.ms-excel',
          '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          '.csv': 'text/csv',
          '.txt': 'text/plain',
        };
        
        const ext = filePath.toLowerCase().slice(filePath.lastIndexOf('.'));
        const contentType = mimeTypes[ext] || 'application/octet-stream';

        const response = await xero.accountingApi.createBankTransactionAttachmentByFileName(
          tenantId,
          transactionId,
          fileName,
          fileContent,
          contentType
        );

        const attachment = response.body.attachments?.[0];
        console.log(JSON.stringify({
          success: true,
          attachment: {
            attachmentId: attachment?.attachmentID,
            fileName: attachment?.fileName,
            mimeType: attachment?.mimeType,
            contentLength: attachment?.contentLength,
            url: attachment?.url,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  bankTxns
    .command('attachments <transactionId>')
    .description('List attachments for a bank transaction')
    .action(async (transactionId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const response = await xero.accountingApi.getBankTransactionAttachments(
          tenantId,
          transactionId
        );

        const attachments = response.body.attachments?.map(att => ({
          attachmentId: att.attachmentID,
          fileName: att.fileName,
          mimeType: att.mimeType,
          contentLength: att.contentLength,
          url: att.url,
        })) || [];

        console.log(JSON.stringify({ attachments, count: attachments.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });
}
