import type { CardWithId, CardHeader, CardSection, WebhookMessage, Thread } from './types';

interface BuildCardOptions {
  cardId: string;
  title: string;
  subtitle?: string;
  imageUrl?: string;
  imageType?: 'SQUARE' | 'CIRCLE';
  sections: CardSection[];
}

/**
 * Build a cardsV2 webhook message.
 *
 * Usage:
 *   const message = buildCard({ cardId: 'my-card', title: 'Hello', sections: [...] });
 *   await sendWebhook(webhookUrl, message);
 */
export function buildCard(
  options: BuildCardOptions,
  thread?: { threadKey: string }
): WebhookMessage {
  const header: CardHeader = {
    title: options.title,
    ...(options.subtitle && { subtitle: options.subtitle }),
    ...(options.imageUrl && { imageUrl: options.imageUrl }),
    ...(options.imageType && { imageType: options.imageType }),
  };

  const card: CardWithId = {
    cardId: options.cardId,
    card: {
      header,
      sections: options.sections,
    },
  };

  const message: WebhookMessage = {
    cardsV2: [card],
  };

  if (thread) {
    message.thread = { threadKey: thread.threadKey };
  }

  return message;
}

/**
 * Build a simple text webhook message.
 *
 * Remember: Google Chat uses *bold*, _italic_, ~strikethrough~, `code`,
 * and <url|text> for links. NOT standard Markdown.
 */
export function buildText(
  text: string,
  thread?: { threadKey: string }
): WebhookMessage {
  const message: WebhookMessage = { text };

  if (thread) {
    message.thread = { threadKey: thread.threadKey };
  }

  return message;
}
