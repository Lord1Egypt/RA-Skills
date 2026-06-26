# WP-CLI Essentials

## SSH Connection Patterns

### Inline SSH

```bash
wp --ssh=user@host/path/to/wordpress <command>
```

### Alias in wp-cli.yml (project-level)

```yaml
ssh:
  mysite:
    cmd: ssh -o StrictHostKeyChecking=no %pseudotty% user@hostname %cmd%
    url: /path/to/wordpress
```

Usage: `wp @mysite <command>`

### Global Aliases (~/.wp-cli/config.yml)

```yaml
@client1:
  ssh: user@client1.com/www/public
@client2:
  ssh: user@client2.rocketcdn.me/www/client2/public
```

## Common Flags

| Flag | Purpose |
|------|---------|
| `--fields=ID,post_title` | Limit output columns |
| `--format=json` | JSON output (pipe to jq) |
| `--format=csv` | CSV output |
| `--posts_per_page=N` | Limit results |
| `--post_type=page` | Filter by post type |
| `--post_status=publish` | Filter by status |
| `--allow-root` | Run as root (hosting that requires it) |
| `--skip-plugins` | Skip plugin loading (faster, useful for debugging) |
| `--skip-themes` | Skip theme loading |
| `--quiet` | Suppress informational messages |

## Useful Diagnostic Commands

```bash
# Site health
wp @site core version
wp @site option get siteurl
wp @site option get home

# Database
wp @site db size
wp @site db tables

# Plugins
wp @site plugin list --status=active --fields=name,version
wp @site plugin status elementor

# Users
wp @site user list --fields=ID,user_login,user_email,roles

# Cron (useful for scheduled posts)
wp @site cron event list
```

## Rocket.net SSH Pattern

Rocket.net sites typically use:

```bash
wp --ssh=sshuser@hostname.rocketcdn.me/www/sitename/public <command>
```

Or with their MCP server for direct API access without SSH.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `wp: command not found` on remote | Use full path: `/usr/local/bin/wp` or install via SSH |
| SSH key not accepted | Check `~/.ssh/config` for correct IdentityFile |
| `Error establishing a database connection` | DB credentials may differ — check `wp-config.php` |
| Timeout on large exports | Use `--skip-plugins --skip-themes` to reduce memory |
| `PHP Fatal error: Allowed memory size` | Add `--exec="ini_set('memory_limit','512M');"` |
