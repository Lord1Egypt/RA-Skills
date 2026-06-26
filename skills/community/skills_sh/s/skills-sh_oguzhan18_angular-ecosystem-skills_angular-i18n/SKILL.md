---
name: angular-i18n
description: "ALWAYS use when working with Angular i18n, internationalization, localization, translations, or multi-language support in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular i18n

**Version:** Angular 21 (2025)
**Tags:** i18n, Internationalization, Localization, Translations

**References:** [i18n Guide](https://angular.dev/guide/i18n) • [Angular Localize](https://angular.dev/guide/localize)

## API Changes

This section documents recent version-specific API changes.

- NEW: @angular/localize — Built-in i18n support

- NEW: $localize — Message extraction

- NEW: Angular CLI i18n — Multiple language builds

- NEW: Lazy-loaded translations — Runtime translation loading

## Best Practices

- Mark text for translation

```ts
@Component({
  template: `
    <h1 i18n="@@welcome">Welcome to our app!</h1>
    <p i18n="@@greeting">Hello, world!</p>
  `
})
export class HomeComponent {}
```

- Use translations with placeholders

```ts
@Component({
  template: `
    <p i18n="@@userCount">
      There are { count, plural, =0 { no users } =1 { one user } other { {{ count }} users } } in the system.
    </p>
  `
})
export class UsersComponent {
  count = 5;
}
```

- Use gender-specific translations

```ts
@Component({
  template: `
    <p i18n="@@message">
      { gender, select, male {He} female {She} other {They} } is attending.
    </p>
  `
})
export class MessageComponent {}
```

- Extract messages

```bash
ng extract-i18n --output-path src/locale
```

- Build for multiple locales

```bash
ng build --localize
```

- Configure locales in angular.json

```json
{
  "projects": {
    "my-app": {
      "i18n": {
        "locales": {
          "en": "src/locale/messages.en.xlf",
          "es": "src/locale/messages.es.xlf",
          "fr": "src/locale/messages.fr.xlf"
        }
      }
    }
  }
}
```

- Use i18n attribute for elements

```ts
@Component({
  template: `
    <img i18n-title title="Logo" src="logo.png" />
    <a i18n-href href="/about" hreflang="es">About</a>
  `
})
export class HeaderComponent {}
```

- Use @angular/localize for runtime translations

```ts
import { $localize } from '@angular/localize';

$localize`:@@greeting:Hello, ${name}:name:World!`;
```

- Use ngx-translate for runtime translations

```ts
// Alternative: use @ngx-translate/core
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
  imports: [TranslateModule.forRoot()]
})
export class AppModule {}
```

- Lazy load translations

```ts
// Using @ngx-translate
this.translate.getTranslation('en').subscribe(translations => {
  // Load translations
});
```
