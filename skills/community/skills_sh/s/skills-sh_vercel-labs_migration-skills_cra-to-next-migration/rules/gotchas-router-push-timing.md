---
title: Never Call router.push During Render
impact: HIGH
impactDescription: Calling router.push in render body causes React errors
tags: gotchas, routing, useRouter, useEffect
---

## Never Call router.push During Render

Calling `router.push()` during the render phase causes React errors. Navigation must happen in event handlers or effects, not in the component body.

**Problem: Navigation during render**

```tsx
// BAD - Called during render phase
function MyComponent() {
  const router = useRouter();

  if (someCondition) {
    router.push('/other'); // Error: Cannot update during render
  }

  return <div>Content</div>;
}
```

Error: `Cannot update a component while rendering a different component`

**Solution: Use useEffect for conditional navigation**

```tsx
// GOOD - Navigation in useEffect
function MyComponent() {
  const router = useRouter();

  useEffect(() => {
    if (someCondition) {
      router.push('/other');
    }
  }, [someCondition, router]);

  // Show nothing or loading while redirecting
  if (someCondition) {
    return null;
  }

  return <div>Content</div>;
}
```

**Pattern for auth redirects**

```tsx
'use client';

function ProtectedPage() {
  const router = useRouter();
  const { authenticated, authenticating } = useAuth();

  useEffect(() => {
    if (!authenticating && !authenticated) {
      router.push('/login');
    }
  }, [authenticating, authenticated, router]);

  if (authenticating) {
    return <LoadingSpinner />;
  }

  if (!authenticated) {
    return null; // Will redirect via useEffect
  }

  return <div>Protected content</div>;
}
```

**Pattern for post-action redirects**

```tsx
function CreateItemPage() {
  const router = useRouter();
  const [isCreating, setIsCreating] = useState(false);

  const handleSubmit = async (data: FormData) => {
    setIsCreating(true);
    try {
      const item = await createItem(data);
      // GOOD - Navigation in event handler after async action
      router.push(`/items/${item.id}`);
    } catch (error) {
      setIsCreating(false);
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button disabled={isCreating}>Create</button>
    </form>
  );
}
```

**Server Component alternative: redirect()**

For server components, use the `redirect()` function instead:

```tsx
// app/protected/page.tsx (Server Component)
import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth';

export default async function ProtectedPage() {
  const session = await auth();

  if (!session) {
    redirect('/login'); // Works in server components
  }

  return <div>Protected content</div>;
}
```

**When to use each approach:**

| Context | Method |
|---------|--------|
| Server Component | `redirect()` from `next/navigation` |
| Client Component (event handler) | `router.push()` directly |
| Client Component (conditional) | `router.push()` in `useEffect` |
| After form submission | `router.push()` in submit handler |
| After mutation | `router.push()` in mutation callback |

**Common mistakes:**

```tsx
// BAD - In render body
function Component() {
  const router = useRouter();
  if (done) router.push('/success');
  return <div>...</div>;
}

// BAD - In useMemo (still render phase)
const result = useMemo(() => {
  if (error) router.push('/error');
  return data;
}, [data, error]);

// GOOD - In useEffect
useEffect(() => {
  if (done) router.push('/success');
}, [done, router]);
```
