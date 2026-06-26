# Project Format Reference

## Repository

Target repo: `https://github.com/agegr/mindmap-ppt`

Core files:

- `project/source.js`: project content and image references.
- `project/`: project content and local illustration assets.
- `src/main.js`: parser, navigation, layout, camera, node/image rendering.
- `src/styles.css`: visual style and animations.
- `AGENTS.md`: source-of-truth project rules.

## `project/source.js`

Use this shape:

```js
export const sourceMarkdown = `
- Markdown Mindmap
  项目汇报思维导图演示
  @image overview.png
    - 需求分析
      用户目标与演示场景
`;
```

Parsing rules:

- Lines matching `- text` create nodes.
- Indented continuation lines add to the current node label.
- `@image path` attaches one image to the current node and is not visible text.
- Short image paths such as `overview.png` resolve to `./project/overview.png`.
- Nested short paths such as `image-asset-1/a.jpg` resolve to `./project/image-asset-1/a.jpg`.
- Explicit paths beginning with `./`, `../`, `/`, `http:`, `https:`, or `data:` are used as-is.
- Multiple `@image` lines on one node: last one wins.
- The tree is traversed preorder.

## Node Text

Two-line node convention:

- first line: subtitle/category, smaller text
- second line: main title, normal title text

Single-line nodes render as title only.

Control readouts collapse multiline labels into `subtitle / title`.

## Image Behavior

Images render inside node cards:

- selected image node: expanded image below text
- non-selected image node: thumbnail below text
- no image: no image space

Supported formats: PNG, JPG/JPEG, SVG via browser `<img>`.

Use `object-fit: contain`; avoid crop-dependent compositions.

## Current Visual Style

Match the existing presentation style:

- background: warm off-white, light grid/dot texture
- selected node: dark teal `#183a4a`
- accent: orange `#d8894f`
- completed node fill: pale green `#eef7f3`
- path node fill: near-white `#fffdf8`
- restrained shadows
- small `8px` radii
- no heavy decorative effects, gradient blobs, dense textures, photorealism, or text inside generated images

## Camera And Layout Constraints

- Current path is horizontal.
- Already visited non-path branches appear above their parent.
- Unvisited nodes are hidden.
- Node sizes are real HTML/CSS sizes; do not rely on SVG text measurement.
- Links are SVG curves from node border to node border.
- Camera uses actual viewport size and only auto-scales when user changes the zoom slider.
