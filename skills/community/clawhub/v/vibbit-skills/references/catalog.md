# Module catalog

Read this to locate a module or explain capability boundaries. A listed module does not imply every platform feature is publicly available.

## Creative methods

Use creative methods when content needs design. Direct generation, processing, resource queries, and task recovery use their own capabilities. Records are local conventions, not platform APIs.

- [Creative direction](creation/creative-direction.md)
- [Understanding a reference for adaptation](creation/reference-analysis.md)
- [Script and semantic timing](creation/script-and-timing.md)
- [Creative handoff and revisions](contracts/creative-handoff.md)
- [Project definition, execution intent, and selected artifacts](contracts/production-plan.md)
- [Private script, talent, scene, and batch records](contracts/creative-library.md)
- [Mixcut templates and audio/picture plans](contracts/semantic-mixcut.md)
- [Render artifacts and cloud handoff](contracts/render-artifact.md)
- [User-owned render template contract](contracts/render-template.md)

## Platform methods

Only Meta methods are bundled. TikTok search is a resource query, not a TikTok creative-method package.

- [Platform methods](platforms/index.md)
- [Meta advertising methods](platforms/meta/index.md)

## Workflows

Enter at the current missing step; do not repeat all stages. Workflows are host orchestration, not new server commands.

- [Agent semantic mixcut: reference analysis, templates, selection, and cloud assembly](workflows/semantic-mixcut.md)
- [Batch production](workflows/batch-production.md)
- [Creative library and reuse](workflows/creative-library.md)
- [B-roll and overlays](workflows/broll-production.md)
- [Local video production and Vibbit cloud composition](workflows/hybrid-video.md)
- [Desktop handoff for a Jianying draft](workflows/jianying-draft.md): blocked export without a Job ID, official installation guidance, and task launch only with a real ID
- [1:1 visual remake](workflows/one-to-one-remake.md)
- [Creator-led and digital human talking-head videos](workflows/oral-broadcast.md)
- [Product research and strategy](workflows/product-research.md)
- [Product marketing images](workflows/product-marketing-image.md)
- [Product marketing videos](workflows/product-video.md)
- [Reference adaptation](workflows/reference-remake.md)
- [Short drama](workflows/short-drama.md)
- [Novel-to-comic adaptation](workflows/novel-comic.md)
- [Storyboard to video](workflows/storyboard-video.md)
- [Video localization](workflows/video-localization.md)
- [Audio content, caption files, and speech checks](workflows/audio-content.md)

## Capabilities

Each capability documents its actual public contract and unavailable operations. Review depends on the host’s real media tools.

