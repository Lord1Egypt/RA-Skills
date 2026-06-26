---
name: skill-docker
description: "skill-docker:interface-01 - Manifest Inspect; skill-docker:interface-02 - Build Init; skill-docker:interface-03 - Build Destroy; skill-docker:interface-04 - Build and Push"
---

## Important Principles ⭐

**Modification Prohibited (Mandatory)**: Any files under `skill-docker`. This skill is maintained via
`openclaw skills update skill-docker`; any alterations will disrupt its normal operation.

## skill-docker:interface-01 - Manifest Inspect

```bash
result=$(DOCKER_IMAGE=<DOCKER_IMAGE> DOCKER_TAGS=(<DOCKER_TAG1> [<DOCKER_TAG2> ...]) bash scripts/docker_manifest_inspect.sh)
```

### Input value

- `DOCKER_IMAGE`: Required, docker image name
- `DOCKER_TAGS`: Required, image tags array (e.g. DOCKER_TAGS=(1.0.0 latest))

### Return value (result)

**Success**: (sample only)

```json
{
  "image": "debian",
  "tags": [
    {
      "tag": "latest",
      "exists": true,
      "archs": {
      }
    },
    {
      "tag": "latest",
      "exists": true,
      "archs": {
        "linux/amd64": {
          "size": 1021,
          "digest": "sha256:2477d9ee0ead4370c778ce3aa42258a0b07684d1a84ded8f4af518383fbc3f2d"
        },
        "linux/arm64/v8": {
          "size": 1041,
          "digest": "sha256:b1e30180b5678df3c17d6b0e659f7107ae4c299506e97427a9373640804db927"
        },
        ...
      }
    }
  ]
}
```

**Error**: (sample only)

- `ERROR: Usage: DOCKER_IMAGE=<DOCKER_IMAGE> DOCKER_TAGS=(<TAG1> [<TAG2> ...]) scripts/docker_manifest_inspect.sh`
- `ERROR: authentication required or image('$DOCKER_IMAGE') not found`

## skill-docker:interface-02 - Build Init

```bash
result=$(DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_BUILD_CONCURRENCY=<DOCKER_BUILD_CONCURRENCY> DOCKER_PRUNE_FIRST=<DOCKER_PRUNE_FIRST> bash scripts/docker_buildx_init.sh)
```

### Input value

- `DOCKER_BUILDER_NAME`: Required, builder name to init (via env)
- `DOCKER_BUILD_CONCURRENCY`: Optional, max parallelism (default: 2)
- `DOCKER_PRUNE_FIRST`: Optional, remove all build cache (including internal/frontend images) (default: false)

### Return value (result)

**Success**: (sample only)

- `SUCCESS: initted`

## skill-docker:interface-03 - Build Destroy

```bash
result=$(DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PRUNE_FIRST=<DOCKER_PRUNE_FIRST> bash scripts/docker_buildx_destroy.sh)
```

### Input value

- `DOCKER_BUILDER_NAME`: Required, builder name to destroy (via env)
- `DOCKER_PRUNE_FIRST`: Optional, remove all build cache (including internal/frontend images) (default: false)

### Return value (result)

**Success**: (sample only)

- `SUCCESS: destroyed`

## skill-docker:interface-04 - Build and Push

### skill-docker:step-0401

If the `DOCKER_BUILDER_NAME` is not provided, ask user with "Confirm to use docker builder 'skilldockerbuilder' ?" to
obtain the value, then assign the value to variable __DOCKER_BUILDER_NAME__ . Then ask user with "Confirm to remove all
build cache (including internal/frontend images) ?", then assign the value to variable __DOCKER_PRUNE_FIRST__

### skill-docker:step-0402

Call `skill-docker:interface-02` to initialize builder with `DOCKER_BUILDER_NAME=variable __DOCKER_BUILDER_NAME__` and
with `DOCKER_PRUNE_FIRST=__DOCKER_PRUNE_FIRST__`.

### skill-docker:step-0403

Run build and push

```bash
result=$(DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_PROVENANCE=<DOCKER_PROVENANCE> DOCKER_SBOM=<DOCKER_SBOM> \
  DOCKER_IMAGE_TAGS=(<IMAGE_TAG1> [<IMAGE_TAG2> ...]) DOCKER_BUILD_ARGS=(<BUILD_ARG1> [<BUILD_ARG2> ...]) bash scripts/docker_buildx_push.sh)
```

#### Input value

- `DOCKER_BUILDER_NAME`: Fixed, via `variable __DOCKER_BUILDER_NAME__`
- `DOCKER_PLATFORM`: Required, target platforms separated by comma (e.g. linux/amd64,linux/arm64)
- `DOCKER_IMAGE_TAGS`: Required, image tags array (e.g. TAGS=(myimage:1.0.0 myimage:latest))
- `DOCKER_BUILD_ARGS`: Optional, build arguments array (e.g. BUILD_ARGS=(BUILD_ARG1=val1 BUILD_ARG2=val2))
- `DOCKER_PROVENANCE`: Optional, enable provenance attestation (default: false)
- `DOCKER_SBOM`: Optional, enable SBOM attestation (default: false)

#### Return value (result)

**Success**: (sample only)

- `SUCCESS: Build and push completed successfully`

**Error**: (sample only)

- `ERROR: DOCKER_BUILDER_NAME is required. 
Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_IMAGE_TAGS=<DOCKER_IMAGE_TAGS> $0`
- `ERROR: DOCKER_PLATFORM is required. 
Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_IMAGE_TAGS=<DOCKER_IMAGE_TAGS> $0`
- `ERROR: At least one tag must be provided via DOCKER_IMAGE_TAGS environment variable. 
Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_IMAGE_TAGS=<DOCKER_IMAGE_TAGS> $0`

### skill-docker:step-0404

Call `skill-docker:interface-03` to destroy builder with `DOCKER_BUILDER_NAME=variable __DOCKER_BUILDER_NAME__` and with
`DOCKER_PRUNE_FIRST=__DOCKER_PRUNE_FIRST__`.

## More skills

https://github.com/lentiancn/skills
