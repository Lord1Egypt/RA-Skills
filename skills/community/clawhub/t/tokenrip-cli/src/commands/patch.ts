import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatAssetPatched } from '../formatters.js';
import { parseJsonObjectOption } from '../json.js';
import { getFrontendUrl } from '../config.js';

export async function patch(
  identifier: string,
  options: { metadata?: string; alias?: string },
): Promise<void> {
  if (!options.metadata && !options.alias) {
    throw new CliError('INVALID_ARGS', 'Provide at least one of --metadata or --alias.');
  }

  const body: Record<string, unknown> = {};
  if (options.metadata) {
    body.metadata = parseJsonObjectOption(options.metadata, '--metadata');
  }
  if (options.alias) {
    body.alias = options.alias;
  }

  const { client, config } = requireAuthClient();
  const { data } = await client.patch(`/v0/assets/${encodeURIComponent(identifier)}`, body);
  const url = `${getFrontendUrl(config)}/s/${data.data.id}`;
  outputSuccess({ ...data.data, url }, formatAssetPatched);
}
