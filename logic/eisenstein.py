from fractions import Fraction #分数を扱うクラス
import math #数学の関数のライブラリ

def get_bernoulli(n):
    """ベルヌーイ数 B_n を計算"""
    if n == 0: return Fraction(1, 1)
    def nCr(n, r):
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
    s = Fraction(0)
    for k in range(n):
        s += Fraction(nCr(n + 1, k)) * get_bernoulli(k)
    return -s / Fraction(n + 1)

def sigma_k(n, k_pow):
    """約数関数"""
    s = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            s += i ** k_pow
            if i != n // i:
                s += (n // i) ** k_pow
    return s

def calculate_e4_coeffs(num_terms):
    """
    E_4 のq展開係数を計算してリストで返す
    将来的にここをクラス化して汎用的にします
    """
    k = 4
    bk = get_bernoulli(k)
    factor = Fraction(-2 * k) / bk # E4なら 240 になるはず
    
    coeffs = [1] # 定数項
    for n in range(1, num_terms + 1):
        c = factor * sigma_k(n, k - 1)
        coeffs.append(int(c)) # 整数の場合はintにキャスト
        
    return coeffs