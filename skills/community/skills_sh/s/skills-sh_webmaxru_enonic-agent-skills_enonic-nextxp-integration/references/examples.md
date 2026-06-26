# Next.XP Examples

Complete working examples for common Next.XP integration patterns.

## Example 1: Content Type with Custom Query and View

### Guillotine Query (src/components/queries/getPerson.ts)

```typescript
import {APP_NAME_UNDERSCORED} from '@enonic/nextjs-adapter';

const getPerson = () => `
query($path:ID!){
  guillotine {
    get(key:$path) {
      displayName
      ... on ${APP_NAME_UNDERSCORED}_Person {
        data {
          dateofbirth
          photos {
            ... on media_Image {
              imageUrl: imageUrl(type: absolute, scale: "width(500)")
              attachments {
                name
              }
            }
          }
        }
      }
      parent {
        _path(type: siteRelative)
      }
    }
  }
}`;

export default getPerson;
```

### React View (src/components/views/Person.tsx)

```typescript
import React from 'react';
import {FetchContentResult, getUrl, I18n} from '@enonic/nextjs-adapter';
import Link from 'next/link';

const Person = (props: FetchContentResult) => {
    const {displayName, data, parent} = props.data?.get as any;
    const {photos} = data;
    const meta = props.meta;

    return (
        <>
            <div>
                <h2>{displayName}</h2>
                {photos.map((photo: any, i: number) => (
                    <img
                        key={i}
                        src={getUrl(photo.imageUrl, meta)}
                        title={getTitle(photo, displayName)}
                        alt={getTitle(photo, displayName)}
                        width="500"
                    />
                ))}
            </div>
            <p>
                <Link href={getUrl(`/${parent._path}`, meta)}>
                    {I18n.localize('back')}
                </Link>
            </p>
        </>
    );
};

export default Person;

function getTitle(photo: any, displayName: string) {
    return (photo.attachments || [])[0]?.name || displayName;
}
```

### Registration (src/components/_mappings.ts)

```typescript
import {ComponentRegistry, APP_NAME} from '@enonic/nextjs-adapter';
import getPerson from './queries/getPerson';
import Person from './views/Person';

ComponentRegistry.addContentType(`${APP_NAME}:person`, {
    query: getPerson,
    view: Person
});
```

## Example 2: Part with Query, Variables, and Processor

### Part Component (src/components/parts/ChildList.tsx)

```typescript
import {Context, PartProps, VariablesGetterResult} from '@enonic/nextjs-adapter';
import Link from 'next/link';
import React from 'react';

const FORBIDDEN_TYPES_REGEXP = "^media:.*|portal:fragment|portal:template-folder|portal:page-template$";

const ChildList = (props: PartProps) => {
    const {data, meta} = props;
    const children = data.get.children;
    if (!children || children.length === 0) {
        return null;
    }
    const prefix = meta.baseUrl +
        (meta.locale && meta.locale !== meta.defaultLocale ? meta.locale + '/' : '');

    return (
        <main style={{margin: '0 auto', maxWidth: 960, padding: '0 1.0875rem'}}>
            <ul>
                {children.map((child: any, i: number) => (
                    <li key={i}>
                        <Link href={prefix + child._path}>{child.displayName}</Link>
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default ChildList;

export const getChildList = {
    query: function(path: string, context?: Context, config?: any): string {
        return `query($path:ID!, $order:String){
            guillotine {
                getSite { displayName }
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

export async function childListProcessor(data: any, context?: Context, config?: any): Promise<any> {
    data.get.children = data.get.children?.filter(
        (child: any) => !child.type.match(FORBIDDEN_TYPES_REGEXP)
    );
    return data;
}
```

### Registration

```typescript
import ChildList, {childListProcessor, getChildList} from './parts/ChildList';

ComponentRegistry.addPart(`${APP_NAME}:child-list`, {
    query: getChildList,
    processor: childListProcessor,
    view: ChildList
});
```

## Example 3: Page Component with Region

### Enonic Page Definition (src/main/resources/site/pages/main/main.xml)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<page xmlns="urn:enonic:xp:model:1.0">
  <display-name>Main page</display-name>
  <description>Will be rendered by front-end</description>
  <form/>
  <regions>
      <region name="main"/>
  </regions>
</page>
```

### Next.js Page Component (src/components/pages/Main.tsx)

```typescript
import type {PageProps} from '@enonic/nextjs-adapter';
import React from 'react';
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

### Registration

```typescript
import MainPage from './pages/Main';

ComponentRegistry.addPage(`${APP_NAME}:main`, {
    view: MainPage
});
```

## Example 4: Layout with Two Columns

### Enonic Layout Definition (src/main/resources/site/layouts/2-column/2-column.xml)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<layout xmlns="urn:enonic:xp:model:1.0">
    <display-name>2 columns</display-name>
    <description>Provides left and right regions</description>
    <form/>
    <regions>
        <region name="left"/>
        <region name="right"/>
    </regions>
</layout>
```

### Next.js Layout Component (src/components/layouts/TwoColumnLayout.tsx)

```typescript
import type {LayoutProps} from '@enonic/nextjs-adapter';
import React from 'react';
import {RegionView} from '@enonic/nextjs-adapter/views/Region';

const TwoColumnLayout = (props: LayoutProps) => {
    const regions = props.layout.regions;
    const {common, meta} = props;

    return (
        <div style={{display: 'flex', gap: '10px', flexWrap: 'wrap'}}>
            <RegionView name="left" components={regions['left']?.components} common={common} meta={meta}/>
            <RegionView name="right" components={regions['right']?.components} common={common} meta={meta}/>
        </div>
    );
};

export default TwoColumnLayout;
```

### Registration

```typescript
import TwoColumnLayout from './layouts/TwoColumnLayout';

ComponentRegistry.addLayout(`${APP_NAME}:2-column`, {
    view: TwoColumnLayout
});
```

## Example 5: Rich Text with RichTextView

### Query with richTextQuery Helper (src/components/queries/getPersonWithBio.ts)

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
          dateofbirth
          photos {
            ... on media_Image {
              imageUrl: imageUrl(type: absolute, scale: "width(500)")
              attachments {
                name
              }
            }
          }
        }
      }
      parent {
        _path(type: siteRelative)
      }
    }
  }
}`;

export default getPersonWithBio;
```

