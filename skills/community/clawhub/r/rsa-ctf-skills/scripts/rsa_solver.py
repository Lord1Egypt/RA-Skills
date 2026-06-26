#!/usr/bin/env python3
"""
RSA CTF Solver - 集成多种RSA攻击算法
支持11种常见攻击方式，适用于CTF密码学题目
"""

import argparse
import sys
import math
from functools import reduce
import requests

try:
    import gmpy2
    from sympy import sqrt_mod
except ImportError as e:
    print(f"错误: 缺少依赖包 {e.name}")
    print("请安装依赖: pip install gmpy2 sympy")
    sys.exit(1)


# ==================== 工具函数 ====================

def int_nth_root(x, n):
    '''Finds the integer component of the n'th root of x.'''
    high = 1
    while high ** n <= x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid ** n < x:
            low = mid
        elif high > mid and mid ** n > x:
            high = mid
        else:
            return mid
    return mid


def egcd(a, b):
    """扩展欧几里得算法"""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modinv(a, m):
    """模逆运算"""
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m


def crt(items):
    """中国剩余定理"""
    N = reduce(lambda a, b: a * b, [n for c, n in items])
    result = 0
    for c, n in items:
        m = N // n
        inv = modinv(m, n)
        if inv is None:
            return None
        result += c * inv * m
    return result % N, N


def decode_message(m):
    """尝试解码明文"""
    try:
        m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
        # 尝试UTF-8解码
        decoded = m_bytes.decode('utf-8', errors='ignore')
        if decoded.isprintable():
            return decoded
        return m_bytes.hex()
    except:
        return str(m)


# ==================== 攻击算法 ====================

def factorize_factordb(n):
    """使用factordb.com API分解n"""
    try:
        api = "https://factordb.com/api?query="
        response = requests.get(api + str(n), timeout=30)
        if response.status_code != 200:
            return None
        
        data = response.json()
        status = data.get("status", "")
        
        # FF: Fully Factored (完全分解)
        # CF: Composite Factor (部分分解)
        # P: Prime (是素数)
        # U: Unknown (未知)
        if status in ["FF", "CF", "P"]:
            factors = data.get("factors", [])
            if not factors:
                return None
            
            # 收集所有因子
            p_factors = []
            for factor, exp in factors:
                factor_int = int(factor)
                for _ in range(exp):
                    p_factors.append(factor_int)
            
            # 如果有两个因子且乘积等于n，直接返回
            if len(p_factors) >= 2:
                p = p_factors[0]
                q = 1
                for factor in p_factors[1:]:
                    q *= factor
                
                if p * q == n:
                    return p, q
            
            # 如果因子多于2个，尝试合并
            # 找到p和q使得p*q=n
            from itertools import combinations
            for r in range(1, len(p_factors)):
                for combo in combinations(p_factors, r):
                    p_candidate = 1
                    for f in combo:
                        p_candidate *= f
                    q_candidate = n // p_candidate
                    if p_candidate * q_candidate == n and p_candidate > 1 and q_candidate > 1:
                        return p_candidate, q_candidate
            
            return None
        else:
            return None
    except Exception as e:
        return None


def factor_attack(n, e=None, c=None):
    """使用factordb进行分解"""
