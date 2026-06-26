# INSTALLATION AND HOSTING

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Additional Devenv Options
**Source:** [guides/installation/setups/devenv-options.md](https://developer.shopware.com/docs/guides/installation/setups/devenv-options.md)  
# Additional Devenv Options

## Enable Blackfire

To enable [Blackfire](https://blackfire.io/) profiling in your Devenv setup, add the following configuration to your `devenv.local.nix` file:

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.blackfire.enable = true;
 services.blackfire.server-id = "<SERVER_ID>";
 services.blackfire.server-token = "<SERVER_TOKEN>";
 services.blackfire.client-id = "<CLIENT_ID>";
 services.blackfire.client-token = "<CLIENT_TOKEN>";
}
```

## Enable XDebug

To enable [Xdebug](https://xdebug.org/) for debugging or profiling, add the following configuration to your `devenv.local.nix` file:

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 # XDebug
 languages.php.extensions = [ "xdebug" ];
 languages.php.ini = ''
 xdebug.mode = debug
 xdebug.discover_client_host = 1
 xdebug.client_host = 127.0.0.1
 '';
}
```

After modifying your `devenv.local.nix` file, reload your environment.

## Use MariaDB instead of MySQL

To switch from MySQL to [MariaDB](https://mariadb.org/), update your `devenv.local.nix` file:

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.mysql.package = pkgs.mariadb;
}
```

## Use a custom MySQL port

You can change the default MySQL port if it conflicts with another service on your system:

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.mysql.settings = {
 mysqld = {
 port = 33881;
 };
 };

}
```

After any change, run `devenv reload` to apply updates.

## Customize Caddy ports or virtual hosts

You can adjust the Caddy web server configuration to use a different port or virtual host.

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.caddy.virtualHosts.":8029" = {
 extraConfig = ''
 root * public
 php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
 file_server
 '';
 };
}
```

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.caddy.virtualHosts."http://shopware.swag:8029" = {
 extraConfig = ''
 root * public
 php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
 file_server
 '';
 };
}
```

## Use a custom Adminer port

If you need to change the default Adminer port (for example, to avoid conflicts with another service), update your `devenv.local.nix` file:

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.adminer.listen = "127.0.0.1:9084";
}
```

After modifying `devenv.local.nix`, reload your environment.

## Use Varnish

You can integrate [Varnish](https://varnish-cache.org/) into your local Shopware development setup to test reverse caching behavior. The following example shows how to configure Caddy and Varnish in your `devenv.local.nix` file:

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 # caddy config
 services.caddy = {
 enable = true;

 # all traffic to localhost is redirected to varnish
 virtualHosts."http://localhost" = {
 extraConfig = ''
 reverse_proxy 127.0.0.1:6081 {
 # header_up solves this issue: https://discord.com/channels/1308047705309708348/1309107911175176217
 header_up Host sw.localhost
 }
 '';
 };

 # the actual shopware application is served from sw.localhost,
 # choose any domain you want.
 # you may need to add the domain to /etc/hosts:
 # 127.0.0.1       sw.localhost
 virtualHosts."http://sw.localhost" = {
 extraConfig = ''
 # set header to avoid CORS errors
 header {
 Access-Control-Allow-Origin *
 Access-Control-Allow-Credentials true
 Access-Control-Allow-Methods *
 Access-Control-Allow-Headers *
 defer
 }
 root * public
 php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
 encode zstd gzip
 file_server
 log {
 output stderr
 format console
 level ERROR
 }
 '';
 };
 };

 # varnish config
 services.varnish = {
 enable = true;
 package = pkgs.varnish;
 listen = "127.0.0.1:6081";
 # enables xkey module
 extraModules = [ pkgs.varnishPackages.modules ];
 # it's a slightly adjusted version from the [docs](https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html#configure-varnish)
 vcl = ''
 # ...
 # Specify your app nodes here. Use round-robin balancing to add more than one.
 backend default {
 .host = "sw.localhost";
 .port = "80";
 }
 # ...
 # ACL for purgers IP. (This needs to contain app server ips)
 acl purgers {
 "sw.localhost";
 "127.0.0.1";
 "localhost";
 "::1";
 }
 # ...
 '';
 };
}
```

After updating your `devenv.local.nix`, reload your development environment to apply the changes:

```bash
devenv reload
```

## Use an older package version

Sometimes, you may want to pin a service to an older version to, for example, ensure compatibility with legacy components or reproduce a previous environment state.

Here are examples showing how to use older versions of MySQL and RabbitMQ in your `devenv.local.nix` configuration:

**Example: Use a specific MySQL version**:

```nix
{
 services.mysql = let
 mysql8033 = pkgs.mysql80.overrideAttrs (oldAttrs: {
 version = "8.0.33";
 # the final url would look like this: https://github.com/mysql/mysql-server/archive/mysql-8.0.33.tar.gz
 # make sure the url exists.
 # alternatively you could use that url directly via pkgs.fetchurl { url = "xyz"; hash="xyz";};
 # for reference see the [different fetchers](https://ryantm.github.io/nixpkgs/builders/fetchers/#chap-pkgs-fetchers)
 src = pkgs.fetchFromGitHub {
 owner = "mysql";
 repo = "mysql-server";
 rev = "mysql-8.0.33";
 # leave empty on the first run, you will get prompted with the expected hash
 sha256 = "sha256-s4llspXB+rCsGLEtI4WJiPYvtnWiKx51oAgxlg/lATg=";
 };
 });
 in
 {
 enable = true;
 package = mysql8033; # use the overridden package
 # ...
 };
}
```

