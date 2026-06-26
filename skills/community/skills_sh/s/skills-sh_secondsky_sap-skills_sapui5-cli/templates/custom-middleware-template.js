/**
 * Custom UI5 Server Middleware Template (CommonJS)
 *
 * Purpose: [Describe what this middleware does]
 * Use Case: [Describe when to use this middleware]
 *
 * Module Format: CommonJS (works out-of-the-box)
 * To use ESM instead, see the commented alternative at the bottom of this file.
 *
 * Configuration in ui5.yaml:
 * ---
 * specVersion: "4.0"
 * kind: extension
 * type: server-middleware
 * metadata:
 *   name: my-custom-middleware
 * middleware:
 *   path: lib/middleware/myCustomMiddleware.js
 * ---
 *
 * Usage in project ui5.yaml:
 * server:
 *   customMiddleware:
 *     - name: my-custom-middleware
 *       mountPath: /api                        # Optional: only handle /api/* requests
 *       afterMiddleware: compression           # or beforeMiddleware
 *       configuration:
 *         # Your custom configuration
 *         enabled: true
 *         target: https://api.example.com
 *
 * Specification Version: 4.0+
 * Required Dependencies: [list npm packages]
 */

/**
 * Main middleware factory function
 *
 * @param {object} params
 * @param {module:@ui5/logger.Logger} params.log - Logger instance (Spec v3.0+)
 * @param {module:@ui5/server.middleware.MiddlewareUtil} params.middlewareUtil - Utility functions (Spec v2.0+)
 * @param {object} params.options - Middleware options
 * @param {object} params.options.configuration - Custom configuration from ui5.yaml
 * @param {string} params.options.middlewareName - Middleware name (Spec v3.0+)
 * @param {object} params.resources - Resource access
 * @param {module:@ui5/fs.ReaderCollection} params.resources.all - Root project + dependencies
 * @param {module:@ui5/fs.ReaderCollection} params.resources.rootProject - Root project only
 * @param {module:@ui5/fs.ReaderCollection} params.resources.dependencies - Dependencies only
 * @returns {Function} Express middleware function
 */
module.exports = function({log, middlewareUtil, options = {}, resources}) {
    const {configuration = {}} = options;

    // Validate configuration
    if (configuration.enabled === false) {
        log.info("Middleware disabled by configuration");
        return (req, res, next) => next();
    }

    log.info("Initializing custom middleware...");

    /**
     * Express middleware function
     *
     * @param {object} req - Express request object
     * @param {object} res - Express response object
     * @param {Function} next - Next middleware function
     * @returns {Promise<void>}
     */
    return async function(req, res, next) {
        try {
            // Example 1: Simple request/response modification
            if (req.path === "/custom-endpoint") {
                res.json({
                    message: "Custom endpoint response",
                    timestamp: new Date().toISOString()
                });
                return;
            }

            // Example 2: Read UI5 resources
            if (req.path.startsWith("/resources/")) {
                const resource = await resources.rootProject.byPath(req.path);

                if (resource) {
                    const content = await resource.getString();
                    res.type("application/javascript");
                    res.end(content);
                    return;
                }
            }

            // Example 3: Add custom headers
            res.setHeader("X-Custom-Header", "UI5-Custom-Middleware");

            // Example 4: Log requests
            log.info(`${req.method} ${req.path}`);

            // Pass to next middleware
            next();

        } catch (error) {
            log.error(`Middleware error: ${error.message}`);
            next(error);
        }
    };
};

/**
 * Common patterns and examples:
 */

// Pattern 1: API Proxy
module.exports.createProxyExample = function({log, options = {}}) {
    const {createProxyMiddleware} = require("http-proxy-middleware");
    const {configuration = {}} = options;

    if (!configuration.target) {
        throw new Error("Configuration 'target' is required for proxy");
    }

    return createProxyMiddleware({
        target: configuration.target,
        changeOrigin: true,
        pathRewrite: configuration.pathRewrite || {},
        onProxyReq: (proxyReq, req) => {
            log.info(`Proxying ${req.path} to ${configuration.target}`);
        },
        onError: (err, req, res) => {
            log.error(`Proxy error: ${err.message}`);
            res.status(500).json({error: "Proxy error"});
        }
    });
};

