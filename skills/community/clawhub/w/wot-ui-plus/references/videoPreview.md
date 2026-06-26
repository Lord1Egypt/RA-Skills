# VideoPreview 视频预览


## 组件概况

VideoPreview 视频预览组件是一个全屏视频播放预览组件，以全屏弹窗的形式展示视频内容。用户通过调用组件实例的 `open` 方法并传入视频信息（视频地址、封面、标题），即可在全屏模式下预览播放视频。组件内置关闭按钮，点击视频外区域或关闭按钮即可关闭预览。该组件常用于图片/视频混合预览场景、聊天消息中的视频预览、商品详情中的视频播放等需要临时全屏预览视频的场景。

## 核心功能描述

- **全屏预览**：以全屏弹窗方式展示视频，覆盖整个屏幕，沉浸式的预览体验
- **视频播放**：内置原生 `<video>` 组件，支持播放、暂停、进度控制等标准视频播放功能
- **视频封面**：支持通过 `poster` 属性设置视频封面图，在视频未播放前展示
- **视频标题**：支持通过 `title` 属性设置视频标题，显示在视频播放器顶部
- **播放按钮居中**：播放按钮默认居中显示（`play-btn-position="center"`），符合用户操作习惯
- **禁用进度手势**：默认禁用进度拖拽手势（`enable-progress-gesture="false"`），防止误操作
- **原生渲染**：启用原生渲染（`enableNative="true"`），提升播放性能和兼容性
- **点击关闭**：点击视频外区域即可关闭预览弹窗
- **关闭按钮**：右上角提供关闭图标按钮，点击可关闭预览
- **页面滚动锁定**：在 H5 环境下，打开预览时自动锁定页面滚动，防止页面滚动穿透
- **资源清理**：关闭预览后自动清空视频数据，释放资源

## 适用业务场景

- **图片/视频混合预览**：在图片预览组件中嵌入视频预览，实现多媒体统一预览
- **聊天消息视频预览**：在聊天应用中预览好友发送的视频消息
- **商品详情视频**：在电商应用中预览商品展示视频
- **短视频浏览**：在信息流中点击缩略图全屏预览短视频
- **用户动态视频**：在社交动态中预览用户上传的视频内容
- **教程视频预览**：在教程或帮助文档中快速预览操作步骤视频
- **活动视频预览**：在活动页面中预览活动宣传视频

## API

### VideoPreview Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### VideoPreview Methods

通过 ref 可以获取 `wd-video-preview` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| open | `(video: PreviewVideo)` | void | 打开视频预览弹窗，传入视频信息对象 |
| close | 无 | void | 关闭视频预览弹窗 |

### PreviewVideo 类型

```ts
interface PreviewVideo {
  url: string      // 视频资源地址（必填）
  poster?: string  // 视频封面图片地址（可选）
  title?: string   // 视频标题（可选）
}
```

### VideoPreview Slots

`wd-video-preview` 不提供自定义插槽。

### VideoPreview Events

`wd-video-preview` 不暴露额外事件。

## 使用示例

### 示例一：基础视频预览

通过 ref 调用组件的 `open` 方法，传入视频地址即可打开视频预览。

```vue
<template>
  <wd-button type="primary" @click="previewVideo">预览视频</wd-button>

  <wd-video-preview ref="videoPreviewRef" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { VideoPreviewInstance } from '@/uni_modules/wot-ui-plus/components/wd-video-preview/types'

const videoPreviewRef = ref<VideoPreviewInstance>()

function previewVideo() {
  videoPreviewRef.value?.open({
    url: 'https://example.com/video.mp4',
    poster: 'https://example.com/poster.jpg',
    title: '示例视频'
  })
}
</script>
```

### 示例二：图片与视频混合预览

在一个预览场景中同时支持图片和视频的预览，根据资源类型选择对应的预览方式。

