import os
import sys
import re
import base64
import argparse
from openai import OpenAI


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def extract_base64_from_content(content):
    """
    从API返回的内容中提取Base64图像数据。
    支持两种格式：
    1. 列表格式（包含 type='image_url' 的元素）
    2. 字符串格式（Markdown图片语法）
    """
    if isinstance(content, list):
        for part in content:
            if hasattr(part, 'type') and part.type == 'image_url':
                if hasattr(part, 'image_url') and hasattr(part.image_url, 'url'):
                    url = part.image_url.url
                    # 如果URL已经包含 data:image/...;base64, 则提取逗号后面的部分
                    if ',' in url:
                        return url.split(',', 1)[1]
                    else:
                        return url
    elif isinstance(content, str):
        # 匹配 Markdown 图片语法： ![alt](data:image/...;base64,base64data)
        pattern = r'!\[.*?\]\(data:image/(?:png|jpeg|jpg);base64,([^")\s]+)\)'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def generate_image_with_text(base_url, model, base_image_path, text_to_add, output_path, prompt_template):
    if not os.path.exists(base_image_path):
        print(f"Error: Base image not found at {base_image_path}", file=sys.stderr)
        sys.exit(1)

    print("Initializing OpenAI client...")
    client = OpenAI(
        api_key=get_config_value("qdd"),
        base_url=base_url
    )

    print(f"Encoding base image from {base_image_path}...")
    base64_image = encode_image_to_base64(base_image_path)

    final_prompt = prompt_template.format(text_to_add=text_to_add)
    print("Using provided prompt...", final_prompt)

    print("Sending request to the image generation API...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": final_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2048,
            timeout=180,
            extra_body={
                "modalities": ["text", "image"]
            }
        )

        print("API response received.")
        # 保存完整响应内容到日志文件（便于调试）
        with open("api_response_content.log", "w", encoding="utf-8") as f:
            f.write(str(response))

        image_base64 = None
        if response.choices and response.choices[0].message:
            content = response.choices[0].message.content
            # 尝试从内容中提取Base64图像数据
            image_base64 = extract_base64_from_content(content)

        if image_base64:
            print(f"Image data found. Saving to {output_path}...")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(image_base64))
            print(f"Successfully saved image to {output_path}")
        else:
            print("Error: No image data found in API response.", file=sys.stderr)
            print("Full response content:", file=sys.stderr)
            print(response.choices[0].message.content if response.choices else "No choices", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate a cover image via AI.")
    parser.add_argument("--base-url", required=True, help="The API base URL.")
    parser.add_argument("--model", required=True, help="The model ID.")
    parser.add_argument("--image", required=True, help="Path to the base image.")
    parser.add_argument("--text", required=True, help="Text to add to the image.")
    parser.add_argument("--output", required=True, help="Path to save the output image.")
    parser.add_argument("--prompt",default="请在这张图片上，移除所有旧的文字，然后用醒目的、专业的风格加上新文字：'{text_to_add}',请直接输出最终处理完成的、无水印的高清图片。", required=True, help="The prompt template string.")

    args = parser.parse_args()

    generate_image_with_text(
        base_url=args.base_url,
        model=args.model,
        base_image_path=args.image,
        text_to_add=args.text,
        output_path=args.output,
        prompt_template=args.prompt
    )


if __name__ == "__main__":
    main()