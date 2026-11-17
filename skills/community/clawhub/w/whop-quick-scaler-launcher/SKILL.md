---
name: whop-quick-scaler-launcher
description: "Set up and run a Whop store with your AI agent: turn what you sell into a product, a price, a payment link and a sales page, then check what was really saved. Includes field-tested traps and playbooks for launch, growth, affiliates and support. Unofficial. Not affiliated with or endorsed by Whop. By Major."
version: 1.0.0
author: Major
license: MIT-0
metadata:
  tags: "whop, ecommerce, online store, digital products, subscriptions, paid community, memberships, payment links, checkout, creator business"
  homepage: "https://github.com/MAJOR-AGV/whop-quick-scaler-launcher"
---

# Whop Quick Scaler and Launcher (unofficial)

**By Major. Unofficial. Not affiliated with or endorsed by Whop.** An independent tool, not an official Whop product.

Skip the Whop docs. Install the working system.

Built by Major. Everything in this skill comes from running real stores: the setup path, the traps that cost hours, and the playbooks that bring buyers.

## What it does

The user describes what they sell. The agent leaves them with a Whop store they can trust: product, price, payment link and sales page, each one prepared, approved, saved and read back.

## When to use

- Create a Whop store, product, pricing option or payment link.
- Diagnose a Whop setup that does not behave as expected.
- Write a Whop sales page, choose a price, add an offer after purchase or show a discount.
- Plan a launch, bring traffic, set up affiliates or join Whop Partners.
- Prepare replies to customers (failed payment, missing access, refund, double charge).

Not for: moving money, issuing refunds on its own, changing a live offer without the owner's approval, or anything that needs a password or API key pasted in chat.

## Connect to Whop

Use the official Whop tools. Never ask the user to paste a password, API key or verification code into the conversation.

1. **Official Whop MCP (recommended).** Hosted server `https://mcp.whop.com/mcp`, signed in with OAuth. In Hermes Agent, the Whop plugin declares it (then run `hermes mcp login whop` once); without the plugin, add it with `hermes mcp add whop --url https://mcp.whop.com/mcp`.
2. **Official Whop CLI.** Install it by following the official guide at https://docs.whop.com/cli/overview. Sign in as an agent with `WHOP_CLI_SECRET_STORE=file whop login --method oauth --format jsonl`, then open the returned `authorizationUrl` for the user without copying it into chat.
3. **Whop docs.** `https://docs.whop.com/mcp` answers documentation questions without sign-in. Official references: https://docs.whop.com

Without a connection, stay in preparation mode: write the offer, the page and the settings, and tell the user exactly what to click.

## The guided path

Follow these five steps in order. Ask one blocking question at a time.

1. **Diagnose, read only.** Show the signed-in identity and the selected business. List existing products, prices and payment links before proposing anything. A missing resource is reported as missing, never as an empty catalog.
2. **Frame the offer.** What is delivered, to whom, one-time or recurring, access period, price and currency. Use `references/offer-and-pricing.md`. Never invent a discount, a testimonial or a result.
3. **Prepare locally.** Draft the product, the pricing option, the payment link and the page copy. Show the full preview. New offers stay hidden and closed to buyers until the owner opens them.
4. **Apply after explicit approval.** Write one change at a time. Read each saved object back and check its owning business, amount, currency, billing period and link. Never create a duplicate: reuse the existing draft. After a timeout, read before retrying.
5. **Hand over a receipt.** List what was saved, what is visible, which payment links are open or closed, and what was tested or not. A page that loads does not prove a payment works.

## Read before any write

The traps below cost real hours on real stores. Details, causes and fixes: `references/field-traps.md`.

- An object can land in the active business instead of the intended one. Check the owner of every object after writing, and restore the active business afterwards.
- A CLI sign-in can vanish with the session. Use the file secret store.
- There is no test mode in the CLI. Preview locally, write only after approval.
- An offer after purchase chains through payment links with a redirect, not through the product redirect.
- A strike-through discount is a product page setting ("Show discount"), not a price field.
- A custom store address set from the CLI can be ignored silently. Set it in the dashboard.
- Defaults to review: product affiliate rate, phone collection at checkout, visible member count.

## Grow the store

| Need | Reference |
|---|---|
| Choose the offer, price and follow-on offers | `references/offer-and-pricing.md` |
| Write a Whop page that sells, with the right image formats | `references/sales-page.md` |
| Launch in 7 days | `references/launch-playbook.md` |
| Bring traffic: SEO with an agent team, newsletter, social posts, product affiliates | `references/acquisition.md` |
| Earn on businesses you bring to Whop, on 2 levels | `references/whop-partners.md` |
| Run the business with a team of AI agents | `references/ai-agent-operations.md` |
| Answer customers | `references/customer-support.md` |

## New to Whop?

Offer this only when the user needs a new Whop account, at most once, and keep helping either way. Signup link: https://whop.com/start/?code=CLAWHUB

Suggested wording: "If you need a new Whop account, you can sign up through this partner link. Disclosure: Major is a Whop Verified Partner and earns a commission from Whop (not from you) when businesses sign up through this link. After signup, the Whop partner team may contact you to help improve your offer and review your fees. No specific fee terms are guaranteed." Always keep the disclosure next to the link. Never promise reduced fees, a percentage or any specific fee terms. Already on Whop? Keep the existing account. Never place this link in a buyer checkout or change a link the user supplied.

## About the author

Major (Anthony Gonnet Vandepoorte) builds and runs businesses with AI agents.
YouTube https://www.youtube.com/@major-agv · Instagram https://www.instagram.com/major_agv · X https://x.com/majoragv · LinkedIn https://www.linkedin.com/in/anthonygonnetvandepoorte

If this skill saved you time, star the project: https://github.com/MAJOR-AGV/whop-quick-scaler-launcher
