import streamlit as st
import random
from datetime import datetime
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🌱 Smart Irrigation System", layout="wide")

# ------------------ STYLE ------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images8.alphacoders.com/108/1088470.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4CBB17, #2E8B57);
}
* { font-family: 'Poppins', sans-serif; }
.app-header {
    background: linear-gradient(90deg, #6B8E23, #8FBC8F);
    color: #fff;
    padding: 20px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}
.app-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
}
.red-delete-btn > button {
    background-color: #FF0000 !important;
    color: red !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 6px 14px !important;
    font-weight: 600 !important;
    transition: 0.3s !important;
}
.red-delete-btn > button:hover {
    background-color: #b71c1c !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------ SENSOR + AI FUNCTIONS ------------------
def get_sensor_data():
    soil = random.uniform(30, 60)
    temp = random.uniform(25, 35)
    humidity = random.uniform(55, 80)
    water = random.uniform(2000, 4000)
    weather = random.choice(["Sunny", "Cloudy", "Rainy", "Storm"])
    return soil, temp, humidity, water, weather

def predict_water_need(weather, soil, crop_type):
    crop_factor = {"Rice": 70, "Corn": 60, "Vegetables": 55}
    base = crop_factor.get(crop_type, 60)
    if weather == "Rainy": return max(0, base - soil - 10)
    elif weather == "Sunny": return max(0, base - soil + 10)
    elif weather == "Cloudy": return max(0, base - soil)
    else: return 0

def generate_recommendation(water_need):
    if water_need <= 0:
        return "💧 No irrigation needed today. Soil moisture is sufficient."
    elif water_need < 20:
        return "💧 Minimal irrigation needed — monitor soil moisture."
    elif water_need < 40:
        return "💦 Moderate irrigation recommended for optimal growth."
    else:
        return "🚿 High irrigation required! Soil is too dry."

# ------------------ AUTH SYSTEM ------------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "farms" not in st.session_state:
    st.session_state.farms = []
if "harvest_results" not in st.session_state:
    st.session_state.harvest_results = []

def signup():
    st.subheader("Create Account")
    user = st.text_input("Username", key="signup_user")
    pw = st.text_input("Password", type="password", key="signup_pass")
    role = st.selectbox("Role", ["User", "Admin"], key="signup_role")
    if st.button("Sign Up"):
        if user in st.session_state.users:
            st.warning("⚠️ Username already exists.")
        elif user and pw:
            st.session_state.users[user] = {"password": pw, "role": role}
            st.success(f"✅ {role} account created! Please log in.")
        else:
            st.error("❌ Please fill in all fields.")

def login():
    st.subheader("Log In")
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user]["password"] == pw:
            st.session_state.logged_in_user = user
            st.success(f"✅ Welcome, {user}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

def logout():
    st.session_state.logged_in_user = None
    st.success("Logged out successfully!")
    st.rerun()

# ------------------ LOGIN / SIGNUP ------------------
if not st.session_state.logged_in_user:
    auth = st.sidebar.radio("Account Access", ["Login", "Sign Up"])
    login() if auth == "Login" else signup()
    st.stop()

current_user = st.session_state.logged_in_user
role = st.session_state.users[current_user]["role"]

# ------------------ HEADER ------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="app-header"><h1>AI-Powered Smart Irrigation System</h1></div>', unsafe_allow_html=True)
with col2:
    st.button("Logout", on_click=logout, key="logout_btn", use_container_width=True)

# ------------------ ADMIN VIEW ------------------
if role == "Admin":
    st.subheader("Admin Dashboard")

    # USERS TABLE
    st.markdown("### 👥 Registered Users")
    if st.session_state.users:
        df_users = pd.DataFrame([{"Username": u, "Role": d["role"]} for u, d in st.session_state.us
import streamlit as st
import random
from datetime import datetime
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🌱 Smart Irrigation System", layout="wide")

# ------------------ STYLE ------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images8.alphacoders.com/108/1088470.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4CBB17, #2E8B57);
}
* { font-family: 'Poppins', sans-serif; }
.app-header {
    background: linear-gradient(90deg, #6B8E23, #8FBC8F);
    color: #fff;
    padding: 20px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}
.app-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
}
.red-delete-btn > button {
    background-color: #FF0000 !important;
    color: red !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 6px 14px !important;
    font-weight: 600 !important;
    transition: 0.3s !important;
}
.red-delete-btn > button:hover {
    background-color: #b71c1c !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------ SENSOR + AI FUNCTIONS ------------------
def get_sensor_data():
    soil = random.uniform(30, 60)
    temp = random.uniform(25, 35)
    humidity = random.uniform(55, 80)
    water = random.uniform(2000, 4000)
    weather = random.choice(["Sunny", "Cloudy", "Rainy", "Storm"])
    return soil, temp, humidity, water, weather

def predict_water_need(weather, soil, crop_type):
    crop_factor = {"Rice": 70, "Corn": 60, "Vegetables": 55}
    base = crop_factor.get(crop_type, 60)
    if weather == "Rainy": return max(0, base - soil - 10)
    elif weather == "Sunny": return max(0, base - soil + 10)
    elif weather == "Cloudy": return max(0, base - soil)
    else: return 0

def generate_recommendation(water_need):
    if water_need <= 0:
        return "💧 No irrigation needed today. Soil moisture is sufficient."
    elif water_need < 20:
        return "💧 Minimal irrigation needed — monitor soil moisture."
    elif water_need < 40:
        return "💦 Moderate irrigation recommended for optimal growth."
    else:
        return "🚿 High irrigation required! Soil is too dry."

# ------------------ AUTH SYSTEM ------------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "farms" not in st.session_state:
    st.session_state.farms = []
if "harvest_results" not in st.session_state:
    st.session_state.harvest_results = []

def signup():
    st.subheader("Create Account")
    user = st.text_input("Username", key="signup_user")
    pw = st.text_input("Password", type="password", key="signup_pass")
    role = st.selectbox("Role", ["User", "Admin"], key="signup_role")
    if st.button("Sign Up"):
        if user in st.session_state.users:
            st.warning("⚠️ Username already exists.")
        elif user and pw:
            st.session_state.users[user] = {"password": pw, "role": role}
            st.success(f"✅ {role} account created! Please log in.")
        else:
            st.error("❌ Please fill in all fields.")

def login():
    st.subheader("Log In")
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user]["password"] == pw:
            st.session_state.logged_in_user = user
            st.success(f"✅ Welcome, {user}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

def logout():
    st.session_state.logged_in_user = None
    st.success("Logged out successfully!")
    st.rerun()

# ------------------ LOGIN / SIGNUP ------------------
if not st.session_state.logged_in_user:
    auth = st.sidebar.radio("Account Access", ["Login", "Sign Up"])
    login() if auth == "Login" else signup()
    st.stop()

current_user = st.session_state.logged_in_user
role = st.session_state.users[current_user]["role"]

# ------------------ HEADER ------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="app-header"><h1>AI-Powered Smart Irrigation System</h1></div>', unsafe_allow_html=True)
with col2:
    st.button("Logout", on_click=logout, key="logout_btn", use_container_width=True)

# ------------------ ADMIN VIEW ------------------
if role == "Admin":
    st.subheader("Admin Dashboard")

    # USERS TABLE
    st.markdown("### 👥 Registered Users")
    if st.session_state.users:
        df_users = pd.DataFrame([{"Username": u, "Role": d["role"]}]) for u, d in st.session_state.us
