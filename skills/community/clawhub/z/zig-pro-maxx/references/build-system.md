# build.zig — 0.16.0 build system

---

## Minimal executable build.zig

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target   = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target   = target,
            .optimize = optimize,
        }),
    });
    b.installArtifact(exe);

    // `zig build run` support:
    const run = b.addRunArtifact(exe);
    run.step.dependOn(b.getInstallStep());
    if (b.args) |args| run.addArgs(args);
    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run.step);
}
```

---

## Adding a test step

```zig
const unit_tests = b.addTest(.{
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target   = target,
        .optimize = optimize,
    }),
});
const run_tests = b.addRunArtifact(unit_tests);

const test_step = b.step("test", "Run unit tests");
test_step.dependOn(&run_tests.step);
```

Run with: `zig build test`

---

## Library build.zig

```zig
pub fn build(b: *std.Build) void {
    const target   = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Static library:
    const lib = b.addLibrary(.{
        .name    = "mylib",
        .linkage = .static,
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/lib.zig"),
            .target   = target,
            .optimize = optimize,
        }),
    });
    b.installArtifact(lib);

    // Install public header if exposing a C API:
    b.installFile("include/mylib.h", "include/mylib.h");
}
```

---

## Cross-compilation

Zig can cross-compile to any supported target without installing extra toolchains.

### From the command line

```sh
# Build for Linux ARM64 from any host:
zig build -Dtarget=aarch64-linux-gnu -Doptimize=ReleaseFast

# Build for Windows x86_64:
zig build -Dtarget=x86_64-windows-gnu

# Build for WebAssembly:
zig build -Dtarget=wasm32-freestanding -Doptimize=ReleaseSmall

# Build for macOS ARM (Apple Silicon):
zig build -Dtarget=aarch64-macos
```

`standardTargetOptions` + `standardOptimizeOption` in `build.zig` are what
make `-Dtarget` and `-Doptimize` available on the command line.

### Available optimize modes

| Flag | Mode | Use case |
|---|---|---|
| (none) | `Debug` | Development; full safety checks |
| `-Doptimize=ReleaseSafe` | `ReleaseSafe` | Production + safety checks |
| `-Doptimize=ReleaseFast` | `ReleaseFast` | Max performance, no safety |
| `-Doptimize=ReleaseSmall` | `ReleaseSmall` | Minimal binary size |

### Common target triples

| Target | Triple |
|---|---|
| Linux x86_64 (glibc) | `x86_64-linux-gnu` |
| Linux x86_64 (musl) | `x86_64-linux-musl` |
| Linux ARM64 | `aarch64-linux-gnu` |
| Windows x86_64 | `x86_64-windows-gnu` |
| macOS ARM64 | `aarch64-macos` |
| macOS x86_64 | `x86_64-macos` |
| WASM freestanding | `wasm32-freestanding` |

---

## Specifying a CPU model

```sh
# Target a specific CPU for better code generation:
zig build -Dtarget=x86_64-linux -Dcpu=znver3
zig build -Dtarget=aarch64-linux -Dcpu=apple_a14
```

---

## Linking C libraries

```zig
exe.linkLibC();                         // libc (required for @cImport)
exe.linkSystemLibrary("ssl");           // libssl from the system
exe.linkSystemLibrary("z");             // libz (zlib)

// Static link a local .a file:
exe.addObjectFile(b.path("libs/libfoo.a"));
```

---

## Adding a module (reusable across executables/tests)

```zig
const utils_mod = b.createModule(.{
    .root_source_file = b.path("src/utils.zig"),
    .target   = target,
    .optimize = optimize,
});

const exe_mod = b.createModule(.{
    .root_source_file = b.path("src/main.zig"),
    .target   = target,
    .optimize = optimize,
    .imports  = &.{
        .{ .name = "utils", .module = utils_mod },
    },
});
```

In `src/main.zig`:

```zig
const utils = @import("utils");
```

---

## Build options (passing values from build to source)

```zig
// In build.zig:
const opts = b.addOptions();
opts.addOption(bool, "enable_logging", b.option(bool, "log", "Enable logging") orelse false);
exe_mod.addImport("build_options", opts.createModule());

// In src/main.zig:
const opts = @import("build_options");
if (opts.enable_logging) std.log.info("logging on", .{});
```

---

## Useful `zig build` flags

```sh
zig build                 # default install step
zig build test            # run test step
zig build run             # run the app
zig build -Doptimize=ReleaseFast
zig build --summary all   # print build graph summary
zig build --verbose       # show all commands
zig build clean           # remove zig-out/ and .zig-cache/
```
