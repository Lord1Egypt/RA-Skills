# Client Implementation (Safe Mock)

Build UI against your own API endpoints that use the mock provider.

## Hook Skeleton

```ts
import { useState } from 'react';

export function useCheckout() {
  const [loading, setLoading] = useState(false);

  async function startCheckout(orderId: string) {
    setLoading(true);
    try {
      const res = await fetch('/api/checkout/mock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ orderId }),
      });
      const data = await res.json();
      window.location.href = data.redirectUrl;
    } finally {
      setLoading(false);
    }
  }

  return { startCheckout, loading };
}
```

## UI States

Render deterministic views for:
- pending
- approved
- rejected

Do not reference external provider APIs from client code.
