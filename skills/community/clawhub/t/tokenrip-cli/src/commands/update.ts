import fs from 'node:fs';
import path from 'node:path';
import FormData from 'form-data';
import mime from 'mime-types';
import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatVersionCreated } from '../formatters.js';

const VALID_TYPES = ['markdown', 'html', 'chart', 'code', 'text', 'json', 'csv'] as const;
type ContentType = (typeof VALID_TYPES)[number];

export async function update(
  uuid: string,
  filePath: string,
  options: { type?: string; label?: string; context?: string; dryRun?: boolean },
): Promise<void> {
  const absPath = path.resolve(filePath);
  if (!fs.existsSync(absPath)) {
    throw new CliError('FILE_NOT_FOUND', `File not found: ${absPath}`);
  }

  if (options.type && !VALID_TYPES.includes(options.type as ContentType)) {
    throw new CliError('INVALID_TYPE', `Type must be one of: ${VALID_TYPES.join(', ')}`);
  }

  if (options.dryRun) {
    outputSuccess({ dryRun: true, action: 'would update', assetId: uuid, file: absPath }, formatVersionCreated);
    return;
  }

  const { client } = requireAuthClient();

  if (options.type) {
    // Content publish mode
    const content = fs.readFileSync(absPath, 'utf-8');
    const body: Record<string, unknown> = { type: options.type, content };
    if (options.label) body.label = options.label;
    if (options.context) body.creatorContext = options.context;

    const { data } = await client.post(`/v0/assets/${uuid}/versions`, body);
    outputSuccess(data.data, formatVersionCreated);
  } else {
    // File upload mode
    const form = new FormData();
    form.append('file', fs.createReadStream(absPath));
    if (options.label) form.append('label', options.label);
    if (options.context) form.append('creatorContext', options.context);

    const { data } = await client.post(`/v0/assets/${uuid}/versions`, form, {
      headers: form.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    });
    outputSuccess(data.data, formatVersionCreated);
  }
}
