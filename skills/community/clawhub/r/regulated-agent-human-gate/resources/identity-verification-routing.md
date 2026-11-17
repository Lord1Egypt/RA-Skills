# Identity Verification Routing

Identity is not authority. Authentication is not business approval. A passed check satisfies only the named control and must not clear unrelated controls.

- Authentication confirms a session factor such as OTP, passkey, PIN, or device binding.
- Identity verification checks document, liveness, face match, and identity consistency evidence.
- Authority verification checks whether the person and agent are allowed to perform this exact action.
- Business approval decides whether the payment, loan, off-ramp, or account-control change should happen.
- Compliance review resolves screening, policy, or provider uncertainty through an authorized process.

Bind every provider result to `subject_id`, `decision_id`, `action_hash`, provider, check type, completion time, expiry, and evidence reference. Reject stale results, subject mismatch, action mismatch, unverifiable provider assertions, and agent-authored claims.

If identity passes but business risk remains high, keep independent human approval or compliance review active. Re-run time-sensitive checks when the receipt would outlive the evidence.
