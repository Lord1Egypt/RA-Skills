# Xiamen Tide Calculator

> An intelligent tide calculation skill designed for Xiamen beachcombing enthusiasts, featuring automatic solar-to-lunar date conversion, multi-window analysis, beachcombing scoring, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/kingwingshome/xiamen-tide-calculator/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/Version-v3.2-blue.svg)](https://github.com/kingwingshome/xiamen-tide-calculator)
[![Author](https://img.shields.io/badge/Author-Ke%20Yingjie-green.svg)](https://github.com/kingwingshome)

## 📋 Project Overview

The Xiamen Tide Calculator is an intelligent tool that calculates tide times for Xiamen waters based on lunar calendar dates, designed specifically for beachcombing enthusiasts. It supports automatic solar-to-lunar date conversion, current date recognition, and leap month handling, providing beachcombing scores, location recommendations, equipment suggestions, and safety reminders.

## ✨ Core Features

### 🌊 Tide Calculation
- ✅ Accurate high/low tide time calculation based on lunar calendar dates
- ✅ Automatic tide size classification (spring tide / middle tide / neap tide)
- ✅ Solar-to-lunar date auto-conversion
- ✅ Current date auto-detection
- ✅ Complete leap month handling

### 🎯 Beachcombing Recommendations
- ✅ Intelligent beachcombing scoring system (0-10 points)
- ✅ Multi-window analysis (morning / afternoon / evening / early morning)
- ✅ Detailed pros and cons for each window
- ✅ Recommendation index (⭐⭐⭐-⭐⭐⭐⭐⭐)
- ✅ Integrated window feature (displays all available windows for the day)

### 📊 Smart Recommendations
- ✅ Intelligent beachcombing location recommendations based on tide size
- ✅ Expected harvest tips
- ✅ Season-adapted equipment suggestions
- ✅ Comprehensive safety reminders
- ✅ Multi-day comparison (recommends best beachcombing dates)

## 🚀 Installation

### Method 1: Install via WorkBuddy Skill Market (Recommended)

1. Open the WorkBuddy client
2. Click the "Skills" button at the top, or go to Profile → "Claw Settings" → "SkillHub Store"
3. Search for "Xiamen Tide Calculator"
4. Click "Free Subscribe" to complete installation

### Method 2: Import via Git Repository

1. Visit the GitHub repository: https://github.com/kingwingshome/xiamen-tide-calculator
2. Copy the repository's HTTPS clone URL
3. In WorkBuddy's "Skills Management", click "Import from Git Repository"
4. Paste the repository URL, select a branch, and click "Validate and Import"

### Method 3: Local File Import

1. Download the skill package: `xiamen-tide-calculator-v3.2.skill`
2. In WorkBuddy, go to "Claw Settings" → "Skills Management"
3. Click "Import Skills" and select the downloaded `.skill` file
4. Wait for the import to complete

## 📖 Usage

### Standard Mode: Query Tide Times

```bash
# Use current date
python scripts/tide_calculator.py --today

# Use solar (Gregorian) date
python scripts/tide_calculator.py --solar-date 2025-04-02

# Use lunar date
python scripts/tide_calculator.py --lunar-day 15 --lunar-month 3
```

### Beachcombing Mode: Get Beachcombing Advice

```bash
# Current date beachcombing advice
python scripts/tide_calculator.py --today --beach-mode

# Specific date beachcombing advice
python scripts/tide_calculator.py --solar-date 2025-04-02 --beach-mode

# Integrated window mode (recommended)
python scripts/tide_calculator.py --solar-date 2026-04-05 --beach-mode --integrated
```

### Multi-day Comparison: Choose the Best Beachcombing Date

```bash
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 10
```

## 📁 Project Structure

```
xiamen-tide-calculator/
├── SKILL.md                          # Skill main document
├── README.md                         # Project documentation
├── LICENSE                           # MIT License file
├── 使用说明.md                       # Basic usage guide (Chinese)
├── 新功能使用指南.md                 # New feature guide (Chinese)
├── references/                       # Reference documents directory
│   ├── beachcombing_improvement.md    # Beachcombing improvement plan
│   └── lunar_conversion.md           # Lunar conversion reference
└── scripts/                         # Scripts directory
    ├── tide_calculator.py            # Tide calculation main script
    └── compare_beach_days.py        # Multi-day comparison script
```

## 🎯 Feature Demo

### Tide Query Example

```
【Xiamen Tide · Lunar 2026/2/17】
High Tide 1: 01:36
High Tide 2: 14:00
Low Tide 1: Previous Day 19:24
Low Tide 2: 07:48
Best Beachcombing: 05:48-08:48 (Window 1), 18:12-21:12 (Window 2)
Tide Size: Spring Tide
Beachcombing Score: 9.0 (Highly Recommended)
```

### Beachcombing Advice Example

```
【Xiamen Beachcombing Advice · Lunar 2026/2/17】

🌊 Beachcombing Score: 9.0 (Highly Recommended)

⏰ Best Beachcombing Periods:

  【Window 1】05:48-08:48
  └─ Time Type: Early Morning
  └─ Advantages:
     ✅ Cool temperature, high comfort
     ✅ Best tide retreat, most seafood
     ✅ Quiet environment, great experience
  └─ Notes:
     ❌ Need to wake up very early (3-4 AM)
     ❌ Low light, illumination needed
  └─ ⭐ Recommendation Index: ⭐⭐⭐

  【Window 2】18:12-21:12
  └─ Time Type: Evening
  └─ Advantages:
     ✅ Cool temperature, high comfort
     ✅ Soft light, great for photos
     ✅ Long tide retreat, abundant seafood
  └─ Notes:
     ❌ Getting dark, limited visibility
     ❌ Tide rises quickly, safety caution needed
  └─ ⭐ Recommendation Index: ⭐⭐⭐⭐⭐
```

## 🔧 Tech Stack

- **Language**: Python 3.6+
- **Lunar Conversion**: zhdate library
- **Output Encoding**: UTF-8
- **License**: MIT License

## 📊 Version History

### v3.2 (2026-04-03) - Integrated Window Feature
- ✅ Added integrated window feature, optimized cross-day window display
- ✅ Improved copyright notice and open-source address
- ✅ Skill packaged as `.skill` file

### v3.1 (2026-04-02) - Multi-Window Analysis
- ✅ Multi-window automatic identification
- ✅ Detailed pros and cons for each window
- ✅ Automatic recommendation index

### v3.0 (2026-04-02) - Basic Enhancements
- ✅ Solar-to-lunar date auto-conversion
- ✅ Current date auto-detection
- ✅ Leap month handling

### v2.0 (2026-04-02) - Beachcombing Mode
- ✅ Beachcombing scoring system
- ✅ Location recommendations
- ✅ Equipment suggestions
- ✅ Multi-day comparison

### v1.0 (2026-04-02) - Initial Release
- ✅ Basic tide calculation
- ✅ Tide size classification
- ✅ Beachcombing window calculation

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome!

### How to Contribute
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a Pull Request

### Reporting Issues
- Use GitHub Issues to report bugs
- Provide detailed reproduction steps and environment info
- Include screenshots if possible

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ke Yingjie** - [GitHub](https://github.com/kingwingshome)

## 📞 Contact

- **GitHub**: https://github.com/kingwingshome/xiamen-tide-calculator
- **WorkBuddy**: Feedback via WorkBuddy platform

## ⚠️ Disclaimer

1. **Accuracy Notice**: This skill is based on standard tide calculation formulas for Xiamen waters and is for reference only. Actual tide times may be affected by weather, atmospheric pressure, terrain, and other factors. It is recommended to use it in combination with on-site observation or official tide tables.

2. **Safety Warning**: Beachcombing involves certain risks. Please pay attention to safety:
   - Tide rise speed may exceed expectations
   - Reef surfaces are slippery and may cause falls
   - Marine life may cause injuries
   - Weather changes may bring danger

3. **Limitation of Liability**: Users assume all risks when using this skill for beachcombing activities. The developer is not responsible for any direct or indirect losses arising from the use of this skill.

## ⭐ Star Support

If this project helps you, please give it a ⭐ Star!

---

**Made with ❤️ by Ke Yingjie**
