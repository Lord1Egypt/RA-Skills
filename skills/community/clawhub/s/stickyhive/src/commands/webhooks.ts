import { apiRequest, output } from '../api';

export async function listWebhooks() {
  output(await apiRequest('GET', '/webhooks/'));
}

export async function createWebhook(argv: { url: string; events: string }) {
  const events = argv.events.split(',').map(e => e.trim());
  output(await apiRequest('POST', '/webhooks/', { url: argv.url, events }));
}

export async function deleteWebhook(argv: { id: number }) {
  output(await apiRequest('DELETE', `/webhooks/${argv.id}/`));
}