**Example**: Use a specific RabbitMQ version:

```nix
{
 services.rabbitmq = let
 rabbitmq3137 = pkgs.rabbitmq-server.overrideAttrs (oldAttrs: {
 version = "3.13.7";
 src = pkgs.fetchurl {
 url = "https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.13.7/rabbitmq-server-3.13.7.tar.xz";
 sha256 = "sha256-GDUyYudwhQSLrFXO21W3fwmH2tl2STF9gSuZsb3GZh0=";
 };
 });
 in
 {
 enable = true;
 package = rabbitmq3137; # use the overridden package
 };
}
```

Pinning versions may increase build time; use only when necessary.

## Maintenance

Run `devenv gc` periodically to remove unused packages, services, and caches. This helps free disk space and keeps your environment clean.

Use `devenv down` to stop services first. If processes remain, as a last resort terminate them manually:

```bash
kill $(ps -ax | grep /nix/store | grep -v "grep" | awk '{print $1}')
```

If you can’t access <http://127.0.0.1:8000> in your browser, try <http://localhost:8000> instead. This issue is common when using WSL2 on Windows.

On macOS or Linux, the app should be available at <http://127.0.0.1:8000>.

---

---

## Devenv
**Source:** [guides/installation/setups/devenv.md](https://developer.shopware.com/docs/v6.6/guides/installation/setups/devenv.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Devenv

## What is devenv?

Imagine [devenv](https://devenv.sh) to function as a dependency manager for the services and packages that you need to run your application for local development or even in a CI/CD context.

Similar to other package managers, devenv lets you describe what your environment should look like and locks dependencies to a specific version to help you compose a reproducible setup.

Devenv not only lets you choose from and install different versions of binaries (e.g., PHP, Node, npm), but it also allows you to configure and run services (like MySQL, Redis, OpenSearch). The binaries and states of the services are stored on a per-project level.

The main difference to other tools like Docker or a VM is that it neither uses containerization nor virtualization techniques. Instead, the services run natively on your machine.

## Installation

### Nix

As devenv is built on top of Nix, first install Nix with the following command based on your OS:

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

#### Using Oh My ZSH?

You probably won't be able to use the commands below. Use the following steps to continue using [oh my zsh](https://ohmyz.sh/):

* Open `/etc/zshrc` and look for lines enclosed in `# Nix` and `# End Nix` like so (probably at the end of the file):

```bash
# Nix

# ... content ...

# End Nix
```

* Copy the lines block enclosed in `# Nix` and `# End Nix`
* Open `~/.zshrc` and add the copied lines to the end of this file
* Initiate the terminal with `source ~/.zshrc` or reboot your terminal for nix to work
* Delete the lines between `# Nix` and `# End Nix` from `/etc/zshrc`

[Credits: "nixos installation issue,'command not found: nix'", StackOverflow](https://stackoverflow.com/a/70822086/982278)

### Cachix

Next, install [Cachix](https://www.cachix.org/) to speed up the installation:

```bash
nix-env -iA cachix -f https://cachix.org/api/v1/install
```

::: info
If this is the first time using cachix, you need to add your account to the trusted users:

```bash
echo "trusted-users = root ${USER}" | sudo tee -a /etc/nix/nix.conf && sudo pkill nix-daemon
```

:::

Before installing devenv, instruct Cachix to use the devenv cache:

```bash
cachix use devenv
```

### Devenv

Finally, install devenv:

```bash
nix-env -iA devenv -f https://github.com/NixOS/nixpkgs/tarball/nixpkgs-unstable
```

Before booting up your development environment, configure Cachix to use Shopware's cache:

```bash
cachix use shopware
```

You can find the whole installation guide for devenv in their official documentation:

### Shopware

Depending on whether you want to set up a fresh Shopware project or contribute to the Shopware core, you have to choose between the [Symfony Flex template](template) or the Shopware project.

First, change to a temporary nix shell providing all necessary packages for composer:

```bash
nix-shell -p php82 php82Packages.composer
```

In that shell, create a new project:

```bash
composer create-project shopware/production <project-name>
```

Change into the project folder you've just created:

```bash
cd <project-name>
```

Require devenv:

```bash
composer require devenv
```

This will create a basic `devenv.nix` file to enable devenv support for Shopware.

```bash
git clone git@github.com:shopware/shopware.git
```

Since the environment is described via a `devenv.nix` file committed to version control, you can now boot up the environment:

```bash
devenv up
```

::: warning
Make sure that the ports for the services are not already in use, or else the command will fail.
:::

Check your default web services with the following commands:

```bash
netstat -p tcp -van | grep '^Proto\|LISTEN'
```

```bash
ss -tulpn | grep ':80\|:3306\|:6379'
```

Change your `.env` file to the correct database settings:

```bash
# <PROJECT_ROOT>/.env
DATABASE_URL="mysql://shopware:shopware@127.0.0.1:3306/shopware?sslmode=disable&charset=utf8mb4"
```

Start a *new terminal*, navigate to the project directory and run the following command to launch a devenv shell.
This shell includes all necessary programs (php, composer, npm, node, etc.) to initialize Shopware:

```bash
devenv shell
```

In the devenv shell, run the following command to initialize Shopware:

```bash
bin/console system:install --basic-setup --create-database --force
```

Open <http://localhost:8000/admin> in your browser after the installation has finished.
You should see the Shopware admin interface.

The default credentials are:

* User: admin
* Password: shopware

::: info

When using Windows and WSL2, you need to change the default sales channel domain to `http://localhost:8000`.

Important: Do use *http*, not https.

:::

### Direnv

If you wish to switch between multiple development environments which use devenv seamlessly, we recommend installing [direnv](https://direnv.net/).

When you enter a project directory using devenv, direnv will automatically activate the environment for you.
This means you can use the binaries without having to run `devenv shell` manually, though you still have to run `devenv up` to start all services.

First, install direnv:

```bash
brew install direnv
```

```bash
apt install direnv
```

Afterward, add the following hook to your shell:

```bash
// ~/.bashrc
eval "$(direnv hook bash)"
```

```bash
// ~/.zshrc
eval "$(direnv hook zsh)"
```

```bash
// ~/.config/fish/config.fish
direnv hook fish | source
```

After you change into a project directory using devenv for the first time, you need to allow direnv to load the environment:

```bash
direnv allow
```

## Default services

Here is an overview of services Shopware provides by default and how you can access them:

| Service        | Access                                          |
|----------------|-------------------------------------------------|
| MySQL          | `mysql://shopware:shopware@127.0.0.1:3306`      |
| Mailhog (SMTP) | `smtp://127.0.0.1:1025`                         |
| Redis (TCP)    | `tcp://127.0.0.1:6379`                          |

### Caddy

Caddy is a powerful, enterprise-ready, open-source web server with automatic HTTPS written in Go.

<http://127.0.0.1:8000>

### Adminer

Adminer is a full-featured database management tool written in PHP.

<http://localhost:8010>

### Mailhog

MailHog is an email testing tool for developers.

<http://localhost:8025>

## Customize your setup

To customize the predefined services to match your needs, e.g., changing the virtual host, database name, or environment variables, you can create `devenv.local.nix` to override the service definitions.
It also allows you to add and configure additional services you might require for your local development.

::: warning
After changing `devenv.local.nix`, please [reload your environment](#manually-reloading-devenv).
:::

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  # Disable a service
  services.adminer.enable = false;
  
  # Use a custom virtual host
  services.caddy.virtualHosts."http://shopware.swag" = {
    extraConfig = ''
      root * public
      php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
      file_server
    '';
  };
  
  # Customize nodejs version
  languages.javascript = {
    package = pkgs.nodejs-18_x;
  };

  # Override an environment variable
  env.APP_URL = "http://shopware.swag:YOUR_CADDY_PORT";
}
```

Refer to the official devenv documentation to get a complete list of all available services and their configuration possibilities:

### Enable Blackfire

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.blackfire.enable = true;
  services.blackfire.server-id = "<SERVER_ID>";
  services.blackfire.server-token = "<SERVER_TOKEN>";
  services.blackfire.client-id = "<CLIENT_ID>";
  services.blackfire.client-token = "<CLIENT_TOKEN>";
}
```

### Enable XDebug

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  # XDebug
  languages.php.extensions = [ "xdebug" ];
  languages.php.ini = ''
    xdebug.mode = debug
    xdebug.discover_client_host = 1
    xdebug.client_host = 127.0.0.1
  '';
}
```

### Use MariaDB instead of MySQL

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.mysql.package = pkgs.mariadb;
}
```

### Use customized MySQL port

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.mysql.settings = {
    mysqld = {
      port = 33881;
    };
  };
  
}
```

### Use customized VirtualHosts port for Caddy

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.caddy.virtualHosts.":8029" = {
    extraConfig = ''
      root * public
      php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
      file_server
    '';
  };
}
```

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.caddy.virtualHosts."http://shopware.swag:8029" = {
    extraConfig = ''
      root * public
      php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
      file_server
    '';
  };
}
```

### Use customized Adminer port

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.adminer.listen = "127.0.0.1:9084";
}
```

### Use varnish

```nix
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  # caddy config
  services.caddy = {
    enable = true;

    # all traffic to localhost is redirected to varnish
    virtualHosts."http://localhost" = {
      extraConfig = ''
        reverse_proxy 127.0.0.1:6081 {
          # header_up solves this issue: https://shopwarecommunity.slack.com/archives/C05CQT51H1V/p1721754934084939
          header_up Host sw.localhost
        }
      '';
    };

    # the actual shopware application is served from sw.localhost,
    # choose any domain you want.
    # you may need to add the domain to /etc/hosts:
    # 127.0.0.1       sw.localhost
    virtualHosts."http://sw.localhost" = {
      extraConfig = ''
        # set header to avoid CORS errors
        header {
            Access-Control-Allow-Origin *
            Access-Control-Allow-Credentials true
            Access-Control-Allow-Methods *
            Access-Control-Allow-Headers *
            defer
        }
        root * public
        php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
        encode zstd gzip
        file_server
        log {
          output stderr
          format console
          level ERROR
        }
      '';
    };
  };

  # varnish config
  services.varnish = {
    enable = true;
    package = pkgs.varnish;
    listen = "127.0.0.1:6081";
    # enables xkey module
    extraModules = [ pkgs.varnishPackages.modules ];
    # it's a slightly adjusted version from the [docs](https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html#configure-varnish)
    vcl = ''
      # ...
      # Specify your app nodes here. Use round-robin balancing to add more than one.
      backend default {
          .host = "sw.localhost";
          .port = "80";
      }
      # ...
      # ACL for purgers IP. (This needs to contain app server ips)
      acl purgers {
          "sw.localhost";
          "127.0.0.1";
          "localhost";
          "::1";
      }
      # ...
    '';
  };
}
```

### Use an older package version

Sometimes you want to pin a service to an older version.
Here is an example to use a specific mysql version.

```nix
{
  services.mysql = let 
    mysql8033 = pkgs.mysql80.overrideAttrs (oldAttrs: {
      version = "8.0.33";
      # the final url would look like this: https://github.com/mysql/mysql-server/archive/mysql-8.0.33.tar.gz
      # make sure the url exists. 
      # alternatively you could use that url directly via pkgs.fetchurl { url = "xyz"; hash="xyz";};
      # for reference see the [different fetchers](https://ryantm.github.io/nixpkgs/builders/fetchers/#chap-pkgs-fetchers)
      src = pkgs.fetchFromGitHub {
        ow

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/installation/setups/devenv.md


---

## Additional Docker Options
**Source:** [guides/installation/setups/docker-options.md](https://developer.shopware.com/docs/guides/installation/setups/docker-options.md)  
# Additional Docker Options

## Connecting to a remote database

If you want to use a database outside the Docker stack (running on your host or another server, for examples), set `DATABASE_URL` in `.env.local` in the standard form:

```bash
DATABASE_URL="mysql://user:password@<host>:3306/<database>"
```

Note: containers cannot always reach services bound only to the host's `localhost`. If `localhost` does not work you can try `host.docker.internal`, your host machine’s LAN IP, or add an `extra_hosts` entry in `compose.yaml`.

## Enable profiler/debugging for PHP

Once your Shopware environment is running, you may want to enable PHP debugging or profiling to inspect code execution, set breakpoints, or measure performance. The default setup doesn’t include these tools, but you can enable them using Docker overrides.

### Enable Xdebug

To enable [Xdebug](https://xdebug.org/) inside the web container, create a `compose.override.yaml` in your project root with the following configuration:

```yaml
services:
    web:
        environment:
            - XDEBUG_MODE=debug
            - XDEBUG_CONFIG=client_host=host.docker.internal
            - PHP_PROFILER=xdebug
```

After saving the file, apply the changes:

```bash
docker compose up -d
```

This restarts the containers with Xdebug enabled. You can now attach your IDE (for example, PHPStorm or VS Code) to the remote debugger on the default Xdebug port `9003`.

Shopware’s Docker setup also supports other profilers, like [Blackfire](https://www.blackfire.io/), [Tideways](https://tideways.com/), and [PCOV](https://github.com/krakjoe/pcov). For Tideways and Blackfire, you'll need to run an additional container. For example:

```yaml
services:
    web:
        environment:
            - PHP_PROFILER=blackfire
    blackfire:
        image: blackfire/blackfire:2
        environment:
            BLACKFIRE_SERVER_ID: XXXX
            BLACKFIRE_SERVER_TOKEN: XXXX
```

## Image variations

The Shopware Docker image is available in several variations, allowing you to match your local setup to your project’s PHP version, Node version, and preferred web server. Use the following pattern to select the right image tag:

`ghcr.io/shopware/docker-dev:php(PHP_VERSION)-node(NODE_VERSION)-(WEBSERVER)`

Here’s the version matrix:

PHP versions:

* `8.4` - PHP 8.4
* `8.3` - PHP 8.3
* `8.2` - PHP 8.2

Node versions:

* `node24` - Node 24
* `node22` - Node 22

Web server:

* `caddy` - Caddy as web server
* `nginx` - Nginx as web server

Example:

* `ghcr.io/shopware/docker-dev:php8.4-node24-caddy` - PHP 8.4, Node 24, Caddy as web server
* `ghcr.io/shopware/docker-dev:php8.3-node24-caddy` - PHP 8.3, Node 24, Caddy as web server
* `ghcr.io/shopware/docker-dev:php8.4-node22-nginx` - PHP 8.4, Node 22, Nginx as web server
* `ghcr.io/shopware/docker-dev:php8.3-node22-nginx` - PHP 8.3, Node 22, Nginx as web server

## Adding Minio for local S3 storage

Some projects use Amazon S3 for file storage in production. If you want to mimic that behavior locally—for example, to test uploads or CDN-like delivery—you can add [Minio](https://www.min.io/), an open-source S3-compatible storage server.

### 1. Add the Minio service

Include a `minio` service in your `compose.yaml`:

```yaml
services:
  # ....
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      start_period: 20s
      start_interval: 10s
      interval: 1m
      timeout: 20s
      retries: 3
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data

  minio-setup:
    image: minio/mc
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
        set -e;
        mc alias set local http://minio:9000 minioadmin minioadmin;
        mc mb local/shopware-public local/shopware-private --ignore-existing;
        mc anonymous set download local/shopware-public;
        "
    restart: no
  # ...

volumes:
  # ...
  minio-data:
```

### 2. Configure Shopware to use Minio

Create a new YAML file at `config/packages/minio.yaml` with the following content:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/shopware/shopware/refs/heads/trunk/config-schema.json

shopware:
  filesystem:
    public: &s3_public
      type: "amazon-s3"
      url: "http://localhost:9000/shopware-public"
      config:
        bucket: shopware-public
        endpoint: http://minio:9000
        use_path_style_endpoint: true
        region: us-east-1
        credentials:
          key: minioadmin
          secret: minioadmin
    theme: *s3_public
    sitemap: *s3_public
    private:
      type: "amazon-s3"
      config:
        bucket: shopware-private
        endpoint: http://minio:9000
        use_path_style_endpoint: true
        region: us-east-1
        credentials:
          key: minioadmin
          secret: minioadmin

```

After adding the Minio service to your `compose.yaml` and creating the configuration file, this will configure Shopware to use Minio as the S3 storage for public and private files.

Run `docker compose up -d` to start the Minio containers. You can access the Minio console at <http://localhost:9001> with the username `minioadmin` and password `minioadmin`.

Finally, regenerate the assets to upload them to S3:

```bash
make shell
bin/console asset:install
bin/console theme:compile
```

## Using OrbStack routing

If you're using [OrbStack](https://orbstack.dev) on macOS, you can take advantage of its built-in routing feature.
OrbStack automatically assigns local `.orb.local` URLs to your containers, so you don’t need to manage port mappings manually. This allows running multiple Shopware instances at the same time without port conflicts.

To enable it, create a `compose.override.yaml` in your project root with the following content:

```yaml
services:
  web:
      ports: !override []
      environment:
          APP_URL: https://web.sw.orb.local
          SYMFONY_TRUSTED_PROXIES: REMOTE_ADDR

###> symfony/mailer ###
  mailer:
    image: axllent/mailpit
    environment:
      MP_SMTP_AUTH_ACCEPT_ANY: 1
      MP_SMTP_AUTH_ALLOW_INSECURE: 1
###< symfony/mailer ###

```

The APP\_URL environment variable follows this pattern: `web.<project-name>.orb.local`. The `<project-folder-name>` comes from your local directory name. For example: a project called `shopware` will have the URL `https://web.shopware.orb.local`. A project called `shopware-6` will have the URL `https://web.shopware-6.orb.local`.

You can also open `https://orb.local` in your browser to view all running containers and their assigned URLs.

## Proxy production images

When you import a production database into your local environment, image URLs in the data may still point to production servers. As a result, your local store might show broken or missing images. You can fix this in two ways:

* **download all production images** and import them locally, or
* **set up a lightweight proxy service** that serves those images directly from the production server (recommended for quick testing).

### 1. Add the image proxy service

Add a `imageproxy` service to your `compose.override.yaml`:

```yaml
services:
    imageproxy:
        image: ghcr.io/shopwarelabs/devcontainer/image-proxy
        ports:
          - "8050:80"
        environment:
          # Your production URL.
          REMOTE_SERVER_HOST: shopware.com
```

This starts a proxy server that fetches images from the production environment and caches them locally. For example, a request to `http://localhost:8050/assets/images.png` will be served from `https://[REMOTE_SERVER_HOST]/assets/images.png` and then stored in the local cache for faster reuse.

### 2. Point Shopware to the proxy

Next, we need to configure Shopware to use the proxy server. To do this, create a new YAML file `config/packages/media-proxy.yaml`

```yaml
shopware:
  filesystem:
    public:
      url: "http://localhost:8050"
```

This tells Shopware to use the proxy server URL for all images.

---

---

## Docker
**Source:** [guides/installation/setups/docker.md](https://developer.shopware.com/docs/v6.6/guides/installation/setups/docker.md)  
# Docker

::: info
This setup is intended for development, if you want to use Docker for production, please check out this [guide](../../hosting/installation-updates/docker.md).
:::

Docker is a platform that enables developers to develop, ship, and run applications inside containers. These containers are lightweight, standalone, and executable packages that include everything needed to run an application: code, runtime, system tools, libraries, and settings. To get started with Docker, you can follow the official [Docker installation guide](https://docs.docker.com/get-docker/).

In this guide, we will run PHP, Node and all required services in Docker containers. If you just want to run the services (MySQL/OpenSearch/Redis/...) in Docker, check out the [Docker + Symfony CLI](./docker+symfony-cli.md) guide.

## Prerequisites

::: info
On macOS we recommend OrbStack, instead of Docker Desktop. OrbStack is a lightweight and fast alternative to Docker Desktop, and it is free for personal use. You can follow the official [OrbStack installation guide](https://orbstack.dev/docs/getting-started/installation) to install OrbStack.
:::

* Docker installed on your machine. You can follow the official [Docker installation guide](https://docs.docker.com/get-docker/) to install Docker.
* Docker Compose installed on your machine. You can follow the official [Docker Compose installation guide](https://docs.docker.com/compose/install/) to install Docker Compose.
* make installed on your machine. (`apt install make` on Ubuntu, `brew install make` on macOS)

## Create a new project

Create a new empty directory and navigate to it:

```bash
mkdir my-project
cd my-project
```

Then create a new Project:

```bash
docker run --rm -it -v $PWD:/var/www/html ghcr.io/shopwarelabs/devcontainer/base-slim:8.3 new-shopware-setup

# or specific version
docker run --rm -it -v $PWD:/var/www/html ghcr.io/shopwarelabs/devcontainer/base-slim:8.3 new-shopware-setup 6.6.10.0
```

This will create a new Shopware project in the current directory additionally with a `compose.yaml` and a `Makefile`. The difference to regular `composer create-project` is that we use PHP, Composer from the Docker image and do not need to install PHP and Composer on your local machine.

## Initial Setup

After the project is created, you can run the initial setup commands to install Shopware itself.

First, we need to start the containers

```bash
make up
```

This will start the containers in the background. You can install Shopware through the Browser at <http://localhost:8000> or through the CLI:

```bash
make setup
```

This will install Shopware itself, create an admin user with username `admin` and password `shopware`.

If you want to stop the setup, you can run `make stop` and to start it again, you can run `make up` again. If you want to remove the containers, you can run `make down`. This will remove all containers and **keep the data**. If you want to remove all containers and the data, you can run `docker compose down -v`

## Development

To access the Shopware `bin/console`, you have to enter first the container:

```bash
make shell
```

and run then `bin/console` commands.

You can also run the commands directly from your host machine without entering the container:

```bash
docker compose exec web bin/console cache:clear
```

To build the Administration or Storefront, you can run the following commands:

```bash
# Build the administration
make build-administration

# Build the storefront
make build-storefront

# Start watcher for administration
make watch-admin

# Start watcher for storefront
make watch-storefront
```

## Services

The setup comes with the following services:

* Nginx + PHP-FPM at port 8000
* MariaDB at port 3306
* Mailpit at port 8025

### Enable Profiler/Debugging for PHP

To enable XDebug, you will need to create a `compose.override.yaml`

```yaml
services:
    web:
        environment:
            - XDEBUG_MODE=debug
            - XDEBUG_CONFIG=client_host=host.docker.internal
            - PHP_PROFILER=xdebug
```

and then run `docker compose up -d` to apply the changes.

It also supports `blackfire`, `tideways` and `pcov`. For `tideways` and `blackfire` you will need a separate container like:

```yaml
services:
    web:
        environment:
            - PHP_PROFILER=blackfire
    blackfire:
        image: blackfire/blackfire:2
        environment:
            BLACKFIRE_SERVER_ID: XXXX
            BLACKFIRE_SERVER_TOKEN: XXXX
```

### Using OrbStack Routing

If you are using OrbStack as your Docker provider, you can use the OrbStack routing feature to access your services without needing to manage port mappings.

OrbStack generates for each running container a URL like `https://web.orb.local` and allows for easier access to your services without needing to manage port mappings.
This allows running multiple Shopware instances at the same time without port conflicts.

Create a `compose.override.yaml` with:

```yaml
services:
  web:
      ports: !override []
      environment:
          APP_URL: https://web.sw.orb.local
          SYMFONY_TRUSTED_PROXIES: REMOTE_ADDR
          HTTPS: on
          SERVER_PORT: 443

###> symfony/mailer ###
  mailer:
    image: axllent/mailpit
    environment:
      MP_SMTP_AUTH_ACCEPT_ANY: 1
      MP_SMTP_AUTH_ALLOW_INSECURE: 1
###< symfony/mailer ###

```

The APP\_URL environment variable always starts with `web.<project-name>.orb.local` and the rest of the URL is generated by the project name. The project name is the folder name of the project. So if you have a project called `shopware`, the URL will be `https://web.shopware.orb.local`. If you have a project called `shopware-6`, the URL will be `https://web.shopware-6.orb.local`.

You can also open `https://orb.local` in your browser and see all running containers and their URLs.

## Proxy Production Images

Typically, you import for local development a copy of the production database to your local environment. This allows you to test changes with production similar data. However, this can lead to issues that all images are missing in the local environment. To avoid this, you can download all images from the production environment and import them into your local environment. Or set up a proxy server that serves the images from the production environment.

To do this, you can add a `imageproxy` service to your `compose.override.yaml`:

```yaml
services:
    imageproxy:
        image: ghcr.io/shopwarelabs/devcontainer/image-proxy
        ports:
          - "8050:80"
        environment:
          # Your production URL.
          REMOTE_SERVER_HOST: shopware.com
```

This will start a proxy server that serves all images from the production environment. In this case if we request `http://localhost:8050/assets/images.png`, it will load `https://[REMOTE_SERVER_HOST]/assets/images.png` and serve it to the local environment, it will also cache the images locally.

Next, we need to configure Shopware to use the proxy server. To do this, create a new YAML file `config/packages/media-proxy.yaml`

```yaml
shopware:
  filesystem:
    public:
      url: "http://localhost:8050"
```

This will tell Shopware to use the proxy server URL for all images.

## Known issues

### Linux host user-id must be 1000

If you are using Docker on Linux, your host user-id must be 1000. This is a known issue with Docker on Linux. You can check your user-id with the following command:

```bash
id -u
```

---

---

## Symfony CLI
**Source:** [guides/installation/setups/symfony-cli.md](https://developer.shopware.com/docs/v6.6/guides/installation/setups/symfony-cli.md)  
# Symfony CLI

Symfony CLI is a popular tool in the Symfony ecosystem that helps to spawn a local development environment. It is a lightweight and an alternative way to Docker to run the application locally.

## Prerequisites

* Symfony CLI installed on your machine. You can follow the official [Symfony CLI installation guide](https://symfony.com/download) to install Symfony CLI.
* PHP, Composer and Node installed locally, see [here](../requirements.md) to install them.

Shopware requires a Database server, you can install MySQL or MariaDB locally using your system package manager or if Docker is installed, Symfony CLI can run the database server in a container.

## Create a new project

```bash
composer create-project shopware/production <project-name>

# or install a specific version
composer create-project shopware/production:6.6.10.0 <project-name>
```

Symfony Flex will ask while you create if you want to use Docker or not, choose **Yes** if you want to run the database in a container. If you choose **No**, you need to install MySQL or MariaDB locally.

## Initial Setup

### Local

After the project is created, you need to adjust the `DATABASE_URL` to match your local database server. To do that create a `.env.local` file in the project root and add the following line:

```dotenv
DATABASE_URL=mysql://username:password@localhost:3306/dbname
```

### Docker

To run the database in a container, you need to start the containers first with:

```bash
docker compose up -d
```

To stop the containers, you can run:

```bash
docker compose down
```

This will stop the containers and remove them. If you want to remove the containers and the data, you can run `docker compose down -v`.
This will remove all containers and the data.
If you want to remove the containers and keep the data, you can run `docker compose down` without the `-v` flag.
This will remove all containers and keep the data.

## Install Shopware

::: info
It's important that you prefix all your commands with `symfony` to ensure that the correct PHP version is used. If you don't do this, you might run into issues with the wrong PHP version being used or the Docker MySQL database is not used.
:::

After that, you can run the following command to install Shopware:

```bash
symfony console system:install --basic-setup
```

The flag `--basic-setup` will automatically create an admin user and a default sales channel for the given `APP_URL`. If you didn't create a MySQL Database yet, you can pass the `--create-database` flag to create a new database.

### Default Administration Credentials

The Shopware's default Administration credentials are:

| Username | Password   |
|:---------|:-----------|
| `admin`  | `shopware` |

Change these credentials after finishing the installation.

## Starting the Webserver

To start the webserver, run the following command:

```bash
symfony server:start
```

This will start the webserver on port 8000. You can access the Shopware Administration at <http://localhost:8000/admin> and the Storefront at <http://localhost:8000>.

If you wish to run it on the background, you can use the `-d` flag:

```bash
symfony server:start -d
```

### Stopping the Webserver

To stop the webserver, run the following command:

```bash
symfony server:stop
```

This will stop the webserver and all running processes.

## Change PHP Version

To change the used PHP version, you need to create a `.php-version` file in the project root and add the desired PHP version to it. For example, to use PHP 8.3, create a file called `.php-version` and add the following line:

```dotenv
8.3
```

This will set the PHP version to 8.3 for the current project so that any `symfony` commands will use this version. Make sure to commit this change to your version control system to keep track of the PHP version configuration. You can also verify the PHP version by running the command:

```bash
symfony php -v
```

## Changing PHP Configuration

To change the PHP Configuration, you need to create a `php.ini` file in the project root and add the desired PHP configuration to it. For example, to change the `memory_limit` to `512M`, create a file called `php.ini` and add the following line:

```ini
memory_limit = 512M
```

This will set the `memory_limit` to `512M` for the current project so that any `symfony` commands will use this configuration. Make sure to commit this change to your version control system to keep track of the PHP configuration.
You can also verify the PHP configuration by running the command:

```bash
symfony php -i
```

## Building/Watcher the Administration and Storefront

---

---

## Project Template
**Source:** [guides/installation/template.md](https://developer.shopware.com/docs/v6.6/guides/installation/template.md)  
# Project Template

The Shopware project template is a Composer project that can be used as starting point for new Shopware Projects, or if you want to develop extensions or themes for Shopware.

## Set up a new project

To create a new Shopware project, run the following command:

```bash
composer create-project shopware/production <project-name>

# or install a specific version
composer create-project shopware/production:6.6.10.5 <project-name>
```

::: info
Composer create-project clones the latest tag from the [Template repository](https://github.com/shopware/template) and installs the dependencies. If you don't have Composer installed, you could also clone the repository itself and run `composer install` in Docker to proceed with the installation.
:::

This creates a new project in the `<project-name>` directory.

The template contains all Shopware bundles like `shopware/administration`, `shopware/storefront` and `shopware/elasticsearch`. If you don't need any, then you can uninstall them with:

```bash
composer remove shopware/<bundle-name>
```

## Installation

After you have created the project, you have automatically a `.env` file in your project root. This file contains all the environment variables you need to run Shopware.

If you want to adjust a variable, you should put the variable in a `.env.local` file. This file will override the variables in the `.env` file.

::: info
The `.env` will be overwritten when the Shopware Web Installer is used for Shopware updates, so it's highly recommended to use a `.env.local` file.
:::

After you have adjusted the `.env` file, you can run the following command to install Shopware:

```bash
bin/console system:install --basic-setup
```

The flag `--basic-setup` will automatically create an admin user and a default sales channel for the given `APP_URL`. If you haven't created a MySQL Database yet, you can pass the `--create-database` flag to create a new database.

The Shopware's default Administration credentials are:

| Username | Password   |
|:---------|:-----------|
| `admin`  | `shopware` |

Change these credentials after finishing the installation.

### Optional packages

The template is small and does not contain any dev-tooling or integrations like PaaS or Fastly. You can easily add them to your project with the following commands:

```bash
# Install profiler and other dev tools, eg Faker for demo data generation
composer require --dev shopware/dev-tools

# Or Install symfony dev tools
composer require --dev symfony/profiler-pack

# Install PaaS integration
composer require paas --ignore-platform-req=ext-amqp

# Install Fastly integration
composer require fastly
```

### Add Shopware packagist

Using Shopware Packagist, you can manage all your Shopware Store plugins directly in the `composer.json`. Refer to ["Using Composer for plugin installation in Shopware"](https://www.shopware.com/en/news/using-composer-for-plugin-installation-in-shopware/) blog post for detailed information.

## Building/Watching Administration and Storefront

The created project contains Bash scripts in `bin/` folder to build and watch the Administration and Storefront. You can run the following commands:

```bash
./bin/build-administration.sh
./bin/build-storefront.sh
./bin/watch-administration.sh
./bin/watch-storefront.sh
```

Use these scripts to build the Administration and Storefront. The `watch` commands will watch for changes in the Administration and Storefront and rebuild them automatically.

## Update Shopware

There are two ways to update Shopware:

* Initially run `bin/console system:update:prepare` to enable the maintenance mode and then update all Composer packages using `composer update --no-scripts`. The `--no-scripts` flag instructs composer to not run any scripts that may reference Shopware CLI commands. They will only be functional after updating the recipes. To disable the maintenance mode, run `bin/console system:update:finish`.

* To force-update all config files, run `composer recipes:update`.

## Migrate from old zip installation to new Project Template

Before Shopware 6.5, we provided a zip file for installation. The zip file contained all dependencies required to run Shopware. This method has been deprecated and replaced with a Composer project template. The Composer project template is way more flexible and allows you to manage extensions together with Shopware itself using Composer.

To migrate from the old zip installation to the new Composer project template, you can use `shopware-cli project autofix flex` command to migrate it automatically, or you can do it manually by following the steps below.

### 1. Backup

Start with a clean git state, stash everything or make a backup of your files.

### 2. Adjust root composer.json

First, adjust your root `composer.json`. Add the following lines to your `composer.json`:

```json
"extra": {
    "symfony": {
        "allow-contrib": true,
        "endpoint": [
            "https://raw.githubusercontent.com/shopware/recipes/flex/main/index.json",
            "flex://defaults"
        ]
    }
}
```

Next, replace all the existing scripts with the following:

```json
"scripts": {
    "auto-scripts": [],
    "post-install-cmd": [
        "@auto-scripts"
    ],
    "post-update-cmd": [
        "@auto-scripts"
    ]
}
```

Finally, remove the fixed platform as it will now be determined by the required packages.

```diff
"config": {
    "optimize-autoloader": true,
-    "platform": {
-        "php": "7.4.3"
-    },
    "sort-packages": true,
    "allow-plugins": {
        "composer/package-versions-deprecated": true
    }
},
```

### 3. Cleanup the template

After having installed the new Composer packages, you can clean up the template by removing the following files:

```bash
rm -r .dockerignore \
    .editorconfig \
    .env.dist \
    .github \
    .gitlab-ci \
    .gitlab-ci.yml \
    Dockerfile \
    docker-compose.yml \
    easy-coding-standard.php \
    PLATFORM_COMMIT_SHA \
    artifacts \
    bin/deleted_files_vendor.sh \
    bin/entrypoint.sh \
    bin/package.sh \
    config/etc \
    src \
    config/secrets \
    config/services \
    config/services.xml \
    config/services_test.xml \
    license.txt \
    phpstan.neon \
    phpunit.xml.dist \
    psalm.xml

touch .env
```

### 4. Install required Composer packages

To install Symfony Flex, you need to have Composer installed. If you don't have Composer installed, please follow the [official documentation](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos).

To install Symfony Flex, you need to run the following commands and allow both new Composer plugins.

```bash
composer require "symfony/flex:*" "symfony/runtime:*"

composer recipe:install --force --reset
```

### 5. Review changes

Review the changes and commit them to your Git repository. All upcoming config changes can be applied with `composer recipes:update`.

You may need to adjust some environment variables as the names have changed:

| **Old name**      | **New name**   |
|-------------------|----------------|
| MAILER\_URL        | MAILER\_DSN     |
| SHOPWARE\_ES\_HOSTS | OPENSEARCH\_URL |

## Known issues

### `APP_ENV=dev` web\_profiler missing extension error

Prior to Shopware 6.4.17.0, you have to install the Profiler bundle to get `APP_ENV=dev` working with:

```bash
composer require --dev profiler
```

### framework:demo-data is missing faker classes

Prior to Shopware 6.4.17.0, you have to install some packages to get `framework:demo-data` command working:

```bash
composer require --dev mbezhanov/faker-provider-collection maltyxx/images-generator
```

---

---

