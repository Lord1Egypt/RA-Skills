# Form 表单


## 组件概况

Form 表单组件用于对表单输入内容进行校验和提交管理。该组件由 `wd-form`（表单容器）和 `wd-form-item`（表单项）两个子组件组成。`wd-form` 负责表单数据绑定、校验规则管理和错误提示分发，`wd-form-item` 基于 Cell 单元格组件封装，用于承载具体的表单域并展示校验错误信息。该组件支持必填校验、正则校验、自定义函数校验和异步校验等多种校验方式，可灵活搭配 Input、Select、Picker、Upload 等各类表单组件使用。

## 核心功能描述

- **数据绑定**：通过 `model` 属性绑定表单数据对象，统一管理表单字段的值
- **校验规则管理**：支持在 `wd-form` 上统一配置 `rules`，也可在表单子组件（如 `wd-input`）上单独配置 `rules`，两者自动合并
- **多种校验方式**：
  - **必填校验**：通过 `required: true` 进行非空校验
  - **正则校验**：通过 `pattern` 属性进行正则表达式匹配
  - **函数校验**：通过 `validator` 函数进行自定义逻辑校验
  - **异步校验**：`validator` 函数返回 Promise 实现异步校验（如接口验证）
- **错误提示方式**：支持 `toast`（弹窗提示）、`message`（表单项下方文字提示）、`none`（不提示）三种错误展示方式
- **字段校验**：`validate` 方法支持传入指定字段名（字符串或数组），仅校验指定字段
- **动态表单**：支持动态增减表单项，`prop` 支持嵌套路径写法（如 `phoneNumbers.0.value`）
- **失焦校验**：配合表单子组件的 `@blur` 事件，在输入框失焦时触发单个字段校验
- **自动重置**：`reset-on-change` 控制表单数据变化时是否自动清除错误信息
- **自定义样式**：支持 `custom-class` 和 `custom-style` 属性进行样式定制

## 适用业务场景

- **用户注册与登录**：表单提交前的字段必填、格式校验（手机号、邮箱、密码强度等）
- **信息填写**：优惠券创建、活动配置、地址管理等复杂表单场景
- **动态表单**：需要动态添加/删除输入项的场景，如多联系人信息、多商品规格
- **分步表单**：每一步提交前对当前步骤的指定字段进行校验
- **数据录入系统**：后台管理系统中各类数据的新增、编辑表单

## API

### wd-form Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| model | Record\<string, any\> | - | 是 | 表单数据对象，键名为字段名，键值为字段值 |
| rules | FormRules | {} | 否 | 表单验证规则，键名为字段名，值为校验规则数组 |
| resetOnChange | boolean | true | 否 | 是否在输入时（model 变化时）重置表单校验信息 |
| errorType | string | 'message' | 否 | 错误提示类型，可选值：`toast`（弹窗提示）、`message`（文字提示）、`none`（不提示） |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-form-item Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| prop | string | - | 是 | 表单域模型字段名，用于关联校验规则和错误信息展示 |
| rules | FormItemRule[] | [] | 否 | 表单域校验规则，会与 wd-form 上的 rules 合并 |
| required | boolean | false | 否 | 是否显示必填星号标识 |
| center | boolean | false | 否 | 是否居中对齐 |
| label | string | '' | 否 | 标签文本 |
| labelWidth | string | '100px' | 否 | 标签宽度 |
| isLink | boolean | false | 否 | 是否显示为链接样式 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-form Methods

通过 ref 可以获取 `wd-form` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| validate | prop?: string / string[] | Promise\<{ valid: boolean; errors: ErrorMessage[] }\> | 表单校验方法。不传参时校验全部字段；传入字符串时校验指定字段；传入字符串数组时校验指定字段集合 |
| reset | 无 | void | 重置表单项的验证提示信息，清除所有错误状态 |

### wd-form Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 表单内容区域，用于放置表单子组件（如 wd-input、wd-picker 等）或 wd-form-item |

### wd-form-item Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 表单项的内容区域，用于放置具体的表单组件 |

## 类型定义

### FormRules

```ts
type FormRules = {
  [key: string]: FormItemRule[]
}
```

表单校验规则对象，键名为字段名，值为该校验字段对应的规则数组。

### FormItemRule

