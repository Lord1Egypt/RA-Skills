# Postman MCP Tool Reference

Quick reference for selecting the right Postman MCP tool.

## Workspace Operations

| Tool | Use For |
|------|---------|
| `getWorkspaces` | List all workspaces |
| `getWorkspace` | Get workspace details |
| `createWorkspace` | Create new workspace |

## Collection CRUD

| Tool | Use For |
|------|---------|
| `getCollections` | List collections in workspace (supports `name` filter) |
| `getCollection` | Get full collection with requests and folders |
| `createCollection` | Create new collection (flat only, no nested folders) |
| `putCollection` | Replace entire collection |
| `patchCollection` | Update collection metadata |
| `deleteCollection` | Delete a collection |
| `duplicateCollection` | Copy a collection |

## Request and Response

| Tool | Use For |
|------|---------|
| `getCollectionRequest` | Get request details (method, URL, body, auth) |
| `createCollectionRequest` | Add new request to collection/folder |
| `updateCollectionRequest` | Modify existing request |
| `deleteCollectionRequest` | Remove request |
| `getCollectionResponse` | Get saved example response |
| `createCollectionResponse` | Add example response (used by mocks) |
| `updateCollectionResponse` | Modify example response |
| `deleteCollectionResponse` | Remove example response |

## Folder Management

| Tool | Use For |
|------|---------|
| `getCollectionFolder` | Get folder details |
| `createCollectionFolder` | Create folder in collection |
| `updateCollectionFolder` | Modify folder |
| `deleteCollectionFolder` | Remove folder |

## Spec Hub

| Tool | Use For |
|------|---------|
| `getAllSpecs` | List specs in workspace |
| `getSpec` | Get spec metadata |
| `createSpec` | Create new spec (types: OPENAPI:2.0, 3.0, 3.1, ASYNCAPI:2.0) |
| `getSpecDefinition` | Get full spec content |
| `getSpecFiles` | List spec files |
| `getSpecFile` | Get individual spec file |
| `updateSpecFile` | Update spec file content |
| `deleteSpec` | Delete a spec |

## Sync Operations

| Tool | Use For | Notes |
|------|---------|-------|
| `generateCollection` | Generate collection from spec | Async (202), poll with `getGeneratedCollectionSpecs` |
| `syncCollectionWithSpec` | Update collection from spec changes | Async (202), OpenAPI 3.0 only |
| `syncSpecWithCollection` | Update spec from collection changes | |
| `getCollectionUpdatesTasks` | Poll async collection update status | |
| `getGeneratedCollectionSpecs` | Poll async generation status | |
| `getSpecCollections` | Get collections linked to a spec | |

## Environments

| Tool | Use For |
|------|---------|
| `getEnvironments` | List environments in workspace |
| `getEnvironment` | Get environment variables |
| `createEnvironment` | Create new environment |
| `putEnvironment` | Replace environment |
| `patchEnvironment` | Update environment metadata |
| `deleteEnvironment` | Remove environment |

## Mock Servers

| Tool | Use For |
|------|---------|
| `getMocks` | List mock servers |
| `getMock` | Get mock details and URL |
| `createMock` | Create mock server from collection |
| `updateMock` | Modify mock settings |
| `deleteMock` | Remove mock server |
| `publishMock` | Make mock publicly accessible |
| `unpublishMock` | Make mock private |

## Testing

| Tool | Use For |
|------|---------|
| `runCollection` | Execute collection tests (needs UID in OWNER-UUID format) |

## Documentation

| Tool | Use For |
|------|---------|
| `publishDocumentation` | Publish collection docs publicly |
| `unpublishDocumentation` | Take down public docs |

## Search and Discovery

| Tool | Use For | Notes |
|------|---------|-------|
| `searchPostmanElements` | Search the Postman API Network | **Public only**, not private workspaces |
| `getTaggedEntities` | Find entities by tag | May return 404; **Enterprise plan may be required** |
| `getCollectionTags` | Get tags on a collection | May return 403; **Enterprise plan may be required** |
| `updateCollectionTags` | Set tags on a collection | **Enterprise plan may be required** |

## Monitors

| Tool | Use For |
|------|---------|
| `getMonitors` | List monitors |
| `getMonitor` | Get monitor details |
| `createMonitor` | Create scheduled monitor |
| `updateMonitor` | Modify monitor |
| `deleteMonitor` | Remove monitor |
| `runMonitor` | Trigger monitor run |

## Code Generation

| Tool | Use For |
|------|---------|
| `getCodeGenerationInstructions` | Get Postman-specific codegen guidance |

## User

| Tool | Use For |
|------|---------|
| `getAuthenticatedUser` | Verify API key and get user info |
