"""
stripe_helpers.py — Drop-in Stripe helpers for agent-built apps.

Usage:
    from scripts.stripe_helpers import (
        create_checkout_session,
        create_portal_session,
        is_subscription_active,
        handle_webhook_event,
    )

Requires: pip install stripe python-dotenv
Env vars: STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY,
          STRIPE_WEBHOOK_SECRET, STRIPE_PRICE_ID
"""

import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")


# ── Checkout ──────────────────────────────────────────────────────────────────

def create_checkout_session(
    customer_email: str,
    success_url: str,
    cancel_url: str,
    price_id: str | None = None,
    mode: str = "subscription",
    allow_promo_codes: bool = True,
    metadata: dict | None = None,
) -> str:
    """
    Create a Stripe Checkout session. Returns the redirect URL.

    Args:
        customer_email: Pre-fill the email on the Stripe checkout page.
        success_url: Redirect here after successful payment.
                     Append ?session_id={CHECKOUT_SESSION_ID} to retrieve session data.
        cancel_url: Redirect here if the user cancels.
        price_id: Override the default STRIPE_PRICE_ID env var.
        mode: "subscription" (recurring) or "payment" (one-time).
        allow_promo_codes: Show the promo code field on checkout.
        metadata: Extra key/value pairs attached to the session.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode=mode,
        line_items=[{"price": price_id or PRICE_ID, "quantity": 1}],
        customer_email=customer_email or None,
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        allow_promotion_codes=allow_promo_codes,
        metadata=metadata or {},
    )
    return session.url


# ── Portal ────────────────────────────────────────────────────────────────────

def create_portal_session(stripe_customer_id: str, return_url: str) -> str:
    """
    Create a Stripe billing portal session for self-service billing management.
    Returns the redirect URL.

    Prerequisites: Enable Customer Portal in Stripe Dashboard →
                   Settings → Billing → Customer portal.
    """
    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=return_url,
    )
    return session.url


# ── Subscription status ───────────────────────────────────────────────────────

def is_subscription_active(stripe_customer_id: str) -> bool:
    """Return True if the customer has at least one active subscription."""
    subs = stripe.Subscription.list(
        customer=stripe_customer_id,
        status="active",
        limit=1,
    )
    return len(subs.data) > 0


def get_subscription(stripe_customer_id: str) -> dict | None:
    """
    Return the first active subscription for a customer as a dict,
    or None if no active subscription exists.

    Useful fields:
        sub["id"]                          → subscription ID
        sub["status"]                      → "active", "past_due", etc.
        sub["current_period_end"]          → Unix timestamp of next renewal
        sub["cancel_at_period_end"]        → True if scheduled to cancel
    """
    subs = stripe.Subscription.list(
        customer=stripe_customer_id,
        status="active",
        limit=1,
    )
    if not subs.data:
        return None
    return subs.data[0].to_dict()


# ── Webhook ───────────────────────────────────────────────────────────────────

def verify_webhook(payload: bytes, sig_header: str) -> dict | None:
    """
    Verify a Stripe webhook signature and return the parsed event dict.
    Returns None if verification fails.

    Usage (Flask):
        payload = request.data
        sig = request.headers.get("Stripe-Signature")
        event = verify_webhook(payload, sig)
        if event is None:
            return jsonify({"error": "Invalid signature"}), 400
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
        return event
    except stripe.error.SignatureVerificationError:
        return None


def handle_webhook_event(event: dict, handlers: dict) -> str:
    """
    Dispatch a Stripe webhook event to the correct handler.

    Args:
        event: Parsed event dict from verify_webhook().
        handlers: Dict mapping event type → callable(data).
                  e.g. {
                      "checkout.session.completed": my_checkout_handler,
                      "customer.subscription.deleted": my_cancel_handler,
                  }

    Returns:
        "handled" if a matching handler was called, "ignored" otherwise.
    """
    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})
    handler = handlers.get(event_type)
    if handler:
        handler(data)
        return "handled"
    return "ignored"


# ── Customer helpers ──────────────────────────────────────────────────────────

def get_or_create_customer(email: str, name: str | None = None, metadata: dict | None = None) -> str:
    """
    Return an existing Stripe customer ID for this email, or create one.
    Returns the customer ID string (cus_...).
    """
    existing = stripe.Customer.list(email=email, limit=1)
    if existing.data:
        return existing.data[0].id

    customer = stripe.Customer.create(
        email=email,
        name=name,
        metadata=metadata or {},
    )
    return customer.id


# ── CLI test ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.getenv("STRIPE_SECRET_KEY", "")
    if not key:
        print("❌ STRIPE_SECRET_KEY not set. Add it to your .env file.")
    elif key.startswith("sk_test_"):
        print(f"✅ Stripe connected (test mode)")
        print(f"   Key prefix: {key[:12]}...")
        # List products as a connectivity check
        products = stripe.Product.list(limit=3, active=True)
        print(f"   Active products: {len(products.data)}")
        for p in products.data:
            print(f"     - {p.name} ({p.id})")
    elif key.startswith("sk_live_"):
        print(f"✅ Stripe connected (LIVE mode)")
        print(f"   Key prefix: {key[:12]}...")
    else:
        print(f"⚠️  Unexpected key format: {key[:8]}...")
