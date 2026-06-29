# WAPC Workflow Reference

## Core Page Flow

1. Open the WAPC page on `mulandxc.com`.
2. Inspect `account/donation_app_list?wapc_app_id=806`.
3. Save text fields with `account/update_app_detail`.
4. Upload the LoTW evidence image with `account/upload_app_img?id=<row id>`.
5. Recheck `account/check_detail`.
6. If the check passes, open the applicant-info modal and call `on_save()`.

## Row Data Contract

The row JSON returned by `donation_app_list` uses these fields:

- `id`
- `seq`
- `province`
- `suffix`
- `call_sign`
- `date`
- `time`
- `band`
- `mode`
- `rst`
- `qsl_path`
- `status`

## Saving Text Fields

Use `POST /account/update_app_detail` with:

- `field`
- `value`
- `id`

The page uses this same endpoint after inline edits.

## Uploading Evidence

The upload control eventually posts to:

- `POST /account/upload_app_img?id=<row id>`

The returned JSON is expected to contain:

- `state: "ok"`
- `file_path`

The page then sets the row image `src` to `file_path`.

## Validation

`do_submit()` calls:

- `POST /account/check_detail` with `wapc_app_id=806`

If the response is not `{"state":"ok"}`, the page shows:

- `QSL通联列表，没有填写完整，请完善后再提交！`

Do not trust the visible image alone. Recheck the backend row JSON if the page still fails validation.

## Applicant Info Modal

The submit modal calls:

- `POST /account/app_save`

Payload fields:

- `po.id=806`
- `po.is_qrp`
- `po.member_callsign`
- `po.member_name`
- `po.member_phone`
- `po.address`

If any required field is empty, the modal shows:

- `必填项不能为空！`

## Local Evidence Convention

Keep final evidence files under the project folder path used for WAPC work, with numbered names in sequence. For this session the confirmed screenshot files were:

- `32_BV7RR.png`
- `33_VR2WAA.png`
- `34_XX9W.png`

## Known Good Check

For this session, `check_detail` returned `{"state":"ok"}` only after the backend text fields were saved for every populated row.
