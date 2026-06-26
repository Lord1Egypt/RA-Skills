# Video Gen API (dashboard-console)

Base:
- `https://xiaonian.cc/employee-console/dashboard/v2/api`

## Auth

`Authorization: Bearer <jwt>`

## Endpoints

### 1) Generate script

- `POST /video/script/gen`
- body: `{ video_type, request_desc, duration?, has_subtitle? }`
- resp: `{ data: { script } }`

### 2) Create task

- `POST /video/task/create`
- body: `{ video_type, request_desc, script, duration?, image_file_path?, orientation?, is_hd? }`
- resp: `{ data: { task_id } }`

### 3) Poll state

- `GET /video/task/state?task_id=...`
- resp: `{ data: { status, progress?, video_url?, failed_reason? } }`

Status values (dashboard):
- queued
- in_progress
- completed
- failed
