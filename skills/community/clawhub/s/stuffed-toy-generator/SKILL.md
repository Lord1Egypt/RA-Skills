---
name: "stuffed-toy-generator"
description: "AI Stuffed Toy Generator Generated Toy Multi View Sheets and 3D Models Generator using SOTA 3D APIs such as Tripo/Meshy/etc served on OneKey Agent Gateway by Craftsman Agent, useful for AI Figurine, Stuffed Toy, 3D Printing, Game Asset and Architecture Toy Generation"
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: Onekey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# AI Stuffed Toy generator designer skills from craftsman-agent

The Workflow of typical Toy Model Generation is shown as below. These Toy Generation APIs are served through the OneKey Agent Gateway and used by the Craftsman Agent Toy Designer website console.

The typical workflow is:

```commandline
[Text/Image Prompt]
        ->
[Toy Design Draft / Multi-View Sheet]
        ->
[Create 3D Generation Task: Task ID]
        ->
[Poll Task Results Progress using Task ID]
        ->
[3D Toy Model + Preview]

```

| API                        | Description                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| toy_generator_design_draft | Generate a toy design draft and multi-view reference sheets from text prompts and/or images |
| toy_generator_task_create  | Create a new Toy 3D Generation Task from images, prompts, and/or multi-view references      |
| toy_generator_task_poll    | Poll the progress and final results of a Toy 3D Generation Task                             |


#### Toy Generation Templates For Parameter `template_id`

| Template ID  | Template Name | Description                                                           |
| ------------ | ------------- | --------------------------------------------------------------------- |
| figurine     | Figurine      | AI Figurine Design with optional textures                             |
| stuffed-toy  | Stuffed Toy   | Stuffed Toy Template for plush texture and stuffed materials          |
| 3d-printing  | 3D Printing   | 3D Printed Toy Design Generation, outputs ready-to-use 3D model files |
| game-assets  | Game Assets   | Game Design Assets                                                    |
| architecture | Architecture  | Architecture Toy Design                                               |


#### Toy Generator Templates Models and Asset Sizes 

| template_id | asset_size | Description                                      |
| ----------- | ---------- | ------------------------------------------------ |
| Figurine    | small      | Small Collectible (5cm) - W:10mm, D:10mm, H:50mm |
| Figurine    | standard   | Standard Figure (10cm) - W:20mm, D:20mm, H:100mm |
| Figurine    | premium    | Premium Statue (30cm) - W:30mm, D:30mm, H:300mm  |


### OneKey Agent Gateway

The Toy Generator APIs are registered under:
unique_id: craftsman-agent/craftsman-agent
Gateway endpoint:
```commandline
https://agent.deepnlp.org/agent_router

```
Set the registered OneKey Gateway access key:

