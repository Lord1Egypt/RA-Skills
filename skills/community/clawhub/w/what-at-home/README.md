# 🏠 What At Home

A simple solution for: *"What's in my house?"* and *"Where did I put that thing?"*

Stop wondering what's in your home. Record everything you own, find anything instantly.

**Perfect for:** Home inventory, item tracking, moving preparation, decluttering, knowing what you have

## Features Overview

| Feature | Description | Example |
|---------|-------------|---------|
| Initialize Suite | Create a new property and define rooms | `Set up a suite called Studio with living room, bedroom` |
| Add Room | Add rooms to an existing suite | `Add a room called Kitchen to Studio` |
| Add Furniture | Add furniture to a room | `Living room has a TV cabinet` |
| Add Item | Record item storage location | `Put the remote in the living room TV cabinet, quantity 2` |
| Query Item | Quickly locate item position | `Where is my remote?` |
| View Suite | List all items in a property | `View Studio` |
| Move Item | Change item storage location | `Move the remote to the bedroom wardrobe` |
| Delete Item | Remove item record | `Delete remote` |
| Search Item | Fuzzy search items | `Search remote` |
| Backup | Backup data to file | `Backup data` |
| List Backups | List all backups | `List backups` |
| Restore | Restore from backup | `Restore 20260325_143000` |
| Export | Export data (text/JSON) | `Export data` |

## Data Structure

```
🏠 Suite
  └── 📦 Room
      └── 🪑 Furniture
          └── 📦 Item
```

## Item Properties

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | ✅ | Unique identifier |
| name | string | ✅ | Item name |
| quantity | number | ✅ | Quantity, default 1 |
| addedAt | datetime | ✅ | Placement time |
| updatedAt | datetime | ✅ | Last update time |
| note | string | ❌ | Notes |

## Timestamp Fields (All Levels)

| Level | Fields | Description |
|-------|--------|-------------|
| Suite | createdAt, updatedAt | Creation/update time |
| Room | createdAt, updatedAt | Creation/update time |
| Furniture | createdAt, updatedAt | Creation/update time |
| Item | addedAt, updatedAt | Placement/update time |

## Quick Start

### 1. Initialize Your First Suite

```
Set up a suite called Studio with living room, bedroom, kitchen
```

The system will automatically create the suite and rooms.

### 2. Add Furniture

```
Living room has a TV cabinet
Bedroom has a wardrobe
Kitchen has a wall cabinet
```

### 3. Add Items

```
Put the spare remote in the living room TV cabinet
Put the winter comforter in the bedroom wardrobe, quantity 2
I put the keys in the living room coffee table drawer
```

### 4. Query Items

```
Where is my remote?
View Studio
```

### 5. Move Items

```
Move the remote to the bedroom wardrobe
```

### 6. Search Items

```
Search remote
Search phone
```

### 7. Delete Items

```
Delete remote
```

### 8. Backup & Restore

```
Backup data
List backups
Restore 20260325_143000
```

### 9. Export

```
Export data
Export JSON
```

## Complete Example

```bash
# Step 1: Initialize suite
Set up a suite called Studio with living room, bedroom, study

# Step 2: Add furniture
Living room has a TV cabinet
Living room has a coffee table
Bedroom has a large wardrobe
Study has a bookcase

# Step 3: Add items
Put the game controller in the living room TV cabinet
Put the spare keys in the living room coffee table drawer
Put the thick winter comforter in the bedroom large wardrobe, quantity 2

# Step 4: Query
Where is my game controller?
View Studio
```

## Command Format Reference

### Initialize Suite
| Format | Example |
|--------|---------|
| `Set up a suite called {name}, with {room1}, {room2}...` | `Set up a suite called Old House, with living room, master bedroom` |
| `Add suite: {name}, containing {room1} and {room2}` | `Add suite: Studio, containing living room and kitchen` |

### Add Room
| Format | Example |
|--------|---------|
| `Add a room called {room} to {suite}` | `Add a room called Storage to Studio` |
| `{suite} add {room}` | `Studio add balcony` |

### Add Furniture
| Format | Example |
|--------|---------|
| `{room} has a {furniture}` | `Living room has a TV cabinet` |
| `{room} has a {quantity}{furniture}` | `Master bedroom has a large wardrobe` |

### Add Item
| Format | Example |
|--------|---------|
| `Put {item} in {room}{furniture}` | `Put remote in living room TV cabinet` |
| `Put {item} in {room}{furniture}, quantity {quantity}` | `Put comforter in bedroom wardrobe, quantity 2` |

### Query
| Format | Example |
|--------|---------|
| `Where is my {item}?` | `Where are my keys?` |
| `{item} location` | `Remote location` |
| `View {suite}` | `View Studio` |

### Search
| Format | Example |
|--------|---------|
| `Search {keyword}` | `Search remote` |
| `Find {keyword}` | `Find phone` |

### Move
| Format | Example |
|--------|---------|
| `Move {item} to {room}{furniture}` | `Move remote to bedroom wardrobe` |
| `Move {item} to {room}-{furniture}` | `Move keys to living room-coffee table` |

### Delete
| Format | Example |
|--------|---------|
| `Delete {item}` | `Delete remote` |
| `Throw away {item}` | `Throw away old newspapers` |

### Backup & Restore
| Format | Example |
|--------|---------|
| `Backup data` | - |
| `List backups` | - |
| `Restore {timestamp}` | `Restore 20260325_143000` |

### Export
| Format | Example |
|--------|---------|
| `Export data` | - |
| `Export JSON` | - |

## Technical Information

- **Data Storage**: `{workspace}/data/home_storage.json` (default: `~/.openclaw/workspace/data/home_storage.json`)
- **Backup Directory**: `{workspace}/data/backups/`
- **Data Format**: JSON
- **Dependency**: Python 3

## Version

- v2.1.0 (2026-03-25) - Optimized code, added search/backup/export features, timestamps
- v2.0.0 (2026-03-24) - Added natural language add features
- v1.0.0 (2026-03-23) - Initial release

---

*Make life more organized, let items find their place* 🐾