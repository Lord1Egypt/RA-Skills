# SpendCap security boundary

- Reuse one OAuth-authenticated Receipt connection; never collect a provider key or static Receipt
  credential.
- Verify exactly eight universal Receipt tools and reject seller-specific or diagnostic tools.
- The authenticated Receipt owner selects the connected app and sets limits on Receipt's site.
- Trusted app identity, owner, connection, registered client, platform, and USD currency binding
  come from Receipt server records, not chat or URL claims.
- Installation and conversation do not grant spending authority.
- High-risk, recurring, physical-world, transfer, cash-equivalent, or suspected-compromise
  purchases remain approval-required or blocked by Receipt policy.
- Pause and Revoke must stop the next purchase before provider execution.
- SpendCap only governs purchases made through Receipt today.
