'use strict'

const entry = (task_type, doc, mode, fields, required, example, extra = {}) => ({
  task_type, ...(doc ? { documentation_url: `https://vibbit.apifox.cn/${doc}` } : {}), mode,
  wire: 'object', status: 'documented', min_poll_ms: 5000,
  fields, required, example, ...extra,
})

const commands = {
  translate_video: entry('VIDEO_VOICE_OVER_TASK', '515706553e0', 'async', {
    business_id: 'id', task_name: 'string', source_language: 'string', target_language: 'string',
    translation_style: 'string', default_speed: 'number', auto_translate: 'boolean',
    subtitle_enabled: 'boolean', lip_sync_enabled: 'boolean', remove_subtitles_enabled: 'boolean',
    align_original_subtitle_position: 'boolean', translate_and_align_original_title: 'boolean',
    persona_mode: 'string', template_type: 'integer', template_configs: 'objects',
    default_digital_human_id: 'id', default_prompt: 'string', default_voice: 'nullable_object',
    settings: 'object', items: 'objects',
  }, ['items', 'auto_translate'], {
    auto_translate: true, target_language: 'en', items: [{ source_video: { url: 'https://example.com/source.mp4' } }],
  }, { wire: 'native_object', result_kind: 'translation',
    note: 'Set auto_translate explicitly. Only ordinary subtitles and template_type=0 packaging are currently supported; dynamic subtitle templates are temporarily unavailable. With auto_translate=false, query the returned task until task_result.result exposes the safe review details and phase before editing or confirming.' }),
  update_translation: entry('VIDEO_VOICE_OVER_TASK', '515712723e0', 'mutation', {
    sub_task_id: 'id', target_language: 'string', segments: 'objects', confirmed: 'boolean',
  }, ['sub_task_id', 'target_language', 'segments'], {
    sub_task_id: '2100065567327711232', target_language: 'en', segments: [{ from: 0, to: 2.4, translated_text: 'Hello.' }],
  }, { operation: 'update_translation', method: 'PUT', suffix: '/translation', result_kind: 'translation',
    note: 'Requires real review context. Saves text only and clears previous audio/render checkpoints; never approves review.' }),
  confirm_translation: entry('VIDEO_VOICE_OVER_TASK', '515938897e0', 'mutation', {
    sub_task_id: 'id',
  }, [], { sub_task_id: '2100065567327711232' }, {
    operation: 'confirm_translation', method: 'POST', suffix: '/storyboard/confirm', result_kind: 'translation',
    note: 'Requires actual reviewed storyboard context. Omitted sub_task_id confirms the whole batch; CLI requires --all-items explicitly.' }),
  update_speaker_voices: entry('VIDEO_VOICE_OVER_TASK', '515706553e0', 'mutation', {
    sub_task_id: 'id', speaker_voice_mappings: 'objects',
  }, ['sub_task_id', 'speaker_voice_mappings'], {
    sub_task_id: '2100065567327711232', speaker_voice_mappings: [{ speaker_id: 0, reference_audio_url: 'https://example.com/voice.mp3' }],
  }, { operation: 'update_speaker_voices', wire: 'translation_operation', result_kind: 'translation',
    note: 'Replaces ALL speaker bindings for this video; preserve every binding still needed. [] clears them. Saves configuration only, invalidates old previews across languages, and preserves delivered videos. Read current ASR speakers and mappings first.' }),
  retry_segments: entry('VIDEO_VOICE_OVER_TASK', '515706553e0', 'mutation', {
    sub_task_id: 'id', target_language: 'string', request_id: 'string', segments: 'objects',
  }, ['sub_task_id', 'target_language', 'request_id', 'segments'], {
    sub_task_id: '2100065567327711232', target_language: 'en', request_id: 'retry-example-001',
    segments: [{ id: 1, translated_text: 'Welcome.' }],
  }, { operation: 'retry_segments', wire: 'translation_operation', result_kind: 'translation',
    note: 'Generates preview speech for existing segment IDs in one language; short sentences may share an audio group. Does not render a video. Keep the same business request_id for recovery; changing it may charge again. Times, speakers and lip sync inherit the server draft.' }),
  resynthesize_language: entry('VIDEO_VOICE_OVER_TASK', '515706553e0', 'mutation', {
    sub_task_id: 'id', target_language: 'string', request_id: 'string', translated_segments_by_language: 'object',
  }, ['sub_task_id', 'target_language', 'request_id', 'translated_segments_by_language'], {
    sub_task_id: '2100065567327711232', target_language: 'en', request_id: 'render-example-001',
    translated_segments_by_language: { en: [{ id: 1, from: 0, to: 2.5, source_text: 'Hello', translated_text: 'Welcome.', speaker_id: 0, lip_sync: false }] },
  }, { operation: 'resynthesize_language', wire: 'translation_operation', result_kind: 'translation',
    note: 'Renders ONE language from its complete, already voiced server draft; never generates missing TTS. Preserve all segment IDs, times, speakers and text. Poll the matching request_id receipt, not the parent COMPLETED status. Old videos remain available on failure.' }),
  upload_reference_audio: entry('VIDEO_VOICE_OVER_TASK', '515706553e0', 'sync', {}, [], {}, {
    operation: 'upload_reference_audio', method: 'GET', suffix: '/reference-audio/upload-signature', result_kind: 'upload_instructions',
    note: 'Gets a task-scoped OSS signature; --file uploads a local .mp3 and returns its URL. Uploading does not bind a voice, generate speech or create a reusable voice asset. Never send the OpenAPI token to OSS.' }),
  seedance: entry('SEEDANCE_VIDEO_GENERATION', '514565013e0', 'async', {
    model: 'string', prompt: 'string', duration_seconds: 'integer', resolution: 'string',
    aspect_ratio: 'string', generate_audio: 'boolean', tools: 'objects',
    omni_reference_task_type: 'string', image_url: 'url', first_frame_image_url: 'url',
    last_frame_image_url: 'url', reference_image_urls: 'urls', reference_video_urls: 'urls',
    reference_audio_urls: 'urls',
  }, ['model', 'prompt', 'duration_seconds', 'resolution', 'aspect_ratio'], {
    model: 'doubao-seedance-2-5-260628', prompt: 'A paper boat crosses a misty lake at dawn as the camera gently follows.',
    duration_seconds: 5, resolution: '720p', aspect_ratio: '16:9',
  }, { validation: 'documented_fields_and_cross_field_rules', result_kind: 'video' }),
  remove_subtitles: entry('SUBTITLE_REMOVAL', '514584287e0', 'async',
    { video_url: 'url' }, ['video_url'], { video_url: 'https://example.com/source.mp4' },
    { result_kind: 'video', min_poll_ms: 10000,
      note: 'Subtitle removal may affect scene details. Compare the source and output for remaining text and damage. COMPLETED indicates task completion only.' }),
  parse_url: entry('PARSE_CONTENT_URL', '450679333e0', 'async',
    { url: 'url' }, ['url'], { url: 'https://example.com/shared-video' },
    { result_kind: 'analysis',
      note: 'input_info is an object; input_info.input is a JSON string. Do not automatically resubmit with another encoding.' }),
  breakdown: entry('VIDEO_BREAKDOWN', '452941686e0', 'async',
    { video_url: 'url', sub_tasks: 'strings' }, ['video_url', 'sub_tasks'],
    { video_url: 'https://example.com/source.mp4', sub_tasks: ['asr', 'hot'] },
    { result_kind: 'analysis',
      note: 'sub_tasks is an array of strings: asr, hot, transition, bgm. Select only the analyses needed.' }),
  transcribe_audio: entry('ASR', '522015345e0', 'async',
    { url: 'url' }, ['url'], { url: 'https://example.com/speech.mp3' },
    { result_kind: 'transcription',
      note: 'Transcribe an accessible audio URL and query the original task for full text, sentences, and words. Preserve raw timestamps and confirm their unit before conversion; completed transcription does not establish audio quality.' }),
  digital_human_video: entry('DIGITAL_HUMAN_VIDEO_GENERATION', '513300728e0', 'async',
    { audio_url: 'url', digital_human_id: 'id' }, ['audio_url', 'digital_human_id'],
    { audio_url: 'https://example.com/speech.mp3', digital_human_id: 'replace-with-real-id' },
    { result_kind: 'video', validation: 'example_fields_only' }),
  generate_audio: entry('AI_GENERATE_AUDIO', '513300730e0', 'async', {
    text_prompt: 'string', format: 'string', sample_rate: 'integer', speech_rate: 'integer',
    loudness_rate: 'integer', pitch_rate: 'integer', max_duration_seconds: 'integer',
    reference_audio_urls: 'urls', reference_material_ids: 'ids', reference_image_urls: 'urls',
  }, ['text_prompt'], { text_prompt: 'A natural English male voice says: "Welcome to the show." Soft background music supports the voice, with one light chime at the end. Add no other speech.', format: 'mp3', sample_rate: 48000 },
  { result_kind: 'audio', validation: 'documented_fields_and_ranges', note: 'Generate speech, BGM, sound effects or a combined audio track through text_prompt. Pass uploaded object_url values directly in reference_audio_urls; reference_material_ids remains supported. The service resolves IDs before URLs and deduplicates audio references before numbering them (default maximum 3). A single audio reference gets @音频1 automatically; multiple references need explicit prompt references. Optional reference_image_urls use @图片1, etc. Preserve the script and verify the resulting audio; voice_id is not an input field.' }),
  search_videos: entry('GOOGLE_SHORT_VIDEO_SEARCH', '513300732e0', 'sync', {
    query: 'string', google_domain: 'string', gl: 'string', hl: 'string', limit: 'integer',
  }, ['query'], { query: 'portable projector', gl: 'us', hl: 'en', limit: 5 }),
  visual_matches: entry('GOOGLE_VISUAL_MATCH_SEARCH', '513300733e0', 'sync', {
    image_url: 'url', hl: 'string', country: 'string', limit: 'integer',
  }, ['image_url'], { image_url: 'https://example.com/product.jpg', country: 'US', limit: 5 }),
  search_suppliers: entry('ALIBABA_1688_SUPPLIER_SEARCH', '513300734e0', 'unknown', {
    image_url: 'url', sort: 'string', limit: 'integer',
  }, ['image_url'], { image_url: 'https://example.com/product.jpg', sort: 'default', limit: 5 },
  { validation: 'example_fields_only', note: 'Use the actual returned fields. If results cannot be interpreted, report the query status without inventing supplier details.' }),
  search_tiktok: entry('TIKTOK_VIDEO_SEARCH', '513300735e0', 'sync', {
    query: 'string', offset: 'integer', limit: 'integer', sortType: 'integer', publishTime: 'integer', region: 'string',
  }, ['query'], { query: 'portable projector', offset: 0, limit: 5, sortType: 0, publishTime: 0, region: 'US' },
  { note: 'Preserve the exact casing of sortType and publishTime; do not convert them to snake_case.' }),
  amazon_reviews: entry('AMAZON_REVIEW_SEARCH', '513300736e0', 'unknown', {
    url: 'url', domain: 'string', limit: 'integer',
  }, ['url'], { url: 'https://www.amazon.com/dp/REPLACE_ASIN', domain: 'com', limit: 5 },
  { validation: 'example_fields_only', note: 'Use actual response fields. If results cannot be interpreted, report query status; an empty response does not establish zero reviews.' }),
  reddit_reviews: entry('REDDIT_REVIEW_SEARCH', '513300737e0', 'sync',
    { query: 'string', limit: 'integer' }, ['query'], { query: 'portable projector', limit: 5 }),
  list_templates: entry('VIDEO_PACKING_TEMPLATE_LIST', '513300738e0', 'sync', {
    business_type: 'string', template_type: 'string', scope: 'string', keyword: 'text', page: 'integer', size: 'integer',
  }, [], { business_type: 'mixed_cut', template_type: 'video-editor', page: 1, size: 100 },
  {
    note: 'For ordinary translation packaging use mixed_cut / video-editor, omit scope for all visible scopes, and follow returned pagination. Use the relevant category for other workflows; application must match the destination operation.' }),
  get_template: entry('VIDEO_PACKING_TEMPLATE_DETAIL', '513300739e0', 'sync', {
    template_id: 'id',
  }, ['template_id'], { template_id: '2100065567327711232' }, {
    wire: 'json_text_exact', result_kind: 'resource',
    note: 'Queries an existing packaging template by its real ID. Read-only; it does not create, edit or apply a template and does not enable dynamic subtitle workflows.' }),
  list_materials: entry(undefined, '526954858e0', 'sync', {
    name: 'text', media_type: 'string', collection_name: 'string', tag_names: 'string_array',
    tag_match_mode: 'string', category: 'string', classification_source: 'string', page: 'integer', page_size: 'integer',
  }, [], { media_type: 'VIDEO', page: 1, page_size: 20 }, {
    wire: 'resource', method: 'GET', endpoint: '/materials', result_kind: 'material', material_operation: 'list', read_only: true,
    note: 'Lists accessible materials, including unanalyzed items. Pages start at 1; repeated tag_names preserve exact names. Fetch detail before using original media.' }),
  batch_get_materials: entry(undefined, '526956401e0', 'sync', {
    material_ids: 'ids',
  }, ['material_ids'], { material_ids: ['2100065567327711232', '2100065567327711233'] }, {
    wire: 'resource', method: 'POST', endpoint: '/materials:batchGet', result_kind: 'material', material_operation: 'batch', read_only: true,
    note: 'Read-only lookup of 1..100 IDs before deduplication. Missing IDs may be inaccessible or absent; they are not proven deleted. No task or submission journal is created.' }),
  get_material: entry(undefined, '526971802e0', 'sync', {
    material_id: 'id', segment_page: 'integer', segment_page_size: 'integer',
  }, ['material_id'], { material_id: '2100065567327711232', segment_page: 1, segment_page_size: 20 }, {
    wire: 'resource', method: 'GET', endpoint: '/materials/{materialId}', result_kind: 'material', material_operation: 'detail', read_only: true,
    note: 'Fetches source media, metadata and existing analysis. Segment pagination applies separately to every scene. Refresh detail when its signed media URLs expire; this query does not start analysis.' }),
  search_materials: entry(undefined, '526973679e0', 'sync', {
    query: 'string', media_types: 'string_array', collection_name: 'string', tag_names: 'string_array',
    tag_match_mode: 'string', category: 'string', classification_source: 'string', top_k: 'integer',
  }, ['query'], { query: 'A person running beside the sea', media_types: ['VIDEO'], top_k: 5 }, {
    wire: 'resource', method: 'POST', endpoint: '/materials:search', result_kind: 'material', material_operation: 'search', read_only: true,
    note: 'Searches existing analyzed text, not every library item. Scores rank this response only. No pagination; top_k counts materials, with at most 20 matches each. Read timeout defaults to 120 seconds; --timeout-seconds overrides it.' }),
  import_material_videos: entry(undefined, '526975082e0', 'async', {
    items: 'objects', collection_name: 'string', auto_ingest: 'boolean',
  }, ['items'], { items: [{ url: 'https://example.com/source.mp4', name: 'Product-showcase-v1.mp4' }], auto_ingest: false }, {
    wire: 'resource', method: 'POST', endpoint: '/materials:importFromUrls', result_kind: 'material_import', defaults: { auto_ingest: false },
    note: 'Imports video URLs into the material library; one existing collection_name applies to the batch. auto_ingest defaults to false in this client. Save the original import task ID; imported media and analysis have separate outcomes.' }),
  get_material_import: entry(undefined, '526977708e0', 'sync', {
    import_task_id: 'string',
  }, ['import_task_id'], { import_task_id: '2100065567327711232' }, {
    wire: 'resource', method: 'GET', endpoint: '/material-import-tasks/{taskId}', result_kind: 'material_import',
    note: 'Queries the original material import task ID, not a generation task. SUCCESS does not prove analysis completed. Read imported material IDs and each item outcome.' }),
  upload_info: entry('MATERIAL_UPLOAD', '513300740e0', 'sync',
    { is_temporary: 'boolean' }, ['is_temporary'], { is_temporary: false },
    { result_kind: 'upload_instructions',
      note: 'Without --file, request upload information only. With --file, transfer the local file using OSS V4 form credentials and return object_url. This does not register library material; obtain a real material_id separately when required.' }),
  compose: entry('MEDIA_PRODUCTION', '513300741e0', 'async',
    { packing_origin: 'object', video_packing_template: 'object' }, ['packing_origin', 'video_packing_template'], {
      packing_origin: { video_track_list: [{ MainTrack: true, VideoTrackClips: [
        { MediaURL: 'https://example.com/source.mp4', Type: 'Video', In: 0, Out: 5 },
      ] }] },
      video_packing_template: {
        background: { type: 'color', width: 1920, height: 1080, color: '#000000' },
        video: { x: 0, y: 0, width: 1, height: 1, adapt_mode: 'Contain' },
      },
    }, { result_kind: 'video', validation: 'example_fields_only', note: 'Preserve track-field casing and use the documented composition configuration. Inspect the actual rendered result.' }),
  gen_image: entry('AIGC_IMAGE_GENERATION', '517411420e0', 'async',
    { prompt: 'string', model: 'string', size: 'string', reference_image_urls: 'urls' }, ['prompt', 'model', 'size'],
    { prompt: 'A blue ceramic cup on a white background', model: 'gpt-image-2.5-sunburst', size: '1024x1024' },
    { wire: 'native_object', result_kind: 'image',
      defaults: { model: 'gpt-image-2.5-sunburst', size: '1024x1024' },
      models: ['gpt-image-2', 'gpt-image-2.5-flare', 'gpt-image-2.5-sunburst'],
      note: 'Default model: gpt-image-2.5-sunburst; default size: 1024x1024. Explicit model and size are preserved. Inputs: prompt, model, size and optional reference_image_urls. The singular reference_image_url and mask fields are not supported; verify the returned image and dimensions.' }),
  list_digital_humans: entry('QUERY_DIGITAL_HUMAN_LIST', '517439849e0', 'sync', {}, [], {},
    { result_kind: 'resource', requires_opt_in: false,
      note: 'Query directly; resource counts, IDs, and access scope come from the current account response.' }),

  list_products: entry('ECOM_PRODUCT_LIST', '519653477e0', 'sync',
    { keyword: 'text', page: 'integer', size: 'integer' }, [],
    { keyword: '', page: 0, size: 20 },
    { wire: 'native_object', result_kind: 'product',
      note: 'Product pages start at page=0. Use real pagination. List entries are summaries; read the selected product detail before production.' }),
  get_product: entry('ECOM_PRODUCT_DETAIL', '519653734e0', 'sync',
    { product_id: 'id' }, ['product_id'], { product_id: '2102324709335007232' },
    { wire: 'native_object', result_kind: 'product',
      note: 'Use a real product ID. Preserve product facts, AI profiles and analysis states; a successful save does not mean analysis is complete.' }),
  parse_products: entry('ECOM_PRODUCT_PARSE_LINKS', '519694921e0', 'sync',
    { links: 'urls' }, ['links'], { links: ['https://example.com/products/projector'] },
    { wire: 'native_object', result_kind: 'product',
      note: 'Parse product links without saving. Check each status and data completeness, retaining source links and failures.' }),
  create_product: entry('ECOM_PRODUCT_CREATE', '519655769e0', 'sync', {
    name: 'string', price: 'number', price_unit: 'string', image_url: 'url',
    description: 'text', source: 'string', selling_points: 'strings',
  }, ['name'], { name: 'Portable projector', price: 99, price_unit: 'USD', source: 'manual' },
  { wire: 'native_object', result_kind: 'product', validation: 'example_fields_only',
    note: 'Save supplied product facts and omit unknown values. Retain the returned ID; AI analysis may remain PENDING. Use batch_create_products to preserve parsed multiple images and source identity.' }),
  update_product: entry('ECOM_PRODUCT_UPDATE', '519688859e0', 'sync', {
    product_id: 'id', name: 'string', price: 'number', price_unit: 'string',
    description: 'text', selling_points: 'strings',
  }, ['product_id', 'name'], { product_id: '2102324709335007232', name: 'Portable projector', price: 89, price_unit: 'USD' },
  { wire: 'native_object', result_kind: 'product', validation: 'example_fields_only',
    note: 'Read detail first; use its current name and documented writable values that must be retained. Do not promise safe patch semantics when omission/clearing is undefined. Do not submit AI profiles or creative requirements.' }),
  delete_product: entry('ECOM_PRODUCT_DELETE', '519690178e0', 'sync',
    { product_id: 'id' }, ['product_id'], { product_id: '2102324709335007232' },
    { wire: 'native_object', result_kind: 'product',
      note: 'Use only for an explicit deletion request with an identified target. Check returned product_id and deleted; never automatically clean up candidates.' }),
  batch_create_products: entry('ECOM_PRODUCT_BATCH_CREATE', '519696014e0', 'sync',
    { products: 'objects' }, ['products'], { products: [{
      url: 'https://example.com/products/projector', name: 'Portable projector', price: 99,
      price_unit: 'USD', image_url: 'https://example.com/projector.jpg',
      image_urls: ['https://example.com/projector.jpg'], description: 'A portable projector',
      selling_points: ['Compact design'], third_product_id: 'projector-001',
      third_product_url: 'https://example.com/products/projector', source: 'shopline',
      platform: 'shopline', status: 'SUCCESS',
    }] }, { wire: 'native_object', result_kind: 'product', validation: 'example_fields_only',
      note: 'Save only selected, successfully parsed products using documented fields. Do not send source_asin, error_code, AI profiles or other parse/detail fields unchanged. Verify returned IDs individually; do not assume ordering or automatic deduplication.' }),

}

const models = {
  'doubao-seedance-2-0-fast-260128': { resolutions: ['480p', '720p'], max_duration: 15, references: [9, 3, 3] },
  'doubao-seedance-2-0-260128': { resolutions: ['480p', '720p', '1080p', '4k'], max_duration: 15, references: [9, 3, 3] },
  'doubao-seedance-2-0-mini-260615': { resolutions: ['480p', '720p'], max_duration: 15, references: [9, 3, 3] },
  'doubao-seedance-2-5-260628': { resolutions: ['480p', '720p', '1080p'], max_duration: 30, references: [30, 10, 10] },
}

module.exports = { commands, models }
