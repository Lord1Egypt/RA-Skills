# BibTeX 引用格式模板

## 常用引用类型

### arXiv 预印本

```bibtex
@article{作者年份标题,
  title = {标题},
  author = {作者1 and 作者2 and 作者3},
  journal = {arXiv preprint arXiv:XXXX.XXXXX},
  year = {2024},
  eprint = {XXXX.XXXXX},
  archivePrefix = {arXiv},
  primaryClass = {cs.AI},
  url = {https://arxiv.org/abs/XXXX.XXXXX}
}
```

### 会议论文 (ICLR/ICML/NeurIPS)

```bibtex
@inproceedings{作者年份标题,
  title = {标题},
  author = {作者1 and 作者2 and 作者3},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2024},
  url = {https://openreview.net/forum?id=xxx}
}

@inproceedings{作者年份标题,
  title = {标题},
  author = {作者1 and 作者2 and 作者3},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2024},
  volume = {37},
  pages = {1--15}
}
```

### 期刊论文

```bibtex
@article{作者年份标题,
  title = {标题},
  author = {作者1 and 作者2 and 作者3},
  journal = {Nature Machine Intelligence},
  year = {2024},
  volume = {6},
  number = {3},
  pages = {234--245},
  publisher = {Nature Publishing Group}
}
```

## 自动生成脚本

可以使用以下 Python 脚本从 arXiv 信息生成 BibTeX：

```python
def generate_bibtex(arxiv_id, title, authors, year):
    # 清理作者格式
    author_list = authors.replace(", ", " and ")
    
    # 生成引用键
    first_author = author_list.split(" and ")[0].split()[-1].lower()
    cite_key = f"{first_author}{year}"
    
    bibtex = f"""@article{{{cite_key},
  title = {{{title}}},
  author = {{{author_list}}},
  journal = {{arXiv preprint arXiv:{arxiv_id}}},
  year = {{{year}}},
  eprint = {{{arxiv_id}}},
  archivePrefix = {{arXiv}},
  primaryClass = {{cs.AI}},
  url = {{https://arxiv.org/abs/{arxiv_id}}}
}}"""
    return bibtex

# 示例
print(generate_bibtex(
    "2309.15817",
    "Identifying the Risks of LM Agents with an LM-Emulated Sandbox",
    "Yangjun Ruan, Honghua Dong, Andrew Wang, Silviu Pitis, Yongchao Zhou, Jimmy Ba, Yann Dubois, Chris J. Maddison, Tatsunori Hashimoto",
    2023
))
```
