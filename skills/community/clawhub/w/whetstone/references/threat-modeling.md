# Threat modeling

Use when a change adds or moves a trust boundary: a new entry point, integration, file upload, outbound request, role or tenant split, or an agent with tools. Scale the depth to the risk; a note in the pull request often suffices, and an existing model should be updated rather than replaced.

## Four questions

These questions are adapted from the Threat Modeling Manifesto. Answer them in writing, in proportion to the change.

1. What are we building? Sketch the actors, processes, data stores and flows, and mark each place where trust changes: internet to service, service to database, one tenant to another, untrusted content into a model's context, CI into production. List what an attacker would want, such as personal data, credentials, money or availability.
2. What can go wrong? For each flow that crosses a boundary, ask whether someone could pose as another party, alter data, deny an action, read data they should not, exhaust a resource or gain rights they were not given. These are the STRIDE categories.
3. What will we do about it? Mitigate it, remove the feature that creates it, transfer it to a party that owns it, or accept it with a named owner and a reason.
4. Did we do a good enough job? Check that the model matches the code as built, that every serious threat has a tested control or an owned acceptance, and that someone other than the author challenged it.

## Abuse cases

Ask how an intended feature could be misused, not only how code could be attacked:

- A step skipped, repeated, replayed or reordered, such as a coupon applied twice or an order confirmed before payment.
- Two concurrent requests that both succeed where only one should.
- Identifiers that can be guessed to probe other users' records.
- Fields the client should not control, such as role, price, owner or entitlement, accepted through mass assignment.
- A cheap request that triggers expensive work, such as an export or a model call, at scale.

## Mitigations become tests

Write each agreed mitigation as a requirement with a check that fails if the control is removed, for example "a user of tenant A gets 404 for tenant B's invoice". Cite an OWASP ASVS requirement where one fits. Track any mitigation not yet built as an issue; an untracked mitigation is a risk nobody accepted. Rate likelihood and impact as high, medium or low rather than with precise-looking scores.

For an agent, check whether one component combines private data, untrusted content and the ability to act or send data out, and remove or constrain one of the three ([AI boundaries](ai-features.md)). Keep the model beside the design and update it when flows or boundaries change. The [threat model template](../templates/threat-model.md) is optional.

## Sources

- [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
