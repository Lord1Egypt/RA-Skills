# ENBX 课件格式参考（希沃白板）

`ENBX` 是希沃白板（EasiNote 5）的私有课件格式。**它本质是一个 ZIP 压缩包**，内部采用类 XAML/XML 的描述文件（注意：它不是标准 OOXML，没有 `ppt/` 目录，也无需 `[Content_Types].xml` 以外的 OOXML 关系文件）。本参考基于对一个真实样本（`courseware.enbx`，由希沃白板 5.1.x 生成）的逆向拆解，描述了生成合规课件必须满足的结构。

## 1. 文件清单（必须完全一致）

```
[Content_Types].xml        # 内容类型声明（带 UTF-8 BOM）
Document.xml               # 课件元信息（名称、作者、版本、时间戳）
Reference.xml              # 资源关系表：资源 Id/Hash -> Resources\<hash>.<ext>
Board.xml                  # 幻灯片顺序：<Slides><Item>幻灯片Id</Item>...
SaveInfoMetadataFile.xml   # 静态元素类型契约列表（内容无关，原样复制即可）
Slides/Slide_0.xml         # 第 1 页
Slides/Slide_1.xml         # 第 2 页
...                        # 顺序与 Board.xml 的 Item 顺序一致
Resources/<hash>.png       # 图片/背景（带扩展名）
Resources/<hash>.mp3       # 音频（带扩展名）
thumbnail.png              # 预览缩略图
```

### 致命细节（错一个都可能打不开）
- **所有 XML 文件必须以 UTF-8 BOM（`ï»¿`）开头**，并声明 `<?xml version="1.0" encoding="utf-8"?>`（小写 `utf-8`）。
- **`Slide` 的 `<Id>` 必须与 `Board.xml` 中的 `<Item>` 一一对应且顺序一致**。
- 元素通过 `id://<hash>` 引用的资源，**必须**同时出现在 `Reference.xml` 和 `Resources/` 实体文件中。
- 资源 `Target` 使用 Windows 路径分隔符：`Resources\<hash>.png`。
- 颜色为 ARGB 十六进制：`#FFFFFFFF`（不透明白）、`#FF000000`（不透明黑）、`#00FFFFFF`（透明）。

## 2. 关键文件结构

### Document.xml
```xml
<Document>
  <Name>课件名称</Name>
  <Creator>...</Creator>
  <LastModifiedBy>...</LastModifiedBy>
  <CreatedDateTime>M/D/YYYY H:MM:SS</CreatedDateTime>
  <ModifiedDateTime>M/D/YYYY H:MM:SS</ModifiedDateTime>
  <CreatedDocumentVersion>1.0</CreatedDocumentVersion>
  <DocumentVersion>1.0</DocumentVersion>
  <CreatedAppVersion>5.1.17.73189</CreatedAppVersion>
  <AppVersion>5.1.17.73189</AppVersion>
  <DocumentExtraInfo>
    <CoursewareSourceTrace>
      <UpstreamAuthor>...</UpstreamAuthor>
      <UpstreamId>{uuid}</UpstreamId>
      <UpstreamVersion>1</UpstreamVersion>
    </CoursewareSourceTrace>
  </DocumentExtraInfo>
</Document>
```

### Reference.xml
```xml
<Reference>
  <Relationships>
    <Relationship>
      <Id>944acab37cce4d78a5a7871f9e1d1460</Id>
      <Target>Resources\944acab37cce4d78a5a7871f9e1d1460.png</Target>
      <Hash>944acab37cce4d78a5a7871f9e1d1460</Hash>
    </Relationship>
  </Relationships>
</Reference>
```
`Id` 与 `Hash` 相同，`Target` 为 `Resources\<hash>.<ext>`。

### Board.xml
```xml
<Board>
  <Slides>
    <Item>6c843c1baada48259711b891da2901ff</Item>
    <Item>cb27ea6786c444fe925ff88cb6c17ebd</Item>
  </Slides>
  <ThemeForBoard>
    <ThemeId>-12</ThemeId>
    <ThemeBrush>
      <ImageBrush>
        <Source>id://<背景资源hash></Source>
        <Stretch>Fill</Stretch><TileMode>None</TileMode><Opacity>1</Opacity>
        <ViewboxUnits>RelativeToBoundingBox</ViewboxUnits>
        <ViewportUnits>RelativeToBoundingBox</ViewportUnits>
        <Viewbox>0,0,1,1</Viewbox><Viewport>0,0,1,1</Viewport>
        <RelativeMatrixTransform>1,0,0,1,0,0</RelativeMatrixTransform>
      </ImageBrush>
    </ThemeBrush>
  </ThemeForBoard>
</Board>
```

## 3. 幻灯片（Slides/Slide_N.xml）

