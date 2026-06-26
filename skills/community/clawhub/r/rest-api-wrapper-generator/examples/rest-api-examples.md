# REST API Wrapper Examples

This file contains 5 complete, production-ready examples of REST API wrappers for different domains and graph databases. Each example demonstrates real-world scenarios with full API specifications and implementation examples.

---

## Table of Contents

1. [Social Network REST API](#1-social-network-rest-api)
2. [E-Commerce Product API](#2-e-commerce-product-api)
3. [Organization Management API](#3-organization-management-api)
4. [Knowledge Base Documentation API](#4-knowledge-base-documentation-api)
5. [Scientific Research API](#5-scientific-research-api)

---

## 1. Social Network REST API

### Domain Description

REST API for a social network graph built on Neo4j. Demonstrates:
- User management endpoints
- Relationship (friendship, following) endpoints
- Social graph traversal
- Recommendation endpoints
- Search and filtering

### API Specification

#### Base URL
```
https://api.socialnetwork.com/v1
```

#### Authentication
```
Header: Authorization: Bearer {token}
```

### Node Endpoints

#### Create User
```http
POST /users
Content-Type: application/json
Authorization: Bearer token

{
  "username": "alice",
  "email": "alice@example.com",
  "bio": "Software Engineer",
  "profile_image_url": "https://example.com/alice.jpg"
}
```

Response (201):
```json
{
  "id": "u1",
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get User Profile
```http
GET /users/u1
Authorization: Bearer token
```

Response (200):
```json
{
  "id": "u1",
  "username": "alice",
  "email": "alice@example.com",
  "bio": "Software Engineer",
  "followers_count": 150,
  "following_count": 80,
  "posts_count": 45
}
```

#### List Users with Filtering
```http
GET /users?limit=20&offset=0&filter[status]=active&sort=-created_at
Authorization: Bearer token
```

### Relationship Endpoints

#### Create Friendship
```http
POST /relationships/friendships
Content-Type: application/json
Authorization: Bearer token

{
  "user1_id": "u1",
  "user2_id": "u2"
}
```

Response (201):
```json
{
  "id": "r1",
  "type": "FRIENDS_WITH",
  "user1_id": "u1",
  "user2_id": "u2",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Follow User
```http
POST /relationships/follows
Content-Type: application/json
Authorization: Bearer token

{
  "follower_id": "u1",
  "following_id": "u2"
}
```

#### Get User's Friends
```http
GET /users/u1/friends?limit=20
Authorization: Bearer token
```

Response (200):
```json
{
  "friends": [
    {"id": "u2", "username": "bob"},
    {"id": "u3", "username": "charlie"}
  ],
  "total": 150,
  "limit": 20
}
```

### Advanced Endpoints

#### Get Mutual Friends
```http
GET /users/u1/mutual-friends/u2
Authorization: Bearer token
```

Response (200):
```json
{
  "mutual_friends": [
    {"id": "u4", "username": "david"},
    {"id": "u5", "username": "eve"}
  ],
  "total": 5
}
```

#### Get Recommendations (Friend of Friends)
```http
GET /users/u1/recommendations?limit=10
Authorization: Bearer token
```

#### Social Distance
```http
POST /graph/shortest-path
Content-Type: application/json
Authorization: Bearer token

{
  "start_user_id": "u1",
  "end_user_id": "u20",
  "max_hops": 6
}
```

Response:
```json
{
  "path": [
    {"id": "u1", "username": "alice"},
    {"id": "u5", "username": "eve"},
    {"id": "u20", "username": "frank"}
  ],
  "distance": 2
}
```

### Python Implementation

```python
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Social Network API")

class UserCreate(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    email: str

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate, db = Depends(get_db)):
    """Create new user"""
    user_id = db.create_node("Person", user.dict())
    return {"id": user_id, **user.dict()}

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, db = Depends(get_db)):
    """Get user profile"""
    user = db.get_node(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}/friends")
async def get_friends(
    user_id: str,
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db = Depends(get_db)
):
    """Get user's friends with pagination"""
    friends = db.execute_query(
        f"""
        MATCH (u:Person)--[r:FRIENDS_WITH]--(friend:Person)
        WHERE u.id = '{user_id}'
        RETURN friend
        SKIP {offset} LIMIT {limit}
        """
    )
    return {"friends": friends, "limit": limit, "offset": offset}

@app.post("/relationships/friendships")
async def create_friendship(
    user1_id: str,
    user2_id: str,
    db = Depends(get_db)
):
    """Create friendship between two users"""
    rel_id = db.create_relationship(
        user1_id,
        user2_id,
        "FRIENDS_WITH"
    )
    return {"id": rel_id, "type": "FRIENDS_WITH"}
```

---

## 2. E-Commerce Product API

### Domain Description

REST API for e-commerce product catalog and recommendations built on Neo4j. Demonstrates:
- Product management
- Category hierarchies
- Supplier relationships
- Product recommendations
- Inventory management

### API Specification

#### Base URL
```
https://api.ecommerce.com/v1
```

### Product Endpoints

#### Get Product
```http
GET /products/p1
Accept: application/json
```

Response:
```json
{
  "id": "p1",
  "name": "Laptop",
  "price": 999.99,
  "category_id": "c1",
  "supplier_id": "s1",
  "stock": 45,
  "rating": 4.5,
  "reviews_count": 128
}
```

#### List Products with Filters
```http
GET /products?category=c1&min_price=500&max_price=2000&limit=20&sort=-rating
```

#### Search Products
```http
GET /products/search?q=laptop&limit=10
```

#### Get Product Recommendations
```http
GET /products/p1/recommendations?limit=5
```

Response:
```json
{
  "recommendations": [
    {
      "id": "p2",
      "name": "USB-C Hub",
      "price": 49.99,
      "reason": "frequently_purchased_with"
    }
  ]
}
```

### Relationship Endpoints

#### Get Category Products
```http
GET /categories/c1/products?limit=20&sort=name
```

#### Get Related Products
```http
GET /products/p1/related?limit=10
```

#### Get Supplier Products
```http
GET /suppliers/s1/products?limit=50
```

### Implementation Example

```python
@app.get("/products")
async def list_products(
    category: Optional[str] = None,
    min_price: float = Query(0, ge=0),
    max_price: float = Query(999999, ge=0),
    limit: int = Query(20, le=100),
    offset: int = 0,
    sort: str = "name",
    db = Depends(get_db)
):
    """List products with filtering and pagination"""
    query = "MATCH (p:Product)"
    filters = []
    
    if category:
        filters.append(f"WHERE (p)-[:IN_CATEGORY]->(c:Category {{id:'{category}'}})")
    
    if min_price > 0 or max_price < 999999:
        price_filter = f"p.price >= {min_price} AND p.price <= {max_price}"
        filters.append(f"WHERE {price_filter}")
    
    where_clause = " ".join(filters) if filters else ""
    order_by = f"ORDER BY p.{sort.lstrip('-')}" + (" DESC" if sort.startswith("-") else "")
    
    full_query = f"""
    {query}
    {where_clause}
    {order_by}
    SKIP {offset} LIMIT {limit}
    """
    
    products = db.execute_query(full_query)
    return {
        "products": products,
        "limit": limit,
        "offset": offset
    }

@app.get("/products/{product_id}/recommendations")
async def get_product_recommendations(
    product_id: str,
    limit: int = Query(5, le=20),
    db = Depends(get_db)
):
    """Get product recommendations using collaborative filtering"""
    query = f"""
    MATCH (p:Product {{id:'{product_id}'}})-[:PURCHASED_WITH]-(rec:Product)
    WITH rec, COUNT(*) as frequency
    ORDER BY frequency DESC
    LIMIT {limit}
    RETURN rec
    """
    recommendations = db.execute_query(query)
    return {"recommendations": recommendations}
```

---

## 3. Organization Management API

### Domain Description

REST API for organizational structure and hierarchy. Demonstrates:
- Department management
- Employee management
- Reporting relationships
- Role assignments
- Organizational charts

### API Specification

### Department Endpoints

#### Create Department
```http
POST /departments
Content-Type: application/json

{
  "name": "Engineering",
  "parent_department_id": null,
  "budget": 5000000
}
```

#### Get Department
```http
GET /departments/d1
```

#### Get Department Hierarchy
```http
GET /departments/d1/tree
```

Response:
```json
{
  "id": "d1",
  "name": "Engineering",
  "subdepartments": [
    {"id": "d2", "name": "Backend"},
    {"id": "d3", "name": "Frontend"}
  ]
}
```

### Employee Endpoints

#### Create Employee
```http
POST /employees
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@company.com",
  "department_id": "d1",
  "manager_id": "e5",
  "job_title": "Senior Engineer"
}
```

#### Get Employee
```http
GET /employees/e1
```

#### Get Employee's Team
```http
GET /employees/e1/team?include_indirect=false
```

#### Get Organizational Chart
```http
GET /departments/d1/org-chart?depth=3
```

---

## 4. Knowledge Base Documentation API

### Domain Description

REST API for documentation and knowledge base. Demonstrates:
- Topic management
- Documentation relationships
- Learning paths
- Search and navigation

### API Specification

### Topic Endpoints

#### Create Topic
```http
POST /topics
Content-Type: application/json

{
  "title": "Python Basics",
  "description": "Introduction to Python",
  "difficulty": "beginner",
  "estimated_time_minutes": 120
}
```

#### Get Topic with Prerequisites
```http
GET /topics/t1/full
```

Response:
```json
{
  "id": "t1",
  "title": "Data Structures",
  "prerequisites": [
    {"id": "t0", "title": "Python Basics"}
  ],
  "documents": [
    {"id": "d1", "title": "Arrays and Lists"}
  ]
}
```

#### Get Learning Path
```http
GET /topics/t5/learning-path
```

Response:
```json
{
  "path": [
    {"id": "t1", "title": "Python Basics"},
    {"id": "t2", "title": "Data Types"},
    {"id": "t3", "title": "Functions"},
    {"id": "t5", "title": "Algorithms"}
  ]
}
```

#### Search Topics
```http
GET /topics/search?q=algorithm&limit=10
```

---

## 5. Scientific Research API

### Domain Description

REST API for research papers and citations. Demonstrates:
- Paper management
- Author relationships
- Citation networks
- Research statistics

### API Specification

### Paper Endpoints

#### Create Paper
```http
POST /papers
Content-Type: application/json

{
  "title": "Graph Neural Networks",
  "authors": ["Alice", "Bob"],
  "year": 2024,
  "venue": "NeurIPS"
}
```

#### Get Paper with Citations
```http
GET /papers/p1
```

Response:
```json
{
  "id": "p1",
  "title": "Graph Neural Networks",
  "authors": [{"id": "a1", "name": "Alice"}],
  "year": 2024,
  "citations_count": 150,
  "cited_by": [{"id": "p5", "title": "Deep Learning"}]
}
```

#### Get Citation Network
```http
GET /papers/p1/citations?depth=2
```

#### Get Author Papers
```http
GET /authors/a1/papers?sort=-year
```

#### Get Collaboration Graph
```http
GET /authors/a1/collaborators?limit=20
```

---

## Summary

These 5 examples demonstrate:

✅ **Social Network** - User relationships, recommendations, social graphs  
✅ **E-Commerce** - Products, categories, recommendations  
✅ **Organization** - Hierarchies, teams, reporting structures  
✅ **Knowledge Base** - Topics, prerequisites, learning paths  
✅ **Research** - Papers, citations, collaborations  

Each example includes:
- Complete API specification
- HTTP request/response examples
- Filtering and pagination
- Python implementation examples
- Real-world use cases

All examples follow best practices:
- RESTful conventions
- Proper status codes
- Error handling
- Authentication
- Pagination and filtering
- Documentation

---

**Last Updated:** April 12, 2026  
**API Version:** 1.0.0

