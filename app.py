import streamlit as st
import requests

st.set_page_config(page_title="📋 نظام إدارة الأجهزة", layout="wide")
st.title("🧾 نظام إدارة الأجهزة والموظفين")

# 🗂️ أنواع الجداول المتوفرة
TABLES = {
    "جدول الموظفين": "employee",
    "الأجهزة الجديدة": "new-device",
    "الأجهزة القديمة": "old-device",
    "الأجهزة المحالة للشطب": "scrap-device",
    "الطابعات وأجهزة التوقيع الإلكتروني": "printer-signature",
    "اللابتوب": "laptop-device"
}

# 🔗 رابط Google Apps Script Web App الخاص بك
BASE_URL = "https://script.google.com/macros/s/AKfycbzxMhNY5gMb6e5SXDhyiKlwxHVvDfsdLn3SMhSzIMphrgVPnl81ScWbeyu2NPCJkVeE/exec"

# ⬇️ اختيار الجدول من الواجهة
selected_label = st.selectbox("اختر الجدول", list(TABLES.keys()))
selected_type = TABLES[selected_label]

# 🧲 جلب البيانات من Google Apps Script
@st.cache_data(ttl=60)
def fetch_data(table_type):
    try:
        response = requests.get(f"{BASE_URL}?type={table_type}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
        return []

# 📦 عرض البيانات
data = fetch_data(selected_type)

st.subheader(f"📋 عرض البيانات - {selected_label}")
if data:
    st.success(f"تم تحميل {len(data)} سجل.")
    st.dataframe(data, use_container_width=True)
else:
    st.warning("لا توجد بيانات متاحة حاليًا.")
