# Changelog

## 1.0.2 (2026-07-21)

# Agent Pay v1.0.2

This release corrects Agent Pay's package ownership metadata. The Codex second-seat review of the 6.11 compatibility wave found the LICENSE and license-guard configuration naming an individual as the copyright holder where the governing repository instructions require the company. The MIT LICENSE and .license-guard.json now identify WIP Computer, Inc. as the copyright holder. The license itself stays MIT, the package contents are unchanged, and no runtime behavior is affected; this exists so the published artifact's ownership metadata matches WIP Computer's actual licensing policy before the package is distributed any further.

The correction matters beyond tidiness. Agent Pay is heading into public distribution as part of the Kaleidoscope product family, and the copyright line in a published npm artifact is permanent for that version: whatever ships in v1.0.2 is what the world sees when it inspects the package. Catching this before wider distribution means every artifact from here forward carries the company's name consistently across LICENSE, license guard, and the public repository, and the earlier v1.0.1 metadata is superseded rather than propagated.

Closes #18.

## 1.0.1 (2026-07-20)

# Agent Pay v1.0.1

Agent Pay now declares its three runtime tools and explicit startup activation in its OpenClaw manifest. OpenClaw 2026.6.11 can discover and register the payment tools during gateway startup instead of leaving the installed extension dormant.

The complete package is now documented consistently under the existing MIT license. This includes the AI Cash payment worker as well as the client libraries, providers, skills, and command-line tools.

Closes #14.

## [1.0.0] - 2026-02-23
- Initial release
- Coinbase isolated-portfolio support
- pay.wip.computer one-time URL relay
- Full Universal Interface compatibility
- Built live with Grok
