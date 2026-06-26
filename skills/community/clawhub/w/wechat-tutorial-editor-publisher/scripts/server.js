const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs-extra');
const path = require('path');

const app = express();
const PORT = 3000;

// 基础路径配置
const ASSETS_DIR = path.join(__dirname, '../assets');
const FILES_DIR = path.join(__dirname, '../files');
const PUBLIC_DIR = path.join(__dirname, 'public');

// 确保目录存在
fs.ensureDirSync(ASSETS_DIR);
fs.ensureDirSync(path.join(ASSETS_DIR, 'personal-imgs'));
fs.ensureDirSync(FILES_DIR);

app.use(cors());
app.use(express.json());
app.use(express.static(PUBLIC_DIR));

// 1. 个人信息收集接口
const personalStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(ASSETS_DIR, 'personal-imgs'));
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});
const uploadPersonal = multer({ storage: personalStorage });

app.post('/api/personal-info', uploadPersonal.single('qrCode'), async (req, res) => {
  try {
    const { nickname, intro } = req.body;
    const infoContent = `昵称: ${nickname}\n个人简介: ${intro}\n`;
    await fs.writeFile(path.join(ASSETS_DIR, 'personal-info.txt'), infoContent, 'utf8');
    res.json({ success: true, message: '个人信息保存成功' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: '保存失败' });
  }
});

// 2. 步骤信息保存接口
const stepsStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    // 这里暂时存到临时目录，稍后移动
    const tempDir = path.join(FILES_DIR, 'temp_upload');
    fs.ensureDirSync(tempDir);
    cb(null, tempDir);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});
const uploadSteps = multer({ storage: stepsStorage });

app.post('/api/save-steps', uploadSteps.fields([
  { name: 'coverImage', maxCount: 1 },
  { name: 'stepImages' }
]), async (req, res) => {
  try {
    const { steps: stepsJson } = req.body;
    const stepsData = JSON.parse(stepsJson);
    
    // 生成本地时间目录名: [yyyy-MM-ddTHH-mm-ss]
    const now = new Date();
    const pad = (n) => n.toString().padStart(2, '0');
    const dirName = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`;
    
    const targetDir = path.join(FILES_DIR, dirName);
    const imgsDir = path.join(targetDir, 'imgs');
    
    await fs.ensureDir(imgsDir);

    // 处理头图
    let coverPath = null;
    if (req.files['coverImage'] && req.files['coverImage'][0]) {
      const coverFile = req.files['coverImage'][0];
      const ext = path.extname(coverFile.originalname);
      const targetCoverPath = path.join(imgsDir, `cover-img${ext}`);
      fs.moveSync(coverFile.path, targetCoverPath, { overwrite: true });
      coverPath = path.relative(targetDir, targetCoverPath);
    }

    // 移动图片到目标目录并更新路径
    const files = req.files['stepImages'] || [];
    const updatedSteps = stepsData.map(step => {
      const stepImages = [];
      // 根据 stepNumber 和图片索引重新命名
      step.images.forEach((imgName, index) => {
        const file = files.find(f => f.originalname === imgName);
        if (file) {
          const ext = path.extname(file.originalname);
          const newFileName = `${step.stepNumber}-${index + 1}${ext}`;
          const targetPath = path.join(imgsDir, newFileName);
          fs.moveSync(file.path, targetPath, { overwrite: true });
          // 存储相对路径
          stepImages.push(path.relative(targetDir, targetPath));
        }
      });
      return {
        stepNumber: step.stepNumber,
        description: step.description,
        'images-paths': stepImages
      };
    });

    // 保存 steps.json
    await fs.writeJson(path.join(targetDir, 'steps.json'), { 
      cover: coverPath,
      steps: updatedSteps 
    }, { spaces: 2 });
    
    // 清理临时目录
    const tempDir = path.join(FILES_DIR, 'temp_upload');
    if (await fs.pathExists(tempDir)) {
      await fs.emptyDir(tempDir);
    }

    res.json({ success: true, dirName });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: '保存失败' });
  }
});

app.listen(PORT, () => {
  console.log(`服务器启动在 http://localhost:${PORT}`);
});
