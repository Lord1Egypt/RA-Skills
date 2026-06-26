# Image Generation Reference

Use this file during the generation step.

## The canonical command

This is the only command structure to use. Do not alter it.

```bash
nano-img generate -w 1600 -f webp --save-to ~/blog-images \
  "1920x1080 thumbnail on topic \"{TOPIC}\" dont just use text use proper vectors resarch on web and make and all, add more vectors then just text (less text more vectors images and all)"
```

Substitute `{TOPIC}` with the exact topic string. Everything else stays identical.

## Flag reference

| Flag | Value | Reason |
|------|-------|--------|
| `-w 1600` | 1600px width | Standard wide blog thumbnail width |
| `-f webp` | webp format | Best compression for web use |
| `--save-to ~/blog-images` | output dir | Consistent location across all blog posts |
| height | auto | `-h` is omitted so aspect ratio is preserved from the 1920x1080 generation |

## Optional additions

Only use these if the user explicitly asks:

- `--prefix <name>` — adds a filename prefix to the output file
- `--model <name>` — override the default model (require user to specify the exact model name)
- `--save-to <custom-path>` — override output location

## If the command fails

1. Check that `NANO_IMAGE_API_KEY` is set in the environment:
   ```bash
   echo $NANO_IMAGE_API_KEY
   ```
2. If missing, ask the user to set it:
   ```bash
   export NANO_IMAGE_API_KEY=your_gemini_api_key
   ```
3. Check available models and confirm one is set:
   ```bash
   nano-img model
   ```
4. If no model is saved, list and pick one:
   ```bash
   nano-img models
   ```
5. Retry the generate command after resolving the issue.
6. If it still fails, report the exact error text.

## Never do these

- CRITICAL NON-NEGOTIABLE: never change the prompt text
- CRITICAL NON-NEGOTIABLE: never drop `-w 1600` or `-f webp`
- CRITICAL NON-NEGOTIABLE: never generate without confirming `nano-img` is available first
