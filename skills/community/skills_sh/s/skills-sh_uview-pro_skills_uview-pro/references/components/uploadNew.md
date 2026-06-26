---
name: "uploadNew"
description: "该组件用于上传文件场景，支持图片、视频、文档等多种类型，支持网格(grid)和列表(list)两种展示模式. Invoke when user needs to use uploadNew component."
url: "https://uviewpro.cn/zh/components/uploadNew.html"
triggers: ["uploadNew"]
---

# Upload 上传 <BadgeText text="公测版" type="danger" size="large"></BadgeText> <to-api/> 

<demo-model url="/pages/componentsB/upload/index"></demo-model>

该组件用于上传文件场景，支持图片、视频、文档等多种类型，支持网格(grid)和列表(list)两种展示模式

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

**特殊说明：**
- `accept="file"` 仅在 H5 和微信小程序支持
- `accept="media"` 仅在微信小程序、支付宝小程序、App 支持
- 文件预览功能在 H5 支持最好，其他平台可能受限于系统能力

## 基本使用

- 可以通过设置`v-model`参数(数组，元素为对象)，显示预置的文件。其中元素的`url`属性为文件路径
- 设置`action`参数为后端服务器地址，注意H5在浏览器可能会有跨域限制，让后端允许域即可
- 默认`accept="image"`，只支持图片上传

```html
<template>
    <u-upload :action="action" v-model="fileList"></u-upload>
</template>

<script setup lang="ts">
// 演示地址，请勿直接使用
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const fileList = ref([
    {
        url: 'http://pics.sc.chinaz.com/files/pic/pic9/201912/hpic1886.jpg',
    }
])
</script>
```

::: tip 提示
`v-model` 是 `modelValue` 的语法糖，推荐优先使用 `v-model` 替代 `:file-list` + `@on-list-change` 的组合。

如果同时使用 `v-model` 和 `:file-list`，`v-model` 优先级更高。
:::

## 双向绑定（v-model）

组件支持 `v-model` 双向绑定，可以更方便地同步文件列表数据。

### 基础用法

```html
<template>
    <u-upload :action="action" v-model="fileList"></u-upload>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const fileList = ref([
    {
        url: 'http://pics.sc.chinaz.com/files/pic/pic9/201912/hpic1886.jpg',
        name: '示例图片.jpg',
        size: 1024 * 50,
        progress: 100,
        error: false
    }
])
</script>
```

### 与自定义插槽配合使用

当使用自定义 `file` 插槽时，`v-model` 可以确保数据双向同步：

```html
<template>
    <u-upload :action="action" v-model="fileList" :show-upload-list="false">
        <template #file="{ file }">
            <view class="custom-list">
                <view v-for="(item, index) in file" :key="index" class="custom-item">
                    <image :src="item.url" mode="aspectFill"></image>
                    <text>{{ item.name }}</text>
                    <button @click="removeFile(index)">删除</button>
                </view>
            </view>
        </template>
    </u-upload>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const fileList = ref([])

function removeFile(index: number) {
    // 直接修改数组，v-model 会自动同步
    fileList.value.splice(index, 1)
}
</script>
```

### 向后兼容

如果项目中已有代码使用 `:file-list` + `@on-list-change` 的组合，仍然可以继续使用，两者完全兼容：

```html
<!-- 旧版用法（仍然支持） -->
<u-upload 
    :action="action" 
    :file-list="fileList"
    @on-list-change="list => fileList = list"
></u-upload>

<!-- 新版推荐用法 -->
<u-upload :action="action" v-model="fileList"></u-upload>
```

## 上传多种文件类型

通过设置`accept`参数，可以上传不同类型的文件：

- `image` - 图片（默认）
- `video` - 视频
- `file` - 文件（仅H5、微信小程序支持）
- `media` - 媒体文件（图片+视频，仅部分平台支持）
- `all` - 所有文件

```html
<!-- 上传视频 -->
<u-upload :action="action" accept="video" :max-duration="120"></u-upload>

<!-- 上传文件（H5/微信小程序） -->
<u-upload :action="action" accept="file" :extension="['.pdf', '.docx']"></u-upload>

<!-- 上传所有类型 -->
<u-upload :action="action" accept="all"></u-upload>
```

## 展示模式

组件支持两种展示模式，通过`mode`参数设置：

- `grid` - 网格模式（默认），适合图片展示
- `list` - 列表模式，适合文件展示，显示文件名和大小

```html
<!-- 网格模式（默认） -->
<u-upload :action="action" accept="image" mode="grid"></u-upload>

<!-- 列表模式 -->
<u-upload :action="action" accept="file" mode="list" :show-file-name="true" :show-file-size="true"></u-upload>
```

