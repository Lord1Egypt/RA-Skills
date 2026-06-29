# Zip / Unzip - File Compression < 10MB Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `zip-unzip-file-compression-10mb`

x402 availability: not enabled for this product.

## `compress`

Action slug: `compress`

Price: `10` credits

Create a ZIP or GZIP archive from input files. ZIP supports up to 200 files; GZIP compresses a single file. Maximum total size is 10MB.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `archive_format` | `string` | yes | Archive format to use. |
| `filename` | `string` | no | Output archive filename (default: 'archive.zip' or 'archive.gz'). |
| `files` | `array` | no | Files to include in a zip archive. Each object must have 'filename' (string) and 'content_base64' (string). Required for ZIP compression. |
| `include_contents` | `boolean` | no | Include base64 of the archive in the response. |
| `input_base64` | `string` | no | Base64-encoded file content for GZIP compression. |
| `store_file` | `boolean` | no | Store output in cloud storage for file management access. |

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
  "include_contents": false,
  "input_base64": "example input base64",
  "store_file": true
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
  "include_contents": {
    "default": false,
    "description": "Include base64 of the archive in the response.",
    "required": false,
    "type": "boolean"
  },
  "input_base64": {
    "description": "Base64-encoded file content for GZIP compression.",
    "required": false,
    "type": "string"
  },
  "store_file": {
    "default": true,
    "description": "Store output in cloud storage for file management access.",
    "required": false,
    "type": "boolean"
  }
}
```

## `decompress`

Action slug: `decompress`

Price: `10` credits

Extract files from a ZIP or GZIP archive provided via base64 or file ID. Extracted files are stored in cloud storage.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `archive_format` | `string` | yes | Archive format of the input. |
| `file_id` | `string` | no | File ID of a previously stored archive to decompress. |
| `filename` | `string` | no | Output filename for GZIP decompressed file (default: 'decompressed'). |
| `include_contents` | `boolean` | no | Include base64 content of each extracted file in the response. |
| `input_base64` | `string` | no | Base64-encoded archive to decompress. |
| `store_file` | `boolean` | no | Store each extracted file in cloud storage. |

Sample parameters:

```json
{
  "archive_format": "zip",
  "file_id": "example file id",
  "filename": "example filename",
  "include_contents": false,
  "input_base64": "example input base64",
  "store_file": true
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
  "include_contents": {
    "default": false,
    "description": "Include base64 content of each extracted file in the response.",
    "required": false,
    "type": "boolean"
  },
  "input_base64": {
    "description": "Base64-encoded archive to decompress.",
    "required": false,
    "type": "string"
  },
  "store_file": {
    "default": true,
    "description": "Store each extracted file in cloud storage.",
    "required": false,
    "type": "boolean"
  }
}
```
