# Animation

## AnimationMixer (the player)

```js
const mixer = new THREE.AnimationMixer(rootObject);

// In render loop:
const delta = clock.getDelta();
mixer.update(delta);

// Properties
mixer.timeScale = 1;      // Speed multiplier
mixer.time;               // Current time
```

## AnimationAction (controls playback)

```js
const action = mixer.clipAction(animationClip);

// Playback
action.play();
action.pause();
action.stop();
action.reset();
action.halt(duration);    // Gradual stop

// Properties
action.time;              // Current time in clip
action.timeScale = 1;     // Speed (negative = reverse)
action.weight = 1;        // Blend weight 0–1
action.loop = THREE.LoopRepeat | THREE.LoopOnce | THREE.LoopPingPong;
action.repetitions = Infinity;
action.paused = false;
action.enabled = true;
action.clampWhenFinished = false;    // Hold last frame
action.zeroSlopeAtStart = true;     // Smooth start
action.zeroSlopeAtEnd = true;       // Smooth end
action.blendMode = THREE.NormalAnimationBlendMode | THREE.AdditiveAnimationBlendMode;

// Cross-fading
action.crossFadeTo(otherAction, duration, warp);
action.fadeIn(duration);
action.fadeOut(duration);
action.startAt(startTime);
```

## Animation State Machine
```js
const actions = { idle: mixer.clipAction(idleClip), walk: mixer.clipAction(walkClip) };
let current = actions.idle;
current.play();

function switchTo(name, dur = 0.3) {
  const prev = current;
  current = actions[name];
  current.reset().play();
  prev.crossFadeTo(current, dur, true);
}
```

## Skeletal Animation (from glTF)
```js
loader.load('character.glb', gltf => {
  const mixer = new THREE.AnimationMixer(gltf.scene);
  gltf.animations.forEach(c => mixer.clipAction(c).play());
  // In loop: mixer.update(delta);
  // Access bones: gltf.scene.traverse(c => { if(c.isSkinnedMesh) console.log(c.skeleton.bones); });
});
```

## Morph Target Animation
```js
mesh.morphTargetInfluences[0] = 0.5;  // Blend first morph target 50%

// Generate clips from morph sequences:
const clips = THREE.AnimationClip.CreateClipsFromMorphTargetSequences(meshes, fps, false);
```

## AnimationClip (keyframe data)
```js
const clip = new THREE.AnimationClip(name, duration, tracks);
clip.tracks;              // KeyframeTrack[]
clip.duration;            // Seconds

// Tracks:
new THREE.VectorKeyframeTrack('.position', times, values);
new THREE.QuaternionKeyframeTrack('.quaternion', times, values);
new THREE.NumberKeyframeTrack('.material.opacity', times, values);
new THREE.ColorKeyframeTrack('.material.color', times, values);
```

## Addons
```js
import { CCDIKSolver } from 'three/addons/animation/CCDIKSolver.js';       // Inverse kinematics
import { AnimationClipCreator } from 'three/addons/animation/AnimationClipCreator.js';
// CreateRotationAnimation(period, axis), CreateScaleAxisAnimation, CreateShakeAnimation, CreatePulsationAnimation
```