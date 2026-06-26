# Planning, State, and Navigation Contract

Version: 1.0.0

## Every TEXT_ONLY reply

Every text reply must contain, in this order:

1. `当前执行计划` near the beginning.
2. The substantive answer.
3. A default recommendation when multiple options/actions exist.
4. `当前状态与产物` immediately before the final section, automatically listing current status and current outputs.
5. `下一步你可以这样问` as the final section.

The status/output section is mandatory for every `TEXT_ONLY` reply. It must not be omitted because the answer is short, corrective, or mostly explanatory.
For generated specialized figure-making skills, the state/footer must also list the full workflow steps and the current position, and every step introduction must mark whether the current/next response is `TEXT_ONLY` or `IMAGE_ONLY`.

## Visible plan requirements

The visible plan must include:

- current workflow code: `S0`, `B1`-`B9`, or `P1`-`P7`;
- current layer: Startup gate / Skill Builder layer / Figure Production layer;
- turn goal;
- compact checklist;
- whether the plan changed.

## Two-layer state requirements

The state footer must never hide whether the assistant is:

- building a specialized figure-making skill; or
- using a generated specialized skill for a concrete target paper figure.

Required builder-layer fields:

- target figure class;
- target specialized skill slug/name;
- corpus and acquisition status;
- corpus coverage status: candidate/accessible/processed/skipped PDF counts, skipped reasons, processing scope, and whether representative pages are only audit aids;
- figure inspection reliability;
- label and multi-label coverage when one paper or figure can support multiple figure classes;
- taxonomy status;
- generated skill status/version;
- test/patch status;
- shortcut/fallback status.

Required production-layer fields:

- active specialized skill;
- target paper material status;
- figure need state;
- reference/sample image status, including per-image attribute preferences when provided;
- visual style and decision board state;
- prompt/generation/review artifacts.
- full production-step list and current position, including the response mode for the current step.

Required output fields:

- outputs produced in the current turn;
- cumulative outputs produced so far;
- output paths, package names, prompt IDs, candidate IDs, image-batch IDs, or artifact names when available;
- pending planned outputs;
- whether the previous `IMAGE_ONLY` image batch has been recorded into state.

## Next-question consistency

The only copyable next-turn prompts may appear in `下一步你可以这样问`. The first item should match the recommended default. Always include:

`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

Older guide-specific prompts that mention `引导skill` should be understood as compatible user input, but new generated skills should prefer `相关skill以及当前状态`.

Every final `下一步你可以这样问` section must include a short session-continuation reminder: the assistant should continue from the active session/history by default, so the user does not need to manually upload or paste state during normal follow-up turns. The first copyable prompt should start with `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：...`. If the reply presents multiple schemes, layouts, styles, prompts, or other visual options, the first/recommended prompt must ask to generate/display multiple candidate images or schematic boards, normally 6, rather than merely asking the user to choose from text. Always include the fallback prompt `请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`. If history is unavailable, truncated, or moved to another conversation, ask for the latest `当前状态与产物` footer as a fallback only.

## Startup gate

The first trigger must be a plan-only turn. It cannot analyze, download, build the specialized skill, construct prompts, generate images, or invoke image generation after the startup text.

If the user's first message asks to generate images immediately, record that request as pending only. The first assistant response is still startup text only and must not include `$imagegen`, a text-to-image API call, image markdown, or any image artifact.

## Stepwise confirmation gate

Generated specialized skills must guide one step at a time. A normal text turn should present the current step, the decision/options for that step, a default recommendation, and the exact confirmation or choice needed to continue. Do not jump from an initial request directly to final prompt, final figure, caption package, or paper text unless the required prior gates are already confirmed in state.

Require explicit user confirmation or choice before major transitions, including startup to B1, locking figure subtype/layout/metaphor/style, approving the final image brief, and starting any image-generation batch.

## Fast-track handling

If the user explicitly asks to skip the builder layer and directly make a figure, record skipped steps and fallback skill/taxonomy. Do not pretend a domain-specific generated skill exists unless it has been produced or provided.


## v1.0.0 response modality invariant

State must include whether the current response is `TEXT_ONLY` or `IMAGE_ONLY`. A text response cannot transition to image generation inside the same assistant response. If image generation is ready, set `generation.awaiting_generation_confirmation` or `generation.next_turn_must_be_image_only`, then stop. The next assistant response may be image-only only after a user request/confirmation.

`IMAGE_ONLY` responses cannot include the status/output footer. The next `TEXT_ONLY` response after an `IMAGE_ONLY` response must record the generated image batch under `当前状态与产物`.

