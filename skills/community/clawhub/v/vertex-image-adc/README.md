# Google Cloud Vertex AI Image Generator (ADC) Skill

Generate high-quality images via Google Cloud's Vertex AI `generateContent` API using Application Default Credentials (ADC).

This skill is designed for [OpenClaw](https://github.com/openclaw/openclaw) as a portable, generic capability.

## Features
- Fully compliant with Google Cloud's official Vertex AI API regional routing requirements.
- Automatically handles regional endpoints (e.g. `us-central1-aiplatform.googleapis.com`) or global endpoints as specified.
- Support for `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` environment variables.
- Outputs clean, standard JSON for seamless integration with automation platforms.

## Installation & Setup

Place this directory in your OpenClaw workspace `skills/` folder:
```text
skills/vertex-image-adc/
```

### Prerequisites
1. Ensure the Google Cloud SDK (`gcloud`) and `curl` are installed and available on your system path.
2. Authenticate application credentials:
   - For `adc` mode (default): `gcloud auth application-default login`
   - For `user-token` mode: `gcloud auth login`

## Usage

### Inline
```bash
python3 scripts/image_harness.py --prompt-file <path_to_prompt> --out <path_to_output>
```

### Advanced Usage
- Specify custom project, location, and model:
```bash
python3 scripts/image_harness.py --prompt-file <path_to_prompt> --out <path_to_output> --project <project_id> --location <location> --model <model>
```

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.