def factor_attack(n, e=None, c=None):
    """使用factordb进行分解"""
    try:
        if n <= 0:
            raise ValueError("n 必须为正整数")
        
        # 尝试使用factordb分解
        result = factorize_factordb(n)
        if result is None:
            return {'success': False, 'error': 'factordb无法分解n，可能n太大或未在数据库中'}
        
        p, q = result
        
        attack_result = {'success': True, 'p': p, 'q': q, 'source': 'factordb'}
        
        if c is not None and e is not None:
            phi = (p - 1) * (q - 1)
            d = modinv(e, phi)
            if d is not None:
                m = pow(c, d, n)
                attack_result['d'] = d
                attack_result['plaintext'] = decode_message(m)
                attack_result['m'] = m
            else:
                attack_result['warning'] = 'e与phi不互素，无法计算d'
        
        return attack_result
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def small_e_attack(n, e, c):
    """低指数攻击 - 适用于m^e < n"""
    try:
        m, exact = gmpy2.iroot(c, e)
        if pow(int(m), e, n) == c:
            return {
                'success': True,
                'm': int(m),
                'plaintext': decode_message(int(m)),
                'exact': exact
            }
        return {'success': False, 'error': '未找到有效明文 (m^e >= n 或密文不匹配)'}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def common_modulus_attack(n, e1, c1, e2, c2):
    """共模攻击 - 同一n，不同e"""
    try:
        g, s1, s2 = egcd(e1, e2)
        if g != 1:
            return {'success': False, 'error': 'e1和e2必须互质'}

        # 处理负指数
        if s1 < 0:
            inv_c1 = modinv(c1, n)
            if inv_c1 is None:
                return {'success': False, 'error': 'c1模逆不存在'}
            c1 = inv_c1
            s1 = -s1

        if s2 < 0:
            inv_c2 = modinv(c2, n)
            if inv_c2 is None:
                return {'success': False, 'error': 'c2模逆不存在'}
            c2 = inv_c2
            s2 = -s2

        m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
        return {
            'success': True,
            'm': m,
            'plaintext': decode_message(m),
            's1': s1,
            's2': s2
        }
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def d_leak_attack(n, d, c):
    """私钥泄露攻击"""
    try:
        m = pow(c, d, n)
        return {
            'success': True,
            'm': m,
            'plaintext': decode_message(m)
        }
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def wiener_attack(n, e, c=None):
    """Wiener攻击 - 适用于d过小的情况"""
    try:
        def continued_fraction(a, b):
            while b:
                q = a // b
                yield q
                a, b = b, a - q * b

        def convergents(cf):
            n0, d0 = 1, 0
            n1, d1 = cf[0], 1
            yield (n1, d1)
            for q in cf[1:]:
                n2 = q * n1 + n0
                d2 = q * d1 + d0
                yield (n2, d2)
                n0, d0 = n1, d1
                n1, d1 = n2, d2

        cf = list(continued_fraction(e, n))
        for k, d_candidate in convergents(cf):
            if k == 0:
                continue
            phi = (e * d_candidate - 1) // k
            if phi <= 0:
                continue
            s = n - phi + 1
            discr = s * s - 4 * n
            if discr >= 0:
                t = math.isqrt(discr)
                if t * t == discr:
                    p = (s + t) // 2
                    q = (s - t) // 2
                    if p * q == n:
                        result = {
                            'success': True,
                            'd': d_candidate,
                            'p': p,
                            'q': q,
                            'k': k
                        }
                        if c is not None:
                            m = pow(c, d_candidate, n)
                            result['m'] = m
                            result['plaintext'] = decode_message(m)
                        return result
        return {'success': False, 'error': '未找到合适的d，Wiener攻击失败'}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def necpq_attack(p, q, e, c):
    """已知p,q直接解密"""
    try:
        n = p * q
        phi = (p - 1) * (q - 1)
        d = modinv(e, phi)
        if d is None:
            return {'success': False, 'error': '无法计算d，e与phi不互素'}
        m = pow(c, d, n)
        return {
            'success': True,
            'n': n,
            'phi': phi,
            'd': d,
            'm': m,
            'plaintext': decode_message(m)
        }
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def crt_attack(c_list, n_list, e):
    """中国剩余定理广播攻击"""
    try:
        if not (len(c_list) == len(n_list) and len(c_list) >= e):
            return {'success': False, 'error': f'需要至少{e}组密文和模数'}
        
        items = list(zip(c_list, n_list))
        crt_result = crt(items)
        if crt_result is None:
            return {'success': False, 'error': '模数不互素，无法使用CRT'}
        
        C, N = crt_result
        m, exact = gmpy2.iroot(C, e)
        
        if pow(int(m), e, N) == C:
            return {
                'success': True,
                'm': int(m),
                'plaintext': decode_message(int(m)),
                'exact': exact
            }
        return {'success': False, 'error': 'CRT结果验证失败'}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def dp_leak_attack(n, e, c, dp):
    """dp泄露攻击"""
    try:
        for k in range(1, e):
            if (e * dp - 1) % k != 0:
                continue
            p_candidate = (e * dp - 1) // k + 1
            if n % p_candidate == 0 and 1 < p_candidate < n:
                p = p_candidate
                q = n // p
                phi = (p - 1) * (q - 1)
                d = modinv(e, phi)
                if d is None:
                    continue
                m = pow(c, d, n)
                return {
                    'success': True,
                    'p': p,
                    'q': q,
                    'd': d,
                    'k': k,
                    'plaintext': decode_message(m),
                    'm': m
                }
        return {'success': False, 'error': '未能利用dp泄露恢复p'}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def rabin_attack(p, q, c):
    """Rabin密码系统攻击 (e=2)"""
    try:
        if p <= 1 or q <= 1 or p == q:
            return {'success': False, 'error': 'p和q必须是不同的素数且大于1'}
        
        if p % 4 != 3 or q % 4 != 3:
            return {'success': False, 'error': 'p和q必须是模4余3的素数'}
        
        inv_p = gmpy2.invert(p, q)
        inv_q = gmpy2.invert(q, p)
        
        mp = pow(c, (p + 1) // 4, p)
        mq = pow(c, (q + 1) // 4, q)
        n = p * q
        
        # 计算四个可能解
        candidates = [
            (inv_p * p * mq + inv_q * q * mp) % n,
            n - ((inv_p * p * mq + inv_q * q * mp) % n),
            (inv_p * p * mq - inv_q * q * mp) % n,
            n - ((inv_p * p * mq - inv_q * q * mp) % n)
        ]
        
        for candidate in candidates:
            try:
                m_bytes = int(candidate).to_bytes((int(candidate).bit_length() + 7) // 8, 'big')
                decoded = m_bytes.decode('utf-8', errors='ignore')
                if decoded.isprintable():
                    return {
                        'success': True,
                        'plaintext': decoded,
                        'm': int(candidate),
                        'candidates': [int(x) for x in candidates]
                    }
            except:
                continue
        
        return {
            'success': True,
            'plaintext': '未找到可打印明文',
            'candidates': [int(x) for x in candidates]
        }
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def e_power_two_attack(n, e, c):
    """e为2的幂的攻击"""
    try:
        if not ((e & (e - 1)) == 0) or e == 1:
            return {'success': False, 'error': 'e必须是大于1的2的幂次方'}
        
        max_iterations = int(math.log2(e))
        possible = [c]
        
        for _ in range(max_iterations):
            new_possible = []
            for val in possible:
                roots = sqrt_mod(val, n, all_roots=True)
                new_possible.extend(roots)
            possible = list(set(new_possible))
        
        results = []
        for m in possible:
            try:
                m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
                if all(32 <= b < 127 for b in m_bytes):
                    decoded = m_bytes.decode('utf-8', errors='ignore')
                    results.append({'m': m, 'plaintext': decoded})
            except:
                continue
        
        if results:
            return {'success': True, 'results': results}
        return {
            'success': False,
            'error': '未找到可打印明文',
            'all_candidates': [int(x) for x in possible]
        }
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


def non_coprime_e_attack(n, e, c, p, q):
    """e与phi不互素的解密"""
    try:
        phi = (p - 1) * (q - 1)
        t = gmpy2.gcd(e, phi)
        
        if t == 1:
            # 正常解密
            d = modinv(e, phi)
            m = pow(c, d, n)
            return {
                'success': True,
                'note': 'e与phi(n)互素，正常解密',
                'm': m,
                'plaintext': decode_message(m),
                'd': d
            }
        
        # t > 1, 使用修正算法
        d = gmpy2.invert(e // t, phi)
        m2 = pow(c, d, n)
        m, exact = gmpy2.iroot(m2, t)
        
        return {
            'success': True,
            'g': int(t),
            'm2': m2,
            'm': int(m),
            'exact': exact,
            'plaintext': decode_message(int(m)),
            'd': int(d)
        }
    except Exception as ex:
        return {'success': False, 'error': str(ex)}


# ==================== 主程序 ====================

def main():
    parser = argparse.ArgumentParser(
        description='RSA CTF Solver - 集成11种RSA攻击算法',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
攻击类型列表:
  factor          factordb分解
  small_e         低指数攻击 (m^e < n)
  common_modulus  共模攻击
  d_leak          私钥泄露
  wiener          Wiener攻击 (d过小)
  necpq           已知p,q
  crt             中国剩余定理广播攻击
  dp_leak         dp泄露攻击
  rabin           Rabin密码系统 (e=2)
  e_power_two     e为2的幂
  non_coprime_e   e与phi不互素

示例:
  %(prog)s factor --n 123456789 --e 65537 --c 987654321
  %(prog)s small_e --n 123456789 --e 3 --c 987654321
  %(prog)s necpq --p 61 --q 53 --e 17 --c 2790
        """
    )
    
    subparsers = parser.add_subparsers(dest='attack_type', help='攻击类型')
    
    # factor attack
    parser_factor = subparsers.add_parser('factor', help='factordb分解攻击')
    parser_factor.add_argument('--n', required=True, type=int, help='模数n')
    parser_factor.add_argument('--e', type=int, help='公钥指数e')
    parser_factor.add_argument('--c', type=int, help='密文c')
    
    # small_e attack
    parser_small_e = subparsers.add_parser('small_e', help='低指数攻击')
    parser_small_e.add_argument('--n', required=True, type=int, help='模数n')
    parser_small_e.add_argument('--e', required=True, type=int, help='公钥指数e')
    parser_small_e.add_argument('--c', required=True, type=int, help='密文c')
    
    # common_modulus attack
    parser_common = subparsers.add_parser('common_modulus', help='共模攻击')
    parser_common.add_argument('--n', required=True, type=int, help='模数n')
    parser_common.add_argument('--e1', required=True, type=int, help='公钥指数e1')
    parser_common.add_argument('--c1', required=True, type=int, help='密文c1')
    parser_common.add_argument('--e2', required=True, type=int, help='公钥指数e2')
    parser_common.add_argument('--c2', required=True, type=int, help='密文c2')
    
    # d_leak attack
    parser_d_leak = subparsers.add_parser('d_leak', help='私钥泄露攻击')
    parser_d_leak.add_argument('--n', required=True, type=int, help='模数n')
    parser_d_leak.add_argument('--d', required=True, type=int, help='私钥d')
    parser_d_leak.add_argument('--c', required=True, type=int, help='密文c')
    
    # wiener attack
    parser_wiener = subparsers.add_parser('wiener', help='Wiener攻击')
    parser_wiener.add_argument('--n', required=True, type=int, help='模数n')
    parser_wiener.add_argument('--e', required=True, type=int, help='公钥指数e')
    parser_wiener.add_argument('--c', type=int, help='密文c')
    
    # necpq attack
    parser_necpq = subparsers.add_parser('necpq', help='已知p,q解密')
    parser_necpq.add_argument('--p', required=True, type=int, help='素数p')
    parser_necpq.add_argument('--q', required=True, type=int, help='素数q')
    parser_necpq.add_argument('--e', required=True, type=int, help='公钥指数e')
    parser_necpq.add_argument('--c', required=True, type=int, help='密文c')
    
    # crt attack
    parser_crt = subparsers.add_parser('crt', help='中国剩余定理广播攻击')
    parser_crt.add_argument('--c-list', required=True, type=str, help='密文列表，逗号分隔')
    parser_crt.add_argument('--n-list', required=True, type=str, help='模数列表，逗号分隔')
    parser_crt.add_argument('--e', required=True, type=int, help='公钥指数e')
    
    # dp_leak attack
    parser_dp_leak = subparsers.add_parser('dp_leak', help='dp泄露攻击')
    parser_dp_leak.add_argument('--n', required=True, type=int, help='模数n')
    parser_dp_leak.add_argument('--e', required=True, type=int, help='公钥指数e')
    parser_dp_leak.add_argument('--c', required=True, type=int, help='密文c')
    parser_dp_leak.add_argument('--dp', required=True, type=int, help='dp值')
    
    # rabin attack
    parser_rabin = subparsers.add_parser('rabin', help='Rabin密码系统攻击')
    parser_rabin.add_argument('--p', required=True, type=int, help='素数p (p%%4==3)')
    parser_rabin.add_argument('--q', required=True, type=int, help='素数q (q%%4==3)')
    parser_rabin.add_argument('--c', required=True, type=int, help='密文c')
    
    # e_power_two attack
    parser_e_power = subparsers.add_parser('e_power_two', help='e为2的幂的攻击')
    parser_e_power.add_argument('--n', required=True, type=int, help='模数n')
    parser_e_power.add_argument('--e', required=True, type=int, help='公钥指数e (2的幂)')
    parser_e_power.add_argument('--c', required=True, type=int, help='密文c')
    
    # non_coprime_e attack
    parser_non_coprime = subparsers.add_parser('non_coprime_e', help='e与phi不互素解密')
    parser_non_coprime.add_argument('--n', required=True, type=int, help='模数n')
    parser_non_coprime.add_argument('--e', required=True, type=int, help='公钥指数e')
    parser_non_coprime.add_argument('--c', required=True, type=int, help='密文c')
    parser_non_coprime.add_argument('--p', required=True, type=int, help='素数p')
    parser_non_coprime.add_argument('--q', required=True, type=int, help='素数q')
    
    args = parser.parse_args()
    
    if not args.attack_type:
        parser.print_help()
        sys.exit(1)
    
    # 执行对应的攻击
    result = None
    
    if args.attack_type == 'factor':
        result = factor_attack(args.n, args.e, args.c)
    
    elif args.attack_type == 'small_e':
        result = small_e_attack(args.n, args.e, args.c)
    
    elif args.attack_type == 'common_modulus':
        result = common_modulus_attack(args.n, args.e1, args.c1, args.e2, args.c2)
    
    elif args.attack_type == 'd_leak':
        result = d_leak_attack(args.n, args.d, args.c)
    
    elif args.attack_type == 'wiener':
        result = wiener_attack(args.n, args.e, args.c)
    
    elif args.attack_type == 'necpq':
        result = necpq_attack(args.p, args.q, args.e, args.c)
    
    elif args.attack_type == 'crt':
        c_list = [int(x.strip()) for x in args.c_list.split(',')]
        n_list = [int(x.strip()) for x in args.n_list.split(',')]
        result = crt_attack(c_list, n_list, args.e)
    
    elif args.attack_type == 'dp_leak':
        result = dp_leak_attack(args.n, args.e, args.c, args.dp)
    
    elif args.attack_type == 'rabin':
        result = rabin_attack(args.p, args.q, args.c)
    
    elif args.attack_type == 'e_power_two':
        result = e_power_two_attack(args.n, args.e, args.c)
    
    elif args.attack_type == 'non_coprime_e':
        result = non_coprime_e_attack(args.n, args.e, args.c, args.p, args.q)
    
    # 输出结果
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 如果成功且包含明文，额外打印
    if result.get('success') and 'plaintext' in result:
        print(f"\n{'='*50}")
        print(f"明文: {result['plaintext']}")
        print(f"{'='*50}")
    
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
