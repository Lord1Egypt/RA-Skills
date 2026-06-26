# ImgCropper 图片裁剪

## 组件概况

ImgCropper 图片裁剪组件是一个全屏的图片裁剪工具，通过 Canvas 模拟裁剪框的方式实现图片裁剪功能。用户可以选择图片后，在裁剪区域内通过拖动、缩放、旋转等操作调整图片位置和大小，最终将裁剪区域的内容导出为图片文件。组件支持自定义裁剪框宽高比、导出图片质量和格式、是否禁用旋转等功能，广泛应用于头像裁剪、图片编辑等场景。

## 核心功能描述

- **全屏裁剪界面**：组件以全屏模式展示，包含裁剪框、操作按钮和旋转控制
- **裁剪框规则展示**：裁剪框带有辅助网格线（井字线）和四角标记，帮助用户对齐裁剪区域
- **图片拖动**：支持单指拖动移动图片位置，双指捏合缩放调整图片大小
- **图片旋转**：支持点击旋转按钮每次逆时针旋转 90 度，旋转时带有平滑过渡动画
- **边缘检测**：自动检测图片边缘，确保图片始终覆盖裁剪框，防止图片移出可视区域
- **缩放限制**：通过 `max-scale` 限制最大缩放倍数，防止过度放大
- **自定义裁剪比例**：通过 `aspect-ratio` 设置裁剪框的宽高比（如 `1:1`、`16:9`、`3:2` 等）
- **导出图片**：裁剪完成后通过 Canvas 绘制并导出为指定格式的图片文件，支持设置导出质量（`quality`）和缩放比例（`export-scale`）
- **操作动画**：旋转等操作带有过渡动画（默认 300ms 后自动关闭动画）
- **高亮遮罩**：拖动和缩放过程中，裁剪框外遮罩变亮提示操作状态，操作结束后恢复
- **取消与确认**：提供取消和确认两个操作按钮，取消关闭组件，确认裁剪并导出图片
- **加载状态监听**：提供图片加载完成和加载失败的事件回调

## 适用业务场景

- **头像裁剪**：用户上传头像时进行裁剪，确保头像图片符合正方形或其他比例要求
- **封面图裁剪**：用户上传文章封面、商品主图时进行比例裁剪
- **图片编辑**：简易的图片裁剪编辑功能，支持旋转、缩放和位置调整
- **证件照裁剪**：裁剪证件照为指定比例
- **相册图片裁剪**：从相册中选择图片后进行裁剪再上传
- **拍照后裁剪**：拍照后进入裁剪界面，对拍摄的图片进行裁剪处理

## API

### ImgCropper Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | boolean | false | 否 | 是否打开图片裁剪组件，通过 `v-model` 双向绑定控制 |
| imgSrc | string | '' | 否 | 图片源路径 |
| imgWidth | number / string | '' | 否 | 图片宽度 |
| imgHeight | number / string | '' | 否 | 图片高度 |
| cancelButtonText | string | '' | 否 | 取消按钮文案，未设置时跟随国际化配置 |
| confirmButtonText | string | '' | 否 | 确认按钮文案，未设置时跟随国际化配置 |
| disabledRotate | boolean | false | 否 | 是否禁用旋转功能 |
| fileType | string | 'png' | 否 | 目标文件的类型，支持 png / jpg |
| quality | number | 1 | 否 | 生成的图片质量，取值范围 0~1 |
| exportScale | number | 2 | 否 | 设置导出图片尺寸，值越大图片越清晰 |
| maxScale | number | 3 | 否 | 最大缩放倍数 |
| aspectRatio | string | '1:1' | 否 | 裁剪框宽高比，格式为 `width:height`，如 `1:1`、`16:9`、`3:2` |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### ImgCropper Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| confirm | 确认裁剪并导出图片成功时触发 | `{ tempFilePath: string, width: number, height: number }` | `tempFilePath` 为裁剪后图片的临时路径，`width` 和 `height` 为导出图片的宽高 |
| cancel | 点击取消按钮时触发 | 无 | - |
| imgloaded | 图片加载完成时触发 | `(res: any)` | 图片加载成功的事件对象 |
| imgloaderror | 图片加载失败时触发 | `(err: any)` | 图片加载失败的事件对象 |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: boolean)` | 值为 `false` 表示关闭裁剪组件 |

### ImgCropper Methods

通过 ref 可以获取 `wd-img-cropper` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| revertIsAnimation | `(animation: boolean)` | void | 控制是否使用过渡动画 |
| resetImg | 无 | void | 初始化图片的大小、角度和位置（恢复默认状态） |
| setRoate | `(angle: number)` | void | 控制旋转角度，传入目标角度值 |

## 使用示例

### 示例一：基础头像裁剪

最常用的图片裁剪用法，选择图片后进入裁剪界面，裁剪完成后获取裁剪后的图片临时路径。

```vue
<template>
  <wd-img-cropper
    v-model="show"
    :img-src="src"
    @confirm="handleConfirm"
    @cancel="handleCancel"
    @imgloaderror="imgLoaderror"
    @imgloaded="imgLoaded"
  ></wd-img-cropper>

  <view class="profile">
    <view v-if="!imgSrc" class="img" @click="upload">
      <wd-icon name="camera-filled" custom-class="img-icon"></wd-icon>
    </view>
    <wd-img
      v-if="imgSrc"
      round
      width="200px"
      height="200px"
      :src="imgSrc"
      mode="aspectFit"
      custom-class="profile-img"
      @click="upload"
    />
    <view style="font-size: 14px">点击上传头像</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const src = ref<string>('')
