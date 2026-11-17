---
name: "shorts-designer"
description: "Agentic AI Shorts Designer generates customized Shorts designs for print on demand (POD) and manufacturing on demand (MOD). It supports structured clothing parameters, reference images, customized text and logos, interactive 3D viewers, and multi-view design generation."
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: OneKey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# AI Shorts Designer Skills from Craftsman Agent

Agentic AI Clothing Designer generates customized clothing designs for print, personalization, prototyping, and manufacturing. It supports T-Shirts, Shirts, Polo Shirts, Hoodies / Sweatshirts, Jackets, Coats, Dresses, Skirts, Pants / Trousers, Jeans, Shorts, Hats / Caps, Scarves, Gloves, and Socks.

The designer can use natural-language prompts, structured clothing parameters, and reference images to generate customized designs with materials, fits, silhouettes, dimensions, closures, decorations, prints, text, logos, and other design details.

The design workflow can generate:

* Clothing design concepts
* Customized text and logo placement
* Reference-image-based designs
* Multi-view design sheets
* Interactive 3D clothing viewers
* Final 3D design assets when available
* Manufacturing-on-demand designs

After the design, you can also use the Craftsman Agent Manufacturing Platform to find suppliers of Craftsman of all kinds.

https://craftsman-agent.aiagenta2z.com/app/clothing-designer/shorts

The typical Clothing designer workflow such as T-Shirt POD include:

```commandline
[Text/Image Prompt of your Clothing Type, Texture, ]
        ->
[Define Customized Text or Logo Printing, Dimensions]
        ->
[Generate 3D Interactive Viewer] or [Generate final 3D Models.g. ]        
        ->
[Generate Preview Images From Multiple Views]
        ->
[Manufacturing on Demand Send Designs to Factory]
```

| API                             | Description                                                                                                                    |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| clothing_generator_design_draft | Generate Design Draft of your preferred Clothing type, e.g. shirts, texture, dimension, customized text and logo for printing. |

### OneKey Agent Gateway

The Bag Designer APIs are registered under:
unique_id: craftsman-agent/craftsman-agent
Gateway endpoint:
```commandline
https://agent.deepnlp.org/agent_router

```
Set the registered OneKey Gateway access key:

```
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

| Section                                 | Description                                                  |
|-----------------------------------------|--------------------------------------------------------------|
| Craftsman Clothing Designer App Online  | https://craftsman-agent.aiagenta2z.com/app/clothing-designer/shorts |
| Craftsman Website                       | https://craftsman-agent.aiagenta2z.com                       |
| Craftsman App                           | https://craftsman-agent.aiagenta2z.com/app                   |
| Craftsman Gallery                       | https://craftsman-agent.aiagenta2z.com/gallery               |
| Craftsman Workspace                     | https://craftsman-agent.aiagenta2z.com/workspace             |
| Craftsman Marketplace                   | https://craftsman-agent.aiagenta2z.com/marketplace           |
| Craftsman Manufacturing on Demand Store | https://craftsman-agent.aiagenta2z.com/store                 |


## Quick Start
Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://www.deepnlp.org/workspace/keys).

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

### Prompt Examples:


#### Template ID:  t-shirt
  Prompt: Design an white T-shirt graphic tee made of cotton. The front prints 'Craftsman' and the logo of Craftsman Agent.

#### Template ID:  shirt
  Prompt: Create a slim fit casual shirt using linen material.

#### Template ID:  polo-shirt
  Prompt: A regular fit pique polo shirt with a ribbed collar.

#### Template ID:  hoodie
  Prompt: Design a relaxed fit fleece pullover hoodie sweater. The front prints 'Craftsman' and the logo of Craftsman Agent.
  
#### Template ID:  jacket
  Prompt: Create a regular fit leather bomber jacket.
  
#### Template ID:  coat
  Prompt: Design a long wool trench coat.
  
#### Template ID:  dress
  Prompt: Create an A-line maxi dress made of silk.

#### Template ID:  skirt
  Prompt: Design a high-waisted pleated skirt made of polyester.

#### Template ID:  pants
  Prompt: Tailored fit chinos made from a cotton blend.

#### Template ID:  jeans
  Prompt: Design a pair of mid-rise skinny jeans in denim.

#### Template ID:  shorts
  Prompt: Loose fit nylon board shorts.

#### Template ID:  hat
  Prompt: A felt fedora hat with a teardrop crown.

#### Template ID:  scarf
  Prompt: Design a cashmere infinity loop scarf.

#### Template ID:  gloves
  Prompt: Full-finger leather winter gloves.

#### Template ID:  socks
  Prompt: Athletic cotton socks with a ribbed cuff.


# 1. API: Clothing Designer Design Draft

### 1.1 REST API Requests Usage
```
clothing_generator_design_draft
```

Generate a clothing design draft with an interactive 3D model and multi-view images from:

* User text prompts
* Reference images
* Structured clothing parameters
* Clothing template IDs
* Customized print, text, logo, and decoration requirements

The resulting design draft can contain an online interactive 3D model viewer for future modification.


#### Requests Input Parameter

| Parameter           | Description                                                                                                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt`            | Text description of the desired clothing style, material, fit, dimensions, decoration, printing, personalization, or manufacturing intent                                     |
| `images`            | Array of source image URLs used as visual references                                                                                                                          |
| `template_id`       | Clothing template ID such as `t-shirt`, `shirt`, `polo-shirt`, `hoodie`, `jacket`, `coat`, `dress`, `skirt`, `pants`, `jeans`, `shorts`, `hat`, `scarf`, `gloves`, or `socks` |
| `options`           | Structured customization parameters defined by the selected clothing template                                                                                                 |
| `provider_model_id` | Clothing design provider/model identifier; `default` is supported                                                                                                             |
| `session_name`      | Name of the generated workspace session                                                                                                                                       |
| `tag_list`          | Optional tags associated with the generation                                                                                                                                  |
| `mode`              | Generation mode: `basic`, `standard`, `advanced`, or `demo`                                                                                                                   |


#### Input Parameter Options

**template_id**: The template reference model to generate 

#### Supported Jewelry Category Template IDs

Supported `template_id` include

| Template ID  | Clothing Type       |
| ------------ | ------------------- |
| `t-shirt`    | T-Shirt             |
| `shirt`      | Shirt               |
| `polo-shirt` | Polo Shirt          |
| `hoodie`     | Hoodie / Sweatshirt |
| `jacket`     | Jacket              |
| `coat`       | Coat                |
| `dress`      | Dress               |
| `skirt`      | Skirt               |
| `pants`      | Pants / Trousers    |
| `jeans`      | Jeans               |
| `shorts`     | Shorts              |
| `hat`        | Hat / Cap           |
| `scarf`      | Scarf               |
| `gloves`     | Gloves              |
| `socks`      | Socks               |

**Always use the exact template ID when constructing a request.**

**mode**: The mode as complexity of design for each generation task


| ID         | Description                                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| `basic`    | Basic complexity for design                                                                                  |
| `standard` | Standard complexity for design                                                                               |
| `advanced` | Advanced complexity for design                                                                               |
| `demo`     | Demo mode for predefined/debug API results; use `basic`, `standard`, or `advanced` for production generation |


