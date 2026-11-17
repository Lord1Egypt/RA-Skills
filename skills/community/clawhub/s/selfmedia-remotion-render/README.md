# Remotion 渲染

在用户指定的 Remotion 项目中，用其现有工具链渲染指定 Composition，并按用户合同核验结果。本包不包含模板、渲染器、私有工作台 API 或固定本机工作区。

## 依赖与运行

项目需已有可用的 Remotion 依赖、兼容浏览器运行环境和 FFmpeg 能力。候选不会静默安装依赖或下载浏览器。先填写或调整 [渲染请求示例](examples/render-request.json)，再运行预检：

```bash
python3 scripts/validate_render_request.py examples/render-request.json
```

预检只核对工作区文件、Remotion 依赖声明和新输出路径，不会执行渲染。正式渲染使用项目自己的包管理器命令，Remotion CLI 基本形式为：

```bash
remotion render <entry-point> <composition-id> <output-location> --codec=h264 --overwrite=false
```

参数以项目安装的 Remotion 版本为准。参考 [Remotion 渲染指南](https://www.remotion.dev/docs/render) 与 [CLI 参数文档](https://convert.remotion.dev/docs/cli/render)。结束后用 `ffprobe` 检查编码、尺寸、帧率、音视频轨道和时长，并实际查看画面。只将结果写到用户指定的新输出路径；此 Skill 不负责上传、晋级或发布。

## 来源与许可

原始 Skill 只有项目内 Remotion/FFmpeg 渲染步骤，无随附第三方代码或素材。此候选将固定仓库路径和私有工作台晋级接口改为用户指定项目合同，且保留源工具及事实的边界。[来源记录](SOURCE-ORIGIN.md) · [MIT-0](LICENSE)
