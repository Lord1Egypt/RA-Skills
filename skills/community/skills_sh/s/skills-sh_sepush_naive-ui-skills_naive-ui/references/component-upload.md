---
name: component-upload
description: File upload component with custom requests, drag-drop, and file validation
---

# Upload

File upload component with support for drag-drop, file validation, custom requests, and multiple file handling.

## Basic Usage

```vue
<script setup lang="ts">
import { ref } from 'vue'
import type { UploadFileInfo } from 'naive-ui'

const fileList = ref<UploadFileInfo[]>([])

const handleChange = (options: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  console.log('File changed:', options.file)
}

const handleFinish = (options: { file: UploadFileInfo; event?: ProgressEvent }) => {
  console.log('Upload finished:', options.file)
}
</script>

<template>
  <n-upload
    v-model:file-list="fileList"
    action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
    @change="handleChange"
    @finish="handleFinish"
  >
    <n-button>Upload File</n-button>
  </n-upload>
</template>
```

## Multiple Files

```vue
<template>
  <n-upload
    v-model:file-list="fileList"
    action="/api/upload"
    multiple
    :max="5"
    :default-upload="false"
  >
    <n-button>Select Files</nbutton>
  </n-upload>
</template>
```

## File Types & Size

```vue
<script setup lang="ts">
const beforeUpload = (data: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  // Check file size (max 5MB)
  if (data.file.file?.size && data.file.file.size > 5 * 1024 * 1024) {
    message.error('File size should not exceed 5MB')
    return false
  }

  // Check file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(data.file.type || '')) {
    message.error('Only JPG, PNG and GIF images are allowed')
    return false
  }

  return true
}
</script>

<template>
  <n-upload
    action="/api/upload"
    accept="image/*"
    :max-size="5242880"
    @before-upload="beforeUpload"
  >
    <n-button>Upload Image</n-button>
  </n-upload>
</template>
```

## Custom Request

For complete control over the upload process:

```vue
<script setup lang="ts">
import type { UploadCustomRequestOptions } from 'naive-ui'

const customRequest = async ({
  file,
  data,
  headers,
  withCredentials,
  action,
  onFinish,
  onError,
  onProgress
}: UploadCustomRequestOptions) => {
  try {
    const formData = new FormData()
    formData.append('file', file.file as File)

    // Add additional data
    if (data) {
      Object.keys(data).forEach((key) => {
        formData.append(key, data[key])
      })
    }

    const response = await fetch(action as string, {
      method: 'POST',
      body: formData,
      headers: headers as HeadersInit,
      credentials: withCredentials ? 'include' : 'same-origin'
    })

    if (response.ok) {
      const result = await response.json()
      onFinish(result)
    } else {
      onError()
    }
  } catch (error) {
    onError()
  }
}
</script>

<template>
  <n-upload
    action="/api/upload"
    :custom-request="customRequest"
  >
    <n-button>Custom Upload</n-button>
  </n-upload>
</template>
```

## Drag & Drop

```vue
<template>
  <n-upload
    v-model:file-list="fileList"
    action="/api/upload"
    multiple
    directory-dnd
  >
    <n-upload-dragger>
      <div style="margin-bottom: 12px">
        <n-icon size="48" :depth="3">
          <ArchiveIcon />
        </n-icon>
      </div>
      <n-text style="font-size: 16px">
        Click or drag files to this area
      </n-text>
      <n-p depth="3" style="margin: 8px 0 0 0">
        Support for single or bulk upload. Strictly prohibited from uploading company data.
      </n-p>
    </n-upload-dragger>
  </n-upload>
</template>
```

## Image Preview

```vue
<script setup lang="ts">
const fileList = ref<UploadFileInfo[]>([
  {
    id: 'a',
    name: 'image.png',
    status: 'finished',
    url: 'https://example.com/image.png'
  }
])

const previewFileList = computed(() =>
  fileList.value.map(file => ({
    src: file.url,
    alt: file.name
  }))
)
</script>

<template>
  <n-upload
    v-model:file-list="fileList"
    action="/api/upload"
    list-type="image-card"
    :max="5"
  />
  <n-image-group>
    <n-space>
      <n-image
        v-for="file in previewFileList"
        :key="file.src"
        width="100"
        :src="file.src"
      />
    </n-space>
  </n-image-group>
</template>
```

## Controlled Upload (Manual Trigger)

