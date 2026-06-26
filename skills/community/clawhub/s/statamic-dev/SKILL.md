# Statamic CMS Development

This skill covers how to work with the Statamic CMS layer: content structure, blueprints, fieldsets, and writing content files.

## Content File Format

All content lives in `content/` as Markdown files with YAML front matter. The front matter holds all field data; the body after `---` is typically empty (Bard fields are stored in the front matter, not the Markdown body).

```yaml
---
id: unique-id
blueprint: page
title: My Page
some_field: value
---
```

Every entry must have an `id` (unique across the site) and a `blueprint` that determines which fields are available.

## Collections

Collections live in `content/collections/`. Each collection has a config YAML at `content/collections/{handle}.yaml` and entries as `.md` files in `content/collections/{handle}/`.

### Collection Config

```yaml
# content/collections/{handle}.yaml
title: Articles
template: articles/show     # Default Antlers template
layout: layout              # Layout wrapper
route: '/articles/{slug}'   # URL pattern
sort_dir: desc
revisions: true
structure:                  # Only for structured collections
  root: true                # true = can have entries at root level
taxonomies:
  - categories              # Attach taxonomy terms
preview_targets:
  -
    label: Entry
    url: '{permalink}'
    refresh: true
```

The `pages` collection is a default Statamic structured collection using `{parent_uri}/{slug}` routing and a tree structure.

## Blueprints

Blueprints define the field schema for entries. They live in `resources/blueprints/collections/{collection}/{blueprint}.yaml`.

### Blueprint Structure

```yaml
title: Page
tabs:
  main:
    display: Main
    sections:
      -
        display: Content
        fields:
          -
            handle: title
            field:
              type: text
              required: true
              validate:
                - required
          -
            import: my_fieldset        # Import a fieldset
  seo:
    display: SEO
    sections:
      -
        fields:
          -
            import: common/seo         # Import from subfolder
  sidebar:
    display: Sidebar
    sections:
      -
        fields:
          -
            handle: slug
            field:
              type: slug
              localizable: true
              validate: 'max:200'
```

Tabs organise the CP editing UI. The `sidebar` tab renders in the right sidebar. Use `import:` to pull in reusable fieldsets.

## Fieldsets

Reusable field groups live in `resources/fieldsets/`. They are imported into blueprints and other fieldsets with `import: {path}`.

Fieldsets in subfolders are referenced with dot or slash notation (e.g. `import: common/seo` or `import: common.seo`).

### Fieldset Structure

```yaml
title: My Fieldset
fields:
  -
    handle: heading
    field:
      type: text
      display: Heading
  -
    handle: content
    field:
      type: bard
      display: Content
      buttons:
        - h2
        - h3
        - bold
        - italic
        - unorderedlist
        - orderedlist
        - quote
        - link
```

## Writing Bard Content

Bard fields store content as a ProseMirror document structure in YAML. This is an array of nodes, not raw HTML or Markdown. Understanding this structure is essential when writing or editing content files by hand.

### Basic Structure

A Bard field value is an array of block-level nodes. Each node has a `type` and usually `content` (an array of inline nodes):

```yaml
my_bard_field:
  -
    type: paragraph
    content:
      -
        type: text
        text: 'Plain paragraph text.'
```

### Paragraphs

The most common node. Contains inline `text` nodes:

```yaml
-
  type: paragraph
  content:
    -
      type: text
      text: 'This is a paragraph.'
```

A paragraph with text alignment uses `attrs`:

```yaml
-
  type: paragraph
  attrs:
    textAlign: center
  content:
    -
      type: text
      text: 'Centered paragraph text.'
```

### Headings

Headings use the `heading` type with a `level` attribute:

```yaml
-
  type: heading
  attrs:
    level: 2
  content:
    -
      type: text
      text: 'This is an H2'
```

Valid levels: `1` through `6` (corresponding to h1–h6). Only use levels that are enabled in the Bard field's `buttons` config.