- [Content URL parsing](capabilities/analysis/content-url-parsing.md)
- [Music recognition](capabilities/analysis/music-recognition.md)
- [Speech transcription](capabilities/analysis/speech-transcription.md)
- [Video breakdown](capabilities/analysis/video-breakdown.md)
- [Video review and focused revisions](capabilities/analysis/video-review.md)
- [Audio generation](capabilities/generation/audio-generation.md)
- [Reusable digital human creation](capabilities/generation/digital-human-creation.md)
- [Digital human video](capabilities/generation/digital-human-video.md)
- [Image generation](capabilities/generation/image-generation.md)
- [Programmatic video](capabilities/generation/programmatic-video.md)
- [Video generation](capabilities/generation/video-generation.md)
- [Filler-word removal](capabilities/processing/filler-word-removal.md)
- [Local media composition](capabilities/processing/local-composition.md)
- [Cloud media composition](capabilities/processing/media-composition.md)
- [Adding Vibbit subtitles](capabilities/processing/subtitles-and-packaging.md#subtitle-addition)
- [Subtitle removal](capabilities/processing/subtitles-and-packaging.md#subtitle-removal)
- [Video packaging](capabilities/processing/subtitles-and-packaging.md#video-packaging)
- [Video editing and extension](capabilities/processing/video-editing.md#video-segment-edit)
- [Video slicing](capabilities/processing/video-editing.md#video-slicing)
- [Video translation](capabilities/processing/video-translation.md)
- [Video upscaling](capabilities/processing/video-upscale.md)

## Resources

Use only real returned IDs and supported lookup/save operations.

- [Brands](resources/brands.md)
- [Digital humans](resources/digital-humans.md)
- [Materials](resources/materials.md)
- [Packaging templates](resources/packaging-templates.md)
- [Product library management and creative inputs](resources/products.md)
- [Projects](resources/project-work-tasks.md#projects)
- [Local render templates](resources/render-templates.md)
- [Subtitle templates (dynamic templates unavailable)](resources/subtitle-templates.md)
- [Tasks](resources/project-work-tasks.md#tasks)
- [Reference structures](resources/viral-structures.md)
- [Voices](resources/voices.md)
- [Existing works](resources/project-work-tasks.md#works)
- [External reviews](resources/external-research.md#reviews)
- [Supplier discovery](resources/external-research.md#suppliers)
- [External video references](resources/external-research.md#videos)
- [Visual matches](resources/external-research.md#visual-matches)

## Rendering engines

Official engine skills are separate dependencies. Select one engine and actual project; engines are not cloud task types.

- [Render engine selection](engines/index.md#engine-selection)
- [Remotion](engines/index.md#remotion)
- [Hyperframes](engines/index.md#hyperframes)

## Runtime

Authentication, media, task recovery, local planning/rendering, limits, and troubleshooting.

- [Vibbit API client](runtime/api-client.md)
- [External source data, candidate selection, and execution scope](runtime/external-content.md)
- [Authentication and environment](runtime/authentication.md)
- [Capabilities and execution conditions](runtime/capability-discovery.md)
- [External rendering dependencies](runtime/external-render-dependencies.md)
- [Limits, credits, and batches](runtime/limits-and-credits.md)
- [Local production planning and reuse](runtime/local-production.md)
- [Local rendering](runtime/local-rendering.md)
- [Media inputs, upload, and reuse](runtime/media-inputs.md)
- [Image previews](runtime/media-preview.md)
- [Task lifecycle and recovery](runtime/task-lifecycle.md)
- [Troubleshooting](runtime/troubleshooting.md)

## Models

Read the chosen model’s relevant guide; full fields and limits remain in API contracts.

- [GPT Image](models/gpt-image.md)
- [Model guides](models/index.md)
- [Seedance 2.0](models/seedance-2.0.md)
- [Editing and extension](models/seedance-2.5.md#editing-and-extension)
- [Frames and storyboards](models/seedance-2.5.md#frames-and-storyboards)
- [Seedance 2.5](models/seedance-2.5.md#overview)
- [Prompting Seedance 2.5](models/seedance-2.5.md#prompting)
- [Reference generation](models/seedance-2.5.md#reference-generation)

## API contracts

Public commands, exact field names, examples, and execution boundaries.

- [Product library list: list_products](api/products.md#list-products)
- [Product detail: get_product](api/products.md#get-product)
- [Parse product links: parse_products](api/products.md#parse-products)
- [Create a product: create_product](api/products.md#create-product)
- [Save parsed products: batch_create_products](api/products.md#batch-create-products)
- [Update a product: update_product](api/products.md#update-product)
- [Delete a product: delete_product](api/products.md#delete-product)

- [Amazon reviews: amazon_reviews](api/reviews.md#amazon-reviews)
- [Video breakdown: breakdown](api/breakdown.md)
- [Media composition: compose](api/compose.md)
- [Approve the current storyboard: confirm_translation](api/translation-review.md#confirm-translation)
- [Digital-human video: digital_human_video](api/digital_human_video.md)
- [Image generation: gen_image](api/gen_image.md)
- [Audio generation: generate_audio](api/generate_audio.md)
- [Digital-human listing: list_digital_humans](api/list_digital_humans.md)
- [Packaging templates: list_templates](api/templates.md#list-templates)
- [Share-link parsing: parse_url](api/parse_url.md)
- [Reddit discussions: reddit_reviews](api/reviews.md#reddit-reviews)
- [Subtitle removal: remove_subtitles](api/remove_subtitles.md)
- [1688 supplier search: search_suppliers](api/search_suppliers.md)
- [TikTok video search: search_tiktok](api/video-search.md#search-tiktok)
- [Google short-video search: search_videos](api/video-search.md#search-videos)
- [Seedance video: seedance](api/seedance.md)
- [Audio transcription: transcribe_audio](api/transcribe_audio.md)
- [Video translation: translate_video](api/translate_video.md)
- [Save translated text: update_translation](api/translation-review.md#update-translation)
- [Media upload: upload_info](api/upload_info.md)
- [Visual product matches: visual_matches](api/visual_matches.md)

- [Translation speaker voices, segment retries and language renders](api/translation-revision.md)
- [Existing packaging template details: get_template](api/templates.md#get-template)

- [Material listing, batch lookup, detail and search](api/material-queries.md): list_materials / batch_get_materials / get_material / search_materials
