# SYRI 共线性分析技能

用于执行基因组间的 SYRI 共线性和结构变异分析。

## 技能说明

本技能提供完整的 SYRI 共线性分析流程，包括：
- 染色体提取与重命名
- minimap2 比对
- SYRI 结构变异分析
- plotsr 可视化

## 软件安装

### 1. minimap2
```bash
# conda 安装
conda install -c bioconda minimap2

# 或从源码编译
git clone https://github.com/lh3/minimap2.git
cd minimap2 && make
```

### 2. SYRI
```bash
# conda 安装（推荐）
conda install -c bioconda syri

# pip 安装
pip install syri
```

### 3. plotsr
```bash
# conda 安装
conda install -c bioconda plotsr

# pip 安装
pip install plotsr
```

### 4. Biopython（用于染色体处理）
```bash
pip install biopython
```

## 关键发现

### 1. 线程数设置
**重要**：使用 64-120 线程加速分析
```bash
N_THREADS=64  # 根据 CPU 核心数调整
minimap2 -ax asm5 --eqx -t $N_THREADS ref.fa query.fa > output.sam
```

### 2. minimap2 输出缓冲问题
**问题**：minimap2 运行但 SAM 文件始终为 0 字节（进程正在运行）
**原因**：stdout/stderr 输出缓冲导致文件写入延迟
**解决**：使用 stdbuf 禁用输出缓冲
```bash
stdbuf -oL -eL minimap2 -ax asm5 --eqx -t $N_THREADS ref.fa query.fa > output.sam
```

### 3. SAM 文件清理
minimap2 可能输出日志行到文件，需要清理：
```bash
grep -v "^\[" A_vs_Vc.sam > A_vs_Vc_clean.sam
mv A_vs_Vc_clean.sam A_vs_Vc.sam
```

## 标准流程

### 步骤 1：染色体提取与重命名
```python
from Bio.Seq import Seq
from Bio import SeqIO

# 染色体对应关系（根据实际项目调整）
# 格式：(新染色体名称, 原始染色体名称, 是否反向互补)
mapping = [
    ("chr01", "Vcev1_p0.Chr02", True),   # 反向互补
    ("chr02", "Vcev1_p0.Chr11", False),
    # ... 其他染色体
]

src_file = "V_caesariense_W85-20_P0_v2.fasta"
out_file = "Vc_for_SYRI.fa"

records = {rec.id: rec for rec in SeqIO.parse(src_file, "fasta")}

with open(out_file, "w") as f:
    for new_name, old_name, rc in mapping:
        if old_name in records:
            seq = records[old_name].seq
            if rc:
                seq = seq.reverse_complement()
            f.write(f">{new_name}\n")
            f.write(str(seq) + "\n")
            print(f"{new_name} <- {old_name} {'(RC)' if rc else '(direct)'}")
```

### 步骤 2：生成染色体长度文件
```python
from Bio import SeqIO

# Vc.len
with open("Vc.len", "w") as f:
    for rec in SeqIO.parse("Vc_for_SYRI.fa", "fasta"):
        f.write(f"{rec.id}\t{len(rec.seq)}\n")

# A.len
with open("A.len", "w") as f:
    for rec in SeqIO.parse("subgenome_a_renamed.fa", "fasta"):
        f.write(f"{rec.id}\t{len(rec.seq)}\n")
```

### 步骤 3：创建基因组信息文件
```bash
cat > genomes.txt << 'EOF'
#file	name	tags
A.len	A	ft:cl
Vc.len	Vc	ft:cl
EOF
```

### 步骤 4：minimap2 比对
```bash
# 关键参数：
# -ax asm5: 用于长读长的基因组比对
# --eqx: 将 CIGAR 中的 =/X 转换为 M（SYRI 需要）
# -t: 线程数（推荐 64-120）
# stdbuf: 解决输出缓冲问题

N_THREADS=64
stdbuf -oL -eL minimap2 -ax asm5 --eqx -t $N_THREADS \
/path/to/ref.fa \
/path/to/query.fa > A_vs_Vc.sam 2>&1 &

echo "Started minimap2, PID: $!"
# 等待完成（约 10-15 分钟）
```

### 步骤 5：SAM 文件预处理
```bash
# 1. 移除 minimap2 日志行（以 [ 开头的行）
grep -v "^\[" A_vs_Vc.sam > A_vs_Vc_clean.sam
mv A_vs_Vc_clean.sam A_vs_Vc.sam

# 2. 可选：过滤低质量比对（MAPQ >= 20）
awk 'BEGIN {FS="\t"} /^@/ {print; next} $5 >= 20 {print}' A_vs_Vc.sam > A_vs_Vc_filtered.sam
```

### 步骤 6：SYRI 分析
```bash
mkdir -p syri_out

syri -c A_vs_Vc_filtered.sam \
-r /path/to/ref.fa \
-q /path/to/query.fa \
-F S -k --dir syri_out

# 参数说明：
# -c: 比对文件 (SAM/BAM/PAF)
# -r: 参考基因组
# -q: 查询基因组
# -F S: 输入格式为 SAM
# -k: 保留中间文件
```

### 步骤 7：plotsr 可视化
```bash
# 单染色体
plotsr --sr syri_out/syri.out --genomes genomes.txt \
-o output.png --chr chr01 -H 8 -W 10

# 全染色体
plotsr --sr syri_out/syri.out --genomes genomes.txt \
-o output_all.png -H 8 -W 15
```

## 注意事项

### 1. 染色体命名一致性
- SYRI 要求 ref 和 query 的染色体名称和数量完全匹配
- 建议使用统一的命名格式（如 chr01-chr12）

### 2. CIGAR 格式
- SYRI 需要标准化的 CIGAR 字符串（使用 =/X 而非 M）
- 必须使用 `--eqx` 参数

### 3. 输入格式
- SAM 文件必须有正确的格式
- 使用 `-F S` 参数明确指定 SAM 格式

### 4. 内存和存储
- 大型基因组比对会产生很大的 SAM 文件（10-20GB）
- 确保有足够的磁盘空间
- 考虑过滤低质量比对以加速分析

### 5. 线程数选择
- 推荐使用 CPU 核心数的 50%-100%
- 过高线程数可能因内存带宽受限而无法提速

## 错误排查

### 错误：SAM 文件格式问题
```
Error: invalid literal for int() with base 10: '*'
```
解决：确保使用 `-a` 参数生成标准 SAM 格式

### 错误：CIGAR 格式问题
```
Error: Incorrect CIGAR string found
```
解决：添加 `--eqx` 参数

### 错误：染色体长度不匹配
```
Error: length in genome fasta is less than the maximum coordinate
```
解决：检查并确保 genomes.txt 中的长度与实际染色体匹配

### 错误：minimap2 进程运行但文件为 0
```
SAM file size = 0 bytes
```
解决：使用 `stdbuf -oL -eL` 禁用输出缓冲

## 输出文件说明

| 文件 | 说明 |
|------|------|
| syri.out | 结构变异注释（主要结果） |
| syri.vcf | VCF 格式结果 |
| synOut.txt | 共线性区域 |
| invOut.txt | 倒位区域 |
| TLOut.txt | 易位区域 |
| dupOut.txt | 重复区域 |
| snps.txt | SNP 位置 |
| sv.txt | 结构变异位置 |

## 文件位置（示例）

- 工作目录：`/path/to/syri/AVc_v2/`
- SYRI 结果：`syri_out_v2/`
- 图片输出：`/path/to/syri/plots/`