### Inline Formatting (Marks)

Bold, italic, and other inline styles are applied via `marks` on text nodes. Multiple marks can be combined on a single text node:

**Bold:**
```yaml
-
  type: text
  marks:
    -
      type: bold
  text: 'Bold text'
```

**Italic:**
```yaml
-
  type: text
  marks:
    -
      type: italic
  text: 'Italic text'
```

**Bold + Italic:**
```yaml
-
  type: text
  marks:
    -
      type: bold
    -
      type: italic
  text: 'Bold and italic'
```

**Underline:**
```yaml
-
  type: text
  marks:
    -
      type: underline
  text: 'Underlined text'
```

**Strikethrough:**
```yaml
-
  type: text
  marks:
    -
      type: strike
  text: 'Struck through'
```

**Inline code:**
```yaml
-
  type: text
  marks:
    -
      type: code
  text: 'some_code()'
```

**Superscript / Subscript:**
```yaml
-
  type: text
  marks:
    -
      type: superscript
  text: '2'
```

**Small text:**
```yaml
-
  type: text
  marks:
    -
      type: small
  text: 'Fine print'
```

### Links

Links are a mark with `attrs` containing the `href`:

```yaml
-
  type: text
  marks:
    -
      type: link
      attrs:
        href: 'https://example.com'
  text: 'Click here'
```

Link with target and rel attributes:

```yaml
-
  type: text
  marks:
    -
      type: link
      attrs:
        href: 'https://example.com'
        target: _blank
        rel: 'noopener noreferrer'
  text: 'External link'
```

Links to Statamic entries use the `entry::` prefix:

```yaml
-
  type: text
  marks:
    -
      type: link
      attrs:
        href: 'entry::some-entry-id'
  text: 'Internal link'
```

### Mixed Inline Content

A paragraph often contains a mix of plain and formatted text. Each run of text with different formatting is a separate node in the `content` array:

```yaml
-
  type: paragraph
  content:
    -
      type: text
      text: 'This is '
    -
      type: text
      marks:
        -
          type: bold
      text: 'important'
    -
      type: text
      text: ' information.'
```

### Lists

**Unordered list:**
```yaml
-
  type: bulletList
  content:
    -
      type: listItem
      content:
        -
          type: paragraph
          content:
            -
              type: text
              text: 'First item'
    -
      type: listItem
      content:
        -
          type: paragraph
          content:
            -
              type: text
              text: 'Second item'
```

**Ordered list:**
```yaml
-
  type: orderedList
  attrs:
    start: 1
  content:
    -
      type: listItem
      content:
        -
          type: paragraph
          content:
            -
              type: text
              text: 'Step one'
    -
      type: listItem
      content:
        -
          type: paragraph
          content:
            -
              type: text
              text: 'Step two'
```

### Blockquotes

```yaml
-
  type: blockquote
  content:
    -
      type: paragraph
      content:
        -
          type: text
          text: 'This is a quoted passage.'
```

### Horizontal Rule

```yaml
-
  type: horizontalRule
```

### Code Blocks

```yaml
-
  type: codeBlock
  attrs:
    language: php
  content:
    -
      type: text
      text: 'echo "Hello World";'
```

### Images

Images in Bard reference assets by their path:

```yaml
-
  type: image
  attrs:
    src: 'assets::images/photo.jpg'
    alt: 'Description of the image'
```

### Tables

```yaml
-
  type: table
  content:
    -
      type: tableRow
      content:
        -
          type: tableHeader
          content:
            -
              type: paragraph
              content:
                -
                  type: text
                  text: 'Column 1'
        -
          type: tableHeader
          content:
            -
              type: paragraph
              content:
                -
                  type: text
                  text: 'Column 2'
    -
      type: tableRow
      content:
        -
          type: tableCell
          content:
            -
              type: paragraph
              content:
                -
                  type: text
                  text: 'Cell value'
        -
          type: tableCell
          content:
            -
              type: paragraph
              content:
                -
                  type: text
                  text: 'Another value'
```

