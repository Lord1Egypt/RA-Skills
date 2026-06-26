# Model Catalog

Use this file to shortlist likely TFLite candidates quickly.

## 1. MediaPipe vision tasks

Best first stop for common interactive camera tasks.

### Good for
- object detection
- image classification
- image segmentation
- pose landmarks
- hand landmarks
- face detection / landmarks

### Why prefer it
- official TFLite-oriented stack
- consistent task APIs
- good mobile/edge ergonomics
- documented preprocessing and outputs

### Caveats
- task abstraction may hide tensor-level details
- some tasks are easiest through MediaPipe runtimes rather than raw TFLite interpreter use

## 2. TensorFlow Lite model zoo / task examples

Best for standard TensorFlow-native vision tasks.

### Look here for
- EfficientDet-Lite object detectors
- EfficientNet-Lite classifiers
- MobileNet classifiers
- segmentation examples

### Good default choices
- **Balanced object detection:** EfficientDet-Lite0 or Lite1
- **Fast object detection:** SSD MobileNet variants
- **Balanced classification:** EfficientNet-Lite0
- **Very lightweight classification:** MobileNetV3 small

## 3. TensorFlow Hub

Use when you need a reputable upstream source but can tolerate some validation work.

### Watch for
- whether the asset is already `.tflite` or only a SavedModel
- whether labels are bundled
- input resolution and normalization details

## 4. Coral / Edge TPU ecosystem

Use when target hardware may use Edge TPU now or later.

### Good for
- low-latency detection/classification on supported hardware

### Caveats
- Edge TPU compiled models are a subset of generic TFLite models
- some models require separate CPU fallback if accelerator is absent

## 5. YOLO exported to TFLite

Use only when the user specifically needs YOLO-family accuracy/behavior or already has a YOLO pipeline.

### Good for
- custom detection tasks with strong upstream ecosystem

### Caveats
- output tensor layouts vary by exporter/version
- NMS may be external or fused
- integration risk is higher than EfficientDet-Lite/SSD
- documentation quality varies a lot

## Practical recommendations by task

### General camera object detection for OpenClaw feature work
1. EfficientDet-Lite0
2. SSD MobileNet V2
3. EfficientDet-Lite1 if accuracy matters more than speed

### Lightweight on-device classification
1. MobileNetV3 small
2. EfficientNet-Lite0

### Person/background separation
1. MediaPipe Selfie Segmentation

### Body/hand/face understanding
1. MediaPipe task models first

## What to capture while evaluating a model page

- exact artifact URL
- model version
- license
- classes / label map
- input size
- dtype and quantization
- sample code availability
- any custom op requirement
- output decoding notes
