---
name: enonic-nextxp-integration
description: Guides setup, development, and troubleshooting of the Next.js and Enonic XP headless integration (Next.XP framework). Covers Enonic adapter configuration, content type to React component mapping, Guillotine GraphQL data fetching, Content Studio preview mode, and draft/master branch switching. Use when building a Next.js frontend powered by Enonic XP, configuring the Next.XP adapter, mapping content types to components, fetching Enonic content via Guillotine in Next.js, or debugging Content Studio preview. Don't use for traditional server-side Enonic XP rendering, standalone Guillotine queries without Next.js, non-Next.js frontend frameworks with Enonic, or React4XP embedded rendering.
license: MIT
metadata:
  author: webmaxru
  version: "1.5"
---

# Next.js + Enonic XP Headless Integration (Next.XP)

## Procedures

**Step 1: Identify the workspace integration surface**
1. Inspect the workspace for Next.js entry points (`next.config.*`, `package.json` with `next` dependency), Enonic XP app markers (`build.gradle` with `com.enonic.xp`), or existing Next.XP adapter references (`@enonic/nextjs-adapter`).
2. Execute `node scripts/find-nextxp-targets.mjs .` to inventory Next.js projects, `.env` files with `ENONIC_*` variables, component mapping files (`_mappings.ts`), and Guillotine query files when a Node runtime is available.
3. If a Node runtime is unavailable, inspect `package.json`, `.env`, and `src/components/_mappings.ts` manually to identify the integration surface.
4. If the workspace contains both an Enonic XP app and a Next.js frontend, confirm which side the task targets before proceeding.
5. If the workspace is not a Next.js + Enonic XP project, stop and explain that this skill does not apply.

**Step 2: Configure the Enonic adapter**
1. Read `references/nextxp-reference.md` before writing or modifying configuration.
2. Verify or create the `.env` (or `.env.local` for local development) file in the Next.js project root with the required variables:
   - `ENONIC_API_TOKEN` — shared secret for preview mode authentication.
   - `ENONIC_APP_NAME` — fully qualified Enonic application name (e.g., `com.example.myproject`).
   - `ENONIC_MAPPINGS` — locale-to-project/site mapping (e.g., `en:intro/hmdb`).
   - `ENONIC_API` — base URL for the Guillotine API endpoint (e.g., `http://127.0.0.1:8080/site/`).
3. Install the `@enonic/nextjs-adapter` package if not already present: `npm install @enonic/nextjs-adapter`.
4. Import `@enonic/nextjs-adapter/baseMappings` at the top of `src/components/_mappings.ts` to register built-in component renderers.
5. Verify the Next.js project was scaffolded from the `nextxp-template` or contains the expected file structure: `src/components/_mappings.ts`, `src/app/[locale]/[[...contentPath]]/page.tsx`, and API routes under `src/app/api/`.
6. Read `references/compatibility.md` to confirm version requirements between `@enonic/nextjs-adapter` (v4.x), Next.js (16+), React (19), and Enonic XP.

**Step 3: Map content types to React components**
1. Read `references/nextxp-reference.md` for the component registry API and mapping patterns.
2. Read `references/examples.md` for complete content type mapping examples including queries, views, and processors.
3. For each Enonic content type that needs a custom rendering:
   a. Create a Guillotine GraphQL query function in `src/components/queries/` that fetches the fields specific to that content type using type introspection (`... on AppName_ContentTypeName`).
   b. For content types with HTML area (rich text) fields, use `richTextQuery(fieldName)` from `@enonic/nextjs-adapter` to generate the query fragment. See `references/nextxp-reference.md` for the rich text rendering section.
   c. Create a React view component in `src/components/views/` that accepts `FetchContentResult` props and renders the fetched data. Use `RichTextView` from `@enonic/nextjs-adapter/views/RichTextView` for HTML area fields.
   d. Register both in `src/components/_mappings.ts` using `ComponentRegistry.addContentType()`.
4. For page components (pages, parts, layouts):
   a. Define the component XML in the Enonic app under `src/main/resources/site/pages/`, `parts/`, or `layouts/`.
   b. Create a corresponding React component in `src/components/pages/`, `parts/`, or `layouts/`. Use `LayoutProps` for layouts and the named `RegionView` export for individual region rendering.
   c. Register using `ComponentRegistry.addPage()`, `ComponentRegistry.addPart()`, or `ComponentRegistry.addLayout()`.
