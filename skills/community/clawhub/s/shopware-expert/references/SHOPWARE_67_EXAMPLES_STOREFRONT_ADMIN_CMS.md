# Shopware 6.7 examples: Storefront, Administration, CMS

Full listings (neutralized `Acme` / `acme-*`). See `STOREFRONT_THEMES_TWIG.md`, `ADMINISTRATION_UI.md`, `CMS_AND_CONTENT.md` for official depth.

**Storefront controller and Store API conventions:** [CODE_GUIDELINES_ESSENTIALS.md](CODE_GUIDELINES_ESSENTIALS.md).

**Storefront forms (6.5+):** CSRF helpers were removed from the Storefront; use SameSite cookies. This file keeps the original form layout; omit `csrf_field()` in real 6.7 storefront forms (see `SHOPWARE_67_PRACTICAL_NOTES.md`).

---

## 5. Storefront (frontend)

### 5.1 Controller with PHP 8 attributes

```php
<?php declare(strict_types=1);

namespace Acme\ExamplePlugin\Controller\Storefront;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'])]
    public function showExample(SalesChannelContext $context): Response
    {
        return $this->renderStorefront('@AcmeExamplePlugin/storefront/page/example.html.twig', [
            'pageTitle' => 'Example Page'
        ]);
    }

    #[Route(path: '/example/form', name: 'frontend.example.form', methods: ['POST'])]
    public function handleForm(Request $request, SalesChannelContext $context): Response
    {
        $formData = $request->request->all();
        
        // Verarbeitung...
        
        $this->addFlash('success', 'Form submitted successfully');
        
        return $this->redirectToRoute('frontend.example.example');
    }
}
```