### Empty Bard Field

An empty Bard field can be represented as an empty array or omitted entirely:

```yaml
story: []
```

## Globals

Global sets store site-wide data. Configs live at `content/globals/{handle}.yaml`, values at `content/globals/default/{handle}.yaml`, and blueprints at `resources/blueprints/globals/{handle}.yaml`.

### Accessing Globals in Templates

```antlers
{{ settings:website_name }}
{{ settings:primary_contact_tel }}
{{ settings:socials }}
    {{ name }} — {{ link }}
{{ /settings:socials }}
```

## Taxonomies

Taxonomies live in `content/taxonomies/`. Each taxonomy has a config YAML and term files in a subfolder.

### Taxonomy Terms

Terms are YAML files in `content/taxonomies/{handle}/`:

```yaml
# content/taxonomies/categories/my-term.yaml
title: My Term
```

### Attaching Taxonomies to Collections

In the collection config:

```yaml
taxonomies:
  - categories
```

In the blueprint, add a terms field:

```yaml
-
  handle: category
  field:
    type: terms
    taxonomies:
      - categories
    display: Category
    mode: select
    max_items: 1
```

In content files, reference terms by slug:

```yaml
category:
  - my_term
```

## Navigation

Navigation menus live in `content/navigation/`. Each has a config YAML and a tree YAML in `content/trees/navigation/`.

### Navigation Config

```yaml
# content/navigation/{handle}.yaml
title: Primary
collections:
  - pages
max_depth: 1
```

### Navigation Blueprints

Navigation items can have custom fields via blueprints at `resources/blueprints/navigation/{handle}.yaml`.

### Rendering Navigation

```antlers
{{ nav:primary }}
    <a href="{{ url }}">{{ title }}</a>
{{ /nav:primary }}
```

## Statamic Forms

Statamic's built-in form system handles user submissions. Form configs live at `resources/forms/{handle}.yaml` and blueprints at `resources/blueprints/forms/{handle}.yaml`.

### Form Config

```yaml
title: 'Contact Form'
honeypot: honeypot
store: true
email:
  -
    to: '{{ site:contact_email }}'
    from: '{{ email }}'
    reply_to: '{{ email }}'
    subject: 'New Contact Submission'
    html: emails/contact
```

### Rendering Forms in Templates

```antlers
{{ form:contact }}
    {{ if errors }}
        {{ errors }}
            <p>{{ value }}</p>
        {{ /errors }}
    {{ /if }}
    {{ if success }}
        <p>Thank you!</p>
    {{ else }}
        <input type="text" name="name" value="{{ old:name }}" />
        <!-- more fields -->
        <button type="submit">Submit</button>
    {{ /if }}
{{ /form:contact }}
```

## Assets

Asset containers are configured at `content/assets/{handle}.yaml`. The main container is `assets`. Assets are referenced by their path relative to the container:

```yaml
featured_image: images/photo.jpg
gallery:
  - images/photo1.jpg
  - images/photo2.jpg
```

In Bard fields, assets use the `assets::` prefix:

```yaml
-
  type: image
  attrs:
    src: 'assets::images/photo.jpg'
    alt: 'A photo'
```

## Replicator Fields

Replicators allow content editors to build flexible content by stacking predefined sets of fields. They appear in blueprints, fieldsets, and globals.

### Replicator Content Format

```yaml
items:
  -
    id: item-1
    type: my_set
    value: 'Some value'
    label: 'Some label'
    enabled: true
  -
    id: item-2
    type: my_set
    value: 'Another value'
    label: 'Another label'
    enabled: true
```

Each item needs `id`, `type` (matching the set handle), and `enabled`. The remaining fields come from the set's field definitions.

## Link Fields

Statamic's `link` fieldtype can store various link types:

