# CDS Service Definitions - Complete Reference

**Source**: [https://cap.cloud.sap/docs/services](https://cap.cloud.sap/docs/services)

## Table of Contents
- [Service Basics](#service-basics)
- [Service Projections](#service-projections)
- [Actions and Functions](#actions-and-functions)
- [Service Configuration](#service-configuration)
- [Service Composition](#service-composition)
- [External Services](#external-services)
- [Service Annotations](#service-annotations)

## Service Basics

### Service Definition
```cds
service BookService {
  // Entity definitions
  entity Books { ... }
  entity Authors { ... }
  
  // Actions and functions
  action submitOrder(...) returns ...;
  function getOrderCount() returns ...;
}
```

### Service Path
```cds
service CatalogService @(path: '/browse') {
  ...
}
```

### Service Exposure Control
```cds
// Exposed to OData
service CatalogService { ... }

// Internal service only
@impl['srv/cat-service.js']
service InternalService { ... }
```

## Service Projections

### Basic Projection
```cds
using { my.bookshop as my } from '../db/schema';

service CatalogService {
  // Simple projection
  entity Books as projection on my.Books;
  
  // With column selection
  entity Books as projection on my.Books {
    *, author.name as author
  } excluding { createdBy, modifiedBy };
}
```

### Projection with Calculated Fields
```cds
service CatalogService {
  entity Books as projection on my.Books {
    *, 
    author.name as author,
    discountedPrice: price * 0.9
  };
}
```

### Projection with Filtering
```cds
service CatalogService {
  entity AvailableBooks as projection on my.Books {
    key ID, title, price
  } where stock > 0;
}
```

### Projection with Associations
```cds
service CatalogService {
  entity Books as projection on my.Books {
    key ID,
    title,
    author { key ID, name },
    reviews { rating, comment }
  };
}
```

## Actions and Functions

### Unbound Actions (Service-level)
```cds
service OrderService {
  // Action that changes state
  action cancelOrder(orderID: UUID, reason: String) returns {
    success: Boolean;
    message: String;
  };
  
  // Function for read-only operations
  function getOrderCount() returns Integer;
  
  // Function with parameters
  function getBooksByGenre(genre: String) returns array of Books;
}
```

### Bound Actions (Entity-level)
```cds
service ProductService {
  entity Products {
    key ID : UUID;
    name : String;
    price : Decimal;
    stock : Integer;
  } actions {
    // Bound action
    action discount(percent: Decimal) returns Decimal;
    
    // Bound function
    function getStock() returns Integer;
    
    // Action with entity return
    action createVariants(variants: array of String) returns array of Products;
  };
}
```

### Parameterized Entities
```cds
service CatalogService {
  entity Books(genre: String) as projection on my.Books
    where genre = $genre;
}
```

### Actions with Complex Types
```cds
service OrderService {
  type OrderResult : {
    success: Boolean;
    orderID: UUID;
    message: String;
    items: array of {
      productID: UUID;
      quantity: Integer;
      price: Decimal;
    };
  };
  
  action placeOrder(order: OrderInput) returns OrderResult;
}
```

## Service Configuration

### Service-level Settings
```cds
service CatalogService @(path: '/browse') {
  @odata.draft.enabled
  entity Books as projection on my.Books;
  
  @readonly
  entity Authors as projection on my.Authors;
}
```

### Service-specific Requires
```cds
service MyService {
  @requires: 'authenticated-user'
  entity SensitiveData { ... }
  
  @requires: ['admin', 'support']
  action adminOperation(...) returns ...;
}
```

### Service Endpoints
```cds
// Different protocols
service RESTService @(protocol: 'rest') { ... }
service GraphQLService @(protocol: 'graphql') { ... }
service ODataV2Service @(protocol: 'odata-v2') { ... }
```

## Service Composition

### Service Inclusion
```cds
// Include another service
service AdminService {
  include CatalogService;
  
  // Add admin-specific entities
  entity AdminLogs { ... }
}
```

### Service Extension
```cds
// Extend existing service
extend service CatalogService with {
  entity FeaturedBooks as projection on my.Books where featured = true;
}
```

### Service Redefinition
```cds
// Redefine parts of a service
redefine service CatalogService {
  // Change behavior of Books
  entity Books {
    // Add new elements
    priority: Integer;
    
    // Override annotations
    @UI.LineItem: [ { Value: priority } ]
  }
}
```

## External Services

### Define External Service
```cds
service ExternalAPI {
  entity BusinessPartners as projection on srv.BusinessPartner;
  
  action searchPartners(query: String) returns array of BusinessPartners;
}
```

### External Service Configuration
```json
{
  "cds": {
    "requires": {
      "ExternalAPI": {
        "kind": "odata-v2",
        "credentials": {
          "url": "https://api.example.com"
        }
      }
    }
  }
}
```

### Use External Service
```cds
using { ExternalAPI as ext } from '../external';

service MyService {
  entity LocalPartners as projection on ext.BusinessPartners;
}
```

## Service Annotations

### OData Annotations
```cds
service CatalogService {
  @odata.draft.enabled
  entity Books { ... }
  
  @readonly
  entity StaticData { ... }
  
  @insertonly
  entity AuditLog { ... }
}
```

### CAP-specific Annotations
```cds
service AdminService @(
  impl: 'srv/admin-service.js',
  path: '/admin'
) {
  ...
}
```

### Protocol-specific Annotations
```cds
service MyService {
  // OData V4
  @(odata.v4) {}
  
  // OData V2
  @(odata.v2) {}
  
  // REST
  @(rest) {}
}
```

## Best Practices

### Service Design
- **Single Purpose**: Each service should have a clear, single responsibility
- **Coarse-grained**: Prefer fewer, larger services over many small ones
- **Domain-aligned**: Services should align with business domains
- **Consistent**: Use consistent naming and patterns across services

### Projection Guidelines
- **Expose Only Needed Data**: Use projections to limit exposed fields
- **Optimize for Use Cases**: Design projections for specific UI or API needs
- **Maintain Performance**: Consider database implications of projections
- **Version Compatibility**: Use projections to maintain API compatibility

### Action Design
- **Use Actions for State Changes**: Actions should modify data
- **Use Functions for Queries**: Functions should be read-only
- **Batch Operations**: Consider batch operations for efficiency
- **Error Handling**: Provide clear error messages and error codes

### Performance Considerations
- **Lazy Loading**: Use associations for related data access
- **Pagination**: Implement pagination for large result sets
- **Caching**: Use CAP's built-in caching where appropriate
- **Database Optimization**: Consider indexes for frequently queried fields

## Complete Example

```cds
using { sap.capire.bookshop as db } from '../db/schema';
using { cuid, managed } from '@sap/cds/common';

// Main catalog service for end users
service CatalogService @(path: '/browse', impl: 'srv/catalog-service.js') {
  
  // Read-only book catalog with author information
  @readonly
  @odata.draft.enabled
  entity Books as projection on db.Books {
    key ID,
    title,
    descr,
    price,
    currency,
    stock,
    genre { code, text },
    author { key ID, name },
    rating: Decimal(3,2)
  } 
  excluding { createdBy, modifiedAt, modifiedBy }
  where stock > 0;
  
  // Author information
  @readonly
  entity Authors as projection on db.Authors {
    key ID,
    name,
    bio,
    books {
      key ID,
      title,
      price
    } where stock > 0;
  };
  
  // User actions
  @requires: 'authenticated-user'
  action submitOrder(book: UUID, quantity: Integer) returns {
    orderID: UUID;
    status: String;
    message: String;
  };
  
  // Utility functions
  function getGenres() returns array of String;
  function searchBooks(query: String, genre: String) returns array of Books;
}

// Admin service for content management
service AdminService @(path: '/admin', impl: 'srv/admin-service.js') {
  
  // Full book management with drafts
  @odata.draft.enabled
  entity Books as projection on db.Books;
  
  @odata.draft.enabled
  entity Authors as projection on db.Authors;
  
  // Admin-only operations
  @requires: 'admin'
  entity AdminLogs as projection on db.AdminLogs;
  
  @requires: ['admin', 'manager']
  action bulkUpdatePrices(updates: array of {
    book: UUID;
    newPrice: Decimal;
    reason: String;
  }) returns {
    success: Boolean;
    updated: Integer;
    failed: array of UUID;
  };
  
  // Analytics functions
  @requires: 'admin'
  function getSalesReport(fromDate: Date, toDate: Date) returns {
    totalOrders: Integer;
    totalRevenue: Decimal;
    topBooks: array of {
      title: String;
      unitsSold: Integer;
      revenue: Decimal;
    };
  };
}

// Public API service for external integration
service PublicAPI @(protocol: 'rest', path: '/api/v1') {
  
  // Simplified book catalog for public API
  entity PublicBooks as projection on db.Books {
    key ID,
    title,
    price,
    currency,
    genre { code },
    rating: Decimal(3,2)
  } 
  where published = true
  excluding { createdBy, modifiedAt, modifiedBy };
  
  // Public endpoints
  function getFeaturedBooks(limit: Integer = 10) returns array of PublicBooks;
  function getBooksByGenre(genre: String) returns array of PublicBooks;
}
```

**Last Updated**: 2025-11-27
**CAP Version**: 9.4.x
**Documentation**: [https://cap.cloud.sap/docs/services](https://cap.cloud.sap/docs/services)
