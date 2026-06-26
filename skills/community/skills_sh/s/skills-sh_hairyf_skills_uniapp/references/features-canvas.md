---
name: features-canvas
description: uni-app 画布 createCanvasContext、CanvasContext、canvasToTempFilePath
---

# 画布 API

## uni.createCanvasContext(canvasId, componentInstance)

创建指定 canvas 的绘图上下文。**canvasId** 为 `<canvas>` 的 canvas-id 或 id（支付宝用 id）。在自定义组件内使用时，第二参数传组件实例 this，以便在组件内查找对应 canvas。返回 **CanvasContext** 实例。

## CanvasContext

通过上下文实例可调用绘图方法：drawImage、fillRect、strokeRect、fillText、stroke、fill、arc、moveTo、lineTo、setFillStyle、setStrokeStyle、setLineWidth、setFontSize 等。绘制完成后需调用 **ctx.draw()**（或 draw(reserve, callback)）将内容绘制到 canvas 上。各端对 draw 的调用时机有要求，详见官方「CanvasContext」文档。

## uni.canvasToTempFilePath(OBJECT)

将当前 canvas 区域导出为临时图片。参数：canvasId、x、y、width、height、destWidth、destHeight、fileType、quality、success 等。需在 **draw() 的回调**中调用，否则可能拿到空白图。自定义组件内需传 componentInstance。

## 其它

- **uni.canvasGetImageData** / **uni.canvasPutImageData**：获取/设置画布像素数据。部分平台支持。
- 使用 canvas 时注意层级：canvas 为原生组件，层级较高，覆盖需用 cover-view。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/canvas/createCanvasContext
- https://uniapp.dcloud.net.cn/api/canvas/CanvasContext
- https://uniapp.dcloud.net.cn/api/canvas/canvasToTempFilePath
-->
