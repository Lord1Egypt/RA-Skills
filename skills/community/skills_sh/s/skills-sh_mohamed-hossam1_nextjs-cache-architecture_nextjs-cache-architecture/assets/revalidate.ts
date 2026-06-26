// lib/cache/revalidate.ts
//
// Every `updateTag()` call in the project lives here.
// Mutations import these functions — they never call `updateTag()` directly.
//
// Why centralize:
//   - One place to audit invalidation behavior.
//   - One place to change the strategy (e.g., add observability).
//   - Mutations stay focused on data changes, not cache mechanics.

"use server";

import { updateTag } from "next/cache";
import { CACHE_TAGS } from "./tags";

function updateTags(tags: string[]) {
  // Optional: add observability here. Because every invalidation flows
  // through this one function, a single console.log / OpenTelemetry span
  // gives full coverage with no per-call-site instrumentation.
  // Example:
  //   console.log("[cache] updateTag", { tags, at: new Date().toISOString() });
  for (const tag of tags) updateTag(tag);
}

// Bulk — any entry in the collection changed.
// Replace [Collection] / [collection] with the user's real names.
export async function revalidate[Collection]Cache() {
  updateTags([CACHE_TAGS.[collection]]);
}

// Surgical — one specific entry changed.
// Only export this if `CACHE_TAGS.[entity]` factory exists in tags.ts.
// Always invalidate the parent collection too — list views read from it.
export async function revalidate[Entity]Cache(id: string | number) {
  updateTags([
    CACHE_TAGS.[collection],
    CACHE_TAGS.[entity](id),
  ]);
}
