/**
 * MPP Router catalog client — pure library, hardcoded API_BASE.
 *
 * Callers pass all arguments explicitly; this module takes no external state.
 */

const API_BASE = "https://apiserver.mpprouter.dev";

export interface ServiceRecord {
  id: string;
  name: string;
  category: string;
  description: string;
  public_path: string;
  method: string;
  price: string;
  payment_method: string;
  network: string;
  asset: string;
  status: string;
  docs_url?: string;
  methods?: Record<string, { intents: string[]; role?: string }>;
  verified_mode?: string;
}

export interface Catalog {
  version: string;
  base_url: string;
  generated_at: string;
  services: ServiceRecord[];
}

/** Fetch the live MPP Router service catalog. */
export async function fetchCatalog(): Promise<Catalog> {
  const res = await fetch(`${API_BASE}/v1/services/catalog`);
  if (!res.ok) {
    throw new Error(`Catalog fetch failed: ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as Catalog;
}

/** Score a service against a free-text query. Higher = more relevant. */
export function scoreService(service: ServiceRecord, query: string): number {
  const q = query.toLowerCase();
  let s = 0;
  if (service.id.toLowerCase().includes(q)) s += 5;
  if (service.name.toLowerCase().includes(q)) s += 3;
  if (service.category.toLowerCase().includes(q)) s += 3;
  if (service.description.toLowerCase().includes(q)) s += 1;
  const tokens = q.split(/\s+/).filter(Boolean);
  const haystack =
    `${service.id} ${service.name} ${service.category} ${service.description}`.toLowerCase();
  for (const t of tokens) {
    if (haystack.includes(t)) s += 1;
  }
  return s;
}
