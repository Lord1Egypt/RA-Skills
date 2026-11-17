// lib/models.ts
import 'server-only';

/** One row of a model's price list. `inputs` is empty when one price fits every setting. */
export type PriceRow = { price: number; priceMethod: string; inputs?: Record<string, unknown> };

export type ModelSummary = { id: string; title: string; prices: PriceRow[] };

type ToolItem = { cleanslugowner?: string; cleanslugproject?: string; title?: string; dynamicprice?: unknown };

const PER: Record<string, string> = {
  cpr: 'per run',
  cpo: 'per output',
  cps: 'per second of run time',
  cpt: 'per token',
  'cp-pixel': 'per 1024x1024 tile',
  'cp-promptlength': 'per prompt character',
  'cp-audiosecondslength': 'per second of input audio',
  'cp-outputVideoLength': 'per second of video',
};

/** Tool/List and Tool/Detail are public: they need no key. */
async function catalog<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const response = await fetch(`https://api.wiro.ai/v1${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return (await response.json()) as T;
}

/** `dynamicprice` is an array in Tool/Detail and JSON text in Tool/List. */
function parsePrices(value: unknown): PriceRow[] {
  const rows: unknown = typeof value === 'string' ? JSON.parse(value || '[]') : value;
  return Array.isArray(rows) ? (rows as PriceRow[]) : [];
}

/** Searches the catalog, optionally within categories such as "text-to-image" or "text-to-speech". */
export async function findModels(search: string, categories: string[] = []): Promise<ModelSummary[]> {
  const { tool = [] } = await catalog<{ tool?: ToolItem[] }>('/Tool/List', {
    search,
    categories,
    start: '0',
    limit: '20',
    summary: true,
    hideworkflows: true,
  });
  return tool.map((item) => ({
    id: `${item.cleanslugowner}/${item.cleanslugproject}`,
    title: item.title ?? '',
    prices: parsePrices(item.dynamicprice),
  }));
}

/** One model's price list, from Tool/Detail, which also lists its inputs in `parameters[].items[]`. */
export async function getPrices(model: string): Promise<PriceRow[]> {
  const [slugowner, slugproject] = model.split('/');
  const { tool } = await catalog<{ tool?: ToolItem[] }>('/Tool/Detail', { slugowner, slugproject });
  return parsePrices(tool?.[0]?.dynamicprice);
}

/** The row for the settings you will send: one whose inputs all match, or else the row without inputs. */
export function priceFor(prices: PriceRow[], params: Record<string, unknown>): PriceRow | undefined {
  const matches = (row: PriceRow) =>
    Object.entries(row.inputs ?? {}).every(([key, value]) => String(params[key]) === String(value));
  return (
    prices.find((row) => Object.keys(row.inputs ?? {}).length > 0 && matches(row)) ??
    prices.find((row) => Object.keys(row.inputs ?? {}).length === 0)
  );
}

/** "$0.005 per run", "$0.00008 per prompt character". */
export const priceLabel = (row: PriceRow) => `$${row.price} ${PER[row.priceMethod] ?? row.priceMethod}`;
