# 部署与配置

适用对象：B/S 架构的 AI 短剧创作台——后端常驻服务提供接口，
前端为构建后的静态资源，异步任务调用外部模型，最后由本机多媒体工具
完成合成。下面按「先验收再前进」的顺序组织，每一步都给出验收方法。

---

## 一、架构形态先认清

这类系统一般是四层：

```
浏览器（前端静态资源）
    ↓ HTTP
应用服务（业务逻辑 + 任务调度）
    ↓                        ↘
数据库 / 缓存            外部模型服务（异步，返回任务号）
    ↓
多媒体工具（本机进程，负责拼接、字幕、音画对齐）
    ↓
对象存储 / CDN（成品与素材）
```

**三个关键判断**：

1. 合成在**本机**做 → 机器要有 CPU 余量，且多媒体工具必须装在被服务进程
   能调用到的位置。
2. 模型是**异步**的 → 必须有任务状态表与轮询机制，不能同步等结果。
3. 素材走**对象存储** → 存储不是可选项，上线前必须配好，否则素材会堆在本地盘。

---

## 二、硬件基线

按「每月集数」选档，别按「感觉」选：

| 档位 | 月产出 | CPU | 内存 | 系统盘 | 数据盘 | 显卡 |
|---|---|---|---|---|---|---|
| 试水 | ≤ 20 集 | 4 核 | 8 GB | 40 GB | 100 GB | 不需要 |
| 常规 | 20–100 集 | 8 核 | 16 GB | 60 GB | 500 GB | 不需要 |
| 高产 | 100–300 集 | 16 核 | 32 GB | 100 GB | 1 TB+ | 不需要 |
| 自建推理 | 任意 | 16 核+ | 64 GB+ | 100 GB | 2 TB+ | 按模型定 |

**重要提醒**：若模型全部走外部 API，**显卡不是瓶颈，CPU 才是**。
视频拼接、字幕烧录、音画对齐都吃 CPU，机器配成「强 GPU + 弱 CPU」
是最常见的浪费。只有确实要本地跑图像或视频模型时，显卡才有意义。

**带宽**：成品预览与回源都走带宽。若面向公网用户，建议对象存储挂 CDN，
并在测算脚本里按实际码率估算（见 `scripts/cost_estimate.py`）。

---

## 三、依赖安装

### 3.1 三件套版本要求

| 组件 | 版本 | 用途 | 验收命令 |
|---|---|---|---|
| 运行时 | 与后端语言匹配的 LTS 版本 | 跑应用服务 | 版本号打印正常 |
| 构建工具 | 与运行时配套 | 编译与打包 | 能输出构建成功 |
| 前端运行时 | Node.js 18 LTS 及以上 | 构建前端资源 | `node -v` |
| 数据库 | MySQL 8.0 及以上 | 业务数据 | `mysql --version` |
| 缓存 | Redis 6 及以上 | 会话、限流、任务锁 | `redis-cli ping` 返回 PONG |
| 多媒体工具 | FFmpeg 稳定版 | 合成、转码、字幕 | `ffmpeg -version` |

**后端语言与运行时版本必须与项目声明一致。** 版本不对导致的编译错误
信息通常很难读，先对齐版本能省大量时间。

### 3.2 Linux 安装要点

```bash
# 系统包方式装数据库、缓存与多媒体工具
sudo apt update
sudo apt install -y mysql-server redis-server ffmpeg

# 验证三件套
mysql --version && redis-cli ping && ffmpeg -version | head -n 1
```

前端运行时建议用版本管理器（nvm 之类）安装，避免系统包版本过旧。

### 3.3 Windows 安装要点

```powershell
# 用包管理器安装，省去手工配 PATH
winget install OpenJS.NodeJS.LTS
winget install Gyan.FFmpeg

# 装完必须重开终端再验证，否则 PATH 未刷新
node -v
ffmpeg -version
```

Windows 上数据库与缓存建议用官方安装包，或直接在 WSL 中运行。
**FFmpeg 必须确认在服务进程的 PATH 中**，服务以系统账户启动时
用户级 PATH 往往不生效——这是 Windows 上最高频的「找不到 ffmpeg」原因。

---

## 四、数据库初始化

### 4.1 建库与字符集（关键）

中文标题、台词、提示词必须用 `utf8mb4`。用默认字符集建库，
后期改字符集要重建表，代价很大。

