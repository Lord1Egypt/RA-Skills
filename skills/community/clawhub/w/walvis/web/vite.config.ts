import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { TanStackRouterVite } from '@tanstack/router-plugin/vite';
import { localApiPlugin } from './vite-plugin-local-api.js';

export default defineConfig({
  plugins: [
    TanStackRouterVite({
      target: 'react',
      autoCodeSplitting: true,
      routesDirectory: './src/routes',
      generatedRouteTree: './src/routeTree.gen.ts',
    }),
    react(),
    tailwindcss(),
    localApiPlugin(),
  ],
  server: {
    allowedHosts: true,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});