const imgSrc = ref<string>('')
const show = ref<boolean>(false)

function upload() {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      src.value = res.tempFilePaths[0]
      show.value = true
    }
  })
}

function handleConfirm(event: { tempFilePath: string }) {
  const { tempFilePath } = event
  imgSrc.value = tempFilePath
}

function handleCancel() {
  console.log('取消裁剪')
}

function imgLoaderror(res: any) {
  console.log('图片加载失败', res)
}

function imgLoaded(res: any) {
  console.log('图片加载成功', res)
}
</script>

<style lang="scss" scoped>
.profile {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  height: 300px;
}

.img {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.04);
  position: relative;
}

:deep(.img-icon) {
  font-size: 60px;
  color: #fff;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

:deep(.profile-img) {
  border: 1px solid rgba(0, 0, 0, 0.09);
}
</style>
```

### 示例二：自定义裁剪比例

通过 `aspect-ratio` 设置不同的裁剪框宽高比，适配不同业务场景的图片比例需求。

```vue
<template>
  <view class="profile-grid">
    <view v-for="(ratio, index) in ['3:2', '16:9', '16:10']" :key="index" class="profile-item">
      <wd-img-cropper
        v-model="showCustom[index]"
        :img-src="srcCustom[index]"
        :aspect-ratio="ratio"
        @confirm="handleCustomConfirm(index, $event)"
        @cancel="handleCustomCancel"
      ></wd-img-cropper>

      <view v-if="!imgSrcCustom[index]" class="img" @click="uploadCustom(index)">
        <wd-icon name="camera-filled" custom-class="img-icon"></wd-icon>
      </view>
      <wd-img
        v-if="imgSrcCustom[index]"
        width="300px"
        :height="getHeight(ratio)"
        :src="imgSrcCustom[index]"
        mode="aspectFit"
        custom-class="profile-img"
        @click="uploadCustom(index)"
      />
      <view style="font-size: 14px">{{ ratio }}比例裁剪</view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const showCustom = ref<boolean[]>([false, false, false])
const srcCustom = ref<string[]>(['', '', ''])
const imgSrcCustom = ref<string[]>(['', '', ''])

function uploadCustom(index: number) {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      srcCustom.value[index] = res.tempFilePaths[0]
      showCustom.value[index] = true
    }
  })
}

function handleCustomConfirm(index: number, event: { tempFilePath: string }) {
  const { tempFilePath } = event
  imgSrcCustom.value[index] = tempFilePath
}

function handleCustomCancel() {
  console.log('取消裁剪')
}

function getHeight(ratio: string): string {
  const [w, h] = ratio.split(':').map(Number)
  if (ratio === '1:1') return '200px'
  return `${(300 * h) / w}px`
}
</script>

<style lang="scss" scoped>
.profile-grid {
  display: flex;
  flex-direction: column;
  gap: 40px;
  align-items: center;
  padding: 20px;
}

.profile-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.profile-item .img {
  width: 300px;
  height: 169px;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.04);
  position: relative;
}