```sql
-- 建库：显式指定字符集与排序规则
CREATE DATABASE drama_studio
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 建专用账号，不要用 root 跑应用
CREATE USER 'drama_app'@'%' IDENTIFIED BY 'REPLACE_WITH_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON drama_studio.* TO 'drama_app'@'%';
FLUSH PRIVILEGES;
```

### 4.2 连接参数

```ini
jdbc:mysql://127.0.0.1:3306/drama_studio
  ?useUnicode=true
  &characterEncoding=utf8
  &useSSL=false
  &serverTimezone=Asia/Shanghai
  &allowPublicKeyRetrieval=true
```

`serverTimezone` 必须显式指定，否则时间字段可能整体偏移。

### 4.3 验收

```sql
-- 插一条中文，再读回来，字符不能变成问号
INSERT INTO drama_studio.t_probe (title) VALUES ('测试·中文标题');
SELECT title FROM drama_studio.t_probe;
```

读回来是问号说明字符集或连接参数有问题，**此时不要继续往下走**。

### 4.4 库表结构要重点确认的四类表

不一定表名相同，但功能应当齐备：

| 类别 | 作用 | 缺失后果 |
|---|---|---|
| 作品与集 | 组织内容层级 | 无法管理多集项目 |
| 分镜 | 核心创作单元 | 无法逐镜头控制 |
| 素材与成品 | 记录生成结果地址 | 素材丢失、无法复用 |
| 任务日志 | 异步任务状态 | 失败无法重试、无法定位 |

若目标项目缺少「任务日志」类表，**异步生成会变成黑盒**，
建议先自行补一张状态表再进入生产使用。

---

## 五、密钥管理规范

**铁律：任何密钥都不进代码库。**

| 密钥类型 | 存放位置 | 禁止 |
|---|---|---|
| 数据库口令 | 环境变量或密文配置 | 写进配置文件提交 |
| 模型 API Key | 环境变量 / 加密存储 | 前端可见、日志打印 |
| 对象存储 AK/SK | 环境变量 | 硬编码 |
| 会话与签名密钥 | 环境变量 | 使用默认示例值 |

```bash
# Linux / macOS：写入当前用户环境，重启终端生效
export DRAMA_DB_PASSWORD='REPLACE_ME'
export DRAMA_AI_API_KEY='REPLACE_ME'
export DRAMA_OSS_ACCESS_KEY_ID='REPLACE_ME'
export DRAMA_OSS_ACCESS_KEY_SECRET='REPLACE_ME'
```

```powershell
# Windows：写用户级环境变量
[Environment]::SetEnvironmentVariable('DRAMA_AI_API_KEY','REPLACE_ME','User')
```

**上线前自查**：在代码库中搜索 `key`、`secret`、`password`、`token`，
确认没有真实凭据被提交。**示例值必须明显是占位符。**

若项目把密钥存在数据库里，确认是否加密存储；明文存储时至少限制
数据库访问来源，并单独审计配置读取接口。

---

## 六、模型接入

四类能力要**分别配置**，不要只配一家：

| 能力 | 用途 | 配置要点 |
|---|---|---|
| 文本 | 拆镜头、生成提示词、写台词 | 注意长文本截断与上下文长度 |
| 图片 | 场景图、角色图、参考图 | 关注参考图数量上限与一致性 |
| 视频 | 图生视频、镜头片段 | 异步任务，必须配轮询与超时 |
| 配音 | 台词转语音 | 关注音色库与是否有情感参数 |

### 6.1 供应商可替换性检查

好的架构会有一个适配层，让供应商可替换。检查方式：

> 把当前供应商的调用代码注释掉，换另一家需要改几个文件？
> 只改适配层 → 良好；要改业务逻辑 → 有风险，尽早重构。

### 6.2 混配策略

不要为了统一而只用一家。常见混配：

- 文本用便宜且稳定的，量大
- 图片选角色一致性好的，短剧最怕角色漂移
- 视频选时长与分辨率满足要求的，成本占比最大
- 配音选音色贴合角色的

配置完成后**每类都要做一次真实调用**，不要等到批量生产才发现某一类没配通。

### 6.3 异步任务必备的三件事

