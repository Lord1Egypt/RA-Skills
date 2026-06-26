# Known MCP Limitations

These limitations are documented so they are handled correctly in all workflows.

## getWorkspaces Returns All Workspaces (Large Payload)

`getWorkspaces` with no parameters returns every workspace the user has access to. For large organizations (like Postman's own team), this can be 300KB+ and overflow inline display limits.

**Workaround:** If you already have a workspace ID, use `getWorkspace(workspaceId)` directly. If you need to find a workspace, ask the user for the ID or use `getCollections` with a known workspace ID.

## getCollection Full Model Can Overflow

`getCollection` with `model=full` returns the complete collection including all request bodies, response examples, and test scripts. For large collections (50+ requests with examples), this can exceed 300KB.

**Workaround:** Use the default response (lightweight map with `itemRefs`) for discovery and structure. Then make targeted `getCollectionRequest` and `getCollectionResponse` calls for specific endpoints you need detail on.

## Tag Tools May Require Enterprise Plan

`getTaggedEntities` returns 404 for missing tag slugs (instead of an empty result). `getCollectionTags` returns 403 ("You do not have view permission") on non-Enterprise plans. Both tag-related tools are unreliable for general use.

**Workaround:** Do not rely on tag tools for API discovery. Use `getCollections` with name filtering as the primary discovery method. If tag calls fail with 404 or 403, silently fall back to collection-based search.

## runCollection Returns Aggregate Results Only

`runCollection` returns a high-level summary: total requests, failed requests, total assertions, failed assertions, and duration. It does NOT return per-request results, response bodies, or specific error messages.

**Workaround:** For debugging specific failures, examine individual requests with `getCollectionRequest` (to see test scripts) and `getCollectionResponse` (to see expected responses). The user may need to check the Postman app or set up a monitor for detailed per-request logs.

## searchPostmanElements is Public-Only

`searchPostmanElements` searches the PUBLIC Postman network only, not the user's private workspaces.

**Workaround:** For private content, use `getWorkspaces` + `getCollections` + `getCollection`. Use `searchPostmanElements` only as a fallback when searching for public APIs.

## generateCollection is Async

`generateCollection` returns HTTP 202 (accepted), not the collection directly.

**Workaround:** Poll `getGeneratedCollectionSpecs` or `getSpecCollections` for completion. Note: `getAsyncSpecTaskStatus` may return 403 on some plans; use the alternatives.

## syncCollectionWithSpec is Async and OpenAPI 3.0 Only

`syncCollectionWithSpec` returns HTTP 202 and only supports OpenAPI 3.0 specifications.

**Workaround for async:** Poll `getCollectionUpdatesTasks` for completion.

**Workaround for non-3.0 specs:** For Swagger 2.0 or OpenAPI 3.1 specs, use `updateSpecFile` to update the spec and regenerate the collection with `generateCollection`.

## createCollection Cannot Nest Folders

`createCollection` creates a flat collection. You cannot nest folders in a single call.

**Workaround:** Decompose the operation:
1. `createCollection` to create the collection
2. `createCollectionFolder` to add folders
3. `createCollectionRequest` to add requests to folders

## putCollection Auth Enum Lacks "noauth"

The `putCollection` auth type enum does not include "noauth" as a valid value.

**Workaround:** Endpoints that need no auth should inherit from collection-level settings or use a different auth type as a placeholder.

## createSpec Impractical for Large Specs

`createSpec` struggles with specs larger than ~50KB due to request size limits.

**Workaround:** For large APIs, parse the spec locally and create collection items directly using `createCollection` + `createCollectionFolder` + `createCollectionRequest` + `createCollectionResponse`.
