# File Handling

**Impact: MEDIUM**

File uploads, URL generation, thumbnail creation, and validation patterns.

---

## 1. Generate File URLs Correctly

**Impact: MEDIUM (Proper URLs with thumbnails and access control)**

Use the SDK's `getURL` method to generate proper file URLs with thumbnail support and access tokens for protected files.

**Incorrect (manually constructing URLs):**

```javascript
// Hardcoded URL construction - brittle
const imageUrl = `http://localhost:8090/api/files/${record.collectionId}/${record.id}/${record.image}`;

// Missing token for protected files
const privateUrl = pb.files.getURL(record, record.document);
// Returns URL but file access denied if protected!

// Wrong thumbnail syntax
const thumb = `${imageUrl}?thumb=100x100`;  // Wrong format
```

**Correct (using SDK methods):**

```javascript
// Basic file URL
const imageUrl = pb.files.getURL(record, record.image);
// Returns: http://host/api/files/COLLECTION/RECORD_ID/filename.jpg

// With thumbnail (for images only)
const thumbUrl = pb.files.getURL(record, record.image, {
  thumb: '100x100'  // Width x Height
});

// Thumbnail options
const thumbs = {
  square: pb.files.getURL(record, record.image, { thumb: '100x100' }),
  fit: pb.files.getURL(record, record.image, { thumb: '100x0' }),     // Fit width
  fitHeight: pb.files.getURL(record, record.image, { thumb: '0x100' }), // Fit height
  crop: pb.files.getURL(record, record.image, { thumb: '100x100t' }), // Top crop
  cropBottom: pb.files.getURL(record, record.image, { thumb: '100x100b' }), // Bottom
  force: pb.files.getURL(record, record.image, { thumb: '100x100f' }), // Force exact
};

// Protected files (require auth)
async function getProtectedFileUrl(record, filename) {
  // Get file access token (valid for limited time)
  const token = await pb.files.getToken();

  // Include token in URL
  return pb.files.getURL(record, filename, { token });
}

// Example with protected document
async function downloadDocument(record) {
  const token = await pb.files.getToken();
  const url = pb.files.getURL(record, record.document, { token });

  // Token is appended: ...?token=xxx
  window.open(url, '_blank');
}
```

**React component example:**

```jsx
function UserAvatar({ user, size = 50 }) {
  if (!user.avatar) {
    return <DefaultAvatar size={size} />;
  }

  const avatarUrl = pb.files.getURL(user, user.avatar, {
    thumb: `${size}x${size}`
  });

  return (
    <img
      src={avatarUrl}
      alt={user.name}
      width={size}
      height={size}
      loading="lazy"
    />
  );
}

function ImageGallery({ record }) {
  // Record has multiple images
  const images = record.images || [];

  return (
    <div className="gallery">
      {images.map((filename, index) => (
        <img
          key={filename}
          src={pb.files.getURL(record, filename, { thumb: '200x200' })}
          onClick={() => openFullSize(record, filename)}
          loading="lazy"
        />
      ))}
    </div>
  );
}

function openFullSize(record, filename) {
  const fullUrl = pb.files.getURL(record, filename);
  window.open(fullUrl, '_blank');
}
```

**Handling file URLs in lists:**

```javascript
// Efficiently generate URLs for list of records
const posts = await pb.collection('posts').getList(1, 20, {
  expand: 'author'
});

const postsWithUrls = posts.items.map(post => ({
  ...post,
  thumbnailUrl: post.image
    ? pb.files.getURL(post, post.image, { thumb: '300x200' })
    : null,
  authorAvatarUrl: post.expand?.author?.avatar
    ? pb.files.getURL(post.expand.author, post.expand.author.avatar, { thumb: '40x40' })
    : null
}));
```

**Thumbnail format reference:**

| Format | Description |
|--------|-------------|
| `WxH` | Fit within dimensions |
| `Wx0` | Fit width, auto height |
| `0xH` | Auto width, fit height |
| `WxHt` | Crop from top |
| `WxHb` | Crop from bottom |
| `WxHf` | Force exact dimensions |

**Performance and caching:**

```javascript
// File URLs are effectively immutable (randomized filenames on upload).
// This makes them ideal for aggressive caching.

// Configure Cache-Control via reverse proxy (Nginx/Caddy):
// location /api/files/ { add_header Cache-Control "public, immutable, max-age=86400"; }

// Thumbnails are generated on first request and cached by PocketBase.
// Pre-generate expected thumb sizes after upload to avoid cold-start latency:
async function uploadWithThumbs(record, file) {
  const updated = await pb.collection('posts').update(record.id, { image: file });

  // Pre-warm thumbnail cache by requesting expected sizes
  const sizes = ['100x100', '300x200', '800x600'];
  await Promise.all(sizes.map(size =>
    fetch(pb.files.getURL(updated, updated.image, { thumb: size }))
  ));

  return updated;
}
```

**S3 file serving optimization:**

When using S3 storage, PocketBase proxies all file requests through the server. For better performance with public files, serve directly from your S3 CDN:

```javascript
// Default: All file requests proxy through PocketBase
const url = pb.files.getURL(record, record.image);
// -> https://myapp.com/api/files/COLLECTION/ID/filename.jpg (proxied)

// For public files with S3 + CDN, construct CDN URL directly:
const cdnBase = 'https://cdn.myapp.com';  // Your S3 CDN domain
const cdnUrl = `${cdnBase}/${record.collectionId}/${record.id}/${record.image}`;
// Bypasses PocketBase, served directly from CDN edge

