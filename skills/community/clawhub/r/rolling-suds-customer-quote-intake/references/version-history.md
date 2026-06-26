# Version history

## 0.1.10
- Require Lead number before intake handoff


## 0.1.9
- Require Lead number before estimator flow


## 0.1.8
- Added ClawHub publish metadata headers (`homepage`, `metadata.openclaw.emoji`) for registry publishing.


## 0.1.7 - 2026-04-05
- Added hard rule: address is required before producing estimator-ready output.
- Clarified that missing address should block forward estimate flow until supplied.

## 0.1.6 - 2026-04-05
- Added rule: preserve Workiz Lead # in intake and estimator handoff when available.
- Clarified that missing customer/contact details in pasted lead blobs may simply not be included in the source text.

## 0.1.5 - 2026-04-05
- Renamed skill from `quote-intake` to `rolling-suds-customer-quote-intake`.
- Updated Rolling Suds branding in skill metadata and repo/project naming.

## 0.1.4 - 2026-04-05
- Added rule: virtual appointments are real quote appointments, not weak lead signals.
- Added handling for appointment type (virtual vs in-person) and photo/access dependency in intake logic.
- Clarified residential workflow should support virtual quotes as a primary mode.

## 0.1.3 - 2026-04-05
- Added rule: partial-house requests should tee up two outputs from estimating: a recommended whole-house quote and a separate $250 partial-only comparison quote.

## 0.1.2 - 2026-04-05
- Added rule: partial house requests should note that the $250 minimum may make a whole-house quote the better customer value.
- Clarified estimator handoff should preserve that sales guidance for partial-house inquiries.

## 0.1.1 - 2026-04-05
- Added rule: "agreed to an in-person visit" means a real quote appointment.
- Added wording-normalization guidance for awkward cold-calling / lead-gen phrasing.
- Clarified Workiz note should reflect appointment status when implied by the source wording.

## 0.1.0 - 2026-04-05
- Initial release of `quote-intake`.
- Added default workflow for messy sales/customer intake.
- Added standardized outputs: intake summary, estimator handoff, Workiz note, follow-up questions, and manual-review flags.
- Added default design guidance and iteration notes.