```ts
interface FormItemRule {
  [key: string]: any
  required: boolean
  message: string
  pattern?: RegExp
  validator?: (value: any, rule: FormItemRuleWithoutValidator) => boolean | Promise<string> | Promise<boolean> | Promise<void> | Promise<unknown>
}
```

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| required | boolean | 是 | 是否为必填项，为 true 时会对空值进行校验 |
| message | string | 是 | 校验失败时的错误提示信息 |
| pattern | RegExp | 否 | 正则表达式校验规则，对字段值进行正则匹配 |
| validator | Function | 否 | 自定义校验函数，接收 `(value, rule)` 两个参数 |

**validator 返回值说明**：

- 返回 `true` 或 `Promise.resolve(true)` 表示校验通过
- 返回 `false` 或 `Promise.resolve(false)` 表示校验失败，使用 `message` 作为错误信息
- 返回 `Promise.resolve('自定义错误信息')` 表示校验失败，使用返回的字符串作为错误信息
- 返回 `Promise.reject(new Error('错误信息'))` 或 `Promise.reject('错误信息')` 表示校验失败
- `Promise.reject()` 表示校验失败，使用 `message` 作为错误信息

### ErrorMessage

```ts
type ErrorMessage = {
  prop: string
  message: string
}
```

校验错误信息对象，包含字段名和对应的错误提示。

### FormInstance

```ts
type FormInstance = ComponentPublicInstance<FormProps, FormExpose>
```

通过 `ref<FormInstance>()` 获取表单实例的类型定义。

## 使用示例

### 示例 1：基础表单校验

展示最基础的表单必填校验，在表单子组件上直接配置 `rules`，提交时统一校验。

```vue
<template>
  <view class="form-section">
    <wd-form ref="formRef" :model="formModel">
      <wd-cell-group border>
        <wd-input
          label="用户名"
          label-width="100px"
          prop="username"
          clearable
          v-model="formModel.username"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请输入用户名' }]"
        />
        <wd-input
          label="密码"
          label-width="100px"
          prop="password"
          show-password
          clearable
          v-model="formModel.password"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请输入密码' }]"
        />
      </wd-cell-group>
      <view class="footer">
        <wd-button type="primary" size="large" @click="handleSubmit" block>提交</wd-button>
      </view>
    </wd-form>
  </view>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance } from 'wot-design-uni/components/wd-form/types'

const formRef = ref<FormInstance>()
const formModel = reactive({
  username: '',
  password: ''
})

function handleSubmit() {
  formRef.value!
    .validate()
    .then(({ valid }) => {
      if (valid) {
        uni.showToast({ title: '提交成功', icon: 'success' })
      }
    })
    .catch((error) => {
      console.log('校验失败:', error)
    })
}
</script>

<style lang="scss" scoped>
.form-section {
  padding: 16px;
}

.footer {
  padding: 16px;
}
</style>
```

该示例中，每个表单字段通过 `prop` 属性绑定到 `model` 对应的键名，`rules` 直接配置在输入组件上。点击提交按钮时调用 `formRef.value.validate()` 对所有字段进行校验。如果校验通过，`valid` 为 `true`；否则为 `false` 且 `errors` 数组中包含具体的错误信息。

### 示例 2：多种校验方式

展示正则校验、函数校验和异步校验的完整用法。

