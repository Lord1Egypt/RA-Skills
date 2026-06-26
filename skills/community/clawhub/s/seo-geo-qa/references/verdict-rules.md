# Verdict rules

Use these as defaults, not dogma.

## FAIL

Fail when any of the following is true:
- one or more dead external links
- too many TIER-D sources
- SERP topic overlap is materially low
- the article is missing critical evidence for its core claims

## REVISE

Use REVISE in writer mode when:
- the article is not publish-ready
- the issues are fixable in another draft pass
- no human escalation is needed yet

## PASS

Pass when:
- no critical issues remain
- weak-source warnings are tolerable or addressed
- the article has enough evidence to support its major claims
- the report does not reveal obvious structural reliability problems

## Warning-only issues

These should not fail an article by themselves:
- FAQ count slightly low
- a small number of moved links
- SERP analyzer temporarily unavailable
- a few TIER-C sources in otherwise strong evidence mix

## Degrade gracefully

If public search or target sites block automation:
- keep the report running
- emit warnings instead of crashing the whole workflow
- require editorial judgment on ambiguous cases