```
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

[//]: # (![3D Generated Images]&#40;https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png&#41;)
<img src="https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png" alt="Craftsman-agent Perler Beads for Minecraft Diamond Pickaxes" width="500" />

| Section                       | Description                                   |
|-------------------------------|-----------------------------------------------|
| Craftsman 3D Generator Online | https://craftsman-agent.aiagenta2z.com/app/3d-generator |
| Craftsman Website     | https://craftsman-agent.aiagenta2z.com           |
| Craftsman App         | https://craftsman-agent.aiagenta2z.com/app       |
| Craftsman Gallery     | https://craftsman-agent.aiagenta2z.com/gallery   |
| Craftsman Workspace   | https://craftsman-agent.aiagenta2z.com/workspace |
| Craftsman Marketplace | https://craftsman-agent.aiagenta2z.com/marketplace |


## Quick Start
Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://deepnlp.org/workspace/keys).

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

# 1. API: Toy Generator Design Draft

### 1.1 REST API Requests Usage
```
toy_generator_design_draft
```
Generate and design a multi-view toy reference sheet from text prompts and/or source images.

The design draft can be used as the input for the subsequent Toy 3D Model Generation Task.

#### Requests Input Parameter

| Parameter         | Description                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| prompt            | Text prompt describing the desired toy                                                          |
| images            | Array of source image URLs used as visual references                                            |
| asset_size        | Toy asset size, such as `small`, `standard`, or `premium`                                       |
| template_id       | Toy template such as `figurine`, `stuffed-toy`, `3d-printing`, `game-assets`, or `architecture` |
| provider_model_id | Toy design provider/model identifier; `default` is supported                                    |
| session_name      | Name of the generated workspace session                                                         |
| tag_list          | Optional tags associated with the generation                                                    |
| mode              | Generation mode such as `demo` or `basic`                                                       |


#### Input Parameter Options

**template_id**: The template of the toys to generate
**asset_size**: Default Asset Size Enumeration for selection, e.g. common settings for AI Figurine, 

| template_id | asset_size | Description                                      |
| ----------- | ---------- | ------------------------------------------------ |
| Figurine    | small      | Small Collectible (5cm) - W:10mm, D:10mm, H:50mm |
| Figurine    | standard   | Standard Figure (10cm) - W:20mm, D:20mm, H:100mm |
| Figurine    | premium    | Premium Statue (30cm) - W:30mm, D:30mm, H:300mm  |

**mode**: The mode as complexity of design for each generation task

| mode     | Description                                                                                                          |
|----------|----------------------------------------------------------------------------------------------------------------------|
| basic    | Basic Complexity for Design                                                                                          |
| standard | Standard Complexity for Design                                                                                       |
| advanced | Advanced Complexity for Design                                                                                       |
| demo     | Demo mode will only return predefined results for debug and APIs purpose, for production, please use other settings. |


#### Requests Input Example
```commandline
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
  -H "Content-Type: application/json" \
  -H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
  -d '{
    "unique_id": "craftsman-agent/craftsman-agent",
    "api_id": "toy_generator_design_draft",
    "data": {
      "prompt": "Stuffed Steve in Minecraft",
      "images": [
        "https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png"
      ],
      "asset_size": "small",
      "template_id": "stuffed-toy",
      "provider_model_id": "default",
      "session_name": "3D Build Plan",
      "tag_list": "",
      "mode": "demo"
    }
  }'
```

#### Output Keys Definition
| Key                  | Description                                   |
| -------------------- | --------------------------------------------- |
| success              | Whether the design draft generation succeeded |
| share_url            | The URL of workspace containing the canvas to view the design |
| blueprint            | Toy design blueprint data, when available     |
| reference_images     | Generated reference image URLs                |
| final_image_url      | URL of the generated multi-view design sheet  |
| overall_image        | Object containing individual generated views  |
| overall_image.front  | Front view image URL                          |
| overall_image.right  | Right view image URL                          |
| overall_image.back   | Back view image URL                           |
| session_id           | Workspace/session identifier                  |
| title                | Generated session title                       |
| workspace_session_id | Workspace session identifier                  |
| tag_list             | Tags associated with the generation           |

#### Output Example
```commandline
{
  "success": true,
  "share_url": "https://craftsman-agent.aiagenta2z.com/app/sessions/share/71b3a8b8-66b7-460d-ab80-998313a6a2f2?pwd=da5e",      
  "blueprint": {},
  "reference_images": [
    "/static/derekzz/1f752866-6757-49e8-ace3-58a0631592f9/2ae7b059979f412ea9b023c741efb3df.png",
    "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/e1ea5a81-cd69-4300-8aa5-b2cf682c5c2e.png"
  ],
  "final_image_url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png",
  "overall_image": {
    "front": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_front.png",
    "right": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_right.png",
    "back": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_back.png"
  },
  "session_id": "45860ee4-dd85-4562-8e51-27232dc9414e",
  "title": "3D Build Plan",
  "workspace_session_id": "",
  "tag_list": ""
}

