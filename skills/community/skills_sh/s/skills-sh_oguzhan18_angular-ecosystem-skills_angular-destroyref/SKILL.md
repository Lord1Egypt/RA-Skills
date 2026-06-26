---
name: angular-destroyref
description: "ALWAYS use when working with Angular DestroyRef, takeUntilDestroyed, or cleanup in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular DestroyRef

**Version:** Angular 16+ (2025)
**Tags:** DestroyRef, Cleanup, takeUntilDestroyed

**References:** [DestroyRef](https://angular.io/api/core/DestroyRef)

## Best Practices

- Use takeUntilDestroyed

```ts
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({})
export class MyComponent {
  private destroyRef = inject(DestroyRef);
  
  ngOnInit() {
    this.data$.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe();
  }
}
```

- Use in service

```ts
@Injectable({ providedIn: 'root' })
export class DataService {
  private destroyRef = inject(DestroyRef);
  
  getData() {
    return this.http.get('/api/data').pipe(
      takeUntilDestroyed(this.destroyRef)
    );
  }
}
```
