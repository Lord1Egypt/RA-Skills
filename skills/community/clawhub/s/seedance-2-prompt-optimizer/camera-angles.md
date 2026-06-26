# Camera Angles & Movement Reference — Seedance 2.0

Use this file when the user asks about camera language, shot types, or camera movement.
Include precise camera descriptors in every shot of a Seedance prompt for best results.

---

## 1. Shot Size (Framing)

### Extreme Close-Up (ECU)
- Fills frame with a single detail: eyes, lips, fingertip, product logo
- Use for: emotional intensity, texture reveals, product detail shots
- Seedance tip: pair with "shallow depth of field, bokeh background" for cinematic feel
- Example: `ECU on her trembling hands gripping the letter`

### Close-Up (CU)
- Subject's face or a prominent object fills most of the frame
- Use for: emotion, reaction, identity establishment
- Seedance tip: great anchor shot for character ID — use as first shot with face reference image
- Example: `CU on the detective's narrowed eyes`

### Medium Close-Up (MCU)
- Frames from chest/shoulders up
- Use for: dialogue scenes, interviews, moderate intimacy
- Example: `MCU, two-shot, characters facing each other`

### Medium Shot (MS)
- Waist up; standard conversational frame
- Use for: action with visible gesture, product demos
- Example: `MS showing the chef's hands folding dough`

### Medium Wide / Cowboy Shot
- Thighs up; classic for action heroes
- Use for: drawing weapons, walking shots, standoffs
- Example: `Cowboy shot, hero draws sword, dust kicks up`

### Wide Shot (WS)
- Full body visible with environment context
- Use for: establishing character in space, action choreography
- Example: `WS, lone figure walking across salt flats at dusk`

### Establishing Shot / Extreme Wide Shot (EWS)
- Vast environment, subject tiny or absent
- Use for: scene setting, geography, scale
- Seedance tip: use as opening or closing shot; pair with slow push-in for drama
- Example: `EWS, aerial view of neon-lit city grid at midnight`

### Over-the-Shoulder (OTS)
- Camera behind one character looking at another
- Use for: dialogue, confrontation, power dynamics
- Example: `OTS shot — camera behind Subject1, facing Subject2 across the table`

### POV (Point of View)
- Camera represents a character's eyes
- Use for: immersion, first-person perspective, chase scenes
- Example: `POV shot sprinting through narrow alley, walls blurring`

---

## 2. Camera Angle (Vertical Position)

### Eye Level
- Camera at subject's eye height — neutral, natural
- Default for most dialogue and product shots
- Example: `fixed shot, eye level, medium shot`

### High Angle / Bird's Eye
- Camera looks down on subject — subject appears smaller, vulnerable
- Use for: establishing dominance hierarchy, overhead maps, crowd shots
- Bird's eye (90° top-down): great for choreography reveals, flat-lay product shots
- Example: `high angle shot looking down at crowd below`
- Example: `bird's eye view, top-down shot of sushi arrangement on black stone`

### Low Angle / Worm's Eye
- Camera looks up — subject appears powerful, looming, heroic
- Use for: villain introductions, hero moments, towering architecture
- Example: `low angle shot looking up at skyscraper facade in rain`

### Dutch Angle (Canted Frame)
- Camera tilted diagonally — unsettling, tense, disorienting
- Use for: psychological thriller moments, madness, instability
- Example: `Dutch angle, character staggers through tilted corridor`

---

## 3. Camera Movement

### Static / Fixed
- Camera does not move
- Use for: stability, dialogue, product reveals
- Seedance tip: explicitly write "static shot" or "fixed camera" — model defaults to slight drift otherwise
- Example: `static shot, fixed camera, MS on product rotating in place`

### Pan (horizontal rotation)
- Camera pivots left or right on a fixed axis
- Use for: following moving subjects, revealing wide scenes
- Example: `slow pan right revealing the length of the dining table`

### Tilt (vertical rotation)
- Camera pivots up or down on fixed axis
- Use for: revealing height, scanning a body, dramatic reveals
- Example: `tilt up from muddy boots to warrior's defiant face`

### Dolly / Track (physical movement)
- Camera physically moves forward/backward (dolly) or sideways (track)
- Use for: approaching a subject, lateral follow
- Example: `dolly in slowly toward the glowing door`
- Example: `tracking shot following subject from the left`

