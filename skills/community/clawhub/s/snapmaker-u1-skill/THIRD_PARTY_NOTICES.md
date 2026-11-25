# Third-party components

The MIT license in this repository covers its original skill instructions, helper code and CAD example. It does not relicense downloaded source, dependencies, model weights, datasets, generated third-party assets or external applications. No such runtime or weight bundle is included in this repository or its source release.

| Optional component | Source and attribution | Notes |
|---|---|---|
| Snapmaker Orca | [Snapmaker/OrcaSlicer](https://github.com/Snapmaker/OrcaSlicer) | Separate application and profiles; retain upstream licenses. No printer G-code or user calibration project is distributed here. |
| U1 toolkit reference | [bbolinger/snapmaker-u1-toolkit](https://github.com/bbolinger/snapmaker-u1-toolkit/tree/c66284ce990fa71ccf969cae517fbd3b0c780450) | Feature-colored toolpath review inspiration; no upstream runtime or printer-control code is bundled. MIT, copyright 2026 Brent Bolinger; [notice retained](references/licenses/snapmaker-u1-toolkit-MIT.txt). |
| U1 printer-query references | [Snapmaker/u1-klipper](https://github.com/Snapmaker/u1-klipper), [lucakaufmann/snapmaker v1.0.0](https://clawhub.ai/lucakaufmann/skills/snapmaker) | References for U1 filament objects and decoded field schemas. The read-only helper is an original implementation using documented Moonraker APIs; no upstream source, control commands or runtime is bundled. |
| Bambu-to-U1 backend | [thadius83/bambu-to-snapmaker-u1](https://github.com/thadius83/bambu-to-snapmaker-u1) | PolyForm Noncommercial 1.0.0 at the pinned revision. The wrapper does not make that backend commercially permissive. |
| TripoSR code | [VAST-AI-Research/TripoSR](https://github.com/VAST-AI-Research/TripoSR) | MIT; copyright Tripo AI & Stability AI. Weights are obtained separately from [stabilityai/TripoSR](https://huggingface.co/stabilityai/TripoSR). |
| Modly | [lightningpixel/modly](https://github.com/lightningpixel/modly) | MIT; copyright Lightning Pixel. Extensions and models have separate terms. |
| TripoSG | [VAST-AI-Research/TripoSG](https://github.com/VAST-AI-Research/TripoSG), [weights](https://huggingface.co/VAST-AI/TripoSG) | Separately installed model; check its current license and the Modly extension's terms. |
| TRELLIS / Apple Silicon port | [Microsoft TRELLIS](https://github.com/microsoft/TRELLIS), [trellis-mac-mps](https://github.com/vinayapathak/trellis-mac-mps) | Advanced separately provisioned runtime and weights, not a bundled installer. |
| DINO models | [DINOv2](https://github.com/facebookresearch/dinov2), applicable model cards | Encoder terms are separate from reconstruction model terms. |
| Segmentation models | [rembg](https://github.com/danielgatis/rembg) and selected weight provider | A rembg package license does not automatically cover every optional model weight. |
| Apple frameworks | [Vision](https://developer.apple.com/documentation/vision), [RealityKit](https://developer.apple.com/documentation/realitykit), [Foundation Models](https://developer.apple.com/documentation/foundationmodels) | OS/SDK components subject to Apple's terms; framework binaries are not redistributed. |
| Python geometry libraries | NumPy, SciPy, trimesh, Matplotlib, Pillow, Manifold | Installed separately using requirements files; retain their upstream notices. |

Review current model/provider terms before downloading or using assets, especially for commercial use. Public reference datasets and personal photos used during development are not part of this distribution.
