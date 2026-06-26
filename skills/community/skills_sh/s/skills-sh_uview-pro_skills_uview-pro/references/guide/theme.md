---
name: "theme"
description: ":::tip 说明. Invoke when user needs guidance on theme."
url: "https://uviewpro.cn/zh/guide/theme.html"
triggers: ["theme","主题配置"]
---

# 自定义主题 <BadgeVersion text="0.4.x以下" :show-suffix="false" />

:::tip 说明
本文适用于 uView Pro 版本 0.4.1 以下，仅支持单主题配置等。
:::

<demo-model url="/pages/componentsC/color/index"></demo-model>

uView Pro 目前可以自定主题色，字体颜色，边框颜色等，所有组件内部的样式，都基于同一套主题，比如您修改了`primary`主题色，所有用到了`primary`颜色
的组件都会受影响。

## 教程

1. 可以在打开的颜色拾取器中输入或者选择颜色，再点"确定"按钮即可。
2. 颜色配置完后，在页面底部下载文件，会得到一个名为`uview-pro.theme.scss`和`uview-pro.theme.ts`(可选)的文件。

## 配置 scss 变量

1. 将`uview-pro.theme.scss`文件复制到项目的公共目录(视情况而定)中，再在项目根目录的`uni.scss`中引入即可。
2. 删除`uni.scss`文件中原来引入的`@import 'uview-pro/theme.scss';`(旧的内置主题文件引入语句)。
3. 重新编译项目或者重启编辑器即可生效。

## 配置 ts 变量

1. 将`uview-pro.theme.ts`文件复制到项目的公共目录(视情况而定)中，再在项目根目录的`main.ts`中引入即可，如下：
2. 重新编译项目即可生效。

引入方式：

```ts
import { createSSRApp } from 'vue'
import App from './App.vue'
import theme from '@/common/uview-pro.theme'
import uViewPro from 'uview-pro'

export function createApp() {
  const app = createSSRApp(App)
  // 引入uView Pro 主库，及theme主题
  app.use(uViewPro, { theme })
  return {
    app
  }
}
```

## 如何使用

在 scss 中使用：

```html
<style lang="scss" scoped>
	.title{
		color: $u-type-primary;
	}
</style>

```

在 ts 中使用：

```js
import { ref, onMounted } from 'vue';

const color = ref('');

onMounted(() => {
  color.value = uni.$u.color['primary'];
});
```

两者的主题即可同步！

<theme-generate></theme-generate>
