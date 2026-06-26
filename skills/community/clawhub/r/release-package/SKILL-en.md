---
name: Storage Manager
description: Feishu Bitable Storage Manager - Integrated tool for item storage, retrieval, and location updates
read_when:
  - Need to record item storage locations
  - Need to find item locations
  - Need to update item locations
  - Need to manage personal item storage
metadata: {"clawdbot":{"emoji":"🗃️","requires":{"bins":["python3"]}}}
allowed-tools: Bash(storage-manager:*)
---

# Storage Manager

## Overview

Intelligent storage management tool based on Feishu Bitable, integrating three core functions: item storage, retrieval, and location updates.

## Core Features

### 1. Item Storage Tool (add_storage_item)
- **Trigger:** User sends image with location description (e.g., "this goes under the bed")
- **Input parameters:**
  - item_name (String): Item name
  - location (String): Storage location
  - image_path (String, Optional): Local image path or URL
- **Logic:**
  a. If image exists, upload to Feishu to get file_token
  b. Call Feishu Bitable API to create new record
- **Return:** Success status and confirmation message

### 2. Item Retrieval Tool (search_storage_item)
- **Trigger:** User asks for item location (e.g., "Where is my passport?")
- **Input parameters:**
  - query_item (String): Item name to find
- **Logic:**
  a. Call Feishu Bitable search API
  b. Use fuzzy matching to find records containing query_item
- **Return:** Location and Image link of the item

### 3. Location Update Tool (update_storage_location)
- **Trigger:** User indicates item moved to new location (e.g., "I moved passport to backpack")
- **Input parameters:**
  - item_name (String): Item name to move
  - new_location (String): New storage location
- **Logic:**
  a. First call retrieval API to get record_id
  b. Call Feishu Bitable update API
- **Return:** Update success confirmation

## Configuration Requirements

### Feishu App Configuration
1. Create Feishu custom app
2. Enable permissions:
   - Bitable related permissions
   - File upload permissions
   - Document access permissions

### Environment Variables
- `FEISHU_APP_ID`: Feishu App ID
- `FEISHU_APP_SECRET`: Feishu App Secret
- `FEISHU_BITABLE_TOKEN`: Bitable app token
- `FEISHU_TABLE_ID`: Table ID

## Usage Examples

### Item Storage
```bash
# Record item location (with image)
storage-manager add "Medicine" "TV cabinet left drawer" --image="/path/to/image.jpg"

# Record item location (no image)
storage-manager add "Passport" "Backpack inner layer"
```

### Item Retrieval
```bash
# Find item location
storage-manager search "Passport"
```

### Location Update
```bash
# Update item location
storage-manager update "Passport" "Office desk drawer"
```

## Data Structure

### Bitable Field Structure
1. **Item_Name** - Text (Item name)
2. **Location** - Text (Storage location)
3. **Image** - Attachment (Item image)

## Technical Implementation

Based on Feishu Open Platform API, implementing complete item location management. Supports image upload, fuzzy search, location updates.