### View with RichTextView (src/components/views/PersonWithBio.tsx)

```typescript
import React from 'react';
import {FetchContentResult, getUrl, I18n} from '@enonic/nextjs-adapter';
import Link from 'next/link';
import RichTextView from '@enonic/nextjs-adapter/views/RichTextView';

const PersonWithBio = (props: FetchContentResult) => {
    const {displayName, data, parent} = props.data?.get as any;
    const {bio, photos} = data;
    const meta = props.meta;

    return (
        <>
            <h2>{displayName}</h2>
            <RichTextView data={bio} meta={meta}/>
            <div>
                {photos.map((photo: any, i: number) => (
                    <img key={i}
                         src={getUrl(photo.imageUrl, meta)}
                         alt={displayName}
                         width="500"
                    />
                ))}
            </div>
            <p><Link href={getUrl(`/${parent._path}`, meta)}>{I18n.localize('back')}</Link></p>
        </>
    );
};

export default PersonWithBio;
```

### Registration

```typescript
import getPersonWithBio from './queries/getPersonWithBio';
import PersonWithBio from './views/PersonWithBio';

ComponentRegistry.addContentType(`${APP_NAME}:person`, {
    query: getPersonWithBio,
    view: PersonWithBio
});
```

## Example 6: Macro Component

### Macro Component (src/components/macros/FactBox.tsx)

```typescript
import type {MacroProps} from '@enonic/nextjs-adapter';
import React from 'react';

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

### Registration

Macros must be registered before any component that uses `RichTextView`:

```typescript
import FactBox from './macros/FactBox';

ComponentRegistry.addMacro(`${APP_NAME}:factbox`, {
    view: FactBox,
    configQuery: '{ header }'
});
```

## Example 7: Simple Part without Query (Config-only)

### Heading Part (src/components/parts/Heading.tsx)

```typescript
import React from 'react';
import {APP_NAME, PartData} from '@enonic/nextjs-adapter';

export const HEADING_PART_NAME = `${APP_NAME}:heading`;

export interface HeadingData {
    part: PartData;
    common: any;
}

const HeadingView = ({part, common}: HeadingData) => (
    <h2>{part?.config?.heading || common?.get?.displayName}</h2>
);

export default HeadingView;
```

### Registration

```typescript
import Heading from './parts/Heading';

ComponentRegistry.addPart(`${APP_NAME}:heading`, {
    view: Heading
});
```

## Example 8: Nested Type Introspection Query

Fetching a movie with nested person references and image URLs:

```graphql
query($path:ID!){
  guillotine {
    get(key:$path) {
      type
      displayName
      ... on com_example_myproject_Movie {
        data {
          subtitle
          abstract
          trailer
          release
          photos {
            ... on media_Image {
              imageUrl: imageUrl(type: absolute, scale: "width(500)")
            }
          }
          cast {
            character
            actor {
              displayName
              ... on com_example_myproject_Person {
                _path
                data {
                  photos {
                    ... on media_Image {
                      imageUrl: imageUrl(type: absolute, scale: "block(100,100)")
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```


