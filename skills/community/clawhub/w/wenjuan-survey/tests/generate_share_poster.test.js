"use strict";

const assert = require("assert");
const fs = require("fs").promises;
const os = require("os");
const path = require("path");
const sharp = require("sharp");
const {
  POSTER_TEMPLATES,
  OUTPUT_WIDTH,
  OUTPUT_HEIGHT,
  generateSharePoster,
  wrapTitle,
} = require("../scripts/generate_share_poster");

async function main() {
  assert.equal(POSTER_TEMPLATES.length, 4);
  assert.equal(OUTPUT_WIDTH, 900);
  assert.equal(OUTPUT_HEIGHT, 1350);
  assert.deepEqual(wrapTitle("大学生恋爱观调查", 20, 2), ["大学生恋爱观调查"]);
  assert.equal(wrapTitle("这是一个非常长的项目标题用于测试自动换行效果", 8, 2).length, 2);

  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "wenjuan-poster-"));
  try {
    for (const template of POSTER_TEMPLATES) {
      const output = path.join(dir, `${template.id}.png`);
      await generateSharePoster({
        title: "大学生恋爱观与情感现状调查",
        surveyLink: "https://www.wenjuan.com/s/test/",
        projectId: "test",
        outputPath: output,
        templatePath: template.path,
      });
      const metadata = await sharp(output).metadata();
      assert.equal(metadata.width, OUTPUT_WIDTH, template.id);
      assert.equal(metadata.height, OUTPUT_HEIGHT, template.id);
    }

    const randomOutput = path.join(dir, "random.png");
    await generateSharePoster({
      title: "随机模板测试",
      surveyLink: "https://www.wenjuan.com/s/test/",
      outputPath: randomOutput,
    });
    const randomMeta = await sharp(randomOutput).metadata();
    assert.equal(randomMeta.width, OUTPUT_WIDTH);
    assert.equal(randomMeta.height, OUTPUT_HEIGHT);
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
}

main()
  .then(() => console.log("share poster generation test passed"))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