#### Requests Input Example
```commandline
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
  -H "Content-Type: application/json" \
  -H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
  -d '{
      "prompt": "Loose fit nylon board shorts.",
      "images": [],
      "template_id": "shorts",
      "provider_model_id": "default",
      "options": {},
      "session_name": "Craftsman Shorts",
      "tag_list": "t-shirt,graphic,pod",
      "mode": "demo"
    }
  }'

```

This example use the 'demo' mode for debug purpose, for real example, please use 'basic' instead.

#### Output Keys Definition

| Key                    | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| `success`              | Whether the design draft generation succeeded                  |
| `share_url`            | URL of the workspace containing the generated design           |
| `blueprint`            | Generated clothing design blueprint data, when available       |
| `reference_images`     | Generated reference or multi-view image URLs                   |
| `final_image_url`      | URL of the generated multi-view design sheet                   |
| `overall_image`        | Overall generated design image information, when available     |
| `options`              | Structured clothing options generated or applied to the design |
| `prompt`               | Prompt used for the generation                                 |
| `session_id`           | Workspace/session identifier                                   |
| `title`                | Generated session title                                        |
| `workspace_session_id` | Workspace session identifier                                   |
| `tag_list`             | Tags associated with the generation                            |


#### Output Example

```json
{
  "success": true,
  "blueprint": {},
  "reference_images": [],
  "final_image_url": "",
  "overall_image": {},
  "session_id": "31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb",
  "title": "T-Shirt Designer",
  "workspace_session_id": "",
  "tag_list": "t-shirt,graphic,pod",
  "options": {
    "gender": "unisex",
    "sub_category": "graphic",
    "material": "cotton",
    "asset_size": "m",
    "fit": "regular",
    "neckline": "crew",
    "sleeve": "short",
    "length": "hip",
    "hem_style": "straight"
  },
  "prompt": "Design a white cotton graphic T-shirt with a regular fit.",
  "share_url": "https://craftsman-agent.aiagenta2z.com/app/sessions/share/31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb?pwd=de06"
}
```

**Note**:
`share_url`: After the Jewelry Design generation task finished, a `share_url` value contains URL of the canvas workspace will be returned.
This is the website to view the progress of the generation and the multiview sheets, the front view, side view, backview.
Please notify user the `share_url` link to view the Jewelry Design generation task status and results online!


### 1.2 CLI Usage

```shell
npx onekey agent craftsman-agent/craftsman-agent clothing_generator_design_draft '{"prompt":"Design a white cotton graphic T-shirt with a regular fit. Print text CRAFTSMAN and the Craftsman Agent logo on the front.","images":[],"template_id":"t-shirt","provider_model_id":"default","options":{"gender":"unisex","sub_category":"graphic","material":"cotton","asset_size":"m","fit":"regular","neckline":"crew","sleeve":"short","length":"hip","hem_style":"straight"},"session_name":"Craftsman Graphic T-Shirt","tag_list":"t-shirt,graphic,pod","mode":"demo"}'
```

**Note**:
demo mode will return demo results for debug purpose, when production, change to 'basic' or other modes.



#### 1.3 Detailed Clothing Designer Options

## 1.3.1 T-Shirt

`template_id`: `t-shirt`

### Main Parameters

 White T-Shirt with Customizable Text Fonts and Colors on the T-Shirt and Picture

| Field                    | Type        | Default             | Description                                     |
| ------------------------ | ----------- | ------------------- | ----------------------------------------------- |
| `gender`                 | string      | `"male"`            | Gender                                          |
| `sub_category`           | string      | `"basic"`           | T-shirt style                                   |
| `material`               | string      | `"cotton"`          | Material                                        |
| `asset_size`             | string      | `"m"`               | Size                                            |
| `fit`                    | string      | `"regular"`         | Fit                                             |
| `neckline`               | string      | `"crew"`            | Neckline                                        |
| `sleeve`                 | string      | `"short"`           | Sleeve                                          |
| `length`                 | string      | `"hip"`             | Garment length                                  |
| `collar_width`           | string      | `"2cm"`             | Collar width                                    |
| `sleeve_length`          | string      | `"22cm"`            | Sleeve length                                   |
| `garment_length`         | string      | `"70cm"`            | Garment length                                  |
| `hem_style`              | string      | `"straight"`        | Hem style                                       |
| `colors`                 | object      | —                   | Garment colors; existing nested state structure |
| `print_text`             | string      | `"Craftsman Agent"` | Global/legacy print text                        |
| `print_text_front`       | string      | `"Craftsman Agent"` | Front print text                                |
| `print_text_back`        | string      | `"Craftsman Agent"` | Back print text                                 |
| `print_font`             | string      | `"Great Vibes"`     | Print font                                      |
| `print_placement`        | string      | `"front"`           | `front`, `back`, `both`                         |
| `print_scale`            | number      | `1`                 | Global/legacy print scale                       |
| `print_scale_front`      | number      | `1`                 | Front text scale                                |
| `print_scale_back`       | number      | `1`                 | Back text scale                                 |
| `graphic_scale`          | number      | `1`                 | Global/legacy graphic scale                     |
| `graphic_scale_front`    | number      | `1`                 | Front graphic scale                             |
| `graphic_scale_back`     | number      | `1`                 | Back graphic scale                              |
| `print_offset_x`         | number      | `0`                 | Global/legacy print X                           |
| `print_offset_y`         | number      | `0`                 | Global/legacy print Y                           |
| `print_offset_x_front`   | number      | `0`                 | Front text X                                    |
| `print_offset_y_front`   | number      | `0`                 | Front text Y                                    |
| `print_offset_x_back`    | number      | `0`                 | Back text X                                     |
| `print_offset_y_back`    | number      | `0`                 | Back text Y                                     |
| `graphic_style`          | string      | `"none"`            | Graphic type/style                              |
| `graphic_image`          | string/null | `null`              | Global/legacy graphic                           |
| `graphic_image_front`    | string/null | `null`              | Front graphic                                   |
| `graphic_image_back`     | string/null | `null`              | Back graphic                                    |
| `graphic_offset_x`       | number      | `0`                 | Global/legacy graphic X                         |
| `graphic_offset_y`       | number      | `0`                 | Global/legacy graphic Y                         |
| `graphic_offset_x_front` | number      | `0`                 | Front graphic X                                 |
| `graphic_offset_y_front` | number      | `0`                 | Front graphic Y                                 |
| `graphic_offset_x_back`  | number      | `0`                 | Back graphic X                                  |
| `graphic_offset_y_back`  | number      | `0`                 | Back graphic Y                                  |
| `logo_visible`           | boolean     | `true`              | Show logo                                       |
| `logo_text`              | string      | `"CA"`              | Logo text                                       |
| `logo_position`          | string      | `"left"`            | Logo position                                   |
| `logo_type`              | string      | `"text"`            | Logo type                                       |
| `doodle_mode`            | boolean     | `false`             | Doodle mode                                     |
| `doodle_color`           | string      | `"#141414"`         | Doodle color                                    |
| `doodle_shape`           | string      | `"round"`           | Doodle shape                                    |
| `doodle_size`            | number      | `8`                 | Doodle size                                     |
| `doodles`                | array       | `[]`                | Doodle data                                     |
| `selected_part`          | string      | `"body"`            | Selected garment part                           |
| `show_mannequin`         | boolean     | `true`              | Show mannequin                                  |
| `auto_rotate`            | boolean     | `true`              | Auto rotation                                   |


