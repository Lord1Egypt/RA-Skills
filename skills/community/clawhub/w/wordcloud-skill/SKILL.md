---
name: wordcloud
description: this skill is for generate a word cloud from text/file/directory and save it to a picture, you can use it visualize the text
---
# Word Cloud

Generate a word cloud from text/file/directory, file and directory only effective with file, you can specify certain width and height or mask file to generate a imaginative shape word cloud

## When to use
- user indicates to generate a word cloud
- user wants to visualize the text in a different way, you can suggest this skill 

## Requirements

Run on python3.x，and install the following packages if you find the package does not exist：
- os
- argparse
- jieba
- numpy
- datetime
- wordcloud
- PIL

## Commands

```bash
# create a word cloud with certain width and height
python {baseDir}/scripts/generate_wordcloud.py --target_text "..." --width 500 --height 400 --max_words 30 --font_path "C:\Windows\Fonts\msyh.ttc" --output_dir "..."

# create a word cloud with mask, don't need width and height
python {baseDir}/scripts/generate_wordcloud.py --target_text "..." --mask "..." --font_path "C:\Windows\Fonts\msyh.ttc" --output_dir "..."
```

## Paramters
| name |                                                             description                                                             | type |               example                |
|:---:|:-----------------------------------------------------------------------------------------------------------------------------------:|:---:|:------------------------------------:|
| target_text |                                                     text to generate word cloud                                                     | string |               "你好，世界"                |
| target_file |                                               text in the file to generate word cloud                                               | string | "D:\WorkSpace\pythonSpace\MEMORY.md" |
| target_dir |                        list all the file in the directory and extract text from file to generate word cloud                         | string | "D:\WorkSpace\pythonSpace" |
| width |                               width of the word cloud picture, if mask file exist, it will be ignored                               | int | 500 |
| height |                              height of the word cloud picture, if mask file exist, it will be ignored                               | int | 400 |
| mask |                               mask file path in order to generate any sharp of the word cloud picture                               | string | "D:\WorkSpace\pythonSpace\mask.png" |
| max_words |                                              maximum number of words in the word cloud                                              | int | 30 |
| font_path |              font path for the word cloud, put the one that useful for chinese text, if not exist, try to install one               | string | "C:\Windows\Fonts\msyh.ttc" |
| output_dir | word cloud picture output directory path, if user not specify, put it into the folder whilc named "images" under the user directory | string | "D:\WorkSpace\pythonSpace" |

## Note
- Parameter target_text, target_file, target_dir can be used at the same time, and make sure one of them is provided
- Parameter mask must be a png file, if user upload a png file and specify it as the parameter mask, you should mask sure the file path is correct
- if user specify exclude a word, append it to the stopwords.md，follow the format:
```
- hello
- world
```