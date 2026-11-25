# Portrait and organic image reconstruction

Use this branch for genuine volumetric people, pets and organic objects. See [RESEARCH.md](RESEARCH.md) for documented provider choices. The [local engine](LOCAL_ENGINE.md) can run without a service account after downloading public weights. It is a single-view general-object baseline, not a guaranteed likeness engine. External providers still need a connection and authorization; documenting one does not integrate it.

## Capture and isolate

Confirm head/shoulders bust, visible torso, or whole figure, intended scale, and desired realism. Preserve recognizable proportions and accessories. Remove the photographic background before reconstruction and inspect the mask around hair, ears, eyewear and clothing. A transparent cutout is only preparation; it is not the final mesh.

Prefer real front, side, opposite side and rear images of the same pose, scale and lighting. Request matching photos rather than pretending that generated side/back images provide measured anatomy. Reflective sunglasses obscure the eyes and can be difficult to reconstruct; preserve them as observed unless the user supplies an unobstructed reference and requests a change. A cropped torso does not specify legs.

For likeness where another capture is possible, consider a real photogrammetry/scan workflow. For a one-photo generative candidate, label side/back anatomy as inferred and inspect the result before progressing.

## Generate and inspect

Choose a provider's detailed geometry option rather than a low-poly game-asset mode. Preserve the highest useful source and a textured master. A bigger texture alone does not add printable facial detail. Before final export, inspect actual untextured front, side and three-quarter geometry to ensure the nose, lips, jaw, cheeks, ears and glasses exist physically.

A suitable portrait candidate has:

- Recognizable face proportions relative to the supplied photo, with critical hidden areas disclosed.
- Complete three-dimensional head, neck and requested body region, viewable from front, sides, back and underside.
- No photographic wall, image rectangle, scene floor, or accidental background fragments.
- A closed intended torso cut and stable base where needed.
- Printable connections for eyewear/hair/features at the requested scale.

Present the candidate's turntable or several actual mesh views for the user's acceptance. A watertight but unrecognizable model does not satisfy the visual goal. A 2D AI render is not evidence of a completed mesh. If repair loses detail, revisit the accepted source rather than smoothing until topology passes.

## Prepare the accepted result

Inspect/repair intersections, non-manifold regions, disconnected shells and thickness. Preserve master textures and editable meshes. For a portrait bust, compare upright and tilted orientations, support contact on chin/nose/glasses, visible seam placement, and optional assembly seams. Do not reuse the support-free recommendation of a flat plaque.

Export a geometry copy for checks and a color-preserving master. Verify actual color-region import before Full Spectrum setup; see [FULL_SPECTRUM.md](FULL_SPECTRUM.md). Finish with an actual U1 slice and review, not just a successful model import.
