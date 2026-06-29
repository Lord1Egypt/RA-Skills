---
name: "object"
description: "对象操作 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 对象操作 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/object.html"
---

---

### [#](#对象操作) 对象操作

注意

由于JS对象包括的范围非常广，加上ES6又有众多的新特性，很难、也没必要做到囊括所有的类型和情况，这里说的"对象"，指的是普通的对象，不包括修改对象原型链， 或者为"Function"，"Promise"等的情况，请留意。

### [#](#对象深度克隆) 对象深度克隆

场景：

-   我们平时可能会遇到需要通过`console.log`打印一个对象，至执行打印的时刻，此对象为空，后面的逻辑中对此对象进行了修改赋值，但是我们在控制台直接看到的打印结果 却是修改后的值，这让人匪夷所思，虽然我们可以通过`console.log(JSON.parse(JSON.stringify(object)))`的形式处理，但是需要写这长长的一串，难免让人心生抵触。

-   当我们将一个对象(变量A)赋值给另一个变量(变量B)时，修改变量B，因为对象引用的特性，导致A也同时被修改，所以有时候我们需要将A克隆给B，这样修改B的时候，就不会 导致A也被修改。

### [#](#deepclone-object) deepClone(object = {})

-   `object` <Object> 需要被克隆的对象

```
let a = {
	name: 'mary'
};

let b = a;

b.name = 'juli';
console.log(b);
console.log(a);

let b = uni.$u.deepClone(a);

b.name = 'juli';
console.log(b);
console.log(a);
```

### [#](#对象深度合并) 对象深度合并

在ES6中，我们可以很方便的使用`Object.assign`进行对象合并，但这只是浅层的合并，如果对象的属性为数组或者对象的时候，会导致属性内部的值丢失。

**注意：** 此处合并不同于`Object.assign`，因为`Object.assign(a, b)`会修改`a`的值为最终的结果(这往往不是我们所期望的)，但是`deepMerge(a, b)`并不会修改`a`的值。

### [#](#deepmerge-target-source) deepMerge(target = {}, source = {})

-   `target` <Object> 目标对象
-   `source` <Object> 源对象

`Object.assign`浅合并示例：

```
let a = {
	info: {
		name: 'mary'
	}
}

let b = {
	info: {
		age: '22'
	}
}

let c = Object.assign(a, b);

c = {
	info: {
		name: 'mary',
		age: '22'
	}
}

c = {
	info: {
		age: '22'
	}
}
```

深度合并示例：

```
let a = {
	info: {
		name: 'mary'
	}
}

let b = {
	info: {
		age: '22'
	}
}

let c = uni.$u.deepMerge(a, b);

c = {
	info: {
		age: '22',
		name: 'mary'
	}
}
```

### [#](#链式读取对象属性) 链式读取对象属性

读取属性时，我们需要从一个`对象`中进行操作，否则就会引起报错，因此uView提供了一个链式属性的读取方式。
当然，我们也可以使用`可选链操作符`的形式去获取，但是此方式在`Vue2`的`template`中不适用。

### [#](#getproperty-object-key) getProperty(object, key)

```

const object = {
	userInfo: {
		address: {
			province: '深圳'
		}
	}
}

uni.$u.getProperty(object, 'userInfo.address.province')

console.log(object?.userInfo?.address?.province)
```

### [#](#链式设置对象属性) 链式设置对象属性

设置属性时，我们需要从一个`对象`中进行操作，否则就会引起报错，因此uView提供了一个链式属性的设置方式。

```

const object = {}

uni.$u.setProperty(object, 'userInfo.address.province')

{
	userInfo: {
		address: {
			province: '深圳'
		}
	}
}
```

← [节流防抖](https://www.uviewui.com/js/debounce.html) [时间格式化](https://www.uviewui.com/js/time.html) →


