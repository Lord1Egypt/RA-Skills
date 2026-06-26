# CodeInput 验证码输入


## 组件概况

### 组件概述
CodeInput 验证码输入组件是一个专门用于验证码、密码等短数字或字符输入的组件，提供了美观的输入框样式和流畅的交互体验，支持多种自定义配置。

### 详细功能描述
- 支持自定义输入框长度（默认6位）
- 提供盒子模式和线条模式两种显示样式
- 支持密码式圆点显示
- 支持自定义字体大小、颜色和粗细
- 支持自定义输入框大小和间距
- 提供焦点状态指示和光标动画
- 支持自动获取焦点
- 支持禁止原生键盘，便于自定义键盘集成
- 支持输入完成事件回调
- 支持细边框样式
- 支持自动调整位置以适应键盘

### 适用业务场景
- 手机验证码输入
- 邮箱验证码输入
- 支付密码输入
- 邀请码输入
- 身份验证码输入
- 各种需要短数字/字符输入的场景

## 完整API参考

### Props
| 名称 | 类型 | 默认值 | 必填 | 描述 |
| --- | --- | --- | --- | --- |
| type | string | 'number' | 否 | 输入框类型，目前只支持number |
| confirmType | string | 'done' | 否 | 设置右下角按钮的文字，有效值：send|search|next|go|done |
| confirmHold | boolean | false | 否 | 点击键盘右下角按钮时是否保持键盘不收起，H5无效 |
| adjustPosition | boolean | true | 否 | 键盘弹起时，是否自动上推页面 |
| maxlength | number | 6 | 否 | 最大输入长度 |
| dot | boolean | false | 否 | 是否用圆点填充（密码模式） |
| mode | string | 'box' | 否 | 显示模式，box-盒子模式，line-底部横线模式 |
| hairline | boolean | false | 否 | 是否细边框 |
| space | string \| number | 10 | 否 | 字符间的距离，单位px |
| modelValue | string \| number | '' | 否 | 预置值 |
| focus | boolean | false | 否 | 是否自动获取焦点 |
| bold | boolean | false | 否 | 字体是否加粗 |
| color | string | '#606266' | 否 | 字体颜色 |
| fontSize | string \| number | 18 | 否 | 字体大小，单位px |
| size | string \| number | 35 | 否 | 输入框的大小，宽等于高，单位px |
| disabledKeyboard | boolean | false | 否 | 是否隐藏原生键盘，如果想用自定义键盘的话，需设置此参数为true |
| borderColor | string | '#e4e7ed' | 否 | 边框和线条颜色 |
| disabledDot | boolean | true | 否 | 是否禁止输入"."符号 |
| bgColor | string | '' | 否 | 背景颜色 |
| round | string \| number | 4 | 否 | 设置圆角值，单位px |
| customStyle | object | - | 否 | 自定义样式，对象形式 |
| customClass | string | - | 否 | 自定义类名 |

### Events
| 名称 | 触发条件 | 参数说明 |
| --- | --- | --- |
| change | 输入内容变化时 | 当前输入的验证码字符串 |
| finish | 输入达到最大长度时 | 完整的验证码字符串 |
| update:modelValue | 输入内容变化时 | 当前输入的验证码字符串（用于v-model双向绑定） |

### Methods
该组件没有对外暴露的方法。

### Slots
该组件不包含任何插槽。

## 多场景使用示例代码

### 1. 基础用法
```vue
<template>
  <view class="demo-container">
    <text class="title">输入验证码</text>
    <wd-code-input v-model="code"></wd-code-input>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const code = ref('')
</script>

<style scoped>
.demo-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin-bottom: 20px;
  font-size: 16px;
  color: #303133;
}
</style>
```

### 2. 密码模式
```vue
<template>
  <view class="demo-container">
    <text class="title">输入支付密码</text>
    <wd-code-input v-model="password" dot maxlength="4"></wd-code-input>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const password = ref('')
</script>

<style scoped>
.demo-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin-bottom: 20px;
  font-size: 16px;
  color: #303133;
}
</style>
```

