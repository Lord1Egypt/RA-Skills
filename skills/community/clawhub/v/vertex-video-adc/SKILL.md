---
name: vertex-video-adc
description: "Generate videos via Google Cloud Vertex AI predictLongRunning (Veo) using Application Default Credentials (ADC)."
homepage: "https://cloud.google.com/vertex-ai"
metadata: {
  "openclaw": {
    "emoji": "🎬",
    "requires": {
      "binaries": ["gcloud", "curl"]
    }
  }
}
---

# Google Cloud Vertex AI Video Generator (ADC)

This skill utilizes the Google Cloud SDK (`gcloud`) and application credentials to call the Google Cloud Vertex AI `predictLongRunning` (Veo) endpoint, generating videos from text prompts or reference images.

## Workflow

1. Configure required environment variables or parameters:
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
   - `GOOGLE_CLOUD_LOCATION` (Optional): Location/region (defaults to `us-central1`).
   - `GOOGLE_CLOUD_MODEL` (Optional): Model name (defaults to `veo-3.1-generate-001`).
2. Construct/save prompt to a local text file.
3. Call the generation script.

## Commands

### Text-to-Video
```bash
python3 {baseDir}/scripts/video_harness.py --prompt-file <prompt_path> --out <output_path>
```

### Image-to-Video
Provide an optional reference image:
```bash
python3 {baseDir}/scripts/video_harness.py --prompt-file <prompt_path> --image <image_path> --out <output_path>
```

### Advanced Usage
- Specify custom project, location, and model:
```bash
python3 {baseDir}/scripts/video_harness.py --prompt-file <prompt_path> --out <output_path> --project <project_id> --location <location> --model <model>
```
- Custom resolution/aspect ratio/duration/audio generation:
```bash
python3 {baseDir}/scripts/video_harness.py --prompt-file <prompt_path> --out <output_path> --aspect-ratio 16:9 --duration 5 --resolution 720p --generate-audio false
```

## Setup & Requirements
- Google Cloud SDK (`gcloud` CLI) installed and available in `$PATH`.
- Active authentication token:
  - Default ADC mode: `gcloud auth application-default login`
  - User-token mode: `gcloud auth login`
- The system must have `curl` installed to issue the API request.
