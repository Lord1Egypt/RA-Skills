import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    react({
      // Use React Fast Refresh
      fastRefresh: true,
      // Use automatic JSX runtime (no need to import React)
      jsxRuntime: 'automatic',
      // Babel plugins (if needed)
      babel: {
        plugins: [
          // Add babel plugins here if needed
        ],
      },
    }),

    // Bundle analyzer (only in analyze mode)
    mode === 'analyze' && visualizer({
      filename: './dist/stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
      template: 'treemap', // or 'sunburst', 'network'
    }),
  ].filter(Boolean),

  // Path aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
      '@/utils': path.resolve(__dirname, './src/utils'),
      '@/lib': path.resolve(__dirname, './src/lib'),
      '@/types': path.resolve(__dirname, './src/types'),
      '@/assets': path.resolve(__dirname, './src/assets'),
      '@/features': path.resolve(__dirname, './src/features'),
      '@/pages': path.resolve(__dirname, './src/pages'),
      '@/store': path.resolve(__dirname, './src/store'),
      '@/services': path.resolve(__dirname, './src/services'),
    },
  },

  // Development server
  server: {
    port: 3000,
    open: true, // Auto-open browser
    cors: true,
    // Proxy API requests (if needed)
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },

  // Preview server (for production build testing)
  preview: {
    port: 4173,
    open: true,
  },

  // Build options
  build: {
    // Output directory
    outDir: 'dist',

    // Target modern browsers
    target: 'esnext',

    // Chunk size warning limit (KB)
    chunkSizeWarningLimit: 500,

    // Minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: mode === 'production', // Remove console.log in production
        drop_debugger: true,
        pure_funcs: mode === 'production' ? ['console.log'] : [],
      },
    },

    // Source maps
    sourcemap: mode === 'production' ? false : true,

    // CSS code splitting
    cssCodeSplit: true,

    // Rollup options
    rollupOptions: {
      output: {
        // Manual chunks for better caching
        manualChunks: (id) => {
          // Vendor chunk for React and related libraries
          if (id.includes('node_modules')) {
            // React vendor chunk
            if (id.includes('react') || id.includes('react-dom') || id.includes('react-router-dom')) {
              return 'react-vendor';
            }

            // UI library chunk
            if (id.includes('@radix-ui') || id.includes('@headlessui')) {
              return 'ui-vendor';
            }

            // State management chunk
            if (id.includes('zustand') || id.includes('@reduxjs') || id.includes('react-redux')) {
              return 'state-vendor';
            }

            // Data fetching chunk
            if (id.includes('@tanstack/react-query') || id.includes('axios')) {
              return 'data-vendor';
            }

            // Form libraries chunk
            if (id.includes('react-hook-form') || id.includes('zod')) {
              return 'form-vendor';
            }

            // Other vendor libraries
            return 'vendor';
          }

          // Feature-based chunks (adjust to your features)
          if (id.includes('/src/features/auth')) {
            return 'feature-auth';
          }
          if (id.includes('/src/features/dashboard')) {
            return 'feature-dashboard';
          }
          if (id.includes('/src/features/products')) {
            return 'feature-products';
          }
        },

        // Asset file naming
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          let extType = info[info.length - 1];

          if (/png|jpe?g|svg|gif|tiff|bmp|ico|webp|avif/i.test(extType)) {
            extType = 'images';
          } else if (/woff|woff2|ttf|otf|eot/i.test(extType)) {
            extType = 'fonts';
          } else if (/css/i.test(extType)) {
            extType = 'css';
          }

          return `assets/${extType}/[name]-[hash][extname]`;
        },

        // JS file naming
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',

        // Compact output
        compact: true,
      },
    },

    // Report compressed size
    reportCompressedSize: true,

    // Write bundle to disk
    write: true,
  },

  // Dependency optimization
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      // Add other dependencies to pre-bundle
    ],
    exclude: [
      // Dependencies to exclude from pre-bundling
    ],
  },

  // CSS options
  css: {
    modules: {
      // CSS Modules naming pattern
      generateScopedName: mode === 'production'
        ? '[hash:base64:5]'
        : '[name]__[local]__[hash:base64:5]',
      localsConvention: 'camelCaseOnly',
    },
    preprocessorOptions: {
      scss: {
        // Global SCSS variables/mixins
        additionalData: `@import "@/assets/styles/variables.scss";`,
      },
    },
    devSourcemap: true,
  },

  // JSON handling
  json: {
    stringify: true,
  },

  // ESBuild options
  esbuild: {
    logOverride: { 'this-is-undefined-in-esm': 'silent' },
    // Drop console and debugger in production
    drop: mode === 'production' ? ['console', 'debugger'] : [],
  },

  // Environment variables prefix
  envPrefix: 'VITE_',

  // Base public path
  base: '/',

  // Define global constants
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __BUILD_DATE__: JSON.stringify(new Date().toISOString()),
  },
}));

// Package.json scripts to add:
/*
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "build:analyze": "tsc && vite build --mode analyze",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  }
}
*/

// Installation instructions:
/*
npm install -D rollup-plugin-visualizer

// For TypeScript path aliases to work in dev, also update tsconfig.json:
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/utils/*": ["src/utils/*"],
      "@/lib/*": ["src/lib/*"],
      "@/types/*": ["src/types/*"],
      "@/assets/*": ["src/assets/*"],
      "@/features/*": ["src/features/*"],
      "@/pages/*": ["src/pages/*"],
      "@/store/*": ["src/store/*"],
      "@/services/*": ["src/services/*"]
    }
  }
}
*/