```xml
<Slide>
  <Id>32位十六进制</Id>
  <Width>1280</Width>
  <Height>720</Height>
  <Background>
    <ImageBrush>
      <Source>id://<背景资源hash></Source>
      <Stretch>Fill</Stretch> ... (同 Board 的 ImageBrush)
    </ImageBrush>
  </Background>
  <Elements>
    <!-- Text / Picture / Table / Audio -->
  </Elements>
  <Duration>5000000</Duration>
  <ThemeForSlide><ThemeId>-12</ThemeId></ThemeForSlide>
</Slide>
```

### 3.1 文本元素 `<Text>`
- 内部 `<RichText>` 包含 `<TextLines><TextLine>`；**每个视觉行对应一个 `<TextLine>`**。
- 每个 `<TextLine>` 含一个 `<TextRuns><TextRun>`（可见文本+格式）和一个 `<DefaultRunProperty><TextRun>`（默认格式，文本为空）。
- `<TextRun><Text>` 文本后接 `&#xD;` 换行；顶层 `<Text>` 为全部行拼接。
- `<Lines><LineProperty><Length>` = 该行可见字符数（含中文按字数计）。
- 位置属性：`<X> <Y> <Width> <Height> <Rotation>0</Rotation> <IsLocked>False</IsLocked> <CanClone>False</CanClone> <Hyperlink></Hyperlink> <HasMask>False</HasMask> <RotateOrigin>0.5,0.5</RotateOrigin> <TextMask></TextMask>`。
- 字体：`<FontFamily><Source>微软雅黑</Source></FontFamily>`；字号 `<FontSize>`；粗细 `<FontWeight>Normal|Bold</FontWeight>`；前景色 `<Foreground><ColorBrush>#FF000000</ColorBrush></Foreground>`。

### 3.2 图片元素 `<Picture>`
```xml
<Picture>
  <Source>id://<资源hash></Source>
  <PictureName>file0.png</PictureName>
  <Alpha>1</Alpha>
  <DisplayRegion><Rectangle>0,0,天然宽,天然高</Rectangle></DisplayRegion>
  <Style><StyleType>None</StyleType><PicturePresetStyle>None</PicturePresetStyle></Style>
  <MetaData><PictureSize>天然高,天然宽</PictureSize><FileSize>字节数</FileSize></MetaData>
  <Id>{guid}</Id>
  <X>..</X><Y>..</Y><Width>显示宽</Width><Height>显示高</Height>
  ...
</Picture>
```

### 3.3 表格元素 `<Table>`
包含 `<Skin>`（Gray 风格、表头填充、行皮肤、描边）、`<ColumnWidths><Item>`、`Rows><Row><Height><Cells><Cell>`。每个 `<Cell>` 内含一个完整的 `<Text>`（RichText），以及 `<HMerged>/<VMerged>/<RowSpan>/<ColumnSpan>/<IsErasable>`。

## 4. 生成器输入规格（spec.json）

生成器 `scripts/generate_enbx.py` 读取如下 JSON：

```jsonc
{
  "courseware_name": "课件名称",
  "canvas": {"width": 1280, "height": 720},   // 可选，默认 1280x720
  "pages": [
    {
      // 方式 A：便捷字段（自动排版）
      "layout": "title_slide | content",        // 可选
      "background": "#1565C0",                  // 页面背景色（支持渐变 background2）
      "background2": "#0D47A1",                // 可选，渐变结束色
      "title": "标题文本",
      "subtitle": "副标题",
      "bullets": ["要点1", "要点2"],
      "content": "正文段落（自动折行）",
      "table": {"header": true, "rows": [["列1","列2"],["a","b"]]},

      // 方式 B：完全自定义（提供 elements 时忽略上面的便捷字段）
      "elements": [
        {"type":"title",  "text":"...", "x":80,"y":60,"w":1120,"h":90,"size":48,"color":"#1A237E","align":"Left"},
        {"type":"text",   "text":"...", "x":100,"y":240,"w":1080,"h":300,"size":30,"color":"#222222","line_spacing":4},
        {"type":"bullets","items":["a","b"], "x":100,"y":240,"w":1080,"size":30},
        {"type":"table",  "rows":[[...]], "x":100,"y":240,"w":1080,"header":true,"size":24},
        {"type":"box",    "x":120,"y":230,"w":1040,"h":60,"color":"#FFB300"},
        {"type":"picture","src":"/绝对路径/图片.png","x":100,"y":100,"w":400,"h":300}
      ]
    }
  ]
}
```

坐标单位为幻灯片像素（默认画布 1280×720，原点在左上角）。脚本会自动对文本按宽度折行、生成背景/色块 PNG、登记资源与关系表，并打包为 `.enbx`。

运行方式：
```bash
python3 scripts/generate_enbx.py spec.json output.enbx
```

## 5. 校验

`scripts/validate_enbx.py` 可执行与真实样本相同的结构校验（ZIP 完整性、XML 良构、资源解析、Slide↔Board 对应），对生成产物运行它，应得到 `✅ 校验通过`。
