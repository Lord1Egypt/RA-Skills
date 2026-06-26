# Build SeekDB — macOS

**Supported targets:** macOS arm64 (≥13), macOS x86_64 (≥15).

Before building, complete the dependency check from [build/SKILL.md → Step 2](../SKILL.md#step-2--determine-repo-root) — compile actions require the matching MD5 deps marker to exist.

---

## Compile modes

| Action | `build.sh` command | Build dir | Key flags |
|--------|--------------------|-----------|-----------|
| `release` | `./build.sh release --make -j<N>` | `build_release/` | RelWithDebInfo |
| `debug`   | `./build.sh debug --make -j<N>`   | `build_debug/`   | Debug |
| `perf`    | `./build.sh mac_perf --make -j<N>`| `build_mac_perf/`| RelWithDebInfo + ThinLTO (no FDO/BOLT — macOS limitation) |

Artifact (inside the build dir):
- `src/observer/seekdb`

Verify:
```bash
./build_release/src/observer/seekdb --version
```

---

## Package — `tgz`

macOS does **not** support Thin LTO in the package build configuration (`build.sh tgz`
enables it by default). Call `build.sh` directly from `$REPO_ROOT` with
`-DENABLE_THIN_LTO=OFF` — no need to `cd` into any subdirectory:

```bash
./build.sh tgz \
    -DOB_RELEASEID=<RELEASE> \
    -DBUILD_NUMBER=<RELEASE> \
    -DUSE_LTO_CACHE=ON       \
    -DENABLE_THIN_LTO=OFF    \
    --init --make tgz
# Artifact: build_tgz/seekdb-<VERSION>-<RELEASE>-macos26-arm64.tar.gz
```
