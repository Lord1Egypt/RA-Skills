#!/usr/bin/env python3
"""
Telnyx Embeddings - Index & Bucket Management

Upload files to Telnyx Storage, trigger embedding, and manage buckets.
Files become searchable via similarity search after embedding completes.

Usage:
  ./index.py upload path/to/file.md
  ./index.py upload path/to/dir/ --pattern "*.md"
  ./index.py embed
  ./index.py embed --bucket my-bucket
  ./index.py status <task_id>
  ./index.py list
  ./index.py list --bucket my-bucket
  ./index.py buckets
  ./index.py create-bucket my-bucket
  ./index.py delete path/to/file.md
"""

import os
import sys
import json
import hashlib
import hmac
import datetime
import urllib.request
import urllib.error
import urllib.parse
import re
import argparse
import mimetypes
from pathlib import Path


# Default configuration
DEFAULT_CONFIG = {
    "bucket": "openclaw-main",
    "region": "us-central-1",
    "default_num_docs": 5,
}


def load_config():
    """Load configuration from file or defaults"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                user_config = json.load(f)
                return {**DEFAULT_CONFIG, **user_config}
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG


def load_credentials():
    """Load Telnyx API key from environment or .env file

    Returns:
        str: The Telnyx API key

    Raises:
        SystemExit: If no API key found
    """
    if os.environ.get("TELNYX_API_KEY"):
        return os.environ["TELNYX_API_KEY"]

    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("TELNYX_API_KEY="):
                    return line.split("=", 1)[1].strip('"').strip("'")

    print("ERROR: No Telnyx API key found", file=sys.stderr)
    print("Set TELNYX_API_KEY environment variable or create .env file with:", file=sys.stderr)
    print("  TELNYX_API_KEY=your-api-key", file=sys.stderr)
    sys.exit(1)


def parse_telnyx_error(error_body):
    """Parse Telnyx API error response"""
    try:
        error_data = json.loads(error_body)
        if "errors" in error_data and error_data["errors"]:
            error = error_data["errors"][0]
            code = error.get("code", "unknown")
            detail = error.get("detail", "No details provided")
            return "%s: %s" % (code, detail)
        elif "message" in error_data:
            return error_data["message"]
        else:
            return error_body.strip()
    except (json.JSONDecodeError, KeyError):
        return error_body.strip()


# ---------------------------------------------------------------------------
# S3 Client (rewritten from tools/rag/sync.py TelnyxS3Client)
# ---------------------------------------------------------------------------

class TelnyxS3Client:
    """S3 client for Telnyx Cloud Storage using AWS SigV4"""

    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region
        self.secret_key = "placeholder"  # Telnyx uses API key as access key

    def _sign(self, key, msg):
        """AWS SigV4 signing helper"""
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def _get_signature_key(self, date_stamp):
        """Generate AWS SigV4 signing key"""
        k_date = self._sign(("AWS4" + self.secret_key).encode("utf-8"), date_stamp)
        k_region = self._sign(k_date, self.region)
        k_service = self._sign(k_region, "s3")
        k_signing = self._sign(k_service, "aws4_request")
        return k_signing

    def _make_request(self, method, bucket, key, payload=b"", content_type=None, extra_headers=None):
        """Make authenticated S3 request"""
        host = (
            "%s.%s.telnyxcloudstorage.com" % (bucket, self.region)
            if bucket
            else "%s.telnyxcloudstorage.com" % self.region
        )
        path = "/%s" % key if key else "/"

        t = datetime.datetime.now(datetime.timezone.utc)
        amz_date = t.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = t.strftime("%Y%m%d")

        payload_hash = hashlib.sha256(payload).hexdigest()

        headers = {
            "host": host,
            "x-amz-content-sha256": payload_hash,
            "x-amz-date": amz_date,
        }

        if content_type:
            headers["content-type"] = content_type
        if payload:
            headers["content-length"] = str(len(payload))
        if extra_headers:
            headers.update(extra_headers)

        canonical_headers = "".join("%s:%s\n" % (k, v) for k, v in sorted(headers.items()))
        signed_headers = ";".join(sorted(headers.keys()))

        canonical_request = "%s\n%s\n\n%s\n%s\n%s" % (
            method, path, canonical_headers, signed_headers, payload_hash
        )

        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = "%s/%s/s3/aws4_request" % (date_stamp, self.region)
        string_to_sign = "%s\n%s\n%s\n%s" % (
            algorithm,
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode()).hexdigest(),
        )

        signing_key = self._get_signature_key(date_stamp)
        signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()

        auth = "%s Credential=%s/%s, SignedHeaders=%s, Signature=%s" % (
            algorithm, self.api_key, credential_scope, signed_headers, signature
        )

        request_headers = {
            "x-amz-date": amz_date,
            "x-amz-content-sha256": payload_hash,
            "Authorization": auth,
        }
        if content_type:
            request_headers["Content-Type"] = content_type
        if payload:
            request_headers["Content-Length"] = str(len(payload))
        if extra_headers:
            request_headers.update(extra_headers)

        url = "https://%s%s" % (host, path)
        req = urllib.request.Request(
            url, data=payload if payload else None, headers=request_headers, method=method
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.status, response.read().decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return 0, str(e)

    def put_object(self, bucket, key, data, content_type=None):
        """Upload object to bucket"""
        if isinstance(data, str):
            data = data.encode("utf-8")

        if not content_type:
            if key.endswith(".md"):
                content_type = "text/markdown"
            elif key.endswith(".json"):
                content_type = "application/json"
            elif key.endswith(".txt"):
                content_type = "text/plain"
            else:
                guessed, _ = mimetypes.guess_type(key)
                content_type = guessed or "application/octet-stream"

        status, body = self._make_request("PUT", bucket, key, data, content_type)
        return status in [200, 204], status, body

    def list_objects(self, bucket, prefix=""):
        """List objects in bucket"""
        query = "?prefix=%s" % urllib.parse.quote(prefix) if prefix else ""
        status, body = self._make_request("GET", bucket, "" + query)

        if status == 200:
            files = []
            for match in re.finditer(r"<Key>([^<]+)</Key>", body):
                files.append(match.group(1))
            return files
        return []

    def delete_object(self, bucket, key):
        """Delete object from bucket"""
        status, _ = self._make_request("DELETE", bucket, key)
        return status in [200, 204]

    def create_bucket(self, bucket):
        """Create bucket in region"""
        bucket_config = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">\n'
            "  <LocationConstraint>%s</LocationConstraint>\n"
            "</CreateBucketConfiguration>" % self.region
        )

        host = "%s.telnyxcloudstorage.com" % self.region
        path = "/%s" % bucket

        t = datetime.datetime.now(datetime.timezone.utc)
        amz_date = t.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = t.strftime("%Y%m%d")

        payload = bucket_config.encode()
        payload_hash = hashlib.sha256(payload).hexdigest()

        headers = {
            "host": host,
            "x-amz-content-sha256": payload_hash,
            "x-amz-date": amz_date,
            "content-type": "application/xml",
            "content-length": str(len(payload)),
        }

        canonical_headers = "".join("%s:%s\n" % (k, v) for k, v in sorted(headers.items()))
        signed_headers = ";".join(sorted(headers.keys()))

        canonical_request = "PUT\n%s\n\n%s\n%s\n%s" % (
            path, canonical_headers, signed_headers, payload_hash
        )

        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = "%s/%s/s3/aws4_request" % (date_stamp, self.region)
        string_to_sign = "%s\n%s\n%s\n%s" % (
            algorithm,
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode()).hexdigest(),
        )

        signing_key = self._get_signature_key(date_stamp)
        signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()

        auth = "%s Credential=%s/%s, SignedHeaders=%s, Signature=%s" % (
            algorithm, self.api_key, credential_scope, signed_headers, signature
        )

        request_headers = {
            "x-amz-date": amz_date,
            "x-amz-content-sha256": payload_hash,
            "Authorization": auth,
            "Content-Type": "application/xml",
            "Content-Length": str(len(payload)),
        }

        url = "https://%s%s" % (host, path)
        req = urllib.request.Request(url, data=payload, headers=request_headers, method="PUT")

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                status = response.status
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception:
            status = 0

        return status in [200, 204] or status == 409  # 409 = already exists


# ---------------------------------------------------------------------------
# Telnyx API helpers
# ---------------------------------------------------------------------------

def make_api_request(method, endpoint, payload=None, timeout=60):
    """Make Telnyx API request

    Args:
        method (str): HTTP method
        endpoint (str): API endpoint (after /v2/)
        payload (dict): Request body
        timeout (int): Request timeout

    Returns:
        tuple: (status_code, response_data)
    """
    api_key = load_credentials()

    url = "https://api.telnyx.com/v2/%s" % endpoint
    data = json.dumps(payload).encode() if payload else None

    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json",
        "User-Agent": "openclaw-telnyx-embeddings/1.0",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode()
            try:
                return response.status, json.loads(body)
            except json.JSONDecodeError:
                return response.status, body
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        return e.code, error_body
    except Exception as e:
        return 0, str(e)


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_upload(args):
    """Upload file(s) to a Telnyx Storage bucket"""
    config = load_config()
    api_key = load_credentials()
    bucket = args.bucket or config["bucket"]
    client = TelnyxS3Client(api_key, config["region"])

    path = Path(args.path)

    if not path.exists():
        print("ERROR: Path not found: %s" % path, file=sys.stderr)
        sys.exit(1)

    files_to_upload = []

    if path.is_file():
        # Single file upload — use filename as key
        key = args.key or path.name
        files_to_upload.append((path, key))
    elif path.is_dir():
        # Directory upload with optional pattern
        pattern = args.pattern or "*"
        for filepath in sorted(path.glob(pattern)):
            if filepath.is_file():
                rel = filepath.relative_to(path)
                files_to_upload.append((filepath, str(rel)))
    else:
        print("ERROR: Not a file or directory: %s" % path, file=sys.stderr)
        sys.exit(1)

    if not files_to_upload:
        print("No files matched pattern '%s' in %s" % (args.pattern or "*", path))
        sys.exit(1)

    print("\nUploading %d file(s) to bucket '%s':\n" % (len(files_to_upload), bucket))

    success = 0
    failed = 0

    for filepath, key in files_to_upload:
        try:
            with open(filepath, "rb") as f:
                data = f.read()

            ok, status, body = client.put_object(bucket, key, data)
            if ok:
                print("  + %s (%d bytes)" % (key, len(data)))
                success += 1
            else:
                print("  x %s (HTTP %d)" % (key, status), file=sys.stderr)
                failed += 1
        except IOError as e:
            print("  x %s (%s)" % (key, e), file=sys.stderr)
            failed += 1

    print("\nUploaded: %d | Failed: %d" % (success, failed))

    if success > 0:
        print("\nTip: Run './index.py embed --bucket %s' to make files searchable." % bucket)


def cmd_embed(args):
    """Trigger embedding on a bucket"""
    config = load_config()
    bucket = args.bucket or config["bucket"]

    print("\nTriggering embedding on bucket: %s" % bucket)

    status, response = make_api_request("POST", "ai/embeddings", {
        "bucket_name": bucket,
    })

    if status in [200, 201, 202]:
        print("Embedding triggered successfully.")
        if isinstance(response, dict) and "data" in response:
            task_id = response["data"].get("task_id")
            if task_id:
                print("  Task ID: %s" % task_id)
                print("  Check status: ./index.py status %s" % task_id)
    else:
        print("ERROR: Failed to trigger embedding (HTTP %s)" % status, file=sys.stderr)
        if isinstance(response, str):
            print("  %s" % parse_telnyx_error(response), file=sys.stderr)
        elif isinstance(response, dict):
            print("  %s" % json.dumps(response, indent=2), file=sys.stderr)


def cmd_status(args):
    """Check embedding task status"""
    task_id = args.task_id

    print("\nChecking embedding task: %s" % task_id)

    status, response = make_api_request("GET", "ai/embeddings/%s" % task_id)

    if status == 200 and isinstance(response, dict):
        data = response.get("data", {})
        task_status = data.get("status", "unknown")
        progress = data.get("progress", 0)

        print("  Status: %s" % task_status)
        print("  Progress: %s%%" % progress)

        if task_status == "completed":
            print("\nEmbedding complete! Files are now searchable.")
        elif task_status == "failed":
            error = data.get("error", "Unknown error")
            print("\nEmbedding failed: %s" % error)
    else:
        print("ERROR: Failed to check status (HTTP %s)" % status, file=sys.stderr)
        if isinstance(response, str):
            print("  %s" % parse_telnyx_error(response), file=sys.stderr)


def cmd_list(args):
    """List files in a bucket"""
    config = load_config()
    api_key = load_credentials()
    bucket = args.bucket or config["bucket"]

    if args.embeddings:
        # List embedding status for the bucket
        print("\nEmbedding status for bucket: %s" % bucket)
        status, response = make_api_request("GET", "ai/embeddings/buckets/%s" % bucket)

        if status == 200 and isinstance(response, dict):
            data = response.get("data", {})
            if isinstance(data, list):
                files = data
            else:
                files = data.get("files", data.get("embedded_files", []))
            if isinstance(files, list):
                print("  Embedded files: %d" % len(files))
                for f in files:
                    if isinstance(f, dict):
                        print("    %s (%s)" % (f.get("filename", "?"), f.get("status", "?")))
                    else:
                        print("    %s" % f)
            else:
                print(json.dumps(response, indent=2))
        else:
            print("ERROR: Failed to get embedding status (HTTP %s)" % status, file=sys.stderr)
            if isinstance(response, str):
                print("  %s" % parse_telnyx_error(response), file=sys.stderr)
        return

    # List S3 objects
    client = TelnyxS3Client(api_key, config["region"])
    prefix = args.prefix or ""
    files = client.list_objects(bucket, prefix)

    print("\nFiles in '%s'%s (%d):\n" % (
        bucket,
        " (prefix: %s)" % prefix if prefix else "",
        len(files),
    ))

    for f in sorted(files):
        print("  %s" % f)

    if not files:
        print("  (empty)")


def cmd_buckets(args):
    """List all embedded buckets"""
    print("\nListing embedded buckets:")

    status, response = make_api_request("GET", "ai/embeddings/buckets")

    if status == 200 and isinstance(response, dict):
        buckets = response.get("data", [])
        if isinstance(buckets, list):
            if not buckets:
                print("  No embedded buckets found.")
            for b in buckets:
                if isinstance(b, dict):
                    name = b.get("bucket_name", b.get("name", "?"))
                    print("  %s" % name)
                else:
                    print("  %s" % b)
        else:
            print(json.dumps(response, indent=2))
    else:
        print("ERROR: Failed to list buckets (HTTP %s)" % status, file=sys.stderr)
        if isinstance(response, str):
            print("  %s" % parse_telnyx_error(response), file=sys.stderr)


def cmd_create_bucket(args):
    """Create a new bucket"""
    config = load_config()
    api_key = load_credentials()
    bucket = args.bucket_name
    region = args.region or config["region"]

    client = TelnyxS3Client(api_key, region)

    print("\nCreating bucket: %s (region: %s)" % (bucket, region))

    if client.create_bucket(bucket):
        print("Bucket '%s' ready." % bucket)
    else:
        print("ERROR: Failed to create bucket '%s'" % bucket, file=sys.stderr)
        sys.exit(1)


def cmd_delete(args):
    """Delete a file from a bucket"""
    config = load_config()
    api_key = load_credentials()
    bucket = args.bucket or config["bucket"]
    key = args.key

    client = TelnyxS3Client(api_key, config["region"])

    print("\nDeleting '%s' from bucket '%s'" % (key, bucket))

    if client.delete_object(bucket, key):
        print("Deleted: %s" % key)
    else:
        print("ERROR: Failed to delete '%s'" % key, file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Telnyx Embeddings - Index & Bucket Management"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # upload
    p_upload = subparsers.add_parser("upload", help="Upload file(s) to bucket")
    p_upload.add_argument("path", help="File or directory path to upload")
    p_upload.add_argument("--bucket", "-b", help="Target bucket name")
    p_upload.add_argument("--key", "-k", help="Override S3 key (single file only)")
    p_upload.add_argument("--pattern", "-p", help="Glob pattern for directory upload (e.g., '*.md')")

    # embed
    p_embed = subparsers.add_parser("embed", help="Trigger embedding on a bucket")
    p_embed.add_argument("--bucket", "-b", help="Bucket name")

    # status
    p_status = subparsers.add_parser("status", help="Check embedding task status")
    p_status.add_argument("task_id", help="Embedding task ID")

    # list
    p_list = subparsers.add_parser("list", help="List files in a bucket")
    p_list.add_argument("--bucket", "-b", help="Bucket name")
    p_list.add_argument("--prefix", help="Filter by prefix")
    p_list.add_argument("--embeddings", "-e", action="store_true",
                        help="Show embedding status instead of S3 listing")

    # buckets
    subparsers.add_parser("buckets", help="List all embedded buckets")

    # create-bucket
    p_create = subparsers.add_parser("create-bucket", help="Create a new bucket")
    p_create.add_argument("bucket_name", help="Name for the new bucket")
    p_create.add_argument("--region", "-r", help="Storage region (default: from config)")

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a file from a bucket")
    p_delete.add_argument("key", help="S3 key (filename) to delete")
    p_delete.add_argument("--bucket", "-b", help="Bucket name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "upload": cmd_upload,
        "embed": cmd_embed,
        "status": cmd_status,
        "list": cmd_list,
        "buckets": cmd_buckets,
        "create-bucket": cmd_create_bucket,
        "delete": cmd_delete,
    }

    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)


if __name__ == "__main__":
    main()
