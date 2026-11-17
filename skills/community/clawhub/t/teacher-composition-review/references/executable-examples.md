# 批注与成长档案命令样例

以下示例用于验证脚本，不是实际学生作文。执行样例须使用临时目录，不能把样例结果当成用户批改结果。

## 命令与确认门槛

以下命令从本 Skill 所在仓库根目录执行。先用当前平台提供的临时目录能力建立工作目录，并将其绝对路径代入下方的 `<WORK_DIR>`、`<STORE_DIR>` 和 `<RESTORE_STORE>`；这些尖括号名称是待代入的路径占位符，不是要原样执行的环境变量。批注请求中的 `source_image` 与 `output_image` 必须是绝对路径，档案 CLI 的 `--settings`、`--feedback-preferences`、`--review` 和 `import --input` 则可使用 `--store-dir` 内的相对路径。所有档案创建、追加、修正、导入和导出命令只在重新检查 `profile_enabled=true` 后执行。使用 `python3`，并以脚本实际输出的 JSON 为准。

```bash
# 在平台临时目录内准备原图，并把 fixture 改写为使用实际绝对路径的临时请求。
python3 -c "import json; from pathlib import Path; from PIL import Image; d=Path(r'<WORK_DIR>').resolve(); d.mkdir(parents=True, exist_ok=True); source=d/'source.png'; Image.new('RGB', (200, 120), 'white').save(source); request=json.loads(Path('elementary-composition-review/tests/fixtures/annotation-request.json').read_text(encoding='utf-8')); request.update(source_image=str(source), output_image=str(d/'annotated.png')); (d/'annotation-request.json').write_text(json.dumps(request, ensure_ascii=False), encoding='utf-8')"
python3 elementary-composition-review/scripts/render_annotations.py --request "<WORK_DIR>/annotation-request.json"
```

渲染成功后，最终回复必须直接展示脚本实际生成的绝对路径文件，例如 `![第 1 页批注图](<WORK_DIR>/annotated.png)`（展示时将占位符替换为真实绝对路径）；不得只输出路径文本或声称已经生成。

```bash
# <STORE_DIR> 必须是平台临时目录中的绝对路径，并包含全部 JSON 输入。下面提取第 1 条给 append，并生成 review_id 不变的修正版本给 update-review。
python3 -c "import json, shutil; from pathlib import Path; d=Path(r'<STORE_DIR>').resolve(); d.mkdir(parents=True, exist_ok=True); shutil.copyfile('elementary-composition-review/tests/fixtures/profile-updates.json', d/'profile-updates.json'); (d/'settings.json').write_text(json.dumps({'grade_levels':[4], 'revision_level':'moderate', 'comment_style':'gentle', 'ratings':['优秀','良好','合格','待提高'], 'profile_enabled':True, 'privacy_notice_confirmed':True}, ensure_ascii=False), encoding='utf-8'); review=json.loads((d/'profile-updates.json').read_text(encoding='utf-8'))[0]; (d/'review.json').write_text(json.dumps(review, ensure_ascii=False), encoding='utf-8'); review.update(rating='优秀', next_goals=['检查收尾标点']); (d/'updated-review.json').write_text(json.dumps(review, ensure_ascii=False), encoding='utf-8')"
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" settings-set --settings settings.json
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" create --class-name "四年级2班" --student-name "张小明" --grade-level 4 --confirmed
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" append --class-name "四年级2班" --student-name "张小明" --review review.json --confirmed
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" get --class-name "四年级2班" --student-name "张小明"
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" update-review --class-name "四年级2班" --student-name "张小明" --review-id r01 --review updated-review.json --confirmed
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" export --class-name "四年级2班" --student-name "张小明" --output exports/zhang-xiaoming.json
```

在下一次会话恢复便携档案时，先把导出文件复制到新的 `--store-dir` 内，再确认恢复并继续追加；`import` 默认不覆盖同名学生档案，需要替换时才额外加 `--overwrite`：

```bash
python3 -c "import json, shutil; from pathlib import Path; source=Path(r'<STORE_DIR>').resolve(); d=Path(r'<RESTORE_STORE>').resolve(); (d/'imports').mkdir(parents=True, exist_ok=True); shutil.copyfile(source/'exports'/'zhang-xiaoming.json', d/'imports'/'zhang-xiaoming.json'); records=json.loads(Path('elementary-composition-review/tests/fixtures/profile-updates.json').read_text(encoding='utf-8')); (d/'next-review.json').write_text(json.dumps(records[1], ensure_ascii=False), encoding='utf-8')"
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<RESTORE_STORE>" import --input imports/zhang-xiaoming.json --confirmed
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<RESTORE_STORE>" append --class-name "四年级2班" --student-name "张小明" --review next-review.json --confirmed
```

查询到要删除的精确 `review_id` 后，使用以下命令；最后一条会删除整份档案，必须保留显式确认开关：

```bash
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" delete-review --class-name "四年级2班" --student-name "张小明" --review-id r01
python3 elementary-composition-review/scripts/manage_profiles.py --store-dir "<STORE_DIR>" delete-profile --class-name "四年级2班" --student-name "张小明" --confirm-delete
```
