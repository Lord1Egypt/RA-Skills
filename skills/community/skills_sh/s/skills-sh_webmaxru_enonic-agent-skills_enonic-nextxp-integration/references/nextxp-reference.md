# Next.XP Reference

Canonical reference for the Next.js + Enonic XP integration framework (Next.XP). Covers adapter configuration, component registry, rendering modes, Guillotine queries, preview architecture, and deployment.

Source: https://developer.enonic.com/learn/next.xp/stable

## Architecture Overview

Next.XP connects two systems:
- **Enonic XP** (backend): Content management, content types, Guillotine GraphQL API, draft/master branches, Content Studio editorial UI.
- **Next.js** (frontend): React-based rendering, server-side rendering (SSR), static site generation (SSG), App Router.

The `@enonic/nextjs-adapter` npm package bridges them by handling content fetching, component resolution, preview mode, and URL rewriting.

## Environment Configuration (.env)

Required variables in the Next.js project root `.env` file:

```
# Shared secret for preview mode authentication
ENONIC_API_TOKEN=mySecretKey

# Fully qualified Enonic application name
ENONIC_APP_NAME=com.example.myproject

# Locale-to-project/site mapping: <locale>:<project>/<site>[,<locale>:<project>/<site>]
ENONIC_MAPPINGS=en:intro/hmdb

# Base URL for the Guillotine API (without project and branch segments)
ENONIC_API=http://127.0.0.1:8080/site/
```

Multiple locale mappings example:
```
ENONIC_MAPPINGS=en:intro/hmdb,no:intro-no/hmdb
```

## Project File Structure

Standard Next.XP project layout after scaffolding from `nextxp-template`:

```
.env                                  # Environment variables
src/
    proxy.ts                          # Middleware routing by locale
    utils.ts                          # Token/path validation helpers
    components/
        _mappings.ts                  # Central component registry
        queries/                      # Guillotine GraphQL query functions
        views/                        # React view components for content types
        pages/                        # React page components
        parts/                        # React part components
        layouts/                      # React layout components
        macros/                       # Macro components for rich text
    phrases/
        en.json                       # i18n phrase files
    app/
        [locale]/
            [[...contentPath]]/
                page.tsx              # Main catch-all rendering page
            layout.tsx                # Root layout with header/footer
            error.tsx                 # Error handler
            not-found.tsx             # 404 handler
        api/
            preview/
                route.ts              # Preview mode API route
            renderable/
                route.ts              # Renderable check API route
            revalidate/
                route.ts              # ISR revalidation API route
```

## Component Registry API

All component registrations go in `src/components/_mappings.ts`.

### Content Type Mapping

```typescript
import {ComponentRegistry, APP_NAME} from '@enonic/nextjs-adapter';
import getMyType from './queries/getMyType';
import MyTypeView from './views/MyTypeView';

ComponentRegistry.addContentType(`${APP_NAME}:my-type`, {
    query: getMyType,    // GraphQL query function
    view: MyTypeView     // React component
});
```

### Page Mapping

```typescript
import MainPage from './pages/Main';

ComponentRegistry.addPage(`${APP_NAME}:main`, {
    view: MainPage
});
```

### Part Mapping

```typescript
import ChildList, {childListProcessor, getChildList} from './parts/ChildList';

ComponentRegistry.addPart(`${APP_NAME}:child-list`, {
    query: getChildList,         // Query object with query() and variables()
    processor: childListProcessor, // Optional post-processing function
    view: ChildList
});
```

### Layout Mapping

```typescript
import TwoColumnLayout from './layouts/TwoColumn';

ComponentRegistry.addLayout(`${APP_NAME}:two-column`, {
    view: TwoColumnLayout
});
```

Layout components receive `LayoutProps` (not `PageProps`) and access regions via `props.layout.regions`.

### Common Query

Data shared across all components on the page:

```typescript
ComponentRegistry.setCommonQuery([commonQuery, commonVariables]);
```

Remove if not needed to optimize performance.

### Macro Mapping

```typescript
import FactBox from './macros/FactBox';

ComponentRegistry.addMacro(`${APP_NAME}:factbox`, {
    view: FactBox,
    configQuery: '{ header }'
});
```

Register macros before any component that uses `RichTextView`.

## Guillotine GraphQL Query Patterns

