# Agent Pay v1.0.2

This release corrects Agent Pay's package ownership metadata. The Codex second-seat review of the 6.11 compatibility wave found the LICENSE and license-guard configuration naming an individual as the copyright holder where the governing repository instructions require the company. The MIT LICENSE and .license-guard.json now identify WIP Computer, Inc. as the copyright holder. The license itself stays MIT, the package contents are unchanged, and no runtime behavior is affected; this exists so the published artifact's ownership metadata matches WIP Computer's actual licensing policy before the package is distributed any further.

The correction matters beyond tidiness. Agent Pay is heading into public distribution as part of the Kaleidoscope product family, and the copyright line in a published npm artifact is permanent for that version: whatever ships in v1.0.2 is what the world sees when it inspects the package. Catching this before wider distribution means every artifact from here forward carries the company's name consistently across LICENSE, license guard, and the public repository, and the earlier v1.0.1 metadata is superseded rather than propagated.

Closes #18.