1. **任务号落库**：提交后立刻记录外部任务号与本地记录映射
2. **轮询与退避**：固定间隔轮询会触发限流，要有退避策略
3. **超时与重试上限**：无上限重试会把预算烧光，必须设次数上限

---

## 七、对象存储与 CDN

| 配置项 | 说明 | 常见错误 |
|---|---|---|
| 区域 / 端点 | 与服务器同区域可省回源费用 | 跨区导致回源慢且贵 |
| 存储桶 | 素材桶与成品桶分开 | 混用导致权限难管 |
| 访问域名 | 绑定 CDN 获得加速 | 直接用源站地址对外 |
| 跨域（CORS） | 允许前端域名访问 | 用 `*` 通配，存在安全隐患 |
| 生命周期 | 对中间素材设过期清理 | 不清理，存储无限增长 |

**成本提醒**：中间素材（参考图、废弃镜头）往往比成品大得多。
按「中间素材保存 30 天，成品长期保存」设置生命周期，能省掉相当一部分费用。

---

## 八、后端托管与前端发布

### 8.1 后端以常驻服务方式托管

不要把后端跑在交互式终端里。用系统服务托管，实现开机自启与崩溃重启。

```ini
# /etc/systemd/system/drama-studio.service
[Unit]
Description=Drama Studio Backend
After=network.target mysql.service redis-server.service

[Service]
Type=simple
User=drama
WorkingDirectory=/opt/drama-studio
EnvironmentFile=/etc/drama-studio/env
ExecStart=/opt/drama-studio/bin/start.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now drama-studio
sudo systemctl status drama-studio
```

**注意**：`EnvironmentFile` 是密钥进服务进程的正确方式；
直接写在 unit 文件里会被任何能读该文件的人看到。

### 8.2 前端构建

```bash
# 构建产物交给 Web 服务器，不要用开发服务器对外
npm ci
npm run build
# 产物通常在 dist/ 或 build/ 目录
```

**绝不要用开发模式的服务对外提供访问**——没有性能优化，且存在安全风险。

### 8.3 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name drama.example.com;

    # 前端静态资源
    root /opt/drama-studio/web;
    index index.html;

    # 单页应用回退
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 接口转发到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # 生成类接口耗时长，必须放宽超时
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
    }
}
```

**两个坑**：

- 单页应用必须写 `try_files` 回退，否则刷新子路由会 404
- 生成类接口**必须放宽超时**，默认 60 秒会导致长任务被网关掐断

### 8.4 跨域设置

前后端不同域时必须配置。生产环境**把允许来源写成具体域名**，
不要使用通配符；同时确认预检请求（OPTIONS）被正确响应。

---

## 九、最小闭环验收

装完之后，**先跑一个镜头**，不要直接批量：

- [ ] 能创建作品与集
- [ ] 能录入一段剧情并拆出分镜
- [ ] 至少一个分镜能生成场景图 / 角色图
- [ ] 参考图能正常预览（对象存储连通）
- [ ] 至少一个分镜能生成视频片段
- [ ] 台词能生成配音，且能试听
- [ ] 单镜头能完成合成，产出可播放文件
- [ ] 多镜头能整集拼接，音画时长基本对齐
- [ ] 后台任务列表能看到上述每一步的状态流转
- [ ] 失败任务能重试并成功

**其中「音画时长对齐」是最需要重点观察的一项**：配音时长与视频时长
通常不相等，合理做法是补静音或延长末帧。若对齐策略粗糙，
成片会出现明显跳音或画面停滞。发现该问题的成本，
在单镜头阶段发现是几分钟，在批量阶段发现是几十集的钱。

---

## 十、部署期常见问题速查

| 现象 | 优先排查 |
|---|---|
| 服务起不来 | 端口占用、数据库连不上、环境变量未加载 |
| 中文变问号 | 建库字符集、连接串 `characterEncoding` |
| 找不到 ffmpeg | 服务账户的 PATH；用绝对路径 |
| 调用模型超时 | 网关超时设置、任务是否异步 |
| 素材无法预览 | 对象存储跨域设置、域名是否可公网访问 |
| 长任务被中断 | 反向代理超时、轮询超时过短 |
| 前端刷新 404 | 缺少单页应用回退配置 |
| 磁盘迅速占满 | 中间素材未设生命周期、日志未切割 |

其余运维与成本问题见 `references/ops-and-compliance.md`。
