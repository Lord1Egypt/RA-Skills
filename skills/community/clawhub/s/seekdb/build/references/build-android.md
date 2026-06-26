# Build SeekDB — Android (cross-compile from macOS or Linux host)

**Supported targets:** Android arm64-v8a.

Before building, complete the dependency check from [build/SKILL.md → Step 2](../SKILL.md#step-2--determine-repo-root) — compile actions require the matching MD5 deps marker (`android.arm64`) to exist.

---

## Environment prerequisites

```bash
export PATH="${ANDROID_HOME:-$HOME/Library/Android/sdk}/platform-tools:$PATH"
export ANDROID_NDK_HOME="${ANDROID_NDK_HOME:-${ANDROID_HOME:-$HOME/Library/Android/sdk}/ndk/27.3.13750724}"
```

---

## Compile modes

| Action | `build.sh` command | Build dir |
|--------|--------------------|-----------|
| `release` | `./build.sh release --android --make -j<N>` | `build_android_release/` |
| `debug`   | `./build.sh debug --android --make -j<N>`   | `build_android_debug/`   |

Artifacts (inside the build dir):
- `src/observer/seekdb`
- `src/observer/embed/libseekdb_embed_c.so`
- `src/observer/embed/embedded_client`

**Incremental make** (fastest for day-to-day iteration; skip dep check — deps already resolved):
```bash
cd $REPO_ROOT/build_android_release && make -j<N>
```

---

## Package — `apk`

`seekdb-apk-build.sh --build` runs `build.sh clean + release --android --init + make`
internally — skip the Step 2 init check when using `--build`:
```bash
cd $REPO_ROOT
./package/apk/seekdb-apk-build.sh --build --apk [--with-jni] [--install] \
    seekdb <VERSION> <RELEASE>
# Artifact: package/apk/seekdb-<VERSION>-<RELEASE>.apk
#
# --build    : clean + android init + make
# --apk      : gradlew assembleDebug, rename and move APK
# --with-jni : also build/sync libseekdb_embed.so
# --install  : adb install -r onto connected device/emulator
```

Script requirements:
- `ANDROID_NDK_HOME` set (default: `$HOME/Library/Android/sdk/ndk/27.3.13750724`)
- JDK 17+ for Gradle (auto-detected from Android Studio JBR if not set)
- `curl` or `wget` (downloads `gradle-wrapper.jar` on first run)

---

## Manual APK steps (alternative to `seekdb-apk-build.sh`)

```bash
# Step A: binary already built by compile step above

# Step B: strip + copy into jniLibs
_prebuilt=$(ls $ANDROID_NDK_HOME/toolchains/llvm/prebuilt/ | head -1)
NDK_STRIP="$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/$_prebuilt/bin/llvm-strip"
$NDK_STRIP -o $REPO_ROOT/build_android_app/app/src/main/jniLibs/arm64-v8a/libseekdb_embed_c.so \
              $REPO_ROOT/build_android_release/src/observer/embed/libseekdb_embed_c.so
$NDK_STRIP -o $REPO_ROOT/build_android_app/app/src/main/jniLibs/arm64-v8a/libembedded_client.so \
              $REPO_ROOT/build_android_release/src/observer/embed/embedded_client

# Step C: build APK
echo "sdk.dir=${ANDROID_HOME:-$HOME/Library/Android/sdk}" > $REPO_ROOT/build_android_app/local.properties
cd $REPO_ROOT/build_android_app && ./gradlew assembleDebug
# Artifact: build_android_app/app/build/outputs/apk/debug/app-debug.apk
```
