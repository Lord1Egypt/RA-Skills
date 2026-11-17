# Media upload: upload_info

Task type: `MATERIAL_UPLOAD`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300740e0)

Without --file, request upload information only. With --file, transfer the local file using OSS V4 form credentials and return object_url. For reference audio generation, pass that URL directly in [generate_audio](generate_audio.md)'s `reference_audio_urls`, without library registration. Obtain a real material_id separately only for operations that require one.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `is_temporary` | boolean | Yes |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "is_temporary": false
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" upload_info --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" upload_info --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

## Actual local-file upload

Without --file, this command only obtains upload information. With --file, it sends the file through the returned OSS V4 multipart form credentials. The file must be a regular local file. If --input is omitted, permanent storage is requested; use {"is_temporary":true} for temporary storage.

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" upload_info --file /absolute/path/source.mp4 --input /absolute/path/upload-request.json
~~~

The request object contains is_temporary. The sequence is: submit MATERIAL_UPLOAD; parse the synchronous task_result.result; obtain host, dir, policy, xoss_credential, xoss_date, signature, security_token; generate a unique key under dir; POST actual file bytes to host using multipart/form-data. Form names include x-oss-credential, x-oss-date, x-oss-signature, x-oss-security-token.

### Upload security checks

Use `upload_info --file` to apply these checks. A custom uploader must enforce the same checks before sending data; do not pass a returned host directly to curl.

- Require HTTPS with TLS certificate verification. Reject HTTP and redirects; never retry with a different protocol or host after failure.
- Accept only the built-in Vibbit storage hosts: `willing-video-test.oss-cn-shanghai.aliyuncs.com` and `vibbit-ai.oss-ap-southeast-1.aliyuncs.com`. Reject other hosts, internal endpoints, embedded credentials, nonstandard ports, paths, queries, and fragments. Stop an upload to an unsupported target, retain the local file, and explain the reason; never expand the allowlist from an API response.
- Decode the policy before upload. Check expiry, a nonempty object-key constraint, file-size limits, and exact constraints for signing version, credential, date, and temporary token. Check bucket/host, signing-region/host, and generated-key/policy consistency. Missing, conflicting, or unsupported conditions stop the upload; never weaken the policy to proceed.
- Only normalize the known `oss-` prefix within the same region, such as `oss-cn-shanghai` to `cn-shanghai`. Never re-sign a credential for a different region.
- The AccessKey ID in `x-oss-credential` supports the valid `STS.` temporary-credential prefix. Preserve that ID and its consistency with the response and policy; do not strip the dot or rewrite it.
- Return the HTTP status or a generic transport error without exposing the raw OSS response or temporary credentials. When validation fails, retain the local file and check the returned upload information or contact support; do not bypass validation.

| Output with --file | Meaning |
| --- | --- |
| object_url | Uploaded OSS URL for operations that accept accessible media |
| object_key | Storage object key |
| bytes | Actual local byte count |
| oss_http_status | Upload response status |
| material_id | null; no library registration is provided by this public operation |

Without --file, results can contain temporary credentials, host, dir, policy, signature, and expiry. Keep credentials restricted to the specified upload; never place them in final user-facing results, skill files, or persistent journals. The client excludes them from task journals.

Check that the resulting URL can be read by the next service. A storage path alone does not establish file existence, completed transfer, or library registration. A material_id requires a separate supported registration result; the current public skill provides no registration operation. If transfer is unavailable, use an existing accessible URL supplied by the user.
