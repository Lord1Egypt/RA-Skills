---
name: component-feedback
description: Message, Notification, Dialog, and LoadingBar programmatic APIs
---

# Feedback Components

## Message

> **Prerequisite:** To use `message`, wrap the calling component inside `n-message-provider` and use `useMessage` to get the API.
> **Warning:** To use it outside setup, mount the return value of `useMessage` to `window` in top-level setup first.

```vue
<script setup lang="ts">
const message = useMessage()

message.success('Operation successful')
message.error('Something went wrong')
message.warning('Warning message')
message.info('Info message')
message.loading('Loading...')

// With duration
message.success('Will disappear in 3s', { duration: 3000 })

// Closable
message.info('Click to close', { closable: true })
</script>
```

## Dialog

> **Prerequisite:** To use `dialog`, wrap the calling component inside `n-dialog-provider` and use `useDialog` to get the API.

```vue
<script setup lang="ts">
const dialog = useDialog()

dialog.confirm({
  title: 'Confirm',
  content: 'Are you sure?',
  positiveText: 'Yes',
  negativeText: 'No',
  onPositiveClick: () => {
    message.success('Confirmed')
  }
})

dialog.warning({
  title: 'Warning',
  content: 'This action cannot be undone'
})

dialog.error({
  title: 'Error',
  content: 'Operation failed'
})
</script>
```

## Notification

> **Prerequisite:** To use `notification`, wrap the calling component inside `n-notification-provider` and use `useNotification` to get the API.

```vue
<script setup lang="ts">
const notification = useNotification()

notification.success({
  title: 'Success',
  content: 'Operation completed',
  duration: 3000
})

notification.error({
  title: 'Error',
  content: 'Something went wrong',
  meta: '2024-01-01',
  action: () => h(NButton, { text: true }, { default: () => 'Retry' })
})
</script>
```

## LoadingBar

> **Prerequisite:** To use `loading-bar`, wrap the calling component inside `n-loading-bar-provider` and inject `loadingBar`.

```vue
<script setup lang="ts">
const loadingBar = useLoadingBar()

loadingBar.start()
loadingBar.finish()
loadingBar.error()
</script>
```

## Global Setup

```ts
// main.ts
import { createApp } from 'vue'
import {
  create,
  NMessageProvider,
  NDialogProvider,
  NNotificationProvider,
  NLoadingBarProvider
} from 'naive-ui'
import App from './App.vue'

const app = createApp(App)

app.use(create({
  providers: [
    NMessageProvider,
    NDialogProvider,
    NNotificationProvider,
    NLoadingBarProvider
  ]
}))
```