```vue
<template>
  <view class="form-section">
    <wd-form ref="formRef" :model="formModel">
      <wd-cell-group border>
        <wd-input
          label="验证码"
          label-width="100px"
          prop="code"
          clearable
          v-model="formModel.code"
          placeholder="正则校验：6位数字"
          :rules="[{ required: false, pattern: /\d{6}/, message: '请输入6位数字验证码' }]"
        />
        <wd-input
          label="手机号"
          label-width="100px"
          prop="phone"
          clearable
          v-model="formModel.phone"
          placeholder="函数校验：手机号格式"
          :rules="[
            {
              required: false,
              message: '请输入正确的手机号',
              validator: phoneValidator
            }
          ]"
        />
        <wd-input
          label="邀请码"
          label-width="100px"
          prop="inviteCode"
          clearable
          v-model="formModel.inviteCode"
          placeholder="函数校验：长度不少于4位"
          :rules="[
            {
              required: false,
              message: '长度不得少于4位',
              validator: lengthValidator
            }
          ]"
        />
        <wd-input
          label="账号"
          label-width="100px"
          prop="account"
          clearable
          v-model="formModel.account"
          placeholder="异步校验：接口验证唯一性"
          :rules="[{ required: false, validator: asyncValidator, message: '该账号已被使用' }]"
        />
      </wd-cell-group>
      <view class="footer">
        <wd-button type="primary" size="large" @click="handleSubmit" block>提交</wd-button>
      </view>
    </wd-form>
  </view>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance } from 'wot-design-uni/components/wd-form/types'

const formRef = ref<FormInstance>()
const formModel = reactive({
  code: '',
  phone: '',
  inviteCode: '',
  account: ''
})

// 正则校验：6位数字验证码，直接在 rules 中使用 pattern

// 函数校验：手机号格式
function phoneValidator(val: string) {
  return /^1\d{10}$/.test(val)
}

// 函数校验：返回 Promise 并自定义错误提示
function lengthValidator(val: string) {
  if (String(val).length >= 4) {
    return Promise.resolve()
  } else {
    return Promise.reject(new Error('长度不得少于4位'))
  }
}

// 异步校验：模拟接口请求验证
function asyncValidator(val: string) {
  return new Promise((resolve) => {
    uni.showLoading({ title: '验证中...' })
    setTimeout(() => {
      uni.hideLoading()
      // 模拟接口返回结果：val === '1234' 表示校验通过
      resolve(val === '1234')
    }, 1000)
  })
}

function handleSubmit() {
  formRef.value!
    .validate()
    .then(({ valid, errors }) => {
      if (valid) {
        uni.showToast({ title: '提交成功', icon: 'success' })
      } else {
        console.log('校验失败字段:', errors)
      }
    })
    .catch((error) => {
      console.log('校验异常:', error)
    })
}
</script>

<style lang="scss" scoped>
.form-section {
  padding: 16px;
}

.footer {
  padding: 16px;
}
</style>
```

本示例演示了三种常见的校验方式：

1. **正则校验**：通过 `pattern` 属性传入正则表达式，字段值不匹配时提示错误。
2. **函数校验**：`validator` 函数返回布尔值（同步）或 Promise（异步）。返回 `false` 时使用 `message` 作为错误提示，`Promise.resolve()` 表示通过，`Promise.reject()` 表示失败。
3. **异步校验**：`validator` 返回 Promise 模拟接口请求，异步校验期间可以展示 loading 状态，完成后根据结果决定校验是否通过。

### 示例 3：失焦校验与指定字段校验

展示在输入框失焦时触发单个字段校验，以及在提交时仅校验部分指定字段。

```vue
<template>
  <view class="form-section">
    <wd-form ref="formRef" :model="formModel" :reset-on-change="false">
      <wd-cell-group border>
        <wd-input
          label="用户名"
          label-width="100px"
          prop="username"
          clearable
          v-model="formModel.username"
          placeholder="请输入用户名"
          @blur="handleBlur('username')"
          :rules="[{ required: true, message: '请输入用户名' }]"
        />
        <wd-input
          label="订单号"
          label-width="100px"
          prop="orderNo"
          clearable
          v-model="formModel.orderNo"
          placeholder="请填写订单号"
          @blur="handleBlur('orderNo')"
          :rules="[{ required: true, message: '请填写订单号' }]"
        />
        <wd-input
          label="商品ID"
          label-width="100px"
          prop="productId"
          clearable
          v-model="formModel.productId"
          placeholder="请填写商品ID"
          @blur="handleBlur('productId')"
          :rules="[{ required: true, message: '请填写商品ID' }]"
        />
      </wd-cell-group>
    </wd-form>

    <view class="footer">
      <wd-button type="primary" @click="handleSubmit" block>提交</wd-button>
      <wd-button type="primary" @click="handlePartialValidate">校验订单号和商品ID</wd-button>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance } from 'wot-design-uni/components/wd-form/types'

const formRef = ref<FormInstance>()
const formModel = reactive({
  username: '',
  orderNo: '',
  productId: ''
})

// 失焦时校验单个字段
function handleBlur(prop: string) {
  formRef.value!.validate(prop)
}

// 仅校验指定的多个字段
function handlePartialValidate() {
  formRef.value!
    .validate(['orderNo', 'productId'])
    .then(({ valid }) => {
      if (valid) {
        uni.showToast({ title: '校验通过', icon: 'success' })
      }
    })
    .catch((error) => {
      console.log('校验失败:', error)
    })
}

// 校验全部字段
function handleSubmit() {
  formRef.value!
    .validate()
    .then(({ valid }) => {
      if (valid) {
        uni.showToast({ title: '提交成功', icon: 'success' })
      }
    })
    .catch((error) => {
      console.log('校验失败:', error)
    })
}
</script>

<style lang="scss" scoped>
.form-section {
  padding: 16px;
}

.footer {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
```