## 手动上传

组件默认为自动上传，可以设置`auto-upload`为`false`，然后通过`ref`调用组件的`upload`方法，手动上传文件

```html
<!-- 手动上传 -->
<template>
    <view>
        <u-upload ref="uUploadRef" :action="action" :auto-upload="false" ></u-upload>
        <u-button @click="submit">提交</u-button>
    </view>
</template>

<script setup lang="ts">
// 非真实地址
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const uUploadRef = ref()

function submit() {
    uUploadRef.value?.upload()
}
</script>
```

## 获取上传的文件列表

文件选择或者上传成功后，会保存在组件内部的`lists`数组中，数组元素为对象，有如下属性：
- `url`: 文件地址
- `name`: 文件名
- `size`: 文件大小（字节）
- `fileType`: 文件类型（image/video/file）
- `error`：上传失败标记
- `progress`：上传进度，0-100，100表示上传成功
- `response`：上传成功后，服务器返回的数据

为了获得上传的文件列表，可以在提交表单时，通过`ref`获取组件内部的`lists`文件数组，筛选出`progress`为100的文件

```html
<!-- 获取上传的文件列表 -->
<template>
    <view>
        <u-upload ref="uUploadRef" :action="action" :auto-upload="true" ></u-upload>
        <u-button @click="submit">提交</u-button>
    </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const uUploadRef = ref()

function submit() {
    let files = []
    // 通过filter，筛选出上传进度为100的文件(因为某些上传失败的文件，进度值不为100，这个是可选的操作)
    files = uUploadRef.value?.lists.filter((val: any) => {
        return val.progress == 100
    })
    // 如果您不需要进行太多的处理，直接如下即可
    // files = uUploadRef.value?.lists
    console.log(files)
}
</script>
```

## 报错提示

在以下几种情况，组件会默认通过toast提示用户信息，可以把`show-tips`设置为`false`取消默认的提示，这时可以通过API
中的各种事件，进行自定义的个性化提示
- 超出允许的最大上传数量
- 文件大小超出最大允许大小
- 上传文件出错
- 移除文件

以下示例为屏蔽组件内部的提示，在移除文件时，监听`onRemove`事件，手动提示的情况

```html
<!-- 屏蔽组件内部的提示，在移除文件时，监听onRemove事件，手动提示的情况 -->
<template>
    <u-upload ref="uUploadRef" :action="action" :show-tips="false" @on-remove="onRemove"></u-upload>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const uUploadRef = ref()

function onRemove(index: number, lists: any[]) {
    console.log('文件已被移除')
}
</script>
```

## 限制文件数量和大小

- 通过`max-count`可以设置最多可以选择的文件的数量
- 通过`max-size`设置单个文件最大的大小，单位为B(byte)，默认不限制

下方示例为单张最大为5M，最多选择6个文件的情况：

```html
<u-upload :max-size="5 * 1024 * 1024" max-count="6"></u-upload>
```

## 限制文件类型

可以通过以下方式限制文件类型：

1. **`accept`参数** - 基础文件类型限制（image/video/file/media/all）
2. **`limit-type`参数** - 详细的文件后缀限制，优先级最高
3. **`extension`参数** - 仅在 H5 和微信小程序 `accept="file"` 时有效，用于系统文件选择器过滤

```html
<!-- 方式1：限制为图片 -->
<u-upload accept="image"></u-upload>

<!-- 方式2：详细限制后缀（推荐） -->
<u-upload accept="image" :limit-type="['png', 'jpg', 'jpeg']"></u-upload>

<!-- 方式3：H5/微信小程序选择PDF和Word -->
<u-upload accept="file" :extension="['.pdf', '.docx']" :limit-type="['pdf', 'docx']"></u-upload>
```

## 上传前的钩子

某些时候，**每个文件**上传前可能需要动态修改文件名，修改额外参数等，就会需要用到一个叫`before-upload`的钩子(参数注意不要加括号)，也即回调方法，此方法会返回两个参数：

- `index`——即当前上传文件在上传列表中的索引
- `lists`——当前所有的文件列表

此回调可以返回一个`promise`、`true`，或者`false`，下面分别阐述三者的处理情况：

- `false`——如果返回`false`，将会跳过当前文件，继续上传下一个文件(如果有)，并且再次执行`before-upload`钩子
- `true`——如果返回`true`，会随即上传当前文件，上传成功后，继续上传下一个文件(如果有)，并且再次执行`before-upload`钩子
- `promise`——如果返回的是一个`promise`，如果进入`then`回调，就会和返回`true`的情况一样，如果进入`catch`回调，就会和返回`false`的情况一样