### Other Parameters / Defaults

| Parameter        | Default / Value |
| ---------------- | --------------- |
| `collar_width`   | `2cm`           |
| `sleeve_length`  | `22cm`          |
| `garment_length` | `70cm`          |

### Asset Size Metadata

| Asset Size ID | Chest                   | Length            | Unit |
| ------------- | ----------------------- | ----------------- | ---- |
| `xs`          | `84-89cm` / `33-35in`   | `64cm` / `25.2in` | `cm` |
| `s`           | `89-94cm` / `35-37in`   | `67cm` / `26.4in` | `cm` |
| `m`           | `94-102cm` / `37-40in`  | `70cm` / `27.6in` | `cm` |
| `l`           | `102-109cm` / `40-43in` | `73cm` / `28.7in` | `cm` |
| `xl`          | `109-117cm` / `43-46in` | `76cm` / `29.9in` | `cm` |
| `2xl`         | `117-125cm` / `46-49in` | `79cm` / `31.1in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "sub_category": "basic",
  "material": "cotton",
  "asset_size": "m",
  "fit": "regular",
  "neckline": "crew",
  "sleeve": "short",
  "length": "hip",
  "hem_style": "straight"
}
```

---

## 1.3.2 Shirt

`template_id`: `shirt`

### Main Parameters

| Parameter      | Type        | Default             | Supported IDs                                                                                                               |
| -------------- |-------------|---------------------| --------------------------------------------------------------------------------------------------------------------------- |
| `gender`       | string      | `unisex`  | `male`, `female`, `unisex`, `kids`                                                                                          |
| `sub_category` | string      | `casual-shirt`  | `dress-shirt`, `casual-shirt`, `oxford`, `oversized`, `crop-shirt`, `tunic`, `blouse`                                       |
| `material`    | string      | `default`  | `default`, `cotton`, `organic-cotton`, `linen`, `silk`, `rayon`, `polyester`, `oxford`, `poplin`, `flannel`, `cotton-blend` |
| `asset_size`  | string      | `default`  | `default`, `xs`, `s`, `m`, `l`, `xl`                                                                                        |
| `fit`         | string      | `regular`  | `slim`, `regular`, `relaxed`, `oversized`                                                                                   |
| `collar`      | string      | `point`  | `point`, `spread`, `mandarin`, `peter-pan`, `button-down`, `no-collar`                                                      |
| `sleeve`      | string      | `short`  | `short`, `long`, `puff`, `bell`, `bishop`, `sleeveless`                                                                     |
| `closure`     | string      | `buttons`  | `buttons`, `zipper`, `snap`, `tie`                                                                                          |
| `pocket`      | string      | `none`                    | `none`, `chest`, `double`                                                                                                   |
| `cuff`        | string      | `standard`  | `standard`, `button`, `french`                                                                                              |
| `colors`                 | object      | —                   | Garment colors; existing nested state structure |
| `print_text`             | string      | `"Craftsman Agent"` | Global/legacy print text                        |
| `print_text_front`       | string      | `"Craftsman Agent"` | Front print text                                |
| `print_text_back`        | string      | `"Craftsman Agent"` | Back print text                                 |
| `print_font`             | string      | `"Great Vibes"`     | Print font                                      |
| `print_placement`        | string      | `"front"`           | `front`, `back`, `both`                         |
| `print_scale`            | number      | `1`                 | Global/legacy print scale                       |
| `print_scale_front`      | number      | `1`                 | Front text scale                                |
| `print_scale_back`       | number      | `1`                 | Back text scale                                 |
| `graphic_scale`          | number      | `1`                 | Global/legacy graphic scale                     |
| `graphic_scale_front`    | number      | `1`                 | Front graphic scale                             |
| `graphic_scale_back`     | number      | `1`                 | Back graphic scale                              |
| `print_offset_x`         | number      | `0`                 | Global/legacy print X                           |
| `print_offset_y`         | number      | `0`                 | Global/legacy print Y                           |
| `print_offset_x_front`   | number      | `0`                 | Front text X                                    |
| `print_offset_y_front`   | number      | `0`                 | Front text Y                                    |
| `print_offset_x_back`    | number      | `0`                 | Back text X                                     |
| `print_offset_y_back`    | number      | `0`                 | Back text Y                                     |
| `graphic_style`          | string      | `"none"`            | Graphic type/style                              |
| `graphic_image`          | string/null | `null`              | Global/legacy graphic                           |
| `graphic_image_front`    | string/null | `null`              | Front graphic                                   |
| `graphic_image_back`     | string/null | `null`              | Back graphic                                    |
| `graphic_offset_x`       | number      | `0`                 | Global/legacy graphic X                         |
| `graphic_offset_y`       | number      | `0`                 | Global/legacy graphic Y                         |
| `graphic_offset_x_front` | number      | `0`                 | Front graphic X                                 |
| `graphic_offset_y_front` | number      | `0`                 | Front graphic Y                                 |
| `graphic_offset_x_back`  | number      | `0`                 | Back graphic X                                  |
| `graphic_offset_y_back`  | number      | `0`                 | Back graphic Y                                  |
| `logo_visible`           | boolean     | `true`              | Show logo                                       |
| `logo_text`              | string      | `"CA"`              | Logo text                                       |
| `logo_position`          | string      | `"left"`            | Logo position                                   |
| `logo_type`              | string      | `"text"`            | Logo type                                       |
| `doodle_mode`            | boolean     | `false`             | Doodle mode                                     |
| `doodle_color`           | string      | `"#141414"`         | Doodle color                                    |
| `doodle_shape`           | string      | `"round"`           | Doodle shape                                    |
| `doodle_size`            | number      | `8`                 | Doodle size                                     |
| `doodles`                | array       | `[]`                | Doodle data                                     |
| `selected_part`          | string      | `"body"`            | Selected garment part                           |
| `show_mannequin`         | boolean     | `true`              | Show mannequin                                  |
| `auto_rotate`            | boolean     | `true`              | Auto rotation                                   |


### Asset Size Metadata

| Asset Size ID | Chest                   | Length            | Unit |
| ------------- | ----------------------- | ----------------- | ---- |
| `xs`          | `84-89cm` / `33-35in`   | `68cm` / `26.8in` | `cm` |
| `s`           | `89-94cm` / `35-37in`   | `71cm` / `28in`   | `cm` |
| `m`           | `94-102cm` / `37-40in`  | `74cm` / `29.1in` | `cm` |
| `l`           | `102-109cm` / `40-43in` | `77cm` / `30.3in` | `cm` |
| `xl`          | `109-117cm` / `43-46in` | `80cm` / `31.5in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "sub_category": "casual-shirt",
  "material": "linen",
  "asset_size": "m",
  "fit": "slim",
  "collar": "point",
  "sleeve": "long",
  "closure": "buttons",
  "pocket": "none",
  "cuff": "standard"
}
```

