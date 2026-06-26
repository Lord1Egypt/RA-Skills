import { Command } from 'commander';
import { Contact, Phone, Address } from 'xero-node';
import { getAuthenticatedClient, getActiveTenantId, formatApiError } from '../auth/index.js';

export function registerContactCommands(program: Command): void {
  const contacts = program
    .command('contacts')
    .description('Manage Xero contacts');

  contacts
    .command('list')
    .description('List contacts')
    .option('-s, --search <name>', 'Search by name')
    .option('-p, --page <page>', 'Page number', '1')
    .option('--customers', 'Only show customers')
    .option('--suppliers', 'Only show suppliers')
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
        
        filters.push('ContactStatus=="ACTIVE"');
        
        if (options.search) {
          filters.push(`Name.Contains("${options.search}")`);
        }
        if (options.customers) {
          filters.push('IsCustomer==true');
        }
        if (options.suppliers) {
          filters.push('IsSupplier==true');
        }
        
        whereFilter = filters.join(' AND ');

        const response = await xero.accountingApi.getContacts(
          tenantId,
          undefined,
          whereFilter,
          'Name ASC',
          undefined,
          parseInt(options.page),
          false,
          true
        );

        const contactList = response.body.contacts?.map(c => ({
          contactId: c.contactID,
          name: c.name,
          firstName: c.firstName,
          lastName: c.lastName,
          emailAddress: c.emailAddress,
          isCustomer: c.isCustomer,
          isSupplier: c.isSupplier,
          accountNumber: c.accountNumber,
        })) || [];

        console.log(JSON.stringify({ contacts: contactList, count: contactList.length }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  contacts
    .command('get <contactId>')
    .description('Get contact details')
    .action(async (contactId: string) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);
        const response = await xero.accountingApi.getContact(tenantId, contactId);

        const c = response.body.contacts?.[0];
        if (!c) {
          console.error(JSON.stringify({ error: 'Contact not found' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          contactId: c.contactID,
          name: c.name,
          firstName: c.firstName,
          lastName: c.lastName,
          emailAddress: c.emailAddress,
          phones: c.phones?.filter(p => p.phoneNumber).map(p => ({
            type: p.phoneType,
            number: p.phoneNumber,
          })),
          addresses: c.addresses?.filter(a => a.addressLine1).map(a => ({
            type: a.addressType,
            line1: a.addressLine1,
            line2: a.addressLine2,
            city: a.city,
            region: a.region,
            postalCode: a.postalCode,
            country: a.country,
          })),
          isCustomer: c.isCustomer,
          isSupplier: c.isSupplier,
          taxNumber: c.taxNumber,
          accountNumber: c.accountNumber,
          defaultCurrency: c.defaultCurrency,
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });

  contacts
    .command('create')
    .description('Create a new contact')
    .requiredOption('-n, --name <name>', 'Contact name (company or person)')
    .option('-f, --first-name <firstName>', 'First name')
    .option('-l, --last-name <lastName>', 'Last name')
    .option('-e, --email <email>', 'Email address')
    .option('-p, --phone <phone>', 'Phone number')
    .option('--customer', 'Mark as customer')
    .option('--supplier', 'Mark as supplier')
    .action(async (options) => {
      try {
        const xero = await getAuthenticatedClient();
        if (!xero) {
          console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
          process.exit(1);
        }

        const tenantId = await getActiveTenantId(xero);

        const contact: Contact = {
          name: options.name,
          firstName: options.firstName,
          lastName: options.lastName,
          emailAddress: options.email,
          isCustomer: options.customer || false,
          isSupplier: options.supplier || false,
        };

        if (options.phone) {
          contact.phones = [{
            phoneType: Phone.PhoneTypeEnum.DEFAULT,
            phoneNumber: options.phone,
          }];
        }

        const response = await xero.accountingApi.createContacts(
          tenantId,
          { contacts: [contact] }
        );

        const created = response.body.contacts?.[0];
        if (!created) {
          console.error(JSON.stringify({ error: 'Failed to create contact' }));
          process.exit(1);
        }

        console.log(JSON.stringify({
          success: true,
          contact: {
            contactId: created.contactID,
            name: created.name,
            emailAddress: created.emailAddress,
          }
        }, null, 2));
      } catch (err) {
        console.error(JSON.stringify({ error: formatApiError(err) }));
        process.exit(1);
      }
    });
}
