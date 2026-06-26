# React Performance Optimization Guide

Comprehensive guide to optimizing React + Vite applications for maximum performance.

## Performance Metrics to Track

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: < 2.5s (Good)
- **FID (First Input Delay)**: < 100ms (Good)
- **CLS (Cumulative Layout Shift)**: < 0.1 (Good)
- **FCP (First Contentful Paint)**: < 1.8s (Good)
- **TTI (Time to Interactive)**: < 3.8s (Good)

### Bundle Size Goals
- **Initial JS bundle**: < 200KB (gzipped)
- **Total JS**: < 500KB (gzipped)
- **CSS**: < 50KB (gzipped)
- **Images**: Use WebP/AVIF, lazy load

## React Rendering Optimization

### 1. React.memo() - Prevent Unnecessary Re-renders

```typescript
// ❌ Bad: Re-renders on every parent render
export const ExpensiveComponent = ({ data }) => {
  return <div>{/* Complex rendering */}</div>;
};

// ✅ Good: Only re-renders when props change
export const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* Complex rendering */}</div>;
});

// ✅ Best: Custom comparison for complex props
export const ExpensiveComponent = React.memo(
  ({ data }) => {
    return <div>{/* Complex rendering */}</div>;
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (don't re-render)
    return prevProps.data.id === nextProps.data.id;
  }
);
```

**When to use React.memo():**
- ✅ Pure components that render often
- ✅ Components with expensive rendering
- ✅ Components that receive same props frequently
- ❌ Simple components (overhead > benefit)
- ❌ Components that rarely re-render

### 2. useMemo() - Memoize Expensive Calculations

```typescript
// ❌ Bad: Recalculates on every render
function ProductList({ products }) {
  const sortedProducts = products.sort((a, b) => b.price - a.price);
  const filteredProducts = sortedProducts.filter(p => p.inStock);

  return <div>{/* Render filtered products */}</div>;
}

// ✅ Good: Only recalculates when products change
function ProductList({ products }) {
  const processedProducts = useMemo(() => {
    const sorted = [...products].sort((a, b) => b.price - a.price);
    return sorted.filter(p => p.inStock);
  }, [products]);

  return <div>{/* Render processed products */}</div>;
}
```

**When to use useMemo():**
- ✅ Expensive calculations (sorting, filtering large arrays)
- ✅ Creating objects/arrays passed as props to memoized components
- ✅ Complex transformations
- ❌ Simple calculations (overhead > benefit)

### 3. useCallback() - Memoize Functions

```typescript
// ❌ Bad: Creates new function on every render (breaks memo)
function Parent() {
  const handleClick = (id) => {
    console.log(id);
  };

  return <MemoizedChild onClick={handleClick} />;
}

// ✅ Good: Function identity stays same
function Parent() {
  const handleClick = useCallback((id) => {
    console.log(id);
  }, []); // Empty deps: function never changes

  return <MemoizedChild onClick={handleClick} />;
}

// ✅ With dependencies
function Parent() {
  const [userId, setUserId] = useState('123');

  const handleClick = useCallback((id) => {
    console.log(userId, id);
  }, [userId]); // Re-creates when userId changes

  return <MemoizedChild onClick={handleClick} />;
}
```

**When to use useCallback():**
- ✅ Passing callbacks to memoized child components
- ✅ Callbacks in dependency arrays of other hooks
- ✅ Event handlers passed to many children
- ❌ Simple event handlers not affecting memoization

### 4. Code Splitting with React.lazy()

```typescript
// ❌ Bad: Loads everything upfront
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Settings from './pages/Settings';

// ✅ Good: Loads on-demand
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));

// Usage with Suspense
function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

**Route-based code splitting pattern:**
```typescript
// pages/DashboardPage/DashboardPage.lazy.tsx
import { lazy } from 'react';

