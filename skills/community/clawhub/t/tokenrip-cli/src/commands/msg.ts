import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatMessageSent, formatMessages } from '../formatters.js';
import { resolveRecipient } from '../contacts.js';
import { parseJsonObjectOption } from '../json.js';

export async function msgSend(
  body: string,
  options: {
    to?: string;
    thread?: string;
    asset?: string;
    intent?: string;
    type?: string;
    data?: string;
    inReplyTo?: string;
  },
): Promise<void> {
  const targets = [options.to, options.thread, options.asset].filter(Boolean);
  if (targets.length === 0) {
    throw new CliError('MISSING_OPTION', 'Provide --to <recipient>, --thread <id>, or --asset <uuid>');
  }
  if (targets.length > 1) {
    throw new CliError('CONFLICTING_OPTIONS', 'Use only one of --to, --thread, or --asset');
  }

  const { client } = requireAuthClient();

  const payload: Record<string, unknown> = { body };
  if (options.intent) payload.intent = options.intent;
  if (options.type) payload.type = options.type;
  if (options.data) payload.data = parseJsonObjectOption(options.data, '--data');

  let endpoint: string;
  if (options.to) {
    payload.to = [resolveRecipient(options.to)];
    endpoint = '/v0/messages';
  } else if (options.asset) {
    endpoint = `/v0/assets/${options.asset}/messages`;
  } else {
    if (options.inReplyTo) payload.in_reply_to = options.inReplyTo;
    endpoint = `/v0/threads/${options.thread}/messages`;
  }

  const { data } = await client.post(endpoint, payload);
  outputSuccess(data.data, formatMessageSent);
}

export async function msgList(options: {
  thread?: string;
  asset?: string;
  since?: string;
  limit?: string;
}): Promise<void> {
  if (!options.thread && !options.asset) {
    throw new CliError('MISSING_OPTION', '--thread <id> or --asset <uuid> is required');
  }
  if (options.thread && options.asset) {
    throw new CliError('CONFLICTING_OPTIONS', 'Use --thread or --asset, not both');
  }

  const { client } = requireAuthClient();
  const params: Record<string, string> = {};
  if (options.since) params.since_sequence = options.since;
  if (options.limit) params.limit = options.limit;

  const endpoint = options.asset
    ? `/v0/assets/${options.asset}/messages`
    : `/v0/threads/${options.thread}/messages`;

  const { data } = await client.get(endpoint, { params });
  outputSuccess(data.data as unknown as Record<string, unknown>, formatMessages);
}
