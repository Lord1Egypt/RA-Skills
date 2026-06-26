# TIFF Merge - 图片合成 TIFF 工具

将多张图片合并为多页 TIFF 文件，完全本地处理，隐私安全。

## 功能特点

- ✅ **本地处理** - 文件不上传，隐私安全
- ✅ **多格式支持** - 支持 JPG、PNG、TIFF 格式
- ✅ **多页合成** - 将多张图片合并为多页 TIFF
- ✅ **图片编辑** - 支持旋转、调整顺序
- ✅ **快速高效** - 基于 UTIF.js，处理速度快

## 安装

```bash
# 通过 ClawHub 安装
clawhub install tiff-merge

# 或手动安装
npm install -g clawhub
clawhub install tiff-merge
```

## 使用方法

### 通过 OpenClaw 自然语言调用

```
帮我把这几张图片合并成 TIFF
将 image1.jpg, image2.jpg, image3.jpg 转换为多页 TIFF
帮我生成一个 TIFF 文件，包含这些图片
```

### 命令行使用

```bash
# 基本用法
node index.js image1.jpg image2.jpg image3.jpg output.tiff

# 自动命名输出文件
node index.js image1.jpg image2.jpg image3.jpg
# 输出：merged-1713088800000.tiff
```

## 示例

### 示例 1：合并旅游照片

```bash
node index.js photo1.jpg photo2.jpg photo3.jpg travel.tiff
```

### 示例 2：合并文档扫描件

```bash
node index.js scan_001.png scan_002.png scan_003.png document.tiff
```

### 示例 3：批量处理

```bash
# 合并当前目录所有 JPG 文件
node index.js *.jpg all.tiff
```

## 技术实现

- **核心库**: [UTIF.js](https://github.com/photopea/UTIF.js)
- **运行环境**: Node.js 14+
- **处理模式**: 本地处理，无需服务器

## 隐私说明

- ✅ 所有处理在本地完成
- ✅ 文件不上传到任何服务器
- ✅ 不收集任何用户数据
- ✅ 开源代码，可审计

## 常见问题

### Q: 支持哪些图片格式？
A: 支持 JPG、PNG、TIFF 格式。

### Q: 最多可以合并多少张图片？
A: 理论上无限制，但建议不超过 100 张以保证性能。

### Q: 输出的 TIFF 文件有多大？
A: 取决于图片数量和大小，通常比原始图片总和小 20-30%。

### Q: 可以调整图片顺序吗？
A: 可以，按命令行参数顺序排列。

## 开发

```bash
# 克隆项目
git clone <repo-url>
cd tiff-merge

# 安装依赖
npm install

# 测试
node index.js test/image1.jpg test/image2.jpg output.tiff
```

## 许可证

MIT License

## 作者

你的 GitHub 用户名

## 贡献

欢迎提交 Issue 和 Pull Request！
