# Upload 上传


## 组件概况

Upload 上传组件是一个功能丰富的文件上传组件，支持图片、视频、媒体、文件等多种文件类型的选择与上传。组件内置文件预览、上传进度展示、上传状态管理、文件大小校验等核心功能，并支持自动上传和手动触发上传两种模式。用户可以通过自定义插槽灵活定制上传唤起按钮样式和预览项的覆盖层，同时提供多个生命周期钩子函数（beforeChoose、beforeUpload、beforePreview、beforeRemove、buildFormData）以实现对上传流程的精细控制。该组件适用于头像上传、附件上传、图片/视频分享、资料提交等需要文件上传功能的业务场景。

## 核心功能描述

- **多文件类型支持**：支持 `image`、`video`、`media`（图片+视频）、`all`（全部类型）、`file`（文档文件）五种文件类型，其中 `media`、`file`、`all` 类型仅在微信小程序和 H5 平台可用
- **自动/手动上传**：通过 `auto-upload` 属性控制，默认为 `true`（选择文件后自动上传），设置为 `false` 后可通过 ref 调用 `submit()` 方法手动触发上传
- **上传进度展示**：上传过程中自动展示 loading 动画和百分比进度，支持自定义 loading 图标的类型、尺寸和颜色
- **上传状态管理**：文件经历 `pending`（待上传）-> `loading`（上传中）-> `success`（成功）/ `fail`（失败）四种状态，并在预览列表中可视化展示
- **文件大小校验**：通过 `max-size` 属性限制最大文件大小（单位为 byte），超出限制时触发 `oversize` 事件且文件不会进入上传列表
- **上传数量限制**：通过 `limit` 属性限制最大上传文件数，达到上限后自动隐藏上传唤起按钮
- **多选上传**：通过 `multiple` 属性开启多选模式，支持一次选择多个文件上传
- **图片/视频/文件预览**：点击已上传文件可预览，图片调用 `uni.previewImage` 全屏预览，视频使用 `uni.previewMedia` 或内置 `wd-video-preview` 组件预览，文件调用 `uni.openDocument` 打开
- **自定义上传方法**：通过 `upload-method` 属性可完全自定义上传逻辑（如上传至 OSS），替代默认的 `uni.uploadFile` 实现
- **FormData 构建钩子**：通过 `build-form-data` 钩子可动态构建上传时附加的表单数据，适用于需要签名计算的 OSS 上传场景
- **多种前置拦截钩子**：
  - `before-choose`：选择文件前拦截
  - `before-upload`：上传文件前拦截
  - `before-preview`：预览文件前拦截
  - `before-remove`：移除文件前拦截
- **覆盖上传**：通过 `reupload` 属性，点击已上传文件时可以选择替换该文件而非预览
- **扩展名过滤**：通过 `extension` 属性按文件扩展名过滤可选文件（H5 全类型支持，微信小程序支持 `all` 和 `file` 类型过滤）
- **自定义唤起样式**：通过默认插槽可完全自定义上传按钮的展示样式
- **自定义预览覆盖层**：通过 `preview-cover` 插槽可在预览项上叠加自定义内容（如文件名称标注）
- **禁用状态**：通过 `disabled` 属性禁用上传功能，禁用后不显示移除按钮

## 适用业务场景

- **用户头像上传**：用户注册或修改个人信息时上传头像图片
- **商品图片上传**：电商应用中商家上传商品主图和详情图
- **附件/文档上传**：OA 办公、审批流程中上传合同、报表等文档附件
- **图片/视频分享**：社交应用、社区论坛中用户发布图文或视频动态
- **凭证上传**：金融、保险应用中上传身份证、发票等凭证材料
- **反馈投诉附件**：用户反馈、投诉工单中上传相关截图或证明材料
- **资料审核上传**：资质认证、实名认证场景下的多材料上传提交
- **短视频上传**：内容创作平台中用户上传视频作品

## API

