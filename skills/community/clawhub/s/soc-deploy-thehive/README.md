# soc-deploy-thehive

Deploy TheHive 5 + Cortex 3 incident response platform on any Docker-ready Linux host. Automates account creation, API key generation, Cortex CSRF dance, and TheHive-Cortex integration wiring.

## Platform Agnostic

This skill deploys the application. It doesn't create infrastructure. Pair with:
- `hyperv-create-vm` for Hyper-V VMs
- `proxmox-create-vm` for Proxmox containers/VMs
- Or any existing Linux host with Docker

## Stack

- **TheHive 5.4** (case management, port 9000)
- **Cortex 3.1.8** (observable analysis, port 9001)
- **Elasticsearch 7.17** (shared index backend)
- **Cassandra 4.1** (TheHive database)

## What Gets Automated

- Docker Compose stack deployment
- TheHive admin password change + API key generation
- Cortex CSRF-aware superadmin + org setup
- API key generation for all accounts
- TheHive-Cortex integration wiring
- MCP connection info output

## Requirements

- SSH access to a Linux host with Docker + Compose v2
- At least 4GB RAM free

## Tags

soc, thehive, cortex, incident-response, security, docker, automation, mcp
