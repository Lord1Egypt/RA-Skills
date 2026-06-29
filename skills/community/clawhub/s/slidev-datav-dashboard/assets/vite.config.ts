// Merged into Slidev's own Vite config. Docs: https://sli.dev/custom/config-vite
// Purpose: pre-bundle DataV for fast dev, and bundle it for SSR so `slidev build` / `slidev export`
// (which server-render first) don't choke on DataV's ESM or its window/DOM access.
import { defineConfig } from 'vite'

export default defineConfig({
  optimizeDeps: {
    include: ['@kjgl77/datav-vue3'],
  },
  ssr: {
    // Bundle DataV during SSR instead of treating it as external (prevents build/export errors).
    noExternal: ['@kjgl77/datav-vue3'],
  },
})
