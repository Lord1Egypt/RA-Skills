# Animations Reference — 50 Video & Text Animations

Complete library of ffmpeg-based animations for Instagram Reels.
Each animation is a tested filter snippet. Drop into your `-filter_complex`.

---

## Table of Contents

| #   | Animation              | Category     | #   | Animation              | Category     |
|-----|------------------------|--------------|-----|------------------------|--------------|
| 1   | Fade In                | Transition   | 26  | Vertical Slide Up      | Movement     |
| 2   | Fade Out               | Transition   | 27  | Vertical Slide Down    | Movement     |
| 3   | Cross Fade             | Transition   | 28  | Diagonal Slide         | Movement     |
| 4   | Zoom In                | Scale        | 29  | Spiral Zoom            | Scale        |
| 5   | Zoom Out               | Scale        | 30  | Shake / Earthquake     | Distortion   |
| 6   | Ken Burns Zoom In      | Scale        | 31  | Glitch Horizontal      | Distortion   |
| 7   | Ken Burns Zoom Out     | Scale        | 32  | Glitch RGB Split       | Distortion   |
| 8   | Ken Burns Pan Left     | Movement     | 33  | VHS / Retro Lines      | Distortion   |
| 9   | Ken Burns Pan Right    | Movement     | 34  | Mirror Horizontal      | Distortion   |
| 10  | Ken Burns Pan Up       | Movement     | 35  | Mirror Vertical        | Distortion   |
| 11  | Ken Burns Pan Down     | Movement     | 36  | Kaleidoscope           | Distortion   |
| 12  | Bounce In              | Text Anim    | 37  | Rotate 360             | Movement     |
| 13  | Bounce Out             | Text Anim    | 38  | Rotate Wiggle          | Movement     |
| 14  | Typewriter             | Text Anim    | 39  | Pulse / Heartbeat      | Scale        |
| 15  | Pop Scale              | Text Anim    | 40  | Flash / Strobe         | Transition   |
| 16  | Slide In Left          | Text Anim    | 41  | Blur In                | Transition   |
| 17  | Slide In Right         | Text Anim    | 42  | Blur Out               | Transition   |
| 18  | Slide In Bottom        | Text Anim    | 43  | Radial Blur            | Distortion   |
| 19  | Slide In Top           | Text Anim    | 44  | Vignette Pulse         | Color        |
| 20  | Float / Hover          | Text Anim    | 45  | Color Flash            | Color        |
| 21  | Wiggle Text            | Text Anim    | 46  | Black & White Flash    | Color        |
| 22  | Glow Pulse             | Text Anim    | 47  | Split Screen Slide     | Composition  |
| 23  | Rubber Band            | Text Anim    | 48  | Picture-in-Picture     | Composition  |
| 24  | Flip In                | Text Anim    | 49  | Parallax Layers        | Composition  |
| 25  | Horizontal Slide Left  | Movement     | 50  | Countdown Timer        | Utility      |

---

## TRANSITION ANIMATIONS

### 1. Fade In
```
fade=t=in:st=0:d=1
```
`st` = start time, `d` = duration in seconds.

### 2. Fade Out
```
fade=t=out:st=8:d=1
```

### 3. Cross Fade (between two clips)
```
[0:v]trim=0:5,setpts=PTS-STARTPTS,fade=t=out:st=4:d=1[v0];
[1:v]trim=0:5,setpts=PTS-STARTPTS,fade=t=in:st=0:d=1[v1];
[v0][v1]overlay=enable='gte(t,4)'
```

### 40. Flash / Strobe
```
geq=r='if(between(t,2,2.15),255,r(X,Y))':g='if(between(t,2,2.15),255,g(X,Y))':b='if(between(t,2,2.15),255,b(X,Y))'
```

---

## SCALE ANIMATIONS

### 4. Zoom In (slow progressive)
```
zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30
```
**Note:** Input image should be at least 2x target resolution.

### 5. Zoom Out (start zoomed, pull back)
```
zoompan=z='if(eq(on,1),1.5,max(zoom-0.0015,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30
```

### 6. Ken Burns Zoom In (image for 5s)
```
zoompan=z='min(zoom+0.001,1.4)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30
```

### 7. Ken Burns Zoom Out
```
zoompan=z='if(eq(on,1),1.4,max(zoom-0.001,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30
```

### 29. Spiral Zoom
```
zoompan=z='min(zoom+0.002,2.0)':x='iw/2-(iw/zoom/2)+50*sin(on/30)':y='ih/2-(ih/zoom/2)+50*cos(on/30)':d=150:s=1080x1920:fps=30
```

### 39. Pulse / Heartbeat (video scale oscillation)
```
scale='1080+20*sin(2*PI*t*2)':'1920+36*sin(2*PI*t*2)'
```

---

## KEN BURNS MOVEMENT (Images)

### 8. Ken Burns Pan Left
```
zoompan=z=1.3:x='if(eq(on,1),0,min(x+1,iw-iw/zoom))':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30
```

### 9. Ken Burns Pan Right
```
zoompan=z=1.3:x='if(eq(on,1),iw-iw/zoom,max(x-1,0))':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30
```

