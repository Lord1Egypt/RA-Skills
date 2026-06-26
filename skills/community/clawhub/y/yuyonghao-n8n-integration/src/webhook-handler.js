/**
 * n8n Integration - Webhook Handler
 * Receives and processes webhooks from n8n workflows
 */

const http = require('http');
const https = require('https');
const url = require('url');
const { EventEmitter } = require('events');

class WebhookHandler extends EventEmitter {
  constructor(options = {}) {
    super();
    this.port = options.port || 3000;
    this.path = options.path || '/webhook';
    this.secret = options.secret || process.env.WEBHOOK_SECRET;
    this.server = null;
    this.requestCount = 0;
  }

  /**
   * Start webhook server
   */
  start() {
    return new Promise((resolve, reject) => {
      this.server = http.createServer(async (req, res) => {
        const parsedUrl = url.parse(req.url, true);
        
        // Check path
        if (parsedUrl.pathname !== this.path) {
          res.writeHead(404);
          res.end('Not found');
          return;
        }

        // Only accept POST
        if (req.method !== 'POST') {
          res.writeHead(405);
          res.end('Method not allowed');
          return;
        }

        // Collect body
        let body = '';
        req.on('data', chunk => {
          body += chunk.toString();
        });

        req.on('end', async () => {
          try {
            const payload = JSON.parse(body);
            
            // Verify signature if secret is configured
            if (this.secret) {
              const signature = req.headers['x-n8n-signature'];
              if (!this.verifySignature(body, signature)) {
                res.writeHead(401);
                res.end('Invalid signature');
                return;
              }
            }

            this.requestCount++;
            
            // Emit event for processing
            this.emit('webhook', {
              payload,
              headers: req.headers,
              timestamp: new Date().toISOString(),
              requestId: this.requestCount
            });

            // Respond
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
              success: true,
              requestId: this.requestCount,
              received: new Date().toISOString()
            }));

          } catch (error) {
            console.error('[Webhook] Parse error:', error.message);
            res.writeHead(400);
            res.end('Invalid JSON');
          }
        });
      });

      this.server.listen(this.port, () => {
        console.log(`[Webhook] Server listening on port ${this.port}`);
        console.log(`[Webhook] Path: ${this.path}`);
        resolve();
      });

      this.server.on('error', reject);
    });
  }

  /**
   * Stop webhook server
   */
  stop() {
    return new Promise((resolve, reject) => {
      if (!this.server) {
        resolve();
        return;
      }

      this.server.close((err) => {
        if (err) reject(err);
        else {
          console.log('[Webhook] Server stopped');
          resolve();
        }
      });
    });
  }

  /**
   * Verify webhook signature
   */
  verifySignature(body, signature) {
    if (!signature) return false;
    
    const crypto = require('crypto');
    const expected = crypto
      .createHmac('sha256', this.secret)
      .update(body)
      .digest('hex');
    
    return signature === `sha256=${expected}`;
  }

  /**
   * Get server status
   */
  getStatus() {
    return {
      running: !!this.server,
      port: this.port,
      path: this.path,
      requestCount: this.requestCount
    };
  }
}

module.exports = { WebhookHandler };
