# Ai Game Art Generation - Validations

## Hardcoded Api Key

### **Id**
hardcoded-api-key
### **Pattern**
(?:api[_-]?key|secret|token)\s*[=:]\s*["'][a-zA-Z0-9_-]{20,}["']
### **Severity**
critical
### **Message**
Hardcoded API key detected - use environment variables
### **Fix**
Move to .env file: STABILITY_API_KEY=your_key_here
### **Applies To**
  - *.py
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - api_key = "sk-1234567890abcdefghijklmnop"
    - STABILITY_KEY: "abcd1234567890efghijklmn"
  #### **Should Not Match**
    - api_key = os.environ.get("STABILITY_API_KEY")
    - const key = process.env.API_KEY

## No Seed In Batch

### **Id**
no-seed-in-batch
### **Pattern**
batch.*generate|generate.*batch(?!.*seed)
### **Severity**
warning
### **Message**
Batch generation without seed documentation - results won't be reproducible
### **Fix**
Document or lock seeds for reproducibility: seed=42
### **Applies To**
  - *.py
  - *.js
### **Test Cases**
  #### **Should Match**
    - batch_generate(prompts, count=100)
    - generate_batch(images, num=50)
  #### **Should Not Match**
    - batch_generate(prompts, count=100, seed=42)
    - generate_batch(images, seed=12345)

## No License Comment

### **Id**
no-license-comment
### **Pattern**
(?:midjourney|stability|dall-?e|openai|replicate).*(?:api|client)
### **Severity**
info
### **Message**
AI service usage detected - ensure license compliance documented
### **Fix**
Add comment documenting license tier and commercial rights
### **Applies To**
  - *.py
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - stability_client = StabilityClient()
    - midjourney_api.generate()
  #### **Should Not Match**
    - # Licensed under Stability AI Pro tier for commercial use

## Missing Background Removal

### **Id**
missing-background-removal
### **Pattern**
generate.*sprite|sprite.*generat(?!.*background|.*transparent|.*alpha)
### **Severity**
warning
### **Message**
Sprite generation without background removal - ensure transparency
### **Fix**
Add background removal node or use alpha channel output
### **Applies To**
  - *.py
  - *.json
### **Test Cases**
  #### **Should Match**
    - generate_sprite(prompt)
    - sprite_generator.create()
  #### **Should Not Match**
    - generate_sprite(prompt, transparent=True)
    - sprite_generator.create(background_removal=True)

## No Quality Check

### **Id**
no-quality-check
### **Pattern**
save.*asset|export.*image(?!.*review|.*quality|.*check)
### **Severity**
info
### **Message**
Asset export without quality check step
### **Fix**
Add human review before final export to catch AI artifacts
### **Applies To**
  - *.py
  - *.js
### **Test Cases**
  #### **Should Match**
    - save_asset(image, path)
    - export_image(generated)
  #### **Should Not Match**
    - save_asset(image, path) # Manual review required
    - if quality_check(image): export_image(generated)

## Negative Prompt Missing

### **Id**
negative-prompt-missing
### **Pattern**
prompt\s*=\s*["'][^"']+["'](?!.*negative)
### **Severity**
info
### **Message**
Generation without negative prompt - may produce artifacts
### **Fix**
Add negative_prompt for anatomy/quality: 'extra fingers, blurry, watermark'
### **Applies To**
  - *.py
  - *.json
### **Test Cases**
  #### **Should Match**
    - prompt = "fantasy warrior character"
  #### **Should Not Match**
    - prompt = "warrior", negative_prompt = "bad anatomy"

## Resolution Not Power Of Two

### **Id**
resolution-not-power-of-two
### **Pattern**
resolution|size|dimensions.*=.*(?:100|150|200|300|500|600|700|900)[^0-9]
### **Severity**
warning
### **Message**
Non-power-of-2 resolution may cause issues with game engines
### **Fix**
Use power of 2: 256, 512, 1024, 2048
### **Applies To**
  - *.py
  - *.json
  - *.yaml
### **Test Cases**
  #### **Should Match**
    - resolution = 500
    - size: 300
  #### **Should Not Match**
    - resolution = 512
    - size: 1024

## No Vae Decode Tiled

### **Id**
no-vae-decode-tiled
### **Pattern**
VAEDecode(?!.*tiled)
### **Severity**
info
### **Message**
VAE decode without tiling may cause VRAM issues at high resolution
### **Fix**
Use VAEDecodeTiled for resolutions above 1024px
### **Applies To**
  - *.json
### **Test Cases**
  #### **Should Match**
    - "class_type": "VAEDecode"
  #### **Should Not Match**
    - "class_type": "VAEDecodeTiled"

## Git Lfs Not Configured

### **Id**
git-lfs-not-configured
### **Pattern**
\.png|\.jpg|\.psd
### **Severity**
warning
### **Message**
Binary asset referenced - ensure Git LFS is configured
### **Fix**
Run: git lfs track '*.png' '*.jpg' '*.psd'
### **Applies To**
  - .gitattributes
### **Test Cases**
  #### **Should Match**
    - character.png
  #### **Should Not Match**
    - *.png filter=lfs

## Training Data Too Small

### **Id**
training-data-too-small
### **Pattern**
train.*(?:images|samples).*(?:[1-9]|1[0-4])[^0-9]
### **Severity**
warning
### **Message**
Training dataset may be too small - need 15-30 for characters, 30-50 for styles
### **Fix**
Increase training dataset or verify quality over quantity
### **Applies To**
  - *.py
  - *.yaml
### **Test Cases**
  #### **Should Match**
    - train_images = 10
    - samples: 5
  #### **Should Not Match**
    - train_images = 30
    - samples: 50

## Steam Disclosure Missing

### **Id**
steam-disclosure-missing
### **Pattern**
steam.*(?:upload|publish|release)(?!.*ai.*disclos|.*content.*survey)
### **Severity**
warning
### **Message**
Steam publishing mentioned - ensure AI content disclosure completed
### **Fix**
Complete Steam Content Survey AI section before submission
### **Applies To**
  - *.md
  - *.txt
### **Test Cases**
  #### **Should Match**
    - upload to steam
    - steam publish
  #### **Should Not Match**
    - steam upload (AI disclosure completed)