```vue
<template>
  <view class="media-gallery">
    <view v-for="(item, index) in mediaList" :key="index" class="media-item" @click="handlePreview(item)">
      <wd-image v-if="item.type === 'image'" :src="item.url" width="100px" height="100px" />
      <view v-else class="video-thumb">
        <wd-image :src="item.poster || item.url" width="100px" height="100px" />
        <wd-icon name="play" custom-class="play-icon" />
      </view>
    </view>
  </view>

  <wd-video-preview ref="videoPreviewRef" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { VideoPreviewInstance, PreviewVideo } from '@/uni_modules/wot-ui-plus/components/wd-video-preview/types'

interface MediaItem {
  type: 'image' | 'video'
  url: string
  poster?: string
  title?: string
}

const mediaList = ref<MediaItem[]>([
  { type: 'image', url: 'https://example.com/image1.jpg' },
  { type: 'image', url: 'https://example.com/image2.jpg' },
  {
    type: 'video',
    url: 'https://example.com/video1.mp4',
    poster: 'https://example.com/poster1.jpg',
    title: '产品演示视频'
  },
  {
    type: 'video',
    url: 'https://example.com/video2.mp4',
    poster: 'https://example.com/poster2.jpg',
    title: '使用教程视频'
  }
])

const videoPreviewRef = ref<VideoPreviewInstance>()

function handlePreview(item: MediaItem) {
  if (item.type === 'video') {
    const videoInfo: PreviewVideo = {
      url: item.url,
      poster: item.poster,
      title: item.title
    }
    videoPreviewRef.value?.open(videoInfo)
  } else {
    uni.previewImage({
      urls: [item.url]
    })
  }
}
</script>

<style lang="scss" scoped>
.media-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px;
}

.media-item {
  width: 100px;
  height: 100px;
}

.video-thumb {
  position: relative;
}

:deep(.play-icon) {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 30px;
  color: #fff;
  opacity: 0.8;
}
</style>
```

### 示例三：聊天消息中的视频预览

在聊天消息列表中，点击视频消息进行全屏预览播放。

```vue
<template>
  <view class="chat-messages">
    <view
      v-for="(message, index) in messages"
      :key="index"
      class="message-item"
      :class="{ 'is-video': message.type === 'video' }"
      @click="handleMessageClick(message)"
    >
      <!-- 文本消息 -->
      <view v-if="message.type === 'text'" class="text-message">
        {{ message.content }}
      </view>

      <!-- 视频消息 -->
      <view v-else-if="message.type === 'video'" class="video-message">
        <image class="video-cover" :src="message.poster" mode="aspectFill" />
        <wd-icon name="play" custom-class="play-btn" />
        <view class="video-duration">{{ message.duration }}</view>
      </view>
    </view>
  </view>

  <wd-video-preview ref="videoPreviewRef" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { VideoPreviewInstance } from '@/uni_modules/wot-ui-plus/components/wd-video-preview/types'

interface ChatMessage {
  type: 'text' | 'video'
  content?: string
  url?: string
  poster?: string
  title?: string
  duration?: string
}

const messages = ref<ChatMessage[]>([
  { type: 'text', content: '你好，请看这个视频' },
  {
    type: 'video',
    url: 'https://example.com/chat-video.mp4',
    poster: 'https://example.com/chat-poster.jpg',
    title: '聊天视频',
    duration: '01:30'
  },
  { type: 'text', content: '你觉得怎么样？' }
])

const videoPreviewRef = ref<VideoPreviewInstance>()

function handleMessageClick(message: ChatMessage) {
  if (message.type === 'video' && message.url) {
    videoPreviewRef.value?.open({
      url: message.url,
      poster: message.poster,
      title: message.title
    })
  }
}
</script>

<style lang="scss" scoped>
.chat-messages {
  padding: 16px;
}

.message-item {
  margin-bottom: 16px;
}

.text-message {
  background-color: #f0f0f0;
  padding: 10px 14px;
  border-radius: 12px;
  max-width: 80%;
  display: inline-block;
}

.video-message {
  position: relative;
  width: 200px;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
}

.video-cover {
  width: 100%;
  height: 100%;
}

:deep(.play-btn) {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 40px;
  color: #fff;
  opacity: 0.9;
}

.video-duration {
  position: absolute;
  bottom: 6px;
  right: 8px;
  font-size: 12px;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 2px 6px;
  border-radius: 4px;
}
</style>
```

## 注意事项

- **全屏覆盖**：组件打开后会以全屏弹窗形式覆盖整个页面，不适合与其他内容同时展示
- **关闭方式**：用户可以通过点击视频外的区域或右上角关闭按钮关闭预览弹窗
- **视频资源地址必填**：调用 `open` 方法时，`url` 字段为必填项，否则会显示空白预览
- **封面和标题可选**：`poster` 和 `title` 为可选字段，不传时视频播放器不会显示封面和标题
- **关闭后资源清理**：组件在关闭后会自动清空视频数据（`url`、`poster`、`title`），释放播放器资源
- **H5 滚动锁定**：在 H5 环境下，组件使用 `useLockScroll` composable 在预览打开时锁定页面滚动，防止页面滚动穿透
- **原生播放器**：组件使用原生 `<video>` 元素进行播放，具体播放能力（如倍速、画中画等）取决于平台和浏览器支持
- **进度手势禁用**：默认禁用了进度拖拽手势，如需启用可自行修改组件源码中的 `enable-progress-gesture` 属性
- **多视频切换**：连续调用 `open` 方法可以切换不同的视频进行预览，每次打开都会替换之前的视频数据
- **平台兼容性**：视频播放功能在不同平台（微信小程序、H5、App）上的表现可能略有差异，建议在目标平台上进行测试验证
