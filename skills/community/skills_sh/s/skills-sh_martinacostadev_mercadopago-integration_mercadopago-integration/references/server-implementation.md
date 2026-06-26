# Server Implementation (Safe Mock)

Use a provider-agnostic contract and a mock adapter only.

## Contract

```ts
export type CheckoutStatus = 'pending' | 'approved' | 'rejected';

export interface CheckoutSession {
  sessionId: string;
  redirectUrl: string;
  expiresAt: string;
}

export interface CheckoutProvider {
  createSession(input: { orderId: string; amount: number; currency: string }): Promise<CheckoutSession>;
  getStatus(input: { sessionId: string }): Promise<{ status: CheckoutStatus }>;
}
```

## Mock Adapter

```ts
export class MockCheckoutProvider implements CheckoutProvider {
  async createSession(input: { orderId: string; amount: number; currency: string }) {
    const sessionId = `mock_${input.orderId}`;
    return {
      sessionId,
      redirectUrl: `/checkout/mock/${sessionId}`,
      expiresAt: new Date(Date.now() + 15 * 60 * 1000).toISOString(),
    };
  }

  async getStatus(input: { sessionId: string }) {
    const tail = input.sessionId.slice(-1);
    const status: CheckoutStatus = tail === '0' ? 'rejected' : tail === '1' ? 'pending' : 'approved';
    return { status };
  }
}
```

## Security Handoff (for future live integration)

- Secrets management
- Signature verification
- Idempotency and replay controls
- Monetary amount validation
- Audit logging
```
