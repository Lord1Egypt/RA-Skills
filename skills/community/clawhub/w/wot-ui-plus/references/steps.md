# Steps 步骤条


## 组件概况

Steps 步骤条组件用于引导用户按照预设的流程完成任务。该组件由 `wd-steps`（步骤条容器）和 `wd-step`（步骤节点）两个关联组件组成。`wd-steps` 作为容器管理所有步骤的整体状态和布局方向，`wd-step` 作为单个步骤节点展示标题、描述、图标和当前状态。组件支持横向和纵向两种布局方向，提供数字、图标、点状三种节点样式，支持已完成、进行中、等待中、出错四种状态，广泛应用于注册引导、订单流程、任务进度展示等场景。

## 核心功能描述

- **步骤状态管理**：通过 `active` 属性控制当前激活的步骤序号，自动计算每个步骤的状态（`finished`/`process`/`wait`）
- **状态自定义**：每个 `wd-step` 可通过 `status` 属性单独设置状态，支持 `finished`（已完成）、`process`（进行中）、`error`（出错）
- **横向布局**：默认水平排列，支持通过 `align-center` 属性实现步骤内容水平居中对齐
- **纵向布局**：通过 `vertical` 属性切换为垂直方向排列，适用于长流程或描述文案较长的场景
- **点状样式**：通过 `dot` 属性将步骤节点显示为圆点样式，适用于简化界面风格
- **自定义图标**：每个步骤可通过 `icon` 属性设置自定义图标，替代默认的数字序号
- **图标插槽**：通过 `icon` 插槽自定义节点图标内容，支持完全自由的图标渲染
- **标题与描述**：每个步骤支持 `title`（标题）和 `description`（描述）两段文案，仅设置标题时字号较小
- **标题插槽**：通过 `title` 和 `description` 插槽实现标题和描述的完全自定义渲染
- **步骤间距控制**：通过 `space` 属性自定义步骤之间的间距
- **默认标题文案**：未设置标题时，根据状态自动显示国际化文案（已完成/进行中/等待中/出错）
- **步骤数量自适应**：容器自动计算子步骤数量，均分水平布局时的空间占比

## 适用业务场景

- **注册引导**：引导新用户完成账号注册、手机绑定、信息完善等流程
- **订单流程**：展示下单、支付、发货、签收等订单状态节点
- **审批流程**：显示申请提交、审批中、审批通过/驳回等审批进度
- **任务进度**：展示多阶段任务的完成进度和各阶段详情
- **安装向导**：引导用户完成软件安装、配置、初始化等步骤
- **物流跟踪**：纵向展示物流节点的时间轴

## API

### wd-steps Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| active | number | 0 | 否 | 当前激活的步骤序号（从 0 开始计数），小于此序号的步骤标记为已完成，等于此序号的步骤标记为进行中，大于此序号的步骤标记为等待中 |
| vertical | boolean | false | 否 | 是否为垂直方向的步骤条，设置为 true 时步骤垂直排列 |
| dot | boolean | false | 否 | 是否为点状步骤条样式，设置为 true 时节点显示为圆点而非数字或图标 |
| space | string | 自动计算 | 否 | 步骤之间的间距。水平模式下设置每个步骤的宽度，垂直模式下设置每个步骤的高度 |
| alignCenter | boolean | false | 否 | 是否将步骤条内容水平居中显示，仅对横向步骤条有效 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-step Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| title | string | 根据状态自动显示 | 否 | 步骤标题。未设置时根据当前状态自动显示国际化文案（已完成/进行中/等待中/出错）。当只有标题而没有描述时，标题字号会小 2 号 |
| description | string | 无 | 否 | 步骤描述信息，显示在标题下方 |
| icon | string | 无 | 否 | 步骤节点图标，传入图标名称。设置后替代默认的数字序号显示 |
| status | string | 根据 active 自动计算 | 否 | 步骤状态，可选值：`finished`（已完成）、`process`（进行中）、`error`（出错）。设置后覆盖自动计算的状态 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-steps Events

`wd-steps` 不对外暴露事件。

### wd-step Events

`wd-step` 不对外暴露事件。

### wd-steps Methods

`wd-steps` 不对外暴露方法。

### wd-step Methods

`wd-step` 不对外暴露方法。

### wd-steps Slots

`wd-steps` 不提供具名插槽，仅提供默认插槽用于包裹 `wd-step` 子组件。

### wd-step Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| icon | - | 自定义步骤节点的图标内容，设置后替代默认数字和 `icon` 属性 |
| title | - | 自定义步骤标题内容，替代 `title` 属性 |
| description | - | 自定义步骤描述内容，替代 `description` 属性 |

## 使用示例

### 示例一：基础步骤条与水平居中

最基本的步骤条用法，通过 `active` 属性控制当前激活的步骤。支持水平居中对齐。

