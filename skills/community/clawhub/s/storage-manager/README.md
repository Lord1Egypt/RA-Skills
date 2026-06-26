# Storage Manager Skill

## Complete Storage Management Solution

This skill provides comprehensive storage management capabilities using Feishu Bitable API.

## Features

### 1. Item Storage (add_storage_item)
- Store items with location information
- Upload and attach images
- Automatic Feishu Bitable integration

### 2. Item Retrieval (search_storage_item)
- Fast search by item name
- Fuzzy matching support
- Location display with images

### 3. Location Update (update_storage_location)
- Update item locations
- Preserve image attachments
- Maintain data integrity

## Installation

```bash
# After publishing, install with:
clawhub install storage-manager
```

## Usage Examples

```python
# Python API
from storage_manager import FeishuStorageManager
manager = FeishuStorageManager()
manager.add_storage_item("Passport", "Backpack inner layer", "passport.jpg")
```

## Configuration

Set environment variables:
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET` 
- `FEISHU_BITABLE_TOKEN`
- `FEISHU_TABLE_ID`

## Technical Details

- Built with Python 3.6+
- Uses Feishu Open Platform API
- Full error handling
- Comprehensive testing