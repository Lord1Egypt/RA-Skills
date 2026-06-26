# Rough Cut API

Local API base:

- `http://localhost/api/v1`

## Create a job

`POST /rough-cuts`

Multipart form fields:
- `file`
- `name`
- `platform_preset`
- `remove_pauses`
- `remove_breaths`
- `adjust_brightness`
- `apply_beauty`
- `trim_head_tail`
- `auto_center`
- `stabilize`
- `denoise_audio`
- `min_pause_duration`
- `breath_sensitivity`
- `brightness_mode`
- `beauty_mode`
- `beauty_strength`
- `crossfade_duration`
- `auto_start`

## Poll status

`GET /rough-cuts/{job_id}`

Important fields:
- `status`
- `progress`
- `progress_message`
- `error_message`
- `output_path`

## View cut decisions

`GET /rough-cuts/{job_id}/decisions`

Returns:
- `cut_decisions`
- `transcript_words`
- `total_removed_duration`
- `original_duration`

## Download output

`GET /rough-cuts/{job_id}/download`

Only valid when `status == completed`.

## Common statuses

- `uploaded`
- `processing`
- `transcribing`
- `detecting_pauses`
- `analyzing_brightness`
- `applying_beauty`
- `encoding`
- `completed`
- `failed`
- `cancelled`
