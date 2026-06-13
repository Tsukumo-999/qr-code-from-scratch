# qr-code-from-scratch

QRコードをゼロからスクラッチしていく記事シリーズ
QRコードを理解する https://tukumolog.com/qr-reed-solomon-crc/
の参考プログラムとして作成しました。

*環境*
python3.12

## Step0 ガロア体の計算の基本
ガロア体の計算について、Step0のフォルダに参考となるプログラムを入れています。
### ガロア体の計算（XOR）
ガロア体における加減算にあたるものはXOR演算です。これはプログラムに書くまでもないのでメモ

### ガロア体の乗法表

精製手順を表記したテーブル作成手順csv

```
python3 generate_galois_tabele_step_by_step.py
```

16進数でのテーブル作成
```
python3 generate_galois_tables.py
```