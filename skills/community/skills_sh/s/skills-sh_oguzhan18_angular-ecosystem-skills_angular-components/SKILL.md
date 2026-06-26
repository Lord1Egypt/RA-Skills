---
name: angular-components
description: "ALWAYS use when working with Angular Components, component architecture, @Component decorator, inputs, outputs, or component design patterns."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Components

**Version:** Angular 21 (2025)
**Tags:** Components, @Component, Architecture

**References:** [Components Guide](https://angular.dev/guide/components) • [@Component API](https://angular.io/api/core/Component)

## Best Practices

- Create standalone component

```ts
@Component({
  standalone: true,
  selector: 'app-my',
  imports: [CommonModule],
  template: `<p>Content</p>`
})
export class MyComponent {}
```

- Use inputs with signals

```ts
@Component({})
export class MyComponent {
  data = input<string>('');
  required = input.required<User>();
  
  computed = computed(() => this.data()?.name);
}
```

- Use outputs for events

```ts
@Component({})
export class MyComponent {
  data = output<string>();
  
  onClick() {
    this.data.emit('event');
  }
}
```

- Use template reference variables

```ts
@Component({
  template: `
    <input #nameInput>
    <button (click)="onSubmit(nameInput.value)">Submit</button>
  `
})
export class MyComponent {}
```

- Use content projection

```ts
@Component({
  selector: 'app-card',
  template: `
    <div class="header">
      <ng-content select="[header]"></ng-content>
    </div>
    <div class="body">
      <ng-content></ng-content>
    </div>
  `
})
export class CardComponent {}
```

- Use change detection strategy

```ts
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OptimizedComponent {}
```

- Use encapsulation

```ts
@Component({
  encapsulation: ViewEncapsulation.None // or Emulated, ShadowDom
})
export class StyledComponent {}
```

- Use host binding

```ts
@Component({
  host: {
    '[class.active]': 'isActive',
    '(click)': 'onClick()'
  }
})
export class HostComponent {
  isActive = false;
}
```
