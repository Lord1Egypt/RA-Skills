---
name: publish-website-traefik
description: Manages static website deployments to subdomains under *.sites.friendify.cloud using Traefik reverse proxy and Docker. Provides functions to deploy, list, and delete websites. Requires a path to the website files and the desired subdomain name for deployment. Assumes Docker permissions and DNS configuration for Traefik are already set up.
---

# Publish Website via Traefik

This skill allows you to publish static websites to subdomains under `*.sites.friendify.cloud` using a Traefik reverse proxy and Docker.

## How to Use

### Example Usage:

```
To publish a website, you will run the `deploy_site.sh` script with two arguments:\n\n`./scripts/deploy_site.sh <path_to_website_files> <subdomain_name>`\n\n**Example:**\n\n`./scripts/deploy_site.sh /data/.openclaw/workspace/landingpages/new-deutscheschuleonline my-german-school`\n\nThis would deploy the website to `https://my-german-school.sites.friendify.cloud`.
```

## Architecture: One Website, One Container

This skill operates on the principle of "one website per Docker container." When you deploy a website, a dedicated Nginx container is launched. Traefik, acting as a reverse proxy, routes traffic from your specified subdomain (`{subdomain}.sites.friendify.cloud`) to this container. This approach ensures:

*   **Isolation:** Each website runs independently, preventing conflicts.
*   **Dynamic Routing:** Traefik uses Docker labels to automatically configure routing, simplifying management.
*   **Scalability:** Individual websites can be scaled or updated without affecting others.

## Managing Deployments

The skill provides the following commands for managing your website deployments:

### Deploying a Website

To deploy a website, you will run the `deploy_site.sh` script with two arguments:

`./scripts/deploy_site.sh <path_to_website_files> <subdomain_name>`

**Example:**

`./scripts/deploy_site.sh /data/.openclaw/workspace/landingpages/new-deutscheschuleonline my-german-school`

This would deploy the website to `https://my-german-school.sites.friendify.cloud`.

### Listing Deployed Websites

To see all currently deployed websites managed by this skill, use the `list_sites.sh` script:

`./scripts/list_sites.sh`

This will display a list of subdomains and their corresponding URLs.

### Deleting a Website

To remove a deployed website, use the `delete_site.sh` script, providing the subdomain name:

`./scripts/delete_site.sh <subdomain_name>`

**Example:**

`./scripts/delete_site.sh my-german-school`

This will stop and remove the associated Docker container and its resources, effectively undeploying the website.