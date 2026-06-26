# LDM OS v0.4.12

Two critical fixes from dogfood:

1. Deploy aborts if build fails or dist/ is missing. Prevents overwriting working extensions with unbuilt clones. Memory Crystal was broken today by this. Closes #69.

2. wip-install --version exits immediately. Was triggering a recursive spawn loop (detectCLIBinaries -> wip-install --version -> ldm install -> npm checks -> more processes). Machine was grinding to a halt with 200+ zombie processes. Closes #70.

## Issues closed

- Closes #69
- Closes #70
