# Source and integration index

Links identify external documentation, not installed tools or guaranteed output quality. Check current versions, model/device support, privacy settings, credits and export terms before using a service. Observe the user's local-only preference and obtain their choice before sending a personal image elsewhere.

## Printer and CAD

- [Snapmaker U1](https://wiki.snapmaker.com/en/snapmaker_u1), [U1 FAQ](https://wiki.snapmaker.com/en/FAQ/u1), [Orca quick start](https://wiki.snapmaker.com/en/snapmaker_orca/qsg), [Snapmaker Orca source](https://github.com/Snapmaker/OrcaSlicer): hardware, profiles and supported model formats.
- [Full Spectrum matching](https://wiki.snapmaker.com/en/snapmaker_orca/color_mixing_match_guide): configured spools, achievable colors and matching workflow. See the [skill's color guide](FULL_SPECTRUM.md).
- [SolidCraft](https://solidcraft.io/), [documentation](https://docs.solidcraft.io/): editable parametric solid modeling and integrations; discover the user's actual tool connection before invoking it.
- [Bambu-to-U1](https://github.com/thadius83/bambu-to-snapmaker-u1): separate noncommercial project converter, not an inference engine.

## Optional generation and capture providers

- Tripo: [multiview guidance](https://www.tripo3d.ai/help/features/how-to-use-multi-view-input-effectively), [print preparation](https://www.tripo3d.ai/help/features/how-to-prepare-models-for-3d-printing), [exports](https://www.tripo3d.ai/product-doc/export-and-integration/export-dcc), [Codex integration](https://developers.tripo3d.ai/en/docs/codex-plugin).
- Meshy: [image generation](https://docs.meshy.ai/en/webapp/image-to-3d), [printing workflow](https://docs.meshy.ai/en/webapp/guides/use-cases/3d-printing), [Orca plugin](https://docs.meshy.ai/en/webapp/plugins/orcaslicer/use-the-plugin), [agent integration](https://docs.meshy.ai/en/api/ai). A plugin for upstream Orca does not establish compatibility with Snapmaker's fork.
- Rodin: [Hyper3D API](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5), [official guide](https://hyper3d.ai/help/articles/how-to-use-hyper3d-beginners-guide).
- Polycam: [person capture](https://learn.poly.cam/hc/en-us/articles/28271869062420-How-to-Capture-a-Person), [export formats](https://learn.poly.cam/hc/en-us/articles/27756102599572-What-File-Types-Can-Polycam-Export). An overlapping capture and independent portraits serve different reconstruction methods.
- Open/local models: [TripoSR](https://github.com/VAST-AI-Research/TripoSR), [TripoSG](https://github.com/VAST-AI-Research/TripoSG), [TRELLIS](https://github.com/microsoft/TRELLIS), [Hunyuan3D](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1). Model and encoder licenses/device needs are separate from this skill; a public repository is not proof of Mac compatibility.
- [Apple Object Capture](https://developer.apple.com/documentation/realitykit/capturing-photographs-for-realitykit-object-capture/): observed multi-angle input requirements. Use it for a suitable static capture set, not a synthesized set of angles.

Texture resolution, generation completion and triangle count are not measures of facial identity. Prefer a method appropriate to the input, inspect the full untextured shape, and require separate geometry, color and slicing checks. This index does not rank providers or promise commercial-service parity.
