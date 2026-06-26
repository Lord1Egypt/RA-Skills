# 各识别类型的字段说明（stamps 内容）

根据 ocrType 不同，返回的 `stamps` 对象包含以下字段：

## SEAL_CHARACTER_RECOGNITION (印章文字识别)
- `stampPosition`: 印章坐标：[x1,y1,x2,y2]，（x1, y1）是左上角坐标，（x2, y2）是右下角坐标
- `stampConfidence`: 印章清晰度：取值范围[0, 1]
- `stampShape`: 印章形状：圆形、椭圆形、方形、三角形、菱形
- `stampColor`: 印章颜色：红色、黑色、蓝色
- `stampType`: 印章类型：监制章、财务专用章、代开发票专用章、发票专用章、个人名章、公章、合同专用章、收费专用章、税收业务专用章、业务专用章、其他印章
- `stampTextList`: 印章文字
