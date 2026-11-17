---
name: blog-image
description: Generate a 1600px-wide webp blog thumbnail image using the pixr CLI. Use when the user provides a blog topic or blog name and wants a thumbnail image generated and saved to ~/blog-images. Requires the pixr-cli npm package (pixr command).
---

# Blog Image

Use this skill to generate one blog thumbnail per run using the `pixr` CLI (npm package `pixr-cli`, version 0.3.0 or newer).

pixr works with several providers (Gemini, OpenAI-compatible, OpenRouter, fal) and has no built-in model. The provider, model, and API key come from the user's own pixr config. Never pick or change them yourself.

If the user did not provide a topic, ask for one before proceeding.

## Inputs to infer

- `TOPIC`: the subject of the blog post the image is for (e.g. "vector databases", "building a notes app in Rust")
- Optional: `--save-to` path override (default: `~/blog-images/`)
- Optional: `--prefix` for the output filename

## Prerequisite check

Before generating, run these checks in order:

**1. Confirm `pixr` is available:**

```bash
pixr --help
```

If this fails, run:

```bash
npm install -g pixr-cli
```

Then verify again. If still failing, stop and report.

**2. Confirm the API key and model are configured:**

```bash
source ~/.zshrc && pixr config --json
```

Read `hasApiKey`, `provider`, and `model` from the output.

- `hasApiKey` must be `true`. pixr reads `PIXR_API_KEY` (the older `NANO_IMAGE_API_KEY` also works), or the variable named by `apiKeyEnv` in the user's pixr config. These are defined in `~/.zshrc`.
- `model` must not be `null`. pixr has no default model.

CRITICAL NON-NEGOTIABLE: never ask the user to add or set the API key manually. It is already in `~/.zshrc`. Always source it before concluding the key is missing.
If `hasApiKey` is still `false` after sourcing, report the exact output and stop.

If `model` is `null`, list the models for the user's provider and ask the user which one to use. Do not choose one yourself:

```bash
source ~/.zshrc && pixr models --no-interactive
```

Save the model they pick with `pixr model <name>`, then run the config check again.

## Workflow

1. Confirm the topic with the user or infer it from the blog name they provided.
2. Create `~/blog-images/` if it does not exist.
3. Run the generation command using this exact structure (source `~/.zshrc` in the same shell first):

```bash
pixr generate -w 1600 -f webp --save-to ~/blog-images --no-stdin \
  "1920x1080 thumbnail on topic \"{TOPIC}\" dont just use text use proper vectors resarch on web and make and all, add more vectors then just text (less text more vectors images and all)"
```

Replace `{TOPIC}` with the actual topic. Keep the rest of the prompt exactly as written.
Do not paraphrase, shorten, or reword the prompt text. It is battle-tested.

4. Confirm the output file was written to `~/blog-images/`. pixr prints `saved image: <absolute path>`; note that exact path. Warnings are printed as `warning: ...`; report them but they do not fail the run.
5. Update the blog-meta JSON with the image path.
   - Look for a matching JSON file in `~/blog-meta/` whose `blog_path` value corresponds to the same blog.
   - If found, set `thumbnail_path` to the exact absolute path of the generated image file.
   - Write the updated JSON back to the same file. Do not change any other field.
   - If no matching JSON file is found, note it in the completion report but do not fail the run.
6. Report the full output file path.

## Quality bar

- CRITICAL NON-NEGOTIABLE: always use `-w 1600 -f webp`. Never change these flags.
- CRITICAL NON-NEGOTIABLE: always use `--save-to ~/blog-images` unless the user explicitly provides a different path.
- CRITICAL NON-NEGOTIABLE: never modify the prompt text. Use it verbatim with only `{TOPIC}` substituted.
- CRITICAL NON-NEGOTIABLE: do not skip the prerequisite check. If `pixr` is missing, install it first.
- CRITICAL NON-NEGOTIABLE: never choose a provider or model for the user. Use their pixr config; if no model is set, ask them.
- CRITICAL NON-NEGOTIABLE: after a successful generation, always attempt to update the matching `~/blog-meta/*.json` with `thumbnail_path`. Never skip this step.

## Completion report

At the end, report:

- Topic used
- Full `pixr` command run
- Output file path
- Whether the file exists at that path after generation
- Which `~/blog-meta/*.json` file was updated (or that no match was found)