```yaml
# Entry link
cta_link: 'entry::some-entry-id'

# URL
button_url: 'https://example.com'

# Relative path
cta_link: /some-page
```

## Entries Field

The `entries` fieldtype stores references to other entries by their ID:

```yaml
# Single entry
related: b031fb38-4392-42b8-9b72-4554d1fed7c5

# Multiple entries
team_members:
  - person-entry-id-1
  - person-entry-id-2
```

## Addons

Statamic addons are Laravel packages that extend Statamic's functionality. They live in `addons/{vendor}/{name}/` during local development and are registered as path repositories in the root `composer.json`.

### Addon Directory Structure

A Statamic addon follows this layout:

```
addons/{vendor}/{name}/
├── composer.json              # Package definition + Statamic/Laravel metadata
├── package.json               # Node dependencies (if addon has CP JS)
├── vite.config.js             # Vite config for building CP assets
├── phpunit.xml                # Test configuration
├── config/
│   └── {name}.php             # Publishable config file
├── resources/
│   ├── js/
│   │   ├── cp.js              # CP JavaScript entry point
│   │   └── components/        # Vue components for the CP
│   ├── views/                 # Blade views (for CP pages)
│   └── dist/                  # Built assets (committed for distribution)
├── routes/
│   ├── api.php                # Public/API routes
│   └── cp.php                 # Control Panel routes
├── src/
│   ├── ServiceProvider.php    # Main addon service provider
│   ├── Http/
│   │   ├── Controllers/       # Route controllers
│   │   └── Middleware/         # Custom middleware
│   ├── Support/               # Helper/utility classes
│   ├── Policies/              # Authorization policies
│   ├── Exceptions/            # Custom exception classes
│   └── Tools/                 # Domain-specific classes
│       └── Contracts/         # Interfaces
└── tests/
    ├── TestCase.php           # Base test case
    ├── Unit/                  # Unit tests
    ├── Integration/           # Integration tests
    └── Property/              # Property-based tests (optional)
```

### Addon composer.json

The addon's `composer.json` defines the package, its autoloading, and Statamic/Laravel metadata:

```json
{
    "name": "{vendor}/{name}",
    "autoload": {
        "psr-4": {
            "{Vendor}\\{Name}\\": "src"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "{Vendor}\\{Name}\\Tests\\": "tests"
        }
    },
    "require": {
        "statamic/cms": "^6.0"
    },
    "require-dev": {
        "orchestra/testbench": "^10.8"
    },
    "config": {
        "allow-plugins": {
            "pixelfear/composer-dist-plugin": true
        }
    },
    "extra": {
        "statamic": {
            "name": "My Addon",
            "description": "What the addon does"
        },
        "laravel": {
            "providers": [
                "{Vendor}\\{Name}\\ServiceProvider"
            ]
        }
    },
    "minimum-stability": "dev",
    "prefer-stable": true
}
```

Key points:
- `extra.statamic` provides the addon name and description for the Statamic marketplace/CP.
- `extra.laravel.providers` registers the service provider for auto-discovery.
- `pixelfear/composer-dist-plugin` must be allowed for Statamic's asset distribution.

### Registering the Addon in the Root Project

In the root `composer.json`, add a path repository and require the addon:

```json
{
    "repositories": [
        {
            "type": "path",
            "url": "addons/{vendor}/{name}"
        }
    ],
    "require": {
        "{vendor}/{name}": "*@dev"
    }
}
```

Then run `composer update` to symlink the addon into `vendor/`.

### The Service Provider

Every addon has a service provider that extends `Statamic\Providers\AddonServiceProvider`. This is the central registration point for everything the addon provides.

