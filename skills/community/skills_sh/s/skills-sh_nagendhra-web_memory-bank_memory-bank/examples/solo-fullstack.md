# Project Memory
Last updated: 2025-04-08 | Session 7 | Branch: feature/checkout
Health: 8/10

## Project Overview
Bakery e-commerce (Sweet Crumb). Next.js 14 App Router, Prisma, PostgreSQL, Stripe, Tailwind. Vercel + Neon. Launch: end April.

## Where We Left Off
- **Task:** Stripe webhook handler `src/app/api/webhooks/stripe/route.ts`
- **Status:** WIP. `handlePaymentSuccess()` DONE, `handleRefund()` stubbed at line 89
- **Next:** Implement `handleRefund()` using `refund.created` event, then integration tests
- **Open:** Use Stripe CLI for local webhook testing or mock events?

## Blockers
- Need Stripe webhook signing secret from client for staging

## Key Decisions
| Decision | Why | Affects |
|----------|-----|---------|
| App Router over Pages | Server components, future-proof | All pages |
| Prisma over Drizzle | TS inference, migrations | All DB |
| Stripe over Paddle | Client has Stripe account | Payments |
| Zustand for cart | Simple API, localStorage built-in | Cart state |
| Resend for email | React Email support, simple pricing | Transactional email |

## Key Files
| File | Purpose |
|------|---------|
| `src/app/api/webhooks/stripe/route.ts` | Webhook handler |
| `src/app/api/checkout/route.ts` | Stripe session creation |
| `src/lib/stripe.ts` | Stripe client singleton |
| `src/stores/cart.ts` | Zustand cart + persistence |
| `prisma/schema.prisma` | DB schema (User, Product, Order) |
| `src/lib/email.ts` | Resend client + helpers |

## Active Work
- [ ] `handleRefund()` in webhook handler
- [ ] Integration tests for webhook endpoints
- [ ] Order confirmation email template
- [ ] Admin dashboard (not started)

## Completed
- [S1-3] Scaffolding, Prisma schema, seed data
- [S4] Product listing SSR + pagination
- [S5] Cart with Zustand + localStorage, checkout UI
- [S6] Stripe checkout session creation
- [S7] `handlePaymentSuccess()` webhook, Resend email setup

## Architecture
- All payment logic server-side only. No Stripe keys in client.
- Cart is client-side. On checkout, items validated against DB prices.
- Orders created only after webhook confirmation, not at session creation.

## Session Log
| S# | Date | Summary |
|----|------|---------|
| 5 | 04-02 | Cart UI, started Stripe |
| 6 | 04-05 | Checkout session creation |
| 7 | 04-08 | Payment webhook, email setup |

## External Context
- Stripe: test keys in `.env.local`, client-managed account
- Neon: `DATABASE_URL` in env
- Resend: `RESEND_API_KEY`, sending from `orders@sweetcrumb.com`
- Vercel: auto-deploys from `main`
