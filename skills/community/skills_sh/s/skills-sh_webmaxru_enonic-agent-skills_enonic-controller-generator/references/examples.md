# Enonic XP Controller Examples

## Page Controller with Region

### Descriptor — `src/main/resources/site/pages/default/default.xml`

```xml
<page>
  <display-name>Default Page</display-name>
  <description>Standard page with a main region</description>
  <form/>
  <regions>
    <region name="main"/>
  </regions>
</page>
```

### Controller (TypeScript) — `src/main/resources/site/pages/default/default.ts`

```ts
import { getContent, pageUrl } from '/lib/xp/portal';
import thymeleafLib from '/lib/thymeleaf';

const view = resolve('default.html');

export function get(req) {
  const content = getContent();
  const model = {
    displayName: content.displayName,
    mainRegion: content.page.regions.main
  };
  return {
    body: thymeleafLib.render(view, model),
    contentType: 'text/html'
  };
}
```

### View — `src/main/resources/site/pages/default/default.html`

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <title data-th-text="${displayName}">Page Title</title>
</head>
<body>
  <main data-portal-region="main">
    <div data-th-each="component : ${mainRegion.components}"
         data-th-remove="tag"
         data-portal-component="${component.path}">
    </div>
  </main>
</body>
</html>
```

---

## Part Controller — Hero Banner

### Descriptor — `src/main/resources/site/parts/hero-banner/hero-banner.xml`

```xml
<part>
  <display-name>Hero Banner</display-name>
  <description>Displays a hero banner with heading and background image</description>
  <form>
    <input name="heading" type="TextLine">
      <label>Heading</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="subheading" type="TextLine">
      <label>Subheading</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
    <input name="backgroundImage" type="ImageSelector">
      <label>Background Image</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
  </form>
</part>
```

### Controller (TypeScript) — `src/main/resources/site/parts/hero-banner/hero-banner.ts`

```ts
import { getComponent, imageUrl } from '/lib/xp/portal';
import thymeleafLib from '/lib/thymeleaf';

const view = resolve('hero-banner.html');

export function get(req) {
  const component = getComponent();
  const config = component.config;

  const model = {
    heading: config.heading,
    subheading: config.subheading || '',
    backgroundImageUrl: config.backgroundImage
      ? imageUrl({ id: config.backgroundImage, scale: 'width(1920)' })
      : ''
  };

  return {
    body: thymeleafLib.render(view, model),
    contentType: 'text/html'
  };
}
```

### View — `src/main/resources/site/parts/hero-banner/hero-banner.html`

```html
<section class="hero-banner"
         data-th-attr="style=${'background-image: url(' + backgroundImageUrl + ')'}"
         data-th-if="${backgroundImageUrl}">
  <h1 data-th-text="${heading}">Heading</h1>
  <p data-th-text="${subheading}" data-th-if="${subheading}">Subheading</p>
</section>
<section class="hero-banner" data-th-unless="${backgroundImageUrl}">
  <h1 data-th-text="${heading}">Heading</h1>
  <p data-th-text="${subheading}" data-th-if="${subheading}">Subheading</p>
</section>
```

---

## Part Controller — Content List

### Descriptor — `src/main/resources/site/parts/content-list/content-list.xml`

```xml
<part>
  <display-name>Content List</display-name>
  <description>Lists child content items</description>
  <form>
    <input name="parentPath" type="ContentSelector">
      <label>Parent content</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    <input name="maxItems" type="Long">
      <label>Max items</label>
      <occurrences minimum="0" maximum="1"/>
    </input>
  </form>
</part>
```

### Controller (JavaScript) — `src/main/resources/site/parts/content-list/content-list.js`

```js
var portalLib = require('/lib/xp/portal');
var contentLib = require('/lib/xp/content');
var thymeleafLib = require('/lib/thymeleaf');

var view = resolve('content-list.html');

exports.get = function (req) {
  var component = portalLib.getComponent();
  var config = component.config;

  var result = contentLib.getChildren({
    key: config.parentPath,
    start: 0,
    count: config.maxItems || 10
  });

  var model = {
    items: result.hits
  };

  return {
    body: thymeleafLib.render(view, model),
    contentType: 'text/html'
  };
};
```

---

## Layout Controller — Two-Column

### Descriptor — `src/main/resources/site/layouts/two-column/two-column.xml`

```xml
<layout>
  <display-name>Two Column Layout</display-name>
  <description>Splits content into left and right columns</description>
  <form/>
  <regions>
    <region name="left"/>
    <region name="right"/>
  </regions>
</layout>
```

### Controller (TypeScript) — `src/main/resources/site/layouts/two-column/two-column.ts`

```ts
import { getComponent } from '/lib/xp/portal';
import thymeleafLib from '/lib/thymeleaf';

const view = resolve('two-column.html');

export function get(req) {
  const component = getComponent();

  const model = {
    leftRegion: component.regions.left,
    rightRegion: component.regions.right
  };

  return {
    body: thymeleafLib.render(view, model),
    contentType: 'text/html'
  };
}
```

### View — `src/main/resources/site/layouts/two-column/two-column.html`

```html
<div class="row">
  <div class="col-left" data-portal-region="left">
    <div data-th-each="component : ${leftRegion.components}"
         data-th-remove="tag"
         data-portal-component="${component.path}">
    </div>
  </div>
  <div class="col-right" data-portal-region="right">
    <div data-th-each="component : ${rightRegion.components}"
         data-th-remove="tag"
         data-portal-component="${component.path}">
    </div>
  </div>
</div>
```

---

## Response Processor — Inject Tracking Script

### Controller — `src/main/resources/site/processors/tracker.js`

```js
exports.responseProcessor = function (req, res) {
  var trackingScript = '<script src="https://cdn.example.com/tracker.js"></script>';

  if (!res.pageContributions.bodyEnd) {
    res.pageContributions.bodyEnd = [];
  }

  res.pageContributions.bodyEnd.push(trackingScript);
  return res;
};
```

### Registration — `src/main/resources/site/site.xml`

```xml
<site>
  <processors>
    <response-processor name="tracker" order="10"/>
  </processors>
  <form/>
</site>
```
