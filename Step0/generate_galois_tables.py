"""
GF(2^8) 乗法表（指数表・対数表）生成スクリプト
Author: lumenHero
"""

import csv

def generate_galois_tables() -> tuple[list[int], list[int]]:
    """
    QRコード用のガロア体 GF(2^8) の指数表(exp)と対数表(log)を生成する
    """
    exp = [0] * 256
    log = [0] * 256
    
    # 初期値 V = 1 (α^0 に相当)
    v = 1
    
    for i in range(255):
        exp[i] = v
        # logのインデックスは生成された値 V
        log[v] = i
        
        # V を左に1ビットシフト (x倍する)
        v <<= 1
        
        # 8ビット目があふれたら(256以上になったら)、既約多項式 0x11D で XOR
        if v & 0x100:
            v ^= 0x11D
            
    # α^255 = α^0 = 1 であるため、周期性を持たせるために exp[255] に 1 を入れる
    exp[255] = exp[0]
    
    return exp, log

def export_to_csv(exp: list[int], log: list[int], filename: str = "gf256_tables.csv") -> None:
    """
    生成した表をCSVファイルとして出力する
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # ヘッダー行
        writer.writerow(["Index (Dec)", "Index (Hex)", "Exp Table (α^i)", "Log Table (log_α(i))"])
        
        for i in range(256):
            idx_hex = f"0x{i:02X}"
            
            # 値を16進数文字列にフォーマット（例: 0x45）
            exp_val = f"0x{exp[i]:02X}"
            
            # log[0] は数学的に定義されないため、CSV上でも明示しておく
            if i == 0:
                log_val = "Undefined (0x00)"
            else:
                log_val = f"0x{log[i]:02X}"
                
            writer.writerow([i, idx_hex, exp_val, log_val])
            
    print(f"乗法表を '{filename}' として出力しました。")

if __name__ == "__main__":
    # 1. 表の生成
    exp_table, log_table = generate_galois_tables()
    
    # 2. CSVへの書き出し
    export_to_csv(exp_table, log_table)