## Description: <br>
Enforces strict API compliance, memory safety, and idiomatic patterns for Zig 0.16.0, and refuses to generate code for any earlier version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debuggerdragon311](https://clawhub.ai/user/debuggerdragon311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to write, edit, debug, review, and test Zig code that follows Zig 0.16.0 APIs and idioms. It is especially focused on allocator discipline, build files, file I/O, formatting, collections, testing, SIMD, comptime, and C interop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan notes that the main risk is inaccurate sample code rather than install-time behavior, persistence, credential access, or hidden execution. <br>
Mitigation: Compile and test generated Zig code, and pay particular attention to allocator ownership and Zig 0.16 API details before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/debuggerdragon311/zig-pro-maxx) <br>
- [Allocators - Verified API Reference (Zig 0.16.0)](references/allocators.md) <br>
- [build.zig - 0.16.0 build system](references/build-system.md) <br>
- [C interop - @cImport, extern fn, and FFI boundaries](references/c-interop.md) <br>
- [Code Discipline - Zig 0.16.0](references/code-discipline.md) <br>
- [Common Mistakes - Zig 0.16.0](references/common-mistakes.md) <br>
- [comptime - Zig's superpower](references/comptime.md) <br>
- [Error sets, tagged unions, and exhaustive switch](references/error-sets.md) <br>
- [SIMD - @Vector and std.simd](references/simd.md) <br>
- [std Collections - Verified API Reference (Zig 0.16.0)](references/std-collections.md) <br>
- [std.debug - Verified API Reference (Zig 0.16.0)](references/std-debug.md) <br>
- [std.fmt - Verified API Reference (Zig 0.16.0)](references/std-fmt.md) <br>
- [std.Io - Verified API Reference (Zig 0.16.0)](references/std-io.md) <br>
- [std.testing - Verified API Reference (Zig 0.16.0)](references/testing.md) <br>
- [Zig 0.16.0 - Breaking Changes Reference](references/zig-0_16-breaking-changes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Zig code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Zig guidance is constrained to Zig 0.16.0 APIs and should be compiled and reviewed before use.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