// Pattern 2: Authentication/Authorization
module.exports.createAuthExample = function({log, options = {}}) {
    const {configuration = {}} = options;

    return async function(req, res, next) {
        const authHeader = req.headers.authorization;

        if (!authHeader) {
            res.status(401).json({error: "Unauthorized"});
            return;
        }

        try {
            // Validate token/credentials
            const isValid = await validateCredentials(authHeader, configuration);

            if (!isValid) {
                res.status(403).json({error: "Forbidden"});
                return;
            }

            next();
        } catch (error) {
            log.error(`Auth error: ${error.message}`);
            res.status(500).json({error: "Authentication failed"});
        }
    };
};

// Helper function for auth example
async function validateCredentials(authHeader, configuration) {
    // Example validation logic - handle Bearer prefix robustly
    const token = authHeader.startsWith("Bearer ")
        ? authHeader.slice("Bearer ".length).trim()
        : authHeader.trim();
    return token === configuration.validToken;
}

// Pattern 3: Mock Data Server
module.exports.createMockExample = function({log, resources}) {
    return async function(req, res, next) {
        // Only handle /mock/* requests
        if (!req.path?.startsWith("/mock/")) {
            next();
            return;
        }

        try {
            // Read mock data from project
            const mockDataPath = req.path.replace("/mock", "/test/mock");
            const mockResource = await resources.rootProject.byPath(mockDataPath + ".json");

            if (mockResource) {
                const mockData = await mockResource.getString();
                res.type("application/json");
                res.end(mockData);
                log.info(`Served mock data: ${req.path}`);
                return;
            }

            res.status(404).json({error: "Mock data not found"});
        } catch (error) {
            log.error(`Mock data error: ${error.message}`);
            next(error);
        }
    };
};

// Pattern 4: File Upload Handler
module.exports.createUploadExample = function({log, options = {}}) {
    const multer = require("multer");
    const fs = require("fs");

    // Ensure upload directory exists
    fs.mkdirSync("uploads", {recursive: true});

    const upload = multer({dest: "uploads/"});

    return function(req, res, next) {
        // Invoke multer middleware
        upload.single("file")(req, res, (err) => {
            if (err) {
                log.error(`Upload error: ${err.message}`);
                return next(err);
            }

            if (!req.file) {
                next();
                return;
            }

            log.info(`File uploaded: ${req.file.originalname}`);

            // Process uploaded file
            res.json({
                message: "File uploaded successfully",
                filename: req.file.originalname,
                size: req.file.size
            });
        });
    };
};

// Pattern 5: Content Transformation (Markdown to HTML)
module.exports.createMarkdownExample = function({log, resources}) {
    const MarkdownIt = require("markdown-it");
    const md = new MarkdownIt();

    return async function(req, res, next) {
        // Transform .md requests to HTML
        if (req.path.endsWith(".md")) {
            const resource = await resources.rootProject.byPath(req.path);

            if (resource) {
                const markdown = await resource.getString();
                const html = md.render(markdown);

                res.type("text/html");
                res.send(`<!DOCTYPE html>
<html>
<head><title>Markdown Preview</title></head>
<body>${html}</body>
</html>`);
                log.info(`Rendered markdown: ${req.path}`);
                return;
            }
        }

        next();
    };
};

// Pattern 6: Request Validation
// NOTE: This assumes a body parser middleware (e.g., express.json()) runs before this
module.exports.createValidationExample = function({log, options = {}}) {
    const {configuration = {}} = options;

    return function(req, res, next) {
        // Validate request parameters (requires body parser to populate req.body)
        if (req.method === "POST" && !req.body) {
            res.status(400).json({error: "Request body required"});
            return;
        }

        // Validate content type
        if (configuration.requireContentType) {
            const contentType = req.headers["content-type"];
            if (!contentType?.includes("application/json")) {
                res.status(415).json({error: "Content-Type must be application/json"});
                return;
            }
        }

        next();
    };
};