```

**Note**:
`share_url`: After the Toy Design generation task finished, a `share_url` value contains URL of the canvas workspace will be returned.
This is the website to view the progress of the generation and the multiview sheets, the front view, side view, backview.
Please notify user the `share_url` link to view the Toy Design generation task status and results online!


### 1.2 CLI Usage

```shell
npx onekey agent craftsman-agent/craftsman-agent toy_generator_design_draft '{"prompt":"Stuffed Steve in Minecraft","images":["https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png"],"asset_size":"small","template_id":"stuffed-toy","provider_model_id":"default","session_name":"3D Build Plan","tag_list":"","mode":"demo"}'
```


# 2. API :Toy Generator 3D Model Task Create

API ID:
```
toy_generator_task_create
```
Create a new Toy 3D Model Generation Task from a text prompt, source images, and/or generated multi-view images.  The API supports toy-specific templates and 3D generation providers such as Tripo and Meshy.

### 2.1 REST API Requests Usage

#### Request Input Parameters

| Parameter         | Description                                                                                                                                 |
| ----------------- |---------------------------------------------------------------------------------------------------------------------------------------------|
| session_id        | Set Existing session_id the same as results from `toy_generator_design_draft` API in 1.1 section or Create a new separate session id (uuid) |
| prompt            | Text prompt describing the desired 3D toy                                                                                                   |
| images            | Array of source image URLs                                                                                                                  |
| multi_view        | Object containing multi-view image URLs. `front` is required when using multi-view generation; `left`, `right` and `back` can be supplied   |
| asset_size        | Target toy asset size, depending on the selected template                                                                                   |
| template_id       | Toy generation template                                                                                                                     |
| provider_model_id | 3D generation provider, such as `tripo/tripo` or `meshy/meshy`                                                                              |
| model             | Optional provider-specific model, such as `P1-20260311` or `v3.1-20260211`                                                                  |
| session_name      | Name of the generation session                                                                                                              |
| tag_list          | Optional tags                                                                                                                               |
| mode              | Generation mode such as `basic`, `standard`, `advanced`, or `demo`                                                                          |

**Note**: 
`session_id` of Toy Generation 3D Task API
a. If you are calling the API `toy_generator_task_create` generating toy 3D models from the outputs design craft images of first API `toy_generator_design_draft`, 
please set the input `session_id` of new API calling `toy_generator_task_create` the same as the outputs `session_id` of results of `toy_generator_design_draft`,
which combine the two APIs into the same session and workflow in the context.
b. Otherwise, if you are calling the `toy_generator_task_create` stand alone using other reference images, set the `session_id` as blank.


#### Request Example
```
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
  -H "Content-Type: application/json" \
  -H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
  -d '{
    "unique_id": "craftsman-agent/craftsman-agent",
    "api_id": "toy_generator_task_create",
    "data": {
      "prompt": "",
      "images": [
        "https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png"
      ],
      "multi_view": {
        "front": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_front.png",
        "left": "",        
        "right": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_right.png",
        "back": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_back.png"
      },
      "asset_size": "small",
      "template_id": "stuffed-toy",
      "provider_model_id": "tripo/tripo",
      "model": "P1-20260311",
      "session_name": "3D Build Plan",
      "tag_list": "",
      "mode": "basic"
    }
  }'
```

#### Output Keys Definition

| Key                  | Description                                             |
| -------------------- |---------------------------------------------------------|
| provider_model_id    | Selected 3D generation provider                         |
| task_id              | Unique ID of the created 3D generation task             |
| share_url            | The Private URL with keys to view your Toy Generator Task Models, Images on a Canvas, Available to track task progress and final results |
| session_id           | Generated workspace/session ID                          |
| title                | Generation session title                                |
| workspace_session_id | Workspace session ID                                    |
| tag_list             | Associated tags                                         |
| final_image_url      | Source/final image associated with the task             |
| status               | Initial task status,e.g. normally `running` `completed` |

#### Output example 
```
{
  "provider_model_id": "tripo/tripo",
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "session_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "title": "3D Build Plan",
  "workspace_session_id": "",
  "tag_list": "",
  "final_image_url": "https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png",
  "status": "running"
}
```

### 2.2 CLI Usage

```shell
npx onekey agent craftsman-agent/craftsman-agent toy_generator_task_create '{"prompt":"","images":["https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png"],"multi_view":{"front":"https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_front.png","right":"https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_right.png","back":"https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_back.png"},"asset_size":"small","template_id":"stuffed-toy","provider_model_id":"tripo/tripo","model":"P1-20260311","session_name":"3D Build Plan","tag_list":"","mode":"basic"}'
```

# 3. API : Toy Generator 3D Model Task Poll

API ID:
```commandline
toy_generator_task_poll
```

Poll the progress and results of a Toy 3D Model Generation Task created by toy_generator_task_create.
Continue polling with the returned task_id until the task reaches a terminal status such as success or failed.

#### Request Input Parameters

| Parameter                | Description                                         |
| ------------------------ | --------------------------------------------------- |
| task_id                  | The task ID returned by `toy_generator_task_create` |
| kwargs                   | Optional generation parameters used when polling    |
| kwargs.provider_model_id | Provider model ID, such as `tripo/tripo`            |
| kwargs.mode              | Generation mode such as `basic`                     |


#### Request Example

```commandline
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
  -H "Content-Type: application/json" \
  -H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
  -d '{
    "unique_id": "craftsman-agent/craftsman-agent",
    "api_id": "toy_generator_task_poll",
    "data": {
      "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
      "kwargs": {
        "provider_model_id": "tripo/tripo",
        "mode": "basic"
      }
    }
  }'
