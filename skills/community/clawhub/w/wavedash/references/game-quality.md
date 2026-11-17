# Game Quality

Canonical docs:

- Best practices: https://docs.wavedash.com/tutorials/best-practices
- Shader stutter: https://docs.wavedash.com/tutorials/shader-stutter

## Launch-quality checklist

- Warm up WebGL/WebGPU shaders and materials before gameplay.
- Do not use Escape as the only pause/menu key.
- Handle `fullscreenchange` and `pointerlockchange` browser events.
- Resume audio on the first user interaction, especially for Safari.
- Use compressed audio and memory-conscious asset loading.
- Test long sessions, not only quick boot.
- Verify load progress and call `Wavedash.init()` when playable.
- Test Chrome, Firefox, and Safari if the game is public-facing.

## Common fixes

Escape key:

```javascript
document.addEventListener("fullscreenchange", () => {
  if (!document.fullscreenElement) game.pause();
});
document.addEventListener("pointerlockchange", () => {
  if (!document.pointerLockElement) game.showMenu();
});
```

Safari audio:

```javascript
document.addEventListener("click", () => {
  if (audioContext.state === "suspended") audioContext.resume();
}, { once: true });
```

Shader stutter: instantiate or render materials off-screen during loading, then
start gameplay after the warmup pass.
