# Native 3D keyframes

Use these tools for editable 3D model, camera, and outer-canvas animation. Never write raw `threeDLayerData` and never claim custom keyframes are unavailable until the named semantic tool returns a concrete error.

Start by calling `mcp_editor__list_tools` with:

```json
{
  "domain": "3d",
  "query": "keyframe animation sequence",
  "includeSchemas": true,
  "limit": 30
}
```

Then pass the selected underlying tool name and validated arguments to `mcp_editor__call_read_tool` or `mcp_editor__call_tool`.

## Complete tool lifecycle

| Intent | Tool |
| --- | --- |
| Read ordered keys and stable IDs | `list_3d_keyframes` |
| Write a complete multi-point animation atomically | `set_3d_keyframe_sequence` |
| Create one point | `create_3d_keyframe` |
| Change values or move one point by ID | `update_3d_keyframe` |
| Copy an exact state to end a hold | `duplicate_3d_keyframe` |
| Delete one point | `delete_3d_keyframe` |
| Remove all editable points | `clear_3d_keyframes` |
| Add a reviewed preset without deleting keys | `append_3d_animation_preset` |
| Explicitly replace all keys with a preset | `apply_3d_animation_preset` |
| Verify exact requested state | `verify_3d_layer_setup` |

For any request containing two or more custom points, prefer `set_3d_keyframe_sequence`. It saves the complete animation in one project mutation and avoids partial states when a later call fails.

## Coordinate contract

- Every tool time is an absolute project time in seconds.
- Model position and camera position/target use model-specific GLB units.
- Model scale is `[x, y, z]` in model space.
- `modelRotationDegrees` is `[x, y, z]` in degrees.
- Canvas X/Y/width/height are composition percentages.
- Canvas rotation is degrees, opacity is 0 to 1, and corner radius is pixels.
- Stored radians are internal and must not be supplied to MCP tools.

## Axis meaning

- X rotation pitches the model up or down.
- Y rotation turns the model left/right and normally reveals the opposite physical face.
- Z rotation rolls the model in the image plane.
- Do not move a camera linearly from positive Z through its target to negative Z. That crosses the model.
- For a front-to-back device reveal, keep the camera in front and rotate model Y by 180 degrees unless the creator explicitly requests another path.

## Holds and interpolation

The easing stored on a keyframe controls the transition from that keyframe to the next keyframe. Two points with identical states create a hold.

For a 10-second animation with two-second opening and closing holds:

1. Write the opening state at 0s.
2. Repeat the opening state at 2s.
3. Write the ending state at 8s.
4. Repeat the ending state at 10s.

With `set_3d_keyframe_sequence`, omitted values inherit from the closest preceding state. Therefore the 2s and 10s hold points can omit transforms when the preceding state is exactly the desired hold state.

## Atomic sequence example

This example uses no screen-content assumptions. Read the model's base state first and preserve every unspecified value.

```json
{
  "itemId": "<exact 3D item ID>",
  "mode": "replace",
  "loop": false,
  "points": [
    {
      "timeSeconds": 0,
      "easing": "linear",
      "modelRotationDegrees": [0, 0, 0]
    },
    {
      "timeSeconds": 2,
      "easing": "ease-in-out"
    },
    {
      "timeSeconds": 8,
      "easing": "linear",
      "modelRotationDegrees": [0, 180, 0]
    },
    {
      "timeSeconds": 10,
      "easing": "linear"
    }
  ]
}
```

Use `mode: "replace"` only for a newly created layer or when the creator explicitly requested a complete animation reset. Use `mode: "merge"` for additions to an existing animation.

## Individual editing

1. Call `list_3d_keyframes` and retain the exact keyframe ID.
2. Call `update_3d_keyframe` to move its absolute time or change only requested values.
3. Use `duplicate_3d_keyframe` when the intended state must remain identical.
4. Use `delete_3d_keyframe` for one point.
5. Use `clear_3d_keyframes` only when every editable point should be removed.

Never identify a keyframe only by visual order after edits. Stable IDs are authoritative.

## Required verification

After writing animation:

1. Call `list_3d_keyframes`.
2. Confirm every requested absolute time exists.
3. Confirm the requested transform values and easing exist.
4. Call `verify_3d_layer_setup` with every expected keyframe time plus model, timing, screen binding, appearance, lighting, and background requirements.
5. Require `passed: true`.
6. Call `view_current_frame` at each hold and transition midpoint.
7. Do not update the director brief or report completion when requested keys are missing.

Project schema validation alone is not visual or animation validation.

## Failure handling

- If a point is outside the layer range, correct the layer timing or requested point before retrying.
- If a point collides with an existing time, update that stable keyframe ID or use sequence merge behavior.
- If a model swap changes scale or camera framing, inspect and retarget relative motion before reporting success.
- If a semantic tool is absent from the callable inventory, report the exact missing tool name. Do not use `update_editor_state` as a raw keyframe fallback.
- If a tool returns an error, report that exact error after attempting the tool. Never infer unsupported capability from an empty keyframe list.
