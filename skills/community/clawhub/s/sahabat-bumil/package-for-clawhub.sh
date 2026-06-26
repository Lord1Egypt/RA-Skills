#!/bin/bash
# Package Sahabat Bumil for ClawHub submission

echo "🤰 Packaging Sahabat Bumil for ClawHub..."
echo ""

# Create package directory
PACKAGE_DIR="sahabat-bumil-clawhub"
rm -rf $PACKAGE_DIR
mkdir -p $PACKAGE_DIR

# Copy essential files
cp SKILL.md $PACKAGE_DIR/
cp README.md $PACKAGE_DIR/
cp manifest.json $PACKAGE_DIR/
cp VERSION $PACKAGE_DIR/ 2>/dev/null || echo "1.0.0" > $PACKAGE_DIR/VERSION
cp requirements.txt $PACKAGE_DIR/ 2>/dev/null || echo "requests>=2.28.0" > $PACKAGE_DIR/requirements.txt

# Copy src directory
cp -r src $PACKAGE_DIR/

# Remove Python cache
find $PACKAGE_DIR -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find $PACKAGE_DIR -type f -name "*.pyc" -delete 2>/dev/null

# Create LICENSE file if not exists
if [ ! -f LICENSE ]; then
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Bowo (Fajrizky)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
fi

cp LICENSE $PACKAGE_DIR/

# Create package manifest
cat > $PACKAGE_DIR/manifest.json << 'EOF'
{
  "name": "sahabat-bumil",
  "version": "1.0.0",
  "description": "Indonesian Pregnancy Guide - Nutrition, wellness, and support for Indonesian moms",
  "author": "Bowo (Fajrizky) <dev.fajrizky@gmail.com>",
  "category": "Health & Wellness",
  "tags": ["pregnancy", "indonesian", "nutrition", "mom", "baby", "bumil", "kehamilan", "health", "young-mom"],
  "license": "MIT",
  "repository": "https://github.com/defzky/openclaw-sahabat-bumil",
  "requirements": ["requests>=2.28.0"],
  "features": [
    "Indonesian foods safe for pregnancy",
    "Traditional Indonesian recipes",
    "Morning sickness management",
    "Young mom nutrition (age 22-30)",
    "Warung/restaurant safety guide",
    "Pregnancy tracking",
    "Hospital bag checklist",
    "BPJS coverage guide",
    "Financial planning for Indonesian hospitals"
  ]
}
EOF

# Create zip package
cd $PACKAGE_DIR
zip -r ../sahabat-bumil-v1.0.0.zip .
cd ..

echo ""
echo "✅ Package created successfully!"
echo ""
echo "📦 Package: sahabat-bumil-v1.0.0.zip"
echo "📁 Directory: $PACKAGE_DIR/"
echo ""
echo "📊 Package Contents:"
ls -lh sahabat-bumil-v1.0.0.zip
echo ""
echo "🚀 Next Steps:"
echo "1. Upload sahabat-bumil-v1.0.0.zip to ClawHub"
echo "   Visit: https://clawhub.com"
echo "   → Submit Skill"
echo "   → Upload file"
echo ""
echo "2. Or via CLI (if available):"
echo "   openclaw skill submit sahabat-bumil-v1.0.0.zip"
echo ""
echo "3. Wait for approval (1-3 days)"
echo ""
echo "💕 Good luck with your submission!"
echo ""
