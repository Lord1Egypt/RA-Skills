import { Command } from 'commander';
import { getAuthenticatedClient, tokenStore } from '../auth/index.js';

export function registerTenantCommands(program: Command): void {
  const tenants = program
    .command('tenants')
    .description('Manage Xero organizations (tenants)');

  tenants
    .command('list')
    .description('List connected Xero organizations')
    .action(async () => {
      const xero = await getAuthenticatedClient();
      
      if (!xero) {
        console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
        process.exit(1);
      }

      const activeTenantId = tokenStore.getActiveTenantId();
      
      const tenantList = xero.tenants.map(t => ({
        tenantId: t.tenantId,
        tenantName: t.tenantName,
        tenantType: t.tenantType,
        active: t.tenantId === activeTenantId,
      }));

      console.log(JSON.stringify({ tenants: tenantList }, null, 2));
    });

  tenants
    .command('select <tenantId>')
    .description('Set the active Xero organization')
    .action(async (tenantId: string) => {
      const xero = await getAuthenticatedClient();
      
      if (!xero) {
        console.error(JSON.stringify({ error: 'Not authenticated. Run: xero-cli auth login' }));
        process.exit(1);
      }

      const tenant = xero.tenants.find(t => t.tenantId === tenantId);
      
      if (!tenant) {
        console.error(JSON.stringify({ 
          error: 'Tenant not found',
          availableTenants: xero.tenants.map(t => ({ id: t.tenantId, name: t.tenantName }))
        }));
        process.exit(1);
      }

      tokenStore.setActiveTenantId(tenantId);
      
      console.log(JSON.stringify({
        success: true,
        message: `Active organization set to: ${tenant.tenantName}`,
        tenantId: tenant.tenantId,
        tenantName: tenant.tenantName,
      }, null, 2));
    });
}
