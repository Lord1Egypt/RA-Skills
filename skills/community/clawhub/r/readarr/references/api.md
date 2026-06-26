# Readarr API Reference

Base: `$READARR_URL/api/v1/`
Auth: Header `X-Api-Key: $READARR_KEY`

## Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/book` | List all books |
| GET | `/book/{id}` | Get book by ID |
| GET | `/book/lookup?term=` | Search GoodReads/ISBN |
| POST | `/book` | Add a book |
| PUT | `/book/{id}` | Update book |
| DELETE | `/book/{id}` | Remove book |

## Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/author` | List monitored authors |
| GET | `/author/{id}` | Get author |
| GET | `/author/lookup?term=` | Search for author |
| POST | `/author` | Add/monitor author |
| PUT | `/author/{id}` | Update author |
| DELETE | `/author/{id}` | Remove author |

## Queue & Wanted
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/queue` | Current download queue |
| DELETE | `/queue/{id}` | Remove from queue |
| GET | `/wanted/missing` | Monitored but missing |
| GET | `/wanted/cutoff` | Below quality cutoff |

## Commands
POST `/command` with `{"name": "<CommandName>"}`:
- `MissingBookSearch` — search for all missing books
- `RescanFolders` — rescan root folders
- `RefreshAuthor` — refresh author metadata (`{"name":"RefreshAuthor","authorId":N}`)
- `AuthorSearch` — search for specific author books (`{"name":"AuthorSearch","authorId":N}`)

## Config Endpoints
| Endpoint | Description |
|----------|-------------|
| GET `/qualityprofile` | List quality profiles |
| GET `/metadataprofile` | List metadata profiles |
| GET `/rootfolder` | List root folders |
| GET `/system/status` | System info + version |
| GET `/history?pageSize=20` | Recent activity |
| GET `/downloadclient` | Download clients |

## Pagination
Add `?page=1&pageSize=20&sortKey=title&sortDir=asc` to list endpoints.

## Add Book Payload Example
```json
{
  "foreignBookId": "12345678",
  "title": "The Player of Games",
  "monitored": true,
  "author": {
    "foreignAuthorId": "87654321",
    "authorName": "Iain M. Banks"
  },
  "qualityProfileId": 1,
  "metadataProfileId": 1,
  "rootFolderPath": "/books",
  "addOptions": {
    "searchForNewBook": true
  }
}
```
