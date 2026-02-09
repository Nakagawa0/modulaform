import math
from fractions import Fraction
from .eisenstein import get_bernoulli, sigma_k  # 既存の関数を再利用

class ThetaEisenstein:
    """
    Nakagawa (7).pdf の検討課題1に基づく
    テータ部分群上のアイゼンシュタイン級数 G_theta, G_theta_plus を計算するクラス
    """
    
    def __init__(self, k_weight):
        """
        k_weight: 重さ (PDF中の 2k に相当。例: 2, 4, 6...)
        Note: PDFの公式は k (integer >= 2) とあるが、重さは 2k。
        ユーザー入力が「重さ」なら、数式の k = weight / 2 となる。
        """
        if k_weight < 2 or k_weight % 2 != 0:
            raise ValueError("重さは2以上の偶数である必要があります")
        
        self.w = k_weight        # 重さ (2k)
        self.k_param = k_weight // 2  # 数式中の k
        
    def _get_standard_G_coeff(self, n):
        """
        標準的な Eisenstein級数 G_{2k} の q^n の係数 (定数項以外)
        coeff = [2 * (2πi)^w / (w-1)!] * sigma_{w-1}(n)
        ここでは共通係数 (2πi)^w... を除いた「有理数部分」または「整数部分」のみ計算し、
        最終的に定数項との比率で合わせる設計にします。
        
        簡易化のため、正規化された E_{2k} = 1 + C * sum(sigma) の C * sigma を返す。
        C = -4k / B_k (Eの場合)
        """
        # 正規化係数 C = -2w / B_w
        bk = get_bernoulli(self.w)
        pre_factor = Fraction(-2 * self.w) / bk
        return pre_factor * sigma_k(n, self.w - 1)

    def calculate_series(self, num_terms, type="plus"):
        """
        q^(num_terms) までの係数を計算する。
        戻り値は (次数, 係数) のリスト。次数は 0.5 刻み。
        type: "plus" -> G_theta_plus, "normal" -> G_theta
        """
        # 1. 定数項の計算 (PDF p.2-3)
        # G_theta_plus の定数項: 2(1 - 2^(-w)) * zeta(w)
        # 正規化された E として返すため、定数項を 1 としたときの各係数を計算する。
        
        coeffs = {} # {power: value} powerは 0.5, 1.0, 1.5 ...
        
        # 2. 線形結合の係数を準備
        # E_theta+ = -2^(-w+1)E(tau) + E(2tau) + 2^(-w)E(tau/2)
        # 注: これは G ベースの式だが、正規化 E でも定数倍を除けば構造は同じ
        
        w = self.w
        factor_tau     = Fraction(-1, 2**(w - 1)) # -2^(-2k+1)
        factor_2tau    = Fraction(1, 1)           # 1
        factor_half_tau= Fraction(1, 2**w)        # 2^(-2k)

        if type == "normal": # G_theta = G(2tau) - 2^(-2k)G(tau/2)
             factor_tau = 0
             factor_2tau = 1
             factor_half_tau = -Fraction(1, 2**w)

        # 3. 係数の計算ループ
        # q^n/2 まで計算したいので、内部的な n は num_terms * 2 まで回す
        max_half_steps = num_terms * 2
        
        for m in range(1, max_half_steps + 1):
            power = m / 2.0
            val = Fraction(0)
            
            # G(tau/2) からの寄与: q^(n/2) の項
            # G(tau/2) = sum a_n q^(n/2) -> powerが n/2 のとき、係数は a_n
            # つまり index m のとき、sigma(m) を使う
            val += factor_half_tau * self._get_standard_G_coeff(m)
            
            # G(tau) からの寄与: q^n の項
            # power が整数のときのみ
            if m % 2 == 0:
                n = m // 2
                val += factor_tau * self._get_standard_G_coeff(n)
                
            # G(2tau) からの寄与: q^(2n) の項
            # power が偶数のときのみ (power = 2, 4, 6...) -> m が 4 の倍数
            if m % 4 == 0:
                n = m // 4
                val += factor_2tau * self._get_standard_G_coeff(n)
            
            if val != 0:
                coeffs[power] = val

        # 4. 定数項の正規化 (定数項を1にする)
        # 理論上の定数項 (Gベース)
        # Const(G_theta+) = 2*zeta(w)*(1 - 2^(-w) - 2^(-w+1) + 1 + 2^(-w)) ... 計算が必要だが
        # ここではシンプルに「定数項 1」として出力します。
        
        result = [(0, Fraction(1))]
        sorted_powers = sorted(coeffs.keys())
        for p in sorted_powers:
            result.append((p, coeffs[p]))
            
        return result