---
name: "xiaohongshu-post-generator"
description: "AI Xiaohongshu Post Generator — Generate editable, Xiaohongshu - ready posts and slides with AI-created content, captions, images, text blocks, storylines, and backgrounds. Supports Knowledge Cards, Posters, Movie Introductions, and more, with designs automatically structured according to visual style rules. Powered by Nano Banana, Nano Banana 2, and Imagen 2, with export-ready final posts and slides."
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: Onekey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# AI Xiaohongshu Post Generator Generator Skills from craftsman-agent

Auto-generated skill for OneKey Agent Gateway registered agent `craftsman-agent/craftsman-agent` for the API ID `social_media_posts`.

| Section                                       | Description                                                |
|-----------------------------------------------|------------------------------------------------------------|
| Craftsman Social Media Posts Generator Online | https://craftsman-agent.aiagenta2z.com/app/social-media-posts |
| Craftsman Website                             | https://craftsman-agent.aiagenta2z.com                     |
| Craftsman App                                 | https://craftsman-agent.aiagenta2z.com/app                 |
| Craftsman Gallery                             | https://craftsman-agent.aiagenta2z.com/gallery             |
| Craftsman Workspace                           | https://craftsman-agent.aiagenta2z.com/workspace           |
| Craftsman Marketplace                         | https://craftsman-agent.aiagenta2z.com/marketplace         |
| Craftsman Store Manufacturing on Demand Platform | https://craftsman-agent.aiagenta2z.com/store               |

## Quick Start

This is a demo to generate an 2 pages Instagram Ready Social Media Posts using just simple text and reference images prompts. The AI X-Twitter posts asset size ratio/width/height can be customized.
The final generated assets (contents, images, captains, backgrounds) are editable, and the generated final posts can be exported and published to X-Twitter instantly.

| Item                | Value                                                                                                                                                                       |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| prompt              | Write a simple character introduction for the movie Odyssey                                                                                                                 |
| Task                | Task:  Briefly describe the main characters, their roles, personalities, and relationships.  Choose Instagram as distribution channel, output imags using 4:5 images ratios |
| Final Workspace URL | https://craftsman-agent.aiagenta2z.com/app/sessions/share/4d7342da-ea5b-45c0-8e53-f0a1ae6d0183                                                                              |


## 1. API Usage

Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://deepnlp.org/workspace/keys).

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

