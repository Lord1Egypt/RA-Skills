import type { WebhookMessage } from './types';

interface SendOptions {
  /** Thread key for threading messages together */
  threadKey?: string;
  /** If true, replies to existing thread or falls back to new thread */
  replyToThread?: boolean;
}

/**
 * Send a message to Google Chat via incoming webhook.
 *
 * @param webhookUrl - The webhook URL from Google Chat space settings
 * @param message - WebhookMessage (use buildCard or buildText to create)
 * @param options - Threading options
 *
 * @example
 *   // Simple text
 *   await sendWebhook(url, { text: '*Hello* from webhook' });
 *
 *   // Card message
 *   const card = buildCard({ cardId: 'test', title: 'Test', sections: [...] });
 *   await sendWebhook(url, card);
 *
 *   // Threaded reply
 *   await sendWebhook(url, card, { threadKey: 'deploy-123', replyToThread: true });
 */
export async function sendWebhook(
  webhookUrl: string,
  message: WebhookMessage,
  options?: SendOptions
): Promise<void> {
  let url = webhookUrl;

  // Add threading parameters to URL
  if (options?.replyToThread && options?.threadKey) {
    const separator = url.includes('?') ? '&' : '?';
    url += `${separator}messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`;
  }

  // Add thread key to message body
  if (options?.threadKey) {
    message.thread = { threadKey: options.threadKey };
  }

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      `Google Chat webhook error ${response.status}: ${body}`
    );
  }
}

/**
 * Convenience: send a text message.
 */
export async function sendText(
  webhookUrl: string,
  text: string,
  options?: SendOptions
): Promise<void> {
  await sendWebhook(webhookUrl, { text }, options);
}
