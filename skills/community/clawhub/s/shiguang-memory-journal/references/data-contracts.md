# Portable data contracts

Use these shapes as a common handoff language. Add implementation-specific fields without removing provenance.

## Source and element manifest

```json
{
  "memoryId": "memory-stable-id",
  "source": {
    "id": "source-01",
    "kind": "key-frame",
    "uri": "relative/or/tool-specific/frame-reference",
    "sourceUrl": null,
    "title": "optional verified title",
    "observations": ["visible, supportable facts"],
    "warnings": ["source URL not supplied"]
  },
  "intention": "诗与远方",
  "journalType": "life",
  "style": "realistic",
  "requestedElementCount": 3,
  "backgroundMode": "mixed",
  "elements": [
    {
      "id": "element-01",
      "parentSourceId": "source-01",
      "title": "远山",
      "visibleEvidence": "层叠的蓝绿色山体",
      "storyRole": "hero",
      "generationMode": "redraw",
      "style": "realistic",
      "backgroundMode": "preserve-context",
      "assetUri": "relative/or/tool-specific/asset-reference",
      "sourceUrl": null,
      "promptSummary": "single-subject hand-drawn redraw preserving meaningful scene context",
      "warnings": []
    },
    {
      "id": "element-02",
      "parentSourceId": "source-01",
      "title": "山城背景",
      "visibleEvidence": "城市建筑、山体与道路",
      "storyRole": "setting",
      "generationMode": "redraw",
      "backgroundMode": "background-only",
      "assetUri": "relative/or/tool-specific/background-reference",
      "sourceUrl": null,
      "promptSummary": "environment redraw excluding foreground people",
      "warnings": []
    }
  ]
}
```

Allowed `generationMode` values:

- `redraw`: a model or artist created a new visual interpretation;
- `crop`: the original visual was isolated without being redrawn;
- `prompt-only`: no asset was created; a reusable prompt was delivered;
- `user-provided`: the asset came directly from the user.

Allowed `style` values:

- `handdrawn`: soft hand-drawn cartoon rendering;
- `comic`: high-contrast comic highlight rendering;
- `collage`: aged collage rendering;
- `realistic`: natural photographic light and materials with restrained refinement. It must preserve identity, people count, pose, anatomy, lens perspective, and scene relationships; it must not imply face replacement, body reshaping, aggressive HDR, or synthetic 3D treatment.

Allowed task-level `backgroundMode` values:

- `subject-only`: isolate the subject and remove unrelated background;
- `preserve-context`: keep one primary subject together with the environment needed to preserve its spatial, action, or narrative relationship;
- `mixed`: assign an explicit element-level mode to every output. It requires at least two elements and at least two distinct element-level modes.

Allowed element-level `backgroundMode` values:

- `subject-only`;
- `preserve-context`;
- `background-only`: keep the requested environment while removing excluded foreground subjects. This value is only valid for an element within a `mixed` task.

`sourceUrl` is nullable. A missing URL must be recorded as unavailable and must not block extraction or composition.

## Composition input and layout reference

Keep approved content and an optional reference structurally separate:

```json
{
  "contentMaterials": [
    {
      "id": "element-01",
      "kind": "element",
      "sourceUrl": null,
      "approved": true
    }
  ],
  "layoutReference": {
    "id": "reference-01",
    "uri": "relative/or/tool-specific/reference",
    "mode": "layout-only",
    "focus": "主图、小图和文字区域的阅读节奏",
    "restrictions": "不要复制照片、人物、地点、品牌、原文字或事实",
    "analysis": {
      "readingPath": "top-left hero to right-side details",
      "heroStrategy": "one dominant image with two smaller supports",
      "textZones": ["beside hero", "lower closing area"],
      "whitespace": "calm center and generous footer",
      "overlapRhythm": "limited edge overlap"
    }
  }
}
```

Allowed `layoutReference.mode` values:

- `layout-only`: transfer only composition and reading logic;
- `allow-abstract-decoration`: may also transfer non-identifying paper, tape, line, and palette relationships.

