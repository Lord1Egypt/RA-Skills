import argparse
import requests
import json
import time
import math
import re

def get_transcript(accession):
    if not accession: return None
    print(f"Fetching sequence for {accession}...")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text"
    for _ in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                return "".join(lines[1:])
        except:
            time.sleep(1)
    return None

def get_exon_junctions(accession):
    print(f"Fetching exon annotation for {accession}...")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=gb&retmode=text"
    junctions = []
    for _ in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current_end = 0
                for line in lines:
                    if line.strip().startswith('exon'):
                        # Simplified parsing of GenBank exon feature
                        match = re.search(r"(\d+)\.\.(\d+)", line)
                        if match:
                            start, end = match.groups()
                            if current_end > 0:
                                junctions.append(int(current_end))
                            current_end = int(end)
                return junctions
        except:
            time.sleep(1)
    return junctions

def map_homolog_junctions(target_seq, homolog_acc):
    """
    Professional-grade homology mapping: Uses multiple anchor points 
    around each known junction to find reliable mapping in target.
    """
    print(f"Mapping homolog junctions from {homolog_acc} to target...")
    homolog_seq = get_transcript(homolog_acc)
    if not homolog_seq: return []
    
    h_juncs = get_exon_junctions(homolog_acc)
    target_juncs = []
    
    for j in h_juncs:
        found_j = False
        # Try different window sizes and offsets for robustness
        for win_size in [20, 15, 25]:
            if j - win_size < 0 or j + win_size > len(homolog_seq): continue
            anchor = homolog_seq[j-win_size : j+win_size]
            idx = target_seq.find(anchor)
            if idx != -1:
                target_juncs.append(idx + win_size)
                found_j = True
                break
        
        if not found_j:
            # Try splitting anchor into left and right halves
            left_anchor = homolog_seq[j-20 : j]
            right_anchor = homolog_seq[j : j+20]
            idx_l = target_seq.find(left_anchor)
            idx_r = target_seq.find(right_anchor)
            if idx_l != -1 and idx_r != -1 and 0 < (idx_r - (idx_l + 20)) < 1000:
                # Intron detected! The junction is the end of the left exon
                target_juncs.append(idx_l + 20)
    
    return sorted(list(set(target_juncs)))

def calculate_tm_nn(seq):
    if not seq: return 0
    # SantaLucia (1998) parameters
    nn_data = {
        'AA': (-7.9, -22.2), 'TT': (-7.9, -22.2), 'AT': (-7.2, -20.4), 'TA': (-7.2, -21.3),
        'CA': (-8.5, -22.7), 'TG': (-8.5, -22.7), 'GT': (-8.4, -22.4), 'AC': (-8.4, -22.4),
        'CT': (-7.8, -21.0), 'AG': (-7.8, -21.0), 'GA': (-8.2, -22.2), 'TC': (-8.2, -22.2),
        'CG': (-10.6, -27.2), 'GC': (-9.8, -24.4), 'GG': (-8.0, -19.9), 'CC': (-8.0, -19.9)
    }
    h, s = 0.2, -5.7
    seq = seq.upper()
    for i in range(len(seq) - 1):
        dinuc = seq[i:i+2]
        if dinuc in nn_data:
            dh, ds = nn_data[dinuc]
            h += dh
            s += ds
    if seq[0] in 'AT': h += 2.2; s += 6.9
    if seq[-1] in 'AT': h += 2.2; s += 6.9
    s += 0.368 * (len(seq) - 1) * math.log(0.05)
    tm = (1000 * h) / (s + 1.987 * math.log(0.0000002 / 4.0)) - 273.15
    return round(float(tm), 1)

def rev_comp(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join([complement.get(b, 'N') for b in seq[::-1]])

def check_self_dimer(seq):
    rc = rev_comp(seq)
    for length in range(4, 7):
        for i in range(len(seq) - length + 1):
            if seq[i:i+length] in rc: return True
    return False

def check_3prime_quality(seq):
    last_5 = seq[-5:]
    gc_count = last_5.count('G') + last_5.count('C')
    return gc_count <= 3 # Standard Rule

def check_3prime_mismatch(primer_seq, off_target_seq):
    """
    Prevents 3' end mispriming on unwanted transcripts.
    """
    if not off_target_seq: return True
    # If the last 8-10 bp match perfectly, it might misprime
    anchor = primer_seq[-10:]
    if anchor in off_target_seq: return False
    return True

def spans_exon_junction(start, end, junctions):
    """
    Strict junction check: The junction must be at least 5bp away 
    from either end of the primer for stable annealing.
    """
    for j in junctions:
        if start + 5 <= j <= end - 5: return True
    return False

def design_assay(target_seq, offtarget_seq=None, junctions=None, amplicon_range=(70, 150)):
    candidates = []
    seq_len = len(target_seq)
    if not junctions: junctions = []
    
    for f in range(20, seq_len - amplicon_range[1] - 30):
        for f_len in range(18, 24):
            f_seq = target_seq[f : f+f_len]
            f_tm = calculate_tm_nn(f_seq)
            if 58 <= f_tm <= 62:
                if check_3prime_quality(f_seq) and not check_self_dimer(f_seq):
                    if check_3prime_mismatch(f_seq, offtarget_seq):
                        for r_len in range(18, 24):
                            for r in range(f + amplicon_range[0], f + amplicon_range[1]):
                                if r + r_len > seq_len: break
                                r_seq = rev_comp(target_seq[r : r+r_len])
                                r_tm = calculate_tm_nn(r_seq)
                                if 58 <= r_tm <= 62 and abs(f_tm - r_tm) <= 2.0:
                                    if check_3prime_quality(r_seq) and not check_self_dimer(r_seq):
                                        if check_3prime_mismatch(r_seq, offtarget_seq):
                                            
                                            # gDNA Check
                                            is_safe = False
                                            if not junctions: is_safe = True
                                            else:
                                                if spans_exon_junction(f, f+f_len, junctions) or spans_exon_junction(r, r+r_len, junctions):
                                                    is_safe = True
                                            
                                            if is_safe:
                                                # TaqMan Probe Design
                                                best_probe = None
                                                for p_len in range(20, 30):
                                                    for p in range(f + f_len + 5, r - 5):
                                                        if p + p_len > r: break
                                                        p_seq = target_seq[p : p+p_len]
                                                        p_tm = calculate_tm_nn(p_seq)
                                                        # Probe Tm must be 8-10C higher than primers
                                                        if f_tm + 8 <= p_tm <= 72:
                                                            if p_seq[0] != 'G' and 'GGGG' not in p_seq:
                                                                best_probe = {"seq": p_seq, "tm": p_tm}
                                                                break
                                                    if best_probe: break
                                                
                                                candidates.append({
                                                    "Amplicon": f"{r + r_len - f}bp",
                                                    "F_Primer": {"seq": f_seq, "tm": f_tm},
                                                    "R_Primer": {"seq": r_seq, "tm": r_tm},
                                                    "Probe": best_probe
                                                })
                                                if len(candidates) >= 3: return candidates
    return candidates

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--homolog")
    parser.add_argument("--offtarget")
    args = parser.parse_args()
    
    target_seq = get_transcript(args.target)
    offtarget_seq = get_transcript(args.offtarget)
    
    if target_seq:
        junctions = []
        if args.homolog:
            junctions = map_homolog_junctions(target_seq, args.homolog)
        else:
            junctions = get_exon_junctions(args.target)
        
        print(f"Searching with {len(junctions)} junctions...")
        results = design_assay(target_seq, offtarget_seq, junctions)
        print(json.dumps(results, indent=2))
