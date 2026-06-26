const https = require('https');
const http = require('http');

class UctooApiClient {
    constructor() {
        this.baseUrl = process.env.BACKEND_URL || 'https://javatoarktsapi.uctoo.com';
        this.accessToken = null;
        this.tokenExpiration = null;
    }

    login(username, password) {
        return new Promise((resolve, reject) => {
            const endpoint = '/api/uctoo/auth/login';
            const body = JSON.stringify({ username, password });
            
            this.callApi(endpoint, 'POST', body, false)
                .then(result => {
                    try {
                        const json = JSON.parse(result);
                        if (json.data && json.data.access_token) {
                            this.accessToken = json.data.access_token;
                            this.tokenExpiration = Date.now() + 7200 * 1000;
                        }
                    } catch (e) {
                    }
                    resolve(result);
                })
                .catch(reject);
        });
    }

    isAuthenticated() {
        if (!this.accessToken) {
            return false;
        }
        if (this.tokenExpiration) {
            return Date.now() < this.tokenExpiration;
        }
        return true;
    }

    callApi(endpoint, method, body = '{}', requireAuth = true) {
        return new Promise((resolve, reject) => {
            let fullUrl = this.baseUrl;
            if (!this.baseUrl.endsWith('/') && !endpoint.startsWith('/')) {
                fullUrl += '/';
            }
            fullUrl += endpoint;

            const url = new URL(fullUrl);
            const isHttps = fullUrl.startsWith('https://');
            const client = isHttps ? https : http;

            const options = {
                hostname: url.hostname,
                port: url.port || (isHttps ? 443 : 80),
                path: url.pathname + url.search,
                method: method.toUpperCase(),
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            if (requireAuth && this.isAuthenticated()) {
                options.headers['Authorization'] = `Bearer ${this.accessToken}`;
            }

            const req = client.request(options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    try {
                        JSON.parse(data);
                        resolve(data);
                    } catch (e) {
                        resolve(JSON.stringify({
                            error: 'API returned invalid JSON',
                            message: 'The API response is not in valid JSON format'
                        }));
                    }
                });
            });

            req.on('error', (e) => {
                resolve(JSON.stringify({
                    error: 'API call failed',
                    message: e.message
                }));
            });

            if (method.toUpperCase() !== 'GET' && body) {
                req.write(body);
            }

            req.end();
        });
    }

    getResource(entityType, id) {
        const endpoint = `/api/uctoo/${entityType}/${id}`;
        return this.callApi(endpoint, 'GET');
    }

    getResources(entityType, limit = 10, page = 0) {
        const endpoint = `/api/uctoo/${entityType}/${limit}/${page}`;
        return this.callApi(endpoint, 'GET');
    }

    createResource(entityType, data) {
        const endpoint = `/api/uctoo/${entityType}/add`;
        return this.callApi(endpoint, 'POST', typeof data === 'string' ? data : JSON.stringify(data));
    }

    updateResource(entityType, data) {
        const endpoint = `/api/uctoo/${entityType}/edit`;
        return this.callApi(endpoint, 'POST', typeof data === 'string' ? data : JSON.stringify(data));
    }

    deleteResource(entityType, id) {
        const endpoint = `/api/uctoo/${entityType}/del`;
        const body = JSON.stringify({ id });
        return this.callApi(endpoint, 'POST', body);
    }
}

if (require.main === module) {
    const client = new UctooApiClient();
    console.log('Uctoo API Client initialized');
    console.log('Base URL:', client.baseUrl);
}

module.exports = UctooApiClient;
