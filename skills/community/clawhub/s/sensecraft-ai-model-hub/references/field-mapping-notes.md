# Field Mapping Notes

Use this file when the user asks what numeric fields such as `task`, `uniform_type`, or `model_format` mean.

## Rule

Do not hallucinate mappings.

If SenseCraft documentation or the API response does not explicitly define a value, present the raw numeric value and say the semantic label is not yet confirmed.

## Safe language

Good:
- `task=1`
- `uniform_types=[32, 36]`
- `model_format=2`
- “These values can be filtered and grouped, but their human-readable meanings are not confirmed in the available docs.”

Bad:
- “task=1 definitely means object detection” unless documented
- “uniform_type 32 is device X” unless documented
- “model_format 2 means TFLite” unless documented

## Practical fallback

If the user needs a working filter but not a semantic label:
- filter on the raw value
- show example models under that value
- let the user validate the bucket by names/descriptions/downloaded artifacts

## How to become more certain

You may increase confidence only if at least one of these is true:
- official SenseCraft documentation defines the mapping
- model names/descriptions plus repeated examples make the mapping very likely and you clearly label it as inferred, not confirmed
- downloaded artifacts can be inspected and strongly support a format inference

## Recommended phrasing for inferred meanings

Use wording like:
- “likely corresponds to … based on the surrounding model names, but not confirmed by the API docs”
- “appears to group models of this kind, but I would not treat that label as authoritative yet”
