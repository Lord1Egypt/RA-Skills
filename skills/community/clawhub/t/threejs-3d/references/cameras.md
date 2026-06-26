# Cameras

## PerspectiveCamera (3D view)
```js
const cam = new THREE.PerspectiveCamera(fov, aspect, near, far);
// fov: vertical field of view in degrees (not radians!)
// aspect: width/height
// near/far: clipping planes

cam.zoom = 1;                   // Zoom factor (>1 = zoom in)
// After changing: cam.updateProjectionMatrix()

// Stereo / split-screen view offset:
cam.setViewOffset(fullW, fullH, x, y, w, h);
cam.clearViewOffset();
```

## OrthographicCamera (parallel projection)
```js
const aspect = innerWidth / innerHeight;
const size = 10;
const cam = new THREE.OrthographicCamera(
  -size * aspect / 2, size * aspect / 2,  // left, right
  size / 2, -size / 2,                     // top, bottom
  0.1, 1000                                // near, far
);

// 2D pixel-perfect (top-left origin):
const cam = new THREE.OrthographicCamera(0, canvasW, 0, canvasH, -1, 1);
```

## CubeCamera (dynamic cubemap/environment)
```js
const cubeRT = new THREE.WebGLCubeRenderTarget(256);
const cubeCam = new THREE.CubeCamera(near, far, cubeRT);
// In loop: obj.visible=false; cubeCam.update(renderer, scene); obj.visible=true;
// Use cubeRT.texture as envMap
```

## StereoCamera (VR, used internally by WebXR)
```js
const stereo = new THREE.StereoCamera();
stereo.eyeSep = 0.064;           // IPD in meters
stereo.update(camera);
// stereo.cameraL / cameraR for each eye
```

## ArrayCamera (multiple cameras, single scene)
```js
new THREE.ArrayCamera([cam1, cam2]);
```

## Camera Helper
```js
const helper = new THREE.CameraHelper(camera);
scene.add(helper);
helper.update();
```

## Gotchas
- **fov** is degrees (unique in Three.js where everything else uses radians)
- `lookAt` points **-Z** axis at target — set `camera.up.set(0,0,1)` before for top-down views
- `near` should be as large as possible to maximize depth buffer precision
- For huge scenes with z-fighting: `renderer.logarithmicDepthBuffer = true` (WebGL only)
- `updateProjectionMatrix()` must be called after changing fov/aspect/near/far/zoom