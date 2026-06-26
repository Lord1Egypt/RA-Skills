---
title: Handle SDK Errors Properly
impact: HIGH
impactDescription: Graceful error recovery, better UX, easier debugging
tags: sdk, errors, error-handling, exceptions
---

## Handle SDK Errors Properly

All SDK methods return Promises that may reject with `ClientResponseError`. Proper error handling improves user experience and simplifies debugging.

**Incorrect (ignoring or poorly handling errors):**

```javascript
// No error handling
const posts = await pb.collection('posts').getList();

// Generic catch that loses information
try {
  await pb.collection('posts').create({ title: '' });
} catch (e) {
  alert('Something went wrong');  // No useful info
}

// Not checking specific error types
try {
  await pb.collection('posts').getOne('nonexistent');
} catch (e) {
  console.log(e.message);  // Missing status, response details
}
```

**Correct (comprehensive error handling):**

```javascript
import PocketBase, { ClientResponseError } from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// Basic error handling with ClientResponseError
async function createPost(data) {
  try {
    return await pb.collection('posts').create(data);
  } catch (error) {
    if (error instanceof ClientResponseError) {
      console.log('Status:', error.status);
      console.log('Response:', error.response);
      console.log('URL:', error.url);
      console.log('Is abort:', error.isAbort);

      // Handle specific status codes
      switch (error.status) {
        case 400:
          // Validation error - extract user-friendly messages only
          // IMPORTANT: Don't expose raw error.response.data to clients
          // as it may leak internal field names and validation rules
          const fieldErrors = {};
          if (error.response?.data) {
            for (const [field, details] of Object.entries(error.response.data)) {
              fieldErrors[field] = details.message;
            }
          }
          return { error: 'validation', fields: fieldErrors };
        case 401:
          // Unauthorized - need to login
          return { error: 'unauthorized' };
        case 403:
          // Forbidden - no permission
          return { error: 'forbidden' };
        case 404:
          // Not found
          return { error: 'not_found' };
        default:
          return { error: 'server_error' };
      }
    }
    throw error;  // Re-throw non-PocketBase errors
  }
}

// Handle validation errors with field details
async function updateProfile(userId, data) {
  try {
    return await pb.collection('users').update(userId, data);
  } catch (error) {
    if (error.status === 400 && error.response?.data) {
      // Extract field-specific errors
      const fieldErrors = {};
      for (const [field, details] of Object.entries(error.response.data)) {
        fieldErrors[field] = details.message;
      }
      return { success: false, errors: fieldErrors };
      // { errors: { email: "Invalid email format", name: "Required field" } }
    }
    throw error;
  }
}

// Handle request cancellation
async function searchWithCancel(query) {
  try {
    return await pb.collection('posts').getList(1, 20, {
      filter: pb.filter('title ~ {:query}', { query })
    });
  } catch (error) {
    if (error.isAbort) {
      // Request was cancelled (e.g., user typed again)
      console.log('Search cancelled');
      return null;
    }
    throw error;
  }
}

// Wrapper function for consistent error handling
async function pbRequest(fn) {
  try {
    return { data: await fn(), error: null };
  } catch (error) {
    if (error instanceof ClientResponseError) {
      return {
        data: null,
        error: {
          status: error.status,
          message: error.response?.message || 'Request failed',
          data: error.response?.data || null
        }
      };
    }
    return {
      data: null,
      error: { status: 0, message: error.message, data: null }
    };
  }
}

// Usage
const { data, error } = await pbRequest(() =>
  pb.collection('posts').getList(1, 20)
);

if (error) {
  console.log('Failed:', error.message);
} else {
  console.log('Posts:', data.items);
}
```

**ClientResponseError structure:**

```typescript
interface ClientResponseError {
  url: string;           // The request URL
  status: number;        // HTTP status code (0 if network error)
  response: {            // API response body
    code: number;
    message: string;
    data: { [field: string]: { code: string; message: string } };
  };
  isAbort: boolean;      // True if request was cancelled
  cause: Error | null;   // Original error (added in JS SDK v0.26.1)
}
```

Reference: [PocketBase Error Handling](https://github.com/pocketbase/js-sdk#error-handling)