5. For layouts, use `LayoutProps` type and `RegionView` (singular, named export) for individual regions instead of `RegionsView`.
6. Use `APP_NAME` and `APP_NAME_UNDERSCORED` imports from `@enonic/nextjs-adapter` to keep content type references dynamic.

**Step 4: Configure Guillotine data fetching**
1. Read `references/nextxp-reference.md` for the Guillotine query structure and variable passing.
2. Write GraphQL queries that use `$path:ID!` as the primary variable for content retrieval via `guillotine { get(key:$path) { ... } }`.
3. Use type introspection to access content-type-specific fields: `... on AppName_ContentTypeName { data { ... } }`.
4. For rich text fields (HtmlArea), use `richTextQuery(fieldName)` from the adapter instead of querying the field directly. Render with `RichTextView` from `@enonic/nextjs-adapter/views/RichTextView`.
5. For parts and configurable components, export a query object with `query(path, context, config)` and `variables(path, context, config)` functions.
6. Use processors (optional async functions) to post-process query results before passing to the view.
7. Use `ComponentRegistry.setCommonQuery()` for data shared across all page components. Remove the common query if not needed to optimize performance.
8. Use `getUrl()` and `getAsset()` helper functions from the adapter for URL handling that works in both standalone and Content Studio preview modes.
9. For macros in rich text, register them with `ComponentRegistry.addMacro()` before other components that use `RichTextView`. See `references/nextxp-reference.md` for the macro registration API.

**Step 5: Enable Content Studio preview mode**
1. Read `references/nextxp-reference.md` for full preview architecture details.
2. Install the `Next.XP` app in Enonic XP: `XP Menu → Applications → Install → search "Next.XP"`.
3. Add the Next.XP app to the target site in Content Studio via the "Applications" combobox on the site edit view.
4. Verify default preview configuration: URL `http://127.0.0.1:3000` and secret matching `ENONIC_API_TOKEN`.
5. For production, configure the Next.XP app with the deployed Next.js URL and shared secret via app config:
   ```
   nextjs.default.url = <Next.js app URL>
   nextjs.default.secret = <shared secret>
   ```
6. Preview mode automatically switches the Guillotine API to the `draft` branch, while the public Next.js frontend uses the `master` (published) branch.
7. Use `getUrl()` in all component links to ensure URLs resolve correctly across preview, inline, and edit modes in Content Studio.
8. If preview shows a blank page, read `references/troubleshooting.md` for diagnostic steps.

**Step 6: Deploy to production**
1. Read `references/nextxp-reference.md` for the deployment checklist.
2. Deploy the Enonic app to Enonic Cloud using `enonic cloud app install`.
3. Create an ingress in Enonic Cloud to expose the Guillotine API (target path `/site`, public path `/api`).
4. Deploy the Next.js app to Vercel or another hosting platform.
5. Set production environment variables: `ENONIC_API`, `ENONIC_APP_NAME`, `ENONIC_API_TOKEN`, `ENONIC_MAPPINGS`.
6. Configure the Next.XP app in Enonic Cloud to point to the production Next.js URL.
7. Publish content in Content Studio to make it visible on the live frontend.

**Step 7: Validate the integration**
1. Execute `node scripts/find-nextxp-targets.mjs .` to confirm the adapter, mappings, and env configuration still resolve correctly.
2. Verify that standalone Next.js rendering works at `http://localhost:3000` with published content.
3. Verify Content Studio preview renders correctly for both draft and published content.
4. Test content type mappings by visiting content URLs and confirming custom views render.
5. Use `validateData()` from `@enonic/nextjs-adapter` in the page handler to catch invalid content responses. See `references/nextxp-reference.md` for the SSG page handler pattern.
6. Run the workspace build (`npm run build`) to catch TypeScript or build errors.

## Error Handling
* If Content Studio preview shows a blank page, read `references/troubleshooting.md` for preview proxy diagnostics, token mismatch detection, and CORS issues.
* If Guillotine queries return empty or unexpected data, verify the content type name matches the introspection pattern and test the query in GraphQL Playground at `http://localhost:8080/site/<project>`.
* If `@enonic/nextjs-adapter` imports fail, check `references/compatibility.md` for version requirements and confirm the package is installed.
* If content renders in preview but not on the public site, verify the content is published (moved from `draft` to `master` branch).
* If component mappings are not applied, verify registrations in `_mappings.ts` use the correct fully-qualified content type or component name with `APP_NAME`.
