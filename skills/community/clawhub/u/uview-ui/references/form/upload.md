---
name: "upload"
description: "Upload 上传 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Upload 上传 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/upload.html"
---

---

## [#](#upload-上传) Upload 上传 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件用于上传图片场景

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基础用法) 基础用法

-   可以通过设置`fileList`参数(数组，元素为对象)，显示预置的图片。其中元素的`url`属性为图片路径

```
<template>
  <u-upload
    :fileList="fileList1"
    @afterRead="afterRead"
    @delete="deletePic"
    name="1"
    multiple
    :maxCount="10"
  ></u-upload>
</template>

<script>
  export default {
    data() {
      return {
        fileList1: [],
      };
    },
    methods: {

      deletePic(event) {
        this[`fileList${event.name}`].splice(event.index, 1);
      },

      async afterRead(event) {

        let lists = [].concat(event.file);
        let fileListLen = this[`fileList${event.name}`].length;
        lists.map((item) => {
          this[`fileList${event.name}`].push({
            ...item,
            status: "uploading",
            message: "上传中",
          });
        });
        for (let i = 0; i < lists.length; i++) {
          const result = await this.uploadFilePromise(lists[i].url);
          let item = this[`fileList${event.name}`][fileListLen];
          this[`fileList${event.name}`].splice(
            fileListLen,
            1,
            Object.assign(item, {
              status: "success",
              message: "",
              url: result,
            })
          );
          fileListLen++;
        }
      },
      uploadFilePromise(url) {
        return new Promise((resolve, reject) => {
          let a = uni.uploadFile({
            url: "http://192.168.2.21:7001/upload",
            filePath: url,
            name: "file",
            formData: {
              user: "test",
            },
            success: (res) => {
              setTimeout(() => {
                resolve(res.data.data);
              }, 1000);
            },
          });
        });
      },
    },
  };
</script>
```

### [#](#上传视频) 上传视频

-   通过设置`accept='video'`属性，将上传改为视频上传。

```
<u-upload
  :fileList="fileList2"
  @afterRead="afterRead"
  @delete="deletePic"
  name="2"
  multiple
  :maxCount="10"
  accept="video"
></u-upload>

data(){ return{ fileList2: [], } }
```

### [#](#文件预览) 文件预览

-   通过设置`:previewFullImage="true"`属性，达到文件预览的目的。

```
<u-upload
  :fileList="fileList3"
  @afterRead="afterRead"
  @delete="deletePic"
  name="3"
  multiple
  :maxCount="10"
  :previewFullImage="true"
></u-upload>

data(){ return{ fileList3: [{ url: 'https://uviewui.com/swiper/1.jpg', }], } }
```

### [#](#隐藏上传按钮) 隐藏上传按钮

-   上传数量等于`maxCount`所规定的数据时，隐藏上传按钮。

```
<u-upload
  :fileList="fileList4"
  @afterRead="afterRead"
  @delete="deletePic"
  name="4"
  multiple
  :maxCount="2"
></u-upload>

data(){ return{ fileList4: [{ url: 'https://uviewui.com/swiper/1.jpg', }, { url:
'https://uviewui.com/swiper/1.jpg', } ], } }
```

### [#](#限制上传数量) 限制上传数量

-   同上，规定`maxCount`的数据时。

```
<u-upload
  :fileList="fileList5"
  @afterRead="afterRead"
  @delete="deletePic"
  name="5"
  multiple
  :maxCount="3"
></u-upload>

data(){ return{ fileList5: [], } }
```

### [#](#自定义上传样式) 自定义上传样式

-   添加`image`以自定义上传样式，达到身份证，银行卡等不同场景需求。

