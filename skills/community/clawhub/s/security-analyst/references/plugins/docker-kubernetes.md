---
name: Docker / Kubernetes
detect:
  files: ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", "k8s", "kubernetes", "helm"]
  dependencies: ["dockerode", "@kubernetes/client-node", "kubernetes"]
  keywords: ["Docker", "Kubernetes", "K8s", "Container"]
---

## recon-agent

**Container/Orchestration Discovery:**
1. Glob for `**/Dockerfile*`, `**/.dockerignore`, `**/docker-compose*.yml`, `**/docker-compose*.yaml`
2. Glob for `**/k8s/**`, `**/kubernetes/**`, `**/helm/**`, `**/charts/**`, `**/*.helm`
3. Glob for `**/kustomization.yaml`, `**/kustomization.yml`
4. Check for container registry references in CI/CD configs
5. Check for Kubernetes secrets, configmaps, service accounts in manifests

## config-infrastructure

**Dockerfile Security:**
1. **Base Image:**
   - Is the base image pinned to a specific digest? (tag-only like `node:18` can be overwritten)
   - Is the base image from a trusted registry? (Docker Hub, GCR, ECR, etc.)
   - Is the base image minimal? (`alpine`, `distroless`, `scratch` vs full `ubuntu`/`debian`)
   - Is the base image up to date? Check for known CVEs in the base image
2. **Running as Root:**
   - Is there a `USER` instruction to drop from root? (default is root)
   - If no `USER` instruction: the container runs as root, and a container escape gives root on the host
   - Is the user created with minimal capabilities?
3. **Secrets in Image:**
   - Are secrets copied into the image via `COPY` or `ADD`? (`.env`, credentials, keys)
   - Are secrets passed via `ARG` instructions? (`ARG` values are stored in image layers and visible with `docker history`)
   - Is `.dockerignore` configured to exclude `.env`, `.git`, `node_modules`, credentials?
   - Are multi-stage builds used to avoid leaking build-time secrets into the final image?
4. **Layer Secrets:**
   - Even if a secret file is deleted in a later layer, it exists in earlier layers
   - Are `--mount=type=secret` build secrets used instead of `COPY`+`RUN`+`rm`?
5. **HEALTHCHECK:**
   - Is a HEALTHCHECK defined? (without one, orchestrators can't detect unhealthy containers)
6. **Exposed Ports:**
   - Are only necessary ports exposed? (`EXPOSE` documents intent but doesn't restrict access)

**Docker Compose Security:**
7. **Privileged Mode:**
   - Is any service running with `privileged: true`? (full host access — container escape trivial)
   - Are `cap_add` capabilities minimized? (`SYS_ADMIN`, `NET_ADMIN`, `SYS_PTRACE` are dangerous)
   - Is `cap_drop: [ALL]` used with only necessary capabilities added back?
8. **Network Isolation:**
   - Are services on separate networks? (frontend/backend separation)
   - Can the frontend container directly reach the database? (should only be accessible to backend)
9. **Volume Mounts:**
   - Is the Docker socket (`/var/run/docker.sock`) mounted? (host escape via Docker API)
   - Are host paths mounted that contain sensitive data? (`/etc`, `/root`, `/home`)
   - Are volumes read-only where possible? (`:ro` flag)
10. **Environment Variables:**
    - Are secrets passed via `environment:` in docker-compose? (visible in `docker inspect`)
    - Are Docker secrets or external secret managers used instead?

**Kubernetes Security:**
11. **Pod Security:**
    - Is `runAsNonRoot: true` set in the security context?
    - Is `readOnlyRootFilesystem: true` set?
    - Is `allowPrivilegeEscalation: false` set?
    - Are `capabilities` dropped? (`drop: [ALL]` with only necessary capabilities added)
12. **RBAC:**
    - Are ServiceAccounts using the default SA? (default SA often has too many permissions)
    - Are Roles/ClusterRoles following least privilege?
    - Are there `ClusterRoleBinding`s granting `cluster-admin` to application service accounts?
13. **Secrets Management:**
    - Are Kubernetes Secrets encrypted at rest? (`EncryptionConfiguration`)
    - Are secrets mounted as files rather than environment variables? (env vars leak in logs/debug)
    - Is an external secrets operator used? (Vault, AWS Secrets Manager, etc.)
14. **Network Policies:**
    - Are NetworkPolicies defined? (without them, all pods can communicate with all pods)
    - Is egress restricted? (prevent data exfiltration from compromised pods)
15. **Resource Limits:**
    - Are CPU and memory limits set? (prevent a single pod from starving the cluster)
    - Are there `LimitRange` and `ResourceQuota` objects for namespaces?
16. **Image Security:**
    - Is `imagePullPolicy: Always` set? (prevents using stale cached images)
    - Are image registries restricted via admission controllers?
    - Is there an image scanning webhook? (Trivy, Snyk Container, etc.)

## dependency-audit

**Container Dependency Concerns:**
1. Check Docker base image for known CVEs (if Trivy, Grype, or Snyk is available, note existing scan results)
2. Are pinned image digests used for reproducible builds?
3. Check Kubernetes manifest versions — are deprecated APIs used? (`extensions/v1beta1`, `apps/v1beta1`)
4. Are Helm chart dependencies from trusted registries?
