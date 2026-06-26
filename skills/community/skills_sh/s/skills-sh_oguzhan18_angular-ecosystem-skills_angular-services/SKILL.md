---
name: angular-services
description: "ALWAYS use when working with Angular Services, @Injectable, dependency injection, or business logic services."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Services

**Version:** Angular 21 (2025)
**Tags:** Services, @Injectable, DI

**References:** [Services Guide](https://angular.dev/guide/services) • [@Injectable API](https://angular.io/api/core/Injectable)

## Best Practices

- Create service with providedIn

```ts
@Injectable({ providedIn: 'root' })
export class DataService {
  getData() {
    return this.http.get('/api/data');
  }
}
```

- Use inject() function

```ts
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);
  
  getUsers() {
    return this.http.get<User[]>('/api/users');
  }
}
```

- Use factory providers

```ts
@Injectable({
  providedIn: 'root',
  useFactory: () => new LoggerService(environment.production)
})
export class LoggerService {
  constructor(private isProduction: boolean) {}
}
```

- Use providedIn: 'any' for lazy services

```ts
@Injectable({ providedIn: 'any' })
export class LazyService {}
```

- Use service in component

```ts
@Component({})
export class MyComponent {
  private dataService = inject(DataService);
  
  data$ = this.dataService.getData();
}
```

- Use multiple services

```ts
@Component({})
export class MyComponent {
  private auth = inject(AuthService);
  private http = inject(HttpClient);
  private router = inject(Router);
}
```

- Use service for shared state

```ts
@Injectable({ providedIn: 'root' })
export class CartService {
  private items = signal<Item[]>([]);
  
  cartItems = this.items.asReadonly();
  
  addItem(item: Item) {
    this.items.update(items => [...items, item]);
  }
}
```
