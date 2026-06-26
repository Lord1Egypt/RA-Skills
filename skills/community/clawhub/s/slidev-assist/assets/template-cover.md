---
theme: default
title: 演示标题
fonts:
  sans: Inter
lineNumbers: false
colorSchema: auto
layout: cover
transition: fade
class: text-center
---

# {{ title }}

{{ subtitle }}

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    按空格继续 <carbon:arrow-right class="inline"/>
  </span>
</div>