### Upload Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| file-list | UploadFile[] | [] | 否 | 上传的文件列表，例如: `[{name:'food.jpg',url:'https://xxx.cdn.com/xxx.jpg'}]`，支持 v-model 双向绑定 |
| action | string | '' | 是 | 必选参数，上传服务器地址 |
| header | Record\<string, any\> | {} | 否 | 设置上传的请求头部 |
| multiple | boolean | false | 否 | 是否支持多选文件 |
| disabled | boolean | false | 否 | 是否禁用上传组件 |
| limit | number | - | 否 | 最大允许上传个数 |
| show-limit-num | boolean | true | 否 | 限制上传个数的情况下，是否展示当前上传的个数，格式为（已传数量/最大数量） |
| max-size | number | Number.MAX_VALUE | 否 | 文件大小限制，单位为 byte |
| source-type | UploadSourceType[] | ['album', 'camera'] | 否 | 选择文件的来源，可选值：`album`（相册）、`camera`（相机） |
| size-type | UploadSizeType[] | ['original', 'compressed'] | 否 | 所选图片的尺寸，可选值：`original`（原图）、`compressed`（压缩图） |
| name | string | 'file' | 否 | 文件对应的 key，服务端通过该 key 获取文件的二进制内容 |
| form-data | Record\<string, any\> | {} | 否 | HTTP 请求中额外的 formdata 数据 |
| on-preview-fail | UploadOnPreviewFail | - | 否 | 预览失败时的回调函数，参数为 `{index, imgList}` |
| before-upload | UploadBeforeUpload | - | 否 | 上传文件之前的钩子，参数为 `{files, fileList, resolve}`，若调用 `resolve(false)` 则停止上传 |
| before-choose | UploadBeforeChoose | - | 否 | 选择文件之前的钩子，参数为 `{fileList, resolve}`，若调用 `resolve(false)` 则停止选择 |
| before-remove | UploadBeforeRemove | - | 否 | 删除文件之前的钩子，参数为 `{file, index, fileList, resolve}`，若调用 `resolve(false)` 则停止删除 |
| before-preview | UploadBeforePreview | - | 否 | 预览文件之前的钩子，参数为 `{file, index, imgList, fileList, resolve}`，若调用 `resolve(false)` 则停止预览 |
| build-form-data | UploadBuildFormData | - | 否 | 构建上传 formData 的钩子，参数为 `{file, formData, resolve}`，调用 `resolve(formData)` 传入处理后的 formData |
| loading-type | string | 'ring' | 否 | 加载中图标类型，参考 Loading 组件的 type 属性 |
| loading-color | string | '#ffffff' | 否 | 加载中图标颜色 |
| accept | UploadFileType | 'image' | 否 | 接受文件类型，可选值：`image`、`video`、`media`、`all`、`file`。`media` 和 `file` 仅微信小程序支持，`all` 仅微信小程序和 H5 支持 |
| status-key | string | 'status' | 否 | file 数据结构中，status 对应的 key |
| loading-size | string | '24px' | 否 | 加载中图标尺寸 |
| compressed | boolean | true | 否 | 是否压缩视频，当 `accept` 为 `video` 时生效 |
| max-duration | number | 60 | 否 | 拍摄视频最长拍摄时间，当 `accept` 为 `video` / `media` 时生效，单位：秒 |
| camera | UploadCameraType | 'back' | 否 | 使用前置或后置相机，当 `accept` 为 `video` / `media` 时生效，可选值：`front`、`back` |
| image-mode | ImageMode | 'aspectFit' | 否 | 预览图片的 mode 属性 |
| success-status | number | 200 | 否 | 接口响应的成功状态码（statusCode）值 |
| custom-evoke-class | string | '' | 否 | 自定义上传唤起按钮样式类 |
| custom-preview-class | string | '' | 否 | 自定义预览图片列表样式类 |
| auto-upload | boolean | true | 否 | 是否选择文件后自动上传 |
| reupload | boolean | false | 否 | 点击已上传文件时是否可以重新上传（覆盖上传） |
| upload-method | UploadMethod | - | 否 | 自定义上传文件的请求方法，替代默认 `uni.uploadFile` |
| extension | string[] | - | 否 | 根据文件扩展名过滤，每一项都不能是空字符串，默认不过滤。H5 支持全部类型过滤，微信小程序支持 `all` 和 `file` 时过滤 |
| custom-style | string | '' | 否 | 自定义根节点样式 |
| custom-class | string | '' | 否 | 自定义根节点样式类 |