Never copy reference-only content into `contentMaterials`.

## Story and layout plan

```json
{
  "story": {
    "spine": "从眼前出发，把向往留在可抵达的路上",
    "readingPath": "top-left to lower-right S-curve",
    "orderedElementIds": ["element-02", "element-01", "element-03", "element-04"],
    "layoutReferenceId": "reference-01",
    "assessment": {
      "source": "user-story",
      "fidelityScore": 10,
      "narrativeScore": 8,
      "selectionScore": 9,
      "editingNotes": "remove repetition, preserve concrete turns and the original closing meaning",
      "retainedFacts": ["verified event or relationship that the final copy may not lose"]
    },
    "copyBlocks": [
      {
        "id": "copy-opening",
        "role": "opening",
        "text": "verified or carefully framed copy",
        "linkedElementIds": ["element-02"],
        "highlightPhrases": ["verbatim phrase already present in text"],
        "typography": {
          "fontFamily": "display",
          "fontWeight": 700,
          "fontSize": 16,
          "letterSpacing": 1.2,
          "lineHeight": 1.55,
          "align": "left",
          "container": "quote"
        }
      }
    ]
  },
  "paper": {
    "palette": ["#F4F0E6", "#7890A0", "#60745B"],
    "material": "warm fibrous paper with mist-blue wash",
    "reservedAreas": ["central content field", "footer source action"],
    "forbiddenMotifs": ["food table", "unrelated fruit", "readable fake text"]
  },
  "layout": {
    "canvas": { "width": 720, "height": 920 },
    "items": [
      {
        "id": "element-01",
        "x": 72,
        "y": 260,
        "width": 396,
        "height": 250,
        "rotation": -1.5,
        "z": 4,
        "role": "hero",
        "frameStyle": "polaroid",
        "tapeStyle": "top",
        "backgroundMode": "preserve-context"
      }
    ]
  }
}
```

Allowed `frameStyle` values are `none`, `paper`, and `polaroid`. Allowed `tapeStyle` values are `none`, `top`, and `corner`. Keep transparent subject cutouts unframed; use frames on contextual images and tape on only a few accents. Highlight phrases must occur verbatim in their copy block.

## Archive record

```json
{
  "schemaVersion": "1.0",
  "memoryId": "memory-stable-id",
  "createdAt": "ISO-8601 when known",
  "source": {},
  "elements": [],
  "story": {},
  "paper": {},
  "layout": {},
  "journalArtifact": {
    "uri": "relative/or/tool-specific/reference",
    "editable": true,
    "previewUri": "optional-preview-reference",
    "title": "可由用户快速整理的标题",
    "subtitle": "可搜索摘要",
    "location": "optional verified place",
    "date": "optional user-facing date",
    "tags": ["optional", "editable"],
    "journalType": "life",
    "updatedAt": "ISO-8601 when known"
  },
  "searchText": "combined factual and interpretive memory description",
  "sourceLinks": [],
  "warnings": ["original source URL unavailable"],
  "generation": {
    "engine": "agent-specific",
    "status": "passed",
    "guideVersion": "auditable-version@content-fingerprint",
    "stages": [
      {
        "id": "story",
        "engine": "agent-specific",
        "summary": "user story scored, refined, and selected"
      }
    ],
    "interactive": {
      "enabled": true,
      "sessionId": "stable-continuation-id",
      "lastApprovedStage": "layout"
    },
    "localRepairs": [
      {
        "type": "controlled-overlap",
        "affectedIds": ["element-01", "element-02"],
        "summary": "moved the contextual image minimally and revalidated"
      }
    ]
  },
  "quality": {
    "story": 8,
    "copy": 8,
    "typography": 8,
    "hierarchy": 9,
    "paperFit": 8,
    "legibility": 8,
    "fidelity": 8,
    "factualIntegrity": 10,
    "provenance": 10
  }
}
```

## Collection mutation

Use a dry-run/confirm/apply sequence for destructive actions:

