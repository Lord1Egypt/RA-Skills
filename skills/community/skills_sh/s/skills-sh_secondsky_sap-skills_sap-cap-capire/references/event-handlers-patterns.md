# CAP Event Handlers - Complete Pattern Reference

**Source**: [https://cap.cloud.sap/docs/node.js/event-handling](https://cap.cloud.sap/docs/node.js/event-handling)

## Table of Contents
- [Handler Registration](#handler-registration)
- [Handler Types](#handler-types)
- [Request Processing](#request-processing)
- [Common Patterns](#common-patterns)
- [Error Handling](#error-handling)
- [Transaction Management](#transaction-management)
- [Performance Optimization](#performance-optimization)
- [Testing Handlers](#testing-handlers)

## Handler Registration

### Class-based Handlers
```js
// srv/cat-service.js
const cds = require('@sap/cds');

module.exports = class CatalogService extends cds.ApplicationService {
  init() {
    // Register handlers
    this.before('READ', 'Books', this.validateRead);
    this.on('READ', 'Books', this.readBooks);
    this.after('READ', 'Books', this.enrichBooks);
    
    return super.init();
  }
  
  validateRead(req) { /* ... */ }
  readBooks(req) { /* ... */ }
  enrichBooks(data, req) { /* ... */ }
}
```

### Function-based Handlers
```js
// srv/cat-service.js
module.exports = function() {
  const { Books } = this.entities;
  
  // Register handlers
  this.before('READ', Books, validateRead);
  this.on('READ', Books, readBooks);
  this.after('READ', Books, enrichBooks);
  
  function validateRead(req) { /* ... */ }
  function readBooks(req) { /* ... */ }
  function enrichBooks(data, req) { /* ... */ }
}
```

### Async Handlers
```js
// srv/cat-service.js
module.exports = async function() {
  // Async registration
  this.on('READ', 'Books', async (req) => {
    const books = await SELECT.from('Books');
    // Process async
    return books;
  });
  
  // Async with error handling
  this.on('CREATE', 'Orders', async (req) => {
    try {
      const order = await processOrder(req.data);
      return order;
    } catch (error) {
      req.reject(500, error.message);
    }
  });
};
```

## Handler Types

### Before Handlers (Validation/Preprocessing)
```js
// Single event
this.before('CREATE', 'Books', (req) => {
  if (!req.data.title) {
    req.error(400, 'Title is required');
  }
  if (req.data.price < 0) {
    req.error(400, 'Price cannot be negative');
  }
});

// Multiple events
this.before(['CREATE', 'UPDATE'], 'Books', (req) => {
  req.data.modifiedAt = new Date();
});

// All entities
this.before('*', (req) => {
  console.log(`Event: ${req.event}, Target: ${req.target}`);
});

// Conditional
this.before('SAVE', 'Books', (req) => {
  if (req.data.stock < 10) {
    req.warn('Low stock warning');
  }
});
```

### On Handlers (Custom Implementation)
```js
// Replace default CRUD
this.on('READ', 'Books', async (req) => {
  const { Books } = this.entities;
  
  // Custom query logic
  let query = SELECT.from(Books);
  
  // Apply filters
  if (req.query.SELECT.where) {
    query = query.where(req.query.SELECT.where);
  }
  
  // Apply ordering
  if (req.query.SELECT.orderBy) {
    query = query.orderBy(req.query.SELECT.orderBy);
  }
  
  return await cds.db.run(query);
});

// Custom action implementation
this.on('submitOrder', async (req) => {
  const { book, quantity } = req.data;
  const { Books, Orders } = this.entities;
  
  // Check stock
  const bookStock = await SELECT.one('stock').from(Books, book);
  if (!bookStock || bookStock.stock < quantity) {
    return req.reject(409, 'Insufficient stock');
  }
  
  // Create order
  const order = await INSERT.into(Orders).entries({
    book_ID: book,
    quantity,
    status: 'confirmed',
    createdAt: new Date()
  });
  
  // Update stock
  await UPDATE(Books, book).set({
    stock: { '-=': quantity }
  });
  
  return {
    orderID: order.ID,
    status: 'confirmed',
    message: 'Order submitted successfully'
  };
});
```

### After Handlers (Postprocessing)
```js
// Single entity processing
this.after('READ', 'Books', (books, req) => {
  if (Array.isArray(books)) {
    books.forEach(book => {
      if (book.stock > 100) {
        book.discount = '10%';
      }
    });
  }
});

// Modify response
this.after('CREATE', 'Orders', (order, req) => {
  // Add calculated fields
  order.estimatedDelivery = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
  order.trackingNumber = generateTrackingNumber();
});

// Emit events
this.after('CREATE', 'Orders', (order, req) => {
  this.emit('OrderCreated', { 
    orderID: order.ID,
    customer: order.customer_ID,
    amount: order.total 
  });
});
```

## Request Processing

### Access Request Data
```js
this.on('myAction', (req) => {
  // Request data
  const data = req.data;
  
  // Request headers
  const authHeader = req.headers.authorization;
  
  // Request parameters
  const param = req.params.paramName;
  
  // User information
  const user = req.user;
  const locale = req.user.locale;
  
  // Query information
  const target = req.target;        // Entity name
  const event = req.event;          // Event type
});
```

### Modify Response
```js
this.on('READ', 'Books', async (req) => {
  // Direct response
  return {
    ID: '123',
    title: 'Sample Book',
    // ... other fields
  };
  
  // Or modify after processing
  let result = await SELECT.from('Books');
  result.totalCount = result.length;
  return result;
});
```

### Error Responses
```js
// Error with status code
req.error(400, 'Invalid input data');

// Error with details
req.error(404, 'Book not found', {
  entity: 'Books',
  key: bookId
});

// Reject with message
req.reject(409, 'Conflict detected');

// Warning
req.warn('This operation is deprecated');

// Info
req.info('Process completed successfully');
```

## Common Patterns

### Validation Pattern
```js
// Centralized validation
const validateBook = (book) => {
  const errors = [];
  
  if (!book.title || book.title.length < 3) {
    errors.push({ field: 'title', message: 'Title must be at least 3 characters' });
  }
  
  if (!book.price || book.price < 0) {
    errors.push({ field: 'price', message: 'Price must be positive' });
  }
  
  return errors;
};

this.before('CREATE', 'Books', (req) => {
  const errors = validateBook(req.data);
  if (errors.length > 0) {
    req.error(400, 'Validation failed', errors);
  }
});
```

### Enrichment Pattern
```js
// Add calculated fields
this.after('READ', 'Books', async (books) => {
  if (!Array.isArray(books)) books = [books];
  
  for (const book of books) {
    // Calculate discount
    book.discount = book.stock > 100 ? '10%' : '0%';
    
    // Get related data
    const reviews = await SELECT('rating')
      .from('BookReviews')
      .where({ book_ID: book.ID });
    
    book.avgRating = reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length;
    
    // Format currency
    book.formattedPrice = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: book.currency || 'USD'
    }).format(book.price);
  }
});
```

### Authorization Pattern
```js
// Role-based access
this.before('DELETE', 'Books', (req) => {
  if (req.user.is('admin')) return; // Admin can delete
  
  // Check ownership
  const book = await SELECT.one('createdBy')
    .from('Books', req.params[0]);
    
  if (book.createdBy !== req.user.id) {
    req.error(403, 'Only book owners can delete books');
  }
});

// Attribute-based access
this.before('READ', 'SensitiveData', (req) => {
  if (!req.user.attr.department.includes('Finance')) {
    req.error(403, 'Access denied: Finance department only');
  }
});
```

### Audit Trail Pattern
```js
// Log all modifications
this.after(['CREATE', 'UPDATE', 'DELETE'], '*', (data, req) => {
  const audit = {
    entity: req.target.name,
    operation: req.event,
    user: req.user.id,
    timestamp: new Date(),
    data: req.event === 'DELETE' ? data : req.data
  };
  
  cds.run(INSERT.into('AuditLogs').entries(audit));
});

// Specific entity audit
this.after('UPDATE', 'Books', (data, req) => {
  const changes = {};
  
  // Track changed fields
  for (const field in req.data) {
    if (data[field] !== req.data[field]) {
      changes[field] = {
        old: data[field],
        new: req.data[field]
      };
    }
  }
  
  if (Object.keys(changes).length > 0) {
    cds.run(INSERT.into('BookChangeHistory').entries({
      book_ID: data.ID,
      changedBy: req.user.id,
      changedAt: new Date(),
      changes: JSON.stringify(changes)
    }));
  }
});
```

## Error Handling

### Global Error Handler
```js
// srv/index.js
const cds = require('@sap/cds');
cds.on('error', (err) => {
  // Log all errors
  console.error('[ERROR]', err.message);
  
  // Customize error response
  if (err.code === 'NOT_FOUND') {
    err.message = 'Resource not found';
  }
});
```

### Handler-specific Error Handling
```js
this.on('riskyOperation', async (req) => {
  try {
    const result = await riskyApiCall();
    return result;
  } catch (error) {
    // Log error
    console.error('Risky operation failed:', error);
    
    // Return user-friendly message
    req.error(500, 'Operation failed. Please try again later.');
  }
});

// Async error handling with fallback
this.on('optionalData', async (req) => {
  try {
    const data = await fetchOptionalData();
    return data;
  } catch (error) {
    // Fallback to default
    console.warn('Optional data unavailable, using defaults');
    return { default: true };
  }
});
```

## Transaction Management

### Automatic Transactions
```js
// CAP automatically wraps handlers in transactions
this.on('transferStock', async (req) => {
  const { fromBook, toBook, quantity } = req.data;
  
  // These operations are in the same transaction
  await UPDATE('Books', fromBook).set({
    stock: { '-=': quantity }
  });
  
  await UPDATE('Books', toBook).set({
    stock: { '+=': quantity }
  });
  
  // Create transfer record
  await INSERT.into('StockTransfers').entries({
    fromBook,
    toBook,
    quantity,
    timestamp: new Date()
  });
  
  return { success: true };
});
```

### Manual Transaction Control
```js
this.on('batchOperation', async (req) => {
  const { operations } = req.data;
  
  // Start manual transaction
  await cds.tx(async (tx) => {
    for (const op of operations) {
      if (op.type === 'create') {
        await tx.run(INSERT.into('Books').entries(op.data));
      } else if (op.type === 'update') {
        await tx.run(UPDATE('Books', op.id).set(op.data));
      }
      // Continue processing...
    }
  });
  
  return { processed: operations.length };
});
```

## Performance Optimization

### Batching Operations
```js
// Process in batches for large datasets
this.on('bulkUpdate', async (req) => {
  const { updates } = req.data;
  const batchSize = 100;
  
  for (let i = 0; i < updates.length; i += batchSize) {
    const batch = updates.slice(i, i + batchSize);
    
    await Promise.all(
      batch.map(update => 
        UPDATE('Books', update.id).set(update.data)
      )
    );
  }
  
  return { updated: updates.length };
});
```

### Caching Pattern
```js
// Cache frequently accessed data
const cache = new Map();

this.on('getPopularBooks', async (req) => {
  const cacheKey = 'popular_books';
  
  if (cache.has(cacheKey)) {
    const cached = cache.get(cacheKey);
    if (Date.now() - cached.timestamp < 5 * 60 * 1000) {
      return cached.data; // Return cached if less than 5 minutes old
    }
  }
  
  // Fetch fresh data
  const books = await SELECT.from('Books')
    .where({ popularity: { '>': 80 } })
    .limit(10);
  
  // Update cache
  cache.set(cacheKey, {
    data: books,
    timestamp: Date.now()
  });
  
  return books;
});
```

### Lazy Loading
```js
// Load related data only when needed
this.after('READ', 'Books', async (books, req) => {
  // Check if expand was requested
  const expandAuthor = req.query.SELECT?.expand?.includes('author');
  
  if (expandAuthor && books.length > 0) {
    const authorIds = [...new Set(books.map(b => b.author_ID))];
    
    const authors = await SELECT('ID', 'name', 'bio')
      .from('Authors')
      .where({ ID: { 'in': authorIds } });
    
    const authorMap = new Map(authors.map(a => [a.ID, a]));
    
    books.forEach(book => {
      if (book.author_ID) {
        book.author = authorMap.get(book.author_ID);
      }
    });
  }
});
```

## Testing Handlers

### Unit Test Example
```js
// test/handlers.test.js
const { GET, POST, PATCH, DELETE } = cds.test(__dirname + '/..');

describe('CatalogService', () => {
  let CatalogService, Books;
  
  beforeAll(async () => {
    CatalogService = await cds.serve('CatalogService').from('srv/cat-service');
    Books = CatalogService.entities.Books;
  });
  
  beforeEach(async () => {
    // Setup test data
    await INSERT.into(Books).entries([
      { ID: '1', title: 'Test Book 1', stock: 10 },
      { ID: '2', title: 'Test Book 2', stock: 0 }
    ]);
  });
  
  it('should only return books with stock', async () => {
    const books = await GET(Books);
    expect(books.value).toHaveLength(1);
    expect(books.value[0].title).toBe('Test Book 1');
  });
  
  it('should submit order successfully', async () => {
    const order = await POST(Books, 'submitOrder', {
      book: '1',
      quantity: 2
    });
    
    expect(order.status).toBe('confirmed');
    
    // Verify stock reduction
    const book = await GET(Books, '1');
    expect(book.stock).toBe(8);
  });
});
```

## Best Practices

### Handler Organization
- **Single Responsibility**: Each handler should do one thing well
- **Avoid Side Effects**: Before handlers shouldn't modify data
- **Consistent Error Handling**: Use standard error patterns
- **Testability**: Write handlers that are easy to test

### Performance Guidelines
- **Minimize Database Calls**: Batch operations when possible
- **Use Appropriate Caching**: Cache frequently accessed data
- **Lazy Load Associations**: Load related data only when needed
- **Optimize Queries**: Be specific about fields you need

### Security Considerations
- **Validate All Inputs**: Never trust client data
- **Implement Authorization**: Check user permissions
- **Sanitize Outputs**: Prevent data leaks
- **Use Prepared Statements**: Prevent SQL injection

**Last Updated**: 2025-11-27
**CAP Version**: 9.4.x
**Documentation**: [https://cap.cloud.sap/docs/node.js/event-handling](https://cap.cloud.sap/docs/node.js/event-handling)
