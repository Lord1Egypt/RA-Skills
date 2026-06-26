import { createServer } from "http";
import open from "open";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

/**
 * Authenticate with Zion.app to acquire a developer JWT token (OAuth Flow).
 * 
 * @param authEndpoint The Zion authentication endpoint.
 * @param port The port for the local callback server.
 * @returns A promise that resolves to the developer JWT token.
 */
export async function authenticate(authEndpoint = "https://auth.functorz.com/login", port = 8088): Promise<string> {
  const redirectUri = `http://localhost:${port}/callback`;

  return new Promise<string>((resolve, reject) => {
    const server = createServer((req, res) => {
      if (!req.url) return;
      const url = new URL(req.url, `http://localhost:${port}`);
      
      if (url.pathname === "/callback") {
        const token = url.searchParams.get("token");
        if (token) {
          res.writeHead(200, { "Content-Type": "text/html" });
          res.end("<h1>Token Received. You can close this window.</h1><script>setTimeout(() => window.close(), 2000)</script>");
          setTimeout(() => {
            server.close();
            resolve(token);
          }, 1000);
        } else {
          res.writeHead(400, { "Content-Type": "text/html" });
          res.end("<h1>Error: No token received</h1>");
          server.close();
          reject(new Error("No token parameter"));
        }
      }
    });

    server.listen(port, async () => {
      const authUrl = new URL(authEndpoint);
      authUrl.searchParams.set("redirect_uri", redirectUri);
      await open(authUrl.toString());
      console.log(`Waiting for authentication on port ${port}...`);
    });

    // Timeout after 5 minutes
    setTimeout(() => {
      server.close();
      reject(new Error("Authentication timeout"));
    }, 300000);
  });
}

function getJwtExpiry(token: string): string {
  try {
    const payloadBase64 = token.split('.')[1];
    const payloadJson = Buffer.from(payloadBase64, 'base64').toString('utf8');
    const payload = JSON.parse(payloadJson);
    if (payload.exp) {
      return new Date(payload.exp * 1000).toISOString();
    }
  } catch (e) {
    // Ignore invalid JWTs
  }
  return "unknown";
}

// Example usage when run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  authenticate()
    .then((token) => {
      console.log("Authentication successful.");
      
      const credentialsDir = path.resolve(process.cwd(), ".zion");
      const credentialsPath = path.join(credentialsDir, "credentials.yaml");
      
      let data: any = {};
      if (fs.existsSync(credentialsPath)) {
        try {
          data = yaml.load(fs.readFileSync(credentialsPath, "utf8")) || {};
        } catch (e) {
          console.error("Failed to parse existing credentials file, overwriting.");
        }
      }
      
      data.developer_token = {
        token: token,
        expiry: getJwtExpiry(token)
      };
      
      if (!fs.existsSync(credentialsDir)) {
        fs.mkdirSync(credentialsDir, { recursive: true });
      }
      fs.writeFileSync(credentialsPath, yaml.dump(data));
      
      console.log(`Developer token written to ${credentialsPath}`);
      process.exit(0);
    })
    .catch((error) => {
      console.error("Authentication failed:", error);
      process.exit(1);
    });
}
