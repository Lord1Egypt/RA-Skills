---
name: skill-alpine
description: "alpine:interface-01 - Fetch Latest Releases; alpine:interface-02 - Aggregate Latest Version Archs"
---

## Important Principles ⭐

**Modification Prohibited (Mandatory)**: Any files under `skill-alpine`. This skill is maintained via
`openclaw skills update skill-alpine`; any alterations will disrupt its normal operation.

## alpine:interface-01 - Fetch Latest Releases

```bash
latest_releases_json=$(bash scripts/alpine_fetch_latest_releases.sh)
```

### Return value (latest_releases_json=stdout, example only)

```json
[
  {
    "version": "3.23.4",
    "arch": "x86_64",
    "file_url": "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-3.23.4-x86_64.tar.gz"
  },
  {
    "version": "3.23.4",
    "arch": "aarch64",
    "file_url": "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/aarch64/alpine-minirootfs-3.23.4-aarch64.tar.gz"
  }
]
```

## alpine:interface-02 - Aggregate Latest Version Archs

```bash
latest_version_archs_json=$(bash scripts/alpine_aggregate_latest_version_archs.sh)
```

### Return value (latest_version_archs_json=stdout, example only)

```json
[
  {
    "version": "3.23.4",
    "archs": [
      "aarch64",
      "armhf",
      "armv7",
      "loongarch64",
      "ppc64le",
      "riscv64",
      "s390x",
      "x86",
      "x86_64"
    ]
  }
]
```

## More skills

https://github.com/lentiancn/skills
