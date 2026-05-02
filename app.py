import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Shipment Dashboard", layout="wide")

# تحميل البيانات
df = pd.read_csv('cleaned_shipments.csv')

# تجهيز البيانات
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])

# Sidebar Filters
st.sidebar.header("🔎 Filters")
status = st.sidebar.multiselect("Status", df['Status'].unique(), default=df['Status'].unique())
destination = st.sidebar.multiselect("Destination", df['Destination'].unique(), default=df['Destination'].unique())

df_filtered = df[(df['Status'].isin(status)) & (df['Destination'].isin(destination))]

# Title
st.title("🚚 Shipment Performance Dashboard")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Shipments", len(df_filtered))
col2.metric("Avg Shipping Days", round(df_filtered['Shipping_Days'].mean(),2))
col3.metric("Delay %", round(df_filtered['Is_Delayed'].mean()*100,2))
col4.metric("Total Cost", round(df_filtered['Cost'].sum(),2))

# Alert
if df_filtered['Is_Delayed'].mean() > 0.2:
    st.warning("⚠️ High Delay Rate Detected!")

# Charts
colA, colB = st.columns(2)

with colA:
    fig1 = px.bar(df_filtered, x='Status', title="Shipments by Status")
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    fig2 = px.pie(df_filtered, names='Destination', title="Destination Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# Trend
fig3 = px.line(df_filtered, x='Ship_Date', y='Cost', title="Cost Over Time")
st.plotly_chart(fig3, use_container_width=True)

# Delay Analysis
st.subheader("🚨 Delay Analysis")
delay_dest = df[df['Is_Delayed']==1]['Destination'].value_counts()
st.bar_chart(delay_dest)

# Cost Analysis
st.subheader("💰 Cost Analysis")
route_cost = df.groupby(['Origin','Destination'])['Cost_per_kg'].mean().reset_index()
top_routes = route_cost.sort_values(by='Cost_per_kg', ascending=False).head(10)
st.dataframe(top_routes)
# /////////////////////////////////////////



    # /////////////////////////////////////////////////////////////////////////////
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

st.subheader("🤖 Delay Prediction")

# تجهيز البيانات
df_ml = df.copy()

# ❌ احذف الأعمدة اللي تسبب leakage + التواريخ
df_ml = df_ml.drop(columns=['Status','Ship_Date','Delivery_Date','Shipment_ID','Order_ID'], errors='ignore')

# ✅ تحويل النصوص لأرقام
df_ml = pd.get_dummies(df_ml, drop_first=True)

# تقسيم البيانات
X = df_ml.drop(['Is_Delayed'], axis=1)
y = df_ml['Is_Delayed']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# تدريب
model = RandomForestClassifier()
model.fit(X_train, y_train)

# تقييم
accuracy = model.score(X_test, y_test)

st.metric("Model Accuracy", f"{round(accuracy*100,2)}%")
st.success("Model trained successfully ✅")
# ظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظظ
# =========================
# MAP
# =========================
st.subheader("🌍 Shipments Map")

city_coords = {
    "Cairo": [30.0444, 31.2357],
    "New York": [40.7128, -74.0060],
    "London": [51.5074, -0.1278],
    "Paris": [48.8566, 2.3522],
    "Dubai": [25.2048, 55.2708],
    "Mumbai": [19.0760, 72.8777],
    "Toronto": [43.65107, -79.347015],
    "Sydney": [-33.8688, 151.2093],
    "Los Angeles": [34.0522, -118.2437]
}

df_map = df.copy()
df_map['lat'] = df_map['Origin'].map(lambda x: city_coords.get(x, [None,None])[0])
df_map['lon'] = df_map['Origin'].map(lambda x: city_coords.get(x, [None,None])[1])

df_map = df_map.dropna(subset=['lat','lon'])

st.map(df_map[['lat','lon']])



# شششششششششششششششششششششششششششششششششششششششششش
# =========================
# USER INPUT PREDICTION
# =========================
st.subheader("🧠 Predict New Shipment")

# اختيارات المستخدم
origin_input = st.selectbox("Select Origin", df['Origin'].unique())
destination_input = st.selectbox("Select Destination", df['Destination'].unique())
weight_input = st.number_input("Enter Weight (kg)", min_value=1.0)

# زرار التوقع
if st.button("Predict Delay"):

    # إنشاء DataFrame من المدخلات
    input_df = pd.DataFrame({
        'Weight_kg': [weight_input],
        'Origin': [origin_input],
        'Destination': [destination_input]
    })

    # تحويله لنفس شكل الداتا
    input_df = pd.get_dummies(input_df)

    # 🔥 أهم خطوة: مطابقة الأعمدة مع التدريب
    input_df = input_df.reindex(columns=X.columns, fill_value=0)

    # التوقع
    prediction = model.predict(input_df)[0]

    # عرض النتيجة
    if prediction == 1:
        st.error("🚨 Shipment will be Delayed")
    else:
        st.success("✅ Shipment will be On Time")

        st.info("Use filters on the left to explore shipment data. Scroll down for prediction.")