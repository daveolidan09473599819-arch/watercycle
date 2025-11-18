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
        df_users = pd.DataFrame([{"Username": u, "Role": d["role"]} for u, d in st.session_state.users.items()])
        st.dataframe(df_users, use_container_width=True)
        
        # User management
        st.markdown("### 🛠️ User Management")
        user_to_delete = st.selectbox("Select user to delete", list(st.session_state.users.keys()))
        if st.button("Delete User", type="primary"):
            if user_to_delete == current_user:
                st.error("❌ You cannot delete your own account!")
            else:
                del st.session_state.users[user_to_delete]
                st.success(f"✅ User '{user_to_delete}' deleted successfully!")
                st.rerun()
    else:
        st.info("No users registered yet.")

    # FARM MANAGEMENT
    st.markdown("### 🌾 Farm Management")
    if st.session_state.farms:
        df_farms = pd.DataFrame(st.session_state.farms)
        st.dataframe(df_farms, use_container_width=True)
    else:
        st.info("No farms added yet.")

# ------------------ USER VIEW ------------------
else:
    st.subheader("Farm Dashboard")
    
    # ADD NEW FARM
    with st.form("add_farm"):
        st.markdown("### 🚜 Add New Farm")
        farm_name = st.text_input("Farm Name")
        crop_type = st.selectbox("Crop Type", ["Rice", "Corn", "Vegetables"])
        area = st.number_input("Area (acres)", min_value=0.1, step=0.1)
        
        if st.form_submit_button("Add Farm"):
            if farm_name:
                new_farm = {
                    "user": current_user,
                    "farm_name": farm_name,
                    "crop_type": crop_type,
                    "area": area,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.farms.append(new_farm)
                st.success(f"✅ Farm '{farm_name}' added successfully!")
            else:
                st.error("❌ Please enter a farm name!")

    # DISPLAY USER'S FARMS
    st.markdown("### 🌱 Your Farms")
    user_farms = [farm for farm in st.session_state.farms if farm["user"] == current_user]
    
    if user_farms:
        for i, farm in enumerate(user_farms):
            with st.expander(f"🏠 {farm['farm_name']} - {farm['crop_type']} ({farm['area']} acres)"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Get sensor data
                    soil, temp, humidity, water, weather = get_sensor_data()
                    
                    # Calculate water need
                    water_need = predict_water_need(weather, soil, farm["crop_type"])
                    recommendation = generate_recommendation(water_need)
                    
                    # Display metrics
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.metric("🌡️ Temperature", f"{temp:.1f}°C")
                    with m2:
                        st.metric("💧 Soil Moisture", f"{soil:.1f}%")
                    with m3:
                        st.metric("💨 Humidity", f"{humidity:.1f}%")
                    with m4:
                        st.metric("🌤️ Weather", weather)
                    
                    # Water recommendation
                    st.metric("💦 Water Need", f"{water_need:.1f} L")
                    st.info(recommendation)
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{i}", type="secondary"):
                        st.session_state.farms.pop(i)
                        st.success("Farm deleted!")
                        st.rerun()
                    
                    if st.button("📊 Record Harvest", key=f"harvest_{i}"):
                        harvest_data = {
                            "farm": farm['farm_name'],
                            "crop": farm['crop_type'],
                            "yield_kg": random.randint(100, 1000),
                            "date": datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.harvest_results.append(harvest_data)
                        st.success("Harvest recorded!")
    else:
        st.info("No farms added yet. Add your first farm above!")

    # HARVEST HISTORY
    if st.session_state.harvest_results:
        st.markdown("### 📈 Harvest History")
        user_harvests = [h for h in st.session_state.harvest_results 
                        if any(farm["farm_name"] == h["farm"] and farm["user"] == current_user 
                              for farm in st.session_state.farms)]
        
        if user_harvests:
            df_harvest = pd.DataFrame(user_harvests)
            st.dataframe(df_harvest, use_container_width=True)
        else:
            st.info("No harvest records yet.")

# ------------------ SIDEBAR WEATHER INFO ------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌤️ Current Conditions")
if st.session_state.farms:
    soil, temp, humidity, water, weather = get_sensor_data()
    st.sidebar.metric("Temperature", f"{temp:.1f}°C")
    st.sidebar.metric("Humidity", f"{humidity:.1f}%")
    st.sidebar.metric("Weather", weather)
    st.sidebar.metric("Water Reserve", f"{water:.0f} L")
