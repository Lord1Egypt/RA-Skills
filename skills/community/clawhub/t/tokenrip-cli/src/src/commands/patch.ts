import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatAssetPatched } from '../formatters.js';
import { parseJsonObjectOption } from '../json.js';
import { getFrontendUrl } from '../config.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function patch(
  identifier: string,
  options: { metadata?: string; alias?: string; title?: string; description?: string },
): Promise<void> {
  if (!options.metadata && !options.alias && options.title === undefined && options.description === undefined) {
    throw new CliError('INVALID_ARGS', 'Provide at least one of --title, --description, --metadata, or --alias.');
  }

  const body: Record<string, unknown> = {};
  if (options.metadata) {
    body.metadata = parseJsonObjectOption(options.metadata, '--metadata');
  }
  if (options.alias) {
    body.alias = options.alias;
  }
  if (options.title !== undefined) {
    body.title = options.title;
  }
  if (options.description !== undefined) {
    body.description = options.description;
  }

  const id = parseAssetId(identifier);
  const { client, config } = requireAuthClient();
  const { data } = await client.patch(`/v0/assets/${id}`, body);
  const url = `${getFrontendUrl(config)}/s/${data.data.id}`;
  outputSuccess({ ...data.data, url }, formatAssetPatched);
}
