#!/usr/bin/env python3
"""Return a simulated inquiry success response.

Version 1 does not transmit, store, or email inquiry data. It only validates
required fields and prints a local JSON success response.
"""

from __future__ import annotations

import argparse
import json
import re


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate a B2B safety footwear inquiry submission.")
    parser.add_argument("--name", required=True, help="Buyer contact name.")
    parser.add_argument("--email", required=True, help="Buyer email address.")
    parser.add_argument("--company", default="", help="Buyer company name.")
    parser.add_argument("--product", required=True, help="Product or product type of interest.")
    parser.add_argument("--quantity", default="", help="Estimated order quantity.")
    parser.add_argument("--message", required=True, help="Inquiry details.")
    args = parser.parse_args()

    errors: list[str] = []
    if not args.name.strip():
        errors.append("name is required")
    if not EMAIL_RE.match(args.email.strip()):
        errors.append("email must be a valid address")
    if not args.product.strip():
        errors.append("product is required")
    if len(args.message.strip()) < 10:
        errors.append("message should include at least 10 characters")

    if errors:
        print(json.dumps({
            "ok": False,
            "status": "validation_error",
            "errors": errors
        }, ensure_ascii=False, indent=2))
        return 2

    print(json.dumps({
        "ok": True,
        "status": "success",
        "message": "Inquiry draft accepted by this local skill simulation. It does not transmit data externally.",
        "inquiry": {
            "name": args.name.strip(),
            "email": args.email.strip(),
            "company": args.company.strip(),
            "product": args.product.strip(),
            "quantity": args.quantity.strip(),
            "message": args.message.strip()
        },
        "live_follow_up": {
            "supplier": "Reliable Safety Products",
            "website": "https://reliablesafetyboots.com",
            "contact_page": "https://reliablesafetyboots.com/contact-us",
            "reference_note": "Use live supplier channels for real quotations, samples, certifications, and order follow-up."
        }
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
