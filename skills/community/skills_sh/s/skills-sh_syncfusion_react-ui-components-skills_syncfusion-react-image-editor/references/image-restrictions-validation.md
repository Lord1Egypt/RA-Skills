# Image Restrictions and Validation

## Table of Contents

- [File Type Restrictions](#file-type-restrictions)
- [Size Restrictions](#size-restrictions)
- [Dimension Restrictions](#dimension-restrictions)
- [Validation](#validation)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)

## File Type Restrictions

### Allowed Image Formats

```tsx
const allowedFormats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'];

function isValidFormat(filename: string): boolean {
  const extension = filename.split('.').pop()?.toLowerCase();
  return allowedFormats.includes(extension || '');
}

// Usage
if (isValidFormat('photo.jpg')) {
  // Proceed with image
}
```

### File Extension Validation

```tsx
const fileTypeRestrictions = {
  'jpg': true,
  'jpeg': true,
  'png': true,
  'gif': true,
  'bmp': true,
  'svg': true,
  'webp': true
};

function validateFileExtension(file: File): boolean {
  const extension = file.name.split('.').pop()?.toLowerCase();
  return extension ? fileTypeRestrictions[extension as keyof typeof fileTypeRestrictions] : false;
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
if (fileInput) {
  fileInput.addEventListener('change', (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file && !validateFileExtension(file)) {
      alert('Invalid file format. Please use JPG, PNG, GIF, BMP, or WebP');
    }
  });
}
```

### MIME Type Validation

```tsx
function validateMimeType(file: File): boolean {
  const validMimeTypes = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/bmp',
    'image/svg+xml',
    'image/webp'
  ];
  
  return validMimeTypes.includes(file.type);
}

// Usage
const file = new File([''], 'image.jpg', { type: 'image/jpeg' });
if (validateMimeType(file)) {
  // File is valid
}
```

## Size Restrictions

### Maximum File Size

```tsx
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

function validateFileSize(file: File): { valid: boolean; message?: string } {
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      message: `File size exceeds ${MAX_FILE_SIZE / (1024 * 1024)} MB limit`
    };
  }
  return { valid: true };
}

// Usage
const file = new File(['data'], 'image.jpg', { type: 'image/jpeg' });
const validation = validateFileSize(file);
if (!validation.valid) {
  console.log(validation.message);
}
```

### Minimum File Size

```tsx
const MIN_FILE_SIZE = 1024; // 1 KB

function validateMinimumSize(file: File): boolean {
  return file.size >= MIN_FILE_SIZE;
}
```

### File Size Constraints

```tsx
interface FileSizeConstraints {
  minSize: number;
  maxSize: number;
}

const defaultConstraints: FileSizeConstraints = {
  minSize: 1024,        // 1 KB
  maxSize: 5 * 1024 * 1024  // 5 MB
};

function validateFileSize(file: File, constraints: FileSizeConstraints): boolean {
  return file.size >= constraints.minSize && file.size <= constraints.maxSize;
}
```

## Dimension Restrictions

### Maximum Dimensions

```tsx
interface ImageDimensions {
  maxWidth: number;
  maxHeight: number;
}

const maxDimensions: ImageDimensions = {
  maxWidth: 4000,
  maxHeight: 4000
};

function validateImageDimensions(width: number, height: number, constraints: ImageDimensions): boolean {
  return width <= constraints.maxWidth && height <= constraints.maxHeight;
}

// Usage
const dim = imgObj.getImageDimension();
if (!validateImageDimensions(dim.width, dim.height, maxDimensions)) {
  alert('Image dimensions exceed maximum allowed');
}
```

### Minimum Dimensions

```tsx
interface MinimumDimensions {
  minWidth: number;
  minHeight: number;
}

const minDimensions: MinimumDimensions = {
  minWidth: 100,
  minHeight: 100
};

function validateMinimumDimensions(width: number, height: number, constraints: MinimumDimensions): boolean {
  return width >= constraints.minWidth && height >= constraints.minHeight;
}
```

### Aspect Ratio Validation

```tsx
interface AspectRatioConstraint {
  minRatio: number;
  maxRatio: number;
}

function validateAspectRatio(width: number, height: number, constraint: AspectRatioConstraint): boolean {
  const ratio = width / height;
  return ratio >= constraint.minRatio && ratio <= constraint.maxRatio;
}

// Usage: 4:3 to 16:9
const constraint: AspectRatioConstraint = {
  minRatio: 4 / 3,  // 1.33
  maxRatio: 16 / 9  // 1.78
};

const dim = imgObj.getImageDimension();
if (!validateAspectRatio(dim.width, dim.height, constraint)) {
  alert('Image aspect ratio not supported');
}
```

## Validation

### Complete File Validation

```tsx
interface ValidationResult {
  valid: boolean;
  errors: string[];
}

interface ValidationConstraints {
  allowedFormats: string[];
  maxFileSize: number;
  maxWidth: number;
  maxHeight: number;
  minWidth: number;
  minHeight: number;
}

function validateImage(file: File, constraints: ValidationConstraints): ValidationResult {
  const errors: string[] = [];
  
  // Check file type
  const ext = file.name.split('.').pop()?.toLowerCase();
  if (!ext || !constraints.allowedFormats.includes(ext)) {
    errors.push(`File format not allowed. Use: ${constraints.allowedFormats.join(', ')}`);
  }
  
  // Check file size
  if (file.size > constraints.maxFileSize) {
    errors.push(`File size exceeds ${constraints.maxFileSize / (1024 * 1024)} MB`);
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

// Usage
const constraints: ValidationConstraints = {
  allowedFormats: ['jpg', 'jpeg', 'png', 'webp'],
  maxFileSize: 5 * 1024 * 1024,
  maxWidth: 4000,
  maxHeight: 4000,
  minWidth: 100,
  minHeight: 100
};

const result = validateImage(new File([], 'image.jpg'), constraints);
if (!result.valid) {
  result.errors.forEach(error => console.log(error));
}
```

### Before Opening Image

```tsx
const handleFileOpened = (file: File): void => {
  const result = validateImage(file, constraints);
  
  if (!result.valid) {
    alert('Image validation failed:\n' + result.errors.join('\n'));
    return;
  }
  
  // Load image
  imgObj.open(URL.createObjectURL(file));
};
```

## Error Handling

### Invalid File Detection

```tsx
function handleInvalidFile(error: Error): void {
  console.error('Image loading failed:', error.message);
  
  if (error.message.includes('format')) {
    alert('Unsupported image format');
  } else if (error.message.includes('size')) {
    alert('File is too large');
  } else if (error.message.includes('dimension')) {
    alert('Image dimensions invalid');
  } else {
    alert('Failed to load image');
  }
}
```

### Graceful Degradation

```tsx
async function loadImageWithFallback(url: string, fallbackUrl?: string): Promise<void> {
  try {
    imgObj.open(url);
  } catch (error) {
    console.error('Failed to load image:', error);
    
    if (fallbackUrl) {
      try {
        imgObj.open(fallbackUrl);
      } catch (fallbackError) {
        alert('Failed to load both primary and fallback image');
      }
    }
  }
}
```

## Advanced Patterns

### Custom Validation Rules

```tsx
interface ValidationRule {
  name: string;
  test: (file: File, dimensions?: any) => boolean;
  message: string;
}

const customRules: ValidationRule[] = [
  {
    name: 'format',
    test: (file) => ['jpg', 'png'].includes(file.name.split('.').pop()?.toLowerCase() || ''),
    message: 'Only JPG and PNG allowed'
  },
  {
    name: 'size',
    test: (file) => file.size <= 2 * 1024 * 1024,
    message: 'File must be under 2 MB'
  },
  {
    name: 'dimensions',
    test: (file, dim) => dim?.width <= 2000 && dim?.height <= 2000,
    message: 'Image must be under 2000x2000 pixels'
  }
];

function applyCustomValidation(file: File, dimensions?: any): ValidationResult {
  const errors: string[] = [];
  
  customRules.forEach(rule => {
    if (!rule.test(file, dimensions)) {
      errors.push(rule.message);
    }
  });
  
  return {
    valid: errors.length === 0,
    errors
  };
}
```

### Validation Presets

```tsx
enum ValidationPreset {
  Web = 'web',
  Mobile = 'mobile',
  Print = 'print',
  Social = 'social'
}

const presets: Record<ValidationPreset, ValidationConstraints> = {
  [ValidationPreset.Web]: {
    allowedFormats: ['jpg', 'png', 'webp'],
    maxFileSize: 2 * 1024 * 1024,
    maxWidth: 2000,
    maxHeight: 2000,
    minWidth: 200,
    minHeight: 200
  },
  [ValidationPreset.Mobile]: {
    allowedFormats: ['jpg', 'png', 'webp'],
    maxFileSize: 1 * 1024 * 1024,
    maxWidth: 1200,
    maxHeight: 1600,
    minWidth: 100,
    minHeight: 100
  },
  [ValidationPreset.Print]: {
    allowedFormats: ['jpg', 'png', 'tiff'],
    maxFileSize: 50 * 1024 * 1024,
    maxWidth: 8000,
    maxHeight: 8000,
    minWidth: 800,
    minHeight: 800
  },
  [ValidationPreset.Social]: {
    allowedFormats: ['jpg', 'png'],
    maxFileSize: 5 * 1024 * 1024,
    maxWidth: 1200,
    maxHeight: 1200,
    minWidth: 400,
    minHeight: 400
  }
};

function getPreset(preset: ValidationPreset): ValidationConstraints {
  return presets[preset];
}
```

### Batch Validation

```tsx
async function validateBatch(files: File[]): Promise<Array<{ file: File; valid: boolean; errors: string[] }>> {
  const constraints = presets[ValidationPreset.Web];
  
  return files.map(file => ({
    file,
    ...validateImage(file, constraints)
  }));
}

// Usage
const files = Array.from(document.querySelector('input[type="file"]')?.files || []);
const results = await validateBatch(files);

results.forEach(result => {
  if (!result.valid) {
    console.log(`${result.file.name}: ${result.errors.join(', ')}`);
  }
});
```

### Validation with Warnings

```tsx
interface ValidationSeverity {
  level: 'error' | 'warning' | 'info';
  message: string;
}

function validateWithSeverity(file: File, constraints: ValidationConstraints): ValidationSeverity[] {
  const issues: ValidationSeverity[] = [];
  
  // Errors
  if (file.size > constraints.maxFileSize) {
    issues.push({
      level: 'error',
      message: 'File too large'
    });
  }
  
  // Warnings
  if (file.size > constraints.maxFileSize * 0.8) {
    issues.push({
      level: 'warning',
      message: 'File is approaching size limit'
    });
  }
  
  // Info
  issues.push({
    level: 'info',
    message: `File size: ${(file.size / 1024).toFixed(2)} KB`
  });
  
  return issues;
}
```
