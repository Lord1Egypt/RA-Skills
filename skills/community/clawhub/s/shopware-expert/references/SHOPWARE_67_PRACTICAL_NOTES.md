# Shopware 6.7 practical notes (requirements, breaking changes, commands, assets, learnings)

Derived from the same internal 6.7 guide; **neutralized** examples and **English** section titles where the source was German. Cross-check `RELEASE_AND_UPGRADES.md`, `APPS_VS_PLUGINS_AND_PATHS.md`.

**Backward compatibility, Twig/JS/API rules (official summary):** [CODE_GUIDELINES_ESSENTIALS.md](CODE_GUIDELINES_ESSENTIALS.md) and the full [backward compatibility](https://developer.shopware.com/docs/resources/guidelines/code/backward-compatibility/) guide when changing templates or public extension APIs.

**DDEV:** If you use DDEV, prefix with `ddev exec` or run `ddev ssh` first; plain `bin/console` is shown for generic Linux/macOS shells.

**Related (full code listings):** [SHOPWARE_67_EXAMPLES_PLUGIN_DAL.md](SHOPWARE_67_EXAMPLES_PLUGIN_DAL.md), [SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md](SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md).

---

## 1. System requirements

| Komponente | Version | Hinweise |
|------------|---------|----------|
| **PHP** | 8.2 - 8.4 | PHP 8.2 ist Minimum |
| **Node.js** | 20+ | Für Admin-Builds |
| **MySQL** | 8.0.17+ | Vermeide 8.0.20, 8.0.21 |
| **MariaDB** | 10.11+ | Vermeide 10.11.5, 11.0.3 |
| **Symfony** | 7.x | |
| **Redis** | 7.0+ | Optional |
| **PHPUnit** | 11.x | Für Tests |

---

## 2. Architecture overview

### 2.1 Core directory layout

```
src/
├── Core/                    # Framework-Grundlage
│   ├── Framework/           # Events, DAL, Context, DI
│   ├── System/              # SystemConfig, SalesChannel
│   ├── Content/             # Product, Category, CMS, Media
│   └── Checkout/            # Cart, Order, Payment, Shipping
├── Storefront/              # Frontend (Twig, JS, SCSS)
│   ├── Controller/
│   ├── Resources/views/     # Twig-Templates
│   └── Theme/               # Theme-System
├── Administration/          # Vue.js 3 Admin-Interface
│   └── Resources/app/administration/
└── Elasticsearch/           # Search-Integration
```

### 2.2 Plugin structure

```
AcmeExamplePlugin/
├── composer.json
├── src/
│   ├── AcmeExamplePlugin.php      # Plugin-Basisklasse
│   ├── Controller/
│   │   ├── Administration/
│   │   └── Storefront/
│   ├── Core/
│   │   └── Content/
│   │       └── Example/
│   │           ├── ExampleDefinition.php
│   │           ├── ExampleEntity.php
│   │           └── ExampleCollection.php
│   ├── Migration/
│   ├── Resources/
│   │   ├── config/
│   │   │   ├── services.xml
│   │   │   └── config.xml
│   │   ├── app/
│   │   │   ├── administration/
│   │   │   │   └── src/
│   │   │   │       ├── main.js
│   │   │   │       └── module/
│   │   │   └── storefront/
│   │   │       └── src/
│   │   │           ├── main.js
│   │   │           ├── scss/
│   │   │           └── js/
│   │   └── views/
│   ├── Service/
│   └── Subscriber/
└── tests/
```



---

## 10. Shopware 6.7 breaking changes

### 10.1 Critical changes

| Bereich | Änderung | Impact |
|---------|----------|--------|
| **Build** | Webpack → Vite | Separate Plugin-Versionen für 6.6/6.7 |
| **Vue** | Vue 3 Kompatibilität entfernt | Nur native Vue 3 |
| **State** | Vuex → Pinia | `Shopware.State` → `Shopware.Store` |
| **Components** | sw-* → mt-* | Alle UI-Komponenten umbenannt |
| **Routing** | Annotations entfernt | Nur PHP 8 Attributes |
| **Caching** | Store-API Caching entfernt | Andere Caching-Strategie |
| **ESI** | Header/Footer via ESI | Template-Struktur geändert |

### 10.2 PHP changes

```php
// Alle Properties müssen native Typen haben
// Vorher:
protected $myProperty;

// Nachher:
protected string $myProperty;
```

### 10.3 Vuex to Pinia migration

```javascript
// Vorher (Vuex)
Shopware.State.get('cmsPageState');
Shopware.State.commit('cmsPageState/setPage', page);

// Nachher (Pinia)
Shopware.Store.get('cmsPage');
Shopware.Store.get('cmsPage').page = page;
```

---

## 11. Useful commands

```bash
# Cache
ddev ssh
bin/console cache:clear

# Plugin Management
bin/console plugin:refresh
bin/console plugin:install -a AcmeExamplePlugin
bin/console plugin:update -c -r -n AcmeExamplePlugin
bin/console plugin:uninstall AcmeExamplePlugin

# Datenbank
bin/console database:migrate
bin/console database:create-migration -p AcmeExamplePlugin --name CreateExampleTable
bin/console database:migrate-destructive AcmeExamplePlugin --all

# Theme
bin/console theme:compile
bin/console theme:change --all Storefront

# Admin/Storefront Builds (innerhalb Plugin-Verzeichnis)
./bin/build-administration.sh
./bin/build-storefront.sh
./bin/watch-administration.sh
./bin/watch-storefront.sh

# Assets
bin/console assets:install

# Scheduled Tasks
bin/console scheduled-task:register
bin/console scheduled-task:run
bin/console scheduled-task:run-single swag.cleanup_old_data

# System
bin/console system:update:prepare
bin/console system:update:finish

# DDEV spezifisch
ddev start
ddev stop
ddev ssh
```

---

## 12. Further links

### Official documentation
- [Developer Docs](https://developer.shopware.com/docs/) - Hauptdokumentation
- [GitHub Repository](https://github.com/shopware/shopware)
- [Upgrade Guide 6.7](https://github.com/shopware/shopware/blob/trunk/UPGRADE-6.7.md)
- [Release Info 6.7](https://github.com/shopware/shopware/blob/trunk/RELEASE_INFO-6.7.md)

### Components and UI
- [Meteor Component Library](https://meteor.shopware.com/) - UI Komponenten
- [Shopware UI](https://shopware.github.io/meteor-admin-sdk/) - Admin SDK

### Frameworks
- [Symfony Docs](https://symfony.com/doc/current/)
- [Vue 3 Docs](https://vuejs.org/guide/)
- [Pinia Docs](https://pinia.vuejs.org/)
- [Twig Docs](https://twig.symfony.com/doc/)

### Community
- [Shopware Community Discord](https://chat.shopware.com)
- [Shopware Forum](https://forum.shopware.com)


---

## 13. Storefront asset build process (Shopware 6.7+)

### 13.1 IMPORTANT: theme:compile does NOT build plugin JavaScript

**Common misconception:** `theme:compile` only compiles theme SCSS/CSS, **not** plugin JavaScript files.

| Build command | What is built |
|--------------|-----------------|
| `theme:compile` | Theme SCSS/CSS only (no plugin JS!) |
| `bin/build-storefront.sh` | Storefront Core + alle Plugins (mit Webpack) |
| `shopware-cli extension build` | Einzelnes Plugin (mit ESBuild) |

### 13.2 Plugin structure for storefront assets

```
PluginName/
├── src/
│   └── Resources/
│       └── app/
│           └── storefront/
│               ├── src/                    # Source-Dateien
│               │   ├── main.js            # Entry Point (REQUIRED)
│               │   ├── plugin/
│               │   │   └── my-plugin.plugin.js
│               │   └── scss/
│               │       └── base.scss
│               ├── dist/                  # Kompilierte Assets (wird ausgeliefert!)
│               │   └── storefront/
│               │       └── js/
│               │           └── plugin-name/
│               │               └── plugin-name.js
│               └── package.json           # Optional: npm Dependencies
```

### 13.3 Build options for plugin assets

#### Option A: shopware-cli (recommended for 6.7+)

```bash
# Installation: https://developer.shopware.com/docs/products/cli/
brew install shopware/tap/shopware-cli  # macOS

# Build des Plugins (nutzt ESBuild - schneller)
shopware-cli extension build ./custom/plugins/MeinPlugin

# Mit Konfiguration (.shopware-extension.yml)
```

**.shopware-extension.yml:**
```yaml
build:
  zip:
    assets:
      enable_es_build_for_admin: true
      enable_es_build_for_storefront: true
```

#### Option B: classic Shopware build

```bash
# Baut Storefront Core + alle Plugins
./bin/build-storefront.sh

# Dann Assets installieren
bin/console assets:install
```

#### Option C: compile theme only (uses existing dist/)

```bash
# Schnellste Variante - nutzt bereits kompilierte dist/
# Die dist/ Dateien müssen bereits im Plugin sein!
bin/console theme:compile
```

### 13.4 Storefront vs administration build tools

| Bereich | Build-Tool in 6.7 | Config-Datei |
|---------|-------------------|--------------|
| **Storefront** | Webpack/ESBuild (unchanged) | `webpack.config.js` (optional) |
| **Administration** | **Vite** (neu ab 6.7) | `vite.config.mts` |

**⚠️ Achtung:** Nur die Administration wurde auf Vite umgestellt! Die Storefront verwendet weiterhin Webpack.

### 13.5 main.js entry point (storefront)

```javascript
// src/Resources/app/storefront/src/main.js
import MyPlugin from './plugin/my-plugin.plugin';

const PluginManager = window.PluginManager;

// Synchrone Registrierung
PluginManager.register('MyPlugin', MyPlugin, '[data-my-plugin]');

// Lazy Loading (für bessere Performance)
PluginManager.register('HeavyPlugin', () => import('./heavy-plugin/heavy-plugin.plugin'), '[data-heavy-plugin]');

// Hot Module Replacement
if (module.hot) {
    module.hot.accept();
}
```

### 13.6 Production: ship precompiled assets

**Best Practice:** Plugins sollten vorkompilierte Assets im `dist/` Verzeichnis mitliefern:

1. **Entwickler** baut das Plugin mit `shopware-cli` oder `build-storefront.sh`
2. **Die dist/ Dateien** werden committed und im Repository mitgeliefert
3. **Endkunde** installiert das Plugin und führt nur `theme:compile` aus

```bash
# Für Endkunden (Production) - Einfach!
bin/console plugin:install MeinPlugin
bin/console plugin:activate MeinPlugin
bin/console theme:compile  # Nutzt die mitgelieferten dist/ Dateien
```


---

### 14.4 Composer vs. custom/plugins - Wichtiger Unterschied

**Kritisch:** Prüfe immer, aus welchem Pfad das Plugin wirklich läuft!

```bash
# Prüfe, ob Plugin aus Composer oder custom/plugins läuft
ddev exec bin/console plugin:list

# Oder direkt in der Datenbank:
ddev mysql -e "SELECT name, managed_by_composer, path FROM plugin WHERE name LIKE '%ExamplePlugin%'"
```

| Quelle | Pfad | Managed by Composer |
|--------|------|---------------------|
| **Composer (path repo)** | `vendor/acme/example-plugin/` → Symlink zu `custom/static-plugins/AcmeExamplePlugin/` | `1` |
| **Lokal** | `custom/plugins/AcmeExamplePlugin/` | `0` |

**Bei Path Repos (`"type":"path","url":"custom/static-plugins/*"`):** `vendor/` ist ein Symlink – Änderungen in `custom/static-plugins/` sind sofort in `vendor/` sichtbar. Für `composer.json`-Änderungen (z. B. plugin-icon) trotzdem `composer update acme/example-plugin` ausführen, damit `installed.json` aktualisiert wird.

**Wenn `managed_by_composer = 1`:**
- Änderungen in der Quelldatei (custom/static-plugins oder vendor) reichen
- Für composer.json: `composer update` + `plugin:refresh` (siehe 14.20)

**Best Practice für Entwicklung:**
```bash
# Plugin aus Composer entfernen, lokale Version nutzen
composer remove acme/example-plugin
# Dann aus custom/plugins installieren
bin/console plugin:install AcmeExamplePlugin
```

---

### 14.5 Null-Safe in Twig-Templates (Email-Templates)

**Problem:** Twig crasht bei `null` Werten:
```twig
{# CRASH: Impossible to access attribute ("letterName") on a null variable #}
{{ letterContext.salutation.letterName }}
```

**Lösung:** Null-Check vor dem Zugriff:
```twig
{# KORREKT: Null-safe mit ternary operator #}
{{ letterContext.salutation is not null ? letterContext.salutation.letterName : '' }}

{# ODER: Null-Coalescing Operator (??) #}
{{ letterContext.salutation.letterName ?? '' }}
```

**Anwendung in Email-Templates:**
```twig
<p>Sehr geehrte/r 
    {{ letterContext.salutation is not null ? letterContext.salutation.letterName : '' }} 
    {{ letterContext.firstName }} 
    {{ letterContext.lastName }},
</p>
```

---

### 14.6 FormCmsHandler Konflikte vermeiden

**Problem:** Shopwares `FormCmsHandler` greift auf Custom-Formulare zu, wenn die Klasse `cms-element-form` verwendet wird.

```twig
{# FALSCH: FormCmsHandler verarbeitet das Formular zusätzlich #}
<div class="cms-element-form" data-form-cms-handler="true">
    <form>...</form>
</div>
```

**Lösung:** Eigene CSS-Klasse verwenden:
```twig
{# KORREKT: Nur eigenes Plugin verarbeitet das Formular #}
<div class="cms-element-acme-example-form">
    <form data-example-form="true">...</form>
</div>
```

**Zusätzlicher Schutz im JS:**
```javascript
// Submit-Event hart abfangen
_handleSubmit(event) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    
    // Double-Submit verhindern
    if (this.isSubmitting) return;
    this.isSubmitting = true;
    
    // ... Rest der Logik
}
```

---

### 14.7 Step-Indikator: Scope-Problem beheben

**Problem:** Step-Indikator außerhalb des Formulars, JS sucht innerhalb:
```javascript
// FALSCH: Sucht nur im Formular
const step1 = this.el.querySelector('.step-1'); // null, weil außerhalb
```

**Lösung:** Im gemeinsamen Parent suchen:
```javascript
// KORREKT: Sucht im gemeinsamen Wrapper
_showStep(step) {
    const indicatorRoot = this.el.closest('.example-form-wrapper');
    const step1 = indicatorRoot.querySelector('.step-1');
    const step2 = indicatorRoot.querySelector('.step-2');
    const step3 = indicatorRoot.querySelector('.step-3');
    // ...
}
```

---

### 14.8 Step-Farben korrekt definieren

| Zustand | Klasse | Farbe |
|---------|--------|-------|
| Aktiv (current) | `.active` | Blau |
| Abgeschlossen | `.completed` | Grün |
| Fehler | `.error` | Rot |

**Step 3 bei Erfolg = Grün (completed):**
```javascript
if (response.type === 'success') {
    // Step 1 & 2: completed (grün)
    // Step 3: completed (grün) - NICHT active (blau)
    this._showStep(3, 'completed');
}
```

**Step 3 bei Fehler = Rot (error):**
```javascript
if (response.type === 'warning') {
    // Widerruf gespeichert, aber Mail fehlgeschlagen
    this._showStep(3, 'error');
}
```

---

### 14.9 node_modules in .gitignore

**Wichtig:** `node_modules` niemals ins Git-Repository committen!

```bash
# .gitignore
/node_modules/
/vendor/
/var/
/public/theme/
/public/bundles/
```

**Wenn node_modules bereits im Repo:**
```bash
# Entfernen und in .gitignore aufnehmen
git rm -r --cached node_modules
echo "/node_modules/" >> .gitignore
git add .gitignore
git commit -m "Remove node_modules from repository"
```

---

## 14. Practical learnings and best practices (session notes)

> **Note:** Field experiences from Shopware 6.7 plugin work; neutralized and partially translated from the source guide.

---

### 14.10 CSRF-Tokens in Shopware 6.5+ (WICHTIG!)

**Ab Shopware 6.5 wurden CSRF-Tokens komplett aus dem Storefront entfernt!**

| Version | CSRF-Handling |
|---------|---------------|
| **6.4 und älter** | `{{ sw_csrf('route.name') }}` in Twig |
| **6.5+ (inkl. 6.7)** | **Keine CSRF-Tokens mehr** - Schutz via SameSite-Cookies |

**Falsch (veraltet):**
```twig
{# Diese Funktionen existieren NICHT mehr in 6.7! #}
{{ sw_csrf('frontend.example.submit') }}
{{ csrf_field() }}
{{ csrf_token('route.name') }}
```

**Richtig (Shopware 6.7):**
```twig
{# Einfach KEIN CSRF-Token im Formular #}
<form action="{{ path('frontend.example.submit') }}" method="POST">
    {# Formularfelder #}
    <button type="submit">Absenden</button>
</form>
```

**Referenz:** [Shopware ADR - Deprecate Storefront CSRF](https://developer.shopware.com/docs/resources/references/adr/2022-11-16-deprecate-csrf.html)

---

### 14.11 CMS-Elemente: Kritische Registrierungs-Reihenfolge

**Häufigster Fehler:** CMS-Elemente importieren Komponenten, registrieren sie aber nicht!

**FALSCH (Element wird nicht im Admin angezeigt):**
```javascript
// elements/my-element/index.js
import './component';      // Nur importiert, nicht registriert!
import './config';         // Nur importiert, nicht registriert!
import './preview';        // Nur importiert, nicht registriert!

Shopware.Service('cmsService').registerCmsElement({
    name: 'my-element',
    component: 'sw-cms-el-my-element',  // ← Komponente existiert nicht!
    // ...
});
```

**CORRECT (pattern from AcmeAccordionElement):**
```javascript
// elements/my-element/index.js

// 1. Zuerst ALLE Komponenten registrieren
Shopware.Component.register('sw-cms-el-preview-my-element', () => import('./preview'));
Shopware.Component.register('sw-cms-el-config-my-element', () => import('./config'));
Shopware.Component.register('sw-cms-el-my-element', () => import('./component'));

// 2. DANN das Element registrieren
Shopware.Service('cmsService').registerCmsElement({
    name: 'my-element',
    label: 'sw-cms.elements.myElement.label',
    component: 'sw-cms-el-my-element',
    configComponent: 'sw-cms-el-config-my-element',
    previewComponent: 'sw-cms-el-preview-my-element',
    defaultConfig: {
        // ...
    }
});
```

---

### 14.12 CMS-Blöcke: Storefront-Templates nicht vergessen!

CMS-Blöcke brauchen **zwei** Template-Sätze:

1. **Admin-Templates** (für Layout-Editor):
   - `blocks/my-block/component/template.html.twig`
   - `blocks/my-block/preview/template.html.twig`

2. **Storefront-Templates** (für Frontend-Ausgabe):
   - `views/storefront/block/cms-block-my-block.html.twig` ← **Wird oft vergessen!**

**Storefront-Block-Template-Struktur:**
```twig
{# cms-block-my-block.html.twig #}
{% block block_my_block %}
    {% set element = block.slots.getSlot('content') %}

    <div class="col-12" data-cms-element-id="{{ element.id }}">
        {% block block_my_block_inner %}
            {% sw_include "@PluginName/storefront/element/cms-element-" ~ element.type ~ ".html.twig" ignore missing %}
        {% endblock %}
    </div>
{% endblock %}
```

**Wichtig:** Ohne das Storefront-Block-Template wird der Block im Frontend leer angezeigt (nur `cms-block-container-row row cms-row`)!

---

### 14.13 Controller für reine API/JSON-Antworten

Für Controller, die nur JSON zurückgeben (keine Twig-Templates rendern):

**Nicht erweitern:**
```php
// FALSCH - StorefrontController hat Twig-Abhängigkeiten
class MyController extends StorefrontController
{
    // Symfony versucht setTwig() aufzurufen
}
```

**Stattdessen:**
```php
// RICHTIG - Einfache Klasse ohne Twig-Abhängigkeit
use Symfony\Component\HttpFoundation\JsonResponse;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class MyController
{
    public function __construct(
        private MyService $myService,
        private DataValidator $dataValidator
    ) {}

    #[Route(path: '/api/action', name: 'frontend.api.action', methods: ['POST'])]
    public function action(Request $request): JsonResponse
    {
        // ...
        return new JsonResponse(['success' => true]);
    }
}
```

**services.xml:** Keine `setTwig()` oder `setContainer()` Calls für solche Controller!

---

### 14.14 Preview-Komponenten: SCSS nicht vergessen

**Pattern aus funktionierenden Plugins (AcmeAccordionElement):**

```javascript
// preview/index.js
import template from './template.html.twig';
import './styles.scss';  // ← Wichtig!

export default {
    template,
};
```

**SCSS-Datei (preview/styles.scss):**
```scss
.sw-cms-el-preview-my-element {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 80px;
    padding: 16px;
    background-color: #e0aaaa;
    border-radius: 4px;

    &__title {
        font-size: 14px;
        font-weight: 600;
        color: #1a1a1a;
        text-align: center;
    }
}
```

**Farben für Preview:**
- Commerce/CTA-Elemente: Orange-Ton (`#ff6b35` - example brand)
- Formular-Elemente: Blau-Ton (`#17a2b8`)
- Content-Elemente: Neutral (`#e0aaaa`)

---

### 14.15 Typo-Check: Slot-Namen und Element-Namen

**Kritischer Fehler:** Slot-Name passt nicht zu Element-Name

```javascript
// Block-Definition
slots: {
    content: 'acme-example-buton',  // ← Tippfehler! 'button' nicht 'buton'
}

// Element-Definition
Shopware.Service('cmsService').registerCmsElement({
    name: 'acme-example-button',  // ← Korrekt
    // ...
});
```

**Empfehlung:** Immer Copy-Paste für Namen verwenden, nie abtippen!

---

### 14.16 services.xml: Autowiring-Probleme vermeiden

**Problem:** Symfony wirft Fehler wegen fehlender `setTwig()` Methode

**Ursache:** Controller wird als `autowire="true"` behandelt, hat aber keine Twig-Injection

**Lösung:** Explizite Service-Definition ohne Autowiring:
```xml
<service id="Acme\ExamplePlugin\Controller\Storefront\MyController" 
         public="true" 
         autowire="false" 
         autoconfigure="false">
    <argument type="service" id="Acme\ExamplePlugin\Service\MyService"/>
    <argument type="service" id="Shopware\Core\Framework\Validation\DataValidator"/>
    <tag name="controller.service_arguments"/>
</service>
```

---

### 14.17 E-Mail-Konfiguration über config.xml

**E-Mail-Templates im Plugin konfigurierbar machen:**

**WICHTIG – Sprachen explizit angeben:** Labels und HelpTexte in `config.xml` müssen `lang="de-DE"` und `lang="en-GB"` haben. Ohne explizites `de-DE` fällt Shopware auf Englisch zurück, auch wenn der Admin auf Deutsch eingestellt ist.

```xml
<!-- config.xml -->
<config>
    <card>
        <title lang="de-DE">E-Mail Konfiguration</title>
        <title lang="en-GB">Email Configuration</title>
        
        <input-field type="text">
            <name>adminEmail</name>
            <label lang="de-DE">Admin E-Mail Empfänger</label>
            <label lang="en-GB">Admin Email Recipient</label>
            <helpText lang="de-DE">E-Mail-Adresse für Admin-Benachrichtigungen</helpText>
            <helpText lang="en-GB">Email address for admin notifications</helpText>
            <defaultValue>admin@example.com</defaultValue>
        </input-field>
        
        <input-field type="single-select">
            <name>confirmationEmailTemplate</name>
            <label lang="de-DE">Kunden E-Mail Template</label>
            <label lang="en-GB">Customer Email Template</label>
            <options>
                <option>
                    <id>example_confirmation</id>
                    <name>Example confirmation</name>
                </option>
            </options>
        </input-field>
    </card>
</config>
```

**Zugriff im Service:**
```php
$adminEmail = $this->systemConfigService->get('AcmeExamplePlugin.config.adminEmail');
```

---

### 14.18 Zwei-Agenten-Entwicklungsprozess

**Empfohlener Workflow für komplexe Plugins:**

1. **Implementierungs-Agent:** Setzt den Code um
2. **Review-Agent:** Prüft gegen Best Practices und Shopware-Doku

**Vorteile:**
- Frühe Fehlererkennung
- Wissenstransfer zwischen Agenten
- Qualitätssicherung

**Kritische Prüfpunkte beim Review:**
- ✅ Shopware 6.7 Kompatibilität (Meteor Components)
- ✅ CMS-Element Registrierung korrekt?
- ✅ Storefront-Templates vorhanden?
- ✅ CSRF-Tokens entfernt (6.5+)?
- ✅ PHP 8 native Types?

---

### 14.19 Debugging-Checkliste

**Problem: CMS-Element/Block wird nicht angezeigt**

1. `bin/console cache:clear`
2. `./bin/build-administration.sh` ausführen
3. Browser Hard-Reload (Strg+F5)
4. Prüfen: `Shopware.Component.register()` vor `registerCmsElement()`?
5. Prüfen: Alle Template-Dateien vorhanden?

**Problem: Block im Frontend leer**

1. Storefront-Block-Template vorhanden? (`cms-block-*.html.twig`)
2. Theme neu kompilieren: `bin/console theme:compile`
3. Slot-Name in Block-Definition korrekt?

**Problem: Controller wirft Twig-Fehler**

1. Controller erweitert `StorefrontController`?
2. Wenn nur JSON: Nicht von `StorefrontController` erweitern!
3. services.xml: `setTwig()` entfernen

---

### 14.20 Plugin-Icon nach Änderung sichtbar machen

**Problem:** Nach Änderung von `plugin-icon` in `composer.json` oder Hinzufügen einer Icon-Datei wird das Icon im Admin unter „Erweiterungen“ nicht angezeigt.

**`cache:clear` reicht nicht aus!** Shopware speichert das Icon beim Plugin-Refresh in der Datenbank. Die Composer-Metadaten müssen zuerst aktualisiert werden:

```bash
# 1. Composer-Metadaten aktualisieren (liest composer.json neu)
composer update acme/example-plugin

# 2. Plugin-Liste aus Dateisystem in DB übertragen (inkl. Icon)
bin/console plugin:refresh

# 3. Optional: Cache leeren
bin/console cache:clear
```

**Ursache:** `PluginService` liest das Icon aus `vendor/.../plugin-icon-path` und speichert es als `iconRaw` in der Plugin-Tabelle. Ohne `composer update` bleibt die alte `installed.json`, ohne `plugin:refresh` wird die DB nicht aktualisiert.

---

### 14.21 Mail-Templates: Migration für bestehende Installationen

**Problem:** Eine Migration erstellt Mail-Templates nur bei **neuen** Installationen. Shops, die das Plugin bereits installiert haben, führen die Migration nicht erneut aus.

**Lösung:** Zusätzliche Migration, die **bestehende** `mail_template_translation`-Einträge per UPDATE anpasst:

- Templates über `mail_template_type.technical_name` finden (nicht über `system_config`)
- `content_html` und `content_plain` komplett ersetzen (robuster als String-Einfügungen)
- Für jede Sprache (`de-DE`/`en-GB`) das passende Template setzen

**Beispiel-Aufbau:**
```php
$typeId = $connection->fetchOne(
    'SELECT id FROM mail_template_type WHERE technical_name = :name',
    ['name' => 'acme_example_confirmation']
);
$templates = $connection->fetchAllAssociative(
    'SELECT id FROM mail_template WHERE mail_template_type_id = :typeId',
    ['typeId' => $typeId]
);
// Pro Template: mail_template_translation per UPDATE anpassen
```

---

### 14.22 Mail template wording (example: legal vs action)

German shops often confuse two terms (keep this distinction when writing copy):

- **Legal disclosure text** = static information shown to the customer (policy / instructions).
- **Customer action** = the act they took (e.g. submitted a cancellation or request).

In **confirmation emails**, address the **action** (e.g. “Thank you for your submission”) rather than naming the long legal disclosure heading. Adapt to your locale and lawyer-approved wording.

---

### 14.23 Dateistruktur-Checkliste für CMS-Plugins

**Komplette Struktur für CMS-Element + Block:**

```
PluginName/
├── src/
│   ├── Resources/
│   │   ├── app/
│   │   │   └── administration/
│   │   │       └── src/
│   │   │           └── module/
│   │   │               └── sw-cms/
│   │   │                   ├── elements/
│   │   │                   │   └── my-element/
│   │   │                   │       ├── index.js              ← Component.register()!
│   │   │                   │       ├── component/
│   │   │                   │       │   ├── index.js
│   │   │                   │       │   └── template.html.twig
│   │   │                   │       ├── config/
│   │   │                   │       │   ├── index.js
│   │   │                   │       │   └── template.html.twig
│   │   │                   │       └── preview/
│   │   │                   │           ├── index.js          ← SCSS import!
│   │   │                   │           ├── template.html.twig
│   │   │                   │           └── styles.scss       ← Farben!
│   │   │                   └── blocks/
│   │   │                       └── my-block/
│   │   │                           ├── index.js
│   │   │                           ├── component/
│   │   │                           │   └── template.html.twig
│   │   │                           └── preview/
│   │   │                               ├── index.js
│   │   │                               ├── template.html.twig
│   │   │                               └── styles.scss
│   │   └── views/
│   │       └── storefront/
│   │           ├── element/
│   │           │   └── cms-element-my-element.html.twig
│   │           └── block/                      ← WIRD OFT VERGESSEN!
│   │               └── cms-block-my-block.html.twig
```

---

*Letzte Aktualisierung: 2026-02-18*
*Based on practical plugin project experience (neutralized examples).*
