import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu (giả sử đã tiền xử lý từ bước trước)
df = pd.read_csv('All_GPUs.csv')

# Tiền xử lý dữ liệu (lặp lại để đảm bảo)
def clean_numeric_column(value):
    if pd.isna(value):
        return value
    try:
        value = str(value).replace('Watts', '').replace('W', '').replace('MB', '').replace('GB', '').replace('MHz', '').replace('\n-', '').replace(' ', '').strip()
        return float(value) if value else None
    except (ValueError, TypeError):
        return None

cols_to_clean = ['Max_Power', 'Memory', 'TMUs']
for col in cols_to_clean:
    if col in df.columns:
        df[col] = df[col].apply(clean_numeric_column)
        median_value = df[col].median()
        if pd.isna(median_value):
            print(f"Cảnh báo: Trung vị của {col} là NaN, không thể điền giá trị khuyết.")
        else:
            df[col] = df[col].fillna(median_value)

df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
df['Release_Year'] = df['Release_Date'].dt.year

# Chuẩn hóa dữ liệu
max_power_min = df['Max_Power'].min()
max_power_max = df['Max_Power'].max()
memory_min = df['Memory'].min()
memory_max = df['Memory'].max()

df['Max_Power_Scaled'] = (df['Max_Power'] - max_power_min) / (max_power_max - max_power_min)
df['Memory_Scaled'] = (df['Memory'] - memory_min) / (memory_max - memory_min)

# Phương pháp 1: t-test
nvidia_power = df[df['Manufacturer'] == 'Nvidia']['Max_Power'].dropna()
amd_power = df[df['Manufacturer'] == 'AMD']['Max_Power'].dropna()
t_stat, p_value = stats.ttest_ind(nvidia_power, amd_power, equal_var=False)
print(f"\nPhương pháp 1: Kiểm định t-test")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Phương pháp 2: Hồi quy tuyến tính
X = df['Memory']
y = df['Max_Power']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print("\nPhương pháp 2: Hồi quy tuyến tính")
print(model.summary())