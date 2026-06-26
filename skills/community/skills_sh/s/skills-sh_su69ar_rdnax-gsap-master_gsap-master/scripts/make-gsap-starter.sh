#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-./gsap-starter}"
mkdir -p "$TARGET_DIR"

cat > "$TARGET_DIR/index.html" <<'HTML'
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GSAP Starter</title>
  <style>
    body { font-family: system-ui, sans-serif; padding: 48px; }
    .box { width: 80px; height: 80px; background: #111; border-radius: 16px; }
    .spacer { height: 120vh; }
  </style>
</head>
<body>
  <h1>GSAP Starter</h1>
  <div class="spacer"></div>
  <div class="box"></div>
  <div class="spacer"></div>

  <!-- GSAP + ScrollTrigger -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>

  <script>
    gsap.registerPlugin(ScrollTrigger);

    gsap.to(".box", {
      x: 400,
      duration: 1,
      ease: "power2.out",
      scrollTrigger: {
        trigger: ".box",
        start: "top 80%",
        end: "top 30%",
        scrub: 1,
        markers: true
      }
    });
  </script>
</body>
</html>
HTML

echo "Created $TARGET_DIR/index.html"