.profile-item:nth-child(1) .img {
  height: 200px;
}
</style>
```

### 示例三：裁剪后上传

将裁剪后的图片通过上传组件上传到服务器，实现完整的头像裁剪上传流程。

```vue
<template>
  <wd-img-cropper
    v-model="showUpload"
    :img-src="srcUpload"
    @confirm="handleConfirmUpload"
    @cancel="handleCancel"
  ></wd-img-cropper>

  <view class="profile">
    <view v-if="!imgSrcUpload" class="img" @click="uploadWithCrop">
      <wd-icon name="camera-filled" custom-class="img-icon"></wd-icon>
    </view>
    <wd-img
      v-if="imgSrcUpload"
      round
      width="200px"
      height="200px"
      :src="imgSrcUpload"
      mode="aspectFit"
      custom-class="profile-img"
      @click="uploadWithCrop"
    />
    <view style="font-size: 14px">点击上传裁剪后的头像</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useUpload, useToast } from '@/uni_modules/wot-ui-plus'
import { type UploadFileItem } from '@/uni_modules/wot-ui-plus/components/wd-upload/types'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const { startUpload, UPLOAD_STATUS } = useUpload()
const { show: showToast } = useToast()

const srcUpload = ref<string>('')
const imgSrcUpload = ref<string>('')
const showUpload = ref<boolean>(false)

function uploadWithCrop() {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      srcUpload.value = res.tempFilePaths[0]
      showUpload.value = true
    }
  })
}

async function handleConfirmUpload(event: { tempFilePath: string }) {
  const { tempFilePath } = event

  const file: UploadFileItem = {
    url: tempFilePath,
    status: UPLOAD_STATUS.PENDING,
    percent: 0,
    uid: new Date().getTime()
  }

  try {
    await startUpload(file, {
      action: 'https://mockapi.eolink.com/zhTuw2P8c29bc981a741931bdd86eb04dc1e8fd64865cb5/upload',
      onSuccess() {
        imgSrcUpload.value = tempFilePath
        showToast({
          msg: t('shang-chuan-cheng-gong')
        })
      },
      onError() {
        showToast({
          msg: t('shang-chuan-shi-bai')
        })
      },
      onProgress(res) {
        console.log('上传进度:', res.progress)
      }
    })
  } catch (error) {
    console.error('上传失败:', error)
  }
}

function handleCancel() {
  console.log('取消裁剪')
}
</script>

<style lang="scss" scoped>
.profile {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  height: 300px;
}

.img {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.04);
  position: relative;
}

:deep(.img-icon) {
  font-size: 60px;
  color: #fff;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

:deep(.profile-img) {
  border: 1px solid rgba(0, 0, 0, 0.09);
}
</style>
```

## 注意事项

- **全屏模式**：组件以全屏模式展示，打开后会覆盖整个页面，通过 `v-model` 控制显隐
- **Canvas 渲染原理**：裁剪框通过 CSS 样式实现，实际裁剪是通过 Canvas 模拟裁剪区域进行绘制导出的
- **图片尺寸计算**：组件会自动计算图片尺寸，使图片短边完全显示并填满裁剪框。也可通过 `img-width` 和 `img-height` 手动指定
- **旋转角度限制**：旋转角度必须是 90 度的倍数，组件内部会自动修正非 90 倍数的角度值
- **导出图片质量**：`export-scale` 默认为 2，即导出图片的宽高为裁剪框的两倍，可以获得更清晰的图片
- **边缘检测机制**：组件内置了边缘检测逻辑，确保图片在拖动和缩放时始终覆盖裁剪区域，不会出现空白区域
- **动画过渡**：旋转等操作会开启过渡动画（约 400ms），动画结束后自动关闭，可通过 `revertIsAnimation` 方法手动控制
- **防抖处理**：在 Android 平台上，组件对移动操作进行了节流处理（每秒最多 40 帧），以保证流畅的交互体验
- **钉钉小程序兼容**：钉钉小程序中 `canvasToTempFilePath` 返回的文件路径字段为 `filePath` 而非 `tempFilePath`，组件内部已做兼容处理
- **触摸事件阻止**：组件内部使用了 `@touchmove` 阻止默认行为，防止裁剪界面滑动穿透
