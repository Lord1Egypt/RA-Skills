# Complete SVG Examples

## Example 1: Flat Monochrome — "Rocket Icon"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <path d="M42 72 L50 95 L58 72" fill="#F39C12"/>
  <rect x="42" y="22" width="16" height="50" rx="3" fill="#3498DB"/>
  <path d="M50 8 L38 28 L62 28 Z" fill="#E74C3C"/>
  <circle cx="50" cy="35" r="6" fill="white"/>
  <path d="M42 60 L30 72 L42 72" fill="#2980B9"/>
  <path d="M58 60 L70 72 L58 72" fill="#2980B9"/>
</svg>
```

## Example 2: Gradient Style — "Star Logo"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="400" height="400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#667EEA"/>
      <stop offset="100%" stop-color="#764BA2"/>
    </linearGradient>
    <linearGradient id="star" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEE140"/>
      <stop offset="100%" stop-color="#FA709A"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#bg)"/>
  <polygon points="100,20 115,70 170,70 125,100 140,150 100,120 60,150 75,100 30,70 85,70" fill="url(#star)"/>
  <text x="50" y="40" font-size="12" fill="white" opacity=".6">✦</text>
  <text x="155" y="60" font-size="8" fill="white" opacity=".5">✦</text>
  <text x="40" y="150" font-size="10" fill="white" opacity=".4">✦</text>
</svg>
```

## Example 3: Stroke Style — "Owl Illustration"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="400" height="400">
  <ellipse cx="100" cy="120" rx="55" ry="60" fill="#FEF3C7" stroke="#D97706" stroke-width="2.5"/>
  <path d="M55 85 L45 45 L75 75" fill="#FEF3C7" stroke="#D97706" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M145 85 L155 45 L125 75" fill="#FEF3C7" stroke="#D97706" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="78" cy="110" r="18" fill="white" stroke="#D97706" stroke-width="2.5"/>
  <circle cx="122" cy="110" r="18" fill="white" stroke="#D97706" stroke-width="2.5"/>
  <circle cx="78" cy="110" r="9" fill="#92400E"/>
  <circle cx="122" cy="110" r="9" fill="#92400E"/>
  <circle cx="74" cy="106" r="3" fill="white"/>
  <circle cx="118" cy="106" r="3" fill="white"/>
  <path d="M88 130 Q100 140 112 130" fill="#F59E0B" stroke="#D97706" stroke-width="1.5"/>
  <path d="M65 140 Q100 175 135 140" fill="#FDE68A" stroke="#D97706" stroke-width="1.5"/>
  <path d="M75 175 L70 190 M80 175 L80 190 M85 175 L90 190" stroke="#D97706" stroke-width="2" stroke-linecap="round"/>
  <path d="M115 175 L110 190 M120 175 L120 190 M125 175 L130 190" stroke="#D97706" stroke-width="2" stroke-linecap="round"/>
</svg>
```

## Example 4: Tech Style — "Data Dashboard"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="600" height="400">
  <rect width="300" height="200" fill="#0A1628"/>
  <line x1="40" y1="170" x2="280" y2="170" stroke="#1A2D4A" stroke-width="1"/>
  <line x1="40" y1="130" x2="280" y2="130" stroke="#1A2D4A" stroke-width="1"/>
  <line x1="40" y1="90" x2="280" y2="90" stroke="#1A2D4A" stroke-width="1"/>
  <polyline points="40,150 80,120 120,140 160,80 200,100 240,60 280,70"
    fill="none" stroke="#00D4FF" stroke-width="2"/>
  <circle cx="40" cy="150" r="3" fill="#00D4FF"/>
  <circle cx="160" cy="80" r="4" fill="#00D4FF"/>
  <circle cx="240" cy="60" r="4" fill="#00D4FF"/>
  <circle cx="280" cy="70" r="3" fill="#00D4FF"/>
  <polygon points="40,170 40,150 80,120 120,140 160,80 200,100 240,60 280,70 280,170"
    fill="url(#areaGrad)" opacity=".3"/>
  <defs>
    <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00D4FF" stop-opacity=".5"/>
      <stop offset="100%" stop-color="#00D4FF" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <text x="20" y="15" font-family="monospace" font-size="10" fill="#00D4FF">REALTIME METRICS</text>
  <circle cx="285" cy="10" r="4" fill="#00FF88"/>
</svg>
```