### Content Type Query Function

A query function returns a GraphQL query string:

```typescript
import {APP_NAME_UNDERSCORED} from '@enonic/nextjs-adapter';

const getMovie = () => `
query($path:ID!){
  guillotine {
    get(key:$path) {
      displayName
      ... on ${APP_NAME_UNDERSCORED}_Movie {
        data {
          subtitle
          abstract
          release
          photos {
            ... on media_Image {
              imageUrl: imageUrl(type: absolute, scale: "width(500)")
            }
          }
        }
      }
    }
  }
}`;

export default getMovie;
```

### Part Query Object

Parts use a query object with `query()` and `variables()` functions to support dynamic configuration:

```typescript
export const getChildList = {
    query: function(path: string, context?: Context, config?: any): string {
        return `query($path:ID!, $order:String){
            guillotine {
                get(key:$path) {
                    displayName
                    children(sort: $order, first: 50) {
                        _path(type: siteRelative)
                        _id
                        displayName
                        type
                    }
                }
            }
        }`;
    },
    variables: function(path: string, context?: Context, config?: any): VariablesGetterResult {
        return {
            path,
            order: config?.sorting
        };
    }
};
```

### Type Introspection Pattern

Access content-type-specific fields via inline fragments. The type name follows the pattern: dots replaced with underscores, name capitalized.

- Content type `com.example.myproject:movie` becomes `com_example_myproject_Movie`
- Media images use `media_Image`

```graphql
... on com_example_myproject_Movie {
    data {
        subtitle
        photos {
            ... on media_Image {
                imageUrl: imageUrl(type: absolute, scale: "width(500)")
            }
        }
    }
}
```

## View Component Pattern

```typescript
import React from 'react';
import {FetchContentResult, getUrl, I18n} from '@enonic/nextjs-adapter';

const MyView = (props: FetchContentResult) => {
    const {displayName, data, parent} = props.data?.get as any;
    const meta = props.meta;

    return (
        <>
            <h2>{displayName}</h2>
            {/* Use getUrl() for all links */}
            <a href={getUrl(`/${parent._path}`, meta)}>Back</a>
        </>
    );
};

export default MyView;
```

Key adapter imports:
- `FetchContentResult` — props type for content type views.
- `PageProps` — props type for page components.
- `PartProps` — props type for part components.
- `LayoutProps` — props type for layout components.
- `MacroProps` — props type for macro components.
- `getUrl(path, meta)` — resolves URLs for both standalone and preview modes.
- `getAsset(path, meta)` — resolves static asset URLs.
- `richTextQuery(fieldName)` — generates the GraphQL query fragment for HTML area input types.
- `validateData(props)` — validates `FetchContentResult`, throws errors or `notFound()` for invalid data.
- `I18n.localize(key)` — localized string lookup from phrase files.
- `I18n.getLocale()` — returns current locale in server-side components.
- `I18n.setLocale(locale)` — sets the locale for the current request (called in layouts).
- `APP_NAME` — fully qualified app name from env config.
- `APP_NAME_UNDERSCORED` — app name with dots replaced by underscores for GraphQL introspection.
- `PORTAL_COMPONENT_ATTRIBUTE` — HTML attribute for page editor component identification.
- `CATCH_ALL` — wildcard content type name for debug/fallback views.
- `richTextQuery(fieldName)` — generates GraphQL query fragment for rich text fields.
- `validateData(data)` — validates `FetchContentResult` before rendering.
- `getRequestLocaleInfo({contentPath, headers})` — extracts locale from request for middleware.

Server-side imports (from `@enonic/nextjs-adapter/server`):
- `fetchContent(params)` — fetches content and resolves component mappings.
- `fetchContentPathsForAllLocales(basePath)` — generates paths for SSG across all locales.
- `fetchContentPathsForLocale(basePath, locale)` — generates paths for SSG for a single locale.
- `fetchGuillotine(contentApiUrl, options?)` — makes a custom request to Guillotine; used internally by `fetchContent()`.
- `fetchFromApi(apiUrl, body, options?)` — lower-level HTTP POST to any API endpoint.
- `getLocaleMapping(locale)` — resolves locale to project/site mapping from `ENONIC_MAPPINGS`.
- `getLocaleMappingByLocale(locale)` — alias for `getLocaleMapping`.
- `getLocaleMappingByProjectId(projectId)` — resolves project ID to its locale mapping.