---

## 1.3.3 Polo Shirt

`template_id`: `polo-shirt`

### Main Parameters

| Parameter    | Supported IDs                                                                             |
| ------------ | ----------------------------------------------------------------------------------------- |
| `gender`     | `male`, `female`, `unisex`, `kids`                                                        |
| `material`   | `default`, `pique-cotton`, `jersey`, `polyester`, `cotton-blend`, `performance`, `bamboo` |
| `asset_size` | `default`, `s`, `m`, `l`, `xl`, `2xl`                                                     |
| `fit`        | `slim`, `regular`, `relaxed`                                                              |
| `collar`     | `classic`, `spread`, `mandarin`                                                           |
| `placket`    | `two-button`, `three-button`, `zipper`, `snap`                                            |
| `sleeve`     | `short`, `long`, `raglan`                                                                 |
| `details`    | `chest-pocket`, `contrast-collar`, `contrast-cuff`, `embroidery`, `logo`                  |

### Asset Size Metadata

| Asset Size ID | Chest                   | Length            | Unit |
| ------------- | ----------------------- | ----------------- | ---- |
| `s`           | `89-94cm` / `35-37in`   | `68cm` / `26.8in` | `cm` |
| `m`           | `94-102cm` / `37-40in`  | `71cm` / `28in`   | `cm` |
| `l`           | `102-109cm` / `40-43in` | `74cm` / `29.1in` | `cm` |
| `xl`          | `109-117cm` / `43-46in` | `77cm` / `30.3in` | `cm` |
| `2xl`         | `117-125cm` / `47-50in` | `80cm` / `31.5in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "pique-cotton",
  "asset_size": "m",
  "fit": "regular",
  "collar": "classic",
  "placket": "two-button",
  "sleeve": "short",
  "details": "logo"
}
```

---

## 1.3.4 Hoodie / Sweatshirt

`template_id`: `hoodie`

### Main Parameters

| Parameter                | Type                                                                                               | Default           | Supported IDs                                                                                    |
|--------------------------|----------------------------------------------------------------------------------------------------| -------------- | ------------------------------------------------------------------------------------------------ |
| `gender`                 | string                                                                                             | `unisex`  | `unisex`, `male`, `female`, `kids`                                                               |
| `material`               | string                                                                                             | `default` | `default`, `fleece`, `french-terry`, `cotton`, `polyester`, `cotton-blend`, `heavyweight-cotton` |
| `asset_size`             | string                                                                                             | `default` | `default`, `s`, `m`, `l`, `xl`, `2xl`                                                            |
| `sub_category`  | string                                                                                             | `pullover`          | `pullover`, `zip`, `half-zip`, `crewneck`, `cropped`, `oversized`                                |
| `fit`               | string                                                                                             | `slim`      | `slim`, `regular`, `relaxed`, `oversized`                                                        |
| `hood`               | string                                                                                             | `standard`     | `standard`, `oversized`, `double-layer`, `none`                                                  |
| `pocket`            | string                                                                                                    | `kangaroo`      | `kangaroo`, `side`, `zipper`, `none`                                                             |
| `cuff`             | string  | `ribbed`       | `ribbed`, `elastic`, `open`                                                                      |
| `print_text`             | string                                                                                             | `"Craftsman Agent"` | Global/legacy print text                        |
| `print_text_front`       | string                                                                                             | `"Craftsman Agent"` | Front print text                                |
| `print_text_back`        | string                                                                                             | `"Craftsman Agent"` | Back print text                                 |
| `print_font`             | string                                                                                             | `"Great Vibes"`     | Print font                                      |
| `print_placement`        | string                                                                                             | `"front"`           | `front`, `back`, `both`                         |
| `print_scale`            | number                                                                                             | `1`                 | Global/legacy print scale                       |
| `print_scale_front`      | number                                                                                             | `1`                 | Front text scale                                |
| `print_scale_back`       | number                                                                                             | `1`                 | Back text scale                                 |
| `graphic_scale`          | number                                                                                             | `1`                 | Global/legacy graphic scale                     |
| `graphic_scale_front`    | number                                                                                             | `1`                 | Front graphic scale                             |
| `graphic_scale_back`     | number                                                                                             | `1`                 | Back graphic scale                              |
| `print_offset_x`         | number                                                                                             | `0`                 | Global/legacy print X                           |
| `print_offset_y`         | number                                                                                             | `0`                 | Global/legacy print Y                           |
| `print_offset_x_front`   | number                                                                                             | `0`                 | Front text X                                    |
| `print_offset_y_front`   | number                                                                                             | `0`                 | Front text Y                                    |
| `print_offset_x_back`    | number                                                                                             | `0`                 | Back text X                                     |
| `print_offset_y_back`    | number                                                                                             | `0`                 | Back text Y                                     |
| `graphic_style`          | string                                                                                             | `"none"`            | Graphic type/style                              |
| `graphic_image`          | string/null                                                                                        | `null`              | Global/legacy graphic                           |
| `graphic_image_front`    | string/null                                                                                        | `null`              | Front graphic                                   |
| `graphic_image_back`     | string/null                                                                                        | `null`              | Back graphic                                    |
| `graphic_offset_x`       | number                                                                                             | `0`                 | Global/legacy graphic X                         |
| `graphic_offset_y`       | number                                                                                             | `0`                 | Global/legacy graphic Y                         |
| `graphic_offset_x_front` | number                                                                                             | `0`                 | Front graphic X                                 |
| `graphic_offset_y_front` | number                                                                                             | `0`                 | Front graphic Y                                 |
| `graphic_offset_x_back`  | number                                                                                             | `0`                 | Back graphic X                                  |
| `graphic_offset_y_back`  | number                                                                                             | `0`                 | Back graphic Y                                  |
| `logo_visible`           | boolean                                                                                            | `true`              | Show logo                                       |
| `logo_text`              | string                                                                                             | `"CA"`              | Logo text                                       |
| `logo_position`          | string                                                                                             | `"left"`            | Logo position                                   |
| `logo_type`              | string                                                                                             | `"text"`            | Logo type                                       |
| `doodle_mode`            | boolean                                                                                            | `false`             | Doodle mode                                     |
| `doodle_color`           | string                                                                                             | `"#141414"`         | Doodle color                                    |
| `doodle_shape`           | string                                                                                             | `"round"`           | Doodle shape                                    |
| `doodle_size`            | number                                                                                             | `8`                 | Doodle size                                     |
| `doodles`                | array                                                                                              | `[]`                | Doodle data                                     |
| `selected_part`          | string                                                                                             | `"body"`            | Selected garment part                           |
| `show_mannequin`         | boolean                                                                                            | `true`              | Show mannequin                                  |
| `auto_rotate`            | boolean                                                                                            | `true`              | Auto rotation                                   |



### Asset Size Metadata

