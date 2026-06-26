---
name: custom-resources
description: How to define custom REST endpoints with JavaScript or TypeScript in Harper.
metadata:
  mode: generate
  sources:
    - reference/v5/resources/overview.md#Custom External Data Source
    - reference/v5/resources/overview.md#Exporting Resources as Endpoints
    - reference/v5/components/javascript-environment.md#Module Loading
  sourceCommit: 4fe4c9c95e0974eaa77032f6f10e36fbd8ec64ac
  inputHash: 9b911fd8e036b808
---

# Custom Resources

Instructions for the agent to follow when defining custom REST endpoints with JavaScript or TypeScript in Harper.

## When to Use

Apply this rule when creating custom HTTP endpoints, wrapping external APIs, or registering programmatic routes in a Harper application. Use it any time business logic needs to live outside a standard table-backed resource.

## How It Works

1. **Import `Resource` from the `harper` package**: Always import explicitly rather than relying on globals.

   ```javascript
   import { tables, Resource } from 'harper';
   ```

2. **Define a class that `extends Resource`**: Use `export class` so Harper can expose it as an endpoint. Implement HTTP methods as `static` methods on the class.

   ```javascript
   export class CustomEndpoint extends Resource {
   	static get(target) {
   		return {
   			data: doSomething(),
   		};
   	}
   }
   ```

3. **Add async `static` methods for each HTTP verb you need**: Methods receive `target` (contains `target.id`, etc.) and, for write operations, `data`.

   ```javascript
   export class MyExternalData extends Resource {
   	static async get(target) {
   		const response = await fetch(`https://api.example.com/${target.id}`);
   		return response.json();
   	}

   	static async put(target, data) {
   		return fetch(`https://api.example.com/${target.id}`, {
   			method: 'PUT',
   			body: JSON.stringify(await data),
   		});
   	}
   }
   ```

4. **Control the URL by choosing the export form**: The shape of the export determines the resulting URL path. Path matching is case-sensitive.

   | Export form                              | URL             | Notes                                                           |
   | ---------------------------------------- | --------------- | --------------------------------------------------------------- |
   | `export class Foo extends Resource {}`   | `/Foo/`         | Class name becomes the path segment.                            |
   | `export const Bar = { Foo };`            | `/Bar/Foo/`     | Nest under an object to add a path prefix.                      |
   | `export const bar = { 'foo-baz': Foo };` | `/bar/foo-baz/` | Use object keys for lowercase, hyphens, or non-identifier URLs. |
   | `server.resources.set('my-path', Foo);`  | `/my-path/`     | Programmatic registration; useful when the path is dynamic.     |

5. **Register programmatically when the path is dynamic**: Use `server.resources.set(` with a path string and the class.

   ```javascript
   server.resources.set('my-path', Foo);
   ```

6. **Optionally use the resource as a cache source for a local table**: Pass the class to `sourcedFrom`.
   ```javascript
   tables.MyCache.sourcedFrom(MyExternalData);
   ```

## Examples

Wrap an external API and expose it as an endpoint, then back a local cache table with it:

```javascript
import { tables, Resource } from 'harper';

export class MyExternalData extends Resource {
	static async get(target) {
		const response = await fetch(`https://api.example.com/${target.id}`);
		return response.json();
	}

	static async put(target, data) {
		return fetch(`https://api.example.com/${target.id}`, {
			method: 'PUT',
			body: JSON.stringify(await data),
		});
	}
}

// Use as a cache source for a local table
tables.MyCache.sourcedFrom(MyExternalData);
```

Programmatic registration with a custom path:

```javascript
import { Resource } from 'harper';

export class CustomEndpoint extends Resource {
	static get(target) {
		return {
			data: doSomething(),
		};
	}
}

server.resources.set('my-path', CustomEndpoint);
```

## Notes

- `export class` directly produces a URL from the class name (e.g., `export class Foo extends Resource {}` → `/Foo/`). Do not export the same resource from both a schema file and a JavaScript file — this creates conflicting exports.
- URL path segments are case-sensitive: `/Foo/` and `/foo/` are different endpoints.
- For CommonJS modules, use `const { tables, Resource } = require('harper');` instead of the ESM import.
- When developing a component in its own directory, run `npm link harper` to ensure typings match your installed version. All installed components have `harper` automatically linked.
- The `static` keyword is required on all HTTP verb methods — Harper dispatches requests through static class methods, not instance methods.
