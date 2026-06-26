# Database Helper - Supabase

Implementation of `src/lib/db/purchases.ts` using Supabase client.

## Prerequisites

- `@supabase/supabase-js` installed
- A server-side Supabase client (e.g., `createServiceClient` from `src/lib/supabase/server.ts`)
- Run `assets/migration.sql` in Supabase SQL Editor

## Environment Variables

```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...   # Never expose to frontend
```

## Implementation

```typescript
// src/lib/db/purchases.ts
import { createServiceClient } from '@/lib/supabase/server';

interface PurchaseInsert {
  user_email: string;
  status: 'pending';
  total_amount: number;
}

interface PurchaseUpdate {
  status?: 'pending' | 'approved' | 'rejected';
  provider_payment_id?: string;
  provider_preference_id?: string;
  user_email?: string;
  updated_at?: string;
}

export async function createPurchase(data: PurchaseInsert) {
  const supabase = await createServiceClient();
  const { data: purchase, error } = await supabase
    .from('purchases')
    .insert(data)
    .select('id')
    .single();

  if (error || !purchase) {
    console.error('Error creating purchase:', error);
    throw new Error('Failed to create purchase');
  }
  return purchase;
}

export async function updatePurchase(id: string, data: PurchaseUpdate) {
  const supabase = await createServiceClient();
  const { error } = await supabase
    .from('purchases')
    .update(data)
    .eq('id', id);

  if (error) {
    console.error('Error updating purchase:', error);
    throw new Error('Failed to update purchase');
  }
}

export async function getPurchaseStatus(id: string) {
  const supabase = await createServiceClient();
  const { data, error } = await supabase
    .from('purchases')
    .select('id, status, total_amount')
    .eq('id', id)
    .single();

  if (error || !data) return null;
  return data;
}

export async function updatePurchaseStatusAtomically(
  id: string,
  expectedStatus: string,
  data: PurchaseUpdate
): Promise<boolean> {
  const supabase = await createServiceClient();
  const { data: updated, error } = await supabase
    .from('purchases')
    .update(data)
    .eq('id', id)
    .eq('status', expectedStatus)
    .select('id');

  if (error) {
    console.error('Error updating purchase atomically:', error);
    throw new Error('Failed to update purchase atomically');
  }
  return (updated?.length ?? 0) > 0;
}

export async function createPurchaseItems(
  purchaseId: string,
  items: { item_id: string; price: number }[]
) {
  const supabase = await createServiceClient();
  const { error } = await supabase
    .from('purchase_items')
    .insert(items.map((item) => ({ purchase_id: purchaseId, ...item })));

  if (error) {
    console.error('Error creating purchase items:', error);
    throw new Error('Failed to create purchase items');
  }
}
```

## Supabase Server Client Example

If the project doesn't have a server-side Supabase client yet:

```typescript
// src/lib/supabase/server.ts
import { createClient } from '@supabase/supabase-js';

export async function createServiceClient() {
  return createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );
}
```

## Optional: Row Level Security (RLS)

Enable RLS if using Supabase Auth. Add to migration:

```sql
ALTER TABLE public.purchases ENABLE ROW LEVEL SECURITY;

-- Users can view own purchases
CREATE POLICY "Users can view own purchases"
  ON public.purchases FOR SELECT
  USING (user_email = auth.jwt() ->> 'email');

-- Service role bypasses RLS (used by API routes)
-- No additional policy needed when using createServiceClient with service_role key
```

