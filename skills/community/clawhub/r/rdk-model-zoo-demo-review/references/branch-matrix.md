# Branch and Family Matrix

Use this matrix to select likely expectations. The active branch's documentation and closest maintained sibling always take precedence.

## Branches

| Target | Typical runtime artifact | Review focus |
| --- | --- | --- |
| `rdk_model_zoo_mc_rdkx3` | Branch-specific documented artifact | Python-first sample layout; do not require a maintained C++ runtime without branch evidence. |
| `rdk_model_zoo_mc_rdkx5` | `.bin` | X5 paths and commands; do not flag a `.bin` artifact by itself. |
| `rdk_model_zoo_mc_rdks` | `.hbm` for vision, LLM, and VLA | S100/S100P/S600 claims, board-specific defaults, and OE conversion entry points. |

## Known family exceptions

- RDK S speech samples can legitimately use an INT16 `.bin` artifact; verify the family documentation before reporting it.
- A Python-only sample is valid when its own documentation does not claim C++ support.
- Multi-task samples may choose one representative `run.sh` task, but runtime docs must explain every supported task and its defaults.

## Reference-sample selection

Choose the closest maintained sibling by task and runtime before using a generic template:

- Classification: e.g. `mobilenetv1`.
- Detection or YOLO: e.g. `yolov5` or `ultralytics_yolo26`.
- Segmentation, lane, or depth: e.g. `lanenet`.
- Speech: e.g. `kws` or a documented speech sibling.
- New or unusual families: identify a target-branch sibling first; otherwise mark the template comparison as a convention, not a requirement.

Never treat this file as a release matrix. Update it only when a rule is stable across the target branch documentation and maintained samples.
