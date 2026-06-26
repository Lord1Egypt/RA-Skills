import { Command } from 'commander';
import open from 'open';
import { createXeroClient, getConsentUrl, startOAuthServer, tokenStore } from '../auth/index.js';

export function registerAuthCommands(program: Command): void {
  const auth = program
    .command('auth')
    .description('Manage Xero authentication');

  auth
    .command('login')
    .description('Authenticate with Xero (opens browser)')
    .action(async () => {
      try {
        const xero = createXeroClient();
        const consentUrl = await getConsentUrl();

        console.log('Opening browser for Xero authentication...');
        console.log('If browser does not open, visit:', consentUrl);
        
        const serverPromise = startOAuthServer(xero);
        await open(consentUrl);
        
        const result = await serverPromise;
        
        if (result.success) {
          console.log('\n✓ Authentication successful!');
          
          const tenants = xero.tenants;
          if (tenants.length > 0) {
            console.log(`Connected to: ${tenants[0].tenantName}`);
            if (tenants.length > 1) {
              console.log(`\nYou have ${tenants.length} organizations. Use 'xero-cli tenants list' to see all.`);
            }
          }
        } else {
          console.error('\n✗ Authentication failed:', result.error);
          process.exit(1);
        }
      } catch (err) {
        console.error('Error:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });

  auth
    .command('logout')
    .description('Clear stored Xero credentials')
    .action(() => {
      tokenStore.clear();
      console.log('✓ Logged out. Credentials cleared.');
    });

  auth
    .command('status')
    .description('Check authentication status')
    .action(() => {
      const hasTokens = tokenStore.hasTokens();
      
      if (!hasTokens) {
        console.log(JSON.stringify({
          authenticated: false,
          message: 'Not authenticated. Run: xero-cli auth login'
        }, null, 2));
        return;
      }

      const tokenInfo = tokenStore.getTokenInfo();
      const activeTenantId = tokenStore.getActiveTenantId();

      console.log(JSON.stringify({
        authenticated: true,
        tokenValid: tokenInfo.isValid,
        expiresAt: tokenInfo.expiresAt?.toISOString(),
        expiresIn: tokenInfo.expiresIn,
        activeTenantId,
      }, null, 2));
    });
}
