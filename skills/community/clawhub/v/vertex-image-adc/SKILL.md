---
name: vertex-image-adc
description: "Generate images via Google Cloud Vertex AI generateContent using Application Default Credentials (ADC)."
homepage: "https://cloud.google.com/vertex-ai"
metadata: {
  "openclaw": {
    "emoji": "🎨",
    "requires": {
      "binaries": ["gcloud", "curl"]
    },
    "security": {
      "permissions": ["shell", "file-access", "environment-access"],
      "note": "This skill requires shell execution (for gcloud/curl/python) and file access (for prompt/output handling). It uses system temporary storage (/tmp) for debug logs, which are cleared by system management. Users should be aware that sensitive prompt data or API responses may briefly reside in temporary files during the request cycle."
    }
  }
}
---

# Google Cloud Vertex AI Image Generator (ADC)

This skill utilizes the Google Cloud SDK (`gcloud`) and application credentials to call the Google Cloud Vertex AI `generateContent` API, generating images directly using model predictions.

## Security & Privacy Notice
* **Process Execution**: This skill invokes `subprocess` to orchestrate `gcloud` and `curl` for secure API interaction.
* **Privilege & Access**: It requires access to your environment variables (for authentication context) and local file read/write permissions to handle image prompt files and generate the output assets.
* **Debug Artifacts**: For error tracking and development transparency, full API responses may be written to the system-defined temporary directory. These artifacts are local to the machine running the skill.

## Workflow

1. Configure required environment variables or parameters:
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
   - `GOOGLE_CLOUD_LOCATION` (Optional): Location/region (defaults to `global`).
   - `GOOGLE_CLOUD_MODEL` (Optional): Model name (defaults to `gemini-3.1-flash-image-preview`).
2. Construct/save prompt to a local text file.
3. Call the generation script.

## Commands

### Generate Image (Default ADC)
```bash
python3 {baseDir}/scripts/image_harness.py --prompt-file <prompt_path> --out <output_path>
```

### Advanced Usage
- Specify custom project, location, and model:
```bash
python3 {baseDir}/scripts/image_harness.py --prompt-file <prompt_path> --out <output_path> --project <project_id> --location <location> --model <model>
```
- Use user-auth token instead of ADC:
```bash
python3 {baseDir}/scripts/image_harness.py --prompt-file <prompt_path> --out <output_path> --auth-mode user-token
```

## Setup & Requirements
- Google Cloud SDK (`gcloud` CLI) installed and available in `$PATH`.
- Active authentication token:
  - Default ADC mode: `gcloud auth application-default login`
  - User-token mode: `gcloud auth login`
- The system must have `curl` installed to issue the API request.
