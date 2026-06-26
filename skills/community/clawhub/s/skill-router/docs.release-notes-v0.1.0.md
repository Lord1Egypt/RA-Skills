# Skill Router v0.1.0 Release Notes

## Summary

Skill Router v0.1.0 is the first public iteration of a low-presence routing layer for skill-heavy agent environments.

It helps the agent:
- choose the best installed skill first
- avoid unnecessary rediscovery and reinstallation
- move into skill discovery only when installed capabilities are clearly insufficient
- route unfamiliar third-party candidates to vetting before installation

## What changed

### Core routing behavior
- introduced capability-first routing instead of hard-coding one workspace's local skill names as universal truth
- established installed-reality-first resolution
- added reuse-first behavior as the default
- added an enough-is-enough rule so sufficiently capable installed skills are not displaced just because something newer or more specialized might exist

### Discovery and safety
- added a discovery flow for no-strong-match situations
- positioned `find-skills` as the discovery step
- positioned `skill-vetter` as the safety gate for unfamiliar third-party candidates
- clarified that discovery is for insufficiency, not novelty

### Noise control
- kept the skill quiet by default
- limited intervention to cases where skill choice itself becomes the problem
- added reminder policy and micro routing examples to stabilize behavior in both normal and adversarial scenarios

## Validation basis

This version was shaped through comparative testing across:
- high-relevance routing scenarios
- ordinary tasks where the router should stay quiet
- adversarial and pressure-style prompts that try to force unnecessary discovery or unsafe installation

## Outcome

Skill Router v0.1.0 is the first version that feels like a real routing layer rather than a skill-announcement layer: quiet when unnecessary, decisive when routing matters.
