#!/usr/bin/env python3
"""
Post to Facebook Page using Graph API.
Usage:
  Upload photo: python3 post_fb.py upload-photo <PAGE_ID> <TOKEN> <IMAGE_PATH>
  Post: python3 post_fb.py post <PAGE_ID> <TOKEN> "<MESSAGE>" [<PHOTO_ID>]
"""

import sys
import json
import requests

API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def upload_photo(page_id, token, image_path):
    """Upload photo to page (unpublished)."""
    url = f"{BASE_URL}/{page_id}/photos"
    
    try:
        with open(image_path, "rb") as img:
            files = {"source": img}
            data = {
                "published": "false",
                "access_token": token
            }
            response = requests.post(url, files=files, data=data, timeout=60)
        
        result = response.json()
        
        if "error" in result:
            return {"error": result["error"].get("message", "Unknown error"), 
                    "code": result["error"].get("code", 0)}
        
        return {
            "success": True,
            "photo_id": result.get("id"),
            "post_id": result.get("post_id")
        }
        
    except FileNotFoundError:
        return {"error": f"Image file not found: {image_path}"}
    except Exception as e:
        return {"error": str(e)}

def post_to_page(page_id, token, message, photo_id=None):
    """Post to page feed."""
    url = f"{BASE_URL}/{page_id}/feed"
    
    data = {
        "message": message,
        "access_token": token
    }
    
    # If photo_id provided, attach it
    if photo_id:
        data["attached_media"] = json.dumps([{"media_fbid": photo_id}])
    
    try:
        response = requests.post(url, data=data, timeout=60)
        result = response.json()
        
        if "error" in result:
            error_code = result["error"].get("code", 0)
            error_msg = result["error"].get("message", "Unknown error")
            return {"error": error_msg, "code": error_code}
        
        post_id = result.get("id", "")
        # Construct FB link from post_id (format: pageId_postId)
        fb_link = f"https://facebook.com/{post_id.replace('_', '/posts/')}"
        
        return {
            "success": True,
            "post_id": post_id,
            "link": fb_link
        }
        
    except Exception as e:
        return {"error": str(e)}

def get_page_info(page_id, token):
    """Get page info to verify token works."""
    url = f"{BASE_URL}/{page_id}"
    params = {
        "fields": "name,access_token",
        "access_token": token
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else None
    
    if command == "upload-photo":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: upload-photo <PAGE_ID> <TOKEN> <IMAGE_PATH>"}))
            sys.exit(1)
        result = upload_photo(sys.argv[2], sys.argv[3], sys.argv[4])
        
    elif command == "post":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: post <PAGE_ID> <TOKEN> '<MESSAGE>' [<PHOTO_ID>]"}))
            sys.exit(1)
        photo_id = sys.argv[5] if len(sys.argv) > 5 else None
        result = post_to_page(sys.argv[2], sys.argv[3], sys.argv[4], photo_id)
        
    elif command == "verify":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: verify <PAGE_ID> <TOKEN>"}))
            sys.exit(1)
        result = get_page_info(sys.argv[2], sys.argv[3])
        
    else:
        print(json.dumps({
            "error": "Unknown command",
            "usage": "upload-photo | post | verify"
        }))
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False))