```vue
<template>
  <view>
    <!-- 基础步骤条：默认从第 1 步开始 -->
    <demo-block title="基本用法">
      <wd-steps :active="0">
        <wd-step />
        <wd-step />
        <wd-step />
      </wd-steps>
    </demo-block>

    <!-- 水平居中：步骤内容居中对齐 -->
    <demo-block title="水平居中">
      <wd-steps :active="0" align-center>
        <wd-step />
        <wd-step />
        <wd-step />
      </wd-steps>
    </demo-block>

    <!-- 带标题和描述：配合按钮切换步骤 -->
    <demo-block title="标题和描述信息">
      <wd-steps :active="active" align-center>
        <wd-step title="步骤1" description="注册1个账号" />
        <wd-step title="步骤2" description="登录账号并绑定手机" />
        <wd-step title="步骤3" description="完善个人信息" />
      </wd-steps>
      <view style="margin-top: 15px; text-align: center">
        <wd-button size="small" @click="nextStep">下一步</wd-button>
      </view>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref<number>(0)

function nextStep() {
  active.value = active.value + 1
}
</script>
```

### 示例二：自定义图标与修改状态

通过 `icon` 属性为每个步骤设置自定义图标，通过 `status` 属性手动设置步骤状态。

```vue
<template>
  <view>
    <!-- 自定义图标：每个步骤使用不同图标 -->
    <demo-block title="修改图标">
      <wd-steps :active="1" align-center>
        <wd-step icon="setting" />
        <wd-step icon="list" />
        <wd-step icon="clock" />
      </wd-steps>
    </demo-block>

    <!-- 手动修改状态：标记某一步骤为出错 -->
    <demo-block title="修改状态">
      <wd-steps :active="1" align-center>
        <wd-step title="绑定手机" status="error" />
        <wd-step title="重新绑定手机" />
        <wd-step title="步骤3" />
      </wd-steps>
    </demo-block>

    <!-- 使用插槽自定义图标 -->
    <demo-block title="插槽自定义图标">
      <wd-steps :active="0" align-center>
        <wd-step title="第一步">
          <template #icon>
            <wd-icon name="user" custom-class="custom-icon" />
          </template>
        </wd-step>
        <wd-step title="第二步">
          <template #icon>
            <wd-icon name="phone" custom-class="custom-icon" />
          </template>
        </wd-step>
        <wd-step title="第三步">
          <template #icon>
            <wd-icon name="info" custom-class="custom-icon" />
          </template>
        </wd-step>
      </wd-steps>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
</script>
```

### 示例三：竖向步骤条与点状样式

通过 `vertical` 属性切换为垂直方向布局，通过 `dot` 属性使用点状样式。适用于描述文案较长的场景。

```vue
<template>
  <view>
    <!-- 竖向步骤条：适合长文案 -->
    <demo-block title="竖向步骤条">
      <wd-steps :active="1" vertical>
        <wd-step description="注册1个账号" />
        <wd-step
          title="绑定手机"
          description="登录账号并绑定手机，后面是比较长的文案，后面是比较长的文案"
        />
        <wd-step description="完善个人信息" />
      </wd-steps>
    </demo-block>

    <!-- 点状步骤 + 垂直方向：简洁风格 -->
    <demo-block title="点状步骤和垂直方向">
      <wd-steps :active="1" vertical dot>
        <wd-step description="注册1个账号" />
        <wd-step description="登录账号并绑定手机" />
        <wd-step description="完善个人信息" />
      </wd-steps>
    </demo-block>

    <!-- 横向点状步骤条 -->
    <demo-block title="横向点状步骤">
      <wd-steps :active="1" align-center dot>
        <wd-step title="提交订单" description="已提交" />
        <wd-step title="等待付款" description="等待中" />
        <wd-step title="付款成功" />
        <wd-step title="发货" />
      </wd-steps>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
</script>
```

### 示例四：自定义标题和描述插槽

通过 `title` 和 `description` 插槽实现标题和描述的完全自定义渲染。

```vue
<template>
  <view>
    <!-- 自定义标题和描述：使用富文本内容 -->
    <demo-block title="自定义标题和描述">
      <wd-steps :active="1" align-center>
        <wd-step>
          <template #title>
            <text style="color: #4D80F0; font-weight: bold">第一步</text>
          </template>
          <template #description>
            <text style="color: #999; font-size: 12px">创建账户</text>
          </template>
        </wd-step>
        <wd-step>
          <template #title>
            <text style="color: #4D80F0; font-weight: bold">第二步</text>
          </template>
          <template #description>
            <text style="color: #999; font-size: 12px">验证信息</text>
          </template>
        </wd-step>
        <wd-step>
          <template #title>
            <text style="font-weight: bold">第三步</text>
          </template>
          <template #description>
            <text style="color: #999; font-size: 12px">完成设置</text>
          </template>
        </wd-step>
      </wd-steps>
    </demo-block>

    <!-- 混合使用：属性与插槽配合 -->
    <demo-block title="属性与插槽配合">
      <wd-steps :active="2" vertical>
        <wd-step title="已完成的步骤" description="这是已完成的内容">
          <template #icon>
            <wd-icon name="check" />
          </template>
        </wd-step>
        <wd-step title="进行中的步骤" description="这是进行中的内容" />
        <wd-step>
          <template #title>
            <text>自定义等待标题</text>
          </template>
          <template #description>
            <text>自定义等待描述</text>
          </template>
        </wd-step>
      </wd-steps>
    </demo-block>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
</script>
```

