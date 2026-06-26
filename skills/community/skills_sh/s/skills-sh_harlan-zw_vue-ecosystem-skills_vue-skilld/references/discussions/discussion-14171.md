---
number: 14171
title: 全局属性怎么在setup中使用
category: Help/Questions
created: 2025-12-05
url: "https://github.com/orgs/vuejs/discussions/14171"
upvotes: 1
comments: 1
answered: true
---

# 全局属性怎么在setup中使用

app.config.globalProperties.msg = 'hello'
export default {
  mounted() {
    console.log(this.msg) // 'hello'
  }
}
怎么在中使用这个全局变量，感觉组件式没有特别好在script 中获取全局变量的便捷模式，这个全局变量在template的说能够使用的，只能用window.msg在main.js进行注册使用吗？

---

## Accepted Answer

**@baiwusanyu-c** [maintainer]:

```
<script setup>
import { ref, getCurrentInstance } from 'vue'
const instance = getCurrentInstance()
console.log(instance.appContext.config.globalProperties)
const msg = ref('Hello World!')
</script>

<template>
  <h1>{{ msg }}</h1>
  <input v-model="msg" />
</template>
```