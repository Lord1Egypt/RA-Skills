# Changelog

All notable changes to Skill Router should be recorded here.

## `v0.1.0` - 2026-03-12

### Added
- first public `skill-router` skill structure
- capability-first routing model
- resolution order for installed skill reuse, fallback, and discovery
- publish-safe runtime contract
- quiet-by-default reminder policy
- micro routing examples for reuse vs discovery boundaries
- local override example and local map pattern guidance

### Changed
- established `reuse-first` as the default routing behavior
- added an enough-is-enough rule so sufficiently capable installed skills are not displaced by novelty or over-specialization
- added discovery flow through `find-skills` and safety gating through `skill-vetter`

### Validated
- high-relevance routing scenarios
- quiet ordinary-task scenarios
- adversarial / pressure-style routing scenarios
- discovery vs reuse boundary behavior