### Upload Events

| 事件名称 | 参数 | 说明 |
|---------|------|------|
| change | `(value: { fileList: UploadFileItem[] })` | 上传文件列表发生变化时触发 |
| success | `(value: { file: UploadFileItem, fileList: UploadFileItem[], formData: Record<string, any> })` | 单个文件上传成功时触发 |
| fail | `(value: { error: any, file: UploadFileItem, formData: Record<string, any> })` | 单个文件上传失败时触发 |
| progress | `(value: { response: UniApp.OnProgressUpdateResult, file: UploadFileItem })` | 上传进度更新时触发 |
| oversize | `(value: { file: ChooseFile })` | 文件大小超出 `max-size` 限制时触发 |
| chooseerror | `(value: { error: any })` | 选择文件失败时触发 |
| remove | `(value: { file: UploadFileItem })` | 移除文件时触发 |

### Upload Methods

通过 ref 可以获取 `wd-upload` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| submit | 无 | void | 手动触发上传（当 `auto-upload` 为 `false` 时使用） |
| abort | `(task?: UniApp.UploadTask)` | void | 取消上传，可传入指定的上传任务，不传则中断当前正在进行的任务 |

### Upload Slots

| 插槽名称 | 参数 | 说明 |
|---------|------|------|
| default | 无 | 自定义上传唤起按钮，传入后会替换默认的相机图标按钮 |
| preview-cover | `{ file: UploadFileItem, index: number }` | 自定义预览项的覆盖内容，展示在每个预览项上方（微信小程序环境下拿不到 file 对象） |

### UploadFileItem 类型

```ts
interface UploadFileItem {
  uid: number                                  // 当前上传文件在列表中的唯一标识
  url: string                                  // 上传图片/视频的本地地址或已上传文件的URL
  thumb?: string                               // 缩略图地址（视频场景下使用）
  name?: string                                // 当前文件名称，仅 H5 支持
  status?: UploadStatusType                    // 上传状态，可选值：'pending' | 'loading' | 'success' | 'fail'
  size?: number                                // 文件大小
  percent?: number                             // 上传进度百分比
  response?: string | Record<string, any>      // 后端返回的内容，可能是对象或字符串
  error?: string                               // 上传失败时的错误信息
  [key: string]: any                           // 支持扩展任意自定义字段
}
```

```ts
type UploadFile = Partial<UploadFileItem> & { url: string }
```

## 使用示例

### 示例一：基础图片上传

最基础的用法，绑定上传地址和文件列表，选择图片后自动上传。

```vue
<template>
  <wd-upload
    v-model:file-list="fileList"
    :action="action"
    image-mode="aspectFill"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { UploadFile } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([
  {
    url: 'https://wot-ui-plus.cn/assets/panda.jpg'
  }
])
</script>
```

### 示例二：多选上传并限制最大数量

支持多选模式上传，限制最多上传 3 张图片，并监听文件列表变化。

```vue
<template>
  <wd-upload
    :file-list="fileList"
    :action="action"
    :limit="3"
    :multiple="true"
    @change="handleChange"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { UploadFile } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])

function handleChange({ fileList: list }: { fileList: UploadFile[] }) {
  fileList.value = list
}
</script>
```

### 示例三：手动触发上传

设置 `auto-upload` 为 `false`，通过 ref 调用 `submit()` 方法手动触发上传。

```vue
<template>
  <wd-upload
    ref="uploadRef"
    :file-list="fileList"
    :action="action"
    :auto-upload="false"
    @change="handleChange"
  />
  <wd-button type="primary" @click="handleSubmit">开始上传</wd-button>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type {
  UploadFile,
  UploadInstance
} from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])
const uploadRef = ref<UploadInstance>()

function handleChange({ fileList: list }: { fileList: UploadFile[] }) {
  fileList.value = list
}

function handleSubmit() {
  uploadRef.value?.submit()
}
</script>
```