Client-side imports (from `@enonic/nextjs-adapter/client`):
- `useLocaleContext()` — React hook returning `{locale, localize}` for client-side components.

View imports:
- `MainView` from `@enonic/nextjs-adapter/views/MainView` — renders the full page.
- `RegionsView` from `@enonic/nextjs-adapter/views/Region` — renders all regions of a page.
- `RegionView` from `@enonic/nextjs-adapter/views/Region` — renders a single named region (used in layouts).
- `RichTextView` from `@enonic/nextjs-adapter/views/RichTextView` — renders rich text fields with embedded images, links, and macros.
- `PropsView` from `@enonic/nextjs-adapter/views/PropsView` — debug view that displays raw props.

Additional types and utilities:
- `MetaData` — type for runtime metadata (apiUrl, baseUrl, locale, defaultLocale, renderMode).
- `RichTextData` — type for the rich text data shape returned by `richTextQuery`.
- `LocaleContextType` — type for the value returned by `useLocaleContext`.
- `Replacer` — type for custom element replacement functions used with `RichTextView`'s `customReplacer` prop.
- `RENDER_MODE` — enum-like constant for render mode detection (`NEXT`, `INLINE`, `EDIT`, `PREVIEW`, `LIVE`, `ADMIN`).
- `UrlProcessor` — URL processing class; use `UrlProcessor.setSiteKey(key)` to set the site key for URL resolution.

## Page Components with Regions

Pages define regions where editors can add parts, layouts, and text components:

Enonic page definition (`src/main/resources/site/pages/main/main.xml`):
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<page xmlns="urn:enonic:xp:model:1.0">
  <display-name>Main page</display-name>
  <form/>
  <regions>
      <region name="main"/>
  </regions>
</page>
```

Next.js page component:
```typescript
import type {PageProps} from '@enonic/nextjs-adapter';
import RegionsView from '@enonic/nextjs-adapter/views/Region';

const MainPage = (props: PageProps) => {
    const page = props.page;
    const regions = (!page.regions || !Object.keys(page.regions).length) ? {
        main: { name: 'main', components: [] }
    } : page.regions;

    return <RegionsView {...props} page={{...page, regions}} name="main"/>;
};

export default MainPage;
```

## Layout Components with Regions

Layouts are like parts but with regions, allowing nested component structures:

```typescript
import type {LayoutProps} from '@enonic/nextjs-adapter';
import {RegionView} from '@enonic/nextjs-adapter/views/Region';

const TwoColumnLayout = (props: LayoutProps) => {
    const regions = props.layout.regions;
    const {common, meta} = props;

    return (
        <div style={{display: 'flex', gap: '10px'}}>
            <RegionView name="left" components={regions['left']?.components} common={common} meta={meta}/>
            <RegionView name="right" components={regions['right']?.components} common={common} meta={meta}/>
        </div>
    );
};

export default TwoColumnLayout;
```

Use `RegionView` (singular, named export) for individual regions within layouts, and `RegionsView` (default export) for page-level rendering.

## Rich Text Rendering

Rich text fields (HtmlArea) may contain images, links, tables, and macros that need special processing.

### richTextQuery Helper

Use `richTextQuery(fieldName)` to generate the GraphQL fragment for rich text fields:

```typescript
import {APP_NAME_UNDERSCORED, richTextQuery} from '@enonic/nextjs-adapter';

const getPersonWithBio = () => `
query($path:ID!){
  guillotine {
    get(key:$path) {
      displayName
      ... on ${APP_NAME_UNDERSCORED}_Person {
        data {
          ${richTextQuery('bio')}
          photos {
            ... on media_Image {
              imageUrl: imageUrl(type: absolute, scale: "width(500)")
            }
          }
        }
      }
    }
  }
}`;
```

The `richTextQuery` helper generates the necessary sub-query to fetch rich text metadata (links, images, macros). It depends on registered macros, so the query must be a function (not a static string) to ensure macros are registered first.

### RichTextView Component

Render rich text fields with `RichTextView`:

```typescript
import RichTextView from '@enonic/nextjs-adapter/views/RichTextView';

