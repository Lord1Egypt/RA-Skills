#!/usr/bin/env python3
"""Generate images using Stability AI models (Stable Image Ultra / SD 3.5 Large) via AWS Bedrock."""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

MODELS = {
    "ultra": "stability.stable-image-ultra-v1:1",
    "sd35": "stability.sd3-5-large-v1:0",
}

MODEL_LABELS = {
    "ultra": "Stable Image Ultra",
    "sd35": "Stable Diffusion 3.5 Large",
}

# Stability AI models on Bedrock are only available in us-west-2
DEFAULT_REGION = "us-west-2"


def invoke_via_bearer_token(args, model_id, body):
    """Call Bedrock invoke-model using Bearer Token."""
    token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "")
    region = args.region
    encoded_model = urllib.parse.quote(model_id, safe="")
    url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{encoded_model}/invoke"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"Error: Bedrock API {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


def invoke_via_boto3(args, model_id, body):
    """Call Bedrock invoke-model using boto3."""
    try:
        import boto3
    except ImportError:
        print("Error: boto3 not installed. Run: pip install boto3", file=sys.stderr)
        sys.exit(1)

    kwargs = {"region_name": args.region}

    if args.access_key and args.secret_key:
        kwargs["aws_access_key_id"] = args.access_key
        kwargs["aws_secret_access_key"] = args.secret_key
        if args.session_token:
            kwargs["aws_session_token"] = args.session_token
        print("  Auth: explicit keys")
        client = boto3.client("bedrock-runtime", **kwargs)
    elif args.profile:
        session = boto3.Session(profile_name=args.profile, region_name=args.region)
        print(f"  Auth: profile ({args.profile})")
        client = session.client("bedrock-runtime")
    else:
        print("  Auth: boto3 auto-detect")
        client = boto3.client("bedrock-runtime", **kwargs)

    response = client.invoke_model(modelId=model_id, body=body)
    return json.loads(response["body"].read())


def detect_auth_method(args):
    """Determine which auth method to use."""
    if args.access_key and args.secret_key:
        return "boto3"
    if args.profile:
        return "boto3"
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return "bearer"
    try:
        import boto3
        session = boto3.Session(region_name=args.region)
        creds = session.get_credentials()
        if creds:
            return "boto3"
    except Exception:
        pass
    return None


def main():
    # Need urllib.parse for URL encoding
    import urllib.parse

    parser = argparse.ArgumentParser(
        description="Generate images with Stability AI models on AWS Bedrock (Ultra / SD 3.5 Large)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Models:
  ultra   Stable Image Ultra — highest quality, photorealistic (default)
  sd35    Stable Diffusion 3.5 Large — creative diversity, prompt adherence

AWS auth methods (auto-detected):
  AWS_BEARER_TOKEN_BEDROCK      Bearer token (OpenClaw managed)
  --access-key + --secret-key   Direct IAM credentials
  --profile / AWS_PROFILE       Named profile (~/.aws/credentials)
  AWS_ACCESS_KEY_ID env var     Environment variables
  ~/.aws/credentials            Shared credentials file
  IAM instance role             EC2/ECS/Lambda
  AWS SSO                       aws sso login

Note: Stability AI models on Bedrock are only available in us-west-2 (Oregon).
""")
    parser.add_argument("prompt", help="Text description of the image (max 10,000 chars)")
    parser.add_argument("-o", "--output", default="output.png", help="Output path (default: output.png)")
    parser.add_argument("-m", "--model", choices=["ultra", "sd35"], default="ultra",
                        help="Model: ultra (default) or sd35")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of images 1-5 (default: 1)")
    parser.add_argument("--negative", help="Negative prompt (what to avoid)")
    parser.add_argument("--aspect-ratio", dest="aspect_ratio", default=None,
                        help="Aspect ratio: 1:1(default), 16:9, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")

    # AWS auth
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"AWS region (default: {DEFAULT_REGION}, required for Stability AI)")
    parser.add_argument("--profile", default=None, help="AWS named profile")
    parser.add_argument("--access-key", default=None, help="AWS Access Key ID")
    parser.add_argument("--secret-key", default=None, help="AWS Secret Access Key")
    parser.add_argument("--session-token", default=None, help="AWS Session Token")
    parser.add_argument("--bearer-token", default=None, help="Bearer token (overrides env)")

    args = parser.parse_args()

    if args.bearer_token:
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = args.bearer_token

    if len(args.prompt) > 10000:
        print(f"Error: prompt exceeds 10,000 chars ({len(args.prompt)})", file=sys.stderr)
        sys.exit(1)

    method = detect_auth_method(args)
    if not method:
        print("Error: No AWS credentials found. Options:", file=sys.stderr)
        print("  1. AWS_BEARER_TOKEN_BEDROCK env var", file=sys.stderr)
        print("  2. AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY env vars", file=sys.stderr)
        print("  3. ~/.aws/credentials file", file=sys.stderr)
        print("  4. --profile <name>", file=sys.stderr)
        print("  5. --access-key + --secret-key", file=sys.stderr)
        print("  6. --bearer-token <token>", file=sys.stderr)
        sys.exit(1)

    model_id = MODELS[args.model]
    model_label = MODEL_LABELS[args.model]

    # Build request
    body_dict = {"prompt": args.prompt}

    # Aspect ratio
    if args.aspect_ratio:
        body_dict["aspect_ratio"] = args.aspect_ratio

    # Negative prompt
    if args.negative:
        body_dict["negative_prompt"] = args.negative

    # Seed
    if args.seed is not None:
        body_dict["seed"] = args.seed

    # Output format — always PNG for maximum quality
    body_dict["output_format"] = "png"

    body = json.dumps(body_dict)

    print(f"Generating with {model_label} (region: {args.region})...")

    try:
        if method == "bearer":
            print("  Auth: Bearer token")
            result = invoke_via_bearer_token(args, model_id, body)
        else:
            result = invoke_via_boto3(args, model_id, body)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Check for content filter
    finish_reasons = result.get("finish_reasons", [])
    if finish_reasons and finish_reasons[0] is not None:
        print(f"Error: Content filtered — {finish_reasons[0]}", file=sys.stderr)
        sys.exit(1)

    if "images" not in result or not result["images"]:
        print(f"Error: No images returned. Response: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)

    # Save images
    output_dir = os.path.dirname(args.output) or "."
    base_name = os.path.splitext(os.path.basename(args.output))[0]
    ext = os.path.splitext(args.output)[1] or ".png"
    os.makedirs(output_dir, exist_ok=True)

    paths = []
    images = result["images"]
    seeds = result.get("seeds", [])

    for i, img_b64 in enumerate(images):
        if len(images) == 1:
            path = args.output
        else:
            path = os.path.join(output_dir, f"{base_name}_{i+1}{ext}")

        with open(path, "wb") as f:
            f.write(base64.b64decode(img_b64))

        size_kb = os.path.getsize(path) / 1024
        seed_info = f", seed={seeds[i]}" if i < len(seeds) else ""
        print(f"  [{i+1}/{len(images)}] {path} ({size_kb:.0f} KB{seed_info})")
        paths.append(path)

    print(f"Done. {len(paths)} image(s) saved via {model_label}.")
    return paths


if __name__ == "__main__":
    main()