### 示例四：自定义上传方法

通过 `upload-method` 属性自定义上传逻辑，实现对上传过程的完全控制。

```vue
<template>
  <wd-upload
    v-model:file-list="fileList"
    :upload-method="customUpload"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type {
  UploadFile,
  UploadFileItem,
  UploadMethod
} from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])

const customUpload: UploadMethod = (file, formData, options) => {
  const uploadTask = uni.uploadFile({
    url: action,
    header: options.header,
    name: options.name,
    fileName: options.name,
    fileType: options.fileType,
    formData,
    filePath: file.url,
    success(res) {
      if (res.statusCode === options.statusCode) {
        options.onSuccess(res, file, formData)
      } else {
        options.onError({ ...res, errMsg: res.errMsg || '' }, file, formData)
      }
    },
    fail(err) {
      options.onError(err, file, formData)
    }
  })

  // 监听上传进度
  uploadTask.onProgressUpdate((res) => {
    options.onProgress(res, file)
  })
}
</script>
```

### 示例五：上传前拦截与移除前确认

使用 `before-upload` 钩子在选择文件后上传前进行二次确认，使用 `before-remove` 钩子在移除文件前进行确认提示。

```vue
<template>
  <wd-upload
    :file-list="fileList"
    :action="action"
    :before-upload="beforeUpload"
    :before-remove="beforeRemove"
    @change="handleChange"
  />
  <wd-message-box />
  <wd-toast />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useToast, useMessage } from '@/uni_modules/wot-ui-plus'
import type { UploadFile } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])
const toast = useToast()
const messageBox = useMessage()

function handleChange({ fileList: list }: { fileList: UploadFile[] }) {
  fileList.value = list
}

const beforeUpload = ({ files, fileList, resolve }: {
  files: Record<string, any>[]
  fileList: UploadFile[]
  resolve: (isPass: boolean) => void
}) => {
  messageBox
    .confirm({
      msg: '是否确认上传所选文件？',
      title: '提示'
    })
    .then(() => {
      console.log('待上传文件：', files)
      resolve(true)
    })
    .catch(() => {
      toast.show('取消上传操作')
    })
}

const beforeRemove = ({ file, index, fileList, resolve }: {
  file: UploadFileItem
  index: number
  fileList: UploadFile[]
  resolve: (isPass: boolean) => void
}) => {
  messageBox
    .confirm({
      msg: '是否确认删除该文件？',
      title: '提示'
    })
    .then(() => {
      toast.success('删除成功')
      resolve(true)
    })
    .catch(() => {
      toast.show('取消删除操作')
    })
}
</script>
```

### 示例六：自定义上传唤起样式

通过默认插槽自定义上传按钮的展示样式，结合 `limit` 属性限制上传数量。

```vue
<template>
  <wd-upload
    :file-list="fileList"
    :action="action"
    :limit="5"
    @change="handleChange"
  >
    <wd-button type="primary" size="small">选择文件</wd-button>
  </wd-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { UploadFile } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])

function handleChange({ fileList: list }: { fileList: UploadFile[] }) {
  fileList.value = list
}
</script>
```

### 示例七：上传视频

设置 `accept` 为 `video` 支持视频上传，开启多选模式。

```vue
<template>
  <wd-upload
    accept="video"
    :multiple="true"
    :file-list="fileList"
    :action="action"
    @change="handleChange"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { UploadFile } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])

function handleChange({ fileList: list }: { fileList: UploadFile[] }) {
  fileList.value = list
}
</script>
```

### 示例八：自定义预览覆盖层

通过 `preview-cover` 插槽在预览项上叠加自定义内容（如文件名称标注）。

```vue
<template>
  <wd-upload
    v-model:file-list="fileList"
    accept="image"
    image-mode="aspectFill"
    :action="action"
  >
    <template #preview-cover="{ file, index }">
      <view class="preview-cover">{{ file.name || `文件${index}` }}</view>
    </template>
  </wd-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { UploadFile } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([
  {
    url: 'https://wot-ui-plus.cn/assets/panda.jpg',
    name: 'panda'
  }
])
</script>

<style lang="scss" scoped>
.preview-cover {
  margin-top: 10rpx;
  text-align: center;
  color: #ffffff;
  font-size: 12px;
}
</style>
```