```json
{
  "operation": "bulk-delete",
  "collection": "journals",
  "selectedIds": ["journal-01", "journal-02"],
  "confirmed": true,
  "effects": {
    "deleteRecords": ["journal-01", "journal-02"],
    "unlinkMemoryIds": ["memory-01"],
    "removeArchiveUris": [
      "memory-01/journal/journal-01.json",
      "memory-01/previews/journal-01.png"
    ],
    "preserveSharedAssetIds": ["element-01", "background-02"]
  },
  "result": {
    "deletedIds": ["journal-01", "journal-02"],
    "failedIds": [],
    "warnings": []
  }
}
```

For library or memory collections, replace `collection` and keep the same stable-ID, confirmation, effects, and result fields. Add a tombstone or suppression record when automatic backfill could recreate an intentionally deleted item.

## Portable editable journal interchange

Use a versioned envelope for round-trip import and export:

```json
{
  "format": "shiguang-journal",
  "schemaVersion": "1.0",
  "exportedAt": "ISO-8601",
  "journal": {
    "id": "original-journal-id",
    "title": "editable title",
    "canvasMode": "scrapbook",
    "canvasWidth": 720,
    "canvasHeight": 1080,
    "backgroundSrc": "data:image/png;base64,...",
    "annotations": [
      {
        "id": "copy-opening",
        "kind": "lead",
        "text": "editable factual opening",
        "highlightPhrases": ["factual opening"],
        "x": 44,
        "y": 215,
        "width": 632,
        "fontFamily": "display",
        "fontWeight": 700,
        "fontSize": 16,
        "letterSpacing": 1.2,
        "lineHeight": 1.55,
        "textEffect": "none",
        "align": "left",
        "style": "quote"
      }
    ],
    "elements": [
      {
        "id": "element-01",
        "kind": "sticker",
        "title": "independent image layer",
        "src": "data:image/png;base64,...",
        "videoUrl": "",
        "x": 72,
        "y": 260,
        "width": 396,
        "height": 250,
        "rotation": -1.5,
        "zIndex": 4,
        "backgroundMode": "preserve-context",
        "frameStyle": "polaroid",
        "tapeStyle": "top"
      }
    ]
  },
  "provenance": {
    "originalJournalId": "original-journal-id",
    "sourceLinks": [],
    "warnings": ["original source URL unavailable"]
  }
}
```

Rules:

- generate a new stable journal ID on import; never silently overwrite the source record;
- persist embedded images before saving the imported journal and replace `data:` or temporary URLs with durable asset references;
- allow only declared raster image types and safe HTTP(S) source links, with explicit package and per-asset size limits;
- keep missing source links empty rather than inventing them;
- preserve explicit `canvasWidth` and `canvasHeight` when the project does not use the default canvas; use the same dimensions for editing bounds, thumbnails, responsive fit, and export;
- preserve independent element and text records, coordinates, dimensions, rotations, z-order, story metadata, and provenance;
- treat a flattened PNG, JPG, WebP, PDF, or screenshot as a single visual layer or background. It is not a substitute for this structured envelope and cannot truthfully restore original layers.

For target reconstruction, store a process manifest beside the portable journal. At minimum include the source and logical canvas sizes, clean-base URI, every independent layer URI and placement, z-order, element-level background mode, people-count audit, target/reconstructed preview URIs, and visual/browser validation results. Keep original full source images even when a placed element contains only the visible region recovered from an overlapping flattened target.

## Recall result

```json
{
  "query": "那次雨后骑车去山里的记录",
  "engine": "agent-specific semantic or disclosed fallback",
  "results": [
    {
      "memoryId": "memory-stable-id",
      "score": 0.87,
      "reason": "画面、描述与雨后、远山和出发的意象相符",
      "previewUri": "optional-preview-reference",
      "sourceLinks": [],
      "nextAction": "reopen the saved key frame or continue editing the journal"
    }
  ],
  "warnings": []
}
```

## Recommended portable folder

```text
memory-stable-id/
├── manifest.json
├── source/
├── elements/
├── journal/
├── previews/
└── notes/
```