### 10. Ken Burns Pan Up
```
zoompan=z=1.3:x='iw/2-(iw/zoom/2)':y='if(eq(on,1),ih-ih/zoom,max(y-1,0))':d=150:s=1080x1920:fps=30
```

### 11. Ken Burns Pan Down
```
zoompan=z=1.3:x='iw/2-(iw/zoom/2)':y='if(eq(on,1),0,min(y+1,ih-ih/zoom))':d=150:s=1080x1920:fps=30
```

---

## TEXT ANIMATIONS

### 12. Bounce In
```
drawtext=text='BOUNCE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=64:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:
  y='if(between(t,START,START+0.2),-th+((h/2+th)*(t-START)/0.2),
     if(between(t,START+0.2,START+0.35),(h/2)-(80*sin(PI*(t-START-0.2)/0.15)),
     if(between(t,START+0.35,START+0.5),(h/2)-(30*sin(PI*(t-START-0.35)/0.15)),
     h/2)))':
  enable='between(t,START,END)'
```

### 13. Bounce Out
```
drawtext=text='BYE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=64:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:
  y='if(between(t,END-0.5,END), (h/2)-(h*(t-END+0.5)/0.5), h/2)':
  enable='between(t,START,END)'
```

### 14. Typewriter
Use Python generator from `caption-templates.md` Template 7.

### 15. Pop Scale
```
drawtext=text='POP':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize='if(between(t,START,START+0.15),120-((120-64)*(t-START)/0.15),
           if(between(t,START+0.15,START+0.25),64+((80-64)*sin(PI*(t-START-0.15)/0.1)),64))':
  fontcolor=yellow:borderw=4:bordercolor=black:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)'
```

### 16. Slide In from Left
```
drawtext=text='SLIDE LEFT':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x='if(between(t,START,START+0.5),-tw+(tw+(w-tw)/2)*(t-START)/0.5,(w-tw)/2)':
  y=(h-th)/2:
  enable='between(t,START,END)'
```

### 17. Slide In from Right
```
drawtext=text='SLIDE RIGHT':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x='if(between(t,START,START+0.5),w-((w-(w-tw)/2)*(t-START)/0.5),(w-tw)/2)':
  y=(h-th)/2:
  enable='between(t,START,END)'
```

### 18. Slide In from Bottom
```
drawtext=text='SLIDE UP':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:
  y='if(between(t,START,START+0.5),h-((h-(h-th)/2)*(t-START)/0.5),(h-th)/2)':
  enable='between(t,START,END)'
```

### 19. Slide In from Top
```
drawtext=text='SLIDE DOWN':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:
  y='if(between(t,START,START+0.5),-th+((h-th)/2+th)*(t-START)/0.5,(h-th)/2)':
  enable='between(t,START,END)'
```

### 20. Float / Hover
```
drawtext=text='FLOATING':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:
  y='(h-th)/2 + 15*sin(2*PI*t/2)':
  enable='between(t,START,END)'
```

### 21. Wiggle Text
```
drawtext=text='WIGGLE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x='(w-tw)/2 + 8*sin(2*PI*t*6)':
  y=(h-th)/2:
  enable='between(t,START,END)'
```

### 22. Glow Pulse
```
drawtext=text='GLOW':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=64:
  fontcolor='white@(0.5+0.5*sin(2*PI*t/1.5))':
  borderw=3:bordercolor='yellow@(0.3+0.3*sin(2*PI*t/1.5))':
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)'
```

### 23. Rubber Band
```
drawtext=text='STRETCH':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize='if(between(t,START,START+0.3),56*(1+0.8*sin(PI*(t-START)/0.3)),56)':
  fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)'
```

### 24. Flip In
```
drawtext=text='FLIP':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize='if(between(t,START,START+0.3),64*abs(sin(PI*(t-START)/0.3)),64)':
  fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)'
```

---

## VIDEO MOVEMENT ANIMATIONS

### 25. Horizontal Slide Left
```
crop=w=iw*0.8:h=ih:x='(iw*0.2)*(t/DURATION)':y=0,scale=1080:1920
```

### 26. Vertical Slide Up
```
crop=w=iw:h=ih*0.8:x=0:y='(ih*0.2)*(t/DURATION)',scale=1080:1920
```

### 27. Vertical Slide Down
```
crop=w=iw:h=ih*0.8:x=0:y='(ih*0.2)*(1-t/DURATION)',scale=1080:1920
```

### 28. Diagonal Slide
```
crop=w=iw*0.8:h=ih*0.8:x='(iw*0.2)*(t/DURATION)':y='(ih*0.2)*(t/DURATION)',scale=1080:1920
```

---

## DISTORTION ANIMATIONS

### 30. Shake / Earthquake
```
crop=w=iw-20:h=ih-20:x='10+5*sin(t*40)':y='10+5*cos(t*35)',scale=1080:1920
```

### 31. Glitch Horizontal
```
crop=w=iw-30:h=ih:x='15+15*sin(t*80)*if(gt(random(0),0.85),1,0)':y=0,scale=1080:1920
```