```php
<?php

namespace {Vendor}\{Name};

use Statamic\Facades\CP\Nav;
use Statamic\Providers\AddonServiceProvider;

class ServiceProvider extends AddonServiceProvider
{
    // Namespace for Blade views: used as '{namespace}::view.name'
    protected $viewNamespace = '{name}';

    // Vite configuration for CP JavaScript/CSS assets
    protected $vite = [
        'input' => [
            'resources/js/cp.js',
        ],
        'publicDirectory' => 'resources/dist',
        'hotFile' => __DIR__.'/../resources/dist/hot',
    ];

    public function register(): void
    {
        parent::register();

        // Merge default config so config('{name}.key') works immediately
        $this->mergeConfigFrom(__DIR__.'/../config/{name}.php', '{name}');

        // Register singletons that need to be available early
        $this->app->singleton(SomeRepository::class);
    }

    public function bootAddon(): void
    {
        // Publish config file: php artisan vendor:publish --tag={name}-config
        $this->publishes([
            __DIR__.'/../config/{name}.php' => config_path('{name}.php'),
        ], '{name}-config');

        // Register CP navigation items
        $this->bootCp();

        // Conditionally load routes, bindings, etc.
        if (! config('{name}.enabled')) {
            return; // Addon is invisible when disabled
        }

        $this->loadRoutesFrom(__DIR__.'/../routes/api.php');

        // Register additional singletons
        $this->app->singleton(SomeService::class, function ($app) {
            return new SomeService($app);
        });
    }

    protected function bootCp(): void
    {
        Nav::extend(function ($nav) {
            $nav->tools('My Addon')
                ->route('{name}.settings.index')
                ->icon('some-icon');
        });
    }
}
```

Key patterns:
- `register()` runs first — merge config and bind early singletons here.
- `bootAddon()` is the Statamic-specific boot method (not `boot()`). Load routes, publish assets, and register CP nav here.
- The `$vite` property tells Statamic where to find the addon's built JS/CSS assets.
- The `$viewNamespace` property sets the Blade view namespace.
- Use a kill switch pattern (`config('{name}.enabled')`) to make the addon completely invisible when disabled — no routes, no bindings.
- CP nav items should always be registered (even when the addon is disabled) so admins can access settings to enable it.

### AddonServiceProvider Built-in Properties

`AddonServiceProvider` provides several properties you can set to register things declaratively:

```php
// Register route files
protected $routes = [
    'cp' => __DIR__.'/../routes/cp.php',
    'web' => __DIR__.'/../routes/web.php',
    'actions' => __DIR__.'/../routes/actions.php',
];

// Register event listeners
protected $listen = [
    SomeEvent::class => [SomeListener::class],
];

// Register custom fieldtypes
protected $fieldtypes = [MyFieldtype::class];

// Register custom tags
protected $tags = [MyTag::class];

// Register custom modifiers
protected $modifiers = [MyModifier::class];

// Register custom widgets (CP dashboard)
protected $widgets = [MyWidget::class];

// Register custom actions (bulk actions in listings)
protected $actions = [MyAction::class];

// Register custom scopes (query scopes for listings)
protected $scopes = [MyScope::class];

// Register custom policies
protected $policies = [
    SomeModel::class => SomePolicy::class,
];

// Register publishable assets
protected $publishables = [
    __DIR__.'/../public' => 'vendor/{name}',
];

// Register scheduled commands
protected $commands = [MyCommand::class];

// Register middleware
protected $middlewareGroups = [
    'statamic.cp.authenticated' => [MyMiddleware::class],
];

// Register update scripts
protected $updateScripts = [UpdateSomething::class];
```

### Config Files

Addon config files live in `config/` within the addon and are publishable to the app's `config/` directory.

```php
// config/{name}.php
<?php

return [
    'enabled' => env('MY_ADDON_ENABLED', false),
    'some_setting' => env('MY_ADDON_SETTING', 'default'),
    'nested' => [
        'option' => env('MY_ADDON_NESTED_OPTION', true),
    ],
];
```

In the service provider, merge it in `register()`:

```php
$this->mergeConfigFrom(__DIR__.'/../config/{name}.php', '{name}');
```

