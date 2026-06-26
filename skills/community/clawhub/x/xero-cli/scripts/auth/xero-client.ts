import { XeroClient } from 'xero-node';
import { tokenStore } from './token-store.js';

const XERO_CLIENT_ID = process.env.XERO_CLIENT_ID || '';
const XERO_CLIENT_SECRET = process.env.XERO_CLIENT_SECRET || '';
const XERO_REDIRECT_URI = process.env.XERO_REDIRECT_URI || 'http://localhost:5001/callback';
const XERO_SCOPES = process.env.XERO_SCOPES || 
  'openid offline_access accounting.contacts accounting.settings accounting.invoices accounting.payments accounting.banktransactions accounting.attachments';

export function createXeroClient(): XeroClient {
  if (!XERO_CLIENT_ID || !XERO_CLIENT_SECRET) {
    throw new Error(
      'Missing Xero credentials. Set XERO_CLIENT_ID and XERO_CLIENT_SECRET environment variables.\n\n' +
      'For OpenClaw: Add to your openclaw.json skills config:\n' +
      '  "xero": { "env": { "XERO_CLIENT_ID": "...", "XERO_CLIENT_SECRET": "..." } }\n\n' +
      'Get credentials from: https://developer.xero.com/app/manage'
    );
  }

  return new XeroClient({
    clientId: XERO_CLIENT_ID,
    clientSecret: XERO_CLIENT_SECRET,
    redirectUris: [XERO_REDIRECT_URI],
    scopes: XERO_SCOPES.split(' '),
  });
}

export async function getConsentUrl(): Promise<string> {
  const xero = createXeroClient();
  return await xero.buildConsentUrl();
}

export async function getAuthenticatedClient(): Promise<XeroClient | null> {
  const storedTokenSet = tokenStore.getTokenSet();
  
  if (!storedTokenSet) {
    return null;
  }

  const xero = createXeroClient();
  xero.setTokenSet(storedTokenSet);

  if (tokenStore.isTokenExpired()) {
    try {
      const newTokenSet = await xero.refreshWithRefreshToken(
        XERO_CLIENT_ID,
        XERO_CLIENT_SECRET,
        storedTokenSet.refresh_token!
      );
      
      const activeTenantId = tokenStore.getActiveTenantId() || undefined;
      tokenStore.save(newTokenSet, activeTenantId);
      xero.setTokenSet(newTokenSet);
    } catch (err) {
      console.error('Token refresh failed:', err instanceof Error ? err.message : err);
      return null;
    }
  }

  try {
    await xero.updateTenants();
  } catch (err) {
    console.error('Failed to update tenants:', err instanceof Error ? err.message : err);
  }

  return xero;
}

function getFirstTenantId(xero: XeroClient): string | null {
  const firstTenant = xero.tenants[0];
  return firstTenant?.tenantId ?? null;
}

export async function getActiveTenantId(xero: XeroClient): Promise<string> {
  let tenantId = tokenStore.getActiveTenantId();
  
  if (!tenantId && xero.tenants.length > 0) {
    const firstId = getFirstTenantId(xero);
    if (firstId) {
      tenantId = firstId;
      tokenStore.setActiveTenantId(firstId);
    }
  }
  
  const tenantExists = tenantId && xero.tenants.some(t => t.tenantId === tenantId);
  
  if (tenantId && !tenantExists) {
    if (xero.tenants.length > 0) {
      const firstId = getFirstTenantId(xero);
      if (firstId) {
        tenantId = firstId;
        tokenStore.setActiveTenantId(firstId);
      }
    } else {
      throw new Error('No Xero organizations found. Please reconnect your Xero account.');
    }
  }
  
  if (!tenantId) {
    throw new Error('No Xero organization selected. Run: xero-cli tenants list');
  }
  
  return tenantId;
}

export function formatApiError(err: unknown): string {
  if (err instanceof Error) {
    const anyErr = err as unknown as Record<string, unknown>;
    if (anyErr.response && typeof anyErr.response === 'object') {
      const response = anyErr.response as Record<string, unknown>;
      if (response.body && typeof response.body === 'object') {
        const body = response.body as Record<string, unknown>;
        if (body.Message) {
          return String(body.Message);
        }
        if (body.Detail) {
          return String(body.Detail);
        }
      }
      if (response.statusCode) {
        return `API Error (${response.statusCode}): ${err.message}`;
      }
    }
    return err.message;
  }
  return String(err);
}