| Asset Size ID | Chest                   | Length            | Unit |
| ------------- | ----------------------- | ----------------- | ---- |
| `s`           | `90-96cm` / `35-38in`   | `68cm` / `26.8in` | `cm` |
| `m`           | `96-104cm` / `38-41in`  | `71cm` / `28in`   | `cm` |
| `l`           | `104-112cm` / `41-44in` | `74cm` / `29.1in` | `cm` |
| `xl`          | `112-120cm` / `44-47in` | `77cm` / `30.3in` | `cm` |
| `2xl`         | `120-128cm` / `47-50in` | `80cm` / `31.5in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "fleece",
  "asset_size": "m",
  "sub_category": "pullover",
  "fit": "relaxed",
  "hood": "standard",
  "pocket": "kangaroo",
  "cuff": "ribbed"
}
```

---

## 1.3.5 Jacket

`template_id`: `jacket`

### Main Parameters

| Parameter      | Supported IDs                                                                            |
| -------------- | ---------------------------------------------------------------------------------------- |
| `gender`       | `male`, `female`, `unisex`                                                               |
| `material`     | `default`, `leather`, `denim`, `cotton`, `nylon`, `polyester`, `wool`, `suede`, `canvas` |
| `asset_size`   | `default`, `s`, `m`, `l`, `xl`                                                           |
| `sub_category` | `bomber`, `varsity`, `denim`, `leather`, `utility`, `workwear`, `windbreaker`, `cropped` |
| `fit`          | `slim`, `regular`, `relaxed`, `oversized`                                                |
| `length`       | `cropped`, `waist`, `hip`, `long`                                                        |
| `collar`       | `stand`, `bomber`, `shirt`, `lapel`, `hood`                                              |
| `closure`      | `zipper`, `button`, `snap`, `belt`                                                       |
| `pockets`      | `side`, `chest`, `cargo`, `hidden`, `zipper`                                             |

### Asset Size Metadata

| Asset Size ID | Chest                   | Length            | Unit |
| ------------- | ----------------------- | ----------------- | ---- |
| `s`           | `90-96cm` / `35-38in`   | `65cm` / `25.6in` | `cm` |
| `m`           | `96-104cm` / `38-41in`  | `68cm` / `26.8in` | `cm` |
| `l`           | `104-112cm` / `41-44in` | `71cm` / `28in`   | `cm` |
| `xl`          | `112-120cm` / `44-47in` | `74cm` / `29.1in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "leather",
  "asset_size": "m",
  "sub_category": "bomber",
  "fit": "regular",
  "length": "waist",
  "collar": "bomber",
  "closure": "zipper",
  "pockets": "side"
}
```

---

## 1.3.6 Coat

`template_id`: `coat`

### Main Parameters

| Parameter      | Supported IDs                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------- |
| `gender`       | `male`, `female`, `unisex`                                                                      |
| `material`     | `default`, `wool`, `cashmere`, `cotton`, `nylon`, `polyester`, `down`, `wool-blend`, `faux-fur` |
| `asset_size`   | `default`, `s`, `m`, `l`, `xl`                                                                  |
| `sub_category` | `trench`, `peacoat`, `overcoat`, `parka`, `puffer`, `duffle`, `wool-coat`, `long-coat`          |
| `length`       | `waist`, `hip`, `knee`, `full`                                                                  |
| `fit`          | `slim`, `regular`, `relaxed`, `oversized`                                                       |
| `collar`       | `lapel`, `stand`, `shawl`, `hood`, `fur`                                                        |
| `closure`      | `button`, `double-breasted`, `zipper`, `belt`, `toggle`                                         |
| `lining`       | `cotton`, `polyester`, `satin`, `quilted`, `fleece`                                             |

### Asset Size Metadata

| Asset Size ID | Chest                   | Length             | Unit |
| ------------- | ----------------------- | ------------------ | ---- |
| `s`           | `90-96cm` / `35-38in`   | `85cm` / `33.5in`  | `cm` |
| `m`           | `96-104cm` / `38-41in`  | `90cm` / `35.4in`  | `cm` |
| `l`           | `104-112cm` / `41-44in` | `95cm` / `37.4in`  | `cm` |
| `xl`          | `112-120cm` / `44-47in` | `100cm` / `39.4in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "wool",
  "asset_size": "m",
  "sub_category": "trench",
  "length": "full",
  "fit": "regular",
  "collar": "lapel",
  "closure": "belt",
  "lining": "polyester"
}
```

---

## 1.3.7 Dress

`template_id`: `dress`

### Main Parameters

| Parameter      | Supported IDs                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| `gender`       | `female`, `kids`                                                                                           |
| `material`     | `default`, `cotton`, `linen`, `silk`, `satin`, `chiffon`, `velvet`, `lace`, `polyester`, `rayon`, `jersey` |
| `asset_size`   | `default`, `xs`, `s`, `m`, `l`, `xl`                                                                       |
| `sub_category` | `mini`, `midi`, `maxi`, `bodycon`, `a-line`, `slip`, `shirt-dress`, `evening`, `cocktail`                  |
| `silhouette`   | `straight`, `a-line`, `bodycon`, `fit-flare`, `oversized`                                                  |
| `neckline`     | `round`, `v-neck`, `square`, `halter`, `sweetheart`, `off-shoulder`                                        |
| `sleeve`       | `sleeveless`, `short`, `long`, `puff`, `bell`                                                              |
| `waist`        | `natural`, `high`, `low`, `empire`, `none`                                                                 |
| `skirt`        | `straight`, `pleated`, `flared`, `tiered`, `asymmetric`                                                    |
| `details`      | `slit`, `ruffle`, `lace`, `draping`, `bow`, `beading`                                                      |

### Asset Size Metadata

| Asset Size ID | Bust                        | Waist                     | Unit |
| ------------- | --------------------------- | ------------------------- | ---- |
| `xs`          | `80-84cm` / `31.5-33in`     | `60-64cm` / `23.6-25.2in` | `cm` |
| `s`           | `84-88cm` / `33-34.6in`     | `64-68cm` / `25.2-26.8in` | `cm` |
| `m`           | `88-94cm` / `34.6-37in`     | `68-74cm` / `26.8-29.1in` | `cm` |
| `l`           | `94-100cm` / `37-39.4in`    | `74-80cm` / `29.1-31.5in` | `cm` |
| `xl`          | `100-108cm` / `39.4-42.5in` | `80-88cm` / `31.5-34.6in` | `cm` |

### Example `options`

```json
{
  "gender": "female",
  "material": "silk",
  "asset_size": "m",
  "sub_category": "maxi",
  "silhouette": "a-line",
  "neckline": "v-neck",
  "sleeve": "sleeveless",
  "waist": "natural",
  "skirt": "flared",
  "details": "draping"
}
```

---

## 1.3.8 Skirt

`template_id`: `skirt`

### Main Parameters

