# Media Release Package QA

按用户或目标平台提供的明确合同核验媒体交付包。随包示例是一个项目特定的五文件抖音交付合同，不代表平台官方通用规则。校验器只读文件，不会覆盖、移动或晋级任何内容。

## 运行

需要 Python 3 和 `ffprobe`：

```bash
python3 scripts/validate_release_package.py /path/to/package --contract contracts/douyin-five-file.json
python3 scripts/self_test.py
```

修改合同中的必需文件、视频编码/帧率、图片尺寸和音轨规则以符合实际要求；不要把示例约束直接套用到不同发布渠道。通过只说明媒体元数据符合所选合同，不能证明画面质量或平台验收成功。失败时保留用户文件并报告具体字段。

## 内容

- [Skill 指令](SKILL.md)
- [五文件示例合同](contracts/douyin-five-file.json)
- [MIT No Attribution 许可](LICENSE)
- [来源记录](SOURCE-ORIGIN.md)
