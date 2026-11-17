# Image to 3D

Read this reference for `3d` requests. Routing and polling rules remain in `SKILL.md`.

Cataloged models are `Hunyuan3D-2`, `Hi3DGen`, and `Step1X-3D`. Task-model availability can depend on the token group and may be verified only when called. A clean image with a transparent or simple background normally gives the most usable geometry.

For Hunyuan3D 2, the catalog validates:

- texture: boolean
- inference steps: 2–50
- octree resolution: 16–400
- guidance scale: 1–20
- format: GLB or STL
- seed: 0–10,000,000

```bash
python3 scripts/showmeai.py 3d --image character.png --format glb --texture --steps 10 --resolution 256
python3 scripts/showmeai.py 3d --query TASK_ID
```

The normal generation command already waits and downloads the result. `--query` is a recovery/compatibility path, not a reason to stop immediately after submission.
