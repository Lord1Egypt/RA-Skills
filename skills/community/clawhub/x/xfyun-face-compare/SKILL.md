---
name: face-compare
description: Compare two face images and return similarity score using iFlytek Face Recognition API.
homepage: https://www.xfyun.cn/doc/face/xf-silent-in-vivo-detection/API.html
metadata:
  {
    "openclaw":
      {
        "emoji": "👤",
        "requires": {
          "bins": ["python3"],
          "env": ["XF_FACE_APP_ID", "XF_FACE_API_KEY", "XF_FACE_API_SECRET"]
        },
        "primaryEnv": "XF_FACE_APP_ID"
      }
  }
---

# 👤 Face Compare

Compare two face images and calculate their similarity score using iFlytek's advanced face recognition technology.

Designed for identity verification, face matching, and security authentication scenarios.

---

## ✨ Features

- High-accuracy face comparison
- Base64 image encoding support
- Multiple image format support (jpg, png, bmp)
- Detailed similarity scoring
- One-command execution

---

## 🚀 Usage

```bash
python {baseDir}/scripts/index.py "<image1_path>" "<image2_path>"
```

Example:

```
python {baseDir}/scripts/index.py "/path/to/face1.jpg" "/path/to/face2.jpg"
```

## 📋 Input Specification

### Image Requirements

- Supported formats: JPG, PNG, BMP
- File size: < 4MB recommended
- Image should contain clear, frontal face
- One face per image for best results

---

## ⚠ Constraints

- Both image paths must be valid and accessible
- Images must contain detectable faces
- API credentials must be configured
- Network connection required

---

## 🔧 Environment Setup

Required:

- Python available in PATH
- Environment variables configured:

```bash
export XF_FACE_APP_ID=your_app_id
export XF_FACE_API_KEY=your_api_key
export XF_FACE_API_SECRET=your_api_secret
```

Or configure it in `~/.openclaw/openclaw.json`:

```json
{
	"env": {
		"XF_FACE_APP_ID": "your_app_id",
		"XF_FACE_API_KEY": "your_api_key",
		"XF_FACE_API_SECRET": "your_api_secret"
	}
}
```

---

## 📦 Output

Returns JSON response with:
- Similarity score (0-100)
- Comparison result (same person or not)
- Confidence level
- Face detection status

---

## 🎯 Target Use Cases

- Identity verification
- Access control systems
- Duplicate account detection
- Photo matching services
- Security authentication
- Attendance systems

---

## 🛠 Extensibility

Future enhancements may include:

- Batch face comparison
- Face quality assessment
- Multiple face detection
- Liveness detection integration
- Custom threshold configuration

---

Built for automation workflows and AI-driven identity verification.
