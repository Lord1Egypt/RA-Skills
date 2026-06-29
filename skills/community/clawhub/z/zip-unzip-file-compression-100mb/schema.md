# Zip / Unzip - File Compression < 100MB Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `zip-unzip-file-compression-100mb`

x402 availability: not enabled for this product.

## `compress`

Action slug: `compress`

Price: `20` credits

Create a ZIP or GZIP archive from input files. ZIP supports up to 500 files; GZIP compresses a single file. Input and output must be between 10MB and 100MB.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `archive_format` | `string` | yes | Archive format to use. |
| `filename` | `string` | no | Output archive filename (default: 'archive.zip' or 'archive.gz'). |
| `files` | `array` | no | Files to include in a zip archive. Each object must have 'filename' (string) and 'content_base64' (string). Required for ZIP compression. |
| `input_base64` | `string` | no | Base64-encoded file content for GZIP compression. |

Sample parameters:

```json
{
  "archive_format": "zip",
  "filename": "example filename",
  "files": [
    {
      "content_base64": "Draft marketing copy to check for banned phrases.",
      "filename": "example filename"
    }
  ],
  "input_base64": "example input base64"
}
```

Generated JSON parameter schema:

```json
{
  "archive_format": {
    "description": "Archive format to use.",
    "enum": [
      "zip",
      "gzip"
    ],
    "required": true,
    "type": "string"
  },
  "filename": {
    "description": "Output archive filename (default: 'archive.zip' or 'archive.gz').",
    "required": false,
    "type": "string"
  },
  "files": {
    "description": "Files to include in a zip archive. Each object must have 'filename' (string) and 'content_base64' (string). Required for ZIP compression.",
    "items": {
      "properties": {
        "content_base64": {
          "description": "Base64-encoded file content.",
          "required": true,
          "type": "string"
        },
        "filename": {
          "description": "Filename/path inside the archive.",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "input_base64": {
    "description": "Base64-encoded file content for GZIP compression.",
    "required": false,
    "type": "string"
  }
}
```

## `decompress`

Action slug: `decompress`

Price: `20` credits

Extract files from a ZIP or GZIP archive (10-100MB). Provide via file_id or input_base64. All extracted files are uploaded to cloud storage.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `archive_format` | `string` | yes | Archive format of the input. |
| `file_id` | `string` | no | File ID of a previously stored archive to decompress. |
| `filename` | `string` | no | Output filename for GZIP decompressed file (default: 'decompressed'). |
| `input_base64` | `string` | no | Base64-encoded archive to decompress. |

Sample parameters:

```json
{
  "archive_format": "zip",
  "file_id": "example file id",
  "filename": "example filename",
  "input_base64": "example input base64"
}
```

Generated JSON parameter schema:

```json
{
  "archive_format": {
    "description": "Archive format of the input.",
    "enum": [
      "zip",
      "gzip"
    ],
    "required": true,
    "type": "string"
  },
  "file_id": {
    "description": "File ID of a previously stored archive to decompress.",
    "required": false,
    "type": "string"
  },
  "filename": {
    "description": "Output filename for GZIP decompressed file (default: 'decompressed').",
    "required": false,
    "type": "string"
  },
  "input_base64": {
    "description": "Base64-encoded archive to decompress.",
    "required": false,
    "type": "string"
  }
}
```
