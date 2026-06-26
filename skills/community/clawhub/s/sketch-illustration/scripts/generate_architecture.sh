cd /root/.openclaw/workspace/skills/sketch-illustration

export ZENMUX_API_KEY=$(cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; print(json.load(sys.stdin)['models']['providers']['zenmux']['apiKey'])")

python3 scripts/generate_sketch.py \
  --output /root/myfiles/meme_pipeline_arch.png \
  --prompt "A clean, minimalist hand-drawn flow chart diagram showing an automated pipeline. Three main steps connected by arrows. Step 1: 'Data Fetch' (a spider web or globe icon, scraping Reddit/X). Step 2: 'Visual Translation' (an AI robot processing an image, adding subtitles). Step 3: 'WeChat Publishing' (a mobile phone showing a WeChat article). Style A: Sketch minimal, Notion/Linear aesthetic, thin black lines, low saturation, very clean and professional, technical diagram. Wide aspect ratio 16:9."

