import express, { Request, Response } from 'express';
import { XeroClient } from 'xero-node';
import { tokenStore } from './token-store.js';
import type { Server } from 'http';

const PORT = 5001;

export interface OAuthResult {
  success: boolean;
  error?: string;
}

export function startOAuthServer(xero: XeroClient): Promise<OAuthResult> {
  return new Promise((resolve) => {
    const app = express();
    let server: Server;

    app.get('/callback', async (req: Request, res: Response) => {
      try {
        const callbackUrl = `http://localhost:${PORT}${req.url}`;
        const tokenSet = await xero.apiCallback(callbackUrl);
        await xero.updateTenants();
        
        const tenants = xero.tenants;
        const activeTenantId = tenants.length > 0 ? tenants[0].tenantId : undefined;
        tokenStore.save(tokenSet, activeTenantId);

        res.send(`
          <!DOCTYPE html>
          <html>
          <head>
            <title>Xero Authentication</title>
            <style>
              body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                     display: flex; align-items: center; justify-content: center; height: 100vh; 
                     margin: 0; background: #f5f5f5; }
              .container { text-align: center; background: white; padding: 40px; border-radius: 8px; 
                          box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
              .success { color: #22c55e; font-size: 48px; }
              h1 { color: #333; margin-top: 20px; }
              p { color: #666; }
            </style>
          </head>
          <body>
            <div class="container">
              <div class="success">✓</div>
              <h1>Authentication Successful!</h1>
              <p>You can close this window and return to your terminal.</p>
              ${tenants.length > 0 ? `<p>Connected to: <strong>${tenants[0].tenantName}</strong></p>` : ''}
            </div>
          </body>
          </html>
        `);

        setTimeout(() => {
          server.close(() => {
            resolve({ success: true });
          });
        }, 1000);

      } catch (err) {
        console.error('OAuth callback error:', err);
        let error = 'Unknown error during authentication';
        if (err instanceof Error) {
          error = err.message;
          const anyErr = err as unknown as Record<string, unknown>;
          if (anyErr.response) {
            console.error('Response:', JSON.stringify(anyErr.response, null, 2));
            const resp = anyErr.response as Record<string, unknown>;
            if (resp.body) error = JSON.stringify(resp.body);
          }
        }
        
        res.status(500).send(`
          <!DOCTYPE html>
          <html>
          <head>
            <title>Xero Authentication Error</title>
            <style>
              body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                     display: flex; align-items: center; justify-content: center; height: 100vh; 
                     margin: 0; background: #f5f5f5; }
              .container { text-align: center; background: white; padding: 40px; border-radius: 8px; 
                          box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 500px; }
              .error { color: #ef4444; font-size: 48px; }
              h1 { color: #333; margin-top: 20px; }
              p { color: #666; }
              code { background: #f5f5f5; padding: 10px; display: block; margin-top: 10px; 
                    border-radius: 4px; word-break: break-all; }
            </style>
          </head>
          <body>
            <div class="container">
              <div class="error">✗</div>
              <h1>Authentication Failed</h1>
              <p>Please try again.</p>
              <code>${error}</code>
            </div>
          </body>
          </html>
        `);

        setTimeout(() => {
          server.close(() => {
            resolve({ success: false, error });
          });
        }, 1000);
      }
    });

    app.get('/health', (_req: Request, res: Response) => {
      res.json({ status: 'ok', waiting: true });
    });

    server = app.listen(PORT, () => {});

    server.on('error', (err: NodeJS.ErrnoException) => {
      if (err.code === 'EADDRINUSE') {
        resolve({ success: false, error: `Port ${PORT} is already in use. Please close any other OAuth sessions.` });
      } else {
        resolve({ success: false, error: err.message });
      }
    });
  });
}
