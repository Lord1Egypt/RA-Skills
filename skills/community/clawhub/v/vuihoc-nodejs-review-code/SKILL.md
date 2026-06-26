1. Code Structure & Readability
Variable, function, and class names are clear and follow camelCase convention.
Functions are short and do one thing only.
Clear separation between controller, service, and model layers.
No unused code or outdated comments.
2. Error Handling
Proper error handling with try/catch for async/await.
No uncaught errors or unhandled promises.
Clear error messages are returned to the client.
3. Security
No sensitive information (passwords, keys, tokens) exposed in code.
All client input is validated.
Security middleware such as helmet and cors are used.
4. Performance
No heavy tasks blocking the event loop.
Caching is used where appropriate.
Database queries are optimized and indexed if necessary.
5. Best Practices
Environment variables are managed with dotenv.
Complex code blocks are well-commented.
Configurations, constants, and helpers are separated into their own files.
6. Testing
Important logic functions have unit tests.
Edge cases are tested.