# Release Notes: memory-crystal v0.7.31

Closes #101

## Dream Weaver protocol is now optional

The dream-weaver-protocol dependency was a `file:` reference to a sibling directory. This worked in the development environment but broke when the installer cloned the repo to build (the sibling doesn't exist in a clone context). The build failed with "Cannot find module 'dream-weaver-protocol'".

The protocol is now an optional dependency with a dynamic import. If dream-weaver-protocol is available (installed locally or linked), Dream Weaver features work normally. If not, crystal operations continue without Dream Weaver. The build succeeds either way.

This is part of a broader fix to make all repos buildable in isolation. The installer (v0.4.67+) now resolves `file:` dependencies from installed extensions before building, so the protocol will be linked automatically when both packages are installed.
