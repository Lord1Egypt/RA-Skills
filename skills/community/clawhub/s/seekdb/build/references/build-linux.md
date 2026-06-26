# Build SeekDB — Linux

**Supported targets:** Linux x86_64 on RHEL/CentOS 8 (el8) or 9 (el9).

Before building, complete the dependency check from [build/SKILL.md → Step 2](../SKILL.md#step-2--determine-repo-root) — compile actions require the matching MD5 deps marker to exist.

---

## Compile modes

| Action | `build.sh` command | Build dir | Key flags |
|--------|--------------------|-----------|-----------|
| `release` | `./build.sh release --make -j<N>` | `build_release/` | RelWithDebInfo |
| `debug`   | `./build.sh debug --make -j<N>`   | `build_debug/`   | Debug |
| `perf`    | `./build.sh perf --make -j<N>`    | `build_perf/`    | RelWithDebInfo + ThinLTO + AutoFDO + BOLT |

Artifact (inside the build dir):
- `src/observer/seekdb`

---

## Package — `rpm`

Call `rpm/seekdb-build.sh` directly — it handles clean + init + make internally:
```bash
cd $REPO_ROOT/rpm && bash seekdb-build.sh . seekdb <VERSION> <RELEASE>
# Artifact: $REPO_ROOT/rpm/seekdb-<VERSION>-<RELEASE>.rpm
```

## Package — `deb` (Debian/Ubuntu hosts only)

Call `package/deb/seekdb-build.sh` directly — it handles clean + init + make internally:
```bash
cd $REPO_ROOT/package/deb && bash seekdb-build.sh . seekdb <VERSION> <RELEASE>
# Artifact: $REPO_ROOT/package/deb/seekdb-<VERSION>-<RELEASE>.deb + .ddeb
```
