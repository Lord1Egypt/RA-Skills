# CDS Query Language (CQL) - Complete Pattern Reference

**Source**: [https://cap.cloud.sap/docs/cds/cql](https://cap.cloud.sap/docs/cds/cql)

## Table of Contents
- [Basic Queries](#basic-queries)
- [Advanced Queries](#advanced-queries)
- [Aggregations](#aggregations)
- [Subqueries](#subqueries)
- [Joins and Associations](#joins-and-associations)
- [Data Manipulation](#data-manipulation)
- [Transaction Patterns](#transaction-patterns)
- [Performance Optimization](#performance-optimization)

## Basic Queries

### Simple SELECT
```js
const { Books } = cds.entities;

// Select all fields
const books = await SELECT.from(Books);

// Select specific fields
const titles = await SELECT.from(Books).columns('title', 'author');

// Select with alias
const bookData = await SELECT.from(Books, b => {
  b.title,
  b.author_ID.as('author'),
  b.price.as('cost')
});
```

### WHERE Conditions
```js
// Single condition
const inStock = await SELECT.from(Books)
  .where({ stock: { '>': 0 } });

// Multiple conditions (AND)
const cheapBooks = await SELECT.from(Books)
  .where({ 
    stock: { '>': 0 },
    price: { '<': 20 }
  });

// OR conditions
const books = await SELECT.from(Books)
  .where({
    or: [
      { stock: { '>': 100 } },
      { price: { '<': 10 } }
    ]
  });

// Complex conditions
const results = await SELECT.from(Books)
  .where({
    and: [
      { stock: { '>': 0 } },
      { 
        or: [
          { price: { '<': 20 } },
          { rating: { '>': 4 } }
        ]
      }
    ]
  });
```

### Ordering and Limiting
```js
// Order by single field
const sortedBooks = await SELECT.from(Books)
  .orderBy('title')
  .limit(10);

// Order by multiple fields
const popularBooks = await SELECT.from(Books)
  .orderBy('rating', 'title')
  .limit(20);

// Order with direction
const expensiveBooks = await SELECT.from(Books)
  .orderBy('price', 'desc')
  .limit(5);

// Offset for pagination
const page2 = await SELECT.from(Books)
  .orderBy('title')
  .limit(10, 20); // Skip 20, take 10
```

## Advanced Queries

### Functions in SELECT
```js
// Built-in functions
const stats = await SELECT.one.from(Books)
  .columns(
    'count(ID) as total',
    'avg(price) as avgPrice',
    'min(price) as minPrice',
    'max(price) as maxPrice'
  );

// String functions
const bookInfo = await SELECT.from(Books)
  .columns(
    'upper(title) as upperTitle',
    'substring(title, 1, 10) as shortTitle',
    'concat(title, " by ", author.name) as fullTitle'
  );

// Date functions
const recentBooks = await SELECT.from(Books)
  .where({
    createdAt: { '>=': '2024-01-01' }
  })
  .columns(
    'year(createdAt) as year',
    'month(createdAt) as month',
    'day(createdAt) as day'
  );
```

### CASE Statements
```js
// Conditional values
const categorizedBooks = await SELECT.from(Books)
  .columns(
    'title',
    'price',
    {
      expr: 'case',
      args: [
        { when: { price: { '<': 10 } }, then: 'Cheap' },
        { when: { price: { '<': 20 } }, then: 'Moderate' },
        { else: 'Expensive' }
      ],
      as: 'priceCategory'
    }
  );

// Complex CASE with calculations
const discountBooks = await SELECT.from(Books)
  .columns(
    'title',
    'price',
    'stock',
    {
      expr: 'case',
      args: [
        { when: { stock: { '>': 100 } }, then: 0.1 },
        { when: { stock: { '>': 50 } }, then: 0.05 },
        { else: 0 }
      ],
      as: 'discountRate'
    },
    {
      expr: 'price * (1 - discountRate)',
      as: 'finalPrice'
    }
  );
```

## Aggregations

### GROUP BY
```js
// Count by category
const booksByGenre = await SELECT.from(Books)
  .columns('genre', 'count(ID) as bookCount')
  .groupBy('genre')
  .orderBy('bookCount', 'desc');

// Multiple grouping columns
const booksByAuthorAndGenre = await SELECT.from(Books)
  .columns('author_ID', 'genre', 'count(ID) as count', 'avg(price) as avgPrice')
  .groupBy('author_ID', 'genre')
  .orderBy('count', 'desc');

// Aggregation with HAVING
const popularGenres = await SELECT.from(Books)
  .columns('genre', 'count(ID) as bookCount')
  .groupBy('genre')
  .having('count(ID)', '>', 10)
  .orderBy('bookCount', 'desc');
```

### Window Functions
```js
// Row number
const rankedBooks = await SELECT.from(Books)
  .columns(
    'title',
    'price',
    {
      expr: 'row_number()',
      over: { orderBy: 'price', desc: true },
      as: 'priceRank'
    }
  );

// Running totals
const salesData = await SELECT.from('Sales')
  .columns(
    'date',
    'amount',
    {
      expr: 'sum(amount)',
      over: { 
        orderBy: 'date',
        rows: { unbounded_preceding: true }
      },
      as: 'runningTotal'
    }
  );

// Partition by
const rankedByGenre = await SELECT.from(Books)
  .columns(
    'title',
    'genre',
    'price',
    {
      expr: 'rank()',
      over: { 
        partitionBy: 'genre',
        orderBy: 'price', 
        desc: true 
      },
      as: 'rankInGenre'
    }
  );
```

## Subqueries

### EXISTS Subquery
```js
// Books with reviews
const reviewedBooks = await SELECT.from(Books)
  .where({
    ID: {
      in: SELECT.from('Reviews').columns('book_ID')
    }
  });

// Using EXISTS
const booksWithOrders = await SELECT.from(Books)
  .where(`EXISTS (
    SELECT 1 FROM Orders 
    WHERE Orders.book_ID = Books.ID
  )`);
```

### Correlated Subquery
```js
// Books with above average price
const aboveAvgPrice = await SELECT.from(Books)
  .where({
    price: { 
      '>': SELECT.one('avg(price)').from(Books) 
    }
  });

// Latest review for each book
const booksWithLatestReview = await SELECT.from(Books)
  .columns(
    'title',
    {
      subquery: SELECT.one('comment')
        .from('Reviews')
        .where({ book_ID: 'Books.ID' })
        .orderBy('createdAt', 'desc'),
      as: 'latestReview'
    }
  );
```

### IN Subquery
```js
// Books from specific authors
const featuredAuthorBooks = await SELECT.from(Books)
  .where({
    author_ID: {
      in: SELECT.from('Authors')
        .columns('ID')
        .where({ featured: true })
    }
  });
```

## Joins and Associations

### Using Associations
```js
const { Books, Authors } = cds.entities;

// Expand association
const booksWithAuthors = await SELECT.from(Books)
  .columns('title', 'price')
  .columns('author.name', 'author.bio')
  .where({ stock: { '>': 0 } });

// Nested expansion
const detailedBooks = await SELECT.from(Books)
  .columns('title')
  .columns('author.name')
  .columns('reviews { rating, comment }')
  .where({ genre: 'fiction' });

// Multiple associations
const fullBookInfo = await SELECT.from(Books)
  .columns(
    'title',
    'author.name as authorName',
    'publisher.name as publisherName',
    'reviews.rating as avgRating'
  );
```

### Manual JOINs
```js
// Inner join
const innerJoinResult = await SELECT
  .from(Books)
  .innerJoin(Authors)
  .on('Books.author_ID = Authors.ID')
  .columns(
    'Books.title',
    'Authors.name as author'
  );

// Left join
const leftJoinResult = await SELECT
  .from(Books)
  .leftJoin(Reviews)
  .on('Books.ID = Reviews.book_ID')
  .columns(
    'Books.title',
    'Reviews.rating'
  );

// Multiple joins
const complexJoin = await SELECT
  .from(Books)
  .innerJoin(Authors)
  .on('Books.author_ID = Authors.ID')
  .leftJoin(Reviews)
  .on('Books.ID = Reviews.book_ID')
  .columns(
    'Books.title',
    'Authors.name',
    'avg(Reviews.rating) as avgRating'
  )
  .groupBy('Books.ID', 'Books.title', 'Authors.name');
```

## Data Manipulation

### INSERT
```js
// Single record
const newBook = await INSERT.into(Books)
  .entries({
    title: 'New Book Title',
    author_ID: '123',
    price: 29.99,
    stock: 100
  });

// Multiple records
const batchInsert = await INSERT.into(Books).entries([
  { title: 'Book 1', author_ID: '123', price: 19.99, stock: 50 },
  { title: 'Book 2', author_ID: '456', price: 24.99, stock: 30 },
  { title: 'Book 3', author_ID: '123', price: 34.99, stock: 20 }
]);

// Insert from SELECT
const insertFromSelect = await INSERT.into(FeaturedBooks)
  .columns('book_ID', 'featuredAt')
  .select('ID', 'createdAt')
  .from(Books)
  .where({ rating: { '>': 4.5 } });
```

### UPDATE
```js
// Single record
const updateResult = await UPDATE(Books, '123')
  .set({
    price: 39.99,
    stock: 75
  });

// Update with conditions
const bulkUpdate = await UPDATE(Books)
  .set({ stock: { '-=': 1 } })
  .where({ stock: { '>': 0 } });

// Update based on other table
const updateWithJoin = await UPDATE(Books)
  .set({
    discount: 0.1
  })
  .where({
    genre: {
      in: SELECT.from('Promotions').columns('genre')
    }
  });

// Conditional update
const conditionalUpdate = await UPDATE(Books)
  .set({
    price: {
      case: [
        { when: { stock: { '>': 100 } }, then: 'price * 0.9' },
        { when: { stock: { '>': 50 } }, then: 'price * 0.95' },
        { else: 'price' }
      ]
    }
  });
```

### DELETE
```js
// Single record
const deleteResult = await DELETE.from(Books, '123');

// With conditions
const bulkDelete = await DELETE.from(Books)
  .where({ stock: 0 });

// Using subquery
const deleteUnpopular = await DELETE.from(Books)
  .where({
    ID: {
      in: SELECT.from(Reviews)
        .columns('book_ID')
        .groupBy('book_ID')
        .having('count(ID)', '<', 5)
    }
  });
```

### UPSERT
```js
// Insert or update
const upsertResult = await UPSERT.into(Books)
  .entries({
    ID: '123',
    title: 'Updated Title',
    price: 29.99,
    stock: 100
  });

// Multiple upserts
const batchUpsert = await UPSERT.into(Books).entries([
  { ID: '123', title: 'Book 1', price: 19.99, stock: 50 },
  { ID: '456', title: 'Book 2', price: 24.99, stock: 30 }
]);
```

## Transaction Patterns

### Atomic Operations
```js
// Automatic transaction in handler
this.on('placeOrder', async (req) => {
  const { bookId, quantity } = req.data;
  
  // All operations in one transaction
  const book = await SELECT.one.from(Books, bookId);
  
  if (book.stock < quantity) {
    req.error(409, 'Insufficient stock');
  }
  
  // Update stock
  await UPDATE(Books, bookId)
    .set({ stock: { '-=': quantity } });
  
  // Create order
  const order = await INSERT.into(Orders).entries({
    book_ID: bookId,
    quantity,
    total: book.price * quantity,
    status: 'confirmed'
  });
  
  return { orderId: order.ID, status: 'confirmed' };
});
```

### Manual Transaction
```js
// Explicit transaction control
await cds.tx(async (tx) => {
  // Multiple operations in transaction
  await tx.run(
    UPDATE(Books, bookId).set({ stock: { '-=': quantity } }),
    INSERT.into(Orders).entries(orderData),
    INSERT.into(AuditLog).entries(logData)
  );
  
  // Transaction commits automatically
});
```

### Transaction with Error Handling
```js
// Transaction with rollback on error
await cds.tx(async (tx) => {
  try {
    await tx.run(UPDATE(Books, bookId).set({ stock: { '-=': quantity } }));
    
    if (someCondition) {
      throw new Error('Condition failed');
    }
    
    await tx.run(INSERT.into(Orders).entries(orderData));
    
  } catch (error) {
    // Transaction automatically rolls back
    req.error(400, 'Order failed: ' + error.message);
  }
});
```

## Performance Optimization

### Query Optimization
```js
// Select only needed columns
const optimizedQuery = await SELECT.from(Books)
  .columns('ID', 'title', 'price') // Instead of *
  .where({ stock: { '>': 0 } })
  .limit(100);

// Use indexed fields in WHERE
const indexedQuery = await SELECT.from(Books)
  .where({ author_ID: authorId }) // Indexed field first
  .and({ price: { '<': 50 } });

// Use EXISTS instead of IN for large datasets
const existsQuery = await SELECT.from(Books)
  .where(`EXISTS (
    SELECT 1 FROM Reviews 
    WHERE Reviews.book_ID = Books.ID 
    AND Reviews.rating > 4
  )`);
```

### Batch Processing
```js
// Process in batches
const allBooks = await SELECT.from(Books);
const batchSize = 100;

for (let i = 0; i < allBooks.length; i += batchSize) {
  const batch = allBooks.slice(i, i + batchSize);
  
  await Promise.all(
    batch.map(book => 
      UPDATE(Books, book.ID)
        .set({ lastProcessed: new Date() })
    )
  );
}
```

### Prepared Statements (CAP handles automatically)
```js
// CAP automatically parameterizes queries to prevent SQL injection
const safeQuery = await SELECT.from(Books)
  .where({
    title: userProvidedTitle, // Automatically parameterized
    price: { '>': userProvidedPrice }
  });
```

## Best Practices

### Query Writing
- **Be Specific**: Select only columns you need
- **Use Indexes**: Query on indexed fields
- **Limit Results**: Use LIMIT/OFFSET for pagination
- **Avoid SELECT ***: Explicitly list columns

### Performance
- **Batch Operations**: Use bulk inserts/updates when possible
- **Appropriate JOINs**: Use associations over manual joins
- **Filter Early**: Apply WHERE conditions before joins
- **Use EXISTS**: For existence checks, EXISTS is often faster than IN

### Safety
- **Parameterized Queries**: Let CAP handle parameterization
- **Validate Inputs**: Always validate user input
- **Transaction Boundaries**: Keep transactions short
- **Error Handling**: Handle errors appropriately

**Last Updated**: 2025-11-27
**CAP Version**: 9.4.x
**Documentation**: [https://cap.cloud.sap/docs/cds/cql](https://cap.cloud.sap/docs/cds/cql)
