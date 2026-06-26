import http from 'http';
import { receiveEmail } from '../primitives/email.js';

/**
 * Webhook Server — listens for incoming webhooks and dispatches to handlers.
 *
 * Usage:
 *   const server = new WebhookServer({ port: 8430 });
 *   server.on('/github', (payload) => console.log('GitHub event:', payload));
 *   server.on('/stripe', (payload) => console.log('Payment:', payload));
 *   server.start();
 *
 * Built-in routes:
 *   POST /email — receives inbound email from Cloudflare Email Worker
 *
 * Integrates with observe() — when observe uses method: 'webhook',
 * the observer registers a path on this server.
 */
class WebhookServer {
  constructor(options = {}) {
    this.port = options.port || 8430;
    this.host = options.host || '0.0.0.0';
    this.handlers = new Map();
    this.server = null;
    this.requestLog = [];
    this.maxLogSize = options.maxLogSize || 1000;

    // Register built-in email webhook handler
    if (options.email !== false) {
      this.on('/email', (payload) => {
        receiveEmail(payload);
      });
    }
  }

  /**
   * Register a handler for a webhook path.
   *
   * @param {string} path - URL path to listen on (e.g. '/github')
   * @param {function} handler - (payload, headers, request) => void
   * @returns {WebhookServer} this (for chaining)
   */
  on(path, handler) {
    // Normalize path
    if (!path.startsWith('/')) path = `/${path}`;
    this.handlers.set(path, handler);
    console.log(`[webhook] Registered handler: ${path}`);
    return this;
  }

  /**
   * Remove a handler for a path.
   */
  off(path) {
    if (!path.startsWith('/')) path = `/${path}`;
    this.handlers.delete(path);
    console.log(`[webhook] Unregistered handler: ${path}`);
    return this;
  }

  /**
   * Start the webhook server.
   */
  async start() {
    return new Promise((resolve, reject) => {
      this.server = http.createServer((req, res) => {
        this._handleRequest(req, res);
      });

      this.server.on('error', (err) => {
        console.log(`[webhook] Server error: ${err.message}`);
        reject(err);
      });

      this.server.listen(this.port, this.host, () => {
        console.log(`[webhook] Server listening on ${this.host}:${this.port}`);
        console.log(`[webhook] ${this.handlers.size} handlers registered`);
        resolve(this);
      });
    });
  }

  /**
   * Stop the webhook server.
   */
  async stop() {
    return new Promise((resolve) => {
      if (!this.server) {
        resolve();
        return;
      }

      this.server.close(() => {
        console.log(`[webhook] Server stopped`);
        this.server = null;
        resolve();
      });
    });
  }

  /**
   * Get request log.
   */
  getLog() {
    return [...this.requestLog];
  }

  /**
   * List registered paths.
   */
  listPaths() {
    return Array.from(this.handlers.keys());
  }

  /**
   * Handle an incoming request.
   */
  _handleRequest(req, res) {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const path = url.pathname;
    const method = req.method;

    // Health check
    if (path === '/health' || path === '/') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 'ok',
        handlers: Array.from(this.handlers.keys()),
        requestCount: this.requestLog.length,
      }));
      return;
    }

    // List handlers
    if (path === '/handlers') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        handlers: Array.from(this.handlers.keys()),
        observeWebhooks: globalThis.__reachWebhooks
          ? Array.from(globalThis.__reachWebhooks.keys())
          : [],
      }));
      return;
    }

    // Collect request body
    let body = '';
    req.on('data', (chunk) => {
      body += chunk.toString();
      // Limit body size to 1MB
      if (body.length > 1048576) {
        res.writeHead(413);
        res.end('Payload too large');
        req.destroy();
      }
    });

    req.on('end', () => {
      let payload;
      try {
        payload = body ? JSON.parse(body) : {};
      } catch {
        payload = { raw: body };
      }

      // Log the request
      const logEntry = {
        timestamp: new Date().toISOString(),
        method,
        path,
        headers: {
          'content-type': req.headers['content-type'],
          'user-agent': req.headers['user-agent'],
          'x-github-event': req.headers['x-github-event'],
          'x-hub-signature-256': req.headers['x-hub-signature-256'] ? '[present]' : undefined,
          'stripe-signature': req.headers['stripe-signature'] ? '[present]' : undefined,
        },
        payloadSize: body.length,
      };

      this.requestLog.push(logEntry);
      if (this.requestLog.length > this.maxLogSize) {
        this.requestLog.shift();
      }

      // Check registered handlers
      const handler = this.handlers.get(path);
      if (handler) {
        try {
          handler(payload, req.headers, req);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ received: true, path }));
          return;
        } catch (e) {
          console.log(`[webhook] Handler error for ${path}: ${e.message}`);
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
          return;
        }
      }

      // Check observe webhooks (registered via observe(..., { method: 'webhook' }))
      if (globalThis.__reachWebhooks) {
        const observeHandler = globalThis.__reachWebhooks.get(path);
        if (observeHandler && observeHandler.callback) {
          try {
            observeHandler.callback({
              type: 'webhook',
              target: observeHandler.target,
              path,
              payload,
              headers: req.headers,
              timestamp: new Date().toISOString(),
            });
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ received: true, path, observer: observeHandler.id }));
            return;
          } catch (e) {
            console.log(`[webhook] Observer handler error: ${e.message}`);
          }
        }
      }

      // No handler found
      console.log(`[webhook] No handler for ${method} ${path}`);
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'No handler registered for this path', path }));
    });
  }
}

export { WebhookServer };
export default WebhookServer;