| Parameter      | Supported IDs                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------- |
| `gender`       | `female`, `kids`                                                                                |
| `sub_category` | `mini`, `midi`, `maxi`, `pencil`, `a-line`, `pleated`, `wrap`, `cargo`                          |
| `material`     | `default`, `cotton`, `denim`, `linen`, `wool`, `silk`, `satin`, `polyester`, `leather`, `tweed` |
| `asset_size`   | `default`, `xs`, `s`, `m`, `l`, `xl`                                                            |
| `waist`        | `low-rise`, `mid-rise`, `high-rise`                                                             |
| `silhouette`   | `straight`, `a-line`, `flared`, `bodycon`, `asymmetric`                                         |
| `length`       | `mini`, `knee`, `midi`, `maxi`                                                                  |
| `closure`      | `zipper`, `button`, `hook`, `elastic`, `wrap`                                                   |
| `details`      | `pleats`, `slit`, `pockets`, `belt-loops`, `ruffle`                                             |

### Asset Size Metadata

| Asset Size ID | Waist                     | Hip                         | Unit |
| ------------- | ------------------------- | --------------------------- | ---- |
| `xs`          | `60-64cm` / `23.6-25.2in` | `84-88cm` / `33-34.6in`     | `cm` |
| `s`           | `64-68cm` / `25.2-26.8in` | `88-92cm` / `34.6-36.2in`   | `cm` |
| `m`           | `68-74cm` / `26.8-29.1in` | `92-98cm` / `36.2-38.6in`   | `cm` |
| `l`           | `74-80cm` / `29.1-31.5in` | `98-104cm` / `38.6-40.9in`  | `cm` |
| `xl`          | `80-88cm` / `31.5-34.6in` | `104-112cm` / `40.9-44.1in` | `cm` |

### Example `options`

```json
{
  "gender": "female",
  "sub_category": "pleated",
  "material": "polyester",
  "asset_size": "m",
  "waist": "high-rise",
  "silhouette": "a-line",
  "length": "midi",
  "closure": "zipper",
  "details": "pleats"
}
```

---

## 1.3.9 Pants / Trousers

`template_id`: `pants`

### Main Parameters

| Parameter      | Supported IDs                                                                                            |
| -------------- | -------------------------------------------------------------------------------------------------------- |
| `gender`       | `male`, `female`, `unisex`, `kids`                                                                       |
| `sub_category` | `straight`, `wide-leg`, `slim`, `skinny`, `cargo`, `flare`, `pleated`, `dress-pants`                     |
| `material`     | `default`, `cotton`, `linen`, `wool`, `polyester`, `rayon`, `nylon`, `corduroy`, `twill`, `cotton-blend` |
| `asset_size`   | `default`, `28`, `30`, `32`, `34`, `36`, `38`                                                            |
| `fit`          | `slim`, `regular`, `relaxed`, `oversized`                                                                |
| `rise`         | `low`, `mid`, `high`                                                                                     |
| `leg`          | `straight`, `wide`, `tapered`, `flared`, `cropped`                                                       |
| `length`       | `cropped`, `ankle`, `full`                                                                               |
| `waist`        | `button`, `hook`, `elastic`, `drawstring`                                                                |
| `details`      | `pleats`, `cuffs`, `pockets`, `belt-loops`, `side-stripes`                                               |

### Asset Size Metadata

| Asset Size ID | Waist           | Inseam          | Unit |
| ------------- | --------------- | --------------- | ---- |
| `28`          | `71cm` / `28in` | `81cm` / `32in` | `cm` |
| `30`          | `76cm` / `30in` | `81cm` / `32in` | `cm` |
| `32`          | `81cm` / `32in` | `81cm` / `32in` | `cm` |
| `34`          | `86cm` / `34in` | `84cm` / `33in` | `cm` |
| `36`          | `91cm` / `36in` | `84cm` / `33in` | `cm` |
| `38`          | `97cm` / `38in` | `84cm` / `33in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "sub_category": "straight",
  "material": "cotton-blend",
  "asset_size": "32",
  "fit": "regular",
  "rise": "mid",
  "leg": "straight",
  "length": "full",
  "waist": "button",
  "details": "pockets"
}
```

---

##1.3.10 Jeans

`template_id`: `jeans`

### Main Parameters

| Parameter      | Supported IDs                                                                              |
| -------------- | ------------------------------------------------------------------------------------------ |
| `gender`       | `male`, `female`, `unisex`, `kids`                                                         |
| `sub_category` | `skinny`, `slim`, `straight`, `relaxed`, `baggy`, `wide-leg`, `bootcut`, `flare`           |
| `material`     | `default`, `raw-denim`, `stretch-denim`, `organic-denim`, `cotton-denim`, `recycled-denim` |
| `asset_size`   | `default`, `28`, `30`, `32`, `34`, `36`, `38`                                              |
| `rise`         | `low`, `mid`, `high`                                                                       |
| `wash`         | `raw`, `dark`, `medium`, `light`, `acid`, `black`                                          |
| `distressing`  | `none`, `light`, `medium`, `heavy`                                                         |
| `stretch`      | `none`, `low`, `medium`, `high`                                                            |
| `details`      | `rivets`, `contrast-stitch`, `patches`, `embroidery`, `cargo-pockets`                      |
| `denim_weight` | `light`, `medium`, `heavy`                                                                 |
| `thread_color` | `matching`, `gold`, `orange`, `contrast`                                                   |
| `button_type`  | `metal`, `brass`, `antique`                                                                |
| `wash_process` | `raw`, `rinse`, `stone`, `acid`, `enzyme`                                                  |

### Asset Size Metadata

| Asset Size ID | Waist           | Inseam          | Unit |
| ------------- | --------------- | --------------- | ---- |
| `28`          | `71cm` / `28in` | `81cm` / `32in` | `cm` |
| `30`          | `76cm` / `30in` | `81cm` / `32in` | `cm` |
| `32`          | `81cm` / `32in` | `81cm` / `32in` | `cm` |
| `34`          | `86cm` / `34in` | `84cm` / `33in` | `cm` |
| `36`          | `91cm` / `36in` | `84cm` / `33in` | `cm` |
| `38`          | `97cm` / `38in` | `84cm` / `33in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "sub_category": "slim",
  "material": "stretch-denim",
  "asset_size": "32",
  "rise": "mid",
  "wash": "medium",
  "distressing": "light",
  "stretch": "low",
  "details": "contrast-stitch",
  "denim_weight": "medium",
  "thread_color": "orange",
  "button_type": "metal",
  "wash_process": "stone"
}
```

---

##1.3.11 Shorts

`template_id`: `shorts`

### Main Parameters

| Parameter      | Supported IDs                                                                         |
| -------------- | ------------------------------------------------------------------------------------- |
| `gender`       | `male`, `female`, `unisex`, `kids`                                                    |
| `material`     | `default`, `cotton`, `denim`, `linen`, `nylon`, `polyester`, `jersey`, `french-terry` |
| `asset_size`   | `default`, `s`, `m`, `l`, `xl`                                                        |
| `sub_category` | `casual`, `denim`, `cargo`, `athletic`, `tailored`, `lounge`                          |
| `fit`          | `slim`, `regular`, `relaxed`, `oversized`                                             |
| `rise`         | `low`, `mid`, `high`                                                                  |
| `length`       | `short`, `mid`, `long`                                                                |
| `closure`      | `button`, `zipper`, `elastic`, `drawstring`                                           |
| `details`      | `pockets`, `cargo-pockets`, `side-stripe`, `logo`, `embroidery`                       |

