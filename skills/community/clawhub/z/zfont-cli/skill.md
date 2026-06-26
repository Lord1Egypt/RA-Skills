name: zfont-agent-cli
version: 1.5.3
description: >
  全自动免费商用字体获取技能。
  用到的系统命令有：wget 是需要下载字体，unzip 是需要解压字体（也可以不选择解压）
  字体来自ZFONT.CN（免费商用字体）

# 补充缺失的底层依赖声明，解决注册元数据报错问题
required_binaries:
  - wget
  - unzip
  - cp
  - bash

triggers:
  - "下载字体"
  - "免费商用字体"
  - "找字体"

actions:

  # 动作 1：带智能路由的表格化搜索
  search_fonts:
    description: "搜索字体。若存在精确匹配则直达下载；否则输出 Markdown 表格。"
    parameters:
      keyword:
        type: string
        required: true
    execution:
      type: http_request
      method: POST
      url: "https://zfont.cn/tools/openclaw/search/"
      headers:
        Accept: "application/json"
        Content-Type: "application/json"
      body:
        s: "{{keyword}}"
    response_handling:
      instruction: >
        保持简约，禁止使用任何表情符号。
        获取返回的 JSON 后，按以下逻辑分支执行：

        分支 A（唯一结果确认）：
        若无完全一致匹配，且 `data.total` 为 1（或列表中仅有 1 个结果）：
        1. 输出：“**找到 1 个相关字体。**”
        2. 严格使用 Markdown 表格格式输出该字体：
           | 字体名称 | PostScript | 简介 |
           |---|---|---|
           | `name` | `postscript` | 基于 `excerpt` 的极简概括（限一句话） |
        3. 警告：绝对隐藏字体 ID。
        4. 提问：“是否**下载**该字体？(回复 **是** / **否**)”

        分支 B（模糊搜索列表）：
        若无完全一致匹配，且结果大于 1 个：
        1. 输出：“**找到 `data.total` 个相关字体。**”
        2. 挑选 2-4 个最佳匹配输出表格：
           | 字体名称 | PostScript | 简介 |
           |---|---|---|
           | `name` | `postscript` | 基于 `excerpt` 的极简概括（限一句话） |
        3. 警告：绝对隐藏字体 ID。
        4. 提问：“你要下载**第几个**？或回复**字体名称**。”

  # 动作 2：获取直链
  get_font_download_url:
    description: "获取直链，获取后立即触发下载动作。"
    parameters:
      font_id:
        type: integer
        required: true
    execution:
      type: http_request
      method: POST
      url: "https://zfont.cn/tools/openclaw/down/"
      headers:
        Accept: "application/json"
        Content-Type: "application/json"
      body:
        name: "Agent"
        id: "{{font_id}}"
    response_handling:
      instruction: >
        解析到 `data.url` 后，立刻静默调用 `download_font_archive`。不与用户对话。

  # 动作 3：下载字体
  download_font_archive:
    description: "执行 wget 下载，成功后提供文件获取方式。"
    parameters:
      download_url:
        type: string
        required: true
      font_name:
        type: string
        required: true
    execution:
      type: shell_command
      command: >
        bash -c '
        URL="{{download_url}}";
        if [[ "$URL" != https://files.zfont.cn/* ]]; then echo "FAIL_DOMAIN"; exit 1; fi;
        FILE_NAME=$(echo "{{font_name}}" | tr " " "_");
        wget -q -O "/tmp/${FILE_NAME}.zip" "$URL";
        if [ $? -eq 0 ]; then echo "SUCCESS:/tmp/${FILE_NAME}.zip"; else echo "FAIL_WGET"; fi'
    response_handling:
      instruction: >
        严禁使用表情符号。
        1. 如果输出包含 FAIL，输出：“下载失败！
        请前往 ZFONT.CN 官网下载。”并结束对话。
        2. 如果输出包含 SUCCESS，记住文件路径，并严格输出以下提问：

        **字体已下载完成**
        ---
        请选择后续操作：
        - **1. 发送文件给你(压缩包)**
        - **2. 发送文件给你(字体文件)**

  # 动作 4：解压或直接返回
  process_font_asset:
    description: "根据用户选项，解压提取或直接返回压缩包。"
    parameters:
      zip_path:
        type: string
        required: true
      font_name:
        type: string
        required: true
      user_choice:
        type: string
        description: "枚举值：'extract'(提取文件) 或 'zip'(原包)"
        required: true
    execution:
      type: shell_command
      command: >
        bash -c '
        CHOICE="{{user_choice}}"
        ZIP_PATH="{{zip_path}}"
        EXTRACT_DIR="/tmp/extracted_$(echo "{{font_name}}" | tr " " "_")"

        if [ "$CHOICE" = "zip" ]; then
          echo "RESULT_FILE:$ZIP_PATH"
          exit 0
        fi

        mkdir -p "$EXTRACT_DIR"
        unzip -q -j -o "$ZIP_PATH" -d "$EXTRACT_DIR" > /dev/null 2>&1

        if [ "$CHOICE" = "extract" ]; then
          echo "RESULT_DIR:$EXTRACT_DIR"
          exit 0
        fi
        '

    response_handling:
      instruction: >
        解析 stdout 输出：
        1. 如果包含 `RESULT_FILE` 或 `RESULT_DIR`，提取对应路径，并静默调用 `send_font_to_user` 动作。

  # 动作 5：发送文件
  send_font_to_user:
    description: "下发文件，并根据文件类型提供极简指引。"
    parameters:
      target_path:
        type: string
        required: true
    execution:
      type: natural_language_generation
    response_handling:
      instruction: >
        1. 调用框架接口下发 `{{target_path}}` 里的文件。
        2. 绝对不要复述字体的介绍信息。
        3. 检查 `{{target_path}}` 的文件类型，严格按照以下对应的格式输出：

        如果下发的是压缩包（包含 .zip）：
        **文件已发送**
        ---
        解压指南：
        - **Windows**
          右击文件 -> 提取到当前文件夹
        - **macOS**
          双击压缩包文件
        - **Linux**
          终端执行 unzip 文件名.zip

        如果下发的是字体文件：
        **文件已发送**
        ---
        安装指南：
        - **Windows**
          双击字体文件 -> 点击"安装"
        - **macOS**
          右击字体文件 -> "打开方式" -> "字体册"
        - **Linux**
          cp *.ttf ~/.local/share/fonts/ && fc-cache -fv
        ```