import os
import sys
import json
import mimetypes
import urllib.request
import urllib.error
import argparse
import uuid
import base64

def generate_image(
    prompt,
    model=None,
    size=None,
    watermark=None,
    optimize_prompt_options=None,
    tools=None,
    output_format=None,
    sequential_image_generation=None,
    download_dir=None,
    image=None,
    response_format=None
):
    """
    Generates an image using the Volcengine Seedream API.
    
    Args:
        prompt (str): The text description of the image to generate. Required.
        model (str): The target model endpoint ID (e.g., ep-xxxx). Required.
        size (str, optional): Target image size. Can be a resolution class (e.g., '2K', '3K') 
                              or explicit dimensions (e.g., '2048x2048'). Defaults to None.
        watermark (bool, optional): Whether to add an AI watermark. Defaults to False.
        optimize_prompt_options (dict, optional): Options to optimize the prompt (e.g., {"mode": "standard"}). Defaults to None.
        tools (list, optional): A list of tools for the model to use (e.g., [{"type": "web_search"}]).
        output_format (str, optional): Output image format (e.g., 'png', 'jpeg', 'webp'). Defaults to None.
        sequential_image_generation (str, optional): Sequential image generation strategy (e.g., 'auto'). Defaults to None.
        image (str | list[str], optional): Local image path or image path list for I2I. Defaults to None.


        
    Returns:
        dict: The JSON response dictionary.
        
        Successful Return Value Format:
        {
          "data": [
            {
              "url": "https://...",
              "size": "2048x2048" # Included depending on the model capability
            }
          ],
          "usage": { 
              "generated_images": 1,
              ...
          }
        }
        
        Failure Return Value Format:
        {
          "error": "<Error Code or Details>",
          "message": "<Optional detailed message from server>"
        }
    """
    # Retrieve API key
    key = os.environ.get("SEEDREAM_API_KEY")
    if not key:
        err = {"error": "Require SEEDREAM_API_KEY in environment"}
        print("[seedream] error:", json.dumps(err, ensure_ascii=False))
        return err
    
    model_id = model or "doubao-seedream-5-0-260128"

    headers = {
        "Authorization": f"Bearer {key}",
    }

    image_input = [] if image is None else (image if isinstance(image, list) else [image])
    print("[seedream] generate_image input:", json.dumps({
        "prompt": prompt,
        "model": model,
        "size": size,
        "watermark": watermark,
        "optimize_prompt_options": optimize_prompt_options,
        "tools": tools,
        "output_format": output_format,
        "sequential_image_generation": sequential_image_generation,
        "download_dir": download_dir,
        "image": image,
        "response_format": response_format
    }, ensure_ascii=False))

    # Use SEEDREAM_BASE_URL if provided, else use default generations endpoint
    url = os.environ.get("SEEDREAM_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3/images/generations")

    payload = {
        "model": model_id,
        "prompt": prompt,
        "watermark": watermark if watermark is not None else False
    }

    if size is not None:
        payload["size"] = size
    if optimize_prompt_options is not None:
        payload["optimize_prompt_options"] = optimize_prompt_options
    if tools is not None:
        payload["tools"] = tools
    if output_format is not None:
        payload["output_format"] = output_format
    if sequential_image_generation is not None:
        payload["sequential_image_generation"] = sequential_image_generation
    if response_format is not None:
        payload["response_format"] = response_format

    # Convert local image path(s) to base64 data URIs for I2I.
    if len(image_input) > 0:
        image_data_uris = []
        for img_path in image_input:
            if not os.path.exists(img_path):
                err = {"error": f"Image not found: {img_path}"}
                print("[seedream] error:", json.dumps(err, ensure_ascii=False))
                return err

            mime, _ = mimetypes.guess_type(img_path)
            if not mime:
                mime = "image/jpeg"

            with open(img_path, "rb") as f:
                img_data = f.read()

            b64_data = base64.b64encode(img_data).decode("utf-8")
            data_uri = f"data:{mime};base64,{b64_data}"
            image_data_uris.append(data_uri)
            print(f"[seedream] loaded image: {img_path} ({len(img_data)} bytes, mime: {mime})")

        # Support single image (string) or multiple images (array)
        if len(image_data_uris) == 1:
            payload["image"] = image_data_uris[0]
        else:
            payload["image"] = image_data_uris

        print(f"[seedream] total images: {len(image_data_uris)}")

    headers["Content-Type"] = "application/json"
    print("[seedream] request:", json.dumps({
        "url": url,
        "headers": {k: ("<redacted>" if k.lower() == "authorization" else v) for k, v in headers.items()},
        "payload": {**payload, "image": "<base64_data_redacted>" if "image" in payload else None}
    }, ensure_ascii=False))

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    input_params_for_return = payload

    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            print("[seedream] response:", json.dumps(res_json, ensure_ascii=False))

            # If successful, handle downloads if download_dir is provided
            if "data" in res_json:
                res_json["input_params"] = input_params_for_return

                if download_dir:
                    save_path = download_dir
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    output_format_used = input_params_for_return.get("output_format", "jpeg")

                    for item in res_json["data"]:
                        if "url" in item:
                            try:
                                file_ext = ".png" if output_format_used == "png" else ".jpeg"
                                filename = f"image_{int(res_json.get('created', 0))}_{res_json['data'].index(item)}{file_ext}"
                                local_file_path = os.path.join(save_path, filename)

                                urllib.request.urlretrieve(item["url"], local_file_path)
                                item["local_path"] = local_file_path
                            except Exception as download_err:
                                item["local_path_error"] = str(download_err)

            print("[seedream] output:", json.dumps(res_json, ensure_ascii=False))
            return res_json
    except urllib.error.HTTPError as e:
        err = {"error": e.code, "message": e.read().decode("utf-8")}
        print("[seedream] error:", json.dumps(err, ensure_ascii=False))
        return err
    except Exception as e:
        err = {"error": str(e)}
        print("[seedream] error:", json.dumps(err, ensure_ascii=False))
        return err

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seedream Image Generation API Wrapper")
    parser.add_argument("--prompt", type=str, required=True, help="Image generation prompt")
    parser.add_argument("--model", type=str, help="Model endpoint id")
    parser.add_argument("--size", type=str, help="Image size")
    parser.add_argument("--watermark", type=str, help="Add watermark (true/false)")
    parser.add_argument("--optimize_prompt_options", type=str, help="JSON string for prompt optimization options")
    parser.add_argument("--tools", type=str, help="JSON string for tools list, e.g. '[{\"type\": \"web_search\"}]'")
    parser.add_argument("--output_format", type=str, help="Output image format (png, jpeg)")
    parser.add_argument("--sequential_image_generation", type=str, help="Sequential image generation mode (e.g., 'auto')")
    parser.add_argument("--download_dir", type=str, help="Directory to save images")
    parser.add_argument("--image", type=str, help="Local image path or JSON string list of local image paths, e.g. '/a.png' or '[\"/a.png\",\"/b.jpg\"]'")
    parser.add_argument("--response_format", type=str, help="Response format for edits (url or b64_json)")
    args = parser.parse_args()
    
    watermark_val = None
    if args.watermark is not None:
        watermark_val = args.watermark.lower() == "true"
        
    optimize_prompt_val = None
    if args.optimize_prompt_options is not None:
        try:
            optimize_prompt_val = json.loads(args.optimize_prompt_options)
        except json.JSONDecodeError:
            print("Error: --optimize_prompt_options must be a valid JSON string.")
            sys.exit(1)

    tools_val = None
    if args.tools is not None:
        try:
            tools_val = json.loads(args.tools)
        except json.JSONDecodeError:
            print("Error: --tools must be a valid JSON string.")
            sys.exit(1)

    image_val = None
    if args.image is not None:
        if args.image.strip().startswith("["):
            try:
                image_val = json.loads(args.image)
                if not isinstance(image_val, list):
                    print("Error: --image must be a local path or a JSON list of paths.")
                    sys.exit(1)
            except json.JSONDecodeError:
                print("Error: --image must be a local path or a valid JSON string list.")
                sys.exit(1)
        else:
            image_val = args.image

    res = generate_image(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        watermark=watermark_val,
        optimize_prompt_options=optimize_prompt_val,
        tools=tools_val,
        output_format=args.output_format,
        sequential_image_generation=args.sequential_image_generation,
        download_dir=args.download_dir,
        image=image_val,
        response_format=args.response_format
    )
    print(json.dumps(res, indent=2))