And publish it in `bootAddon()`:

```php
$this->publishes([
    __DIR__.'/../config/{name}.php' => config_path('{name}.php'),
], '{name}-config');
```

Users publish with: `php artisan vendor:publish --tag={name}-config`

### Routes

Addon routes are standard Laravel route files. API routes and CP routes are typically separate.

**API routes** (`routes/api.php`):

```php
<?php

use Illuminate\Support\Facades\Route;
use {Vendor}\{Name}\Http\Controllers\MyController;
use {Vendor}\{Name}\Http\Middleware\MyMiddleware;

Route::prefix('{name}')
    ->middleware([MyMiddleware::class])
    ->group(function () {
        Route::post('/action', [MyController::class, 'action']);
        Route::get('/status', [MyController::class, 'status']);
    });
```

**CP routes** (`routes/cp.php`):

```php
<?php

use Illuminate\Support\Facades\Route;
use {Vendor}\{Name}\Http\Controllers\SettingsController;

Route::prefix('{name}')->group(function () {
    Route::get('/settings', [SettingsController::class, 'index'])->name('{name}.settings.index');
    Route::post('/settings', [SettingsController::class, 'update'])->name('{name}.settings.update');
});
```

CP routes are automatically wrapped in Statamic's CP middleware (authentication, etc.). Load API routes manually in `bootAddon()` with `$this->loadRoutesFrom()`. CP routes can be declared via the `$routes` property or loaded manually.

### CP Views and Vue Components

Addon CP pages use Blade views that extend Statamic's layout and mount Vue components.

**Blade view** (`resources/views/settings/index.blade.php`):

```blade
@extends('statamic::layout')

@section('title', 'My Addon Settings')

@section('content')
    <my-settings-component
        :settings='@json($settings)'
        update-url="{{ cp_route('{name}.settings.update') }}"
        csrf-token="{{ csrf_token() }}"
    ></my-settings-component>
@endsection
```

**JS entry point** (`resources/js/cp.js`):

```javascript
import MySettings from './components/MySettings.vue';

Statamic.booting(() => {
    Statamic.$components.register('my-settings-component', MySettings);
});
```

Vue components are registered via `Statamic.$components.register()` during the `Statamic.booting()` lifecycle hook. The component name in JS must match the tag name used in the Blade view.

### CP Controllers

CP controllers extend `Statamic\Http\Controllers\CP\CpController` and can use Statamic's user/permission system:

```php
<?php

namespace {Vendor}\{Name}\Http\Controllers;

use Illuminate\Http\Request;
use Statamic\Facades\User;
use Statamic\Http\Controllers\CP\CpController;

class SettingsController extends CpController
{
    public function index()
    {
        abort_unless(User::current()?->isSuper(), 403);

        $settings = config('{name}');

        return view('{name}::settings.index', compact('settings'));
    }

    public function update(Request $request)
    {
        abort_unless(User::current()?->isSuper(), 403);

        $validated = $request->validate([
            'enabled' => 'boolean',
            'some_setting' => 'nullable|string',
        ]);

        // Persist settings (to YAML, database, etc.)

        if ($request->wantsJson()) {
            return response()->json(['message' => 'Settings saved.']);
        }

        return redirect()->back()->with('success', 'Settings saved.');
    }
}
```

### Vite Configuration for Addons

Addons use Vite with the `@statamic/cms` vite plugin and `laravel-vite-plugin`:

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import statamic from '@statamic/cms/vite-plugin';