const PersonWithBio = (props: FetchContentResult) => {
    const {displayName, data} = props.data?.get as any;
    const {bio} = data;
    const meta = props.meta;

    return (
        <>
            <h2>{displayName}</h2>
            <RichTextView data={bio} meta={meta}/>
        </>
    );
};
```

## Macro Components

Macros are custom components embedded within rich text fields.

### Macro Registration

Register macros with `ComponentRegistry.addMacro()`:

```typescript
import {ComponentRegistry, APP_NAME} from '@enonic/nextjs-adapter';
import FactBox from './macros/FactBox';

ComponentRegistry.addMacro(`${APP_NAME}:factbox`, {
    view: FactBox,
    configQuery: '{ header }'
});
```

- `configQuery` fetches macro form values (available as `config` prop in the component).
- The macro body is implicitly passed as `children`.
- Macros must be registered before any component that uses `RichTextView`.

### Macro Component

```typescript
import type {MacroProps} from '@enonic/nextjs-adapter';

const FactBox = ({name, children, config, meta}: MacroProps) => {
    const header = config.header?.length ? config.header : 'Fact Box';
    return (
        <ins>
            <strong>{header}</strong>
            {children}
        </ins>
    );
};

export default FactBox;
```

## Preview Mode Architecture

### Flow
1. Content Studio loads preview via the Next.XP proxy app installed in Enonic XP.
2. Next.XP proxy activates Next.js preview mode via the `/api/preview` route using the shared `ENONIC_API_TOKEN`.
3. In preview mode, Next.js queries the `draft` branch of the Guillotine API (unpublished content visible).
4. The Next.XP proxy rewrites static asset URLs to resolve correctly within Content Studio.
5. `getUrl()` in component code handles link rewriting for `/preview`, `/inline`, and `/edit` base paths.

### Setup Steps
1. Install the Next.XP app in Enonic XP from the application marketplace.
2. Add Next.XP to the target site in Content Studio (Edit site → Applications combobox).
3. Default configuration: URL `http://127.0.0.1:3000`, secret `mySecretKey`.
4. For production, override via app config in Enonic Cloud console.

### Branch Switching
- **Draft branch**: Used automatically when Content Studio preview is active. Shows unpublished content.
- **Master branch**: Used by the public Next.js frontend. Only published content is visible.
- Publishing content in Content Studio moves it from draft to master.

### Named Configurations for Multi-Frontend

When multiple Next.js front-ends connect to the same Enonic instance (e.g., per-market or per-language sites), use named configurations in `com.enonic.app.nextxp.cfg`:

```
# default config (used when no named config is assigned)
# nextjs.default.secret=yourSecret
# nextjs.default.url=http://127.0.0.1:4242

# named config 'marketA'
nextjs.marketA.secret=yourSecret
nextjs.marketA.url=https://your.next-site.com

# named config 'marketB'
nextjs.marketB.secret=yourOtherSecret
nextjs.marketB.url=https://your.other-next-site.com
```

Assign a named configuration to a site in Content Studio: edit the site → click the pencil icon next to the `Next.XP` app → select the named configuration from the list.

## Static Site Generation (SSG) and Incremental Static Regeneration (ISR)

The main catch-all page handler supports SSG with ISR:

```typescript
import {FetchContentResult, validateData} from "@enonic/nextjs-adapter";
import {fetchContent, fetchContentPathsForAllLocales} from "@enonic/nextjs-adapter/server";
import MainView from '@enonic/nextjs-adapter/views/MainView';
import "../../../components/_mappings";
import {Metadata} from 'next';
import {draftMode} from 'next/headers';

export const revalidate = 3600

export type PageProps = {
    locale: string,
    contentPath?: string[],
}

export default async function Page({params}: { params: Promise<PageProps> }) {
    const {isEnabled: draft} = await draftMode();
    const resolvedParams = await params;

    const data: FetchContentResult = await fetchContent({
        ...resolvedParams,
        contentPath: resolvedParams.contentPath || []
    });

    validateData(data);
    return <MainView {...data}/>;
};

export async function generateMetadata({params}: { params: Promise<PageProps> }): Promise<Metadata> {
    const resolvedParams = await params;
    const {common} = await fetchContent({
        ...resolvedParams,
        contentPath: resolvedParams.contentPath || []
    });
    return { title: common?.get?.displayName || 'Not found' };
}

export async function generateStaticParams(props: { params: PageProps }): Promise<any[]> {
    return await fetchContentPathsForAllLocales('\${site}/');
}
```

