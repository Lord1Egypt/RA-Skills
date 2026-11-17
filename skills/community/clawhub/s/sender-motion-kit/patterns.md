# Patrones de motion (sender-site)
Cada patrón: uso · snippet clave · dónde vive en el sitio.

## P01 · Video pineado scrubbed full-bleed (firma GoPro)
Uso: product films donde el scroll = playback.
```js
ScrollTrigger.create({ trigger: sec, start: 'top top', end: '+=240%',
  pin: stage, scrub: .35,
  onUpdate: s => video.currentTime = s.progress * (video.duration - .05) });
```
Dónde: `#hero` (desarme), `#cine` (reensamble), fichas cap, `.prod`.

## P02 · Galería horizontal pineada con parallax interno
`gsap.to(track, {x: -(w-vw), scrollTrigger:{trigger, pin:true, end:'+='+w, scrub}})` +
`containerAnimation` para parallax de cada imagen. Dónde: `#proyectos` htrack.

## P03 · Sticky two-column
Columna izquierda `position:sticky; top:12vh` mientras la derecha scrollea. Dónde: `#capacidades`.

## P04 · Stacked sticky cards
`.point{position:sticky; top:calc(96px + var(--i)*18px)}` + sombra hacia arriba. Dónde: Nosotros.

## P05 · Split-words con máscara + scramble
Words en `.w>span` con overflow hidden, `gsap.from(yPercent:115, stagger:.05)`;
labels con decode de caracteres. Dónde: todos los h2 y labels.

## P06 · Tilt 3D + botones magnéticos
rotateX/Y ±9° por puntero sobre cards; lerp de translate en CTAs. Dónde: cards, CTAs.

## P07 · Ken Burns loop perfecto (video provisorio desde foto)
`zoompan=z='1.08+0.10*sin(PI*on/144)':d=144:s=800x600:fps=24` (sin(π·on/N) cierra el loop).

## P08 · Animatic flight-map (PIL → mp4)
Frames 640×360: graticule + bezier progresivo + cabeza luminosa blur + contador km;
`ffmpeg -framerate 24 -i f%03d.png -crf 26`. Dónde: `prop-rapanui.mp4` ▸PROVISORIO.

## P09 · Type-ring circular rotatorio
SVG `<textPath>` sobre círculo + `animation: rotate 26s linear infinite`. Dónde: about-media.

## P10 · Marker-sweep en cita
`::after` cian `scaleX(0→1)` con clase `.swept` al entrar (ScrollTrigger once). Dónde: pull quote.

## P11 · Video ambiental bajo glass
`<video loop muted>` absolute cover opacity .3 detrás de `backdrop-filter: blur`. Dónde: CTA band.

## P12 · Keynote 4-vistas crossfade por scroll
Media sticky 100vh; `idx = floor(progress*4)`; toggle `.on` en imgs + dots; si existe
`prod-*.mp4` → scrub del video en vez de vistas. Dónde: `#catalogo` productos.

## P13 · Cursor glow de marca (desktop only)
Div fixed 340px radial cyan .10 mix-blend screen, lerp .12 por rAF; solo
`matchMedia('(pointer: fine)')` y fuera de reduced-motion. Dónde: global v14.

## P14 · Keynote zoom+rotate scrub
En el onUpdate del producto: `scale(1+p*.10) rotateY((p-.5)*5deg)` aplicado al stack y
al video → el media "respira" 3D mientras rotas vistas. Dónde: `.prod` v14.
