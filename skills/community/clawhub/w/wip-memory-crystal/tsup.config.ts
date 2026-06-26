import { defineConfig } from 'tsup';

// Bundle dream-weaver-protocol into every entrypoint so the published npm package
// does not need to resolve the `file:../dream-weaver-protocol-private` dev-only
// path at install/runtime. Without this, `crystal status` (and any entrypoint
// that imports from src/dream-weaver.ts) throws
// `ERR_MODULE_NOT_FOUND: Cannot find package 'dream-weaver-protocol'`
// on strict ESM resolvers like Node 25.6+.
export default defineConfig({
  noExternal: ['dream-weaver-protocol'],
});
