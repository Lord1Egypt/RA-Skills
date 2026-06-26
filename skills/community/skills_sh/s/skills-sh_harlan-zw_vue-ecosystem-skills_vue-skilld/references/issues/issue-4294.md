---
number: 4294
title: How to import interface for defineProps
type: feature
state: closed
created: 2021-08-10
url: "https://github.com/vuejs/core/issues/4294"
reactions: 155
comments: 153
labels: "[:sparkles: feature request, scope: types, scope: script-setup]"
---

# How to import interface for defineProps

update:
please see:
#7394 

https://github.com/vuejs/core/issues/4294#issuecomment-1316097560

---

### Version
3.2.1

### Reproduction link
https://github.com/Otto-J/vue3-setup-interface-errors/blob/master/src/components/HelloWorld.vue







### Steps to reproduce
clone: git clone 
start: yarn && yarn dev
open: master/src/components/HelloWorld.vue
modify: import interface from './types'

### What is expected?
no error

### What is actually happening?
[@vue/compiler-sfc] type argument passed to defineProps() must be a literal type, or a reference to an interface or literal type.

---
in chinese:
我想把 props的interface抽出去，但是会报错，如果interface组件里定义的就正常渲染
in english:
I want to extract the interface of props, but an error will be reported. If the interface component is defined, it will render normally



---

## Top Comments

**@yyx990803** [maintainer] (+219):

Relevant RFC section

> Currently complex types and type imports from other files are not supported. It is theoretically possible to support type imports in the future.

We'll mark it as an enhancement for the future.

**@languanghao** (+94):

I also find a workaround, just use `defineProps(ComplexType)` instead of `defineProps<ComplexType>`. Even the `ComplexType` is imported from other file, it works fine.

**@cdvillard** (+67):

Despite a fairly similar setup to @phasetri's issue, I'm finding that the properties of the interface I'm trying to import resolve as `attrs` instead of `props`, which breaks what I see as expected and predictable functionality.

Control example:
```vue
<script setup lang="ts">
	interface IThingie {
		serial: string,
		id: string,
		startDate: Date | null,
		endDate: Date | null
	}

	const props = withDefaults(defineProps<IThingie>(),{});
</script>

// In vue-devtools (values from route params)
props
    {
        "id": "123",
        "serial": "asdfa",
        "startDate": null,
        "endDate" null
    }
```...