该示例中，`:reset-on-change="false"` 关闭了数据变化时自动清除错误的行为，避免用户在输入过程中错误提示频繁闪烁。通过 `@blur` 事件在输入框失焦时调用 `validate(prop)` 仅校验当前字段。`validate(['orderNo', 'productId'])` 则演示了如何仅对指定字段集合进行校验，适用于分步表单或条件校验场景。

### 示例 4：动态表单

展示动态增减表单项的用法，`prop` 支持嵌套路径格式。

```vue
<template>
  <view class="form-section">
    <wd-form ref="formRef" :model="formModel">
      <wd-cell-group border>
        <wd-input
          label="姓名"
          label-width="100px"
          prop="name"
          clearable
          v-model="formModel.name"
          placeholder="请输入姓名"
          :rules="[{ required: true, message: '请输入姓名' }]"
        />
        <wd-input
          v-for="(item, index) in formModel.phoneNumbers"
          :key="item.key"
          label="手机号"
          :prop="'phoneNumbers.' + index + '.value'"
          label-width="100px"
          clearable
          v-model="item.value"
          placeholder="请填写手机号"
          :rules="[{ required: true, message: '请填写手机号' }]"
        />
        <wd-cell title-width="0px">
          <view class="footer-btns">
            <wd-button size="small" type="info" plain @click="addPhone">添加</wd-button>
            <wd-button size="small" type="info" plain @click="removePhone">删除</wd-button>
            <wd-button size="small" type="info" plain @click="handleReset">重置</wd-button>
            <wd-button type="primary" size="small" @click="handleSubmit">提交</wd-button>
          </view>
        </wd-cell>
      </wd-cell-group>
    </wd-form>
  </view>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance } from 'wot-design-uni/components/wd-form/types'

interface PhoneItem {
  key: number
  value: string
}

const formRef = ref<FormInstance>()
const formModel = reactive<{
  name: string
  phoneNumbers: PhoneItem[]
}>({
  name: '',
  phoneNumbers: [
    {
      key: Date.now(),
      value: ''
    }
  ]
})

function addPhone() {
  formModel.phoneNumbers.push({
    key: Date.now(),
    value: ''
  })
}

function removePhone() {
  formModel.phoneNumbers.splice(formModel.phoneNumbers.length - 1, 1)
}

function handleReset() {
  formRef.value!.reset()
}

function handleSubmit() {
  formRef.value!
    .validate()
    .then(({ valid }) => {
      if (valid) {
        uni.showToast({ title: '校验通过', icon: 'success' })
      }
    })
}
</script>

<style lang="scss" scoped>
.form-section {
  padding: 16px;
}

.footer-btns {
  display: flex;
  gap: 12px;
}
</style>
```

动态表单的关键在于 `prop` 的写法。使用 `'phoneNumbers.' + index + '.value'` 这样的嵌套路径格式，组件内部通过 `getPropByPath` 方法从 `model` 对象中正确读取对应字段的值。删除表单项时 `splice` 操作会改变数组索引，`validate` 校验时会自动根据当前实际存在的子组件进行规则匹配，不会校验已删除的项。`reset()` 方法用于清除所有错误提示。

### 示例 5：Toast 错误提示方式

展示使用弹窗（Toast）方式展示校验错误信息。