// Pattern 7: Response Caching
// WARNING: This is a SIMPLE EXAMPLE for development use only!
// Production implementations should include:
// - Cache size limits (e.g., LRU eviction to prevent unbounded memory growth)
// - Time-to-live (TTL) for entries to expire stale data
// - Cache invalidation on POST/PUT/DELETE operations
// - Memory monitoring and alerting
// - Consider using redis, node-cache, or lru-cache instead
const cache = new Map();
const MAX_CACHE_SIZE = 100; // Simple safeguard for development

module.exports.createCacheExample = function({log}) {
    return async function(req, res, next) {
        if (req.method !== "GET") {
            next();
            return;
        }

        // Use originalUrl to include query string in cache key
        const cacheKey = req.originalUrl || req.url;
        if (cache.has(cacheKey)) {
            log.info(`Cache hit: ${cacheKey}`);
            res.end(cache.get(cacheKey));
            return;
        }

        // Intercept response
        const originalEnd = res.end;
        res.end = function(data, ...args) {
            // Simple size limit - evict oldest entry if at capacity
            if (cache.size >= MAX_CACHE_SIZE) {
                const firstKey = cache.keys().next().value;
                cache.delete(firstKey);
                log.warn(`Cache size limit reached (${MAX_CACHE_SIZE}), evicted oldest entry`);
            }

            cache.set(cacheKey, data);
            log.info(`Cache miss: ${cacheKey}`);
            originalEnd.call(this, data, ...args);
        };

        next();
    };
};

// Pattern 8: CORS Handler
module.exports.createCORSExample = function({log, options = {}}) {
    const {configuration = {}} = options;

    return function(req, res, next) {
        res.setHeader("Access-Control-Allow-Origin", configuration.allowOrigin || "*");
        res.setHeader("Access-Control-Allow-Methods", configuration.allowMethods || "GET, POST, PUT, DELETE, OPTIONS");
        res.setHeader("Access-Control-Allow-Headers", configuration.allowHeaders || "Content-Type, Authorization");

        // Handle preflight
        if (req.method === "OPTIONS") {
            res.status(200).end();
            return;
        }

        next();
    };
};

// Pattern 9: Request Logging
module.exports.createLoggingExample = function({log}) {
    return function(req, res, next) {
        const start = Date.now();

        // Intercept response
        res.on("finish", () => {
            const duration = Date.now() - start;
            log.info(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
        });

        next();
    };
};

// Pattern 10: Error Handler (should be last middleware)
module.exports.createErrorHandler = function({log}) {
    return function(err, req, res, next) {
        // Check if headers already sent
        if (res.headersSent) {
            return next(err);
        }

        log.error(`Error handling ${req.path}: ${err.message}`);
        log.error(err.stack);

        res.status(err.status || 500).json({
            error: err.message || "Internal Server Error",
            path: req.path
        });
    };
};

/* ============================================================================
 * ESM ALTERNATIVE
 * ============================================================================
 * To use ECMAScript modules instead of CommonJS, replace this entire file with:
 *
 * // Main middleware function (ESM)
 * export default function({log, middlewareUtil, options, resources}) {
 *     const {configuration = {}} = options;
 *
 *     return async function(req, res, next) {
 *         // ... implementation
 *     };
 * }
 *
 * // Pattern exports (ESM)
 * export function createProxyExample({log, options}) {
 *     // ... implementation
 * }
 *
 * export function createAuthExample({log, options}) {
 *     // ... implementation
 * }
 * // ... etc.
 *
 * // And use ES6 imports instead of require():
 * import {createProxyMiddleware} from "http-proxy-middleware";
 * import multer from "multer";
 * import MarkdownIt from "markdown-it";
 *
 * IMPORTANT: ESM requires either:
 * 1. Add to package.json: { "type": "module" }
 * 2. Use .mjs file extension: myCustomMiddleware.mjs
 *
 * Without one of these, Node.js will throw: "SyntaxError: Unexpected token 'export'"
 * ============================================================================
 */
