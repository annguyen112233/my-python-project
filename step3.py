import pandas as pd

# 1. Đọc dữ liệu
df = pd.read_csv('All_GPUs.csv')
print("Thông tin ban đầu:")
print(f"Số dòng: {df.shape[0]}")
print(f"Số cột: {df.shape[1]}")
print("\nCác cột:", df.columns.tolist())

# 2. Xử lý dữ liệu khuyết
# 2.1. Loại bỏ cột có >70% giá trị thiếu
threshold = len(df) * 0.3
df_cleaned = df.dropna(thresh=threshold, axis=1)
print("\nCác cột sau khi loại bỏ (ngưỡng 70%):")
print(df_cleaned.columns.tolist())

# 2.2. Làm sạch và điền giá trị khuyết cho cột số
def clean_numeric_column(value):
    if pd.isna(value):
        return value
    try:
        value = str(value).replace('W', '').replace('MHz', '').replace('MB', '').replace('\n-', '').replace('GB', '').strip()
        return float(value)
    except (ValueError, TypeError):
        return None

numeric_cols_to_clean = ['Max_Power', 'Memory', 'Core_Speed', 'Memory_Bandwidth', 'Memory_Bus', 'Memory_Speed', 'Pixel_Rate', 'Texture_Rate', 'ROPs', 'Process']
for col in numeric_cols_to_clean:
    if col in df_cleaned.columns:
        df_cleaned[col] = df_cleaned[col].apply(clean_numeric_column)

numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].median())
print("\nSố lượng giá trị thiếu sau khi điền cột số:")
print(df_cleaned[numeric_cols].isnull().sum())

# 2.3. Điền giá trị khuyết cho cột phân loại
categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if col != 'Release_Date':
        mode_value = df_cleaned[col].mode()
        if not mode_value.empty:
            df_cleaned[col] = df_cleaned[col].fillna(mode_value[0])
        else:
            df_cleaned[col] = df_cleaned[col].fillna('Unknown')
print("\nSố lượng giá trị thiếu sau khi điền cột phân loại:")
print(df_cleaned[categorical_cols].isnull().sum())

# 3. Xử lý định dạng dữ liệu
# 3.1. Chuyển Release_Date sang datetime
df_cleaned['Release_Date'] = pd.to_datetime(df_cleaned['Release_Date'], errors='coerce')
print("\nSố lượng giá trị thiếu trong Release_Date sau chuyển đổi:")
print(df_cleaned['Release_Date'].isnull().sum())

# 4. Thêm biến
df_cleaned['Release_Year'] = df_cleaned['Release_Date'].dt.year
print("\n5 dòng đầu tiên của Release_Year:")
print(df_cleaned[['Release_Date', 'Release_Year']].head())

# 5. Bớt biến
cols_to_drop = ['Power_Connector', 'L2_Cache']
df_cleaned = df_cleaned.drop(columns=[col for col in cols_to_drop if col in df_cleaned.columns])
print("\nCác cột sau khi loại bỏ thêm:")
print(df_cleaned.columns.tolist())

# 6. Chuyển đổi biến
# 6.1. Mã hóa Manufacturer
df_cleaned['Manufacturer_Encoded'] = df_cleaned['Manufacturer'].map({'Nvidia': 1, 'AMD': 0}).fillna(2)
print("\n5 dòng đầu tiên của Manufacturer và Manufacturer_Encoded:")
print(df_cleaned[['Manufacturer', 'Manufacturer_Encoded']].head())

# 6.2. Chuẩn hóa Max_Power
df_cleaned['Max_Power_Scaled'] = (df_cleaned['Max_Power'] - df_cleaned['Max_Power'].min()) / (df_cleaned['Max_Power'].max() - df_cleaned['Max_Power'].min())
print("\n5 dòng đầu tiên của Max_Power và Max_Power_Scaled:")
print(df_cleaned[['Max_Power', 'Max_Power_Scaled']].head())

