import fs from 'node:fs';
import path from 'node:path';
import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatAssetCreated } from '../formatters.js';
import { parseJsonOption, parseJsonObjectOption } from '../json.js';
import { getFrontendUrl } from '../config.js';
import { resolveTeams } from '../teams.js';

const VALID_TYPES = ['markdown', 'html', 'chart', 'code', 'text', 'json', 'collection', 'csv'] as const;
type ContentType = (typeof VALID_TYPES)[number];

export async function publish(
  filePath: string | undefined,
  options: {
    type: string;
    title?: string;
    content?: string;
    parent?: string;
    context?: string;
    refs?: string;
    schema?: string;
    alias?: string;
    headers?: boolean;
    fromCsv?: boolean;
    dryRun?: boolean;
    team?: string;
    folder?: string;
    metadata?: string;
  },
): Promise<void> {
  if (!VALID_TYPES.includes(options.type as ContentType)) {
    throw new CliError('INVALID_TYPE', `Type must be one of: ${VALID_TYPES.join(', ')}`);
  }

  let parsedMetadata: Record<string, unknown> | undefined;
  if (options.metadata) {
    parsedMetadata = parseJsonObjectOption(options.metadata, '--metadata');
  }

  // Validate: exactly one of {filePath, --content}. We treat empty string the
  // same as missing so `publish('', ...)` behaves like the no-arg case.
  const hasFile = filePath !== undefined && filePath !== '';
  const hasContent = options.content !== undefined;
  if (hasFile && hasContent) {
    throw new CliError('INVALID_ARGS', 'Provide either a file or --content, not both.');
  }
  if (!hasFile && !hasContent) {
    throw new CliError('INVALID_ARGS', 'Provide either a file or --content.');
  }

  // Inline content path: skip all filesystem reads and send the string directly.
  // Collections / CSV import still need a file, so this branch is text-like types only.
  if (hasContent) {
    if (!options.title) {
      throw new CliError('INVALID_ARGS', '--title is required when using --content.');
    }

    if (options.dryRun) {
      outputSuccess(
        {
          dryRun: true,
          action: 'would publish inline',
          title: options.title,
          type: options.type,
          size: options.content!.length,
        },
        formatAssetCreated,
      );
      return;
    }

    const { client, config } = requireAuthClient();
    const body: Record<string, unknown> = {
      type: options.type,
      content: options.content,
      title: options.title,
    };
    if (options.alias) body.alias = options.alias;
    if (options.parent) body.parentAssetId = options.parent;
    if (options.context) body.creatorContext = options.context;
    if (options.refs) body.inputReferences = options.refs.split(',').map((r) => r.trim());
    if (options.team) body.teams = resolveTeams(options.team.split(',').map((t) => t.trim()));
    if (options.folder) body.folder = options.folder;
    if (parsedMetadata) body.metadata = parsedMetadata;

    const { data } = await client.post('/v0/assets', body);
    const url = data.data.url || `${getFrontendUrl(config)}/s/${data.data.id}`;
    outputSuccess(
      { id: data.data.id, url, title: data.data.title, type: data.data.type },
      formatAssetCreated,
    );
    return;
  }

  // Collection → CSV import path: single-command creation of a collection from a CSV file
  if (options.type === 'collection' && options.fromCsv) {
    const absPath = path.resolve(filePath!);
    if (!fs.existsSync(absPath)) {
      throw new CliError('FILE_NOT_FOUND', `File not found: ${absPath}`);
    }
    const content = fs.readFileSync(absPath, 'utf-8');
    const title = options.title || path.basename(absPath, path.extname(absPath));

    if (options.dryRun) {
      outputSuccess({ dryRun: true, action: 'would create collection from csv', title, rows: content.split('\n').length }, formatAssetCreated);
      return;
    }

    const body: Record<string, unknown> = {
      type: 'collection',
      from_csv: true,
      content,
      title,
    };
    if (options.headers) body.headers = true;
    if (options.schema) body.schema = parseJsonOption(options.schema, '--schema');
    if (options.alias) body.alias = options.alias;
    if (options.parent) body.parentAssetId = options.parent;
    if (options.context) body.creatorContext = options.context;
    if (options.refs) body.inputReferences = options.refs.split(',').map((r) => r.trim());
    if (options.team) body.teams = resolveTeams(options.team.split(',').map((t) => t.trim()));
    if (options.folder) body.folder = options.folder;
    if (parsedMetadata) body.metadata = parsedMetadata;

    const { client, config } = requireAuthClient();
    const { data } = await client.post('/v0/assets', body);
    const url = data.data.url || `${getFrontendUrl(config)}/s/${data.data.id}`;
    outputSuccess({ id: data.data.id, url, title: data.data.title, type: data.data.type }, formatAssetCreated);
    return;
  }

  // Collection schema-only path
  if (options.type === 'collection') {
    let schema: unknown;
    if (options.schema) {
      schema = parseJsonOption(options.schema, '--schema');
    } else {
      const absPath = path.resolve(filePath!);
      if (!fs.existsSync(absPath)) {
        throw new CliError('FILE_NOT_FOUND', `File not found: ${absPath}`);
      }
      schema = parseJsonOption(fs.readFileSync(absPath, 'utf-8'), filePath!);
    }

    const title = options.title || 'Untitled Collection';

    if (options.dryRun) {
      outputSuccess({ dryRun: true, action: 'would create collection', title, schema }, formatAssetCreated);
      return;
    }

    const { client, config } = requireAuthClient();
    const body: Record<string, unknown> = { type: 'collection', title, schema };
    if (options.alias) body.alias = options.alias;
    if (options.parent) body.parentAssetId = options.parent;
    if (options.context) body.creatorContext = options.context;
    if (options.refs) body.inputReferences = options.refs.split(',').map((r) => r.trim());
    if (options.team) body.teams = resolveTeams(options.team.split(',').map((t) => t.trim()));
    if (options.folder) body.folder = options.folder;
    if (parsedMetadata) body.metadata = parsedMetadata;

    const { data } = await client.post('/v0/assets', body);
    const url = data.data.url || `${getFrontendUrl(config)}/s/${data.data.id}`;
    outputSuccess({ id: data.data.id, url, title: data.data.title, type: data.data.type }, formatAssetCreated);
    return;
  }

  const absPath = path.resolve(filePath!);
  if (!fs.existsSync(absPath)) {
    throw new CliError('FILE_NOT_FOUND', `File not found: ${absPath}`);
  }

  const title = options.title || path.basename(absPath);
  const size = fs.statSync(absPath).size;

  if (options.dryRun) {
    outputSuccess({ dryRun: true, action: 'would publish', file: absPath, title, type: options.type, size }, formatAssetCreated);
    return;
  }

  const { client, config } = requireAuthClient();
  const content = fs.readFileSync(absPath, 'utf-8');

  const body: Record<string, unknown> = {
    type: options.type,
    content,
    title,
  };
  if (options.alias) body.alias = options.alias;
  if (options.parent) body.parentAssetId = options.parent;
  if (options.context) body.creatorContext = options.context;
  if (options.refs) body.inputReferences = options.refs.split(',').map((r) => r.trim());
  if (options.team) body.teams = resolveTeams(options.team.split(',').map((t) => t.trim()));
  if (options.folder) body.folder = options.folder;
  if (parsedMetadata) body.metadata = parsedMetadata;

  const { data } = await client.post('/v0/assets', body);

  const url = data.data.url || `${getFrontendUrl(config)}/s/${data.data.id}`;
  outputSuccess({
    id: data.data.id,
    url,
    title: data.data.title,
    type: data.data.type,
  }, formatAssetCreated);
}
