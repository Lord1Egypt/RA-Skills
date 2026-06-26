/**
 * Walrus storage client for the web frontend
 * Fetches manifests and space data from Walrus aggregator OR local filesystem
 */

import type { BookmarkItem, Space, Manifest } from './types';

// Testnet aggregator
const AGGREGATOR = 'https://aggregator.walrus-testnet.walrus.space';

// Check if running in local mode (dev server with access to filesystem)
const isLocalMode = import.meta.env.DEV;

export async function fetchBlob<T>(blobId: string): Promise<T> {
  const res = await fetch(`${AGGREGATOR}/v1/blobs/${blobId}`);
  if (!res.ok) throw new Error(`Walrus fetch failed: ${res.status}`);
  return res.json() as Promise<T>;
}

export async function fetchManifest(blobId: string): Promise<Manifest> {
  return fetchBlob<Manifest>(blobId);
}

export async function fetchSpace(blobId: string): Promise<Space> {
  return fetchBlob<Space>(blobId);
}

// Local mode: fetch from filesystem via backend API
export async function fetchLocalManifest(): Promise<Manifest> {
  const res = await fetch('/api/local/manifest');
  if (!res.ok) throw new Error('Failed to load local manifest');
  return res.json();
}

export async function fetchLocalSpace(spaceId: string): Promise<Space> {
  const res = await fetch(`/api/local/spaces/${spaceId}`);
  if (!res.ok) throw new Error(`Failed to load space ${spaceId}`);
  return res.json();
}

export async function fetchAllSpaces(manifest: Manifest): Promise<Space[]> {
  const entries = Object.entries(manifest.spaces);
  // Only fetch non-encrypted spaces — encrypted ones require wallet decrypt
  const plainEntries = entries.filter(([, entry]) => !entry.encrypted);
  const results = await Promise.allSettled(
    plainEntries.map(([, { blobId }]) => fetchSpace(blobId))
  );

  return results
    .filter((r): r is PromiseFulfilledResult<Space> => r.status === 'fulfilled')
    .map(r => r.value);
}

export function getEncryptedSpaceIds(manifest: Manifest): Array<{
  id: string;
  blobId: string;
  policyObjectId: string;
}> {
  return Object.entries(manifest.spaces)
    .filter(([, entry]) => entry.encrypted && entry.policyObjectId)
    .map(([id, entry]) => ({
      id,
      blobId: entry.blobId,
      policyObjectId: entry.policyObjectId!,
    }));
}

export async function fetchAllLocalSpaces(manifest: Manifest): Promise<Space[]> {
  const spaceIds = Object.keys(manifest.spaces);
  const results = await Promise.allSettled(
    spaceIds.map(id => fetchLocalSpace(id))
  );

  return results
    .filter((r): r is PromiseFulfilledResult<Space> => r.status === 'fulfilled')
    .map(r => r.value);
}

export function searchItems(spaces: Space[], query: string): Array<{ item: BookmarkItem; space: Space }> {
  const q = query.toLowerCase().trim();
  if (!q) return [];

  const results: Array<{ item: BookmarkItem; space: Space; score: number }> = [];

  for (const space of spaces) {
    for (const item of space.items) {
      let score = 0;
      if (item.title.toLowerCase().includes(q)) score += 10;
      if (item.tags.some(t => t.toLowerCase().includes(q))) score += 8;
      if (item.summary.toLowerCase().includes(q)) score += 5;
      if (item.content.toLowerCase().includes(q)) score += 2;
      if (score > 0) results.push({ item, space, score });
    }
  }

  return results.sort((a, b) => b.score - a.score).map(({ item, space }) => ({ item, space }));
}

export function getAllTags(spaces: Space[]): Array<{ tag: string; count: number }> {
  const counts = new Map<string, number>();
  for (const space of spaces) {
    for (const item of space.items) {
      for (const tag of item.tags) {
        counts.set(tag, (counts.get(tag) ?? 0) + 1);
      }
    }
  }
  return Array.from(counts.entries())
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count);
}

// Update item tags (local mode only)
export async function updateItemTags(spaceId: string, itemId: string, tags: string[]): Promise<void> {
  const res = await fetch(`/api/local/spaces/${spaceId}/items/${itemId}/tags`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tags }),
  });
  if (!res.ok) throw new Error('Failed to update tags');
}

// Update item note (local mode only)
export async function updateItemNote(spaceId: string, itemId: string, notes: string): Promise<void> {
  const res = await fetch(`/api/local/spaces/${spaceId}/items/${itemId}/note`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notes }),
  });
  if (!res.ok) throw new Error('Failed to update note');
}

export { isLocalMode };
