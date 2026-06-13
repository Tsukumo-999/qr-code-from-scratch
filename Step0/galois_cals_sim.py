import sys
import time
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QSpinBox, QPushButton, QTextEdit, QGroupBox, QFormLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

def generate_galois_tables() -> tuple[list[int], list[int]]:
    """GF(2^8) の指数表(exp)と対数表(log)を生成する"""
    exp = [0] * 256
    log = [0] * 256
    v = 1
    for i in range(255):
        exp[i] = v
        log[v] = i
        v <<= 1
        if v & 0x100:
            v ^= 0x11D
    exp[255] = exp[0]
    return exp, log

def multiply_naive(a: int, b: int) -> int:
    """表を使わず、毎回シフトとXORで乗算を行う（逐次計算版）"""
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11D
        b >>= 1
    return result

class GaloisCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.exp_table, self.log_table = generate_galois_tables()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GF(2^8) 乗算シミュレーター & ベンチマーク")
        self.resize(600, 550)
        
        layout = QVBoxLayout()
        font_mono = QFont("Consolas", 12)

        # --- 入力部 (QGroupBoxで囲む) ---
        input_group = QGroupBox("入力 (0〜255の10進数)")
        form_layout = QFormLayout()

        # 値Aの入力UI
        self.spin_a = QSpinBox()
        self.spin_a.setRange(0, 255)
        self.spin_a.setValue(18)  # 初期値 (0x12)
        self.spin_a.setFont(font_mono)
        self.label_a_hexbin = QLabel()
        self.label_a_hexbin.setFont(font_mono)
        
        row_a = QHBoxLayout()
        row_a.addWidget(self.spin_a)
        row_a.addWidget(self.label_a_hexbin)
        row_a.addStretch()

        # 値Bの入力UI
        self.spin_b = QSpinBox()
        self.spin_b.setRange(0, 255)
        self.spin_b.setValue(52)  # 初期値 (0x34)
        self.spin_b.setFont(font_mono)
        self.label_b_hexbin = QLabel()
        self.label_b_hexbin.setFont(font_mono)

        row_b = QHBoxLayout()
        row_b.addWidget(self.spin_b)
        row_b.addWidget(self.label_b_hexbin)
        row_b.addStretch()

        form_layout.addRow("値 A:", row_a)
        form_layout.addRow("値 B:", row_b)
        input_group.setLayout(form_layout)
        layout.addWidget(input_group)

        # 値が変更されたらリアルタイムでラベルを更新するシグナル接続
        self.spin_a.valueChanged.connect(self.update_labels)
        self.spin_b.valueChanged.connect(self.update_labels)
        self.update_labels() # 初期表示用

        # --- 計算ボタン ---
        self.calc_button = QPushButton("乗算を実行 ＆ ベンチマーク計測")
        self.calc_button.setFont(QFont("Meiryo", 11, QFont.Bold))
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        # --- 結果表示部 ---
        self.result_display = QTextEdit()
        self.result_display.setFont(QFont("Consolas", 11))
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def update_labels(self):
        """スピンボックスの値に合わせて16進数/2進数表記を更新する"""
        val_a = self.spin_a.value()
        val_b = self.spin_b.value()
        self.label_a_hexbin.setText(f"→ Hex: 0x{val_a:02X}  Bin: {val_a:08b}")
        self.label_b_hexbin.setText(f"→ Hex: 0x{val_b:02X}  Bin: {val_b:08b}")

    def multiply_table(self, a: int, b: int) -> int:
        """表を用いた高速な乗算"""
        if a == 0 or b == 0:
            return 0
        return self.exp_table[(self.log_table[a] + self.log_table[b]) % 255]

    def calculate(self):
        a = self.spin_a.value()
        b = self.spin_b.value()
        out = []

        # --- 1. ステップバイステップの計算解説 ---
        out.append(f"【計算ステップ解説】")
        if a == 0 or b == 0:
            out.append("一方の値が0であるため、即座に0を返します。")
            result_val = 0
        else:
            log_a = self.log_table[a]
            log_b = self.log_table[b]
            log_sum_mod = (log_a + log_b) % 255
            result_val = self.exp_table[log_sum_mod]
            
            out.append(f" 1. 対数表参照 : log({a}) = {log_a}, log({b}) = {log_b}")
            out.append(f" 2. 指数の加算 : ({log_a} + {log_b}) % 255 = {log_sum_mod}")
            out.append(f" 3. 指数表参照 : exp({log_sum_mod}) = 0x{result_val:02X} ({result_val})")

        out.append(f"\n【計算結果】\n A × B = 0x{result_val:02X} ({result_val:08b})\n")

        # --- 2. ベンチマーク計測 (10万回ループ) ---
        out.append("-" * 40)
        out.append("【ベンチマークテスト (100,000回実行)】")
        loops = 100000

        # 表を用いた乗算の計測
        start_time = time.perf_counter()
        for _ in range(loops):
            self.multiply_table(a, b)
        table_time = time.perf_counter() - start_time

        # 逐次計算（シフト＆XOR）の計測
        start_time = time.perf_counter()
        for _ in range(loops):
            multiply_naive(a, b)
        naive_time = time.perf_counter() - start_time

        # 倍率の計算
        if table_time > 0:
            speedup = naive_time / table_time
        else:
            speedup = 0.0

        out.append(f" 逐次計算版 (シフト＆XOR): {naive_time:.4f} 秒")
        out.append(f" テーブル版 (Log/Exp参照): {table_time:.4f} 秒")
        out.append(f" → テーブル版は逐次計算版より約 {speedup:.1f} 倍 高速！")

        self.result_display.setText("\n".join(out))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GaloisCalculator()
    window.show()
    sys.exit(app.exec())