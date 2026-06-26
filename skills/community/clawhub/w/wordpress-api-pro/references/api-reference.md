# WordPress REST API Reference

## Base URL

```
https://yoursite.com/wp-json/wp/v2/
```

## Common Endpoints

### Posts

- `GET /posts` - List posts
- `GET /posts/{id}` - Get single post
- `POST /posts` - Create post
- `POST /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Pages

- `GET /pages` - List pages
- `GET /pages/{id}` - Get single page
- `POST /pages` - Create page
- `POST /pages/{id}` - Update page

### Media

- `GET /media` - List media
- `POST /media` - Upload media
- `GET /media/{id}` - Get media item

### Users

- `GET /users` - List users (requires auth)
- `GET /users/{id}` - Get user

### Taxonomies

- `GET /categories` - List categories
- `GET /tags` - List tags

## Post Fields

- `title` - Post title (string or object: `{raw, rendered}`)
- `content` - Post content (string or object)
- `status` - Post status (`publish`, `draft`, `pending`, `private`)
- `author` - Author ID (integer)
- `featured_media` - Featured image ID (integer)
- `excerpt` - Post excerpt
- `meta` - Custom fields (object)
- `categories` - Array of category IDs
- `tags` - Array of tag IDs

## Query Parameters

- `per_page` - Posts per page (max 100)
- `page` - Page number
- `status` - Filter by status
- `author` - Filter by author ID
- `order` - Sort order (`asc`, `desc`)
- `orderby` - Sort field (`date`, `title`, `author`)

## Authentication

WordPress REST API requires authentication for most write operations.

**Methods:**
1. Application Passwords (recommended)
2. OAuth 1.0a
3. Basic Authentication (requires plugin)

## Error Responses

```json
{
  "code": "rest_post_invalid_id",
  "message": "Invalid post ID.",
  "data": {"status": 404}
}
```

## Rate Limiting

Rate limiting depends on hosting provider. Most hosts allow 60-120 requests/minute.

## More Info

Official docs: https://developer.wordpress.org/rest-api/