### Asset Size Metadata

| Asset Size ID | Waist                 | Outseam           | Unit |
| ------------- | --------------------- | ----------------- | ---- |
| `s`           | `71-76cm` / `28-30in` | `40cm` / `15.7in` | `cm` |
| `m`           | `76-81cm` / `30-32in` | `42cm` / `16.5in` | `cm` |
| `l`           | `81-86cm` / `32-34in` | `44cm` / `17.3in` | `cm` |
| `xl`          | `86-91cm` / `34-36in` | `46cm` / `18.1in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "cotton",
  "asset_size": "m",
  "sub_category": "casual",
  "fit": "relaxed",
  "rise": "mid",
  "length": "mid",
  "closure": "drawstring",
  "details": "pockets"
}
```

---

## 1.3.12 Hat / Cap

`template_id`: `hat`

### Main Parameters

| Parameter      | Supported IDs                                                                            |
| -------------- | ---------------------------------------------------------------------------------------- |
| `gender`       | `unisex`, `male`, `female`, `kids`                                                       |
| `sub_category` | `baseball`, `snapback`, `trucker`, `bucket`, `beanie`, `visor`, `sun-hat`, `fedora`      |
| `material`     | `default`, `cotton`, `wool`, `acrylic`, `polyester`, `denim`, `canvas`, `straw`, `nylon` |
| `asset_size`   | `default`, `small`, `medium`, `large`, `xlarge`                                          |
| `crown`        | `low`, `mid`, `high`                                                                     |
| `brim`         | `flat`, `curved`, `wide`, `short`                                                        |
| `closure`      | `snapback`, `buckle`, `velcro`, `elastic`, `fitted`                                      |
| `decoration`   | `embroidery`, `patch`, `print`, `woven-label`, `metal-badge`, `3d-logo`                  |

### Asset Size Metadata

| Asset Size ID | Head Circumference | Unit |
| ------------- | ------------------ | ---- |
| `small`       | `54cm` / `21.3in`  | `cm` |
| `medium`      | `57cm` / `22.4in`  | `cm` |
| `large`       | `60cm` / `23.6in`  | `cm` |
| `xlarge`      | `62cm` / `24.4in`  | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "sub_category": "baseball",
  "material": "cotton",
  "asset_size": "medium",
  "crown": "mid",
  "brim": "curved",
  "closure": "snapback",
  "decoration": "embroidery"
}
```

---

## 1.3.13 Scarf

`template_id`: `scarf`

### Main Parameters

| Parameter      | Supported IDs                                                                              |
| -------------- | ------------------------------------------------------------------------------------------ |
| `gender`       | `unisex`, `male`, `female`, `kids`                                                         |
| `material`     | `default`, `wool`, `cashmere`, `cotton`, `silk`, `polyester`, `acrylic`, `fleece`, `linen` |
| `asset_size`   | `default`, `short`, `medium`, `long`, `oversized`                                          |
| `sub_category` | `fashion`, `winter`, `knit`, `silk`, `infinity`, `neck-gaiter`, `souvenir`                 |
| `shape`        | `rectangular`, `square`, `triangle`, `infinity`                                            |
| `length`       | `short`, `medium`, `long`, `custom`                                                        |
| `width`        | `narrow`, `standard`, `wide`, `custom`                                                     |
| `edge`         | `hemmed`, `fringe`, `tassel`, `rolled`, `embroidered`                                      |
| `pattern`      | `solid`, `stripe`, `plaid`, `floral`, `geometric`, `custom`                                |

### Asset Size Metadata

| Asset Size ID | Length             | Width             | Unit |
| ------------- | ------------------ | ----------------- | ---- |
| `short`       | `120cm` / `47.2in` | `20cm` / `7.9in`  | `cm` |
| `medium`      | `160cm` / `63in`   | `25cm` / `9.8in`  | `cm` |
| `long`        | `200cm` / `78.7in` | `30cm` / `11.8in` | `cm` |
| `oversized`   | `220cm` / `86.6in` | `50cm` / `19.7in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "cashmere",
  "asset_size": "medium",
  "sub_category": "fashion",
  "shape": "rectangular",
  "length": "medium",
  "width": "standard",
  "edge": "fringe",
  "pattern": "solid"
}
```

---

## 1.3.14 Gloves

`template_id`: `gloves`

### Main Parameters

| Parameter      | Supported IDs                                                                        |
| -------------- | ------------------------------------------------------------------------------------ |
| `gender`       | `unisex`, `male`, `female`, `kids`                                                   |
| `material`     | `default`, `leather`, `wool`, `cashmere`, `cotton`, `fleece`, `acrylic`, `synthetic` |
| `asset_size`   | `default`, `xs`, `s`, `m`, `l`, `xl`                                                 |
| `sub_category` | `winter`, `fashion`, `knit`, `leather`, `touchscreen`, `fingerless`, `mittens`       |
| `finger`       | `full`, `fingerless`, `mitten`                                                       |
| `length`       | `wrist`, `short`, `mid`, `long`                                                      |
| `cuff`         | `elastic`, `ribbed`, `button`, `strap`, `long`                                       |
| `details`      | `embroidery`, `logo`, `patch`, `pattern`, `touchscreen`                              |

### Asset Size Metadata

| Asset Size ID | Hand Circumference      | Unit |
| ------------- | ----------------------- | ---- |
| `xs`          | `16-17cm` / `6.3-6.7in` | `cm` |
| `s`           | `17-18cm` / `6.7-7.1in` | `cm` |
| `m`           | `18-20cm` / `7.1-7.9in` | `cm` |
| `l`           | `20-22cm` / `7.9-8.7in` | `cm` |
| `xl`          | `22-24cm` / `8.7-9.4in` | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "material": "wool",
  "asset_size": "m",
  "sub_category": "winter",
  "finger": "full",
  "length": "wrist",
  "cuff": "ribbed",
  "details": "logo"
}
```

---

##1.3.15 Socks

`template_id`: `socks`

### Main Parameters

| Parameter      | Supported IDs                                                                          |
| -------------- | -------------------------------------------------------------------------------------- |
| `gender`       | `unisex`, `male`, `female`, `kids`                                                     |
| `sub_category` | `no-show`, `ankle`, `crew`, `mid-calf`, `knee-high`, `athletic`, `novelty`             |
| `material`     | `default`, `cotton`, `wool`, `bamboo`, `polyester`, `nylon`, `spandex`, `cotton-blend` |
| `asset_size`   | `default`, `xs`, `s`, `m`, `l`, `xl`                                                   |
| `cuff`         | `standard`, `ribbed`, `compression`                                                    |
| `toe`          | `standard`, `reinforced`, `contrast`                                                   |
| `design`       | `solid`, `stripe`, `pattern`, `graphic`, `logo`, `character`                           |
| `cushion`      | `none`, `light`, `medium`, `heavy`                                                     |

### Asset Size Metadata