```
<u-upload
  :fileList="fileList6"
  @afterRead="afterRead"
  @delete="deletePic"
  name="6"
  multiple
  :maxCount="1"
  width="250"
  height="150"
>
  <image
    src="https://uviewui.com/demo/upload/positive.png"
    mode="widthFix"
    style="width: 250px;height: 150px;"
  ></image>
</u-upload>

data(){ return{ fileList6: [], } }
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsB/upload/upload.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsB/upload/upload.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| accept | 接受的文件类型，`file`只支持`H5`（只有微信小程序才支持把 accept 配置为 all、media） | String | image | all | media | image | file | video |
| capture | 图片或视频拾取模式，当 accept 为 image 类型时，设置 capture 为 camera 可以直接调起摄像头 | String | Array | \['album', 'camera'\] | \- |
| compressed | 当 accept 为 video 时生效，是否压缩视频，默认为 true | Boolean | true | false |
| camera | 当 accept 为 video 时生效，可选值为 back 或 front | String | back | \- |
| maxDuration | 当 accept 为 video 时生效，拍摄视频最长拍摄时间，单位秒 | Number | 60 | true |
| uploadIcon | 上传区域的图标，只能内置图标 | String | camera-fill | \- |
| uploadIconColor | 上传区域的图标的颜色 | String | #D3D4D6 | \- |
| useBeforeRead | 是否启用(显示/隐藏)组件 | Boolean | false | true |
| previewFullImage | previewFullImage | Boolean | true | false |
| maxCount | 最大选择图片的数量 | String | Number | 52 | \- |
| disabled | 是否启用(显示/隐藏)组件 | Boolean | false | true |
| imageMode | 预览上传的图片时的裁剪模式，和 image 组件 mode 属性一致 | String | aspectFill | \- |
| name | 标识符，可以在回调函数的第二项参数中获取 | String | file | \- |
| sizeType | original 原图，compressed 压缩图，默认二者都有，H5 无效 | Array<String> | \['original', 'compressed'\] | \- |
| multiple | 是否开启图片多选，部分安卓机型不支持 | Boolean | false | true |
| deletable | 是否显示删除图片的按钮 | Boolean | true | false |
| maxSize | 选择单个文件的最大大小，单位 B(byte)，默认不限制 | String | Number | Number.MAX\_VALUE | \- |
| fileList | 显示已上传的文件列表 | Array | \- | \- |
| uploadText | 上传区域的提示文字 | String | \- | \- |
| width | 内部预览图片区域和选择图片按钮的区域宽度，单位 rpx，不能是百分比，或者`auto` | String | Number | 80 | \- |
| height | 内部预览图片区域和选择图片按钮的区域高度，单位 rpx，不能是百分比，或者`auto` | String | Number | 80 | \- |
| previewImage | 是否在上传完成后展示预览图 | Boolean | true | false |

### [#](#methods) Methods

此方法如要通过 ref 手动调用

| 名称 | 说明 |
| --- | --- |
| afterRead | 读取后的处理函数 |
| beforeRead | 读取前的处理函数 |

### [#](#slot) Slot

slot 中您可以内置任何您所需要的样式。

| 名称 | 说明 |
| --- | --- |
| \-(default) | 自定义上传样式 |

### [#](#events) Events

回调参数中的`event`参数，为当前删除元素的所有信息，`index`为当前操作的图片的索引，`name`为删除名称，`file`包含删除的 url 信息

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| afterRead | 读取后的处理函数 | (file, lists, name)，错误信息 |
| beforeRead | 读取前的处理函数 | (file, lists, name)，错误信息 |
| oversize | 图片大小超出最大允许大小 | (file, lists, name), name 为通过`props`传递的`index`参数 |
| clickPreview | 全屏预览图片时触发 | (url, lists, name)，url 为当前选中的图片地址，index 为通过`props`传递的`index`参数 |
| delete | 删除图片 | (event), 回调 event 中包含`index，file，name` |

← [NumberBox 步进器](https://www.uviewui.com/components/numberBox.html) [Code 验证码输入框](https://www.uviewui.com/components/code.html) →