### 示例九：上传状态监听

通过 `success`、`fail`、`progress` 事件实时监听上传状态和进度变化。

```vue
<template>
  <wd-upload
    :file-list="fileList"
    :action="action"
    @change="handleChange"
    @success="handleSuccess"
    @fail="handleFail"
    @progress="handleProgress"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type {
  UploadFile,
  UploadSuccessEvent,
  UploadErrorEvent,
  UploadProgressEvent
} from '@/uni_modules/wot-ui-plus/components/wd-upload/types'

const action = 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload'
const fileList = ref<UploadFile[]>([])

function handleChange({ fileList: list }: { fileList: UploadFile[] }) {
  fileList.value = list
}

function handleSuccess(event: UploadSuccessEvent) {
  console.log('上传成功', event.file, event.fileList)
}

function handleFail(event: UploadErrorEvent) {
  console.log('上传失败', event.file, event.error)
}

function handleProgress(event: UploadProgressEvent) {
  console.log('上传进度', event.file.percent, '%')
}
</script>
```

## 注意事项

- **action 为必填**：`action` 属性为上传服务器地址，必须正确配置，否则上传请求将失败。当使用 `upload-method` 自定义上传方法时可不需要此属性
- **accept 类型平台兼容性**：`accept` 的可选值中，`media`（同时支持图片和视频）和 `file`（文档文件类型）仅在微信小程序可用，`all`（全部类型）在微信小程序和 H5 平台可用，其余平台默认使用 `image` 类型能力
- **extension 扩展名过滤平台差异**：`extension` 属性在 H5 平台支持全部类型文件的扩展名过滤，在微信小程序中仅当 `accept` 为 `all` 或 `file` 时生效，其余平台不支持此功能
- **max-size 单位为 byte**：文件大小限制 `max-size` 的单位是 byte（字节），例如限制为 5MB 应设置为 `5 * 1024 * 1024`
- **fileList 双向绑定**：推荐使用 `v-model:file-list` 进行双向绑定，也可通过 `:file-list` 绑定数据并监听 `@change` 事件手动更新
- **自动上传行为**：默认 `auto-upload` 为 `true`，选择文件后立即开始上传。如需控制上传时机（如表单填完再提交），应设置 `auto-upload="false"` 并通过 `submit()` 手动触发
- **上传状态自定义**：若后端返回的文件数据结构中状态字段不叫 `status`，可通过 `status-key` 属性指定对应的字段名
- **reupload 覆盖上传**：开启 `reupload` 后，点击已上传文件将进入重新选择模式（替换该文件）而非预览。该功能在微信小程序中结合 `accept="all"` 使用时支持图片和视频
- **preview-cover 插槽平台限制**：`preview-cover` 插槽在微信小程序环境下拿不到 `file` 对象，仅能获取 `index` 值
- **disabled 禁用状态**：组件禁用后，不显示已上传文件的移除按钮，且点击上传唤起按钮无响应
- **beforeUpload 钩子参数**：`before-upload` 钩子的 `files` 参数是原始文件数组，`fileList` 是当前已上传列表，需通过调用 `resolve(true)` 放行上传
- **buildFormData 异步支持**：`build-form-data` 钩子支持异步处理，适用于需要请求服务端获取签名后再构建 formData 的场景
- **successStatus 默认值**：默认将 HTTP 状态码 200 视为上传成功，若服务端返回其他状态码表示成功，请通过 `success-status` 属性自定义
- **视频缩略图**：视频文件的 `thumb` 缩略图地址由 uni-app 选择视频 API 返回，若需要自定义缩略图可在 `change` 事件中手动设置
- **预览失败处理**：可通过 `on-preview-fail` 属性自定义预览失败时的提示行为，若不设置则默认显示 `uni.showToast` 提示
- **中断上传**：调用 `abort()` 方法可中断当前正在进行的上传任务。在组件销毁前建议调用此方法避免无效请求
