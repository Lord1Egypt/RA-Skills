# svg2pptskill

Convert SVG vector graphics, Chinese character stroke order, China province maps, and country maps into editable PPTX with one click.

## Features

- Chinese character stroke order to PPT: `char:中`
- Province map to PPT: `map:北京`
- Country map to PPT: `map:中国`
- SVG code to PPT: paste the full `<svg>...</svg>`
- SVG URL to PPT: provide a publicly accessible SVG link

## Prerequisites

You must first enter `svg2pptskill` in the search box on the https://www.handbooks.cn/ homepage, click search, and copy the generated API Key.

## Usage

```bash
node scripts/convert.cjs <your API Key> <svg content>
```

Examples:

```bash
# Recommended: pass the svg value directly as the second argument; Node.js handles Chinese correctly on Windows
node scripts/convert.cjs SVG2PPTSKILL-xxx map:安徽
node scripts/convert.cjs SVG2PPTSKILL-xxx char:中
node scripts/convert.cjs SVG2PPTSKILL-xxx map:Anhui

# Alternatively, use stdin
# "-" means read from stdin
echo "map:安徽" | node scripts/convert.cjs SVG2PPTSKILL-xxx -
echo "char:中" | node scripts/convert.cjs SVG2PPTSKILL-xxx -
```

## Response

```json
{
  "success": true,
  "download_url": "https://www.handbooks.cn/downloads/svg2ppt-xxx.pptx",
  "file_name": "svg2ppt-xxx.pptx",
  "expires_in": 604800
}
```

The download link is valid for about 7 days.