### Push-In / Pull-Out
- Slow dolly forward (push-in) or backward (pull-out)
- Push-in: increasing tension, intimacy, focus
- Pull-out: revelation, isolation, scale
- Example: `slow push-in on character's face as she reads the message`
- Example: `pull-out revealing she's alone in an empty stadium`

### Crane / Jib
- Camera rises or descends on a vertical arm; sweeping upward/downward arcs
- Use for: epic reveals, God's-eye perspective transitions
- Example: `crane shot rising above rooftop to reveal the city skyline`

### Handheld
- Subtle organic camera shake — raw, intimate, documentary feel
- Use for: action scenes, emotional confrontations, found-footage style
- Seedance tip: write "handheld camera with slight natural shake" for best result
- Example: `handheld shot following the argument through the apartment`

### Steadicam / Smooth Tracking
- Smooth follow without shake — glossy, cinematic
- Use for: character entrances, long corridor walks, fashion film
- Example: `smooth Steadicam follow behind character walking runway`

### Zoom (optical)
- Lens zooms without camera movement — flattens space, nostalgic or alarming effect
- Slow zoom in: building dread
- Fast zoom: shock, comedic effect (crash zoom)
- Example: `slow optical zoom onto the ticking clock`
- Example: `crash zoom into suspect's face at moment of revelation`

### Whip Pan
- Extremely fast horizontal pan — used as a cut transition
- Use for: fast-paced montage, action transitions
- Example: `whip pan left cuts to next scene`

### Arc / Orbit Shot
- Camera circles around a subject (full or partial arc)
- Use for: revealing character from all sides, product 360°, dramatic emphasis
- Example: `180° arc around Subject1 as she stands at cliff edge`
- Example: `slow 360° orbit of the product on a white plinth`

### Drone / Aerial
- High altitude, sweeping; often combined with landscape shots
- Use for: opening establishing shots, nature, geography
- Example: `drone aerial shot sweeping over coastal cliffs at golden hour`

---

## 4. Focus & Depth of Field

### Deep Focus
- Both foreground and background sharp
- Use for: environments where all elements matter
- Example: `deep focus wide shot, sharp from actor to distant mountains`

### Shallow Depth of Field (Rack Focus)
- Subject sharp, background blurred (bokeh)
- Use for: isolation of subject, intimacy, product highlights
- Example: `shallow DOF, subject in focus, blurred city lights behind`

### Rack Focus
- Focus shifts from one subject to another within a single shot
- Use for: directing attention, dialogue transitions
- Example: `rack focus from foreground flower to Subject2 behind it`

---

## 5. Lens Type Descriptors

| Lens | Effect | Best for |
|---|---|---|
| Wide angle (16–24mm) | Distortion, expansive space | Architecture, action, landscapes |
| Standard (35–50mm) | Natural human perspective | Dialogue, documentary |
| Telephoto (85–200mm) | Compression, flattering portrait | Face shots, sports, wildlife |
| Macro | Extreme close detail | Product texture, nature, food |
| Anamorphic | Cinematic lens flare, widescreen stretch | Epic drama, sci-fi |
| Fisheye | Strong barrel distortion | Skate, extreme sports, surreal |

---

## 6. Multi-Shot Sequencing in Seedance Prompts

Always describe shots in order using labels. Seedance supports sequential shot ordering
but does not reliably support precise second-level timing — use narrative order instead.

```
Shot 1 (establishing): EWS drone aerial, snow-covered mountain range at dawn, camera slowly descends.
Shot 2 (introduction): WS, Subject1 emerges from tent, breath visible in cold air, static camera.
Shot 3 (detail): ECU on crampons clicking into ice, handheld slight shake.
Shot 4 (hero moment): Low angle looking up at Subject1 planting flag, crane shot rises with her.
```

---

## 7. Seedance-Specific Camera Tips

- **State camera movement explicitly** — the model will add random movement if you don't
- **Avoid mixing too many movements in one shot** — pick one dominant movement per shot
- **Use "fixed camera" for product shots** where stability matters
- **Horizontal (16:9) reduces subtitle generation** significantly vs. vertical (9:16)
- **Combine lens type + movement + framing** for precise control:
  `"85mm telephoto, slow dolly in, MCU on Subject1's face"` outperforms `"close shot of face"`
- **Transitions**: Use whip pan, match cut, or fade to black as explicit shot separators
  rather than hoping the model will infer them