export default defineConfig({
    plugins: [
        statamic(),
        laravel({
            input: ['resources/js/cp.js'],
            refresh: true,
            publicDirectory: 'resources/dist',
            hotFile: 'resources/dist/hot',
        }),
    ],
});
```

**package.json**:

```json
{
    "private": true,
    "scripts": {
        "dev": "rm -rf resources/dist/build && vite",
        "build": "vite build"
    },
    "devDependencies": {
        "@statamic/cms": "file:./vendor/statamic/cms/resources/dist-package",
        "laravel-vite-plugin": "^1.3.0",
        "vite": "^6.4.1"
    }
}
```

The `@statamic/cms` dependency points to the local Statamic dist package within the addon's vendor directory. Run `pnpm install` (or `npm install`) from within the addon directory, then `pnpm run build` to compile assets into `resources/dist/build/`.

### Testing Addons

Addon tests use Orchestra Testbench with Statamic's `AddonTestCase`:

**Base TestCase** (`tests/TestCase.php`):

```php
<?php

namespace {Vendor}\{Name}\Tests;

use {Vendor}\{Name}\ServiceProvider;
use Statamic\Testing\AddonTestCase;

abstract class TestCase extends AddonTestCase
{
    protected string $addonServiceProvider = ServiceProvider::class;
}
```

**PHPUnit config** (`phpunit.xml`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    backupGlobals="false"
    bootstrap="vendor/autoload.php"
    colors="true"
    processIsolation="false"
    stopOnFailure="false">
  <testsuites>
    <testsuite name="Test Suite">
      <directory suffix="Test.php">./tests</directory>
    </testsuite>
  </testsuites>
  <php>
    <env name="APP_ENV" value="testing"/>
    <env name="APP_KEY" value="base64:ybcI9MKuhLnESRSuWDfnJQuohOXMBaynfbTC5Y5i1FE="/>
    <env name="CACHE_DRIVER" value="array"/>
    <env name="SESSION_DRIVER" value="array"/>
    <env name="QUEUE_CONNECTION" value="sync"/>
  </php>
</phpunit>
```

Run tests from the addon directory: `./vendor/bin/phpunit`

Tests have their own `composer.json` dependencies (e.g. `orchestra/testbench`) and their own `vendor/` directory, separate from the root project.

### Middleware

Custom middleware follows standard Laravel patterns. Register it in route groups or via the service provider:

```php
<?php

namespace {Vendor}\{Name}\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class MyMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Pre-processing logic (auth, validation, etc.)

        if ($someConditionFails) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        return $next($request);
    }
}
```

### Creating a New Addon — Step by Step

1. Create the directory structure:
   ```
   addons/{vendor}/{name}/
   ├── composer.json
   ├── src/
   │   └── ServiceProvider.php
   └── config/
       └── {name}.php
   ```

2. Set up `composer.json` with the `extra.statamic` and `extra.laravel.providers` keys.

3. Create the `ServiceProvider` extending `AddonServiceProvider`.

4. Register the addon in the root `composer.json` as a path repository and require it.

5. Run `composer update` from the project root.

6. If the addon has CP assets:
   - Add `package.json` and `vite.config.js`.
   - Create `resources/js/cp.js` as the entry point.
   - Run `pnpm install` and `pnpm run build` from the addon directory.

7. If the addon has config:
   - Create `config/{name}.php`.
   - Merge it in `register()` and publish it in `bootAddon()`.
   - Run `php artisan vendor:publish --tag={name}-config`.

8. If the addon has routes:
   - Create `routes/cp.php` and/or `routes/api.php`.
   - Load them in the service provider.

9. If the addon has tests:
   - Add `orchestra/testbench` to `require-dev`.
   - Create `tests/TestCase.php` extending `AddonTestCase`.
   - Add `phpunit.xml`.
   - Run `composer install` from the addon directory to set up its own vendor.

### Updating an Existing Addon

When modifying an addon:

- PHP changes in `src/` take effect immediately (the addon is symlinked via Composer path repository).
- Config changes require `php artisan config:clear` or republishing.
- Vue/JS changes require rebuilding: run `pnpm run build` from the addon directory.
- New routes or service provider changes may require `php artisan cache:clear`.
- New test files are picked up automatically by PHPUnit.
- If you add new Composer dependencies to the addon, run `composer update` from both the addon directory and the root project.