Key points:
- `revalidate = 3600` enables ISR with a 1-hour cache period.
- `params` is `Promise<PageProps>` in Next.js 15+ and must be awaited.
- `validateData(data)` checks fetch results before rendering.
- `generateStaticParams` pre-renders pages at build time for SSG.
- The Next.XP app triggers revalidation automatically when content is published.
- Start Next.js in production mode with `npm run prod` (builds then starts) for SSG.

## Internationalization (i18n)

### Locale Configuration

Multiple locales are configured via `ENONIC_MAPPINGS`:

```
ENONIC_MAPPINGS=en:intro/hmdb,no:intro-no/hmdb
```

The first entry becomes the `defaultLocale`. Each entry maps a locale code to an Enonic project and site path.

### Locale in Layouts

Set the locale for server-side rendering in the root layout:

```typescript
import {I18n, PORTAL_COMPONENT_ATTRIBUTE} from '@enonic/nextjs-adapter';

export default async function LocaleLayout({params, children}) {
    const resolvedParams = await params;
    await I18n.setLocale(resolvedParams.locale);
    // ...
}
```

### Server-Side Locale Access

```typescript
import {I18n} from '@enonic/nextjs-adapter';

const locale = I18n.getLocale();
const localizedText = I18n.localize('text.key');
```

### Client-Side Locale Access

```typescript
'use client';
import {useLocaleContext} from '@enonic/nextjs-adapter/client';

export default function ClientComponent() {
    const {locale, localize} = useLocaleContext();
    const text = localize('text.key');
}
```

### Middleware Locale Detection

The proxy middleware detects locale from the request path or `Accept-Language` header:

```typescript
import {getRequestLocaleInfo} from '@enonic/nextjs-adapter';

export function proxy(req: NextRequest) {
    const {locale, locales} = getRequestLocaleInfo({
        contentPath: req.nextUrl.pathname,
        headers: req.headers
    });
    // redirect to locale-prefixed path if needed
}
```

## Base Mappings

Import `@enonic/nextjs-adapter/baseMappings` in `_mappings.ts` to register built-in component type renderers:

```typescript
import "@enonic/nextjs-adapter/baseMappings";
```

This should be imported before custom component registrations.

## Deployment

### Enonic Cloud
1. Connect CLI: `enonic cloud login`
2. Install app: `enonic cloud app install`
3. Create ingress: target path `/site`, public path `/api`

### Next.js (Vercel or other)
1. Deploy the Next.js app to the hosting platform.
2. Set environment variables matching the production Enonic Cloud endpoints.
3. Configure Next.XP app in Enonic to point to the deployed Next.js URL.

### Production Environment Variables
```
ENONIC_APP_NAME=com.example.myproject
ENONIC_API=https://<account>-<solution>-<env>.enonic.net/api
ENONIC_API_TOKEN=<production-secret>
ENONIC_MAPPINGS=en:intro/hmdb,no:intro-no/hmdb
```

## Rich Text Rendering

Enonic content types may include HTML area fields (rich text). To render these correctly — including embedded images, links, and macros — use the `richTextQuery` helper and `RichTextView` component.

### Querying Rich Text

Use `richTextQuery(fieldName)` from `@enonic/nextjs-adapter` to generate the GraphQL fragment for an HTML area field. This generates the required query including image, link, and macro metadata:

```typescript
import {APP_NAME_UNDERSCORED, richTextQuery} from '@enonic/nextjs-adapter';

const getPersonWithBio = () => `
query($path:ID!){
  guillotine {
    get(key:$path) {
      displayName
      ... on ${APP_NAME_UNDERSCORED}_Person {
        data {
          ${richTextQuery('bio')}
          photos {
            ... on media_Image {
              imageUrl: imageUrl(type: absolute, scale: "width(500)")
            }
          }
        }
      }
    }
  }
}`;

export default getPersonWithBio;
```

The query function **must** be a function (not a static string) when using `richTextQuery`, because it depends on registered macros being available at execution time.

### Rendering Rich Text

