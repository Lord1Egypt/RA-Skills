import fs from 'node:fs';
import path from 'node:path';
import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatCollectionRows, formatRowsAppended, formatRowUpdated, formatRowsDeleted } from '../formatters.js';
import { parseJsonObjectArrayOption, parseJsonObjectOption } from '../json.js';

export async function collectionAppend(
  uuid: string,
  options: { data?: string; file?: string },
): Promise<void> {
  let rows: Record<string, unknown>[];

  if (options.file) {
    const absPath = path.resolve(options.file);
    if (!fs.existsSync(absPath)) {
      throw new CliError('FILE_NOT_FOUND', `File not found: ${absPath}`);
    }
    rows = parseJsonObjectArrayOption(fs.readFileSync(absPath, 'utf-8'), '--file');
  } else if (options.data) {
    rows = parseJsonObjectArrayOption(options.data, '--data');
  } else {
    throw new CliError('MISSING_FIELD', 'Provide --data or --file');
  }

  const { client } = requireAuthClient();
  const { data } = await client.post(`/v0/assets/${uuid}/rows`, { rows });
  outputSuccess({ rows: data.data, count: data.data.length }, formatRowsAppended);
}

export async function collectionRows(
  uuid: string,
  options: { limit?: string; after?: string; sortBy?: string; sortOrder?: string; filter?: string[] },
): Promise<void> {
  const { client } = requireAuthClient();
  const params: Record<string, string> = {};
  if (options.limit) params.limit = options.limit;
  if (options.after) params.after = options.after;
  if (options.sortBy) params.sort_by = options.sortBy;
  if (options.sortOrder) params.sort_order = options.sortOrder;
  if (options.filter) {
    for (const f of options.filter) {
      const eq = f.indexOf('=');
      if (eq > 0) params[`filter.${f.slice(0, eq)}`] = f.slice(eq + 1);
    }
  }

  const { data } = await client.get(`/v0/assets/${uuid}/rows`, { params });
  outputSuccess(data.data, formatCollectionRows);
}

export async function collectionUpdate(
  uuid: string,
  rowId: string,
  options: { data: string },
): Promise<void> {
  const parsed = parseJsonObjectOption(options.data, '--data');
  const { client } = requireAuthClient();
  const { data } = await client.put(`/v0/assets/${uuid}/rows/${rowId}`, { data: parsed });
  outputSuccess(data.data, formatRowUpdated);
}

export async function collectionDelete(
  uuid: string,
  options: { rows: string },
): Promise<void> {
  const ids = options.rows.split(',').map((s) => s.trim());
  const { client } = requireAuthClient();
  await client.delete(`/v0/assets/${uuid}/rows`, { data: { row_ids: ids } });
  outputSuccess({ deleted: ids.length }, formatRowsDeleted);
}
