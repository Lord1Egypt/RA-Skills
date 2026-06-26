#!/usr/bin/env python3

import subprocess
import json
import os
from pathlib import Path

# --- Config (from Skill's references/properties.md) ---
MASTER_SHEET_ID = "11u3rE6sTojZfHuO7-38MJO5agyJ7mndo-7OvdOHoD2E"
LONGUEUIL_CONTROL_ID = "1698_UaKYY1m0X7Yujo7oDjLnYcq6O2k6_3w59p5rN0g"

# Google Drive Folder IDs
FOLDER_GAUVIN = "1APxrzAqXMRUe6ZGvyIDKIqK7gzvsD5tX" # Quebec (Gauvin)
FOLDER_LEVIS = "1AvpX_M1Lr36d86Oqcgh4-JNfbo-sNsbl"   # Levis (249 Champagnat)
FOLDER_LONGUEUIL_RECEIPTS = "1P6a06wsVSGSpcHYDgnugh2TcVhSolbBr" # Longueuil / Receipts
FOLDER_GENERAL = "1E7jo9EdX0LdS51Yb-M4OUf39sNUHz_Ab" # General

def get_folder_id(property_name: str) -> str:
    if "gauvin" in property_name.lower() or "quebec" in property_name.lower():
        return FOLDER_GAUVIN
    if "levis" in property_name.lower() or "champagnat" in property_name.lower():
        return FOLDER_LEVIS
    if "longueuil" in property_name.lower() or "goyette" in property_name.lower():
        return FOLDER_LONGUEUIL_RECEIPTS
    if "general" in property_name.lower():
        return FOLDER_GENERAL
    raise ValueError(f"Unknown property name: {property_name}")

def get_sheet_id(property_name: str) -> str:
    if "longueuil" in property_name.lower() or "goyette" in property_name.lower():
        return LONGUEUIL_CONTROL_ID # Longueuil uses its own control sheet
    return MASTER_SHEET_ID # Other properties use the master sheet

def get_sheet_tab_name(property_name: str) -> str:
    if "gauvin" in property_name.lower() or "quebec" in property_name.lower():
        return "'Quebec (Gauvin)'"
    if "levis" in property_name.lower() or "champagnat" in property_name.lower():
        return "'Levis (249 Champagnat)'"
    if "longueuil" in property_name.lower() or "goyette" in property_name.lower():
        return "'Longueuil (168 Goyette)'"
    if "general" in property_name.lower():
        return "'General / Personal Business'"
    raise ValueError(f"Unknown property name for sheet tab: {property_name}")


def get_next_index(sheet_id: str, tab_name: str) -> int:
    cmd = ["gog", "sheets", "get", sheet_id, f"{tab_name}!A:A", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout).get("values", [])
    
    max_index = 0
    # Skip header (first row) and look for numbers
    for row in data[1:]:
        if row and str(row[0]).strip().isdigit():
            max_index = max(max_index, int(row[0].strip()))
    return max_index + 1


async def handle_receipt_upload(file_id: str, original_file_name: str, property_name: str, excel_index: str = None, desired_file_name: str = None) -> dict:
    try:
        # 1. Get folder ID
        target_folder_id = get_folder_id(property_name)
        
        # 2. Determine final file name
        file_extension = Path(original_file_name).suffix
        if desired_file_name:
            final_name = desired_file_name
        elif excel_index:
            final_name = f"{excel_index}{file_extension}"
        else:
            return {"success": False, "error": "Cannot determine final file name. Please provide excel_index or desired_file_name."}

        # 3. Move and rename file in Drive
        # gog drive move <fileId> --parent <newParentId>
        subprocess.run(["gog", "drive", "move", file_id, "--parent", target_folder_id], capture_output=True, text=True, check=True)
        # gog drive rename <fileId> <newName>
        subprocess.run(["gog", "drive", "rename", file_id, final_name], capture_output=True, text=True, check=True)

        # 4. Get webViewLink (need to search again by ID as rename might change some metadata)
        cmd_get_link = ["gog", "drive", "get", file_id, "--json", "--select", "file(webViewLink)"]
        result_link = subprocess.run(cmd_get_link, capture_output=True, text=True, check=True)
        file_link = json.loads(result_link.stdout).get("file", {}).get("webViewLink", "")

        # 5. Update Excel sheet
        if excel_index:
            sheet_id = get_sheet_id(property_name)
            tab_name = get_sheet_tab_name(property_name)
            
            # Find the row for the given index
            # Assuming index is in column A and data starts from row 2
            cmd_get_all_data = ["gog", "sheets", "get", sheet_id, f"{tab_name}!A2:A100", "--json"]
            all_data_result = subprocess.run(cmd_get_all_data, capture_output=True, text=True, check=True)
            all_data = json.loads(all_data_result.stdout).get("values", [])
            
            target_row_number = -1
            for i, row in enumerate(all_data):
                if row and str(row[0]).strip() == str(excel_index):
                    target_row_number = i + 2 # +2 because A2 is index 0 in the list
                    break
            
            if target_row_number != -1:
                # Update G column (7th column) with the link
                update_range = f"{tab_name}!G{target_row_number}"
                cmd_update_sheet = ["gog", "sheets", "update", sheet_id, update_range, file_link, "--json", "--input=USER_ENTERED"]
                subprocess.run(cmd_update_sheet, capture_output=True, text=True, check=True)
                return {"success": True, "file_link": file_link, "message": f"File {final_name} processed and linked in Excel."}
            else:
                return {"success": False, "error": f"Index {excel_index} not found in Excel tab {tab_name}."}
        else:
            return {"success": True, "file_link": file_link, "message": f"File {final_name} processed and uploaded. No Excel link update as no index provided."}

    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"Command failed: {e.cmd}, Output: {e.stderr}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Example usage (for testing, not part of the Skill's direct invocation)
# if __name__ == "__main__":
#     # This part would be called by OpenClaw after capturing a file upload
#     # You'd get file_id, original_file_name from the message context
#     # property_name, excel_index, desired_file_name would be extracted from user's prompt
#     # For manual testing:
#     import asyncio
#     asyncio.run(handle_receipt_upload(
#         file_id="YOUR_UPLOADED_FILE_ID",
#         original_file_name="my_receipt.pdf",
#         property_name="Quebec",
#         excel_index="11",
#         # desired_file_name="11.pdf" # Optional
#     ))