### 5.2 routes.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="Acme\ExamplePlugin\Controller\Storefront\ExampleController" type="attribute" />
</routes>
```

### 5.3 Twig templates

```twig
{# @AcmeExamplePlugin/storefront/page/example.html.twig #}
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_content %}
    {{ parent() }}
    
    <div class="acme-example-container">
        <h1>{{ pageTitle }}</h1>
        
        {# Flash Messages #}
        {% for type, messages in app.flashes %}
            {% for message in messages %}
                <div class="alert alert-{{ type }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endfor %}
        
        {# Formular #}
        <form action="{{ path('frontend.example.form') }}" method="post">
            {# No CSRF field in Shopware 6.5+ storefront (SameSite cookies). #}
            
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" name="name" class="form-control" required>
            </div>
            
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
{% endblock %}
```

### 5.4 JavaScript plugins

```javascript
// src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    static options = {
        delay: 500,
        selector: '.my-element'
    };

    init() {
        this._registerEvents();
    }
    
    _registerEvents() {
        window.addEventListener('scroll', this._onScroll.bind(this));
        this.el.addEventListener('click', this._onClick.bind(this));
    }
    
    _onScroll() {
        // Scroll-Logik
    }
    
    _onClick(event) {
        event.preventDefault();
        // Click-Logik
    }
}
```

```javascript
// src/Resources/app/storefront/src/main.js
import ExamplePlugin from './example-plugin/example-plugin.plugin';

const PluginManager = window.PluginManager;

// Basis-Registrierung
PluginManager.register('ExamplePlugin', ExamplePlugin);

// Mit DOM-Selector
PluginManager.register('ExamplePlugin', ExamplePlugin, '[data-example-plugin]');

// Lazy Loading (für große Plugins)
PluginManager.register('HeavyPlugin', () => import('./heavy-plugin/heavy-plugin.plugin'), '[data-heavy-plugin]');
```

### 5.5 Template integration

```twig
{# Daten-Attribute für JS-Plugin #}
<div data-example-plugin
     data-example-plugin-options='{"delay": 1000}'>
    Content
</div>
```

---

## 6. Administration (backend)

### 6.1 main.js entry point

```javascript
// src/Resources/app/administration/src/main.js
import './module/acme-example';
```

### 6.2 Module registration

```javascript
// src/Resources/app/administration/src/module/acme-example/index.js
import './page/example-list';
import './page/example-detail';

import deDE from './snippet/de-DE.json';
import enGB from './snippet/en-GB.json';

Shopware.Module.register('acme-example', {
    type: 'plugin',
    name: 'AcmeExample',
    title: 'acme-example.general.mainMenuItemGeneral',
    description: 'acme-example.general.description',
    color: '#ff6b35',
    icon: 'regular-shopping-bag',
    entity: 'acme_example',

    snippets: {
        'de-DE': deDE,
        'en-GB': enGB
    },

    routes: {
        list: {
            component: 'acme-example-list',
            path: 'list'
        },
        detail: {
            component: 'acme-example-detail',
            path: 'detail/:id',
            meta: {
                parentPath: 'acme.example.list'
            }
        },
        create: {
            component: 'acme-example-detail',
            path: 'create',
            meta: {
                parentPath: 'acme.example.list'
            }
        }
    },

    navigation: [{
        id: 'acme-example',
        path: 'acme.example.list',
        label: 'acme-example.general.mainMenuItemGeneral',
        icon: 'regular-shopping-bag',
        position: 100,
        parent: 'sw-marketing'  // oder: sw-catalogue, sw-content, sw-settings
    }]
});
```

### 6.3 Meteor components (Shopware 6.7+)

| Old (sw-*) | New (mt-*) |
|------------|------------|
| `sw-button` | `mt-button` |
| `sw-card` | `mt-card` |
| `sw-text-field` | `mt-text-field` |
| `sw-textarea-field` | `mt-textarea` |
| `sw-select-field` | `mt-select` |
| `sw-switch-field` | `mt-switch` |
| `sw-checkbox-field` | `mt-checkbox` |
| `sw-datepicker` | `mt-datepicker` |
| `sw-icon` | `mt-icon` |
| `sw-modal` | `mt-modal` |

### 6.4 Component with Pinia (6.7+)

```javascript
// src/Resources/app/administration/src/module/acme-example/page/example-list/index.js
import template from './example-list.html.twig';

const { Component } = Shopware;
const { Criteria } = Shopware.Data;

Component.register('acme-example-list', {
    template,

    inject: ['repositoryFactory'],

    data() {
        return {
            items: [],
            isLoading: false,
            sortBy: 'createdAt',
            sortDirection: 'DESC'
        };
    },

    computed: {
        repository() {
            return this.repositoryFactory.create('acme_example');
        },

        columns() {
            return [
                {
                    property: 'name',
                    label: this.$tc('acme-example.list.columnName'),
                    primary: true
                },
                {
                    property: 'active',
                    label: this.$tc('acme-example.list.columnActive')
                },
                {
                    property: 'createdAt',
                    label: this.$tc('acme-example.list.columnCreatedAt')
                }
            ];
        }
    },

    created() {
        this.getList();
    },

    methods: {
        async getList() {
            this.isLoading = true;
            
            const criteria = new Criteria();
            criteria.addSorting(Criteria.sort(this.sortBy, this.sortDirection));
            
            try {
                const result = await this.repository.search(
                    criteria,
                    Shopware.Context.api
                );
                this.items = result;
            } finally {
                this.isLoading = false;
            }
        }
    }
});
```

```twig
{# example-list.html.twig #}
<sw-page class="acme-example-list">
    <template #smart-bar-header>
        <h2>{{ $tc('acme-example.list.title') }}</h2>
    </template>

    <template #smart-bar-actions>
        <mt-button variant="primary" @click="$router.push({ name: 'acme.example.create' })">
            {{ $tc('acme-example.list.buttonCreate') }}
        </mt-button>
    </template>

    <template #content>
        <sw-entity-listing
            v-if="items"
            :items="items"
            :columns="columns"
            :repository="repository"
            :is-loading="isLoading"
            detail-route="acme.example.detail">
        </sw-entity-listing>
    </template>
</sw-page>
```

### 6.5 Snippets (translations)

```json
{
    "acme-example": {
        "general": {
            "mainMenuItemGeneral": "Example Module",
            "description": "Manage example items"
        },
        "list": {
            "title": "Example Items",
            "buttonCreate": "Create",
            "columnName": "Name",
            "columnActive": "Active",
            "columnCreatedAt": "Created At"
        },
        "detail": {
            "title": "Example Detail",
            "cardGeneral": "General"
        }
    }
}
```

---

## 7. CMS elements and blocks

### 7.1 Register CMS element

```javascript
// src/Resources/app/administration/src/module/sw-cms/elements/acme-custom/index.js
import './component';
import './config';
import './preview';

Shopware.Service('cmsService').registerCmsElement({
    name: 'acme-custom',
    label: 'sw-cms.elements.acmeCustom.label',
    component: 'sw-cms-el-acme-custom',
    configComponent: 'sw-cms-el-config-acme-custom',
    previewComponent: 'sw-cms-el-preview-acme-custom',
    defaultConfig: {
        headline: {
            source: 'static',
            value: 'Default Headline'
        },
        content: {
            source: 'static',
            value: ''
        }
    }
});
```

### 7.2 Storefront template for CMS element

```twig
{# src/Resources/views/storefront/element/cms-element-acme-custom.html.twig #}
{% block element_acme_custom %}
    <div class="cms-element-acme-custom">
        <h2>{{ element.config.headline.value }}</h2>
        <div class="content">
            {{ element.config.content.value|raw }}
        </div>
    </div>
{% endblock %}
```