| Asset Size ID | Foot Length              | US Shoe Size | Unit |
| ------------- | ------------------------ | ------------ | ---- |
| `xs`          | `20-22cm` / `7.9-8.7in`  | `4-6`        | `cm` |
| `s`           | `22-24cm` / `8.7-9.4in`  | `6-8`        | `cm` |
| `m`           | `24-26cm` / `9.4-10.2in` | `8-10`       | `cm` |
| `l`           | `26-28cm` / `10.2-11in`  | `10-12`      | `cm` |
| `xl`          | `28-30cm` / `11-11.8in`  | `12-14`      | `cm` |

### Example `options`

```json
{
  "gender": "unisex",
  "sub_category": "athletic",
  "material": "cotton",
  "asset_size": "m",
  "cuff": "ribbed",
  "toe": "reinforced",
  "design": "logo",
  "cushion": "medium"
}
```

---

# 7. Clothing Design Parameter Rules

1. Always use the exact `template_id` from the supported Clothing Designer template list.
2. Always use the exact **option IDs** listed for the selected template.
3. Do not use display names such as `Cotton`, `Regular`, `Slim Fit`, or `Graphic T-Shirt` as structured option values; use IDs such as `cotton`, `regular`, `slim-fit`, and `graphic`.
4. Only pass parameters explicitly defined by the selected clothing template.
5. Do not pass parameters from another clothing template.
6. `asset_size` values must use the exact supported IDs for the selected template.
7. Size metadata such as chest, waist, bust, hip, hand circumference, foot length, or head circumference is descriptive metadata and should not replace the corresponding `asset_size` ID.
8. Scalar dimensions and customization values can be included when supported by the API or described in `prompt`.
9. When a user gives natural-language requirements, map requirements to the closest supported IDs.
10. Preserve design details that cannot be represented by structured options in `prompt`.
11. Reference images should be passed through `images`.
12. Use `prompt` to describe material appearance, texture, construction, silhouette, printing, embroidery, logo placement, color, artwork, decoration, and manufacturing intent when no dedicated structured parameter exists.
13. For customized text or logo printing, specify the exact text, logo, placement, color, scale, and orientation in `prompt`.
14. For POD designs, describe the printable artwork and placement clearly.
15. For MOD designs, describe construction, material, finishing, dimensions, and manufacturing requirements clearly.
16. If the user specifies a parameter value that is not supported, choose the closest supported ID and preserve the original requirement in `prompt`.
17. Do not invent unsupported option IDs.
18. Keep `options` limited to structured parameters relevant to the selected `template_id`.
19. Use `provider_model_id: "default"` unless a specific supported provider/model is requested.
20. Use `mode: "basic"`, `"standard"`, or `"advanced"` for actual generation. Use `"demo"` only for debug or predefined-result testing.
21. When generation returns `share_url`, provide the URL to the user so they can view the Clothing Designer workspace and generated results online.
22. The generated design may include an interactive 3D model, multi-view images, front view, back view, side view, and other available design assets.

---

# 8. Natural Language to Structured Options

When a user says:

```text
Create a relaxed oversized black cotton T-shirt for men.
```

Map it to:

```json
{
  "gender": "male",
  "sub_category": "basic",
  "material": "cotton",
  "asset_size": "default",
  "fit": "oversized"
}
```

and preserve the color requirement in the prompt:

```text
Create a black oversized cotton T-shirt for men.
```

When a user says:

```text
Make a long cashmere scarf with fringed edges.
```

Map it to:

```json
{
  "gender": "unisex",
  "material": "cashmere",
  "asset_size": "long",
  "length": "long",
  "edge": "fringe"
}
```

When a user says:

```text
Create a slim mid-rise pair of blue jeans with light distressing.
```

Map it to:

```json
{
  "gender": "unisex",
  "sub_category": "slim",
  "material": "default",
  "asset_size": "default",
  "rise": "mid",
  "wash": "medium",
  "distressing": "light"
}
```

The exact color or visual appearance can remain in `prompt` if it is not represented by a structured parameter.

---

# 9. Custom Printing and Personalization

Clothing designs can contain customized:

* Text
* Logos
* Artwork
* Graphics
* Embroidery
* Patches
* Labels
* Character graphics
* Brand marks
* Front prints
* Back prints
* Placement-specific decoration

For example:

```text
Design a white cotton graphic T-shirt with a regular fit.
Place the text "AI Agent A2Z" centered on the front in dark green.
Add the Craftsman Agent logo underneath the text.
Use a clean premium streetwear aesthetic.
```

When a structured parameter is not available for a specific print or personalization requirement, keep the structured clothing configuration in `options` and describe the exact customization in `prompt`.

---

# 10. Reference Images

Reference images can be supplied through:

```json
{
  "images": [
    "https://example.com/reference-front.jpg",
    "https://example.com/reference-material.jpg"
  ]
}
```

Use the `prompt` to explain how the references should influence the generated design.

For example:

```text
Use the first image as the silhouette reference and the second
image as the material and texture reference. Preserve the overall
construction while changing the garment to an oversized cotton
T-shirt with a black base color and customized front typography.
```

---

# 11. Design Generation Guidelines

The Clothing Designer should:

* Select the correct clothing `template_id`.
* Map natural language to supported option IDs.
* Keep structured parameters inside `options`.
* Keep free-form visual and manufacturing requirements inside `prompt`.
* Use reference images when supplied.
* Generate designs appropriate for the selected clothing category.
* Preserve requested dimensions and size information.
* Preserve requested material and texture.
* Preserve fit and silhouette.
* Preserve closure and construction details.
* Preserve printing, embroidery, logo, and decoration requirements.
* Generate multi-view references when available.
* Return the generated workspace through `share_url` when available.

The API should not assume that a parameter available for one clothing category is available for another category.

---

# 12. Example Complete Request

```json
{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "clothing_generator_design_draft",
  "data": {
    "prompt": "Design a premium oversized cotton graphic T-shirt for a unisex streetwear collection. Use a black base color. Print 'AI Agent A2Z' centered on the front in a clean modern style and place the Craftsman Agent logo underneath. Generate a professional multi-view product design suitable for POD.",
    "images": [],
    "template_id": "t-shirt",
    "provider_model_id": "default",
    "options": {
      "gender": "unisex",
      "sub_category": "graphic",
      "material": "cotton",
      "asset_size": "m",
      "fit": "oversized",
      "neckline": "crew",
      "sleeve": "short",
      "length": "hip",
      "hem_style": "straight"
    },
    "session_name": "AI Agent A2Z Graphic T-Shirt",
    "tag_list": "t-shirt,graphic,streetwear,pod",
    "mode": "basic"
  }
}
```

---

# 13. Important API Naming

The Clothing Designer API is:

```text
clothing_generator_design_draft
```

The OneKey Agent is:

```text
craftsman-agent/craftsman-agent
```

The gateway is:

```text
https://agent.deepnlp.org/agent_router
```

The primary Clothing Designer application is:

```text
https://craftsman-agent.aiagenta2z.com/app/clothing-designer
```

Use these identifiers consistently when constructing API and CLI requests.