// NOTE: This only works for public files (no access token needed).
// Protected files must go through PocketBase for token validation.
```

Reference: [PocketBase Files](https://pocketbase.io/docs/files-handling/)

> **Note (JS SDK v0.26.7):** `pb.files.getURL()` now serializes query parameters the same way as the fetch methods — passing `null` or `undefined` as a query param value is silently skipped from the generated URL, so you no longer need to guard optional params before passing them to `getURL()`.

## 2. Upload Files Correctly

**Impact: MEDIUM (Reliable uploads with progress tracking and validation)**

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

## 3. Validate File Uploads

**Impact: MEDIUM (Prevents invalid uploads, improves security and UX)**

Validate files on both client and server side. Client validation improves UX; server validation (via collection settings) enforces security.

**Incorrect (no validation):**

```javascript
// Accepting any file without checks
async function uploadFile(file) {
  return pb.collection('uploads').create({ file });
  // Could upload 1GB executable!
}

// Only checking extension (easily bypassed)
function validateFile(file) {
  const ext = file.name.split('.').pop();
  return ['jpg', 'png'].includes(ext);
  // User can rename virus.exe to virus.jpg
}

// Client-only validation (can be bypassed)
async function uploadAvatar(file) {
  if (file.size > 1024 * 1024) {
    throw new Error('Too large');
  }
  // Attacker can bypass this with dev tools
  return pb.collection('users').update(userId, { avatar: file });
}
```

**Correct (comprehensive validation):**

```javascript
// 1. Configure server-side validation in collection settings
// In Admin UI or via API:
const collectionConfig = {
  schema: [
    {
      name: 'avatar',
      type: 'file',
      options: {
        maxSelect: 1,           // Single file only
        maxSize: 5242880,       // 5MB in bytes
        mimeTypes: [            // Allowed types
          'image/jpeg',
          'image/png',
          'image/gif',
          'image/webp'
        ],
        thumbs: ['100x100', '200x200']  // Auto-generate thumbnails
      }
    },
    {
      name: 'documents',
      type: 'file',
      options: {
        maxSelect: 10,
        maxSize: 10485760,  // 10MB
        mimeTypes: [
          'application/pdf',
          'application/msword',
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
      }
    }
  ]
};

// 2. Client-side validation for better UX
const FILE_CONSTRAINTS = {
  avatar: {
    maxSize: 5 * 1024 * 1024,
    allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    maxFiles: 1
  },
  documents: {
    maxSize: 10 * 1024 * 1024,
    allowedTypes: ['application/pdf'],
    maxFiles: 10
  }
};

function validateFiles(files, constraintKey) {
  const constraints = FILE_CONSTRAINTS[constraintKey];
  const errors = [];
  const validFiles = [];

  if (files.length > constraints.maxFiles) {
    errors.push(`Maximum ${constraints.maxFiles} file(s) allowed`);
  }

  for (const file of files) {
    const fileErrors = [];

    // Check size
    if (file.size > constraints.maxSize) {
      const maxMB = constraints.maxSize / 1024 / 1024;
      fileErrors.push(`${file.name}: exceeds ${maxMB}MB limit`);
    }

    // Check MIME type (more reliable than extension, but still spoofable)
    // Client-side file.type is based on extension, not file content.
    // Always enforce mimeTypes in PocketBase collection settings for server-side validation.
    if (!constraints.allowedTypes.includes(file.type)) {
      fileErrors.push(`${file.name}: invalid file type (${file.type || 'unknown'})`);
    }

    // Check for suspicious patterns
    if (file.name.includes('..') || file.name.includes('/')) {
      fileErrors.push(`${file.name}: invalid filename`);
    }

    if (fileErrors.length === 0) {
      validFiles.push(file);
    } else {
      errors.push(...fileErrors);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    validFiles
  };
}

// 3. Complete upload with validation
async function handleAvatarUpload(inputElement) {
  const files = Array.from(inputElement.files);

  // Client validation
  const validation = validateFiles(files, 'avatar');
  if (!validation.valid) {
    showErrors(validation.errors);
    return null;
  }

  // Upload (server will also validate)
  try {
    const updated = await pb.collection('users').update(userId, {
      avatar: validation.validFiles[0]
    });
    showSuccess('Avatar updated!');
    return updated;
  } catch (error) {
    // Handle server validation errors
    if (error.response?.data?.avatar) {
      showError(error.response.data.avatar.message);
    } else {
      showError('Upload failed');
    }
    return null;
  }
}

// 4. Image-specific validation
async function validateImage(file, options = {}) {
  const { minWidth = 0, minHeight = 0, maxWidth = Infinity, maxHeight = Infinity } = options;

  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const errors = [];

      if (img.width < minWidth || img.height < minHeight) {
        errors.push(`Image must be at least ${minWidth}x${minHeight}px`);
      }
      if (img.width > maxWidth || img.height > maxHeight) {
        errors.push(`Image must be at most ${maxWidth}x${maxHeight}px`);
      }

      resolve({ valid: errors.length === 0, errors, width: img.width, height: img.height });
    };
    img.onerror = () => resolve({ valid: false, errors: ['Invalid image file'] });
    img.src = URL.createObjectURL(file);
  });
}
```

Reference: [PocketBase Files Configuration](https://pocketbase.io/docs/files-handling/)

