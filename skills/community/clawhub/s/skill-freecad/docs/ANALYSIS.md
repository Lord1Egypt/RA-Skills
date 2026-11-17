# Stress analysis

Read this before using `fem_static`.

Use `fem_static` when the user cares whether a part will hold:
```json
{"op": "fem_static", "target": "Bracket", "material": "aluminium_6061", "fixed": "<X",
 "loads": [{"faces": ">X", "force": "200 N", "direction": [0, 0, -1]}],
 "require": {"min_safety_factor": 2}, "report": "stress.png"}
```
- **Material:** a specific grade with strength data: `steel_s235`, `steel_s355`, `stainless_304`,
  `aluminium_6061`, `aluminium_7075`, `aluminium_5754`, `titanium`, `brass`, `pla`, `petg`, `abs`, `nylon_pa12`.
  Leave `material` out to use the one assigned to the part with the `material` op. Generic materials (`steel`,
  `aluminium`) are refused, because their yield strength depends on the grade: ask the user which grade.
- **Inputs:**
  - Loads need units (`"500 N"`, `"2 kN"`, `"0.5 MPa"`).
  - A force is the total over the selected faces; a pressure pushes into the faces.
- **Results:**
  - Max displacement (mm) and max von Mises stress (MPa), each with its location.
  - Safety factor against yield, and a stress-map PNG.
  - Always check `equilibrium_error`, which should be near 0, and `convergence`.
  - `checks` says whether each check `passed`, `failed` or was `unavailable`/`skipped`. A failed
    equilibrium check is an error. A failed convergence check comes with a `NOT_CONVERGED` or
    `STRESS_CONCENTRATION` warning (below). `NO_EQUILIBRIUM_CHECK` or `NO_CONVERGENCE_CHECK` warnings mean
    the result is unverified. Convergence is `unavailable` when the mesh could not be refined enough to
    compare (`convergence.refined` is false); never report that as converged. In all these cases, say so
    to the user.
- **Warnings:**
  - `STRESS_CONCENTRATION` means the peak sits at a sharp inner corner, where FEM stress is unreliable
    and keeps rising with mesh refinement. Add a fillet there and re-run.
  - `NOT_CONVERGED` means the mesh needs a smaller `mesh_size`.
- **Mesh:** the default element size is about the wall thickness, which suits deflection. For stresses near
  holes, corners and thin sections give a smaller `mesh_size` and check `convergence`.
- **Supports:** the reported peak stress includes the edges of the fixed faces, where a rigid clamp
  over-estimates stress. If `max_stress_at` lies on a fixed face, say so to the user.
- **Limits:**
  - This is a linear estimate (no contact, small deformations). Supports are fixed faces only, and loads are
    forces, and pressures on planar faces: no gravity, moments, bolt preload or bearing loads.
  - Printed plastics are weaker between layers, so treat their safety factors with extra margin, and tell
    the user it is not a certified calculation.
  - It takes seconds to a minute.
