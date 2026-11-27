# Upload and delivery

## Upload input bytes

1. Verify that the host can read the user-authorized file and upload its bytes. Determine the actual byte size and image MIME type or model format.
2. Call `tripo_create_image_upload_grant` with `content_type` and `size_bytes`, or `tripo_create_model_upload_grant` with `format` and `size_bytes`.
3. PUT the exact bytes to the returned HTTPS `upload_grant.upload_url` with the returned `required_headers` before `expire_time`. For images use the declared MIME type. For model uploads use `Content-Type: application/octet-stream`. Preserve any required signed headers, and stop if the grant conflicts with the expected upload type. Send only the upload's required headers and bytes to the granted destination. Stop on a redirect to another origin. If the host cannot perform the PUT, explain what needs to be uploaded.
4. After a successful PUT, use that grant's opaque `object_key` where the next tool expects an input upload key. For model import use `tripo_import_model` with `resource_key`, a stable `idempotency_key`, and only requested import options. Poll the import task and read the resulting model before using it.

If the authorized user explicitly asks to upload the file themselves, request
the matching grant with the supplied byte size and MIME type or format. Provide
the temporary upload URL, required headers, and expiration through the host's
secure handoff or a confirmed private conversation with the requesting user.
If the destination is shared or its privacy is unclear, direct the user to
a private handoff. Stop at the grant. Keep the
URL and headers out of logs and shared conversations. Request a fresh grant if the grant expires before the file has been successfully uploaded.

## Deliver assets and exports

Inspect the successful result's model asset before any export or format write
when delivering a model download. An existing `model_url` that meets the requested
format is the deliverable; a same-format link request does not request export.
For an expired link, re-read that same asset. A request for a GLB link does
not require a new export when the existing link already points to a GLB.
After an import succeeds, read the new model asset before converting it.
If import fails, report the failure and stop without exporting another asset.

For an explicitly requested Blender FBX with embedded textures, use
`format: fbx`, `fbx_preset: blender`, and `texture_packaging: embedded`
when the connected export schema supports them.

| Result | Read and deliver |
| --- | --- |
| Model task | Use `tripo_get_model_asset` with the delivered `model_id` and use its `model_url` if provided. |
| Image task | Use `tripo_get_image_asset` with each delivered `image_id` and use its `download_url` if provided. |
| Motion task | Use `tripo_get_motion_asset` with the delivered `motion_id` and use its `download_url` if provided. |
| Conversion or explicit export settings | Use the existing model file if it already meets the requested output. Otherwise submit `tripo_export_model` for the chosen source and format. After success, use its `export_id` with `tripo_get_model_export` to read the file metadata and any `download_url`. |

Report the actual format and asset ID. Give the authorized recipient the available link or the downloaded file when the host can verify it. When a signed link expires, re-query the same asset or export for a new link. When a successful task has an asset but no link, report the asset ID and that download is unavailable through this connection. Keep task IDs, asset IDs, and upload keys in their respective fields.

## GLB compatibility for Blender and other local tools

Use this only when the user needs to open or process the asset in a tool that
cannot read its GLB. Use the signed `model_url` or export `download_url`
returned by MCP. If a download client gets HTTP 403 on a fresh link, try the
same URL once with the host's HTTP/2-capable curl. Use the returned URL as-is
and send no MCP credentials to the download host. Keep the signed URL out of
logs and shared messages.

```sh
# Set signed_url from the MCP result without echoing it.
printf 'url = "%s"\n' "$signed_url" | \
  curl --disable --http2 --fail --silent --show-error --output model_meshopt.glb --config -
```

If the link expired, refresh it through the same asset or export lookup. If
access is still denied, report the download blocker. Verify that the response
is a complete GLB before processing. Keep the original and inspect its
`extensionsUsed` and `extensionsRequired`. A suffix such as `_meshopt.glb`
is only a hint.

Use the host's preinstalled glTF Transform CLI to decode Meshopt to a
separate file. These commands were verified with version 4.5.1. If the CLI is
unavailable, hand off the commands to the user. Use `copy` when the destination supports the remaining
extensions. If the destination also needs unquantized vertex attributes, use
`dequantize` on the original instead:

```sh
gltf-transform copy model_meshopt.glb model_decoded.glb
# Alternative when the destination also needs dequantization
gltf-transform dequantize model_meshopt.glb model_for_blender.glb
```

Reinspect the output for the unsupported extensions and try importing it in the
target app if available. Report which checks actually ran. Dequantization does
not restore precision lost during quantization. [glTF Transform CLI](https://gltf-transform.dev/cli)

A parse failure alone does not establish encryption. For an asset known to be
encrypted, use a supported, authorized decoder or obtain a compatible download
through Studio. If neither is available, report the blocker. The commands above
require readable glTF input.

**Verification scope.** On a real test MCP asset, the initial Python download
returned HTTP 403 and curl with HTTP/2 returned HTTP 200 on the same fresh
signed URL. Both converted files imported into Blender 5.1.2. This was a
step-by-step toolchain check. Independent Agent execution and the encrypted
GLB path still need end-to-end verification.


If a completed export record has no download_url, report that the export file
cannot be retrieved through this response and stop. A source model link is a
different file. Avoid looking up the original model or creating another export
to fill the missing link unless the user requests that alternative. End the
reply at that blocker; do not append an unsolicited suggestion or offer to
re-export, switch formats or supply the source file instead.

An already-uploaded model key is ready for `tripo_import_model.resource_key`.
Do not open it as a local file, request another upload or search for a substitute.
Follow the import task; a failed import blocks dependent conversion.

Deliver only requested assets or views. If the response contains several views
but the user asks for one, select that view by its authoritative label; do not
append a table of the others or fetch their files solely for completeness.

Treat an uploaded `resource_key` as opaque remote input, never a local file_path.
For an explicitly requested import with an existing uploaded key, call
`tripo_import_model` directly using the input schema, for example:

```json
{"resource_key":"<uploaded key>","idempotency_key":"<new-operation key>"}
```

A supplied key identifies this write; it does not establish an uncertain prior
submission. A conditional recovery instruction applies only after submission.
