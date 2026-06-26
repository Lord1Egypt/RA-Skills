# Runtime Policy

## Config-Driven Operation

This pipeline should behave as a **configuration-driven skill**.

The user should be able to supply different config for:
- upstream Seedance
- downstream waoowaoo image
- downstream waoowaoo video
- downstream waoowaoo TTS
- downstream waoowaoo ambience

If required config is missing, the pipeline should stop and enter first-run guidance instead of guessing.

## Single Main Clip First

Default policy:
- choose one main clip
- finish that clip end-to-end
- only then expand to adjacent clips

## Quota Policy

When video quota is limited:
- spend quota on formal tasks, not casual probes
- if probing is required, note clearly that the result is diagnostic
- do not expand to more clips before a main clip is stable

## Formal vs Probe Results

### Probe Result
A probe result is any task created only to test:
- model availability
- quota availability
- route validity
- response semantics

Probe results:
- may be useful as preview
- must not be counted as formal deliverables by default

### Formal Result
A formal result is a task intentionally submitted for the actual target clip and accepted into delivery flow.

## Audio Policy

For short clips:
- narration is primary
- ambience is secondary
- avoid dense music unless explicitly approved

## Reporting Policy

Always distinguish:
- raw clip
- subtitled clip
- subtitle + TTS clip
- final clip
- probe success
- formal success