### 3. 线条模式
```vue
<template>
  <view class="demo-container">
    <text class="title">线条模式验证码</text>
    <wd-code-input v-model="code" mode="line" border-color="#4d80f0"></wd-code-input>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const code = ref('')
</script>

<style scoped>
.demo-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin-bottom: 20px;
  font-size: 16px;
  color: #303133;
}
</style>
```

### 4. 自定义样式
```vue
<template>
  <view class="demo-container">
    <text class="title">自定义样式验证码</text>
    <wd-code-input 
      v-model="code" 
      :size="50" 
      :font-size="24" 
      color="#67C23A" 
      :space="20"
      border-color="#67C23A"
      :round="8"
    ></wd-code-input>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const code = ref('')
</script>

<style scoped>
.demo-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin-bottom: 20px;
  font-size: 16px;
  color: #303133;
}
</style>
```

### 5. 输入完成事件
```vue
<template>
  <view class="demo-container">
    <text class="title">验证码输入完成事件</text>
    <wd-code-input 
      v-model="code" 
      @finish="onFinish"
    ></wd-code-input>
    <text class="result" v-if="isCompleted">验证码：{{ code }}</text>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const code = ref('')
const isCompleted = ref(false)

// 输入完成事件
const onFinish = (value: string) => {
  console.log('验证码输入完成:', value)
  isCompleted.value = true
  
  // 这里可以添加验证码验证逻辑
  // validateCode(value)
}
</script>

<style scoped>
.demo-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin-bottom: 20px;
  font-size: 16px;
  color: #303133;
}

.result {
  margin-top: 20px;
  font-size: 14px;
  color: #67C23A;
}
</style>
```

## 样式定制指南

### customStyle 自定义样式
通过 `customStyle` 属性可以直接设置组件的内联样式，用于调整组件的位置、边距等。

```vue
<wd-code-input 
  v-model="code" 
  :custom-style="{ margin: '20px', padding: '10px' }"
></wd-code-input>
```

### customClass 自定义类名
通过 `customClass` 属性可以为组件添加自定义类名，结合外部样式表进行更复杂的样式定制。

```vue
<wd-code-input 
  v-model="code" 
  custom-class="my-code-input"
></wd-code-input>
```

```scss
.my-code-input {
  // 自定义验证码输入框样式
  margin: 20px 0;
  
  .wd-code-input__item {
    // 自定义输入框项样式
    border-radius: 8px;
  }
  
  .wd-code-input__item__cursor {
    // 自定义光标样式
    animation: blink 1s infinite;
  }
  
  @keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
  }
}
```

## 注意事项

### 常见问题解决方案
1. **输入框不自动获取焦点**：
   - 确保 `focus` 属性设置为 `true`
   - 检查是否有其他组件抢占了焦点
   - 某些平台可能限制自动获取焦点，需要用户交互触发

2. **输入内容不显示**：
   - 检查 `dot` 属性是否设置为 `true`（密码模式）
   - 确认 `modelValue` 绑定正确
   - 检查字体颜色是否与背景色相同

3. **键盘不弹出**：
   - 检查 `disabledKeyboard` 属性是否设置为 `false`
   - 确认 `type` 属性设置正确
   - 某些平台可能需要特定配置才能弹出键盘

4. **输入完成事件不触发**：
   - 检查 `maxlength` 属性是否设置正确
   - 确保输入内容长度达到 `maxlength`
   - 确认事件监听语法正确

### 性能优化建议
- 避免频繁修改组件的 `size` 和 `fontSize` 等样式属性
- 对于静态样式，建议在外部样式表中定义，而非动态绑定
- 不需要自动获取焦点时，将 `focus` 属性设置为 `false`

### 使用限制条件
- 目前只支持 `number` 类型的输入
- 最大输入长度建议不超过 8 位，过长会影响视觉效果
- 自定义键盘需要自行实现，组件仅提供 `disabledKeyboard` 属性支持
- 某些平台可能对自动调整位置功能有不同的实现效果
