# Vite 配置模板

## 基础配置

```javascript
import { defineConfig } from "vite";
import vue2 from "@vitejs/plugin-vue2";
import { fileURLToPath, URL } from "node:url";
import viteCompression from "vite-plugin-compression";

export default defineConfig({
  base: "/",
  plugins: [
    vue2(),
    viteCompression({
      algorithm: "gzip",
      ext: ".gz",
      threshold: 10240,
      deleteOriginFile: false,
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      vue: "vue/dist/vue.esm.js",
    },
  },
  server: {
    port: 8080,
    open: false,
  },
  optimizeDeps: {
    include: ["vue", "vue-router", "vuex", "element-ui"],
  },
  css: {
    preprocessorOptions: {
      scss: {
        silenceDeprecations: ["legacy-js-api", "import"],
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    cssCodeSplit: true,
    assetsInlineLimit: 4096,
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          "vue-vendor": ["vue", "vue-router", "vuex"],
          "element-ui": ["element-ui"],
          "utils-vendor": ["axios", "lodash", "qs"],
        },
        entryFileNames: "assets/js/[name]-[hash].js",
        chunkFileNames: "assets/js/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            return "assets/css/[name]-[hash][extname]";
          }
          if (/\.(png|jpe?g|gif|svg|webp|ico)$/i.test(assetInfo.name || "")) {
            return "assets/images/[name]-[hash][extname]";
          }
          if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name || "")) {
            return "assets/fonts/[name]-[hash][extname]";
          }
          return "assets/[name]-[hash][extname]";
        },
      },
    },
    commonjsOptions: {
      include: [/node_modules/],
      transformMixedEsModules: true,
    },
    minify: "esbuild",
    esbuildOptions: {
      drop: ["console", "debugger"],
    },
  },
});
```

---

## Webpack/Vite 环境变量兼容

迁移期如果仍会合入 Vue CLI/Webpack 风格代码，可以在 Vite 中自动兼容静态 `process.env.VUE_APP_*` 写法。

```javascript
import { defineConfig, loadEnv } from "vite";

const createProcessEnvDefine = (env) => {
  const define = Object.entries(env).reduce((memo, [key, value]) => {
    if (key.startsWith("VITE_")) {
      memo[`process.env.${key.replace(/^VITE_/, "VUE_APP_")}`] =
        JSON.stringify(value);
    }
    if (key.startsWith("VUE_APP_")) {
      memo[`process.env.${key}`] = JSON.stringify(value);
    }
    return memo;
  }, {});

  if (env.NODE_ENV) {
    define["process.env.NODE_ENV"] = JSON.stringify(env.NODE_ENV);
  }

  return define;
};

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    define: createProcessEnvDefine(env),
  };
});
```

约定：`.env.*` 新增变量优先使用 `VITE_` 前缀；业务新代码优先使用 `import.meta.env.VITE_*`；老代码或并行上线代码允许使用 `process.env.VUE_APP_*`。

不要整体定义 `process.env`，优先定义 `process.env.VUE_APP_XXX` 这种精确 key。该方案只兼容静态访问，不兼容 `process.env[key]` 这类动态访问。

---

## 代理配置

```javascript
server: {
  port: 8080,
  proxy: {
    '/api': {
      target: 'https://api.example.com',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

---

## 可选插件

### JSX 支持

```javascript
import vue2Jsx from "@vitejs/plugin-vue2-jsx";

plugins: [vue2(), vue2Jsx()]
```

### SVG Sprite

```javascript
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'

plugins: [
  vue2(),
  createSvgIconsPlugin({
    iconDirs: [path.resolve(process.cwd(), 'src/icons/svg')],
    symbolId: 'icon-[name]'
  })
]
```

### Legacy 浏览器支持

```javascript
import legacy from '@vitejs/plugin-legacy'

plugins: [
  vue2(),
  legacy({
    targets: ['defaults', 'not IE 11'],
    additionalLegacyPolyfills: ['regenerator-runtime/runtime']
  })
]
```
