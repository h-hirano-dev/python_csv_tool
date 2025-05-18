import pandas as pd
import re

# 1. test.csvを読み込んでDataFrameにする
input_csv = "test1.csv"
output_csv = "filtered_groups.csv"

try:
    # CSVを読み込む
    df = pd.read_csv(input_csv)

    # 2. content列を加工して不要な改行や空白、/**と**/で囲まれた部分を削除
    def clean_content(content):
        # 改行と空白を削除
        content = re.sub(r'\s+', '', content)
        # /** と **/ で囲まれている箇所を削除
        content = re.sub(r'/\*\*.*?\*\*/', '', content)
        return content

    df['cleaned_content'] = df['content'].apply(clean_content)

    # 3. DB列とFileName列が同じものを抽出し、content列でグループ化
    grouped = df.groupby(['DB', 'FileName', 'cleaned_content'])

    # 4. グループ化した際に、グループが2つ以上あるものを抽出
    filtered = grouped.size().reset_index(name='count')
    filtered = filtered.groupby(['DB', 'FileName']).filter(lambda x: len(x) > 1)

    # 5. 結果をCSVに出力
    filtered.to_csv(output_csv, index=False)
    print(f"結果を {output_csv} に出力しました。")
except Exception as e:
    print(f"エラーが発生しました: {e}")