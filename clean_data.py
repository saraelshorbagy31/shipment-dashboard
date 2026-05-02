import pandas as pd

# ✅ قراءة الداتا (اسم الملف الصح)
df = pd.read_csv('data.csv')

# ✅ تحويل التواريخ
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')
df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'], errors='coerce')

# ✅ حذف التكرار
df = df.drop_duplicates()

# ✅ التعامل مع القيم الناقصة
df['Weight_kg'] = df['Weight_kg'].fillna(df['Weight_kg'].median())
df['Cost'] = df['Cost'].fillna(df['Cost'].median())

df['Status'] = df['Status'].fillna('Unknown')
df['Destination'] = df['Destination'].fillna('Unknown')

# ✅ حذف الصفوف اللي فيها تواريخ ناقصة
df = df.dropna(subset=['Ship_Date', 'Delivery_Date'])

# ✅ إنشاء أعمدة جديدة
df['Shipping_Days'] = (df['Delivery_Date'] - df['Ship_Date']).dt.days
df['Cost_per_kg'] = df['Cost'] / df['Weight_kg']
df['Is_Delayed'] = df['Status'].apply(lambda x: 1 if x == 'Delayed' else 0)

# ✅ حفظ الملف بعد التنظيف
df.to_csv('cleaned_shipments.csv', index=False)

print("✅ Data cleaned successfully!")