Use the `RichTextView` component from `@enonic/nextjs-adapter/views/RichTextView`:

```typescript
import RichTextView from '@enonic/nextjs-adapter/views/RichTextView';

// In a view component:
<RichTextView data={bio} meta={meta} tag="section" className="bio"/>
```

Props:
- `data` — rich text data object returned by `richTextQuery`.
- `meta` — `MetaData` from `FetchContentResult`.
- `tag` — HTML wrapper tag (default: `'div'`). Optional.
- `className` — CSS class for the wrapper. Optional.
- `renderMacroInEditMode` — whether macros render in Content Studio edit mode (default: `true`). Optional.
- `customReplacer` — function for custom element processing (not invoked for image, link, macro nodes). Optional.

## Macro Registration

Macros are custom components embedded within rich text fields. They follow the same registration pattern as other components but use `ComponentRegistry.addMacro()`.

```typescript
import {ComponentRegistry, APP_NAME} from '@enonic/nextjs-adapter';
import FactBox from './macros/FactBox';

ComponentRegistry.addMacro(`${APP_NAME}:factbox`, {
    view: FactBox,
    configQuery: '{ header }'
});
```

Key rules:
- Macros use `configQuery` instead of `query`. The `configQuery` operates on the macro's form values, and the result is available in the React component's `config` prop.
- The macro body is implicitly passed to the component as `children`.
- Macros **must be registered before** any component that uses `RichTextView`. Best practice: register macros at the top of `_mappings.ts`.
- Macro React components receive `MacroProps`: `{ name, children, config, meta }`.

## Static Site Generation (SSG)

### Page Handler Pattern

The catch-all page handler at `src/app/[locale]/[[...contentPath]]/page.tsx` controls rendering and SSG:

```typescript
import {FetchContentResult, validateData} from '@enonic/nextjs-adapter';
import {fetchContent, fetchContentPathsForAllLocales} from '@enonic/nextjs-adapter/server';
import MainView from '@enonic/nextjs-adapter/views/MainView';
import '../../../components/_mappings';
import {draftMode} from 'next/headers';

export const revalidate = 3600;

export default async function Page({params}: {params: Promise<PageProps>}) {
    const {isEnabled: draft} = await draftMode();
    const resolvedParams = await params;

    const data: FetchContentResult = await fetchContent({
        ...resolvedParams,
        contentPath: resolvedParams.contentPath || []
    });

    validateData(data);

    return <MainView {...data}/>;
}

export async function generateStaticParams(props: { params: PageProps }): Promise<any[]> {
    return await fetchContentPathsForAllLocales('${site}/');
}

export async function generateMetadata({params}: {params: Promise<PageProps>}): Promise<Metadata> {
    const resolvedParams = await params;
    const {common} = await fetchContent({
        ...resolvedParams,
        contentPath: resolvedParams.contentPath || []
    });
    return {title: common?.get?.displayName || 'Not found'};
}
```

Key points:
- `validateData(data)` validates the response and throws `notFound()` for invalid data.
- `generateStaticParams()` uses `fetchContentPathsForAllLocales()` to pre-render pages at build time.
- `generateMetadata()` provides dynamic page titles from content.
- `revalidate` controls ISR (Incremental Static Regeneration) interval in seconds.
- `draftMode()` detects Content Studio preview mode, which bypasses static pages for fresh draft content.
- The Next.XP app automatically triggers revalidation of pages when content is published.

### StaticContent Component

Use `StaticContent` from `@enonic/nextjs-adapter/views/StaticContent` to disable client-side hydration conditionally (e.g., in Content Studio edit mode):

```typescript
import StaticContent from '@enonic/nextjs-adapter/views/StaticContent';

<StaticContent condition={isEdit}>
    <Header meta={meta}/>
    <main>{children}</main>
    <Footer/>
</StaticContent>
```

## Client-Side Locale Access

In client-side components, use the `useLocaleContext` hook from `@enonic/nextjs-adapter/client`:

```typescript
'use client';

import {useLocaleContext} from '@enonic/nextjs-adapter/client';

export default function ClientSideComponent() {
    const {locale, localize} = useLocaleContext();
    const localizedText = localize('text.key');
    // ...
}
```

This requires a `LocaleContextProvider` wrapper in the layout (included in the nextxp-template).
