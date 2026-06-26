# Database Helper - Prisma

Implementation of `src/lib/db/purchases.ts` using Prisma ORM.

## Prerequisites

- [`prisma`](https://www.npmjs.com/package/prisma) and [`@prisma/client`](https://www.npmjs.com/package/@prisma/client) installed
- PostgreSQL database (AWS RDS, Neon, Supabase, self-hosted, etc.)

## Setup

Install if not already present:

```bash
npm install prisma@^6 @prisma/client@^6
npx prisma init
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## Prisma Schema

Add to `prisma/schema.prisma`:

```prisma
model Purchase {
  id                       String         @id @default(uuid()) @db.Uuid
  user_email               String         @db.VarChar(255)
  provider_payment_id   String?
  provider_preference_id String?
  status                   String         @default("pending") @db.VarChar(20)
  total_amount             Decimal?       @db.Decimal(10, 2)
  created_at               DateTime       @default(now()) @db.Timestamptz()
  updated_at               DateTime       @default(now()) @db.Timestamptz()
  items                    PurchaseItem[]

  @@index([user_email])
  @@index([status])
  @@index([provider_payment_id])
  @@map("purchases")
}

model PurchaseItem {
  id          String   @id @default(uuid()) @db.Uuid
  purchase_id String   @db.Uuid
  item_id     String   @db.Uuid
  price       Decimal  @db.Decimal(10, 2)
  purchase    Purchase @relation(fields: [purchase_id], references: [id], onDelete: Cascade)

  @@index([purchase_id])
  @@map("purchase_items")
}
```

Then run:

```bash
npx prisma migrate dev --name add_purchases
```

**Note:** If using `assets/migration.sql` directly instead of Prisma migrations, run `npx prisma db pull` to sync the schema from the existing database.

## Prisma Client Singleton

```typescript
// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

## Implementation

```typescript
// src/lib/db/purchases.ts
import { prisma } from '@/lib/prisma';

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
  const purchase = await prisma.purchase.create({
    data: {
      user_email: data.user_email,
      status: data.status,
      total_amount: data.total_amount,
    },
    select: { id: true },
  });
  return purchase;
}

export async function updatePurchase(id: string, data: PurchaseUpdate) {
  await prisma.purchase.update({
    where: { id },
    data: {
      ...data,
      updated_at: data.updated_at ? new Date(data.updated_at) : new Date(),
    },
  });
}

export async function getPurchaseStatus(id: string) {
  const purchase = await prisma.purchase.findUnique({
    where: { id },
    select: { id: true, status: true, total_amount: true },
  });
  return purchase;
}

export async function updatePurchaseStatusAtomically(
  id: string,
  expectedStatus: string,
  data: PurchaseUpdate
): Promise<boolean> {
  const result = await prisma.purchase.updateMany({
    where: { id, status: expectedStatus },
    data: {
      ...data,
      updated_at: data.updated_at ? new Date(data.updated_at) : new Date(),
    },
  });
  return result.count > 0;
}

export async function createPurchaseItems(
  purchaseId: string,
  items: { item_id: string; price: number }[]
) {
  await prisma.purchaseItem.createMany({
    data: items.map((item) => ({
      purchase_id: purchaseId,
      item_id: item.item_id,
      price: item.price,
    })),
  });
}
```

