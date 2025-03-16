1 tổng quan dữ liệu


import pandas as pd

# Đọc file CSV
df = pd.read_csv('All_GPUs.csv')

# 1. Thông tin cơ bản
print("Thông tin tổng quan về dữ liệu:")
print(f"Số dòng: {df.shape[0]}")
print(f"Số cột: {df.shape[1]}")
print("\nCác cột trong dữ liệu:")
print(df.columns.tolist())

# 2. Kiểu dữ liệu
print("\nKiểu dữ liệu của các cột:")
print(df.dtypes)

# 3. Giá trị thiếu
print("\nSố lượng giá trị thiếu (NaN) trong mỗi cột:")
print(df.isnull().sum())

# 4. Dữ liệu mẫu
print("\n5 dòng đầu tiên của dữ liệu:")
print(df.head())

# 5. Thống kê cơ bản (các cột số)
print("\nThống kê cơ bản của các cột số:")
print(df.describe())