export const DashboardPageLazy = lazy(() =>
  import('./DashboardPage').then(module => ({
    default: module.DashboardPage
  }))
);
```

### 5. Virtualization for Long Lists

```typescript
// ❌ Bad: Renders 10,000 items (performance killer)
function ProductList({ products }) {
  return (
    <div>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// ✅ Good: Only renders visible items
import { FixedSizeList } from 'react-window';

function ProductList({ products }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={products.length}
      itemSize={100}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <ProductCard product={products[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}
```

**Libraries:**
- **react-window**: Lighter, most use cases
- **react-virtualized**: More features, heavier

### 6. Debouncing & Throttling

```typescript
// Custom debounce hook
function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage in search
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 300);

  useEffect(() => {
    if (debouncedSearchTerm) {
      // API call only after 300ms of no typing
      fetchSearchResults(debouncedSearchTerm);
    }
  }, [debouncedSearchTerm]);

  return (
    <input
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
    />
  );
}
```

### 7. Avoid Inline Objects & Functions

```typescript
// ❌ Bad: Creates new object/function every render
function Component() {
  return (
    <>
      <Child style={{ padding: 10 }} />
      <Child onClick={() => console.log('click')} />
    </>
  );
}

// ✅ Good: Define outside or use constants
const CHILD_STYLE = { padding: 10 };

function Component() {
  const handleClick = () => console.log('click');

  return (
    <>
      <Child style={CHILD_STYLE} />
      <Child onClick={handleClick} />
    </>
  );
}
```

## Vite Build Optimization

### vite.config.ts - Production Optimization

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    // Bundle analyzer
    visualizer({
      filename: './dist/stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
  ],

  build: {
    // Target modern browsers
    target: 'esnext',

    // Chunk size warnings
    chunkSizeWarningLimit: 500,

    // Minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
        drop_debugger: true,
      },
    },

    // Rollup options
    rollupOptions: {
      output: {
        // Manual chunks for better caching
        manualChunks: {
          // Vendor chunk for large libraries
          vendor: ['react', 'react-dom', 'react-router-dom'],
          // UI components chunk
          ui: ['@/components/ui'],
        },

        // Asset file naming
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          let extType = info[info.length - 1];
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            extType = 'images';
          } else if (/woff|woff2|ttf|otf|eot/i.test(extType)) {
            extType = 'fonts';
          }
          return `assets/${extType}/[name]-[hash][extname]`;
        },
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
      },
    },

    // Source maps for production debugging (optional)
    sourcemap: false,

    // CSS code splitting
    cssCodeSplit: true,
  },

  // Optimize deps
  optimizeDeps: {
    include: ['react', 'react-dom'],
  },
});
```

### Manual Chunk Splitting Strategy

```typescript
// Separate chunks by route
manualChunks: (id) => {
  // Vendor chunk
  if (id.includes('node_modules')) {
    if (id.includes('react') || id.includes('react-dom')) {
      return 'react-vendor';
    }
    if (id.includes('@tanstack/react-query')) {
      return 'query-vendor';
    }
    return 'vendor';
  }

  // Feature-based chunks
  if (id.includes('/src/features/auth')) {
    return 'auth';
  }
  if (id.includes('/src/features/dashboard')) {
    return 'dashboard';
  }
}
```

## Image Optimization

### 1. Modern Formats (WebP/AVIF)

```typescript
// Use picture element for format fallback
<picture>
  <source srcSet="image.avif" type="image/avif" />
  <source srcSet="image.webp" type="image/webp" />
  <img src="image.jpg" alt="Description" loading="lazy" />
</picture>
```

### 2. Lazy Loading

```typescript
// Native lazy loading
<img src="image.jpg" loading="lazy" alt="Description" />

// Intersection Observer for custom lazy loading
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setImageSrc(src);
        observer.disconnect();
      }
    });

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return (
    <img
      ref={imgRef}
      src={imageSrc || undefined}
      alt={alt}
      style={{ minHeight: '200px' }} // Prevent layout shift
    />
  );
}
```

### 3. Responsive Images

```typescript
<img
  src="image-800w.jpg"
  srcSet="
    image-400w.jpg 400w,
    image-800w.jpg 800w,
    image-1200w.jpg 1200w
  "
  sizes="
    (max-width: 600px) 400px,
    (max-width: 1200px) 800px,
    1200px
  "
  alt="Description"
  loading="lazy"
/>
```

## Network Performance

### 1. API Request Optimization

```typescript
// ❌ Bad: Multiple sequential requests
async function loadUserData(userId: string) {
  const user = await fetchUser(userId);
  const posts = await fetchPosts(userId);
  const comments = await fetchComments(userId);
  return { user, posts, comments };
}

// ✅ Good: Parallel requests
async function loadUserData(userId: string) {
  const [user, posts, comments] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchComments(userId),
  ]);
  return { user, posts, comments };
}

// ✅ Best: Use React Query for automatic optimization
function useUserData(userId: string) {
  const user = useQuery(['user', userId], () => fetchUser(userId));
  const posts = useQuery(['posts', userId], () => fetchPosts(userId));
  const comments = useQuery(['comments', userId], () => fetchComments(userId));

  return { user, posts, comments };
}
```

### 2. Request Deduplication

```typescript
// React Query automatically deduplicates identical requests
function Component1() {
  const { data } = useQuery(['user', '123'], fetchUser);
  // ...
}

function Component2() {
  const { data } = useQuery(['user', '123'], fetchUser);
  // Only one actual API call made!
}
```

### 3. Prefetching

```typescript
import { queryClient } from '@/lib/queryClient';

function ProductList() {
  const handleMouseEnter = (productId: string) => {
    // Prefetch product details before user clicks
    queryClient.prefetchQuery(['product', productId], () =>
      fetchProduct(productId)
    );
  };

  return (
    <div>
      {products.map(product => (
        <div
          key={product.id}
          onMouseEnter={() => handleMouseEnter(product.id)}
        >
          {product.name}
        </div>
      ))}
    </div>
  );
}
```

## CSS Performance

### 1. CSS Modules (Recommended)

```typescript
// Button.module.css
.button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
}

.primary {
  background: blue;
  color: white;
}

// Button.tsx
import styles from './Button.module.css';

export const Button = ({ variant = 'primary', children }) => (
  <button className={`${styles.button} ${styles[variant]}`}>
    {children}
  </button>
);
```

**Benefits:**
- ✅ Scoped styles (no conflicts)
- ✅ Tree-shakeable
- ✅ Better for code splitting
- ✅ Smaller bundles

### 2. Avoid Runtime CSS-in-JS

```typescript
// ❌ Slow: Runtime CSS-in-JS (styled-components, emotion)
const Button = styled.button`
  padding: 10px 20px;
  background: ${props => props.primary ? 'blue' : 'gray'};
`;

// ✅ Fast: CSS Modules or Vanilla Extract (zero-runtime)
import styles from './Button.module.css';

export const Button = ({ primary, children }) => (
  <button className={primary ? styles.primary : styles.secondary}>
    {children}
  </button>
);
```

### 3. Critical CSS Inlining

```typescript
// vite.config.ts - Inline critical CSS
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    cssCodeSplit: true,
    assetsInlineLimit: 4096, // Inline assets < 4KB
  },
});
```

## State Management Performance

### Zustand with Selectors (Prevent Re-renders)

```typescript
// ❌ Bad: Component re-renders on ANY store change
function Component() {
  const store = useStore(); // Gets entire store
  return <div>{store.user.name}</div>;
}

// ✅ Good: Only re-renders when user.name changes
function Component() {
  const userName = useStore(state => state.user.name); // Selector
  return <div>{userName}</div>;
}

// ✅ Best: Shallow equality for objects
function Component() {
  const user = useStore(
    state => ({ name: state.user.name, email: state.user.email }),
    shallow // Only re-render if object values change
  );
  return <div>{user.name} - {user.email}</div>;
}
```

### Redux with Reselect (Memoized Selectors)

```typescript
import { createSelector } from 'reselect';

// Input selectors
const selectProducts = (state) => state.products;
const selectFilter = (state) => state.filter;

// Memoized selector (only recalculates when inputs change)
const selectFilteredProducts = createSelector(
  [selectProducts, selectFilter],
  (products, filter) => {
    return products.filter(p => p.category === filter);
  }
);

// Usage
const filteredProducts = useSelector(selectFilteredProducts);
```

## Performance Monitoring

### Web Vitals Tracking

```typescript
// src/lib/webVitals.ts
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals';

function sendToAnalytics({ name, delta, value, id }) {
  // Send to your analytics service
  console.log(name, delta, value, id);
}

export function reportWebVitals() {
  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onFCP(sendToAnalytics);
  onLCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}

// main.tsx
import { reportWebVitals } from './lib/webVitals';

reportWebVitals();
```

### React DevTools Profiler

```typescript
import { Profiler } from 'react';

function onRenderCallback(
  id, // Component ID
  phase, // "mount" or "update"
  actualDuration, // Time spent rendering
  baseDuration, // Estimated time without memoization
  startTime,
  commitTime
) {
  console.log({ id, phase, actualDuration, baseDuration });
}

// Wrap component to profile
<Profiler id="Dashboard" onRender={onRenderCallback}>
  <Dashboard />
</Profiler>
```

## Performance Checklist

### Development
- [ ] Use React DevTools Profiler to identify slow components
- [ ] Check for unnecessary re-renders
- [ ] Verify memoization is working
- [ ] Monitor bundle size during development

### Before Production
- [ ] Run bundle analyzer (`npm run build` with visualizer)
- [ ] Check bundle sizes < targets
- [ ] Verify code splitting is working
- [ ] Test on slow 3G connection
- [ ] Test on low-end devices
- [ ] Run Lighthouse audit (score > 90)
- [ ] Measure Core Web Vitals
- [ ] Enable compression (gzip/brotli)
- [ ] Configure CDN for assets
- [ ] Remove console.log statements
- [ ] Enable minification

### Production Monitoring
- [ ] Track Web Vitals in production
- [ ] Monitor bundle sizes on each deployment
- [ ] Set up performance budgets
- [ ] Create alerts for regressions
