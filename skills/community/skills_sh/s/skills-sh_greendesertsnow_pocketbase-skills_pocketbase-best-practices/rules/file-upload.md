---
title: Upload Files Correctly
impact: MEDIUM
impactDescription: Reliable uploads with progress tracking and validation
tags: files, upload, storage, attachments
---

## Upload Files Correctly

File uploads can use plain objects or FormData. Handle large files properly with progress tracking and appropriate error handling.

**Incorrect (naive file upload):**

```javascript
// Missing error handling
async function uploadFile(file) {
  await pb.collection('documents').create({
    title: file.name,
    file: file
  });
  // No error handling, no progress feedback
}

// Uploading without validation
async function uploadAvatar(file) {
  await pb.collection('users').update(userId, {
    avatar: file  // No size/type check - might fail server-side
  });
}

// Base64 upload (inefficient)
async function uploadImage(base64) {
  await pb.collection('images').create({
    image: base64  // Wrong! PocketBase expects File/Blob
  });
}
```

**Correct (proper file uploads):**

```javascript
// Basic upload with object (auto-converts to FormData)
async function uploadDocument(file, metadata) {
  try {
    const record = await pb.collection('documents').create({
      title: metadata.title,
      description: metadata.description,
      file: file  // File object from input
    });
    return record;
  } catch (error) {
    if (error.response?.data?.file) {
      throw new Error(`File error: ${error.response.data.file.message}`);
    }
    throw error;
  }
}

// Upload multiple files
async function uploadGallery(files, albumId) {
  const record = await pb.collection('albums').update(albumId, {
    images: files  // Array of File objects
  });
  return record;
}

// FormData for more control
async function uploadWithProgress(file, onProgress) {
  const formData = new FormData();
  formData.append('title', file.name);
  formData.append('file', file);

  // Using fetch directly for progress (SDK doesn't expose progress)
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`));
      }
    });

    xhr.addEventListener('error', () => reject(new Error('Upload failed')));

    xhr.open('POST', `${pb.baseURL}/api/collections/documents/records`);
    xhr.setRequestHeader('Authorization', pb.authStore.token);
    xhr.send(formData);
  });
}

// Client-side validation before upload
function validateFile(file, options = {}) {
  const {
    maxSize = 10 * 1024 * 1024,  // 10MB default
    allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'],
    maxNameLength = 100
  } = options;

  const errors = [];

  if (file.size > maxSize) {
    errors.push(`File too large. Max: ${maxSize / 1024 / 1024}MB`);
  }

  if (!allowedTypes.includes(file.type)) {
    errors.push(`Invalid file type: ${file.type}`);
  }

  if (file.name.length > maxNameLength) {
    errors.push(`Filename too long`);
  }

  return { valid: errors.length === 0, errors };
}

// Complete upload flow
async function handleFileUpload(inputEvent) {
  const file = inputEvent.target.files[0];
  if (!file) return;

  // Validate
  const validation = validateFile(file, {
    maxSize: 5 * 1024 * 1024,
    allowedTypes: ['image/jpeg', 'image/png']
  });

  if (!validation.valid) {
    showError(validation.errors.join(', '));
    return;
  }

  // Upload with progress
  try {
    setUploading(true);
    const record = await uploadWithProgress(file, setProgress);
    showSuccess('Upload complete!');
    return record;
  } catch (error) {
    showError(error.message);
  } finally {
    setUploading(false);
  }
}
```

**Deleting files:**

```javascript
// Remove specific file(s) from record
await pb.collection('albums').update(albumId, {
  'images-': ['filename1.jpg', 'filename2.jpg']  // Remove these files
});

// Clear all files
await pb.collection('documents').update(docId, {
  file: null  // Removes the file
});
```

Reference: [PocketBase File Upload](https://pocketbase.io/docs/files-handling/)
