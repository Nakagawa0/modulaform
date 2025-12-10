from flask import Flask, render_template, request
from logic.eisenstein import calculate_e4_coeffs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    latex_formula = ""
    terms = 5 # デフォルト値

    if request.method == 'POST':
        # フォームからの入力を受け取る
        try:
            terms = int(request.form.get('terms', 5))
        except ValueError:
            terms = 5
        
        # ロジックを呼び出して計算
        coeffs = calculate_e4_coeffs(terms)
        
        # 係数リストを LaTeX 文字列に変換
        parts = ["1"]
        for n, c in enumerate(coeffs[1:], 1):
            parts.append(f"{c}q^{{{n}}}")
        
        latex_formula = "E_4(z) = " + " + ".join(parts) + " + \\cdots"

    return render_template('index.html', formula=latex_formula, current_terms=terms)

if __name__ == '__main__':
    app.run(debug=True)