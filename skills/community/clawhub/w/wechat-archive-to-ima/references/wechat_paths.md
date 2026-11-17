# 微信 PC 版数据路径参考（实测版）

> 2026-10-06 在 Windows + 微信 4.1.15.13 环境下实测。

## 1. 版本差异对照

| 版本 | 程序目录 | 数据根目录 | 数据库加密 |
|---|---|---|---|
| 微信 3.x（旧） | `Program Files\Tencent\WeChat\` | `<用户主目录>\Documents\WeChat Files\<微信号>\` | AES-128-CBC |
| 微信 4.x（新） | `Program Files\Tencent\Weixin\` | **`<用户主目录>\xwechat_files\<微信号>_<hash>\`** | SQLCipher 4 (AES-256-CBC) |

## 2. 4.x 真实目录结构（实测）

```
<用户主目录>\xwechat_files\<微信号>_<hash>\
├── apm_record\      （APM 性能监控，忽略）
├── business\        （业务数据）
├── cache\           （运行时缓存）
├── config\          （账号配置）
├── db_storage\      （★ 加密数据库：message_*.db、contact.db）
├── msg\              （★ 附件）
│   ├── attach\<hash>\   ← 230 个联系人/群，每个 hash 目录是一个人
│   │   ├── xxx.dat         （V2 头图片，--decrypt 可解）
│   │   ├── xxx.jpg         （明文图片）
│   │   ├── xxx.mp4         （明文视频）
│   │   └── xxx.pdf/docx    （文档）
│   ├── file\YYYY-MM\    ← 文档按月分（通常空，文档实际在 attach 下）
│   ├── video\YYYY-MM\   ← 视频按月分（通常空）
│   └── migrate\         ← 3.x 迁移过来的孤儿文件
├── resource\
└── temp\
```

## 3. 实测数据样例（单个账号目录，路径与账号名均以 `<账号目录>` 占位）

- 总大小：2.38 GB
- 总文件数：4280
- attach 下 hash 目录数：230（即 230 个联系人/群）
- 类型分布：
  - `.dat` 3848 个（V2 头图片，占 90%，可用 wechat_dat_decrypt.py 解出）
  - `.jpg` 208、`.mp4` 93、`.pdf` 49
  - `.pptx` 18、`.docx` 17、`.xlsx` 8、`.md` 3、`.zip` 3
- 时间分布：
  - 2026-04: 790 个
  - 2026-06: 280 个
  - 2026-07: 229 个
  - 2026-08: 1542 个（最多）
  - 2026-09: 912 个
  - 2026-10: 50 个

## 4. 关键事实

1. **数据根目录在用户主目录下，不在 Documents**。这是最容易找错的地方。
2. **附件按 hash 分目录，不是按 wxid 也不是按备注名**。
3. **.dat 是 V2 头图片**（AES-ECB + 尾部异或），本 skill 已支持解密，见 `dat_decryption.md`。
4. **file\YYYY-MM 和 video\YYYY-MM 子目录通常是空的**，因为 4.x 把所有类型都塞在 attach\<hash>\ 下。
5. **db_storage 下是 SQLCipher 4 加密数据库**，不碰。

## 5. 探测脚本逻辑（伪代码）

```python
def detect_wechat_root():
    candidates = [
        Path.home() / "xwechat_files",           # 4.x 默认（★ 最常见）
        Path.home() / "Documents" / "xwechat_files",
        Path.home() / "Documents" / "WeChat Files",  # 3.x
        Path("D:/xwechat_files"),
        Path("D:/WeChat Files"),
    ]
    # 注册表：HKCU\Software\Tencent\Weixin\InstallPath
```

## 6. 附件按类型归类规则

| 扩展名 | 目标分类 |
|---|---|
| .docx .doc .pdf .xlsx .xls .pptx .ppt .txt .md .csv | 01-documents |
| .jpg .jpeg .png .gif .bmp .heic .webp | 02-images |
| .mp4 .mov .avi .mkv | 03-videos |
| .silk .amr .mp3 .wav | 04-voice |
| .dat | 不加 `--decrypt` 跳过并记录；加 `--decrypt` 解出后按真实格式归类 |
| 其他 | 05-misc |

## 7. 常见坑

1. **.dat 要按流程解**。先跑 `wechat_dat_decrypt.py` 拿 code，再 `--decrypt` 归档；
   推导不出来时才退回"微信里点开另存"这条老路。
2. **hash 不是 wxid**。4.x 用了新的 hash 命名，3.x 的目录名是 wxid。
3. **迁移文件**：`<盘符>:\电脑管家迁移文件\微信聊天记录搬家\xwechat_files\` 这种是备份副本，
   不要当主目录用。
4. **自定义路径**：用户可在微信设置 → 文件管理 里改路径，脚本要兼容。