Relative paths make the archive movable. Source URLs maintain the path back to the original content when supplied; otherwise preserve an explicit unavailable state and a useful next action.

## Video poster handoff envelope

Use this additive, stack-independent envelope so a renderer, auditor, archive, ranking service, or another agent can continue the video-poster job.

```json
{
  "workflowVersion": "2.6.0",
  "jobId": "video-poster-stable-id",
  "status": "executed",
  "stage": "audited",
  "sourceRecord": {
    "videoUrl": "https://example.com/video-or-empty",
    "fileHash": "sha256-or-empty",
    "title": "source title",
    "evidenceStatus": "ready | metadata-only | unavailable"
  },
  "artifacts": {
    "videoResult": { "status": "executed", "uri": "video-result.json" },
    "narrativeBriefV2": { "status": "executed", "uri": "narrative-brief.json" },
    "tournament": { "status": "executed", "uri": "poster-tournament.json" },
    "winnerBrief": { "status": "executed", "uri": "winner-brief.json" },
    "evidenceGraph": { "status": "executed", "uri": "evidence-graph.json" },
    "visualConcept": { "status": "executed", "uri": "visual-concept.json" },
    "elementCuration": { "status": "executed", "uri": "element-curation.json" },
    "keyArt": { "status": "executed", "uri": "key-art.png", "auditUri": "key-art-audit.json" },
    "typographyBrief": { "status": "executed", "uri": "typography-brief.json" },
    "typographyTournament": { "status": "executed", "uri": "typography-tournament.json" },
    "poster": { "status": "executed", "uri": "poster.png" },
    "audit": { "status": "executed", "uri": "poster-audit.json", "release": "pass | fail | review" },
    "provenance": { "status": "executed", "uri": "provenance.json" },
    "feedbackPlan": { "status": "proposed", "uri": "feedback-plan.json" }
  },
  "warnings": [],
  "blockers": []
}
```

Compact records for the 2.6.0 additions:

```json
{
  "visualConcept": {
    "source": "deterministic | text-ai",
    "concept": {
      "id": "visual-concept-stable-id",
      "family": "decisive-moment | contrast-diptych | icon-scale | threshold-portal | ai-variant",
      "name": "",
      "visualThesis": "",
      "tensionGrammar": [],
      "heroTreatment": "",
      "supportTreatment": "",
      "thumbnailHook": "",
      "intentSignals": [],
      "negativeSpace": "deep | balanced | tight",
      "scaleContrast": "strong | medium | subtle"
    },
    "score": { "intent": 0, "tension": 0, "total": 0 },
    "candidates": [{ "concept": {}, "score": {} }],
    "summary": ""
  },
  "elementCuration": {
    "source": "multimodal-ai | deterministic",
    "selectedElementIds": [],
    "selections": [{
      "elementId": "",
      "rationale": "",
      "visualRole": "hero-echo | support | detail",
      "placementHint": "left-edge | right-edge | top-band | bottom-band | near-title | any",
      "scaleHint": "small | medium | large"
    }],
    "excluded": [{ "elementId": "", "reason": "" }],
    "warnings": []
  },
  "evidenceGraph": {
    "version": 1,
    "nodes": [{ "id": "", "kind": "frame | transcript | ocr | entity | audio | user-fact | claim", "label": "", "time": 0, "text": "", "source": "", "confidence": 0 }],
    "links": [{ "from": "", "to": "", "type": "occursAt | supports | contradicts | derivedFrom | sameEntity | selectedAsHero" }],
    "claims": [{ "id": "", "text": "", "sourceType": "observation | speech | ocr | user-provided | model-inference", "confidence": 0, "evidenceRefs": [], "allowedUsage": [] }]
  }
}
```

Rules:

- `status` is `executed` only when the referenced artifact exists; `degraded` means it exists through a disclosed fallback; `proposed` means specification only.
- Candidate IDs and frame IDs remain stable within the job. Preserve the candidate-pool frame ID separately when final display frames are renumbered.
- `supportFrame` is optional: omit or use `null`, never `0`.
- Default poster target is portrait `9:16` (`1080×1920` delivery or proportional draft); an explicit user/channel target overrides it.
- A failed audit keeps the poster artifact as a draft and sets `release: fail`; it does not change a real rendered file into `proposed`.

Minimum interoperable records:

```json
{
  "evidenceItem": {
    "id": "evidence-stable-id",
    "modality": "frame | subtitle | speech | metadata | ocr | audio",
    "scope": "timed | global",
    "start": 12.4,
    "end": 15.1,
    "frameId": "optional-source-frame-id",
    "text": "observed fact or transcript",
    "confidence": 0.86,
    "independentForExactCopy": true,
    "trust": "untrusted-source-data"
  },
  "tournamentCandidate": {
    "id": "poster-candidate-stable-id",
    "conceptType": "identity-landmark | story-contrast | emotional-invitation",
    "concept": "",
    "title": "",
    "subtitle": "",
    "heroFrame": "source-frame-id",
    "supportFrame": null,
    "selectedFrameIds": [],
    "requiredMustShow": [],
    "claimEvidenceIds": [],
    "scores": {
      "storyCoverage": 0,
      "titleHeroAlignment": 0,
      "subtitleEvidenceAlignment": 0,
      "supportComplementarity": 0,
      "propagationPromise": 0,
      "total": 0
    },
    "disqualified": false,
    "issues": [],
    "warnings": []
  },
  "winnerBrief": {
    "candidateId": "poster-candidate-stable-id",
    "target": { "width": 1080, "height": 1920, "aspectRatio": "9:16" },
    "referenceInfluence": {
      "referenceId": "optional-reference-id",
      "strength": "none | loose | balanced | faithful",
      "allowed": ["reading-path", "hierarchy", "palette-category"],
      "forbidden": ["people", "objects", "places", "text", "brands", "facts"]
    }
  },
  "typographyBrief": {
    "approvedTitle": "exact editable title",
    "approvedSubtitle": "non-redundant editable subtitle",
    "dramaticPromise": "video-specific audience promise",
    "dominantEmotion": "story emotion",
    "memoryHook": "one word, number, or silhouette",
    "safeRegions": [{
      "id": "safe-bottom",
      "x": 0.07,
      "y": 0.7,
      "width": 0.86,
      "height": 0.24,
      "anchor": "bottom-center",
      "orientation": "horizontal",
      "confidence": 0.91,
      "source": "semantic+pixel"
    }],
    "avoidRegions": [{
      "id": "face-1",
      "x": 0.42,
      "y": 0.16,
      "width": 0.28,
      "height": 0.34,
      "reason": "protected-subject",
      "confidence": 0.96
    }],
    "referenceTypographyDNA": {
      "hierarchyRatio": [1, 0.28, 0.1],
      "titleSilhouette": "stepped-diagonal",
      "orientation": "horizontal",
      "alignmentAxis": "subject-edge",
      "weightContrast": "high",
      "texture": ["dry-brush"],
      "titleImageRelation": "hinge",
      "negativeSpaceUse": "dense-title-in-calm-zone",
      "forbiddenLiteralDetails": ["reference OCR and exact wordmark"]
    },
    "winnerTypography": {
      "source": "reference | story | default",
      "relation": "crown | anchor | hinge | blade | seal | whisper | weave",
      "titleLines": 2,
      "displayLines": ["exact first line", "exact second line"],
      "titleWidthRatio": 0.82,
      "titleScaleRatio": 0.078,
      "fontFamily": "display",
      "fontWeight": 800,
      "letterSpacing": -0.8,
      "lineHeight": 0.9,
      "textEffect": "ink-edge",
      "align": "left",
      "editable": true,
      "rationale": "story, force-line, and reference reasoning"
    },
    "typographyTournament": {
      "keyArtId": "same-approved-key-art",
      "winnerCandidateId": "story-led",
      "selectionSource": "recommendation | user",
      "candidates": [
        { "id": "reference-led", "plan": {}, "safeRegionId": "safe-bottom", "placements": [], "scores": {} },
        { "id": "story-led", "plan": {}, "safeRegionId": "safe-top", "placements": [], "scores": {} },
        { "id": "wild-card", "plan": {}, "safeRegionId": "safe-right-rail", "placements": [], "scores": {} }
      ]
    },
    "selectedTypography": {
      "candidateId": "story-led",
      "selectionSource": "recommendation | user",
      "safeRegionId": "safe-top",
      "placements": [{
        "id": "poster-title",
        "x": 58,
        "y": 84,
        "width": 604,
        "height": 220,
        "orientation": "horizontal",
        "displayLines": ["exact first line", "exact second line"]
      }]
    }
  },
  "audit": {
    "release": "pass | fail | review",
    "metrics": {
      "storyCoverage": 0,
      "titleHeroAlignment": 0,
      "supportComplementarity": 0,
      "mustShowMinimum": 0,
      "requiredMustShowCount": 0,
      "placedMustShowCount": 0,
      "copyReadability": 0,
      "sourceHeroIntegrity": 0,
      "sourceAssetsRendered": 0,
      "sourceTextCropSafety": 0,
      "copyVisualEntailment": 0,
      "textIntegrity": 0,
      "titleStoryFit": 0,
      "typographicVoiceFit": 0,
      "visualIntegration": 0,
      "thumbnailLegibility": 0,
      "referenceTypographyAlignment": 0,
      "fontAvailability": 0,
      "crossRendererConsistency": 0
    },
    "hardFailures": [],
    "warnings": []
  }
}
```