下面举例说明：

### 1. 普通返回

```html
<!-- before-upload 普通返回 -->
<template>
    <u-upload :before-upload="beforeUpload"></u-upload>
</template>

<script setup lang="ts">
function beforeUpload(index: number, list: any[]) {
    // 只上传偶数索引的文件
    if(index % 2 == 0) return true;
    else return false;
}
</script>
```

### 2. 请求之后再返回

```html
<!-- before-upload 请求之后再返回 -->
<template>
    <u-upload :before-upload="beforeUpload"></u-upload>
</template>

<script setup lang="ts">
async function beforeUpload(index: number, list: any[]) {
    // await等待一个请求，请求回来后再返回true，继续上传文件
    let data = await uni.$u.post('url');
    return true; // 或者根据逻辑返回false
}
</script>
```

### 3. 返回一个Promise

```html
<!-- before-upload 返回一个Promise -->
<template>
    <u-upload :before-upload="beforeUpload"></u-upload>
</template>

<script setup lang="ts">
function beforeUpload(index: number, list: any[]) {
    // 返回一个promise
    return new Promise((resolve, reject) => {
        uni.$u.post('url').then(res => {
            // resolve()之后，将会进入promise的组件内部的then回调，相当于返回true
            resolve();
        }).catch(err => {
            // reject()之后，将会进入promise的组件内部的catch回调，相当于返回false
            reject();
        })
    })
}
</script>
```

## 移除前的钩子

某些时候，文件被移除前可能需要进行判断是否可以被移除，就会需要用到一个叫`before-remove`的钩子(参数注意不要加括号)，也即回调方法，此方法会返回两个参数：

- `index`——即当前上传文件在上传列表中的索引
- `lists`——当前所有的文件列表

此回调可以返回一个`promise`、`true`，或者`false`，下面分别阐述三者的处理情况：

- `false`——如果返回`false`，终止移除操作
- `true`——如果返回`true`，执行移除操作
- `promise`——如果返回的是一个`promise`，如果进入`then`回调，就会和返回`true`的情况一样，如果进入`catch`回调，就会和返回`false`的情况一样

此处不举例说明，参考`before-upload`的示例即可。

## 删除确认弹窗

默认情况下，删除文件前会显示确认弹窗。可以通过`show-confirm`参数控制：

```html
<!-- 不显示删除确认弹窗 -->
<u-upload :action="action" :show-confirm="false"></u-upload>
```

## 自定义文件选择

对于不支持文件选择的平台（如 App），可以通过 `custom-choose` 属性开启自定义选择模式：

```html
<template>
    <u-upload 
        ref="uploadRef"
        accept="file"
        :custom-choose="true"
        :action="action"
        @on-choose="handleCustomChoose"
    ></u-upload>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('https://your-server.com/upload')
const uploadRef = ref()

// 自定义文件选择
function handleCustomChoose({ accept, maxCount, currentFiles, index }: any) {
    // App 端使用原生文件选择
    // #ifdef APP-PLUS
    plus.runtime.chooseFile({
        success: (res: any) => {
            const files = res.files.map((file: any) => ({
                path: file.path,
                name: file.name,
                size: file.size,
                fileType: 'file'
            }))
            // 将文件添加到组件
            uploadRef.value?.addFiles(files)
        }
    })
    // #endif
}
</script>
```

**说明：**
- 设置 `:custom-choose="true"` 后，点击选择按钮会触发 `on-choose` 事件，而不是调用默认的文件选择 API
- `on-choose` 事件参数为 `{ accept, maxCount, currentFiles, index }`
- 通过 `ref` 调用 `addFiles(files)` 方法将选择的文件添加到组件列表

## 自定义相关说明

1. 组件内部样式  
组件默认选取文件会展示预览缩略图，包括默认的选取文件的按钮，他们的宽高都是`200rpx`，`border-radius`值为`10rpx`，
另外预览图片的盒子有一个默认的边框，值为`border: 1px solid rgb(235, 236, 238)`。如果用户需要自定义上传按钮，可以参考这些值。

2. 自定义上传按钮  
通过传递名为`addBtn`的`slot`，同时配置`custom-btn`为`true`，可以自定义想要的上传按钮。

如下所示：

