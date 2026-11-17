# Stablecoin Off-ramp Agent

Agent wants to convert USDC to fiat and send funds to a bank account.

Inspect KYC, AML, sanctions, Travel Rule triggers, wallet-bank ownership, amount, and recent account changes.

AML timeout or unknown provider result must route to `COMPLIANCE_REVIEW`, not default allow.

