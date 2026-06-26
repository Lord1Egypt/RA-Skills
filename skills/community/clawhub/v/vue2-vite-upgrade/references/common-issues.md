# 常见问题处理

在升级过程中如果遇到以下错误，按照对应方案处理。

## 目录

- [问题 1：require is not defined](#问题-1require-is-not-defined)
- [问题 2：找不到模块](#问题-2找不到模块cannot-find-module)
- [问题 3：process is not defined](#问题-3process-is-not-defined)
- [问题 4：global is not defined](#问题-4global-is-not-defined)
- [问题 5：图片 require 报错](#问题-5图片-require-报错)
- [问题 6：环境变量判断不生效](#问题-6环境变量判断不生效)
- [问题 7：SCSS :export 不工作](#问题-7scss-export-导出变量不工作)
- [问题 8：JSX 报错](#问题-8vue-文件中使用-jsx-报错)
- [问题 9：HTMLCollection 没有 forEach](#问题-9htmlcollection-没有-foreach-方法)
- [问题 10：导航守卫重定向报错](#问题-10vue-router-导航守卫重定向报错)
- [问题 11：Element-UI 样式丢失](#问题-11element-ui-样式丢失)
- [问题 12：SVG Sprite 图标不显示](#问题-12svg-sprite-图标不显示)
- [问题 13：热更新不生效](#问题-13热更新-hmr-不生效)
- [问题 14：生产构建路径错误](#问题-14生产构建后路径错误)
- [问题 15：path 模块不可用](#问题-15nodejs-path-模块在浏览器不可用)
- [问题 16：axios 安全漏洞](#问题-16axios-版本存在安全漏洞)
- [问题 17：浏览器兼容性](#问题-17浏览器兼容性问题需要支持旧浏览器)
- [问题 18：router.app.$store 为 undefined](#问题-18routerappstore-为-undefined)
- [问题 19：chunk 体积过大](#问题-19构建后-chunk-体积过大警告)
- [问题 20：路由懒加载](#问题-20路由组件未实现懒加载导致主包过大)
- [问题 21：静态资源 404](#问题-21静态资源-404-错误publicdir-配置)
- [问题 22：正则匹配 null](#问题-22正则匹配结果为-null-导致运行时报错)
- [问题 23：动态导入冲突](#问题-23动态导入与静态导入冲突警告)

---

## 问题 1：require is not defined

**原因：** Vite 不支持 CommonJS 的 require 语法

**解决方案：**

1. 将 CommonJS 依赖加入 `vite.config.js` 的 `optimizeDeps.include`
2. 如果是代码中使用了 require，改为 import 语法

---

## 问题 2：找不到模块（Cannot find module）

**原因：** 导入路径缺少 `.vue` 扩展名，或 Vite 默认不自动补全扩展名

**解决方案：**

**方案一：配置 `resolve.extensions`（推荐，批量解决）**

在 `vite.config.js` 中添加：

```javascript
resolve: {
  extensions: ['.js', '.vue', '.json', '.ts'],
  alias: { /* ... */ }
}
```

> 注意：Vite 官方不推荐省略 `.vue` 扩展名，配置此项后仍建议逐步补全扩展名。

**方案二：手动补全扩展名**

```bash
# 搜索所有缺少 .vue 扩展名的导入
grep -rn "from ['\"].*@/.*['\"]" src --include="*.js" --include="*.vue" | grep -v "\.vue"
```

---

## 问题 3：process is not defined

**原因：** 第三方库使用了 Node.js 的 process 对象

**解决方案：** 在 `vite.config.js` 中添加：

```javascript
export default defineConfig({
  define: {
    'process.env': {},
    'process.platform': JSON.stringify(''),
    'process.version': JSON.stringify('')
  }
})
```

---

## 问题 4：global is not defined

**原因：** 代码中使用了 Node.js 的 global 对象

**解决方案：** 全局替换 `global.` 为 `window.`

```bash
find src -type f \( -name "*.js" -o -name "*.vue" \) -exec sed -i '' 's/global\./window./g' {} +
```

---

## 问题 5：图片 require 报错

**原因：** Vite 不支持 require 动态导入图片

**解决方案：**

```javascript
// ❌ 错误
<img :src="require('@/assets/logo.png')" />

// ✅ 方案一：使用 import
import logo from '@/assets/logo.png'
// template 中使用 :src="logo"

// ✅ 方案二：public 目录下的资源直接用绝对路径
<img src="/images/logo.png" />
```

---

## 问题 6：环境变量判断不生效

**原因：** Vite 使用 `import.meta.env` 而非 `process.env`，且只暴露 `VITE_` 前缀变量

**解决方案：**

**情况一：新代码用了 Vite 内置 MODE 变量但不匹配**

```javascript
// ❌ 错误
import.meta.env.MODE === 'testing'  // 永远不匹配

// ✅ 正确：使用自定义的 VITE_RUN_ENV 变量
import.meta.env.VITE_RUN_ENV === 'staging'
```

**情况二：老代码使用 `process.env.VUE_APP_*`，通过配置兼容**

在 `vite.config.js` 中用 `define` 静态替换，无需修改业务代码：

```javascript
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  const define = Object.entries(env).reduce((memo, [key, value]) => {
    if (key.startsWith('VITE_')) {
      memo[`process.env.${key.replace(/^VITE_/, 'VUE_APP_')}`] = JSON.stringify(value)
    }
    if (key.startsWith('VUE_APP_')) {
      memo[`process.env.${key}`] = JSON.stringify(value)
    }
    return memo
  }, {})

  if (env.NODE_ENV) define['process.env.NODE_ENV'] = JSON.stringify(env.NODE_ENV)

  return { define }
})
```

> 此方案只兼容静态访问，不兼容 `process.env[dynamicKey]` 动态访问。

---

## 问题 7：SCSS :export 导出变量不工作

**原因：** Vite 不支持 SCSS 的 :export 语法

**解决方案：** 创建对应的 JS 文件导出变量

```javascript
// src/styles/variables.js
export default {
  menuText: '#101011',
  menuActiveText: '#2255FF',
  menuBg: '#F8F9FB'
}
```

---

## 问题 8：Vue 文件中使用 JSX 报错

**原因：** 缺少 JSX 插件

**解决方案：**

1. 安装插件：`pnpm add -D @vitejs/plugin-vue2-jsx`
2. 在 `vite.config.js` 中添加插件
3. 在 `<script>` 标签添加 `lang="jsx"`

---

## 问题 9：HTMLCollection 没有 forEach 方法

**原因：** Vite 环境没有 polyfill

**解决方案：** 使用 Array.from 转换

```javascript
// ❌ 错误
const children = document.querySelector('.container').children
children.forEach(item => {})

// ✅ 正确
Array.from(children).forEach(item => )
```

---

## 问题 10：Vue Router 导航守卫重定向报错

**原因：** 缺少 replace: true 参数

**解决方案：**

```javascript
// ❌ 可能报错
next({ path: '/' })

// ✅ 正确
next({ path: '/', replace: true })
```

---

## 问题 11：Element-UI 样式丢失

**原因：** 未正确引入 Element-UI 样式

**解决方案：** 在 main.js 中确保正确引入：

```javascript
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)
```

---

## 问题 12：SVG Sprite 图标不显示

**原因：** 原项目使用 `svg-sprite-loader`，需要迁移到 `vite-plugin-svg-icons`

**解决方案：**

1. **安装插件：**

    ```bash
    pnpm add -D vite-plugin-svg-icons
    ```

2. **在 `vite.config.js` 中配置：**

    ```javascript
    import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
    import path from 'path'

    export default defineConfig({
      plugins: [
        vue2(),
        createSvgIconsPlugin({
          iconDirs: [path.resolve(process.cwd(), 'src/icons/svg')],
          symbolId: 'icon-[name]'
        })
      ]
    })
    ```

3. **在 `main.js` 中添加：**

    ```javascript
    import 'virtual:svg-icons-register'
    ```

---

## 问题 13：热更新 HMR 不生效

**原因：** 组件缺少 name 属性

**解决方案：** 确保组件有 name 属性

```javascript
export default {
  name: 'MyComponent',  // 确保有 name
  // ...
}
```

---

## 问题 14：生产构建后路径错误

**原因：** `base` 配置不正确

**解决方案：** 检查 `vite.config.js` 中的 `base` 配置

```javascript
export default defineConfig({
  // 部署在根目录
  base: '/',
  // 部署在子目录
  base: '/admin/',
  // 使用相对路径（推荐用于不确定部署路径的情况）
  base: './'
})
```

---

## 问题 15：Node.js path 模块在浏览器不可用

**原因：** 代码中使用了 Node.js 的 `path` 模块（如 `path.resolve`）

**解决方案：**

1. **安装浏览器兼容版本：**

    ```bash
    pnpm add path-browserify
    ```

2. **在 `vite.config.js` 中配置 alias：**

    ```javascript
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
        vue: "vue/dist/vue.esm.js",
        path: "path-browserify",  // 添加这行
      },
    },
    ```

---

## 问题 16：axios 版本存在安全漏洞

**原因：** 项目继续保留旧的 axios 版本，或迁移文档仍固定推荐已经落后的补丁版本。Vue 2 是否迁移到 Vite，不会改变 axios 的安全风险；需要单独按官方安全公告升级。

**已知漏洞：**

- CVE-2023-45857: XSRF Token 泄露风险（< 1.6.0）
- CVE-2024-39338: 路径解析导致的 SSRF 风险（1.3.2 - 1.7.3）
- CVE-2025-27152: 绝对 URL 可绕过 baseURL，导致 SSRF / 凭据泄露（< 1.8.2）
- CVE-2025-58754: Node 端 `data:` URL 可触发内存型 DoS（< 1.12.0）
- `mergeConfig` 处理 `__proto__` 时可触发 DoS（参考官方 advisory，按最新已修复补丁线处理）

**解决方案：**

1. **升级 axios 到当前 1.x 安全补丁版本：**

    先核对官方 release 和 security advisories，再决定具体补丁号；不要把 skill 写死在某个会过时的版本。

    可以直接写成“升级到当前 1.x 安全补丁版本”，由执行当日再确认具体版本。

2. **说明兼容性边界：**

    - 对 Vue 2 + Vite 迁移场景，axios 与 Vue 主版本没有强绑定，`axios.create()`、请求/响应拦截器、`responseType: 'blob'`、普通上传下载通常可以继续使用。
    - 需要额外排查旧写法：`CancelToken`、`axios.all`、`axios.spread`、`headers.post['Content-Type']`、直接裸用 `axios` 绕过统一封装。
    - 如果项目在 Node 侧会拼接外部 URL，升级后仍要校验 `baseURL` 和入参 URL，不能只依赖版本升级。

3. **修正上传相关旧写法：**

    ```javascript
    // ❌ 旧写法：axios 1.x 下 headers.post 不存在，可能直接报错
    request({
      url: '/upload',
      method: 'post',
      data: formData,
      transformRequest: [(data, headers) => {
        delete headers.post['Content-Type'];
        return data;
      }],
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    ```

    ```javascript
    // ✅ 推荐：直接传 FormData，让 axios / 浏览器自动处理 multipart boundary
    request({
      url: '/upload',
      method: 'post',
      data: formData
    });
    ```

4. **优化 axios 配置文件（如果存在响应拦截器中的 FileReader 异步问题）：**

    ```javascript
    // ✅ 正确：将 FileReader 包装为 Promise
    service.interceptors.response.use((response) => {
      let res = response.data;
      if (res instanceof Blob && res.type === "application/json") {
        return new Promise((resolve, reject) => {
          const file = new FileReader();
          file.readAsText(res, "utf-8");
          file.onload = () => {
            try {
              const jsonRes = JSON.parse(file.result);
              resolve(jsonRes);
            } catch (error) {
              reject(error);
            }
          };
          file.onerror = () => reject(new Error("文件读取失败"));
        });
      }
      return res;
    });
    ```

---

## 问题 17：浏览器兼容性问题（需要支持旧浏览器）

**原因：** Vite 默认只支持现代浏览器

**解决方案：**

1. **安装 legacy 插件：**

    ```bash
    pnpm add -D @vitejs/plugin-legacy terser
    ```

2. **在 `vite.config.js` 中配置：**

    ```javascript
    import legacy from '@vitejs/plugin-legacy'
    
    export default defineConfig({
      plugins: [
        vue2(),
        legacy({
          targets: ['defaults', 'not IE 11'],
          additionalLegacyPolyfills: ['regenerator-runtime/runtime']
        })
      ]
    })
    ```

---

## 问题 18：router.app.$store 为 undefined

**原因：** 在 Vite 环境下，`router.app` 在初始导航时可能尚未设置

**错误示例：**

```text
TypeError: Cannot read properties of undefined (reading 'dispatch')
```

**解决方案：** 直接使用导入的 store 模块

```javascript
// ❌ 错误
router.app.$store.dispatch('setBreadcurmbItems', breadCrumbItems);

// ✅ 正确
import store from '../store/index';
store.dispatch('setBreadcurmbItems', breadCrumbItems);
```

---

## 问题 19：构建后 chunk 体积过大警告

**原因：** 构建后某些 chunk 超过 1000 kB

**解决方案：**

1. **扩展 manualChunks 配置：**

    ```javascript
    manualChunks: {
        'element-ui': ['element-ui'],
        'vue-vendor': ['vue', 'vue-router', 'vuex'],
        'utils': ['axios', 'moment', 'qs'],
    },
    ```

2. **实现路由懒加载**（见问题 20）

3. **调整警告阈值：**

    ```javascript
    build: {
        chunkSizeWarningLimit: 1500,
    }
    ```

---

## 问题 20：路由组件未实现懒加载导致主包过大

**原因：** 使用 `import.meta.glob` 时设置了 `eager: true`

**解决方案：**

1. **移除 eager: true：**

    ```javascript
    // ✅ 正确：懒加载模式
    const viewModules = import.meta.glob('@/views/*/index.vue')
    ```

2. **排除静态导入的组件：**

    ```javascript
    const viewModules = import.meta.glob([
        '@/views/*/index.vue',
        '!@/views/login/index.vue'  // 排除 login
    ])
    ```

---

## 问题 21：静态资源 404 错误（publicDir 配置）

**原因：** Vite 默认使用 `public` 作为静态资源目录

**解决方案：**

1. **配置 publicDir：**

    ```javascript
    export default defineConfig({
        publicDir: 'static',
    })
    ```

2. **修改引用路径（去掉 /static 前缀）：**

    ```html
    <!-- 修改前 -->
    <script src="/static/ckeditor/ckeditor.js"></script>
    
    <!-- 修改后 -->
    <script src="/ckeditor/ckeditor.js"></script>
    ```

---

## 问题 22：正则匹配结果为 null 导致运行时报错

**原因：** 正则匹配未对 null 结果进行检查

**解决方案：** 添加空值检查

```javascript
// ✅ 正确：先检查匹配结果
const match = location.hostname.match(/([a-zA-Z0-9]+\.com)/g)
if (match) {
    this.domain = match[0]
}
```

---

## 问题 23：动态导入与静态导入冲突警告

**原因：** 同一个文件既被静态导入又被 `import.meta.glob` 动态导入

**解决方案：** 在 glob 模式中排除已静态导入的组件

```javascript
// ✅ 正确：使用否定模式排除
const viewModules = import.meta.glob([
    "@/views/*/index.vue",
    "!@/views/login/index.vue"
]);
```