`narrativeBriefV2.mustShow` is the video-level high-recall catalog. `tournamentCandidate.requiredMustShow` is the frozen concept-level subset (maximum three) that the title and composition promise to display. Resolve each item through the NarrativeBrief `mustShow:<claim>` evidence link; every item must map to an actually placed source frame or traceable derivative. A composer that changes the title/concept must rerun this resolution instead of reusing stale requirements.

Model-authored frame commentary is inferred evidence and must set `independentForExactCopy: false`. Exact numbers, dates, prices, temperatures, and visible text may enter final copy only when at least one independently obtained metadata/OCR/subtitle/speech evidence item supports them. A change claim must link at least two distinct actually placed source frames; `copyVisualEntailment` fails when the final title/subtitle promise a concrete visual theme that their placed frames do not show.

Scores use `0–100`. `confidence` uses `0–1`. Times are seconds from the source video. A producer may add fields, but must not remove stable IDs, evidence linkage, status, rejection reasons, or source/derivation lineage.

## Usage optimization handoff envelope

```json
{
  "schemaVersion": "1.0",
  "generatedAt": "ISO-8601",
  "window": { "from": "YYYY-MM-DD", "to": "YYYY-MM-DD", "days": 30 },
  "metrics": {
    "events": 0,
    "sessions": 0,
    "successRate": 0,
    "fallbackRate": 0,
    "failureRate": 0,
    "durationP50Ms": 0,
    "durationP95Ms": 0
  },
  "dimensions": { "feature": [], "provider": [], "engine": [], "failureCode": [] },
  "funnels": [],
  "opportunities": [
    {
      "rank": 1,
      "feature": "video-poster",
      "problem": "bounded evidence statement",
      "evidence": { "count": 0, "rate": 0 },
      "targetMetric": "poster_generation_completed.successRate",
      "guardrail": "factual audit pass rate must not decrease"
    }
  ],
  "experiments": [],
  "privacy": {
    "containsRawPrompts": false,
    "containsMedia": false,
    "containsDirectIdentifiers": false
  },
  "warnings": []
}
```

Only bounded, privacy-safe fields may enter this envelope. Preserve event meanings across baseline and comparison windows. A small sample must be labeled exploratory; an empty pack must not invent an opportunity. See [usage-optimization.md](usage-optimization.md) for invocation, failures, reuse, and evolution.
