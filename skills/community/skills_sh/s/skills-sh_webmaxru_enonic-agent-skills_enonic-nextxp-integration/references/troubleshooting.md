# Troubleshooting

Common issues and diagnostic steps for the Next.js + Enonic XP integration (Next.XP).

## Preview Issues

### Blank page in Content Studio preview
1. Confirm the Next.js dev server is running (`npm run dev`) and accessible at the configured URL (default: `http://127.0.0.1:3000`).
2. Verify the Next.XP app is installed in Enonic XP and added to the site in Content Studio.
3. Check that `ENONIC_API_TOKEN` in `.env` matches the secret configured in the Next.XP app (default: `mySecretKey`).
4. Open the browser developer tools in Content Studio and check for CORS errors or network request failures.
5. Check the Next.js server console for errors during the preview request.
6. Verify the `/api/preview/route.ts` API route exists in the Next.js project.

### Preview works but links are broken
1. Ensure all component links use `getUrl(path, meta)` from `@enonic/nextjs-adapter` instead of hardcoded paths.
2. Content Studio uses different base paths (`/preview`, `/inline`, `/edit`); `getUrl()` handles this automatically.
3. For static assets, use `getAsset(path, meta)` instead of direct path references.

### Draft content not visible in preview
1. Preview mode should automatically query the `draft` branch. Verify the Next.XP proxy is active.
2. Check that the content item has been saved (even if not published) in Content Studio.
3. Verify the Guillotine API endpoint is accessible and returning content for the draft branch.

## Data Fetching Issues

### Guillotine query returns null or empty data
1. Test the query directly in GraphQL Playground at `http://localhost:8080/site/<project>` with the same variables.
2. Verify the content type name in the introspection fragment matches the actual type: dots become underscores, final segment is capitalized.
3. Confirm the content item exists at the queried path and is of the expected type.
4. Check for typos in field names — Guillotine reflects the content type schema exactly.

### Query works in Playground but not in Next.js
1. Verify `ENONIC_API` in `.env` points to the correct Guillotine endpoint.
2. Check that `ENONIC_APP_NAME` matches the fully qualified application name used in the Enonic app.
3. Confirm `ENONIC_MAPPINGS` correctly maps the locale to the project and site path.
4. Check the Next.js console for network errors or authentication failures.

### APP_NAME_UNDERSCORED produces wrong introspection type
1. `APP_NAME_UNDERSCORED` is derived from `ENONIC_APP_NAME` by replacing dots with underscores.
2. Verify `ENONIC_APP_NAME` in `.env` matches the app name in `build.gradle` or `gradle.properties`.
3. The content type `com.example.myproject:movie` should become `com_example_myproject_Movie` in queries.

## Component Mapping Issues

### Custom view not rendering — debug view shown instead
1. Verify the content type mapping is registered in `src/components/_mappings.ts`.
2. Check that the content type string uses `${APP_NAME}:<type-name>` format.
3. Ensure the import paths for query and view components are correct.
4. If the `CATCH_ALL` debug view is still active, comment it out in `_mappings.ts`.

### Part renders with fallback instead of custom component
1. Parts must be registered with `ComponentRegistry.addPart()` using the fully qualified name: `${APP_NAME}:<part-name>`.
2. The part must also be defined in the Enonic app under `src/main/resources/site/parts/<part-name>/<part-name>.xml`.
3. Redeploy the Enonic app after adding new part definitions.

### Regions not rendering in page component
1. Verify the page component uses `<RegionsView>` from `@enonic/nextjs-adapter/views/Region`.
2. Check that the region name in the React component matches the region defined in the Enonic page XML.
3. Ensure editors have added components to the region in Content Studio.

## Build and Runtime Issues

### Rich text renders as plain text or missing components
1. Verify the query uses `richTextQuery(fieldName)` from `@enonic/nextjs-adapter` instead of fetching the field directly.
2. Confirm the query is a function (not a static string) so that macros are registered before query execution.
3. Pass the rich text data to `RichTextView` component from `@enonic/nextjs-adapter/views/RichTextView`.
4. Verify that macros are registered in `_mappings.ts` before any component that uses `RichTextView`.

### Macros not rendering in rich text
1. Confirm the macro is registered with `ComponentRegistry.addMacro()` using the fully qualified name: `${APP_NAME}:<macro-name>`.
2. Macro registrations must appear before other component registrations that use `RichTextView` in `_mappings.ts`.
3. Use `configQuery` to fetch macro form values if the macro component needs configuration.

### @enonic/nextjs-adapter import errors
1. Run `npm install` to ensure the package is installed.
2. Check `package.json` for `@enonic/nextjs-adapter` in dependencies (v4.x requires React 19 and Next.js 16).
3. Verify the import path: some exports require subpath imports (e.g., `@enonic/nextjs-adapter/views/Region`, `@enonic/nextjs-adapter/server`, `@enonic/nextjs-adapter/client`).
4. Server-side functions like `fetchContent` must be imported from `@enonic/nextjs-adapter/server`, not the main entry point.

### TypeScript errors in component files
1. Ensure `FetchContentResult`, `PageProps`, and `PartProps` types are imported from `@enonic/nextjs-adapter`.
2. Cast `props.data?.get` as `any` or define proper interfaces for content type data shapes.

### "Strange issues" in Next.js dev mode
1. Delete the `.next/` folder and restart the dev server.
2. Clear the Node.js module cache: delete `node_modules` and run `npm install` again.
3. Check the Next.js CLI docs for additional debugging options.

## Deployment Issues

### 404 on public frontend but preview works
1. Content must be published (moved from `draft` to `master` branch) to be visible on the public site.
2. In Content Studio: select content → "Mark as ready" → "Publish".
3. Verify `ENONIC_MAPPINGS` includes the correct project and site path for the deployment.

### Vercel deployment shows errors
1. Check Vercel function logs for runtime errors.
2. Verify all `ENONIC_*` environment variables are set in the Vercel project settings.
3. Confirm the Enonic Cloud ingress is accessible from the internet.
4. Test the Guillotine API endpoint directly from a browser or curl to rule out network issues.

### Enonic Cloud app installation fails
1. Verify CLI authentication: `enonic cloud login`.
2. Ensure you are running `enonic cloud app install` from the Enonic app directory (not the Next.js directory).
3. Check that the Enonic Cloud solution has started and is accessible.
