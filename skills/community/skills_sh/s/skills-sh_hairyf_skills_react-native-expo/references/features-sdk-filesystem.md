---
name: expo-file-system
description: Read/write files, use cache and document directories, and download files with expo-file-system.
---

# expo-file-system

**expo-file-system** provides access to the device file system: app cache and document directories, sync/async read and write, downloads, and listing. Use `File`, `Directory`, and `Paths` for the modern API; legacy API lives under `expo-file-system/legacy`.

## Usage

```bash
npx expo install expo-file-system
```

```js
import { File, Directory, Paths } from 'expo-file-system';

// Paths: Paths.cache, Paths.document
const file = new File(Paths.cache, 'data.json');
file.create(); // throws if exists
file.write(JSON.stringify({ key: 'value' }));
const text = file.textSync();

// Async
const file2 = new File(Paths.document, 'notes.txt');
await file2.create();
await file2.write('Hello');
const content = await file2.text();

// Download
const out = await File.downloadFileAsync('https://example.com/file.pdf', new Directory(Paths.cache, 'downloads'));

// List directory
const dir = new Directory(Paths.cache);
const items = dir.list(); // File[] | Directory[]
```

**Upload with expo/fetch:** Use `fetch` from `expo/fetch` with `body: file` or `FormData` appending a `File` instance.

## Key points

- **Paths:** `Paths.cache` (cleared by OS under storage pressure), `Paths.document` (backed up by default on iOS). Use cache for temp data, document for user data.
- **Config plugin (iOS):** Optional. Add `expo-file-system` plugin with `supportsOpeningDocumentsInPlace` and/or `enableFileSharing` if the app must open documents in place or show in Files app.
- **Legacy API:** `import * as FileSystem from 'expo-file-system/legacy'` for `readAsStringAsync(uri)`, `writeAsStringAsync(uri, content)`, etc. Prefer the `File`/`Directory` API for new code.

<!--
Source references:
- https://docs.expo.dev/versions/latest/sdk/filesystem/
-->
