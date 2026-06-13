"""
GF(2^8) 乗法表 生成手順確認スクリプト
Author: lumenHero
"""

import csv

def export_step_by_step_csv(filename: str = "gf256_steps_visualized.csv") -> None:
    """
    GF(2^8) の指数表生成プロセスにおける、各ステップのビット演算の様子をCSVに出力する。
    """
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # ヘッダー行：各計算フェーズが分かるように詳細化
        writer.writerow([
            "i (αの指数)", 
            "現在の値 (Hex)", 
            "現在の値 (Bin)", 
            "左シフト(<<1)後 (Bin)", 
            "8ビット目あふれ判定", 
            "XOR演算 (0x11D)", 
            "次の値 (Bin)", 
            "次の値 (Hex)"
        ])
        
        v = 1  # 初期値
        
        for i in range(255):
            current_v = v
            # 1. 左シフト (内部的には16ビット以上の整数として扱うため、9ビット目以降も保持される)
            shifted_v = v << 1
            
            # 2. あふれ判定 (0x100 = 256 = 100000000_2)
            overflow = (shifted_v & 0x100) != 0
            
            # --- 表示用のフォーマット処理 ---
            current_hex = f"0x{current_v:02X}"
            current_bin = f"{current_v:08b}"
            
            # シフト後は9ビットで表現して「あふれ」を視覚化する
            shifted_bin = f"{shifted_v:09b}"
            
            if overflow:
                # 3. あふれた場合の処理
                next_v = shifted_v ^ 0x11D
                overflow_str = "あり (>= 256)"
                xor_str = "100011101" # 0x11Dの2進数表現
            else:
                # あふれなかった場合の処理
                next_v = shifted_v
                overflow_str = "なし"
                xor_str = "-"
            
            # 次の値を8ビットに切り揃えてフォーマット
            next_bin = f"{next_v:08b}"
            next_hex = f"0x{next_v:02X}"
            
            # CSVに行を書き込み
            writer.writerow([
                i,
                current_hex,
                current_bin,
                shifted_bin,
                overflow_str,
                xor_str,
                next_bin,
                next_hex
            ])
            
            # 次のループへ値を引き継ぐ
            v = next_v
            
    print(f"手順確認用データを '{filename}' に出力しました。")

if __name__ == "__main__":
    export_step_by_step_csv()