# import pandas as pd
# from tqdm import tqdm
# import numpy as np
# from pandas import DataFrame, Series
# import json

# # CSVファイルのパス
# csv_file_path1 = "../csv/test1.csv"
# output_csv_file_path = "../csv/grouped_by_name.csv"

# # CSVファイルを読み込んでDataFrameを作成
# test1_df = pd.read_csv(csv_file_path1)

# # 'name'列でグループ化
# grouped_by_name = test1_df.groupby('name')

# # グループ化したデータを新しいDataFrameに変換
# grouped_df = grouped_by_name.apply(lambda x: x)

# # グループ化したデータをCSVファイルに出力
# grouped_df.to_csv(output_csv_file_path, index=False)

# print(f"グループ化したデータをCSVファイルに出力しました: {output_csv_file_path}")


# data = [10, 20, 30, 40, 50]
# index = ['a', 'b', 'c', 'd', 'e']
# series = pd.Series(data, index=index)

# print("Series:")
# print(series)


# # サンプルデータを使用してDataFrameを作成
# data = {
#     'name': ['Alice', 'Bob', 'Charlie'],
#     'score': [85, 90, 95]
# }
# df = pd.DataFrame(data)

# print("DataFrame:")
# print(df)


import os
import re
import csv
from glob import glob

# PHPファイルのディレクトリパス
php_directory_path = "path"
output_csv_file_path = "sql_querieså.csv"

# ディレクトリ内のすべてのPHPファイルを再帰的に検索
php_files = [y for x in os.walk(php_directory_path) for y in glob(os.path.join(x[0], '*.php'))]

# SQL文を抽出する関数
def extract_sql(file_path):
    sql_queries = []
    current_query = []
    inside_function = False

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('function'):
            inside_function = True
            current_query = []
        elif inside_function and (line.startswith('$query =') or line.startswith('$query .=') or line.startswith('$query.=') or line.startswith('$query. =')):
            query_part = re.search(r'["\'](.*?)["\']', line)
            if query_part:
                current_query.append(query_part.group(1))
        elif inside_function and line.startswith('return'):
            inside_function = False
            if current_query:
                sql_queries.append(' '.join(current_query))
    
    return sql_queries

# 結果をCSVファイルに出力
with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['File Path', 'SQL Query'])

    for php_file in php_files:
        sql_queries = extract_sql(php_file)
        for query in sql_queries:
            csvwriter.writerow([php_file, query])

print(f"SQL文をCSVファイルに出力しました: {output_csv_file_path}")