### OneKey Router

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "social_media_posts",
  "data": {
      "prompt": "=== User Prompt ===\n\Write a simple character introduction for the movie Odyssey\n=== STYLE RULES ===\n\n\\u2022 Clear editorial knowledge cards with strong visual hierarchy and generous negative space\n\n=== PRINT SPECIFICATIONS ===\n\n\\u2022 Keep final typography in editable layers; generated illustrations must contain no text or watermark\n\n\n=== SOCIAL MEDIA POSTS CONFIG ===\n\n{\"template_id\":\"knowledge-card\",\"card_count\":4,\"asset_size\":[{\"width\":1080,\"height\":1080,\"ratio\":\"1:1\"}],\"card_count_source\":\"default\",\"channel_profile\":\"xiaohongshu\",\"audience_profile\":\"general\",\"age_band\":\"auto\",\"profile_version\":\"1.0.0\",\"geometry_source\":\"profile\",\"resolved_profiles\":[{\"type\":\"channel\",\"id\":\"xiaohongshu\",\"version\":\"1.0.0\"},{\"type\":\"audience\",\"id\":\"general\",\"version\":\"1.0.0\"}],\"language\":\"auto\",\"mode\":\"demo\",\"text_model\":\"default\",\"image_model\":\"default\",\"styles\":[\"Clear editorial knowledge cards with strong visual hierarchy and generous negative space\"],\"constraints\":[\"Keep final typography in editable layers; generated illustrations must contain no text or watermark\"],\"social_brief_inputs\":[{\"id\":\"binp-1\",\"type\":\"prompt\",\"content\":\"\"},{\"id\":\"binp-2\",\"type\":\"style\",\"content\":\"Clear editorial knowledge cards with strong visual hierarchy and generous negative space\"},{\"id\":\"binp-3\",\"type\":\"constraint\",\"content\":\"Keep final typography in editable layers; generated illustrations must contain no text or watermark\"}],\"text_styles\":{\"brand\":{\"color\":\"#6D5DFB\",\"font\":\"Inter\",\"font_size\":\"20px\",\"font_weight\":\"600\",\"text_align\":\"left\",\"line_height\":1.3,\"letter_spacing\":0},\"headline\":{\"color\":\"#172033\",\"font\":\"Inter\",\"font_size\":\"48px\",\"font_weight\":\"700\",\"text_align\":\"left\",\"line_height\":1.3,\"letter_spacing\":0},\"content\":{\"color\":\"#374151\",\"font\":\"Inter\",\"font_size\":\"24px\",\"font_weight\":\"400\",\"text_align\":\"left\",\"line_height\":1.3,\"letter_spacing\":0},\"footer\":{\"color\":\"#6B7280\",\"font\":\"Inter\",\"font_size\":\"16px\",\"font_weight\":\"400\",\"text_align\":\"left\",\"line_height\":1.3,\"letter_spacing\":0}},\"page_templates\":[{\"id\":\"knowledge-card-01\",\"label\":\"Knowledge Card 01\",\"layers\":[{\"id\":\"knowledge-card-01-background-0\",\"type\":\"background\",\"name\":\"Background\",\"position\":{\"x\":0,\"y\":0},\"size\":{\"width\":1080,\"height\":1440},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-01-brand-1\",\"type\":\"brand\",\"name\":\"Brand\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-01-image-2\",\"type\":\"image\",\"name\":\"Illustration\",\"position\":{\"x\":80,\"y\":288},\"size\":{\"width\":920,\"height\":605},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-01-headline-3\",\"type\":\"text\",\"name\":\"Headline\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-01-content-4\",\"type\":\"text\",\"name\":\"Content\",\"position\":{\"x\":80,\"y\":950},\"size\":{\"width\":920,\"height\":288},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-01-footer-5\",\"type\":\"cta\",\"name\":\"Footer\",\"position\":{\"x\":80,\"y\":1311},\"size\":{\"width\":920,\"height\":73},\"style_overrides\":[],\"if_selected\":false}]},{\"id\":\"knowledge-card-02\",\"label\":\"Knowledge Card 02\",\"layers\":[{\"id\":\"knowledge-card-02-background-0\",\"type\":\"background\",\"name\":\"Background\",\"position\":{\"x\":0,\"y\":0},\"size\":{\"width\":1080,\"height\":1440},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-02-brand-1\",\"type\":\"brand\",\"name\":\"Brand\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-02-image-2\",\"type\":\"image\",\"name\":\"Illustration\",\"position\":{\"x\":80,\"y\":288},\"size\":{\"width\":920,\"height\":605},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-02-headline-3\",\"type\":\"text\",\"name\":\"Headline\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-02-content-4\",\"type\":\"text\",\"name\":\"Content\",\"position\":{\"x\":80,\"y\":950},\"size\":{\"width\":920,\"height\":288},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-02-footer-5\",\"type\":\"cta\",\"name\":\"Footer\",\"position\":{\"x\":80,\"y\":1311},\"size\":{\"width\":920,\"height\":73},\"style_overrides\":[],\"if_selected\":false}]},{\"id\":\"knowledge-card-03\",\"label\":\"Knowledge Card 03\",\"layers\":[{\"id\":\"knowledge-card-03-background-0\",\"type\":\"background\",\"name\":\"Background\",\"position\":{\"x\":0,\"y\":0},\"size\":{\"width\":1080,\"height\":1440},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-03-brand-1\",\"type\":\"brand\",\"name\":\"Brand\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-03-image-2\",\"type\":\"image\",\"name\":\"Illustration\",\"position\":{\"x\":80,\"y\":288},\"size\":{\"width\":920,\"height\":605},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-03-headline-3\",\"type\":\"text\",\"name\":\"Headline\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-03-content-4\",\"type\":\"text\",\"name\":\"Content\",\"position\":{\"x\":80,\"y\":950},\"size\":{\"width\":920,\"height\":288},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-03-footer-5\",\"type\":\"cta\",\"name\":\"Footer\",\"position\":{\"x\":80,\"y\":1311},\"size\":{\"width\":920,\"height\":73},\"style_overrides\":[],\"if_selected\":false}]},{\"id\":\"knowledge-card-04\",\"label\":\"Knowledge Card 04\",\"layers\":[{\"id\":\"knowledge-card-04-background-0\",\"type\":\"background\",\"name\":\"Background\",\"position\":{\"x\":0,\"y\":0},\"size\":{\"width\":1080,\"height\":1440},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-04-brand-1\",\"type\":\"brand\",\"name\":\"Brand\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-04-image-2\",\"type\":\"image\",\"name\":\"Illustration\",\"position\":{\"x\":80,\"y\":288},\"size\":{\"width\":920,\"height\":605},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-04-headline-3\",\"type\":\"text\",\"name\":\"Headline\",\"position\":{\"x\":80,\"y\":86},\"size\":{\"width\":920,\"height\":130},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-04-content-4\",\"type\":\"text\",\"name\":\"Content\",\"position\":{\"x\":80,\"y\":950},\"size\":{\"width\":920,\"height\":288},\"style_overrides\":[],\"if_selected\":false},{\"id\":\"knowledge-card-04-footer-5\",\"type\":\"cta\",\"name\":\"Footer\",\"position\":{\"x\":80,\"y\":1311},\"size\":{\"width\":920,\"height\":73},\"style_overrides\":[],\"if_selected\":false}]}]}",
      "images": [],
      "mode": "demo",
      "session_name": "Movie Odyssey Character Introduction Knowledge Card Set",
      "tag_list": "",
      "api_id": "social_media_posts",
      "card_count": 2,
      "template_id": "knowledge-card",
      "asset_size": [
        {
          "width": 1080,
          "height": 1350,
          "ratio": "4:5"
        }
      ],
      "model": "default",
      "styles": [
        "Clear editorial knowledge cards with strong visual hierarchy and generous negative space"
      ],
      "channel_profile": "xiaohongshu",
      "audience_profile": "general",
      "age_band": "auto",
      "profile_version": "1.0.0",
      "geometry_source": "profile",
      "resolved_profiles": [
        {
          "type": "channel",
          "id": "xiaohongshu",
          "version": "1.0.0"
        },
        {
          "type": "audience",
          "id": "general",
          "version": "1.0.0"
        }
      ],    
    "design_config": {"template_id":"knowledge-card","card_count":4,"asset_size":[{"width":1080,"height":1080,"ratio":"1:1"}],"card_count_source":"default","channel_profile":"xiaohongshu","audience_profile":"general","age_band":"auto","profile_version":"1.0.0","geometry_source":"profile","resolved_profiles":[{"type":"channel","id":"xiaohongshu","version":"1.0.0"},{"type":"audience","id":"general","version":"1.0.0"}],"language":"auto","mode":"demo","text_model":"default","image_model":"default","styles":["Clear editorial knowledge cards with strong visual hierarchy and generous negative space"],"constraints":["Keep final typography in editable layers; generated illustrations must contain no text or watermark"],"social_brief_inputs":[{"id":"binp-1","type":"prompt","content":""},{"id":"binp-2","type":"style","content":"Clear editorial knowledge cards with strong visual hierarchy and generous negative space"},{"id":"binp-3","type":"constraint","content":"Keep final typography in editable layers; generated illustrations must contain no text or watermark"}],"text_styles":{"brand":{"color":"#6D5DFB","font":"Inter","font_size":"20px","font_weight":"600","text_align":"left","line_height":1.3,"letter_spacing":0},"headline":{"color":"#172033","font":"Inter","font_size":"48px","font_weight":"700","text_align":"left","line_height":1.3,"letter_spacing":0},"content":{"color":"#374151","font":"Inter","font_size":"24px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"footer":{"color":"#6B7280","font":"Inter","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0}},"page_templates":[{"id":"knowledge-card-01","label":"Knowledge Card 01","layers":[{"id":"knowledge-card-01-background-0","type":"background","name":"Background","position":{"x":0,"y":0},"size":{"width":1080,"height":1440},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-01-brand-1","type":"brand","name":"Brand","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-01-image-2","type":"image","name":"Illustration","position":{"x":80,"y":288},"size":{"width":920,"height":605},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-01-headline-3","type":"text","name":"Headline","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-01-content-4","type":"text","name":"Content","position":{"x":80,"y":950},"size":{"width":920,"height":288},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-01-footer-5","type":"cta","name":"Footer","position":{"x":80,"y":1311},"size":{"width":920,"height":73},"style_overrides":[],"if_selected":false}]},{"id":"knowledge-card-02","label":"Knowledge Card 02","layers":[{"id":"knowledge-card-02-background-0","type":"background","name":"Background","position":{"x":0,"y":0},"size":{"width":1080,"height":1440},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-02-brand-1","type":"brand","name":"Brand","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-02-image-2","type":"image","name":"Illustration","position":{"x":80,"y":288},"size":{"width":920,"height":605},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-02-headline-3","type":"text","name":"Headline","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-02-content-4","type":"text","name":"Content","position":{"x":80,"y":950},"size":{"width":920,"height":288},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-02-footer-5","type":"cta","name":"Footer","position":{"x":80,"y":1311},"size":{"width":920,"height":73},"style_overrides":[],"if_selected":false}]},{"id":"knowledge-card-03","label":"Knowledge Card 03","layers":[{"id":"knowledge-card-03-background-0","type":"background","name":"Background","position":{"x":0,"y":0},"size":{"width":1080,"height":1440},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-03-brand-1","type":"brand","name":"Brand","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-03-image-2","type":"image","name":"Illustration","position":{"x":80,"y":288},"size":{"width":920,"height":605},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-03-headline-3","type":"text","name":"Headline","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-03-content-4","type":"text","name":"Content","position":{"x":80,"y":950},"size":{"width":920,"height":288},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-03-footer-5","type":"cta","name":"Footer","position":{"x":80,"y":1311},"size":{"width":920,"height":73},"style_overrides":[],"if_selected":false}]},{"id":"knowledge-card-04","label":"Knowledge Card 04","layers":[{"id":"knowledge-card-04-background-0","type":"background","name":"Background","position":{"x":0,"y":0},"size":{"width":1080,"height":1440},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-04-brand-1","type":"brand","name":"Brand","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-04-image-2","type":"image","name":"Illustration","position":{"x":80,"y":288},"size":{"width":920,"height":605},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-04-headline-3","type":"text","name":"Headline","position":{"x":80,"y":86},"size":{"width":920,"height":130},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-04-content-4","type":"text","name":"Content","position":{"x":80,"y":950},"size":{"width":920,"height":288},"style_overrides":[],"if_selected":false},{"id":"knowledge-card-04-footer-5","type":"cta","name":"Footer","position":{"x":80,"y":1311},"size":{"width":920,"height":73},"style_overrides":[],"if_selected":false}]}]}  
  }
}'
```


### Request Parameters

| Field         | Required | Description                                                                                                                             |
|---------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------|
| prompt        | Required | Text, User Input Design Goal, e.g. `Genreate a movie character description of Movie Odyssey`                                            |
| images        | Required | List of Reference Images that user uploads                                                                                              |
| onekey        | Required | DeepNLP Router OneKey Program                                                                                                           |
| api_id        | Required | use `social_media_posts` to represent Social Media Posts Generator                                                                      | 
| template_id   | Required | use `knowledge-card` as default                                                                                                         |
| channel_profile | Required | The distribution channel of Social Media Cards. Supported Values include:  `general`, `xiaohongshu`,`x-twitter`,`instagram`             |
| audience_profile | Required | The Audience of Social Media Cards. Supported Values include:  `general`, `curiosity`                                                   |
| card_count    | Required | int, e.g. 4 cards of instagram/twitter/xiaohongshu                                                                                      | 
| asset_size    | Required | List of Asset Size Available, default to templates, such as List of width,height,ratio, {"width": 1080, "height": 1080, "ratio": "1:1"} |
| mode          | Optional | The design complexity, basic,standard,advanced                                                                                          |
| styles        | Optional | List, List of Styles Prompt, e.g. deep monochromatic tones,techonology styles                                                           |
| design_config | Optional | Dict, Detailed Layers of Text, Prompt, Images on the Slides                                                                             |

#### channel_profile Support Values

The distribution channel of Social Media Cards. 

| Support Value | Description                                                                  |
|---------------|------------------------------------------------------------------------------|
| general       | General Distribution Channels                                                |
| instagram     | Instagram                                                                    |
| xiaohongshu   | Xiaohongshu RedNote to Distribute the generated social media knowledge cards |
| x-twitter     | X-Twitter Knowledge Cards                                                    |

#### audience_profile Support Values

| Support Value | Description                     |
|---------------|---------------------------------|
| general       | General audience Type           |
| curiosity     | The curiosity Audience Group... |


### API Expected Outputs

### Results Parameters

| Field      | Description                                                                                                                        |
|------------|------------------------------------------------------------------------------------------------------------------------------------|
| session_id | The unique id of AI Generated Images/Slides/Carousels                                                                              |
| title      | The title of the genreate Slides                                                                                                   |
| share_url | The workspace of this generate slides, you can open workspace an edit the generated text,color,size and export the final images... |
| card_count                              | The Int value of Card Counts of Generated 4 Pages of Instagram/Twitter/Xiaohongshu Slides                                          |
| images                                  | List of url, The List of Main Generated Images from AI Image Generator, Each Card Have one image                                   |
| data                                    | The text/references images displayed as layers on the main images.                                                                 |
| data.sequence_pages                     | List of Design Generated Layers config: The text,headline,content                                                                  |
| data.sequence_pages[i]                  | Dict of Pages Data                                                                                                                 |
| data.sequence_pages[i].id               | The ID of the generated Pages                                                                                                      |
| data.sequence_pages[i].label              | The Label of the generated Pages                                                                                                   |
| data.sequence_pages[i].geometry           | The geometry of the generated Page, following the formats of "widthxheight"                                                        |
| data.sequence_pages[i].canvas_width       | The width of the generated Page, e.g. 1080                                                                                         |
| data.sequence_pages[i].canvas_height      | The height of the generated Page, e.g. 1350                                                                                        |
| data.sequence_pages[i].layers             | Layers config: List of Layers Data, text,headline,content displayed                                                                |
| data.sequence_pages[i].layers[j].id       | Int, Card ID                                                                                                                       |
| data.sequence_pages[i].layers[j].type     | String, Supported Type: background,text,image,headline                                                                             |
| data.sequence_pages[i].layers[j].position | Dict of {"x": 0,"y": 0}, position of the text layer display on the main canvas                                                     |
| data.sequence_pages[i].layers[j].position | Dict of x,y position of the text layer display on the main canvas                                                                  |

Note: To Export the Final Multi Slides Images, You can visit the share_url workspace and export the images to .pdf,.png,.ppt formats.

`share_url`: https://craftsman-agent.aiagenta2z.com/app/sessions/share/547083a4-5e38-4e4e-ba78-300cadb88b11

It will show a board of card count, e.g. 4 pages of ready to use knowledge cards of social media posts!


```json

{
  "success": true,
  "partial_success": false,
  "failed_card_indexes": [],
  "summary": "Movie Odyssey Character Guide",
  "final_image_url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/fd946e2a-0d88-425f-952a-0bd42c3dbf79.png",
  "images": [
    {
      "url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/fd946e2a-0d88-425f-952a-0bd42c3dbf79.png"
    },
    {
      "url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/c689495c-bf70-470f-baf9-b2866daee12c.png"
    },
    {
      "url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/e659b1b1-23b9-4339-a554-a124dd0586ff.png"
    },
    {
      "url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/459ec8ab-78ca-487b-a6ed-bd82a5f35d9f.png"
    }
  ],
  "channel_profile": "generic",
  "audience_profile": "general",
  "age_band": "auto",
  "profile_version": "1.0.0",
  "geometry": "1080x1350",
  "geometry_source": "profile",
  "resolved_profiles": [
    {
      "type": "channel",
      "id": "generic",
      "version": "1.0.0"
    },
    {
      "type": "audience",
      "id": "general",
      "version": "1.0.0"
    }
  ],
  "data": {
    "schema_version": "knowledge-card.v1",
    "style_profile": {
      "channel": {
        "id": "generic",
        "version": "1.0.0"
      },
      "audience": {
        "id": "general",
        "version": "1.0.0"
      },
      "age_band": "auto",
      "profile_version": "1.0.0"
    },
    "geometry": "1080x1350",
    "geometry_source": "profile",
    "sequence_pages": [{"id":"card-01","label":"Overview","geometry":"1080x1350","canvas_width":1080,"canvas_height":1350,"generation":{"status":"success","attempts":1,"image_prompt":"clean editorial illustration. cohesive editorial illustration with generous negative space, stylized cinematic motifs, no text, no letters, no typography, no watermark. Palette: #F7F3EA, #172033, #6D5DFB. stylized vintage compass resting on an open leather journal, warm cream background, clean editorial illustration style, generous negative space at top, no text, no letters, no typography, no watermark. No text, no letters, no typography, no watermark. Reserve clean negative space for editable title and body layers. Compose specifically for a 3:2 frame and keep every focal subject fully inside a centered safe area."},"content_blocks":[{"label":"Core Concept","content":"Characters serve as emotional anchors, translating\nabstract themes into relatable human experiences for\nthe audience."}],"layers":[{"id":"card-01-bg","type":"background","name":"Background","value":"#F7F3EA","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"if_selected":false},{"id":"card-01-brand","type":"brand","name":"Brand","value":"Movie Odyssey","position":{"x":80,"y":47},"size":{"width":920,"height":61},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"20px","font_weight":"600"},{"id":"card-01-headline","type":"text","name":"Headline","value":"Meet the Travelers","position":{"x":80,"y":115},"size":{"width":920,"height":162},"if_selected":false,"color":"#172033","font":"Playfair Display","font_size":"48px","font_weight":"700"},{"id":"card-01-image","type":"image","name":"Illustration","value":"https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/fd946e2a-0d88-425f-952a-0bd42c3dbf79.png","position":{"x":80,"y":310},"size":{"width":920,"height":567},"color":"#000000","image_fit":"contain","if_selected":false},{"id":"card-01-content-block-01","type":"text","name":"Content Block 01","value":"Core Concept\nCharacters serve as emotional anchors, translating\nabstract themes into relatable human experiences for\nthe audience.","position":{"x":80,"y":918},"size":{"width":920,"height":304},"if_selected":false,"color":"#172033","font":"Inter","font_size":"24px","font_weight":"400","line_height":1.2},{"id":"card-01-footer","type":"cta","name":"Footer","value":"01 / 04 Introduction","position":{"x":80,"y":1249},"size":{"width":920,"height":54},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"16px","font_weight":"500"}]},{"id":"card-02","label":"The Protagonist","geometry":"1080x1350","canvas_width":1080,"canvas_height":1350,"generation":{"status":"success","attempts":1,"image_prompt":"clean editorial illustration. cohesive editorial illustration with generous negative space, stylized cinematic motifs, no text, no letters, no typography, no watermark. Palette: #F7F3EA, #172033, #6D5DFB. abstract silhouette of a person stepping forward through a glowing doorway, deep navy blue and purple tones, minimalist editorial art, ample negative space on right side, no text, no letters, no typography, no watermark. No text, no letters, no typography, no watermark. Reserve clean negative space for editable title and body layers. Compose specifically for a 3:2 frame and keep every focal subject fully inside a centered safe area."},"content_blocks":[{"label":"Key Trait","content":"Active agency distinguishes\nprotagonists from passive\nobservers; they make\nchoices that trigger\nconsequences."},{"label":"Narrative Function","content":"They embody the central\ndramatic question, forcing\nthe audience to invest in\nthe outcome of their\njourney."}],"layers":[{"id":"card-02-bg","type":"background","name":"Background","value":"#F7F3EA","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"if_selected":false},{"id":"card-02-brand","type":"brand","name":"Brand","value":"Movie Odyssey","position":{"x":80,"y":47},"size":{"width":920,"height":61},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"20px","font_weight":"600"},{"id":"card-02-headline","type":"text","name":"Headline","value":"The Driving Force","position":{"x":80,"y":115},"size":{"width":920,"height":162},"if_selected":false,"color":"#172033","font":"Playfair Display","font_size":"48px","font_weight":"700"},{"id":"card-02-image","type":"image","name":"Illustration","value":"https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/c689495c-bf70-470f-baf9-b2866daee12c.png","position":{"x":80,"y":310},"size":{"width":920,"height":567},"color":"#000000","image_fit":"contain","if_selected":false},{"id":"card-02-content-block-01","type":"text","name":"Content Block 01","value":"Key Trait\nActive agency distinguishes\nprotagonists from passive\nobservers; they make\nchoices that trigger\nconsequences.","position":{"x":80,"y":918},"size":{"width":447,"height":304},"if_selected":false,"color":"#172033","font":"Inter","font_size":"24px","font_weight":"400","line_height":1.2},{"id":"card-02-content-block-02","type":"text","name":"Content Block 02","value":"Narrative Function\nThey embody the central\ndramatic question, forcing\nthe audience to invest in\nthe outcome of their\njourney.","position":{"x":554,"y":918},"size":{"width":447,"height":304},"if_selected":false,"color":"#172033","font":"Inter","font_size":"24px","font_weight":"400","line_height":1.2},{"id":"card-02-footer","type":"cta","name":"Footer","value":"02 / 04 Primary Role","position":{"x":80,"y":1249},"size":{"width":920,"height":54},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"16px","font_weight":"500"}]},{"id":"card-03","label":"The Antagonist","geometry":"1080x1350","canvas_width":1080,"canvas_height":1350,"generation":{"status":"success","attempts":1,"image_prompt":"clean editorial illustration. cohesive editorial illustration with generous negative space, stylized cinematic motifs, no text, no letters, no typography, no watermark. Palette: #F7F3EA, #172033, #6D5DFB. geometric mountain peak casting a long sharp shadow across a textured paper surface, muted purple accent lighting, clean vector style composition, negative space at bottom, no text, no letters, no typography, no watermark. No text, no letters, no typography, no watermark. Reserve clean negative space for editable title and body layers. Compose specifically for a 3:2 frame and keep every focal subject fully inside a centered safe area."},"content_blocks":[{"label":"Structural Purpose","content":"Conflict generates drama; without opposition, there is\nno transformation or meaningful resolution."}],"layers":[{"id":"card-03-bg","type":"background","name":"Background","value":"#F7F3EA","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"if_selected":false},{"id":"card-03-brand","type":"brand","name":"Brand","value":"Movie Odyssey","position":{"x":80,"y":47},"size":{"width":920,"height":61},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"20px","font_weight":"600"},{"id":"card-03-headline","type":"text","name":"Headline","value":"The Necessary Shadow","position":{"x":80,"y":115},"size":{"width":920,"height":162},"if_selected":false,"color":"#172033","font":"Playfair Display","font_size":"48px","font_weight":"700"},{"id":"card-03-image","type":"image","name":"Illustration","value":"https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/e659b1b1-23b9-4339-a554-a124dd0586ff.png","position":{"x":80,"y":310},"size":{"width":920,"height":567},"color":"#000000","image_fit":"contain","if_selected":false},{"id":"card-03-content-block-01","type":"text","name":"Content Block 01","value":"Structural Purpose\nConflict generates drama; without opposition, there is\nno transformation or meaningful resolution.","position":{"x":80,"y":918},"size":{"width":920,"height":304},"if_selected":false,"color":"#172033","font":"Inter","font_size":"24px","font_weight":"400","line_height":1.2},{"id":"card-03-footer","type":"cta","name":"Footer","value":"03 / 04 Counter Force","position":{"x":80,"y":1249},"size":{"width":920,"height":54},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"16px","font_weight":"500"}]},{"id":"card-04","label":"Supporting Cast","geometry":"1080x1350","canvas_width":1080,"canvas_height":1350,"generation":{"status":"success","attempts":1,"image_prompt":"clean editorial illustration. cohesive editorial illustration with generous negative space, stylized cinematic motifs, no text, no letters, no typography, no watermark. Palette: #F7F3EA, #172033, #6D5DFB. three interconnected circles forming a subtle constellation pattern against a soft cream backdrop, elegant line art style, balanced composition with top negative space, no text, no letters, no typography, no watermark. No text, no letters, no typography, no watermark. Reserve clean negative space for editable title and body layers. Compose specifically for a 3:2 frame and keep every focal subject fully inside a centered safe area."},"content_blocks":[{"label":"The Foil","content":"A character whose\ncontrasting traits\nhighlight specific\nqualities in the\nprotagonist through\ncomparison."},{"label":"World Building","content":"Secondary roles establish\nthe social rules, tone, and\natmosphere of the story's\nunique universe."}],"layers":[{"id":"card-04-bg","type":"background","name":"Background","value":"#F7F3EA","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"if_selected":false},{"id":"card-04-brand","type":"brand","name":"Brand","value":"Movie Odyssey","position":{"x":80,"y":47},"size":{"width":920,"height":61},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"20px","font_weight":"600"},{"id":"card-04-headline","type":"text","name":"Headline","value":"Catalysts and Mirrors","position":{"x":80,"y":115},"size":{"width":920,"height":162},"if_selected":false,"color":"#172033","font":"Playfair Display","font_size":"48px","font_weight":"700"},{"id":"card-04-image","type":"image","name":"Illustration","value":"https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/459ec8ab-78ca-487b-a6ed-bd82a5f35d9f.png","position":{"x":80,"y":310},"size":{"width":920,"height":567},"color":"#000000","image_fit":"contain","if_selected":false},{"id":"card-04-content-block-01","type":"text","name":"Content Block 01","value":"The Foil\nA character whose\ncontrasting traits\nhighlight specific\nqualities in the\nprotagonist through\ncomparison.","position":{"x":80,"y":918},"size":{"width":447,"height":304},"if_selected":false,"color":"#172033","font":"Inter","font_size":"24px","font_weight":"400","line_height":1.2},{"id":"card-04-content-block-02","type":"text","name":"Content Block 02","value":"World Building\nSecondary roles establish\nthe social rules, tone, and\natmosphere of the story's\nunique universe.","position":{"x":554,"y":918},"size":{"width":447,"height":304},"if_selected":false,"color":"#172033","font":"Inter","font_size":"24px","font_weight":"400","line_height":1.2},{"id":"card-04-footer","type":"cta","name":"Footer","value":"04 / 04 Ensemble Dynamics","position":{"x":80,"y":1249},"size":{"width":920,"height":54},"if_selected":false,"color":"#6D5DFB","font":"Inter","font_size":"16px","font_weight":"500"}]}],
    "card_count": 4
  },
  "card_count": 4,
  "card_count_source": "default",
  "session_id": "f3b48c2d-28fa-4f57-96c9-5228346b2063",
  "title": "Movie Odyssey Character Introduction",
  "workspace_session_id": "",
  "tag_list": "",
  "description": "",
  "share_url": "http://0.0.0.0:8011/app/sessions/share/f3b48c2d-28fa-4f57-96c9-5228346b2063?pwd=267e"
}

```

### Example Input Design Config for Social Media Posts 

key: design_config
value: 

```json
{
      "template_id": "knowledge-card",
      "card_count": 1,
      "card_count_source": "default",
      "channel_profile": "generic",
      "audience_profile": "general",
      "age_band": "auto",
      "profile_version": "1.0.0",
      "geometry_source": "profile",
      "resolved_profiles": [{
        "type": "channel",
        "id": "generic",
        "version": "1.0.0"
      }, {
        "type": "audience",
        "id": "general",
        "version": "1.0.0"
      }],
      "language": "auto",
      "mode": "standard",
      "text_model": "default",
      "image_model": "default",
      "styles": ["Editorial grid layout with corporate dark deep monochromatic tones"],
      "constraints": ["Limit target output build to 6 high-density pages max for physical double folding print"],
      "brief_inputs": [{
        "id": "binp-1",
        "type": "prompt",
        "content": "Introduction to Difference between MCPs,Skills and Agents CLIs"
      }, {
        "id": "binp-2",
        "type": "style",
        "content": "Editorial grid layout with corporate dark deep monochromatic tones"
      }, {
        "id": "binp-3",
        "type": "constraint",
        "content": "Limit target output build to high-density pages max for physical double folding print"
      }, {
        "id": "binp-1786857754660",
        "type": "prompt",
        "content": "Custom newly configured prompt parameter specifications instructions layout metric..."
      }],
      "text_styles": {
        "brand": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "20px",
          "font_weight": "600",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        },
        "headline": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "18px",
          "font_weight": "400",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        },
        "content": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "16px",
          "font_weight": "400",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        },
        "footer": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "16px",
          "font_weight": "400",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        }
      },
      "page_templates": [{
        "id": "image-generator-01",
        "label": "Cover Page",
        "layers": [{
          "id": "l-bg",
          "type": "background",
          "name": "Backdrop",
          "position": {
            "x": 0,
            "y": 0
          },
          "size": {
            "width": 1080,
            "height": 1350
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-brand",
          "type": "brand",
          "name": "Your Brand",
          "position": {
            "x": 40,
            "y": 40
          },
          "size": {
            "width": 200,
            "height": 40
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-img",
          "type": "image",
          "name": "Graphic URL",
          "position": {
            "x": 150,
            "y": 180
          },
          "size": {
            "width": 780,
            "height": 700
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-headline",
          "type": "text",
          "name": "Headline",
          "position": {
            "x": 40,
            "y": 850
          },
          "size": {
            "width": 400,
            "height": 80
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-content",
          "type": "text",
          "name": "Content",
          "position": {
            "x": 40,
            "y": 950
          },
          "size": {
            "width": 400,
            "height": 80
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-cta",
          "type": "cta",
          "name": "Footer",
          "position": {
            "x": 0,
            "y": 1150
          },
          "size": {
            "width": 1080,
            "height": 50
          },
          "style_overrides": [],
          "if_selected": false
        }]
      }]
    }
```

## 2. CLIs Usage

```bash

export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
npx onekey agent craftsman-agent/craftsman-agent social_media_posts '{"prompt":"Movie Odyssey Main Characters Introduction,"images":[],"card_count":1,"template_id":"knowledge-card","api_id":"image_generator","asset_size":[{"width":1080,"height":1080,"ratio":"1:1"}],"mode":"basic","session_id":"31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb","session_name":"AI Poster of MCPs/CLIs/Agents","tag_list":"","model":"default","styles":["Editorial grid layout with corporate dark deep monochromatic tones"],"design_config":{"template_id":"knowledge-card","card_count":1,"card_count_source":"default","channel_profile":"generic","audience_profile":"general","age_band":"auto","profile_version":"1.0.0","geometry_source":"profile","resolved_profiles":[{"type":"channel","id":"generic","version":"1.0.0"},{"type":"audience","id":"general","version":"1.0.0"}],"language":"auto","mode":"standard","text_model":"default","image_model":"default","styles":["Editorial grid layout with corporate dark deep monochromatic tones"],"constraints":["Limit target output build to 6 high-density pages max for physical double folding print"],"brief_inputs":[{"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"},{"id":"binp-2","type":"style","content":"Editorial grid layout with corporate dark deep monochromatic tones"},{"id":"binp-3","type":"constraint","content":"Limit target output build to 6 high-density pages max for physical double folding print"},{"id":"binp-1786857754660","type":"prompt","content":"Custom newly configured prompt parameter specifications instructions layout metric..."}],"text_styles":{"brand":{"color":"#8b5cf6","font":"Playfair Display","font_size":"20px","font_weight":"600","text_align":"left","line_height":1.3,"letter_spacing":0},"headline":{"color":"#8b5cf6","font":"Playfair Display","font_size":"18px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"content":{"color":"#8b5cf6","font":"Playfair Display","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"footer":{"color":"#8b5cf6","font":"Playfair Display","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0}},"page_templates":[{"id":"image-generator-01","label":"Cover Page","layers":[{"id":"l-bg","type":"background","name":"Backdrop","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"style_overrides":[],"if_selected":false},{"id":"l-brand","type":"brand","name":"Your Brand","position":{"x":40,"y":40},"size":{"width":200,"height":40},"style_overrides":[],"if_selected":false},{"id":"l-img","type":"image","name":"Graphic URL","position":{"x":150,"y":180},"size":{"width":780,"height":700},"style_overrides":[],"if_selected":false},{"id":"l-headline","type":"text","name":"Headline","position":{"x":40,"y":850},"size":{"width":400,"height":80},"style_overrides":[],"if_selected":false},{"id":"l-content","type":"text","name":"Content","position":{"x":40,"y":950},"size":{"width":400,"height":80},"style_overrides":[],"if_selected":false},{"id":"l-cta","type":"cta","name":"Footer","position":{"x":0,"y":1150},"size":{"width":1080,"height":50},"style_overrides":[],"if_selected":false}]}]}}'

```

