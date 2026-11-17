# Image Generation Reference

Use this file during the generation step.

## The canonical command

This is the only command structure to use. Do not alter it.

```bash
pixr generate -w 1600 -f webp --save-to ~/blog-images --no-stdin \
  "1920x1080 thumbnail on topic \"{TOPIC}\" dont just use text use proper vectors resarch on web and make and all, add more vectors then just text (less text more vectors images and all)"
```

Substitute `{TOPIC}` with the exact topic string. Everything else stays identical.

## Flag reference

| Flag | Value | Reason |
|------|-------|--------|
| `-w 1600` | 1600px width | Standard wide blog thumbnail width |
| `-f webp` | webp format | Best compression for web use |
| `--save-to ~/blog-images` | output dir | Consistent location across all blog posts |
| `--no-stdin` | n/a | Never wait for a prompt on stdin |
| height | auto | `-h` is omitted so aspect ratio is preserved from the 1920x1080 generation |

## Optional additions

Only use these if the user explicitly asks:

- `--prefix <name>` — adds a filename prefix to the output file
- `--model <name>` — use a different model (require the user to specify the exact name; list real ones with `pixr models`)
- `--provider <name>`, `--base-url <url>`, `--api-key-env <ENV_VAR>` — use a different provider
- `--save-to <custom-path>` — override output location

## If the command fails

1. Check the resolved config (source `~/.zshrc` first):
   ```bash
   source ~/.zshrc && pixr config --json
   ```
   `hasApiKey` must be `true`; it reads `PIXR_API_KEY` (or the older `NANO_IMAGE_API_KEY`). Never ask the user to set it; it lives in `~/.zshrc`.
2. If `model` is `null`, list the models and ask the user to pick one (never pick for them):
   ```bash
   pixr models --no-interactive
   pixr model <name>
   ```
3. If the error is `request failed (401/403)`, report it; the key does not match the provider.
4. Retry the generate command after resolving the issue.
5. If it still fails, report the exact error text.

## Never do these

- CRITICAL NON-NEGOTIABLE: never change the prompt text
- CRITICAL NON-NEGOTIABLE: never drop `-w 1600` or `-f webp`
- CRITICAL NON-NEGOTIABLE: never generate without confirming `pixr` is available first
- CRITICAL NON-NEGOTIABLE: never choose a provider or model for the user
