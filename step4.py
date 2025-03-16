import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv('All_GPUs.csv')

# Tiền xử lý dữ liệu
def clean_numeric_column(value):
    if pd.isna(value):
        return value
    try:
        # Xóa các ký tự không phải số
        value = str(value).replace('Watts', '').replace('W', '').replace('MB', '').replace('GB', '').replace('MHz', '').replace('\n-', '').replace(' ', '').strip()
        return float(value) if value else None
    except (ValueError, TypeError):
        return None

# Làm sạch cột Max_Power, Memory, TMUs, Core_Speed
cols_to_clean = ['Max_Power', 'Memory', 'TMUs', 'Core_Speed']
for col in cols_to_clean:
    if col in df.columns:
        df[col] = df[col].apply(clean_numeric_column)
        # Điền giá trị khuyết bằng trung vị
        median_value = df[col].median()
        if pd.isna(median_value):
            print(f"Cảnh báo: Trung vị của {col} là NaN, không thể điền giá trị khuyết.")
        else:
            df[col] = df[col].fillna(median_value)

# Làm sạch Release_Date
df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
df['Release_Year'] = df['Release_Date'].dt.year

# Chuẩn hóa dữ liệu
max_power_min = df['Max_Power'].min()
max_power_max = df['Max_Power'].max()
memory_min = df['Memory'].min()
memory_max = df['Memory'].max()
tmus_min = df['TMUs'].min()
tmus_max = df['TMUs'].max()

if not pd.isna(max_power_max) and not pd.isna(max_power_min) and max_power_max > max_power_min:
    df['Max_Power_Scaled'] = (df['Max_Power'] - max_power_min) / (max_power_max - max_power_min)
else:
    print("Lỗi: Không thể chuẩn hóa Max_Power do dữ liệu không hợp lệ.")
    df['Max_Power_Scaled'] = df['Max_Power']

if not pd.isna(memory_max) and not pd.isna(memory_min) and memory_max > memory_min:
    df['Memory_Scaled'] = (df['Memory'] - memory_min) / (memory_max - memory_min)
else:
    print("Lỗi: Không thể chuẩn hóa Memory do dữ liệu không hợp lệ.")
    df['Memory_Scaled'] = df['Memory']

if not pd.isna(tmus_max) and not pd.isna(tmus_min) and tmus_max > tmus_min:
    df['TMUs_Scaled'] = (df['TMUs'] - tmus_min) / (tmus_max - tmus_min)
else:
    print("Lỗi: Không thể chuẩn hóa TMUs do dữ liệu không hợp lệ.")
    df['TMUs_Scaled'] = df['TMUs']

# 1. Thống kê mô tả dạng bảng
# Bảng 1: Thống kê mô tả cho các cột số
numeric_cols = ['Max_Power', 'Memory', 'TMUs']
desc_stats = df[numeric_cols].describe()
desc_stats = desc_stats.round(2)
desc_stats.index = ['Số lượng', 'Trung bình', 'Độ lệch chuẩn', 'Tối thiểu', '25%', '50% (Trung vị)', '75%', 'Tối đa']
print("\nBảng 1: Thống kê mô tả cho các cột số")
print(desc_stats)

# Bảng 2: Phân bố số lượng GPU theo nhà sản xuất
manufacturer_counts = df['Manufacturer'].value_counts().reset_index()
manufacturer_counts.columns = ['Nhà sản xuất', 'Số lượng']
manufacturer_counts['Tỷ lệ (%)'] = (manufacturer_counts['Số lượng'] / manufacturer_counts['Số lượng'].sum() * 100).round(2)
print("\nBảng 2: Phân bố số lượng GPU theo nhà sản xuất")
print(manufacturer_counts)

# 2. Vẽ các đồ thị
# Đồ thị 1: Histogram của Max_Power
plt.figure(figsize=(10, 6))
sns.histplot(df['Max_Power_Scaled'].dropna(), bins=20, kde=True, color='blue')
plt.title('Đồ thị 1: Phân phối công suất tối đa (Max_Power) của GPU', fontsize=14)
plt.xlabel('Công suất tối đa (đã chuẩn hóa)', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)
plt.show()

# Đồ thị 2: Countplot của Release_Year
plt.figure(figsize=(12, 6))
sns.countplot(x='Release_Year', data=df, palette='viridis')
plt.title('Đồ thị 2: Số lượng GPU phát hành theo năm', fontsize=14)
plt.xlabel('Năm phát hành', fontsize=12)
plt.ylabel('Số lượng GPU', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Đồ thị 3: Boxplot của TMUs
plt.figure(figsize=(8, 6))
sns.boxplot(y='TMUs', data=df, color='orange')
plt.title('Đồ thị 3: Phân phối số lượng TMUs của GPU', fontsize=14)
plt.ylabel('Số lượng TMUs', fontsize=12)
plt.show()

# Đồ thị 4: Scatterplot giữa Max_Power và Memory
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Max_Power_Scaled', y='Memory_Scaled', hue='Manufacturer', data=df)
plt.title('Đồ thị 4: Mối quan hệ giữa Công suất tối đa (Max_Power) và Bộ nhớ (Memory)', fontsize=14)
plt.xlabel('Công suất tối đa (đã chuẩn hóa)', fontsize=12)
plt.ylabel('Bộ nhớ (đã chuẩn hóa)', fontsize=12)
plt.show()
