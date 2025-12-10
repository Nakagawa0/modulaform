import unittest
import sys
import os

# 親ディレクトリをパスに追加して logic フォルダを読み込めるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.eisenstein import calculate_e4_coeffs

class TestEisenstein(unittest.TestCase):
    def test_e4_values(self):
        """E4の係数が正しいかチェック"""
        coeffs = calculate_e4_coeffs(5)
        # 期待される値: 1, 240, 2160, 6720, ...
        self.assertEqual(coeffs[0], 1)
        self.assertEqual(coeffs[1], 240)
        self.assertEqual(coeffs[2], 2160)
        print("テスト成功: E4の係数は正しいです")

if __name__ == '__main__':
    unittest.main()