## Example 5: Minimal Lines — "Face Profile"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="400" height="400">
  <path d="M120 40 Q 140 30, 155 50 Q 170 70, 165 90 Q 160 100, 160 110
    Q 160 115, 155 115 L 145 115 Q 145 130, 140 140 L 130 180
    L 100 180 L 95 155 Q 90 145, 95 130 Q 100 115, 100 100
    Q 95 90, 90 85 Q 75 70, 80 50 Q 85 35, 100 35 Z"
    fill="none" stroke="#2C3E50" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M100 80 Q 110 75, 115 85" fill="none" stroke="#2C3E50" stroke-width="2" stroke-linecap="round"/>
  <path d="M80 50 Q 75 30, 100 25 Q 130 20, 145 35" fill="none" stroke="#2C3E50" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M82 42 Q 90 22, 120 18" fill="none" stroke="#2C3E50" stroke-width="2" stroke-linecap="round"/>
</svg>
```

## Example 6: 3D Skeuomorphic — "Glass Button"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="400" height="400">
  <defs>
    <radialGradient id="btnBg" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FF6B6B"/>
      <stop offset="100%" stop-color="#C0392B"/>
    </radialGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="white" stop-opacity=".4"/>
      <stop offset="40%" stop-color="white" stop-opacity=".1"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#7F1D1D" flood-opacity=".4"/>
    </filter>
  </defs>
  <g filter="url(#shadow)">
    <circle cx="100" cy="100" r="70" fill="url(#btnBg)"/>
    <path d="M50 70 A60 60 0 0 1 150 70" fill="url(#shine)" stroke="none"/>
    <circle cx="100" cy="100" r="50" fill="none" stroke="white" stroke-opacity=".15" stroke-width="1"/>
    <polygon points="88,78 88,122 125,100" fill="white"/>
  </g>
</svg>
```

## Example 7: Flat Character — "Office Worker"

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300" width="400" height="600">
  <circle cx="100" cy="45" r="30" fill="#FDBF99"/>
  <path d="M70 35 Q 70 10, 100 8 Q 130 10, 130 35" fill="#2D3748"/>
  <circle cx="88" cy="43" r="3" fill="#2D3748"/>
  <circle cx="112" cy="43" r="3" fill="#2D3748"/>
  <path d="M90 55 Q 100 62, 110 55" fill="none" stroke="#2D3748" stroke-width="1.5" stroke-linecap="round"/>
  <rect x="65" y="72" width="70" height="80" rx="5" fill="#2C3E50"/>
  <polygon points="95,80 105,80 102,130 100,140 98,130" fill="#E74C3C"/>
  <polygon points="85,72 100,85 115,72" fill="white"/>
  <rect x="40" y="80" width="28" height="12" rx="6" fill="#2C3E50" transform="rotate(-15,50,80)"/>
  <rect x="132" y="75" width="28" height="12" rx="6" fill="#2C3E50" transform="rotate(10,145,75)"/>
  <circle cx="48" cy="75" r="8" fill="#FDBF99"/>
  <circle cx="148" cy="78" r="8" fill="#FDBF99"/>
  <rect x="75" y="148" width="20" height="60" rx="4" fill="#1A202C"/>
  <rect x="105" y="148" width="20" height="60" rx="4" fill="#1A202C"/>
  <rect x="70" y="200" width="28" height="10" rx="3" fill="#2D3748"/>
  <rect x="102" y="200" width="28" height="10" rx="3" fill="#2D3748"/>
</svg>
```