### 32. Glitch RGB Split
```
split=3[r][g][b];
[r]lutrgb=g=0:b=0,crop=w=iw-10:h=ih:x=10:y=0[red];
[g]lutrgb=r=0:b=0[green];
[b]lutrgb=r=0:g=0,crop=w=iw-10:h=ih:x=0:y=0[blue];
[green][red]blend=all_mode=addition[rg];
[rg][blue]blend=all_mode=addition
```

### 33. VHS / Retro Scan Lines
```
drawbox=y='mod(t*200,ih)':w=iw:h=2:color=black@0.3:t=fill,
noise=alls=20:allf=t,
eq=saturation=0.8:contrast=1.1
```

### 34. Mirror Horizontal
```
split[left][right];[right]hflip[flipped];[left]crop=iw/2:ih:0:0[l];[flipped]crop=iw/2:ih:0:0[r];[l][r]hstack
```

### 35. Mirror Vertical
```
split[top][bottom];[bottom]vflip[flipped];[top]crop=iw:ih/2:0:0[t];[flipped]crop=iw:ih/2:0:0[b];[t][b]vstack
```

### 36. Kaleidoscope
```
split=4[a][b][c][d];
[a]crop=iw/2:ih/2:0:0[tl];
[b]crop=iw/2:ih/2:0:0,hflip[tr];
[c]crop=iw/2:ih/2:0:0,vflip[bl];
[d]crop=iw/2:ih/2:0:0,hflip,vflip[br];
[tl][tr]hstack[top];
[bl][br]hstack[bot];
[top][bot]vstack
```

---

## ROTATION ANIMATIONS

### 37. Rotate 360
```
rotate='2*PI*t/3:c=none:ow=1080:oh=1920'
```

### 38. Rotate Wiggle
```
rotate='0.05*sin(2*PI*t*3):c=black@0:ow=1080:oh=1920'
```

---

## BLUR ANIMATIONS

### 41. Blur In
```
avgblur='if(lt(t,1.5),ceil(30*(1-t/1.5)),0)':planes=0xF
```

### 42. Blur Out
```
avgblur='if(gt(t,END-1.5),ceil(30*(t-END+1.5)/1.5),0)':planes=0xF
```

### 43. Radial Blur
```
split[a][b];
[a]scale=1.05*iw:1.05*ih,crop=iw/1.05:ih/1.05[zoomed];
[b][zoomed]blend=all_mode=average
```

---

## COLOR ANIMATIONS

### 44. Vignette Pulse
```
vignette='PI/4+PI/8*sin(2*PI*t/3)'
```

### 45. Color Flash
```
geq=r='clip(r(X,Y)+if(between(t,2,2.2),100,0),0,255)':
    g='clip(g(X,Y)+if(between(t,2,2.2),50,0),0,255)':
    b='b(X,Y)'
```

### 46. Black & White Flash
```
hue=s='if(between(t,3,3.3),0,1)'
```

---

## COMPOSITION ANIMATIONS

### 47. Split Screen Slide
```
[0:v]scale=540:1920,crop=540:1920:x='if(lt(t,0.5),540*(1-t/0.5),0)':y=0[left];
[1:v]scale=540:1920,crop=540:1920:x='if(lt(t,0.5),540*(t/0.5),540)':y=0[right];
[left]pad=1080:1920:0:0:black[bg];
[bg][right]overlay=540:0
```

### 48. Picture-in-Picture
```
[1:v]scale=300:-1,setpts=PTS-STARTPTS[pip];
[0:v][pip]overlay=W-w-30:30:enable='between(t,START,END)'
```

### 49. Parallax Layers
```
[0:v]scale=1200:2133,crop=1080:1920:x='60*(t/DURATION)':y=0[bg];
[1:v]scale=400:-1,format=rgba[fg];
[bg][fg]overlay='(W-w)/2+30*(t/DURATION)':H-h-200
```

---

## UTILITY ANIMATIONS

### 50. Countdown Timer
```
drawtext=text='3':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:fontsize=200:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=(h-th)/2:enable='between(t,0,1)',
drawtext=text='2':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:fontsize=200:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=(h-th)/2:enable='between(t,1,2)',
drawtext=text='1':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:fontsize=200:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=(h-th)/2:enable='between(t,2,3)',
drawtext=text='GO!':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:fontsize=180:fontcolor=yellow:borderw=5:bordercolor=black:x=(w-tw)/2:y=(h-th)/2:enable='between(t,3,3.5)'
```

---

## Combining Animations

Chain animations in filter_complex with commas:
```bash
ffmpeg -i input.mp4 -filter_complex "
  fade=t=in:st=0:d=1,
  eq=saturation=1.3,
  vignette=PI/5,
  drawtext=text='Hello':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:fontsize=56:fontcolor=white:borderw=3:bordercolor=black:x='if(between(t,1,1.5),-tw+(tw+(w-tw)/2)*(t-1)/0.5,(w-tw)/2)':y=h-th-250:enable='between(t,1,6)',
  fade=t=out:st=8:d=1
" OUTPUT_FLAGS output.mp4
```
