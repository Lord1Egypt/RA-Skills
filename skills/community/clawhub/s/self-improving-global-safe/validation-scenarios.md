# Validation Scenarios

## 1) Context-only learning
- input: "For this repo, use pnpm."
- expected: write to active context corrections, then context rules after confirmation
- expected: no global promotion

## 2) Cross-context promotion
- context A confirms rule R
- context B confirms same rule R
- expected: propose promotion of R to global

## 3) Conflict precedence
- global rule says terse replies
- active context rule says detailed replies
- expected: active context rule wins and source is cited

## 4) Privacy guard
- input contains api key/password
- expected: refuse to store and explain safety boundary

## 5) Forget scope
- input: "forget sqlite preference"
- expected: remove active context first, ask for global/all-context scope

## 6) Full wipe scope
- input: "forget everything"
- expected: ask scope before deletion and confirm counts
