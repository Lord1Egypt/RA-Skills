# Deployment types — what `aio aem rde install` can ship

`aio aem rde install` accepts a single artifact, of one of eight types, deployed to one or both AEM instances. This file catalogues each type, when to use it, and the gotchas.

The full list (also available in `aio aem rde install --help`):

```
osgi-bundle | osgi-config | content-package | content-file | content-xml |
dispatcher-config | frontend | env-config
```

When `--type` is omitted, the plugin guesses. See the table in `commands.md` for guess rules. The rest of this file goes deeper on each type.

## `osgi-bundle`

A standard OSGi `.jar`.

- Source: `**/target/*.jar` from a Maven OSGi-bundle module.
- Target: usually both author and publish (default). For instance-specific bundles, use `--target author` or `--target publish`.
- Identification: bundle symbolic name (BSN). `aio aem rde delete <bsn>` removes it.
- After install, use `aio aem rde inspect osgi-bundles` (if enabled) to confirm `Active` state.

Pitfalls:
- A bundle that fails to resolve sticks around as `Installed`/`Resolved`. Check the failed update via `history <id>` and look at the bundle in `inspect osgi-bundles`.
- Restart only if the bundle has special activation needs (`@Activate` work that is fragile to refresh, native libs, etc.). Day-to-day bundle iteration is hot-reloadable.

## `osgi-config`

JSON-formatted OSGi configuration consumed via Configuration Admin. Filename **becomes** the config PID — there's no separate `--path` flag.

- Source: `*.json` matching the OSGi config naming convention (e.g. `com.example.MyService.json` or `com.example.MyFactory~instance.json`).
- Target: same as bundle.
- Identification: PID = filename without `.json`. `aio aem rde delete <pid>` removes it.

Pitfalls:
- Filename matters. The plugin sends the filename as the config PID; renaming the file rewrites a different config.
- Use `aio aem rde inspect osgi-configurations` to verify.

## `content-package`

A "regular" AEM content package zip with `jcr_root/` and `META-INF/vault/`.

- Source: `*.zip` produced by `content-package-maven-plugin` / FileVault.
- Detection: zip with a `jcr_root/` entry.
- Target: typically both, but `--target author` lets you push author-only packages.
- Larger packages: the upload is chunked and the progress bar shows KB transferred.

Pitfalls:
- Workflow-bearing packages may need a follow-up `--restart` if they replace OSGi bundles bundled inside the package.
- For very large packages prefer creating a snapshot first so you can `restore` if it breaks state.
- Known regression (SKYOPS-140701, affects RDEs with the buggy base image): install reports `deploy completed` but JCR content never lands. Symptom is silent — bundles in the same deploy still apply, only the content-package extraction is a no-op. Verify by hitting `/content/<site>.json` (404) or by looking for `LoginException … RDEProviderRepositoryAccess.handleContentPackages` in `aio aem rde logs -e ""`. See `troubleshooting.md` → "Content-package install reports success but JCR content never appears" for the workaround OSGi config.

## `content-file`

A single binary content file deployed under a specific JCR path. **Requires `--path`**.

- Source: any non-zip / non-xml file (image, PDF, etc.).
- `--path`: the full JCR path the file should land at, e.g. `/content/dam/example/foo.png`.
- Auto-guess: if the source path is under `…/jcr_root/…`, the plugin derives `--path` from the substring after `jcr_root/`.

Pitfalls:
- Without `--path` and without a `jcr_root/` ancestor, the install throws `MISSING_CONTENT_PATH`.
- Targets are still author/publish — if you only need it on author, pass `--target author`.

## `content-xml`

A single FileVault XML descriptor (`*.xml`, often `.content.xml`). Same `--path` semantics as `content-file`.

- For a `.content.xml`, the auto-guessed path strips the `.content.xml` suffix (the file describes its parent node).
- For other XML files, the path strips just `.xml`.

Pitfalls:
- Hand-crafted XML with non-canonical structure may be rejected by JCR — validate with FileVault first.
- Best for surgical edits; for bigger changes, a content-package is more honest.

## `dispatcher-config`

Apache HTTPD + Dispatcher configuration tree. Shipped as a directory or zip; the directory form is built into a zip on the fly via `dispatcherInputBuild`.

- Source: a directory containing `conf.dispatcher.d/`, or a zip with the same.
- Detection (zip): zip has `conf.dispatcher.d/`.
- Target: only `publish` makes sense for a dispatcher config — but `install` defaults to "both". The dispatcher tier handles it correctly; ignore the author "deploy" message unless something looks off.

Pitfalls:
- Dispatcher validation may surface errors that block the env. Run the [Adobe Dispatcher Validator](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/disp-overview) locally before deploying.
- After dispatcher changes, `aio aem rde inspect request-logs` (if enabled) is a good way to verify rules are matching as expected.

## `frontend`

A frontend bundle for AEM's client-side asset pipeline.

- Source: directory with `package.json` and a built `dist/` folder, or a zip with the same.
- Detection (zip): zip contains both `dist/` and `package.json`.
- Build step: `frontendInputBuild` zips the directory before upload.
- Target: usually both.

Pitfalls:
- Don't include `node_modules` — `frontendInputBuild` zips the whole tree it's given. Build first, then point `install` at the build output's parent.
- For SPAs/CSM the same artifact works; just respect the AEM frontend conventions.

## `env-config`

Cloud Manager environment-level config (variables, secrets references, log forwarding, etc.) packaged as YAML.

- Source: directory containing one or more `*.yaml`, or a zip with `*.yaml` entries.
- Detection (zip): any entry ending in `.yaml`.
- Build step: `configInputBuild` zips the directory before upload.

Pitfalls:
- Order of reload is async — give the env a few seconds before re-reading the affected setting.
- env-config is the only way to manage variables on RDEs without going through Cloud Manager UI; respect existing values to avoid stomping on teammates' settings.

## Targeting (`--target`)

| Type | Sensible default | Notes |
|------|------------------|-------|
| `osgi-bundle` | both | Bundle target depends on the code. |
| `osgi-config` | both | Same. |
| `content-package` | both, or `author` | Mostly author, but query indexes may need both. |
| `content-file` | both, or `author` | Author for editorial content. |
| `content-xml` | as above | |
| `dispatcher-config` | both (plugin handles it) | Logically publish-only. |
| `frontend` | both | |
| `env-config` | both | Targeting flag is accepted but env-config is global to the env. |

## Type-guessing failures

The plugin throws `INVALID_GUESS_TYPE` when it can't narrow the choice to one. Fix by passing `--type` explicitly. Common cases:

- A remote zip URL — the plugin can't peek inside before download. Pass `--type`.
- Unknown extension — pass `--type` *and* `--path` if it's content-file/content-xml.
- A `.zip` that fits multiple shapes (e.g. a content package that also has a stray `dist/` folder) — pass `--type`.

## Source-path handling

For URLs:
- HEAD request to compute size and follow redirects (`computeStats`).
- Effective URL is used for the upload; original URL is used for type guessing if the redirect dropped the extension.

For local files:
- `file://` prefix is stripped automatically.
- `realpathSync` resolves symlinks.

For directories:
- Allowed only for `frontend`, `dispatcher-config`, `env-config`. The plugin packages them inline. Other types throw a clear error.
