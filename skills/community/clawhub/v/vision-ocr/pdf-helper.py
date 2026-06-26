#!/usr/bin/env python3

import argparse
import json
import sys

import fitz


def pdf_to_images(input_path, output_dir):
    doc = fitz.open(input_path)
    images = []

    try:
        page_count = len(doc)
        for page_num in range(page_count):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            output_path = f"{output_dir}/page_{page_num + 1:03d}.png"
            pix.save(output_path)
            images.append(output_path)
    finally:
        doc.close()

    return {
        "images": images,
        "pageCount": len(images)
    }


def pdf_info(input_path):
    doc = fitz.open(input_path)

    try:
        mediabox = doc[0].rect
        return {
            "pages": len(doc),
            "width": mediabox.width,
            "height": mediabox.height,
        }
    finally:
        doc.close()


def optimize_image(input_path, output_path, max_pixels, max_side, jpg_quality):
    pix = fitz.Pixmap(input_path)

    try:
        if pix.colorspace is None or pix.colorspace.n != 3 or pix.alpha:
            pix = fitz.Pixmap(fitz.csRGB, pix)

        original_width = pix.width
        original_height = pix.height
        shrink_steps = 0

        while (
            (pix.width * pix.height > max_pixels or max(pix.width, pix.height) > max_side)
            and min(pix.width, pix.height) > 1
        ):
            pix.shrink(1)
            shrink_steps += 1

        pix.save(output_path, jpg_quality=jpg_quality)

        return {
            "outputPath": output_path,
            "originalWidth": original_width,
            "originalHeight": original_height,
            "width": pix.width,
            "height": pix.height,
            "shrinkSteps": shrink_steps,
        }
    finally:
        pix = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["pdf-to-images", "pdf-info", "optimize-image"])
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--output")
    parser.add_argument("--max-pixels", type=int, default=4000000)
    parser.add_argument("--max-side", type=int, default=1800)
    parser.add_argument("--jpg-quality", type=int, default=85)
    args = parser.parse_args()

    if args.mode == "pdf-to-images":
        if not args.output_dir:
            raise ValueError("--output-dir is required for pdf-to-images")
        result = pdf_to_images(args.input, args.output_dir)
    elif args.mode == "pdf-info":
        result = pdf_info(args.input)
    else:
        if not args.output:
            raise ValueError("--output is required for optimize-image")
        result = optimize_image(args.input, args.output, args.max_pixels, args.max_side, args.jpg_quality)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)