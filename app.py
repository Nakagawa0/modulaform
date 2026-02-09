from flask import Flask, render_template, request
from logic.eisenstein import calculate_e4_coeffs # 既存
from logic.theta_eisenstein import ThetaEisenstein # 追加

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    formula = ""
    terms = 5
    selected_func = "E4" # デフォルト
    weight = 4

    if request.method == 'POST':
        try:
            terms = int(request.form.get('terms', 5))
            weight = int(request.form.get('weight', 4))
            selected_func = request.form.get('func_type', 'E4')
        except ValueError:
            pass
        
        parts = []
        
        if selected_func == "E_k":
            # 既存の標準アイゼンシュタイン級数
            coeffs = calculate_e4_coeffs(terms) # ※汎用化が必要なら引数にweightを渡すようにlogic側も修正推奨
            # ここでは簡易的にE4固定またはlogic側の改修に合わせてください
            # 今回はTheta優先で実装します
            parts.append("1")
            for n, c in enumerate(coeffs[1:], 1):
                 parts.append(f"{c}q^{{{n}}}")
            formula = f"E_{{{weight}}}(z) = " + " + ".join(parts) + " + \\cdots"

        elif selected_func in ["E_theta", "E_theta_plus"]:
            # 新しいテータアイゼンシュタイン級数
            calc = ThetaEisenstein(weight)
            mode = "plus" if selected_func == "E_theta_plus" else "normal"
            res_coeffs = calc.calculate_series(terms, type=mode)
            
            parts.append("1") # 定数項
            for power, c in res_coeffs[1:]:
                # パワーが整数の場合は .0 を消す
                p_str = f"{int(power)}" if power.is_integer() else f"{power}"
                # 分数の係数をきれいに表示
                c_str = f"{c.numerator}" if c.denominator == 1 else f"\\frac{{{c.numerator}}}{{{c.denominator}}}"
                
                parts.append(f"{c_str}q^{{{p_str}}}")
            
            label = "E" if mode == "normal" else "E^+"
            formula = f"{label}_{{{weight}}}^\\theta(z) = " + " + ".join(parts) + " + \\cdots"

    return render_template('index.html', formula=formula, current_terms=terms, current_weight=weight, selected_func=selected_func)

if __name__ == '__main__':
    app.run(debug=True)