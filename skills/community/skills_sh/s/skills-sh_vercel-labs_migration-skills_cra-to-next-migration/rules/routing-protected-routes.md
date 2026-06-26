---
title: Implement Protected Routes
impact: MEDIUM
impactDescription: Route protection patterns differ between CRA and Next.js
tags: routing, auth, protected, middleware, layout
---

## Implement Protected Routes

Next.js offers multiple patterns for route protection. Choose based on whether you need client-side or server-side protection.

**Pattern 1: Layout-level protection (Client Component)**

Best for client-side auth (Auth0, Clerk client SDK, custom JWT):

```tsx
// app/(protected)/layout.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { authenticated, authenticating } = useAuth();

  useEffect(() => {
    if (!authenticating && !authenticated) {
      router.push('/login');
    }
  }, [authenticating, authenticated, router]);

  if (authenticating) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  if (!authenticated) {
    return null; // Will redirect via useEffect
  }

  return <>{children}</>;
}
```

**Pattern 2: Page-level protection (Server Component)**

Best for server-side auth (NextAuth, Clerk server SDK):

```tsx
// app/(protected)/admin/page.tsx
import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth'; // Your server-side auth

export default async function AdminPage() {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  if (session.user.role !== 'admin') {
    redirect('/');
  }

  return <AdminDashboard user={session.user} />;
}
```

**Pattern 3: Middleware protection**

Best for protecting multiple routes with the same rules:

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value;

  // Protect all /dashboard routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // Redirect logged-in users away from auth pages
  if (request.nextUrl.pathname.startsWith('/login')) {
    if (token) {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
};
```

**Pattern 4: Role-based protection**

```tsx
// app/(protected)/layout.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';

interface ProtectedLayoutProps {
  children: React.ReactNode;
  requiredRole?: string;
}

export default function ProtectedLayout({
  children,
  requiredRole,
}: ProtectedLayoutProps) {
  const router = useRouter();
  const { user, authenticated, authenticating } = useAuth();

  useEffect(() => {
    if (authenticating) return;

    if (!authenticated) {
      router.push('/login');
      return;
    }

    if (requiredRole && user?.role !== requiredRole) {
      router.push('/unauthorized');
    }
  }, [authenticating, authenticated, user?.role, requiredRole, router]);

  if (authenticating) return <LoadingSpinner />;
  if (!authenticated) return null;
  if (requiredRole && user?.role !== requiredRole) return null;

  return <>{children}</>;
}
```

**Folder structure for protected routes:**

```
app/
├── (public)/              # No auth required
│   ├── page.tsx           # Home page
│   ├── about/
│   └── pricing/
├── (auth)/                # Auth pages (redirect if logged in)
│   ├── login/
│   └── register/
├── (protected)/           # Requires authentication
│   ├── layout.tsx         # Auth check layout
│   ├── dashboard/
│   └── settings/
└── (admin)/               # Requires admin role
    ├── layout.tsx         # Admin check layout
    └── users/
```

**Migrating from React Router:**

```tsx
// CRA with React Router
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>

// Next.js App Router
// app/(protected)/dashboard/page.tsx
// Protection handled by (protected)/layout.tsx
export default function DashboardPage() {
  return <Dashboard />;
}
```

**When to use each pattern:**

| Pattern | Use Case |
|---------|----------|
| Layout (client) | Client-side auth, SPA-like behavior |
| Page (server) | Server-side auth, SEO pages |
| Middleware | Simple token checks, redirects |
| Combined | Complex auth with role hierarchy |