```vue
<script setup lang="ts">
import type { UploadInst } from 'naive-ui'

const uploadRef = ref<UploadInst | null>(null)
const fileList = ref<UploadFileInfo[]>([])

const handleUpload = () => {
  uploadRef.value?.submit()
}

const handleClear = () => {
  fileList.value = []
}
</script>

<template>
  <n-upload
    ref="uploadRef"
    v-model:file-list="fileList"
    action="/api/upload"
    multiple
    :default-upload="false"
  >
    <n-button>Select Files</n-button>
  </n-upload>

  <n-space style="margin-top: 12px">
    <n-button type="primary" @click="handleUpload">
      Upload All
    </n-button>
    <n-button @click="handleClear">
      Clear All
    </n-button>
  </n-space>
</template>
```

## Form Integration

```vue
<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'

const formRef = ref<FormInst | null>(null)
const formValue = ref({
  name: '',
  files: [] as UploadFileInfo[]
})

const rules: FormRules = {
  name: { required: true, message: 'Name is required' },
  files: {
    required: true,
    validator: (rule, value: UploadFileInfo[]) => {
      if (!value || value.length === 0) {
        return new Error('Please upload at least one file')
      }
      // Check if all files are uploaded
      const hasPending = value.some(f => f.status === 'pending')
      if (hasPending) {
        return new Error('Please wait for all files to finish uploading')
      }
      return true
    }
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    // All files uploaded, submit form
    await api.submitForm({
      name: formValue.value.name,
      fileIds: formValue.value.files.map(f => f.id)
    })
  } catch (errors) {
    console.error('Validation failed:', errors)
  }
}
</script>

<template>
  <n-form ref="formRef" :model="formValue" :rules="rules">
    <n-form-item label="Name" path="name">
      <n-input v-model:value="formValue.name" />
    </n-form-item>
    <n-form-item label="Files" path="files">
      <n-upload
        v-model:file-list="formValue.files"
        action="/api/upload"
        multiple
      >
        <n-button>Upload Files</n-button>
      </n-upload>
    </n-form-item>
  </n-form>
  <n-button type="primary" @click="handleSubmit">Submit</n-button>
</template>
```

## Chunked Upload (Large Files)

```vue
<script setup lang="ts">
const CHUNK_SIZE = 1024 * 1024 // 1MB chunks

const customRequest = async (options: UploadCustomRequestOptions) => {
  const { file, onProgress, onFinish, onError } = options
  const fileObj = file.file as File

  const chunks = Math.ceil(fileObj.size / CHUNK_SIZE)
  const uploadId = generateUploadId()

  try {
    for (let i = 0; i < chunks; i++) {
      const start = i * CHUNK_SIZE
      const end = Math.min(start + CHUNK_SIZE, fileObj.size)
      const chunk = fileObj.slice(start, end)

      const formData = new FormData()
      formData.append('chunk', chunk)
      formData.append('index', String(i))
      formData.append('total', String(chunks))
      formData.append('uploadId', uploadId)

      await fetch('/api/upload-chunk', {
        method: 'POST',
        body: formData
      })

      onProgress({ percent: Math.round((i + 1) / chunks * 100) })
    }

    // Merge chunks
    await fetch('/api/merge-chunks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ uploadId, filename: fileObj.name })
    })

    onFinish()
  } catch (error) {
    onError()
  }
}
</script>
```

## Key Types

```ts
import type {
  UploadProps,
  UploadInst,
  UploadFileInfo,
  UploadCustomRequestOptions,
  UploadSettledFileInfo
} from 'naive-ui'
```

## FileInfo Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique file ID |
| `name` | `string` | File name |
| `status` | `'pending' \| 'uploading' \| 'finished' \| 'removed' \| 'error'` | Upload status |
| `url` | `string` | File URL (after upload) |
| `thumbnailUrl` | `string` | Thumbnail URL |
| `type` | `string` | MIME type |
| `percentage` | `number` | Upload progress |

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Accept not working | Using file extensions instead of MIME types | Use MIME types like `image/*`, `.jpg,.png` |
| onError not called | Error handling in custom request | Call `onError()` explicitly in catch block |
| Files not showing | `v-model:file-list` not bound | Ensure two-way binding with file-list |
| Base64 URL opens blank | Browser security | Convert to blob URL or download properly |

## Best Practices

1. **Always validate file type and size** on both client and server
2. **Use `default-upload="false"`** for forms requiring confirmation
3. **Show upload progress** for large files
4. **Handle errors gracefully** with retry options
5. **Use chunked upload** for files larger than 10MB