```vue
<template>
  <view class="form-section">
    <wd-form ref="formRef" :model="formModel" error-type="toast">
      <wd-cell-group border>
        <wd-input
          label="用户名"
          label-width="100px"
          prop="username"
          clearable
          v-model="formModel.username"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请输入用户名' }]"
        />
        <wd-input
          label="密码"
          label-width="100px"
          prop="password"
          show-password
          clearable
          v-model="formModel.password"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请输入密码' }]"
        />
      </wd-cell-group>
      <view class="footer">
        <wd-button type="primary" size="large" @click="handleSubmit" block>提交</wd-button>
      </view>
    </wd-form>
  </view>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance } from 'wot-design-uni/components/wd-form/types'

const formRef = ref<FormInstance>()
const formModel = reactive({
  username: '',
  password: ''
})

function handleSubmit() {
  formRef.value!
    .validate()
    .then(({ valid }) => {
      if (valid) {
        uni.showToast({ title: '提交成功', icon: 'success' })
      }
    })
    .catch((error) => {
      console.log('校验失败:', error)
    })
}
</script>

<style lang="scss" scoped>
.form-section {
  padding: 16px;
}

.footer {
  padding: 16px;
}
</style>
```

设置 `error-type="toast"` 后，校验失败时会在页面顶部以 Toast 弹窗形式展示第一条错误信息，而不是在表单项下方显示文字提示。这种方式适合页面空间有限或希望减少视觉干扰的场景。`error-type="none"` 则完全不展示错误提示，适用于需要自定义错误处理逻辑的场景。

## 注意事项

1. **rules 合并规则**：`wd-form` 上配置的 `rules` 与表单子组件（如 `wd-input`）上配置的 `rules` 会自动合并。合并时以字段 `prop` 为键，子组件的规则追加到 `wd-form` 规则之后。如果某个字段仅在子组件上配置了规则而 `wd-form` 上没有，该规则同样会生效。

2. **rules 与子组件的对应关系**：`wd-form` 内部会过滤 `rules` 中的规则，仅保留那些有对应子组件存在的字段规则。如果一个字段在 `rules` 中定义了校验规则但页面上没有对应的表单项组件，该规则不会执行。

3. **prop 必填**：`wd-form-item` 和表单子组件的 `prop` 属性是必填项，用于关联校验规则与错误信息的展示。不设置 `prop` 的表单项不会被纳入校验体系。

4. **嵌套路径 prop 写法**：对于数组或嵌套对象的字段，`prop` 使用点号分隔的路径写法，如 `phoneNumbers.0.value` 表示 `model.phoneNumbers[0].value`。路径的层级必须与 `model` 对象的实际结构一致。

5. **validator 函数签名**：`validator` 函数接收两个参数 `(value, rule)`，其中 `value` 是当前字段的值，`rule` 是去除了 `validator` 属性后的规则对象（包含 `required`、`message`、`pattern` 等）。

6. **异步 validator 返回值**：异步校验函数应返回 Promise。校验通过时返回 `Promise.resolve(true)` 或 `Promise.resolve()`；校验失败时返回 `Promise.resolve(false)` 或 `Promise.resolve('自定义错误信息')` 或 `Promise.reject(new Error('错误信息'))`。

7. **resetOnChange 默认行为**：默认情况下，`resetOnChange` 为 `true`，当表单 `model` 数据发生变化时会自动清除所有错误提示。如果希望在用户输入过程中保留错误提示，设置为 `false` 即可。

8. **errorType 默认值**：`errorType` 默认值为 `'message'`，即在表单项下方以红色文字展示错误信息。设置为 `'toast'` 时使用弹窗提示，设置为 `'none'` 时不展示任何提示。

9. **错误信息排序**：当多个字段同时校验失败时，错误信息按照表单项在页面中的排列顺序依次处理，`toast` 模式下只展示排序最靠前的第一个错误。

10. **校验通过自动清除错误**：当校验全部通过后，组件会自动清除对应的错误提示信息。如果仅校验指定字段且全部通过，则仅清除这些字段的错误信息。

11. **wd-form-item 基于 Cell 组件**：`wd-form-item` 内部使用了 `wd-cell` 组件进行布局，支持 Cell 的大部分展示特性（如 `required`、`center`、`border`、`title-width`、`is-link` 等）。`border` 属性从第二个表单项开始生效（通过 `index > 0` 判断）。

12. **样式隔离**：组件启用了 `styleIsolation: 'shared'` 和 `addGlobalClass: true`，支持全局样式和外部样式穿透，可在外部通过自定义类名进行样式覆盖。
