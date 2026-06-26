---
name: angular-animations
description: >-
  Configure Angular animations with triggers, transitions, keyframes, and reusable animation functions. Use when working with Angular enter/leave animations, UI transitions, route animations, stagger effects, animation triggers, or when the user asks to animate Angular components.
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @angular/animations

**Version:** Angular 21 (2025)
**Tags:** Animations, UI, Transitions, Motion

**References:** [Animations Guide](https://angular.dev/guide/animations) • [API](https://angular.dev/api/animations) • [npm](https://www.npmjs.com/package/@angular/animations)

## API Changes

This section documents recent version-specific API changes.

- NEW: Modern animation API — Use `animateEnter` and `animateLeave` over deprecated `:enter`/`:leave`

- NEW: CSS-based animations — Angular team recommends CSS for better performance

- NEW: View transitions API — Support for browser View Transitions API

- DEPRECATED: `:enter` and `:leave` — Use `animateEnter` and `animateLeave` instead

## Best Practices

- Enable animations module

```ts
import { provideAnimations } from '@angular/platform-browser/animations';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimations()
  ]
};
```

- Use triggers for state-based animations

```ts
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  animations: [
    trigger('fadeInOut', [
      state('hidden', style({ opacity: 0 })),
      state('visible', style({ opacity: 1 })),
      transition('hidden <=> visible', animate(500))
    ])
  ]
})
export class FadeComponent {
  isVisible = signal(false);
}
```

- Use enter/leave animations

```ts
@Component({
  animations: [
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(-100%)' }),
        animate('300ms ease-in', style({ transform: 'translateX(0%)' }))
      ]),
      transition(':leave', [
        animate('300ms ease-out', style({ transform: 'translateX(-100%)' }))
      ])
    ])
  ]
})
export class SlideComponent {}
```

- Use wildcard states for any transition

```ts
trigger('expand', [
  transition('* => expanded', [
    style({ height: '*' }),
    animate('300ms ease-out', style({ height: '200px' }))
  ]),
  transition('expanded => *', [
    animate('300ms ease-in', style({ height: '*' }))
  ])
])
```

- Use query and stagger for list animations

```ts
trigger('listAnimation', [
  transition('* => *', [
    query(':enter', [
      style({ opacity: 0 }),
      stagger(100, [
        animate('300ms', style({ opacity: 1 }))
      ])
    ], { optional: true })
  ])
])
```

- Use animation callbacks

```ts
@Component({
  template: `
    <div [@fade]="state" 
         (@fade.start)="onAnimationStart()"
         (@fade.done)="onAnimationDone()">
    </div>
  `
})
export class AnimComponent {
  onAnimationStart() { console.log('Start'); }
  onAnimationDone() { console.log('Done'); }
}
```

- Use reusable triggers

```ts
// animations.ts
export const fadeAnimation = trigger('fade', [
  transition(':enter', [
    style({ opacity: 0 }),
    animate('300ms', style({ opacity: 1 }))
  ]),
  transition(':leave', [
    animate('300ms', style({ opacity: 0 }))
  ])
]);
```

- Use functional animations (Angular 17+)

```ts
@Component({
  animations: [
    trigger('expanded', [
      transition(':expanded', [
        animate('300ms cubic-bezier(0.4, 0, 0.2, 1)')
      ])
    ])
  ]
})
export class ExpandComponent {}
```

- Optimize for performance

```ts
// Prefer transform and opacity
transition('* => *', [
  animate('200ms', style({ 
    transform: 'translateX(10px)',
    opacity: 0.5 
  }))
])

// Avoid expensive properties
// ❌ Don't animate: width, height, margin, top
// ✅ Do animate: transform, opacity
```

- Provide reduced motion for accessibility

```ts
@Component({
  animations: [
    trigger('slide', [
      transition('* => *', [
        style({ '@.disabled': '' }), // Disable for reduced motion
        animate('300ms')
      ])
    ])
  ]
})
```
