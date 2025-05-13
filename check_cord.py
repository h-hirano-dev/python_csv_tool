import pandas as pd
import re


def preprocess_code(content):
    """
    content列のコードを前処理して、空白やコメントを除外
    """
    processed = []
    for line in content.splitlines():
        # 前後の空白を削除
        stripped_line = line.strip()
        # 空白行や/**で始まるコメント行をスキップ
        if stripped_line and not stripped_line.startswith("/**"):
            # コメントブロックを削除
            stripped_line = re.sub(r"/\*.*?\*/", "", stripped_line, flags=re.DOTALL)
            # 行内のスペースを削除（必要に応じて）
            processed.append("".join(stripped_line.split()))
    return "\n".join(processed)


def compare_and_export_matching_rows(file1, file2, output_csv):
    """
    2つのCSVファイルを比較し、content列が同じ行を新しいCSVに出力する
    """
    # CSVファイルをデータフレームとして読み込む
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # content列を前処理
    df1["processed_content"] = df1["content"].apply(preprocess_code)
    df2["processed_content"] = df2["content"].apply(preprocess_code)

    # content列が一致する行を取得
    matching_rows = pd.merge(
        df1, df2, on="processed_content", suffixes=("_file1", "_file2")
    )

    # 必要な列を抽出
    matching_rows = matching_rows[
        ["Server_file1", "DB_file1", "FileName_file1", "content_file1"]
    ]
    matching_rows.columns = ["Server", "DB", "FileName", "content"]

    # 結果をCSVに出力
    matching_rows.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"一致する行を {output_csv} に出力しました。")


# 使用例
file1 = "test1.csv"
file2 = "test2.csv"
output_csv_file = "matching_rows.csv"

compare_and_export_matching_rows(file1, file2, output_csv_file)
