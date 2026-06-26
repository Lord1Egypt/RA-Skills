---
name: qr-code-generator
description: Generate QR codes with clean URLs, optional UTM parameters, captions, and print-safe exports. Use for single codes or batch campaign generation.
---

# QR Code Generator

Create QR assets that are safe to print, easy to scan, and explicit about the encoded destination.

## Workflow

1. Validate the target URL and prefer HTTPS.
2. Add UTM parameters only when the campaign needs them.
3. Generate single codes with `scripts/generate_qr.py` or batches with `scripts/batch_generate.py`.
4. Prefer SVG and higher error correction for print uses.

## Guardrails

- Do not generate QR codes for suspicious or deceptive destinations.
- Return the final encoded URL alongside the output files.
- Explain when PNG is fine and when SVG is the better choice.
