# 安装 TCCLI

**前提**：Python 3 + pip。

```bash
pip install -U tccli tencentcloud-sdk-python   # 必须同时升级 SDK
```

portal 接口要求 `tencentcloud-sdk-python >= 3.1.164`。只装 `tccli` 不升级 SDK，调用时会报 `No module named 'tencentcloud.portal'`，此时执行上面的命令升级即可。

验证：

```bash
tccli --version
python3 -c "import tencentcloud.portal"   # 无报错即可用
```

多次安装失败时，引导用户参照官方文档手动安装：https://cloud.tencent.com/document/product/440/34011