```html
<u-upload :custom-btn="true">
	<template #addBtn>
		<view class="slot-btn" hover-class="slot-btn__hover" hover-stay-time="150">
			<u-icon name="photo" size="60" color="#2979ff"></u-icon>
		</view>
	</template>
</u-upload>

<style>
.slot-btn {
	width: 329rpx;
	height: 140rpx;
	display: flex;
	justify-content: center;
	align-items: center;
	background: rgb(244, 245, 246);
	border-radius: 10rpx;
}

.slot-btn__hover {
	background-color: rgb(235, 236, 238);
}
</style>
```

3. 自定义预览列表
首先需要设置`show-upload-list`为`false`来去除组件内部的默认预览列表，其次需要通过`ref`获取组件，进而
操作组件内部的变量和方法，下面为一些组件内部的方法和变量说明：
- `lists`(变量)，可以通过此值，构建自定义的预览列表，该变量内部如下：

```js
lists = [
	{
		url: 'xxx.png', // 预览文件的地址
		name: 'xxx.png', // 文件名
		size: 1024, // 文件大小（字节）
		fileType: 'image', // 文件类型
		error: false, // 上传失败，此值为true
		progress: 100, // 0-100之间的值
	},
	......
]
```

- `deleteItem(index)`(方法)，可以用此方法在自定义列表中通过`ref`删除某一个文件

以下为完整的自定义文件预览列表示例：

```html
<!-- 自定义文件预览列表 -->
<template>
    <view class="wrap">
        <view class="pre-box" v-if="!showUploadList">
            <view class="pre-item" v-for="(item, index) in lists" :key="index">
                <image class="pre-item-image" :src="item.url" mode="aspectFill"></image>
            </view>
        </view>
        <u-upload :custom-btn="true" ref="uUploadRef" :show-upload-list="showUploadList" :action="action">
            <template #addBtn>
                <view class="slot-btn" hover-class="slot-btn__hover" hover-stay-time="150">
                    <u-icon name="photo" size="60" color="#c0c4cc"></u-icon>
                </view>
            </template>
        </u-upload>
    </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const action = ref('http://www.example.com') // 演示地址
const showUploadList = ref(false)
const uUploadRef = ref()
const lists = ref<any[]>([])

// 只有onMounted生命周期才能调用refs操作组件
onMounted(() => {
    // 得到整个组件对象，内部文件列表变量为"lists"
    lists.value = uUploadRef.value?.lists || []
})
</script>

<style lang="scss">
    .wrap {
        padding: 24rpx;
    }
    
    .slot-btn {
        width: 341rpx;
        height: 140rpx;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgb(244, 245, 246);
        border-radius: 10rpx;
    }

    .slot-btn__hover {
        background-color: rgb(235, 236, 238);
    }

    .pre-box {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .pre-item {
        flex: 0 0 48.5%;
        border-radius: 10rpx;
        height: 140rpx;
        overflow: hidden;
        position: relative;
        margin-bottom: 20rpx;
    }

    .pre-item-image {
        width: 100%;
        height: 140rpx;
    }
</style>
```


## API

### Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 | 版本 |
|------|------|------|--------|--------|------|
| action | 服务器上传地址 | String | - | - | - |
| accept | 接受的文件类型 | String | image | image/video/file/media/all | 0.6.0 |
| modelValue | 文件列表（推荐，v-model 双向绑定） | Array | [] | - | 0.6.0 |
| mode | 展示模式 | String | grid | grid/list | 0.6.0 |
| max-count | 最大选择文件的数量 | String/Number | 52 | - | - |
| max-size | 选择单个文件的最大大小，单位B(byte) | String/Number | Number.MAX_VALUE | - | - |
| width | 预览区域和添加按钮的宽度，单位rpx | String/Number | 200 | - | - |
| height | 预览区域和添加按钮的高度，单位rpx | String/Number | 200 | - | - |
| multiple | 是否开启文件多选 | Boolean | true | true/false | - |
| disabled | 是否禁用组件 | Boolean | false | true/false | - |
| auto-upload | 选择完文件是否自动上传 | Boolean | true | true/false | - |
| deletable | 是否显示删除文件的按钮 | Boolean | true | true/false | - |
| show-confirm | 删除文件前是否显示确认弹窗 | Boolean | true | true/false | 0.6.0 |
| show-tips | 特殊情况下是否自动提示toast | Boolean | true | true/false | - |
| show-progress | 是否显示上传进度条 | Boolean | true | true/false | - |
| show-upload-list | 是否显示组件内部的文件预览列表 | Boolean | true | true/false | - |
| show-file-name | 是否显示文件名 | Boolean | true | true/false | 0.6.0 |
| show-file-size | 是否显示文件大小 | Boolean | false | true/false | 0.6.0 |
| preview-full-image | 是否可以通过`uni.previewImage`预览已选择的图片 | Boolean | true | true/false | - |
| preview-file | 是否可预览文件（非图片类型） | Boolean | true | true/false | 0.6.0 |
| custom-btn | 是否自定义选择文件的按钮 | Boolean | false | true/false | - |
| upload-text | 选择文件按钮的提示文字 | String | 根据accept自动显示 | - | - |
| image-mode | 预览图片的显示模式 | String | aspectFill | - | - |
| del-icon | 右上角删除图标名称 | String | close | - | - |
| del-bg-color | 右上角删除按钮的背景颜色 | String | var(--u-type-error) | - | - |
| del-color | 右上角删除按钮图标的颜色 | String | var(--u-white-color) | - | - |
| header | 上传携带的请求头信息 | Object | {} | - | - |
| form-data | 上传额外携带的参数 | Object | {} | - | - |
| name | 上传文件的字段名 | String | file | - | - |
| size-type | original原图，compressed压缩图 | Array | ['original','compressed'] | - | - |
| source-type | 选择文件的来源，album-相册，camera-相机 | Array | ['album','camera'] | - | - |
| limit-type | 限制允许上传的文件后缀，优先级高于accept | Array | [] | - | - |
| extension | 选择文件时的扩展名过滤，仅H5和微信小程序有效 | Array | [] | - | 0.6.0 |
| file-icon-map | 文件类型图标映射配置 | Object | {} | - | 0.6.0 |
| file-list | 默认显示的文件列表（旧版，建议使用v-model） | Array | [] | - | - |
| compressed | 选择视频时是否压缩 | Boolean | true | true/false | 0.6.0 |
| max-duration | 选择视频时拍摄最长时长，单位秒 | Number | 60 | - | 0.6.0 |
| camera | 选择视频时摄像头方向 | String | back | front/back | 0.6.0 |
| image-shape | 图片/图标展示形状 | String | square | square/circle | 0.6.0 |
| custom-choose | 是否使用自定义文件选择 | Boolean | false | true/false | 0.6.0 |
| before-upload | 上传前钩子 | Function | - | - | - |
| before-remove | 删除前钩子 | Function | - | - | - |
| to-json | 如果上传后返回值为json字符串，是否自动转为json | Boolean | true | true/false | - |
| index | 在各个回调事件中的最后一个参数返回，用于区别是哪一个组件的事件 | String/Number | - | - | - |


### Methods

此方法如要通过ref手动调用

| 名称 | 说明 | 版本 |
|------|------|------|
| upload | 手动上传文件 | - |
| clear | 清空内部文件列表 | - |
| reUpload | 重新上传所有失败/未上传的文件 | - |
| retry(index) | 重新上传指定索引的文件 | - |
| remove(index) | 手动移除指定索引的文件 | - |
| selectFile | 手动触发文件选择 | - |
| doPreviewImage(url, index) | 预览图片 | - |
| doPreviewFile(item, index) | 预览/打开文件 | 0.6.0 |
| addFiles(files) | 添加文件到列表（配合custom-choose使用） | 0.6.0 |


### Slots

| 名称 | 说明 | 版本 |
|------|------|------|
| addBtn | 自定义选择文件按钮 | - |
| file | 自定义文件列表插槽 | - |



### Events

回调参数中的`lists`参数，为目前组件内的所有文件数组，`index`为当前操作的文件的索引，`name`为通过`props`传递的`index`参数：

| 事件名 | 说明 | 回调参数 | 版本 |
|--------|------|----------|------|
| on-oversize | 文件大小超出max-size限制时触发 | (file,lists,name) | - |
| on-exceed | 文件数量超出max-count限制时触发 | (file,lists,name) | - |
| on-choose-complete | 每次选择文件后触发 | (lists,name) | - |
| on-choose-fail | 文件选择失败时触发 | (error) | - |
| on-uploaded | 所有文件上传完毕触发 | (lists,name) | - |
| on-success | 单个文件上传成功时触发 | (data,index,lists,name) | - |
| on-error | 单个文件上传失败时触发 | (res,index,lists,name) | - |
| on-change | 单个文件上传状态改变时触发 | (res,index,lists,name) | - |
| on-progress | 文件上传过程中的进度变化时触发 | (res,index,lists,name) | - |
| on-remove | 移除文件时触发 | (index,lists,name) | - |
| on-preview | 预览文件时触发 | (url,lists,name) | - |
| on-list-change | 文件列表发生变化时触发 | (lists,name) | - |
| on-choose | 启用custom-choose时触发 | ({accept,maxCount,currentFiles,index}) | 0.6.0 |
| update:modelValue | v-model双向绑定事件 | (lists) | 0.6.0 |
