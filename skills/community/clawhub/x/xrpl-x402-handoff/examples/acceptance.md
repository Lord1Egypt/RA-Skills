# Acceptance criteria — xrpl-x402-handoff

- [ ] Frontmatter: `name: xrpl-x402-handoff` + trigger-based `description`
- [ ] Steps cover discover → pay exact/paychan → verify-lag retry → handoff
- [ ] Output format includes handoff owner + do-not-do
- [ ] Constraints: no seed in chat; testnet default; no Spec72 XRP rail until buyer asks
- [ ] README ≤5 install lines
- [ ] Zip layout: `xrpl-x402-handoff/SKILL.md` at folder root
- [ ] No secrets, private keys, or fabricated tx hashes in sample
- [ ] Install test: trigger phrase loads skill and returns structured block