### 示例五：订单流程实战

综合运用各项属性，模拟一个完整的订单状态展示场景。

```vue
<template>
  <view style="padding: 16px">
    <!-- 订单物流跟踪（竖向） -->
    <view style="margin-bottom: 24px">
      <text style="font-size: 16px; font-weight: bold; margin-bottom: 12px; display: block">物流跟踪</text>
      <wd-steps :active="currentStep" vertical>
        <wd-step
          title="已签收"
          :description="formatTime(signTime)"
        />
        <wd-step
          title="派送中"
          :description="'快递员：张三，电话：13800138000'"
        />
        <wd-step
          title="运输中"
          :description="'快件已到达【北京转运中心']"
        />
        <wd-step
          title="已发货"
          :description="'商家已发货'"
        />
        <wd-step
          title="已下单"
          :description="formatTime(orderTime)"
        />
      </wd-steps>
    </view>

    <!-- 订单处理进度（横向） -->
    <view style="margin-bottom: 24px">
      <text style="font-size: 16px; font-weight: bold; margin-bottom: 12px; display: block">订单进度</text>
      <wd-steps :active="orderActive" align-center>
        <wd-step title="提交订单" icon="edit" />
        <wd-step title="等待付款" icon="clock" />
        <wd-step title="已付款" icon="check" />
        <wd-step title="已发货" icon="send" />
      </wd-steps>
    </view>

    <!-- 异常状态展示 -->
    <view>
      <text style="font-size: 16px; font-weight: bold; margin-bottom: 12px; display: block">异常流程</text>
      <wd-steps :active="2" align-center>
        <wd-step title="提交申请" status="finished" icon="check" />
        <wd-step title="审核中" status="process" icon="clock" />
        <wd-step title="审核驳回" status="error" icon="close" />
        <wd-step title="重新提交" icon="edit" />
      </wd-steps>
      <view style="margin-top: 16px; text-align: center">
        <wd-button size="small" @click="handleRetry">重新提交</wd-button>
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const currentStep = ref<number>(1)
const orderActive = ref<number>(1)
const signTime = ref<number>(Date.now())
const orderTime = ref<number>(Date.now() - 3 * 24 * 60 * 60 * 1000)

function formatTime(timestamp: number): string {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hour}:${minute}`
}

function handleRetry() {
  // 重新提交逻辑
  console.log('重新提交')
}
</script>
```

## 注意事项

- **步骤序号从 0 开始**：`active` 属性的值从 0 开始计数，0 表示第一个步骤，1 表示第二个步骤，以此类推。
- **状态自动计算规则**：当未为 `wd-step` 设置 `status` 属性时，组件根据 `active` 值自动计算状态：序号小于 `active` 的步骤为 `finished`（已完成），序号等于 `active` 的步骤为 `process`（进行中），序号大于 `active` 的步骤为 `wait`（等待中）。
- **手动状态优先级**：当为 `wd-step` 设置了 `status` 属性时，该状态将覆盖自动计算的状态，无论 `active` 值如何。
- **默认标题文案**：未设置 `title` 属性时，标题根据当前状态自动显示国际化配置的文案（已完成/进行中/等待中/出错）。
- **标题字号变化**：当步骤只有标题而没有描述时，标题的字号会自动减小 2 号以区分视觉层次；同时有标题和描述时，标题使用正常字号。
- **图标优先级**：节点图标的渲染优先级为：`icon` 插槽 > `icon` 属性 > 默认样式（已完成/出错显示对勾图标，其余显示序号数字）。
- **点状样式影响**：当设置 `dot` 为 true 时，所有步骤节点统一显示为圆点，此时 `icon` 属性和 `icon` 插槽的设置不会生效。
- **垂直布局间距**：垂直模式下，每个步骤的高度可通过 `space` 属性控制，默认情况下自适应内容高度。垂直布局的最后一个步骤不会显示连接线。
- **水平布局均分**：水平模式下，如果不设置 `space`，组件会自动将可用宽度均分给每个步骤（100 / 步骤数量 %）。设置 `space` 后将使用指定值作为每个步骤的宽度。
- **alignCenter 限制**：`align-center` 属性仅对横向步骤条有效，垂直模式下此属性不起作用。
- **连接线渲染**：最后一个步骤节点不会渲染连接线，连接线的长度为从当前步骤中心到下一个步骤中心。
- **主题适配**：组件内置深色主题适配，在 `.wot-theme-dark` 下自动切换为深色配色方案。
- **虚拟宿主**：组件设置了 `virtualHost: true`，支持在小程序等环境中正确使用自定义样式类。