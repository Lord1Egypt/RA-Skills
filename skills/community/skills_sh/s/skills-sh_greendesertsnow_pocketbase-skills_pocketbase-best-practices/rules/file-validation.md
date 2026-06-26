---
title: Validate File Uploads
impact: MEDIUM
impactDescription: Prevents invalid uploads, improves security and UX
tags: files, validation, security, upload
---

## Validate File Uploads

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
