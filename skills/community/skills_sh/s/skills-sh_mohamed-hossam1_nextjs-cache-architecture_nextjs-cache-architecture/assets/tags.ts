// lib/cache/tags.ts
//
// Single source of truth for every cache tag in the project.
// Raw tag strings are never written anywhere else.
//
// Conventions:
//   - Lowercase only.
//   - Entity tags use `domain:id` format.
//   - Match the actual data model — do not invent names.
//   - Add an entity factory ONLY when a mutation needs `updateTag()`
//     on a single entry. Otherwise the collection tag is enough.
//
// Type safety:
//   `as const satisfies TagRegistry` keeps every value literal-typed
//   (so the compiler knows `CACHE_TAGS.posts` is exactly `"posts"`)
//   AND enforces that every entry is either a tag string or a factory
//   that returns one. Misuse — e.g. dropping in a number, an object,
//   or a function with the wrong signature — fails to compile.

type Tag = string;
type EntityTagFactory = (id: string | number) => Tag;
type TagRegistry = Record<string, Tag | EntityTagFactory>;

export const CACHE_TAGS = {
  // COLLECTION TAGS — one per logical data group, always present.
  // Replace [collection] with the user's real collection name.
  [collection]: "[collection]",
  [anotherCollection]: "[anotherCollection]",

  // ENTITY TAG FACTORIES — only when a mutation targets a single entry.
  // Replace [entity] with the user's real entity name.
  [entity]: ((id) => `[entity]:${id}`) satisfies EntityTagFactory,
} as const satisfies TagRegistry;
