'use strict'

const entry = (task_type, doc, mode, fields, required, example, extra = {}) => ({
  task_type, ...(doc ? { documentation_url: `https://vibbit.apifox.cn/${doc}` } : {}), mode,
  wire: 'object', status: 'documented', min_poll_ms: 5000,
  fields, required, example, ...extra,
})

const commands = {
  translate_video: entry('VIDEO_VOICE_OVER_TASK', '515705766e0', 'async', {
    business_id: 'id', task_name: 'string', source_language: 'string', target_language: 'string',
    translation_style: 'string', default_speed: 'number', auto_translate: 'boolean',
    subtitle_enabled: 'boolean', lip_sync_enabled: 'boolean', remove_subtitles_enabled: 'boolean',
    persona_mode: 'string', template_type: 'integer', template_configs: 'objects',
    default_digital_human_id: 'id', default_prompt: 'string',
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
  }, [], { business_type: 'scrolling_subtitle', template_type: 'video-editor', scope: 'common', keyword: '', page: 1, size: 20 },
  {
    note: 'Query the list directly and use returned detail; template application must match the destination operation.' }),
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
  list_digital_humans: entry('QUERY_DIGITAL_HUMAN_LIST', '', 'sync', {}, [], {},
    { status: 'legacy', result_kind: 'resource', requires_opt_in: false,
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