```

#### Output Keys Definition

| Key                    | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| task_id                | ID of the Toy 3D Generation Task                     |
| share_url            | The URL with Private keys to view your Toy Generator Task Models, Images on a Canvas, Available to track task progress and final results |
| status                 | Current task status, such as `running` or `success`  |
| progress               | Generation progress from 0-100                       |
| model                  | Generated 3D model information                       |
| model.url              | Downloadable URL of the generated 3D model           |
| model.type             | 3D model file type, such as `glb`                    |
| preview                | Rendered preview information                         |
| preview.url            | URL of the rendered preview                          |
| preview.type           | Preview image type, such as `webp`                   |
| metadata               | 3D model generation metadata                         |
| metadata.model_version | Provider model version                               |
| metadata.texture       | Whether textures were generated                      |
| metadata.pbr           | Whether PBR materials were generated                 |
| metadata.face_limit    | Face/polycount limit when available                  |
| metadata.export_uv     | Whether UV coordinates were exported                 |
| credits                | Credits consumed by the generation task              |
| raw_output             | Original provider generation response when available |
| session_id             | Workspace/session ID                                 |
| title                  | Generation title                                     |
| workspace_session_id   | Workspace session ID                                 |
| tag_list               | Associated tags                                      |

Running Output Example

```
{
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "status": "running",
  "progress": 81,
  "model": {
    "url": "",
    "type": ""
  },
  "preview": {
    "url": "",
    "type": ""
  },
  "metadata": {
    "model_version": "P1-20260311",
    "texture": true,
    "pbr": true,
    "face_limit": null,
    "export_uv": true
  },
  "credits": 50.0,
  "raw_output": {
    "code": 0,
    "status": "success",
    "data": {
      "type": "multiview_to_model",
      "status": "running",
      "progress": 81
    }
  },
  "session_id": "",
  "title": "",
  "workspace_session_id": "",
  "tag_list": ""
}
```


Finished Output Example

```commandline
{
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "status": "success",
  "progress": 100,
  "model": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb",
    "type": "glb"
  },
  "preview": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/legacy_mesh.webp",
    "type": "webp"
  },
  "metadata": {
    "model_version": "P1-20260311",
    "texture": true,
    "pbr": true,
    "face_limit": null,
    "export_uv": true
  },
  "credits": 50,
  "raw_output": {
    "code": 0,
    "status": "success",
    "data": {
      "type": "multiview_to_model",
      "status": "success",
      "progress": 100,
      "output": {
        "model_url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb",
        "rendered_image_url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af0da0c23ac/legacy_mesh.webp"
      },
      "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
      "credits_consumed": 50
    }
  },
  "session_id": "",
  "title": "",
  "workspace_session_id": "",
  "tag_list": ""
}
```

**Note**:
`share_url`: After the 3D model generation task are started, a `share_url` value contains URL of the canvas workspace will be returned.
This is the website to view the progress of the generation task as well as the final online 3D model preview of the model files (.glb,.obj,etc). 
Please notify user the `share_url` link to view the Toy 3D generation task status and results online!


#### 3.2 CLI Usage
```commandline
npx onekey agent craftsman-agent/craftsman-agent toy_generator_task_poll '{"task_id":"96b2116e-4b86-4d3c-af04-baf0da0c23ac","kwargs":{"provider_model_id":"tripo/tripo","mode":"basic"}}'
```

