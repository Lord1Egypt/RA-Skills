# Optimal React + Vite Project Structure Example

This is a complete, production-ready project structure example.

## Directory Tree

```
my-react-app/
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions CI/CD
│
├── .husky/
│   ├── pre-commit                   # Lint staged files
│   └── pre-push                     # Run tests before push
│
├── public/
│   ├── favicon.ico
│   └── robots.txt
│
├── src/
│   ├── app/
│   │   ├── App.tsx                  # Root component
│   │   ├── App.test.tsx
│   │   ├── router.tsx               # Route configuration
│   │   └── providers.tsx            # Context providers wrapper
│   │
│   ├── features/                    # Feature modules
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── LoginForm/
│   │   │   │   │   ├── LoginForm.tsx
│   │   │   │   │   ├── LoginForm.types.ts
│   │   │   │   │   ├── LoginForm.module.css
│   │   │   │   │   ├── LoginForm.test.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   └── RegisterForm/
│   │   │   ├── hooks/
│   │   │   │   ├── useAuth.ts
│   │   │   │   └── useLogin.ts
│   │   │   ├── api/
│   │   │   │   ├── authApi.ts
│   │   │   │   └── authApi.types.ts
│   │   │   └── index.ts
│   │   │
│   │   └── dashboard/
│   │       ├── components/
│   │       ├── hooks/
│   │       └── index.ts
│   │
│   ├── components/                  # Shared components
│   │   ├── ui/
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   └── index.ts
│   │   ├── layout/
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   └── index.ts
│   │   └── form/
│   │       └── FormField/
│   │
│   ├── hooks/                       # Shared custom hooks
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   ├── useMediaQuery.ts
│   │   └── index.ts
│   │
│   ├── lib/                         # Third-party setup
│   │   ├── queryClient.ts           # React Query setup
│   │   ├── axios.ts                 # Axios instance
│   │   └── i18n.ts                  # i18n configuration
│   │
│   ├── pages/                       # Page components
│   │   ├── HomePage/
│   │   │   ├── HomePage.tsx
│   │   │   ├── HomePage.lazy.tsx
│   │   │   └── index.ts
│   │   ├── DashboardPage/
│   │   └── NotFoundPage/
│   │
│   ├── services/                    # Business logic
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── endpoints.ts
│   │   │   └── types.ts
│   │   └── auth/
│   │       ├── authService.ts
│   │       └── tokenService.ts
│   │
│   ├── store/                       # Global state
│   │   ├── slices/
│   │   │   ├── userSlice.ts
│   │   │   └── uiSlice.ts
│   │   └── index.ts
│   │
│   ├── types/                       # Shared types
│   │   ├── api.types.ts
│   │   ├── user.types.ts
│   │   └── index.ts
│   │
│   ├── utils/                       # Utilities
│   │   ├── formatters/
│   │   │   ├── dateFormatter.ts
│   │   │   └── currencyFormatter.ts
│   │   ├── validators/
│   │   │   └── emailValidator.ts
│   │   ├── constants/
│   │   │   ├── routes.ts
│   │   │   └── config.ts
│   │   └── index.ts
│   │
│   ├── assets/                      # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   ├── fonts/
│   │   └── styles/
│   │       ├── globals.css
│   │       ├── variables.css
│   │       └── reset.css
│   │
│   ├── test/                        # Test utilities
│   │   ├── setup.ts
│   │   ├── utils.tsx
│   │   └── mocks/
│   │       ├── handlers.ts
│   │       └── data.ts
│   │
│   ├── main.tsx                     # Entry point
│   └── vite-env.d.ts               # Vite types
│
├── .env.development                 # Dev environment variables
├── .env.production                  # Prod environment variables
├── .eslintrc.cjs                    # ESLint config
├── .gitignore
├── .prettierrc                      # Prettier config
├── index.html                       # HTML template
├── package.json
├── tsconfig.json                    # TypeScript config
├── tsconfig.node.json              # TS config for build tools
├── vite.config.ts                  # Vite config
├── vitest.config.ts                # Vitest config
└── README.md
```

## Key Files Content

### src/main.tsx
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './app/App';
import './assets/styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### src/app/App.tsx
```typescript
import { Providers } from './providers';
import { Router } from './router';

export function App() {
  return (
    <Providers>
      <Router />
    </Providers>
  );
}
```

### src/app/providers.tsx
```typescript
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/queryClient';
import { BrowserRouter } from 'react-router-dom';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
}
```

### src/app/router.tsx
```typescript
import { Routes, Route } from 'react-router-dom';
import { Suspense } from 'react';
import { HomePageLazy } from '@/pages/HomePage';
import { DashboardPageLazy } from '@/pages/DashboardPage';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export function Router() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<HomePageLazy />} />
        <Route path="/dashboard" element={<DashboardPageLazy />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}
```

### src/lib/queryClient.ts
```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000,   // 10 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

### src/lib/axios.ts
```typescript
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### src/utils/constants/routes.ts
```typescript
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  LOGIN: '/login',
  PROFILE: '/profile',
  SETTINGS: '/settings',
} as const;
```

### src/types/api.types.ts
```typescript
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  page: number;
  pageSize: number;
  total: number;
}

export interface ApiError {
  message: string;
  code: string;
  details?: unknown;
}
```

### src/test/setup.ts
```typescript
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});
```

### src/test/utils.tsx
```typescript
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

interface AllProvidersProps {
  children: React.ReactNode;
}

function AllProviders({ children }: AllProvidersProps) {
  const testQueryClient = createTestQueryClient();

  return (
    <QueryClientProvider client={testQueryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
}

function customRender(ui: React.ReactElement, options?: RenderOptions) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { customRender as render };
```

### vitest.config.ts
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'clover', 'json'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        '**/*.stories.tsx',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### .eslintrc.cjs
```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': [
      'error',
      { argsIgnorePattern: '^_' },
    ],
  },
};
```

### .prettierrc
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
```

## Creating This Structure

Use the provided scripts to generate this structure:

```bash
# Create a component
python scripts/create_component.py Button --type component

# Create a page with lazy loading
python scripts/create_component.py HomePage --type page

# Create a custom hook
python scripts/create_hook.py useAuth --type custom

# Create a feature module
mkdir -p src/features/auth/{components,hooks,api,store}
```

## Best Practices Applied

1. ✅ Feature-based organization
2. ✅ Colocation of related files
3. ✅ Path aliases for clean imports
4. ✅ Lazy loading for routes
5. ✅ Centralized configuration
6. ✅ Type-safe everything
7. ✅ Test utilities and setup
8. ✅ Consistent naming conventions
9. ✅ Separation of concerns
10. ✅ Barrel exports (index.ts)

## Scaling Guidelines

### Small App (< 10 components)
- Flat structure in `src/components`
- Single `hooks` folder
- Minimal organization

### Medium App (10-50 components)
- Use feature folders
- Separate pages
- Shared components folder
- Custom hooks folder

### Large App (50+ components)
- Full feature-based architecture
- Domain-driven design
- Microservice-ready structure
- Consider monorepo (nx, turborepo)

## Migration Path

If you have an existing project:

1. Add path aliases to vite.config.ts and tsconfig.json
2. Create `features/` folder
3. Move related components into features
4. Extract shared components to `components/`
5. Extract hooks to `hooks/`
6. Create `lib/` for third-party setup
7. Move pages to `pages/`
8. Update imports gradually
