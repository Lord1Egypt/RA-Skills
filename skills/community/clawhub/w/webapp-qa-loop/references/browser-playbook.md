# Browser Playbook

## Preserve the user's browser state

Use a browser that already contains the required signed-in session only when that state is necessary. Otherwise prefer an isolated in-app browser for local or public pages. Do not close unrelated tabs, modify extensions, clear browser-wide data, inspect unrelated history, or expose session storage.

An authorized session permits in-scope navigation; it does not authorize account switching, security-setting changes, credential changes, completing MFA, or triggering notifications. Treat login, MFA, CAPTCHA, consent, and account switching as user-controlled boundaries unless exact authorization covers the specific action.

## Environment and data boundary

Production and shared environments are read-only by default. Do not create, edit, delete, or clean data there without exact authorization for that target, object, maximum count, external effect, and recovery/cleanup plan.

In a verified isolated non-production tenant, bounded synthetic data may be created and cleaned automatically when all of these hold:

- data uses a unique prefix such as `qa-<date>-<short-id>` and belongs only to this run;
- no real recipient, delivery channel, payment rail, billing, or external integration is reached;
- no real user, permission, credential, subscription, or security setting changes;
- cleanup is reliable and cannot affect records not created by this run.

If cleanup cannot safely complete, stop cleanup, record the exact owned IDs and residual impact, and report them. In production or a shared environment, cleanup itself is a separate mutation requiring authorization; do not infer permission from ownership of the test record.

## Notifications, OTP, MFA, and permissions

- A test sink or repository-provided fake inbox/phone/push endpoint may be used in isolated non-production when no real delivery occurs.
- Triggering a real email, SMS, chat, push, invitation, or OTP requires exact authorization naming the recipient/account and maximum count. A request to test a form or login is not enough.
- Never read an OTP from email, SMS, notifications, clipboard history, or another app. The user enters the code or approves the MFA prompt.
- Do not bypass CAPTCHA, MFA, rate limits, authorization checks, or provider safeguards.
- Permission tests must not remove the last owner/admin, disable the only recovery channel, lock out the active account, or strand a tenant. Such tests require an isolated fixture designed for recovery or an explicitly authorized plan.

## Interaction rules

- Prefer accessible names, labels, roles, and stable test identifiers over coordinates or brittle CSS paths.
- Wait for observable state: URL, heading, enabled control, network completion, DOM change, persisted data, or confirmed downstream effect.
- Avoid fixed sleeps except a short diagnostic delay with an explicit reason.
- Scroll and resize deliberately; record viewport when layout matters.
- Before any mutation, verify target identity, reversibility, authority, maximum count, external effect, and cleanup/recovery plan.
- After a mutation, verify durable state or downstream behavior. A toast alone is not proof.
- Record every actual externally visible action and synthetic-data cleanup result in the ledger.

## Evidence packet

For every confirmed defect, capture the smallest packet that proves it:

- environment URL, immutable target identity when relevant, and version/build when available;
- role, viewport, and relevant preconditions;
- concise reproduction steps;
- expected and actual behavior;
- screenshot or recording at the decisive state;
- relevant DOM/accessibility evidence;
- relevant console or network evidence with secrets removed;
- persistence or downstream verification when state changes;
- issue ID, declared scenario ID, and target/artifact/attempt binding when applicable.

Do not capture passwords, OTPs, tokens, cookies, authorization headers, personal conversations, unrelated user data, or full production payloads. Redact or summarize sensitive fields.

## Confirming a defect

For non-P0 issues, prefer either two consistent reproductions or one reproduction plus deterministic browser, test, log, DOM, or network evidence. Record a P0 immediately and stop the unsafe mutation. Do not repeatedly reproduce destructive behavior.

## Filter common noise

Do not classify an observation as a product defect without correlation. Common noise includes:

- expected development-only duplicate effects from framework strict modes;
- expected 401/403 responses during auth probes or session refresh;
- canceled requests caused by intentional navigation;
- browser extensions and injected scripts;
- third-party analytics or ads outside product control;
- stale cache or service workers not reproducible in the target release state;
- pre-existing console warnings unrelated to the journey.

Record persistent relevant warnings as baseline debt when they are real but outside scope.

## UI and interaction review

Check objective behavior before subjective polish:

- controls have clear accessible names and states;
- focus is visible and moves predictably;
- validation appears near the field and is announced when applicable;
- loading prevents accidental duplicate work without trapping the user;
- empty/error/retry states explain the next action;
- overlays manage focus, escape, scroll, and stacking correctly;
- navigation, back, refresh, and deep links preserve or intentionally reset state;
- text does not clip or overlap at selected viewports;
- contrast and target size follow the product's existing system and accessibility standard.

Do not invent colors, typography, spacing, animation, or a design language. Use established tokens/components; if no objective standard exists, report the subjective observation instead of redesigning silently. Route an explicitly pure UX or visual audit to the dedicated product-design audit workflow rather than this skill.

## Browser failure handling

If browser control loses state:

1. record the last completed declared scenario, ledger state, target, and current URL;
2. take a screenshot if safe;
3. retry the control connection once;
4. reconcile the current browser and application state before resuming from the latest durable step;
5. ask the user only when authentication, MFA, or external confirmation is required.

Do not replay state-changing steps until their actual outcome is known.
