# TRELLIS Mac compatibility notes

The [advanced runner](TRELLIS_RUNNER.md) targets a separately provisioned, compatible Apple Silicon TRELLIS runtime. Microsoft TRELLIS image-large and DINOv2 are distinct from TRELLIS.2/DINOv3; do not infer that one model's access or device support applies to another.

The wrapper pins specific source and model revisions. A stock checkout is insufficient if it lacks the compatible `scripts/run_real_pipeline.py`, runtime metadata and expected environment. This repository does not distribute the patched generation runtime or its weights and does not install them automatically.

## Operational constraints

- Use one fresh process per low-memory job. Completed conditioning/flow stages may release models needed for another invocation.
- Keep normal MPS memory guards. A completed sampling stage does not bound extraction memory or prove the machine can complete a job; process footprint may exceed physical RAM through swapping.
- Saved latent diagnostics are not a supported resume contract.
- Verify cached source, models and DINO files before generation. Hugging Face flags alone do not block all possible downloads; the Python network guard also has the limits documented by the runner.
- Inspect atlas/UV orientation in exported appearance. Record any correction separately and preserve the source; a coherent texture still does not establish printable physical facial detail.
- Recheck the complete form. Better detail in a cropped head can coexist with an inferred hollow or incomplete back.

Generation, complete 360° form, likeness, mesh validity, calibrated color and a reviewed slice are separate results. Do not keep rerunning a rejected candidate without changing the missing input or reconstruction method.

Primary sources: [Microsoft TRELLIS](https://github.com/microsoft/TRELLIS), [public image-large weights](https://huggingface.co/microsoft/TRELLIS-image-large), [Apple Silicon port](https://github.com/vinayapathak/trellis-mac-mps), [DINOv2 model card](https://github.com/facebookresearch/dinov2/blob/main/MODEL_CARD.md).
