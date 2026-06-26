import { WebhookServer } from './utils/webhook-server.js';
const server = new WebhookServer({ port: 8430 });
server.start();
console.log('[reach] Webhook server running on port 8430');
